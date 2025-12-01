# API 参考文档

> 本文档提供 ViMax 框架所有公共类和方法的详细 API 参考

## 目录

- [前置知识](#前置知识)
- [流水线 API](#流水线-api)
- [智能体 API](#智能体-api)
- [工具 API](#工具-api)
- [数据接口](#数据接口)
- [工具函数](#工具函数)
- [版本兼容性](#版本兼容性)
- [相关资源](#相关资源)

## 前置知识

在使用 ViMax API 之前，建议您先了解：

- [快速开始](./getting_started.md) - 了解基本使用方法
- [系统架构](./architecture.md) - 理解系统设计
- Python 异步编程（asyncio）基础
- Pydantic 数据模型基础

**API 设计原则**：

- 所有智能体和流水线方法都是异步的（使用 `async/await`）
- 使用 Pydantic 模型进行数据验证和序列化
- 支持通过配置文件动态初始化
- 提供统一的错误处理机制

## 流水线 API

### Idea2VideoPipeline

将简单创意扩展为完整视频的流水线。

#### 类签名

```python
class Idea2VideoPipeline:
    def __init__(
        self,
        chat_model: Any,
        image_generator: Any,
        video_generator: Any,
        working_dir: str,
    )
```

#### 初始化参数

| 参数 | 类型 | 说明 | 必需 |
|------|------|------|------|
| `chat_model` | `Any` | 大语言模型实例，用于驱动智能体 | 是 |
| `image_generator` | `Any` | 图像生成工具实例 | 是 |
| `video_generator` | `Any` | 视频生成工具实例 | 是 |
| `working_dir` | `str` | 工作目录路径，用于保存中间文件和最终输出 | 是 |

#### 类方法

##### `init_from_config`

从配置文件初始化流水线。

```python
@classmethod
def init_from_config(cls, config_path: str) -> Idea2VideoPipeline
```

**参数**：
- `config_path` (str): 配置文件路径（YAML 格式）

**返回值**：
- `Idea2VideoPipeline`: 初始化后的流水线实例

**使用示例**：

```python
from pipelines import Idea2VideoPipeline

# 从配置文件初始化
pipeline = Idea2VideoPipeline.init_from_config(
    config_path="configs/idea2video.yaml"
)
```

#### 实例方法

##### `__call__`

执行完整的创意到视频生成流程。

```python
async def __call__(
    self,
    idea: str,
    user_requirement: str,
    style: str,
) -> str
```

**参数**：
- `idea` (str): 创意描述，可以是一句话或简短的故事梗概
- `user_requirement` (str): 用户需求和约束，如目标观众、场景数量等
- `style` (str): 视觉风格，如 "Cartoon"、"Anime"、"Realistic" 等

**返回值**：
- `str`: 最终视频文件的路径

**使用示例**：

```python
import asyncio
from pipelines import Idea2VideoPipeline

async def main():
    pipeline = Idea2VideoPipeline.init_from_config("configs/idea2video.yaml")
    
    video_path = await pipeline(
        idea="一只猫和一只狗是最好的朋友，当它们遇到一只新来的猫时会发生什么？",
        user_requirement="面向儿童观众，不超过3个场景",
        style="Cartoon"
    )
    
    print(f"视频已生成：{video_path}")

asyncio.run(main())
```

##### `develop_story`

将创意扩展为完整故事。

```python
async def develop_story(
    self,
    idea: str,
    user_requirement: str,
) -> str
```

**参数**：
- `idea` (str): 创意描述
- `user_requirement` (str): 用户需求

**返回值**：
- `str`: 扩展后的完整故事文本

**使用示例**：

```python
story = await pipeline.develop_story(
    idea="一个关于友谊的故事",
    user_requirement="适合儿童，积极向上"
)
```

##### `extract_characters`

从故事中提取角色信息。

```python
async def extract_characters(
    self,
    story: str,
) -> List[CharacterInScene]
```

**参数**：
- `story` (str): 故事文本

**返回值**：
- `List[CharacterInScene]`: 角色列表

**使用示例**：

```python
characters = await pipeline.extract_characters(story=story)
for character in characters:
    print(f"角色 {character.idx}: {character.identifier_in_scene}")
```

##### `generate_character_portraits`

为角色生成画像（前视图、侧视图、后视图）。

```python
async def generate_character_portraits(
    self,
    characters: List[CharacterInScene],
    character_portraits_registry: Optional[Dict[str, Dict[str, Dict[str, str]]]],
    style: str,
) -> Dict[str, Dict[str, Dict[str, str]]]
```

**参数**：
- `characters` (List[CharacterInScene]): 角色列表
- `character_portraits_registry` (Optional[Dict]): 已有的角色画像注册表，如果为 None 则创建新的
- `style` (str): 视觉风格

**返回值**：
- `Dict[str, Dict[str, Dict[str, str]]]`: 角色画像注册表，格式为 `{角色名: {视图: {path, description}}}`

**使用示例**：

```python
portraits = await pipeline.generate_character_portraits(
    characters=characters,
    character_portraits_registry=None,
    style="Cartoon"
)

# 访问角色画像
alice_front = portraits["Alice"]["front"]["path"]
```

##### `write_script_based_on_story`

基于故事编写场景剧本。

```python
async def write_script_based_on_story(
    self,
    story: str,
    user_requirement: str,
) -> List[str]
```

**参数**：
- `story` (str): 故事文本
- `user_requirement` (str): 用户需求

**返回值**：
- `List[str]`: 场景剧本列表

**使用示例**：

```python
scripts = await pipeline.write_script_based_on_story(
    story=story,
    user_requirement="不超过3个场景"
)
```

---

### Script2VideoPipeline

将剧本转换为视频的核心流水线。

#### 类签名

```python
class Script2VideoPipeline:
    def __init__(
        self,
        chat_model: Any,
        image_generator: Any,
        video_generator: Any,
        working_dir: str,
    )
```

#### 初始化参数

与 `Idea2VideoPipeline` 相同。

#### 类方法

##### `init_from_config`

从配置文件初始化流水线。

```python
@classmethod
def init_from_config(cls, config_path: str) -> Script2VideoPipeline
```

**使用示例**：

```python
from pipelines import Script2VideoPipeline

pipeline = Script2VideoPipeline.init_from_config(
    config_path="configs/script2video.yaml"
)
```

#### 实例方法

##### `__call__`

执行完整的剧本到视频生成流程。

```python
async def __call__(
    self,
    script: str,
    user_requirement: str,
    style: str,
    characters: Optional[List[CharacterInScene]] = None,
    character_portraits_registry: Optional[Dict] = None,
) -> str
```

**参数**：
- `script` (str): 剧本文本
- `user_requirement` (str): 用户需求
- `style` (str): 视觉风格
- `characters` (Optional[List[CharacterInScene]]): 角色列表，如果为 None 则自动提取
- `character_portraits_registry` (Optional[Dict]): 角色画像注册表，如果为 None 则自动生成

**返回值**：
- `str`: 最终视频文件的路径

**使用示例**：

```python
import asyncio
from pipelines import Script2VideoPipeline

async def main():
    pipeline = Script2VideoPipeline.init_from_config("configs/script2video.yaml")
    
    script = """
    EXT. 公园 - 白天
    一只猫和一只狗在草地上玩耍...
    """
    
    video_path = await pipeline(
        script=script,
        user_requirement="快节奏，不超过15个镜头",
        style="Cartoon"
    )
    
    print(f"视频已生成：{video_path}")

asyncio.run(main())
```

---

## 智能体 API

### Screenwriter

编剧智能体，负责创作和扩写剧本。

#### 类签名

```python
class Screenwriter:
    def __init__(self, chat_model: Any)
```

#### 初始化参数

| 参数 | 类型 | 说明 | 必需 |
|------|------|------|------|
| `chat_model` | `Any` | 大语言模型实例 | 是 |

#### 方法

##### `develop_story`

将创意扩展为完整故事。

```python
async def develop_story(
    self,
    idea: str,
    user_requirement: str,
) -> str
```

**参数**：
- `idea` (str): 创意描述
- `user_requirement` (str): 用户需求

**返回值**：
- `str`: 完整故事文本

**使用示例**：

```python
from agents import Screenwriter
from langchain.chat_models import init_chat_model

chat_model = init_chat_model(
    model="google/gemini-2.5-flash-lite-preview-09-2025",
    model_provider="openai",
    api_key="YOUR_API_KEY",
    base_url="https://openrouter.ai/api/v1"
)

screenwriter = Screenwriter(chat_model=chat_model)
story = await screenwriter.develop_story(
    idea="一个关于友谊的故事",
    user_requirement="适合儿童"
)
```

##### `write_script_based_on_story`

基于故事编写场景剧本。

```python
async def write_script_based_on_story(
    self,
    story: str,
    user_requirement: str,
) -> List[str]
```

**参数**：
- `story` (str): 故事文本
- `user_requirement` (str): 用户需求

**返回值**：
- `List[str]`: 场景剧本列表

---

### CharacterExtractor

角色提取智能体，从剧本或故事中提取角色信息。

#### 类签名

```python
class CharacterExtractor:
    def __init__(self, chat_model: Any)
```

#### 方法

##### `extract_characters`

从文本中提取角色信息。

```python
async def extract_characters(
    self,
    text: str,
) -> List[CharacterInScene]
```

**参数**：
- `text` (str): 剧本或故事文本

**返回值**：
- `List[CharacterInScene]`: 角色列表

**使用示例**：

```python
from agents import CharacterExtractor

extractor = CharacterExtractor(chat_model=chat_model)
characters = await extractor.extract_characters(text=script)

for char in characters:
    print(f"{char.identifier_in_scene}: {char.static_features}")
```

---

### StoryboardArtist

分镜师智能体，设计分镜脚本。

#### 类签名

```python
class StoryboardArtist:
    def __init__(self, chat_model: Any)
```

#### 方法

##### `design_storyboard`

设计分镜脚本。

```python
async def design_storyboard(
    self,
    script: str,
    characters: List[CharacterInScene],
    user_requirement: str,
) -> List[ShotBriefDescription]
```

**参数**：
- `script` (str): 剧本文本
- `characters` (List[CharacterInScene]): 角色列表
- `user_requirement` (str): 用户需求

**返回值**：
- `List[ShotBriefDescription]`: 分镜简要描述列表

**使用示例**：

```python
from agents import StoryboardArtist

artist = StoryboardArtist(chat_model=chat_model)
storyboard = await artist.design_storyboard(
    script=script,
    characters=characters,
    user_requirement="快节奏，不超过15个镜头"
)
```

##### `decompose_visual_descriptions`

分解详细的视觉描述。

```python
async def decompose_visual_descriptions(
    self,
    shot_brief_descriptions: List[ShotBriefDescription],
    characters: List[CharacterInScene],
) -> List[ShotDescription]
```

**参数**：
- `shot_brief_descriptions` (List[ShotBriefDescription]): 分镜简要描述列表
- `characters` (List[CharacterInScene]): 角色列表

**返回值**：
- `List[ShotDescription]`: 详细镜头描述列表

---

### CharacterPortraitsGenerator

角色画像生成智能体，为角色生成标准形象。

#### 类签名

```python
class CharacterPortraitsGenerator:
    def __init__(self, image_generator: Any)
```

#### 初始化参数

| 参数 | 类型 | 说明 | 必需 |
|------|------|------|------|
| `image_generator` | `Any` | 图像生成工具实例 | 是 |

#### 方法

##### `generate_front_portrait`

生成角色的前视图画像。

```python
async def generate_front_portrait(
    self,
    character: CharacterInScene,
    style: str,
) -> ImageOutput
```

**参数**：
- `character` (CharacterInScene): 角色信息
- `style` (str): 视觉风格

**返回值**：
- `ImageOutput`: 图像输出对象

**使用示例**：

```python
from agents import CharacterPortraitsGenerator

generator = CharacterPortraitsGenerator(image_generator=image_generator)
front_portrait = await generator.generate_front_portrait(
    character=characters[0],
    style="Cartoon"
)
front_portrait.save("alice_front.png")
```

##### `generate_side_portrait`

生成角色的侧视图画像。

```python
async def generate_side_portrait(
    self,
    character: CharacterInScene,
    front_portrait_path: str,
) -> ImageOutput
```

**参数**：
- `character` (CharacterInScene): 角色信息
- `front_portrait_path` (str): 前视图画像路径，用作参考

**返回值**：
- `ImageOutput`: 图像输出对象

##### `generate_back_portrait`

生成角色的后视图画像。

```python
async def generate_back_portrait(
    self,
    character: CharacterInScene,
    front_portrait_path: str,
) -> ImageOutput
```

**参数**：
- `character` (CharacterInScene): 角色信息
- `front_portrait_path` (str): 前视图画像路径，用作参考

**返回值**：
- `ImageOutput`: 图像输出对象

---

## 工具 API

### 图像生成工具

所有图像生成工具都实现了统一的接口。

#### ImageGeneratorNanobananaGoogleAPI

使用 Google API 生成图像。

##### 类签名

```python
class ImageGeneratorNanobananaGoogleAPI:
    def __init__(self, api_key: str)
```

##### 初始化参数

| 参数 | 类型 | 说明 | 必需 |
|------|------|------|------|
| `api_key` | `str` | Google API Key | 是 |

##### 方法

###### `generate_single_image`

生成单张图像。

```python
async def generate_single_image(
    self,
    prompt: str,
    reference_image_paths: Optional[List[str]] = None,
    size: str = "1600x900",
) -> ImageOutput
```

**参数**：
- `prompt` (str): 图像生成提示词
- `reference_image_paths` (Optional[List[str]]): 参考图像路径列表
- `size` (str): 图像尺寸，默认 "1600x900"

**返回值**：
- `ImageOutput`: 图像输出对象

**使用示例**：

```python
from tools import ImageGeneratorNanobananaGoogleAPI

generator = ImageGeneratorNanobananaGoogleAPI(api_key="YOUR_API_KEY")

image = await generator.generate_single_image(
    prompt="A cute cartoon cat playing in a park",
    reference_image_paths=["reference.png"],
    size="1600x900"
)

image.save("output.png")
```

---

### 视频生成工具

所有视频生成工具都实现了统一的接口。

#### VideoGeneratorVeoGoogleAPI

使用 Google Veo API 生成视频。

##### 类签名

```python
class VideoGeneratorVeoGoogleAPI:
    def __init__(self, api_key: str)
```

##### 初始化参数

| 参数 | 类型 | 说明 | 必需 |
|------|------|------|------|
| `api_key` | `str` | Google API Key | 是 |

##### 方法

###### `generate_single_video`

生成单个视频片段。

```python
async def generate_single_video(
    self,
    prompt: str,
    reference_image_paths: List[str],
) -> VideoOutput
```

**参数**：
- `prompt` (str): 视频生成提示词，描述运动和变化
- `reference_image_paths` (List[str]): 参考图像路径列表（通常是关键帧）

**返回值**：
- `VideoOutput`: 视频输出对象

**使用示例**：

```python
from tools import VideoGeneratorVeoGoogleAPI

generator = VideoGeneratorVeoGoogleAPI(api_key="YOUR_API_KEY")

video = await generator.generate_single_video(
    prompt="The cat runs towards the camera, wagging its tail happily",
    reference_image_paths=["keyframe.png"]
)

video.save("output.mp4")
```

---

## 数据接口

### CharacterInScene

场景中的角色信息。

#### 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `idx` | `int` | 角色索引，从 0 开始 |
| `identifier_in_scene` | `str` | 场景中的角色标识符 |
| `is_visible` | `bool` | 角色是否可见 |
| `static_features` | `str` | 静态特征（外貌、体型等） |
| `dynamic_features` | `str` | 动态特征（服装、配饰等） |

#### 使用示例

```python
from interfaces import CharacterInScene

character = CharacterInScene(
    idx=0,
    identifier_in_scene="Alice",
    is_visible=True,
    static_features="长金发，蓝眼睛，苗条身材",
    dynamic_features="穿着红色围巾和黑色皮夹克"
)

print(character)
```

---

### ShotDescription

详细的镜头描述。

#### 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `idx` | `int` | 镜头索引 |
| `is_last` | `bool` | 是否为最后一个镜头 |
| `cam_idx` | `int` | 摄像机索引 |
| `visual_desc` | `str` | 整体视觉描述 |
| `ff_desc` | `str` | 首帧描述 |
| `lf_desc` | `str` | 末帧描述 |
| `motion_desc` | `str` | 运动描述 |
| `audio_desc` | `str` | 音频描述 |
| `variation_type` | `Literal["large", "medium", "small"]` | 变化类型 |
| `ff_vis_char_idxs` | `List[int]` | 首帧可见角色索引 |
| `lf_vis_char_idxs` | `List[int]` | 末帧可见角色索引 |

#### 使用示例

```python
from interfaces import ShotDescription

shot = ShotDescription(
    idx=0,
    is_last=False,
    cam_idx=0,
    visual_desc="中景镜头，Alice 和 Bob 在超市过道中相遇",
    ff_desc="Alice 推着购物车从左侧进入画面",
    lf_desc="Alice 和 Bob 面对面站立，微笑交谈",
    motion_desc="Alice 推着购物车向前移动，Bob 转身面向她",
    audio_desc="[音效] 超市背景音，购物车轮子滚动声",
    variation_type="medium",
    ff_vis_char_idxs=[0],
    lf_vis_char_idxs=[0, 1]
)
```

---

### Camera

摄像机信息，用于管理镜头连续性。

#### 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `idx` | `int` | 摄像机索引 |
| `active_shot_idxs` | `List[int]` | 该摄像机拍摄的镜头索引列表 |
| `parent_cam_idx` | `Optional[int]` | 父摄像机索引 |
| `parent_shot_idx` | `Optional[int]` | 依赖的父镜头索引 |
| `is_parent_fully_covers_child` | `Optional[bool]` | 父镜头是否完全覆盖子镜头内容 |
| `missing_info` | `Optional[str]` | 子镜头中缺失的信息描述 |

---

### ImageOutput

图像输出对象。

#### 方法

##### `save`

保存图像到文件。

```python
def save(self, path: str) -> None
```

**参数**：
- `path` (str): 保存路径

---

### VideoOutput

视频输出对象。

#### 方法

##### `save`

保存视频到文件。

```python
def save(self, path: str) -> None
```

**参数**：
- `path` (str): 保存路径

---

## 工具函数

### 图像处理

位于 `utils/image.py`。

#### `download_image`

从 URL 下载图像到本地。

```python
@retry
def download_image(url: str, save_path: str) -> None
```

**参数**：
- `url` (str): 图像 URL
- `save_path` (str): 保存路径

**使用示例**：

```python
from utils.image import download_image

download_image(
    url="https://example.com/image.png",
    save_path="local_image.png"
)
```

#### `image_path_to_b64`

将图像文件转换为 Base64 编码。

```python
def image_path_to_b64(image_path: str, mime: bool = True) -> str
```

**参数**：
- `image_path` (str): 图像文件路径
- `mime` (bool): 是否包含 MIME 类型前缀，默认 True

**返回值**：
- `str`: Base64 编码的字符串

**使用示例**：

```python
from utils.image import image_path_to_b64

b64_string = image_path_to_b64("image.png", mime=True)
# 返回: "data:image/png;base64,iVBORw0KGgo..."
```

#### `pil_to_b64`

将 PIL Image 对象转换为 Base64 编码。

```python
def pil_to_b64(image: Image, mime: bool = True) -> str
```

**参数**：
- `image` (PIL.Image): PIL Image 对象
- `mime` (bool): 是否包含 MIME 类型前缀，默认 True

**返回值**：
- `str`: Base64 编码的字符串

#### `save_base64_image`

将 Base64 编码的图像保存为文件。

```python
def save_base64_image(b64_string: str, save_path: str) -> None
```

**参数**：
- `b64_string` (str): Base64 编码的图像字符串
- `save_path` (str): 保存路径

---

### 视频处理

位于 `utils/video.py`。

#### `download_video`

从 URL 下载视频到本地。

```python
@retry
def download_video(url: str, save_path: str) -> None
```

**参数**：
- `url` (str): 视频 URL
- `save_path` (str): 保存路径

**使用示例**：

```python
from utils.video import download_video

download_video(
    url="https://example.com/video.mp4",
    save_path="local_video.mp4"
)
```

**注意**: 视频拼接功能由 MoviePy 库提供。

**视频拼接示例**：

```python
from moviepy import VideoFileClip, concatenate_videoclips

# 加载多个视频片段
clips = [VideoFileClip(path) for path in video_paths]

# 拼接视频
final_video = concatenate_videoclips(clips)

# 保存最终视频
final_video.write_videofile("output.mp4")
```

更多示例参考 [示例文档](./examples.md)。

---

### 重试机制

位于 `utils/retry.py`。

ViMax 使用 `tenacity` 库提供重试功能。工具函数（如 `download_image`, `download_video`）已使用 `@retry` 装饰器。

#### `after_func`

重试回调函数，用于记录重试日志。

```python
def after_func(retry_state: tenacity.RetryCallState) -> None
```

**使用示例**：

```python
from tenacity import retry, stop_after_attempt, wait_exponential
from utils.retry import after_func

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    after=after_func
)
async def unstable_api_call():
    # 可能失败的 API 调用
    pass
```

---

### 计时工具

位于 `utils/timer.py`。

#### `Timer`

计时器类，可用作装饰器或上下文管理器。

```python
class Timer:
    def __init__(
        self,
        prefix: str = "Start at {start_time}",
        postfix: str = "End at {end_time}, took {duration} seconds.",
    )
```

**使用示例**：

```python
from utils.timer import Timer
import time

# 作为上下文管理器
with Timer():
    time.sleep(1)

# 作为装饰器
@Timer(
    prefix="开始执行 {start_time}",
    postfix="执行完成 {end_time}，耗时 {duration} 秒"
)
async def long_running_task():
    # 长时间运行的任务
    pass
```

---

## 版本兼容性

### 当前版本

- **版本**: 1.0.0
- **Python 要求**: 3.12+
- **主要依赖**:
  - `langchain`: 用于 LLM 集成
  - `pydantic`: 用于数据验证
  - `moviepy`: 用于视频处理
  - `asyncio`: 用于异步编程

### API 稳定性

| API 类别 | 稳定性 | 说明 |
|---------|--------|------|
| 流水线 API | 稳定 | 核心接口，向后兼容 |
| 智能体 API | 稳定 | 核心接口，向后兼容 |
| 工具 API | 稳定 | 接口统一，支持扩展 |
| 数据接口 | 稳定 | Pydantic 模型，向后兼容 |
| 工具函数 | 实验性 | 可能在未来版本中调整 |

### 废弃警告

- `idea2video_pipeline_deprecated.py`: 已废弃，请使用新版 `Idea2VideoPipeline`
- `Novel2Video`: 实验性功能，API 可能变化

### 迁移指南

如果您从旧版本升级，请注意：

1. **配置文件格式**: 确保使用新的 YAML 配置格式
2. **异步方法**: 所有智能体方法现在都是异步的，需要使用 `await`
3. **数据模型**: 使用 Pydantic 模型替代字典

---

## 相关资源

### 深入学习

- **[快速开始](./getting_started.md)** - 基础使用教程
- **[系统架构](./architecture.md)** - 理解系统设计
- **[智能体详解](./agents.md)** - 了解各个智能体的功能
- **[配置详解](./configuration.md)** - 配置文件说明
- **[示例与最佳实践](./examples.md)** - 实际使用案例

### 外部文档

- **[Pydantic 文档](https://docs.pydantic.dev/)** - 数据验证和模型
- **[LangChain 文档](https://python.langchain.com/)** - LLM 应用开发
- **[asyncio 文档](https://docs.python.org/3/library/asyncio.html)** - Python 异步编程

### 社区支持

- **GitHub Issues**: [提交问题](https://github.com/HKUDS/ViMax/issues)
- **交流群**: 查看 [Communication.md](../Communication.md)

---

**注意**: 本文档基于 ViMax 1.0.0 版本编写。API 可能在未来版本中有所变化，请关注项目更新日志。
