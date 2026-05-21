#!/usr/bin/env python3
"""
Live2D Master Agent - 本地图像生成器
版本: 1.0
功能: 使用本地 diffusers 生成图片，无需网络
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    print("🔍 检查依赖...")
    
    packages = ['torch', 'diffusers', 'transformers', 'accelerate']
    missing = []
    
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"  ✅ {pkg}")
        except ImportError:
            print(f"  ❌ {pkg} 未安装")
            missing.append(pkg)
    
    return missing

def install_dependencies(missing):
    """安装缺失的依赖"""
    if not missing:
        return True
    
    print("\n📦 安装缺失的依赖...")
    print("这可能需要几分钟...")
    
    for pkg in missing:
        print(f"安装 {pkg}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg], 
                                stdout=subprocess.DEVNULL, 
                                stderr=subprocess.DEVNULL)
            print(f"  ✅ {pkg} 安装成功")
        except Exception as e:
            print(f"  ❌ {pkg} 安装失败: {e}")
            return False
    
    return True

def generate_local(prompt: str, output_dir: str = "./output"):
    """使用本地 diffusers 生成图片"""
    try:
        import torch
        from diffusers import StableDiffusionPipeline
        
        print(f"🎨 使用本地模型生成图片...")
        print(f"提示词: {prompt}")
        
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # 加载模型
        print("📥 加载模型（首次可能需要下载）...")
        model_id = "stablediffusionapi/anything-v5"
        
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float32,  # 使用 float32 以支持 CPU
            safety_checker=None
        )
        
        # 使用 CPU
        pipe = pipe.to("cpu")
        
        # 生成图片
        print("✨ 正在生成，请稍候...")
        image = pipe(
            prompt=prompt + ", perfect for Live2D rigging, clean layer separation, isolated character on white background",
            num_inference_steps=20,
            guidance_scale=7.5
        ).images[0]
        
        # 保存图片
        output_file = output_path / f"local_gen_{int(__import__('time').time())}.png"
        image.save(output_file)
        
        print(f"✅ 生成完成: {output_file}")
        return str(output_file)
        
    except Exception as e:
        print(f"❌ 本地生成失败: {e}")
        return None

def main():
    """主函数"""
    print("=" * 70)
    print("🎨 Live2D Master Agent - 本地图像生成器")
    print("=" * 70)
    print()
    
    # 检查依赖
    missing = check_dependencies()
    
    if missing:
        print("\n⚠️ 部分依赖缺失")
        response = input("是否安装缺失的依赖？(y/n): ").strip().lower()
        
        if response == 'y':
            if not install_dependencies(missing):
                print("\n❌ 依赖安装失败")
                print("\n💡 备选方案:")
                print("  1. 手动安装: pip install torch diffusers transformers accelerate")
                print("  2. 访问在线工具:")
                print("     - https://pollinations.ai")
                print("     - https://huggingface.co/spaces")
                print("     - https://civitai.com")
                return
        else:
            print("\n💡 备选方案:")
            print("  1. 手动安装: pip install torch diffusers transformers accelerate")
            print("  2. 访问在线工具:")
            print("     - https://pollinations.ai")
            print("     - https://huggingface.co/spaces")
            print("     - https://civitai.com")
            return
    
    # 获取提示词
    print()
    prompt = input("请输入角色描述（直接回车使用默认）: ").strip()
    
    if not prompt:
        prompt = "anime girl, cute, pink hair, JK uniform"
        print(f"使用默认提示词: {prompt}")
    
    # 生成图片
    print()
    result = generate_local(prompt)
    
    if not result:
        print("\n⚠️ 本地生成失败")
        print("\n💡 建议:")
        print("  1. 确保有足够的内存（建议 8GB+）")
        print("  2. 考虑使用 GPU 版本 PyTorch")
        print("  3. 或者使用在线免费工具")

if __name__ == "__main__":
    main()
