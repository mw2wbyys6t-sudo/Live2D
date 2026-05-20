# 免费图像生成方案完整指南

## 🆓 完全免费方案

### 方案 1: Stable Diffusion 本地部署 ⭐⭐⭐⭐⭐

**优点**:
- ✅ 完全免费
- ✅ 无限制使用
- ✅ 隐私保护（本地运行）
- ✅ 可自定义模型
- ✅ 质量可控

**缺点**:
- ❌ 需要较好的显卡（推荐 8GB+ 显存）
- ❌ 需要一定的技术基础

**安装步骤**:

#### Windows 安装

```powershell
# 1. 安装 Python 3.10
# 下载: https://www.python.org/downloads/release/python-31011/

# 2. 安装 Git
# 下载: https://git-scm.com/download/win

# 3. 安装 ComfyUI（推荐）
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py

# 4. 下载动漫模型
# 访问 https://civitai.com/models/9409 下载 Anything V5
# 放到 ComfyUI/models/checkpoints/ 目录
```

#### Linux/macOS 安装

```bash
# 1. 安装依赖
pip install torch torchvision diffusers transformers

# 2. 克隆 ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt
python main.py
```

---

### 方案 2: 免费在线工具 ⭐⭐⭐⭐

#### Leonardo.ai（推荐）

**免费额度**: 每天 150 张图片

**使用步骤**:
1. 访问 https://leonardo.ai/
2. 注册账号（免费）
3. 选择 "Anime" 或 "Pastel" 模型
4. 输入提示词生成

**Live2D 提示词模板**:
```
anime girl, beautiful face, big eyes,
pink long hair, JK school uniform,
isolated on white background,
clean lines, vibrant colors,
ultra detailed, masterpiece
```

---

#### Playground AI

**免费额度**: 每天 1000 张图片

**特点**:
- 完全免费
- 支持多种风格
- 可调节参数

**使用步骤**:
1. 访问 https://playground.com/
2. 注册账号
3. 选择模型和风格
4. 生成图片

---

#### Bing Image Creator

**免费额度**: 无限制（需要微软账号）

**特点**:
- 微软官方
- 使用 DALL-E 3
- 质量不错

**使用步骤**:
1. 访问 https://www.bing.com/images/create
2. 登录微软账号
3. 输入描述生成

---

### 方案 3: ComfyUI 工作流 ⭐⭐⭐⭐⭐

**ComfyUI** 是最强大的免费工具，支持工作流自动化。

#### Live2D 专用工作流

```json
{
  "workflow": "Live2D Character Generation",
  "steps": [
    {
      "step": 1,
      "action": "generate_base",
      "prompt": "anime girl, [description], white background",
      "model": "AnythingV5",
      "size": "2048x2048"
    },
    {
      "step": 2,
      "action": "upscale",
      "model": "RealESRGAN",
      "scale": 2
    },
    {
      "step": 3,
      "action": "refine",
      "prompt": "sharp lines, clean edges, vibrant colors"
    }
  ]
}
```

#### 推荐模型下载

| 模型名称 | 用途 | 下载链接 |
|----------|------|----------|
| Anything V5 | 动漫生成 | https://civitai.com/models/9409 |
| Counterfeit V3 | 高质量动漫 | https://civitai.com/models/4468 |
| Pastel Mix | 柔和风格 | https://civitai.com/models/39759 |
| RealESRGAN | 图片放大 | https://github.com/xinntao/Real-ESRGAN |

---

### 方案 4: 手绘 + 数字化 ⭐⭐⭐

**完全免费 + 可控性最强**

#### 工具

| 工具 | 类型 | 特点 |
|------|------|------|
| **Krita** | 开源绘画 | 免费，功能强大 |
| **GIMP** | 图像处理 | 免费，类似 Photoshop |
| **Inkscape** | 矢量绘制 | 免费，适合线条 |
| **FireAlpaca** | 动漫绘画 | 免费，专为动漫设计 |

#### 工作流

```
1. 在 Krita 中绘制角色
   ↓
2. 分层导出（每层一个部件）
   ↓
3. 在 GIMP 中调整
   ↓
4. 导出为 PSD
   ↓
5. 使用 Live2D Master Agent 检查
```

---

## 📊 方案对比

| 方案 | 成本 | 质量 | 易用性 | 速度 | 推荐度 |
|------|------|------|--------|------|--------|
| **Stable Diffusion 本地** | 免费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Leonardo.ai** | 免费 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Playground AI** | 免费 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Bing Creator** | 免费 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **手绘** | 免费 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐ |

---

## 🎨 Live2D 提示词模板库

### 基础模板

```
anime girl, cute kawaii style,
beautiful face, big expressive eyes,
isolated character on white background,
perfect for Live2D rigging,
clean layer separation,
sharp clean lines, vibrant colors,
ultra detailed, masterpiece
```

### 风格变体

**可爱萌系**:
```
anime girl, cute kawaii, moe style,
big eyes, soft features,
pastel colors, gentle expression
```

**帅气中性**:
```
anime girl, cool style, tomboy,
sharp features, confident expression,
dark colors, dynamic pose
```

**优雅精致**:
```
anime girl, elegant, refined,
detailed features, graceful pose,
vibrant colors, high fashion
```

**奇幻魔法**:
```
anime girl, magical girl, fantasy,
sparkles, magical elements,
ethereal, mystical atmosphere
```

---

## 💡 使用建议

### 最低配置方案（完全免费）

1. **使用 Playground AI** - 每天 1000 张免费
2. **或使用 Leonardo.ai** - 每天 150 张免费
3. **导入到 Live2D Master Agent** - 进行后续处理

### 最佳质量方案（需要显卡）

1. **安装 ComfyUI** - 本地运行
2. **下载动漫模型** - Anything V5
3. **生成高质量图片** - 无限制
4. **导入处理** - Live2D 流程

### 最灵活方案

1. **使用 Krita 手绘** - 完全控制
2. **或约稿** - 专业质量
3. **导入处理** - Live2D 流程

---

## 🔧 快速开始脚本

### Stable Diffusion 一键启动

```bash
#!/bin/bash
# install_sd.sh - Stable Diffusion 一键安装

echo "🎨 安装 Stable Diffusion..."

# 安装 ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt

# 下载推荐模型
echo "📥 下载动漫模型..."
wget -P models/checkpoints/ \
  "https://civitai.com/api/download/models/9409"

echo "✅ 安装完成！"
echo "🚀 启动命令: python main.py"
```

---

## 📚 学习资源

### Stable Diffusion 教程
- [ComfyUI 官方文档](https://comfyanonymous.github.io/ComfyUI_examples/)
- [Civitai 模型库](https://civitai.com/)
- [提示词指南](https://civitai.com/models/4201)

### 动漫绘画教程
- [Krita 教程](https://docs.krita.org/)
- [Live2D 分层指南](https://docs.live2d.com/)

---

## 🎯 总结

**完全免费的方案有很多！**

推荐顺序：
1. **Playground AI** - 最简单，每天 1000 张
2. **Leonardo.ai** - 质量好，每天 150 张
3. **Stable Diffusion 本地** - 最佳质量，无限制
4. **手绘** - 最灵活，完全控制

选择适合你的方案，然后导入到 Live2D Master Agent 进行后续处理！

---

**文档版本**: v1.0  
**更新时间**: 2026-05-20
