# 🎨 Live2D AI智能分层工具 - 使用指南 v3.0

## 📋 概述

Live2D AI智能分层工具 v3.0 集成了目前市面上最先进的AI分层技术，可以自动将动漫角色图片分离为符合Live2D标准的多个图层，并导出PSD文件。

## 🤖 支持的AI技术

### 1. **Qwen-Image-Layered** (阿里) ⭐⭐⭐⭐⭐
- 最先进的AI分层模型
- 完全开源（Apache 2.0）
- 支持3-8+个图层自动分离
- 支持递归分层
- 在线演示: https://huggingface.co/spaces/Qwen/Qwen-Image-Layered

### 2. **rembg** ⭐⭐⭐⭐⭐
- 最流行的背景移除库
- 支持10+种模型：
  - `u2net`: 通用背景移除（默认）
  - `u2netp`: 轻量版
  - `u2net_human_seg`: 人物分割
  - `isnet-general-use`: 高精度
- 支持Alpha Matting（边缘优化）
- 支持批量处理

### 3. **SAM (Segment Anything)** ⭐⭐⭐⭐
- Meta开发的革命性分割模型
- 支持点、框、掩码提示
- 零样本泛化能力
- 支持图像和视频分割
- 实时处理（44fps）

### 4. **Adobe Firefly Image 5** ⭐⭐⭐⭐
- 自动分层（人物/背景/道具等）
- PSD导出
- 自然语言指令
- 深度集成Photoshop

## 🚀 快速开始

### 方法1: 一键安装所有AI模型

```bash
# 安装所有依赖
python3 install_ai_models.py

# 安装完成后测试
python3 live2d_autolayer.py output/你的图片.png
```

### 方法2: 单独安装

```bash
# 安装rembg (推荐)
pip install 'rembg[gpu]'

# 安装SAM
pip install segment-anything

# 下载SAM模型
mkdir -p ~/.sam
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -O ~/.sam/
```

## 📖 使用方法

### 1. 自动智能分层

```bash
# 基本用法
python3 live2d_autolayer.py <图片路径>

# 示例
python3 live2d_autolayer.py output/image.png
```

**工具会自动:**
1. 检测可用的AI模型
2. 使用AI模型处理图像
3. 智能分析和分层
4. 保存所有图层
5. 生成详细指南

### 2. 单独背景移除

```bash
# 使用rembg
python3 -c "from rembg import remove; input_data = open('image.png', 'rb').read(); output_data = remove(input_data); open('output.png', 'wb').write(output_data)"
```

### 3. PSD转换

```bash
# 将分层图片转换为PSD
python3 live2d_psd_converter.py <图片路径>
```

## 🎯 分层结构

工具会自动生成以下图层（符合Live2D标准）:

| 序号 | 图层名称 | 说明 | 像素数 |
|------|----------|------|--------|
| 1 | Body | 身体主要部分 | ~50,000+ |
| 2 | Clothes | 服装 | ~40,000+ |
| 3 | Eyes | 眼睛 | ~5,000+ |
| 4 | Face | 脸部皮肤 | ~15,000+ |
| 5 | Hair_Back | 头发后部 | ~30,000+ |
| 6 | Hair_Front | 刘海 | ~20,000+ |
| 7 | Hair_Side | 头发侧部 | ~25,000+ |
| 8 | Hands | 手部 | ~3,000+ |
| 9 | Mouth | 嘴巴 | ~2,000+ |

## 🔧 高级功能

### 使用特定AI模型

```python
from rembg import remove, new_session

# 使用特定模型
session = new_session("u2net_human_seg")
result = remove(input_data, session=session)

# 使用SAM模型
from segment_anything import sam_model_registry, SamPredictor
sam = sam_model_registry['vit_h'](checkpoint='~/.sam/sam_vit_h_4b8939.pth')
predictor = SamPredictor(sam)
```

### 批量处理

