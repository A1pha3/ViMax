# 工具与集成 (Tools)

ViMax 通过 `tools` 模块集成外部的 AI 模型和 API。这种设计使得系统可以灵活切换不同的底层模型。

## 视频生成工具 (Video Generators)

### VideoGeneratorVeoGoogleAPI
集成 Google Veo 模型。
- **特点**: 生成质量高，连贯性好。
- **配置**: 需要 Google Cloud API Key。

### VideoGeneratorVeoYunwuAPI
集成 Google Veo 模型（通过云雾 API）。
- **特点**: 国内访问更稳定。

### VideoGeneratorDoubaoSeedanceYunwuAPI
集成字节跳动豆包 (Doubao) 视频生成模型（通过云雾 API）。
- **特点**: 响应速度快，适合生成特定风格的视频。

## 图像生成工具 (Image Generators)

### ImageGeneratorNanobananaGoogleAPI
集成 Google 的图像生成能力。
- **用途**: 用于生成分镜关键帧、角色画像等。

### ImageGeneratorNanobananaYunwuAPI
集成 Google 的图像生成能力（通过云雾 API）。

### ImageGeneratorDoubaoSeedreamYunwuAPI
集成豆包 (Doubao) 图像生成模型。

## 辅助工具

### RerankerBgeSiliconapi
集成 BGE Rerank 模型（通过 SiliconFlow API）。
- **用途**: 在 RAG（检索增强生成）流程中，对检索到的文本块进行重排序，提高相关性准确度。主要用于 Novel2Video 流程中的知识库检索。

## 如何配置工具

在 `configs/*.yaml` 文件中，您可以指定使用哪个工具类以及相应的初始化参数（如 API Key）。

示例：

```yaml
# 使用 Google Veo 生成视频
video_generator:
  class_path: tools.VideoGeneratorVeoGoogleAPI
  init_args:
    api_key: "YOUR_GOOGLE_API_KEY"

# 切换为豆包模型
# video_generator:
#   class_path: tools.VideoGeneratorDoubaoSeedanceYunwuAPI
#   init_args:
#     api_key: "YOUR_YUNWU_API_KEY"
```

## 添加新工具

如果您需要支持新的模型（如 Sora, Runway 等），只需在 `tools/` 目录下创建一个新的 Python 文件，继承基类并实现相应的接口（通常是 `generate_video` 或 `generate_image` 方法），然后在配置文件中引用即可。
