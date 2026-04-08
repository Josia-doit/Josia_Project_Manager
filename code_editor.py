import os
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciLexerJavaScript, QsciLexerHTML, QsciLexerCSS, QsciLexerJSON
from PyQt5.QtGui import QFont, QKeySequence, QColor
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QShortcut

class CodeEditor(QsciScintilla):
    file_saved = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file = None
        self._setup_editor()
        self._setup_shortcuts()

    def _setup_editor(self):
        # 字体设置
        font = QFont('Consolas', 10)
        font.setFixedPitch(True)
        self.setFont(font)
        self.setMarginsFont(font)
        
        # 行号设置
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "0000")
        self.setMarginsForegroundColor(QColor("#888888"))
        self.setMarginsBackgroundColor(QColor("#f8f9fa"))
        
        # 缩进设置
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        self.setAutoIndent(True)
        self.setBackspaceUnindents(True)
        
        # 代码折叠
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        self.setFoldMarginColors(QColor("#f8f9fa"), QColor("#ffffff"))
        
        # 当前行高亮
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#f0f4f8"))
        
        # 编辑器背景与文本颜色
        self.setPaper(QColor("#ffffff"))
        self.setColor(QColor("#2d3748"))
        
        # 滚动条样式适配
        self.SendScintilla(QsciScintilla.SCI_SETVSCROLLBAR, True)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, True)

    # 根据文件后缀自动切换语法高亮
    def _set_lexer_by_file(self, file_path):
        suffix = os.path.splitext(file_path)[1].lower()
        font = self.font()
        
        lexer_map = {
            '.py': QsciLexerPython,
            '.js': QsciLexerJavaScript,
            '.html': QsciLexerHTML,
            '.css': QsciLexerCSS,
            '.json': QsciLexerJSON
        }
        
        lexer_class = lexer_map.get(suffix)
        if lexer_class:
            lexer = lexer_class()
            lexer.setFont(font)
            lexer.setDefaultFont(font)
            lexer.setDefaultColor(QColor("#2d3748"))
            lexer.setPaper(QColor("#ffffff"))
            self.setLexer(lexer)
        else:
            self.setLexer(None)

    # 编辑器内快捷键（仅焦点在编辑器时生效）
    def _setup_shortcuts(self):
        self.undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.undo_shortcut.activated.connect(self.undo)
        
        self.redo_shortcut = QShortcut(QKeySequence("Ctrl+Y"), self)
        self.redo_shortcut.activated.connect(self.redo)

    def load_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.setText(f.read())
            self.current_file = file_path
            self._set_lexer_by_file(file_path)
            self.setModified(False)
        except Exception as e:
            print(f"打开失败: {e}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.text())
                self.setModified(False)
                self.file_saved.emit()
                return True
            except Exception as e:
                print(f"保存失败: {e}")
        return False

    # 强化清空：确保释放文件
    def clear_editor(self):
        self.setText("")
        self.current_file = None
        self.setLexer(None)
        self.setModified(False)
