#!/usr/bin/env python3
"""
生成动漫少女立绘 - Live2D 专用
使用 Seedream 5.0 高质量生成
"""

import asyncio
import sys
import os

sys.path.insert(0, '/workspace/scripts')
from seedream_image_generate import seedream_generate

async def generate_anime_character():
    character_prompt = """
anime girl, cute kawaii style, beautiful face, big expressive eyes,
long flowing pink hair, soft pink gradient hair, hair strands detailed,
wearing JK school uniform, white blouse, navy blue pleated skirt,
red ribbon tie, school bag accessory,
slender figure, elegant pose, standing pose,
perfect for Live2D rigging, clean layer separation,
isolated character on white background, easy to rig,
sharp clean lines, vibrant colors, ultra detailed,
masterpiece, award-winning quality, professional artwork,
4K resolution, high quality render, anime art style,
soft lighting, detailed facial features, sparkling eyes
""".strip().replace('\n', ' ')

    tasks = [{
        "prompt": character_prompt
    }]

    print("🎨 开始生成动漫少女立绘...")
    print(f"📐 分辨率: 4096x4096 (4K)")
    print(f"🎯 模型: Seedream 5.0")
    print(f"✨ 质量: Ultra High Quality")
    print(f"📝 提示词长度: {len(character_prompt)} 字符")
    print()

    try:
        result = await seedream_generate(
            tasks=tasks,
            version="5.0",
            timeout=1200
        )

        if result.get("success"):
            print("✅ 生成成功！")
            print()
            print("📊 生成结果:")
            for i, task_result in enumerate(result.get("results", [])):
                print(f"  图像 {i+1}:")
                print(f"    - 状态: {task_result.get('status')}")
                if task_result.get('image_url'):
                    print(f"    - 图片URL: {task_result.get('image_url')}")
                if task_result.get('local_path'):
                    print(f"    - 本地路径: {task_result.get('local_path')}")
            
            return result
        else:
            print("❌ 生成失败")
            print(f"错误信息: {result.get('error')}")
            return None

    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        return None

if __name__ == "__main__":
    result = asyncio.run(generate_anime_character())
    
    if result and result.get("success"):
        print()
        print("=" * 60)
        print("🎉 立绘生成完成！")
        print("=" * 60)
        print()
        print("💡 下一步建议:")
        print("  1. 查看生成的图片")
        print("  2. 进行 PSD 分层规划")
        print("  3. 转换为分层 PSD 文件")
        print("  4. 进行 Live2D 质量检查")
