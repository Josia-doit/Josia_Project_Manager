import os
import re

class StructureParser:
    @staticmethod
    def parse(text):
        # 1. 预处理：统一换行符，清理多余空白
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # 2. 智能分割：无换行文本自动补全换行，兼容一行式结构
        if '\n' not in text:
            text = re.sub(r'(?=├──|└──|-- |- |├──|└──)', r'\n', text)
            text = text.strip()

        lines = text.split('\n')
        paths = []
        stack = []
        top_level_dir = None # 记录AI给的最外层根目录名
        
        for line in lines:
            original_line = line.strip()
            if not original_line:
                continue
                
            # 计算缩进层级
            indent = len(line) - len(line.lstrip(' │├└─'))
            
            # 【彻底修复】清除所有前缀符号：长破折号、短破折号、树形符号、空格
            # 匹配所有开头的非文件名符号，直到遇到第一个有效字符（字母/数字/中文/下划线/点）
            name = re.sub(r'^[\s│├└─-]+', '', original_line)
            # 移除路径末尾的斜杠，统一格式
            name = name.rstrip('/\\')
            
            if not name:
                continue

            # 记录最外层的根目录名
            if indent == 0 and not top_level_dir:
                top_level_dir = name

            # 拼接完整路径
            while stack and stack[-1][0] >= indent:
                stack.pop()
            
            current_path = os.path.join(stack[-1][1], name) if stack else name
            paths.append(current_path)
            stack.append((indent, current_path))
        
        # 【核心优化】剥离外层根目录，返回根目录名+内部路径
        inner_paths = paths
        if top_level_dir and len(paths) > 0:
            # 提取所有路径的最顶层节点
            top_items = set(p.split(os.sep)[0] for p in paths)
            # 如果所有内容都在同一个外层目录里，剥离这一层
            if len(top_items) == 1:
                new_paths = []
                for p in paths:
                    if len(p) > len(top_level_dir) + len(os.sep):
                        new_paths.append(p[len(top_level_dir)+len(os.sep):])
                    elif p == top_level_dir and '.' in top_level_dir:
                        new_paths.append(p)
                inner_paths = new_paths
        
        # 返回：(内部文件路径列表, AI给的根目录名)
        return inner_paths, top_level_dir
