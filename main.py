import sys
import os
import json
import shutil
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QSplitter, QFileDialog, QMessageBox, QDialog, QTextEdit,
                             QPushButton, QToolBar, QAction, QLabel, QFrame, QMenu,
                             QInputDialog, QRadioButton, QGroupBox, QLineEdit, QPlainTextEdit,
                             QFormLayout)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QTimer, QUrl, QThread
from PyQt5.QtGui import QIcon, QKeySequence, QFont, QClipboard, QDesktopServices
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
    spacing: 4px;
    padding: 12px 8px;
}
QToolBar::separator {
    background-color: #e0e0e0;
    width: 1px;
    margin: 16px 6px;
}
QToolButton {
    background-color: transparent;
    border: none;
    border-radius: 8px;
    padding: 6px 2px;
    font-size: 11px;
    font-weight: bold;
    color: #1a1a1a;
    min-width: 64px;
    max-width: 64px;
    min-height: 64px;
    max-height: 64px;
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

# ====================== 打包线程（自动清理 build/dist/spec）======================
class PackageThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)

    def __init__(self, pack_args, project_root, exe_name):
        super().__init__()
        self.pack_args = pack_args
        self.project_root = project_root
        self.exe_name = exe_name
        self.spec_file = os.path.join(project_root, f"{exe_name}.spec")

    def run(self):
        original_cwd = os.getcwd()
        os.chdir(self.project_root)

        try:
            process = subprocess.Popen(
                self.pack_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="ignore"
            )

            while process.poll() is None:
                line = process.stdout.readline()
                if line:
                    self.log_signal.emit(line.strip())

            return_code = process.returncode
        except Exception as e:
            self.log_signal.emit(f"打包异常：{str(e)}")
            return_code = -1
        finally:
            os.chdir(original_cwd)

        # 打包成功才自动清理
        if return_code == 0:
            self.log_signal.emit("\n=== 开始自动清理临时文件 ===")

            # 删除 build
            build_dir = os.path.join(self.project_root, "build")
            if os.path.exists(build_dir):
                try:
                    shutil.rmtree(build_dir)
                    self.log_signal.emit("已删除：build 目录")
                except Exception as e:
                    self.log_signal.emit(f"删除 build 失败：{e}")

            # 删除项目内 dist（已用 --distpath，无用）
            dist_dir = os.path.join(self.project_root, "dist")
            if os.path.exists(dist_dir):
                try:
                    shutil.rmtree(dist_dir)
                    self.log_signal.emit("已删除：dist 目录")
                except Exception as e:
                    self.log_signal.emit(f"删除 dist 失败：{e}")

            # 删除 spec
            if os.path.exists(self.spec_file):
                try:
                    os.remove(self.spec_file)
                    self.log_signal.emit(f"已删除：{os.path.basename(self.spec_file)}")
                except Exception as e:
                    self.log_signal.emit(f"删除 spec 失败：{e}")

            self.log_signal.emit("=== 清理完成，无残留临时文件 ===")

        self.finished_signal.emit(return_code)

# ====================== 批量导出对话框 ======================
class ExportJsonDialog(QDialog):
    def __init__(self, project_root, parent=None):
        super().__init__(parent)
        self.project_root = project_root
        self.setWindowTitle("批量导出")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setFixedSize(800, 600)

        # 只允许代码类文件
        self.allowed_extensions = {
            '.py', '.js', '.md', '.html', '.css', '.json', '.txt',
            '.java', '.cpp', '.h', '.c', '.cs', '.php', '.go', '.rs',
            '.ts', '.jsx', '.tsx', '.vue', '.scss', '.less', '.yaml', '.yml'
        }

        main_layout = QVBoxLayout(self)
        btn_layout = QHBoxLayout()

        self.export_btn = QPushButton("开始导出")
        self.copy_btn = QPushButton("复制代码")
        self.copy_btn.setEnabled(False)

        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.copy_btn)
        btn_layout.addStretch()

        self.json_edit = QPlainTextEdit()
        self.json_edit.setReadOnly(True)
        self.json_edit.setPlaceholderText("导出的项目结构代码将显示在此处...")

        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.json_edit)

        self.export_btn.clicked.connect(self.export_json)
        self.copy_btn.clicked.connect(self.copy_json)

    def export_json(self):
        if not self.project_root or not os.path.exists(self.project_root):
            QMessageBox.warning(self, "警告", "请先打开一个项目！")
            return

        try:
            project_files = []
            skipped_files = []

            for root, dirs, files in os.walk(self.project_root):
                if '__pycache__' in root or '.git' in root or 'dist' in root or 'build' in root:
                    continue

                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.project_root)
                    file_ext = os.path.splitext(file)[1].lower()

                    if file_ext in self.allowed_extensions:
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                            project_files.append({
                                "path": relative_path.replace('\\', '/'),
                                "content": content
                            })
                        except:
                            skipped_files.append(relative_path)
                    else:
                        skipped_files.append(relative_path)

            result = {"files": project_files}
            json_str = json.dumps(result, ensure_ascii=False, indent=4)
            self.json_edit.setPlainText(json_str)

            self.export_btn.setEnabled(False)
            self.copy_btn.setEnabled(True)

            if skipped_files:
                QMessageBox.information(self, "提示",
                    f"导出完成！\n\n已跳过 {len(skipped_files)} 个非代码文件（图片、图标等）\n这些文件需要手动保存。")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败：{str(e)}")

    def copy_json(self):
        try:
            text = self.json_edit.toPlainText()
            QApplication.clipboard().setText(text)
            tip = QLabel("已复制", self)
            tip.setStyleSheet("color:green; background:white; padding:6px; border-radius:4px")
            tip.adjustSize()
            tip.move(self.width()//2 - tip.width()//2, self.height()//2 - tip.height()//2)
            tip.show()
            QTimer.singleShot(1500, tip.close)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"复制失败：{str(e)}")

