"""Skill directory scanning and SKILL.md parsing."""

import os
import re
from dataclasses import dataclass, field

import yaml

from utils.paths import find_skill_dirs, skill_dir_size, format_size
from utils.logger import get_logger

_log = get_logger("scanner")


# ── Chinese translation map for common English descriptions ────
_CN_MAP = {
    "deep research": "深度研究：并行子代理多源调研",
    "arxiv": "学术论文：搜索、阅读、引用 arXiv 论文",
    "design blueprint": "设计蓝图：视觉产出的结构化设计规范",
    "docx": "Word文档：创建、编辑、读取 .docx 文件",
    "drive mimo": "MiMo驱动：程序化驱动另一个MiMoCode进程",
    "evolve": "自我进化：修改自身能力和行为",
    "frontend design": "前端设计：UI/UX 视觉设计指导",
    "html-to-video": "HTML转视频：无头浏览器录制+ffmpeg渲染",
    "loop": "循环调度：定时重复执行提示词",
    "mimocode": "MiMoCode：MiMoCode自身的参考文档",
    "modern python": "现代Python：uv/ruff/pyright项目搭建",
    "pdf official": "PDF工具：创建、编辑、读取、转换PDF",
    "pptx official": "PPT工具：创建、编辑、读取PowerPoint",
    "research paper": "学术论文：撰写、润色、引用校验ML/CV论文",
    "skill creator": "技能创建：交互式创建和验证技能",
    "super research": "自主研究：实验循环、调研、分析、评测",
    "xlsx official": "Excel工具：创建、编辑、分析电子表格",
    "novel continuation": "小说续写：基于大纲自动续写章节",
    "pm game build": "PM养成记：游戏构建工作流",
    "python encoding fix": "Python编码修复：Windows UTF-8兼容",
    "lark approval": "飞书审批：查询处理审批待办",
    "lark apps": "妙搭应用：HTML站点发布和托管",
    "lark attendance": "飞书考勤：查询打卡记录",
    "lark base": "飞书多维表格：建表、字段、记录操作",
    "lark calendar": "飞书日历：管理日程和会议室",
    "lark contact": "飞书通讯录：姓名/邮箱/ID查询",
    "lark doc": "飞书文档：读取和编辑云文档",
    "lark drive": "飞书云盘：文件上传下载管理",
    "lark event": "飞书事件：实时事件监听订阅",
    "lark im": "飞书通讯：收发消息管理群聊",
    "lark mail": "飞书邮箱：邮件收发管理",
    "lark markdown": "飞书Markdown：创建编辑Markdown文件",
    "lark minutes": "飞书妙记：搜索查看会议纪要",
    "lark note": "飞书纪要：查询会议纪要详情",
    "lark okr": "飞书OKR：管理目标与关键结果",
    "lark openapi": "飞书API：探索原生OpenAPI接口",
    "lark shared": "飞书认证：授权登录状态管理",
    "lark sheets": "飞书表格：创建操作电子表格",
    "lark skill maker": "技能制作：创建lark-cli自定义Skill",
    "lark slides": "飞书幻灯片：创建编辑演示文稿",
    "lark task": "飞书任务：管理待办和任务清单",
    "lark vc": "飞书会议：搜索历史会议记录",
    "lark vc agent": "飞书会中：加入/离开进行中会议",
    "lark whiteboard": "飞书画板：查询编辑飞书画板",
    "lark wiki": "飞书知识库：管理知识空间文档",
    "dashiai ppt": "DashiAI PPT：基于主题的HTML演示生成",
    "playwright cli": "Playwright：浏览器自动化测试",
    "playwright trace": "Playwright追踪：检查trace文件",
}


