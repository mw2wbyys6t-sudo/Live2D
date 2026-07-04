#!/usr/bin/env python3
"""
Live2D AI分层工具 v4.0 - 依赖安装脚本
集成Qwen-Image-Layered、rembg、SAM等最先进的AI模型
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd_args, description):
    """运行命令并显示结果（安全版本）"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd_args, 
            shell=False, 
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout[-5000:] if len(result.stdout) > 5000 else result.stdout)
        print(f"✅ {description} 成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败!")
        if e.stderr:
            print(f"错误: {e.stderr[-2000:]}")
        return False

def check_installed(package):
    """检查包是否已安装（安全版本）"""
    try:
        result = subprocess.run(
            [sys.executable, "-c", f"import {package}"],
            shell=False,
            capture_output=True
        )
        return result.returncode == 0
    except:
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🎨 Live2D AI分层工具 v4.0 - 依赖安装                 ║
║                                                          ║
║     集成最先进的AI分层技术:                               ║
║     • Qwen-Image-Layered (阿里)                          ║
║     • rembg (背景移除)                                   ║
║     • SAM 2 (Meta)                                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # 检查Python版本
    print(f"📌 Python版本: {sys.version}")
    if sys.version_info < (3, 8):
        print("⚠️  警告: 推荐使用Python 3.8或更高版本")
    
    # 安装基础依赖
    print("\n" + "="*60)
    print("🔧 安装基础依赖")
    print("="*60)
    
    packages = [
        ("Pillow", "PIL"),
        ("numpy", "numpy"),
        ("psd-tools", "psd_tools"),
        ("requests", "requests"),
        ("tqdm", "tqdm"),
    ]
    
    for name, import_name in packages:
        if check_installed(import_name):
            print(f"✅ {name} 已安装")
        else:
            print(f"⏳ 安装 {name}...")
            run_command([sys.executable, "-m", "pip", "install", name.lower()], f"安装 {name}")
    
    # 安装rembg
    print("\n" + "="*60)
    print("🤖 安装 rembg (背景移除)")
    print("="*60)
    
    if check_installed("rembg"):
        print("✅ rembg 已安装")
    else:
        print("\n⏳ 安装 rembg...")
        run_command([sys.executable, "-m", "pip", "install", "rembg"], "安装 rembg")
    
    # 安装SAM
    print("\n" + "="*60)
    print("🎯 安装 SAM (Segment Anything)")
    print("="*60)
    
    if check_installed("segment_anything"):
        print("✅ SAM 已安装")
    else:
        print("\n⏳ 安装 SAM...")
        run_command([sys.executable, "-m", "pip", "install", "segment-anything"], "安装 SAM")
        
        # SAM模型下载提示
        model_dir = Path.home() / ".sam"
        model_dir.mkdir(exist_ok=True)
        
        if (model_dir / "sam_vit_h_4b8939.pth").exists():
            print("✅ SAM模型已存在")
        else:
            print("\n📥 请手动下载SAM模型:")
            print("   mkdir -p ~/.sam")
            print("   wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -O ~/.sam/")
    
    # 安装Qwen-Image-Layered
    print("\n" + "="*60)
    print("🌟 安装 Qwen-Image-Layered (阿里最新分层模型)")
    print("="*60)
    
    if check_installed("qwen_image_layered"):
        print("✅ Qwen-Image-Layered 已安装")
    else:
        print("\n⏳ 安装 Qwen-Image-Layered...")
        print("   这是目前最先进的图像分层模型")
        if run_command(
            [sys.executable, "-m", "pip", "install", "qwen-image-layered"],
            "安装 Qwen-Image-Layered"
        ):
            print("\n✅ Qwen-Image-Layered 安装成功!")
            print("\n   📝 使用方法:")
            print("   from qwen_image_layered import QwenImageLayered")
            print("   model = QwenImageLayered.from_pretrained('Qwen/Qwen-VL-Layered-7B')")
            print("   layers = model.decompose('image.png', num_layers=6)")
    
    # 安装PyTorch（可选）
    print("\n" + "="*60)
    print("🔥 检查 PyTorch")
    print("="*60)
    
    if check_installed("torch"):
        print("✅ PyTorch 已安装")
    else:
        print("\n⏳ 安装 PyTorch...")
        print("   (GPU加速需要)")
        print("\n   安装命令:")
        print("   - CPU: pip3 install torch torchvision")
        print("   - GPU: pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu118")
    
    # 总结
    print("\n" + "="*60)
    print("📋 安装总结")
    print("="*60)
    
    installed = []
    not_installed = []
    
    for name, import_name in packages:
        if check_installed(import_name):
            installed.append(name)
        else:
            not_installed.append(name)
    
    for model in ['rembg', 'segment_anything', 'qwen_image_layered']:
        if check_installed(model):
            installed.append(model)
        else:
            not_installed.append(model)
    
    print("\n✅ 已安装:")
    for name in installed:
        print(f"   - {name}")
    
    if not_installed:
        print("\n⚠️  未安装:")
        for name in not_installed:
            print(f"   - {name}")
    
    # 下一步
    print("\n" + "="*60)
    print("🚀 下一步")
    print("="*60)
    
    print("""
1. 测试分层工具:
   python3 live2d_layer_tool.py <图片路径>

2. 查看示例:
   python3 live2d_layer_tool.py output/你的图片.png

3. 下载Qwen-Image-Layered模型（首次使用时自动下载）
   - 模型大小: ~1.8GB
   - 推荐GPU: RTX 3060+

4. 开始使用:
   - 基础分层: python3 live2d_layer_tool.py <图片>
   - 高级分层: python3 live2d_autolayer.py <图片>
   - PSD转换: python3 live2d_psd_converter.py <图片>
   - 一站式工具: python3 master_tool.py

5. 如果遇到问题:
   - 查看 AI_LAYERING_GUIDE.md
   - 检查网络连接
   - 确保有足够的磁盘空间
    """)
    
    print("✅ 安装完成!")

if __name__ == "__main__":
    main()