# ====================== 打包为EXE对话框 ======================
class PackageExeDialog(QDialog):
    def __init__(self, project_root, parent=None):
        super().__init__(parent)
        self.project_root = project_root
        self.setWindowTitle("打包为EXE")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setFixedSize(900, 700)
        self.output_dir = ""
        self.package_thread = None

        main_layout = QVBoxLayout(self)
        top_layout = QFormLayout()
        btn_layout = QHBoxLayout()

        self.dir_btn = QPushButton("选择输出目录")
        self.dir_label = QLabel("未选择输出目录")
        top_layout.addRow(self.dir_btn, self.dir_label)

        self.exe_name_edit = QLineEdit()
        self.exe_name_edit.setPlaceholderText("请输入EXE文件名（无需.exe后缀）")
        self.exe_name_label = QLabel("当前EXE文件名：未输入")
        top_layout.addRow("EXE文件名：", self.exe_name_edit)
        top_layout.addRow(self.exe_name_label)

        self.pack_type_group = QGroupBox("打包方式")
        pack_layout = QHBoxLayout(self.pack_type_group)
        self.single_exe_radio = QRadioButton("单EXE文件 (-F)")
        self.multi_exe_radio = QRadioButton("多文件目录 (-D)")
        self.multi_exe_radio.setChecked(True)
        pack_layout.addWidget(self.single_exe_radio)
        pack_layout.addWidget(self.multi_exe_radio)
        top_layout.addRow(self.pack_type_group)

        self.pack_btn = QPushButton("开始打包")
        self.open_dir_btn = QPushButton("打开输出目录")
        self.open_dir_btn.setEnabled(False)
        btn_layout.addWidget(self.pack_btn)
        btn_layout.addWidget(self.open_dir_btn)
        btn_layout.addStretch()

        self.log_edit = QPlainTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setPlaceholderText("打包日志将显示在此处...")

        main_layout.addLayout(top_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.log_edit)

        self.dir_btn.clicked.connect(self.choose_output_dir)
        self.exe_name_edit.textChanged.connect(self.update_exe_name_label)
        self.pack_btn.clicked.connect(self.start_package)
        self.open_dir_btn.clicked.connect(self.open_output_dir)

    def choose_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出目录", "./")
        if dir_path:
            self.output_dir = dir_path
            self.dir_label.setText(f"已选择：{dir_path}")
            self.open_dir_btn.setEnabled(True)

    def update_exe_name_label(self):
        exe_name = self.exe_name_edit.text().strip()
        if exe_name:
            self.exe_name_label.setText(f"当前EXE文件名：{exe_name}.exe")
        else:
            self.exe_name_label.setText("当前EXE文件名：未输入")

    def start_package(self):
        if not self.project_root or not os.path.exists(self.project_root):
            QMessageBox.warning(self, "警告", "请先打开一个项目！")
            return
        if not self.output_dir:
            QMessageBox.warning(self, "警告", "请先选择输出目录！")
            return
        exe_name = self.exe_name_edit.text().strip()
        if not exe_name:
            QMessageBox.warning(self, "警告", "请输入EXE文件名！")
            return

        self.log_edit.clear()
        self.pack_btn.setEnabled(False)

        pack_args = ["pyinstaller"]
        if self.single_exe_radio.isChecked():
            pack_args.append("-F")
        else:
            pack_args.append("-D")

        pack_args.extend([
            "-w",
            "-n", exe_name,
            "-i", "icons/app.ico",
            "--add-data", "help_left.md;.",
            "--add-data", "help_right.md;.",
            "--add-data", "icons/*;icons/",
            "--distpath", self.output_dir,
            "--clean",
            "main.py"
        ])

        # 传入 exe_name 用于删除 spec
        self.package_thread = PackageThread(pack_args, self.project_root, exe_name)
        self.package_thread.log_signal.connect(self.update_log)
        self.package_thread.finished_signal.connect(self.package_finished)
        self.package_thread.start()

    def update_log(self, line):
        self.log_edit.appendPlainText(line)
        self.log_edit.verticalScrollBar().setValue(self.log_edit.verticalScrollBar().maximum())

    def package_finished(self, returncode):
        self.pack_btn.setEnabled(True)
        if returncode == 0:
            self.log_edit.appendPlainText("\n=== 打包 + 清理全部完成 ===")
            QMessageBox.information(self, "完成", "EXE打包完成且已自动清理临时文件！")
        else:
            self.log_edit.appendPlainText(f"\n=== 打包失败 ===")
            QMessageBox.critical(self, "失败", "打包失败，请查看日志")

    def open_output_dir(self):
        if self.output_dir and os.path.exists(self.output_dir):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.output_dir))

