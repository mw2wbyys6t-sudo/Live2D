#!/usr/bin/env python3
"""
Live2D Master Agent - 本地图像生成器 v4.0
基于 Stable Diffusion + diffusers 的专业图像生成工具

核心升级：
- 🎯 针对参考图质量级别优化（商业插画师水准）
- 🎨 专业 pastel 调色板控制
- ⚡ 权重控制语法 (keyword:1.3) 提升关键元素质量
- 🔧 与分层工具无缝连接（生成即分层就绪）
- 📊 生成参数智能推荐
- 🖼️ 专业后处理管道（线条锐化/色彩校正/降噪）

使用方法：
    python local_image_generator.py "cute anime girl"
    python local_image_generator.py --model "gsdf/Counterfeit-V3.0" --quality ultra "beautiful character"
    python local_image_generator.py --live2d-mode --width 512 --height 768 "idol girl"
"""

import os
import sys
import time
import argparse
import warnings
from pathlib import Path
from typing import Optional, Tuple, Dict, List, Union
import json

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class ModelConfig:
    """模型配置 - 基于搜索研究的最佳模型选择"""

    MODELS = {
        "anything-v3": {
            "id": "Linaqruf/anything-v3.0",
            "desc": "Anything V3 - 通用动漫风格",
            "size": "约 4GB",
            "quality": "standard",
            "best_for": "通用动漫角色",
            "type": "sd15",
        },
        "anything-v5": {
            "id": "stablediffusionapi/anything-v5",
            "desc": "Anything V5 - 高质量动漫",
            "size": "约 4GB",
            "quality": "high",
            "best_for": "精细动漫角色",
            "type": "sd15",
        },
        "counterfeit-v3": {
            "id": "gsdf/Counterfeit-V3.0",
            "desc": "Counterfeit V3 - 细腻画风（推荐）",
            "size": "约 4GB",
            "quality": "ultra",
            "best_for": "高质量插画风格",
            "type": "sd15",
        },
        "meinaMix": {
            "id": "Meina/MeinaMix",
            "desc": "MeinaMix - 萌系风格",
            "size": "约 4GB",
            "quality": "high",
            "best_for": "萌系角色",
            "type": "sd15",
        },
        "pastel-mix": {
            "id": "andite/pastel-mix",
            "desc": "Pastel Mix - 柔和色彩（推荐）",
            "size": "约 4GB",
            "quality": "high",
            "best_for": "柔和梦幻风格",
            "type": "sd15",
        },
        "abyss-orange": {
            "id": "WarriorMama777/OrangeMixs",
            "desc": "AbyssOrangeMix - 丰富色彩",
            "size": "约 4GB",
            "quality": "high",
            "best_for": "色彩丰富的角色",
            "type": "sd15",
        },
        "shiitake-mix": {
            "id": "Vsukiyaki/ShiitakeMix",
            "desc": "Shiitake-Mix - SDXL动漫",
            "size": "约 7GB",
            "quality": "ultra",
            "best_for": "SDXL高质量动漫",
            "type": "sdxl",
        },
        "nova-anime": {
            "id": "NovaAnimeXL",
            "desc": "Nova Anime XL - 2.5D风格",
            "size": "约 7GB",
            "quality": "ultra",
            "best_for": "2.5D动漫风格",
            "type": "sdxl",
        },
    }

    QUALITY_PRESETS = {
        "draft": {
            "steps": 15,
            "guidance_scale": 7.0,
            "desc": "快速草稿",
        },
        "standard": {
            "steps": 25,
            "guidance_scale": 7.5,
            "desc": "标准质量",
        },
        "high": {
            "steps": 35,
            "guidance_scale": 8.0,
            "desc": "高质量",
        },
        "ultra": {
            "steps": 50,
            "guidance_scale": 8.5,
            "desc": "超高质量",
        },
    }


