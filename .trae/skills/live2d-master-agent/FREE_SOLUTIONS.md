# 免费图像生成方案

## ⚠️ 如果在线服务无法使用

### 方案 1: 访问网页版（推荐）

如果命令行工具无法使用，可以直接访问网页：

1. **Pollinations.ai** (推荐)
   - 网址: https://pollinations.ai
   - 完全免费，无需注册
   - 支持中文

2. **Hugging Face Spaces**
   - 网址: https://huggingface.co/spaces
   - 搜索 "Stable Diffusion" 或 "Anime"
   - 多个免费模型可选

3. **Civitai**
   - 网址: https://civitai.com
   - 需要注册（免费）
   - 海量模型下载

4. **Stable Diffusion WebUI**
   - 网址: https://webui.direct/
   - 无需安装，直接使用
   - 支持多种模型

---

### 方案 2: 本地生成

#### 2.1 使用本地 diffusers

```bash
cd /workspace/.trae/skills/live2d-master-agent
python local_generator.py
```

首次运行会自动安装依赖。

#### 2.2 安装 Stable Diffusion WebUI

Windows:
```bash
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui
webui-user.bat
```

Linux/macOS:
```bash
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui
./webui.sh
```

---

### 方案 3: 使用 ComfyUI

如果你已经安装了 ComfyUI：

```bash
cd /workspace/.trae/skills/live2d-master-agent/Live2D-ComfyUI
./start_comfyui.sh  # Linux/macOS
start_comfyui.bat     # Windows
```

然后访问 http://127.0.0.1:8188

---

### 方案 4: 配置 API（可选）

如果你有火山引擎 API Key：

```bash
cd /workspace/.trae/skills/live2d-master-agent
python config_api.py
```

---

## 📋 提示词模板

### Live2D 专用提示词

```
正面提示词:
anime girl, [颜色] hair, [服装], perfect for Live2D rigging, 
clean layer separation, isolated character on white background, 
sharp clean lines, vibrant colors, ultra detailed, masterpiece

负面提示词:
blurry, low quality, deformed, bad anatomy, bad hands, 
extra fingers, missing fingers, watermark, text
```

### 推荐参数

| 参数 | 值 | 说明 |
|------|------|------|
| Width | 1024 | 宽度 |
| Height | 1024/1280 | 高度 |
| Steps | 20-30 | 生成步数 |
| CFG Scale | 7-9 | 引导强度 |

---

## 🔧 常见问题

### Q1: Pollinations.ai 无法访问？

**A**: 
1. 检查网络连接
2. 使用 VPN
3. 直接访问网页版 https://pollinations.ai
4. 使用其他在线工具

### Q2: Hugging Face 模型加载慢？

**A**: 
1. 首次加载需要下载模型（约 4GB）
2. 可以使用国内镜像
3. 或者使用网页版

### Q3: 本地生成太慢？

**A**:
1. 确保使用 GPU
2. 减少 Steps (20-25)
3. 使用更小的分辨率
4. 使用量化模型

### Q4: 内存不足？

**A**:
1. 关闭其他程序
2. 使用更小的批次大小
3. 使用 float32 而不是 float16
4. 增加虚拟内存

---

## 📚 相关资源

- [Pollinations.ai](https://pollinations.ai) - 免费在线生成
- [Hugging Face](https://huggingface.co) - 模型库
- [Civitai](https://civitai.com) - 模型分享
- [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) - 本地部署
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - 节点式工作流

---

**版本**: 1.0  
**更新**: 2026-05-21