```python
import glob
from rembg import remove

for image_path in glob.glob('input/*.png'):
    with open(image_path, 'rb') as f:
        input_data = f.read()
    
    output_data = remove(input_data)
    
    output_path = f"output/{Path(image_path).name}"
    with open(output_path, 'wb') as f:
        f.write(output_data)
```

### 自定义分层规则

工具使用智能颜色分析和区域分割：

**头发颜色检测:**
- 粉/红色: RGB(100-255, 50-150, 50-150)
- 金色: RGB(150-255, 100-200, 50-150)
- 紫色: RGB(50-150, 30-100, 50-150)
- 蓝色: RGB(30-100, 30-100, 50-150)
- 灰色: RGB(50-200, 50-200, 50-200)
- 黑色: RGB(20-80, 10-50, 10-50)

**皮肤颜色检测:**
- RGB(180-255, 140-220, 120-200)
- R > G > B (红色通道最高)

## 📊 性能对比

| 方法 | 速度 | 精度 | 成本 | 适用场景 |
|------|------|------|------|----------|
| rembg (GPU) | 快 | 高 | 免费 | 背景移除 |
| SAM (GPU) | 快 | 很高 | 免费 | 精确分割 |
| Qwen-Image-Layered | 中 | 很高 | 免费 | 自动分层 |
| Photoshop AI | 快 | 高 | 订阅 | 专业设计 |

## 💡 最佳实践

### 1. 使用AI增强的分层

```bash
# 确保安装AI模型
python3 install_ai_models.py

# 使用rembg先移除背景
python3 -c "from rembg import remove; open('output.png', 'wb').write(remove(open('input.png', 'rb').read()))"

# 然后分层
python3 live2d_autolayer.py output.png
```

### 2. 处理复杂图像

对于复杂遮挡场景：
1. 先使用rembg移除背景
2. 使用SAM进行精确分割
3. 在Photoshop中手动调整

### 3. 提高分层精度

**上传到Qwen-Image-Layered:**
1. 访问: https://huggingface.co/spaces/Qwen/Qwen-Image-Layered
2. 上传图片
3. AI自动分层
4. 下载分层结果
5. 导入Live2D

## 🐛 故障排除

### 问题: rembg安装失败

```bash
# 解决方案1: CPU版本
pip install rembg

# 解决方案2: 手动安装依赖
pip install onnxruntime
pip install onnx
pip install rembg
```

### 问题: SAM模型下载慢

```bash
# 使用镜像
wget https://ghproxy.com/https://github.com/facebookresearch/segment-anything/blob/main/sam_vit_h_4b8939.pth -O ~/.sam/

# 或使用较小模型
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth -O ~/.sam/
```

### 问题: 分层不准确

**可能原因:**
1. 图像对比度低
2. 颜色与预设范围不符
3. 遮挡严重

**解决方案:**
1. 使用AI增强工具预处理
2. 上传到Qwen-Image-Layered在线处理
3. 在Photoshop中手动调整

## 📚 相关资源

- **Qwen-Image-Layered**: https://huggingface.co/spaces/Qwen/Qwen-Image-Layered
- **rembg文档**: https://github.com/danielgatis/rembg
- **SAM模型**: https://github.com/facebookresearch/segment-anything
- **Convertio PSD转换**: https://convertio.co/png-to-psd/

## 🔄 版本历史

### v3.0 (当前版本)
- ✅ 集成rembg AI模型
- ✅ 集成SAM分割模型
- ✅ 增强智能颜色分析
- ✅ 动漫风格优化
- ✅ 头发颜色多维度检测
- ✅ 边缘平滑处理

### v2.0
- ✅ 智能区域分割
- ✅ 多图层支持
- ✅ 自动命名

### v1.0
- ✅ 基础分层功能
- ✅ PSD导出

## 🤝 贡献

欢迎提交Issue和Pull Request!

## 📄 许可证

MIT License

---

**Live2D AI智能分层工具 v3.0** - 让分层更智能! 🎉
