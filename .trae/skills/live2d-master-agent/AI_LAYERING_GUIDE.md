# 🎨 Live2D AI智能分层工具 v4.0 - 完整使用指南

## 📋 概述

Live2D AI智能分层工具 v4.0 集成了目前市面上最先进的AI图像分层技术，可以自动将动漫角色图片分离为符合Live2D标准的多个图层，并导出PSD文件。

## 🤖 支持的AI技术

### 1. **Qwen-Image-Layered** (阿里通义实验室) ⭐⭐⭐⭐⭐
- **最新技术**: 2026年最新发布的图像分层模型
- **核心能力**: 将图像分解为3-8+个RGBA图层
- **特点**: 支持递归分层、智能填充遮挡区域
- **开源**: Apache 2.0许可证
- **模型**: `Qwen/Qwen-VL-Layered-7B` (~1.8GB)
- **推荐GPU**: RTX 3060+ (12GB显存)

```python
from qwen_image_layered import QwenImageLayered
model = QwenImageLayered.from_pretrained("Qwen/Qwen-VL-Layered-7B")
layers = model.decompose("image.png", num_layers=6)
```

### 2. **rembg** ⭐⭐⭐⭐⭐
- 最流行的背景移除库
- 支持10+种模型: u2net, u2netp, u2net_human_seg, isnet-general-use
- 支持Alpha Matting边缘优化

### 3. **SAM 2 (Segment Anything Model 2)** ⭐⭐⭐⭐
- Meta最新分割模型
- 实时处理44fps
- 支持点、框、掩码提示
- 零样本泛化能力

### 4. **本地智能分层** ⭐⭐⭐⭐
- 动漫风格优化的颜色分析
- 8种头发颜色检测
- 智能区域分割
- 边缘平滑处理

## 🚀 快速开始

### 安装依赖

```bash
# 一键安装所有AI模型
python3 install_ai_models.py

# 或者单独安装
pip3 install rembg
pip3 install segment-anything
pip3 install qwen-image-layered
```

### 下载模型

```bash
# SAM模型
mkdir -p ~/.sam
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -O ~/.sam/

# Qwen-Image-Layered模型（首次使用自动下载）
```

## 📖 使用方法

### 1. 基础分层

```bash
# 使用v4.0新版工具
python3 live2d_layer_tool.py <图片路径>

# 示例
python3 live2d_layer_tool.py output/anime_girl.png
```

### 2. 高级分层（AI增强）

```bash
# 使用AI增强版
python3 live2d_autolayer.py <图片路径>

# 使用rembg预处理
python3 live2d_autolayer.py --use-rembg output/anime_girl.png

# 使用SAM分割
python3 live2d_autolayer.py --use-sam output/anime_girl.png
```

### 3. PSD转换

```bash
# 将分层图片转换为PSD
python3 live2d_psd_converter.py <图片路径>
```

### 4. 一站式工具

```bash
# 使用主工具箱
python3 master_tool.py "anime girl, pink hair"

# 使用已有图片（离线模式）
python3 master_tool.py --skip-generate
```

## 🎯 分层结构

工具会自动生成以下图层（符合Live2D标准）:

| 序号 | 图层名称 | 说明 | 典型大小 |
|------|----------|------|----------|
| 1 | Background | 背景 | 按需 |
| 2 | Body | 身体主体 | ~150 KB |
| 3 | Clothes | 服装 | ~400 KB |
| 4 | Hair_Back | 头发后部 | ~400 KB |
| 5 | Hair_Side | 头发侧部 | ~100 KB |
| 6 | Face | 脸部皮肤 | ~100 KB |
| 7 | Hair_Front | 刘海 | ~50 KB |
| 8 | Eyes | 眼睛 | ~140 KB |
| 9 | Mouth | 嘴巴 | ~90 KB |
| 10 | Hands | 手部 | ~10 KB |
| 11 | Accessories | 配饰 | 按需 |

## 🔧 技术原理

### 智能分层算法

**步骤1: AI预处理**
- rembg: 自动移除背景（如可用）
- SAM: 精确语义分割（如可用）

**步骤2: 颜色分析**
- 头发颜色检测（8种颜色范围）
- 皮肤颜色检测（RGB范围）
- 眼睛/嘴巴颜色检测

**步骤3: 区域分割**
- top (0-15%): 刘海区域
- upper (15-35%): 脸部上半
- middle (35-60%): 脸部
- lower (60-85%): 身体上半
- bottom (85-100%): 身体下半

**步骤4: 智能分配**
```
颜色检测 → 位置检测 → 图层分配
  ↓            ↓           ↓
头发颜色? → 在顶部? → Hair_Front
皮肤颜色? → 在侧边? → Hair_Side
眼睛颜色? → 在脸部? → Eyes
皮肤颜色? → 在中间? → Face
其他颜色? → 在底部? → Body/Clothes
```

