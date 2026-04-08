from PyQt5.QtWidgets import (QTreeView, QFileSystemModel, QMenu, QAction, QInputDialog, 
                             QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt5.QtCore import QModelIndex, Qt, pyqtSignal, QDir
from PyQt5.QtGui import QKeyEvent, QFont
import os
import shutil

# 文件夹选择对话框（仅显示目录，支持新建/重命名/删除）
class FolderSelectDialog(QDialog):
    def __init__(self, root_path, parent=None):
        super().__init__(parent)
        self.root_path = root_path
        self.selected_path = None
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("选择目标文件夹")
        self.resize(500, 600)
        layout = QVBoxLayout(self)
        # 文件夹树
        self.model = QFileSystemModel()
        self.model.setRootPath(self.root_path)
        self.model.setFilter(QDir.Dirs | QDir.NoDotAndDotDot) # 只显示文件夹，不显示文件
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.root_path))
        self.tree.setHeaderHidden(True)
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)
        self.tree.setEditTriggers(QTreeView.NoEditTriggers)
        layout.addWidget(self.tree)
        # 按钮栏
        btn_layout = QHBoxLayout()
        
        # 新建文件夹
        self.new_btn = QPushButton("新建文件夹")
        self.new_btn.clicked.connect(self._create_folder)
        btn_layout.addWidget(self.new_btn)
        # 重命名
        self.rename_btn = QPushButton("重命名")
        self.rename_btn.clicked.connect(self._rename_folder)
        btn_layout.addWidget(self.rename_btn)
        # 删除
        self.delete_btn = QPushButton("删除")
        self.delete_btn.clicked.connect(self._delete_folder)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addStretch()
        # 确认/取消
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        self.confirm_btn = QPushButton("确认移动")
        self.confirm_btn.setStyleSheet("background-color: #3b82f6; color: white;")
        self.confirm_btn.clicked.connect(self._confirm_select)
        btn_layout.addWidget(self.confirm_btn)
        layout.addLayout(btn_layout)

    # 获取当前选中的文件夹路径
    def _get_selected_path(self):
        index = self.tree.currentIndex()
        if not index.isValid():
            return self.root_path
        path = self.model.filePath(index)
        return path if os.path.isdir(path) else os.path.dirname(path)

    # 新建文件夹
    def _create_folder(self):
        base_path = self._get_selected_path()
        name, ok = QInputDialog.getText(self, "新建文件夹", "请输入文件夹名:")
        if ok and name:
            full_path = os.path.join(base_path, name)
            try:
                os.makedirs(full_path, exist_ok=True)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"创建失败: {str(e)}")

    # 重命名文件夹
    def _rename_folder(self):
        old_path = self._get_selected_path()
        if old_path == self.root_path:
            QMessageBox.warning(self, "提示", "不能重命名项目根目录")
            return
        
        old_name = os.path.basename(old_path)
        new_name, ok = QInputDialog.getText(self, "重命名", "请输入新的文件夹名:", text=old_name)
        if ok and new_name and new_name != old_name:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            try:
                os.rename(old_path, new_path)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"重命名失败: {str(e)}")

    # 删除文件夹
    def _delete_folder(self):
        del_path = self._get_selected_path()
        if del_path == self.root_path:
            QMessageBox.warning(self, "提示", "不能删除项目根目录")
            return
        
        # 检查文件夹是否有内容
        has_content = len(os.listdir(del_path)) > 0
        tip = f"确定要永久删除这个文件夹吗？\n{del_path}"
        if has_content:
            tip += "\n\n⚠️  该文件夹内包含文件，删除后无法恢复！"
        
        reply = QMessageBox.question(self, "确认删除", tip, QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                shutil.rmtree(del_path)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"删除失败: {str(e)}")

    # 确认选择
    def _confirm_select(self):
        self.selected_path = self._get_selected_path()
        self.accept()

