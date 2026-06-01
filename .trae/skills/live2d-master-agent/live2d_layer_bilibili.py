#!/usr/bin/env python3
"""
Live2D 分层工具 - B站优化版 v1.0
专为B站Live2D创作者设计的分层工具

特点：
- 🎨 颜色分层 + 智能部件识别
- 📺 分层预览 + 部件自动命名
- 📁 标准图层结构
- 🎬 适合B站教程友好的输出格式
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image
import numpy as np
from typing import Dict, List, Tuple


class Live2DLayerToolBilibili:
    """B站版Live2D分层工具
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
            (0, 0, 0),       # 黑色
            (20, 20, 20),    # 深灰
            (100, 50, 30), # 棕色
            (255, 200, 150), # 金色
            (200, 100, 150), # 粉色
            (100, 150, 200), # 蓝色
            (200, 200, 255), # 浅色
            (150, 150, 150), # 灰色
        ],
        "皮肤": [
            (255, 220, 200), # 浅色皮肤
            (255, 200, 180), # 浅粉
            (230, 180, 160), # 肤色
            (200, 160, 140), # 深肤色
        ],
        "眼睛": [
            (100, 150, 200), # 蓝色眼睛
            (200, 150, 100), # 棕色眼睛
            (150, 100, 200), # 紫色眼睛
            (255, 255, 255), # 白色眼白
            (50, 50, 50), # 瞳孔
        ],
        "衣服": [
            (200, 100, 100), # 红色衣服
            (100, 200, 100), # 绿色衣服
            (100, 100, 200), # 蓝色衣服
            (200, 200, 100), # 黄色衣服
            (200, 150, 200), # 紫色衣服
            (150, 200, 200), # 青色衣服
        ],
        "背景": [
            (240, 240, 250), # 浅色背景
            (255, 255, 255), # 白色背景
        ],
    }

    def __init__(self, image_path: str, output_dir: str = "./output",
                 k_clusters: int = 8, threshold: float = 0.8):
        self.image_path = image_path
        self.output_dir = Path(output_dir)
        self.k_clusters = k_clusters
        self.threshold = threshold
        self.layers: List[Dict] = []

    def _color_distance(self, color1: Tuple, color2: Tuple) -> float:
        """计算两个颜色之间的欧氏距离
        """
        return np.sqrt(sum((a - b) ** 2 for a, b in zip(color1, color2)))

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
                    min_dist = best_part = part

        return best_part

    def process(self) -> str:
        """执行分层处理
        返回输出目录路径
        """
        print("=" * 80)
        print("🎬 Live2D B站优化版 - 分层工具")
        print("=" * 80)

        img = Image.open(self.image_path).convert("RGBA")
        width, height = img.size
        print(f"📁 输入图片: {self.image_path}")
        print(f"📐 尺寸: {width}x{height}")

        # 创建输出目录
        timestamp = int(os.path.getmtime(self.image_path))
        output_path = self.output_dir / f"bilibili_layer_{timestamp}"
        output_path.mkdir(parents=True, exist_ok=True)

        # 保存原图
        img.save(output_path / "00_原图.png")
        print(f"\n✅ 原图已保存: 00_原图.png")

        # K-means 颜色聚类
        img_array = np.array(img)
        pixels = img_array.reshape(-1, 4)
        non_transparent = pixels[pixels[:, 3] > 50]

        if len(non_transparent) < 100:
            print("❌ 图片内容太少，无法分层")
            return None

        # 简单K-means
        from sklearn.cluster import KMeans

        kmeans = KMeans(n_clusters=self.k_clusters, random_state=42)
        kmeans.fit(non_transparent[:, :3])

        # 为每个像素分配聚类
        labels = np.zeros((height, width)
        for i, label in enumerate(pixels):
            if pixels[i][3] < 50:
                labels[h, w] = -1
            else:
                label = kmeans.predict([pixels[i][:3]])[0]
                labels[h, w] = label
            else:
                labels[i] = -1

        # 提取每个聚类的颜色
        colors = kmeans.cluster_centers_.astype(int)

        print(f"\n🎨 颜色聚类完成: {len(colors)}个颜色簇")

        # 为每个颜色创建图层
        for i, color in enumerate(colors):
            # 创建蒙版
            mask = np.zeros((height, width), dtype=bool)
            for h in range(height):
                for w in range(width):
                    mask[h, w] = labels[h, w] == i

            # 识别部件类型
            avg_alpha = np.mean(pixels[mask][:, 3]) if mask.any() else 0
            part_type = self._identify_part_type(tuple(color), avg_alpha)

            # 创建图层图像
            layer_img = img_array.copy()
            layer_img[~mask] = [0, 0, 0, 0]

            # 保存图层
            layer_pil = Image.fromarray(layer_img)
            layer_filename = f"{i+1:02d}_{part_type}.png"
            layer_pil.save(output_path / layer_filename)

            self.layers.append({
                "id": i+1,
                "type": part_type,
                "color": color.tolist(),
                "filename": layer_filename,
                "area": np.sum(mask),
            })

            print(f"✅ 图层 {i+1:02d}: {part_type} - {layer_filename}")

        # 生成分层指南
        self._create_guide(output_path, img.size)

        print(f"\n🎉 分层完成！")
        print(f"📁 输出目录: {output_path}")
        print(f"📦 图层数量: {len(self.layers)}")
        return str(output_path)

    def _create_guide(self, output_dir: Path, image_size: Tuple[int, int]):
        """生成B站友好的分层指南
        """
        guide_path = output_dir / "分层指南_B站版.txt"
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("📺 Live2D B站分层指南\n")
            f.write("=" * 80 + "\n\n")

            f.write("📋 基础信息\n")
            f.write("-" * 80 + "\n")
            f.write(f"原图尺寸: {image_size[0]}x{image_size[1]}\n")
            f.write(f"分层时间: {os.path.getmtime(self.image_path)}\n")
            f.write(f"图层数量: {len(self.layers)}\n\n")

            f.write("🎨 图层列表（按从后往前顺序\n")
            f.write("-" * 80 + "\n")
            for layer in sorted(self.layers, key=lambda x: x["id"]):
                f.write(f"{layer['id']:02d}. {layer['type']} ({layer['filename']}\n")

            f.write("\n📖 B站Live2D分层顺序建议\n")
            f.write("-" * 80 + "\n")
            for layer in self.LIVE2D_LAYER_ORDER:
                f.write(f"{layer}\n")

            f.write("\n💡 B站教程提示\n")
            f.write("-" * 80 + "\n")
            f.write("1. 导入 Live2D Cubism Editor: File -> Import PSD\n")
            f.write("2. 勾选 Create ArtMeshes\n")
            f.write("3. 按建议顺序排列图层\n")
            f.write("4. 添加部件设置参数\n")

        print(f"📖 分层指南已保存: {guide_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Live2D 分层工具 - B站优化版 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础分层
  python live2d_layer_bilibili.py character.png

  # 更多颜色数量
  python live2d_layer_bilibili.py character.png --k 10

  # 指定输出目录
  python live2d_layer_bilibili.py character.png --output my_output
""",
    )
    parser.add_argument("image", help="输入图片路径")
    parser.add_argument("--k", type=int, default=8, help="颜色聚类数量（默认8）")
    parser.add_argument("--threshold", type=float, default=0.8, help="透明度阈值（默认0.8）")
    parser.add_argument("--output", type=str, default="./output", help="输出目录")

    args = parser.parse_args()

    tool = Live2DLayerToolBilibili(
        args.image,
        output_dir=args.output,
        k_clusters=args.k,
        threshold=args.threshold,
    )
    result = tool.process()

    if not result:
        sys.exit(1)


if __name__ == "__main__":
    main()
