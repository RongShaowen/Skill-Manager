"""System language detection and UI string translations."""

import ctypes
import locale
from utils.logger import get_logger

_log = get_logger("i18n")


def _detect_lang() -> str:
    """Detect system UI language."""
    try:
        lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage() & 0x3FF
        # 0x04 = zh (Chinese), 0x09 = en (English)
        if lang_id == 0x04:
            return "zh"
    except Exception as e:
        _log.debug("Cannot detect language via WinAPI: %s", e)
    try:
        loc = locale.getdefaultlocale()[0] or ""
        if loc.startswith("zh"):
            return "zh"
    except Exception as e:
        _log.debug("Cannot detect language via locale: %s", e)
    return "en"


LANG = _detect_lang()

STRINGS = {
    "zh": {
        "app_title": "Skill Manager - MiMoCode 技能管理器",
        "search_placeholder": "搜索技能...",
        "all": "全部",
        "builtin": "内置",
        "compose": "组合",
        "claude": "Claude",
        "agent": "Agent",
        "user": "用户",
        "codex": "Codex",
        "trae": "Trae",
        "cursor": "Cursor",
        "windsurf": "Windsurf",
        "continue": "Continue",
        "aider": "Aider",
        "mcp": "MCP",
        "github_copilot": "Copilot",
        "cline": "Cline",
        "discovered": "已发现",
        "stats_total": "总计",
        "btn_download": "下载技能",
        "btn_delete": "删除",
        "btn_open_dir": "打开目录",
        "btn_marketplace": "技能市场",
        "detail_name": "名称",
        "detail_source": "来源",
        "detail_path": "路径",
        "detail_desc": "描述",
        "detail_version": "版本",
        "detail_files": "文件",
        "detail_size": "大小",
        "detail_readonly": "内置技能，不可删除",
        "app_subtitle": "MiMoCode 技能管理",
        "filter_label": "来源筛选",
        "stats_label": "统计",
        "btn_cancel": "取消",
        "btn_refresh": "刷新",
        "download_enter_url": "请输入 URL",
        "download_title": "下载技能",
        "download_url_label": "GitHub 仓库 URL 或 .zip 下载链接",
        "download_url_placeholder": "https://github.com/user/repo",
        "download_btn": "下载并安装",
        "download_success": "技能下载成功！",
        "download_fail": "下载失败",
        "download_validating": "正在验证...",
        "download_downloading": "正在下载...",
        "download_installing": "正在安装...",
        "delete_confirm": "确认删除",
        "delete_msg": "确定要删除技能 \"{name}\" 吗？\n\n路径: {path}\n\n此操作不可撤销。",
        "delete_success": "技能已删除",
        "delete_fail": "删除失败",
        "marketplace_title": "技能市场",
        "marketplace_install": "安装",
        "marketplace_installed": "已安装",
        "marketplace_loading": "正在加载市场...",
        "marketplace_error": "市场加载失败",
        "no_skills": "没有找到技能",
        "files_count": "{n} 个文件/目录",
        "source_legend": "来源标识",
        "cross_platform": "跨平台",
        "native": "平台专属",
        "installed": "用户安装",
        "filter_cross_platform": "跨平台",
        "filter_native": "平台专属",
        "filter_installed": "用户安装",
        "detail_cn_desc": "中文描述",
        "detail_en_desc": "英文描述",
        "btn_sync": "同步到其他平台",
        "sync_title": "同步技能",
        "sync_msg": "将技能 \"{name}\" 同步到以下平台：",
        "sync_success": "同步完成",
        "sync_fail": "同步失败",
    },
    "en": {
        "app_title": "Skill Manager - MiMoCode Skill Manager",
        "search_placeholder": "Search skills...",
        "all": "All",
        "builtin": "Built-in",
        "compose": "Compose",
        "claude": "Claude",
        "agent": "Agent",
        "user": "User",
        "codex": "Codex",
        "trae": "Trae",
        "cursor": "Cursor",
        "windsurf": "Windsurf",
        "continue": "Continue",
        "aider": "Aider",
        "mcp": "MCP",
        "github_copilot": "Copilot",
        "cline": "Cline",
        "discovered": "Discovered",
        "stats_total": "Total",
        "btn_download": "Download",
        "btn_delete": "Delete",
        "btn_open_dir": "Open Folder",
        "btn_marketplace": "Marketplace",
        "detail_name": "Name",
        "detail_source": "Source",
        "detail_path": "Path",
        "detail_desc": "Description",
        "detail_version": "Version",
        "detail_files": "Files",
        "detail_size": "Size",
        "detail_readonly": "Built-in skill, cannot be deleted",
        "app_subtitle": "MiMoCode Skill Manager",
        "filter_label": "Source Filter",
        "stats_label": "Statistics",
        "btn_cancel": "Cancel",
        "btn_refresh": "Refresh",
        "download_enter_url": "Please enter a URL",
        "download_title": "Download Skill",
        "download_url_label": "GitHub repo URL or .zip download link",
        "download_url_placeholder": "https://github.com/user/repo",
        "download_btn": "Download & Install",
        "download_success": "Skill downloaded successfully!",
        "download_fail": "Download failed",
        "download_validating": "Validating...",
        "download_downloading": "Downloading...",
        "download_installing": "Installing...",
        "delete_confirm": "Confirm Delete",
        "delete_msg": 'Are you sure you want to delete skill "{name}"?\n\nPath: {path}\n\nThis action cannot be undone.',
        "delete_success": "Skill deleted",
        "delete_fail": "Delete failed",
        "marketplace_title": "Skill Marketplace",
        "marketplace_install": "Install",
        "marketplace_installed": "Installed",
        "marketplace_loading": "Loading marketplace...",
        "marketplace_error": "Failed to load marketplace",
        "no_skills": "No skills found",
        "files_count": "{n} files/dirs",
        "source_legend": "Source Legend",
        "cross_platform": "Cross-platform",
        "native": "Native",
        "installed": "Installed",
        "filter_cross_platform": "Cross-platform",
        "filter_native": "Native",
        "filter_installed": "Installed",
        "detail_cn_desc": "Chinese Desc",
        "detail_en_desc": "English Desc",
        "btn_sync": "Sync to Other Platforms",
        "sync_title": "Sync Skill",
        "sync_msg": 'Sync skill "{name}" to:',
        "sync_success": "Sync complete",
        "sync_fail": "Sync failed",
    },
}


def t(key: str, **kwargs) -> str:
    """Translate a key using the detected language."""
    s = STRINGS.get(LANG, STRINGS["en"]).get(key, key)
    if kwargs:
        return s.format(**kwargs)
    return s
