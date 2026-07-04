# 📚 Live2D Master Agent - 开源项目研究与集成报告

## 📋 摘要

本文档研究并推荐了适合集成到 Live2D Master Agent 项目的开源方案，重点关注：
1. **图片生成质量提升**
2. **前后端连通性增强**
3. **与现有工具链的无缝整合**

---

## 🎯 一、推荐的开源方案

### 1.1 图片生成核心方案

#### 🥇 方案A：Stable Diffusion WebUI + API（推荐！）

**项目地址**: https://github.com/AUTOMATIC1111/stable-diffusion-webui

**优势**:
- ✅ 成熟稳定的开源项目，社区活跃
- ✅ 内置完整的 API（FastAPI 驱动）
- ✅ 支持海量扩展（ControlNet、LoRA 等）
- ✅ Python SDK 可用：`webuiapi`（pip install 即可）
- ✅ 支持本地部署，无网络依赖
- ✅ 模型丰富，易于定制动漫风格

**Python SDK**: https://pypi.org/project/webuiapi/

#### 🥈 方案B：ComfyUI + API

**项目地址**: https://github.com/comfyanonymous/ComfyUI

**优势**:
- ✅ 我们已经集成了 ComfyUI + See-through
- ✅ 完整的 API 支持
- ✅ 可以直接复用现有安装
- ✅ 有 Python 客户端库：`comfyapi`

**Python 客户端**: https://pypi.org/project/comfyapi/

#### 🥉 方案C：保留 Pollinations.ai 作为备用

**优势**:
- ✅ 无需本地安装
- ✅ 快速起步
- ✅ 完全免费

---

### 1.2 前后端连通工具

| 工具 | 语言 | 功能 | 适配方案 |
|------|------|------|---------|
| **webuiapi** | Python | Stable Diffusion WebUI API客户端 | 方案A |
| **comfyapi** | Python | ComfyUI API客户端 | 方案B |
| **FastAPI** | Python | API框架 | 自建后端 |
| **Gradio** | Python | WebUI框架 | 现有工具 |

---

## 🚀 二、推荐的集成架构

### 2.1 完整架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    Live2D Master Agent (v6.3+)              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │        🖼️ 多源图片生成引擎 (新增!)                  │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │  源1: Stable Diffusion WebUI (推荐优先级最高) │  │  │
│  │  │  源2: ComfyUI API                          │  │  │
│  │  │  源3: Pollinations.ai (备用)                │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                       ↓ (自动降级)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              🎨 图片质量处理层                      │  │
│  │  - 优化提示词、调整尺寸、添加水印等                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                       ↓                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           🛠️ 现有的工具链 (保持不变)                 │  │
│  │  - PSD 规划、分层工具、See-through 集成              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 💡 三、具体集成建议

### 3.1 阶段一：核心集成（优先级最高）

#### 目标：添加 Stable Diffusion WebUI 作为主要源

**新增文件：`sd_webui_integration.py`**

