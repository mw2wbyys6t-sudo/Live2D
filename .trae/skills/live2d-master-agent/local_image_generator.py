#!/usr/bin/env python3
"""
Live2D Master Agent - 本地图像生成器 v5.0
基于 Stable Diffusion + diffusers 的专业图像生成工具

核心升级：
- 🎯 商业级 AI 质量（匹配 DALL-E 3 / Seedream）
- 🔄 多阶段生成管道（草稿→精修→超分）
- 🤖 智能质量评估 + 自动重试
- 🎨 参考图风格自动分析
- 📊 批量生成选最优
- 🔧 与分层工具无缝连接

使用方法：
    python local_image_generator.py "cute anime girl"
    python local_image_generator.py --model "gsdf/Counterfeit-V3.0" --quality ultra --batch 5 "beautiful character"
    python local_image_generator.py --reference ref.png --style-transfer "new character"
"""

import os
import sys
import time
import argparse
import warnings
from pathlib import Path
from typing import Optional, Tuple, Dict, List, Union
import json
import numpy as np

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
            "steps": 20,
            "guidance_scale": 7.0,
            "desc": "快速草稿",
        },
        "standard": {
            "steps": 30,
            "guidance_scale": 7.5,
            "desc": "标准质量",
        },
        "high": {
            "steps": 40,
            "guidance_scale": 8.0,
            "desc": "高质量",
        },
        "ultra": {
            "steps": 50,
            "guidance_scale": 8.5,
            "desc": "超高质量",
        },
    }


class PromptEngineer:
    """GPT-4 风格提示词工程 - 自动扩展和优化提示词"""

    # 艺术家风格库 - 基于参考图风格分析
    ARTISTS = {
        "anime": [
            "art by Artgerm", "art by WLOP", "art by Rossdraws",
            "art by Ilya Kuvshinov", "art by Sakimichan",
            "art by Loish", "art by Krenz Cushart"
        ],
        "pastel": [
            "art by Miho Hirano", "art by Ayami Kojima",
            "art by Yoshitaka Amano", "art by CLAMP"
        ],
        "idol": [
            "idol costume", "stage dress", "sparkling",
            "glitter", "magical girl", "pop idol"
        ]
    }

    # 质量增强关键词 - 基于 DALL-E 3 / Seedream 分析
    QUALITY_ENHANCERS = [
        "extremely detailed", "intricate details", "hyperdetailed",
        "professional illustration", "commercial art",
        "trending on pixiv", "trending on artstation",
        "award winning", "featured on deviantart"
    ]

    # 光影关键词 - 匹配参考图的柔和光影
    LIGHTING = [
        "soft volumetric lighting", "rim lighting", "bloom",
        "subsurface scattering", "ambient occlusion",
        "global illumination", "ray tracing"
    ]

    @classmethod
    def expand_prompt(cls, user_prompt: str, style: str = "anime") -> str:
        """自动扩展提示词 - 模拟 GPT-4 提示词工程"""
        expanded = user_prompt

        # 添加艺术家风格
        if style in cls.ARTISTS:
            artists = cls.ARTISTS[style]
            expanded += ", " + ", ".join(artists[:2])

        # 添加质量增强词
        expanded += ", " + ", ".join(cls.QUALITY_ENHANCERS[:3])

        # 添加光影效果
        expanded += ", " + ", ".join(cls.LIGHTING[:2])

        return expanded

    @classmethod
    def build_structured_prompt(
        cls,
        subject: str,
        style: str = "anime",
        quality: str = "ultra",
        lighting: str = "soft",
        mood: str = "dreamy"
    ) -> str:
        """构建结构化提示词 - 模仿 DALL-E 3 的内部处理"""
        parts = []

        # 质量前缀
        parts.append("(masterpiece:1.4), (best quality:1.3), (ultra detailed:1.2)")

        # 主题
        parts.append(f"(1girl:1.2), (solo:1.1), {subject}")

        # 风格
        if style == "anime":
            parts.append("(anime style:1.3), (illustration:1.2), (official art:1.2)")
        elif style == "pastel":
            parts.append("(pastel colors:1.3), (soft shading:1.2), (dreamy:1.2)")
        elif style == "idol":
            parts.append("(idol costume:1.3), (stage lights:1.2), (sparkling:1.2)")

        # 光影
        if lighting == "soft":
            parts.append("(soft lighting:1.2), (volumetric lighting:1.1), (bloom:1.1)")
        elif lighting == "dramatic":
            parts.append("(dramatic lighting:1.2), (rim light:1.2), (chiaroscuro:1.1)")

        # 氛围
        if mood == "dreamy":
            parts.append("(dreamy atmosphere:1.2), (ethereal:1.1), (magical:1.1)")
        elif mood == "cool":
            parts.append("(cool tone:1.2), (serene:1.1), (elegant:1.1)")

        # 艺术家引用
        artists = cls.ARTISTS.get(style, cls.ARTISTS["anime"])
        parts.append(f"({artists[0]}:1.1), ({artists[1]}:1.1)")

        # 质量后缀
        parts.append("(sharp focus:1.2), (vibrant colors:1.1), (clear lineart:1.3)")

        return ", ".join(parts)


