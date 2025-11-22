# 系统架构

ViMax 是一个多智能体（Multi-Agent）视频生成框架，旨在通过协作工作流解决长视频生成中的一致性和连贯性问题。

## 核心设计理念

传统的 AI 视频生成工具通常只能生成几秒钟的片段，且难以保持角色和场景的一致性。ViMax 通过以下设计理念解决了这些问题：

1.  **分层规划**: 从小说/创意到事件，再到场景，最后到分镜，层层递进。
2.  **多智能体协作**: 不同的智能体（Agent）扮演不同的角色（如编剧、导演、摄影师），各司其职。
3.  **全局一致性**: 通过全局信息规划器（Global Information Planner）和资产索引（Asset Indexing）维护角色和环境的一致性。

## 架构概览

系统主要由以下几层组成：

### 1. 输入层 (Input Layer)
接收用户的原始输入，包括：
- **文本**: 创意、剧本或小说全文。
- **指令**: 风格描述、用户约束（如“面向儿童”、“黑白电影风格”）。
- **资产**: 参考图像（可选）。

### 2. 中央调度层 (Central Orchestration)
负责协调各个智能体的工作流，管理资源，处理重试和降级逻辑。

### 3. 智能体层 (Agent Layer)

ViMax 包含多个专门的智能体：

- **剧本理解 (Script Understanding)**:
    - **Event Extractor**: 从长文本中提取关键事件。
    - **Scene Extractor**: 将事件细化为具体的场景脚本。
    - **Character Extractor**: 提取角色特征和性格。
- **视觉规划 (Visual Planning)**:
    - **Script Planner**: 规划分镜脚本。
    - **Storyboard Artist**: 设计分镜画面，确定构图和运镜。
- **资产管理 (Asset Management)**:
    - **Global Information Planner**: 跨场景追踪角色和环境状态。
    - **Best Image Selector**: 从多张生成图中选择最符合一致性要求的一张。

### 4. 视觉合成层 (Visual Synthesis)
- **Image Generator**: 根据 Prompt 和参考图生成高质量图像。
- **Video Generator**: 将图像转化为视频片段（Image-to-Video）。
- **Video Editor**: 拼接片段，添加音效（未来规划）。

## 工作流示例 (Novel2Video)

1.  **压缩与分割**: 将长篇小说分割并压缩摘要。
2.  **事件提取**: 识别关键情节节点。
3.  **场景拆解**: 将每个事件拆解为具体的场景脚本。
4.  **角色统一**: 跨场景合并角色信息，生成统一的角色画像（Character Portrait）。
5.  **分镜生成**: 为每个场景生成分镜脚本。
6.  **视频生成**: 逐个场景生成视频，保持角色一致性。

## 目录结构说明

- `agents/`: 存放各类智能体的实现代码。
- `pipelines/`: 定义主要的业务流水线（Idea2Video, Script2Video 等）。
- `tools/`: 封装外部 API 工具（如 Google Gemini, Veo, Doubao 等）。
- `interfaces/`: 定义系统内部的数据交换格式（Schema）。
- `configs/`: 配置文件目录。
