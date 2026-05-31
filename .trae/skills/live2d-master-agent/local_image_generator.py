#!/usr/bin/env python3
"""
Live2D Master Agent - 图像生成器 v6.0
支持本地 Stable Diffusion + 商汤SenseNova云端 + 多种免费服务

核心升级：
- 🎯 商业级 AI 质量（匹配 DALL-E 3 / Seedream）
- ☁️ 商汤SenseNova云端生成（OpenAI兼容）
- 🦴 Live2D分层专用模式（全身照+部件分离+遮挡补全）
- 🔧 一键生成→自动分层
- 🔄 多阶段生成管道（草稿→精修→超分）
- 🤖 智能质量评估 + 自动重试（7维度Live2D适配度）
- 🎨 参考图风格自动分析
- 📊 批量生成选最优
- 🔐 安全审计修复（7项安全问题）

使用方法：
    # 基础生成
    python local_image_generator.py "cute anime girl"
    
    # 商汤SenseNova + Live2D分层专用
    python local_image_generator.py --provider sensenova --live2d-rig "蓝发猫耳少女"
    
    # 一键生成+自动分层
    python local_image_generator.py --provider sensenova --live2d-rig --auto-layer "蓝发猫耳少女"
    
    # 本地SD多阶段生成
    python local_image_generator.py --model "gsdf/Counterfeit-V3.0" --quality ultra --batch 5 "beautiful character"
    
    # 参考图风格迁移
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
    """GPT-4 风格提示词工程 - 自动扩展和优化提示词 v6.0"""

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

    # Live2D 分层专用提示词 - 基于官方文档和社区最佳实践
    LIVE2D_RIGGING_KEYWORDS = {
        "full_body": "(full body:1.3), (standing straight:1.2), (front view:1.2), (looking at viewer:1.2), (arms at sides:1.1), (legs visible:1.2), (feet visible:1.1)",
        "part_separation": "(distinct part separation:1.2), (clear boundaries between hair and face:1.2), (separate bangs:1.1), (separate side hair:1.1), (separate back hair:1.1), (separate arms:1.1), (separate legs:1.1)",
        "occlusion_fill": "(complete body parts under clothing:1.2), (hidden parts drawn:1.2), (complete limbs behind hair:1.1), (complete body under outfit:1.1), (no cut-off parts:1.2)",
        "layer_friendly": "(flat coloring:1.2), (cel shading:1.2), (minimal gradients:1.2), (solid colors:1.2), (no soft blending between parts:1.2), (hard edges:1.3)",
        "symmetry": "(symmetrical face:1.2), (symmetrical eyes:1.2), (centered composition:1.2), (balanced proportions:1.2)",
        "rigging_ready": "(Live2D rigging ready:1.2), (VTuber model:1.1), (clean lineart:1.3), (white background:1.2), (simple background:1.2), (isolated character:1.2)",
    }

    # 角色特征解析规则 v6.0 - 支持自然语言解析
    CHARACTER_PATTERNS = {
        "hair_color": {
            "蓝": "blue", "藍": "blue", "blue": "blue",
            "红": "red", "紅": "red", "red": "red",
            "金": "blonde", "黄": "blonde", "blonde": "blonde", "yellow": "blonde",
            "黑": "black", "black": "black",
            "白": "white", "white": "white",
            "粉": "pink", "pink": "pink",
            "紫": "purple", "purple": "purple",
            "绿": "green", "綠": "green", "green": "green",
            "银": "silver", "銀": "silver", "silver": "silver",
            "橙": "orange", "orange": "orange",
            "灰": "grey", "gray": "grey", "grey": "grey",
        },
        "hair_style": {
            "长发": "long hair", "long hair": "long hair", "long": "long hair",
            "短发": "short hair", "short hair": "short hair", "short": "short hair",
            "双马尾": "twintails", "twintails": "twintails",
            "单马尾": "ponytail", "ponytail": "ponytail",
            "丸子头": "bun", "bun": "bun",
            "卷发": "curly hair", "curly": "curly hair",
            "波浪发": "wavy hair", "wavy": "wavy hair",
            "直发": "straight hair", "straight": "straight hair",
            "波波头": "bob cut", "bob": "bob cut",
            "姬发式": "hime cut", "hime": "hime cut",
        },
        "eye_color": {
            "蓝眼": "blue eyes", "蓝眼睛": "blue eyes", "blue eyes": "blue eyes",
            "红眼": "red eyes", "红眼睛": "red eyes", "red eyes": "red eyes",
            "绿眼": "green eyes", "绿眼睛": "green eyes", "green eyes": "green eyes",
            "紫眼": "purple eyes", "紫眼睛": "purple eyes", "purple eyes": "purple eyes",
            "金眼": "golden eyes", "金眼睛": "golden eyes", "golden eyes": "golden eyes",
            "粉眼": "pink eyes", "粉眼睛": "pink eyes", "pink eyes": "pink eyes",
        },
        "features": {
            "猫耳": "cat ears", "cat ears": "cat ears", "nekomimi": "cat ears",
            "狐耳": "fox ears", "fox ears": "fox ears",
            "兽耳": "animal ears", "animal ears": "animal ears",
            "尾巴": "tail", "tail": "tail",
            "翅膀": "wings", "wings": "wings",
            "角": "horns", "horns": "horns",
            "眼镜": "glasses", "glasses": "glasses",
            "眼罩": "eyepatch", "eyepatch": "eyepatch",
        },
        "expression": {
            "微笑": "smile", "smile": "smile", "笑": "smile",
            "开心": "happy", "happy": "happy",
            "可爱": "cute", "cute": "cute",
            "严肃": "serious", "serious": "serious",
            "害羞": "shy", "shy": "shy", " blush": "blushing",
            "冷酷": "cool", "cool": "cool",
            "惊讶": "surprised", "surprised": "surprised",
        },
        "clothing": {
            "校服": "school uniform", "school uniform": "school uniform",
            "水手服": "serafuku", "serafuku": "serafuku", "sailor uniform": "sailor uniform",
            "连衣裙": "dress", "dress": "dress",
            "和服": "kimono", "kimono": "kimono",
            "女仆装": "maid outfit", "maid": "maid outfit",
            "哥特": "gothic", "gothic": "gothic",
            "洛丽塔": "lolita fashion", "lolita": "lolita fashion",
            "运动服": "sportswear", "sportswear": "sportswear",
        }
    }

    @classmethod
    def parse_character_from_text(cls, text: str) -> Dict[str, str]:
        """从自然语言解析角色特征 v6.0"""
        text_lower = text.lower()
        character = {
            "hair_color": "",
            "hair_style": "",
            "eye_color": "",
            "features": [],
            "expression": "",
            "clothing": "",
            "raw": text
        }

        # 解析发色
        for key, value in cls.CHARACTER_PATTERNS["hair_color"].items():
            if key in text or key in text_lower:
                character["hair_color"] = value
                break

        # 解析发型
        for key, value in cls.CHARACTER_PATTERNS["hair_style"].items():
            if key in text or key in text_lower:
                character["hair_style"] = value
                break

        # 解析眼睛颜色
        for key, value in cls.CHARACTER_PATTERNS["eye_color"].items():
            if key in text or key in text_lower:
                character["eye_color"] = value
                break

        # 解析特征
        for key, value in cls.CHARACTER_PATTERNS["features"].items():
            if key in text or key in text_lower:
                if value not in character["features"]:
                    character["features"].append(value)

        # 解析表情
        for key, value in cls.CHARACTER_PATTERNS["expression"].items():
            if key in text or key in text_lower:
                character["expression"] = value
                break

        # 解析服装
        for key, value in cls.CHARACTER_PATTERNS["clothing"].items():
            if key in text or key in text_lower:
                character["clothing"] = value
                break

        return character

    @classmethod
    def build_prompt_from_character(cls, character: Dict[str, str],
                                     style: str = "anime",
                                     live2d_mode: bool = True,
                                     live2d_rigging: bool = False) -> Tuple[str, str]:
        """从结构化角色构建Prompt v6.0

        Args:
            character: 角色特征字典
            style: 风格
            live2d_mode: 是否启用Live2D基础优化
            live2d_rigging: 是否启用Live2D分层专用优化（全身照+部件分离+遮挡补全）
        """
        parts = []

        # 质量前缀
        parts.append("(masterpiece:1.4), (best quality:1.3), (ultra detailed:1.2)")

        # 基础
        parts.append("1girl, solo")

        # 发色
        if character.get("hair_color"):
            parts.append(f"({character['hair_color']} hair:1.2)")

        # 发型
        if character.get("hair_style"):
            parts.append(f"({character['hair_style']}:1.1)")

        # 眼睛
        if character.get("eye_color"):
            parts.append(f"({character['eye_color']}:1.2)")

        # 特征
        for feature in character.get("features", []):
            parts.append(f"({feature}:1.2)")

        # 表情
        if character.get("expression"):
            parts.append(f"({character['expression']}:1.1)")

        # 服装
        if character.get("clothing"):
            parts.append(f"({character['clothing']}:1.1)")

        # 原始描述补充
        raw = character.get("raw", "")
        if raw:
            # 移除已解析的关键词，保留其他描述
            cleaned = raw
            for category in cls.CHARACTER_PATTERNS.values():
                for key in category.keys():
                    cleaned = cleaned.replace(key, "")
            cleaned = cleaned.strip()
            if cleaned and len(cleaned) > 2:
                parts.append(cleaned)

        # 风格
        if style == "anime":
            parts.append("(anime style:1.3), (illustration:1.2)")
        elif style == "pastel":
            parts.append("(pastel colors:1.3), (soft shading:1.2)")

        # Live2D分层专用优化（最高优先级）
        if live2d_rigging:
            parts.extend([
                cls.LIVE2D_RIGGING_KEYWORDS["full_body"],
                cls.LIVE2D_RIGGING_KEYWORDS["part_separation"],
                cls.LIVE2D_RIGGING_KEYWORDS["occlusion_fill"],
                cls.LIVE2D_RIGGING_KEYWORDS["layer_friendly"],
                cls.LIVE2D_RIGGING_KEYWORDS["symmetry"],
                cls.LIVE2D_RIGGING_KEYWORDS["rigging_ready"],
            ])
        elif live2d_mode:
            # 基础Live2D优化
            parts.extend([
                "(clean lineart:1.3)", "(clear edges:1.3)",
                "(flat colors:1.2)", "(white background:1.2)",
                "(simple background:1.2)", "(front view:1.2)",
                "(perfect anatomy:1.2)", "(beautiful detailed face:1.3)",
                "(beautiful detailed eyes:1.3)"
            ])

        # 艺术家
        artists = cls.ARTISTS.get(style, cls.ARTISTS["anime"])
        parts.append(f"({artists[0]}:1.1), ({artists[1]}:1.1)")

        # 质量后缀
        parts.append("(sharp focus:1.2), (vibrant colors:1.1)")

        prompt = ", ".join(parts)

        # 负向提示词
        negative = """(lowres:1.4), (bad anatomy:1.4), (bad hands:1.3), (text:1.3),