class FileTree(QTreeView):
    file_opened = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_root = None
        self.model = QFileSystemModel()
        self.model.setReadOnly(False)
        self.setModel(self.model)
        
        # 界面美化
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        self.setHeaderHidden(True)
        self.setEditTriggers(QTreeView.EditKeyPressed)
        self.setFocusPolicy(Qt.StrongFocus)
        
        # 多选模式
        self.setSelectionMode(QTreeView.ExtendedSelection)
        self.setSelectionBehavior(QTreeView.SelectRows)
        
        # 拖拽功能配置
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QTreeView.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        
        # 事件绑定
        self.clicked.connect(self._on_click)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    # 设置项目根目录
    def set_project_root(self, path):
        self.project_root = path
        self.model.setRootPath(path)
        self.setRootIndex(self.model.index(path))
        self.show()

    # 关闭项目时清空（修复占用：强化清空）
    def clear_project(self):
        self.project_root = None
        self.setRootIndex(QModelIndex())
        self.model.setRootPath("")
        self.model.beginResetModel()
        self.model.endResetModel()
        self.hide()

    # 单击打开文件，文件夹自动展开/折叠
    def _on_click(self, index: QModelIndex):
        path = self.model.filePath(index)
        if os.path.isfile(path):
            self.file_opened.emit(path)
        elif os.path.isdir(path):
            self.expand(index) if not self.isExpanded(index) else self.collapse(index)

    # 捕获Delete键，一键删除选中项
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Delete:
            self._delete_selected_items()
        else:
            super().keyPressEvent(event)

    # 拖拽事件：判断落点，移动文件
    def dropEvent(self, event):
        if not self.project_root:
            event.ignore()
            return
        
        target_index = self.indexAt(event.pos())
        target_path = self.model.filePath(target_index)
        
        if os.path.isfile(target_path):
            target_path = os.path.dirname(target_path)
        
        if not os.path.isdir(target_path) or not target_path.startswith(self.project_root):
            event.ignore()
            return
        
        source_paths = self._get_selected_paths()
        if not source_paths:
            event.ignore()
            return
        
        for src in source_paths:
            if src == self.project_root or target_path.startswith(src):
                QMessageBox.warning(self, "提示", "不能将文件夹移动到自身或其子目录中")
                event.ignore()
                return
        
        reply = QMessageBox.question(
            self, "确认移动", 
            f"确定要将选中的 {len(source_paths)} 个项移动到\n{target_path} 吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            fail_count = 0
            for src in source_paths:
                try:
                    dest = os.path.join(target_path, os.path.basename(src))
                    if os.path.exists(dest):
                        cover_reply = QMessageBox.question(
                            self, "文件已存在", 
                            f"{os.path.basename(src)} 已存在，是否覆盖？",
                            QMessageBox.Yes | QMessageBox.No
                        )
                        if cover_reply == QMessageBox.No:
                            continue
                        if os.path.isfile(dest):
                            os.remove(dest)
                        else:
                            shutil.rmtree(dest)
                    
                    shutil.move(src, dest)
                except Exception:
                    fail_count += 1
            
            if fail_count > 0:
                QMessageBox.warning(self, "提示", f"移动完成，有 {fail_count} 个项移动失败")
        
        event.accept()

    # 拖拽进入事件
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and self.project_root:
            event.acceptProposedAction()
        else:
            event.ignore()

    # 拖拽移动事件
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls() and self.project_root:
            event.acceptProposedAction()
        else:
            event.ignore()

    # 右键菜单
    def _show_context_menu(self, position):
        index = self.indexAt(position)
        selected_paths = self._get_selected_paths()
        
        menu = QMenu()
        
        action_new_file = QAction("新建文件", self)
        action_new_file.triggered.connect(lambda: self._create_file(self._get_click_base_path(index)))
        menu.addAction(action_new_file)
        
        action_new_folder = QAction("新建文件夹", self)
        action_new_folder.triggered.connect(lambda: self._create_folder(self._get_click_base_path(index)))
        menu.addAction(action_new_folder)
        
        if index.isValid():
            action_rename = QAction("重命名 (F2)", self)
            action_rename.triggered.connect(lambda: self.edit(index))
            menu.addAction(action_rename)
        
        if selected_paths:
            menu.addSeparator()
            action_move = QAction("移动到...", self)
            action_move.triggered.connect(lambda: self._move_selected_items(selected_paths))
            menu.addAction(action_move)
            
            menu.addSeparator()
            action_delete = QAction(f"删除选中的 {len(selected_paths)} 个项", self)
            action_delete.triggered.connect(self._delete_selected_items)
            menu.addAction(action_delete)
        
        menu.exec_(self.viewport().mapToGlobal(position))

    # 右键移动选中的文件
    def _move_selected_items(self, source_paths):
        if not source_paths or not self.project_root:
            return
        
        dlg = FolderSelectDialog(self.project_root, self)
        if dlg.exec_() == QDialog.Accepted:
            target_path = dlg.selected_path
            if not target_path or not os.path.isdir(target_path):
                return
            
            for src in source_paths:
                if src == self.project_root or target_path.startswith(src):
                    QMessageBox.warning(self, "提示", "不能将文件夹移动到自身或其子目录中")
                    return
            
            fail_count = 0
            for src in source_paths:
                try:
                    dest = os.path.join(target_path, os.path.basename(src))
                    if os.path.exists(dest):
                        cover_reply = QMessageBox.question(
                            self, "文件已存在", 
                            f"{os.path.basename(src)} 已存在，是否覆盖？",
                            QMessageBox.Yes | QMessageBox.No
                        )
                        if cover_reply == QMessageBox.No:
                            continue
                        if os.path.isfile(dest):
                            os.remove(dest)
                        else:
                            shutil.rmtree(dest)
                    
                    shutil.move(src, dest)
                except Exception:
                    fail_count += 1
            
            if fail_count > 0:
                QMessageBox.warning(self, "提示", f"移动完成，有 {fail_count} 个项移动失败")

    # 获取所有选中的路径
    def _get_selected_paths(self):
        indexes = self.selectedIndexes()
        paths = []
        for index in indexes:
            if index.column() == 0:
                path = self.model.filePath(index)
                if path and path != self.project_root:
                    paths.append(path)
        return list(set(paths))

    # 获取右键点击的基础路径
    def _get_click_base_path(self, index):
        path = self.model.filePath(index)
        if not path or not os.path.exists(path):
            return self.project_root
        if os.path.isfile(path):
            return os.path.dirname(path)
        return path

    # 批量删除
    def _delete_selected_items(self):
        paths = self._get_selected_paths()
        if not paths:
            return
        
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要永久删除选中的 {len(paths)} 个项吗？此操作无法撤销！",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            fail_count = 0
            for path in paths:
                try:
                    if os.path.isfile(path):
                        os.remove(path)
                    else:
                        shutil.rmtree(path)
                except Exception:
                    fail_count += 1
            
            if fail_count > 0:
                QMessageBox.warning(self, "提示", f"删除完成，有 {fail_count} 个项删除失败")

    # 新建文件
    def _create_file(self, base_path):
        if not self.project_root:
            return
        if os.path.isfile(base_path):
            base_path = os.path.dirname(base_path)
            
        name, ok = QInputDialog.getText(self, "新建文件", "请输入文件名:")
        if ok and name:
            full_path = os.path.join(base_path, name)
            try:
                with open(full_path, 'w', encoding='utf-8') as f:
                    pass
            except Exception as e:
                QMessageBox.warning(self, "错误", f"创建失败: {str(e)}")

    # 新建文件夹
    def _create_folder(self, base_path):
        if not self.project_root:
            return
        if os.path.isfile(base_path):
            base_path = os.path.dirname(base_path)
            
        name, ok = QInputDialog.getText(self, "新建文件夹", "请输入文件夹名:")
        if ok and name:
            full_path = os.path.join(base_path, name)
            try:
                os.makedirs(full_path, exist_ok=True)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"创建失败: {str(e)}")

    # 允许项可编辑（重命名关键）
    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return super().flags(index) | Qt.ItemIsEditable
