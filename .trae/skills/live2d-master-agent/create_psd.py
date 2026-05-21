#!/usr/bin/env python3
"""
Live2D Master Agent - 直接创建PSD文件工具
用于快速创建可导入Live2D的PSD文件
"""

import os
import sys
from pathlib import Path
from PIL import Image
import time

def create_live2d_psd(image_path, output_path=None):
    """
    创建可导入Live2D的PSD文件
    虽然不能完全自动分层，但创建一个包含参考图像和
    标准图层结构的PSD文件，便于后续在Photoshop中处理
    """
    print("=" * 70)
    print("🎨 Live2D PSD 文件创建工具")
    print("=" * 70)
    print()

    # 打开原始图片
    try:
        img = Image.open(image_path)
        print(f"✅ 图片已打开: {image_path}")
        print(f"   尺寸: {img.size[0]} x {img.size[1]}")
        print(f"   模式: {img.mode}")
    except Exception as e:
        print(f"❌ 无法打开图片: {e}")
        return None

    # 创建输出路径
    if output_path is None:
        base_dir = Path(image_path).parent
        base_name = Path(image_path).stem
        output_path = base_dir / f"{base_name}_live2d.psd"
    else:
        output_path = Path(output_path)

    # 确保输出目录存在
    output_path.parent.mkdir(exist_ok=True)

    print()
    print("📝 正在创建PSD文件...")

    # 方法1: 创建一个简单的PSD文件（使用基本方法）
    # 首先创建一个包含原图的参考PSD文件
    # 同时创建详细的操作指南

    # 步骤1: 保存原始图片的副本
    backup_path = output_path.parent / f"{output_path.stem}_reference.png"
    img.save(backup_path)
    print(f"   ✅ 参考图片已保存: {backup_path}")

    # 步骤2: 创建详细的Photoshop操作指南
    guide_path = output_path.parent / f"{output_path.stem}_README.txt"

    with open(guide_path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("Live2D PSD 文件制作指南\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"🎯 原始图片: {Path(image_path).name}\n")
        f.write(f"📐 尺寸: {img.size[0]} x {img.size[1]}\n")
        f.write(f"📁 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("📋 快速操作步骤:\n")
        f.write("-" * 70 + "\n\n")

        f.write("方法一: 使用Photoshop（推荐）\n")
        f.write("1. 打开 reference.png\n")
        f.write("2. 选择整个画布 (Ctrl+A)\n")
        f.write("3. 复制 (Ctrl+C)\n")
        f.write("4. 新建文档 (Ctrl+N) - 使用默认设置\n")
        f.write("5. 粘贴 (Ctrl+V)\n")
        f.write("6. 保存为 PSD 格式 (File > Save As > Photoshop)\n\n")

        f.write("方法二: 自动图层结构（在Photoshop中）\n")
        f.write("1. 打开 reference.png\n")
        f.write("2. 执行以下操作创建图层组:\n\n")

        f.write("图层结构（从下到上）:\n")
        layers = [
            ("身体", "Body - torso and body parts"),
            ("头发_后", "Hair_Back - back layer of hair"),
            ("服装", "Clothes - main clothing"),
            ("头发_侧", "Hair_Side - side hair layers"),
            ("脸", "Face - face base"),
            ("眼睛", "Eyes - both eyes on separate layers"),
            ("嘴巴", "Mouth - mouth layer"),
            ("头发_前", "Hair_Front - fringe/bangs"),
            ("手", "Hands - hand parts"),
            ("配饰", "Accessories - decorations"),
        ]

        for i, (name, desc) in enumerate(layers, 1):
            f.write(f"{i:2d}. {name:12} - {desc}\n")

        f.write("\n")
        f.write("-" * 70 + "\n")
        f.write("⚠️  Live2D 导入要求:\n")
        f.write("-" * 70 + "\n\n")
        f.write("- 使用英文图层名（推荐）\n")
        f.write("- 不要使用图层样式\n")
        f.write("- 保持图层结构清晰\n")
        f.write("- 建议使用图层蒙版\n")
        f.write("- 所有图层分辨率相同\n")
        f.write("- 颜色模式: RGB\n")
        f.write("- 保存格式: Photoshop PSD\n\n")

        f.write("-" * 70 + "\n")
        f.write("✅ 导入Live2D Cubism:\n")
        f.write("-" * 70 + "\n\n")
        f.write("1. 打开 Live2D Cubism Editor\n")
        f.write("2. File > Import PSD\n")
        f.write("3. 选择生成的PSD文件\n")
        f.write("4. 确认图层映射\n")
        f.write("5. 开始制作！\n\n")

        f.write("=" * 70 + "\n")

    print(f"   ✅ 操作指南已保存: {guide_path}")

    # 步骤3: 尝试使用psd-tools创建PSD（如果可用）
    try:
        import psd_tools
        print(f"   🔧 使用 psd-tools 创建PSD文件...")

        # 创建PSD文档
        from psd_tools import PSDImage
        from psd_tools.constants import BlendMode, ChannelID
        from psd_tools.api.layers import Layer, Group

        # 创建新的PSD
        psd = PSDImage.new(img.mode, img.size)

        # 添加原始参考图层
        ref_layer = Layer(psd, name="Reference", top=0, left=0,
                         bottom=img.size[1], right=img.size[0])

        # 添加数据
        ref_layer.image_data = img.tobytes()

        psd.append(ref_layer)

        # 创建ArtMesh组
        artmesh_group = Group(psd, name="ArtMesh", top=0, left=0,
                              bottom=img.size[1], right=img.size[0])
        psd.append(artmesh_group)

        # 在ArtMesh组内添加标准图层结构（空图层）
        layer_names = [
            "Body", "Hair_Back", "Clothes", "Hair_Side",
            "Face", "Eyes", "Mouth", "Hair_Front", "Hands", "Accessories"
        ]

        for layer_name in layer_names:
            layer = Layer(psd, name=layer_name, top=0, left=0,
                         bottom=img.size[1], right=img.size[0])
            artmesh_group.append(layer)

        # 保存PSD
        psd.save(output_path)
        print(f"   ✅ PSD文件已创建: {output_path}")

    except ImportError:
        print(f"   ⚠️  psd-tools不可用，使用替代方法")
        # 如果没有psd-tools，至少提供详细说明
        pass
    except Exception as e:
        print(f"   ⚠️  自动PSD创建遇到问题: {e}")
        print("   📝 请按照README.txt中的说明手动创建")

    print()
    print("=" * 70)
    print("✅ PSD 文件准备完成！")
    print("=" * 70)
    print()
    print("📁 生成的文件:")
    print(f"   📷 {backup_path.name} - 参考图片")
    print(f"   📄 {guide_path.name} - 操作指南")
    if output_path.exists():
        print(f"   🎨 {output_path.name} - PSD文件（可直接导入）")
    print()
    print("💡 下一步:")
    print("   1. 查看README.txt了解详细步骤")
    print("   2. 在Photoshop中打开参考图片")
    print("   3. 进行分层或直接导入")
    print("   4. 保存并导入Live2D")
    print()
    print("=" * 70)

    return str(output_path) if output_path.exists() else str(guide_path)


def main():
    """主函数"""
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # 默认使用示例图片
        output_dir = Path.cwd() / "output"
        image_files = sorted(output_dir.glob("*.png"),
                            key=lambda p: p.stat().st_mtime, reverse=True)

        if image_files:
            image_path = str(image_files[0])
        else:
            print("❌ 没有找到PNG图片")
            print("\n使用方法:")
            print(f"   python {Path(__file__).name} <图片路径>")
            return 1

    create_live2d_psd(image_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
