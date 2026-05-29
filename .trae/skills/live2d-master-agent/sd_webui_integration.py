#!/usr/bin/env python3
"""
Stable Diffusion WebUI 集成模块
提供高质量本地图片生成，与 Live2D Master Agent 完美兼容

功能特性：
- 🔄 自动检测 SD WebUI 服务可用性
- 🎨 内置 Live2D 优化的提示词
- 📦 支持多种尺寸
- 🛡️ 完整的错误处理
"""

import requests
import base64
import json
import random
import time
from pathlib import Path
from typing import Optional, Dict, Any, Tuple


class StableDiffusionWebUIClient:
    """Stable Diffusion WebUI API 客户端"""

    def __init__(self, base_url="http://127.0.0.1:7860", timeout=300):
        """
        初始化客户端

        Args:
            base_url: SD WebUI 服务地址
            timeout: 请求超时时间（秒）
        """
        self.base_url = base_url.rstrip("/")
        self.txt2img_endpoint = f"{self.base_url}/sdapi/v1/txt2img"
        self.health_endpoint = f"{self.base_url}/sdapi/v1/health"
        self.headers = {"Content-Type": "application/json"}
        self.timeout = timeout
        self.available = None

    def is_available(self, force_check=False) -> bool:
        """
        检查 SD WebUI 服务是否可用

        Args:
            force_check: 是否强制检查（忽略缓存）

        Returns:
            服务是否可用
        """
        if self.available is not None and not force_check:
            return self.available

        try:
            print(f"🔍 检查 SD WebUI 服务状态: {self.base_url}")
            response = requests.get(self.health_endpoint, timeout=5)
            self.available = response.status_code == 200
            if self.available:
                print("✅ SD WebUI 服务可用！")
            else:
                print("⚠️ SD WebUI 服务响应异常")
            return self.available
        except requests.exceptions.RequestException as e:
            print(f"❌ SD WebUI 服务不可用: {e}")
            self.available = False
            return False
        except Exception as e:
            print(f"❌ 检查服务状态时出错: {e}")
            self.available = False
            return False

    def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 768,
        height: int = 768,
        steps: int = 30,
        sampler_name: str = "DPM++ 2M Karras",
        cfg_scale: float = 7.5,
        seed: int = -1,
        auto_negative_prompt: bool = True
    ) -> Dict[str, Any]:
        """
        生成图片

        Args:
            prompt: 正向提示词
            negative_prompt: 反向提示词（如果为 None，会自动使用 Live2D 优化版本）
            width: 图片宽度
            height: 图片高度
            steps: 采样步数
            sampler_name: 采样器名称
            cfg_scale: 提示词引导强度
            seed: 随机种子（-1 表示随机）
            auto_negative_prompt: 是否自动使用优化的反向提示词

        Returns:
            包含生成状态的字典
        """
        if seed == -1:
            seed = random.randint(0, 999999999)

        if negative_prompt is None and auto_negative_prompt:
            negative_prompt = get_negative_prompt_for_live2d()

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
            "n_iter": 1,
            "send_images": True,
            "save_images": False
        }

        print(f"🎨 开始生成图片 (SD WebUI)...")
        print(f"   尺寸: {width}x{height}")
        print(f"   步数: {steps}")
        print(f"   种子: {seed}")

        try:
            response = requests.post(
                self.txt2img_endpoint,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()

            if "images" in data and len(data["images"]) > 0:
                print("✅ 图片生成成功！")
                return {
                    "status": "success",
                    "images": data["images"],
                    "parameters": data.get("parameters", {}),
                    "info": data.get("info", ""),
                    "seed": seed
                }
            else:
                print("❌ API 返回为空")
                return {
                    "status": "error",
                    "message": "No images returned from API"
                }

        except requests.exceptions.Timeout:
            print("❌ 生成超时（请检查 GPU 是否正在运行）")
            return {
                "status": "error",
                "message": "Generation timeout - check your GPU"
            }
        except requests.exceptions.RequestException as e:
            print(f"❌ API 请求失败: {e}")
            return {
                "status": "error",
                "message": f"API request failed: {e}"
            }
        except Exception as e:
            print(f"❌ 生成图片时出错: {e}")
            return {
                "status": "error",
                "message": f"Unexpected error: {e}"
            }

    def save_image_from_base64(self, base64_data: str, output_path: Path) -> bool:
        """
        从 Base64 数据保存图片

        Args:
            base64_data: Base64 编码的图片数据
            output_path: 输出路径

        Returns:
            是否成功
        """
        try:
            image_bytes = base64.b64decode(base64_data)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            print(f"💾 图片已保存: {output_path}")
            return True
        except Exception as e:
            print(f"❌ 保存图片失败: {e}")
            return False


def get_negative_prompt_for_live2d() -> str:
    """
    获取 Live2D 优化的反向提示词

    避免生成低质量、不适合分层的图片
    """
    return (
        "blurry, low quality, low resolution, pixelated, noisy, grainy, "
        "distorted, deformed, bad anatomy, bad hands, bad face, bad eyes, "
        "extra fingers, missing fingers, fused fingers, too many fingers, "
        "bad proportions, extra limbs, long neck, bad feet, bad ears, "
        "ugly, disgusting, horror, watermark, text, signature, logo, "
        "simple background, messy hair, messy clothes, complex background, "
        "photorealistic, realistic, 3d, ugly eyes, deformed eyes, closed eyes, "
        "depth of field, blurry background, multiple girls, multiple people"
    )


def optimize_prompt_for_live2d(prompt: str) -> str:
    """
    优化提示词以适合 Live2D 制作

    添加动漫风格、清晰轮廓等关键词
    """
    live2d_prefix = (
        "masterpiece, best quality, high quality, extremely detailed, "
        "anime style, anime girl, solo, 1girl, clean lineart, clear edges, "
        "simple background, white background, isolated character, "
        "perfect for Live2D rigging, distinct color separation, "
        "clean colors, sharp lines, cel shading, "
    )

    # 检查用户是否已经提供了风格相关的关键词
    keywords_to_check = ["anime", "masterpiece", "best quality"]
    has_style = any(k in prompt.lower() for k in keywords_to_check)

    if has_style:
        # 用户已经提供了风格，只添加 Live2D 优化
        return (
            prompt + ", clean lineart, clear edges, "
            "perfect for Live2D rigging, distinct color separation"
        )
    else:
        # 添加完整的优化关键词
        return live2d_prefix + prompt


def get_default_samplers() -> list:
    """获取推荐的采样器列表"""
    return [
        "DPM++ 2M Karras",
        "DPM++ SDE Karras",
        "Euler a",
        "Euler",
        "Heun",
        "DPM2 a Karras"
    ]


def main():
    """演示函数"""
    print("=" * 60)
    print("🎨 Stable Diffusion WebUI 集成测试")
    print("=" * 60)

    # 检查服务
    client = StableDiffusionWebUIClient()
    if not client.is_available():
        print("\n❌ SD WebUI 服务不可用")
        print("请先运行: python launch.py --api --listen")
        print("\n或者跳过，继续使用 Pollinations.ai")
        return

    # 生成测试图片
    print("\n" + "=" * 60)
    print("🖼️  测试图片生成")
    print("=" * 60)

    test_prompt = "cute anime girl with pink hair, blue eyes, school uniform, smiling"
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    result = client.generate_image(
        prompt=optimize_prompt_for_live2d(test_prompt),
        width=768,
        height=768,
        steps=25
    )

    if result["status"] == "success":
        output_path = output_dir / f"sd_test_{int(time.time())}.png"
        if client.save_image_from_base64(result["images"][0], output_path):
            print("\n✅ 测试成功！")
            print(f"   输出文件: {output_path}")
    else:
        print(f"\n❌ 测试失败: {result.get('message', 'Unknown error')}")


if __name__ == "__main__":
    main()
