#!/usr/bin/env python3
"""
Live2D Master Agent - 本地图像生成器
基于 Stable Diffusion + diffusers 的纯本地图像生成工具

特点：
- 🎯 完全本地运行，无需网络
- 🚀 支持 CPU 推理（无需 GPU）
- 🎨 针对动漫风格优化
- 💾 自动下载和管理模型
- ⚡ 支持模型量化加速

使用方法：
    python local_image_generator.py "cute anime girl"
    python local_image_generator.py --model "Linaqruf/anything-v3.0" "beautiful anime character"
    python local_image_generator.py --steps 30 --width 512 --height 768 "idol girl"
"""

import os
import sys
import time
import argparse
import warnings
from pathlib import Path
from typing import Optional, Tuple

# 忽略不必要的警告
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class LocalImageGenerator:
    """本地图像生成器"""

    # 推荐的动漫风格模型
    RECOMMENDED_MODELS = {
        "anything-v3": {
            "id": "Linaqruf/anything-v3.0",
            "desc": "Anything V3 - 通用动漫风格",
            "size": "约 4GB",
        },
        "anything-v5": {
            "id": "stablediffusionapi/anything-v5",
            "desc": "Anything V5 - 高质量动漫",
            "size": "约 4GB",
        },
        "counterfeit-v3": {
            "id": "gsdf/Counterfeit-V3.0",
            "desc": "Counterfeit V3 - 细腻画风",
            "size": "约 4GB",
        },
        "meinaMix": {
            "id": "Meina/MeinaMix",
            "desc": "MeinaMix - 萌系风格",
            "size": "约 4GB",
        },
        "pastel-mix": {
            "id": "andite/pastel-mix",
            "desc": "Pastel Mix - 柔和色彩",
            "size": "约 4GB",
        },
        "sd-1.5": {
            "id": "runwayml/stable-diffusion-v1-5",
            "desc": "Stable Diffusion 1.5 - 官方基础模型",
            "size": "约 4GB",
        },
    }

    def __init__(
        self,
        model_id: str = "Linaqruf/anything-v3.0",
        device: str = "auto",
        cache_dir: Optional[str] = None,
    ):
        """
        初始化生成器

        Args:
            model_id: HuggingFace 模型 ID
            device: 运行设备 (auto/cpu/cuda/mps)
            cache_dir: 模型缓存目录
        """
        self.model_id = model_id
        self.device = self._get_device(device)
        self.cache_dir = cache_dir or self._get_default_cache_dir()
        self.pipe = None
        self.model_loaded = False

        print(f"🎯 本地图像生成器初始化")
        print(f"   模型: {model_id}")
        print(f"   设备: {self.device}")
        print(f"   缓存: {self.cache_dir}")

    def _get_device(self, device: str) -> str:
        """自动检测设备"""
        if device != "auto":
            return device

        try:
            import torch
            if torch.cuda.is_available():
                return "cuda"
            elif torch.backends.mps.is_available():
                return "mps"
            else:
                return "cpu"
        except ImportError:
            return "cpu"

    def _get_default_cache_dir(self) -> str:
        """获取默认缓存目录"""
        base_dir = Path(__file__).parent
        cache_dir = base_dir / "models" / "diffusers"
        cache_dir.mkdir(parents=True, exist_ok=True)
        return str(cache_dir)

    def load_model(self) -> bool:
        """
        加载模型

        Returns:
            是否成功加载
        """
        if self.model_loaded:
            return True

        try:
            print(f"\n📥 正在加载模型...")
            print(f"   首次下载可能需要几分钟，请耐心等待...")

            from diffusers import StableDiffusionPipeline
            import torch

            # 加载管道
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float32 if self.device == "cpu" else torch.float16,
                cache_dir=self.cache_dir,
                safety_checker=None,  # 禁用安全检查器，提高速度
                requires_safety_checker=False,
            )

            # 移动到设备
            self.pipe = self.pipe.to(self.device)

            # CPU 优化
            if self.device == "cpu":
                print("   启用 CPU 优化...")
                # 使用半精度注意力（如果支持）
                try:
                    self.pipe.enable_attention_slicing()
                    print("   ✓ Attention slicing 已启用")
                except:
                    pass

                # 尝试启用 VAE 切片
                try:
                    self.pipe.enable_vae_slicing()
                    print("   ✓ VAE slicing 已启用")
                except:
                    pass

            self.model_loaded = True
            print(f"✅ 模型加载完成！")
            return True

        except ImportError as e:
            print(f"❌ 缺少依赖: {e}")
            print(f"\n💡 请安装 diffusers:")
            print(f"   pip install diffusers transformers torch accelerate")
            return False

        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            return False

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 512,
        height: int = 768,
        steps: int = 25,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None,
        output_path: Optional[str] = None,
    ) -> Tuple[bool, Optional[str]]:
        """
        生成图片

        Args:
            prompt: 正向提示词
            negative_prompt: 反向提示词
            width: 图片宽度
            height: 图片高度
            steps: 推理步数
            guidance_scale: 引导强度
            seed: 随机种子
            output_path: 输出路径

        Returns:
            (是否成功, 输出路径)
        """
        # 加载模型（如果尚未加载）
        if not self.load_model():
            return False, None

        try:
            import torch

            print(f"\n🎨 开始生成图片...")
            print(f"   提示词: {prompt[:80]}...")
            print(f"   尺寸: {width}x{height}")
            print(f"   步数: {steps}")

            # 设置随机种子
            if seed is None:
                seed = int(time.time()) % 1000000

            generator = torch.Generator(device=self.device).manual_seed(seed)

            # 生成图片
            start_time = time.time()

            result = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                num_inference_steps=steps,
                guidance_scale=guidance_scale,
                generator=generator,
            )

            image = result.images[0]

            elapsed = time.time() - start_time
            print(f"   生成耗时: {elapsed:.1f} 秒")

            # 保存图片
            if output_path is None:
                output_dir = Path(__file__).parent / "output"
                output_dir.mkdir(exist_ok=True)
                output_path = str(
                    output_dir / f"local_sd_{int(time.time())}_{seed}.png"
                )

            image.save(output_path, "PNG")
            print(f"✅ 图片已保存: {output_path}")

            return True, output_path

        except Exception as e:
            print(f"❌ 生成失败: {e}")
            return False, None

    def get_recommended_models(self) -> dict:
        """获取推荐模型列表"""
        return self.RECOMMENDED_MODELS