**步骤5: 边缘处理**
- GaussianBlur(radius=1) 平滑边缘
- Alpha通道优化

## 📊 性能对比

| AI模型 | 精度 | 速度 | GPU要求 | 成本 |
|--------|------|------|---------|------|
| **Qwen-Image-Layered** | ⭐⭐⭐⭐⭐ | 中等 | RTX 3060+ | 免费 |
| **rembg** | ⭐⭐⭐⭐ | 快 | 无 | 免费 |
| **SAM 2** | ⭐⭐⭐⭐⭐ | 快 | RTX 2080+ | 免费 |
| **本地智能** | ⭐⭐⭐⭐ | 极快 | 无 | 免费 |

## 💡 最佳实践

### 1. 使用Qwen-Image-Layered（推荐）

```bash
# 确保安装了qwen-image-layered
pip3 install qwen-image-layered

# 使用v4工具
python3 live2d_layer_tool.py output/anime_girl.png
```

### 2. 处理复杂图像

```bash
# 步骤1: 使用rembg移除背景
python3 -c "from rembg import remove; open('nobg.png','wb').write(remove(open('input.png','rb').read()))"

# 步骤2: 使用智能分层
python3 live2d_layer_tool.py nobg.png
```

### 3. 在线使用Qwen-Image-Layered

访问在线演示:
- https://huggingface.co/spaces/Qwen/Qwen-Image-Layered
- https://qwen-image.net/layered

### 4. PSD导出

**方法1: Photoshop（推荐）**
1. 下载所有分层PNG文件
2. Photoshop → File → Scripts → Load Files into Stack
3. 调整图层顺序
4. File → Save As → PSD

**方法2: 在线转换**
- https://convertio.co/png-to-psd/
- https://www.iloveimg.com/png-to-psd

**方法3: GIMP（免费）**
1. File → Open as Layers
2. File → Export As → PSD

### 5. Live2D导入

1. 打开 **Live2D Cubism Editor**
2. **File → Import PSD**
3. 选择生成的PSD文件
4. 勾选 "Create ArtMeshes"
5. 点击 **OK**
6. 开始制作！

## 🐛 故障排除

### 问题1: Qwen-Image-Layered安装失败

```bash
# 解决方案
pip3 install --upgrade torch
pip3 install qwen-image-layered --no-deps
pip3 install transformers accelerate
```

### 问题2: 内存不足

```bash
# 使用较小模型
# SAM: 使用vit_b模型（375MB）
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth -O ~/.sam/

# 或使用CPU模式
export CUDA_VISIBLE_DEVICES=""
python3 live2d_layer_tool.py input.png
```

### 问题3: 分层不准确

**解决方案:**
1. 使用rembg预处理
2. 上传到Qwen-Image-Layered在线演示
3. 在Photoshop中手动调整

### 问题4: 网络问题

**解决方案:**
1. 使用离线模式
2. 手动下载模型
3. 使用本地智能分层

## 📁 文件结构

```
live2d-master-agent/
├── live2d_layer_tool.py      # v4.0 新版分层工具
├── live2d_autolayer.py       # AI增强版分层工具
├── live2d_psd_converter.py   # PSD转换器
├── master_tool.py            # 一站式工具箱
├── install_ai_models.py      # AI模型安装脚本
├── AI_LAYERING_GUIDE.md      # 完整使用指南
└── output/
    ├── anime_girl.png
    ├── anime_girl_layers_qwen/
    │   ├── 01_Body.png
    │   ├── 02_Clothes.png
    │   └── ...
    └── anime_girl_live2d.psd
```

## 🔄 版本历史

### v4.0 (当前版本)
- ✅ 集成Qwen-Image-Layered
- ✅ 支持3-8+图层自动分解
- ✅ 递归分层细化
- ✅ 增强的颜色分析（8种头发颜色）
- ✅ 改进的边缘处理
- ✅ PSD直接导出

### v3.0
- ✅ rembg集成
- ✅ SAM集成
- ✅ 智能区域分割
- ✅ 边缘平滑处理

### v2.0
- ✅ 基础智能分层
- ✅ 多图层支持
- ✅ 标准命名

### v1.0
- ✅ 基础分层功能

## 📚 相关资源

- **Qwen-Image-Layered**: https://qwen-image.net/layered
- **rembg**: https://github.com/danielgatis/rembg
- **SAM 2**: https://github.com/facebookresearch/segment-anything
- **ComfyUI集成**: https://github.com/Comfy-Org/comfyui_qwen_image_layered

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

---

**🎉 Live2D AI智能分层工具 v4.0 - 让分层更智能！**
