# 示例与最佳实践

> 本文档提供 ViMax 的完整使用示例和最佳实践指南

## 目录

- [前置知识](#前置知识)
- [Idea2Video 完整示例](#idea2video-完整示例)
- [Script2Video 完整示例](#script2video-完整示例)
- [自定义智能体示例](#自定义智能体示例)
- [自定义工具示例](#自定义工具示例)
- [常见场景最佳实践](#常见场景最佳实践)
- [性能优化技巧](#性能优化技巧)
- [相关资源](#相关资源)

## 前置知识

在学习示例之前，建议您先完成：

- [快速开始](./getting_started.md) - 基本安装和配置
- [系统架构](./architecture.md) - 理解系统设计
- [配置详解](./configuration.md) - 了解配置选项

**示例代码说明**：

- 所有示例都是完整可运行的代码
- 需要先配置好 API Key
- 示例使用 Python 3.12+ 和 asyncio

---

## Idea2Video 完整示例

### 示例 1: 儿童故事视频

创建一个适合儿童观看的友谊主题短视频。

#### 完整代码

```python
import asyncio
from pipelines import Idea2VideoPipeline

async def create_children_story():
    """创建儿童友谊故事视频"""
    
    # 1. 初始化流水线
    pipeline = Idea2VideoPipeline.init_from_config(
        config_path="configs/idea2video.yaml"
    )
    
    # 2. 定义创意
    idea = """
    一只橙色的小猫咪叫 Whiskers，和一只棕色的小狗狗叫 Buddy 是最好的朋友。
    他们每天都在公园里一起玩耍。有一天，一只灰色的新猫咪 Shadow 来到了公园。
    Whiskers 和 Buddy 会如何对待这位新朋友呢？
    """
    
    # 3. 定义用户需求
    user_requirement = """
    - 目标观众：3-8 岁儿童
    - 主题：友谊、包容、善良
    - 场景数量：不超过 3 个场景
    - 每个场景：不超过 5 个镜头
    - 情感基调：温暖、积极、欢快
    - 避免：任何暴力或恐怖元素
    """
    
    # 4. 定义视觉风格
    style = "Cartoon"  # 卡通风格，适合儿童
    
    # 5. 生成视频
    print("🎬 开始生成视频...")
    video_path = await pipeline(
        idea=idea,
        user_requirement=user_requirement,
        style=style
    )
    
    print(f"✅ 视频生成完成！")
    print(f"📁 视频路径：{video_path}")
    
    return video_path

# 运行示例
if __name__ == "__main__":
    asyncio.run(create_children_story())
```

#### 预期输出

```
🎬 开始生成视频...
🧠 Developing story...
✅ Developed story and saved to .working_dir/idea2video/story.txt.
🚀 Loaded 3 characters from existing file.
☑️ Completed character portrait generation for Whiskers.
☑️ Completed character portrait generation for Buddy.
☑️ Completed character portrait generation for Shadow.
✅ Completed character portrait generation for 3 characters.
🧠 Writing script based on story...
✅ Written script based on story and saved to .working_dir/idea2video/script.json.
[场景 1/3] 开始生成...
[场景 2/3] 开始生成...
[场景 3/3] 开始生成...
🎬 Starting concatenating videos...
☑️ Concatenated videos, saved to .working_dir/idea2video/final_video.mp4.
✅ 视频生成完成！
📁 视频路径：.working_dir/idea2video/final_video.mp4
```

#### 生成的文件结构

```
.working_dir/idea2video/
├── story.txt                           # 扩展后的完整故事
├── characters.json                     # 提取的角色信息
├── character_portraits/                # 角色画像
│   ├── 0_Whiskers/
│   │   ├── front.png
│   │   ├── side.png
│   │   └── back.png
│   ├── 1_Buddy/
│   └── 2_Shadow/
├── character_portraits_registry.json   # 画像注册表
├── script.json                         # 场景剧本列表
├── scene_0/                            # 场景 0
│   ├── storyboard.json
│   ├── shots.json
│   ├── frames/
│   ├── videos/
│   └── final_video.mp4
├── scene_1/                            # 场景 1
├── scene_2/                            # 场景 2
└── final_video.mp4                     # 最终视频
```

### 示例 2: 科幻短片

创建一个科幻风格的短片。

#### 完整代码

```python
import asyncio
from pipelines import Idea2VideoPipeline

async def create_scifi_short():
    """创建科幻短片"""
    
    pipeline = Idea2VideoPipeline.init_from_config(
        config_path="configs/idea2video.yaml"
    )
    
    idea = """
    2157年，地球最后一位宇航员 Alex 独自驾驶飞船前往遥远的星系。
    在漫长的旅途中，飞船的 AI 助手 ARIA 成为了他唯一的伙伴。
    当飞船遭遇未知的能量波动时，Alex 必须做出艰难的选择。
    """
    
    user_requirement = """
    - 目标观众：成人科幻爱好者
    - 主题：孤独、人工智能、选择
    - 场景数量：4-5 个场景
    - 节奏：缓慢而深沉
    - 视觉：太空、飞船内部、未知现象
    """
    
    style = "Cyberpunk"  # 赛博朋克风格
    
    video_path = await pipeline(
        idea=idea,
        user_requirement=user_requirement,
        style=style
    )
    
    print(f"✅ 科幻短片生成完成：{video_path}")
    return video_path

if __name__ == "__main__":
    asyncio.run(create_scifi_short())
```

---

## Script2Video 完整示例

### 示例 1: 校园场景

将一个校园剧本转换为视频。

#### 完整代码

```python
import asyncio
from pipelines import Script2VideoPipeline

async def create_school_scene():
    """创建校园场景视频"""
    
    # 1. 初始化流水线
    pipeline = Script2VideoPipeline.init_from_config(
        config_path="configs/script2video.yaml"
    )
    
    # 2. 定义剧本
    script = """
EXT. 学校体育馆 - 白天

一群学生正在体育馆里练习篮球。体育馆宽敞明亮，一端是篮球架，另一端是大片的观众席。

JOHN（18岁，男，高大健壮）是球队的明星球员，正在练习运球和投篮。
JANE（17岁，女，身材娇小但充满活力）是助理教练，正在帮助 John 训练。
其他学生在一旁观看训练，为 John 加油。

JOHN
（运球）我要投进这个球！

JANE
（微笑）加油，John！

JOHN
（投篮）太棒了！

镜头切换到观众席，学生们欢呼雀跃。

JANE
（走向 John）你今天的状态很好！继续保持！

JOHN
（擦汗）谢谢你，Jane。有你的指导，我才能进步这么快。

两人击掌，其他学生围过来祝贺。

淡出。
    """
    
    # 3. 定义用户需求
    user_requirement = """
    - 节奏：快节奏，充满活力
    - 镜头数量：不超过 15 个镜头
    - 重点：展现团队合作和青春活力
    - 音效：篮球声、欢呼声、对话
    """
    
    # 4. 定义视觉风格
    style = "Anime Style"  # 动漫风格
    
    # 5. 生成视频
    print("🎬 开始生成校园场景视频...")
    video_path = await pipeline(
        script=script,
        user_requirement=user_requirement,
        style=style
    )
    
    print(f"✅ 视频生成完成！")
    print(f"📁 视频路径：{video_path}")
    
    return video_path

if __name__ == "__main__":
    asyncio.run(create_school_scene())
```

### 示例 2: 使用预定义角色

使用已有的角色画像生成视频。

#### 完整代码

```python
import asyncio
import json
from pipelines import Script2VideoPipeline
from interfaces import CharacterInScene

async def create_with_predefined_characters():
    """使用预定义角色生成视频"""
    
    pipeline = Script2VideoPipeline.init_from_config(
        config_path="configs/script2video.yaml"
    )
    
    # 定义角色
    characters = [
        CharacterInScene(
            idx=0,
            identifier_in_scene="Alice",
            is_visible=True,
            static_features="长金发，蓝眼睛，苗条身材，20多岁",
            dynamic_features="穿着红色连衣裙和白色运动鞋"
        ),
        CharacterInScene(
            idx=1,
            identifier_in_scene="Bob",
            is_visible=True,
            static_features="短棕发，绿眼睛，健壮体格，30多岁",
            dynamic_features="穿着蓝色衬衫和黑色牛仔裤"
        )
    ]
    
    # 加载已有的角色画像注册表（如果有）
    # 注意：这里的路径需要替换为实际的图像文件路径
    character_portraits_registry = {
        "Alice": {
            "front": {
                "path": "character_portraits/alice_front.png",  # 替换为实际路径
                "description": "Alice 的正面画像"
            },
            "side": {
                "path": "character_portraits/alice_side.png",  # 替换为实际路径
                "description": "Alice 的侧面画像"
            },
            "back": {
                "path": "character_portraits/alice_back.png",  # 替换为实际路径
                "description": "Alice 的背面画像"
            }
        },
        "Bob": {
            "front": {"path": "character_portraits/bob_front.png", "description": "Bob 的正面画像"},  # 替换为实际路径
            "side": {"path": "character_portraits/bob_side.png", "description": "Bob 的侧面画像"},  # 替换为实际路径
            "back": {"path": "character_portraits/bob_back.png", "description": "Bob 的背面画像"}  # 替换为实际路径
        }
    }
    
    script = """
EXT. 咖啡馆 - 下午

Alice 和 Bob 坐在咖啡馆的露天座位上，享受着温暖的阳光。

ALICE
（微笑）今天天气真好！

BOB
（点头）是啊，很适合出来走走。

两人愉快地交谈着。
    """
    
    video_path = await pipeline(
        script=script,
        user_requirement="轻松愉快的氛围，不超过10个镜头",
        style="Realistic",
        characters=characters,  # 传入预定义角色
        character_portraits_registry=character_portraits_registry  # 传入画像
    )
    
    print(f"✅ 视频生成完成：{video_path}")
    return video_path

if __name__ == "__main__":
    asyncio.run(create_with_predefined_characters())
```

---

## 自定义智能体示例

### 示例 1: 创建自定义编剧智能体

创建一个专门生成恐怖故事的编剧智能体。

#### 完整代码

```python
from agents import Screenwriter
from langchain.chat_models import init_chat_model

class HorrorScreenwriter(Screenwriter):
    """专门创作恐怖故事的编剧智能体"""
    
    def __init__(self, chat_model):
        super().__init__(chat_model)
        self.genre = "horror"
    
    async def develop_story(self, idea: str, user_requirement: str) -> str:
        """扩展创意为恐怖故事"""
        
        # 添加恐怖元素的提示
        horror_prompt = f"""
你是一位专业的恐怖故事编剧。请将以下创意扩展为一个引人入胜的恐怖故事。

创意：{idea}

用户需求：{user_requirement}

要求：
1. 营造紧张悬疑的氛围
2. 使用心理恐怖而非血腥暴力
3. 设置意想不到的转折
4. 保持故事的连贯性和逻辑性
5. 字数控制在 500-800 字

请开始创作：
        """
        
        response = await self.chat_model.ainvoke(horror_prompt)
        story = response.content
        
        return story

# 使用示例
async def main():
    chat_model = init_chat_model(
        model="google/gemini-2.5-flash-lite-preview-09-2025",
        model_provider="openai",
        api_key="YOUR_API_KEY",
        base_url="https://openrouter.ai/api/v1"
    )
    
    horror_writer = HorrorScreenwriter(chat_model=chat_model)
    
    story = await horror_writer.develop_story(
        idea="一个人搬进了一栋老房子",
        user_requirement="适合成人观众，心理恐怖"
    )
    
    print(story)

import asyncio
asyncio.run(main())
```

### 示例 2: 创建自定义角色提取器

创建一个提取更详细角色信息的智能体。

#### 完整代码

```python
from agents import CharacterExtractor
from interfaces import CharacterInScene
from typing import List
import json

class DetailedCharacterExtractor(CharacterExtractor):
    """提取详细角色信息的智能体"""
    
    async def extract_characters_with_relationships(
        self,
        text: str
    ) -> dict:
        """提取角色及其关系"""
        
        # 首先提取基本角色信息
        characters = await self.extract_characters(text)
        
        # 然后提取角色关系
        relationship_prompt = f"""
基于以下文本和角色列表，分析角色之间的关系。

文本：{text}

角色列表：
{json.dumps([char.model_dump() for char in characters], ensure_ascii=False, indent=2)}

请以 JSON 格式返回角色关系，格式如下：
{{
    "relationships": [
        {{
            "character1": "角色1名称",
            "character2": "角色2名称",
            "relationship": "关系描述"
        }}
    ]
}}
        """
        
        response = await self.chat_model.ainvoke(relationship_prompt)
        relationships = json.loads(response.content)
        
        return {
            "characters": characters,
            "relationships": relationships["relationships"]
        }

# 使用示例
async def main():
    from langchain.chat_models import init_chat_model
    
    chat_model = init_chat_model(
        model="google/gemini-2.5-flash-lite-preview-09-2025",
        model_provider="openai",
        api_key="YOUR_API_KEY",
        base_url="https://openrouter.ai/api/v1"
    )
    
    extractor = DetailedCharacterExtractor(chat_model=chat_model)
    
    text = """
    Alice 和 Bob 是多年的好友。Alice 是一位医生，而 Bob 是一位教师。
    他们经常一起喝咖啡，讨论生活和工作。
    """
    
    result = await extractor.extract_characters_with_relationships(text)
    
    print("角色：")
    for char in result["characters"]:
        print(f"  - {char.identifier_in_scene}: {char.static_features}")
    
    print("\n关系：")
    for rel in result["relationships"]:
        print(f"  - {rel['character1']} 和 {rel['character2']}: {rel['relationship']}")

import asyncio
asyncio.run(main())
```

---

## 自定义工具示例

### 示例 1: 创建自定义图像生成器

创建一个使用本地 Stable Diffusion 的图像生成器。

#### 完整代码

```python
from interfaces import ImageOutput
from typing import List, Optional
import requests
from PIL import Image
import io

class LocalStableDiffusionGenerator:
    """使用本地 Stable Diffusion API 的图像生成器"""
    
    def __init__(self, api_url: str = "http://localhost:7860"):
        """
        初始化本地 Stable Diffusion 生成器
        
        Args:
            api_url: Stable Diffusion WebUI 的 API 地址
        """
        self.api_url = api_url
    
    async def generate_single_image(
        self,
        prompt: str,
        reference_image_paths: Optional[List[str]] = None,
        size: str = "1600x900",
    ) -> ImageOutput:
        """
        生成单张图像
        
        Args:
            prompt: 图像生成提示词
            reference_image_paths: 参考图像路径列表（用于 ControlNet）
            size: 图像尺寸
        
        Returns:
            ImageOutput: 图像输出对象
        """
        width, height = map(int, size.split('x'))
        
        # 构建请求参数
        payload = {
            "prompt": prompt,
            "negative_prompt": "low quality, blurry, distorted",
            "width": width,
            "height": height,
            "steps": 30,
            "cfg_scale": 7.5,
            "sampler_name": "DPM++ 2M Karras",
        }
        
        # 如果有参考图像，使用 img2img
        if reference_image_paths:
            # 读取参考图像
            with open(reference_image_paths[0], 'rb') as f:
                import base64
                img_data = base64.b64encode(f.read()).decode()
            
            payload["init_images"] = [img_data]
            payload["denoising_strength"] = 0.7
            endpoint = f"{self.api_url}/sdapi/v1/img2img"
        else:
            endpoint = f"{self.api_url}/sdapi/v1/txt2img"
        
        # 发送请求
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        
        # 解析响应
        result = response.json()
        image_data = result['images'][0]
        
        # 解码图像
        import base64
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # 创建 ImageOutput 对象
        image_output = ImageOutput(image=image)
        
        return image_output

# 使用示例
async def main():
    generator = LocalStableDiffusionGenerator(api_url="http://localhost:7860")
    
    image = await generator.generate_single_image(
        prompt="A cute cartoon cat playing in a park, vibrant colors",
        size="1600x900"
    )
    
    image.save("output.png")
    print("✅ 图像生成完成：output.png")

import asyncio
asyncio.run(main())
```

**注意**：使用此自定义工具需要：
1. 安装并运行 Stable Diffusion WebUI
2. 启用 API 模式（`--api` 参数）
3. 确保端口可访问

### 示例 2: 创建自定义视频生成器包装器

创建一个带有重试和缓存机制的视频生成器。

#### 完整代码

```python
from tools import VideoGeneratorVeoGoogleAPI
from interfaces import VideoOutput
from typing import List
import hashlib
import os
import json
import asyncio

class CachedVideoGenerator:
    """带缓存机制的视频生成器"""
    
    def __init__(self, base_generator: VideoGeneratorVeoGoogleAPI, cache_dir: str = ".cache/videos"):
        """
        初始化缓存视频生成器
        
        Args:
            base_generator: 基础视频生成器
            cache_dir: 缓存目录
        """
        self.base_generator = base_generator
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_key(self, prompt: str, reference_image_paths: List[str]) -> str:
        """生成缓存键"""
        content = f"{prompt}|{','.join(reference_image_paths)}"
        return hashlib.md5(content.encode()).hexdigest()
    
    async def generate_single_video(
        self,
        prompt: str,
        reference_image_paths: List[str],
        max_retries: int = 3,
    ) -> VideoOutput:
        """
        生成单个视频（带缓存和重试）
        
        Args:
            prompt: 视频生成提示词
            reference_image_paths: 参考图像路径列表
            max_retries: 最大重试次数
        
        Returns:
            VideoOutput: 视频输出对象
        """
        # 检查缓存
        cache_key = self._get_cache_key(prompt, reference_image_paths)
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.mp4")
        cache_meta_path = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_path):
            print(f"🚀 从缓存加载视频：{cache_key}")
            with open(cache_meta_path, 'r') as f:
                meta = json.load(f)
            
            video_output = VideoOutput(path=cache_path)
            return video_output
        
        # 生成视频（带重试）
        for attempt in range(max_retries):
            try:
                print(f"🎬 生成视频（尝试 {attempt + 1}/{max_retries}）...")
                video_output = await self.base_generator.generate_single_video(
                    prompt=prompt,
                    reference_image_paths=reference_image_paths
                )
                
                # 保存到缓存
                video_output.save(cache_path)
                
                # 保存元数据
                meta = {
                    "prompt": prompt,
                    "reference_images": reference_image_paths,
                    "cache_key": cache_key
                }
                with open(cache_meta_path, 'w') as f:
                    json.dump(meta, f, ensure_ascii=False, indent=2)
                
                print(f"✅ 视频生成成功并已缓存")
                return video_output
                
            except Exception as e:
                print(f"❌ 生成失败（尝试 {attempt + 1}/{max_retries}）：{e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # 指数退避
                    print(f"⏳ 等待 {wait_time} 秒后重试...")
                    await asyncio.sleep(wait_time)
                else:
                    raise

# 使用示例
async def main():
    from tools import VideoGeneratorVeoGoogleAPI
    
    base_generator = VideoGeneratorVeoGoogleAPI(api_key="YOUR_API_KEY")
    cached_generator = CachedVideoGenerator(
        base_generator=base_generator,
        cache_dir=".cache/videos"
    )
    
    video = await cached_generator.generate_single_video(
        prompt="The cat runs towards the camera, wagging its tail happily",
        reference_image_paths=["keyframe.png"],
        max_retries=3
    )
    
    print(f"✅ 视频路径：{video.path}")

import asyncio
asyncio.run(main())
```

---

## 常见场景最佳实践

### 场景 1: 批量生成短视频

为社交媒体批量生成短视频内容。

#### 最佳实践

```python
import asyncio
from pipelines import Idea2VideoPipeline
from typing import List

async def batch_generate_videos(ideas: List[dict]):
    """批量生成视频"""
    
    pipeline = Idea2VideoPipeline.init_from_config(
        config_path="configs/idea2video.yaml"
    )
    
    results = []
    
    for i, idea_config in enumerate(ideas):
        print(f"\n{'='*50}")
        print(f"生成视频 {i+1}/{len(ideas)}")
        print(f"{'='*50}\n")
        
        try:
            video_path = await pipeline(
                idea=idea_config["idea"],
                user_requirement=idea_config["requirement"],
                style=idea_config["style"]
            )
            
            results.append({
                "success": True,
                "video_path": video_path,
                "idea": idea_config["idea"]
            })
            
        except Exception as e:
            print(f"❌ 生成失败：{e}")
            results.append({
                "success": False,
                "error": str(e),
                "idea": idea_config["idea"]
            })
    
    # 生成报告
    print(f"\n{'='*50}")
    print("批量生成完成")
    print(f"{'='*50}\n")
    
    success_count = sum(1 for r in results if r["success"])
    print(f"✅ 成功：{success_count}/{len(ideas)}")
    print(f"❌ 失败：{len(ideas) - success_count}/{len(ideas)}")
    
    return results

# 使用示例
async def main():
    ideas = [
        {
            "idea": "一只猫学习弹钢琴",
            "requirement": "适合儿童，不超过2个场景",
            "style": "Cartoon"
        },
        {
            "idea": "一个机器人学习人类情感",
            "requirement": "科幻风格，3-4个场景",
            "style": "Cyberpunk"
        },
        {
            "idea": "一朵花的一生",
            "requirement": "纪录片风格，展现生命周期",
            "style": "Realistic"
        }
    ]
    
    results = await batch_generate_videos(ideas)
    
    # 保存结果
    import json
    with open("batch_results.json", "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

asyncio.run(main())
```

**关键点**：
- 使用异常处理确保单个失败不影响整体
- 生成详细的执行报告
- 保存结果以便后续分析

### 场景 2: 长视频分段生成

生成超过 5 分钟的长视频。

#### 最佳实践

```python
import asyncio
from pipelines import Script2VideoPipeline
from moviepy import VideoFileClip, concatenate_videoclips
import os

async def generate_long_video(full_script: str, segment_length: int = 10):
    """
    分段生成长视频
    
    Args:
        full_script: 完整剧本
        segment_length: 每段的最大镜头数
    """
    
    pipeline = Script2VideoPipeline.init_from_config(
        config_path="configs/script2video.yaml"
    )
    
    # 1. 将剧本分段
    segments = split_script_into_segments(full_script, segment_length)
    
    print(f"📝 剧本已分为 {len(segments)} 段")
    
    # 2. 逐段生成视频
    segment_videos = []
    
    for i, segment in enumerate(segments):
        print(f"\n🎬 生成第 {i+1}/{len(segments)} 段...")
        
        segment_dir = f".working_dir/long_video/segment_{i}"
        os.makedirs(segment_dir, exist_ok=True)
        
        # 为每段创建独立的流水线实例
        segment_pipeline = Script2VideoPipeline(
            chat_model=pipeline.chat_model,
            image_generator=pipeline.image_generator,
            video_generator=pipeline.video_generator,
            working_dir=segment_dir
        )
        
        video_path = await segment_pipeline(
            script=segment,
            user_requirement=f"这是第 {i+1} 段，不超过 {segment_length} 个镜头",
            style="Realistic"
        )
        
        segment_videos.append(video_path)
        print(f"✅ 第 {i+1} 段完成：{video_path}")
    
    # 3. 合并所有段
    print(f"\n🎬 合并 {len(segment_videos)} 个视频段...")
    
    clips = [VideoFileClip(path) for path in segment_videos]
    final_video = concatenate_videoclips(clips)
    
    final_path = ".working_dir/long_video/final_video.mp4"
    final_video.write_videofile(final_path)
    
    print(f"✅ 长视频生成完成：{final_path}")
    print(f"📊 总时长：{final_video.duration:.2f} 秒")
    
    return final_path

def split_script_into_segments(script: str, max_shots: int) -> List[str]:
    """将剧本分段"""
    # 简单的分段逻辑：按场景分割
    scenes = script.split("\n\n")
    
    segments = []
    current_segment = []
    current_shot_count = 0
    
    for scene in scenes:
        # 估算场景的镜头数（简化版）
        estimated_shots = len(scene.split("\n")) // 3
        
        if current_shot_count + estimated_shots > max_shots and current_segment:
            # 当前段已满，开始新段
            segments.append("\n\n".join(current_segment))
            current_segment = [scene]
            current_shot_count = estimated_shots
        else:
            current_segment.append(scene)
            current_shot_count += estimated_shots
    
    # 添加最后一段
    if current_segment:
        segments.append("\n\n".join(current_segment))
    
    return segments

# 使用示例
async def main():
    full_script = """
EXT. 公园 - 白天
[长剧本内容...]

EXT. 咖啡馆 - 下午
[更多场景...]

INT. 办公室 - 晚上
[更多场景...]
    """
    
    video_path = await generate_long_video(
        full_script=full_script,
        segment_length=10
    )

asyncio.run(main())
```

**关键点**：
- 将长剧本分段处理
- 为每段使用独立的工作目录
- 最后合并所有段
- 监控内存使用，避免同时加载过多视频

### 场景 3: 多语言视频生成

生成多语言版本的视频。

#### 最佳实践

```python
import asyncio
from pipelines import Script2VideoPipeline
from typing import Dict

async def generate_multilingual_videos(
    script_template: str,
    translations: Dict[str, str]
):
    """
    生成多语言视频
    
    Args:
        script_template: 剧本模板
        translations: 语言翻译字典 {"en": "English script", "zh": "中文剧本"}
    """
    
    results = {}
    
    for lang_code, translated_script in translations.items():
        print(f"\n🌍 生成 {lang_code} 版本...")
        
        pipeline = Script2VideoPipeline.init_from_config(
            config_path="configs/script2video.yaml"
        )
        
        # 为每种语言使用独立的工作目录
        pipeline.working_dir = f".working_dir/multilingual/{lang_code}"
        
        video_path = await pipeline(
            script=translated_script,
            user_requirement=f"语言：{lang_code}",
            style="Realistic"
        )
        
        results[lang_code] = video_path
        print(f"✅ {lang_code} 版本完成：{video_path}")
    
    return results

# 使用示例
async def main():
    translations = {
        "en": """
EXT. PARK - DAY
A cat and a dog are playing in the park.
        """,
        "zh": """
EXT. 公园 - 白天
一只猫和一只狗在公园里玩耍。
        """,
        "ja": """
EXT. 公園 - 昼
猫と犬が公園で遊んでいます。
        """
    }
    
    videos = await generate_multilingual_videos(
        script_template="park_scene",
        translations=translations
    )
    
    print("\n✅ 所有语言版本生成完成：")
    for lang, path in videos.items():
        print(f"  {lang}: {path}")

asyncio.run(main())
```

---

## 性能优化技巧

### 技巧 1: 使用缓存避免重复生成

```python
import os
import hashlib
import json

def get_cache_path(content: str, cache_dir: str = ".cache") -> str:
    """根据内容生成缓存路径"""
    content_hash = hashlib.md5(content.encode()).hexdigest()
    return os.path.join(cache_dir, f"{content_hash}.json")

async def cached_operation(content: str, operation_func, cache_dir: str = ".cache"):
    """带缓存的操作"""
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = get_cache_path(content, cache_dir)
    
    # 检查缓存
    if os.path.exists(cache_path):
        print("🚀 从缓存加载")
        with open(cache_path, 'r') as f:
            return json.load(f)
    
    # 执行操作
    result = await operation_func(content)
    
    # 保存到缓存
    with open(cache_path, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result
```

**提示**: ViMax 已内置缓存机制，会自动保存中间结果到 `.working_dir/` 目录。

### 技巧 2: 并行处理独立任务

```python
import asyncio

async def parallel_generate_portraits(characters, generator, style):
    """并行生成角色画像"""
    
    tasks = [
        generator.generate_front_portrait(char, style)
        for char in characters
    ]
    
    # 并行执行所有任务
    portraits = await asyncio.gather(*tasks)
    
    return portraits
```

**提示**: ViMax 的工具函数（如 `download_image`, `download_video`）已使用 `tenacity` 库的 `@retry` 装饰器实现自动重试。

### 技巧 3: 监控和限制资源使用

```python
import psutil
import asyncio

async def generate_with_resource_monitoring(pipeline, **kwargs):
    """带资源监控的生成"""
    
    # 记录初始资源使用
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    print(f"📊 初始内存使用：{initial_memory:.2f} MB")
    
    # 执行生成
    result = await pipeline(**kwargs)
    
    # 记录最终资源使用
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory
    
    print(f"📊 最终内存使用：{final_memory:.2f} MB")
    print(f"📊 内存增长：{memory_increase:.2f} MB")
    
    return result
```

### 技巧 4: 增量生成和断点续传

```python
import os
import json

async def incremental_generate(pipeline, script, checkpoint_file=".checkpoint.json"):
    """支持断点续传的生成"""
    
    # 加载检查点
    checkpoint = {}
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoint = json.load(f)
        print(f"🚀 从检查点恢复：{checkpoint}")
    
    # 检查是否已完成角色提取
    if "characters" not in checkpoint:
        print("📝 提取角色...")
        characters = await pipeline.extract_characters(script)
        checkpoint["characters"] = [c.model_dump() for c in characters]
        save_checkpoint(checkpoint, checkpoint_file)
    
    # 检查是否已完成画像生成
    if "portraits" not in checkpoint:
        print("🎨 生成角色画像...")
        portraits = await pipeline.generate_character_portraits(...)
        checkpoint["portraits"] = portraits
        save_checkpoint(checkpoint, checkpoint_file)
    
    # 继续其他步骤...
    
    return result

def save_checkpoint(checkpoint, file_path):
    """保存检查点"""
    with open(file_path, 'w') as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=2)
    print(f"💾 检查点已保存")
```

---

## 相关资源

### 深入学习

- **[快速开始](./getting_started.md)** - 基础使用教程
- **[API 参考](./api_reference.md)** - 详细的 API 文档
- **[配置详解](./configuration.md)** - 配置选项说明
- **[开发指南](./development.md)** - 扩展和定制指南

### 示例代码仓库

- **GitHub Examples**: 查看更多示例代码
- **Community Showcase**: 社区用户分享的作品

### 社区支持

- **GitHub Issues**: [提交问题和建议](https://github.com/HKUDS/ViMax/issues)
- **交流群**: 查看 [Communication.md](../Communication.md)

---

**提示**: 所有示例代码都可以直接运行，但请确保先配置好 API Key。如果遇到问题，请参考 [故障排查](./troubleshooting.md) 文档。
