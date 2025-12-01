# 开发指南

> 本指南为开发者提供详细的开发环境设置、代码结构说明、扩展指南和最佳实践，帮助您深入理解 ViMax 并为项目做出贡献。

## 目录

- [开发环境设置](#开发环境设置)
- [代码结构详解](#代码结构详解)
- [添加新智能体](#添加新智能体)
- [添加新工具](#添加新工具)
- [代码风格与最佳实践](#代码风格与最佳实践)
- [测试与调试](#测试与调试)
- [提交代码](#提交代码)
- [相关资源](#相关资源)

## 前置知识

在开始开发之前，建议您先阅读以下文档：
- [快速开始](./getting_started.md) - 了解项目基本使用
- [系统架构](./architecture.md) - 理解系统设计原理
- [智能体详解](./agents.md) - 了解智能体的工作机制
- [工具详解](./tools.md) - 了解工具的集成方式

## 开发环境设置

### 系统要求

- **操作系统**: Linux、macOS 或 Windows
- **Python 版本**: Python 3.12 或更高版本
- **包管理器**: 推荐使用 [uv](https://github.com/astral-sh/uv) 进行依赖管理
- **Git**: 用于版本控制

### 详细安装步骤

#### 1. Fork 和克隆仓库

首先，在 GitHub 上 Fork ViMax 仓库到您的账户：

```bash
# 克隆您 Fork 的仓库
git clone https://github.com/YOUR_USERNAME/ViMax.git
cd ViMax

# 添加上游仓库（用于同步最新代码）
git remote add upstream https://github.com/ORIGINAL_OWNER/ViMax.git
```

#### 2. 安装 uv 包管理器

如果您还没有安装 uv，请按照以下方式安装：

```bash
# macOS 和 Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

验证安装：

```bash
uv --version
```

#### 3. 创建虚拟环境并安装依赖

```bash
# 使用 uv 同步项目依赖（会自动创建虚拟环境）
uv sync

# 激活虚拟环境
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**依赖说明**：项目主要依赖包括：
- `langchain` 及相关包：用于 LLM 集成和智能体开发
- `moviepy`：用于视频处理和合成
- `opencv-python`：用于图像和视频处理
- `google-genai`、`openai`：用于调用各种 AI 模型 API
- `faiss-cpu`：用于向量检索（如需要）

#### 4. 配置 API Keys

复制配置文件模板并填入您的 API Keys：

```bash
# 复制配置文件
cp configs/idea2video.yaml configs/idea2video_local.yaml
cp configs/script2video.yaml configs/script2video_local.yaml
```

编辑配置文件，填入您的 API Keys：

```yaml
chat_model:
  init_args:
    model: google/gemini-2.5-flash-lite-preview-09-2025
    model_provider: openai
    api_key: YOUR_API_KEY_HERE  # 填入您的 API Key
    base_url: https://openrouter.ai/api/v1

image_generator:
  class_path: tools.ImageGeneratorNanobananaGoogleAPI
  init_args:
    api_key: YOUR_IMAGE_API_KEY_HERE  # 填入图像生成 API Key

video_generator:
  class_path: tools.VideoGeneratorVeoGoogleAPI
  init_args:
    api_key: YOUR_VIDEO_API_KEY_HERE  # 填入视频生成 API Key
```

#### 5. 安装开发工具（可选但推荐）

```bash
# 安装 pre-commit hooks（用于代码质量检查）
pip install pre-commit
pre-commit install

# 安装代码格式化工具
pip install black isort flake8

# 安装类型检查工具
pip install mypy
```

#### 6. 验证安装

运行一个简单的测试来验证环境配置正确：

```bash
# 测试导入主要模块
python -c "from pipelines import Idea2VideoPipeline; print('✅ 环境配置成功！')"
```

## 代码结构详解

### 项目目录结构

```
ViMax/
├── agents/                      # 智能体模块
│   ├── __init__.py             # 导出所有智能体类
│   ├── screenwriter.py         # 编剧智能体：生成故事和剧本
│   ├── character_extractor.py  # 角色提取智能体：从故事中提取角色
│   ├── character_portraits_generator.py  # 角色画像生成器
│   ├── scene_extractor.py      # 场景提取智能体
│   ├── event_extractor.py      # 事件提取智能体
│   ├── storyboard_artist.py    # 分镜艺术家：生成分镜描述
│   ├── camera_image_generator.py  # 镜头图像生成器
│   ├── reference_image_selector.py  # 参考图选择器
│   ├── best_image_selector.py  # 最佳图像选择器
│   ├── script_planner.py       # 剧本规划器
│   ├── script_enhancer.py      # 剧本增强器
│   ├── novel_compressor.py     # 小说压缩器
│   └── global_information_planner.py  # 全局信息规划器
│
├── pipelines/                   # 流水线模块
│   ├── __init__.py             # 导出所有流水线类
│   ├── idea2video_pipeline.py  # Idea2Video 流水线
│   ├── script2video_pipeline.py  # Script2Video 流水线
│   ├── novel2movie_pipeline.py  # Novel2Movie 流水线
│   └── idea2video_pipeline_deprecated.py  # 已废弃的版本
│
├── tools/                       # 工具模块（外部 API 封装）
│   ├── __init__.py             # 导出所有工具类
│   ├── image_generator_doubao_seedream_yunwu_api.py  # 豆包图像生成
│   ├── image_generator_nanobanana_google_api.py      # Google 图像生成
│   ├── image_generator_nanobanana_yunwu_api.py       # 云雾图像生成
│   ├── video_generator_doubao_seedance_yunwu_api.py  # 豆包视频生成
│   ├── video_generator_veo_google_api.py             # Google Veo 视频生成
│   ├── video_generator_veo_yunwu_api.py              # 云雾 Veo 视频生成
│   └── reranker_bge_silicon_api.py                   # BGE 重排序工具
│
├── interfaces/                  # 数据接口定义
│   ├── __init__.py             # 导出所有接口类
│   ├── character.py            # 角色数据结构
│   ├── scene.py                # 场景数据结构
│   ├── event.py                # 事件数据结构
│   ├── frame.py                # 帧数据结构
│   ├── shot_description.py     # 镜头描述数据结构
│   ├── camera.py               # 镜头参数数据结构
│   ├── environment.py          # 环境数据结构
│   ├── image_output.py         # 图像输出数据结构
│   └── video_output.py         # 视频输出数据结构
│
├── utils/                       # 工具函数
│   ├── __init__.py
│   ├── image.py                # 图像处理工具
│   ├── video.py                # 视频处理工具
│   ├── retry.py                # 重试机制
│   └── timer.py                # 计时工具
│
├── configs/                     # 配置文件
│   ├── idea2video.yaml         # Idea2Video 配置模板
│   └── script2video.yaml       # Script2Video 配置模板
│
├── docs/                        # 文档目录
│   ├── index.md                # 文档首页
│   ├── getting_started.md      # 快速开始
│   ├── architecture.md         # 系统架构
│   ├── agents.md               # 智能体详解
│   ├── pipelines.md            # 流水线详解
│   ├── tools.md                # 工具详解
│   ├── api_reference.md        # API 参考
│   ├── configuration.md        # 配置详解
│   ├── examples.md             # 示例与最佳实践
│   ├── troubleshooting.md      # 故障排查
│   ├── faq.md                  # 常见问题
│   └── development.md          # 开发指南（本文档）
│
├── main_idea2video.py          # Idea2Video 入口脚本
├── main_script2video.py        # Script2Video 入口脚本
├── pyproject.toml              # 项目配置和依赖定义
├── uv.lock                     # 依赖锁定文件
└── README.md                   # 项目说明
```

### 核心模块职责

#### Agents（智能体）

智能体是系统中执行特定任务的独立模块，每个智能体负责一个明确的功能：

- **Screenwriter（编剧）**: 根据创意生成完整故事，并将故事改编为分场景剧本
- **CharacterExtractor（角色提取器）**: 从故事文本中识别和提取所有角色及其特征
- **CharacterPortraitsGenerator（角色画像生成器）**: 为每个角色生成标准化的正面、侧面、背面画像
- **SceneExtractor（场景提取器）**: 从剧本中提取场景信息
- **EventExtractor（事件提取器）**: 从剧本中提取关键事件
- **StoryboardArtist（分镜艺术家）**: 将剧本转换为详细的分镜描述
- **CameraImageGenerator（镜头图像生成器）**: 根据分镜描述生成图像
- **ReferenceImageSelector（参考图选择器）**: 为图像生成选择合适的参考图
- **BestImageSelector（最佳图像选择器）**: 从多个生成的图像中选择最佳结果

#### Pipelines（流水线）

流水线协调多个智能体和工具，实现端到端的视频生成工作流：

- **Idea2VideoPipeline**: 从创意到视频的完整流程
  - 输入：创意描述、用户需求、风格
  - 输出：完整视频文件
  - 流程：创意 → 故事 → 剧本 → 角色提取 → 角色画像 → 分场景视频 → 合成

- **Script2VideoPipeline**: 从剧本到视频的流程
  - 输入：剧本文本、用户需求、风格、角色信息
  - 输出：场景视频文件
  - 流程：剧本 → 分镜 → 图像生成 → 视频生成

- **Novel2MoviePipeline**: 从小说到电影的流程（适用于长文本）
  - 输入：小说文本
  - 输出：电影视频
  - 流程：小说压缩 → 剧本规划 → 场景生成 → 视频合成

#### Tools（工具）

工具是对外部 API 的封装，提供统一的接口：

- **ImageGenerator**: 图像生成工具的基类
  - 实现：DoubaoSeedream、NanobananaGoogle 等
  - 核心方法：`generate_single_image(prompt, reference_images, size, **kwargs)`

- **VideoGenerator**: 视频生成工具的基类
  - 实现：DoubaoSeedance、VeoGoogle 等
  - 核心方法：`generate_single_video(prompt, reference_image_path, duration, **kwargs)`

- **Reranker**: 重排序工具
  - 用于从多个候选结果中选择最佳结果

#### Interfaces（接口）

接口定义了系统中传递的数据结构，使用 Pydantic 进行数据验证：

- **CharacterInScene**: 角色信息（名称、描述、特征等）
- **Scene**: 场景信息（地点、时间、氛围等）
- **Event**: 事件信息（动作、对话、情感等）
- **ShotDescription**: 镜头描述（构图、运镜、内容等）
- **Camera**: 镜头参数（角度、运动、焦距等）
- **ImageOutput**: 图像输出（格式、数据、路径等）
- **VideoOutput**: 视频输出（格式、数据、路径等）

#### Utils（工具函数）

提供通用的辅助功能：

- **image.py**: 图像处理（格式转换、Base64 编码、保存等）
- **video.py**: 视频处理（合成、剪辑、格式转换等）
- **retry.py**: 重试机制（处理 API 调用失败）
- **timer.py**: 计时工具（性能监控）

## 添加新智能体

### 智能体开发流程

添加新智能体通常包括以下步骤：

1. **定义智能体职责**：明确智能体要完成的任务
2. **设计输入输出**：确定智能体的输入参数和输出格式
3. **实现智能体类**：编写智能体代码
4. **集成到流水线**：在流水线中使用新智能体
5. **测试验证**：确保智能体正常工作

### 完整示例：创建情感分析智能体

假设我们要创建一个 `SentimentAnalyzer` 智能体，用于分析剧本中的情感基调。

#### 步骤 1：创建智能体文件

在 `agents/` 目录下创建 `sentiment_analyzer.py`：

```python
# agents/sentiment_analyzer.py
import logging
from typing import List, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt

# 定义输出数据结构
class SentimentAnalysis(BaseModel):
    """情感分析结果"""
    overall_sentiment: str = Field(
        ...,
        description="整体情感基调：positive（积极）、negative（消极）、neutral（中性）"
    )
    emotional_arc: List[str] = Field(
        ...,
        description="情感曲线：按场景顺序描述情感变化"
    )
    key_emotional_moments: List[Dict[str, str]] = Field(
        ...,
        description="关键情感时刻：包含场景和情感描述"
    )
    confidence_score: float = Field(
        ...,
        description="分析置信度（0-1）"
    )

# 定义系统提示词
SYSTEM_PROMPT = """
[Role]
You are an expert in emotional analysis and narrative psychology. You can identify 
emotional tones, character emotional states, and emotional arcs in scripts.

[Task]
Analyze the emotional content of the provided script and identify:
1. The overall emotional tone of the script
2. The emotional arc across scenes
3. Key emotional moments that drive the narrative
4. Your confidence in this analysis

[Output]
{format_instructions}

[Guidelines]
- Consider both explicit emotions (dialogue, actions) and implicit emotions (subtext, atmosphere)
- Identify emotional turning points in the narrative
- Provide specific scene references for key emotional moments
- Be objective and evidence-based in your analysis
"""

HUMAN_PROMPT = """
<SCRIPT>
{script}
</SCRIPT>

Please analyze the emotional content of this script.
"""

class SentimentAnalyzer:
    """情感分析智能体
    
    该智能体分析剧本的情感基调、情感曲线和关键情感时刻。
    
    Attributes:
        chat_model: 用于分析的语言模型
    """
    
    def __init__(self, chat_model):
        """初始化情感分析智能体
        
        Args:
            chat_model: LangChain 聊天模型实例
        """
        self.chat_model = chat_model
        self.logger = logging.getLogger(__name__)
    
    @retry(stop=stop_after_attempt(3))
    async def analyze_sentiment(self, script: str) -> SentimentAnalysis:
        """分析剧本的情感内容
        
        Args:
            script: 剧本文本
            
        Returns:
            SentimentAnalysis: 情感分析结果
            
        Raises:
            Exception: 当 API 调用失败或解析失败时
        """
        self.logger.info("开始分析剧本情感...")
        
        # 创建输出解析器
        parser = PydanticOutputParser(pydantic_object=SentimentAnalysis)
        format_instructions = parser.get_format_instructions()
        
        # 构建提示词
        messages = [
            ("system", SYSTEM_PROMPT.format(format_instructions=format_instructions)),
            ("human", HUMAN_PROMPT.format(script=script)),
        ]
        
        # 调用模型
        response = await self.chat_model.ainvoke(messages)
        
        # 解析输出
        result = parser.parse(response.content)
        
        self.logger.info(f"情感分析完成，整体基调：{result.overall_sentiment}")
        return result
    
    async def __call__(self, script: str) -> SentimentAnalysis:
        """便捷调用方法
        
        Args:
            script: 剧本文本
            
        Returns:
            SentimentAnalysis: 情感分析结果
        """
        return await self.analyze_sentiment(script)
```

#### 步骤 2：在 `agents/__init__.py` 中导出

```python
# agents/__init__.py
from agents.screenwriter import Screenwriter
from agents.character_extractor import CharacterExtractor
# ... 其他导入 ...
from agents.sentiment_analyzer import SentimentAnalyzer  # 添加新智能体

__all__ = [
    "Screenwriter",
    "CharacterExtractor",
    # ... 其他导出 ...
    "SentimentAnalyzer",  # 导出新智能体
]
```

#### 步骤 3：在流水线中使用

```python
# 在 pipelines/idea2video_pipeline.py 或自定义流水线中使用
from agents import SentimentAnalyzer

class CustomPipeline:
    def __init__(self, chat_model, ...):
        self.chat_model = chat_model
        # 初始化情感分析智能体
        self.sentiment_analyzer = SentimentAnalyzer(chat_model=self.chat_model)
    
    async def process_script(self, script: str):
        # 分析剧本情感
        sentiment_result = await self.sentiment_analyzer.analyze_sentiment(script)
        
        print(f"整体情感基调：{sentiment_result.overall_sentiment}")
        print(f"情感曲线：{sentiment_result.emotional_arc}")
        
        # 根据情感分析结果调整后续处理...
        return sentiment_result
```

#### 步骤 4：测试智能体

创建测试脚本 `test_sentiment_analyzer.py`：

```python
import asyncio
from langchain.chat_models import init_chat_model
from agents import SentimentAnalyzer

async def test_sentiment_analyzer():
    # 初始化模型
    chat_model = init_chat_model(
        model="gpt-4",
        model_provider="openai",
        api_key="your-api-key"
    )
    
    # 创建智能体
    analyzer = SentimentAnalyzer(chat_model=chat_model)
    
    # 测试剧本
    test_script = """
    场景一：清晨的咖啡馆
    小李独自坐在角落，望着窗外的雨。他的手机响了，是前女友的消息。
    
    场景二：公园长椅
    小李在雨中奔跑，终于在长椅上找到了她。两人相视而笑。
    """
    
    # 执行分析
    result = await analyzer(test_script)
    
    print(f"整体情感：{result.overall_sentiment}")
    print(f"情感曲线：{result.emotional_arc}")
    print(f"关键时刻：{result.key_emotional_moments}")
    print(f"置信度：{result.confidence_score}")

if __name__ == "__main__":
    asyncio.run(test_sentiment_analyzer())
```

### 智能体开发最佳实践

1. **使用 Pydantic 定义输出结构**：确保输出格式清晰且可验证
2. **添加重试机制**：使用 `@retry` 装饰器处理 API 调用失败
3. **记录日志**：使用 `logging` 记录关键步骤和错误
4. **编写 Docstring**：为类和方法添加清晰的文档字符串
5. **异步设计**：使用 `async/await` 提高并发性能
6. **错误处理**：捕获并妥善处理可能的异常
7. **提示词工程**：精心设计系统提示词和人类提示词
8. **可配置性**：通过参数控制智能体行为，避免硬编码

## 添加新工具

### 工具开发流程

添加新工具（外部 API 封装）的步骤：

1. **选择 API 服务**：确定要集成的外部服务
2. **设计统一接口**：确保与现有工具接口兼容
3. **实现工具类**：封装 API 调用逻辑
4. **配置支持**：在配置文件中支持新工具
5. **测试验证**：确保工具正常工作

### 完整示例：创建音频生成工具

假设我们要集成一个新的音频生成 API，创建 `AudioGenerator` 工具。

#### 步骤 1：创建工具文件

在 `tools/` 目录下创建 `audio_generator_example_api.py`：

```python
# tools/audio_generator_example_api.py
import logging
import aiohttp
from typing import Optional
from tenacity import retry, stop_after_attempt
from utils.retry import after_func

class AudioGeneratorExampleAPI:
    """示例音频生成 API 封装
    
    该工具封装了外部音频生成 API，提供统一的接口用于生成音频。
    
    Attributes:
        api_key: API 密钥
        base_url: API 基础 URL
        model: 使用的模型名称
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "audio-gen-v1",
        base_url: str = "https://api.example.com/v1/audio",
    ):
        """初始化音频生成工具
        
        Args:
            api_key: API 密钥
            model: 模型名称，默认为 "audio-gen-v1"
            base_url: API 基础 URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.logger = logging.getLogger(__name__)
    
    @retry(stop=stop_after_attempt(3), after=after_func)
    async def generate_audio(
        self,
        text: str,
        voice: str = "default",
        duration: Optional[float] = None,
        format: str = "mp3",
        **kwargs,
    ) -> str:
        """生成音频
        
        Args:
            text: 要转换为音频的文本或音频描述
            voice: 语音类型，如 "male", "female", "child" 等
            duration: 音频时长（秒），None 表示自动
            format: 输出格式，如 "mp3", "wav"
            **kwargs: 其他 API 特定参数
            
        Returns:
            str: 生成的音频文件 URL 或路径
            
        Raises:
            Exception: 当 API 调用失败时
        """
        self.logger.info(f"正在使用 {self.model} 生成音频...")
        
        # 构建请求负载
        payload = {
            "model": self.model,
            "text": text,
            "voice": voice,
            "format": format,
        }
        
        if duration is not None:
            payload["duration"] = duration
        
        # 添加额外参数
        payload.update(kwargs)
        
        # 设置请求头
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        try:
            # 发送异步 HTTP 请求
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    json=payload,
                    headers=headers
                ) as response:
                    # 检查响应状态
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(
                            f"API 请求失败 (状态码 {response.status}): {error_text}"
                        )
                    
                    # 解析响应
                    response_json = await response.json()
                    
        except aiohttp.ClientError as e:
            self.logger.error(f"网络请求错误: {e}")
            raise Exception(f"音频生成失败: {e}")
        except Exception as e:
            self.logger.error(f"音频生成过程中发生错误: {e}")
            raise
        
        # 提取音频 URL
        audio_url = response_json.get("data", {}).get("url")
        
        if not audio_url:
            raise Exception("API 响应中未找到音频 URL")
        
        self.logger.info(f"✅ 音频生成成功: {audio_url}")
        return audio_url
    
    async def __call__(self, text: str, **kwargs) -> str:
        """便捷调用方法
        
        Args:
            text: 要转换为音频的文本
            **kwargs: 其他参数
            
        Returns:
            str: 生成的音频 URL
        """
        return await self.generate_audio(text, **kwargs)
```

#### 步骤 2：在 `tools/__init__.py` 中导出

```python
# tools/__init__.py
from tools.image_generator_doubao_seedream_yunwu_api import ImageGeneratorDoubaoSeedreamYunwuAPI
from tools.video_generator_veo_google_api import VideoGeneratorVeoGoogleAPI
# ... 其他导入 ...
from tools.audio_generator_example_api import AudioGeneratorExampleAPI  # 添加新工具

__all__ = [
    "ImageGeneratorDoubaoSeedreamYunwuAPI",
    "VideoGeneratorVeoGoogleAPI",
    # ... 其他导出 ...
    "AudioGeneratorExampleAPI",  # 导出新工具
]
```

#### 步骤 3：在配置文件中支持

创建或修改配置文件以支持新工具：

```yaml
# configs/custom_pipeline.yaml
chat_model:
  init_args:
    model: gpt-4
    model_provider: openai
    api_key: your-openai-key

image_generator:
  class_path: tools.ImageGeneratorDoubaoSeedreamYunwuAPI
  init_args:
    api_key: your-image-key

video_generator:
  class_path: tools.VideoGeneratorVeoGoogleAPI
  init_args:
    api_key: your-video-key

# 添加音频生成器配置
audio_generator:
  class_path: tools.AudioGeneratorExampleAPI
  init_args:
    api_key: your-audio-key
    model: audio-gen-v1
    base_url: https://api.example.com/v1/audio

working_dir: .working_dir/custom_pipeline
```

#### 步骤 4：在流水线中使用

```python
# 在自定义流水线中使用新工具
import yaml
import importlib

class CustomPipeline:
    @classmethod
    def init_from_config(cls, config_path: str):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        # 动态加载音频生成器
        audio_gen_cls_module, audio_gen_cls_name = config["audio_generator"]["class_path"].rsplit(".", 1)
        audio_gen_cls = getattr(importlib.import_module(audio_gen_cls_module), audio_gen_cls_name)
        audio_gen_args = config["audio_generator"]["init_args"]
        audio_generator = audio_gen_cls(**audio_gen_args)
        
        return cls(audio_generator=audio_generator, ...)
    
    def __init__(self, audio_generator, ...):
        self.audio_generator = audio_generator
    
    async def generate_narration(self, text: str):
        # 使用音频生成器
        audio_url = await self.audio_generator.generate_audio(
            text=text,
            voice="narrator",
            format="mp3"
        )
        return audio_url
```

#### 步骤 5：测试工具

创建测试脚本：

```python
# test_audio_generator.py
import asyncio
from tools import AudioGeneratorExampleAPI

async def test_audio_generator():
    # 初始化工具
    generator = AudioGeneratorExampleAPI(
        api_key="your-api-key",
        model="audio-gen-v1"
    )
    
    # 测试生成音频
    audio_url = await generator.generate_audio(
        text="这是一段测试音频",
        voice="female",
        format="mp3"
    )
    
    print(f"生成的音频 URL: {audio_url}")

if __name__ == "__main__":
    asyncio.run(test_audio_generator())
```

### 工具开发最佳实践

1. **统一接口设计**：确保核心方法签名与同类工具一致
2. **异步 HTTP 请求**：使用 `aiohttp` 进行异步网络请求
3. **重试机制**：使用 `@retry` 装饰器处理临时性失败
4. **错误处理**：捕获并提供清晰的错误信息
5. **日志记录**：记录关键操作和错误
6. **参数验证**：验证输入参数的有效性
7. **配置灵活性**：通过配置文件支持不同的 API 服务
8. **文档完善**：为所有公共方法添加详细的 Docstring

## 代码风格与最佳实践

### Python 代码规范

ViMax 项目遵循 [PEP 8](https://peps.python.org/pep-0008/) Python 代码风格指南。

#### 命名规范

```python
# 类名：使用 PascalCase（大驼峰）
class VideoGenerator:
    pass

# 函数和方法名：使用 snake_case（下划线）
def generate_video():
    pass

async def process_script():
    pass

# 变量名：使用 snake_case
user_input = "创意描述"
api_key = "your-key"

# 常量：使用 UPPER_CASE（全大写）
MAX_RETRY_ATTEMPTS = 3
DEFAULT_MODEL = "gpt-4"

# 私有方法和属性：使用前导下划线
def _internal_helper():
    pass

self._private_attribute = value
```

#### 导入规范

```python
# 标准库导入
import os
import logging
from typing import List, Dict, Optional

# 第三方库导入
import yaml
import aiohttp
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

# 本地模块导入
from agents import Screenwriter
from tools import ImageGeneratorDoubaoSeedreamYunwuAPI
from interfaces import CharacterInScene
from utils.retry import after_func
```

#### 类型注解

使用类型注解提高代码可读性和可维护性：

```python
from typing import List, Dict, Optional, Union

async def generate_images(
    prompts: List[str],
    reference_images: Optional[List[str]] = None,
    size: str = "1024x1024",
) -> List[str]:
    """生成多张图像
    
    Args:
        prompts: 图像描述列表
        reference_images: 可选的参考图像路径列表
        size: 图像尺寸
        
    Returns:
        List[str]: 生成的图像 URL 列表
    """
    results: List[str] = []
    # 实现...
    return results
```

#### Docstring 规范

使用 Google 风格的 Docstring：

```python
class ImageGenerator:
    """图像生成器基类
    
    该类定义了图像生成器的通用接口，所有具体的图像生成器
    实现都应该继承此类并实现其方法。
    
    Attributes:
        api_key: API 密钥
        model: 使用的模型名称
        base_url: API 基础 URL
        
    Example:
        >>> generator = ImageGenerator(api_key="your-key")
        >>> image_url = await generator.generate_image("a cat")
    """
    
    def __init__(self, api_key: str, model: str = "default"):
        """初始化图像生成器
        
        Args:
            api_key: API 密钥
            model: 模型名称，默认为 "default"
            
        Raises:
            ValueError: 当 api_key 为空时
        """
        if not api_key:
            raise ValueError("API key 不能为空")
        
        self.api_key = api_key
        self.model = model
    
    async def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
    ) -> str:
        """生成单张图像
        
        根据提供的文本描述生成图像。
        
        Args:
            prompt: 图像描述文本
            size: 图像尺寸，格式为 "宽x高"
            
        Returns:
            str: 生成的图像 URL
            
        Raises:
            Exception: 当 API 调用失败时
            
        Note:
            此方法需要在子类中实现具体逻辑
        """
        raise NotImplementedError("子类必须实现此方法")
```

### 异步编程最佳实践

#### 使用 async/await

```python
# ✅ 推荐：使用 async/await
async def process_multiple_scripts(scripts: List[str]):
    tasks = [process_single_script(script) for script in scripts]
    results = await asyncio.gather(*tasks)
    return results

# ❌ 避免：在异步函数中使用同步阻塞调用
async def bad_example():
    # 这会阻塞事件循环
    time.sleep(5)  # 不要这样做！
    
# ✅ 正确做法
async def good_example():
    await asyncio.sleep(5)  # 使用异步睡眠
```

#### 并发控制

```python
import asyncio
from typing import List

async def process_with_concurrency_limit(
    items: List[str],
    max_concurrent: int = 5
):
    """限制并发数量的处理
    
    Args:
        items: 要处理的项目列表
        max_concurrent: 最大并发数
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_with_semaphore(item: str):
        async with semaphore:
            return await process_item(item)
    
    tasks = [process_with_semaphore(item) for item in items]
    results = await asyncio.gather(*tasks)
    return results
```

### 错误处理最佳实践

```python
import logging

logger = logging.getLogger(__name__)

async def robust_api_call(prompt: str):
    """健壮的 API 调用示例"""
    try:
        # 尝试调用 API
        result = await api_client.generate(prompt)
        return result
        
    except aiohttp.ClientError as e:
        # 处理网络错误
        logger.error(f"网络请求失败: {e}")
        raise Exception(f"无法连接到 API 服务: {e}")
        
    except ValueError as e:
        # 处理参数错误
        logger.error(f"参数错误: {e}")
        raise
        
    except Exception as e:
        # 处理其他未预期的错误
        logger.exception(f"未预期的错误: {e}")
        raise Exception(f"API 调用失败: {e}")
    
    finally:
        # 清理资源
        logger.info("API 调用完成")
```

### 日志记录最佳实践

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def process_pipeline():
    logger.info("开始处理流水线")
    
    try:
        # 处理步骤 1
        logger.debug("执行步骤 1: 生成故事")
        story = await generate_story()
        logger.info(f"✅ 故事生成完成，长度: {len(story)} 字符")
        
        # 处理步骤 2
        logger.debug("执行步骤 2: 提取角色")
        characters = await extract_characters(story)
        logger.info(f"✅ 提取到 {len(characters)} 个角色")
        
    except Exception as e:
        logger.error(f"❌ 流水线处理失败: {e}", exc_info=True)
        raise
    
    logger.info("流水线处理完成")
```

### 配置管理最佳实践

```python
import yaml
from typing import Dict, Any

def load_config(config_path: str) -> Dict[str, Any]:
    """加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        Dict[str, Any]: 配置字典
        
    Raises:
        FileNotFoundError: 当配置文件不存在时
        yaml.YAMLError: 当配置文件格式错误时
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"配置文件格式错误: {e}")

# 使用环境变量覆盖配置
import os

def get_api_key(config: Dict[str, Any], key_name: str) -> str:
    """获取 API Key，优先使用环境变量
    
    Args:
        config: 配置字典
        key_name: 配置中的 key 名称
        
    Returns:
        str: API Key
    """
    # 优先使用环境变量
    env_key = os.getenv(f"{key_name.upper()}_API_KEY")
    if env_key:
        return env_key
    
    # 否则使用配置文件中的值
    return config.get(key_name, {}).get("api_key", "")
```

## 测试与调试

### 单元测试

虽然项目当前没有完整的测试套件，但建议为新功能编写测试。

#### 测试框架推荐

```bash
# 安装 pytest
pip install pytest pytest-asyncio pytest-cov
```

#### 测试示例

创建 `tests/test_agents.py`：

```python
import pytest
from unittest.mock import Mock, AsyncMock
from agents import Screenwriter

@pytest.mark.asyncio
async def test_screenwriter_develop_story():
    """测试编剧智能体生成故事功能"""
    # 创建模拟的聊天模型
    mock_chat_model = AsyncMock()
    mock_response = Mock()
    mock_response.content = "这是一个生成的故事..."
    mock_chat_model.ainvoke.return_value = mock_response
    
    # 创建编剧智能体
    screenwriter = Screenwriter(chat_model=mock_chat_model)
    
    # 测试生成故事
    story = await screenwriter.develop_story(
        idea="一个关于时间旅行的故事",
        user_requirement="适合青少年观看"
    )
    
    # 验证结果
    assert story == "这是一个生成的故事..."
    assert mock_chat_model.ainvoke.called
    
@pytest.mark.asyncio
async def test_screenwriter_write_script():
    """测试编剧智能体编写剧本功能"""
    mock_chat_model = AsyncMock()
    mock_response = Mock()
    mock_response.content = '{"script": ["场景一", "场景二"]}'
    mock_chat_model.ainvoke.return_value = mock_response
    
    screenwriter = Screenwriter(chat_model=mock_chat_model)
    
    script = await screenwriter.write_script_based_on_story(
        story="一个完整的故事",
        user_requirement="分为2个场景"
    )
    
    assert isinstance(script, list)
    assert len(script) == 2
```

#### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_agents.py

# 运行特定测试函数
pytest tests/test_agents.py::test_screenwriter_develop_story

# 显示详细输出
pytest -v

# 生成覆盖率报告
pytest --cov=agents --cov-report=html
```

### 集成测试

创建端到端测试来验证完整流程：

```python
# tests/test_integration.py
import pytest
import os
from pipelines import Idea2VideoPipeline

@pytest.mark.asyncio
@pytest.mark.integration
async def test_idea2video_pipeline_end_to_end():
    """端到端测试 Idea2Video 流水线"""
    # 跳过如果没有配置 API Keys
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("需要配置 API Keys")
    
    # 初始化流水线
    pipeline = Idea2VideoPipeline.init_from_config(
        config_path="configs/idea2video.yaml"
    )
    
    # 运行流水线（使用简短的测试输入）
    result = await pipeline(
        idea="一只猫在追逐蝴蝶",
        user_requirement="10秒短视频",
        style="卡通风格"
    )
    
    # 验证结果
    assert os.path.exists(result)
    assert result.endswith(".mp4")
```

### 调试技巧

#### 使用 Python 调试器

```python
# 在代码中设置断点
import pdb

async def debug_example():
    story = await generate_story()
    
    # 设置断点
    pdb.set_trace()
    
    # 继续执行...
    characters = await extract_characters(story)
```

#### 使用 IPython 进行交互式调试

```bash
# 安装 IPython
pip install ipython

# 在代码中使用
from IPython import embed

async def debug_with_ipython():
    story = await generate_story()
    
    # 进入交互式 shell
    embed()
    
    # 可以在 shell 中检查变量
```

#### 日志调试

```python
import logging

# 设置详细日志级别
logging.basicConfig(level=logging.DEBUG)

# 或者只为特定模块设置
logging.getLogger("agents").setLevel(logging.DEBUG)
logging.getLogger("tools").setLevel(logging.DEBUG)
```

#### 保存中间结果

在开发和调试时，保存中间结果非常有用：

```python
import json
import os

async def debug_pipeline():
    # 创建调试目录
    debug_dir = ".debug_output"
    os.makedirs(debug_dir, exist_ok=True)
    
    # 生成故事
    story = await generate_story()
    with open(f"{debug_dir}/story.txt", "w", encoding="utf-8") as f:
        f.write(story)
    
    # 提取角色
    characters = await extract_characters(story)
    with open(f"{debug_dir}/characters.json", "w", encoding="utf-8") as f:
        json.dump([c.model_dump() for c in characters], f, ensure_ascii=False, indent=2)
    
    print(f"调试输出已保存到 {debug_dir}/")
```

#### 性能分析

```python
import time
import asyncio
from functools import wraps

def async_timer(func):
    """异步函数计时装饰器"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 耗时: {end - start:.2f} 秒")
        return result
    return wrapper

@async_timer
async def generate_story(idea: str):
    # 实现...
    pass
```

### 常见问题调试

#### API 调用失败

```python
# 添加详细的错误日志
try:
    response = await api_client.generate(prompt)
except Exception as e:
    logger.error(f"API 调用失败")
    logger.error(f"Prompt: {prompt}")
    logger.error(f"错误信息: {e}")
    logger.error(f"错误类型: {type(e).__name__}")
    raise
```

#### 内存问题

```python
import gc
import psutil

def log_memory_usage():
    """记录当前内存使用情况"""
    process = psutil.Process()
    memory_info = process.memory_info()
    print(f"内存使用: {memory_info.rss / 1024 / 1024:.2f} MB")

# 在关键位置检查内存
log_memory_usage()
await process_large_data()
log_memory_usage()

# 手动触发垃圾回收
gc.collect()
```

#### 异步问题

```python
# 检查是否在事件循环中
import asyncio

def check_event_loop():
    try:
        loop = asyncio.get_running_loop()
        print(f"当前事件循环: {loop}")
    except RuntimeError:
        print("没有运行中的事件循环")

# 调试异步任务
async def debug_async_tasks():
    tasks = asyncio.all_tasks()
    print(f"当前运行的任务数: {len(tasks)}")
    for task in tasks:
        print(f"任务: {task.get_name()}, 状态: {task.done()}")
```

## 提交代码

### Git 工作流程

#### 1. 同步上游代码

在开始新功能开发前，先同步最新代码：

```bash
# 获取上游更新
git fetch upstream

# 切换到主分支
git checkout main

# 合并上游更新
git merge upstream/main

# 推送到您的 Fork
git push origin main
```

#### 2. 创建功能分支

为每个新功能或修复创建独立的分支：

```bash
# 创建并切换到新分支
git checkout -b feature/sentiment-analyzer

# 或者修复 bug
git checkout -b fix/api-timeout-issue

# 或者改进文档
git checkout -b docs/update-development-guide
```

分支命名规范：
- `feature/` - 新功能
- `fix/` - Bug 修复
- `docs/` - 文档更新
- `refactor/` - 代码重构
- `test/` - 测试相关

#### 3. 提交更改

```bash
# 查看更改
git status

# 添加文件到暂存区
git add agents/sentiment_analyzer.py
git add tests/test_sentiment_analyzer.py

# 或添加所有更改
git add .

# 提交更改（使用清晰的提交信息）
git commit -m "feat: 添加情感分析智能体

- 实现 SentimentAnalyzer 类
- 支持分析剧本的情感基调和情感曲线
- 添加单元测试
- 更新文档"
```

#### 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<类型>(<范围>): <简短描述>

<详细描述>

<footer>
```

类型：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建或辅助工具

示例：

```bash
# 新功能
git commit -m "feat(agents): 添加情感分析智能体"

# Bug 修复
git commit -m "fix(tools): 修复图像生成 API 超时问题"

# 文档更新
git commit -m "docs: 更新开发指南中的测试章节"

# 重构
git commit -m "refactor(pipelines): 优化流水线错误处理逻辑"
```

#### 4. 推送到远程仓库

```bash
# 推送分支到您的 Fork
git push origin feature/sentiment-analyzer

# 如果是第一次推送该分支
git push -u origin feature/sentiment-analyzer
```

#### 5. 创建 Pull Request

1. 访问您 Fork 的 GitHub 页面
2. 点击 "Compare & pull request" 按钮
3. 填写 PR 标题和描述：

```markdown
## 描述

添加了情感分析智能体，用于分析剧本的情感基调和情感曲线。

## 更改内容

- 新增 `agents/sentiment_analyzer.py`
- 新增 `tests/test_sentiment_analyzer.py`
- 更新 `agents/__init__.py` 导出新智能体
- 更新文档 `docs/agents.md`

## 测试

- [x] 单元测试通过
- [x] 集成测试通过
- [x] 手动测试通过

## 相关 Issue

Closes #123
```

4. 等待代码审查和反馈

### 代码审查清单

在提交 PR 前，请自查以下内容：

#### 代码质量
- [ ] 代码遵循 PEP 8 规范
- [ ] 所有函数和类都有 Docstring
- [ ] 使用了类型注解
- [ ] 没有未使用的导入和变量
- [ ] 错误处理完善

#### 功能完整性
- [ ] 功能按预期工作
- [ ] 边界情况已处理
- [ ] 添加了必要的配置选项
- [ ] 与现有代码集成良好

#### 测试
- [ ] 添加了单元测试
- [ ] 测试覆盖率足够
- [ ] 所有测试通过
- [ ] 手动测试通过

#### 文档
- [ ] 更新了相关文档
- [ ] 添加了使用示例
- [ ] 更新了 API 参考（如适用）
- [ ] 提交信息清晰

#### 性能
- [ ] 没有明显的性能问题
- [ ] 资源使用合理
- [ ] 异步操作正确实现

### Pre-commit Hooks

使用 pre-commit hooks 自动检查代码质量：

```bash
# 安装 pre-commit
pip install pre-commit

# 安装 hooks
pre-commit install
```

创建 `.pre-commit-config.yaml`：

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.12
        
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100', '--ignore=E203,W503']
```

现在每次提交时会自动运行这些检查：

```bash
git commit -m "feat: 添加新功能"
# pre-commit hooks 会自动运行
```

### 持续集成（CI）

如果项目配置了 CI（如 GitHub Actions），确保：

1. 所有 CI 检查通过
2. 测试覆盖率达标
3. 代码质量检查通过
4. 构建成功

查看 CI 状态：
- 在 PR 页面查看检查结果
- 点击详情查看失败原因
- 修复问题后重新推送

## 相关资源

### 官方文档

- [Python 官方文档](https://docs.python.org/3/)
- [PEP 8 代码风格指南](https://peps.python.org/pep-0008/)
- [LangChain 文档](https://python.langchain.com/)
- [Pydantic 文档](https://docs.pydantic.dev/)
- [aiohttp 文档](https://docs.aiohttp.org/)

### 项目文档

- [快速开始](./getting_started.md) - 了解如何使用 ViMax
- [系统架构](./architecture.md) - 理解系统设计
- [智能体详解](./agents.md) - 深入了解智能体
- [流水线详解](./pipelines.md) - 了解流水线工作原理
- [工具详解](./tools.md) - 了解工具集成
- [API 参考](./api_reference.md) - 查阅 API 文档
- [配置详解](./configuration.md) - 了解配置选项
- [示例与最佳实践](./examples.md) - 学习实际应用
- [故障排查](./troubleshooting.md) - 解决常见问题
- [常见问题](./faq.md) - 查看常见疑问

### 开发工具

- [uv](https://github.com/astral-sh/uv) - 快速的 Python 包管理器
- [pytest](https://docs.pytest.org/) - Python 测试框架
- [black](https://black.readthedocs.io/) - Python 代码格式化工具
- [isort](https://pycqa.github.io/isort/) - Python 导入排序工具
- [flake8](https://flake8.pycqa.org/) - Python 代码检查工具
- [mypy](https://mypy.readthedocs.io/) - Python 静态类型检查
- [pre-commit](https://pre-commit.com/) - Git hooks 管理工具

### 学习资源

- [异步编程教程](https://realpython.com/async-io-python/)
- [Pydantic 教程](https://docs.pydantic.dev/latest/concepts/models/)
- [LangChain 快速开始](https://python.langchain.com/docs/get_started/quickstart)
- [Python 类型注解指南](https://realpython.com/python-type-checking/)

### 社区与支持

- **GitHub Issues**: 报告 Bug 或提出功能请求
- **GitHub Discussions**: 讨论想法和最佳实践
- **Pull Requests**: 贡献代码和文档

### 开发环境推荐

#### IDE 和编辑器

- **VS Code**: 推荐安装以下扩展
  - Python
  - Pylance
  - Python Test Explorer
  - GitLens
  - YAML

- **PyCharm**: 专业的 Python IDE
  - 内置调试器
  - 代码分析
  - 重构工具

#### 终端工具

- **iTerm2** (macOS) 或 **Windows Terminal** (Windows)
- **Oh My Zsh** - 增强的 shell 体验
- **tmux** - 终端复用器

### 贡献指南

感谢您考虑为 ViMax 做出贡献！我们欢迎：

- **代码贡献**: 新功能、Bug 修复、性能优化
- **文档改进**: 修正错误、添加示例、改进说明
- **测试**: 添加测试用例、提高覆盖率
- **问题报告**: 报告 Bug、提出改进建议
- **代码审查**: 审查其他人的 PR

#### 贡献流程

1. Fork 项目
2. 创建功能分支
3. 编写代码和测试
4. 提交 Pull Request
5. 参与代码审查
6. 合并到主分支

#### 行为准则

- 尊重所有贡献者
- 提供建设性的反馈
- 保持专业和友好
- 遵循项目规范

### 获取帮助

如果您在开发过程中遇到问题：

1. **查阅文档**: 首先查看相关文档
2. **搜索 Issues**: 看看是否有人遇到过类似问题
3. **提问**: 在 GitHub Discussions 或 Issues 中提问
4. **调试**: 使用本文档中的调试技巧
5. **联系维护者**: 如果问题紧急，可以直接联系项目维护者

### 版本发布

项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

- **主版本号**: 不兼容的 API 变更
- **次版本号**: 向下兼容的功能新增
- **修订号**: 向下兼容的问题修正

### 许可证

本项目采用 [LICENSE](../LICENSE) 中指定的许可证。在贡献代码前，请确保您了解并同意许可证条款。

---

## 更新记录

- 2025-01-XX: 初始版本，包含完整的开发环境设置、代码结构、扩展指南和最佳实践

---

## 完整开发示例

本节提供完整的、可直接运行的开发示例，展示如何扩展 ViMax 的功能。

### 示例 1：创建自定义流水线

创建一个简化的流水线，只包含核心功能：

```python
# custom_simple_pipeline.py
import asyncio
import yaml
import importlib
from typing import Dict, Any
from langchain.chat_models import init_chat_model
from agents import Screenwriter, CharacterExtractor, StoryboardArtist

class SimplePipeline:
    """简化的视频生成流水线
    
    只包含故事生成、角色提取和分镜设计功能，
    不包含实际的图像和视频生成。
    """
    
    def __init__(
        self,
        chat_model,
        output_dir: str = ".working_dir/simple_pipeline"
    ):
        """初始化流水线
        
        Args:
            chat_model: 聊天模型实例
            output_dir: 输出目录
        """
        self.chat_model = chat_model
        self.output_dir = output_dir
        
        # 初始化智能体
        self.screenwriter = Screenwriter(chat_model=chat_model)
        self.character_extractor = CharacterExtractor(chat_model=chat_model)
        self.storyboard_artist = StoryboardArtist(chat_model=chat_model)
        
        # 创建输出目录
        import os
        os.makedirs(output_dir, exist_ok=True)
    
    @classmethod
    def init_from_config(cls, config_path: str):
        """从配置文件初始化流水线
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            SimplePipeline: 流水线实例
        """
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        # 初始化聊天模型
        chat_model_config = config["chat_model"]["init_args"]
        chat_model = init_chat_model(
            model=chat_model_config["model"],
            model_provider=chat_model_config["model_provider"],
            api_key=chat_model_config["api_key"],
            base_url=chat_model_config["base_url"]
        )
        
        # 获取工作目录
        working_dir = config.get("working_dir", ".working_dir/simple_pipeline")
        
        return cls(chat_model=chat_model, output_dir=working_dir)
    
    async def __call__(
        self,
        idea: str,
        user_requirement: str = "",
        style: str = "Realistic"
    ):
        """运行流水线
        
        Args:
            idea: 创意描述
            user_requirement: 用户需求
            style: 视觉风格
        """
        import json
        
        print("🚀 简化流水线开始运行...")
        print(f"📁 输出目录: {self.output_dir}")
        
        # 步骤 1：生成故事
        print("\n📝 步骤 1/4: 生成故事...")
        story = await self.screenwriter.develop_story(
            idea=idea,
            user_requirement=user_requirement
        )
        
        story_path = f"{self.output_dir}/story.txt"
        with open(story_path, "w", encoding="utf-8") as f:
            f.write(story)
        print(f"✅ 故事已保存: {story_path}")
        
        # 步骤 2：生成剧本
        print("\n🎬 步骤 2/4: 生成剧本...")
        script_scenes = await self.screenwriter.write_script_based_on_story(
            story=story,
            user_requirement=user_requirement
        )
        
        full_script = "\n\n".join(script_scenes)
        script_path = f"{self.output_dir}/script.txt"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(full_script)
        print(f"✅ 剧本已保存: {script_path} ({len(script_scenes)} 个场景)")
        
        # 步骤 3：提取角色
        print("\n🔍 步骤 3/4: 提取角色...")
        characters = await self.character_extractor.extract_characters(full_script)
        
        characters_data = [
            {
                "name": char.identifier_in_scene,
                "static_features": char.static_features,
                "dynamic_features": char.dynamic_features
            }
            for char in characters
        ]
        
        characters_path = f"{self.output_dir}/characters.json"
        with open(characters_path, "w", encoding="utf-8") as f:
            json.dump(characters_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 角色信息已保存: {characters_path} ({len(characters)} 个角色)")
        
        # 步骤 4：设计分镜
        print("\n📋 步骤 4/4: 设计分镜...")
        all_shot_descs = []
        
        for i, scene_script in enumerate(script_scenes, 1):
            print(f"  正在为场景 {i} 设计分镜...")
            
            shot_brief_descs = await self.storyboard_artist.design_storyboard(
                script=scene_script,
                characters=characters,
                user_requirement=user_requirement
            )
            
            for shot_brief in shot_brief_descs:
                shot_desc = await self.storyboard_artist.decompose_visual_description(
                    shot_brief_desc=shot_brief,
                    characters=characters
                )
                all_shot_descs.append(shot_desc)
            
            print(f"  ✅ 场景 {i} 完成 ({len(shot_brief_descs)} 个镜头)")
        
        # 保存分镜信息
        storyboard_data = [
            {
                "shot_idx": shot.idx,
                "camera_idx": shot.cam_idx,
                "first_frame": shot.ff_desc,
                "last_frame": shot.lf_desc,
                "motion": shot.motion_desc,
                "audio": shot.audio_desc
            }
            for shot in all_shot_descs
        ]
        
        storyboard_path = f"{self.output_dir}/storyboard.json"
        with open(storyboard_path, "w", encoding="utf-8") as f:
            json.dump(storyboard_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 分镜信息已保存: {storyboard_path} ({len(all_shot_descs)} 个镜头)")
        
        # 完成
        print("\n" + "=" * 60)
        print("🎉 简化流水线执行完成！")
        print(f"📁 所有输出文件保存在: {self.output_dir}/")
        print("=" * 60)

async def main():
    """运行示例"""
    # 初始化流水线
    pipeline = SimplePipeline.init_from_config("configs/idea2video.yaml")
    
    # 运行流水线
    await pipeline(
        idea="一个机器人学会了画画",
        user_requirement="温馨治愈风格，2个场景",
        style="Cartoon"
    )

if __name__ == "__main__":
    asyncio.run(main())
```

### 示例 2：扩展现有流水线

为现有流水线添加新功能（如情感分析）：

```python
# extended_pipeline.py
import asyncio
from pipelines.idea2video_pipeline import Idea2VideoPipeline
from agents.sentiment_analyzer import SentimentAnalyzer  # 假设已创建
import json

class ExtendedIdea2VideoPipeline(Idea2VideoPipeline):
    """扩展的 Idea2Video 流水线
    
    在原有流水线基础上添加情感分析功能。
    """
    
    def __init__(self, *args, **kwargs):
        """初始化扩展流水线"""
        super().__init__(*args, **kwargs)
        
        # 添加情感分析智能体
        self.sentiment_analyzer = SentimentAnalyzer(
            chat_model=self.chat_model
        )
    
    async def __call__(
        self,
        idea: str,
        user_requirement: str = "",
        style: str = "Realistic"
    ):
        """运行扩展流水线
        
        Args:
            idea: 创意描述
            user_requirement: 用户需求
            style: 视觉风格
        """
        print("🚀 扩展流水线开始运行...")
        
        # 步骤 1：生成故事（使用父类方法）
        print("\n📝 生成故事...")
        story = await self.screenwriter.develop_story(
            idea=idea,
            user_requirement=user_requirement
        )
        
        # 步骤 2：情感分析（新增功能）
        print("\n💭 分析故事情感...")
        sentiment_result = await self.sentiment_analyzer.analyze_sentiment(story)
        
        print(f"  整体情感: {sentiment_result.overall_sentiment}")
        print(f"  情感曲线: {', '.join(sentiment_result.emotional_arc)}")
        
        # 保存情感分析结果
        sentiment_path = f"{self.working_dir}/sentiment_analysis.json"
        with open(sentiment_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "overall_sentiment": sentiment_result.overall_sentiment,
                    "emotional_arc": sentiment_result.emotional_arc,
                    "key_moments": sentiment_result.key_emotional_moments,
                    "confidence": sentiment_result.confidence_score
                },
                f,
                ensure_ascii=False,
                indent=2
            )
        print(f"  ✅ 情感分析已保存: {sentiment_path}")
        
        # 步骤 3：根据情感调整用户需求
        enhanced_requirement = f"{user_requirement}\n情感基调: {sentiment_result.overall_sentiment}"
        
        # 步骤 4：继续执行原有流水线
        print("\n🎬 继续执行视频生成...")
        await super().__call__(
            idea=idea,
            user_requirement=enhanced_requirement,
            style=style
        )
        
        print("\n🎉 扩展流水线执行完成！")

async def main():
    """运行示例"""
    # 初始化扩展流水线
    pipeline = ExtendedIdea2VideoPipeline.init_from_config(
        "configs/idea2video.yaml"
    )
    
    # 运行流水线
    await pipeline(
        idea="一个孤独的老人与一只流浪猫成为朋友",
        user_requirement="温馨感人，适合全年龄观众",
        style="Realistic"
    )

if __name__ == "__main__":
    asyncio.run(main())
```

### 示例 3：创建插件系统

创建一个支持插件的流水线架构：

```python
# plugin_pipeline.py
import asyncio
from typing import List, Callable, Any
from pipelines.idea2video_pipeline import Idea2VideoPipeline

class Plugin:
    """插件基类"""
    
    def __init__(self, name: str):
        """初始化插件
        
        Args:
            name: 插件名称
        """
        self.name = name
    
    async def before_story(self, idea: str, **kwargs) -> dict:
        """在生成故事之前执行
        
        Args:
            idea: 创意描述
            **kwargs: 其他参数
            
        Returns:
            dict: 修改后的参数
        """
        return {"idea": idea, **kwargs}
    
    async def after_story(self, story: str, **kwargs) -> dict:
        """在生成故事之后执行
        
        Args:
            story: 生成的故事
            **kwargs: 其他参数
            
        Returns:
            dict: 修改后的参数
        """
        return {"story": story, **kwargs}
    
    async def before_script(self, story: str, **kwargs) -> dict:
        """在生成剧本之前执行"""
        return {"story": story, **kwargs}
    
    async def after_script(self, script: List[str], **kwargs) -> dict:
        """在生成剧本之后执行"""
        return {"script": script, **kwargs}

class LoggingPlugin(Plugin):
    """日志插件示例"""
    
    def __init__(self):
        super().__init__("LoggingPlugin")
    
    async def before_story(self, idea: str, **kwargs):
        print(f"[{self.name}] 开始生成故事，创意长度: {len(idea)} 字符")
        return {"idea": idea, **kwargs}
    
    async def after_story(self, story: str, **kwargs):
        print(f"[{self.name}] 故事生成完成，长度: {len(story)} 字符")
        return {"story": story, **kwargs}

class StoryEnhancerPlugin(Plugin):
    """故事增强插件示例"""
    
    def __init__(self, enhancement_prompt: str):
        super().__init__("StoryEnhancerPlugin")
        self.enhancement_prompt = enhancement_prompt
    
    async def before_story(self, idea: str, **kwargs):
        # 在创意中添加增强提示
        enhanced_idea = f"{idea}\n\n{self.enhancement_prompt}"
        print(f"[{self.name}] 已添加增强提示")
        return {"idea": enhanced_idea, **kwargs}

class PluginPipeline(Idea2VideoPipeline):
    """支持插件的流水线"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugins: List[Plugin] = []
    
    def register_plugin(self, plugin: Plugin):
        """注册插件
        
        Args:
            plugin: 插件实例
        """
        self.plugins.append(plugin)
        print(f"✅ 已注册插件: {plugin.name}")
    
    async def _run_plugin_hook(
        self,
        hook_name: str,
        **kwargs
    ) -> dict:
        """运行插件钩子
        
        Args:
            hook_name: 钩子名称
            **kwargs: 参数
            
        Returns:
            dict: 修改后的参数
        """
        result = kwargs
        for plugin in self.plugins:
            hook_method = getattr(plugin, hook_name, None)
            if hook_method:
                result = await hook_method(**result)
        return result
    
    async def __call__(
        self,
        idea: str,
        user_requirement: str = "",
        style: str = "Realistic"
    ):
        """运行插件流水线"""
        print("🚀 插件流水线开始运行...")
        
        # 运行 before_story 钩子
        params = await self._run_plugin_hook(
            "before_story",
            idea=idea,
            user_requirement=user_requirement,
            style=style
        )
        idea = params["idea"]
        
        # 生成故事
        print("\n📝 生成故事...")
        story = await self.screenwriter.develop_story(
            idea=idea,
            user_requirement=user_requirement
        )
        
        # 运行 after_story 钩子
        params = await self._run_plugin_hook(
            "after_story",
            story=story,
            user_requirement=user_requirement,
            style=style
        )
        story = params["story"]
        
        # 运行 before_script 钩子
        params = await self._run_plugin_hook(
            "before_script",
            story=story,
            user_requirement=user_requirement
        )
        
        # 生成剧本
        print("\n🎬 生成剧本...")
        script_scenes = await self.screenwriter.write_script_based_on_story(
            story=params["story"],
            user_requirement=user_requirement
        )
        
        # 运行 after_script 钩子
        params = await self._run_plugin_hook(
            "after_script",
            script=script_scenes
        )
        
        # 继续执行原有流水线...
        print("\n✅ 插件流水线执行完成！")

async def main():
    """运行示例"""
    # 初始化流水线
    pipeline = PluginPipeline.init_from_config("configs/idea2video.yaml")
    
    # 注册插件
    pipeline.register_plugin(LoggingPlugin())
    pipeline.register_plugin(
        StoryEnhancerPlugin(
            enhancement_prompt="请确保故事包含明确的起承转合结构"
        )
    )
    
    # 运行流水线
    await pipeline(
        idea="一个年轻人追寻梦想的故事",
        user_requirement="励志主题",
        style="Realistic"
    )

if __name__ == "__main__":
    asyncio.run(main())
```

### 示例 4：创建测试框架

为自定义智能体创建测试框架：

```python
# test_custom_agent.py
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from agents.sentiment_analyzer import SentimentAnalyzer  # 假设已创建

class TestSentimentAnalyzer:
    """情感分析智能体测试套件"""
    
    @pytest.fixture
    def mock_chat_model(self):
        """创建模拟的聊天模型"""
        mock_model = AsyncMock()
        mock_response = Mock()
        mock_response.content = '''
        {
            "overall_sentiment": "positive",
            "emotional_arc": ["neutral", "hopeful", "joyful"],
            "key_emotional_moments": [
                {"scene": "Scene 1", "emotion": "hope"}
            ],
            "confidence_score": 0.85
        }
        '''
        mock_model.ainvoke.return_value = mock_response
        return mock_model
    
    @pytest.mark.asyncio
    async def test_analyze_sentiment_success(self, mock_chat_model):
        """测试情感分析成功场景"""
        # 创建智能体
        analyzer = SentimentAnalyzer(chat_model=mock_chat_model)
        
        # 测试剧本
        script = "一个温馨的故事..."
        
        # 执行分析
        result = await analyzer.analyze_sentiment(script)
        
        # 验证结果
        assert result.overall_sentiment == "positive"
        assert len(result.emotional_arc) == 3
        assert result.confidence_score == 0.85
        assert mock_chat_model.ainvoke.called
    
    @pytest.mark.asyncio
    async def test_analyze_sentiment_with_retry(self, mock_chat_model):
        """测试重试机制"""
        # 模拟第一次失败，第二次成功
        mock_chat_model.ainvoke.side_effect = [
            Exception("API Error"),
            Mock(content='{"overall_sentiment": "positive", ...}')
        ]
        
        analyzer = SentimentAnalyzer(chat_model=mock_chat_model)
        
        # 应该在重试后成功
        result = await analyzer.analyze_sentiment("test script")
        
        # 验证调用了两次
        assert mock_chat_model.ainvoke.call_count == 2
    
    @pytest.mark.asyncio
    async def test_analyze_empty_script(self, mock_chat_model):
        """测试空剧本处理"""
        analyzer = SentimentAnalyzer(chat_model=mock_chat_model)
        
        # 测试空字符串
        with pytest.raises(ValueError):
            await analyzer.analyze_sentiment("")

# 运行测试
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### 示例 5：创建性能监控工具

```python
# performance_monitor.py
import asyncio
import time
import functools
from typing import Dict, List
import json

class PerformanceMonitor:
    """性能监控工具"""
    
    def __init__(self):
        """初始化监控器"""
        self.metrics: Dict[str, List[float]] = {}
    
    def measure(self, name: str):
        """装饰器：测量函数执行时间
        
        Args:
            name: 指标名称
        """
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.time()
                    duration = end_time - start_time
                    
                    if name not in self.metrics:
                        self.metrics[name] = []
                    self.metrics[name].append(duration)
                    
                    print(f"⏱️  {name}: {duration:.2f}秒")
            
            return wrapper
        return decorator
    
    def get_summary(self) -> dict:
        """获取性能摘要
        
        Returns:
            dict: 性能统计信息
        """
        summary = {}
        for name, durations in self.metrics.items():
            summary[name] = {
                "count": len(durations),
                "total": sum(durations),
                "average": sum(durations) / len(durations),
                "min": min(durations),
                "max": max(durations)
            }
        return summary
    
    def save_report(self, path: str = "performance_report.json"):
        """保存性能报告
        
        Args:
            path: 报告文件路径
        """
        summary = self.get_summary()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"📊 性能报告已保存: {path}")

# 使用示例
monitor = PerformanceMonitor()

@monitor.measure("story_generation")
async def generate_story_with_monitoring(screenwriter, idea, requirement):
    """带监控的故事生成"""
    return await screenwriter.develop_story(idea, requirement)

@monitor.measure("character_extraction")
async def extract_characters_with_monitoring(extractor, script):
    """带监控的角色提取"""
    return await extractor.extract_characters(script)

async def main():
    """运行监控示例"""
    from langchain.chat_models import init_chat_model
    from agents import Screenwriter, CharacterExtractor
    
    # 初始化
    chat_model = init_chat_model(
        model="gpt-4",
        model_provider="openai",
        api_key="your-key"
    )
    
    screenwriter = Screenwriter(chat_model=chat_model)
    extractor = CharacterExtractor(chat_model=chat_model)
    
    # 执行任务（带监控）
    story = await generate_story_with_monitoring(
        screenwriter,
        "一个关于友谊的故事",
        "温馨治愈"
    )
    
    characters = await extract_characters_with_monitoring(
        extractor,
        story
    )
    
    # 显示性能摘要
    print("\n" + "=" * 60)
    print("性能摘要:")
    print("=" * 60)
    for name, stats in monitor.get_summary().items():
        print(f"\n{name}:")
        print(f"  平均耗时: {stats['average']:.2f}秒")
        print(f"  最小耗时: {stats['min']:.2f}秒")
        print(f"  最大耗时: {stats['max']:.2f}秒")
    
    # 保存报告
    monitor.save_report()

if __name__ == "__main__":
    asyncio.run(main())
```

### 运行开发示例的注意事项

1. **环境准备**: 确保已安装所有依赖并配置好 API Keys
2. **代码测试**: 在生产环境使用前，先在测试环境验证
3. **错误处理**: 添加适当的错误处理和日志记录
4. **性能优化**: 根据实际需求优化代码性能
5. **文档维护**: 为自定义代码编写清晰的文档

### 调试开发中的问题

如果在开发过程中遇到问题：

1. **使用日志**: 添加详细的日志输出
2. **单元测试**: 为每个组件编写测试
3. **断点调试**: 使用 IDE 的调试功能
4. **性能分析**: 使用性能监控工具定位瓶颈
5. **代码审查**: 请其他开发者审查您的代码

---

**祝您开发愉快！如有任何问题或建议，欢迎随时联系我们。** 🚀
