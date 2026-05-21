#!/usr/bin/env python3
"""
Live2D Master Agent - 一键生成工具
版本: 3.1
特点: 完全免费，无需配置，一行命令生成图片
提示: 如需更高质量，可运行 python config_api.py 配置 API Key
"""

import sys
import urllib.request
import urllib.parse
import time
from pathlib import Path

def check_api_config() -> bool:
    """检查是否已配置 API Key"""
    try:
        from config import config
        return config.has_api_key
    except:
        return False


def print_tips():
    """打印使用提示"""
    print()
    print("💡 提示:")
    print("  - 免费方案（当前使用）: Pollinations.ai")
    if check_api_config():
        print("  - 🔑 已配置 API Key，可使用更高质量的 Seedream:")
        print("     python scripts/seedream_image_generate.py --prompt \"描述\"")
    else:
        print("  - 想要更高质量？配置 API Key:")
        print("     python config_api.py")
    print()


def generate(prompt: str, output_dir: str = "./output") -> str:
    """
    一键生成图片
    
    参数:
        prompt: 角色描述
        output_dir: 输出目录
    
    返回:
        图片路径
    """
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # 添加 Live2D 优化提示词
    full_prompt = f"{prompt}, perfect for Live2D rigging, clean layer separation, isolated character on white background, sharp clean lines, vibrant colors, ultra detailed, masterpiece"
    
    # 构建URL
    encoded = urllib.parse.quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}"
    
    # 下载图片
    output_file = output_path / f"live2d_{int(time.time())}.png"
    
    print(f"🎨 生成中...")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    
    with urllib.request.urlopen(req, timeout=120) as response:
        with open(output_file, 'wb') as f:
            f.write(response.read())
    
    print(f"✅ 完成: {output_file}")
    
    # 打印提示
    print_tips()
    
    return str(output_file)


# 命令行使用
if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "anime girl, pink hair, JK uniform"
    
    generate(prompt)
