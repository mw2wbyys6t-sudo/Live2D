#!/usr/bin/env python3
"""
Live2D Master Agent - 极简版 v4.0
功能: 图片生成 + PSD转换
无循环，直接输出结果
"""

import os
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

def get_latest_image(output_dir):
    """获取最新图片"""
    png_files = sorted(output_dir.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    return str(png_files[0]) if png_files else None

def download_image(url, output_path):
    """下载图片"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': 'https://pollinations.ai/'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=120) as response:
            data = response.read()
            if len(data) < 1000:
                return False
            with open(output_path, 'wb') as f:
                f.write(data)
        return True
    except:
        return False

def generate_image(prompt, output_dir):
    """生成图片"""
    print(f"✅ 正在生成图片...")
    print(f"📝 提示词: {prompt}")
    
    optimizations = ", perfect for Live2D rigging, clean layer separation, isolated character on white background, sharp clean lines, vibrant colors, ultra detailed, masterpiece"
    full_prompt = prompt + optimizations
    encoded = urllib.parse.quote(full_prompt)
    seed = int(time.time()) % 1000000
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=768&height=768&seed={seed}"
    
    output_file = output_dir / f"live2d_{int(time.time())}.png"
    
    if download_image(url, output_file):
        print(f"✅ 图片生成成功: {output_file.name}")
        return str(output_file)
    else:
        print("❌ 图片生成失败")
        return None

def create_psd_plan(image_path, output_dir):
    """创建PSD分层规划"""
    try:
        from PIL import Image
        img = Image.open(image_path)
        plan_dir = output_dir / f"psd_plan_{int(time.time())}"
        plan_dir.mkdir(exist_ok=True)
        img.save(plan_dir / "reference.png")
        
        layers = [
            "ArtMesh/Body - 身体",
            "ArtMesh/Hair_Back - 头发后部",
            "ArtMesh/Clothes - 服装",
            "ArtMesh/Hair_Side - 头发侧部",
            "ArtMesh/Face - 脸部",
            "ArtMesh/Eyes - 眼睛",
            "ArtMesh/Mouth - 嘴巴",
            "ArtMesh/Hair_Front - 头发前部",
            "ArtMesh/Hands - 手",
            "ArtMesh/Accessories - 配饰"
        ]
        
        with open(plan_dir / "LAYER_GUIDE.txt", 'w', encoding='utf-8') as f:
            f.write("Live2D PSD 分层指南\n")
            f.write(f"图片尺寸: {img.size[0]} x {img.size[1]}\n\n")
            for layer in layers:
                f.write(f"- {layer}\n")
        
        print(f"✅ 分层规划已创建")
        return str(plan_dir)
    except:
        print("⚠️  创建分层规划失败")
        return None

def convert_to_psd(image_path):
    """转换为PSD"""
    try:
        from PIL import Image
        img = Image.open(image_path)
        psd_path = str(image_path).replace('.png', '_live2d.psd')
        
        try:
            img.save(psd_path)
            print(f"✅ PSD文件已创建: {Path(psd_path).name}")
            return psd_path
        except:
            png_path = str(image_path).replace('.png', '_live2d.png')
            img.save(png_path)
            print(f"✅ PNG文件已创建(可导入Photoshop转换): {Path(png_path).name}")
            print("💡 提示: 使用Photoshop打开PNG后另存为PSD格式")
            return png_path
    except:
        print("⚠️  PSD转换失败")
        return None

def main():
    """主函数"""
    base_dir = Path(__file__).parent
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)
    
    print("\n" + "=" * 60)
    print("🎨 Live2D Master Agent v4.0")
    print("=" * 60)
    
    # 参数处理
    skip_generate = False
    prompt = "anime girl, cute, pink hair"
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--skip-generate':
            skip_generate = True
        elif sys.argv[1] in ['-h', '--help']:
            print("""
使用方法:
  python master_tool.py                    # 默认生成
  python master_tool.py "提示词"           # 自定义提示词
  python master_tool.py --skip-generate    # 使用已有图片
            """)
            return
        else:
            prompt = " ".join(sys.argv[1:])
    
    # 获取图片
    image_path = None
    
    if skip_generate:
        image_path = get_latest_image(output_dir)
        if image_path:
            print(f"📁 使用已有图片: {Path(image_path).name}")
        else:
            print("❌ output/ 目录中没有图片")
            return
    else:
        image_path = generate_image(prompt, output_dir)
        if not image_path:
            print("\n💡 备选方案:")
            print("1. 访问 https://pollinations.ai 在线生成")
            print("2. 将图片放到 output/ 目录后运行: python master_tool.py --skip-generate")
            print("3. 安装ComfyUI: python install_comfyui.py")
            return
    
    # 创建PSD规划
    create_psd_plan(image_path, output_dir)
    
    # 转换为PSD
    convert_to_psd(image_path)
    
    print("\n" + "=" * 60)
    print("🎉 完成!")
    print("=" * 60)
    print(f"\n📁 输出文件:")
    print(f"  - {Path(image_path).name}")
    print(f"  - {Path(image_path).stem}_live2d.psd")
    print(f"  - psd_plan_*/")

if __name__ == "__main__":
    main()
