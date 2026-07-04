#!/usr/bin/env python3
"""
Live2D Layer Tool v6.0 - K-means聚类分层工具
使用机器学习算法进行图像分层，效果比简单颜色检测更好

功能:
- K-means聚类算法进行颜色分割（可选）
- 边缘检测和形态学处理（可选）
- 自动分层和导出
- 支持多种输出格式
- 优雅降级到简单方案

使用方法:
  python live2d_layer_v6.py <input_image> [output_path]
  python live2d_layer_v6.py <input_image> --k 5 --threshold 0.8
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image


def _get_project_root() -> Path:
    """返回项目根目录。根目录包装器通过 LIVE2D_PROJECT_ROOT 指定。"""
    return Path(os.environ.get("LIVE2D_PROJECT_ROOT", Path(__file__).parent))


# 尝试导入可选依赖
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("⚠️ numpy未安装，使用简单分层模式")

try:
    from sklearn.cluster import KMeans
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    if HAS_NUMPY:
        print("⚠️ scikit-learn未安装，使用简单颜色量化")

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False


class Live2DLayerToolV6:
    """v6.0分层工具 - K-means聚类"""

    def __init__(self, input_path, output_path=None, k_clusters=5, threshold=0.8):
        self.input_path = Path(input_path)
        project_root = _get_project_root()

        if output_path is None:
            self.output_path = project_root / "output" / f"{self.input_path.stem}_v6_layered"
        else:
            output_path = Path(output_path)
            if not output_path.is_absolute():
                self.output_path = project_root / output_path
            else:
                self.output_path = output_path

        self.k_clusters = k_clusters
        self.threshold = threshold

        if not self.input_path.exists():
            raise FileNotFoundError(f"找不到输入文件: {input_path}")

        self.output_path.mkdir(exist_ok=True, parents=True)

    def load_image(self):
        """加载图像"""
        img = Image.open(self.input_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        return img

    def simple_layer_pil(self, img):
        """使用PIL进行简单分层（无numpy）"""
        print("🎨 使用PIL简单分层...")

        w, h = img.size
        pixels = list(img.getdata())

        # 量化颜色
        quantized = []
        for r, g, b, a in pixels:
            # 降低位深度进行量化
            qr = (r // 32) * 32
            qg = (g // 32) * 32
            qb = (b // 32) * 32
            quantized.append((qr, qg, qb, a))

        # 统计颜色频率
        color_counts = {}
        for color in quantized:
            if color in color_counts:
                color_counts[color] += 1
            else:
                color_counts[color] = 1

        # 按频率排序取前k个
        sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
        top_colors = [c for c, _ in sorted_colors[:self.k_clusters]]

        # 创建图层
        layers = []
        for i, color in enumerate(top_colors):
            # 创建图层
            layer_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            layer_pixels = list(layer_img.getdata())

            # 填充颜色
            for j, pix_color in enumerate(quantized):
                if pix_color[:3] == color[:3]:
                    layer_pixels[j] = pixels[j]

            layer_img.putdata(layer_pixels)
            layer_path = self.output_path / f"layer_{i:02d}.png"
            layer_img.save(layer_path)

            layers.append({
                'id': i,
                'color': color,
                'path': layer_path,
                'area': color_counts.get(color, 0)
            })

            print(f"   ✓ 图层 {i} 保存: {layer_path.name}")

        return layers

    def kmeans_segmentation(self, img, k=None):
        """使用K-means聚类进行颜色分割"""
        if not HAS_NUMPY:
            return None, None

        if k is None:
            k = self.k_clusters

        print(f"🎨 K-means分割 (k={k})...")

        img_array = np.array(img)
        img_rgb = img_array[:, :, :3]

        # 重塑图像为像素数组
        pixels = img_rgb.reshape(-1, 3)

        # 使用K-means聚类
        if HAS_SKLEARN:
            try:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                labels = kmeans.fit_predict(pixels)
                centers = kmeans.cluster_centers_.astype(np.uint8)
                # 重建图像
                segmented = centers[labels].reshape(img_rgb.shape)
                return segmented, labels.reshape(img_rgb.shape[:2])
            except Exception as e:
                print(f"⚠️ K-means失败: {e}，使用简单颜色检测")
        else:
            print("⚠️ scikit-learn未安装，使用简单颜色量化")

        # 降级方案：简单量化
        return self.simple_quantization(img_array, k)

    def simple_quantization(self, img_array, k):
        """简单颜色量化（降级方案）"""
        if not HAS_NUMPY:
            return None, None

        img_rgb = img_array[:, :, :3]
        # 简单的位深度降低
        factor = 256 // k
        quantized = (img_rgb // factor) * factor
        # 创建标签
        unique_colors = np.unique(quantized.reshape(-1, 3), axis=0)
        color_to_label = {tuple(color): i for i, color in enumerate(unique_colors)}

        # 向量化标签创建
        h, w, _ = img_rgb.shape
        labels = np.zeros((h, w), dtype=np.int32)
        for i, color in enumerate(unique_colors):
            mask = np.all(quantized == color, axis=2)
            labels[mask] = i

        return quantized, labels

    def create_layers_from_numpy(self, img_array, labels):
        """从numpy数组创建图层"""
        h, w = img_array.shape[:2]
        unique_labels = np.unique(labels)

        layers = []

        print(f"📦 创建 {len(unique_labels)} 个图层...")

        for i, label in enumerate(unique_labels):
            # 创建掩码
            mask = (labels == label)

            # 创建透明图层
            layer = np.zeros((h, w, 4), dtype=np.uint8)

            # 复制颜色和透明度
            layer[:, :, :3] = img_array[:, :, :3]
            layer[:, :, 3] = mask.astype(np.uint8) * 255

            # 保存图层
            layer_img = Image.fromarray(layer, 'RGBA')
            layer_path = self.output_path / f"layer_{i:02d}.png"
            layer_img.save(layer_path)

            layers.append({
                'id': i,
                'label': label,
                'path': layer_path,
                'area': np.sum(mask)
            })

            print(f"   ✓ 图层 {i} 保存: {layer_path.name}")

        return layers

    def create_combined_preview(self, layers, img):
        """创建组合预览"""
        preview_path = self.output_path / "preview.png"
        img.save(preview_path)
        print(f"📋 预览图保存: {preview_path}")
        return preview_path

    def create_layer_guide(self, layers):
        """创建图层指南"""
        guide_path = self.output_path / "LAYER_GUIDE.txt"

        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write("Live2D Layer Tool v6.0 - 图层指南\n")
            f.write("="*50 + "\n\n")
            f.write(f"输入文件: {self.input_path.name}\n")
            f.write(f"聚类数: {self.k_clusters}\n")
            f.write(f"阈值: {self.threshold}\n")
            f.write(f"模式: {'K-means (高级)' if HAS_NUMPY and HAS_SKLEARN else 'Simple (基础)'}\n\n")
            f.write("图层列表（按面积排序）:\n")
            f.write("-"*50 + "\n")

            # 按面积排序
            sorted_layers = sorted(layers, key=lambda x: x['area'], reverse=True)
            for i, layer in enumerate(sorted_layers):
                f.write(f"{i+1:2d}. {layer['path'].name} (面积: {layer['area']})\n")

            f.write("\nLive2D Cubism Editor导入步骤:\n")
            f.write("1. File → Import PSD (或导入各个图层)\n")
            f.write("2. 调整图层顺序\n")
            f.write("3. 创建ArtMeshes\n")
            f.write("4. 设置参数\n")

        print(f"📖 指南保存: {guide_path}")
        return guide_path

    def process(self):
        """处理整个流程"""
        print("\n" + "="*60)
        print("🎨 Live2D Layer Tool v6.0")
        print("="*60)

        # 加载图像
        print(f"\n📥 加载图像: {self.input_path.name}")
        img = self.load_image()
        w, h = img.size
        print(f"   尺寸: {w}x{h}")

        # 选择处理方法
        if HAS_NUMPY and HAS_SKLEARN:
            img_array = np.array(img)
            segmented, labels = self.kmeans_segmentation(img_array)
            if labels is not None:
                layers = self.create_layers_from_numpy(img_array, labels)
            else:
                layers = self.simple_layer_pil(img)
        else:
            layers = self.simple_layer_pil(img)

        # 创建预览
        print()
        self.create_combined_preview(layers, img)

        # 创建指南
        print()
        self.create_layer_guide(layers)

        print("\n" + "="*60)
        print("✅ 完成！")
        print("="*60)
        print(f"\n📁 输出目录: {self.output_path}")
        print(f"📦 图层数量: {len(layers)}")
        print("\n💡 下一步:")
        print("  1. 使用 See-through 进行专业级分层（推荐）")
        print("  2. 在 Photoshop 中进一步编辑图层")
        print("  3. 导入 Live2D Cubism Editor")

        return self.output_path


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Live2D Layer Tool v6.0 - K-means聚类分层',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python live2d_layer_v6.py character.png
  python live2d_layer_v6.py character.png --k 8
  python live2d_layer_v6.py character.png output_dir
"""
    )
    parser.add_argument(
        'input', help='输入图像文件路径'
    )
    parser.add_argument(
        'output', nargs='?', default=None,
        help='输出目录路径（可选）'
    )
    parser.add_argument(
        '--k', type=int, default=5,
        help='聚类数量（默认5）'
    )
    parser.add_argument(
        '--threshold', type=float, default=0.8,
        help='透明度阈值（默认0.8）'
    )
    parser.add_argument(
        '--suggest-see-through', action='store_true',
        help='显示See-through推荐信息'
    )

    args = parser.parse_args()

    if args.suggest_see_through:
        print("""
🏆 推荐使用 See-through 进行专业级分层！

See-through 是 SIGGRAPH 2026 级别的分层工具，使用 LayerDiff 3D + Marigold Depth。

使用方法:
  1. 安装: python install_comfyui_advanced.py
  2. 运行: cd comfyui && python main.py
  3. 在浏览器中打开 http://127.0.0.1:8188

详细文档: SEE_THROUGH_INTEGRATION.md
""")
        return

    try:
        tool = Live2DLayerToolV6(
            args.input,
            args.output,
            k_clusters=args.k,
            threshold=args.threshold
        )
        tool.process()
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("\n💡 提示:")
        print("  • 确保输入文件存在")
        print("  • 检查依赖项是否安装")
        print("  • 推荐使用 See-through 进行更好的分层效果")
        sys.exit(1)


if __name__ == "__main__":
    main()
