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

## 🌟 核心功能
- 📁 **项目管理**：打开/关闭项目、重命名项目文件夹
- 📝 **文件编辑**：内置代码编辑器，支持语法高亮、保存
- 🧩 **批量写入**：通过 JSON 指令一键生成完整项目结构
- 🗂️ **目录管理**：新建文件、新建文件夹、删除选中项
- 📖 **内置帮助**：使用说明 + AI 指令模板，一键复制
- 🎨 **现代界面**：Windows11 风格简洁 UI，操作流畅

## ⌨️ 完整快捷键列表
| 操作               | 快捷键              | 说明                     |
|--------------------|---------------------|--------------------------|
| 保存文件           | `Ctrl + S`          | 保存当前编辑的文件内容   |
| 新建文件           | `Ctrl + N`          | 在选中目录下新建文件     |
| 新建文件夹         | `Ctrl + Shift + N`  | 在选中目录下新建文件夹   |
| 关闭当前文件       | `Ctrl + W`          | 关闭编辑器中当前打开的文件 |
| 全选文本           | `Ctrl + A`          | 编辑器中全选当前文件内容 |
| 复制文本           | `Ctrl + C`          | 编辑器中复制选中的内容   |
| 粘贴文本           | `Ctrl + V`          | 编辑器中粘贴剪贴板内容   |
| 剪切文本           | `Ctrl + X`          | 编辑器中剪切选中的内容   |
| 撤销操作           | `Ctrl + Z`          | 编辑器中撤销上一步编辑   |
| 重做操作           | `Ctrl + Y`          | 编辑器中重做上一步撤销   |
| 删除选中项         | `Delete`            | 删除文件树中选中的文件/文件夹 |
| 重命名选中项       | `F2`                | 重命名文件树中选中的文件/文件夹 |
| 打开帮助           | `F1`                | 快速打开内置帮助文档     |

## 📖 快速使用指南
### 1. 启动程序
运行编译后的 `exe` 文件，进入主界面。

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
```
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

## 📁 生成文件说明
使用测试指令后，会自动生成以下文件：
1. **main.py**：完整可运行的 PyQt5 窗口程序
2. **config/settings.py**：项目配置（DEBUG、版本、作者）
3. **utils/tools.py**：通用工具方法
4. **static/style.css**：基础 CSS 样式表
5. **README.md**：项目说明文档

## 💡 适用场景
- AI 代码 → 一键生成真实项目
- 快速搭建项目模板骨架
- 教学演示文件目录结构
- 批量生成配置、脚本、示例文件
- 小型项目可视化管理与快速编辑

## 📄 License
MIT License
