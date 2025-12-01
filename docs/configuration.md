# 配置详解

> 本文档详细说明 ViMax 的所有配置选项和参数

## 目录

- [前置知识](#前置知识)
- [配置文件概述](#配置文件概述)
- [配置文件结构](#配置文件结构)
- [chat_model 配置](#chat_model-配置)
- [image_generator 配置](#image_generator-配置)
- [video_generator 配置](#video_generator-配置)
- [working_dir 配置](#working_dir-配置)
- [配置示例](#配置示例)
- [配置验证](#配置验证)
- [故障排查](#故障排查)
- [相关资源](#相关资源)

## 前置知识

在配置 ViMax 之前，建议您先了解：

- [快速开始](./getting_started.md) - 基本的安装和使用
- YAML 文件格式基础
- 您计划使用的 AI 服务（Google、OpenRouter、云雾等）

**配置文件位置**：

- `configs/idea2video.yaml` - Idea2Video 流水线配置
- `configs/script2video.yaml` - Script2Video 流水线配置

## 配置文件概述

ViMax 使用 YAML 格式的配置文件来管理所有运行时参数。每个流水线都有独立的配置文件，但它们的结构是相同的。

### 配置文件的作用

1. **API 密钥管理**: 集中管理所有 API 密钥
2. **模型选择**: 指定使用的语言模型、图像生成器和视频生成器
3. **工作目录**: 设置输出文件的保存位置
4. **参数调整**: 自定义各种生成参数

### 配置文件加载

配置文件在流水线初始化时加载：

```python
from pipelines import Idea2VideoPipeline

# 从配置文件初始化流水线
pipeline = Idea2VideoPipeline.init_from_config(
    config_path="configs/idea2video.yaml"
)
```

## 配置文件结构

完整的配置文件包含四个主要部分：

```yaml
# 1. 对话模型配置
chat_model:
  init_args:
    model: <模型名称>
    model_provider: <提供商类型>
    api_key: <API 密钥>
    base_url: <API 端点>

# 2. 图像生成器配置
image_generator:
  class_path: <工具类路径>
  init_args:
    api_key: <API 密钥>

# 3. 视频生成器配置
video_generator:
  class_path: <工具类路径>
  init_args:
    api_key: <API 密钥>

# 4. 工作目录配置
working_dir: <输出目录路径>
```

---

## chat_model 配置

对话模型用于驱动所有智能体进行推理、创作和决策。

### 配置结构

```yaml
chat_model:
  init_args:
    model: string              # 模型名称
    model_provider: string     # 模型提供商类型
    api_key: string           # API 密钥
    base_url: string          # API 端点地址
```

### 参数详解

#### `model`

指定使用的大语言模型名称。

**类型**: `string`  
**必需**: 是  
**示例**:
- `"google/gemini-2.5-flash-lite-preview-09-2025"` - Google Gemini 模型（通过 OpenRouter）
- `"gemini-2.0-flash-exp"` - Google Gemini 模型（直接访问）
- `"gpt-4o"` - OpenAI GPT-4o
- `"claude-3-5-sonnet-20241022"` - Anthropic Claude

**说明**:
- 模型名称格式取决于使用的提供商
- 通过 OpenRouter 访问时，使用 `提供商/模型名` 格式
- 直接访问时，使用模型的官方名称

#### `model_provider`

指定模型提供商的接口类型。

**类型**: `string`  
**必需**: 是  
**可选值**: `"openai"`  
**默认值**: 无

**说明**:
- 当前仅支持 `"openai"`，表示使用 OpenAI 兼容的 API 接口
- 大多数现代 LLM 服务都提供 OpenAI 兼容接口
- 包括 OpenRouter、云雾 API、Google AI Studio 等

#### `api_key`

API 服务的认证密钥。

**类型**: `string`  
**必需**: 是  
**格式**:
- Google API Key: 通常以 `AIza` 开头
- OpenRouter API Key: 通常以 `sk-or-v1-` 开头
- 云雾 API Key: 通常以 `yw-` 开头
- OpenAI API Key: 通常以 `sk-` 开头

**安全提示**:
- ⚠️ 不要将 API Key 提交到公开仓库
- 建议使用环境变量或密钥管理工具
- 定期轮换 API Key

#### `base_url`

API 服务的基础 URL。

**类型**: `string`  
**必需**: 是  
**常用值**:
- OpenRouter: `https://openrouter.ai/api/v1`
- 云雾 API: `https://api.yunwu.ai/v1`
- Google AI Studio: `https://generativelanguage.googleapis.com/v1beta/openai/`
- OpenAI: `https://api.openai.com/v1`

**说明**:
- 确保 URL 以 `/v1` 结尾（根据服务要求）
- 使用 HTTPS 协议确保安全

### 配置示例

#### 示例 1: 使用 OpenRouter

```yaml
chat_model:
  init_args:
    model: google/gemini-2.5-flash-lite-preview-09-2025
    model_provider: openai
    api_key: sk-or-v1-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    base_url: https://openrouter.ai/api/v1
```

#### 示例 2: 直接使用 Google AI Studio

```yaml
chat_model:
  init_args:
    model: gemini-2.0-flash-exp
    model_provider: openai
    api_key: AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    base_url: https://generativelanguage.googleapis.com/v1beta/openai/
```

#### 示例 3: 使用云雾 API

```yaml
chat_model:
  init_args:
    model: google/gemini-2.5-flash-lite-preview-09-2025
    model_provider: openai
    api_key: yw-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    base_url: https://api.yunwu.ai/v1
```

---

## image_generator 配置

图像生成器用于生成分镜关键帧、角色画像等静态图像。

### 配置结构

```yaml
image_generator:
  class_path: string    # 图像生成工具类的完整路径
  init_args:
    api_key: string     # API 密钥
```

### 参数详解

#### `class_path`

图像生成工具类的完整 Python 路径。

**类型**: `string`  
**必需**: 是  
**可选值**:
- `tools.ImageGeneratorNanobananaGoogleAPI` - Google 图像生成（推荐）
- `tools.ImageGeneratorNanobananaYunwuAPI` - 通过云雾 API 访问 Google
- `tools.ImageGeneratorDoubaoSeedreamYunwuAPI` - 字节豆包图像生成

**说明**:
- 路径格式为 `模块.类名`
- 所有工具类都实现了统一的接口
- 可以通过修改此参数轻松切换不同的图像生成服务

#### `init_args.api_key`

图像生成服务的 API 密钥。

**类型**: `string`  
**必需**: 是

**说明**:
- 不同的 `class_path` 需要不同服务的 API Key
- 确保 API Key 与选择的服务匹配

### 可用的图像生成器

#### ImageGeneratorNanobananaGoogleAPI

使用 Google 的图像生成服务（推荐）。

**特点**:
- 高质量图像生成
- 支持参考图像
- 生成速度快

**配置示例**:

```yaml
image_generator:
  class_path: tools.ImageGeneratorNanobananaGoogleAPI
  init_args:
    api_key: AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

#### ImageGeneratorNanobananaYunwuAPI

通过云雾 API 访问 Google 图像生成服务。

**特点**:
- 国内访问稳定
- 支持国内支付方式
- 与 Google 原生 API 功能相同

**配置示例**:

```yaml
image_generator:
  class_path: tools.ImageGeneratorNanobananaYunwuAPI
  init_args:
    api_key: yw-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

#### ImageGeneratorDoubaoSeedreamYunwuAPI

使用字节豆包的图像生成服务。

**特点**:
- 国内服务，访问快速
- 支持中文提示词
- 适合特定风格需求

**配置示例**:

```yaml
image_generator:
  class_path: tools.ImageGeneratorDoubaoSeedreamYunwuAPI
  init_args:
    api_key: yw-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

---

## video_generator 配置

视频生成器用于将静态图像转换为动态视频片段。

### 配置结构

```yaml
video_generator:
  class_path: string    # 视频生成工具类的完整路径
  init_args:
    api_key: string     # API 密钥
```

### 参数详解

#### `class_path`

视频生成工具类的完整 Python 路径。

**类型**: `string`  
**必需**: 是  
**可选值**:
- `tools.VideoGeneratorVeoGoogleAPI` - Google Veo（推荐，质量最高）
- `tools.VideoGeneratorVeoYunwuAPI` - 通过云雾 API 访问 Veo
- `tools.VideoGeneratorDoubaoSeedanceYunwuAPI` - 字节豆包视频生成

**说明**:
- 路径格式为 `模块.类名`
- 所有工具类都实现了统一的接口
- 可以通过修改此参数轻松切换不同的视频生成服务

#### `init_args.api_key`

视频生成服务的 API 密钥。

**类型**: `string`  
**必需**: 是

### 可用的视频生成器

#### VideoGeneratorVeoGoogleAPI

使用 Google Veo 视频生成服务（推荐）。

**特点**:
- 业界领先的视频质量
- 支持复杂的运动描述
- 生成时间较长但质量最高

**配置示例**:

```yaml
video_generator:
  class_path: tools.VideoGeneratorVeoGoogleAPI
  init_args:
    api_key: AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

#### VideoGeneratorVeoYunwuAPI

通过云雾 API 访问 Google Veo。

**特点**:
- 国内访问稳定
- 与 Google 原生 API 功能相同
- 支持国内支付方式

**配置示例**:

```yaml
video_generator:
  class_path: tools.VideoGeneratorVeoYunwuAPI
  init_args:
    api_key: yw-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

#### VideoGeneratorDoubaoSeedanceYunwuAPI

使用字节豆包的视频生成服务。

**特点**:
- 国内服务，访问快速
- 生成速度较快
- 适合快速原型开发

**配置示例**:

```yaml
video_generator:
  class_path: tools.VideoGeneratorDoubaoSeedanceYunwuAPI
  init_args:
    api_key: yw-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

---

## working_dir 配置

工作目录用于保存所有生成的中间文件和最终输出。

### 配置结构

```yaml
working_dir: string    # 工作目录路径
```

### 参数详解

#### `working_dir`

指定输出文件的保存目录。

**类型**: `string`  
**必需**: 是  
**默认值**:
- Idea2Video: `.working_dir/idea2video`
- Script2Video: `.working_dir/script2video`

**说明**:
- 可以使用相对路径或绝对路径
- 相对路径相对于项目根目录
- 目录会自动创建（如果不存在）
- 确保有足够的磁盘空间（建议至少 10GB）

### 目录结构

工作目录会包含以下内容：

```
.working_dir/idea2video/
├── story.txt                    # 生成的故事
├── script.json                  # 场景剧本
├── characters.json              # 角色信息
├── character_portraits/         # 角色画像
│   ├── 0_Alice/
│   │   ├── front.png
│   │   ├── side.png
│   │   └── back.png
│   └── 1_Bob/
│       ├── front.png
│       ├── side.png
│       └── back.png
├── character_portraits_registry.json  # 画像注册表
├── scene_0/                     # 场景 0 的输出
│   ├── storyboard.json
│   ├── shots.json
│   ├── cameras.json
│   ├── frames/
│   ├── videos/
│   └── final_video.mp4
├── scene_1/                     # 场景 1 的输出
│   └── ...
└── final_video.mp4              # 最终合成视频
```

### 配置示例

#### 示例 1: 使用默认路径

```yaml
working_dir: .working_dir/idea2video
```

#### 示例 2: 使用自定义路径

```yaml
working_dir: /path/to/my/project/output
```

#### 示例 3: 使用项目子目录

```yaml
working_dir: outputs/my_video_project
```

---

## 配置示例

### 完整配置示例

#### 示例 1: 使用 Google 原生 API

```yaml
# configs/idea2video.yaml

chat_model:
  init_args:
    model: gemini-2.0-flash-exp
    model_provider: openai
    api_key: AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    base_url: https://generativelanguage.googleapis.com/v1beta/openai/

image_generator:
  class_path: tools.ImageGeneratorNanobananaGoogleAPI
  init_args:
    api_key: AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

video_generator:
  class_path: tools.VideoGeneratorVeoGoogleAPI
  init_args:
    api_key: AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

working_dir: .working_dir/idea2video
```

#### 示例 2: 使用 OpenRouter + 云雾 API（推荐国内用户）

```yaml
# configs/idea2video.yaml

chat_model:
  init_args:
    model: google/gemini-2.5-flash-lite-preview-09-2025
    model_provider: openai
    api_key: sk-or-v1-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    base_url: https://openrouter.ai/api/v1

image_generator:
  class_path: tools.ImageGeneratorNanobananaYunwuAPI
  init_args:
    api_key: yw-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

video_generator:
  class_path: tools.VideoGeneratorVeoYunwuAPI
  init_args:
    api_key: yw-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

working_dir: .working_dir/idea2video
```

#### 示例 3: 使用字节豆包服务

```yaml
# configs/idea2video.yaml

chat_model:
  init_args:
    model: google/gemini-2.5-flash-lite-preview-09-2025
    model_provider: openai
    api_key: sk-or-v1-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    base_url: https://openrouter.ai/api/v1

image_generator:
  class_path: tools.ImageGeneratorDoubaoSeedreamYunwuAPI
  init_args:
    api_key: yw-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

video_generator:
  class_path: tools.VideoGeneratorDoubaoSeedanceYunwuAPI
  init_args:
    api_key: yw-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

working_dir: .working_dir/idea2video
```

### 不同场景的配置

#### 场景 1: 快速原型开发

优先考虑速度和成本。

```yaml
chat_model:
  init_args:
    model: google/gemini-2.5-flash-lite-preview-09-2025  # 快速模型
    model_provider: openai
    api_key: YOUR_API_KEY
    base_url: https://openrouter.ai/api/v1

image_generator:
  class_path: tools.ImageGeneratorDoubaoSeedreamYunwuAPI  # 快速生成
  init_args:
    api_key: YOUR_API_KEY

video_generator:
  class_path: tools.VideoGeneratorDoubaoSeedanceYunwuAPI  # 快速生成
  init_args:
    api_key: YOUR_API_KEY

working_dir: .working_dir/prototype
```

#### 场景 2: 高质量生产

优先考虑质量。

```yaml
chat_model:
  init_args:
    model: google/gemini-2.5-flash-lite-preview-09-2025
    model_provider: openai
    api_key: YOUR_API_KEY
    base_url: https://openrouter.ai/api/v1

image_generator:
  class_path: tools.ImageGeneratorNanobananaGoogleAPI  # 高质量
  init_args:
    api_key: YOUR_API_KEY

video_generator:
  class_path: tools.VideoGeneratorVeoGoogleAPI  # 最高质量
  init_args:
    api_key: YOUR_API_KEY

working_dir: .working_dir/production
```

---

## 配置验证

### 验证配置文件

在运行之前，建议验证配置文件的正确性。

#### 方法 1: 手动检查

检查以下项目：

1. **YAML 语法**: 确保缩进正确，使用空格而非制表符
2. **API Key**: 确保所有 API Key 已填写且格式正确
3. **路径**: 确保 `class_path` 和 `working_dir` 正确
4. **URL**: 确保 `base_url` 以正确的格式结尾

#### 方法 2: 使用 Python 验证

```python
import yaml

# 加载配置文件
with open("configs/idea2video.yaml", "r") as f:
    config = yaml.safe_load(f)

# 检查必需字段
assert "chat_model" in config
assert "image_generator" in config
assert "video_generator" in config
assert "working_dir" in config

# 检查 API Key
assert config["chat_model"]["init_args"]["api_key"], "Chat model API key is missing"
assert config["image_generator"]["init_args"]["api_key"], "Image generator API key is missing"
assert config["video_generator"]["init_args"]["api_key"], "Video generator API key is missing"

print("✅ 配置文件验证通过")
```

#### 方法 3: 测试 API 连接

```python
import asyncio
from langchain.chat_models import init_chat_model

async def test_chat_model():
    chat_model = init_chat_model(
        model="google/gemini-2.5-flash-lite-preview-09-2025",
        model_provider="openai",
        api_key="YOUR_API_KEY",
        base_url="https://openrouter.ai/api/v1"
    )
    
    response = await chat_model.ainvoke("Hello, this is a test.")
    print(f"✅ Chat model 连接成功: {response.content[:50]}...")

asyncio.run(test_chat_model())
```

---

## 故障排查

### 常见配置错误

#### 错误 1: YAML 语法错误

**症状**:
```
yaml.scanner.ScannerError: mapping values are not allowed here
```

**原因**: YAML 语法错误，通常是缩进问题

**解决方案**:
1. 确保使用空格而非制表符
2. 检查每一层的缩进是否一致（通常为 2 个空格）
3. 确保冒号后有空格

#### 错误 2: API Key 未填写

**症状**:
```
Authentication failed: Invalid API key
```

**原因**: API Key 为空或格式错误

**解决方案**:
1. 检查配置文件中的 `api_key` 字段
2. 确保 API Key 已正确复制（无多余空格）
3. 验证 API Key 是否有效

#### 错误 3: 模型名称错误

**症状**:
```
Model not found: <model_name>
```

**原因**: 模型名称拼写错误或不存在

**解决方案**:
1. 检查模型名称拼写
2. 确认模型在所选服务中可用
3. 参考服务提供商的模型列表

#### 错误 4: 工具类路径错误

**症状**:
```
ModuleNotFoundError: No module named 'tools.XXX'
```

**原因**: `class_path` 配置错误

**解决方案**:
1. 检查 `class_path` 拼写
2. 确保使用正确的格式：`模块.类名`
3. 参考本文档中的可用工具列表

#### 错误 5: 工作目录权限问题

**症状**:
```
PermissionError: [Errno 13] Permission denied: '.working_dir/idea2video'
```

**原因**: 没有写入权限

**解决方案**:
1. 检查目录权限：`ls -ld .working_dir/`
2. 修改权限：`chmod -R 755 .working_dir/`
3. 或使用其他有权限的目录

### 调试技巧

#### 1. 启用详细日志

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

#### 2. 测试单个组件

分别测试每个组件，定位问题：

```python
# 测试 chat_model
chat_model = init_chat_model(...)
response = await chat_model.ainvoke("test")

# 测试 image_generator
image_generator = ImageGeneratorNanobananaGoogleAPI(api_key="...")
image = await image_generator.generate_single_image(prompt="test")

# 测试 video_generator
video_generator = VideoGeneratorVeoGoogleAPI(api_key="...")
video = await video_generator.generate_single_video(prompt="test", reference_image_paths=["test.png"])
```

#### 3. 检查网络连接

```bash
# 测试 API 端点可访问性
curl -I https://openrouter.ai/api/v1/models

# 测试 DNS 解析
nslookup openrouter.ai
```

---

## 相关资源

### 深入学习

- **[快速开始](./getting_started.md)** - 基础配置和使用
- **[API 参考](./api_reference.md)** - 了解配置如何影响 API 行为
- **[工具与集成](./tools.md)** - 详细了解各个工具的特性
- **[故障排查](./troubleshooting.md)** - 更多故障排查指南

### 外部资源

- **[YAML 语法指南](https://yaml.org/spec/1.2.2/)** - YAML 官方规范
- **[OpenRouter 文档](https://openrouter.ai/docs)** - OpenRouter API 文档
- **[Google AI Studio](https://aistudio.google.com/)** - 获取 Google API Key
- **[云雾 AI](https://yunwu.ai/)** - 云雾 API 文档

### 社区支持

- **GitHub Issues**: [提交配置问题](https://github.com/HKUDS/ViMax/issues)
- **交流群**: 查看 [Communication.md](../Communication.md)

---

**提示**: 配置文件中的 API Key 是敏感信息，请妥善保管，不要提交到公开仓库。建议使用环境变量或密钥管理工具。