# ====================== 运行测试对话框 ======================
class RunTestDialog(QDialog):
    def __init__(self, project_root, parent=None):
        super().__init__(parent)
        self.project_root = project_root
        self.setWindowTitle("运行测试")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setFixedSize(800, 600)

        main_layout = QVBoxLayout(self)
        btn_layout = QHBoxLayout()

        self.run_btn = QPushButton("开始运行测试")
        btn_layout.addWidget(self.run_btn)
        btn_layout.addStretch()

        self.log_edit = QPlainTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setPlaceholderText("运行日志将显示在此处...")

        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.log_edit)

        self.run_btn.clicked.connect(self.run_test)

    def run_test(self):
        if not self.project_root or not os.path.exists(self.project_root):
            QMessageBox.warning(self, "警告", "请先打开项目！")
            return
        main_file = os.path.join(self.project_root, "main.py")
        if not os.path.exists(main_file):
            QMessageBox.warning(self, "提示", "未找到 main.py")
            return

        self.log_edit.clear()
        self.run_btn.setEnabled(False)
        original_cwd = os.getcwd()
        os.chdir(self.project_root)

        try:
            process = subprocess.Popen(
                ["python", "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="ignore"
            )
            self.log_edit.appendPlainText("=== 开始运行 ===\n")
            while process.poll() is None:
                line = process.stdout.readline()
                if line:
                    self.log_edit.appendPlainText(line.strip())
                    QApplication.processEvents()
            if process.returncode == 0:
                self.log_edit.appendPlainText("\n=== 运行完成 ===")
            else:
                self.log_edit.appendPlainText("\n=== 运行异常 ===")
        except Exception as e:
            self.log_edit.appendPlainText(f"错误：{e}")
        finally:
            os.chdir(original_cwd)
            self.run_btn.setEnabled(True)

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("使用帮助")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setFixedSize(1350, 850)
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(30, 30, 20, 30)
        left_layout.setSpacing(12)
        left_title = QLabel("🪟 软件使用说明")
        left_title.setFont(QFont("Microsoft YaHei", 20, QFont.Bold))
        left_layout.addWidget(left_title)
        left_line = QFrame()
        left_line.setFrameShape(QFrame.HLine)
        left_layout.addWidget(left_line)
        self.left_text = QTextEdit()
        self.left_text.setReadOnly(True)
        self.load_md_file("help_left.md", self.left_text)
        left_layout.addWidget(self.left_text)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(20, 30, 30, 30)
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
        self.load_md_file("help_right.md", self.right_text)
        right_layout.addWidget(self.right_text)

        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(right_widget, 1)

    def load_md_file(self, filename, text_edit):
        path = resource_path(filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                text_edit.setMarkdown(f.read())
        except:
            text_edit.setText("加载失败")

    def _copy_template(self):
        QApplication.clipboard().setText(self.right_text.toPlainText())
        self.copy_btn.setText("✅ 已复制")
        self.copy_btn.setEnabled(False)

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
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(1)
        self.splitter.setChildrenCollapsible(False)

        self.left_container = QWidget()
        self.left_layout = QVBoxLayout(self.left_container)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(0)

        self.project_title_bar = QWidget()
        self.project_title_bar.setObjectName("ProjectTitleBar")
        title_bar_layout = QHBoxLayout(self.project_title_bar)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
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

    def _create_actions(self):
        def icon(name):
            return QIcon(resource_path(f"icons/{name}.png"))

        self.action_set_dir = QAction(icon("project"), "项目目录", self)
        self.action_set_dir.setShortcut("Ctrl+Shift+O")
        self.action_set_dir.triggered.connect(self.set_project_dir)

        self.action_rename_project = QAction(icon("re_project"), "项目重命名", self)
        self.action_rename_project.setShortcut("Ctrl+F2")
        self.action_rename_project.triggered.connect(self.rename_project)

        self.action_new_file = QAction(icon("file"), "新建文件", self)
        self.action_new_file.setShortcut("Ctrl+N")
        self.action_new_file.triggered.connect(lambda: self.file_tree._create_file(self.project_root))

        self.action_new_folder = QAction(icon("folder"), "新建文件夹", self)
        self.action_new_folder.setShortcut("Ctrl+Shift+F")
        self.action_new_folder.triggered.connect(lambda: self.file_tree._create_folder(self.project_root))

        self.action_rename_item = QAction(icon("rename"), "文件重命名", self)
        self.action_rename_item.setShortcut(Qt.Key_F2)
        self.action_rename_item.triggered.connect(lambda: self.file_tree.edit(self.file_tree.currentIndex()))

        self.action_delete = QAction(icon("delete"), "删除", self)
        self.action_delete.setShortcut("Delete")
        self.action_delete.triggered.connect(self.file_tree._delete_selected_items)

        self.action_batch_write = QAction(icon("batch"), "批量写入", self)
        self.action_batch_write.setShortcut("Ctrl+G")
        self.action_batch_write.triggered.connect(self.batch_modify)

        self.action_close_proj = QAction(icon("close"), "关闭项目", self)
        self.action_close_proj.setShortcut("Ctrl+Q")
        self.action_close_proj.triggered.connect(self.close_project)

        self.action_undo = QAction(icon("undo"), "撤销", self)
        self.action_undo.setShortcut("Ctrl+Z")
        self.action_undo.triggered.connect(self.editor.undo)

        self.action_redo = QAction(icon("redo"), "重做", self)
        self.action_redo.setShortcut("Ctrl+Y")
        self.action_redo.triggered.connect(self.editor.redo)

        self.action_save = QAction(icon("save"), "保存", self)
        self.action_save.setShortcut("Ctrl+S")
        self.action_save.triggered.connect(self.save_file)

        self.action_help = QAction(icon("help"), "使用帮助", self)
        self.action_help.setShortcut(Qt.Key_F1)
        self.action_help.triggered.connect(self.show_help)

        self.action_export_json = QAction(icon("export"), "批量导出", self)
        self.action_export_json.setShortcut("Ctrl+E")
        self.action_export_json.triggered.connect(self.open_export_json_dialog)

        self.action_package_exe = QAction(icon("package"), "打包为EXE", self)
        self.action_package_exe.setShortcut("Ctrl+B")
        self.action_package_exe.triggered.connect(self.open_package_exe_dialog)

        self.action_run_test = QAction(icon("test"), "运行测试", self)
        self.action_run_test.setShortcut("Ctrl+R")
        self.action_run_test.triggered.connect(self.open_run_test_dialog)

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
        self.toolbar.addAction(self.action_export_json)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_package_exe)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_run_test)
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
        menu_tools.addSeparator()
        menu_tools.addAction(self.action_export_json)
        menu_tools.addAction(self.action_package_exe)
        menu_tools.addAction(self.action_run_test)

        menu_help = bar.addMenu("帮助")
        menu_help.addAction(self.action_help)

    def rename_project(self):
        if not self.project_root:
            return
        old = os.path.basename(self.project_root)
        new_name, ok = QInputDialog.getText(self, "重命名项目", "新项目名：", text=old)
        if ok and new_name and new_name != old:
            new_path = os.path.join(os.path.dirname(self.project_root), new_name)
            try:
                os.rename(self.project_root, new_path)
                self.project_root = new_path
                self.file_tree.set_project_root(new_path)
                self.project_title_label.setText(f"📁 {new_name}")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"失败：{e}")

    def set_project_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择项目目录", "./")
        if dir_path:
            self.project_root = dir_path
            self.file_tree.set_project_root(dir_path)
            self.empty_widget.hide()
            self.file_tree.show()
            self.project_title_label.setText(f"📁 {os.path.basename(dir_path)}")
            self._update_ui_state()

    def close_project(self):
        if self.editor.current_file and self.editor.isModified():
            r = QMessageBox.question(self, "保存", "文件已修改，是否保存？")
            if r == QMessageBox.Cancel:
                return
            if r == QMessageBox.Yes:
                self.save_file()
        self.project_root = None
        self.file_tree.clear_project()
        self.editor.clear_editor()
        self.empty_widget.show()
        self.file_tree.hide()
        self.project_title_label.setText("📁 未打开项目")
        self._update_ui_state()

    def open_file(self, file_path):
        if self.editor.current_file and self.editor.isModified():
            r = QMessageBox.question(self, "保存", "当前文件已修改，是否保存？")
            if r == QMessageBox.Cancel:
                return
            if r == QMessageBox.Yes:
                self.save_file()
        self.editor.load_file(file_path)
        self._update_ui_state()

    def save_file(self):
        if self.editor.save_file():
            QMessageBox.information(self, "成功", "保存成功")

    def _on_file_saved(self):
        pass

    def batch_modify(self):
        if not self.project_root:
            QMessageBox.warning(self, "警告", "请先打开项目")
            return
        dlg = QDialog(self)
        dlg.setWindowTitle("批量写入")
        dlg.setFixedSize(800, 600)
        layout = QVBoxLayout(dlg)
        text_edit = QTextEdit()
        text_edit.setPlaceholderText("粘贴JSON格式项目结构")
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        exec_btn = QPushButton("执行批量写入")
        exec_btn.setObjectName("PrimaryButton")
        exec_btn.clicked.connect(lambda: self._exec_batch_write(text_edit.toPlainText(), dlg))
        btn_layout.addWidget(exec_btn)
        layout.addWidget(text_edit)
        layout.addLayout(btn_layout)
        dlg.exec_()

    def _exec_batch_write(self, text, dlg):
        if not text.strip():
            QMessageBox.warning(dlg, "警告", "内容不能为空")
            return
        try:
            data = json.loads(text)
            if "files" not in data:
                QMessageBox.warning(dlg, "错误", "缺少 files 字段")
                return
            ok_cnt = 0
            fail_cnt = 0
            for fi in data["files"]:
                if "path" not in fi or "content" not in fi:
                    fail_cnt += 1
                    continue
                fp = os.path.join(self.project_root, fi["path"])
                dr = os.path.dirname(fp)
                try:
                    os.makedirs(dr, exist_ok=True)
                    with open(fp, "w", encoding="utf-8") as f:
                        f.write(fi["content"])
                    ok_cnt += 1
                except:
                    fail_cnt += 1
            # 修复目录不跳此电脑
            if self.project_root and os.path.exists(self.project_root):
                self.file_tree.set_project_root(self.project_root)
            QMessageBox.information(dlg, "完成", f"成功：{ok_cnt}  失败：{fail_cnt}")
            dlg.accept()
        except json.JSONDecodeError:
            QMessageBox.warning(dlg, "错误", "JSON格式错误")
        except Exception as e:
            QMessageBox.critical(dlg, "错误", str(e))

    def show_help(self):
        HelpDialog(self).exec_()

    def _update_ui_state(self):
        has_proj = self.project_root is not None
        has_file = self.editor.current_file is not None
        self.action_rename_project.setEnabled(has_proj)
        self.action_new_file.setEnabled(has_proj)
        self.action_new_folder.setEnabled(has_proj)
        self.action_rename_item.setEnabled(has_proj)
        self.action_delete.setEnabled(has_proj)
        self.action_batch_write.setEnabled(has_proj)
        self.action_close_proj.setEnabled(has_proj)
        self.action_export_json.setEnabled(has_proj)
        self.action_package_exe.setEnabled(has_proj)
        self.action_run_test.setEnabled(has_proj)
        # 未打开项目时灰态
        self.action_undo.setEnabled(has_proj and has_file)
        self.action_redo.setEnabled(has_proj and has_file)
        self.action_save.setEnabled(has_proj and has_file)

    def open_export_json_dialog(self):
        ExportJsonDialog(self.project_root, self).exec_()

    def open_package_exe_dialog(self):
        PackageExeDialog(self.project_root, self).exec_()

    def open_run_test_dialog(self):
        RunTestDialog(self.project_root, self).exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
