# 快速开始

> 本指南将帮助您在 15 分钟内搭建 ViMax 环境并生成您的第一个 AI 视频。

## 目录

- [前置知识](#前置知识)
- [环境要求](#环境要求)
- [安装步骤](#安装步骤)
- [配置说明](#配置说明)
- [运行示例](#运行示例)
- [输出结果](#输出结果)
- [故障排查](#故障排查)
- [相关资源](#相关资源)

## 前置知识

在开始之前，建议您了解以下内容：

- 基本的 Python 编程知识
- 命令行操作基础
- 了解 YAML 配置文件格式（可选）

如果您想深入了解 ViMax 的工作原理，请参阅：
- [系统架构](./architecture.md) - 了解多智能体协作机制
- [核心流水线](./pipelines.md) - 了解视频生成流程

## 环境要求

### 操作系统

ViMax 支持以下操作系统：

- **Linux** (推荐)
  - Ubuntu 20.04 LTS 或更高版本
  - Debian 11 或更高版本
  - CentOS 8 或更高版本
  - 其他主流 Linux 发行版（需要 glibc 2.31+）

- **Windows**
  - Windows 10 (版本 1903 或更高)
  - Windows 11
  - **注意**: 推荐使用 WSL2 (Windows Subsystem for Linux 2) 以获得更好的兼容性
  - 原生 Windows 支持可能需要额外配置

- **macOS**
  - macOS 12 (Monterey) 或更高版本
  - 支持 Intel 和 Apple Silicon (M1/M2/M3) 芯片
  - **注意**: 某些依赖（如 OpenCV）可能需要通过 Homebrew 安装额外的系统库

### 软件依赖

#### Python 环境

- **Python 版本**: 3.12 或更高版本（**必需**）
  
  检查当前 Python 版本：
  ```bash
  python --version
  # 或
  python3 --version
  ```
  
  如果版本低于 3.12，请访问 [Python 官网](https://www.python.org/downloads/) 下载并安装最新版本。

#### 包管理器

- **uv** (强烈推荐)
  
  uv 是一个现代化的 Python 包管理器，具有以下优势：
  - 比传统的 pip 快 10-100 倍
  - 提供更可靠的依赖解析
  - 内置虚拟环境管理
  - 更好的依赖锁定机制
  
  安装 uv：
  ```bash
  # macOS/Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh
  
  # Windows (PowerShell)
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  
  # 或使用 pip 安装
  pip install uv
  ```
  
  详细安装说明请参考：https://docs.astral.sh/uv/getting-started/installation/

### 硬件要求

- **内存**: 
  - 最低 8GB RAM
  - 推荐 16GB 或更高（用于处理长视频或复杂场景）

- **存储**: 
  - 至少 10GB 可用磁盘空间
  - 用于存储依赖包、模型缓存和生成的视频文件
  - 建议使用 SSD 以提升性能

- **网络**: 
  - 稳定的互联网连接（必需）
  - 用于调用 API 服务（Google Gemini、Veo 等）
  - 建议带宽：至少 10 Mbps（上传和下载）

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

## 配置说明

ViMax 使用 YAML 文件进行配置。在运行之前，您需要配置 API 密钥和相关参数。

### 配置文件结构

ViMax 提供了两个主要的配置文件：

- `configs/idea2video.yaml` - 用于创意生成视频流水线
- `configs/script2video.yaml` - 用于剧本生成视频流水线

### 配置字段详解

#### 1. chat_model（对话模型配置）

用于驱动智能体进行剧本创作、分镜设计等任务的大语言模型。

```yaml
chat_model:
  init_args:
    model: google/gemini-2.5-flash-lite-preview-09-2025  # 模型名称
    model_provider: openai                                # 模型提供商接口类型
    api_key: YOUR_API_KEY_HERE                           # API 密钥
    base_url: https://openrouter.ai/api/v1               # API 端点地址
```

**字段说明**：

- `model`: 指定使用的模型名称
  - 示例：`google/gemini-2.5-flash-lite-preview-09-2025`
  - 支持任何兼容 OpenAI API 格式的模型
  
- `model_provider`: 模型提供商类型
  - 当前支持：`openai`（使用 OpenAI 兼容接口）
  
- `api_key`: **必填**，您的 API 密钥
  - 获取方式见下文"API Key 获取指南"
  
- `base_url`: API 服务的基础 URL
  - OpenRouter: `https://openrouter.ai/api/v1`
  - 云雾 API: `https://api.yunwu.ai/v1`
  - 直接使用 OpenAI: `https://api.openai.com/v1`

#### 2. image_generator（图像生成器配置）

用于生成分镜关键帧、角色画像等静态图像。

```yaml
image_generator:
  class_path: tools.ImageGeneratorNanobananaGoogleAPI  # 图像生成工具类
  init_args:
    api_key: YOUR_API_KEY_HERE                         # API 密钥
```

**字段说明**：

- `class_path`: 图像生成工具的类路径
  - `tools.ImageGeneratorNanobananaGoogleAPI` - Google 图像生成（推荐）
  - `tools.ImageGeneratorNanobananaYunwuAPI` - 通过云雾 API 访问
  - `tools.ImageGeneratorDoubaoSeedreamYunwuAPI` - 字节豆包图像生成
  
- `api_key`: **必填**，对应服务的 API 密钥

#### 3. video_generator（视频生成器配置）

用于将静态图像转换为动态视频片段。

```yaml
video_generator:
  class_path: tools.VideoGeneratorVeoGoogleAPI  # 视频生成工具类
  init_args:
    api_key: YOUR_API_KEY_HERE                  # API 密钥
```

**字段说明**：

- `class_path`: 视频生成工具的类路径
  - `tools.VideoGeneratorVeoGoogleAPI` - Google Veo（推荐，质量最高）
  - `tools.VideoGeneratorVeoYunwuAPI` - 通过云雾 API 访问 Veo
  - `tools.VideoGeneratorDoubaoSeedanceYunwuAPI` - 字节豆包视频生成
  
- `api_key`: **必填**，对应服务的 API 密钥

#### 4. working_dir（工作目录）

指定生成文件的输出目录。

```yaml
working_dir: .working_dir/idea2video  # 输出目录路径
```

所有生成的中间文件（剧本、分镜描述、图像、视频等）都会保存在此目录下。

### API Key 获取指南

#### Google API Key（用于 Gemini 和 Veo）

1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 登录您的 Google 账号
3. 点击"Create API Key"创建新密钥
4. 复制生成的 API Key
5. 将其填入配置文件的 `api_key` 字段

**注意事项**：
- Google Gemini 和 Veo 可能需要不同的 API Key
- 某些地区可能无法直接访问 Google AI 服务
- 请妥善保管您的 API Key，不要泄露或提交到公开仓库

#### OpenRouter API Key

1. 访问 [OpenRouter](https://openrouter.ai/)
2. 注册并登录账号
3. 进入 [Keys 页面](https://openrouter.ai/keys)
4. 创建新的 API Key
5. 充值账户余额（按使用量计费）

**优势**：
- 可以通过统一接口访问多种模型（包括 Gemini）
- 对于国内用户访问更稳定
- 支持多种支付方式

#### 云雾 API Key

1. 访问 [云雾 AI](https://yunwu.ai/)
2. 注册并完成实名认证
3. 在控制台创建 API Key
4. 充值账户

**优势**：
- 国内访问速度快，稳定性好
- 支持支付宝、微信支付
- 提供多种国内外模型的统一接口

### 配置示例

#### 示例 1：使用 Google 原生 API

```yaml
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

#### 示例 2：使用 OpenRouter（推荐国内用户）

```yaml
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

#### 示例 3：使用字节豆包模型

```yaml
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

### 配置验证

配置完成后，建议先运行一个简单的测试来验证配置是否正确。

#### 方法 1：快速测试脚本

创建一个测试脚本 `test_config.py` 来验证配置：

```python
import asyncio
from langchain.chat_models import init_chat_model
import yaml

async def test_configuration():
    """测试配置是否正确"""
    print("🔍 开始测试配置...")
    
    # 读取配置文件
    try:
        with open("configs/idea2video.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        print("✅ 配置文件读取成功")
    except Exception as e:
        print(f"❌ 配置文件读取失败: {e}")
        return False
    
    # 测试聊天模型
    try:
        chat_model_config = config["chat_model"]["init_args"]
        chat_model = init_chat_model(
            model=chat_model_config["model"],
            model_provider=chat_model_config["model_provider"],
            api_key=chat_model_config["api_key"],
            base_url=chat_model_config["base_url"]
        )
        
        # 发送测试消息
        response = await chat_model.ainvoke("Say 'Hello, ViMax!'")
        print(f"✅ 聊天模型测试成功: {response.content[:50]}...")
    except Exception as e:
        print(f"❌ 聊天模型测试失败: {e}")
        return False
    
    print("\n🎉 所有配置测试通过！您可以开始使用 ViMax 了。")
    return True

if __name__ == "__main__":
    asyncio.run(test_configuration())
```

运行测试：

```bash
python test_config.py
```

#### 方法 2：使用默认示例

直接运行默认的示例脚本：

```bash
# 使用默认的简短示例
python main_idea2video.py
```

如果配置正确，程序将开始生成视频。如果遇到错误，请参阅下文的"故障排查"部分。

#### 完整的环境配置示例

以下是一个完整的配置和运行示例，从头到尾展示整个流程：

```bash
# 1. 克隆仓库
git clone https://github.com/HKUDS/ViMax.git
cd ViMax

# 2. 安装 uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. 同步依赖
uv sync

# 4. 激活虚拟环境
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows

# 5. 复制并编辑配置文件
cp configs/idea2video.yaml configs/my_config.yaml
# 使用文本编辑器编辑 my_config.yaml，填入您的 API Keys

# 6. 创建测试脚本
cat > quick_test.py << 'EOF'
import asyncio
from pipelines.idea2video_pipeline import Idea2VideoPipeline

async def main():
    pipeline = Idea2VideoPipeline.init_from_config(
        config_path="configs/my_config.yaml"
    )
    
    await pipeline(
        idea="一只猫在追逐蝴蝶",
        user_requirement="10秒短视频，1个场景",
        style="Cartoon"
    )

if __name__ == "__main__":
    asyncio.run(main())
EOF

# 7. 运行测试
python quick_test.py

# 8. 查看生成的视频
ls -lh .working_dir/idea2video/final_video.mp4
```

## 运行示例

### 1. 创意生成视频 (Idea2Video)

Idea2Video 流水线可以将一个简单的创意扩展为完整的视频。

#### 方法 1：修改现有脚本（推荐新手）

打开 `main_idea2video.py` 文件，修改以下变量：

```python
# 您的创意描述
idea = """
一只猫和一只狗是最好的朋友，当它们遇到一只新来的猫时会发生什么？
"""

# 用户需求和约束
user_requirement = """
面向儿童观众，不超过3个场景。每个场景不超过5个镜头。
"""

# 视觉风格
style = "Cartoon"  # 可选：Cartoon, Anime, Realistic, Cyberpunk 等
```

**参数说明**：

- `idea`: 您的创意描述，可以是一句话或一段简短的故事梗概
- `user_requirement`: 对视频的具体要求，如目标观众、场景数量、时长限制等
- `style`: 视觉风格，影响图像和视频的生成效果

然后运行脚本：

```bash
# 确保在项目根目录下
python main_idea2video.py
```

#### 方法 2：创建自定义脚本（推荐有经验用户）

创建一个新的 Python 文件 `my_idea2video.py`：

```python
import asyncio
from pipelines.idea2video_pipeline import Idea2VideoPipeline

async def main():
    # 初始化流水线（使用配置文件）
    pipeline = Idea2VideoPipeline.init_from_config(
        config_path="configs/idea2video.yaml"
    )
    
    # 定义您的创意
    idea = """
    一个年轻的程序员发现他编写的 AI 助手开始有了自己的想法。
    """
    
    # 定义用户需求
    user_requirement = """
    科幻风格，适合成人观众。
    不超过 3 个场景，每个场景 5-8 个镜头。
    重点展现人与 AI 的情感互动。
    """
    
    # 定义视觉风格
    style = "Cyberpunk"
    
    # 运行流水线
    print("🎬 开始生成视频...")
    await pipeline(
        idea=idea,
        user_requirement=user_requirement,
        style=style
    )
    print("✅ 视频生成完成！")

if __name__ == "__main__":
    asyncio.run(main())
```

运行您的自定义脚本：

```bash
python my_idea2video.py
```

#### 方法 3：在 Jupyter Notebook 中使用

如果您喜欢交互式开发，可以在 Jupyter Notebook 中使用：

```python
# 在 Jupyter Notebook 单元格中运行
import asyncio
from pipelines.idea2video_pipeline import Idea2VideoPipeline

# 初始化流水线
pipeline = Idea2VideoPipeline.init_from_config(
    config_path="configs/idea2video.yaml"
)

# 定义参数
idea = "一只勇敢的小老鼠拯救了整个村庄"
user_requirement = "儿童动画风格，3个场景"
style = "Cartoon"

# 运行（在 Jupyter 中使用 await）
await pipeline(idea=idea, user_requirement=user_requirement, style=style)
```

#### 步骤 3：等待生成

程序将依次执行以下步骤：
1. 扩写创意为完整剧本
2. 提取场景和角色信息
3. 设计分镜脚本
4. 生成关键帧图像
5. 生成视频片段
6. 合成最终视频

整个过程大约需要 5-10 分钟，具体时间取决于场景复杂度和 API 响应速度。

### 2. 剧本生成视频 (Script2Video)

如果您已有完整的剧本，可以直接使用 Script2Video 流水线。

#### 方法 1：修改现有脚本

打开 `main_script2video.py` 文件，编辑剧本内容：

```python
# 您的剧本（支持标准剧本格式）
script = """
EXT. SCHOOL GYM - DAY
A group of students are practicing basketball in the gym. 
John (18, male, tall, athletic) is the star player, practicing his dribble and shot. 
Jane (17, female, short, athletic) is the assistant coach, helping John with his practice.

John: (dribbling the ball) I'm going to score a basket!
Jane: (smiling) Good job, John!
John: (shooting the ball) Yes!
"""

# 用户需求
user_requirement = """
Fast-paced with no more than 15 shots.
"""

# 视觉风格
style = "Anime Style"
```

**剧本格式说明**：

- 场景标题（Slugline）：`EXT./INT. 地点 - 时间`
- 动作描述（Action）：描述场景中发生的事情
- 角色对话（Dialogue）：`角色名: 对话内容`
- 角色介绍：在首次出现时用括号说明角色特征

然后运行脚本：

```bash
python main_script2video.py
```

#### 方法 2：创建自定义脚本

创建一个新的 Python 文件 `my_script2video.py`：

```python
import asyncio
from pipelines.script2video_pipeline import Script2VideoPipeline

async def main():
    # 初始化流水线
    pipeline = Script2VideoPipeline.init_from_config(
        config_path="configs/script2video.yaml"
    )
    
    # 您的剧本（中文示例）
    script = """
INT. 咖啡馆 - 下午

阳光透过落地窗洒进咖啡馆。小李（25岁，男，程序员装扮）坐在角落，
专注地看着笔记本电脑。小王（24岁，女，设计师）端着咖啡走过来。

小王：（微笑）还在加班？
小李：（抬头）嗨！刚好写完最后一个功能。
小王：（坐下）那太好了，我们可以聊聊新项目了。
小李：（合上电脑）当然，我已经迫不及待了。
    """
    
    # 用户需求
    user_requirement = """
    现代都市风格，节奏轻快。
    不超过 10 个镜头。
    重点展现角色之间的互动和咖啡馆的温馨氛围。
    """
    
    # 视觉风格
    style = "Realistic"
    
    # 运行流水线
    print("🎬 开始从剧本生成视频...")
    await pipeline(
        script=script,
        user_requirement=user_requirement,
        style=style
    )
    print("✅ 视频生成完成！")

if __name__ == "__main__":
    asyncio.run(main())
```

运行脚本：

```bash
python my_script2video.py
```

#### 方法 3：从文件读取剧本

如果您的剧本保存在文件中，可以这样读取：

```python
import asyncio
from pipelines.script2video_pipeline import Script2VideoPipeline

async def main():
    # 初始化流水线
    pipeline = Script2VideoPipeline.init_from_config(
        config_path="configs/script2video.yaml"
    )
    
    # 从文件读取剧本
    with open("my_script.txt", "r", encoding="utf-8") as f:
        script = f.read()
    
    # 定义参数
    user_requirement = "不超过 20 个镜头，节奏紧凑"
    style = "Cinematic"
    
    # 运行流水线
    await pipeline(
        script=script,
        user_requirement=user_requirement,
        style=style
    )

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. 监控运行进度

运行过程中，终端会输出详细的进度信息：

```
[INFO] Initializing Idea2Video Pipeline...
[INFO] Expanding idea into full script...
[INFO] Extracting scenes from script...
[INFO] Scene 1/3: Park scene
[INFO] Generating storyboard for scene 1...
[INFO] Generating images for 5 shots...
[INFO] Shot 1/5: Generating keyframe...
[INFO] Generating video for shot 1...
[INFO] Merging video clips...
[INFO] Final video saved to: .working_dir/idea2video/final_video.mp4
```

### 4. 自定义参数

您还可以通过修改配置文件来调整更多参数：

```yaml
# 在 configs/idea2video.yaml 中
working_dir: .working_dir/my_custom_project  # 自定义输出目录

# 可以添加更多自定义参数（需要代码支持）
max_scenes: 5          # 最大场景数
shots_per_scene: 8     # 每个场景的最大镜头数
video_duration: 5      # 每个镜头的视频时长（秒）
```

## 故障排查

在使用 ViMax 过程中，您可能会遇到一些常见问题。以下是诊断和解决方法。

### 1. API Key 相关问题

#### 问题：`Authentication failed` 或 `Invalid API key`

**原因**：
- API Key 未填写或填写错误
- API Key 已过期或被撤销
- API Key 权限不足

**解决方案**：

1. 检查配置文件中的 `api_key` 字段是否已填写：
   ```bash
   cat configs/idea2video.yaml | grep api_key
   ```

2. 确认 API Key 格式正确：
   - Google API Key: 通常以 `AIza` 开头
   - OpenRouter API Key: 通常以 `sk-or-v1-` 开头
   - 云雾 API Key: 通常以 `yw-` 开头

3. 验证 API Key 是否有效：
   ```bash
   # 测试 OpenRouter API Key
   curl https://openrouter.ai/api/v1/models \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```

4. 重新生成 API Key 并更新配置文件

#### 问题：`Quota exceeded` 或 `Rate limit exceeded`

**原因**：
- API 调用次数超过限额
- 账户余额不足

**解决方案**：

1. 检查账户余额和配额
2. 等待配额重置（通常按分钟或小时计算）
3. 升级 API 套餐或充值账户
4. 在配置中添加重试延迟（需要代码支持）

### 2. 网络连接问题

#### 问题：`Connection timeout` 或 `Network error`

**原因**：
- 网络不稳定
- 防火墙或代理设置阻止连接
- API 服务暂时不可用

**解决方案**：

1. 检查网络连接：
   ```bash
   ping google.com
   ```

2. 测试 API 端点可访问性：
   ```bash
   curl -I https://openrouter.ai/api/v1/models
   ```

3. 如果在国内使用，建议：
   - 使用云雾 API 或 OpenRouter 等国内可访问的服务
   - 配置代理（如果需要）：
     ```bash
     export HTTP_PROXY=http://your-proxy:port
     export HTTPS_PROXY=http://your-proxy:port
     python main_idea2video.py
     ```

4. 检查防火墙设置，确保允许 Python 访问网络

### 3. 依赖安装问题

#### 问题：`ModuleNotFoundError` 或 `ImportError`

**原因**：
- 依赖包未正确安装
- Python 环境不正确

**解决方案**：

1. 重新同步依赖：
   ```bash
   uv sync --reinstall
   ```

2. 检查 Python 版本：
   ```bash
   python --version  # 应该是 3.12 或更高
   ```

3. 确认在正确的虚拟环境中：
   ```bash
   which python  # 应该指向项目的虚拟环境
   ```

4. 手动安装缺失的包：
   ```bash
   uv pip install <package-name>
   ```

#### 问题：`uv: command not found`

**解决方案**：

1. 安装 uv：
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. 重新加载 shell 配置：
   ```bash
   source ~/.bashrc  # 或 ~/.zshrc
   ```

3. 或使用 pip 作为替代：
   ```bash
   pip install -r requirements.txt  # 如果有 requirements.txt
   ```

### 4. 运行时错误

#### 问题：`CUDA out of memory` 或内存不足

**原因**：
- 系统内存不足
- 处理的视频过于复杂

**解决方案**：

1. 减少场景数量和镜头数量
2. 关闭其他占用内存的程序
3. 增加系统交换空间（Linux）
4. 使用更小的模型或降低图像分辨率

#### 问题：生成的视频质量不佳

**原因**：
- 提示词不够详细
- 使用的模型不适合当前风格
- 参考图像质量问题

**解决方案**：

1. 优化创意描述，提供更多细节
2. 尝试不同的视觉风格（`style` 参数）
3. 切换到质量更高的模型（如 Veo）
4. 调整 `user_requirement` 中的约束条件

#### 问题：角色外观不一致

**原因**：
- 角色描述不够详细
- 图像生成的随机性

**解决方案**：

1. 在剧本中详细描述角色特征（发色、服装、体型等）
2. 使用 Novel2Video 流水线（具有更好的一致性保持机制）
3. 在配置中启用角色画像功能（如果支持）

### 5. 文件和权限问题

#### 问题：`Permission denied` 或无法写入文件

**解决方案**：

1. 检查输出目录权限：
   ```bash
   ls -ld .working_dir/
   ```

2. 修改目录权限：
   ```bash
   chmod -R 755 .working_dir/
   ```

3. 确保有足够的磁盘空间：
   ```bash
   df -h .
   ```

### 6. 获取更多帮助

如果以上方法无法解决您的问题：

1. **查看日志文件**：
   - 检查终端输出的详细错误信息
   - 查找 `.working_dir/` 中的日志文件（如果有）

2. **搜索已知问题**：
   - 访问 [GitHub Issues](https://github.com/HKUDS/ViMax/issues)
   - 搜索类似的问题和解决方案

3. **提交新问题**：
   - 在 GitHub 上创建新的 Issue
   - 提供详细的错误信息、配置文件和运行日志
   - 说明您的操作系统和 Python 版本

4. **加入社区**：
   - 查看 [Communication.md](../Communication.md) 了解交流群信息
   - 与其他用户和开发者交流经验

## 输出结果

### 输出目录结构

生成的视频和中间产物将保存在配置文件中 `working_dir` 指定的目录（默认为 `.working_dir/idea2video` 或 `.working_dir/script2video`）。

典型的输出目录结构如下：

```
.working_dir/idea2video/
├── script.txt                    # 生成的完整剧本
├── scenes/                       # 场景分解
│   ├── scene_001.json           # 场景 1 的详细信息
│   ├── scene_002.json           # 场景 2 的详细信息
│   └── ...
├── storyboard/                   # 分镜脚本
│   ├── shot_001.json            # 镜头 1 的分镜描述
│   ├── shot_002.json            # 镜头 2 的分镜描述
│   └── ...
├── images/                       # 生成的关键帧图像
│   ├── shot_001_frame.png       # 镜头 1 的关键帧
│   ├── shot_002_frame.png       # 镜头 2 的关键帧
│   └── ...
├── videos/                       # 生成的视频片段
│   ├── shot_001.mp4             # 镜头 1 的视频
│   ├── shot_002.mp4             # 镜头 2 的视频
│   └── ...
└── final_video.mp4               # 最终合成的完整视频
```

### 输出文件说明

#### 1. 剧本文件（script.txt）

包含完整的剧本内容，采用标准剧本格式：

```
EXT. 公园 - 白天

一只橙色的猫咪（WHISKERS）和一只棕色的狗狗（BUDDY）正在草地上玩耍。
它们追逐着一个红色的球，看起来非常开心。

WHISKERS
（兴奋地）接住它，Buddy！

突然，一只灰色的新猫（SHADOW）出现在树后...
```

#### 2. 场景文件（scenes/*.json）

每个场景的详细信息，包括：
- 场景描述
- 参与角色
- 场景环境
- 时间和地点

#### 3. 分镜文件（storyboard/*.json）

每个镜头的分镜设计，包括：
- 镜头类型（特写、中景、远景等）
- 摄像机运动（推拉摇移等）
- 画面构图描述
- 视觉提示词（用于图像生成）

#### 4. 图像文件（images/*.png）

为每个镜头生成的关键帧图像，分辨率通常为 1280x720 或更高。

#### 5. 视频片段（videos/*.mp4）

基于关键帧生成的短视频片段，通常时长 3-8 秒。

#### 6. 最终视频（final_video.mp4）

将所有视频片段按顺序拼接而成的完整视频。

### 查看结果

生成完成后，您可以：

1. **查看最终视频**：
   ```bash
   # 使用系统默认播放器打开
   open .working_dir/idea2video/final_video.mp4  # macOS
   xdg-open .working_dir/idea2video/final_video.mp4  # Linux
   start .working_dir/idea2video/final_video.mp4  # Windows
   ```

2. **查看剧本**：
   ```bash
   cat .working_dir/idea2video/script.txt
   ```

3. **浏览所有生成的图像**：
   ```bash
   ls -lh .working_dir/idea2video/images/
   ```

### 预期效果

- **视频时长**：根据场景数量和镜头数量，通常在 30 秒到 3 分钟之间
- **视频质量**：1280x720 或 1920x1080，取决于使用的视频生成模型
- **生成时间**：
  - Idea2Video（3 个场景）：约 5-10 分钟
  - Script2Video（10 个镜头）：约 8-15 分钟
  - 实际时间取决于 API 响应速度和网络状况

### 示例截图说明

由于本文档为纯文本格式，无法直接展示截图。但您可以期待看到：

- **剧本生成**：结构清晰的场景描述和对话
- **关键帧图像**：高质量的 AI 生成图像，符合剧本描述
- **视频片段**：流畅的动态画面，角色和场景保持一致性
- **最终视频**：完整的故事叙事，镜头衔接自然

## 相关资源

### 深入学习

完成快速开始后，建议您继续阅读以下文档：

- **[系统架构](./architecture.md)** - 深入了解 ViMax 的多智能体架构和设计理念
- **[核心流水线](./pipelines.md)** - 详细了解 Idea2Video、Script2Video 和 Novel2Video 的工作流程
- **[智能体详解](./agents.md)** - 探索各个智能体的功能和协作机制
- **[工具与集成](./tools.md)** - 了解如何切换和配置不同的 AI 模型
- **[开发指南](./development.md)** - 学习如何扩展和定制 ViMax

### 外部资源

- **[ViMax GitHub 仓库](https://github.com/HKUDS/ViMax)** - 源代码和最新更新
- **[Python 官方文档](https://docs.python.org/3/)** - Python 编程参考
- **[uv 文档](https://docs.astral.sh/uv/)** - uv 包管理器使用指南
- **[Google AI Studio](https://aistudio.google.com/)** - 获取 Gemini 和 Veo API Key
- **[OpenRouter](https://openrouter.ai/)** - 统一的 AI 模型访问平台

### 社区与支持

- **GitHub Issues**: [提交问题和建议](https://github.com/HKUDS/ViMax/issues)
- **交流群**: 查看 [Communication.md](../Communication.md) 了解如何加入社区
- **贡献指南**: 参阅 [开发指南](./development.md) 了解如何为项目做贡献

### 常见问题

如果您在使用过程中遇到问题，可以：

1. 查看本文档的"故障排查"部分
2. 搜索 [GitHub Issues](https://github.com/HKUDS/ViMax/issues) 中的已知问题
3. 创建新的 Issue 并提供详细的错误信息
4. 在社区交流群中寻求帮助

---

**祝您使用愉快！** 如果您成功生成了第一个视频，欢迎在社区分享您的作品和经验。
