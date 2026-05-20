# Live2D Master Agent - 最佳质量方案完整指南

## 🎨 方案概述

这是最佳质量的完全免费方案！使用 Stable Diffusion/ComfyUI 本地部署 + Live2D Master Agent 进行完整工作流处理。

---

## 🚀 快速开始

### 第 1 步：安装 ComfyUI

根据你的系统选择对应的安装脚本：

#### Windows
```cmd
cd /workspace/.trae/skills/live2d-master-agent
install_comfyui.bat
```

#### Linux/macOS
```bash
cd /workspace/.trae/skills/live2d-master-agent
chmod +x install_comfyui.sh
./install_comfyui.sh
```

#### Python 脚本（跨平台）
```bash
cd /workspace/.trae/skills/live2d-master-agent
python install_comfyui.py
```

---

### 第 2 步：下载动漫模型

访问 CivitAI 下载推荐模型：

| 模型 | 特点 | 下载链接 |
|------|------|----------|
| **AnythingV5** | 通用动漫，质量最佳 | https://civitai.com/models/9409 |
| **CounterfeitV3** | 细节丰富，渲染精美 | https://civitai.com/models/4468 |
| **PastelMix** | 柔和风格，色彩漂亮 | https://civitai.com/models/39759 |

下载后放到：
- Windows: `Live2D-ComfyUI\ComfyUI\models\checkpoints\`
- Linux/macOS: `Live2D-ComfyUI/ComfyUI/models/checkpoints/`

---

### 第 3 步：启动 ComfyUI

#### Windows
双击运行：`Live2D-ComfyUI\start_comfyui.bat`

#### Linux/macOS
```bash
cd Live2D-ComfyUI
./start_comfyui.sh
```

然后在浏览器访问：**http://127.0.0.1:8188**

---

### 第 4 步：生成角色立绘

#### 方法 A：使用集成工具（推荐）

确保 ComfyUI 正在运行，然后使用集成工具：

```bash
cd /workspace/.trae/skills/live2d-master-agent
python comfyui_integration.py --preset "Cute Kawaii"
```

或使用交互模式：

```bash
python comfyui_integration.py
```

#### 方法 B：在浏览器中使用

1. 在浏览器中打开 http://127.0.0.1:8188
2. 加载 Live2D 专用工作流（或手动配置）
3. 输入提示词（参考下方模板）
4. 选择模型（推荐 AnythingV5）
5. 设置分辨率 2048x2048
6. 点击生成
7. 保存图片

---

### 第 5 步：导入 Live2D Master Agent

生成图片后，继续使用 Live2D Master Agent 进行后续处理：

```bash
# 返回 workspace 目录
cd /workspace

# 1. 使用角色设定文档进行规划
# （已生成 output/anime_character_concept.md）

# 2. 进行 PSD 分层规划
#（使用 Live2D Master Agent）

