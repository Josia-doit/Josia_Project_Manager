# Josia Project Manager
✨ 可视化项目文件管理器 · 一键批量生成项目结构 ✨

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-orange.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)


## 🎯 项目初衷

在日常开发、AI 代码生成、项目初始化的过程中，**手动创建目录、新建文件、粘贴代码、管理多层级结构** 操作繁琐、效率低下，且极易出现路径错误、文件遗漏等问题。

Josia Project Manager 旨在提供一个**轻量、简洁、可视化**的项目管理工具，让你只需要一段 JSON 指令，就能**一键生成完整项目骨架**，告别重复的手动文件操作。

## 🚀 解决的问题

- 快速将 AI 生成的代码结构，一键落地为真实文件与目录

- 可视化管理项目文件，支持新建、删除、编辑、重命名

- 解决文件写入后文件夹被占用、无法重命名的问题

- 避免手动创建文件导致的路径错误、层级混乱

- 提升项目模板生成、原型开发、教学演示的效率

- 内置代码编辑器，无需切换外部软件即可修改文件

- 打包项目后自动清理临时文件，保持项目目录整洁，避免冗余文件占用空间

- 精简项目核心文件，删除废弃模块，提升程序运行流畅度，降低维护成本

## 🌟 核心功能

- 📁 **项目管理**：打开/关闭项目、重命名项目文件夹

- 📝 **文件编辑**：内置代码编辑器，支持语法高亮、保存

- 🧩 **批量写入**：通过 JSON 指令一键生成完整项目结构

- 🗂️ **目录管理**：新建文件、新建文件夹、删除选中项

- 📖 **内置帮助**：使用说明 + AI 指令模板，一键复制

- 🎨 **现代界面**：扁平化风格简洁 UI，操作流畅

- 📦 **一键打包 EXE**：支持单文件/多文件两种打包模式，满足不同部署需求

- 🧹 **自动清理临时文件**：打包完成后，自动删除 build 目录、dist 目录及 .spec 配置文件，无需手动清理，保持项目目录干净整洁

## ⌨️ 完整快捷键列表

|操作|快捷键|说明|
|---|---|---|
|保存文件|`Ctrl + S`|保存当前编辑的文件内容|
|新建文件|`Ctrl + N`|在选中目录下新建文件|
|新建文件夹|`Ctrl + Shift + N`|在选中目录下新建文件夹|
|关闭当前文件|`Ctrl + W`|关闭编辑器中当前打开的文件|
|全选文本|`Ctrl + A`|编辑器中全选当前文件内容|
|复制文本|`Ctrl + C`|编辑器中复制选中的内容|
|粘贴文本|`Ctrl + V`|编辑器中粘贴剪贴板内容|
|剪切文本|`Ctrl + X`|编辑器中剪切选中的内容|
|撤销操作|`Ctrl + Z`|编辑器中撤销上一步编辑|
|重做操作|`Ctrl + Y`|编辑器中重做上一步撤销|
|删除选中项|`Delete`|删除文件树中选中的文件/文件夹|
|重命名选中项|`F2`|重命名文件树中选中的文件/文件夹|
|打开帮助|`F1`|快速打开内置帮助文档|
|批量导出|`Ctrl + E`|将当前项目文件批量导出为 JSON 格式|
|打包 EXE|`Ctrl + B`|一键打包当前项目为可执行文件，自动清理临时文件|
|批量写入|`Ctrl + G`|粘贴 JSON 指令，一键生成项目文件与目录|

## 📢 重要说明
本软件 **基于 Python 3.13 (64位)开发**
所有代码、依赖、打包功能均适配此环境。

## 📖 快速使用指南（Windows）
### 1. 启动程序

#### 方式 1：直接运行 EXE（推荐普通用户）
1. 下载 `Josia_Project_Manager.exe`
2. 如需使用 **打包 EXE 功能**，请先运行：**install_requirements.bat**
3. 安装完成后，即可正常打开 EXE 使用全部功能

#### 方式 2：源码运行（开发者）
1. 克隆或下载本项目
2. 双击运行：**install_requirements.bat**
3. 运行：**python main.py**

```
🛠️ install_requirements.bat 作用
全自动一键部署完整环境：
1. 自动下载 Python 3.13.1 (64位)
2. 自动静默安装并配置环境变量
3. 自动安装项目所有依赖（从 requirements.txt）
4. 自动配置国内加速源，速度更快
（整个过程无需用户任何操作）
```

### 2. 设定项目目录

点击工具栏 **【设定目录】**，选择一个文件夹作为项目根目录。

### 3. 批量生成文件（核心）

1. 点击 **【批量写入】**

2. 粘贴 JSON 结构指令

3. 点击 **【执行批量写入】**

4. 自动生成所有文件与目录

### 4. 常用操作

- 打开文件：左侧文件树单击

- 重命名项目：右键顶部项目标题

- 打开帮助：点击工具栏【帮助】/ 按下 `F1` 快捷键

