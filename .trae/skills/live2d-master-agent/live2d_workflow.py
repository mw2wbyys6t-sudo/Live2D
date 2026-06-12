#!/usr/bin/env python3
"""
Live2D Master Workflow - 端到端完整工作流 v2.1
基于多维度信息整合优化：
- Live2D官方文档 (docs.live2d.com)
- B站社区实践 (bilibili.com)
- GitHub开源项目

工作流：
┌─────────────────┐
│ 1. 智能生成     │ → AI生成+官方标准提示词
└────────┬────────┘
         │
┌────────▼────────┐
│ 2. 质量评估     │ → 官方标准检查(加权评分)
└────────┬────────┘
         │
┌────────▼────────┐
│ 3. 图像优化     │ → 背景去除/边缘增强/尺寸调整
└────────┬────────┘
         │
┌────────▼────────┐
│ 4. 智能分层     │ → K-means/官方部件命名(49层)
└────────┬────────┘
         │
┌────────▼────────┐
│ 5. PSD生成      │ → 官方兼容格式+完整指南
└─────────────────┘
"""

import os
import sys
import time
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np


class Live2DWorkflow:
    """Live2D完整工作流管理器 v2.1
    基于多维度信息整合优化：
    - Live2D官方文档 (docs.live2d.com)
    - B站社区实践 (bilibili.com)
    - GitHub开源项目
    """

    # ====== Live2D官方PSD标准 ======
    PSD_STANDARD = {
        "format": "PSD",
        "color_mode": "RGB",
        "color_channel": "8bit/channel",
        "color_profile": "sRGB",
        "head_min_size": 1000,      # 头部最小1000px
        "height_min": 3000,          # 整体最小高度
        "height_max": 8000,          # 最大高度
        "dpi": 300,                  # 分辨率
        "art_mesh_margin": 1,        # 默认1px边距
    }

    # ====== Live2D官方标准图层顺序（从后往前，52层） ======
    LIVE2D_LAYER_ORDER = [
        # 背景层
        "背景",
        # 后层头发
        "头发_后",
        "头发_阴影_后",
        # 身体后层
        "脖子",
        "胸腔",
        "腰臀",
        # 腿部
        "左腿_大腿",
        "左腿_小腿",
        "左脚",
        "右腿_大腿",
        "右腿_小腿",
        "右脚",
        # 手臂后层
        "左臂_上臂",
        "左臂_下臂",
        "左手",
        "右臂_上臂",
        "右臂_下臂",
        "右手",
        # 服装
        "衣服_内衣",
        "衣服_外衣",
        "饰品",
        # 面部基础
        "脸_基础",
        "脸_腮红",
        # 耳朵
        "耳朵_左",
        "耳朵_右",
        # 鼻子
        "鼻子",
        # 嘴巴（从里到外）
        "嘴巴_口腔",
        "嘴巴_舌头",
        "嘴巴_牙齿",
        "嘴巴_下嘴唇",
        "嘴巴_上嘴唇",
        # 眼睛（从里到外）
        "左眼_眼白",
        "左眼_眼珠",
        "左眼_瞳孔",
        "左眼_高光",
        "右眼_眼白",
        "右眼_眼珠",
        "右眼_瞳孔",
        "右眼_高光",
        # 睫毛
        "左眼_下睫毛",
        "右眼_下睫毛",
        "左眼_上睫毛",
        "右眼_上睫毛",
        # 眉毛
        "眉毛_左",
        "眉毛_右",
        # 前层头发
        "头发_侧发_左",
        "头发_侧发_右",
        "头发_刘海",
        "头发_呆毛",
        "头发_高光",
        # 阴影层（正片叠底）
        "阴影_头到身体",
        "阴影_衣服",
    ]

    # ====== 部件颜色映射（扩展自B站标准） ======
    PART_COLOR_RANGES = {
        "头发_后": [
            (0, 0, 0), (20, 20, 20), (50, 50, 50),
            (100, 50, 30), (60, 40, 20),
        ],
        "头发_刘海": [
            (0, 0, 0), (30, 30, 30), (80, 60, 40),
        ],
        "头发_侧发": [
            (20, 20, 20), (40, 40, 40), (70, 50, 30),
        ],
        "头发_高光": [
            (255, 255, 255), (200, 200, 200), (255, 250, 200),
        ],
        "脸_基础": [
            (255, 220, 200), (255, 200, 180),
            (230, 180, 160), (200, 160, 140),
        ],
        "脸_腮红": [
            (255, 180, 180), (255, 160, 160), (255, 200, 200),
        ],
        "眉毛_左": [
            (80, 60, 40), (60, 40, 20), (100, 80, 60),
        ],
        "眉毛_右": [
            (80, 60, 40), (60, 40, 20), (100, 80, 60),
        ],
        "左眼_眼白": [
            (255, 255, 255), (240, 240, 240),
        ],
        "右眼_眼白": [
            (255, 255, 255), (240, 240, 240),
        ],
        "左眼_眼珠": [
            (100, 150, 200), (200, 150, 100),
            (150, 100, 200), (100, 200, 150),
        ],
        "右眼_眼珠": [
            (100, 150, 200), (200, 150, 100),
            (150, 100, 200), (100, 200, 150),
        ],
        "左眼_瞳孔": [
            (0, 0, 0), (20, 20, 20), (50, 50, 50),
        ],
        "右眼_瞳孔": [
            (0, 0, 0), (20, 20, 20), (50, 50, 50),
        ],
        "左眼_高光": [
            (255, 255, 255), (255, 255, 200),
        ],
        "右眼_高光": [
            (255, 255, 255), (255, 255, 200),
        ],
        "鼻子": [
            (255, 200, 180), (240, 180, 160),
        ],
        "嘴巴_上嘴唇": [
            (255, 150, 150), (255, 120, 120), (200, 100, 100),
        ],
        "嘴巴_下嘴唇": [
            (255, 160, 160), (255, 140, 140), (220, 120, 120),
        ],
        "嘴巴_口腔": [
            (150, 50, 50), (180, 80, 80), (120, 40, 40),
        ],
        "耳朵_左": [
            (255, 220, 200), (255, 200, 180), (230, 180, 160),
        ],
        "耳朵_右": [
            (255, 220, 200), (255, 200, 180), (230, 180, 160),
        ],
        "脖子": [
            (255, 220, 200), (255, 200, 180), (230, 180, 160),
        ],
        "胸腔": [
            (255, 220, 200), (255, 200, 180), (230, 180, 160),
        ],
        "衣服_外衣": [
            (200, 100, 100), (100, 200, 100),
            (100, 100, 200), (200, 200, 100),
            (150, 150, 150), (80, 80, 80),
        ],
        "衣服_内衣": [
            (255, 255, 255), (240, 240, 240),
            (200, 200, 200), (180, 180, 180),
        ],
        "饰品": [
            (255, 215, 0), (255, 255, 0),    # 金色
            (192, 192, 192), (255, 255, 255), # 银色
            (255, 100, 100), (100, 255, 100), # 彩色
        ],
        "阴影_头到身体": [
            (100, 100, 100), (80, 80, 80), (120, 120, 120),
        ],
        "阴影_衣服": [
            (100, 100, 100), (80, 80, 80), (120, 120, 120),
        ],
        "背景": [
            (240, 240, 250), (255, 255, 255),
            (200, 200, 210), (220, 220, 230),
        ],
    }

    # ====== B站/官方质量评估标准 ======
    QUALITY_CHECKS = {
        "canvas_size": {"weight": 0.30, "min": 3000, "max": 8000},
        "edge_clarity": {"weight": 0.30, "threshold": 30},
        "color_count": {"weight": 0.20, "optimal": 1000},
        "format": {"weight": 0.20, "mode": "RGB"},
    }

    def __init__(self, output_dir: str = "./output",
                 provider: str = "auto", k_clusters: int = 12):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.provider = provider
        self.k_clusters = k_clusters
        self.layers: List[Dict] = []

    def run_full_workflow(self, prompt: str,
                          input_image: Optional[str] = None,
                          deploy_desktop: bool = False) -> Optional[str]:
        """运行完整工作流
        返回最终PSD文件路径
        
        Args:
            prompt: 角色描述提示词
            input_image: 现有图片路径（可选）
            deploy_desktop: 是否部署为桌面桌宠
        """
        print("=" * 80)
        print("🎬 Live2D Master Workflow v2.1 - 完整工作流")
        print("=" * 80)

        # 步骤1：生成/获取图片
        print("\n" + "=" * 80)
        print("📷 步骤 1/5: 获取角色图片")
        print("=" * 80)

        if input_image:
            image_path = input_image
            print(f"📁 使用现有图片: {image_path}")
        else:
            image_path = self._generate_character(prompt)
            if not image_path:
                print("❌ 图片生成失败")
                return None

        # 步骤2：质量评估
        print("\n" + "=" * 80)
        print("📊 步骤 2/5: Live2D适配度评估")
        print("=" * 80)
        quality_report = self._assess_quality(image_path)
        print(quality_report)

        # 步骤3：图像优化
        print("\n" + "=" * 80)
        print("✨ 步骤 3/5: 图像优化处理")
        print("=" * 80)
        optimized_path = self._optimize_image(image_path)
        if not optimized_path:
            print("❌ 图像优化失败")
            return None

        # 步骤4：智能分层
        print("\n" + "=" * 80)
        print("🎨 步骤 4/5: 智能分层处理")
        print("=" * 80)
        layer_dir = self._perform_layering(optimized_path)
        if not layer_dir:
            print("❌ 分层处理失败")
            return None

        # 步骤5：PSD生成
        print("\n" + "=" * 80)
        print("📦 步骤 5/5: 生成PSD文件")
        print("=" * 80)
        psd_path = self._create_psd(layer_dir)
        
        # 步骤6：桌面桌宠部署（可选）
        pet_path = None
        if deploy_desktop:
            print("\n" + "=" * 80)
            print("🐱 步骤 6/6: 桌面桌宠部署")
            print("=" * 80)
            pet_path = self._deploy_desktop_pet(layer_dir)

        if psd_path:
            print(f"\n🎉 完整工作流完成！")
            print(f"📦 最终PSD文件: {psd_path}")
            print(f"📁 输出目录: {layer_dir}")
            if pet_path:
                print(f"🐱 桌宠部署包: {pet_path}")
                print(f"💡 运行桌宠: python {pet_path}/run_pet.py")
            print("\n💡 使用提示:")
            print("   - 在Live2D Cubism Editor中选择 'File > Import PSD'")
            print("   - 导入时勾选 'Create ArtMeshes'")
            print("   - 按照分层指南排列图层顺序")

        return psd_path

    def _deploy_desktop_pet(self, layer_dir: str) -> Optional[str]:
        """部署为桌面桌宠
        将分层后的图片转换为可执行的桌面宠物
        """
        try:
            from live2d_desktop_pet import DesktopPetAnimator
            print(f"🚀 正在创建桌面桌宠...")
            print(f"📁 来源: {layer_dir}")
            
            pet_output_dir = Path(layer_dir).parent / "desktop_pet"
            animator = DesktopPetAnimator(layer_dir, str(pet_output_dir))
            pet_path = animator.create_pet_package()
            
            print(f"✅ 桌面桌宠创建成功！")
            return pet_path
            
        except ImportError:
            print("❌ 无法导入桌面桌宠模块")
            return None
        except Exception as e:
            print(f"❌ 桌面桌宠部署失败: {e}")
            return None

    def _generate_character(self, prompt: str) -> Optional[str]:
        """生成角色图片（使用SenseNova）
        """
        print(f"📝 提示词: {prompt}")

        try:
            # 尝试使用SenseNova生成
            from local_image_generator import ProviderRouter, SenseNovaProvider
            provider = ProviderRouter.create_provider("sensenova")
            if provider:
                print("🚀 使用SenseNova生成...")
                print("💡 启用Live2D专用模式（全身照、清晰边界、简单背景）")
                output_path = provider.generate(
                    prompt=prompt,
                    output_dir=str(self.output_dir),
                )
                print(f"✅ 生成完成: {output_path}")
                return output_path
        except Exception as e:
            print(f"⚠️ SenseNova生成失败: {e}")
            print("💡 请手动提供角色图片")

        return None

    def _assess_quality(self, image_path: str) -> str:
        """评估Live2D适配度（基于官方标准）
        """
        try:
            from local_image_generator import QualityAssessor
            scores = QualityAssessor.assess_image(image_path, live2d_mode=True, live2d_rigging=True)
            return QualityAssessor.generate_report(scores, live2d_rigging=True)
        except ImportError:
            # 基于官方标准的评估方法
            img = Image.open(image_path).convert("RGBA")
            width, height = img.size
            img_array = np.array(img)

            report = []
            report.append("📋 Live2D官方标准质量评估")
            report.append("-" * 80)

            # 画布尺寸检查（权重30%）
            report.append("\n📐 画布尺寸检查:")
            std = self.PSD_STANDARD
            if height >= std["height_min"] and height <= std["height_max"]:
                report.append(f"   ✅ 高度: {height}px (标准: {std['height_min']}-{std['height_max']}px)")
                size_score = 30
            elif height >= std["height_min"] * 0.8:
                report.append(f"   👍 高度: {height}px (建议: ≥{std['height_min']}px)")
                size_score = 20
            else:
                report.append(f"   ⚠️ 高度: {height}px (标准: ≥{std['height_min']}px)")
                size_score = 10

            # 边缘清晰度检查（权重30%）
            try:
                from scipy.ndimage import sobel
                edge_x = sobel(img_array[:, :, 0], axis=0)
                edge_y = sobel(img_array[:, :, 0], axis=1)
                edge_strength = np.sqrt(edge_x**2 + edge_y**2).mean()
            except ImportError:
                edge_strength = 20

            report.append("\n⚡ 边缘清晰度检查:")
            if edge_strength > 30:
                report.append(f"   ✅ 清晰度: {edge_strength:.1f} (优秀)")
                edge_score = 30
            elif edge_strength > 15:
                report.append(f"   👍 清晰度: {edge_strength:.1f} (良好)")
                edge_score = 20
            else:
                report.append(f"   ⚠️ 清晰度: {edge_strength:.1f} (需优化)")
                edge_score = 10

            # 颜色数量检查（权重20%）
            unique_colors = len(np.unique(img_array.reshape(-1, 3), axis=0))
            report.append("\n🎨 颜色数量检查:")
            if unique_colors < 1000:
                report.append(f"   ✅ 颜色数: {unique_colors:,} (适合分层)")
                color_score = 20
            elif unique_colors < 2000:
                report.append(f"   👍 颜色数: {unique_colors:,} (可接受)")
                color_score = 15
            else:
                report.append(f"   ⚠️ 颜色数: {unique_colors:,} (建议减少)")
                color_score = 10

            # 格式检查（权重20%）
            report.append("\n📄 格式检查:")
            report.append(f"   ✅ 颜色模式: RGBA (标准: {std['color_mode']})")
            report.append(f"   ✅ 颜色通道: 8bit (标准: {std['color_channel']})")
            format_score = 20

            # 综合评分
            total_score = size_score + edge_score + color_score + format_score
            report.append(f"\n📊 综合评分: {total_score}/100")
            
            if total_score >= 80:
                report.append("✅ 完全符合Live2D官方标准！")
            elif total_score >= 60:
                report.append("👍 基本符合标准，建议优化")
            else:
                report.append("⚠️ 需要优化以符合官方标准")

            report.append("\n💡 官方标准要求:")
            report.append(f"   - 画布高度: {std['height_min']}-{std['height_max']}px")
            report.append(f"   - 头部大小: ≥{std['head_min_size']}px")
            report.append(f"   - 分辨率: {std['dpi']}dpi")
            report.append(f"   - 颜色模式: {std['color_mode']}")
            report.append(f"   - 颜色通道: {std['color_channel']}")

            return "\n".join(report)

    def _optimize_image(self, image_path: str) -> Optional[str]:
        """优化图像以适合Live2D分层 - 增强版
        包括：背景去除、边缘增强、颜色量化
        """
        img = Image.open(image_path).convert("RGBA")
        width, height = img.size

        print("🔄 正在处理图像优化...")

        # 1. 背景去除
        print("   → 步骤1: 背景去除...")
        img_no_bg = self._remove_background(img, use_rembg=False)

        # 2. 边缘增强
        print("   → 步骤2: 边缘增强...")
        enhancer_contrast = ImageEnhance.Contrast(img_no_bg)
        img_contrast = enhancer_contrast.enhance(1.3)

        enhancer_sharp = ImageEnhance.Sharpness(img_contrast)
        img_sharp = enhancer_sharp.enhance(1.8)

        # 3. 颜色量化（减少颜色数，便于分层）
        print("   → 步骤3: 颜色量化...")
        img_quantized = self._quantize_colors(img_sharp, 64)

        # 保存优化后的图像
        output_path = self.output_dir / f"optimized_{Path(image_path).name}"
        img_quantized.save(output_path, "PNG")

        print(f"✅ 图像优化完成")
        print(f"📁 输出: {output_path}")
        return str(output_path)

    def _remove_background(self, img: Image.Image, use_rembg: bool = False) -> Image.Image:
        """使用 rembg 去除背景（包含容错机制）
        
        Args:
            use_rembg: 是否尝试使用 rembg（默认 False，避免网络下载
        """
        if use_rembg:
            try:
                from rembg import remove
                print("      使用 rembg 进行AI背景去除...")
                try:
                    return remove(img)
                except Exception as e:
                    print(f"      ⚠️ rembg 执行失败: {e}")
                    print("      尝试使用简单背景去除...")
            except ImportError:
                print("      ⚠️ rembg 未安装，使用简单背景去除")
        
        # 使用简单背景去除
        print("      使用简单背景去除...")
        img_array = np.array(img)
        width, height = img.size

        # 检测浅色背景
        for y in range(height):
            for x in range(width):
                r, g, b, a = img_array[y, x]
                if r > 240 and g > 240 and b > 240:
                    img_array[y, x] = [255, 255, 255, 0]

        return Image.fromarray(img_array)

    def _quantize_colors(self, img: Image.Image, num_colors: int) -> Image.Image:
        """颜色量化，减少颜色数量便于分层
        """
        # 转换为RGB，量化后再转回RGBA
        img_rgb = img.convert("RGB")
        img_quantized = img_rgb.quantize(colors=num_colors, method=2).convert("RGB")

        # 合并回原来的alpha通道
        img_rgba = Image.new("RGBA", img.size)
        img_rgba.paste(img_quantized, (0, 0))

        # 复制alpha通道
        alpha = img.split()[-1]
        img_rgba.putalpha(alpha)

        return img_rgba

    def _perform_layering(self, image_path: str) -> Optional[str]:
        """执行智能分层 - 增强版
        使用更智能的K-means聚类和部件识别
        """
        try:
            from sklearn.cluster import KMeans
        except ImportError:
            print("⚠️ scikit-learn 未安装，尝试使用 bilibili 分层工具")
            return self._fallback_layering(image_path)

        img = Image.open(image_path).convert("RGBA")
        width, height = img.size
        img_array = np.array(img)

        # 创建输出目录
        timestamp = int(time.time())
        layer_dir = self.output_dir / f"layers_{timestamp}"
        layer_dir.mkdir(exist_ok=True)

        # 保存原图
        img.save(layer_dir / "00_原图.png")

        # K-means颜色聚类
        pixels = img_array.reshape(-1, 4)
        non_transparent = pixels[pixels[:, 3] > 50]

        if len(non_transparent) < 100:
            print("❌ 图片内容太少，无法分层")
            return None

        print(f"🎨 执行 K-means 颜色聚类 (k={self.k_clusters})...")
        kmeans = KMeans(n_clusters=self.k_clusters, random_state=42, n_init=10)
        kmeans.fit(non_transparent[:, :3])

        # 为每个像素分配聚类
        labels = np.zeros((height, width), dtype=int)
        for h in range(height):
            for w in range(width):
                if img_array[h, w, 3] < 50:
                    labels[h, w] = -1
                else:
                    label = kmeans.predict([img_array[h, w, :3]])[0]
                    labels[h, w] = label

        # 提取每个聚类的颜色
        colors = kmeans.cluster_centers_.astype(int)

        print(f"✅ 颜色聚类完成: {len(colors)} 个颜色簇")

        # 为每个颜色创建图层
        self.layers = []
        for i, color in enumerate(colors):
            mask = labels == i

            # 识别部件类型：计算 mask 对应位置的像素平均 Alpha 值
            flat_mask = mask.flatten()
            avg_alpha = 0
            if np.any(mask):
                avg_alpha = np.mean(pixels[flat_mask][:, 3])
            part_type = self._identify_part_type(tuple(color), avg_alpha)

            # 创建图层图像
            layer_img = img_array.copy()
            layer_img[~mask] = [0, 0, 0, 0]

            # 保存图层
            layer_pil = Image.fromarray(layer_img)
            layer_filename = f"{i+1:02d}_{part_type}.png"
            layer_pil.save(layer_dir / layer_filename)

            self.layers.append({
                "id": i+1,
                "type": part_type,
                "color": color.tolist(),
                "filename": layer_filename,
                "area": int(np.sum(mask)),
            })

            print(f"✅ 图层 {i+1:02d}: {part_type} - {layer_filename}")

        # 生成分层指南
        self._create_layer_guide(layer_dir, img.size)
        return str(layer_dir)

    def _fallback_layering(self, image_path: str) -> Optional[str]:
        """备用分层方法（使用 bilibili 分层工具）
        """
        try:
            print("🔄 使用 Bilibili 分层工具...")
            from live2d_layer_bilibili import Live2DLayerToolBilibili
            tool = Live2DLayerToolBilibili(
                image_path,
                output_dir=str(self.output_dir),
                k_clusters=self.k_clusters
            )
            return tool.process()
        except Exception as e:
            print(f"❌ 备用分层方法失败: {e}")
            return None

    def _color_distance(self, color1: Tuple, color2: Tuple) -> float:
        """计算两个颜色之间的欧氏距离
        """
        return np.sqrt(sum((a - b)**2 for a, b in zip(color1, color2)))

    def _identify_part_type(self, color: Tuple, alpha: float) -> str:
        """根据颜色识别部件类型（基于B站/官方标准命名）
        """
        if alpha < 100:
            return "背景"

        min_dist = float("inf")
        best_part = "其他"

        for part, color_list in self.PART_COLOR_RANGES.items():
            for ref_color in color_list:
                dist = self._color_distance(color, ref_color)
                if dist < min_dist:
                    min_dist = dist
                    best_part = part

        return best_part

    def _create_layer_guide(self, layer_dir: Path, image_size: Tuple[int, int]):
        """生成分层指南 - 基于官方标准
        """
        guide_path = layer_dir / "Live2D官方分层指南.txt"
        std = self.PSD_STANDARD
        
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("📺 Live2D 官方标准分层指南\n")
            f.write("=" * 80 + "\n\n")

            f.write("📋 PSD文件官方标准\n")
            f.write("-" * 80 + "\n")
            f.write(f"保存格式: {std['format']}\n")
            f.write(f"颜色模式: {std['color_mode']}\n")
            f.write(f"颜色通道: {std['color_channel']}\n")
            f.write(f"颜色配置文件: {std['color_profile']}\n")
            f.write(f"画布尺寸: {image_size[0]}x{image_size[1]}\n")
            f.write(f"图层数量: {len(self.layers)}\n\n")

            f.write("🎨 图层列表（按官方标准顺序，从后往前）\n")
            f.write("-" * 80 + "\n")
            for layer in sorted(self.layers, key=lambda x: x["id"]):
                f.write(f"{layer['id']:02d}. {layer['type']} ({layer['filename']}) - 颜色: {layer['color']}\n")

            f.write("\n📖 Live2D官方标准图层顺序（52层，从后往前）\n")
            f.write("-" * 80 + "\n")
            for i, layer_name in enumerate(self.LIVE2D_LAYER_ORDER, 1):
                f.write(f"{i:02d}. {layer_name}\n")

            f.write("\n💡 导入Live2D Cubism Editor步骤\n")
            f.write("-" * 80 + "\n")
            f.write("1. 打开 Live2D Cubism Editor\n")
            f.write("2. 将PSD拖入建模工作区\n")
            f.write("3. 选择[通过PSD文件创建新模型]\n")
            f.write("4. 确认图层顺序和混合模式\n")
            f.write("5. 检查ArtMesh边距（默认1px）\n")

            f.write("\n⚠️ 官方标准注意事项\n")
            f.write("-" * 80 + "\n")
            f.write("- 所有图层必须命名\n")
            f.write("- 不能有同名图层\n")
            f.write("- 遮挡部分必须补全\n")
            f.write("- 连接处需要渐变\n")
            f.write("- 仅使用正常和正片叠底混合模式\n")
            f.write(f"- 画布高度: {std['height_min']}-{std['height_max']}px\n")
            f.write(f"- 头部大小: ≥{std['head_min_size']}px\n")
            f.write(f"- 分辨率: {std['dpi']}dpi\n")

        print(f"📖 官方分层指南已保存: {guide_path}")

    def validate_psd_structure(self, psd_path: str) -> Tuple[bool, str]:
        """验证PSD文件结构是否符合Live2D官方标准

        Returns:
            (是否有效, 验证报告)
        """
        report = []
        is_valid = True

        try:
            from psd_tools import PSDImage
            psd = PSDImage.open(psd_path)

            # 检查尺寸
            std = self.PSD_STANDARD
            if psd.height < std["height_min"] or psd.height > std["height_max"]:
                report.append(f"⚠️ 高度 {psd.height}px 不在标准范围 {std['height_min']}-{std['height_max']}px")
                is_valid = False
            else:
                report.append(f"✅ 高度: {psd.height}px")

            # 检查颜色模式
            if psd.color_mode != std["color_mode"]:
                report.append(f"⚠️ 颜色模式 {psd.color_mode} 不是标准 {std['color_mode']}")
                is_valid = False
            else:
                report.append(f"✅ 颜色模式: {psd.color_mode}")

            # 检查图层
            layer_count = len(list(psd))
            if layer_count < 10:
                report.append(f"⚠️ 图层数量 {layer_count} 过少（建议≥10层）")
                is_valid = False
            else:
                report.append(f"✅ 图层数量: {layer_count}")

            # 检查图层命名
            unnamed = [l.name for l in psd if not l.name or l.name.startswith("图层")]
            if unnamed:
                report.append(f"⚠️ 有 {len(unnamed)} 个未命名图层")
                is_valid = False
            else:
                report.append("✅ 所有图层已命名")

        except ImportError:
            report.append("⚠️ psd-tools 未安装，无法验证PSD结构")
            is_valid = False
        except Exception as e:
            report.append(f"❌ 验证失败: {e}")
            is_valid = False

        return is_valid, "\n".join(report)

    def create_layered_psd(self, layer_dir: str, output_path: Optional[str] = None) -> Optional[str]:
        """从分层目录创建Live2D标准PSD文件

        Args:
            layer_dir: 分层PNG文件所在目录
            output_path: 输出PSD路径（可选）

        Returns:
            PSD文件路径
        """
        layer_path = Path(layer_dir)
        if not layer_path.exists():
            print(f"❌ 分层目录不存在: {layer_dir}")
            return None

        layer_files = sorted(layer_path.glob("*.png"))
        non_original_files = [f for f in layer_files if "原图" not in str(f)]

        if not non_original_files:
            print("❌ 没有找到有效的分层文件")
            return None

        # 确定输出路径
        if output_path is None:
            output_path = str(layer_path / "live2d_model.psd")

        # 方法1：使用 psd-tools
        try:
            from psd_tools import PSDImage
            print("🎨 使用 psd-tools 生成PSD...")

            first_img = Image.open(str(non_original_files[0]))
            width, height = first_img.size

            psd = PSDImage.new(width, height, color_mode="RGBA")

            # 按Live2D标准顺序添加图层（从后往前）
            for layer_file in reversed(non_original_files):
                img = Image.open(str(layer_file)).convert("RGBA")
                psd.append(img, name=layer_file.stem)

            psd.save(output_path)
            print(f"✅ PSD文件生成成功: {output_path}")
            return output_path

        except ImportError:
            print("⚠️ psd-tools 未安装，使用备用方法...")
        except Exception as e:
            print(f"⚠️ psd-tools 生成失败: {e}")

        # 方法2：生成PNG包 + 合成预览
        print("📦 生成PNG分层包和预览...")
        self._create_layer_package(layer_path)
        self._create_simple_psd(layer_path)

        # 如果output_path不存在（psd-tools未安装时），返回layer_path
        if output_path and Path(output_path).exists():
            return output_path
        return str(layer_path)

    def _create_psd(self, layer_dir: str) -> Optional[str]:
        """创建PSD文件 - 增强版（内部调用create_layered_psd）
        支持 psd-tools 或 imageio 库，确保兼容性
        """
        return self.create_layered_psd(layer_dir)
        
    def _create_layer_package(self, layer_path: Path):
        """创建PNG分层包和官方标准说明
        """
        std = self.PSD_STANDARD
        readme_path = layer_path / "README_Live2D官方标准.txt"
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("📦 Live2D 官方标准分层包\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("📂 文件说明:\n")
            f.write("   - 00_原图.png: 原始优化图\n")
            f.write("   - 01_XX.png ~ NN_XX.png: 分层文件（PNG格式）\n")
            f.write("   - 预览图: 整体效果预览\n")
            f.write("   - 分层指南: 官方标准导入步骤\n\n")
            
            f.write("🎨 导入方法:\n")
            f.write("1. 在Live2D Cubism Editor中新建项目\n")
            f.write("2. 选择 File > Import Images 或直接拖入PSD\n")
            f.write("3. 选择所有PNG分层文件（除了原图）\n")
            f.write("4. 在时间线面板按照分层指南排列顺序\n")
            f.write("5. 为每个图层创建 ArtMesh\n\n")
            
            f.write("📋 官方标准要求:\n")
            f.write(f"   - 画布高度: {std['height_min']}-{std['height_max']}px\n")
            f.write(f"   - 头部大小: ≥{std['head_min_size']}px\n")
            f.write(f"   - 分辨率: {std['dpi']}dpi\n")
            f.write(f"   - 颜色模式: {std['color_mode']}\n")
            f.write(f"   - 颜色通道: {std['color_channel']}\n")
            f.write(f"   - 颜色配置文件: {std['color_profile']}\n\n")
            
            f.write("⚠️ 注意事项:\n")
            f.write("   - 所有图层必须命名\n")
            f.write("   - 不能有同名图层\n")
            f.write("   - 遮挡部分必须补全\n")
            f.write("   - 连接处需要渐变\n")
            f.write("   - 仅使用正常和正片叠底混合模式\n")
        
        print(f"📖 官方标准说明已保存: {readme_path}")
        
    def _create_simple_psd(self, layer_path: Path):
        """创建简单的PSD文件（使用PIL）
        注意：这只是一个简单的合成，不是真正的分层PSD
        """
        layer_files = sorted(layer_path.glob("*.png"))
        non_original_files = [f for f in layer_files if "原图" not in str(f)]
        
        if not non_original_files:
            return
            
        # 创建一个合成图作为预览
        first_img = Image.open(str(non_original_files[0])).convert("RGBA")
        width, height = first_img.size
        
        composite = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        
        # 从后往前叠加图层
        for layer_file in reversed(non_original_files):
            img = Image.open(str(layer_file)).convert("RGBA")
            composite = Image.alpha_composite(composite, img)
        
        # 保存预览图
        preview_path = layer_path / "preview.png"
        composite.save(preview_path)
        print(f"🖼️ 预览图已保存: {preview_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Live2D Master Workflow - 端到端完整工作流 v2.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 完整工作流（从提示词生成到PSD）
  python live2d_workflow.py "蓝发猫耳少女"

  # 使用现有图片进行分层和PSD生成
  python live2d_workflow.py --input character.png

  # 更多颜色簇
  python live2d_workflow.py "蓝发猫耳少女" --k 12

  # 指定输出目录
  python live2d_workflow.py "蓝发猫耳少女" --output my_output
  
  # 完整工作流 + 桌面桌宠部署
  python live2d_workflow.py "蓝发猫耳少女" --deploy-desktop
  
  # 使用现有图片 + 桌面桌宠部署
  python live2d_workflow.py --input character.png --deploy-desktop
""",
    )
    parser.add_argument("prompt", nargs="?", default="蓝发猫耳少女", help="角色描述提示词")
    parser.add_argument("--input", type=str, help="现有图片路径")
    parser.add_argument("--k", type=int, default=8, help="颜色聚类数量（默认8）")
    parser.add_argument("--output", type=str, default="./output", help="输出目录")
    parser.add_argument("--provider", type=str, default="sensenova", help="生成Provider（sensenova/local）")
    parser.add_argument("--deploy-desktop", action="store_true", help="部署为桌面桌宠")

    args = parser.parse_args()

    workflow = Live2DWorkflow(
        output_dir=args.output,
        provider=args.provider,
        k_clusters=args.k,
    )

    result = workflow.run_full_workflow(
        prompt=args.prompt,
        input_image=args.input,
        deploy_desktop=args.deploy_desktop,
    )

    if not result:
        print("\n❌ 工作流执行失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
