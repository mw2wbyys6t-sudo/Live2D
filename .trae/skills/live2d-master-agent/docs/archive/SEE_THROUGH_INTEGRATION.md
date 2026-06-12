# 🎯 See-through 完整集成指南

**SIGGRAPH 2026级别AI分层工具 - 真正的解决方案**

---

## 📋 目录

1. [什么是See-through？](#什么是see-through)
2. [为什么选择See-through？](#为什么选择see-through)
3. [安装方法](#安装方法)
4. [使用方法](#使用方法)
5. [工作流程](#工作流程)
6. [常见问题](#常见问题)

---

## 🎓 什么是See-through？

### 项目信息
- **论文**: [See-through: Single-image Layer Decomposition for Anime Characters](https://arxiv.org/abs/2602.03749)
- **GitHub**: [shitagaki-lab/see-through](https://github.com/shitagaki-lab/see-through)
- **ComfyUI版本**: [ComfyUI-See-through](https://github.com/jtydhr88/ComfyUI-See-through)
- **学术认证**: **SIGGRAPH 2026** (计算机图形学顶级会议)

### 核心功能

See-through是一个**专为动漫角色设计**的AI分层工具，能够：

```
✅ 将单个动漫角色图像分解为多个可编辑图层
✅ 自动理解语义（头发、眼睛、衣服、配饰）
✅ 处理透明度和遮挡关系
✅ 智能推断隐藏内容
✅ 正确的深度排序
✅ 直接导出PSD文件
```

### 技术原理

See-through使用**两个AI模型**：

#### 1. LayerDiff 3D (SDXL-based)
```
作用: 合成透明、修复后的图层
输出: 语义分组的Alpha通道图层
模型: layerdifforg/seethroughv0.0.2_layerdiff3d
```

#### 2. Marigold Depth
```
作用: 深度估计
功能: 推断相对深度，引导绘制顺序
模型: 24yearsold/seethroughv0.0.1_marigold
```

---

## 🎯 为什么选择See-through？

### 对比分析

| 特性 | 我们的简单工具 | See-through |
|------|--------------|-------------|
| **技术基础** | 颜色检测/K-means | 深度学习（LayerDiff 3D） |
| **学术认证** | 无 | SIGGRAPH 2026 ⭐ |
| **语义理解** | ❌ 无 | ✅ 完整 |
| **透明度处理** | ⚠️ 简单 | ✅ 智能修复 |
| **深度排序** | ⚠️ 硬编码 | ✅ AI推断 |
| **输出质量** | ⚠️ 较差 | ✅ 学术级 |
| **动漫优化** | ❌ 通用 | ✅ 专为动漫 |

### 真实效果对比

**我们的工具（v5.0/v6.0）**:
```bash
# 输入: 动漫角色图片
# 输出: 
- 可能完全错误的图层分配
- 边缘不清晰
- 眼睛、嘴巴识别错误
- 需要大量手动修正
```

**See-through**:
```bash
# 输入: 动漫角色图片
# 输出:
- 正确的语义分层
- 清晰的边缘
- 正确的遮挡关系
- 基本可直接使用
```

---

## 📦 安装方法

### 方法1: ComfyUI完整安装（推荐）⭐⭐⭐⭐⭐

#### 步骤1: 安装ComfyUI

**Windows用户**:
```bash
# 1. 下载ComfyUI便携版
# 访问: https://github.com/comfyanonymous/ComfyUI/releases
# 下载: ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z

# 2. 解压到任意目录（路径不要有中文）

# 3. 运行
cd ComfyUI
run_nvidia_gpu.bat  # 如果有NVIDIA显卡
# 或
run_cpu.bat  # 仅CPU运行（较慢）
```

**Linux/macOS用户**:
```bash
# 1. 克隆仓库
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装PyTorch（根据你的CUDA版本）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 4. 启动
python main.py
```

#### 步骤2: 安装ComfyUI-See-through插件

```bash
# 进入ComfyUI目录
cd ComfyUI/custom_nodes

# 克隆插件
git clone https://github.com/jtydhr88/ComfyUI-See-through.git

# 安装依赖
cd ComfyUI-See-through
pip install -r requirements.txt
```

#### 步骤3: 下载AI模型

模型会自动下载，但如果你想手动下载：

```bash
# 创建模型目录
mkdir -p ComfyUI/models/diffusers

# LayerDiff 3D模型
# 下载: https://huggingface.co/layerdifforg/seethroughv0.0.2_layerdiff3d
# 放入: ComfyUI/models/diffusers/

# Marigold Depth模型
# 下载: https://huggingface.co/24yearsold/seethroughv0.0.1_marigold
# 放入: ComfyUI/models/marigold/
```

#### 步骤4: 加载工作流

1. 打开浏览器访问: http://127.0.0.1:8188
2. 点击"Load"按钮
3. 加载 See-through 工作流JSON文件
4. 或访问: https://www.runcomfy.com/comfyui-workflows/see-through-workflow-in-comfyui-anime-layer-decomposition-psd

---

### 方法2: 官方原版安装（需要Linux）

如果你有Linux系统或愿意配置：

```bash
# 克隆官方仓库
git clone https://github.com/shitagaki-lab/see-through.git
cd see-through

# 安装依赖
pip install -r requirements.txt

# 下载预训练模型
# (参考官方README)

# 运行
python inference.py --input your_image.png
```

---

## 📖 使用方法

### 基本工作流程

#### 1. 准备输入图片

**推荐规格**:
```
✅ 正面角色图片
✅ 清晰的边界
✅ 最少重叠元素
✅ 建议分辨率: 1024x1024 或更高
✅ PNG格式（支持透明）
```

**避免**:
```
❌ 群像图片
❌ 复杂背景
❌ 过多装饰
❌ 模糊图片
```

#### 2. 在ComfyUI中加载图片

1. 找到 `LoadImage` 节点
2. 点击并选择你的动漫角色图片
3. 图片会传递到See-through节点

#### 3. 生成图层

1. 点击 `SeeThrough_GenerateLayers` 节点
2. 设置参数:
   - **Resolution**: 处理分辨率（越高越慢）
   - **Denoising Steps**: 去噪步数（建议20-30）
   - **Seed**: 随机种子（可复现）

3. 点击 `Queue Prompt` 运行

#### 4. 生成深度图

1. 点击 `SeeThrough_GenerateDepth` 节点
2. 等待深度估计完成
3. 深度图用于分层排序

#### 5. 后处理

1. 点击 `SeeThrough_PostProcess` 节点
2. 系统会:
   - 组合图层
   - 分配名称
   - 排序
   - 导出PSD

#### 6. 导出PSD

1. 找到 `SavePSD` 节点
2. 选择保存位置
3. PSD文件可直接导入Live2D Cubism

---

## 🔄 工作流程

### 推荐完整流程

```
┌─────────────────────────────────────┐
│ 1. 使用本项目生成角色立绘            │
│    python master_tool.py "描述"      │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ 2. 准备图片                          │
│    • 确保正面角色                    │
│    • 清晰的边界                      │
│    • 最少装饰                        │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ 3. See-through分层（最高质量）        │
│    • 加载到ComfyUI                  │
│    • 生成语义图层                    │
│    • 生成深度图                      │
│    • 后处理                          │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ 4. 手动微调（如果需要）             │
│    • Photoshop打开PSD                │
│    • 微调边缘                        │
│    • 修正细节                        │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ 5. 导入Live2D Cubism                │
│    • File → Import PSD              │
│    • 创建部件                        │
│    • 设置参数                        │
│    • 完成Rigging                     │
└─────────────────────────────────────┘
```

### 备选工作流

如果你不想安装ComfyUI：

```
┌─────────────────────────────────────┐
│ 方案A: Live2D官方插件               │
│   • 需要Cubism Editor许可证         │
│   • Photoshop插件                   │
│   • 官方支持                        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 方案B: 我们的简单工具                │
│   • v5.0/v6.0                      │
│   • 作为起点                        │
│   • 需要大量手动修正                │
└─────────────────────────────────────┘
```

---

## ❓ 常见问题

### Q1: See-through需要什么硬件？

**A**:
```
推荐配置:
- NVIDIA显卡（RTX 3060或更高）
- 8GB+ VRAM
- 16GB+ RAM
- 20GB+ 磁盘空间

最低配置:
- CPU模式可以运行
- 但速度会很慢（几分钟 vs 几秒）
```

### Q2: 模型下载失败怎么办？

**A**:
```bash
# 手动下载模型
# LayerDiff 3D:
https://huggingface.co/layerdifforg/seethroughv0.0.2_layerdiff3d/tree/main

# Marigold:
https://huggingface.co/24yearsold/seethroughv0.0.1_marigold/tree/main

# 放入对应目录后重新运行
```

### Q3: 输出质量不好怎么办？

**A**: 尝试以下方法:
1. ✅ 使用更高分辨率的输入图片
2. ✅ 增加去噪步数
3. ✅ 使用正面角色图片
4. ✅ 减少图片中的装饰元素
5. ✅ 确保角色边界清晰

### Q4: 如何加速处理？

**A**:
1. ✅ 使用GPU而非CPU
2. ✅ 降低处理分辨率（会牺牲质量）
3. ✅ 减少去噪步数（会牺牲质量）
4. ✅ 只处理关键图层

### Q5: PSD无法导入Live2D？

**A**:
1. ✅ 确保使用RGB颜色模式
2. ✅ 确保图层命名符合Live2D规范
3. ✅ 尝试重新导出
4. ✅ 检查图层是否有透明度

---

## 🎯 最佳实践

### 1. 输入图片准备

**最佳选择**:
```bash
✅ 单个正面角色
✅ 白色或透明背景
✅ 清晰的轮廓线
✅ 最少配饰
✅ 1024x1024或更高分辨率
✅ PNG格式
```

**避免**:
```bash
❌ 群像
❌ 复杂背景
❌ 模糊
❌ 过多装饰
❌ 低分辨率
```

### 2. 参数设置

**高质量设置**:
```python
resolution = 1024  # 或更高
denoising_steps = 25-30
seed = 固定值  # 可复现
```

**快速设置**:
```python
resolution = 512
denoising_steps = 15-20
```

### 3. 后处理

**必要步骤**:
1. 检查边缘质量
2. 修正明显的错误
3. 确保透明度正确
4. 验证图层顺序

---

## 📚 参考资源

### 官方资源
1. **See-through论文**: https://arxiv.org/abs/2602.03749
2. **GitHub仓库**: https://github.com/shitagaki-lab/see-through
3. **ComfyUI插件**: https://github.com/jtydhr88/ComfyUI-See-through
4. **ComfyUI**: https://github.com/comfyanonymous/ComfyUI

### 模型资源
1. **LayerDiff 3D**: https://huggingface.co/layerdifforg/seethroughv0.0.2_layerdiff3d
2. **Marigold**: https://huggingface.co/24yearsold/seethroughv0.0.1_marigold

### 工作流示例
1. **RunComfy**: https://www.runcomfy.com/comfyui-workflows/see-through-workflow-in-comfyui-anime-layer-decomposition-psd

### 教程资源
1. **日文教程**: https://onlinegamernikki.com/live2d-auto-layering-tool
2. **B站视频**: https://www.bilibili.com/video/BV1UvyqBFEBF (Live2D官方)

---

## 🎉 总结

### See-through优势

```
✅ SIGGRAPH 2026学术认证
✅ 专为动漫角色设计
✅ 深度语义理解
✅ 智能透明度处理
✅ 正确的深度排序
✅ 直接导出PSD
```

### 我们的项目定位

```
✅ 图像生成: 做得很好（免费、快速）
⚠️ 自动分层: 辅助工具（需要AI加持）
🎯 最终方案: See-through + 我们的工具
```

### 下一步行动

1. **立即**: 安装ComfyUI + See-through
2. **使用**: 按照本指南操作
3. **体验**: SIGGRAPH级别的分层效果
4. **反馈**: 帮助改进我们的项目

---

**让AI分层变得真正可用！** 🎨

---

*最后更新：2026-05-25*
*版本：v5.0*
