# Live2D Master Agent - ComfyUI 配置

## 🚀 快速开始

### 系统要求

- Python 3.10+
- Git
- NVIDIA GPU (推荐，用于加速生成)
- 至少 8GB 显存 (推荐)

### Windows 启动

```bash
# 方法1: 双击运行
start_comfyui.bat

# 方法2: 命令行
cd Live2D-ComfyUI
start_comfyui.bat
```

### Linux/macOS 启动

```bash
# 添加执行权限（首次）
chmod +x start_comfyui.sh

# 启动
./start_comfyui.sh
```

启动后，在浏览器访问: http://127.0.0.1:8188

## 📥 安装模型

### 必需步骤

1. 访问 CivitAI: https://civitai.com/
2. 注册账号（免费）
3. 下载推荐模型:
   - **AnythingV5**: https://civitai.com/models/9409 (动漫风格)
   - **CounterfeitV3**: https://civitai.com/models/4468 (高质量)
   - **PastelMix**: https://civitai.com/models/39759 (柔和色调)
4. 将模型文件 (.safetensors 或 .ckpt) 放到:
   ```
   ComfyUI/models/checkpoints/
   ```

### 模型文件命名

下载后，文件应该类似:
- `anything-v5.safetensors`
- `counterfeitV3.safetensors`
- `PastelMixAnim_fix.safetensors`

## 🎨 使用方法

### 方式 1: Web 界面（推荐新手）

1. 启动 ComfyUI
2. 打开浏览器 http://127.0.0.1:8188
3. 使用默认工作流或导入自定义工作流
4. 输入提示词生成图片

### 方式 2: 命令行集成

```bash
cd /workspace/.trae/skills/live2d-master-agent

# 使用交互模式
python comfyui_integration.py

# 使用预设生成
python comfyui_integration.py --preset "Cute Kawaii"
```

### Live2D 专用提示词

查看 `prompts.txt` 获取 Live2D 专用提示词模板，包括:
- 基础模板
- 动漫角色模板
- 负向提示词

## 🖥️ GPU vs CPU 模式

### GPU 模式（推荐）

- 需要 NVIDIA GPU
- 显存建议: 8GB+
- 生成速度快 (几秒到几十秒)

### CPU 模式（备用）

- 无 GPU 时可用
- 生成速度慢 (几分钟到几十分钟)
- 使用 `--cpu-vae` 参数启动

启动脚本会自动检测并选择合适的模式。

## ⚠️ 常见问题

### Q1: 启动失败？

**A**: 检查:
1. Python 和 Git 是否安装: `python --version && git --version`
2. 虚拟环境是否激活
3. 端口 8188 是否被占用

### Q2: 生成速度慢？

**A**: 
- 确保使用 NVIDIA GPU
- 减少生成步骤 (steps: 20-25)
- 使用较小的分辨率

### Q3: 模型加载失败？

**A**: 
1. 确保模型文件在正确目录
2. 检查文件完整性
3. 重启 ComfyUI

### Q4: 显存不足？

**A**: 
- 降低分辨率
- 减少 batch size
- 使用更小的模型

## 📚 相关资源

- [ComfyUI 官方文档](https://github.com/comfyanonymous/ComfyUI)
- [CivitAI 模型下载](https://civitai.com/)
- [Live2D Cubism](https://www.live2d.com/)

## 🔗 与 Live2D Master Agent 集成

安装 ComfyUI 后，可以获得最高质量的图像生成:

```bash
cd /workspace/.trae/skills/live2d-master-agent

# 生成图片
python comfyui_integration.py

# 然后进行 PSD 分层和质量检查
python scripts/qa_engine_enhanced.py

# 设计参数
python scripts/parameter_designer_enhanced.py
```

## 📝 技术细节

- **安装位置**: `Live2D-ComfyUI/`
- **ComfyUI 主目录**: `Live2D-ComfyUI/ComfyUI/`
- **虚拟环境**: `Live2D-ComfyUI/ComfyUI/venv/`
- **模型目录**: `Live2D-ComfyUI/ComfyUI/models/checkpoints/`
- **默认端口**: 8188

---

**版本**: 1.0  
**更新**: 2026-05-21