class Live2DOptimizedGenerator:
    """Live2D 优化的图像生成器 v4.0 - 参考图质量级别"""

    # 基于参考图分析的专业提示词模板
    # 第一张参考图特征：清晰线条、柔和pastel色彩、专业插画风格
    # 第二张参考图特征：梦幻氛围、精细细节、偶像风格
    
    # 专业级提示词模板（匹配参考图质量）
    PROFESSIONAL_PROMPT_TEMPLATE = """(masterpiece:1.4), (best quality:1.3), (ultra detailed:1.2), (highres:1.2), (8k uhd:1.1),
(anime style:1.3), (illustration:1.2), (official art:1.2), (pixiv:1.1), (artstation:1.1),
1girl, solo, {pose}, {hairstyle}, {hair_color}, {eye_color}, {clothing}, {accessory}, {expression},
(beautiful detailed face:1.3), (beautiful detailed eyes:1.3), (detailed skin texture:1.1), (soft lighting:1.2),
(pastel colors:1.2), (soft color palette:1.2), (dreamy atmosphere:1.1), (ethereal:1.1),
(frills:1.1), (lace:1.1), (ribbons:1.1), (bows:1.1), (jewelry:1.1), (elegant outfit:1.2),
(perfect anatomy:1.2), (correct proportions:1.2), (delicate hands:1.2),
(white background:1.2), (simple background:1.2), (clean background:1.2),
(sharp focus:1.2), (vibrant colors:1.1), (clear lineart:1.3), (smooth shading:1.1)"""

    # Live2D专用提示词模板（基于业界最佳实践）
    LIVE2D_PROMPT_TEMPLATE = """(masterpiece:1.4), (best quality:1.3), (ultra detailed:1.2), (highres:1.2),
(anime style:1.3), (illustration:1.2), 1girl, solo, (full body:1.2), (standing:1.1), (looking at viewer:1.2),
{hairstyle}, {hair_color}, {eye_color}, {clothing}, {accessory}, {expression},
(beautiful detailed face:1.3), (beautiful detailed eyes:1.3), (detailed skin texture:1.1), (soft lighting:1.2),
(perfect for Live2D rigging:1.2), (clean lineart:1.3), (clear edges:1.3), (sharp outlines:1.3),
(flat colors:1.2), (minimal shading:1.2), (cel shading:1.2), (distinct color separation:1.2),
(anime coloring:1.2), (sharp lines:1.3), (clean outlines:1.3), (minimal gradients:1.2),
(simple background:1.2), (white background:1.2), (isolated character:1.2),
(clear silhouette:1.2), (symmetrical eyes:1.2), (simple hair strands:1.1),
(visible neck and shoulders:1.2), (visible arms and hands:1.2), (visible legs and feet:1.2),
(closed mouth:1.1), (neutral expression:1.1), (front view:1.2), (straight-on view:1.2),
(perfect anatomy:1.2), (correct proportions:1.2), (delicate hands:1.2),
(sharp focus:1.2), (vibrant colors:1.1)"""

    # 高质量反向提示词（基于搜索研究优化）
    NEGATIVE_PROMPT = """(lowres:1.4), (bad anatomy:1.4), (bad hands:1.3), (text:1.3), (error:1.3), (missing fingers:1.3),
(extra digit:1.3), (fewer digits:1.3), (cropped:1.2), (worst quality:1.3), (low quality:1.3),
(normal quality:1.2), (jpeg artifacts:1.2), (signature:1.2), (watermark:1.2), (username:1.2), (blurry:1.3),
(artist name:1.2), (bad proportions:1.3), (extra limbs:1.3), (cloned face:1.2), (disfigured:1.3),
(gross proportions:1.3), (malformed limbs:1.3), (missing arms:1.2), (missing legs:1.2),
(extra arms:1.2), (extra legs:1.2), (fused fingers:1.2), (too many fingers:1.2), (long neck:1.2),
(photorealistic:1.2), (realistic:1.2), (3d:1.2), (western:1.2), (sketch:1.1), (rough:1.1), (draft:1.1),
(complex background:1.2), (messy hair:1.2), (messy clothes:1.2),
(depth of field:1.1), (blurry background:1.2), (multiple girls:1.3), (multiple people:1.3)"""

    # Live2D专用反向提示词（更严格）
    LIVE2D_NEGATIVE_PROMPT = """(lowres:1.4), (bad anatomy:1.4), (bad hands:1.3), (text:1.3), (error:1.3), (missing fingers:1.3),
(extra digit:1.3), (fewer digits:1.3), (cropped:1.2), (worst quality:1.3), (low quality:1.3),
(normal quality:1.2), (jpeg artifacts:1.2), (signature:1.2), (watermark:1.2), (username:1.2), (blurry:1.3),
(artist name:1.2), (bad proportions:1.3), (extra limbs:1.3), (cloned face:1.2), (disfigured:1.3),
(gross proportions:1.3), (malformed limbs:1.3), (missing arms:1.2), (missing legs:1.2),
(extra arms:1.2), (extra legs:1.2), (fused fingers:1.2), (too many fingers:1.2), (long neck:1.2),
(photorealistic:1.2), (realistic:1.2), (3d:1.2), (western:1.2), (sketch:1.1), (rough:1.1), (draft:1.1),
(complex background:1.2), (messy hair:1.2), (messy clothes:1.2),
(profile view:1.2), (side view:1.2), (back view:1.2), (turned away:1.2),
(open mouth:1.2), (talking:1.2), (shouting:1.2), (laughing:1.2), (crying:1.2),
(dynamic pose:1.2), (action pose:1.2), (jumping:1.2), (running:1.2), (sitting:1.2), (lying down:1.2),
(partial body:1.2), (cropped:1.2), (off-screen:1.2), (out of frame:1.2),
(gradient shading:1.2), (soft shading:1.2), (painterly:1.2), (watercolor:1.2),
(noise:1.2), (grainy:1.2), (pixelated:1.2), (compression artifacts:1.2)"""

    def __init__(
        self,
        model_id: str = "Linaqruf/anything-v3.0",
        device: str = "auto",
        cache_dir: Optional[str] = None,
    ):
        self.model_id = model_id
        self.device = self._get_device(device)
        self.cache_dir = cache_dir or self._get_default_cache_dir()
        self.pipe = None
        self.model_loaded = False
        self.config = ModelConfig()
        self.model_type = self._detect_model_type(model_id)

        print(f"🎯 Live2D 优化图像生成器 v4.0")
        print(f"   模型: {model_id}")
        print(f"   类型: {self.model_type.upper()}")
        print(f"   设备: {self.device}")
        print(f"   缓存: {self.cache_dir}")

    def _detect_model_type(self, model_id: str) -> str:
        """检测模型类型 (sd15/sdxl)"""
        sdxl_keywords = ['xl', 'XL', 'Shiitake', 'NovaAnime']
        for kw in sdxl_keywords:
            if kw in model_id:
                return "sdxl"
        return "sd15"

    def _get_device(self, device: str) -> str:
        if device != "auto":
            return device
        try:
            import torch
            if torch.cuda.is_available():
                print("   ✓ 检测到 CUDA GPU")
                return "cuda"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                print("   ✓ 检测到 MPS (Apple Silicon)")
                return "mps"
            else:
                print("   ℹ 使用 CPU 推理")
                return "cpu"
        except ImportError:
            return "cpu"

    def _get_default_cache_dir(self) -> str:
        base_dir = Path(__file__).parent
        cache_dir = base_dir / "models" / "diffusers"
        cache_dir.mkdir(parents=True, exist_ok=True)
        return str(cache_dir)

    def load_model(self) -> bool:
        if self.model_loaded:
            return True

        try:
            print(f"\n📥 正在加载模型...")
            print(f"   首次下载可能需要几分钟，请耐心等待...")

            import torch

            if self.model_type == "sdxl":
                from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
                self.pipe = StableDiffusionXLPipeline.from_pretrained(
                    self.model_id,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    cache_dir=self.cache_dir,
                    safety_checker=None,
                    requires_safety_checker=False,
                )
            else:
                from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
                self.pipe = StableDiffusionPipeline.from_pretrained(
                    self.model_id,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    cache_dir=self.cache_dir,
                    safety_checker=None,
                    requires_safety_checker=False,
                )

            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )

            self.pipe = self.pipe.to(self.device)

            if self.device == "cpu":
                print("   启用 CPU 优化...")
                try:
                    self.pipe.enable_attention_slicing()
                    print("   ✓ Attention slicing")
                except:
                    pass
                try:
                    self.pipe.enable_vae_slicing()
                    print("   ✓ VAE slicing")
                except:
                    pass
                try:
                    self.pipe.enable_sequential_cpu_offload()
                    print("   ✓ CPU offload")
                except:
                    pass

            self.model_loaded = True
            print(f"✅ 模型加载完成！")
            return True

        except ImportError as e:
            print(f"❌ 缺少依赖: {e}")
            print(f"\n💡 请安装:")
            print(f"   pip install diffusers transformers torch accelerate")
            return False
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            return False

    def build_prompt(
        self,
        custom_prompt: str = "",
        live2d_mode: bool = True,
        style: str = "anime style",
        hairstyle: str = "long hair",
        hair_color: str = "pink hair",
        eye_color: str = "blue eyes",
        clothing: str = "school uniform",
        accessory: str = "hair ribbon",
        expression: str = "smile",
        pose: str = "standing",
        quality: str = "masterpiece, best quality, ultra detailed",
    ) -> Tuple[str, str]:
        if live2d_mode:
            prompt = self.LIVE2D_PROMPT_TEMPLATE.format(
                style=style,
                quality_tags=quality,
                pose=pose,
                hairstyle=hairstyle,
                hair_color=hair_color,
                eye_color=eye_color,
                clothing=clothing,
                accessory=accessory,
                expression=expression,
            )
            negative = self.LIVE2D_NEGATIVE_PROMPT
        else:
            prompt = self.PROFESSIONAL_PROMPT_TEMPLATE.format(
                style=style,
                quality_tags=quality,
                pose=pose,
                hairstyle=hairstyle,
                hair_color=hair_color,
                eye_color=eye_color,
                clothing=clothing,
                accessory=accessory,
                expression=expression,
            )
            negative = self.NEGATIVE_PROMPT

        if custom_prompt:
            prompt = custom_prompt + ", " + prompt

        prompt = ' '.join(prompt.split())
        negative = ' '.join(negative.split())

        return prompt, negative

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
        live2d_optimized: bool = True,
    ) -> Tuple[bool, Optional[str]]:
        if not self.load_model():
            return False, None

        try:
            import torch
            from PIL import Image

            print(f"\n🎨 开始生成图片...")
            print(f"   提示词: {prompt[:80]}...")
            print(f"   尺寸: {width}x{height}")
            print(f"   步数: {steps}")
            print(f"   Live2D优化: {'是' if live2d_optimized else '否'}")

            if seed is None:
                seed = int(time.time()) % 1000000

            generator = torch.Generator(device=self.device).manual_seed(seed)

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

            # Live2D 优化处理
            if live2d_optimized:
                print("   正在进行 Live2D 优化...")
                image = self._optimize_for_live2d(image)

            # 保存图片
            if output_path is None:
                output_dir = Path(__file__).parent / "output"
                output_dir.mkdir(exist_ok=True)
                output_path = str(
                    output_dir / f"live2d_gen_{int(time.time())}_{seed}.png"
                )

            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            image.save(output_path, "PNG")
            print(f"✅ 图片已保存: {output_path}")

            return True, output_path

        except Exception as e:
            print(f"❌ 生成失败: {e}")
            return False, None

    def _optimize_for_live2d(self, image) -> 'Image.Image':
        """
        针对 Live2D 分层优化图片 v4.0
        基于 Layerdivider 和 See-through 的最佳实践
        """
        from PIL import Image, ImageFilter, ImageEnhance

        # 转换为 RGBA
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # 1. 增强锐度（清晰边缘）
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.3)

        # 2. 增强对比度（颜色分离）
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.15)

        # 3. 颜色量化（减少颜色数量，便于分层）
        # 使用自适应调色板，保持主要颜色区域
        if hasattr(Image, 'Quantize'):
            try:
                r, g, b, a = image.split()
                rgb = Image.merge('RGB', (r, g, b))

                # 使用自适应量化，保持边缘清晰
                quantized = rgb.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
                rgb = quantized.convert('RGB')

                r, g, b = rgb.split()
                image = Image.merge('RGBA', (r, g, b, a))
            except:
                pass

        # 4. 轻微边缘增强
        try:
            r, g, b, a = image.split()
            rgb = Image.merge('RGB', (r, g, b))
            edge_enhanced = rgb.filter(ImageFilter.EDGE_ENHANCE_MORE)
            r, g, b = edge_enhanced.split()
            image = Image.merge('RGBA', (r, g, b, a))
        except:
            pass

        return image

    def post_process_pipeline(
        self,
        image_path: str,
        enable_upscale: bool = False,
        enable_face_restore: bool = False,
        target_width: Optional[int] = None,
        target_height: Optional[int] = None,
    ) -> str:
        """
        专业后处理管道 v4.0
        基于业界最佳实践：线条锐化 → 色彩校正 → AI放大 → 降噪
        """
        from PIL import Image, ImageFilter, ImageEnhance

        print("\n🔧 运行专业后处理管道...")

        img = Image.open(image_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # 1. 线条锐化（关键：匹配参考图的清晰线条）
        print("   1. 线条锐化...")
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.4)

        # 2. 色彩校正（ pastel 调色板）
        print("   2. 色彩校正...")
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.15)

        # 3. 对比度优化
        print("   3. 对比度优化...")
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)

        # 4. 亮度微调
        print("   4. 亮度微调...")
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.05)

        # 5. AI放大（如果启用）
        if enable_upscale and target_width and target_height:
            print(f"   5. 放大到 {target_width}x{target_height}...")
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

        # 保存处理后的图片
        processed_path = image_path.replace('.png', '_processed.png')
        img.save(processed_path, "PNG")
        print(f"✅ 后处理完成: {processed_path}")

        return processed_path

    def generate_batch(
        self,
        prompts: List[str],
        negative_prompt: str = "",
        width: int = 512,
        height: int = 768,
        steps: int = 25,
        guidance_scale: float = 7.5,
        output_dir: Optional[str] = None,
    ) -> List[Tuple[bool, Optional[str]]]:
        results = []
        for i, prompt in enumerate(prompts):
            print(f"\n{'='*60}")
            print(f"🎯 生成 {i+1}/{len(prompts)}")
            print(f"{'='*60}")

            success, path = self.generate(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                steps=steps,
                guidance_scale=guidance_scale,
            )
            results.append((success, path))

        return results

    def get_model_info(self) -> Dict:
        return {
            "model_id": self.model_id,
            "model_type": self.model_type,
            "device": self.device,
            "loaded": self.model_loaded,
            "cache_dir": self.cache_dir,
        }

    @staticmethod
    def get_recommended_models() -> Dict:
        return ModelConfig.MODELS

    @staticmethod
    def get_quality_presets() -> Dict:
        return ModelConfig.QUALITY_PRESETS


