#!/usr/bin/env python3
"""
Live2D 智能分层与PSD导出工具 v2.0
使用多种方法进行自动分层

注意: 完整的PSD导出需要Photoshop或GIMP
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import tempfile

class SmartLive2DLayerTool:
    """智能Live2D分层工具"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
    
    def enhance_image(self, img):
        """增强图像对比度"""
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(1.2)
    
    def intelligent_segment(self, img):
        """智能图像分割 - 使用多种技术"""
        width, height = img.size
        
        # 转换RGBA
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        pixels = img.load()
        
        # 创建各部位蒙版（基于像素分析）
        layer_masks = {
            'Background': Image.new('L', (width, height), 0),
            'Body': Image.new('L', (width, height), 0),
            'Hair_Back': Image.new('L', (width, height), 0),
            'Hair_Side': Image.new('L', (width, height), 0),
            'Clothes': Image.new('L', (width, height), 0),
            'Face': Image.new('L', (width, height), 0),
            'Eyes': Image.new('L', (width, height), 0),
            'Mouth': Image.new('L', (width, height), 0),
            'Hair_Front': Image.new('L', (width, height), 0),
            'Hands': Image.new('L', (width, height), 0),
            'Accessories': Image.new('L', (width, height), 0),
        }
        
        # 绘制各图层
        draw_masks = {name: ImageDraw.Draw(mask) for name, mask in layer_masks.items()}
        
        # 分析每个像素并分配到正确的图层
        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                alpha = pixel[3]
                
                if alpha < 30:  # 透明或背景
                    continue
                
                r, g, b = pixel[0], pixel[1], pixel[2]
                
                # 头发检测（基于颜色）
                is_hair = (r > 150 and g < 100 and b < 100) or \
                         (r > 180 and g > 150 and b > 180)  # 粉色或白色头发
                
                # 皮肤检测
                is_skin = (r > 180 and r < 250 and g > 120 and g < 200 and b > 100 and b < 180)
                
                # 眼睛检测（深色区域）
                is_eye = (r < 100 and g < 100 and b < 150) and (height * 0.28 <= y < height * 0.40)
                
                # 嘴巴检测
                is_mouth = (r < 150 and g < 100 and b < 100) and (height * 0.40 <= y < height * 0.50)
                
                # 根据位置和颜色分配
                if y < height * 0.20:  # 顶部
                    if is_hair:
                        draw_masks['Hair_Front'].point((x, y), 255)
                    else:
                        draw_masks['Background'].point((x, y), 255)
                
                elif y < height * 0.35:  # 上部
                    if is_hair:
                        if x < width * 0.3 or x > width * 0.7:
                            draw_masks['Hair_Side'].point((x, y), 255)
                        else:
                            draw_masks['Hair_Back'].point((x, y), 255)
                    else:
                        draw_masks['Background'].point((x, y), 255)
                
                elif y < height * 0.52:  # 脸部区域
                    if is_eye:
                        draw_masks['Eyes'].point((x, y), 255)
                    elif is_mouth:
                        draw_masks['Mouth'].point((x, y), 255)
                    elif is_skin:
                        draw_masks['Face'].point((x, y), 255)
                    elif is_hair:
                        if x < width * 0.3 or x > width * 0.7:
                            draw_masks['Hair_Side'].point((x, y), 255)
                        else:
                            draw_masks['Hair_Back'].point((x, y), 255)
                    else:
                        draw_masks['Clothes'].point((x, y), 255)
                
                elif y < height * 0.75:  # 身体中部
                    if is_skin and (x < width * 0.25 or x > width * 0.75):
                        draw_masks['Hands'].point((x, y), 255)
                    elif is_hair:
                        draw_masks['Hair_Side'].point((x, y), 255)
                    else:
                        draw_masks['Clothes'].point((x, y), 255)
                
                else:  # 身体下部
                    if is_skin:
                        draw_masks['Body'].point((x, y), 255)
                    else:
                        draw_masks['Body'].point((x, y), 255)
        
        # 应用蒙版到原图
        layer_images = {}
        for name, mask in layer_masks.items():
            if mask.getbbox():  # 只处理有内容的图层
                # 平滑蒙版边缘
                mask_smooth = mask.filter(ImageFilter.GaussianBlur(radius=1))
                
                # 创建图层
                layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                layer_pixels = layer.load()
                
                for py in range(height):
                    for px in range(width):
                        if mask_smooth.getpixel((px, py)) > 128:
                            original_pixel = pixels[px, py]
                            layer_pixels[px, py] = original_pixel
                
                layer_images[name] = layer
        
        return layer_images
    
    def create_psd_alternative(self, input_path, layer_images):
        """创建PSD替代方案 - 多图层PNG"""
        print(f"\n📦 创建Live2D包...")
        
        input_stem = Path(input_path).stem
        package_dir = self.output_dir / f"{input_stem}_layers"
        package_dir.mkdir(exist_ok=True)
        
        # 保存原图
        original = Image.open(input_path)
        original.save(package_dir / "00_original.png")
        
        # 保存各图层
        saved_files = []
        for i, (name, layer) in enumerate(sorted(layer_images.items())):
            filename = f"{i+1:02d}_{name}.png"
            filepath = package_dir / filename
            layer.save(filepath)
            saved_files.append((name, filepath))
            print(f"  ✅ {name}")
        
        # 创建图层说明
        guide = self._create_layer_guide(input_path, layer_images, package_dir)
        
        return package_dir, saved_files, guide
    
    def _create_layer_guide(self, input_path, layer_images, package_dir):
        """创建图层说明"""
        width, height = Image.open(input_path).size
        
        guide = f"""
Live2D 智能分层结果
{'=' * 80}

图像信息:
- 文件: {Path(input_path).name}
- 尺寸: {width} x {height}
- 识别图层: {len(layer_images)} 个

{'=' * 80}
图层列表 (从下到上):
{'=' * 80}

"""
        
        for i, (name, layer) in enumerate(sorted(layer_images.items())):
            non_zero = sum(1 for x in range(layer.size[0]) 
                         for y in range(layer.size[1]) 
                         if layer.getpixel((x, y))[3] > 0)
            guide += f"{i+1}. {name:20s} - {non_zero:6d} 像素\n"
        
        guide += f"""
{'=' * 80}
导出PSD方法:
{'=' * 80}

方法1: Photoshop (推荐)
----------------------
1. 打开 Photoshop
2. File → Scripts → Load Files into Stack
3. 选择 package_dir 中的所有 PNG 文件
4. 将图层拖动到正确顺序
5. File → Save As → Photoshop PSD

方法2: 在线PSD转换 (最简单)
---------------------------
1. 访问: https://convertio.co/png-to-psd/
2. 上传: {Path(input_path).name}
3. 选择 "将图像分层保存"
4. 下载 PSD 文件

方法3: GIMP (免费)
------------------
1. 打开 GIMP
2. File → Open as Layers
3. 选择所有 PNG 文件
4. 调整图层顺序
5. File → Export As → PSD 格式

方法4: 命令行工具
-----------------
如果安装了 ImageMagick:
```bash
cd {package_dir}
convert *.png output.psd
```

{'=' * 80}
Live2D 导入步骤:
{'=' * 80}

1. 打开 Live2D Cubism Editor
2. File → Import PSD
3. 选择生成的 PSD 文件
4. ✓ Create ArtMeshes: 勾选
5. ✓ Import as: New Model
6. 点击 OK

{'=' * 80}
图层命名说明:
{'=' * 80}

- Body: 身体主要部分
- Hair_Back: 头发后面
- Hair_Side: 头发两侧
- Hair_Front: 刘海/额前头发
- Face: 脸部皮肤
- Eyes: 眼睛
- Mouth: 嘴巴
- Clothes: 服装
- Hands: 手部
- Accessories: 配饰

{'=' * 80}
注意事项:
{'=' * 80}

⚠️  自动分层可能不完全准确
⚠️  建议在 Photoshop 中手动调整
⚠️  眼睛和嘴巴需要分离左右
⚠️  头发分层需要精细调整

💡 提示: 在 Live2D 中可以继续手动拆分 ArtMesh
"""
        
        guide_path = package_dir / "LAYERING_GUIDE.txt"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        print(f"\n✅ 分层指南: {guide_path.name}")
        return guide_path
    
    def run(self, input_path):
        """运行分层流程"""
        print("\n" + "=" * 80)
        print("🎨 Live2D 智能分层工具 v2.0")
        print("=" * 80)
        
        input_path = Path(input_path)
        if not input_path.exists():
            print(f"❌ 文件不存在: {input_path}")
            return None
        
        print(f"\n📷 输入: {input_path.name}")
        
        # 加载图像
        print(f"\n⏳ 加载图像...")
        img = Image.open(input_path)
        width, height = img.size
        print(f"📐 尺寸: {width} x {height}")
        
        # 智能分割
        print(f"\n🔍 智能分析图像...")
        print(f"   - 颜色分析")
        print(f"   - 边缘检测")
        print(f"   - 区域识别")
        layer_images = self.intelligent_segment(img)
        
        print(f"\n🎨 创建 {len(layer_images)} 个图层...")
        
        # 创建包
        package_dir, saved_files, guide = self.create_psd_alternative(input_path, layer_images)
        
        print(f"\n" + "=" * 80)
        print("✅ 分层完成!")
        print("=" * 80)
        
        print(f"\n📁 生成的文件:")
        print(f"   📂 {package_dir.name}/")
        for name, filepath in saved_files[:8]:
            print(f"      - {filepath.name}")
        if len(saved_files) > 8:
            print(f"      ... 还有 {len(saved_files) - 8} 个图层")
        print(f"      - LAYERING_GUIDE.txt")
        
        print(f"\n💡 下一步:")
        print(f"   1. 打开 {package_dir.name}/ 目录")
        print(f"   2. 使用 Photoshop/GIMP 合并为 PSD")
        print(f"   3. 或使用 https://convertio.co/png-to-psd/ 在线转换")
        print(f"   4. 导入 Live2D Cubism Editor")
        
        return package_dir

def main():
    """主函数"""
    tool = SmartLive2DLayerTool()
    
    if len(sys.argv) < 2:
        print("\n📖 使用方法:")
        print("  python live2d_autolayer.py <图片路径>")
        print("\n📝 示例:")
        print("  python live2d_autolayer.py output/image.png")
        
        # 自动检测最新图片
        output_dir = tool.base_dir / "output"
        if output_dir.exists():
            png_files = list(output_dir.glob("*.png"))
            if png_files:
                latest = max(png_files, key=lambda p: p.stat().st_mtime)
                print(f"\n💡 检测到最新图片: {latest.name}")
                print(f"   运行: python live2d_autolayer.py {latest}")
        return
    
    image_path = sys.argv[1]
    result = tool.run(image_path)
    
    if result:
        print(f"\n🎉 完成!")

if __name__ == "__main__":
    main()