(worst quality:1.3), (low quality:1.3), (blurry:1.3),
(bad proportions:1.3), (extra limbs:1.3), (disfigured:1.3),
(photorealistic:1.2), (3d:1.2), (western:1.2),
(complex background:1.2), (multiple girls:1.3)"""

        if live2d_rigging:
            # Live2D分层专用反向提示词
            negative += """, (profile view:1.2), (side view:1.2), (back view:1.2),
(open mouth:1.2), (talking:1.2), (dynamic pose:1.2), (action pose:1.2),
(sitting:1.2), (lying down:1.2), (partial body:1.3), (cropped:1.3),
(gradient shading:1.2), (soft shading:1.2), (painterly:1.2), (watercolor:1.2),
(messy hair:1.2), (messy clothes:1.2), (torn clothes:1.2),
(missing limbs:1.3), (incomplete body:1.3), (cut-off:1.3),
(depth of field:1.2), (blurry background:1.2), (bokeh:1.2)"""
        elif live2d_mode:
            negative += """, (profile view:1.2), (side view:1.2), (back view:1.2),
(open mouth:1.2), (dynamic pose:1.2), (sitting:1.2),
(gradient shading:1.2), (painterly:1.2), (watercolor:1.2)"""

        return prompt, negative

    @classmethod
    def expand_prompt(cls, user_prompt: str, style: str = "anime") -> str:
        """自动扩展提示词 - 模拟 GPT-4 提示词工程"""
        # 先尝试解析角色特征
        character = cls.parse_character_from_text(user_prompt)

        # 如果解析到了特征，使用结构化构建
        if any([character.get("hair_color"), character.get("features"),
                character.get("clothing")]):
            prompt, _ = cls.build_prompt_from_character(character, style)
            return prompt

        # 否则使用传统扩展
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
    """智能质量评估器 v6.0 - Live2D适配度专业评估"""

    # Live2D适配度评估维度权重
    LIVE2D_WEIGHTS = {
        "face_quality": 0.25,      # 脸部质量（对称性、清晰度）
        "edge_clarity": 0.20,      # 边缘清晰度（分层关键）
        "background_purity": 0.20, # 背景纯净度
        "color_separation": 0.15,  # 颜色分离度
        "sharpness": 0.10,         # 整体清晰度
        "contrast": 0.10,          # 对比度
    }

    # Live2D分层专用评估维度权重（用于rigging-ready图片）
    LIVE2D_RIGGING_WEIGHTS = {
        "full_body_visibility": 0.20,   # 全身可见性（头到脚）
        "part_boundary_clarity": 0.20,  # 部件边界清晰度（头发/脸/身体分离）
        "symmetry": 0.15,               # 对称性（正面站立）
        "edge_clarity": 0.15,           # 边缘清晰度
        "color_flatness": 0.10,         # 颜色平坦度（适合分层）
        "background_purity": 0.10,      # 背景纯净度
        "occlusion_completeness": 0.10, # 遮挡区域完整性
    }

    @staticmethod
    def assess_image(image_path: str, live2d_mode: bool = True, live2d_rigging: bool = False) -> Dict[str, float]:
        """
        评估图片质量 v6.0
        返回分数字典：包含基础质量 + Live2D适配度

        Args:
            image_path: 图片路径
            live2d_mode: 是否启用Live2D基础评估
            live2d_rigging: 是否启用Live2D分层专用评估（全身照+部件分离+遮挡补全）
        """
        try:
            from PIL import Image
            import numpy as np

            img = Image.open(image_path).convert('RGB')
            img_array = np.array(img)
            h, w = img_array.shape[:2]

            # ========== 基础质量评估 ==========
            # 1. 清晰度评估（拉普拉斯算子方差）
            from scipy import ndimage
            laplacian = ndimage.laplace(img_array.mean(axis=2))
            sharpness = float(np.var(laplacian))
            sharpness_score = min(sharpness / 500, 1.0)

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

            # ========== Live2D分层专用评估 ==========
            if live2d_rigging:
                # 1. 全身可见性（检测从头到脚是否有内容）
                # 分析垂直方向上的内容分布
                row_means = img_array.mean(axis=(1, 2))
                # 检测顶部和底部是否有内容（非背景色）
                top_region = row_means[:h//10].mean()
                bottom_region = row_means[-h//10:].mean()
                center_region = row_means[h//3:2*h//3].mean()
                # 如果顶部和底部都有内容，说明是全身照
                full_body_visibility = 0.5
                if top_region < center_region * 0.9 and bottom_region < center_region * 0.9:
                    full_body_visibility = 0.9  # 全身照
                elif top_region < center_region * 0.9:
                    full_body_visibility = 0.6  # 半身照

                # 2. 部件边界清晰度（检测头发/脸/身体的边界）
                # 使用边缘检测评估不同区域的边界清晰度
                sobel_h = ndimage.sobel(img_array.mean(axis=2), axis=0)
                sobel_v = ndimage.sobel(img_array.mean(axis=2), axis=1)
                edge_strength = np.sqrt(sobel_h**2 + sobel_v**2)
                # 分析上半部分（脸部+头发）的边缘密度
                upper_edges = edge_strength[:h//2, :].mean()
                part_boundary_clarity = min(upper_edges / 30, 1.0)

                # 3. 对称性（左右对比）
                left_half = img_array[:, :w//2]
                right_half = np.fliplr(img_array[:, w//2:])
                min_w = min(left_half.shape[1], right_half.shape[1])
                symmetry = 1.0 - np.mean(np.abs(
                    left_half[:, :min_w].astype(float) - right_half[:, :min_w].astype(float)
                )) / 255.0

                # 4. 边缘清晰度（整体）
                edge_clarity = min(edge_strength.mean() / 30, 1.0)

                # 5. 颜色平坦度（颜色量化后的方差小说明颜色平坦）
                try:
                    from sklearn.cluster import KMeans
                    pixels = img_array.reshape(-1, 3)
                    sample_size = min(5000, len(pixels))
                    sample = pixels[np.random.choice(len(pixels), sample_size, replace=False)]
                    kmeans = KMeans(n_clusters=32, random_state=42, n_init=10)
                    kmeans.fit(sample)
                    # 计算每个聚类的方差，方差小说明颜色平坦
                    cluster_vars = []
                    for i in range(32):
                        cluster_pixels = sample[kmeans.labels_ == i]
                        if len(cluster_pixels) > 10:
                            cluster_vars.append(np.var(cluster_pixels))
                    avg_var = np.mean(cluster_vars) if cluster_vars else 1000
                    color_flatness = max(0, min(1, 1.0 - avg_var / 2000))
                except ImportError:
                    color_flatness = 0.7

                # 6. 背景纯净度
                border = np.concatenate([
                    img_array[0, :].flatten(),
                    img_array[-1, :].flatten(),
                    img_array[:, 0].flatten(),
                    img_array[:, -1].flatten()
                ])
                bg_uniformity = 1.0 - min(np.std(border) / 80, 1.0)
                background_purity = bg_uniformity

                # 7. 遮挡区域完整性（检测中间区域是否有被遮挡的内容）
                # 分析中心区域的颜色丰富度，丰富度高说明有完整身体
                center_region_colors = img_array[h//4:3*h//4, w//4:3*w//4]
                color_variety = np.std(center_region_colors)
                occlusion_completeness = min(color_variety / 100, 1.0)

                # Live2D分层综合评分
                rigging_scores = {
                    "full_body_visibility": full_body_visibility,
                    "part_boundary_clarity": part_boundary_clarity,
                    "symmetry": symmetry,
                    "edge_clarity": edge_clarity,
                    "color_flatness": color_flatness,
                    "background_purity": background_purity,
                    "occlusion_completeness": occlusion_completeness,
                }

                rigging_overall = sum(
                    rigging_scores[k] * QualityAssessor.LIVE2D_RIGGING_WEIGHTS[k]
                    for k in QualityAssessor.LIVE2D_RIGGING_WEIGHTS.keys()
                )

                return {
                    "overall": rigging_overall,
                    "sharpness": sharpness_score,
                    "color_balance": color_balance,
                    "contrast": contrast_score,
                    "noise_level": noise_score,
                    "full_body_visibility": full_body_visibility,
                    "part_boundary_clarity": part_boundary_clarity,
                    "symmetry": symmetry,
                    "edge_clarity": edge_clarity,
                    "color_flatness": color_flatness,
                    "background_purity": background_purity,
                    "occlusion_completeness": occlusion_completeness,
                    "live2d_rigging_score": rigging_overall,
                }

            # ========== Live2D基础适配度评估 ==========
            elif live2d_mode:
                # 5. 脸部质量评估（检测上半部分的对称性和清晰度）
                face_region = img_array[:h//2, :]
                face_laplacian = ndimage.laplace(face_region.mean(axis=2))
                face_sharpness = min(np.var(face_laplacian) / 300, 1.0)

                # 脸部对称性（左右对比）
                face_left = face_region[:, :w//2]
                face_right = np.fliplr(face_region[:, w//2:])
                min_w = min(face_left.shape[1], face_right.shape[1])
                face_symmetry = 1.0 - np.mean(np.abs(
                    face_left[:, :min_w].astype(float) - face_right[:, :min_w].astype(float)
                )) / 255.0
                face_quality = (face_sharpness * 0.6 + face_symmetry * 0.4)

                # 6. 边缘清晰度（Sobel算子）
                sobel_h = ndimage.sobel(img_array.mean(axis=2), axis=0)
                sobel_v = ndimage.sobel(img_array.mean(axis=2), axis=1)
                edge_strength = np.sqrt(sobel_h**2 + sobel_v**2).mean()
                edge_clarity = min(edge_strength / 30, 1.0)

                # 7. 背景纯净度（边缘区域颜色方差）
                border = np.concatenate([
                    img_array[0, :].flatten(),
                    img_array[-1, :].flatten(),
                    img_array[:, 0].flatten(),
                    img_array[:, -1].flatten()
                ])
                bg_uniformity = 1.0 - min(np.std(border) / 80, 1.0)
                background_purity = bg_uniformity

                # 8. 颜色分离度（颜色量化后的区域数）
                try:
                    from sklearn.cluster import KMeans
                    pixels = img_array.reshape(-1, 3)
                    sample_size = min(5000, len(pixels))
                    sample = pixels[np.random.choice(len(pixels), sample_size, replace=False)]
                    kmeans = KMeans(n_clusters=16, random_state=42, n_init=10)
                    kmeans.fit(sample)
                    n_colors = len(np.unique(kmeans.labels_))
                    # 颜色区域适中（8-12种）最适合Live2D
                    color_separation = 1.0 - abs(n_colors - 10) / 10.0
                    color_separation = max(0, min(1, color_separation))
                except ImportError:
                    color_separation = 0.7

                # Live2D综合评分
                live2d_scores = {
                    "face_quality": face_quality,
                    "edge_clarity": edge_clarity,
                    "background_purity": background_purity,
                    "color_separation": color_separation,
                    "sharpness": sharpness_score,
                    "contrast": contrast_score,
                }

                live2d_overall = sum(
                    live2d_scores[k] * QualityAssessor.LIVE2D_WEIGHTS[k]
                    for k in QualityAssessor.LIVE2D_WEIGHTS.keys()
                )

                return {
                    "overall": live2d_overall,
                    "sharpness": sharpness_score,
                    "color_balance": color_balance,
                    "contrast": contrast_score,
                    "noise_level": noise_score,
                    "face_quality": face_quality,
                    "edge_clarity": edge_clarity,
                    "background_purity": background_purity,
                    "color_separation": color_separation,
                    "live2d_score": live2d_overall,
                }
            else:
                # 非Live2D模式：基础评分
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
            return {
                "overall": 0.7, "sharpness": 0.7, "color_balance": 0.7,
                "contrast": 0.7, "noise_level": 0.7,
                "face_quality": 0.7, "edge_clarity": 0.7,
                "background_purity": 0.7, "color_separation": 0.7,
                "live2d_score": 0.7,
                "full_body_visibility": 0.7, "part_boundary_clarity": 0.7,
                "symmetry": 0.7, "color_flatness": 0.7,
                "occlusion_completeness": 0.7, "live2d_rigging_score": 0.7,
            }
        except Exception as e:
            print(f"⚠️ 质量评估失败: {e}")
            return {
                "overall": 0.5, "sharpness": 0.5, "color_balance": 0.5,
                "contrast": 0.5, "noise_level": 0.5,
                "face_quality": 0.5, "edge_clarity": 0.5,
                "background_purity": 0.5, "color_separation": 0.5,
                "live2d_score": 0.5,
                "full_body_visibility": 0.5, "part_boundary_clarity": 0.5,
                "symmetry": 0.5, "color_flatness": 0.5,
                "occlusion_completeness": 0.5, "live2d_rigging_score": 0.5,
            }

    @staticmethod
    def is_quality_acceptable(scores: Dict[str, float], threshold: float = 0.6,
                               live2d_mode: bool = True, live2d_rigging: bool = False) -> bool:
        """判断质量是否可接受 v6.0"""
        if live2d_rigging and "live2d_rigging_score" in scores:
            return scores["live2d_rigging_score"] >= threshold
        if live2d_mode and "live2d_score" in scores:
            return scores["live2d_score"] >= threshold
        return scores["overall"] >= threshold

    @staticmethod
    def get_best_image(image_paths: List[str], live2d_mode: bool = True, live2d_rigging: bool = False) -> Tuple[str, Dict[str, float]]:
        """从多张图片中选择质量最好的一张 v6.0"""
        best_path = None
        best_score = -1
        best_scores = None

        for path in image_paths:
            scores = QualityAssessor.assess_image(path, live2d_mode=live2d_mode, live2d_rigging=live2d_rigging)
            # 优先使用对应的评分
            if live2d_rigging and "live2d_rigging_score" in scores:
                score = scores["live2d_rigging_score"]
            elif live2d_mode and "live2d_score" in scores:
                score = scores["live2d_score"]
            else:
                score = scores["overall"]
            if score > best_score:
                best_score = score
                best_path = path
                best_scores = scores

        return best_path, best_scores

    @staticmethod
    def generate_report(scores: Dict[str, float], live2d_rigging: bool = False) -> str:
        """生成质量评估报告"""
        lines = ["📊 质量评估报告:", "=" * 40]

        if live2d_rigging and "live2d_rigging_score" in scores:
            lines.append(f"Live2D分层适配度: {scores['live2d_rigging_score']:.1%}")
            lines.append(f"  全身可见性:   {scores['full_body_visibility']:.1%}")
            lines.append(f"  部件边界清晰度: {scores['part_boundary_clarity']:.1%}")
            lines.append(f"  对称性:       {scores['symmetry']:.1%}")
            lines.append(f"  边缘清晰度:   {scores['edge_clarity']:.1%}")
            lines.append(f"  颜色平坦度:   {scores['color_flatness']:.1%}")
            lines.append(f"  背景纯净度:   {scores['background_purity']:.1%}")
            lines.append(f"  遮挡完整性:   {scores['occlusion_completeness']:.1%}")
            lines.append("")
        elif "live2d_score" in scores:
            lines.append(f"Live2D适配度: {scores['live2d_score']:.1%}")
            lines.append(f"  脸部质量:   {scores['face_quality']:.1%}")
            lines.append(f"  边缘清晰度: {scores['edge_clarity']:.1%}")
            lines.append(f"  背景纯净度: {scores['background_purity']:.1%}")
            lines.append(f"  颜色分离度: {scores['color_separation']:.1%}")
            lines.append("")

        lines.append(f"综合评分: {scores['overall']:.1%}")
        lines.append(f"  清晰度:   {scores['sharpness']:.1%}")
        lines.append(f"  色彩平衡: {scores['color_balance']:.1%}")
        lines.append(f"  对比度:   {scores['contrast']:.1%}")
        lines.append(f"  噪声水平: {scores['noise_level']:.1%}")

        if live2d_rigging:
            status = "✅ 通过" if scores.get("live2d_rigging_score", scores["overall"]) >= 0.6 else "❌ 未通过"
        else:
            status = "✅ 通过" if scores.get("live2d_score", scores["overall"]) >= 0.6 else "❌ 未通过"
        lines.append(f"\n{status}")

        return "\n".join(lines)


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
    """批量生成器 v6.0 - 多维度选优 + 详细报告"""

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
        live2d_mode: bool = True,
        min_live2d_score: float = 0.6,
    ) -> Tuple[Optional[str], List[str], Dict]:
        """
        批量生成并选择最优 v6.0

        Returns:
            (best_path, all_paths, report)
        """
        print(f"\n🎯 批量生成 {batch_size} 张图片...")
        print(f"   Live2D模式: {'是' if live2d_mode else '否'}")
        print(f"   最低适配度: {min_live2d_score:.0%}")

        all_paths = []
        all_scores = []

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
                # 评估
                scores = self.assessor.assess_image(path, live2d_mode=live2d_mode)
                all_scores.append(scores)

                # 显示当前评分
                if live2d_mode and "live2d_score" in scores:
                    print(f"   Live2D适配度: {scores['live2d_score']:.1%}")
                else:
                    print(f"   综合评分: {scores['overall']:.1%}")

        if not all_paths:
            return None, [], {"error": "所有生成失败"}

        # 选择最优
        print(f"\n🏆 从 {len(all_paths)} 张中选择最优...")
        best_path, best_scores = self.assessor.get_best_image(
            all_paths, live2d_mode=live2d_mode
        )

        # 生成详细报告
        report = self._generate_batch_report(all_paths, all_scores, best_path, live2d_mode)
        print(report["summary"])

        # 检查是否达到最低标准
        score_key = "live2d_score" if live2d_mode else "overall"
        if best_scores.get(score_key, 0) < min_live2d_score:
            print(f"\n⚠️ 警告: 最优图片 {score_key}={best_scores.get(score_key, 0):.1%} 低于最低标准 {min_live2d_score:.0%}")
            print("   建议: 调整提示词或使用多阶段生成")

        return best_path, all_paths, report

    def _generate_batch_report(self, paths: List[str], scores: List[Dict],
                                best_path: str, live2d_mode: bool) -> Dict:
        """生成批量生成报告"""
        score_key = "live2d_score" if live2d_mode else "overall"

        # 排序
        ranked = sorted(
            zip(paths, scores),
            key=lambda x: x[1].get(score_key, x[1]["overall"]),
            reverse=True
        )

        lines = ["\n📊 批量生成报告:", "=" * 50]

        for i, (path, score) in enumerate(ranked, 1):
            s = score.get(score_key, score["overall"])
            marker = "🏆" if path == best_path else f"{i}."
            lines.append(f"{marker} {Path(path).name}: {s:.1%}")

            if live2d_mode and "live2d_score" in score:
                lines.append(f"   脸部:{score['face_quality']:.0%} 边缘:{score['edge_clarity']:.0%} "
                           f"背景:{score['background_purity']:.0%} 颜色:{score['color_separation']:.0%}")

        avg_score = sum(s.get(score_key, s["overall"]) for s in scores) / len(scores)
        lines.append(f"\n平均评分: {avg_score:.1%}")
        lines.append(f"最优评分: {ranked[0][1].get(score_key, ranked[0][1]['overall']):.1%}")

        return {
            "summary": "\n".join(lines),
            "ranked": [(p, s) for p, s in ranked],
            "average_score": avg_score,
            "best_score": ranked[0][1].get(score_key, ranked[0][1]["overall"]),
            "total": len(paths)
        }


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
    # 先加载配置（确保 .env 中的环境变量被读取）
    try:
        from config import config as _cfg
        _ = _cfg.has_sensenova_key
    except Exception:
        pass

    parser = argparse.ArgumentParser(
        description="Live2D Master Agent - 本地图像生成器 v6.0 (集成分层工具)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础生成
  python local_image_generator.py "cute anime girl"

  # Live2D分层专用生成（全身照+部件分离）
  python local_image_generator.py --live2d-rig "蓝发猫耳少女"

  # 生成后自动分层（一键生成→分层）
  python local_image_generator.py --live2d-rig --auto-layer "蓝发猫耳少女"

  # 使用商汤SenseNova生成并自动分层
  python local_image_generator.py --provider sensenova --live2d-rig --auto-layer "蓝发猫耳少女"

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
    parser.add_argument(
        "--provider",
        type=str,
        default="auto",
        choices=["auto", "local", "sensenova"],
        help="生成 Provider (auto/local/sensenova，默认auto)",
    )
    parser.add_argument(
        "--list-providers", action="store_true", help="列出可用 Provider"
    )
    parser.add_argument(
        "--live2d-rig",
        action="store_true",
        help="启用 Live2D 分层专用模式（全身照+部件分离+遮挡补全）",
    )
    parser.add_argument(
        "--auto-layer",
        action="store_true",
        help="生成后自动进行Live2D分层（需要安装分层工具依赖）",
    )
    parser.add_argument(
        "--layer-tool",
        type=str,
        default="pro",
        choices=["pro", "v6"],
        help="分层工具选择 (pro=专业版按部位分层, v6=K-means颜色聚类分层，默认pro)",
    )
    parser.add_argument(
        "--layer-k",
        type=int,
        default=8,
        help="K-means聚类数量（仅v6模式有效，默认8）",
    )
    parser.add_argument(
        "--layer-threshold",
        type=float,
        default=0.8,
        help="分层透明度阈值（仅v6模式有效，默认0.8）",
    )

    args = parser.parse_args()

    if args.list_providers:
        print("📚 可用 Provider 列表:")
        print("=" * 60)
        # 先导入 config 确保环境变量已加载
        try:
            from config import config as _cfg
            _ = _cfg.has_sensenova_key  # 触发加载
        except Exception:
            pass
        info = ProviderRouter.get_provider_info()
        for name, details in info.items():
            status = "✅" if details["available"] else "❌"
            print(f"\n{status} {name}")
            print(f"   描述: {details['desc']}")
            print(f"   成本: {details['cost']}")
            print(f"   质量: {details['quality']}")
            print(f"   需要GPU: {'是' if details['requires_gpu'] else '否'}")
        return

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

    # ====== Provider 路由 ======
    selected_provider = ProviderRouter.auto_select(args.provider)
    print(f"\n🔧 使用 Provider: {selected_provider}")

    if selected_provider == "sensenova":
        # 使用商汤 SenseNova
        provider = ProviderRouter.create_provider("sensenova")

        # 结构化解析提示词
        character = PromptEngineer.parse_character_from_text(args.prompt)
        if any([character.get("hair_color"), character.get("features")]):
            prompt, negative = PromptEngineer.build_prompt_from_character(
                character, style="anime",
                live2d_mode=not args.no_live2d,
                live2d_rigging=args.live2d_rig
            )
        else:
            # 非结构化提示词，手动添加Live2D分层关键词
            prompt = args.prompt
            negative = ""
            if args.live2d_rig:
                rig_keywords = PromptEngineer.LIVE2D_RIGGING_KEYWORDS
                prompt += ", " + ", ".join(rig_keywords.values())
                negative = """(profile view:1.2), (side view:1.2), (back view:1.2),
