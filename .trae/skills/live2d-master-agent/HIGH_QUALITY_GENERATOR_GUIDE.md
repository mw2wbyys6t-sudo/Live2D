# 🎨 Live2D 高质量图片生成器 - 完整指南

## 📋 概述

本工具集成了多种高质量免费图片生成服务,专为Live2D角色制作优化。

## 🌐 支持的服务

### 1. Pollinations.ai ⭐⭐⭐⭐⭐ (推荐)
- **费用**: 完全免费
- **API Key**: 无需
- **速度**: 快
- **质量**: 高
- **可靠性**: 较高
- **特点**: 
  - 无需注册
  - 支持自定义种子(可复现)
  - Live2D优化提示词自动添加
  - 支持多种尺寸

### 2. Puter.js ⭐⭐⭐⭐
- **费用**: 免费
- **API Key**: 无需
- **速度**: 中等
- **质量**: 很高
- **特点**:
  - Stable Diffusion 3 / XL
  - 企业级质量
  - 需要JavaScript环境

### 3. SiliconFlow ⭐⭐⭐⭐
- **费用**: 新用户送2000万Tokens
- **API Key**: 需要
- **速度**: 快
- **质量**: 很高
- **特点**:
  - 永久免费(9B以下模型)
  - 支持Stable Diffusion 3/XL
  - 无并发限制

### 4. Hugging Face ⭐⭐⭐
- **费用**: 免费(有速率限制)
- **API Key**: 需要
- **速度**: 慢(模型加载)
- **质量**: 很高
- **特点**:
  - 多种模型选择
  - 社区模型支持
  - 研究友好

### 5. ComfyUI本地 ⭐⭐⭐⭐⭐ (最高质量)
- **费用**: 免费
- **API Key**: 无需
- **速度**: 取决于硬件
- **质量**: 最高
- **特点**:
  - 完全离线可用
  - 无使用限制
  - 完全隐私保护
  - 最高图像质量

## 🚀 快速开始

### 方法1: 使用主工具箱
```bash
# 自动选择最佳服务生成
python master_tool.py "anime girl, pink hair"

# 使用已有图片跳过生成
python master_tool.py --skip-generate
```

### 方法2: 使用高质量生成器
```bash
# 生成基本图片
python high_quality_image_generator.py "cute anime girl"

# 指定尺寸
python high_quality_image_generator.py "anime girl" --width 1024 --height 1024

# 指定种子(可复现)
python high_quality_image_generator.py "anime girl" --seed 12345

# 运行演示
python high_quality_image_generator.py --demo

# 查看帮助
python high_quality_image_generator.py --help-full
```

### 方法3: 在Python中使用
```python
from high_quality_image_generator import HighQualityImageGenerator

gen = HighQualityImageGenerator()

# 基础生成
result = gen.generate("anime girl, pink hair")

# 自定义参数
result = gen.generate(
    prompt="beautiful anime girl",
    width=1024,
    height=1024,
    seed=12345,
    service='pollinations'  # 或 'auto'
)

# 批量生成
prompts = [
    "cute anime girl, pink hair",
    "beautiful girl, blue eyes",
    "kawaii character, cat ears"
]

for prompt in prompts:
    result = gen.generate(prompt)
    if result:
        print(f"Generated: {result}")
```

## 🎯 Live2D优化

工具会自动为你的提示词添加Live2D优化后缀:

```
, perfect for Live2D rigging, clean layer separation, 
isolated character on white background, sharp clean lines, 
vibrant colors, ultra detailed, masterpiece
```

### 优化提示词示例

#### ✅ 推荐写法
```python
"cute anime girl, pink hair, blue eyes, sailor uniform, full body"
```

会自动转换为:
```
"cute anime girl, pink hair, blue eyes, sailor uniform, full body, 
perfect for Live2D rigging, clean layer separation, isolated character 
on white background, sharp clean lines, vibrant colors, 
ultra detailed, masterpiece"
```

#### ❌ 避免写法
```python
# 避免这些词
"blurry", "low quality", "text", "watermark"
```

### 高质量提示词模板

```python
# 角色设定
character_prompts = {
    "动漫女孩": "beautiful anime girl, long flowing pink hair, blue sparkling eyes, soft smile, school uniform, clean outlines",
    
    "猫耳少女": "cute catgirl, white hair, green cat eyes, cat ears, pink outfit, kawaii expression, sharp clean lines",
    
    "战士": "anime warrior girl, silver hair, red eyes, armor, sword, confident pose, detailed costume",
    
    "魔法少女": "magical girl, pink hair, star eyes, elegant dress, wand accessory, sparkles, clean layer separation"
}

# 通用优化词
optimization_suffix = """
, perfect for Live2D rigging
, clean layer separation
, isolated character
, solid white background
, sharp clean lines
, vibrant colors
, ultra detailed
, masterpiece
"""
```

## 🔧 高级配置

### API Key 配置

#### SiliconFlow (推荐)
```bash
# 1. 访问 https://siliconflow.cn
# 2. 注册并获取API Key
# 3. 设置环境变量
export SILICONFLOW_API_KEY='your-api-key'
```

#### Hugging Face
```bash
# 1. 访问 https://huggingface.co/settings/tokens
# 2. 创建新Token
# 3. 设置环境变量
export HUGGINGFACE_TOKEN='your-token'
```

### ComfyUI 本地部署

