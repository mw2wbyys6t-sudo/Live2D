#!/usr/bin/env python3
"""
创建测试图像，用于验证Live2D工具流程
"""

from PIL import Image, ImageDraw, ImageColor
import random
from pathlib import Path


def create_test_image(output_path="test_character.png"):
    """创建一个简单的测试角色图像"""

    # 创建画布
    width, height = 512, 768
    img = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 画背景
    bg_color = (240, 248, 255, 255)
    draw.rectangle([(0, 0), (width, height)], fill=bg_color)

    # 画身体
    body_center_x = width // 2
    body_center_y = height // 2 + 100
    body_color = (255, 200, 200, 255)
    draw.ellipse(
        [body_center_x - 80, body_center_y - 100,
         body_center_x + 80, body_center_y + 120],
        fill=body_color, outline=(200, 150, 150, 255), width=2
    )

    # 画头
    head_center_x = width // 2
    head_center_y = height // 2 - 100
    skin_color = (255, 224, 189, 255)
    draw.ellipse(
        [head_center_x - 70, head_center_y - 70,
         head_center_x + 70, head_center_y + 70],
        fill=skin_color, outline=(200, 180, 160, 255), width=2
    )

    # 画头发
    hair_color = (180, 100, 200, 255)
    # 后发
    draw.ellipse(
        [head_center_x - 80, head_center_y - 90,
         head_center_x + 80, head_center_y + 50],
        fill=hair_color, outline=(150, 80, 170, 255), width=2
    )
    # 刘海
    draw.ellipse(
        [head_center_x - 60, head_center_y - 80,
         head_center_x + 60, head_center_y - 10],
        fill=hair_color, outline=(150, 80, 170, 255), width=2
    )

    # 画眼睛
    eye_color = (100, 150, 200, 255)
    # 左眼
    draw.ellipse(
        [head_center_x - 40, head_center_y - 15,
         head_center_x - 15, head_center_y + 15],
        fill=eye_color, outline=(80, 120, 160, 255), width=2
    )
    # 右眼
    draw.ellipse(
        [head_center_x + 15, head_center_y - 15,
         head_center_x + 40, head_center_y + 15],
        fill=eye_color, outline=(80, 120, 160, 255), width=2
    )

    # 画嘴巴
    mouth_color = (255, 150, 150, 255)
    draw.ellipse(
        [head_center_x - 20, head_center_y + 30,
         head_center_x + 20, head_center_y + 45],
        fill=mouth_color, outline=(200, 120, 120, 255), width=2
    )

    # 保存图像
    output_path = Path(output_path)
    img.save(output_path)
    print(f"✅ 测试图像已创建: {output_path}")
    print(f"   尺寸: {width}x{height}")

    return str(output_path)


if __name__ == "__main__":
    print("="*60)
    print("🎨 Live2D 测试图像生成器")
    print("="*60)

    test_image = create_test_image()

    print("\n💡 接下来可以:")
    print("  1. 使用 v6 分层工具: python live2d_layer_v6.py test_character.png")
    print("  2. 使用 v5 分层工具: python live2d_layer_pro.py test_character.png")
    print("  3. 安装 See-through: python install_comfyui_advanced.py")
    print("  4. 使用主工具: python master_tool.py \"anime girl\"")
    print("\n✅ 测试准备完成！")