(open mouth:1.2), (dynamic pose:1.2), (partial body:1.3), (cropped:1.3),
(gradient shading:1.2), (soft shading:1.2), (missing limbs:1.3)"""

        output_path = provider.generate(
            prompt=prompt,
            negative_prompt=negative,
            width=args.width,
            height=args.height,
            output_dir=args.output or "./outputs",
        )

        # 质量评估
        scores = QualityAssessor.assess_image(
            output_path,
            live2d_mode=not args.no_live2d,
            live2d_rigging=args.live2d_rig
        )
        print(QualityAssessor.generate_report(scores, live2d_rigging=args.live2d_rig))

    else:
        # 使用本地 SD
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
            best_path, all_paths, report = generator.batch_generator.generate_batch(
                prompt=prompt,
                negative_prompt=negative,
                batch_size=args.batch,
                width=args.width,
                height=args.height,
                steps=steps,
                guidance_scale=args.guidance,
                use_multistage=args.multistage,
                live2d_mode=True,
            )
            if best_path:
                print(f"\n🎉 批量生成完成！")
                print(report["summary"])
                output_path = best_path
            else:
                print(f"\n❌ 批量生成失败")
                sys.exit(1)

        elif args.smart:
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

    # ====== 自动分层处理 ======
    if args.auto_layer:
        print("\n" + "="*60)
        print("🔧 自动分层模式")
        print("="*60)

        # 先进行Live2D兼容性检查
        try:
            from live2d_image_processor import check_live2d_compatibility
            compat_result = check_live2d_compatibility(output_path)
            print(f"\n📊 Live2D兼容性评分: {compat_result.get('score', 'N/A')}")
            for issue in compat_result.get('issues', []):
                print(f"   {issue}")
        except Exception as e:
            print(f"⚠️ 兼容性检查跳过: {e}")

        # 选择分层工具
        layer_tool = args.layer_tool

        if layer_tool == "pro":
            # 使用专业版分层工具
            try:
                from live2d_layer_pro import Live2DLayerToolPro
                print("\n🎨 使用 Live2D Layer Tool Pro 进行智能分层...")
                tool = Live2DLayerToolPro()
                result = tool.process_image(output_path)

                if result:
                    print(f"\n✅ 分层完成！")
                    print(f"📁 输出目录: {result['output_dir']}")
                    print(f"📦 图层数量: {len(result['layers'])}")
                    if result.get('psd'):
                        print(f"📄 PSD文件: {result['psd']}")
                    print(f"📖 分层指南: {result['guide']}")
                else:
                    print("❌ 分层失败")

            except Exception as e:
                print(f"❌ 专业版分层失败: {e}")
                print("💡 尝试使用基础版分层...")
                layer_tool = "v6"

        if layer_tool == "v6":
            # 使用v6版分层工具
            try:
                from live2d_layer_v6 import Live2DLayerToolV6
                print("\n🎨 使用 Live2D Layer Tool v6 进行颜色聚类分层...")
                tool = Live2DLayerToolV6(
                    output_path,
                    k_clusters=args.layer_k,
                    threshold=args.layer_threshold
                )
                layer_output = tool.process()

                if layer_output:
                    print(f"\n✅ 分层完成！")
                    print(f"📁 输出目录: {layer_output}")
                else:
                    print("❌ 分层失败")

            except Exception as e:
                print(f"❌ 基础版分层失败: {e}")


class SenseNovaProvider:
    """商汤日日新 SenseNova 文生图 Provider v6.0

    接入商汤教育平台/日日新平台的秒画 SenseMirage 文生图能力。
    支持 OpenAI 兼容接口调用。

    使用方法:
        1. 注册商汤日日新平台: https://platform.sensenova.cn
        2. 获取 API Key
        3. 设置环境变量: export SENSENOVA_API_KEY="sk-xxx"
        4. 使用: python local_image_generator.py --provider sensenova "蓝发猫耳少女"

    免费额度:
        - 公测期间每模型每5小时1500次免费调用
        - 图像生成模型: sensenova-u1-fast
    """

    DEFAULT_BASE_URL = "https://token.sensenova.cn/v1"
    IMAGE_MODEL = "sensenova-u1-fast"

    # 商汤 API 支持的尺寸列表 (宽x高)
    VALID_SIZES = [
        (1664, 2496), (2496, 1664),
        (1760, 2368), (2368, 1760),
        (1824, 2272), (2272, 1824),
        (2048, 2048),
        (2752, 1536), (1536, 2752),
        (3072, 1376), (1344, 3136),
    ]

    @classmethod
    def get_nearest_size(cls, width: int, height: int) -> Tuple[int, int]:
        """将任意尺寸映射到商汤 API 支持的最近尺寸"""
        target = (width, height)
        best = cls.VALID_SIZES[0]
        best_dist = float("inf")
        for w, h in cls.VALID_SIZES:
            # 计算宽高比差异 + 面积差异
            ratio_diff = abs((w / h) - (width / height))
            area_diff = abs(w * h - width * height)
            dist = ratio_diff * 10000 + area_diff / 100000
            if dist < best_dist:
                best_dist = dist
                best = (w, h)
        return best

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.environ.get("SENSENOVA_API_KEY")
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.client = None
        self._init_client()

    def _init_client(self):
        """初始化 OpenAI 兼容客户端"""
        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        except ImportError:
            print("⚠️ 未安装 openai 库，尝试使用 requests 调用")
            self.client = None

    def is_available(self) -> bool:
        """检查 Provider 是否可用"""
        if not self.api_key:
            return False
        try:
            if self.client:
                # 测试连接
                self.client.models.list()
                return True
            else:
                # 使用 requests 测试
                import requests
                resp = requests.get(
                    f"{self.base_url}/models",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=10
                )
                return resp.status_code == 200
        except Exception:
            return False

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1536,
        seed: Optional[int] = None,
        output_dir: str = "./outputs",
        **kwargs
    ) -> str:
        """使用商汤 SenseNova 生成图片

        Args:
            prompt: 正向提示词
            negative_prompt: 负向提示词（SenseNova部分模型支持）
            width: 图片宽度
            height: 图片高度
            seed: 随机种子
            output_dir: 输出目录

        Returns:
            生成的图片路径
        """
        if not self.api_key:
            raise ValueError("未设置 SENSENOVA_API_KEY，请设置环境变量或在初始化时传入")

        # 映射到商汤支持的最近尺寸
        actual_width, actual_height = self.get_nearest_size(width, height)
        if (actual_width, actual_height) != (width, height):
            print(f"   原始尺寸 {width}x{height} 映射为 {actual_width}x{actual_height}")

        print(f"\n🎨 调用商汤 SenseNova 生成图片...")
        print(f"   模型: {self.IMAGE_MODEL}")
        print(f"   尺寸: {actual_width}x{actual_height}")

        os.makedirs(output_dir, exist_ok=True)

        # 构建增强提示词
        live2d_rigging = kwargs.get("live2d_rigging", False)
        enhanced_prompt = self._enhance_prompt(prompt, actual_width, actual_height, live2d_rigging=live2d_rigging)

        try:
            if self.client:
                # 使用 OpenAI SDK 调用
                image_path = self._generate_with_sdk(
                    enhanced_prompt, negative_prompt, actual_width, actual_height, seed, output_dir
                )
            else:
                # 使用 requests 调用
                image_path = self._generate_with_requests(
                    enhanced_prompt, negative_prompt, actual_width, actual_height, seed, output_dir
                )

            print(f"✅ 商汤生成完成: {image_path}")
            return image_path

        except Exception as e:
            print(f"❌ 商汤生成失败: {e}")
            raise

    def _enhance_prompt(self, prompt: str, width: int, height: int, live2d_rigging: bool = False) -> str:
        """增强提示词以提升生成质量

        Args:
            prompt: 原始提示词
            width: 图片宽度
            height: 图片高度
            live2d_rigging: 是否启用Live2D分层专用优化
        """
        # 添加质量前缀
        quality_prefix = "masterpiece, best quality, ultra detailed, "

        if live2d_rigging:
            # Live2D分层专用优化词
            live2d_keywords = (
                "anime style, illustration, "
                "full body, standing straight, front view, looking at viewer, "
                "clean lineart, clear edges, sharp outlines, "
                "flat colors, cel shading, minimal gradients, solid colors, "
                "distinct part separation, clear boundaries, "
                "complete body parts under clothing, hidden parts drawn, "
                "symmetrical face, symmetrical eyes, centered composition, "
                "white background, simple background, isolated character, "
                "perfect anatomy, correct proportions, "
                "beautiful detailed face, beautiful detailed eyes"
            )
        else:
            # 基础Live2D优化词
            live2d_keywords = (
                "anime style, illustration, clean lineart, "
                "white background, simple background, "
                "front view, standing, perfect anatomy, "
                "beautiful detailed face, beautiful detailed eyes"
            )

        # 组合提示词
        enhanced = f"{quality_prefix}{prompt}, {live2d_keywords}"

        # 添加尺寸提示
        if width >= 1024 and height >= 1024:
            enhanced += ", high resolution"

        return enhanced

    def _generate_with_sdk(
        self,
        prompt: str,
        negative_prompt: str,
        width: int,
        height: int,
        seed: Optional[int],
        output_dir: str
    ) -> str:
        """使用 OpenAI SDK 生成"""
        import base64
        from io import BytesIO

        # 调用图像生成接口
        response = self.client.images.generate(
            model=self.IMAGE_MODEL,
            prompt=prompt,
            size=f"{width}x{height}",
            n=1,
            response_format="b64_json"
        )

        # 解码并保存
        image_data = base64.b64decode(response.data[0].b64_json)

        timestamp = int(time.time())
        filename = f"sensenova_{timestamp}.png"
        image_path = os.path.join(output_dir, filename)

        with open(image_path, "wb") as f:
            f.write(image_data)

        return image_path

    def _generate_with_requests(
        self,
        prompt: str,
        negative_prompt: str,
        width: int,
        height: int,
        seed: Optional[int],
        output_dir: str
    ) -> str:
        """使用 requests 直接调用 API"""
        import requests
        import base64

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.IMAGE_MODEL,
            "prompt": prompt,
            "size": f"{width}x{height}",
            "n": 1,
            "response_format": "b64_json"
        }

        resp = requests.post(
            f"{self.base_url}/images/generations",
            headers=headers,
            json=payload,
            timeout=120
        )
        resp.raise_for_status()

        data = resp.json()
        image_data = base64.b64decode(data["data"][0]["b64_json"])

        timestamp = int(time.time())
        filename = f"sensenova_{timestamp}.png"
        image_path = os.path.join(output_dir, filename)

        with open(image_path, "wb") as f:
            f.write(image_data)

        return image_path

    @staticmethod
    def get_setup_guide() -> str:
        """获取设置指南"""
        return """