class LocalImageGenerator:
    """兼容旧接口的包装类"""

    def __init__(self, model_id: str = "Linaqruf/anything-v3.0"):
        self.generator = Live2DOptimizedGenerator(model_id=model_id)

    def generate(self, *args, **kwargs):
        return self.generator.generate(*args, **kwargs)


def get_default_negative_prompt() -> str:
    return Live2DOptimizedGenerator.NEGATIVE_PROMPT


def get_live2d_negative_prompt() -> str:
    return Live2DOptimizedGenerator.LIVE2D_NEGATIVE_PROMPT


def main():
    parser = argparse.ArgumentParser(
        description="Live2D Master Agent - 本地图像生成器 v4.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # Live2D 优化模式（默认）
  python local_image_generator.py "cute anime girl"

  # 高质量模式
  python local_image_generator.py --no-live2d "beautiful anime character"

  # 指定模型
  python local_image_generator.py --model "gsdf/Counterfeit-V3.0" "idol girl"

  # 超高质量
  python local_image_generator.py --quality ultra --steps 50 "masterpiece"

  # 查看推荐模型
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
        "--steps", type=int, default=None, help="推理步数 (默认: 25)"
    )
    parser.add_argument(
        "--guidance", type=float, default=7.5, help="引导强度 (默认: 7.5)"
    )
    parser.add_argument("--seed", type=int, default=None, help="随机种子")
    parser.add_argument(
        "--negative", type=str, default="", help="反向提示词"
    )
    parser.add_argument(
        "--no-live2d",
        action="store_true",
        help="禁用 Live2D 优化（生成自由风格）",
    )
    parser.add_argument(
        "--quality",
        type=str,
        default="standard",
        choices=["draft", "standard", "high", "ultra"],
        help="质量预设",
    )
    parser.add_argument(
        "--list-models", action="store_true", help="列出推荐模型"
    )
    parser.add_argument(
        "--output", type=str, default=None, help="输出路径"
    )
    parser.add_argument(
        "--post-process", action="store_true", help="启用专业后处理"
    )

    args = parser.parse_args()

    if args.list_models:
        print("📚 推荐模型列表:")
        print("=" * 60)
        for key, info in Live2DOptimizedGenerator.get_recommended_models().items():
            print(f"\n🎯 {key}")
            print(f"   ID: {info['id']}")
            print(f"   描述: {info['desc']}")
            print(f"   大小: {info['size']}")
            print(f"   质量: {info['quality']}")
            print(f"   适合: {info['best_for']}")
            print(f"   类型: {info['type'].upper()}")

        print("\n📊 质量预设:")
        print("=" * 60)
        for key, info in Live2DOptimizedGenerator.get_quality_presets().items():
            print(f"\n⚡ {key}")
            print(f"   步数: {info['steps']}")
            print(f"   引导: {info['guidance_scale']}")
            print(f"   描述: {info['desc']}")
        return

    if not args.prompt:
        print("❌ 请提供生成提示词")
        print("💡 使用 --help 查看帮助")
        sys.exit(1)

    quality_preset = Live2DOptimizedGenerator.get_quality_presets()[args.quality]
    steps = args.steps or quality_preset["steps"]

    generator = Live2DOptimizedGenerator(
        model_id=args.model,
        device=args.device,
    )

    prompt, negative = generator.build_prompt(
        custom_prompt=args.prompt,
        live2d_mode=not args.no_live2d,
    )

    if args.negative:
        negative = args.negative + ", " + negative

    success, output_path = generator.generate(
        prompt=prompt,
        negative_prompt=negative,
        width=args.width,
        height=args.height,
        steps=steps,
        guidance_scale=args.guidance,
        seed=args.seed,
        output_path=args.output,
        live2d_optimized=not args.no_live2d,
    )

    if success:
        print(f"\n🎉 生成成功！")
        print(f"📁 文件: {output_path}")

        # 后处理
        if args.post_process:
            processed_path = generator.post_process_pipeline(output_path)
            print(f"📁 处理后文件: {processed_path}")
    else:
        print(f"\n❌ 生成失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