```bash
# 使用一键安装脚本
python install_comfyui.py

# 或手动安装
# 1. 克隆仓库
git clone https://github.com/comfyanonymous/ComfyUI.git

# 2. 安装依赖
cd ComfyUI
pip install -r requirements.txt

# 3. 下载模型
# 从 https://huggingface.co/runwayml/stable-diffusion-v1-5 下载
# 放入 models/checkpoints/

# 4. 启动
python main.py

# 5. 在浏览器打开 http://127.0.0.1:8188
```

## 📊 参数说明

### generate() 方法参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| prompt | str | 必需 | 提示词 |
| width | int | 768 | 图片宽度 |
| height | int | 768 | 图片高度 |
| seed | int | None | 随机种子(可复现) |
| service | str | 'auto' | 服务选择 |

### service 选项

- `'auto'` - 自动选择(默认)
- `'pollinations'` - Pollinations.ai
- `'puter'` - Puter.js
- `'siliconflow'` - SiliconFlow(需API Key)
- `'huggingface'` - Hugging Face(需Token)
- `'comfyui'` - ComfyUI本地

## 💡 最佳实践

### 1. 网络不稳定时
```python
# 使用种子保证可复现
gen = HighQualityImageGenerator()

# 第一次生成
result1 = gen.generate("anime girl", seed=12345)

# 失败后重试(相同种子)
result2 = gen.generate("anime girl", seed=12345)

# 结果相同!
```

### 2. 追求最高质量
```python
# 优先级: ComfyUI > SiliconFlow > HuggingFace > Pollinations

# 最高质量方案
result = gen.generate(prompt, service='comfyui')

# 或使用SiliconFlow(需要API Key)
result = gen.generate(prompt, service='siliconflow')
```

### 3. 批量生成
```python
gen = HighQualityImageGenerator()

prompts = [
    "anime girl, pink hair",
    "anime girl, blue hair",
    "anime girl, red hair"
]

results = []
for prompt in prompts:
    for attempt in range(3):  # 最多重试3次
        result = gen.generate(prompt)
        if result:
            results.append(result)
            break
    time.sleep(1)  # 避免过快请求

print(f"成功: {len(results)}/{len(prompts)}")
```

### 4. 错误处理
```python
try:
    result = gen.generate("anime girl")
    if result:
        print(f"成功: {result}")
    else:
        print("生成失败,尝试备用方案...")
        # 使用已有图片
        from master_tool import Live2DMaster
        tool = Live2DMaster()
        result = tool.generate_offline("")
except Exception as e:
    print(f"错误: {e}")
    # 记录日志等
```

## 🐛 故障排除

### 问题: Pollinations.ai 返回403错误
```python
# 解决方案: 工具已自动处理
# 如果仍然失败,尝试:
result = gen.generate(prompt, service='siliconflow')
```

### 问题: HuggingFace 模型加载慢
```python
# 首次使用需要下载模型
# 耐心等待,或使用其他服务
# 建议: 模型下载后会有缓存
```

### 问题: 网络完全不可用
```python
# 使用离线方案
result = gen.generate(prompt, service='comfyui')

# 或使用已有图片
tool = Live2DMaster()
result = tool.generate_offline("")
```

## 📈 性能对比

| 服务 | 首次生成 | 后续生成 | 质量评分 |
|------|----------|----------|----------|
| Pollinations.ai | 5-15秒 | 5-15秒 | ⭐⭐⭐⭐ |
| Puter.js | 10-30秒 | 10-30秒 | ⭐⭐⭐⭐⭐ |
| SiliconFlow | 3-10秒 | 3-10秒 | ⭐⭐⭐⭐⭐ |
| HuggingFace | 30-120秒 | 5-15秒 | ⭐⭐⭐⭐⭐ |
| ComfyUI本地 | 10-60秒 | 5-30秒 | ⭐⭐⭐⭐⭐+ |

## 🎓 进阶技巧

### 1. 提示词工程
```python
# 使用权重
"anime girl (pink hair:1.5), blue eyes"

# 否定提示词
negative = "blurry, low quality, extra fingers"

# 组合使用
result = gen.generate(
    prompt="anime girl, detailed face, sharp eyes",
    negative_prompt=negative
)
```

### 2. 风格控制
```python
styles = {
    "anime": "anime style, cel shading, vibrant colors",
    "realistic": "photorealistic, detailed, natural lighting",
    "chibi": "chibi style, cute, big head, small body",
    "semi-realistic": "semi-realistic anime, detailed, soft shading"
}

result = gen.generate(f"anime girl, {styles['anime']}")
```

### 3. 批量优化
```python
import concurrent.futures
from high_quality_image_generator import HighQualityImageGenerator

def generate_with_timeout(prompt):
    gen = HighQualityImageGenerator()
    return gen.generate(prompt, timeout=60)

prompts = ["girl1", "girl2", "girl3", "girl4"]

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(generate_with_timeout, prompts))
```

## 📚 相关资源

- **主工具箱**: `master_tool.py`
- **PSD转换器**: `live2d_psd_converter.py`
- **质量检查**: `scripts/qa_engine_enhanced.py`
- **参数设计**: `scripts/parameter_designer_enhanced.py`
- **Rigging指南**: `docs/RIGGING_GUIDE.md`
- **免费方案**: `FREE_SOLUTIONS.md`

## 🤝 贡献

欢迎提交Issue和Pull Request!

## 📄 许可证

MIT License

## 🙏 致谢

- Pollinations.ai - 免费图片生成
- Stability AI - Stable Diffusion
- Hugging Face - 模型平台
- SiliconFlow - 免费API额度
- ComfyUI - 本地AI工具

---

💡 **提示**: 定期检查更新,工具会持续优化和改进!

🎉 **祝创作愉快!**
