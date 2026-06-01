#!/usr/bin/env python3
"""
Live2D Master Workflow - 端到端完整工作流 v1.0
整合从生成到PSD输出的全流程

工作流：
┌─────────────────┐
│ 1. 角色生成     │ → 使用SenseNova/本地生成
└────────┬────────┘
         │
┌────────▼────────┐
│ 2. 质量评估     │ → 检测是否适合分层
└────────┬────────┘
         │
┌────────▼────────┐
│ 3. 图像优化     │ → 轮廓/背景/透明度处理
└────────┬────────┘
         │
┌────────▼────────┐
│ 4. 智能分层     │ → K-means/颜色识别分层
└────────┬────────┘
         │
┌────────▼────────┐
│ 5. PSD生成      │ → 符合Live2D标准格式
└─────────────────┘
"""

import os
import sys
import time
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image
import numpy as np


class Live2DWorkflow:
    """Live2D完整工作流管理器
    """

    # Live2D标准图层顺序（从后往前）
    LIVE2D_LAYER_ORDER = [
        "背景",
        "身体",
        "下半身",
        "脚",
        "腿",
        "腰部",
        "手臂",
        "衣服",
        "头",
        "脖子",
        "脸",
        "眉毛",
        "眼睛",
        "瞳孔",
        "嘴巴",
        "耳朵",
        "头发_后",
        "头发_中",
        "头发_前",
        "头发_刘海",
        "装饰",
        "饰品",
    ]

    # 部件颜色映射
    PART_COLOR_RANGES = {
        "头发": [
            (0, 0, 0),
            (20, 20, 20),
            (100, 50, 30),
            (255, 200, 150),
            (200, 100, 150),
            (100, 150, 200),
        ],
        "皮肤": [
            (255, 220, 200),
            (255, 200, 180),
            (230, 180, 160),
            (200, 160, 140),
        ],
        "眼睛": [
            (100, 150, 200),
            (200, 150, 100),
            (150, 100, 200),
            (255, 255, 255),
        ],
        "衣服": [
            (200, 100, 100),
            (100, 200, 100),
            (100, 100, 200),
            (200, 200, 100),
        ],
        "背景": [
            (240, 240, 250),
            (255, 255, 255),
        ],
    }

    def __init__(self, output_dir: str = "./output",
                 provider: str = "auto", k_clusters: int = 8):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.provider = provider
        self.k_clusters = k_clusters
        self.layers: List[Dict] = []

    def run_full_workflow(self, prompt: str,
                          input_image: Optional[str] = None) -> Optional[str]:
        """运行完整工作流
        返回最终PSD文件路径
        """
        print("=" * 80)
        print("🎬 Live2D Master Workflow - 完整工作流")
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
        if psd_path:
            print(f"\n🎉 完整工作流完成！")
            print(f"📦 最终PSD文件: {psd_path}")
            print(f"📁 输出目录: {layer_dir}")

        return psd_path

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
        """评估Live2D适配度
        """
        img = Image.open(image_path).convert("RGBA")
        width, height = img.size
        img_array = np.array(img)

        # 检测边缘清晰度
        from scipy.ndimage import sobel
        edge_x = sobel(img_array[:, :, 0], axis=0)
        edge_y = sobel(img_array[:, :, 0], axis=1)
        edge_strength = np.sqrt(edge_x**2 + edge_y**2).mean()

        # 检测颜色数量
        unique_colors = len(np.unique(img_array.reshape(-1, 3), axis=0))

        # 检测透明度分布
        alpha = img_array[:, :, 3]
        has_transparent = np.any(alpha < 255)

        report = []
        report.append(f"📐 图片尺寸: {width}x{height}")
        report.append(f"🎨 颜色数量: {unique_colors:,}")
        report.append(f"⚡ 边缘清晰度: {edge_strength:.1f}")
        report.append(f"🔍 透明区域: {'有' if has_transparent else '无'}")
        report.append("")

        if edge_strength > 30 and unique_colors < 1000:
            report.append("✅ 非常适合分层！")
        elif edge_strength > 15:
            report.append("👍 可以分层，建议增加边缘清晰度")
        else:
            report.append("⚠️ 边缘不够清晰，建议优化原图")

        return "\n".join(report)

    def _optimize_image(self, image_path: str) -> Optional[str]:
        """优化图像以适合Live2D分层
        """
        img = Image.open(image_path).convert("RGBA")
        width, height = img.size
        img_array = np.array(img)

        # 优化1：增强边缘
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(img)
        img_contrast = enhancer.enhance(1.2)
        enhancer_sharp = ImageEnhance.Sharpness(img_contrast)
        img_sharp = enhancer_sharp.enhance(1.5)

        # 优化2：处理背景为白色
        img_array_sharp = np.array(img_sharp)
        for y in range(height):
            for x in range(width):
                r, g, b, a = img_array_sharp[y, x]
                # 将浅色背景转为白色透明
                if r > 240 and g > 240 and b > 240:
                    img_array_sharp[y, x] = [255, 255, 255, 0]

        optimized = Image.fromarray(img_array_sharp)
        output_path = self.output_dir / f"optimized_{Path(image_path).name}"
        optimized.save(output_path)

        print(f"✅ 图像优化完成")
        print(f"📁 输出: {output_path}")
        return str(output_path)

    def _perform_layering(self, image_path: str) -> Optional[str]:
        """执行智能分层
        """
        from sklearn.cluster import KMeans

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

        kmeans = KMeans(n_clusters=self.k_clusters, random_state=42)
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

        print(f"🎨 颜色聚类完成: {len(colors)}个颜色簇")

        # 为每个颜色创建图层
        self.layers = []
        for i, color in enumerate(colors):
            mask = labels == i

            # 识别部件类型
            avg_alpha = np.mean(pixels[mask][:, 3]) if mask.any() else 0
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

    def _color_distance(self, color1: Tuple, color2: Tuple) -> float:
        """计算两个颜色之间的欧氏距离
        """
        return np.sqrt(sum((a - b)**2 for a, b in zip(color1, color2)))

    def _identify_part_type(self, color: Tuple, alpha: float) -> str:
        """根据颜色识别部件类型
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
        """生成分层指南
        """
        guide_path = layer_dir / "分层指南.txt"
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("📺 Live2D 分层指南\n")
            f.write("=" * 80 + "\n\n")

            f.write("📋 基础信息\n")
            f.write("-" * 80 + "\n")
            f.write(f"原图尺寸: {image_size[0]}x{image_size[1]}\n")
            f.write(f"图层数量: {len(self.layers)}\n\n")

            f.write("🎨 图层列表（按从后往前顺序\n")
            f.write("-" * 80 + "\n")
            for layer in sorted(self.layers, key=lambda x: x["id"]):
                f.write(f"{layer['id']:02d}. {layer['type']} ({layer['filename']})\n")

            f.write("\n📖 Live2D分层顺序建议\n")
            f.write("-" * 80 + "\n")
            for layer in self.LIVE2D_LAYER_ORDER:
                f.write(f"{layer}\n")

            f.write("\n💡 导入Live2D Cubism Editor\n")
            f.write("-" * 80 + "\n")
            f.write("1. File -> Import PSD\n")
            f.write("2. 勾选 Create ArtMeshes\n")
            f.write("3. 按建议顺序排列图层\n")

        print(f"📖 分层指南已保存: {guide_path}")

    def _create_psd(self, layer_dir: str) -> Optional[str]:
        """创建PSD文件（使用简单的PNG替代方案）
        真实PSD需要psd-tools库，这里提供标准输出
        """
        try:
            from psd_tools import PSDImage, Layer
        except ImportError:
            print("⚠️ psd-tools库未安装，生成PNG分层包")
            print("💡 如需完整PSD，运行: pip install psd-tools")
            return layer_dir

        try:
            # 创建PSD
            layer_path = Path(layer_dir)
            layer_files = sorted(layer_path.glob("*.png"))

            if not layer_files:
                return None

            first_img = Image.open(str(layer_files[0]))
            width, height = first_img.size

            psd = PSDImage.new(width, height, color_mode="RGBA")

            # 添加图层（从后往前）
            for layer_file in reversed(layer_files):
                if "原图" in str(layer_file):
                    continue

                img = Image.open(str(layer_file)).convert("RGBA")
                layer = Layer.frompil(img, name=layer_file.stem)
                psd.append(layer)

            psd_path = layer_path / "layers.psd"
            psd.save(psd_path)

            print(f"✅ PSD文件生成成功: {psd_path}")
            return str(psd_path)

        except Exception as e:
            print(f"⚠️ PSD生成失败: {e}")
            return layer_dir


def main():
    parser = argparse.ArgumentParser(
        description="Live2D Master Workflow - 端到端完整工作流 v1.0",
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
""",
    )
    parser.add_argument("prompt", nargs="?", default="蓝发猫耳少女", help="角色描述提示词")
    parser.add_argument("--input", type=str, help="现有图片路径")
    parser.add_argument("--k", type=int, default=8, help="颜色聚类数量（默认8）")
    parser.add_argument("--output", type=str, default="./output", help="输出目录")
    parser.add_argument("--provider", type=str, default="sensenova", help="生成Provider（sensenova/local）")

    args = parser.parse_args()

    workflow = Live2DWorkflow(
        output_dir=args.output,
        provider=args.provider,
        k_clusters=args.k,
    )

    result = workflow.run_full_workflow(
        prompt=args.prompt,
        input_image=args.input,
    )

    if not result:
        print("\n❌ 工作流执行失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