📖 商汤 SenseNova 设置指南:

1. 注册账号:
   访问 https://platform.sensenova.cn 注册

2. 获取 API Key:
   控制台 → API Key 管理 → 创建 API Key

3. 设置环境变量:
   export SENSENOVA_API_KEY="sk-your-api-key"

4. 安装依赖:
   pip install openai

5. 使用:
   python local_image_generator.py --provider sensenova "蓝发猫耳少女"

💡 免费额度:
   - 公测期间每模型每5小时1500次调用
   - 图像生成模型: sensenova-u1-fast

⚠️ 注意:
   - 需要联网
   - 图片版权归用户所有
        """


class ProviderRouter:
    """Provider 路由器 - 自动选择最优生成方式 v6.0"""

    PROVIDERS = {
        "local": {
            "class": Live2DOptimizedGenerator,
            "desc": "本地 Stable Diffusion",
            "cost": "免费",
            "requires_gpu": True,
            "quality": "中等",
        },
        "sensenova": {
            "class": SenseNovaProvider,
            "desc": "商汤日日新 SenseNova",
            "cost": "免费额度",
            "requires_gpu": False,
            "quality": "高",
        },
    }

    @classmethod
    def get_available_providers(cls) -> List[str]:
        """获取所有可用的 Provider"""
        available = []
        for name, info in cls.PROVIDERS.items():
            if name == "local":
                # 检查是否有 GPU 或是否能运行
                try:
                    import torch
                    available.append(name)
                except ImportError:
                    pass
            elif name == "sensenova":
                # 检查 API Key
                if os.environ.get("SENSENOVA_API_KEY"):
                    available.append(name)
        return available

    @classmethod
    def create_provider(cls, name: str, **kwargs):
        """创建指定 Provider"""
        if name not in cls.PROVIDERS:
            raise ValueError(f"未知 Provider: {name}。可用: {list(cls.PROVIDERS.keys())}")

        provider_class = cls.PROVIDERS[name]["class"]
        return provider_class(**kwargs)

    @classmethod
    def auto_select(cls, preference: str = "auto") -> str:
        """自动选择最优 Provider"""
        available = cls.get_available_providers()

        if not available:
            raise RuntimeError("没有可用的 Provider。请安装依赖或设置 API Key。")

        if preference == "sensenova" and "sensenova" in available:
            return "sensenova"
        elif preference == "local" and "local" in available:
            return "local"
        elif preference == "auto":
            # 优先使用云端（质量更高）
            if "sensenova" in available:
                return "sensenova"
            return "local"

        return available[0]

    @classmethod
    def get_provider_info(cls) -> Dict:
        """获取所有 Provider 信息"""
        return {
            name: {
                "desc": info["desc"],
                "cost": info["cost"],
                "requires_gpu": info["requires_gpu"],
                "quality": info["quality"],
                "available": name in cls.get_available_providers()
            }
            for name, info in cls.PROVIDERS.items()
        }


if __name__ == "__main__":
    main()