# 3. 质量检查
# 4. 参数设计
# 5. 物理设置
# 6. Rigging 指导
```

---

## 📝 Live2D 专用提示词模板

### 基础模板（强烈推荐）

```
anime girl, cute kawaii style,
beautiful face, big expressive eyes,
long flowing pink hair, soft pink gradient hair,
hair strands detailed, wearing JK school uniform,
white blouse, navy blue pleated skirt, red ribbon tie,
slender figure, elegant pose, standing pose,
perfect for Live2D rigging, clean layer separation,
isolated character on white background, easy to rig,
sharp clean lines, vibrant colors, ultra detailed,
masterpiece, award-winning quality, professional artwork,
4K resolution, high quality render, anime art style,
soft lighting, detailed facial features, sparkling eyes
```

### 负向提示词（必须）

```
blurry, low quality, bad anatomy, bad hands,
multiple characters, complex background,
merged layers, overlapping parts, extra fingers,
mutated, deformed, disfigured, lowres,
text, watermark, signature, logo,
worst quality, low quality, normal quality,
jpeg artifacts, blurry, out of focus
```

### 风格变体

#### 可爱萌系（Cute Kawaii）
```
anime girl, cute kawaii, moe style,
big eyes, soft features, pastel colors,
gentle expression, happy, smiling
```

#### 帅气中性（Cool Tomboy）
```
anime girl, cool style, tomboy,
sharp features, confident expression,
dark colors, dynamic pose
```

#### 优雅精致（Elegant Refined）
```
anime girl, elegant, refined,
detailed features, graceful pose,
vibrant colors, high fashion
```

#### 奇幻魔法（Magical Fantasy）
```
anime girl, magical girl, fantasy,
sparkles, magical elements,
ethereal, mystical atmosphere
```

---

## 📋 完整工作流程图

```
┌─────────────────────────────────────────────────────────┐
│  1. 安装 ComfyUI                                        │
│     (使用提供的安装脚本)                                 │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  2. 下载动漫模型                                        │
│     (推荐 AnythingV5)                                   │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  3. 启动 ComfyUI                                        │
│     (访问 http://127.0.0.1:8188)                       │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  4. 生成角色立绘                                        │
│     (使用 Live2D 专用提示词)                            │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  5. 导入 Live2D Master Agent                           │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  6. PSD 分层规划                                        │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  7. 质量检查 (QA)                                       │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  8. 参数设计 + 物理设置                                 │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  9. Rigging 指导                                        │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  10. 导入 Cubism 完成！                                  │
└─────────────────────────────────────────────────────────┘
```

---

## 💾 文件说明

### Skill 目录结构

```
/workspace/.trae/skills/live2d-master-agent/
├── SKILL.md                    # Skill 主文件
├── NO_API_GUIDE.md            # 无 API 使用指南
├── FREE_OPTIONS.md            # 免费方案详细说明
├── install_comfyui.sh         # Linux/macOS 安装脚本
├── install_comfyui.bat        # Windows 安装脚本
├── install_comfyui.py         # Python 安装脚本（跨平台）
├── comfyui_integration.py     # ComfyUI 集成工具
├── start.py                  # Skill 启动脚本
├── config.py                 # 配置加载器
├── live2d_workflow.json      # Live2D 专用工作流
└── .env                      # 环境配置（包含 API 密钥）
```

### 输出目录

```
/workspace/output/
├── anime_character_concept.md  # 角色设定文档
└── [生成的图片文件].png         # 生成的角色立绘
```

---

## 🎯 关键要点

### ✅ 此方案的优点

- **完全免费**：无任何费用
- **最高质量**：本地 Stable Diffusion 可获得专业质量
- **无限制**：想生成多少就生成多少
- **隐私保护**：完全本地运行
- **可控性强**：完全控制模型和参数

### ⚙️ 系统要求

- **显卡**：推荐 8GB+ VRAM 的 NVIDIA 显卡
- **内存**：16GB+ 推荐
- **硬盘**：至少 10GB 可用空间
- **系统**：Windows 10+/macOS 10.15+/Linux

### 📊 推荐配置

| 配置项 | 推荐值 |
|--------|--------|
| 分辨率 | 2048x2048 |
| 步数 | 30-40 |
| CFG | 7-9 |
| 采样器 | Euler |
| 模型 | AnythingV5 |

---

## 🚩 常见问题

### Q: 没有好的显卡怎么办？
A: 使用免费在线方案 Playground AI 或 Leonardo.ai，然后导入到 Live2D Master Agent。

### Q: CivitAI 下载太慢怎么办？
A: 使用其他免费在线方案，或使用预下载好的模型。

### Q: 生成的图片不够好怎么办？
A: 调整提示词，或尝试不同的模型，或增加步数。

### Q: 如何知道哪个模型最好？
A: AnythingV5 是最通用的，推荐先尝试这个。

---

## 📚 相关资源

### Stable Diffusion 资源
- **ComfyUI 官网**: https://github.com/comfyanonymous/ComfyUI
- **CivitAI**: https://civitai.com/ (模型库)
- **Stable Diffusion 教程**: https://stable-diffusion-art.com/

### Live2D 资源
- **Live2D 官网**: https://www.live2d.com/
- **Cubism Editor**: https://www.live2d.com/download/cubism/

---

## 🎉 总结

这就是完整的最佳质量方案！

1. **安装 ComfyUI**（使用我们的一键安装脚本）
2. **下载动漫模型**（推荐 AnythingV5）
3. **启动并生成图片**（使用 Live2D 专用提示词）
4. **导入 Live2D Master Agent**（继续后续处理）
5. **完成 Live2D 制作流程！**

祝制作顺利！🎨

---

**文档版本**: 1.0
**最后更新**: 2026-05-20
