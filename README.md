# Skill Manager — MiMoCode 技能管理器

> **版本**: v1.4.1  
> **平台**: Windows 10/11 (64-bit)  
> **许可证**: MIT

---

## 目录

1. [简介](#1-简介)
2. [功能特性](#2-功能特性)
3. [系统要求](#3-系统要求)
4. [安装方法](#4-安装方法)
   - 4.1 [方式一：运行 .exe 安装包（推荐）](#41-方式一运行-exe-安装包推荐)
   - 4.2 [方式二：直接运行 .exe](#42-方式二直接运行-exe)
   - 4.3 [方式三：从源码运行](#43-方式三从源码运行)
5. [卸载方法](#5-卸载方法)
6. [使用指南](#6-使用指南)
   - 6.1 [启动程序](#61-启动程序)
   - 6.2 [主界面概览](#62-主界面概览)
   - 6.3 [浏览技能列表](#63-浏览技能列表)
   - 6.4 [查看技能详情](#64-查看技能详情)
   - 6.5 [搜索技能](#65-搜索技能)
   - 6.6 [按来源筛选](#66-按来源筛选)
   - 6.7 [删除技能](#67-删除技能)
   - 6.8 [下载技能（URL 方式）](#68-下载技能url-方式)
   - 6.9 [技能市场](#69-技能市场)
   - 6.10 [打开技能目录](#610-打开技能目录)
7. [技能来源说明](#7-技能来源说明)
8. [安全机制](#8-安全机制)
9. [项目结构](#9-项目结构)
10. [从源码构建](#10-从源码构建)
11. [常见问题](#11-常见问题)
12. [技术栈](#12-技术栈)
13. [更新日志](#13-更新日志)

---

## 1. 简介

**Skill Manager** 是一款专为 MiMoCode 用户设计的桌面端技能管理工具。它能够自动扫描、展示、管理和下载本地的 MiMoCode Skills，提供直观的图形化界面，无需任何命令行操作。

MiMoCode Skills 是 MiMoCode 智能体的功能扩展模块，每个 Skill 都是一个包含 `SKILL.md` 描述文件的目录，定义了智能体在特定场景下的行为和能力。

---

## 2. 功能特性

| 功能 | 说明 |
|------|------|
| **自动扫描** | 三层扫描策略：15+ 预设平台 + 全局递归搜索 + 用户自定义路径 |
| **卡片式展示** | 以卡片网格形式展示每个技能的名称、来源、描述 |
| **详情面板** | 点击卡片查看完整信息：名称、来源、路径、版本、大小、描述、文件列表 |
| **搜索过滤** | 支持按名称和描述实时搜索过滤（300ms 防抖） |
| **来源筛选** | 左侧栏按来源快速筛选，图例仅显示实际存在的来源 |
| **统计概览** | 实时显示各来源的技能数量统计 |
| **删除技能** | 一键删除用户自定义技能（内置技能设为只读保护） |
| **URL 下载** | 通过 GitHub 仓库 URL 或 .zip 下载链接安装新技能 |
| **安全防护** | HTTPS 强制、Zip Slip 防护、Zip Bomb 检测、下载大小限制 |
| **多语言** | 自动检测系统语言，支持中文/英文界面 |
| **科技风 UI** | 深色主题，蓝/金/绿配色，现代科技风格 |

---

## 3. 系统要求

| 项目 | 要求 |
|------|------|
| 操作系统 | Windows 10 (1809+) / Windows 11 |
| 架构 | 64-bit (x64) |
| 磁盘空间 | 约 50 MB（.exe 文件约 35 MB） |
| 网络 | 下载/市场功能需要互联网连接 |
| 权限 | 普通用户权限即可运行 |

---

## 4. 安装方法

### 4.1 方式一：运行 .exe 安装包（推荐）

1. 获取 `SkillManager-Setup-1.0.0.exe` 安装包
2. 双击运行安装程序
3. 按照向导操作：
   - 选择安装语言（中文/英文）
   - 选择安装目录（默认：`C:\Program Files\Skill Manager`）
   - 选择是否创建桌面快捷方式
4. 点击「安装」完成
5. 安装完成后可选择立即启动

**安装包特性**：
- 支持中文/英文安装界面
- 自动在 Windows 控制面板注册，可便捷卸载
- 支持静默安装：`SkillManager-Setup-1.0.0.exe /SILENT`

### 4.2 方式二：直接运行 .exe

1. 获取 `dist/SkillManager.exe`
2. 双击运行即可，无需安装
3. 建议将 .exe 放在固定目录（如桌面或文档目录）

### 4.3 方式三：从源码运行

#### 前置条件

- Python 3.10 或更高版本
- pip 包管理器

#### 步骤

```bash
# 1. 进入项目目录
cd skill_manager

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行程序
python main.py
```

或直接双击 `run.bat` 文件。

---

## 5. 卸载方法

### 方式一：通过控制面板

1. 打开 **设置** → **应用** → **已安装的应用**
2. 搜索「Skill Manager」
3. 点击 **卸载**

或通过传统控制面板：

1. 打开 **控制面板** → **程序和功能**
2. 找到「Skill Manager」
3. 右键选择 **卸载**

### 方式二：删除文件

如果使用的是直接运行 .exe 方式：

1. 删除 `SkillManager.exe` 文件
2. 删除整个 `skill_manager` 文件夹（如果不再需要源码）

**注意**：卸载程序不会删除已安装的 Skills，它们仍在原目录中。

---

## 6. 使用指南

### 6.1 启动程序

- **安装版**：从开始菜单或桌面快捷方式启动
- **免安装版**：双击 `SkillManager.exe`
- **源码版**：运行 `python main.py` 或双击 `run.bat`

启动后程序会自动扫描本地所有 Skills 并展示在主界面中。

### 6.2 主界面概览

```
┌─────────────────────────────────────────────────────────────┐
│  ◆ SKILL MANAGER                              [_] [□] [×] │
├──────────┬──────────────────────────────────────────────────┤
│          │  🔍 搜索技能...                                  │
│  侧边栏  │──────────────────────────────────────────────────│
│          │                                                  │
│ ▸ 全部   │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│   (118)  │  │ Skill 1  │ │ Skill 2  │ │ Skill 3  │        │
│          │  │ desc...  │ │ desc...  │ │ desc...  │        │
│ ▸ 内置   │  │ BUILTIN  │ │ AGENT    │ │ USER     │        │
│   (16)   │  └──────────┘ └──────────┘ └──────────┘        │
│          │                                                  │
│ ▸ 组合   │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│   (44)   │  │ Skill 4  │ │ Skill 5  │ │ Skill 6  │        │
│          │  │ ...      │ │ ...      │ │ ...      │        │
│ ▸ Claude │  └──────────┘ └──────────┘ └──────────┘        │
│   (28)   │                                                  │
│          │──────────────────────────────────────────────────│
│ ▸ Agent  │  [下载技能]  [技能市场]                            │
│   (27)   │──────────────────────────────────────────────────│
│          │  名称: deep-research                              │
│ ▸ 用户   │  来源: BUILTIN                                   │
│   (3)    │  路径: C:\Users\...\skills\deep-research\        │
│          │  描述: Deep research on any topic...              │
│──────────│  文件: SKILL.md, reference/, scripts/             │
│ 统计     │                                                  │
│ 总计 118 │  [打开目录]  [删除]                                │
│ 内置  16 │                                                  │
│ 组合  44 │                                                  │
│ Claude 28│                                                  │
│ Agent  27│                                                  │
│ 用户   3 │                                                  │
└──────────┴──────────────────────────────────────────────────┘
```

界面分为三个区域：

| 区域 | 位置 | 功能 |
|------|------|------|
| **侧边栏** | 左侧 (220px) | 来源筛选按钮、技能数量统计 |
| **技能网格** | 中间（主区域） | 卡片式技能列表，支持滚动 |
| **详情面板** | 右侧 (340px) | 选中技能的完整信息和操作按钮 |

### 6.3 浏览技能列表

- 启动后自动扫描并展示所有本地技能
- 每个技能以卡片形式显示：来源标签、名称、描述摘要
- 滚动鼠标或拖动滚动条浏览更多技能
- 卡片数量实时显示在搜索栏右侧（如 `28 / 118`）

### 6.4 查看技能详情

1. 在技能网格中**点击**任意技能卡片
2. 右侧详情面板会显示该技能的完整信息：
   - **名称**：技能的唯一标识符（kebab-case）
   - **来源**：技能所属的来源目录（带颜色标识）
   - **路径**：技能在磁盘上的完整路径
   - **版本**：语义化版本号（如有）
   - **大小**：技能目录的总大小
   - **描述**：技能的功能和使用场景说明
   - **文件**：技能目录下的文件和子目录列表

### 6.5 搜索技能

1. 在顶部搜索框中输入关键词
2. 列表会**实时过滤**，仅显示名称或描述中包含关键词的技能
3. 搜索不区分大小写
4. 清空搜索框恢复显示全部技能

**搜索示例**：
- 输入 `lark` → 显示所有飞书相关技能
- 输入 `research` → 显示研究类技能
- 输入 `pdf` → 显示 PDF 处理相关技能

### 6.6 按来源筛选

左侧边栏提供来源筛选按钮：

| 按钮 | 筛选内容 |
|------|---------|
| **全部** | 显示所有来源的技能 |
| **内置** | MiMoCode 自带的内置技能 |
| **组合** | Compose 模式的组合技能 |
| **Claude** | Claude Code 平台技能 |
| **Agent** | Agent/Lark 集成技能 |
| **用户** | 用户自创建的技能 |

- 点击按钮高亮选中，再次点击其他按钮切换
- 筛选可与搜索配合使用

### 6.7 删除技能

> ⚠️ **注意**：删除操作不可撤销！

1. 在技能列表中点击要删除的技能
2. 在右侧详情面板底部点击红色 **「删除」** 按钮
3. 在确认对话框中点击 **「是」** 确认删除
4. 技能目录将被永久删除

**内置技能保护**：
- 「内置」和「组合」来源的技能设为**只读**
- 选择内置技能时，删除按钮会被替换为提示文字「内置技能，不可删除」
- 用户技能（来源为「用户」）和 Claude/Agent 技能可以自由删除

### 6.8 下载技能（URL 方式）

1. 点击顶部的绿色 **「下载技能」** 按钮
2. 在弹出的对话框中输入下载地址：
   - **GitHub 仓库 URL**：如 `https://github.com/user/repo`
   - **直接 .zip 下载链接**：如 `https://example.com/skill.zip`
3. 点击 **「下载并安装」** 按钮
4. 等待下载和安装完成
5. 新技能会自动出现在列表中

**下载流程**：
```
输入 URL → 验证 HTTPS → 下载 → 校验 zip → 查找 SKILL.md → 解压安装
```

**安全限制**：
- 仅支持 HTTPS 协议
- 下载文件大小限制 50MB
- 自动校验 SKILL.md 存在性

### 6.9 技能市场

1. 点击顶部的金色 **「技能市场」** 按钮
2. 切换到市场浏览界面
3. 浏览社区贡献的技能列表
4. 点击 **「安装」** 按钮一键安装
5. 已安装的技能会显示 **「已安装」** 状态

**市场功能**：
- 从远程 JSON 配置文件加载技能列表
- 显示技能名称、描述、分类、作者
- 自动检测已安装状态
- 支持刷新重新加载

**切换回本地视图**：
- 再次点击「技能市场」按钮
- 或点击左侧来源筛选按钮

### 6.10 打开技能目录

1. 在技能列表中点击要查看的技能
2. 在右侧详情面板底部点击蓝色 **「打开目录」** 按钮
3. Windows 资源管理器会打开该技能的目录

---

## 7. 技能来源说明

程序采用**三层扫描策略**自动发现技能：

### 第一层：15+ 预设平台路径

| 来源 | 路径 | 说明 | 可删除 |
|------|------|------|--------|
| **内置** | `~/.local/share/mimocode/builtin_skills/*/skills/*` | MiMoCode 自带的内置技能 | ❌ |
| **组合** | `~/.local/share/mimocode/compose/*/skills/*` | Compose 模式的组合编排技能 | ❌ |
| **Claude** | `~/.claude/skills/*` | Claude Code 平台技能 | ✅ |
| **Agent** | `~/.agents/skills/*` | Agent/Lark 集成技能 | ✅ |
| **用户** | `~/.mimocode/skills/*` | 用户自创建的技能 | ✅ |
| **OpenAI Codex** | `~/.codex/skills/*` | OpenAI Codex 平台技能 | ✅ |
| **Cursor** | `~/.cursor/skills/*` | Cursor IDE 技能 | ✅ |
| **Trae** | `~/.trae/skills/*` | Trae IDE 技能 | ✅ |
| **Windsurf** | `~/.windsurf/skills/*` | Windsurf IDE 技能 | ✅ |
| **Continue** | `~/.continue/skills/*` | Continue 插件技能 | ✅ |
| **Aider** | `~/.aider/skills/*` | Aider 辅助编程技能 | ✅ |
| **MCP** | `~/.mcp/skills/*` | MCP 协议技能 | ✅ |
| **GitHub Copilot** | `~/.github-copilot/skills/*` | Copilot 技能 | ✅ |
| **Cline** | `~/.cline/skills/*` | Cline 插件技能 | ✅ |
| **其他** | 其他已知平台路径... | 持续扩充中 | ✅ |

### 第二层：全局递归搜索

在 `~` 目录下递归搜索所有包含 `SKILL.md` 的目录（最大深度 4 层），自动识别未知平台的技能。

### 第三层：用户自定义路径

通过 `~/.skill_manager/config.json` 添加自定义扫描路径，格式：
```json
{
  "custom_sources": [
    {"name": "my-custom", "path": "D:/my-skills"}
  ]
}
```

**技能目录结构**：
```
skill-name/
├── SKILL.md          # 必需：技能定义文件（YAML 前置元数据 + Markdown 正文）
├── references/       # 可选：参考文档
├── scripts/          # 可选：可执行脚本
├── assets/           # 可选：静态资源
└── ...
```

**SKILL.md 格式**：
```yaml
---
name: my-skill
description: 技能的功能描述和使用场景
version: 1.0.0
license: MIT
platforms:
  - windows
  - linux
  - macos
---

# 技能标题

技能的详细使用说明...
```

---

## 8. 安全机制

| 安全措施 | 实现方式 |
|---------|---------|
| **HTTPS 强制** | 下载仅允许 `https://` 协议，拒绝 HTTP/FTP 等 |
| **SSL 证书验证** | 使用 `requests` 库的默认证书验证 |
| **Zip Slip 防护** | 解压时校验 `realpath()` 前缀，拒绝路径穿越攻击 |
| **Zip Bomb 检测** | 预检查压缩包总解压大小，超过 500MB 自动拒绝 |
| **流式下载** | 大文件使用 `tempfile.mkstemp()` + `iter_content()` 流式写入，不占用内存 |
| **原子同步** | 技能同步先写入临时目录，再用 `os.replace()` 原子替换，避免中断导致数据损坏 |
| **下载大小限制** | 单次下载上限 50MB |
| **输入验证** | URL 和文件名均经过格式校验 |
| **无代码执行** | 下载内容不执行 `eval()`/`exec()`，仅解压文件 |
| **内置技能保护** | 内置和组合技能设为只读，禁止删除 |
| **线程安全** | 网络操作在后台线程执行，UI 更新通过 `after()` 回调 |
| **可取消下载** | 使用 `threading.Event` 实现真正可中断的下载任务 |

---

## 9. 项目结构

```
skill_manager/
├── main.py                    # 程序入口
├── app.py                     # 主窗口（App 类）
├── requirements.txt           # Python 依赖
├── run.bat                    # 快速启动脚本（源码版）
├── build.bat                  # 构建 .exe 脚本
├── installer.iss              # Inno Setup 安装脚本
│
├── core/                      # 核心业务逻辑
│   ├── __init__.py
│   ├── scanner.py             # 技能扫描 + SKILL.md 解析
│   ├── manager.py             # 技能文件操作（删除/打开）
│   ├── downloader.py          # HTTPS 下载 + zip 解压安装
│   └── marketplace.py         # 社区技能市场数据获取
│
├── ui/                        # 界面组件
│   ├── __init__.py
│   ├── theme.py               # 颜色/字体/尺寸常量
│   ├── components.py          # 可复用组件（卡片/徽章/统计卡）
│   ├── sidebar.py             # 左侧导航栏（筛选+统计）
│   ├── skill_detail.py        # 右侧详情面板
│   ├── skill_list.py          # （已合并到 components.py）
│   ├── download_dialog.py     # 下载对话框
│   └── marketplace_panel.py   # 市场面板
│
├── utils/                     # 工具函数
│   ├── __init__.py
│   ├── paths.py               # 路径发现和格式化
│   ├── security.py            # URL 验证 + 路径安全
│   └── i18n.py                # 多语言翻译
│
├── assets/
│   └── icons/                 # 图标资源
│
├── dist/                      # 构建输出（.exe）
│   └── SkillManager.exe
│
└── build/                     # PyInstaller 临时构建文件
```

---

## 10. 从源码构建

### 构建独立 .exe

```bash
# 1. 安装 PyInstaller
pip install pyinstaller

# 2. 运行构建脚本
build.bat
```

或手动执行：

```bash
pyinstaller --onefile --windowed --name "SkillManager" ^
    --hidden-import yaml ^
    --hidden-import requests ^
    --hidden-import customtkinter ^
    --collect-submodules customtkinter ^
    main.py
```

构建完成后，.exe 文件位于 `dist/SkillManager.exe`。

### 构建安装包

1. 安装 [Inno Setup 6+](https://jrsoftware.org/isinfo.php)
2. 打开 `installer.iss`
3. 点击 **编译** (Build → Compile)
4. 安装包输出到 `installer_output/SkillManager-Setup-1.0.0.exe`

---

## 11. 常见问题

### Q: 启动后看不到任何技能？

**A**: 请检查以下路径是否存在 SKILL.md 文件：
- `C:\Users\<你的用户名>\.mimocode\skills\`
- `C:\Users\<你的用户名>\.claude\skills\`
- `C:\Users\<你的用户名>\.agents\skills\`
- `C:\Users\<你的用户名>\.local\share\mimocode\builtin_skills\`

如果这些目录不存在，说明尚未安装任何 MiMoCode Skills。

### Q: 下载技能时提示"仅支持 HTTPS"？

**A**: 请确保下载链接以 `https://` 开头。GitHub 仓库链接格式为：
`https://github.com/用户名/仓库名`

### Q: 下载后技能没有出现在列表中？

**A**: 可能原因：
1. 下载的 zip 包中不包含 `SKILL.md` 文件
2. 网络连接问题导致下载失败
3. 技能名称与已有技能冲突

尝试点击「技能市场」刷新，或检查 `~/.mimocode/skills/` 目录。

### Q: 内置技能为什么不能删除？

**A**: 内置技能（来源为「内置」或「组合」）是 MiMoCode 的核心功能组件，删除可能导致智能体功能异常。程序默认将其设为只读保护。

### Q: 如何更新技能？

**A**: 目前不支持增量更新。如需更新：
1. 删除旧版本技能
2. 重新下载安装新版本

### Q: 程序支持 macOS/Linux 吗？

**A**: 目前仅支持 Windows。由于使用了 `os.startfile()` 和 Windows 特定的路径检测，需要适配后才能支持其他平台。

### Q: 如何自定义技能市场？

**A**: 修改 `core/marketplace.py` 中的 `MARKETPLACE_URL` 变量，指向你自己的 JSON 配置文件地址。

JSON 格式：
```json
[
  {
    "name": "skill-name",
    "description": "技能描述",
    "url": "https://github.com/user/repo",
    "category": "分类",
    "author": "作者"
  }
]
```

---

## 12. 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| 语言 | Python | 3.10+ |
| UI 框架 | customtkinter | 6.0+ |
| YAML 解析 | PyYAML | 6.0+ |
| HTTP 客户端 | requests | 2.31+ |
| 打包工具 | PyInstaller | 6.0+ |
| 安装程序 | Inno Setup | 6.0+ |

---

## 13. 更新日志

### v1.0.0 (2026-07-09)

**初始版本**

- 自动扫描 5 个来源目录的本地技能
- 卡片式技能展示，支持点击查看详情
- 实时搜索过滤功能
- 按来源筛选（内置/组合/Claude/Agent/用户）
- 技能删除功能（内置技能只读保护）
- 从 GitHub URL / .zip 链接下载安装技能
- 内置社区技能市场
- 科技风深色主题 UI
- 中英文多语言支持
- HTTPS 安全下载 + 路径穿越防护
- PyInstaller 单文件 .exe 打包
- Inno Setup 安装程序（含控制面板卸载）

### v1.1.0 (2026-07-09)

**分类优化 + 性能提升 + 中文描述 + 文字增强**

**新增功能**：
- 技能分类简化：「跨平台」「平台专属」「用户安装」三级分类替代原来的 5 种来源筛选
- 中文描述翻译：内置 60+ 常见技能的中文描述映射，卡片优先显示中文
- 技能同步：支持将用户技能一键同步到 Claude/Agent/User 平台目录
- 详情面板双语：同时显示中文和英文描述

**性能优化**：
- 卡片渲染优化：跳过未变化的列表重绘
- 文字可读性提升：字号增大、颜色提亮、全局加粗

**UI 改进**：
- 文字亮度提升：`text_primary` 从 `#e2e8f0` → `#f1f5f9`，`text_secondary` 从 `#94a3b8` → `#cbd5e1`
- 字号增大：标题 16pt、正文 11pt、卡片名 14pt bold
- 新增分类标签（绿色=跨平台、金色=平台专属、蓝色=用户安装）
- 来源图例缩小为信息性展示

**Bug 修复**：
- 修复 `Sidebar.__init__` 过早触发回调导致 `_marketplace` 未定义的崩溃
- 修复 `SourceBadge` 使用 8 位 hex 颜色导致 tkinter 报错
- 修复 `pack`/`grid` 混用导致的布局冲突
- 修复 `os.makedirs(prefix_len=0)` 无效参数
- 修复 `ALLOWED_SCHEMES` 使用 `https://` 导致所有 HTTPS 被拒绝
- 修复 `marketplace_panel` 空集判断逻辑
- 清理未使用的 `subprocess` 导入

### v1.2.0 (2026-07-09)

**质量审计修复 + 日志系统 + 代码规范化**

**P0 修复**：
- 统一版本号为 1.2.0（app.py / installer.iss / README 三处同步）
- 生成 `assets/icons/icon.ico` 占位图标，Inno Setup 安装包可正常编译

**P1 修复**：
- 所有 `except Exception: pass` 改为记录日志（`utils/logger.py` 新增）
- `_CN_MAP` 子串匹配改为精确匹配 + 词边界正则，避免误匹配
- 清理 filter 逻辑，移除 v1.0 source filter 残留代码
- 新增 `.gitignore`（忽略 `__pycache__/`、`build/`、`dist/`、`.env` 等）
- `downloader.py` 和 `marketplace.py` 的 `requests.get` 添加 `User-Agent` 头

**代码质量**：
- 新增 `utils/logger.py` 日志模块，日志写入 `~/.skill_manager/logs/`
- 异常不再静默吞噬，均有日志记录
- 更新版本日志

### v1.3.0 (2026-07-16)

**重大安全加固 + 技能商店国内镜像 + 全平台扫描 + 动态图例**

**安全加固（核心）**：
- **Zip Slip 防护**：`downloader.py` 重写解压逻辑，使用 `os.path.realpath()` 前缀校验，彻底杜绝路径穿越攻击
- **Zip Bomb 检测**：解压前预计算压缩包总解压大小，超过 500MB 自动拒绝，防止磁盘耗尽攻击
- **流式下载**：`downloader.py` 改为 `tempfile.mkstemp()` + `requests.iter_content()` 流式写入磁盘，不再将整个 zip 加载到内存
- **原子同步**：`manager.py` 技能同步改为先复制到 `.tmp` 临时目录，再用 `os.replace()` 原子替换，避免中断导致数据损坏
- **可取消下载**：`download_dialog.py` 使用 `threading.Event` 实现真正可中断的下载线程
- **错误信息脱敏**：`_log_safe_error()` 过滤日志中的敏感路径信息

**技能商店（国内可用）**：
- **三源回退策略**：`marketplace.py` 实现 GitHub 原站 → `ghfast.top` 国内镜像 → 本地 JSON 缓存三级回退
- **指数退避重试**：连接失败时自动重试，退避基数 1.5 倍
- **缓存管理**：成功获取的数据自动缓存到本地，下次启动无网络也能显示历史列表
- **Schema 校验**：市场 JSON 数据格式校验，防止畸形数据导致崩溃
- **缓存状态显示**：`marketplace_panel.py` 显示「正在使用缓存数据」提示

**全平台技能扫描**：
- **15+ 平台预设**：`paths.py` 新增 OpenAI Codex、Cursor、Trae、Windsurf、Continue、Aider、MCP、GitHub Copilot、Cline 等平台路径
- **全局递归搜索**：在 `~` 目录下递归搜索所有 `SKILL.md`（最大深度 4 层），发现未知平台的技能
- **用户自定义路径**：支持通过 `~/.skill_manager/config.json` 添加自定义扫描目录
- **智能分类**：递归发现的技能统一标记为 `discovered` 来源，与预设平台区分

**UI 优化**：
- **动态侧边栏图例**：`sidebar.py` 的 `update_stats()` 仅显示当前电脑实际存在的来源，未安装的平台不显示颜色和标注，避免视觉干扰
- **搜索防抖**：`app.py` 搜索输入增加 300ms 防抖，避免频繁重绘导致卡顿
- **新增平台配色**：`theme.py` 为 10 个新平台添加专属颜色（Codex 紫、Cursor 青、Trae 蓝等）

**工程规范**：
- **版本封装**：`__version__ = "1.3.0"` 统一集中在 `app.py`，所有模块通过导入引用
- **严格层级结构**：docstring → imports → constants → internal functions → public API
- **模块依赖单向化**：ui → core → utils，禁止反向依赖
- **日志自动清理**：`logger.py` 新增 `_cleanup_old_logs()`，自动删除 30 天前的日志文件
- **跨平台目录打开**：`manager.py` 的 `open_skill_dir()` 支持 Windows (`os.startfile`) / macOS (`open`) / Linux (`xdg-open`)
- **i18n 完整覆盖**：`i18n.py` 新增所有新平台的中英文翻译

**Bug 修复**：
- 修复 `marketplace.py` 默认仓库 `AstraBert/micode-skills` 不存在导致的 404 问题（通过回退机制兼容）
- 修复 `scanner.py` 对未知来源技能返回空字符串 `source=""` 的问题
- 修复 `sidebar.py` 图例固定渲染所有平台导致的信息密度过高问题

### v1.4.0 (2026-07-16)

**技能去重 + 市场容错 + 响应式布局 + 错误透明化**

**技能扫描去重（核心修复）**：
- **版本去重**：`paths.py` 新增 `_deduplicate_by_version()` 函数，当同一技能出现在多个版本目录时（如 `builtin_skills/0.1.3/` 和 `0.1.5/`），自动保留最新版本，消除重复条目
- **版本提取**：`_extract_version_from_path()` 从路径中提取语义版本号进行比较
- **稳定排序**：去重后按来源和名称排序，确保技能列表顺序一致
- **扫描日志**：`find_skill_dirs()` 完成后记录找到的技能总数和去重数量

**技能市场容错（核心修复）**：
- **多源尝试**：`marketplace.py` 从单个仓库改为多仓库列表尝试（main 分支 + master 分支）
- **内置兜底列表**：网络不可用时返回内置技能列表（Claude Code、MiMoCode、社区精选），用户始终能看到可安装的技能
- **四层回退**：GitHub 原站 → ghfast.top 镜像 → 本地缓存 → 内置列表，确保永远不返回空
- **详细错误返回**：`fetch_marketplace()` 返回值新增 `errors` 列表，包含每个失败源的具体错误原因（超时/404/连接失败）

**错误透明化（核心修复）**：
- **错误详情展示**：`marketplace_panel.py` 新增 `_error_detail` 标签，在市场面板中显示每个失败源的具体错误
- **降级提示**：使用内置列表时显示黄色警告「⚠ 使用内置技能列表（网络不可用）」
- **安装错误**：安装失败时显示具体错误信息而非通用提示

**响应式卡片布局（核心修复）**：
- **窗口缩放自适应**：`ScrollableCardGrid` 绑定 `<Configure>` 事件，窗口大小变化时自动重排列数
- **防抖重排**：150ms 防抖避免频繁重排，性能更优
- **最小 2 列保证**：`_calc_columns()` 确保至少 2 列，避免初始渲染只有 1 列的问题
- **自适应文字换行**：`SkillCard.update_wraplength()` 根据列宽动态调整文字换行长度
- **延迟布局**：初始渲染时若几何信息未就绪，200ms 后自动重排
- **描述截断优化**：卡片描述截断长度从 80 提升到 100 字符

**版本封装**：
- `__version__` 统一更新为 `"1.4.0"`
- `USER_AGENT` 在 `downloader.py` 和 `marketplace.py` 中同步更新为 `"SkillManager/1.4.0"`
- V1.3 代码完整保留在独立文件夹 `Skill_Manager_V1.3/`，实现版本隔离

### v1.4.1 (2026-07-16)

**移除技能市场 + 恢复 V1.2 卡片布局 + 保留全部安全加固**

**功能精简（核心变更）**：
- **移除技能市场**：删除顶部的「技能市场」按钮和整个市场浏览面板。GitHub 不仅包含技能，还包含程序和工具，不适合作为定向技能源。保留 URL 下载功能，用户可通过提供 GitHub 链接直接下载技能
- **简化 app.py**：移除 `_toggle_marketplace()`、`_on_marketplace_install()`、`_marketplace_visible` 等市场相关逻辑，恢复 V1.2 的简洁三栏布局（侧边栏 + 卡片网格 + 详情面板）

**卡片布局恢复（核心修复）**：
- **恢复 V1.2 原始卡片样式**：`components.py` 回退到 V1.2 版本，移除 V1.4 引入的响应式重排逻辑（`<Configure>` 绑定、防抖重排、动态 wraplength），恢复固定的 `wraplength=220` 和简洁的 `ScrollableCardGrid`
- **恢复 V1.2 侧边栏**：`sidebar.py` 回退到 V1.2 版本，移除动态图例逻辑，恢复固定显示所有来源的图例
- **恢复 V1.2 下载对话框**：`download_dialog.py` 回退到 V1.2 版本的简洁布局，保留 V1.3 的 `threading.Event` 可取消下载功能

**保留的安全加固（未变动）**：
- Zip Slip 路径穿越防护（`downloader.py._safe_extract()`）
- Zip Bomb 解压大小检测（`downloader.py._check_zip_bomb()`）
- 流式下载到临时文件（`downloader.py._download_to_file()`）
- 原子同步（`manager.py` 临时目录 + `os.replace()`）
- 技能去重（`paths.py._deduplicate_by_version()`）
- 三层扫描策略（`paths.py` 预设 + 递归 + 自定义路径）
- 搜索防抖 300ms（`app.py._on_search()`）

---

## 许可证

MIT License

Copyright (c) 2026 MiMoCode
