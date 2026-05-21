#!/usr/bin/env python3
"""
快速PSD转换工具
将PNG图片转换为Live2D可用的格式
"""

import sys
from pathlib import Path
from PIL import Image

def convert_to_psd_ready(image_path):
    """
    准备图片并提供详细的PSD转换指南
    """
    print("=" * 70)
    print("🎨 Live2D PSD 快速转换工具")
    print("=" * 70)
    print()

    # 打开图片
    img = Image.open(image_path)
    base_name = Path(image_path).stem
    output_dir = Path(image_path).parent

    print(f"✅ 处理图片: {Path(image_path).name}")
    print(f"   尺寸: {img.size[0]} x {img.size[1]}")
    print()

    # 保存优化后的PNG
    ref_path = output_dir / f"{base_name}_ready.png"
    img.save(ref_path, format="PNG", optimize=True)
    print(f"✅ 优化图片已保存: {ref_path.name}")

    # 创建详细的转换指南
    guide_path = output_dir / f"{base_name}_PSD_GUIDE.txt"

    with open(guide_path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("Live2D PSD 转换指南 - 超简单版\n")
        f.write("=" * 70 + "\n\n")

        f.write("📋 3种方法转换为PSD:\n\n")

        f.write("方法1: 使用Photoshop（最推荐）\n")
        f.write("-" * 70 + "\n")
        f.write("1. 在Photoshop中打开: " + ref_path.name + "\n")
        f.write("2. 点击 File > Save As\n")
        f.write("3. 格式选择: Photoshop (*.PSD, *.PDD)\n")
        f.write("4. 保存文件名: " + base_name + "_live2d.psd\n")
        f.write("5. 点击保存即可！\n\n")

        f.write("方法2: 使用在线工具（无需安装软件）\n")
        f.write("-" * 70 + "\n")
        f.write("1. 访问网站: https://convertio.co/png-psd/\n")
        f.write("2. 上传: " + ref_path.name + "\n")
        f.write("3. 点击转换，下载PSD文件\n\n")

        f.write("   其他推荐在线工具:\n")
        f.write("   - https://www.aconvert.com/image/png-to-psd/\n")
        f.write("   - https://onlineconvertfree.com/convert/png-to-psd/\n\n")

        f.write("方法3: 使用GIMP（免费软件）\n")
        f.write("-" * 70 + "\n")
        f.write("1. 下载安装GIMP: https://www.gimp.org/\n")
        f.write("2. 在GIMP中打开: " + ref_path.name + "\n")
        f.write("3. File > Export As\n")
        f.write("4. 选择格式: Photoshop Image (*.PSD)\n")
        f.write("5. 保存！\n\n")

        f.write("✅ 导入Live2D:\n")
        f.write("-" * 70 + "\n")
        f.write("1. 打开 Live2D Cubism Editor\n")
        f.write("2. File > Import PSD (或直接拖入)\n")
        f.write("3. 选择转换好的PSD文件\n")
        f.write("4. 点击 OK 确认导入\n")
        f.write("5. 开始制作你的Live2D模型！\n\n")

        f.write("📝 可选: 分层建议\n")
        f.write("-" * 70 + "\n")
        f.write("如果你想要更好的效果，可以在Photoshop中分层:\n\n")
        f.write("图层顺序（从下往上）:\n")

        layers = [
            ("Body", "身体"),
            ("Hair_Back", "头发后部"),
            ("Clothes", "服装"),
            ("Hair_Side", "头发侧部"),
            ("Face", "脸部"),
            ("Eyes", "眼睛"),
            ("Mouth", "嘴巴"),
            ("Hair_Front", "头发前部"),
            ("Hands", "手"),
            ("Accessories", "配饰")
        ]

        for i, (eng, chn) in enumerate(layers, 1):
            f.write(f"  {i:2d}. {eng:15} ({chn})\n")

        f.write("\n")
        f.write("=" * 70 + "\n")
        f.write("💡 提示: 即使不分层，也可以直接导入Live2D！\n")
        f.write("=" * 70 + "\n")

    print(f"✅ 转换指南已保存: {guide_path.name}")
    print()
    print("=" * 70)
    print("🎉 准备完成！")
    print("=" * 70)
    print()
    print("📁 你的文件包:")
    print(f"   1. {ref_path.name:30} - 优化后的原图")
    print(f"   2. {guide_path.name:30} - 详细转换指南")
    print()
    print("💡 下一步:")
    print("   1. 下载这两个文件")
    print("   2. 查看转换指南选择适合你的方法")
    print("   3. 转换为PSD格式")
    print("   4. 导入Live2D开始制作！")
    print()
    print("=" * 70)

    return ref_path, guide_path


if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # 查找最新的PNG
        output_dir = Path.cwd() / "output"
        images = sorted(output_dir.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
        if images:
            image_path = str(images[0])
        else:
            print("❌ 没有找到PNG图片")
            sys.exit(1)

    convert_to_psd_ready(image_path)
