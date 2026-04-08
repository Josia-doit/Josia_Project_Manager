import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QSplitter, QFileDialog, QMessageBox, QDialog, QTextEdit,
                             QPushButton, QToolBar, QAction, QLabel, QFrame, QMenu,
                             QInputDialog)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QKeySequence, QFont, QClipboard
from file_tree import FileTree
from code_editor import CodeEditor

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

WINDOWS11_STYLE = """
QMainWindow {
    background-color: #f3f3f3;
}
QToolBar {
    background-color: #ffffff;
    border: none;
    border-bottom: 1px solid #e0e0e0;
    spacing: 0px;
    padding: 16px 12px;
}
QToolBar::separator {
    background-color: #e0e0e0;
    width: 1px;
    margin: 20px 10px;
}
QToolButton {
    background-color: transparent;
    border: none;
    border-radius: 8px;
    padding: 8px 4px;
    font-size: 13px;
    font-weight: bold;
    color: #1a1a1a;
    min-width: 72px;
    max-width: 72px;
    min-height: 72px;
    max-height: 72px;
    text-align: center;
    font-family: "Microsoft YaHei", sans-serif;
}
QToolButton:hover {
    background-color: #e5e5e5;
}
QToolButton:pressed {
    background-color: #d9d9d9;
}
#ProjectTitleBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e0e0e0;
    padding: 28px 16px;
}
#ProjectTitleLabel {
    font-size: 17px;
    font-weight: 600;
    color: #1a1a1a;
    font-family: "Microsoft YaHei", sans-serif;
}
QTreeView {
    background-color: #ffffff;
    border: none;
    padding: 8px 4px;
    font-size: 13px;
    color: #1a1a1a;
    outline: none;
    font-family: "Microsoft YaHei", sans-serif;
}
QTreeView::item {
    height: 28px;
    border-radius: 4px;
    padding: 2px 8px;
    margin: 1px 4px;
}
QTreeView::item:selected {
    background-color: #e5e5e5;
    color: #1a1a1a;
}
QTreeView::item:hover:!selected {
    background-color: #f0f0f0;
}
QsciScintilla {
    border: none;
    border-radius: 8px;
    background-color: #ffffff;
    margin: 8px;
}
QDialog {
    background-color: #ffffff;
    border-radius: 8px;
}
QTextEdit {
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 10px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 13px;
    background-color: #ffffff;
    outline: none;
}
QTextEdit:focus {
    border: 1px solid #0067c0;
}
QPushButton {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 8px 20px;
    color: #1a1a1a;
    font-weight: 400;
    font-size: 13px;
    font-family: "Microsoft YaHei", sans-serif;
}
QPushButton:hover {
    background-color: #f0f0f0;
    border: 1px solid #c0c0c0;
}
QPushButton:pressed {
    background-color: #e5e5e5;
}
QPushButton#PrimaryButton {
    background-color: #0067c0;
    border: none;
    color: #ffffff;
}
QMenu {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 8px;
    padding: 4px;
}
QMenu::item {
    padding: 8px 20px;
    border-radius: 4px;
    color: #1a1a1a;
    font-size: 13px;
    font-family: "Microsoft YaHei", sans-serif;
}
QMenu::item:selected {
    background-color: #e5e5e5;
    color: #1a1a1a;
}
QLabel {
    color: #333333;
    font-size: 13px;
    font-family: "Microsoft YaHei", sans-serif;
}
QFrame[frameShape="HLine"] {
    background-color: #e0e0e0;
    max-height: 1px;
}
QFrame[frameShape="VLine"] {
    background-color: #e0e0e0;
    max-width: 1px;
}
"""

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("使用帮助")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setFixedSize(1350, 850)
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(30,30,20,30)
        left_layout.setSpacing(12)
        left_title = QLabel("🪟 软件使用说明")
        left_title.setFont(QFont("Microsoft YaHei", 20, QFont.Bold))
        left_layout.addWidget(left_title)
        left_line = QFrame()
        left_line.setFrameShape(QFrame.HLine)
        left_layout.addWidget(left_line)
        self.left_text = QTextEdit()
        self.left_text.setReadOnly(True)
        self.left_text.document().setDefaultFont(QFont("Microsoft YaHei", 10))
        self.load_md_file("help_left.md", self.left_text)
        left_layout.addWidget(self.left_text)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(20,30,30,30)
        right_layout.setSpacing(12)
        title_bar = QHBoxLayout()
        right_title = QLabel("🪟 AI 指令模板")
        right_title.setFont(QFont("Microsoft YaHei", 20, QFont.Bold))
        title_bar.addWidget(right_title)
        title_bar.addStretch()
        self.copy_btn = QPushButton("📋 复制全部指令")
        self.copy_btn.clicked.connect(self._copy_template)
        title_bar.addWidget(self.copy_btn)
        right_layout.addLayout(title_bar)
        right_line = QFrame()
        right_line.setFrameShape(QFrame.HLine)
        right_layout.addWidget(right_line)
        self.right_text = QTextEdit()
        self.right_text.setReadOnly(True)
        self.right_text.document().setDefaultFont(QFont("Consolas", 10))
        self.load_md_file("help_right.md", self.right_text)
        right_layout.addWidget(self.right_text)

        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(right_widget, 1)

    def load_md_file(self, filename, text_edit):
        path = resource_path(filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            text_edit.setMarkdown(content)
        except:
            text_edit.setText("加载失败")

    def _copy_template(self):
        QApplication.clipboard().setText(self.right_text.toPlainText())
        self.copy_btn.setText("✅ 已复制")
        self.copy_btn.setEnabled(False)
        self.copy_btn.setStyleSheet("color:#888888;")

class EmptyWidget(QWidget):
    set_dir_clicked = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(24)
        title = QLabel("Josia项目文件管理器")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Microsoft YaHei", 24, QFont.Bold))
        title.setStyleSheet("color: #1a1a1a;")
        layout.addWidget(title)
        tip = QLabel("设定项目目录，开始你的开发")
        tip.setAlignment(Qt.AlignCenter)
        tip.setFont(QFont("Microsoft YaHei", 12))
        layout.addWidget(tip)
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        self.set_dir_btn = QPushButton("📖 设定项目目录")
        self.set_dir_btn.setFixedSize(200, 45)
        self.set_dir_btn.setObjectName("PrimaryButton")
        self.set_dir_btn.clicked.connect(self.set_dir_clicked)
        btn_layout.addWidget(self.set_dir_btn)
        layout.addLayout(btn_layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_root = None
        self._setup_ui()
        self._create_actions()
        self._create_menu()
        self._create_toolbar()
        self._update_ui_state()

    def _setup_ui(self):
        self.setWindowTitle("Josia_Project_Manager")
        self.setGeometry(100, 100, 1400, 880)
        self.setStyleSheet(WINDOWS11_STYLE)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(1)
        self.splitter.setChildrenCollapsible(False)

        self.left_container = QWidget()
        self.left_layout = QVBoxLayout(self.left_container)
        self.left_layout.setContentsMargins(0,0,0,0)
        self.left_layout.setSpacing(0)

        self.project_title_bar = QWidget()
        self.project_title_bar.setObjectName("ProjectTitleBar")
        title_bar_layout = QHBoxLayout(self.project_title_bar)
        title_bar_layout.setContentsMargins(0,0,0,0)
        title_bar_layout.setAlignment(Qt.AlignCenter)
        self.project_title_label = QLabel("📁 未打开项目")
        self.project_title_label.setObjectName("ProjectTitleLabel")
        title_bar_layout.addWidget(self.project_title_label)

        self.left_layout.addWidget(self.project_title_bar)
        self.title_divider = QFrame()
        self.title_divider.setFrameShape(QFrame.HLine)
        self.left_layout.addWidget(self.title_divider)

        self.empty_widget = EmptyWidget()
        self.empty_widget.set_dir_clicked.connect(self.set_project_dir)
        self.left_layout.addWidget(self.empty_widget)

        self.file_tree = FileTree()
        self.file_tree.file_opened.connect(self.open_file)
        self.file_tree.hide()
        self.left_layout.addWidget(self.file_tree)

        self.editor = CodeEditor()
        self.editor.file_saved.connect(self._on_file_saved)

        self.splitter.addWidget(self.left_container)
        self.splitter.addWidget(self.editor)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 4)

        main_layout.addWidget(self.splitter)

        self.project_title_bar.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_title_bar.customContextMenuRequested.connect(self._show_title_context_menu)

    def _create_actions(self):
        def icon_path(name):
            return QIcon(resource_path(f"icons/{name}.png"))

        self.action_set_dir = QAction(icon_path("project"), "项目目录", self)
        self.action_set_dir.setToolTip("项目目录 (Ctrl+Shift+O)")
        self.action_set_dir.setShortcut(QKeySequence("Ctrl+Shift+O"))
        self.action_set_dir.triggered.connect(self.set_project_dir)

        self.action_rename_project = QAction(icon_path("re_project"), "项目重命名", self)
        self.action_rename_project.setToolTip("项目重命名 (Ctrl+F2)")
        self.action_rename_project.setShortcut(QKeySequence("Ctrl+F2"))
        self.action_rename_project.triggered.connect(self.rename_project)

        self.action_new_file = QAction(icon_path("file"), "新建文件", self)
        self.action_new_file.setToolTip("新建文件 (Ctrl+N)")
        self.action_new_file.setShortcut(QKeySequence("Ctrl+N"))
        self.action_new_file.triggered.connect(lambda: self.file_tree._create_file(self.project_root))

        self.action_new_folder = QAction(icon_path("folder"), "新建文件夹", self)
        self.action_new_folder.setToolTip("新建文件夹 (Ctrl+Shift+F)")
        self.action_new_folder.setShortcut(QKeySequence("Ctrl+Shift+F"))
        self.action_new_folder.triggered.connect(lambda: self.file_tree._create_folder(self.project_root))

        self.action_rename_item = QAction(icon_path("rename"), "文件重命名", self)
        self.action_rename_item.setToolTip("文件重命名 (F2)")
        self.action_rename_item.setShortcut(QKeySequence(Qt.Key_F2))
        self.action_rename_item.triggered.connect(lambda: self.file_tree.edit(self.file_tree.currentIndex()))

        self.action_delete = QAction(icon_path("delete"), "删除", self)
        self.action_delete.setToolTip("删除 (Delete)")
        self.action_delete.setShortcut(QKeySequence("Delete"))
        self.action_delete.triggered.connect(self.file_tree._delete_selected_items)

        self.action_batch_write = QAction(icon_path("batch"), "批量写入", self)
        self.action_batch_write.setToolTip("批量写入 (Ctrl+G)")
        self.action_batch_write.setShortcut(QKeySequence("Ctrl+G"))
        self.action_batch_write.triggered.connect(self.batch_modify)

        self.action_close_proj = QAction(icon_path("close"), "关闭项目", self)
        self.action_close_proj.setToolTip("关闭项目 (Ctrl+Q)")
        self.action_close_proj.setShortcut(QKeySequence("Ctrl+Q"))
        self.action_close_proj.triggered.connect(self.close_project)

        self.action_undo = QAction(icon_path("undo"), "撤销", self)
        self.action_undo.setToolTip("撤销 (Ctrl+Z)")
        self.action_undo.setShortcut(QKeySequence("Ctrl+Z"))
        self.action_undo.triggered.connect(self.editor.undo)

        self.action_redo = QAction(icon_path("redo"), "重做", self)
        self.action_redo.setToolTip("重做 (Ctrl+Y)")
        self.action_redo.setShortcut(QKeySequence("Ctrl+Y"))
        self.action_redo.triggered.connect(self.editor.redo)

        self.action_save = QAction(icon_path("save"), "保存", self)
        self.action_save.setToolTip("保存 (Ctrl+S)")
        self.action_save.setShortcut(QKeySequence("Ctrl+S"))
        self.action_save.triggered.connect(self.save_file)

        self.action_help = QAction(icon_path("help"), "使用帮助", self)
        self.action_help.setToolTip("使用帮助 (F1)")
        self.action_help.setShortcut(QKeySequence(Qt.Key_F1))
        self.action_help.triggered.connect(self.show_help)

    def _create_toolbar(self):
        self.toolbar = QToolBar("工具栏")
        self.toolbar.setIconSize(QSize(32, 32))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        self.toolbar.addAction(self.action_set_dir)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_rename_project)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_new_file)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_new_folder)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_rename_item)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_delete)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_batch_write)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_close_proj)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_undo)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_redo)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_save)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_help)

    def _create_menu(self):
        bar = self.menuBar()
        menu_proj = bar.addMenu("项目")
        menu_proj.addAction(self.action_set_dir)
        menu_proj.addAction(self.action_rename_project)
        menu_proj.addSeparator()
        menu_proj.addAction(self.action_close_proj)

        menu_edit = bar.addMenu("编辑")
        menu_edit.addAction(self.action_new_file)
        menu_edit.addAction(self.action_new_folder)
        menu_edit.addAction(self.action_rename_item)
        menu_edit.addAction(self.action_delete)
        menu_edit.addSeparator()
        menu_edit.addAction(self.action_undo)
        menu_edit.addAction(self.action_redo)
        menu_edit.addSeparator()
        menu_edit.addAction(self.action_save)

        menu_tools = bar.addMenu("工具")
        menu_tools.addAction(self.action_batch_write)

        menu_help = bar.addMenu("帮助")
        menu_help.addAction(self.action_help)

    def _show_title_context_menu(self, pos):
        if not self.project_root:
            return
        menu = QMenu()
        menu.addAction(self.action_rename_project)
        menu.exec_(self.project_title_bar.mapToGlobal(pos))

    def rename_project(self):
        if not self.project_root:
            QMessageBox.warning(self, "提示", "未打开项目")
            return

        old_name = os.path.basename(self.project_root)
        parent_dir = os.path.dirname(self.project_root)
        new_name, ok = QInputDialog.getText(self, "重命名项目", "新名称:", text=old_name)

        if not ok or not new_name.strip() or new_name == old_name:
            return

        new_path = os.path.join(parent_dir, new_name)

        try:
            self.editor.clear_editor()
            self.file_tree.clear_project()
            QApplication.processEvents()
            QTimer.singleShot(50, lambda: None)

            os.rename(self.project_root, new_path)
            self.project_root = new_path
            self.file_tree.set_project_root(new_path)
            self._update_ui_state()
            QMessageBox.information(self, "成功", "项目已重命名")

        except Exception as e:
            QMessageBox.critical(self, "失败", f"重命名失败：{str(e)}\n请确认文件未被其他程序占用")

    def _update_ui_state(self):
        has_project = self.project_root is not None
        self.action_new_file.setEnabled(has_project)
        self.action_new_folder.setEnabled(has_project)
        self.action_rename_item.setEnabled(has_project)
        self.action_delete.setEnabled(has_project)
        self.action_batch_write.setEnabled(has_project)
        self.action_close_proj.setEnabled(has_project)
        self.action_rename_project.setEnabled(has_project)
        self.action_save.setEnabled(has_project)
        self.action_undo.setEnabled(has_project)
        self.action_redo.setEnabled(has_project)

        if has_project:
            self.project_title_bar.show()
            self.title_divider.show()
            self.project_title_label.setText(f"📁 {os.path.basename(self.project_root)}")
            self.empty_widget.hide()
            self.file_tree.show()
        else:
            self.project_title_bar.hide()
            self.title_divider.hide()
            self.empty_widget.show()
            self.file_tree.hide()
            self.editor.clear_editor()

    def set_project_dir(self):
        path = QFileDialog.getExistingDirectory(self, "选择项目目录")
        if path:
            self.project_root = path
            self.file_tree.set_project_root(path)
            self._update_ui_state()

    def close_project(self):
        if not self.project_root:
            return
        reply = QMessageBox.question(self, "确认", "确定要关闭当前项目吗？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.project_root = None
            self.file_tree.clear_project()
            self._update_ui_state()

    def open_file(self, path):
        self.editor.load_file(path)

    def save_file(self):
        if self.editor.save_file():
            QMessageBox.information(self, "成功", "文件已保存")

    def _on_file_saved(self):
        pass

    def batch_modify(self):
        if not self.project_root:
            QMessageBox.warning(self, "提示", "请先设定项目目录")
            return
        dlg = QDialog(self)
        dlg.setWindowTitle("批量写入")
        dlg.resize(700, 600)
        layout = QVBoxLayout(dlg)
        text_edit = QTextEdit()
        layout.addWidget(text_edit)
        btn = QPushButton("执行批量写入")
        btn.setObjectName("PrimaryButton")
        layout.addWidget(btn)

        def run():
            try:
                data = json.loads(text_edit.toPlainText())
                for item in data["files"]:
                    file_path = os.path.join(self.project_root, item["path"])
                    dir_name = os.path.dirname(file_path)
                    os.makedirs(dir_name, exist_ok=True)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(item["content"])
                QMessageBox.information(dlg, "完成", "所有文件已生成")
                self.editor.clear_editor()
                self.file_tree.clear_project()
                self.file_tree.set_project_root(self.project_root)
                dlg.accept()
            except Exception as e:
                QMessageBox.warning(dlg, "错误", str(e))

        btn.clicked.connect(run)
        dlg.exec_()

    def show_help(self):
        HelpDialog(self).exec_()

if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
