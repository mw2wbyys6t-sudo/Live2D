#!/usr/bin/env python3
"""
Live2D PSD转换器 - 综合版
检测可用工具并提供最佳转换方案
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Optional, List

def check_available_tools() -> dict:
    """检测可用的转换工具"""
    tools = {
        'gimp': False,
        'imagemagick': False,
        'photoshop': False,
        'photopea': False,
        'convertio': False
    }
    
    if shutil.which('gimp'):
        tools['gimp'] = True
    
    if shutil.which('convert'):  # ImageMagick
        tools['imagemagick'] = True
    
    if sys.platform == 'win32':
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Adobe\\Photoshop")
            tools['photoshop'] = True
        except:
            pass
    
    return tools

def create_psd_with_gimp(input_path: Path, output_path: Path) -> bool:
    """使用GIMP创建PSD"""
    try:
        script = f"""
(let* ((image (car (gimp-file-load RUN-NONINTERACTIVE "{input_path}" "{input_path}")))
       (drawable (car (gimp-image-get-active-layer image))))
  (file-psd-save RUN-NONINTERACTIVE image drawable "{output_path}" "{output_path}")
  (gimp-quit TRUE))
"""
        script_path = output_path.parent / "temp_gimp_script.scm"
        with open(script_path, 'w') as f:
            f.write(script)
        
        result = subprocess.run(['gimp', '-ib', script_path, '-batch', '(gimp-quit 0)'], 
                              capture_output=True, timeout=30)
        
        script_path.unlink()
        return output_path.exists()
    except:
        return False

def create_psd_with_imagemagick(input_path: Path, output_path: Path) -> bool:
    """使用ImageMagick创建PSD"""
    try:
        result = subprocess.run(['convert', str(input_path), str(output_path)],
                              capture_output=True, timeout=30)
        return output_path.exists()
    except:
        return False

def create_manual_guide(input_path: Path):
    """创建手动转换指南"""
    try:
        from PIL import Image
        img = Image.open(input_path)
        width, height = img.size
        
        guide_path = input_path.parent / f"{input_path.stem}_PSD_MANUAL_GUIDE.txt"
        
        guide = f"""
{'=' * 70}
Live2D PSD 手动转换指南
{'=' * 70}

图片信息:
- 文件: {input_path.name}
- 尺寸: {width} x {height} 像素

{'=' * 70}
方法1: Photoshop (推荐)
{'=' * 70}

1. 用Photoshop打开图片
2. 菜单: File → Save As
3. 格式选择: Photoshop (*.PSD)
4. 保存即可

Live2D导入:
1. 打开Live2D Cubism Editor
2. File → Import PSD
3. 选择保存的PSD文件
4. 开始制作!

{'=' * 70}
方法2: 在线转换 (无需安装软件)
{'=' * 70}

1. 访问: https://convertio.co/png-to-psd/
2. 点击"选择文件"上传图片
3. 点击"转换"
4. 下载PSD文件

其他在线工具:
- https://image.online-convert.com/convert-to-psd
- https://www.zamzar.com/convert/png-to-psd/

{'=' * 70}
方法3: GIMP (免费)
{'=' * 70}

1. 下载GIMP: https://www.gimp.org/
2. 打开图片
3. 菜单: File → Export As
4. 选择格式: Photoshop PSD
5. 保存

{'=' * 70}
方法4: 命令行 (ImageMagick)
{'=' * 70}

如果已安装ImageMagick:
```bash
convert {input_path.name} output.psd
```

{'=' * 70}
Live2D 分层建议
{'=' * 70}

导入PSD后，建议创建以下图层(从下到上):

1. Body - 身体
2. Hair_Back - 头发后部
3. Clothes - 服装
4. Hair_Side - 头发侧部
5. Face - 脸部
6. Eyes - 眼睛(分开左右)
7. Mouth - 嘴巴
8. Hair_Front - 刘海
9. Hands - 手(分开左右)
10. Accessories - 配饰

{'=' * 70}
常见问题
{'=' * 70}

Q: PSD文件导入Live2D后图层在哪里?
A: Live2D会自动识别PSD中的图层作为ArtMesh

Q: 只有一层怎么办?
A: 在Photoshop中手动分层后再导入

Q: 分辨率太大?
A: 建议缩小到1024x1024或更小

{'=' * 70}
"""
        
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        print(f"✅ 手动转换指南: {guide_path.name}")
        return guide_path
        
    except Exception as e:
        print(f"⚠️  创建指南失败: {e}")
        return None

def create_simple_png_for_live2d(input_path: Path):
    """创建优化后的PNG供Live2D使用"""
    try:
        from PIL import Image
        
        img = Image.open(input_path)
        
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        optimized_path = input_path.parent / f"{input_path.stem}_for_live2d.png"
        img.save(optimized_path, 'PNG', optimize=True)
        
        print(f"✅ Live2D用PNG: {optimized_path.name}")
        print(f"   💡 可直接导入Live2D进行绑定")
        
        return optimized_path
        
    except Exception as e:
        print(f"⚠️  创建PNG失败: {e}")
        return None

def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("🎨 Live2D PSD 转换器 - 综合版")
    print("=" * 70)
    
    tools = check_available_tools()
    
    print("\n📋 检测到的工具:")
    if tools['gimp']:
        print("  ✅ GIMP - 免费图像编辑软件")
    if tools['imagemagick']:
        print("  ✅ ImageMagick - 命令行图像处理")
    if tools['photoshop']:
        print("  ✅ Photoshop - 专业图像编辑")
    if not any(tools.values()):
        print("  ⚠️  未检测到PSD转换工具")
    
    if len(sys.argv) < 2:
        print("\n📖 使用方法:")
        print("  python live2d_psd_converter.py <图片路径>")
        print("\n💡 自动检测可用工具并转换")
        
        base_dir = Path(__file__).parent
        output_dir = base_dir / "output"
        if output_dir.exists():
            png_files = list(output_dir.glob("*.png"))
            if png_files:
                latest = max(png_files, key=lambda p: p.stat().st_mtime)
                print(f"\n📷 检测到最新图片: {latest.name}")
                print(f"   运行: python live2d_psd_converter.py {latest}")
        return
    
    input_path = Path(sys.argv[1])
    
    if not input_path.exists():
        print(f"\n❌ 文件不存在: {input_path}")
        return
    
    print(f"\n📷 输入: {input_path.name}")
    
    output_path = input_path.parent / f"{input_path.stem}.psd"
    
    print("\n🔄 尝试转换...")
    
    success = False
    
    if tools['gimp']:
        print("\n1️⃣ 尝试使用GIMP...")
        if create_psd_with_gimp(input_path, output_path):
            print(f"✅ PSD创建成功: {output_path.name}")
            success = True
    
    if not success and tools['imagemagick']:
        print("\n2️⃣ 尝试使用ImageMagick...")
        if create_psd_with_imagemagick(input_path, output_path):
            print(f"✅ PSD创建成功: {output_path.name}")
            success = True
    
    if not success:
        print("\n⚠️  自动转换不可用")
        print("\n💡 解决方案:")
        print("  1. 使用Photoshop手动保存为PSD")
        print("  2. 使用在线转换: https://convertio.co/png-to-psd/")
        print("  3. 安装GIMP: https://www.gimp.org/")
    
    create_simple_png_for_live2d(input_path)
    create_manual_guide(input_path)
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 完成!")
    else:
        print("⚠️  部分完成，请查看手动转换指南")
    print("=" * 70)

if __name__ == "__main__":
    main()