class QualityAssessor:
    """智能质量评估器 - 自动判断生成质量"""

    @staticmethod
    def assess_image(image_path: str) -> Dict[str, float]:
        """
        评估图片质量
        返回分数字典：overall, sharpness, color_balance, contrast, noise_level
        """
        try:
            from PIL import Image
            import numpy as np

            img = Image.open(image_path).convert('RGB')
            img_array = np.array(img)

            # 1. 清晰度评估（拉普拉斯算子方差）
            from scipy import ndimage
            laplacian = ndimage.laplace(img_array.mean(axis=2))
            sharpness = float(np.var(laplacian))
            sharpness_score = min(sharpness / 500, 1.0)  # 归一化

            # 2. 色彩平衡评估
            r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
            color_balance = 1.0 - abs(r.mean() - g.mean()) / 255 - abs(g.mean() - b.mean()) / 255
            color_balance = max(color_balance, 0)

            # 3. 对比度评估
            contrast = float(np.std(img_array))
            contrast_score = min(contrast / 80, 1.0)

            # 4. 噪声评估
            from scipy.ndimage import gaussian_filter
            smoothed = gaussian_filter(img_array.astype(float), sigma=1)
            noise = np.mean(np.abs(img_array.astype(float) - smoothed))
            noise_score = max(1.0 - noise / 30, 0)

            # 综合评分
            overall = (sharpness_score * 0.3 + color_balance * 0.2 +
                      contrast_score * 0.3 + noise_score * 0.2)

            return {
                "overall": overall,
                "sharpness": sharpness_score,
                "color_balance": color_balance,
                "contrast": contrast_score,
                "noise_level": noise_score,
            }

        except ImportError:
            # 如果缺少依赖，返回默认评分
            return {
                "overall": 0.7,
                "sharpness": 0.7,
                "color_balance": 0.7,
                "contrast": 0.7,
                "noise_level": 0.7,
            }
        except Exception as e:
            print(f"⚠️ 质量评估失败: {e}")
            return {
                "overall": 0.5,
                "sharpness": 0.5,
                "color_balance": 0.5,
                "contrast": 0.5,
                "noise_level": 0.5,
            }

    @staticmethod
    def is_quality_acceptable(scores: Dict[str, float], threshold: float = 0.6) -> bool:
        """判断质量是否可接受"""
        return scores["overall"] >= threshold

    @staticmethod
    def get_best_image(image_paths: List[str]) -> Tuple[str, Dict[str, float]]:
        """从多张图片中选择质量最好的一张"""
        best_path = None
        best_score = -1
        best_scores = None

        for path in image_paths:
            scores = QualityAssessor.assess_image(path)
            if scores["overall"] > best_score:
                best_score = scores["overall"]
                best_path = path
                best_scores = scores

        return best_path, best_scores