```python
#!/usr/bin/env python3
"""
Stable Diffusion WebUI 集成模块
提供高质量本地图片生成
"""

import requests
import base64
import json
from pathlib import Path
from typing import Optional, Dict, Any
from PIL import Image


class StableDiffusionWebUIClient:
    """SD WebUI API客户端"""
    
    def __init__(self, base_url="http://127.0.0.1:7860"):
        self.base_url = base_url
        self.txt2img_endpoint = f"{base_url}/sdapi/v1/txt2img"
        self.health_endpoint = f"{base_url}/sdapi/v1/health"
        self.headers = {"Content-Type": "application/json"}
    
    def is_available(self) -> bool:
        """检查服务是否可用"""
        try:
            response = requests.get(self.health_endpoint, timeout=3)
            return response.status_code == 200
        except:
            return False
    
    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 768,
        height: int = 768,
        steps: int = 30,
        sampler_name: str = "DPM++ 2M Karras",
        cfg_scale: float = 7.5,
        seed: int = -1
    ) -> Dict[str, Any]:
        """
        生成图片
        
        Args:
            prompt: 正向提示词
            negative_prompt: 反向提示词
            width: 宽度
            height: 高度
            steps: 步数
            sampler_name: 采样器
            cfg_scale: 提示词引导强度
            seed: 随机种子 (-1表示随机)
            
        Returns:
            包含生成状态的字典
        """
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "steps": steps,
            "sampler_name": sampler_name,
            "cfg_scale": cfg_scale,
            "seed": seed,
            "batch_size": 1,
            "n_iter": 1
        }
        
        try:
            response = requests.post(
                self.txt2img_endpoint,
                headers=self.headers,
                json=payload,
                timeout=300
            )
            response.raise_for_status()
            data = response.json()
            
            if "images" in data and len(data["images"]) > 0:
                return {
                    "status": "success",
                    "images": data["images"],
                    "parameters": data.get("parameters", {}),
                    "info": data.get("info", "")
                }
            else:
                return {
                    "status": "error",
                    "message": "No images returned from API"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"API request failed: {e}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {e}"
            }
    
    def save_image_from_base64(self, base64_data: str, output_path: Path) -> bool:
        """从Base64数据保存图片"""
        try:
            image_bytes = base64.b64decode(base64_data)
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            return True
        except Exception as e:
            print(f"保存图片失败: {e}")
            return False


def get_negative_prompt_for_live2d() -> str:
    """
    获取Live2D优化的反向提示词
    避免生成低质量、不适合分层的图片
    """
    return (
        "blurry, low quality, low resolution, pixelated, noisy, grainy, "
        "distorted, deformed, bad anatomy, bad hands, bad face, bad eyes, "
        "extra fingers, missing fingers, fused fingers, too many fingers, "
        "bad proportions, extra limbs, long neck, bad feet, bad ears, "
        "ugly, disgusting, horror, watermark, text, signature, logo, "
        "simple background, messy hair, messy clothes, complex background, "
        "photorealistic, realistic, 3d, ugly eyes, deformed eyes, closed eyes"
    )


def optimize_prompt_for_live2d(prompt: str) -> str:
    """
    优化提示词以适合Live2D制作
    添加动漫风格、清晰轮廓等关键词
    """
    prefix = (
        "masterpiece, best quality, high quality, "
        "anime style, anime girl, clean lineart, clear edges, "
        "simple background, white background, isolated character, "
        "perfect for Live2D rigging, distinct color separation, "
    )
    return prefix + prompt
```

---

### 3.2 阶段二：整合到主工具

**修改文件：`master_tool.py`（升级为 v6.3）**

新增内容：

```python
# 在导入部分添加
from sd_webui_integration import (
    StableDiffusionWebUIClient,
    get_negative_prompt_for_live2d,
    optimize_prompt_for_live2d
)

# 在 generate_image 函数内，添加 SD WebUI 源
def generate_image(prompt, output_dir, seed=None, width=768, height=768):
    """
    生成图片（多源智能选择）
    优先级：SD WebUI > ComfyUI > Pollinations
    """
    
    # 源1：尝试 Stable Diffusion WebUI
    print("🔄 尝试 Stable Diffusion WebUI (本地)...")
    sd_client = StableDiffusionWebUIClient()
    
    if sd_client.is_available():
        optimized_prompt = optimize_prompt_for_live2d(prompt)
        negative_prompt = get_negative_prompt_for_live2d()
        
        result = sd_client.generate_image(
            optimized_prompt,
            negative_prompt,
            width=width,
            height=height,
            seed=seed
        )
        
        if result["status"] == "success":
            output_file = output_dir / f"live2d_sd_{int(time.time())}_{seed}.png"
            if sd_client.save_image_from_base64(result["images"][0], output_file):
                print(f"✅ 成功！使用 Stable Diffusion WebUI")
                return str(output_file), seed
    
    # 源2：尝试现有 Pollinations（降级方案）
    print("⚠️ SD WebUI 不可用，降级到 Pollinations.ai...")
    
    # ... 现有的 Pollinations 逻辑 ...
```

---

### 3.3 阶段三：SD WebUI 自动安装（可选）

