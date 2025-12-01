# 工具与集成 (Tools)

> 本文档详细介绍 ViMax 中的工具模块，包括视频生成、图像生成和辅助工具的配置、使用和扩展方法。

## 目录

- [概述](#概述)
- [视频生成工具](#视频生成工具)
- [图像生成工具](#图像生成工具)
- [辅助工具](#辅助工具)
- [工具配置详解](#工具配置详解)
- [工具切换指南](#工具切换指南)
- [添加新工具](#添加新工具)
- [性能对比与选择建议](#性能对比与选择建议)

## 前置知识

- 了解 ViMax 的基本架构（参见 [系统架构](./architecture.md)）
- 熟悉 YAML 配置文件格式
- 准备好相应的 API Key

## 概述

ViMax 通过 `tools/` 模块集成外部的 AI 模型和 API。这种设计使得系统可以灵活切换不同的底层模型，而无需修改核心业务逻辑。

### 工具分类

- **视频生成工具**: 将文本提示和参考图像转换为视频
- **图像生成工具**: 生成分镜关键帧、角色画像等图像
- **辅助工具**: 提供重排序、检索等辅助功能

### 工具接口规范

所有工具都遵循统一的接口规范：
- 视频生成工具实现 `generate_single_video()` 方法
- 图像生成工具实现 `generate_single_image()` 方法
- 辅助工具实现特定的调用接口

---

## 视频生成工具

### VideoGeneratorVeoGoogleAPI

集成 Google Veo 3.1 模型，直接通过 Google AI API 调用。

#### 功能特点

- **高质量生成**: Veo 3.1 提供业界领先的视频生成质量
- **多种生成模式**: 支持文本生成视频 (T2V)、首帧生成视频 (FF2V)、首尾帧生成视频 (FLF2V)
- **灵活配置**: 支持自定义分辨率、宽高比、时长等参数

#### 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `api_key` | str | 必填 | Google AI API Key |
| `t2v_model` | str | `"veo-3.1-generate-preview"` | 文本生成视频模型 |
| `ff2v_model` | str | `"veo-3.1-generate-preview"` | 首帧生成视频模型 |
| `flf2v_model` | str | `"veo-3.1-generate-preview"` | 首尾帧生成视频模型 |

#### API 方法

```python
async def generate_single_video(
    self,
    prompt: str,                          # 视频生成提示词
    reference_image_paths: List[str],     # 参考图像路径列表（0-2张）
    resolution: str = "1080p",            # 分辨率：480p, 720p, 1080p
    aspect_ratio: str = "16:9",           # 宽高比：16:9, 9:16, 1:1
    duration: int = 8,                    # 视频时长（秒）
) -> VideoOutput
```

#### 配置示例

```yaml
video_generator:
  class_path: tools.VideoGeneratorVeoGoogleAPI
  init_args:
    api_key: "YOUR_GOOGLE_API_KEY"
    t2v_model: "veo-3.1-generate-preview"
    ff2v_model: "veo-3.1-generate-preview"
    flf2v_model: "veo-3.1-generate-preview"
```

#### 使用示例

```python
from tools.video_generator_veo_google_api import VideoGeneratorVeoGoogleAPI

# 初始化工具
generator = VideoGeneratorVeoGoogleAPI(
    api_key="your_google_api_key"
)

# 文本生成视频
video_output = await generator.generate_single_video(
    prompt="一只猫在草地上奔跑",
    reference_image_paths=[],
    resolution="1080p",
    aspect_ratio="16:9",
    duration=8
)

# 首帧生成视频
video_output = await generator.generate_single_video(
    prompt="镜头缓慢推进",
    reference_image_paths=["first_frame.png"],
    resolution="1080p",
    aspect_ratio="16:9",
    duration=8
)

# 首尾帧生成视频
video_output = await generator.generate_single_video(
    prompt="平滑过渡",
    reference_image_paths=["first_frame.png", "last_frame.png"],
    resolution="1080p",
    aspect_ratio="16:9",
    duration=8
)
```

#### 注意事项

- 需要有效的 Google AI API Key
- 视频生成为异步操作，需要等待生成完成
- 参考图像数量不能超过 2 张
- 生成的视频以字节流形式返回

---

### VideoGeneratorVeoYunwuAPI

集成 Google Veo 模型，通过云雾 API 调用，适合国内用户使用。

#### 功能特点

- **国内访问优化**: 通过云雾 API 提供更稳定的国内访问
- **多模型支持**: 支持 Veo 2 和 Veo 3 系列多个模型
- **灵活配置**: 可根据需求选择不同速度和质量的模型

#### 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `api_key` | str | 必填 | 云雾 API Key |
| `t2v_model` | str | `"veo3.1-fast"` | 文本生成视频模型 |
| `ff2v_model` | str | `"veo3.1-fast"` | 首帧生成视频模型 |
| `flf2v_model` | str | `"veo2-fast-frames"` | 首尾帧生成视频模型 |

#### 可用模型列表

| 模型名称 | 说明 | 支持模式 |
|---------|------|---------|
| `veo2` | Veo 2 标准版 | T2V, FF2V |
| `veo2-fast` | Veo 2 快速版 | T2V, FF2V |
| `veo2-fast-frames` | Veo 2 快速版（支持首尾帧） | T2V, FF2V, FLF2V |
| `veo2-pro` | Veo 2 专业版 | T2V, FF2V |
| `veo3` | Veo 3 标准版 | T2V, FF2V |
| `veo3-fast` | Veo 3 快速版 | T2V, FF2V |
| `veo3-pro` | Veo 3 专业版 | T2V, FF2V |
| `veo3-fast-frames` | Veo 3 快速版（支持首尾帧） | T2V, FF2V, FLF2V |

> **注意**: Veo 3 系列不支持首尾帧生成视频模式

#### API 方法

```python
async def generate_single_video(
    self,
    prompt: str = "",                     # 视频生成提示词
    reference_image_paths: List[str] = [], # 参考图像路径列表（0-2张）
    aspect_ratio: str = "16:9",           # 宽高比（仅 Veo 3 支持）
    **kwargs,
) -> VideoOutput
```

#### 配置示例

```yaml
video_generator:
  class_path: tools.VideoGeneratorVeoYunwuAPI
  init_args:
    api_key: "YOUR_YUNWU_API_KEY"
    t2v_model: "veo3-fast"
    ff2v_model: "veo3-fast"
    flf2v_model: "veo2-fast-frames"  # Veo 3 不支持首尾帧模式
```

#### 使用示例

```python
from tools.video_generator_veo_yunwu_api import VideoGeneratorVeoYunwuAPI

# 初始化工具
generator = VideoGeneratorVeoYunwuAPI(
    api_key="your_yunwu_api_key",
    t2v_model="veo3-fast"
)

# 生成视频
video_output = await generator.generate_single_video(
    prompt="一只猫在草地上奔跑",
    reference_image_paths=[],
    aspect_ratio="16:9"
)

# 返回的视频为 URL 格式
print(video_output.fmt)  # "url"
print(video_output.data)  # "https://..."
```

#### 注意事项

- 视频生成为异步任务，需要轮询查询状态
- 返回的视频为 URL 格式，需要下载后使用
- Veo 3 系列仅支持宽高比设置，不支持首尾帧模式

---

### VideoGeneratorDoubaoSeedanceYunwuAPI

集成字节跳动豆包 Seedance 视频生成模型，通过云雾 API 调用。

#### 功能特点

- **快速响应**: 生成速度较快，适合快速迭代
- **国内优化**: 针对国内网络环境优化
- **灵活参数**: 支持多种分辨率、帧率和时长配置

#### 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `api_key` | str | 必填 | 云雾 API Key |
| `t2v_model` | str | `"doubao-seedance-1-0-lite-t2v-250428"` | 文本生成视频模型 |
| `ff2v_model` | str | `"doubao-seedance-1-0-lite-i2v-250428"` | 图像生成视频模型 |
| `flf2v_model` | str | `"doubao-seedance-1-0-lite-i2v-250428"` | 首尾帧生成视频模型 |

#### API 方法

```python
async def generate_single_video(
    self,
    prompt: str,                          # 视频生成提示词
    reference_image_paths: List[str],     # 参考图像路径列表（0-2张）
    resolution: Literal["480p", "720p", "1080p"] = "720p",  # 分辨率
    aspect_ratio: str = "16:9",           # 宽高比
    fps: Literal[16, 24] = 16,            # 帧率
    duration: Literal[5, 10] = 5,         # 视频时长（秒）
) -> VideoOutput
```

#### 配置示例

```yaml
video_generator:
  class_path: tools.VideoGeneratorDoubaoSeedanceYunwuAPI
  init_args:
    api_key: "YOUR_YUNWU_API_KEY"
    t2v_model: "doubao-seedance-1-0-lite-t2v-250428"
    ff2v_model: "doubao-seedance-1-0-lite-i2v-250428"
    flf2v_model: "doubao-seedance-1-0-lite-i2v-250428"
```

#### 使用示例

```python
from tools.video_generator_doubao_seedance_yunwu_api import VideoGeneratorDoubaoSeedanceYunwuAPI

# 初始化工具
generator = VideoGeneratorDoubaoSeedanceYunwuAPI(
    api_key="your_yunwu_api_key"
)

# 生成视频
video_output = await generator.generate_single_video(
    prompt="一只猫在草地上奔跑",
    reference_image_paths=["first_frame.png"],
    resolution="720p",
    aspect_ratio="16:9",
    fps=24,
    duration=5
)
```

#### 注意事项

- 分辨率仅支持 480p、720p、1080p
- 帧率仅支持 16 或 24 fps
- 视频时长仅支持 5 或 10 秒
- 返回的视频为 URL 格式

---

## 图像生成工具

### ImageGeneratorNanobananaGoogleAPI

集成 Google Gemini 2.5 Flash 图像生成模型，直接通过 Google AI API 调用。

#### 功能特点

- **高质量生成**: 基于 Gemini 2.5 Flash 的图像生成能力
- **参考图像支持**: 支持使用参考图像引导生成
- **灵活宽高比**: 支持多种宽高比配置

#### 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `api_key` | str | 必填 | Google AI API Key |

#### API 方法

```python
async def generate_single_image(
    self,
    prompt: str,                          # 图像生成提示词
    reference_image_paths: List[str] = [], # 参考图像路径列表
    aspect_ratio: Optional[str] = "16:9", # 宽高比
    **kwargs,
) -> ImageOutput
```

#### 配置示例

```yaml
image_generator:
  class_path: tools.ImageGeneratorNanobananaGoogleAPI
  init_args:
    api_key: "YOUR_GOOGLE_API_KEY"
```

#### 使用示例

```python
from tools.image_generator_nanobanana_google_api import ImageGeneratorNanobananaGoogleAPI

# 初始化工具
generator = ImageGeneratorNanobananaGoogleAPI(
    api_key="your_google_api_key"
)

# 生成图像
image_output = await generator.generate_single_image(
    prompt="一只可爱的猫咪，卡通风格",
    reference_image_paths=[],
    aspect_ratio="16:9"
)

# 使用参考图像
image_output = await generator.generate_single_image(
    prompt="保持风格，改变背景为森林",
    reference_image_paths=["reference.png"],
    aspect_ratio="16:9"
)

# 返回的图像为 PIL Image 格式
print(image_output.fmt)  # "pil"
image_output.data.save("output.png")
```

#### 注意事项

- 需要有效的 Google AI API Key
- 返回的图像为 PIL Image 格式
- 支持多张参考图像
- 自动重试最多 3 次

---

### ImageGeneratorNanobananaYunwuAPI

集成 Google Gemini 图像生成模型，通过云雾 API 调用。

#### 功能特点

- **国内访问优化**: 通过云雾 API 提供更稳定的国内访问
- **模型可选**: 支持选择不同的 Gemini 图像生成模型

#### 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `api_key` | str | 必填 | 云雾 API Key |
| `model` | str | `"gemini-2.5-flash-image-preview"` | 图像生成模型 |

#### API 方法

```python
async def generate_single_image(
    self,
    prompt: str,                          # 图像生成提示词
    reference_image_paths: List[str] = [], # 参考图像路径列表
    aspect_ratio: Optional[str] = "16:9", # 宽高比
    **kwargs,
) -> ImageOutput
```

#### 配置示例

```yaml
image_generator:
  class_path: tools.ImageGeneratorNanobananaYunwuAPI
  init_args:
    api_key: "YOUR_YUNWU_API_KEY"
    model: "gemini-2.5-flash-image-preview"
```

#### 使用示例

```python
from tools.image_generator_nanobanana_yunwu_api import ImageGeneratorNanobananaYunwuAPI

# 初始化工具
generator = ImageGeneratorNanobananaYunwuAPI(
    api_key="your_yunwu_api_key",
    model="gemini-2.5-flash-image-preview"
)

# 生成图像
image_output = await generator.generate_single_image(
    prompt="一只可爱的猫咪，卡通风格",
    reference_image_paths=[],
    aspect_ratio="16:9"
)
```

---

### ImageGeneratorDoubaoSeedreamYunwuAPI

集成豆包 Seedream 图像生成模型，通过云雾 API 调用。

#### 功能特点

- **高分辨率支持**: 支持最高 4096x4096 分辨率
- **快速生成**: 生成速度较快
- **参考图像支持**: 支持使用参考图像引导生成

#### 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `api_key` | str | 必填 | 云雾 API Key |
| `model` | str | `"doubao-seedream-4-0-250828"` | 图像生成模型 |

#### API 方法

```python
async def generate_single_image(
    self,
    prompt: str,                          # 图像生成提示词
    reference_image_paths: List[str] = [], # 参考图像路径列表
    size: Optional[str] = None,           # 图像尺寸（如 "1024x1024"）
    **kwargs,
) -> ImageOutput
```

#### 配置示例

```yaml
image_generator:
  class_path: tools.ImageGeneratorDoubaoSeedreamYunwuAPI
  init_args:
    api_key: "YOUR_YUNWU_API_KEY"
    model: "doubao-seedream-4-0-250828"
```

#### 使用示例

```python
from tools.image_generator_doubao_seedream_yunwu_api import ImageGeneratorDoubaoSeedreamYunwuAPI

# 初始化工具
generator = ImageGeneratorDoubaoSeedreamYunwuAPI(
    api_key="your_yunwu_api_key"
)

# 生成图像
image_output = await generator.generate_single_image(
    prompt="一只可爱的猫咪，卡通风格",
    reference_image_paths=[],
    size="1024x1024"
)

# 生成高分辨率图像
image_output = await generator.generate_single_image(
    prompt="一只可爱的猫咪，卡通风格",
    reference_image_paths=[],
    size="4096x4096"
)

# 返回的图像为 URL 格式
print(image_output.fmt)  # "url"
print(image_output.data)  # "https://..."
```

#### 注意事项

- 支持的尺寸范围：1024x1024 到 4096x4096
- 返回的图像为 URL 格式
- 自动重试最多 3 次

---

## 辅助工具

### RerankerBgeSiliconapi

集成 BGE Reranker 模型，通过 SiliconFlow API 调用，用于文本重排序。

#### 功能特点

- **高精度重排序**: 基于 BGE Reranker v2-m3 模型
- **RAG 优化**: 专为检索增强生成场景设计
- **批量处理**: 支持批量文档重排序

#### 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `api_key` | str | 必填 | SiliconFlow API Key |
| `base_url` | str | 必填 | API 基础 URL |
| `model` | str | `"BAAI/bge-reranker-v2-m3"` | 重排序模型 |

#### API 方法

```python
async def __call__(
    self,
    documents: List[str],                 # 待重排序的文档列表
    query: str,                           # 查询文本
    top_n: int,                           # 返回前 N 个结果
) -> List[Tuple[str, float]]              # 返回 (文档, 相关性分数) 列表
```

#### 配置示例

```yaml
reranker:
  class_path: tools.RerankerBgeSiliconapi
  init_args:
    api_key: "YOUR_SILICONFLOW_API_KEY"
    base_url: "https://api.siliconflow.cn"
    model: "BAAI/bge-reranker-v2-m3"
```

#### 使用示例

```python
from tools.reranker_bge_silicon_api import RerankerBgeSiliconapi

# 初始化工具
reranker = RerankerBgeSiliconapi(
    api_key="your_siliconflow_api_key",
    base_url="https://api.siliconflow.cn"
)

# 重排序文档
documents = [
    "猫是一种可爱的宠物",
    "狗是人类最好的朋友",
    "猫咪喜欢晒太阳",
    "鱼在水里游泳"
]

results = await reranker(
    documents=documents,
    query="猫的习性",
    top_n=2
)

# 输出结果
for doc, score in results:
    print(f"相关性分数: {score:.4f}, 文档: {doc}")
```

#### 注意事项

- 主要用于 Novel2Video 流水线的知识库检索
- 自动重试最多 3 次
- 返回结果按相关性分数降序排列

---

## 工具配置详解

### 配置文件结构

ViMax 使用 YAML 格式的配置文件来管理工具配置。配置文件位于 `configs/` 目录下。

#### 基本配置结构

```yaml
# 聊天模型配置
chat_model:
  init_args:
    model: google/gemini-2.5-flash-lite-preview-09-2025
    model_provider: openai
    api_key: YOUR_API_KEY
    base_url: https://openrouter.ai/api/v1

# 图像生成工具配置
image_generator:
  class_path: tools.ImageGeneratorNanobananaGoogleAPI
  init_args:
    api_key: YOUR_GOOGLE_API_KEY

# 视频生成工具配置
video_generator:
  class_path: tools.VideoGeneratorVeoGoogleAPI
  init_args:
    api_key: YOUR_GOOGLE_API_KEY

# 工作目录
working_dir: .working_dir/idea2video
```

### 配置字段说明

#### class_path

指定工具类的完整路径，格式为 `模块名.类名`。

**示例**:
```yaml
class_path: tools.VideoGeneratorVeoGoogleAPI
```

#### init_args

工具初始化时传递的参数，以字典形式提供。

**示例**:
```yaml
init_args:
  api_key: "YOUR_API_KEY"
  model: "veo3-fast"
```

### 环境变量支持

为了安全起见，建议将 API Key 存储在环境变量中：

```bash
# 设置环境变量
export GOOGLE_API_KEY="your_google_api_key"
export YUNWU_API_KEY="your_yunwu_api_key"
export SILICONFLOW_API_KEY="your_siliconflow_api_key"
```

然后在配置文件中引用：

```yaml
image_generator:
  class_path: tools.ImageGeneratorNanobananaGoogleAPI
  init_args:
    api_key: ${GOOGLE_API_KEY}
```

> **注意**: 当前版本需要在配置文件中直接填写 API Key，未来版本将支持环境变量引用。

---

## 工具切换指南

### 场景 1: 切换视频生成工具

#### 从 Google Veo 切换到豆包 Seedance

**原配置**:
```yaml
video_generator:
  class_path: tools.VideoGeneratorVeoGoogleAPI
  init_args:
    api_key: "YOUR_GOOGLE_API_KEY"
```

**新配置**:
```yaml
video_generator:
  class_path: tools.VideoGeneratorDoubaoSeedanceYunwuAPI
  init_args:
    api_key: "YOUR_YUNWU_API_KEY"
```

#### 从 Google 直连切换到云雾 API

**原配置**:
```yaml
video_generator:
  class_path: tools.VideoGeneratorVeoGoogleAPI
  init_args:
    api_key: "YOUR_GOOGLE_API_KEY"
```

**新配置**:
```yaml
video_generator:
  class_path: tools.VideoGeneratorVeoYunwuAPI
  init_args:
    api_key: "YOUR_YUNWU_API_KEY"
    t2v_model: "veo3-fast"
    ff2v_model: "veo3-fast"
    flf2v_model: "veo2-fast-frames"
```

### 场景 2: 切换图像生成工具

#### 从 Google 切换到豆包

**原配置**:
```yaml
image_generator:
  class_path: tools.ImageGeneratorNanobananaGoogleAPI
  init_args:
    api_key: "YOUR_GOOGLE_API_KEY"
```

**新配置**:
```yaml
image_generator:
  class_path: tools.ImageGeneratorDoubaoSeedreamYunwuAPI
  init_args:
    api_key: "YOUR_YUNWU_API_KEY"
    model: "doubao-seedream-4-0-250828"
```

### 场景 3: 同时切换多个工具

**完整配置示例**:
```yaml
# 使用云雾 API 的完整配置
chat_model:
  init_args:
    model: google/gemini-2.5-flash-lite-preview-09-2025
    model_provider: openai
    api_key: YOUR_OPENROUTER_API_KEY
    base_url: https://openrouter.ai/api/v1

image_generator:
  class_path: tools.ImageGeneratorNanobananaYunwuAPI
  init_args:
    api_key: YOUR_YUNWU_API_KEY
    model: "gemini-2.5-flash-image-preview"

video_generator:
  class_path: tools.VideoGeneratorVeoYunwuAPI
  init_args:
    api_key: YOUR_YUNWU_API_KEY
    t2v_model: "veo3-fast"
    ff2v_model: "veo3-fast"
    flf2v_model: "veo2-fast-frames"

working_dir: .working_dir/idea2video
```

### 切换步骤

1. **备份原配置文件**
   ```bash
   cp configs/idea2video.yaml configs/idea2video.yaml.bak
   ```

2. **修改配置文件**
   - 更新 `class_path` 为新工具的类路径
   - 更新 `init_args` 中的参数

3. **验证配置**
   ```bash
   python main_idea2video.py --config configs/idea2video.yaml
   ```

4. **测试生成**
   - 运行一个简单的测试任务
   - 检查输出结果是否符合预期

---

## 添加新工具

如果您需要支持新的模型（如 Sora、Runway、Midjourney 等），可以按照以下步骤添加新工具。

### 步骤 1: 创建工具文件

在 `tools/` 目录下创建新的 Python 文件，例如 `video_generator_sora_api.py`。

### 步骤 2: 实现工具类

#### 视频生成工具模板

```python
import logging
from typing import List
from interfaces.video_output import VideoOutput

class VideoGeneratorSoraAPI:
    def __init__(
        self,
        api_key: str,
        # 其他初始化参数
    ):
        """
        初始化工具
        
        Args:
            api_key: API Key
        """
        self.api_key = api_key
        # 初始化客户端或其他资源
    
    async def generate_single_video(
        self,
        prompt: str,
        reference_image_paths: List[str],
        # 其他生成参数
        **kwargs,
    ) -> VideoOutput:
        """
        生成单个视频
        
        Args:
            prompt: 视频生成提示词
            reference_image_paths: 参考图像路径列表
            
        Returns:
            VideoOutput: 视频输出对象
        """
        logging.info(f"Calling Sora API to generate video...")
        
        # 1. 调用 API 生成视频
        # 2. 处理响应
        # 3. 返回 VideoOutput 对象
        
        return VideoOutput(
            fmt="url",  # 或 "bytes"
            ext="mp4",
            data=video_data
        )
```

#### 图像生成工具模板

```python
import logging
from typing import List, Optional
from interfaces.image_output import ImageOutput

class ImageGeneratorMidjourneyAPI:
    def __init__(
        self,
        api_key: str,
        # 其他初始化参数
    ):
        """
        初始化工具
        
        Args:
            api_key: API Key
        """
        self.api_key = api_key
        # 初始化客户端或其他资源
    
    async def generate_single_image(
        self,
        prompt: str,
        reference_image_paths: List[str] = [],
        # 其他生成参数
        **kwargs,
    ) -> ImageOutput:
        """
        生成单个图像
        
        Args:
            prompt: 图像生成提示词
            reference_image_paths: 参考图像路径列表
            
        Returns:
            ImageOutput: 图像输出对象
        """
        logging.info(f"Calling Midjourney API to generate image...")
        
        # 1. 调用 API 生成图像
        # 2. 处理响应
        # 3. 返回 ImageOutput 对象
        
        return ImageOutput(
            fmt="pil",  # 或 "url"
            ext="png",
            data=image_data
        )
```

### 步骤 3: 实现关键接口

#### VideoOutput 格式

```python
from interfaces.video_output import VideoOutput

# 字节流格式
video_output = VideoOutput(
    fmt="bytes",
    ext="mp4",
    data=video_bytes  # bytes 类型
)

# URL 格式
video_output = VideoOutput(
    fmt="url",
    ext="mp4",
    data="https://example.com/video.mp4"  # str 类型
)
```

#### ImageOutput 格式

```python
from interfaces.image_output import ImageOutput
from PIL import Image

# PIL Image 格式
image_output = ImageOutput(
    fmt="pil",
    ext="png",
    data=pil_image  # PIL.Image.Image 类型
)

# URL 格式
image_output = ImageOutput(
    fmt="url",
    ext="png",
    data="https://example.com/image.png"  # str 类型
)
```

### 步骤 4: 添加错误处理和重试

使用 `tenacity` 库实现自动重试：

```python
from tenacity import retry, stop_after_attempt
from utils.retry import after_func

class VideoGeneratorSoraAPI:
    @retry(stop=stop_after_attempt(3), after=after_func)
    async def generate_single_video(self, ...):
        # 实现代码
        pass
```

### 步骤 5: 更新配置文件

在 `configs/` 目录下的配置文件中添加新工具：

```yaml
video_generator:
  class_path: tools.VideoGeneratorSoraAPI
  init_args:
    api_key: "YOUR_SORA_API_KEY"
```

### 步骤 6: 测试新工具

创建测试脚本验证新工具：

```python
import asyncio
from tools.video_generator_sora_api import VideoGeneratorSoraAPI

async def test_sora():
    generator = VideoGeneratorSoraAPI(
        api_key="your_api_key"
    )
    
    video_output = await generator.generate_single_video(
        prompt="测试提示词",
        reference_image_paths=[]
    )
    
    print(f"生成成功: {video_output.fmt}, {video_output.ext}")

asyncio.run(test_sora())
```

### 最佳实践

1. **日志记录**: 使用 `logging` 模块记录关键操作
2. **异常处理**: 捕获并处理 API 调用异常
3. **参数验证**: 验证输入参数的有效性
4. **异步支持**: 使用 `async/await` 实现异步操作
5. **重试机制**: 对网络请求实现自动重试
6. **文档注释**: 为类和方法添加详细的文档字符串

---

## 性能对比与选择建议

### 视频生成工具对比

| 工具 | 质量 | 速度 | 成本 | 国内访问 | 推荐场景 |
|------|------|------|------|---------|---------|
| VideoGeneratorVeoGoogleAPI | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 追求最高质量 |
| VideoGeneratorVeoYunwuAPI | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 国内用户，平衡质量和速度 |
| VideoGeneratorDoubaoSeedanceYunwuAPI | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 快速迭代，成本敏感 |

### 图像生成工具对比

| 工具 | 质量 | 速度 | 成本 | 国内访问 | 推荐场景 |
|------|------|------|------|---------|---------|
| ImageGeneratorNanobananaGoogleAPI | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 追求最高质量 |
| ImageGeneratorNanobananaYunwuAPI | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 国内用户 |
| ImageGeneratorDoubaoSeedreamYunwuAPI | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 高分辨率需求 |

### 选择建议

#### 场景 1: 国内用户

**推荐配置**:
```yaml
image_generator:
  class_path: tools.ImageGeneratorNanobananaYunwuAPI
  init_args:
    api_key: YOUR_YUNWU_API_KEY

video_generator:
  class_path: tools.VideoGeneratorVeoYunwuAPI
  init_args:
    api_key: YOUR_YUNWU_API_KEY
    t2v_model: "veo3-fast"
```

**理由**: 云雾 API 针对国内网络优化，访问稳定，速度快。

#### 场景 2: 追求最高质量

**推荐配置**:
```yaml
image_generator:
  class_path: tools.ImageGeneratorNanobananaGoogleAPI
  init_args:
    api_key: YOUR_GOOGLE_API_KEY

video_generator:
  class_path: tools.VideoGeneratorVeoGoogleAPI
  init_args:
    api_key: YOUR_GOOGLE_API_KEY
```

**理由**: Google 原生 API 提供最高质量的生成效果。

#### 场景 3: 快速迭代和原型开发

**推荐配置**:
```yaml
image_generator:
  class_path: tools.ImageGeneratorDoubaoSeedreamYunwuAPI
  init_args:
    api_key: YOUR_YUNWU_API_KEY

video_generator:
  class_path: tools.VideoGeneratorDoubaoSeedanceYunwuAPI
  init_args:
    api_key: YOUR_YUNWU_API_KEY
```

**理由**: 豆包系列模型生成速度快，成本较低，适合快速迭代。

#### 场景 4: 成本敏感

**推荐配置**:
```yaml
image_generator:
  class_path: tools.ImageGeneratorDoubaoSeedreamYunwuAPI
  init_args:
    api_key: YOUR_YUNWU_API_KEY

video_generator:
  class_path: tools.VideoGeneratorDoubaoSeedanceYunwuAPI
  init_args:
    api_key: YOUR_YUNWU_API_KEY
```

**理由**: 豆包系列模型性价比高，适合大规模生成。

### 性能优化建议

#### 1. 批量生成优化

对于需要生成多个视频或图像的场景，可以使用异步并发：

```python
import asyncio

async def generate_multiple_videos(generator, prompts):
    tasks = [
        generator.generate_single_video(prompt, [])
        for prompt in prompts
    ]
    results = await asyncio.gather(*tasks)
    return results
```

#### 2. 缓存策略

对于相同的提示词和参考图像，可以实现缓存机制避免重复生成：

```python
import hashlib
import json

def get_cache_key(prompt, reference_images):
    data = {
        "prompt": prompt,
        "images": reference_images
    }
    return hashlib.md5(json.dumps(data).encode()).hexdigest()
```

#### 3. 降级策略

当主要工具不可用时，自动切换到备用工具：

```python
async def generate_with_fallback(primary_generator, fallback_generator, prompt):
    try:
        return await primary_generator.generate_single_video(prompt, [])
    except Exception as e:
        logging.warning(f"Primary generator failed: {e}, using fallback")
        return await fallback_generator.generate_single_video(prompt, [])
```

#### 4. 参数调优

根据实际需求调整生成参数：

- **快速预览**: 使用较低分辨率（480p）和较短时长（5秒）
- **最终输出**: 使用高分辨率（1080p）和标准时长（8-10秒）
- **特殊需求**: 根据场景调整宽高比和帧率

---

## 相关资源

- [系统架构](./architecture.md) - 了解工具在系统中的位置
- [流水线详解](./pipelines.md) - 了解工具如何在流水线中使用
- [配置详解](./configuration.md) - 深入了解配置文件格式
- [开发指南](./development.md) - 学习如何开发自定义工具
- [故障排查](./troubleshooting.md) - 解决工具使用中的常见问题

## 常见问题

### Q: 如何获取 API Key？

**Google AI API Key**:
1. 访问 [Google AI Studio](https://aistudio.google.com/)
2. 登录 Google 账号
3. 在设置中生成 API Key

**云雾 API Key**:
1. 访问 [云雾 AI](https://yunwu.ai/)
2. 注册并登录账号
3. 在控制台中获取 API Key

**SiliconFlow API Key**:
1. 访问 [SiliconFlow](https://siliconflow.cn/)
2. 注册并登录账号
3. 在 API 管理中生成 Key

### Q: 工具切换后需要重启程序吗？

不需要。修改配置文件后，重新运行流水线即可使用新工具。

### Q: 可以同时使用多个工具吗？

可以。您可以在不同的配置文件中使用不同的工具，或者在代码中动态切换工具。

### Q: 如何处理 API 限流？

1. 实现重试机制（已内置）
2. 添加请求间隔
3. 使用多个 API Key 轮换
4. 联系 API 提供商提升配额

### Q: 生成失败如何调试？

1. 检查 API Key 是否有效
2. 查看日志输出（使用 `logging` 模块）
3. 验证网络连接
4. 检查参数是否符合 API 要求
5. 参考 [故障排查指南](./troubleshooting.md)

---

## 完整使用示例

本节提供完整的、可直接运行的代码示例，展示如何在实际项目中使用和自定义工具。

### 示例 1：创建自定义工具配置脚本

创建一个脚本来测试和验证工具配置：

```python
# test_tools_config.py
import asyncio
import yaml
from tools import (
    ImageGeneratorNanobananaGoogleAPI,
    VideoGeneratorVeoGoogleAPI
)

async def test_image_generator():
    """测试图像生成工具"""
    print("🖼️  测试图像生成工具...")
    
    # 从配置文件读取
    with open("configs/idea2video.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    # 初始化图像生成器
    image_gen_config = config["image_generator"]["init_args"]
    image_generator = ImageGeneratorNanobananaGoogleAPI(
        api_key=image_gen_config["api_key"]
    )
    
    # 测试生成
    try:
        image_output = await image_generator.generate_single_image(
            prompt="一只可爱的卡通猫咪",
            reference_image_paths=[],
            aspect_ratio="16:9"
        )
        print("✅ 图像生成成功！")
        print(f"   格式: {image_output.fmt}")
        print(f"   扩展名: {image_output.ext}")
        
        # 保存测试图像
        if image_output.fmt == "pil":
            image_output.data.save("test_image.png")
            print("   已保存到: test_image.png")
        
        return True
    except Exception as e:
        print(f"❌ 图像生成失败: {e}")
        return False

async def test_video_generator():
    """测试视频生成工具"""
    print("\n🎥 测试视频生成工具...")
    
    # 从配置文件读取
    with open("configs/idea2video.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    # 初始化视频生成器
    video_gen_config = config["video_generator"]["init_args"]
    video_generator = VideoGeneratorVeoGoogleAPI(
        api_key=video_gen_config["api_key"]
    )
    
    # 测试生成
    try:
        video_output = await video_generator.generate_single_video(
            prompt="一只猫在草地上奔跑",
            reference_image_paths=[],
            resolution="720p",
            aspect_ratio="16:9",
            duration=5
        )
        print("✅ 视频生成成功！")
        print(f"   格式: {video_output.fmt}")
        print(f"   扩展名: {video_output.ext}")
        
        return True
    except Exception as e:
        print(f"❌ 视频生成失败: {e}")
        return False

async def main():
    """运行所有测试"""
    print("=" * 60)
    print("工具配置测试")
    print("=" * 60)
    
    image_ok = await test_image_generator()
    video_ok = await test_video_generator()
    
    print("\n" + "=" * 60)
    if image_ok and video_ok:
        print("🎉 所有工具测试通过！")
    else:
        print("⚠️  部分工具测试失败，请检查配置")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
```

### 示例 2：动态切换工具

创建一个支持动态切换工具的脚本：

```python
# dynamic_tool_switching.py
import asyncio
import yaml
import importlib

class ToolManager:
    """工具管理器，支持动态加载和切换工具"""
    
    def __init__(self, config_path: str):
        """初始化工具管理器
        
        Args:
            config_path: 配置文件路径
        """
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        
        self.image_generator = None
        self.video_generator = None
    
    def load_image_generator(self, tool_name: str = None):
        """加载图像生成工具
        
        Args:
            tool_name: 工具类路径，如果为 None 则使用配置文件中的默认值
        """
        if tool_name is None:
            tool_config = self.config["image_generator"]
            tool_name = tool_config["class_path"]
            init_args = tool_config["init_args"]
        else:
            # 使用自定义工具名称，但使用配置文件中的参数
            init_args = self.config["image_generator"]["init_args"]
        
        # 动态导入工具类
        module_name, class_name = tool_name.rsplit(".", 1)
        module = importlib.import_module(module_name)
        tool_class = getattr(module, class_name)
        
        # 实例化工具
        self.image_generator = tool_class(**init_args)
        print(f"✅ 已加载图像生成工具: {class_name}")
    
    def load_video_generator(self, tool_name: str = None):
        """加载视频生成工具
        
        Args:
            tool_name: 工具类路径，如果为 None 则使用配置文件中的默认值
        """
        if tool_name is None:
            tool_config = self.config["video_generator"]
            tool_name = tool_config["class_path"]
            init_args = tool_config["init_args"]
        else:
            init_args = self.config["video_generator"]["init_args"]
        
        # 动态导入工具类
        module_name, class_name = tool_name.rsplit(".", 1)
        module = importlib.import_module(module_name)
        tool_class = getattr(module, class_name)
        
        # 实例化工具
        self.video_generator = tool_class(**init_args)
        print(f"✅ 已加载视频生成工具: {class_name}")
    
    async def generate_image(self, prompt: str, **kwargs):
        """生成图像"""
        if self.image_generator is None:
            raise RuntimeError("图像生成工具未加载")
        
        return await self.image_generator.generate_single_image(
            prompt=prompt,
            **kwargs
        )
    
    async def generate_video(self, prompt: str, **kwargs):
        """生成视频"""
        if self.video_generator is None:
            raise RuntimeError("视频生成工具未加载")
        
        return await self.video_generator.generate_single_video(
            prompt=prompt,
            **kwargs
        )

async def main():
    """演示动态工具切换"""
    
    # 创建工具管理器
    manager = ToolManager("configs/idea2video.yaml")
    
    # 场景 1：使用默认工具
    print("\n场景 1: 使用默认工具")
    print("-" * 60)
    manager.load_image_generator()
    manager.load_video_generator()
    
    # 生成测试内容
    image = await manager.generate_image(
        prompt="一只可爱的猫咪",
        aspect_ratio="16:9"
    )
    print("✅ 图像生成完成")
    
    # 场景 2：切换到不同的工具
    print("\n场景 2: 切换到云雾 API 工具")
    print("-" * 60)
    manager.load_image_generator("tools.ImageGeneratorNanobananaYunwuAPI")
    manager.load_video_generator("tools.VideoGeneratorVeoYunwuAPI")
    
    # 使用新工具生成
    image = await manager.generate_image(
        prompt="一只可爱的猫咪",
        aspect_ratio="16:9"
    )
    print("✅ 图像生成完成（使用新工具）")
    
    print("\n🎉 工具切换演示完成！")

if __name__ == "__main__":
    asyncio.run(main())
```

### 示例 3：创建工具性能对比脚本

```python
# benchmark_tools.py
import asyncio
import time
from tools import (
    ImageGeneratorNanobananaGoogleAPI,
    ImageGeneratorDoubaoSeedreamYunwuAPI,
    VideoGeneratorVeoGoogleAPI,
    VideoGeneratorDoubaoSeedanceYunwuAPI
)

async def benchmark_image_generator(generator, name: str, prompt: str):
    """测试图像生成器性能"""
    print(f"\n测试 {name}...")
    
    start_time = time.time()
    try:
        image_output = await generator.generate_single_image(
            prompt=prompt,
            reference_image_paths=[],
            aspect_ratio="16:9"
        )
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"✅ {name} 完成")
        print(f"   耗时: {duration:.2f} 秒")
        print(f"   格式: {image_output.fmt}")
        
        return {
            "name": name,
            "success": True,
            "duration": duration,
            "format": image_output.fmt
        }
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"❌ {name} 失败: {e}")
        print(f"   耗时: {duration:.2f} 秒")
        
        return {
            "name": name,
            "success": False,
            "duration": duration,
            "error": str(e)
        }

async def benchmark_video_generator(generator, name: str, prompt: str):
    """测试视频生成器性能"""
    print(f"\n测试 {name}...")
    
    start_time = time.time()
    try:
        video_output = await generator.generate_single_video(
            prompt=prompt,
            reference_image_paths=[],
            resolution="720p",
            aspect_ratio="16:9",
            duration=5
        )
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"✅ {name} 完成")
        print(f"   耗时: {duration:.2f} 秒")
        print(f"   格式: {video_output.fmt}")
        
        return {
            "name": name,
            "success": True,
            "duration": duration,
            "format": video_output.fmt
        }
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"❌ {name} 失败: {e}")
        print(f"   耗时: {duration:.2f} 秒")
        
        return {
            "name": name,
            "success": False,
            "duration": duration,
            "error": str(e)
        }

async def main():
    """运行性能对比测试"""
    print("=" * 60)
    print("工具性能对比测试")
    print("=" * 60)
    
    # 测试提示词
    image_prompt = "一只可爱的卡通猫咪，坐在草地上"
    video_prompt = "一只猫在草地上奔跑"
    
    # 图像生成器对比
    print("\n📊 图像生成器性能对比")
    print("-" * 60)
    
    image_generators = [
        (
            ImageGeneratorNanobananaGoogleAPI(api_key="your-google-key"),
            "Google Nanobanana"
        ),
        (
            ImageGeneratorDoubaoSeedreamYunwuAPI(api_key="your-yunwu-key"),
            "Doubao Seedream"
        ),
    ]
    
    image_results = []
    for generator, name in image_generators:
        result = await benchmark_image_generator(generator, name, image_prompt)
        image_results.append(result)
    
    # 视频生成器对比
    print("\n📊 视频生成器性能对比")
    print("-" * 60)
    
    video_generators = [
        (
            VideoGeneratorVeoGoogleAPI(api_key="your-google-key"),
            "Google Veo"
        ),
        (
            VideoGeneratorDoubaoSeedanceYunwuAPI(api_key="your-yunwu-key"),
            "Doubao Seedance"
        ),
    ]
    
    video_results = []
    for generator, name in video_generators:
        result = await benchmark_video_generator(generator, name, video_prompt)
        video_results.append(result)
    
    # 显示汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    print("\n图像生成器:")
    for result in image_results:
        if result["success"]:
            print(f"  {result['name']}: {result['duration']:.2f}秒 ✅")
        else:
            print(f"  {result['name']}: 失败 ❌")
    
    print("\n视频生成器:")
    for result in video_results:
        if result["success"]:
            print(f"  {result['name']}: {result['duration']:.2f}秒 ✅")
        else:
            print(f"  {result['name']}: 失败 ❌")

if __name__ == "__main__":
    asyncio.run(main())
```

### 示例 4：创建工具配置生成器

```python
# generate_tool_config.py
import yaml
from typing import Dict, Any

def generate_config(
    chat_model_key: str,
    image_tool: str,
    image_key: str,
    video_tool: str,
    video_key: str,
    output_path: str = "configs/custom_config.yaml"
) -> None:
    """生成自定义工具配置文件
    
    Args:
        chat_model_key: 聊天模型 API Key
        image_tool: 图像生成工具类路径
        image_key: 图像生成 API Key
        video_tool: 视频生成工具类路径
        video_key: 视频生成 API Key
        output_path: 输出配置文件路径
    """
    
    # 工具配置映射
    tool_configs = {
        "google_image": {
            "class_path": "tools.ImageGeneratorNanobananaGoogleAPI",
            "init_args": {"api_key": image_key}
        },
        "yunwu_image": {
            "class_path": "tools.ImageGeneratorNanobananaYunwuAPI",
            "init_args": {
                "api_key": image_key,
                "model": "gemini-2.5-flash-image-preview"
            }
        },
        "doubao_image": {
            "class_path": "tools.ImageGeneratorDoubaoSeedreamYunwuAPI",
            "init_args": {
                "api_key": image_key,
                "model": "doubao-seedream-4-0-250828"
            }
        },
        "google_video": {
            "class_path": "tools.VideoGeneratorVeoGoogleAPI",
            "init_args": {"api_key": video_key}
        },
        "yunwu_video": {
            "class_path": "tools.VideoGeneratorVeoYunwuAPI",
            "init_args": {
                "api_key": video_key,
                "t2v_model": "veo3-fast",
                "ff2v_model": "veo3-fast",
                "flf2v_model": "veo2-fast-frames"
            }
        },
        "doubao_video": {
            "class_path": "tools.VideoGeneratorDoubaoSeedanceYunwuAPI",
            "init_args": {"api_key": video_key}
        }
    }
    
    # 构建配置
    config = {
        "chat_model": {
            "init_args": {
                "model": "google/gemini-2.5-flash-lite-preview-09-2025",
                "model_provider": "openai",
                "api_key": chat_model_key,
                "base_url": "https://openrouter.ai/api/v1"
            }
        },
        "image_generator": tool_configs.get(image_tool, tool_configs["google_image"]),
        "video_generator": tool_configs.get(video_tool, tool_configs["google_video"]),
        "working_dir": ".working_dir/custom_pipeline"
    }
    
    # 保存配置
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
    
    print(f"✅ 配置文件已生成: {output_path}")
    print(f"\n配置内容:")
    print(f"  聊天模型: Gemini 2.5 Flash")
    print(f"  图像工具: {config['image_generator']['class_path']}")
    print(f"  视频工具: {config['video_generator']['class_path']}")

def main():
    """交互式配置生成"""
    print("=" * 60)
    print("ViMax 工具配置生成器")
    print("=" * 60)
    
    # 获取用户输入
    print("\n请输入您的 API Keys:")
    chat_key = input("聊天模型 API Key (OpenRouter): ")
    
    print("\n选择图像生成工具:")
    print("  1. Google Nanobanana (推荐)")
    print("  2. 云雾 Nanobanana")
    print("  3. 豆包 Seedream")
    image_choice = input("请选择 (1-3): ")
    
    image_tool_map = {
        "1": "google_image",
        "2": "yunwu_image",
        "3": "doubao_image"
    }
    image_tool = image_tool_map.get(image_choice, "google_image")
    image_key = input("图像生成 API Key: ")
    
    print("\n选择视频生成工具:")
    print("  1. Google Veo (推荐)")
    print("  2. 云雾 Veo")
    print("  3. 豆包 Seedance")
    video_choice = input("请选择 (1-3): ")
    
    video_tool_map = {
        "1": "google_video",
        "2": "yunwu_video",
        "3": "doubao_video"
    }
    video_tool = video_tool_map.get(video_choice, "google_video")
    video_key = input("视频生成 API Key: ")
    
    # 生成配置
    print("\n正在生成配置文件...")
    generate_config(
        chat_model_key=chat_key,
        image_tool=image_tool,
        image_key=image_key,
        video_tool=video_tool,
        video_key=video_key
    )
    
    print("\n🎉 配置生成完成！您现在可以使用以下命令测试:")
    print("  python main_idea2video.py --config configs/custom_config.yaml")

if __name__ == "__main__":
    main()
```

### 运行示例的注意事项

1. **API Keys**: 将所有示例中的 API Key 替换为您的实际密钥
2. **依赖检查**: 确保已安装所有必要的依赖
3. **网络连接**: 某些工具可能需要特定的网络环境
4. **成本控制**: 性能对比测试会产生 API 调用费用，请谨慎使用
5. **错误处理**: 生产环境中建议添加更完善的错误处理

### 调试工具问题

如果工具调用失败，可以使用以下调试脚本：

```python
# debug_tool.py
import asyncio
import logging

# 启用详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def debug_tool():
    """调试工具调用"""
    from tools import ImageGeneratorNanobananaGoogleAPI
    
    generator = ImageGeneratorNanobananaGoogleAPI(
        api_key="your-api-key"
    )
    
    try:
        print("开始调用工具...")
        result = await generator.generate_single_image(
            prompt="测试图像",
            reference_image_paths=[],
            aspect_ratio="16:9"
        )
        print(f"成功！格式: {result.fmt}")
    except Exception as e:
        print(f"失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_tool())
```

---

**更新记录**:
- 2025-12-01: 完善工具文档，添加详细配置和使用示例
- 2025-12-01: 添加完整的可运行示例代码
