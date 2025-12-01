#!/usr/bin/env python3
"""
文档格式检查脚本

检查 docs/ 目录下所有 Markdown 文件的格式一致性
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

class DocFormatChecker:
    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = Path(docs_dir)
        self.issues = []
    
    def check_all_docs(self) -> List[Tuple[str, List[str]]]:
        """检查所有文档"""
        results = []
        
        for md_file in self.docs_dir.glob("*.md"):
            if md_file.name.startswith("."):
                continue
            
            issues = self.check_single_doc(md_file)
            if issues:
                results.append((str(md_file), issues))
        
        return results
    
    def check_single_doc(self, file_path: Path) -> List[str]:
        """检查单个文档"""
        issues = []
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")
        
        # 检查文件名
        if not self.check_filename(file_path.name):
            issues.append(f"文件名不符合规范：应使用小写字母和下划线")
        
        # 检查一级标题
        h1_count = content.count("\n# ")
        if h1_count == 0:
            issues.append("缺少一级标题")
        elif h1_count > 1:
            issues.append(f"一级标题过多：{h1_count} 个（应该只有 1 个）")
        
        # 检查代码块
        code_blocks = re.findall(r"```(\w*)\n", content)
        for i, lang in enumerate(code_blocks):
            if not lang:
                issues.append(f"代码块 #{i+1} 缺少语言标识符")
        
        # 检查列表格式
        for i, line in enumerate(lines, 1):
            if line.strip().startswith("* "):
                issues.append(f"第 {i} 行：列表应使用 '-' 而非 '*'")
        
        # 检查文件末尾
        if content and not content.endswith("\n"):
            issues.append("文件末尾缺少空行")
        
        return issues
    
    def check_filename(self, filename: str) -> bool:
        """检查文件名格式"""
        # 允许的格式：小写字母、数字、下划线、点号
        pattern = r"^[a-z0-9_.]+\.md$"
        return bool(re.match(pattern, filename))
    
    def print_report(self):
        """打印检查报告"""
        results = self.check_all_docs()
        
        if not results:
            print("✅ 所有文档格式检查通过！")
            return
        
        print(f"⚠️  发现 {len(results)} 个文档存在格式问题：\n")
        
        for file_path, issues in results:
            print(f"📄 {file_path}")
            for issue in issues:
                print(f"   - {issue}")
            print()
        
        print(f"总计：{sum(len(issues) for _, issues in results)} 个问题")

if __name__ == "__main__":
    checker = DocFormatChecker()
    checker.print_report()