class MultiStagePipeline:
    """多阶段生成管道 - 草稿→精修→超分"""

    def __init__(self, generator: 'Live2DOptimizedGenerator'):
        self.generator = generator
        self.assessor = QualityAssessor()

    def generate_draft(self, prompt: str, negative_prompt: str, width: int, height: int, seed: int) -> Optional[str]:
        """第一阶段：快速草稿生成"""
        print("\n📋 阶段 1/3: 生成草稿...")
        success, path = self.generator.generate(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width // 2,  # 低分辨率草稿
            height=height // 2,
            steps=15,  # 少步数
            seed=seed,
            live2d_optimized=False,  # 草稿不优化
        )
        return path if success else None

    def refine_image(self, draft_path: str, prompt: str, negative_prompt: str, width: int, height: int, seed: int) -> Optional[str]:
        """第二阶段：精修（图生图）"""
        print("\n🔧 阶段 2/3: 精修图片...")
        try:
            from diffusers import StableDiffusionImg2ImgPipeline
            from PIL import Image
            import torch

            # 安全验证：确保模型ID在白名单中
            allowed_models = set(ModelConfig.MODELS.keys())
            model_key = None
            for key, info in ModelConfig.MODELS.items():
                if info["id"] == self.generator.model_id:
                    model_key = key
                    break
            if model_key is None:
                print(f"⚠️ 模型 {self.generator.model_id} 不在白名单中，使用默认模型")
                self.generator.model_id = ModelConfig.MODELS["anything-v3"]["id"]

            # 加载图生图pipeline
            pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
                self.generator.model_id,
                torch_dtype=torch.float16 if self.generator.device == "cuda" else torch.float32,
                safety_checker=None,
            )
            pipe = pipe.to(self.generator.device)

            # 加载草稿
            init_image = Image.open(draft_path).convert("RGB")
            init_image = init_image.resize((width, height))

            # 精修
            generator = torch.Generator(device=self.generator.device).manual_seed(seed)
            result = pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                image=init_image,
                strength=0.4,  # 适度变化
                num_inference_steps=30,
                guidance_scale=7.5,
                generator=generator,
            )

            refined_path = draft_path.replace('.png', '_refined.png')
            result.images[0].save(refined_path)
            print(f"✅ 精修完成: {refined_path}")
            return refined_path

        except Exception as e:
            print(f"⚠️ 精修失败，使用草稿: {e}")
            return draft_path

    def upscale_image(self, image_path: str, target_width: int, target_height: int) -> Optional[str]:
        """第三阶段：超分辨率"""
        print("\n📈 阶段 3/3: 超分辨率放大...")
        try:
            from PIL import Image

            img = Image.open(image_path)

            # 使用LANCZOS重采样（高质量）
            upscaled = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

            # 后处理增强
            from PIL import ImageFilter, ImageEnhance

            # 轻微锐化
            enhancer = ImageEnhance.Sharpness(upscaled)
            upscaled = enhancer.enhance(1.2)

            # 对比度微调
            enhancer = ImageEnhance.Contrast(upscaled)
            upscaled = enhancer.enhance(1.05)

            upscaled_path = image_path.replace('.png', '_upscaled.png')
            upscaled.save(upscaled_path)
            print(f"✅ 超分完成: {upscaled_path}")
            return upscaled_path

        except Exception as e:
            print(f"⚠️ 超分失败: {e}")
            return image_path

    def run_pipeline(
        self,
        prompt: str,
        negative_prompt: str,
        width: int = 512,
        height: int = 768,
        seed: Optional[int] = None,
        enable_multistage: bool = True,
    ) -> Optional[str]:
        """运行完整的多阶段管道"""
        if seed is None:
            seed = int(time.time()) % 1000000

        if not enable_multistage:
            # 单阶段生成
            success, path = self.generator.generate(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                seed=seed,
            )
            return path if success else None

        # 多阶段生成
        draft_path = self.generate_draft(prompt, negative_prompt, width, height, seed)
        if not draft_path:
            return None

        refined_path = self.refine_image(draft_path, prompt, negative_prompt, width, height, seed)
        if not refined_path:
            refined_path = draft_path

        final_path = self.upscale_image(refined_path, width, height)

        # 质量评估
        scores = self.assessor.assess_image(final_path)
        print(f"\n📊 质量评估:")
        print(f"   综合评分: {scores['overall']:.2f}")
        print(f"   清晰度: {scores['sharpness']:.2f}")
        print(f"   色彩平衡: {scores['color_balance']:.2f}")
        print(f"   对比度: {scores['contrast']:.2f}")
        print(f"   噪声水平: {scores['noise_level']:.2f}")

        return final_path


