# 故障排查指南

> 本文档提供 ViMax 常见问题的诊断方法和解决方案

## 目录

- [前置知识](#前置知识)
- [常见错误分类](#常见错误分类)
- [API 相关错误](#api-相关错误)
- [配置相关错误](#配置相关错误)
- [依赖和环境错误](#依赖和环境错误)
- [运行时错误](#运行时错误)
- [性能问题](#性能问题)
- [输出质量问题](#输出质量问题)
- [日志分析指南](#日志分析指南)
- [获取帮助](#获取帮助)
- [相关资源](#相关资源)

## 前置知识

在排查问题之前，建议您：

1. 查看终端输出的完整错误信息
2. 检查 `.working_dir/` 中的日志文件
3. 确认您的配置文件格式正确
4. 验证网络连接正常

**快速诊断清单**：

- [ ] API Key 是否已正确配置？
- [ ] 网络连接是否正常？
- [ ] Python 版本是否为 3.12+？
- [ ] 依赖包是否已正确安装？
- [ ] 磁盘空间是否充足（至少 10GB）？

---

## 常见错误分类

ViMax 的错误可以分为以下几类：

| 错误类型 | 常见原因 | 严重程度 |
|---------|---------|---------|
| API 错误 | API Key 无效、配额超限、网络问题 | 高 |
| 配置错误 | YAML 语法错误、参数缺失 | 高 |
| 依赖错误 | 包未安装、版本不兼容 | 高 |
| 运行时错误 | 内存不足、文件权限问题 | 中 |
| 性能问题 | 生成速度慢、资源占用高 | 低 |
| 质量问题 | 输出不符合预期 | 低 |

---

## API 相关错误

### 错误 1: Authentication Failed

#### 症状

```
Error: Authentication failed: Invalid API key
```

或

```
401 Unauthorized: API key is invalid
```

#### 原因

1. API Key 未填写或填写错误
2. API Key 已过期或被撤销
3. API Key 权限不足
4. 使用了错误服务的 API Key

#### 诊断步骤

1. **检查配置文件**：

```bash
cat configs/idea2video.yaml | grep api_key
```

确认所有 `api_key` 字段都已填写。

2. **验证 API Key 格式**：

- Google API Key: 应以 `AIza` 开头
- OpenRouter API Key: 应以 `sk-or-v1-` 开头
- 云雾 API Key: 应以 `yw-` 开头

3. **测试 API Key**：

```bash
# 测试 OpenRouter API Key
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

如果返回 401 错误，说明 API Key 无效。

#### 解决方案

1. **重新获取 API Key**：
   - Google: 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
   - OpenRouter: 访问 [OpenRouter Keys](https://openrouter.ai/keys)
   - 云雾: 访问 [云雾控制台](https://yunwu.ai/)

2. **更新配置文件**：

```yaml
chat_model:
  init_args:
    api_key: YOUR_NEW_API_KEY  # 替换为新的 API Key
```

3. **检查 API Key 权限**：
   - 确保 API Key 有访问所需服务的权限
   - 检查账户是否已激活

---

### 错误 2: Quota Exceeded

#### 症状

```
Error: Rate limit exceeded
```

或

```
429 Too Many Requests: You have exceeded your quota
```

#### 原因

1. API 调用次数超过限额
2. 账户余额不足
3. 请求频率过高

#### 诊断步骤

1. **检查账户配额**：
   - 登录服务提供商的控制台
   - 查看当前使用量和限额

2. **检查账户余额**：
   - 确认账户有足够的余额
   - 查看计费历史

#### 解决方案

1. **等待配额重置**：
   - 大多数服务按分钟或小时重置配额
   - 查看服务文档了解重置时间

2. **升级套餐**：
   - 升级到更高的 API 套餐
   - 增加配额限制

3. **充值账户**：
   - 为账户充值以继续使用

4. **添加重试延迟**：

```python
import asyncio

async def generate_with_retry(pipeline, **kwargs):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return await pipeline(**kwargs)
        except Exception as e:
            if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                wait_time = 2 ** attempt * 60  # 指数退避（分钟）
                print(f"⏳ 配额超限，等待 {wait_time} 秒...")
                await asyncio.sleep(wait_time)
            else:
                raise
```

---

### 错误 3: Network Connection Error

#### 症状

```
Error: Connection timeout
```

或

```
requests.exceptions.ConnectionError: Failed to establish connection
```

#### 原因

1. 网络不稳定或断开
2. 防火墙阻止连接
3. API 服务暂时不可用
4. DNS 解析失败

#### 诊断步骤

1. **测试网络连接**：

```bash
ping google.com
```

2. **测试 API 端点**：

```bash
curl -I https://openrouter.ai/api/v1/models
```

3. **检查 DNS 解析**：

```bash
nslookup openrouter.ai
```

4. **检查防火墙设置**：

```bash
# Linux
sudo iptables -L

# macOS
sudo pfctl -s rules
```

#### 解决方案

1. **检查网络连接**：
   - 确保网络连接正常
   - 尝试切换网络（如使用手机热点）

2. **配置代理**（如果需要）：

```bash
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
python main_idea2video.py
```

或在代码中设置：

```python
import os
os.environ['HTTP_PROXY'] = 'http://your-proxy:port'
os.environ['HTTPS_PROXY'] = 'http://your-proxy:port'
```

3. **使用国内可访问的服务**：
   - 使用云雾 API 或 OpenRouter
   - 避免直接访问被墙的服务

4. **检查防火墙规则**：
   - 允许 Python 访问网络
   - 开放必要的端口

---

## 配置相关错误

### 错误 4: YAML Syntax Error

#### 症状

```
yaml.scanner.ScannerError: mapping values are not allowed here
```

或

```
yaml.parser.ParserError: expected <block end>, but found '<block mapping start>'
```

#### 原因

1. YAML 缩进错误
2. 使用了制表符而非空格
3. 冒号后缺少空格
4. 引号不匹配

#### 诊断步骤

1. **检查缩进**：
   - YAML 使用空格缩进，通常为 2 个空格
   - 不要使用制表符

2. **检查冒号**：
   - 冒号后必须有空格：`key: value`
   - 不能是：`key:value`

3. **使用 YAML 验证工具**：

```python
import yaml

with open("configs/idea2video.yaml", "r") as f:
    try:
        config = yaml.safe_load(f)
        print("✅ YAML 语法正确")
    except yaml.YAMLError as e:
        print(f"❌ YAML 语法错误：{e}")
```

#### 解决方案

1. **修正缩进**：

```yaml
# 错误
chat_model:
init_args:
  model: xxx

# 正确
chat_model:
  init_args:
    model: xxx
```

2. **添加空格**：

```yaml
# 错误
api_key:YOUR_KEY

# 正确
api_key: YOUR_KEY
```

3. **使用编辑器的 YAML 插件**：
   - VS Code: YAML 扩展
   - PyCharm: 内置 YAML 支持

---

### 错误 5: Missing Configuration Field

#### 症状

```
KeyError: 'api_key'
```

或

```
AttributeError: 'NoneType' object has no attribute 'api_key'
```

#### 原因

1. 配置文件中缺少必需字段
2. 字段名拼写错误
3. 配置文件路径错误

#### 诊断步骤

1. **检查配置文件完整性**：

```python
import yaml

required_fields = [
    "chat_model.init_args.api_key",
    "image_generator.init_args.api_key",
    "video_generator.init_args.api_key",
    "working_dir"
]

with open("configs/idea2video.yaml", "r") as f:
    config = yaml.safe_load(f)

for field in required_fields:
    keys = field.split('.')
    value = config
    for key in keys:
        value = value.get(key)
        if value is None:
            print(f"❌ 缺少字段：{field}")
            break
    else:
        print(f"✅ 字段存在：{field}")
```

#### 解决方案

1. **补充缺失字段**：

参考 [配置详解](./configuration.md) 补充所有必需字段。

2. **使用模板配置文件**：

```bash
cp configs/idea2video.yaml.template configs/idea2video.yaml
```

然后填写 API Key。

---

## 依赖和环境错误

### 错误 6: ModuleNotFoundError

#### 症状

```
ModuleNotFoundError: No module named 'langchain'
```

或

```
ImportError: cannot import name 'init_chat_model' from 'langchain.chat_models'
```

#### 原因

1. 依赖包未安装
2. Python 环境不正确
3. 包版本不兼容

#### 诊断步骤

1. **检查 Python 版本**：

```bash
python --version  # 应该是 3.12 或更高
```

2. **检查虚拟环境**：

```bash
which python  # 应该指向项目的虚拟环境
```

3. **检查已安装的包**：

```bash
uv pip list | grep langchain
```

#### 解决方案

1. **重新安装依赖**：

```bash
uv sync --reinstall
```

2. **手动安装缺失的包**：

```bash
uv pip install langchain langchain-openai
```

3. **确认在正确的虚拟环境中**：

```bash
# 激活虚拟环境
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
```

4. **清理并重新安装**：

```bash
rm -rf .venv
uv sync
```

---

### 错误 7: Python Version Incompatibility

#### 症状

```
SyntaxError: invalid syntax
```

或

```
RuntimeError: This package requires Python 3.12 or higher
```

#### 原因

Python 版本低于 3.12

#### 解决方案

1. **安装 Python 3.12+**：

```bash
# macOS (使用 Homebrew)
brew install python@3.12

# Ubuntu/Debian
sudo apt install python3.12

# Windows
# 从 python.org 下载安装程序
```

2. **创建新的虚拟环境**：

```bash
python3.12 -m venv .venv
source .venv/bin/activate
uv sync
```

---

## 运行时错误

### 错误 8: Out of Memory

#### 症状

```
MemoryError: Unable to allocate array
```

或

```
Killed (process terminated by system)
```

#### 原因

1. 系统内存不足
2. 处理的视频过于复杂
3. 内存泄漏

#### 诊断步骤

1. **检查内存使用**：

```bash
# Linux
free -h

# macOS
vm_stat

# 或使用 Python
import psutil
print(f"可用内存：{psutil.virtual_memory().available / 1024 / 1024 / 1024:.2f} GB")
```

#### 解决方案

1. **减少场景和镜头数量**：

```python
user_requirement = """
不超过 2 个场景
每个场景不超过 5 个镜头
"""
```

2. **关闭其他程序**：
   - 关闭浏览器和其他占用内存的应用

3. **增加交换空间**（Linux）：

```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

4. **分段处理长视频**：

参考 [示例文档](./examples.md#场景-2-长视频分段生成) 中的分段生成方法。

---

### 错误 9: Permission Denied

#### 症状

```
PermissionError: [Errno 13] Permission denied: '.working_dir/idea2video'
```

#### 原因

1. 没有写入权限
2. 文件被其他程序占用
3. 目录不存在

#### 解决方案

1. **检查目录权限**：

```bash
ls -ld .working_dir/
```

2. **修改权限**：

```bash
chmod -R 755 .working_dir/
```

3. **使用其他目录**：

```yaml
working_dir: /tmp/vimax_output  # 使用临时目录
```

4. **以管理员身份运行**（不推荐）：

```bash
sudo python main_idea2video.py
```

---

## 性能问题

### 问题 1: 生成速度慢

#### 症状

生成视频需要很长时间（超过 30 分钟）

#### 原因

1. API 响应慢
2. 网络速度慢
3. 场景和镜头过多
4. 使用了慢速模型

#### 解决方案

1. **减少场景和镜头**：

```python
user_requirement = "不超过 3 个场景，每个场景不超过 5 个镜头"
```

2. **使用更快的模型**：

```yaml
chat_model:
  init_args:
    model: google/gemini-2.5-flash-lite-preview-09-2025  # 快速模型
```

3. **使用国内服务**：
   - 云雾 API 通常比直接访问 Google 更快

4. **启用并行处理**：

代码已默认启用并行处理，无需额外配置。

---

### 问题 2: 磁盘空间不足

#### 症状

```
OSError: [Errno 28] No space left on device
```

#### 原因

磁盘空间不足

#### 解决方案

1. **检查磁盘空间**：

```bash
df -h .
```

2. **清理旧的输出文件**：

```bash
rm -rf .working_dir/old_projects
```

3. **使用外部存储**：

```yaml
working_dir: /mnt/external_drive/vimax_output
```

4. **压缩中间文件**：

生成完成后，可以删除中间文件：

```bash
# 保留最终视频，删除中间文件
find .working_dir -name "*.json" -delete
find .working_dir -name "*.png" -delete
```

---

## 输出质量问题

### 问题 1: 角色外观不一致

#### 症状

同一角色在不同镜头中外观差异很大

#### 原因

1. 角色描述不够详细
2. 参考图像质量问题
3. 图像生成的随机性

#### 解决方案

1. **详细描述角色特征**：

```python
character = CharacterInScene(
    idx=0,
    identifier_in_scene="Alice",
    is_visible=True,
    static_features="""
    Alice 是一位 25 岁的年轻女性。
    她有长长的金色直发，通常扎成马尾辫。
    蓝色的大眼睛，白皙的皮肤，身材苗条。
    身高约 165cm，体重约 50kg。
    """,
    dynamic_features="穿着红色连衣裙和白色运动鞋"
)
```

2. **使用 Novel2Video 流水线**：
   - Novel2Video 有更好的一致性保持机制

3. **手动提供角色画像**：

参考 [示例文档](./examples.md#示例-2-使用预定义角色) 中的方法。

---

### 问题 2: 视频质量不佳

#### 症状

生成的视频模糊、失真或不符合预期

#### 原因

1. 提示词不够详细
2. 使用的模型质量较低
3. 参考图像质量问题

#### 解决方案

1. **优化提示词**：

```python
# 不好的提示词
idea = "一只猫"

# 好的提示词
idea = """
一只橙色的短毛猫，名叫 Whiskers。
它有明亮的绿色眼睛和白色的爪子。
性格活泼好动，喜欢追逐蝴蝶。
"""
```

2. **使用高质量模型**：

```yaml
video_generator:
  class_path: tools.VideoGeneratorVeoGoogleAPI  # 使用 Veo（质量最高）
```

3. **调整视觉风格**：

```python
style = "Realistic"  # 尝试不同的风格
```

---

## 日志分析指南

### 查看日志

1. **终端输出**：
   - 最直接的日志来源
   - 包含实时进度和错误信息

2. **工作目录中的文件**：

```bash
# 查看生成的中间文件
ls -la .working_dir/idea2video/

# 查看剧本
cat .working_dir/idea2video/story.txt

# 查看角色信息
cat .working_dir/idea2video/characters.json
```

### 常见日志模式

#### 正常执行

```
🎬 开始生成视频...
🧠 Developing story...
✅ Developed story and saved to .working_dir/idea2video/story.txt.
🚀 Loaded 3 characters from existing file.
☑️ Completed character portrait generation for Whiskers.
...
✅ 视频生成完成！
```

#### API 错误

```
❌ Error: Authentication failed: Invalid API key
```

查找包含 `Error` 或 `❌` 的行。

#### 网络错误

```
⏳ Retrying in 5 seconds...
❌ Connection timeout after 3 attempts
```

查找包含 `timeout` 或 `connection` 的行。

---

## 获取帮助

如果以上方法无法解决您的问题：

### 1. 搜索已知问题

访问 [GitHub Issues](https://github.com/HKUDS/ViMax/issues) 搜索类似问题。

### 2. 提交新问题

创建新的 Issue 时，请提供：

- **错误信息**：完整的错误堆栈
- **配置文件**：去除 API Key 后的配置
- **运行环境**：操作系统、Python 版本
- **复现步骤**：如何触发错误

### 3. 加入社区

查看 [Communication.md](../Communication.md) 了解如何加入交流群。

---

## 相关资源

### 文档

- **[快速开始](./getting_started.md)** - 基础配置和使用
- **[配置详解](./configuration.md)** - 配置选项说明
- **[API 参考](./api_reference.md)** - API 文档
- **[示例与最佳实践](./examples.md)** - 使用示例

### 外部资源

- **[Python 异常处理](https://docs.python.org/3/tutorial/errors.html)** - Python 错误处理
- **[YAML 语法](https://yaml.org/)** - YAML 格式说明
- **[asyncio 文档](https://docs.python.org/3/library/asyncio.html)** - 异步编程

---

**提示**: 大多数问题都可以通过仔细检查配置文件和错误信息来解决。如果问题持续存在，不要犹豫，向社区寻求帮助！
