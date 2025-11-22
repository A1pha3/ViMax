# 开发指南

感谢您有兴趣参与 ViMax 的开发！本指南将帮助您了解如何为项目做出贡献。

## 开发环境设置

1.  **Fork 本仓库**: 点击 GitHub 页面右上角的 Fork 按钮。
2.  **克隆代码**:
    ```bash
    git clone https://github.com/YOUR_USERNAME/ViMax.git
    cd ViMax
    ```
3.  **安装依赖**:
    ```bash
    uv sync
    ```
4.  **安装 Pre-commit hooks** (可选但推荐):
    ```bash
    pip install pre-commit
    pre-commit install
    ```

## 代码结构

- `main_*.py`: 入口脚本。
- `pipelines/`: 核心业务逻辑流水线。
- `agents/`: 智能体实现。
- `tools/`: 外部工具封装。
- `configs/`: 配置文件。

## 添加新的智能体 (Agent)

1.  在 `agents/` 目录下创建一个新的 Python 文件。
2.  定义一个类，通常需要包含 `__init__` 和异步的 `__call__` 或处理方法。
3.  在 `agents/__init__.py` 中导出该类。
4.  在 Pipeline 中引入并使用。

## 添加新的工具 (Tool)

1.  在 `tools/` 目录下创建新文件。
2.  实现工具类，确保接口与现有工具保持一致（例如 `generate_image` 方法的签名）。
3.  在配置文件中支持通过 `class_path` 加载该工具。

## 提交代码

1.  创建一个新的分支: `git checkout -b feature/my-new-feature`
2.  提交更改: `git commit -am 'Add some feature'`
3.  推送到分支: `git push origin feature/my-new-feature`
4.  提交 Pull Request

## 代码风格

- 请遵循 PEP 8 编码规范。
- 变量命名请使用清晰的英文单词。
- 关键函数和类请添加 Docstring 注释。

## 反馈与交流

如果您有任何想法或建议，欢迎在 GitHub Issues 中提出，或加入我们的交流群讨论。