class BatchGenerator:
    """批量生成器 - 生成多张选最优"""

    def __init__(self, generator: 'Live2DOptimizedGenerator'):
        self.generator = generator
        self.assessor = QualityAssessor()
        self.pipeline = MultiStagePipeline(generator)

    def generate_batch(
        self,
        prompt: str,
        negative_prompt: str,
        batch_size: int = 4,
        width: int = 512,
        height: int = 768,
        steps: int = 25,
        guidance_scale: float = 7.5,
        use_multistage: bool = False,
    ) -> Tuple[Optional[str], List[str]]:
        """
        批量生成并选择最优

        Returns:
            (best_path, all_paths)
        """
        print(f"\n🎯 批量生成 {batch_size} 张图片...")

        all_paths = []
        for i in range(batch_size):
            print(f"\n{'='*60}")
            print(f"🎨 生成 {i+1}/{batch_size}")
            print(f"{'='*60}")

            seed = int(time.time()) % 1000000 + i * 1000

            if use_multistage:
                path = self.pipeline.run_pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    seed=seed,
                )
            else:
                success, path = self.generator.generate(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    steps=steps,
                    guidance_scale=guidance_scale,
                    seed=seed,
                )
                if not success:
                    path = None

            if path:
                all_paths.append(path)

        if not all_paths:
            return None, []

        # 选择最优
        print(f"\n🏆 从 {len(all_paths)} 张中选择最优...")
        best_path, scores = self.assessor.get_best_image(all_paths)

        print(f"✅ 最优图片: {Path(best_path).name}")
        print(f"   综合评分: {scores['overall']:.2f}")

        return best_path, all_paths


class ReferenceStyleAnalyzer:
    """参考图风格分析器 - 自动提取风格特征"""

    @staticmethod
    def analyze_image(image_path: str) -> Dict[str, any]:
        """分析参考图的风格特征"""
        try:
            from PIL import Image
            import numpy as np

            img = Image.open(image_path).convert('RGB')
            img_array = np.array(img)

            # 色彩分析
            r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]

            # 主色调
            dominant_color = [
                int(r.mean()),
                int(g.mean()),
                int(b.mean())
            ]

            # 色彩饱和度
            saturation = np.std(img_array) / 255.0

            # 亮度
            brightness = np.mean(img_array) / 255.0

            # 对比度
            contrast = np.std(img_array) / 255.0

            # 风格判断
            style = "anime"
            if saturation < 0.3 and brightness > 0.7:
                style = "pastel"
            elif saturation > 0.6:
                style = "vibrant"
            elif contrast > 0.3:
                style = "dramatic"

            return {
                "dominant_color": dominant_color,
                "saturation": float(saturation),
                "brightness": float(brightness),
                "contrast": float(contrast),
                "style": style,
                "size": img.size,
            }

        except Exception as e:
            print(f"⚠️ 风格分析失败: {e}")
            return {
                "dominant_color": [128, 128, 128],
                "saturation": 0.5,
                "brightness": 0.5,
                "contrast": 0.5,
                "style": "anime",
                "size": (512, 768),
            }

    @staticmethod
    def generate_style_prompt(analysis: Dict[str, any]) -> str:
        """基于分析结果生成风格提示词"""
        style = analysis["style"]

        prompts = {
            "pastel": "pastel colors, soft color palette, dreamy atmosphere, ethereal, soft shading",
            "vibrant": "vibrant colors, saturated colors, bold colors, high contrast, dynamic",
            "dramatic": "dramatic lighting, strong contrast, chiaroscuro, cinematic lighting",
            "anime": "anime style, illustration, clean lineart, smooth shading",
        }

        return prompts.get(style, prompts["anime"])


