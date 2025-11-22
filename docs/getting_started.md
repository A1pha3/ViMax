# 快速开始

本指南将帮助您快速搭建 ViMax 环境并生成您的第一个视频。

## 环境要求

- **操作系统**: Linux 或 Windows (macOS 也支持，但需自行处理部分依赖)
- **Python**: 3.12+
- **包管理器**: 推荐使用 [uv](https://github.com/astral-sh/uv) 进行依赖管理

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/HKUDS/ViMax.git
cd ViMax
```

### 2. 安装依赖

我们使用 `uv` 来管理环境，它比 pip 更快且更可靠。

```bash
# 安装 uv (如果尚未安装)
# 参考: https://docs.astral.sh/uv/getting-started/installation/

# 同步依赖
uv sync
```

## 配置

ViMax 使用 YAML 文件进行配置。在使用之前，您需要配置模型 API 密钥。

### Idea2Video 配置

复制或修改 `configs/idea2video.yaml` 文件：

```yaml
chat_model:
  init_args:
    model: google/gemini-2.5-flash-lite-preview-09-2025 # 或其他支持的模型
    model_provider: openai
    api_key: <YOUR_API_KEY>
    base_url: https://openrouter.ai/api/v1 # 如果使用 OpenRouter

image_generator:
  class_path: tools.ImageGeneratorNanobananaGoogleAPI
  init_args:
    api_key: <YOUR_API_KEY>

video_generator:
  class_path: tools.VideoGeneratorVeoGoogleAPI
  init_args:
    api_key: <YOUR_API_KEY>

working_dir: .working_dir/idea2video
```

> **注意**: 配置文件中的 `api_key` 字段默认为空，**您必须填入有效的 API Key** 才能运行程序。
> - Google API Key: 用于 Gemini 和 Veo。
> - OpenRouter API Key: 如果使用 OpenRouter 访问 LLM。
> - 云雾 API Key: 如果使用云雾提供的服务。

## 运行示例

### 1. 创意生成视频 (Idea2Video)

编辑 `main_idea2video.py` 文件，设置您的创意：

```python
idea = """
一只猫和一只狗是最好的朋友，当它们遇到一只新来的猫时会发生什么？
"""

user_requirement = """
面向儿童观众，不超过3个场景。
"""

style = "Cartoon" # 风格：卡通
```

运行脚本：

```bash
python main_idea2video.py
```

### 2. 剧本生成视频 (Script2Video)

如果您已有剧本，可以使用 `main_script2video.py`。首先配置 `configs/script2video.yaml`，然后编辑脚本中的 `script` 变量：

```python
script = """
EXT. SCHOOL GYM - DAY
A group of students are practicing basketball...
"""
```

运行脚本：

```bash
python main_script2video.py
```

## 输出结果

生成的视频和中间产物（分镜图、剧本等）将保存在 `working_dir` 指定的目录中（默认为 `.working_dir/`）。
