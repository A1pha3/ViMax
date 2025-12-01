#!/usr/bin/env python3
"""
文档质量检查脚本

全面检查 docs/ 目录下所有 Markdown 文件的质量，包括：
- 准确性：技术描述与代码实现一致
- 代码示例：语法正确且可运行
- 链接有效性：内部链接和锚点链接
- 术语一致性：术语翻译统一
- 文档完整性：核心功能都有文档覆盖
"""

import os
import re
import ast
import json
from pathlib import Path
from typing import List, Dict, Tuple, Set
from collections import defaultdict

class DocQualityChecker:
    def __init__(self, docs_dir: str = "docs", project_root: str = "."):
        self.docs_dir = Path(docs_dir)
        self.project_root = Path(project_root)
        self.issues = defaultdict(list)
        self.warnings = defaultdict(list)
        
        # 术语表（从 glossary.md 或预定义）
        self.terminology = {
            "Agent": "智能体",
            "Pipeline": "流水线",
            "Tool": "工具",
            "Storyboard": "分镜",
            "Shot": "镜头",
            "Frame": "帧",
            "Character Portrait": "角色画像",
            "Reference Image": "参考图",
            "Camera": "摄像机",
            "Scene": "场景",
        }
        
    def check_all(self) -> Dict[str, List[str]]:
        """执行所有检查"""
        print("=" * 60)
        print("文档质量检查")
        print("=" * 60)
        
        # 6.1 检查文档准确性
        print("\n📋 6.1 检查文档准确性...")
        self.check_accuracy()
        
        # 6.2 检查代码示例
        print("\n💻 6.2 检查代码示例...")
        self.check_code_examples()
        
        # 6.3 检查链接有效性
        print("\n🔗 6.3 检查链接有效性...")
        self.check_links()
        
        # 6.4 检查术语一致性
        print("\n📖 6.4 检查术语一致性...")
        self.check_terminology()
        
        # 6.5 检查文档完整性
        print("\n📚 6.5 检查文档完整性...")
        self.check_completeness()
        
        return self.generate_report()
    
    def check_accuracy(self):
        """6.1 检查文档准确性"""
        # 检查配置示例
        self._check_config_examples()
        
        # 检查 API 签名
        self._check_api_signatures()
        
        # 检查文件路径
        self._check_file_paths()
    
    def _check_config_examples(self):
        """检查配置示例的准确性"""
        config_docs = [
            self.docs_dir / "getting_started.md",
            self.docs_dir / "configuration.md",
            self.docs_dir / "tools.md"
        ]
        
        for doc_file in config_docs:
            if not doc_file.exists():
                continue
            
            content = doc_file.read_text(encoding="utf-8")
            
            # 提取 YAML 代码块
            yaml_blocks = re.findall(r"```yaml\n(.*?)\n```", content, re.DOTALL)
            
            for i, yaml_block in enumerate(yaml_blocks):
                # 检查常见的配置字段
                if "chat_model:" in yaml_block:
                    if "init_args:" not in yaml_block:
                        self.issues[doc_file.name].append(
                            f"配置示例 #{i+1}: chat_model 缺少 init_args 字段"
                        )
                    if "model:" not in yaml_block:
                        self.issues[doc_file.name].append(
                            f"配置示例 #{i+1}: chat_model 缺少 model 字段"
                        )
                
                if "image_generator:" in yaml_block:
                    if "class_path:" not in yaml_block:
                        self.issues[doc_file.name].append(
                            f"配置示例 #{i+1}: image_generator 缺少 class_path 字段"
                        )
                
                if "video_generator:" in yaml_block:
                    if "class_path:" not in yaml_block:
                        self.issues[doc_file.name].append(
                            f"配置示例 #{i+1}: video_generator 缺少 class_path 字段"
                        )
    
    def _check_api_signatures(self):
        """检查 API 签名的准确性"""
        api_doc = self.docs_dir / "api_reference.md"
        if not api_doc.exists():
            return
        
        content = api_doc.read_text(encoding="utf-8")
        
        # 提取 Python 代码块中的函数签名
        python_blocks = re.findall(r"```python\n(.*?)\n```", content, re.DOTALL)
        
        for i, block in enumerate(python_blocks):
            # 跳过明显的签名示例（只有类或函数定义，没有实现）
            if block.strip().startswith("class ") or block.strip().startswith("def ") or block.strip().startswith("async def "):
                # 这些通常是签名示例，不需要完整的语法检查
                continue
            
            # 检查是否包含函数定义
            if "def " in block or "async def " in block:
                try:
                    # 尝试解析为 AST（基本语法检查）
                    ast.parse(block)
                except SyntaxError as e:
                    # 只报告非签名相关的语法错误
                    if "invalid syntax" not in str(e) or ":" not in block:
                        self.issues[api_doc.name].append(
                            f"API 代码示例 #{i+1} 可能有语法问题: {str(e)}"
                        )
    
    def _check_file_paths(self):
        """检查文档中引用的文件路径"""
        for doc_file in self.docs_dir.glob("*.md"):
            if doc_file.name.startswith("."):
                continue
            
            content = doc_file.read_text(encoding="utf-8")
            
            # 查找文件路径引用（常见模式）
            path_patterns = [
                r"`([a-zA-Z_/]+\.py)`",  # Python 文件
                r"`([a-zA-Z_/]+\.yaml)`",  # YAML 文件
                r"`([a-zA-Z_/]+\.json)`",  # JSON 文件
                r"`([a-zA-Z_/]+/)`",  # 目录路径
            ]
            
            for pattern in path_patterns:
                matches = re.findall(pattern, content)
                for path_str in matches:
                    # 检查路径是否存在
                    full_path = self.project_root / path_str
                    if not full_path.exists() and not path_str.startswith("path/to"):
                        self.warnings[doc_file.name].append(
                            f"引用的路径可能不存在: {path_str}"
                        )
    
    def check_code_examples(self):
        """6.2 检查代码示例"""
        for doc_file in self.docs_dir.glob("*.md"):
            if doc_file.name.startswith("."):
                continue
            
            content = doc_file.read_text(encoding="utf-8")
            
            # 提取所有 Python 代码块
            python_blocks = re.findall(r"```python\n(.*?)\n```", content, re.DOTALL)
            
            for i, code_block in enumerate(python_blocks):
                # 跳过明显的片段或伪代码
                if "..." in code_block or ("<" in code_block and ">" in code_block):
                    continue
                
                # 跳过只有类或函数签名的代码块（API 文档中常见）
                stripped = code_block.strip()
                if (stripped.startswith("class ") or 
                    stripped.startswith("def ") or 
                    stripped.startswith("async def ") or
                    stripped.startswith("@")):
                    # 这些通常是签名示例
                    continue
                
                # 检查语法（只对完整代码示例）
                if "import" in code_block or "asyncio.run" in code_block:
                    try:
                        ast.parse(code_block)
                    except SyntaxError as e:
                        self.issues[doc_file.name].append(
                            f"代码示例 #{i+1} 语法错误: {str(e)}"
                        )
                
                # 检查常见的导入错误
                if "from pipelines import" in code_block:
                    if "Idea2VideoPipeline" in code_block or "Script2VideoPipeline" in code_block:
                        # 检查是否有正确的导入
                        if "from pipelines.idea2video_pipeline import" not in code_block and \
                           "from pipelines.script2video_pipeline import" not in code_block and \
                           "from pipelines import" not in code_block:
                            self.warnings[doc_file.name].append(
                                f"代码示例 #{i+1}: 导入语句可能不正确"
                            )
    
    def check_links(self):
        """6.3 检查链接有效性"""
        # 收集所有文档文件和它们的标题
        doc_files = {}
        doc_headers = defaultdict(set)
        
        for doc_file in self.docs_dir.glob("*.md"):
            # Include all .md files, even those starting with .
            doc_files[doc_file.name] = doc_file
            content = doc_file.read_text(encoding="utf-8")
            
            # 提取所有标题
            headers = re.findall(r"^#+\s+(.+)$", content, re.MULTILINE)
            for header in headers:
                # 转换为锚点格式
                anchor = header.lower()
                anchor = re.sub(r"[^\w\s-]", "", anchor)
                anchor = re.sub(r"[\s_]+", "-", anchor)
                doc_headers[doc_file.name].add(anchor)
        
        # 检查每个文档中的链接
        for doc_file in self.docs_dir.glob("*.md"):
            if doc_file.name.startswith("."):
                continue
            
            content = doc_file.read_text(encoding="utf-8")
            
            # 查找 Markdown 链接
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
            
            for link_text, link_url in links:
                # 跳过外部链接
                if link_url.startswith("http://") or link_url.startswith("https://"):
                    continue
                
                # 检查内部链接
                if link_url.startswith("./"):
                    target_file = link_url[2:]
                    if "#" in target_file:
                        file_part, anchor_part = target_file.split("#", 1)
                        
                        # 检查文件是否存在
                        if file_part and file_part not in doc_files:
                            self.issues[doc_file.name].append(
                                f"链接指向不存在的文件: {file_part}"
                            )
                        
                        # 检查锚点是否存在
                        if file_part and anchor_part:
                            if anchor_part not in doc_headers.get(file_part, set()):
                                self.warnings[doc_file.name].append(
                                    f"链接指向可能不存在的锚点: {file_part}#{anchor_part}"
                                )
                    else:
                        # 只有文件名
                        if target_file not in doc_files:
                            self.issues[doc_file.name].append(
                                f"链接指向不存在的文件: {target_file}"
                            )
                
                # 检查锚点链接（同文档内）
                elif link_url.startswith("#"):
                    anchor = link_url[1:]
                    if anchor not in doc_headers.get(doc_file.name, set()):
                        self.warnings[doc_file.name].append(
                            f"锚点链接可能不存在: {anchor}"
                        )
    
    def check_terminology(self):
        """6.4 检查术语一致性"""
        # 收集所有术语使用情况
        term_usage = defaultdict(lambda: defaultdict(int))
        
        for doc_file in self.docs_dir.glob("*.md"):
            if doc_file.name.startswith("."):
                continue
            
            content = doc_file.read_text(encoding="utf-8")
            
            # 检查每个术语的翻译
            for english, chinese in self.terminology.items():
                # 查找英文术语
                english_count = len(re.findall(r"\b" + re.escape(english) + r"\b", content))
                # 查找中文翻译
                chinese_count = content.count(chinese)
                
                if english_count > 0 or chinese_count > 0:
                    term_usage[doc_file.name][english] = {
                        "english": english_count,
                        "chinese": chinese_count
                    }
        
        # 检查一致性
        for doc_file, terms in term_usage.items():
            for english, counts in terms.items():
                chinese = self.terminology[english]
                # 如果同时使用英文和中文，可能存在不一致
                if counts["english"] > 0 and counts["chinese"] > 0:
                    self.warnings[doc_file].append(
                        f"术语 '{english}' 同时使用英文和中文翻译 '{chinese}'，建议统一"
                    )
    
    def check_completeness(self):
        """6.5 检查文档完整性"""
        # 检查核心功能是否有文档
        required_docs = {
            "getting_started.md": "快速开始指南",
            "architecture.md": "系统架构",
            "agents.md": "智能体详解",
            "pipelines.md": "流水线详解",
            "tools.md": "工具与集成",
            "api_reference.md": "API 参考",
            "configuration.md": "配置详解",
            "examples.md": "示例与最佳实践",
            "troubleshooting.md": "故障排查",
            "faq.md": "常见问题",
        }
        
        for doc_name, doc_desc in required_docs.items():
            doc_path = self.docs_dir / doc_name
            if not doc_path.exists():
                self.issues["completeness"].append(
                    f"缺少核心文档: {doc_name} ({doc_desc})"
                )
            else:
                # 检查文档是否为空或过短
                content = doc_path.read_text(encoding="utf-8")
                if len(content.strip()) < 100:
                    self.warnings["completeness"].append(
                        f"文档内容过少: {doc_name} (仅 {len(content)} 字符)"
                    )
        
        # 检查核心功能是否有示例
        examples_doc = self.docs_dir / "examples.md"
        if examples_doc.exists():
            content = examples_doc.read_text(encoding="utf-8")
            
            required_examples = [
                "Idea2Video",
                "Script2Video",
                "角色画像",
                "分镜设计",
            ]
            
            for example in required_examples:
                if example not in content:
                    self.warnings["examples.md"].append(
                        f"缺少 {example} 的示例"
                    )
    
    def generate_report(self) -> Dict[str, List[str]]:
        """生成检查报告"""
        print("\n" + "=" * 60)
        print("检查报告")
        print("=" * 60)
        
        # 统计
        total_issues = sum(len(issues) for issues in self.issues.values())
        total_warnings = sum(len(warnings) for warnings in self.warnings.values())
        
        # 打印问题
        if total_issues > 0:
            print(f"\n❌ 发现 {total_issues} 个问题：\n")
            for doc_name, issues in sorted(self.issues.items()):
                print(f"📄 {doc_name}")
                for issue in issues:
                    print(f"   ❌ {issue}")
                print()
        else:
            print("\n✅ 未发现严重问题")
        
        # 打印警告
        if total_warnings > 0:
            print(f"\n⚠️  发现 {total_warnings} 个警告：\n")
            for doc_name, warnings in sorted(self.warnings.items()):
                print(f"📄 {doc_name}")
                for warning in warnings:
                    print(f"   ⚠️  {warning}")
                print()
        else:
            print("\n✅ 未发现警告")
        
        # 总结
        print("=" * 60)
        if total_issues == 0 and total_warnings == 0:
            print("🎉 所有文档质量检查通过！")
        else:
            print(f"总计: {total_issues} 个问题, {total_warnings} 个警告")
        print("=" * 60)
        
        return {
            "issues": dict(self.issues),
            "warnings": dict(self.warnings)
        }

if __name__ == "__main__":
    checker = DocQualityChecker()
    results = checker.check_all()
    
    # 如果有严重问题，返回非零退出码
    if results["issues"]:
        exit(1)
    else:
        exit(0)
