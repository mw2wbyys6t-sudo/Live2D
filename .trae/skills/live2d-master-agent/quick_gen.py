#!/usr/bin/env python3
"""
Live2D Master Agent - 一键生成工具
版本: 3.0
特点: 完全免费，无需配置，一行命令生成图片
"""

import sys
import urllib.request
import urllib.parse
import time
from pathlib import Path


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
    return str(output_file)


# 命令行使用
if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "anime girl, pink hair, JK uniform"
    
    generate(prompt)
