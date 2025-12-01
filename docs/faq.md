# 常见问题解答 (FAQ)

> 本文档收集和整理 ViMax 使用过程中的常见问题

## 目录

- [基础问题](#基础问题)
- [安装和配置](#安装和配置)
- [功能和特性](#功能和特性)
- [性能和优化](#性能和优化)
- [成本和计费](#成本和计费)
- [技术细节](#技术细节)
- [故障排查](#故障排查)
- [相关资源](#相关资源)

---

## 基础问题

### Q1: ViMax 是什么？

**A**: ViMax 是一个多智能体视频生成框架，可以将创意、剧本或小说自动转换为完整的视频。它通过模拟真实的影视制作团队（编剧、导演、分镜师等），实现从文本到视频的端到端自动化生成。

**相关文档**: [系统架构](./architecture.md)

---

### Q2: ViMax 适合哪些用户？

**A**: ViMax 适合以下用户：

- **内容创作者**: 快速生成社交媒体短视频
- **故事作者**: 将小说或剧本可视化
- **教育工作者**: 制作教学视频
- **开发者**: 研究多智能体系统和视频生成技术
- **企业**: 自动化视频内容生产

---

### Q3: ViMax 支持哪些语言？

**A**: ViMax 支持多种语言：

- **输入**: 支持任何语言的文本输入（创意、剧本等）
- **输出**: 视频内容的语言取决于输入文本
- **文档**: 目前提供中文和英文文档

**注意**: 不同的 AI 模型对不同语言的支持程度可能有所不同。

---

### Q4: ViMax 是免费的吗？

**A**: ViMax 框架本身是开源免费的，但使用过程中需要调用第三方 AI 服务（如 Google Gemini、Veo 等），这些服务通常是按使用量计费的。

**成本估算**: 生成一个 1-2 分钟的视频大约需要 $1-5 美元（取决于使用的模型和服务）。

**相关问题**: [Q15: 生成一个视频大约需要多少费用？](#q15-生成一个视频大约需要多少费用)

## 安装和配置

### Q5: ViMax 需要什么样的硬件配置？

**A**: 最低配置：

- **CPU**: 任何现代 CPU（不需要 GPU）
- **内存**: 8GB RAM（推荐 16GB）
- **存储**: 10GB 可用空间
- **网络**: 稳定的互联网连接（至少 10 Mbps）

**说明**: ViMax 主要调用云端 API，不需要本地 GPU。

**相关文档**: [快速开始 - 环境要求](./getting_started.md#环境要求)

---

### Q6: 支持哪些操作系统？

**A**: ViMax 支持：

- **Linux**: Ubuntu 20.04+, Debian 11+, CentOS 8+（推荐）
- **macOS**: macOS 12+ (支持 Intel 和 Apple Silicon)
- **Windows**: Windows 10/11（推荐使用 WSL2）

**相关文档**: [快速开始 - 操作系统](./getting_started.md#操作系统)

---

### Q7: 如何获取 API Key？

**A**: 不同服务的 API Key 获取方式：

1. **Google API Key**:
   - 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
   - 登录并创建 API Key

2. **OpenRouter API Key**:
   - 访问 [OpenRouter](https://openrouter.ai/keys)
   - 注册并创建 API Key
   - 充值账户

3. **云雾 API Key**:
   - 访问 [云雾 AI](https://yunwu.ai/)
   - 注册并完成实名认证
   - 在控制台创建 API Key

**相关文档**: [快速开始 - API Key 获取指南](./getting_started.md#api-key-获取指南)

---

### Q8: 配置文件中的 API Key 会被泄露吗？

**A**: 为了安全：

1. **不要提交到公开仓库**: 配置文件已在 `.gitignore` 中
2. **使用环境变量**: 可以将 API Key 存储在环境变量中
3. **定期轮换**: 定期更换 API Key
4. **限制权限**: 为 API Key 设置最小必需权限

**最佳实践**:

```bash
# 使用环境变量
export OPENROUTER_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"
```

然后在代码中读取：

```python
import os
api_key = os.getenv("OPENROUTER_API_KEY")
```

## 功能和特性

### Q9: Idea2Video 和 Script2Video 有什么区别？

**A**: 

| 特性 | Idea2Video | Script2Video |
|------|-----------|-------------|
| 输入 | 简单创意（一句话或段落） | 完整剧本 |
| 自动化程度 | 高（自动扩写故事和剧本） | 中（直接使用提供的剧本） |
| 适用场景 | 快速原型、创意探索 | 精确控制、专业制作 |
| 生成时间 | 较长（需要扩写） | 较短 |

**使用建议**:
- 如果您有明确的剧本，使用 Script2Video
- 如果只有一个想法，使用 Idea2Video

**相关文档**: [系统架构 - 流水线层](./architecture.md#流水线层-pipeline-layer)

---

### Q10: 可以生成多长的视频？

**A**: 理论上没有长度限制，但实际受以下因素影响：

- **API 限制**: 单次调用的 token 限制
- **成本**: 更长的视频成本更高
- **时间**: 生成时间与长度成正比
- **一致性**: 越长的视频越难保持一致性

**建议**:
- 短视频（30秒-2分钟）: 直接生成
- 中等视频（2-5分钟）: 分场景生成
- 长视频（5分钟以上）: 使用分段生成

**相关文档**: [示例 - 长视频分段生成](./examples.md#场景-2-长视频分段生成)

---

### Q11: 支持哪些视觉风格？

**A**: ViMax 支持多种视觉风格：

- **Cartoon**: 卡通风格
- **Anime**: 动漫风格
- **Realistic**: 写实风格
- **Cyberpunk**: 赛博朋克风格
- **Watercolor**: 水彩画风格
- **3D Render**: 3D 渲染风格
- **自定义**: 可以在提示词中描述任何风格

**使用方法**:

```python
style = "Cartoon"  # 或其他风格
```

---

### Q12: 可以使用自己的角色画像吗？

**A**: 可以！您可以提供预定义的角色画像：

```python
character_portraits_registry = {
    "Alice": {
        "front": {"path": "portraits/alice_front.png", "description": "..."},  # 使用实际路径
        "side": {"path": "portraits/alice_side.png", "description": "..."},
        "back": {"path": "portraits/alice_back.png", "description": "..."}
    }
}

video_path = await pipeline(
    script=script,
    character_portraits_registry=character_portraits_registry
)
```

**相关文档**: [示例 - 使用预定义角色](./examples.md#示例-2-使用预定义角色)

---

### Q13: Novel2Video 功能可用吗？

**A**: Novel2Video 目前处于实验阶段，部分功能尚未完全实现。

**当前状态**:
- ✅ 小说压缩
- ✅ 事件提取
- ✅ 场景生成
- ⚠️ 角色一致性（实验性）
- ⚠️ 长篇处理（实验性）

**建议**: 对于长篇小说，建议先手动分章节，然后使用 Script2Video 逐章生成。

---

## 性能和优化

### Q14: 生成一个视频需要多长时间？

**A**: 生成时间取决于多个因素：

| 视频长度 | 场景数 | 镜头数 | 预计时间 |
|---------|-------|-------|---------|
| 30秒 | 1-2 | 5-8 | 5-10分钟 |
| 1分钟 | 2-3 | 10-15 | 10-20分钟 |
| 2分钟 | 3-5 | 15-25 | 20-40分钟 |
| 5分钟+ | 5+ | 25+ | 40分钟+ |

**影响因素**:
- API 响应速度
- 网络速度
- 场景复杂度
- 使用的模型

**优化建议**: 参考 [示例 - 性能优化技巧](./examples.md#性能优化技巧)

---

## 成本和计费

### Q15: 生成一个视频大约需要多少费用？

**A**: 成本估算（使用 Google Veo 和 Gemini）：

| 视频长度 | 场景数 | 镜头数 | 预计成本 |
|---------|-------|-------|---------|
| 30秒 | 1-2 | 5-8 | $0.5-1 |
| 1分钟 | 2-3 | 10-15 | $1-2 |
| 2分钟 | 3-5 | 15-25 | $2-5 |
| 5分钟+ | 5+ | 25+ | $5-15 |

**成本构成**:
- 语言模型调用（Gemini）: ~20%
- 图像生成: ~30%
- 视频生成（Veo）: ~50%

**节省成本的方法**:
1. 减少场景和镜头数量
2. 使用更便宜的模型
3. 启用缓存避免重复生成
4. 批量生成获取折扣

---

### Q16: 如何控制成本？

**A**: 控制成本的方法：

1. **限制场景和镜头**:
```python
user_requirement = "不超过 3 个场景，每个场景不超过 5 个镜头"
```

2. **使用缓存**:
```python
# 避免重复生成相同内容
# ViMax 会自动缓存中间结果
```

3. **选择性生成**:
```python
# 先生成关键帧预览，确认后再生成视频
```

4. **使用更便宜的服务**:
```yaml
# 使用字节豆包等国内服务
video_generator:
  class_path: tools.VideoGeneratorDoubaoSeedanceYunwuAPI
```

## 技术细节

### Q17: ViMax 使用了哪些技术？

**A**: 主要技术栈：

- **Python 3.12+**: 主要编程语言
- **asyncio**: 异步编程框架
- **LangChain**: LLM 应用开发框架
- **Pydantic**: 数据验证和序列化
- **MoviePy**: 视频编辑和处理
- **FAISS**: 向量相似度搜索（Novel2Video）
- **OpenCV**: 图像和视频处理

**相关文档**: [系统架构](./architecture.md)

---

### Q18: 如何扩展 ViMax？

**A**: ViMax 提供多种扩展方式：

1. **自定义智能体**: 创建新的智能体类
2. **自定义工具**: 集成新的 AI 服务
3. **自定义流水线**: 组合智能体创建新流程
4. **自定义数据模型**: 扩展数据结构

**相关文档**: 
- [示例 - 自定义智能体](./examples.md#自定义智能体示例)
- [示例 - 自定义工具](./examples.md#自定义工具示例)
- [开发指南](./development.md)

---

### Q19: ViMax 的多智能体架构有什么优势？

**A**: 多智能体架构的优势：

1. **模块化**: 每个智能体职责明确，易于维护
2. **可扩展**: 可以轻松添加新的智能体
3. **并行处理**: 多个智能体可以同时工作
4. **专业化**: 每个智能体专注于特定任务
5. **灵活性**: 可以根据需求组合不同的智能体

**相关文档**: [系统架构 - 多智能体协作机制](./architecture.md#多智能体协作机制)

---

### Q20: 如何保证角色一致性？

**A**: ViMax 使用多种机制保证一致性：

1. **角色画像**: 为每个角色生成标准形象（前/侧/后视图）
2. **参考图像选择**: 智能选择最合适的参考图
3. **全局信息规划**: 跨场景追踪角色状态
4. **摄像机树**: 管理镜头之间的连续性

**相关文档**: [系统架构 - 核心设计理念](./architecture.md#核心设计理念)

---

## 故障排查

### Q21: 为什么生成的视频质量不好？

**A**: 可能的原因和解决方案：

1. **提示词不够详细**: 提供更详细的描述
2. **使用的模型质量较低**: 切换到 Veo 等高质量模型
3. **参考图像质量问题**: 检查角色画像质量
4. **网络问题**: 确保网络连接稳定

**相关文档**: [故障排查 - 输出质量问题](./troubleshooting.md#输出质量问题)

---

### Q22: 遇到 API 错误怎么办？

**A**: 常见 API 错误及解决方案：

1. **Authentication Failed**: 检查 API Key 是否正确
2. **Quota Exceeded**: 等待配额重置或升级套餐
3. **Connection Timeout**: 检查网络连接

**相关文档**: [故障排查 - API 相关错误](./troubleshooting.md#api-相关错误)

---

### Q23: 如何查看详细的错误信息？

**A**: 查看错误信息的方法：

1. **终端输出**: 查看完整的错误堆栈
2. **工作目录**: 检查 `.working_dir/` 中的文件
3. **启用调试日志**:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**相关文档**: [故障排查 - 日志分析指南](./troubleshooting.md#日志分析指南)

---

### Q24: 程序运行中断了，如何恢复？

**A**: ViMax 支持断点续传：

1. **自动缓存**: 已生成的中间文件会被保存
2. **重新运行**: 直接重新运行，会跳过已完成的步骤
3. **手动恢复**: 检查 `.working_dir/` 中的文件

**示例**:

```python
# 重新运行相同的命令
# ViMax 会自动检测已完成的步骤
video_path = await pipeline(
    idea=idea,
    user_requirement=user_requirement,
    style=style
)
```

**相关文档**: [示例 - 增量生成和断点续传](./examples.md#技巧-4-增量生成和断点续传)

---

### Q25: 如何获取帮助？

**A**: 获取帮助的途径：

1. **查看文档**: 
   - [快速开始](./getting_started.md)
   - [故障排查](./troubleshooting.md)
   - [API 参考](./api_reference.md)

2. **搜索 Issues**: [GitHub Issues](https://github.com/HKUDS/ViMax/issues)

3. **提交新 Issue**: 提供详细的错误信息和复现步骤

4. **加入社区**: 查看 [Communication.md](../Communication.md)

---

## 相关资源

### 文档导航

- **[快速开始](./getting_started.md)** - 安装和基础使用
- **[系统架构](./architecture.md)** - 理解系统设计
- **[配置详解](./configuration.md)** - 配置选项说明
- **[API 参考](./api_reference.md)** - API 文档
- **[示例与最佳实践](./examples.md)** - 使用示例
- **[故障排查](./troubleshooting.md)** - 问题解决
- **[开发指南](./development.md)** - 扩展和定制

### 外部资源

- **[GitHub 仓库](https://github.com/HKUDS/ViMax)** - 源代码和更新
- **[Google AI Studio](https://aistudio.google.com/)** - 获取 API Key
- **[OpenRouter](https://openrouter.ai/)** - 统一 AI 模型访问
- **[云雾 AI](https://yunwu.ai/)** - 国内 AI 服务

### 社区

- **GitHub Issues**: [提交问题](https://github.com/HKUDS/ViMax/issues)
- **交流群**: 查看 [Communication.md](../Communication.md)

---

**没有找到您的问题？** 请在 [GitHub Issues](https://github.com/HKUDS/ViMax/issues) 中提问，或加入社区交流群。