def get_default_negative_prompt() -> str:
    """获取默认反向提示词"""
    return (
        "lowres, bad anatomy, bad hands, text, error, missing fingers, "
        "extra digit, fewer digits, cropped, worst quality, low quality, "
        "normal quality, jpeg artifacts, signature, watermark, username, blurry, "
        "artist name, bad proportions, extra limbs, cloned face, disfigured, "
        "gross proportions, malformed limbs, missing arms, missing legs, "
        "extra arms, extra legs, fused fingers, too many fingers, long neck"
    )


def get_live2d_negative_prompt() -> str:
    """获取 Live2D 专用反向提示词"""
    return (
        "lowres, bad anatomy, bad hands, text, error, missing fingers, "
        "extra digit, fewer digits, cropped, worst quality, low quality, "
        "normal quality, jpeg artifacts, signature, watermark, username, blurry, "
        "artist name, bad proportions, extra limbs, cloned face, disfigured, "
        "gross proportions, malformed limbs, missing arms, missing legs, "
        "extra arms, extra legs, fused fingers, too many fingers, long neck, "
        "photorealistic, realistic, 3d, western, sketch, rough, draft, "
        "messy hair, messy clothes, complex background"
    )


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Live2D Master Agent - 本地图像生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python local_image_generator.py "cute anime girl"
  python local_image_generator.py --model "gsdf/Counterfeit-V3.0" "beautiful anime character"
  python local_image_generator.py --steps 30 --width 512 --height 768 "idol girl"
  python local_image_generator.py --list-models
""",
    )

    parser.add_argument("prompt", nargs="?", help="生成提示词")
    parser.add_argument(
        "--model",
        type=str,
        default="Linaqruf/anything-v3.0",
        help='模型 ID (默认: "Linaqruf/anything-v3.0")',
    )
    parser.add_argument(
        "--device", type=str, default="auto", help="运行设备 (auto/cpu/cuda/mps)"
    )
    parser.add_argument(
        "--width", type=int, default=512, help="图片宽度 (默认: 512)"
    )
    parser.add_argument(
        "--height", type=int, default=768, help="图片高度 (默认: 768)"
    )
    parser.add_argument(
        "--steps", type=int, default=25, help="推理步数 (默认: 25)"
    )
    parser.add_argument(
        "--guidance", type=float, default=7.5, help="引导强度 (默认: 7.5)"
    )
    parser.add_argument("--seed", type=int, default=None, help="随机种子")
    parser.add_argument(
        "--negative", type=str, default="", help="反向提示词"
    )
    parser.add_argument(
        "--live2d", action="store_true", help="使用 Live2D 优化提示词"
    )
    parser.add_argument(
        "--list-models", action="store_true", help="列出推荐模型"
    )
    parser.add_argument(
        "--output", type=str, default=None, help="输出路径"
    )

    args = parser.parse_args()

    # 列出模型
    if args.list_models:
        print("📚 推荐模型列表:")
        print("=" * 60)
        generator = LocalImageGenerator()
        for key, info in generator.get_recommended_models().items():
            print(f"\n🎯 {key}")
            print(f"   ID: {info['id']}")
            print(f"   描述: {info['desc']}")
            print(f"   大小: {info['size']}")
        print("\n💡 使用方法:")
        print('   python local_image_generator.py --model "模型ID" "提示词"')
        return

    # 检查提示词
    if not args.prompt:
        print("❌ 请提供生成提示词")
        print("💡 使用 --help 查看帮助")
        sys.exit(1)

    # 构建反向提示词
    negative_prompt = args.negative
    if args.live2d and not negative_prompt:
        negative_prompt = get_live2d_negative_prompt()
    elif not negative_prompt:
        negative_prompt = get_default_negative_prompt()

    # 创建生成器
    generator = LocalImageGenerator(
        model_id=args.model,
        device=args.device,
    )

    # 生成图片
    success, output_path = generator.generate(
        prompt=args.prompt,
        negative_prompt=negative_prompt,
        width=args.width,
        height=args.height,
        steps=args.steps,
        guidance_scale=args.guidance,
        seed=args.seed,
        output_path=args.output,
    )

    if success:
        print(f"\n🎉 生成成功！")
        print(f"📁 文件: {output_path}")
    else:
        print(f"\n❌ 生成失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