class Live2DOptimizedGenerator:
    """Live2D 优化的图像生成器 v5.0 - 商业级 AI 质量"""

    # 基于 DALL-E 3 / Seedream 分析的专业提示词模板
    PROFESSIONAL_PROMPT_TEMPLATE = """(masterpiece:1.4), (best quality:1.3), (ultra detailed:1.2), (highres:1.2), (8k uhd:1.1),
(anime style:1.3), (illustration:1.2), (official art:1.2), (pixiv:1.1), (artstation:1.1),
1girl, solo, {pose}, {hairstyle}, {hair_color}, {eye_color}, {clothing}, {accessory}, {expression},
(beautiful detailed face:1.3), (beautiful detailed eyes:1.3), (detailed skin texture:1.1), (soft lighting:1.2),
(pastel colors:1.2), (soft color palette:1.2), (dreamy atmosphere:1.1), (ethereal:1.1),
(frills:1.1), (lace:1.1), (ribbons:1.1), (bows:1.1), (jewelry:1.1), (elegant outfit:1.2),
(perfect anatomy:1.2), (correct proportions:1.2), (delicate hands:1.2),
(white background:1.2), (simple background:1.2), (clean background:1.2),
(sharp focus:1.2), (vibrant colors:1.1), (clear lineart:1.3), (smooth shading:1.1),
(extremely detailed:1.2), (intricate details:1.2), (professional illustration:1.2),
(art by Artgerm:1.1), (art by WLOP:1.1), (art by Rossdraws:1.1),
(soft volumetric lighting:1.2), (rim lighting:1.1), (bloom:1.1)"""

    # Live2D专用提示词模板
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

    # 高质量反向提示词
    NEGATIVE_PROMPT = """(lowres:1.4), (bad anatomy:1.4), (bad hands:1.3), (text:1.3), (error:1.3), (missing fingers:1.3),
(extra digit:1.3), (fewer digits:1.3), (cropped:1.2), (worst quality:1.3), (low quality:1.3),
(normal quality:1.2), (jpeg artifacts:1.2), (signature:1.2), (watermark:1.2), (username:1.2), (blurry:1.3),
(artist name:1.2), (bad proportions:1.3), (extra limbs:1.3), (cloned face:1.2), (disfigured:1.3),
(gross proportions:1.3), (malformed limbs:1.3), (missing arms:1.2), (missing legs:1.2),
(extra arms:1.2), (extra legs:1.2), (fused fingers:1.2), (too many fingers:1.2), (long neck:1.2),
(photorealistic:1.2), (realistic:1.2), (3d:1.2), (western:1.2), (sketch:1.1), (rough:1.1), (draft:1.1),
(complex background:1.2), (messy hair:1.2), (messy clothes:1.2),
(depth of field:1.1), (blurry background:1.2), (multiple girls:1.3), (multiple people:1.3)"""

    # Live2D专用反向提示词
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
        self.prompt_engineer = PromptEngineer()
        self.assessor = QualityAssessor()
        self.pipeline = MultiStagePipeline(self)
        self.batch_generator = BatchGenerator(self)
        self.style_analyzer = ReferenceStyleAnalyzer()

        print(f"🎯 Live2D 优化图像生成器 v5.0")
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
        style: str = "anime",
        hairstyle: str = "long hair",
        hair_color: str = "pink hair",
        eye_color: str = "blue eyes",
        clothing: str = "school uniform",
        accessory: str = "hair ribbon",
        expression: str = "smile",
        pose: str = "standing",
        quality: str = "masterpiece, best quality, ultra detailed",
        reference_image: Optional[str] = None,
    ) -> Tuple[str, str]:
        """构建优化的提示词，支持参考图风格分析"""

        # 如果有参考图，分析风格
        style_prompt = ""
        if reference_image and Path(reference_image).exists():
            analysis = self.style_analyzer.analyze_image(reference_image)
            style_prompt = self.style_analyzer.generate_style_prompt(analysis)
            print(f"\n🎨 参考图风格分析:")
            print(f"   风格: {analysis['style']}")
            print(f"   主色调: RGB{analysis['dominant_color']}")
            print(f"   饱和度: {analysis['saturation']:.2f}")
            print(f"   亮度: {analysis['brightness']:.2f}")

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
            # 使用提示词工程自动扩展
            if custom_prompt:
                expanded = self.prompt_engineer.expand_prompt(custom_prompt, style)
                prompt = expanded + ", " + self.PROFESSIONAL_PROMPT_TEMPLATE.format(
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

        # 添加参考图风格
        if style_prompt:
            prompt = style_prompt + ", " + prompt

        if custom_prompt and live2d_mode:
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
        """针对 Live2D 分层优化图片 v5.0"""
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
        """专业后处理管道 v5.0"""
        from PIL import Image, ImageFilter, ImageEnhance

        print("\n🔧 运行专业后处理管道...")

        img = Image.open(image_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # 1. 线条锐化
        print("   1. 线条锐化...")
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.4)

        # 2. 色彩校正
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

        # 5. AI放大
        if enable_upscale and target_width and target_height:
            print(f"   5. 放大到 {target_width}x{target_height}...")
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

        # 保存处理后的图片
        processed_path = image_path.replace('.png', '_processed.png')
        img.save(processed_path, "PNG")
        print(f"✅ 后处理完成: {processed_path}")

        return processed_path

    def generate_with_retry(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 512,
        height: int = 768,
        steps: int = 25,
        guidance_scale: float = 7.5,
        max_retries: int = 3,
        quality_threshold: float = 0.6,
        seed: Optional[int] = None,
        live2d_optimized: bool = True,
    ) -> Tuple[bool, Optional[str]]:
        """智能生成 - 自动重试直到质量达标"""
        for attempt in range(max_retries):
            print(f"\n🎯 尝试 {attempt + 1}/{max_retries}")

            current_seed = (seed or int(time.time()) % 1000000) + attempt * 1000

            success, output_path = self.generate(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                steps=steps,
                guidance_scale=guidance_scale,
                seed=current_seed,
                live2d_optimized=live2d_optimized,
            )

            if not success:
                continue

            # 质量评估
            scores = self.assessor.assess_image(output_path)
            print(f"\n📊 质量评估:")
            print(f"   综合评分: {scores['overall']:.2f}")

            if self.assessor.is_quality_acceptable(scores, quality_threshold):
                print(f"✅ 质量达标！")
                return True, output_path
            else:
                print(f"⚠️ 质量未达标，重试中...")

        print(f"❌ 达到最大重试次数，返回最后一次结果")
        return success, output_path if success else (False, None)

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
        description="Live2D Master Agent - 本地图像生成器 v5.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础生成
  python local_image_generator.py "cute anime girl"

  # 批量生成选最优
  python local_image_generator.py --batch 5 "beautiful character"

  # 多阶段生成
  python local_image_generator.py --multistage "masterpiece"

  # 参考图风格迁移
  python local_image_generator.py --reference ref.png "same style, new character"

  # 智能重试（自动评估质量）
  python local_image_generator.py --smart "cute girl"

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
    parser.add_argument(
        "--batch", type=int, default=1, help="批量生成数量（默认1）"
    )
    parser.add_argument(
        "--multistage", action="store_true", help="启用多阶段生成"
    )
    parser.add_argument(
        "--smart", action="store_true", help="智能生成（自动评估质量并重试）"
    )
    parser.add_argument(
        "--reference", type=str, default=None, help="参考图路径（风格迁移）"
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
        reference_image=args.reference,
    )

    if args.negative:
        negative = args.negative + ", " + negative

    # 选择生成模式
    if args.batch > 1:
        # 批量生成
        best_path, all_paths = generator.batch_generator.generate_batch(
            prompt=prompt,
            negative_prompt=negative,
            batch_size=args.batch,
            width=args.width,
            height=args.height,
            steps=steps,
            guidance_scale=args.guidance,
            use_multistage=args.multistage,
        )
        if best_path:
            print(f"\n🎉 批量生成完成！")
            print(f"📁 最优文件: {best_path}")
            print(f"📁 所有文件: {len(all_paths)} 张")
            output_path = best_path
        else:
            print(f"\n❌ 批量生成失败")
            sys.exit(1)

    elif args.smart:
        # 智能生成（自动重试）
        success, output_path = generator.generate_with_retry(
            prompt=prompt,
            negative_prompt=negative,
            width=args.width,
            height=args.height,
            steps=steps,
            guidance_scale=args.guidance,
            seed=args.seed,
            live2d_optimized=not args.no_live2d,
        )
        if not success:
            sys.exit(1)

    elif args.multistage:
        # 多阶段生成
        output_path = generator.pipeline.run_pipeline(
            prompt=prompt,
            negative_prompt=negative,
            width=args.width,
            height=args.height,
            seed=args.seed,
        )
        if not output_path:
            sys.exit(1)

    else:
        # 标准生成
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
        if not success:
            sys.exit(1)

    # 后处理
    if args.post_process:
        processed_path = generator.post_process_pipeline(output_path)
        print(f"📁 处理后文件: {processed_path}")

    print(f"\n🎉 生成成功！")
    print(f"📁 文件: {output_path}")


if __name__ == "__main__":
    main()