**新增文件：`install_sd_webui.py`**

提供一键安装脚本。

---

## 📦 四、快速开始（集成后）

### 4.1 配置 SD WebUI（可选但推荐）

```bash
# 1. 安装 Stable Diffusion WebUI
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
cd stable-diffusion-webui
pip install -r requirements.txt

# 2. 下载动漫风格模型（推荐）
# 从 Civitai 或 Hugging Face 下载
# 放到 models/Stable-diffusion/ 目录

# 3. 启动 API 服务
python launch.py --api --listen

# 4. 运行我们的工具
cd /workspace/.trae/skills/live2d-master-agent
python master_tool.py "cute anime girl with pink hair"
```

### 4.2 使用 webuiapi SDK（更高级用法）

```bash
pip install webuiapi
```

```python
import webuiapi

# 创建客户端
api = webuiapi.WebUIApi()

# 简单示例
result = api.txt2img(
    prompt="cute anime girl, masterpiece, best quality",
    negative_prompt="blurry, low quality",
    width=768,
    height=768,
    steps=30
)

# 保存
result.image.save("output.png")
```

---

## 🎨 五、推荐的模型

为了获得最好的 Live2D 制作效果，推荐以下模型：

| 模型 | 风格 | 来源 | 质量 |
|------|------|------|------|
| **Anything v5** | 动漫通用 | Civitai | ⭐⭐⭐⭐⭐ |
| **Counterfeit v3** | 动漫 | Civitai | ⭐⭐⭐⭐⭐ |
| **GhostMix v2** | 动漫女生 | Civitai | ⭐⭐⭐⭐ |
| **DreamShaper v8** | 通用 | Civitai | ⭐⭐⭐⭐ |
| **Pastel Mix** | 柔和风格 | Civitai | ⭐⭐⭐⭐ |

---

## 🔗 六、项目文件变更清单

### 新增文件（预计）

- 📄 `sd_webui_integration.py` - SD WebUI 集成模块
- 📄 `install_sd_webui.py` - SD WebUI 安装脚本（可选）
- 📄 `OPENSOURCE_INTEGRATION.md` - 本文档（已创建）

### 修改文件（预计）

- 📄 `master_tool.py` - 升级为多源引擎
- 📄 `README.md` - 更新文档
- 📄 `requirements.txt` - 添加 `webuiapi` 或 `requests`
- 📄 `CHANGELOG.md` - 记录变更

---

## 📋 七、总结与建议

### 7.1 优先级排序

| 优先级 | 功能 | 开发时间 | 复杂度 |
|--------|------|---------|--------|
| 🔥P0 | 集成 SD WebUI 作为主要源 | 1-2天 | 中 |
| 🚀P1 | 添加提示词优化层 | 0.5天 | 低 |
| 🎨P2 | SD WebUI 自动安装 | 1天 | 中 |
| 📦P3 | ComfyUI API 深度集成 | 1-2天 | 中 |

### 7.2 建议方案

**推荐方案**：
1. **第一步**：添加 SD WebUI 支持（使用原生 requests，无需额外依赖）
2. **第二步**：优化提示词，确保生成质量
3. **第三步**：保留现有 Pollinations 作为降级方案
4. **第四步**：添加 See-through 自动调用（可选）

这样用户可以：
- 在有 SD WebUI 时获得最高质量
- 没有 SD WebUI 时用 Pollinations 快速上手
- 工具链完全打通！

---

## 📚 参考资源

| 资源 | 链接 |
|------|------|
| Stable Diffusion WebUI | https://github.com/AUTOMATIC1111/stable-diffusion-webui |
| webuiapi Python SDK | https://pypi.org/project/webuiapi/ |
| ComfyUI API 文档 | https://docs.comfyui.org/ |
| Civitai (模型下载) | https://civitai.com/ |
| 本项目 GitHub | https://github.com/mw2wbyys6t-sudo/Live2D |

---

**文档版本**: v1.0  
**最后更新**: 2026-05-29  
**作者**: Live2D Master Agent 团队
