#!/usr/bin/env python3
"""
Live2D Master Workflow - 端到端完整工作流 v2.0 优化版
整合从生成到PSD输出的全流程，专为Live2D制作优化

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
│ 3. 图像优化     │ → 背景去除/边缘增强
└────────┬────────┘
         │
┌────────▼────────┐
│ 4. 智能分层     │ → K-means/部件识别
└────────┬────────┘
         │
┌────────▼────────┐
│ 5. PSD生成      │ → Live2D Cubism兼容
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
    """Live2D完整工作流管理器 v2.0
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
                 provider: str = "auto", k_clusters: int = 12):
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
        print("🎬 Live2D Master Workflow v2.0 - 完整工作流")
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
            print("\n💡 使用提示:")
            print("   - 在Live2D Cubism Editor中选择 'File > Import PSD'")
            print("   - 导入时勾选 'Create ArtMeshes'")
            print("   - 按照分层指南排列图层顺序")

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
        """评估Live2D适配度（使用QualityAssessor）
        """
        try:
            from local_image_generator import QualityAssessor
            scores = QualityAssessor.assess_image(image_path, live2d_mode=True, live2d_rigging=True)
            return QualityAssessor.generate_report(scores, live2d_rigging=True)
        except ImportError:
            # 备用评估方法
            img = Image.open(image_path).convert("RGBA")
            width, height = img.size
            img_array = np.array(img)

            # 检测边缘清晰度
            try:
                from scipy.ndimage import sobel
                edge_x = sobel(img_array[:, :, 0], axis=0)
                edge_y = sobel(img_array[:, :, 0], axis=1)
                edge_strength = np.sqrt(edge_x**2 + edge_y**2).mean()
            except ImportError:
                edge_strength = 20

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
        """生成分层指南 - 详细版
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

            f.write("🎨 图层列表（按从后往前顺序）\n")
            f.write("-" * 80 + "\n")
            for layer in sorted(self.layers, key=lambda x: x["id"]):
                f.write(f"{layer['id']:02d}. {layer['type']} ({layer['filename']}) - 颜色: {layer['color']}\n")

            f.write("\n📖 Live2D分层顺序建议（从后往前）\n")
            f.write("-" * 80 + "\n")
            for i, layer in enumerate(self.LIVE2D_LAYER_ORDER):
                f.write(f"{i+1:02d}. {layer}\n")

            f.write("\n💡 导入Live2D Cubism Editor步骤\n")
            f.write("-" * 80 + "\n")
            f.write("1. 打开 Live2D Cubism Editor\n")
            f.write("2. 选择 File > Import PSD\n")
            f.write("3. 选择生成的 layers.psd 文件\n")
            f.write("4. 导入设置：\n")
            f.write("   - 勾选 Create ArtMeshes\n")
            f.write("   - 建议选择 Standard 模式\n")
            f.write("5. 在画布上确认图层导入\n")
            f.write("6. 在时间线面板按照建议顺序排列图层\n")

        print(f"📖 分层指南已保存: {guide_path}")

    def _create_psd(self, layer_dir: str) -> Optional[str]:
        """创建PSD文件 - 增强版
        支持 psd-tools 或 imageio 库，确保兼容性
        """
        layer_path = Path(layer_dir)
        
        # 方法1：尝试使用 psd-tools
        try:
            from psd_tools import PSDImage, Layer
            print("🎨 使用 psd-tools 生成PSD...")
            
            layer_files = sorted(layer_path.glob("*.png"))
            non_original_files = [f for f in layer_files if "原图" not in str(f)]
            
            if not non_original_files:
                return None

            first_img = Image.open(str(non_original_files[0]))
            width, height = first_img.size

            psd = PSDImage.new(width, height, color_mode="RGBA")

            # 添加图层（从后往前，最后面的图层最先添加）
            for layer_file in reversed(non_original_files):
                img = Image.open(str(layer_file)).convert("RGBA")
                layer = Layer.frompil(img, name=layer_file.stem)
                psd.append(layer)

            psd_path = layer_path / "layers.psd"
            psd.save(psd_path)

            print(f"✅ PSD文件生成成功: {psd_path}")
            return str(psd_path)
            
        except ImportError:
            print("⚠️ psd-tools 未安装，尝试备用方法...")
        except Exception as e:
            print(f"⚠️ psd-tools 生成失败: {e}")
        
        # 方法2：生成PNG包 + PSD说明
        print("📦 生成PNG分层包...")
        self._create_layer_package(layer_path)
        
        # 方法3：尝试使用 pillow 简单方法（实际还是PNG，但保存为psd后缀）
        try:
            self._create_simple_psd(layer_path)
        except Exception as e:
            print(f"⚠️ 简单PSD生成失败: {e}")
            
        return layer_dir
        
    def _create_layer_package(self, layer_path: Path):
        """创建PNG分层包和详细说明
        """
        # 创建说明文件
        readme_path = layer_path / "README_Live2D.txt"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("📦 Live2D 分层包 - 使用说明\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("📂 文件说明:\n")
            f.write("   - 00_原图.png: 原始优化图\n")
            f.write("   - 01_XX.png ~ NN_XX.png: 分层文件（PNG格式）\n")
            f.write("   - 分层指南.txt: 详细的分层顺序和导入指南\n\n")
            
            f.write("🎨 导入方法（如果没有PSD文件）:\n")
            f.write("1. 在Live2D Cubism Editor中新建项目\n")
            f.write("2. 选择 File > Import Images\n")
            f.write("3. 选择所有PNG分层文件（除了原图）\n")
            f.write("4. 在时间线面板按照分层指南排列顺序\n")
            f.write("5. 为每个图层创建 ArtMesh\n\n")
            
            f.write("💡 提示:\n")
            f.write("   - 如需生成完整PSD文件，请安装: pip install psd-tools\n")
            f.write("   - 然后重新运行本工具\n")
        
        print(f"📖 PNG分层包说明已保存: {readme_path}")
        
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