def _translate_desc(name: str, desc: str) -> str:
    """Provide Chinese translation for English descriptions."""
    import re
    name_lower = name.lower().strip()
    desc_lower = desc.lower().strip()

    # Try exact name match first (most reliable)
    if name_lower in _CN_MAP:
        return _CN_MAP[name_lower]

    # Try name prefix match (e.g. "lark-im" starts with "lark im")
    name_normalized = name_lower.replace("-", " ").replace("_", " ")
    for key, cn in _CN_MAP.items():
        if name_normalized == key or name_normalized.startswith(key):
            return cn

    # Try description word-boundary match (avoid substring false positives)
    for key, cn in _CN_MAP.items():
        pattern = r'\b' + re.escape(key) + r'\b'
        if re.search(pattern, desc_lower):
            return cn

    # If already contains Chinese, return as-is
    if any("\u4e00" <= c <= "\u9fff" for c in desc):
        return desc

    # Generic fallback for English-only descriptions
    if len(desc) > 20:
        return desc[:60] + "..." if len(desc) > 60 else desc
    return desc


@dataclass
class SkillInfo:
    name: str
    description: str
    source: str
    path: str
    version: str = "-"
    license_: str = ""
    platforms: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    size: str = "0 B"
    raw_files: list[str] = field(default_factory=list)
    category: str = "cross_platform"  # cross_platform / native / installed
    cn_description: str = ""  # Chinese translation of description

    @property
    def is_readonly(self) -> bool:
        return self.source in ("builtin", "compose")

    @property
    def category_label(self) -> str:
        labels = {
            "cross_platform": "跨平台",
            "native": "平台专属",
            "installed": "用户安装",
        }
        return labels.get(self.category, self.category)


_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _classify_skill(source: str, platforms: list[str]) -> str:
    """Classify a skill's category based on source and platforms."""
    # Preset platform sources: MiMoCode builtin (cross-platform or native)
    if source == "builtin":
        return "native" if (platforms and len(platforms) <= 2) else "cross_platform"
    # All user-installed / discovered / third-party sources
    if source in ("user", "installed", "discovered", "compose",
                  "claude", "agent", "codex", "trae", "cursor",
                  "windsurf", "continue", "aider", "mcp",
                  "github_copilot", "cline"):
        return "installed"
    # Fallback for any future source
    return "installed"


def parse_skill_md(skill_dir: str) -> SkillInfo | None:
    """Parse SKILL.md frontmatter and return SkillInfo, or None on failure."""
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return None

    try:
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read(8192)  # Read first 8KB for frontmatter
    except Exception as e:
        _log.warning("Cannot read %s: %s", skill_md, e)
        return None

    m = _FRONT_MATTER_RE.match(content)
    if not m:
        return None

    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except Exception as e:
        _log.warning("Cannot parse YAML in %s: %s", skill_md, e)
        return None

    name = meta.get("name", os.path.basename(skill_dir))
    description = meta.get("description", "")
    version = str(meta.get("version", "-"))
    license_ = meta.get("license", "")
    platforms = meta.get("platforms", [])

    # List immediate children
    files = []
    try:
        for entry in sorted(os.listdir(skill_dir)):
            full = os.path.join(skill_dir, entry)
            if os.path.isdir(full):
                files.append(f"{entry}/")
            else:
                files.append(entry)
    except Exception as e:
        _log.warning("Cannot list dir %s: %s", skill_dir, e)

    size = format_size(skill_dir_size(skill_dir))

    return SkillInfo(
        name=name,
        description=description,
        source="",
        path=skill_dir,
        version=version,
        license_=license_,
        platforms=platforms if isinstance(platforms, list) else [],
        files=files,
        raw_files=files,
        size=size,
        category="installed",  # placeholder; corrected in scan_all_skills()
        cn_description=_translate_desc(name, description),
    )


def scan_all_skills() -> list[SkillInfo]:
    """Scan all skill sources and return a list of SkillInfo."""
    skills = []
    for source, skill_dir in find_skill_dirs():
        info = parse_skill_md(skill_dir)
        if info:
            info.source = source
            info.category = _classify_skill(source, info.platforms)
            skills.append(info)
    return skills
