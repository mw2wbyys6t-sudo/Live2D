#!/usr/bin/env python3
"""
Live2D AI分层工具 - 依赖安装脚本
自动安装所有AI模型和依赖
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        print(f"✅ {description} 成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败!")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False

def check_installed(package):
    """检查包是否已安装"""
    try:
        result = subprocess.run(
            f"python3 -c 'import {package}'",
            shell=True,
            capture_output=True
        )
        return result.returncode == 0
    except:
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🎨 Live2D AI分层工具 - 依赖安装                      ║
║                                                          ║
║     自动安装最先进的AI分层模型                           ║
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
    ]
    
    for name, import_name in packages:
        if check_installed(import_name):
            print(f"✅ {name} 已安装")
        else:
            print(f"⏳ 安装 {name}...")
            run_command(f"pip3 install {name.lower()}", f"安装 {name}")
    
    # 安装rembg
    print("\n" + "="*60)
    print("🤖 安装AI模型")
    print("="*60)
    
    if check_installed("rembg"):
        print("✅ rembg 已安装 (U2Net/BiRefNet背景移除)")
    else:
        print("\n⏳ 安装 rembg...")
        print("   这将安装10+种AI背景移除模型")
        if run_command(
            "pip3 install 'rembg[gpu]'",
            "安装 rembg (GPU优化版)"
        ):
            print("\n✅ rembg 安装成功!")
            print("\n   可用模型:")
            print("   - u2net: 通用背景移除 (默认)")
            print("   - u2netp: 轻量版")
            print("   - u2net_human_seg: 人物分割")
            print("   - isnet-general-use: 高精度")
    
    # 安装SAM (Segment Anything)
    print("\n" + "="*60)
    print("🎯 安装 SAM (Segment Anything)")
    print("="*60)
    
    if check_installed("segment_anything"):
        print("✅ SAM 已安装")
    else:
        print("\n⏳ 安装 SAM...")
        if run_command(
            "pip3 install segment-anything",
            "安装 SAM"
        ):
            print("\n✅ SAM 安装成功!")
            print("\n   模型下载:")
            print("   - sam_vit_h_4b8939.pth (2.4GB, 高质量)")
            print("   - sam_vit_l_0b3195.pth (1.2GB, 中等)")
            print("   - sam_vit_b_01ec64.pth (375MB, 快速)")
            
            # 自动下载模型
            print("\n⏳ 尝试下载SAM模型...")
            model_dir = Path.home() / ".sam"
            model_dir.mkdir(exist_ok=True)
            
            sam_path = model_dir / "sam_vit_h_4b8939.pth"
            if sam_path.exists():
                print(f"✅ SAM模型已存在: {sam_path}")
            else:
                print(f"\n📥 请手动下载SAM模型:")
                print(f"   mkdir -p ~/.sam")
                print(f"   wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -O ~/.sam/")
    
    # 安装torch (如果需要)
    print("\n" + "="*60)
    print("🔥 检查 PyTorch")
    print("="*60)
    
    if check_installed("torch"):
        print("✅ PyTorch 已安装")
    else:
        print("\n⏳ 安装 PyTorch...")
        print("   (如果需要GPU加速)")
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
    
    if check_installed("rembg"):
        installed.append("rembg")
    else:
        not_installed.append("rembg")
    
    if check_installed("segment_anything"):
        installed.append("SAM")
    else:
        not_installed.append("SAM")
    
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
   python3 live2d_autolayer.py <图片路径>

2. 查看示例:
   python3 live2d_autolayer.py output/你的图片.png

3. 如果使用AI模型，需要下载模型:
   # SAM模型
   mkdir -p ~/.sam
   wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -O ~/.sam/

4. 开始使用:
   - 自动分层: python3 live2d_autolayer.py <图片>
   - PSD转换: python3 live2d_psd_converter.py <图片>
   - 一站式工具: python3 master_tool.py
    """)
    
    print("✅ 安装完成!")

if __name__ == "__main__":
    main()