- 删除文件/文件夹：选中后按 `Delete` 键

- 重命名文件/文件夹：选中后按 `F2` 键

- 批量导出项目：点击工具栏【批量导出】/ 按下 `Ctrl + E` 快捷键，生成项目 JSON 文件

- 打包 EXE：点击工具栏【打包 EXE】/ 按下 `Ctrl + B` 快捷键，完成以下操作即可打包：
        

    - 选择输出目录（存放生成的 EXE 文件）

    - 输入 EXE 文件名（自定义命名）

    - 选择打包模式（单文件/多文件）

    - 点击【开始打包】，等待打包完成

    - 打包完成后，程序会自动清理 build、dist 临时目录及 .spec 配置文件，无需手动删除

## ⚠️ 注意事项
1. **必须使用 Python 3.13 (64位)**，其他版本不保证兼容
2. 首次使用打包 EXE 功能前，必须运行 install_requirements.bat
3. 脚本会自动安装 Python 3.13 及所需依赖环境，无需手动下载
4. 仅支持 64 位 Windows 系统

## 📦 项目依赖
所有依赖已写入 `requirements.txt`，由脚本自动安装：
- PyQt5 >= 5.15.11
- QScintilla >= 2.14.1
- PyInstaller >= 6.10.0

## 🧪 标准测试流程

### Step 1：复制测试 JSON 指令

```json
{
  "files": [
    {
      "path": "main.py",
      "content": "# 主程序\nimport sys\nfrom PyQt5.QtWidgets import *\n\nclass MainWindow(QMainWindow):\n    def __init__(self):\n        super().__init__()\n        self.setWindowTitle('测试窗口')\n        self.resize(400, 300)\n\nif __name__ == '__main__':\n    app = QApplication(sys.argv)\n    window = MainWindow()\n    window.show()\n    sys.exit(app.exec_())"
    },
    {
      "path": "config/settings.py",
      "content": "# 配置文件\nDEBUG = True\nVERSION = '1.0.0'\nAUTHOR = '测试作者'"
    },
    {
      "path": "utils/tools.py",
      "content": "# 工具函数\ndef hello():\n    return 'Hello World'\n\ndef add(a, b):\n    return a + b"
    },
    {
      "path": "static/style.css",
      "content": "/* 样式文件 */\n* {\n    margin: 0;\n    padding: 0;\n}\n\nbody {\n    background: #f5f5f5;\n}"
    },
    {
      "path": "README.md",
      "content": "# 测试项目\n这是自动生成的测试项目\n包含目录结构和多个文件\n用于测试软件功能"
    }
  ]
}
```

### Step 2：执行批量写入

粘贴 → 执行，程序将自动创建完整目录结构。

### Step 3：生成的文件结构

```bash
你的项目目录/
├── main.py              # 可直接运行的 PyQt5 主窗口
├── config/
│   └── settings.py      # 项目配置文件
├── utils/
│   └── tools.py         # 工具函数模块
├── static/
│   └── style.css        # 前端样式文件
└── README.md            # 项目说明文档
```

## 💡 适用场景

- AI 代码 → 一键生成真实项目

- 快速搭建项目模板骨架

- 教学演示文件目录结构

- 批量生成配置、脚本、示例文件

- 小型项目可视化管理与快速编辑

- 项目快速打包部署，自动清理临时文件，提升部署效率

## 📋 项目文件结构（当前最新精简版）

本次更新后，已清理所有废弃文件和目录，仅保留核心模块，文件结构如下（确保程序正常运行的必要文件）：

```bash
Josia_Project_Manager/
├── icons/                    # 程序图标资源（必需）
├── README.md                 # 项目说明文档（当前文件）
├── CHANGELOG.md              # 版本更新日志（新增）
├── requirements.txt          # 依赖环境清单（必需）
├── install_requirements.bat  # 一键环境部署脚本（可选）
├── main.py                   # 主程序入口（必需）
├── file_tree.py              # 左侧文件树模块（必需）
├── code_editor.py            # 右侧代码编辑器模块（必需）
├── help_left.md              # 帮助文档内容（必需）
└── help_right.md             # AI 指令模板（必需）
```

**说明**：已删除废弃的structure_parser.py 文件，此文件为早期版本遗留，当前版本已无需依赖，如曾下载旧版文件，删除后不影响任何功能，且能提升程序运行效率。

## 🔧 常见问题解决

- **启动报错**：若出现代码编辑器相关报错，大概率是 QsciScintilla 颜色参数错误，当前版本已修复，替换最新版 code_editor.py 即可正常启动。

- **打包后冗余文件**：无需手动清理，程序会在打包完成后，自动删除 build、dist 临时目录及 .spec 配置文件，仅保留你指定输出目录中的 EXE 文件。

- **文件操作失败**：优化了文件读写异常处理，若出现创建/删除/重命名失败，会弹出错误提示，可根据提示检查文件是否被占用。

## 📄 License

MIT License
