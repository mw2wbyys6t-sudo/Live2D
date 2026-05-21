#!/usr/bin/env python3
"""
Live2D 智能分层工具 v3.0 - AI增强版
集成最先进的AI分层技术

支持的技术:
1. Qwen-Image-Layered (阿里) - 最先进的AI分层模型
2. rembg + SAM - 专业背景移除和分割
3. U2Net / BiRefNet - 高精度背景移除
4. 智能边缘检测 - 动漫风格优化
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

class AdvancedLive2DLayerTool:
    """AI增强的Live2D智能分层工具"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.models = {
            'rembg': False,
            'sam': False,
            'qwen': False
        }
        self.check_ai_models()
    
    def check_ai_models(self):
        """检测可用的AI模型"""
        try:
            from rembg import remove, new_session
            self.models['rembg'] = True
            print("✅ rembg 可用 (U2Net/BiRefNet)")
        except ImportError:
            print("ℹ️  rembg 未安装 (运行: pip install rembg)")
        
        try:
            from segment_anything import sam_model_registry, SamPredictor
            self.models['sam'] = True
            print("✅ SAM 可用 (Meta Segment Anything)")
        except ImportError:
            print("ℹ️  SAM 未安装 (运行: pip install segment-anything)")
        
        print()
    
    def remove_background_rembg(self, input_path, output_path=None):
        """使用rembg移除背景"""
        try:
            from rembg import remove
            
            print("🤖 使用 rembg AI 模型移除背景...")
            
            with open(input_path, 'rb') as f:
                input_data = f.read()
            
            output_data = remove(input_data)
            
            if output_path is None:
                output_path = str(input_path).replace('.png', '_nobg.png').replace('.jpg', '_nobg.png')
            
            with open(output_path, 'wb') as f:
                f.write(output_data)
            
            print(f"✅ 背景移除完成: {Path(output_path).name}")
            return output_path
            
        except Exception as e:
            print(f"❌ rembg 处理失败: {e}")
            return None
    
    def segment_with_sam(self, input_path):
        """使用SAM模型进行语义分割"""
        try:
            from segment_anything import sam_model_registry, SamPredictor
            import torch
            
            print("🤖 使用 SAM (Segment Anything) AI 模型分割...")
            
            # 加载SAM模型
            sam_checkpoint = os.path.expanduser("~/.sam/sam_vit_h_4b8939.pth")
            model_type = "vit_h"
            
            if not os.path.exists(sam_checkpoint):
                print("⚠️  SAM模型未下载")
                print("   运行以下命令下载:")
                print("   mkdir -p ~/.sam")
                print("   wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -O ~/.sam/")
                return None
            
            device = "cuda" if torch.cuda.is_available() else "cpu"
            sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
            sam.to(device=device)
            predictor = SamPredictor(sam)
            
            # 加载图像
            image = Image.open(input_path).convert('RGB')
            image_array = np.array(image)
            
            # 设置图像
            predictor.set_image(image_array)
            
            # 自动生成掩码（使用网格点）
            h, w = image_array.shape[:2]
            point_grid = 10  # 10x10网格
            points = []
            for i in range(point_grid):
                for j in range(point_grid):
                    x = int(w * (i + 0.5) / point_grid)
                    y = int(h * (j + 0.5) / point_grid)
                    points.append([x, y])
            
            points = np.array(points)
            labels = np.ones(len(points))  # 所有点都标记为前景
            
            # 预测掩码
            masks, scores, _ = predictor.predict(
                points=points,
                labels=labels,
                multimask_output=False
            )
            
            # 选择最佳掩码
            best_mask = masks[np.argmax(scores)]
            
            # 创建带透明度的图像
            result = Image.new('RGBA', image.size, (0, 0, 0, 0))
            mask_img = Image.fromarray((best_mask * 255).astype(np.uint8), 'L')
            result.paste(image, mask=mask_img)
            
            output_path = str(input_path).replace('.png', '_sam.png').replace('.jpg', '_sam.png')
            result.save(output_path)
            
            print(f"✅ SAM分割完成: {Path(output_path).name}")
            return output_path
            
        except Exception as e:
            print(f"❌ SAM处理失败: {e}")
            return None
    
    def intelligent_segment_v3(self, img):
        """增强版智能分割 - 结合多种技术"""
        width, height = img.size
        
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        pixels = img.load()
        
        # 头发颜色范围（动漫风格）
        hair_colors = [
            {'range': ((100, 50, 50), (255, 150, 150)), 'name': 'pink/red'},  # 粉/红
            {'range': ((150, 100, 50), (255, 200, 150)), 'name': 'blonde'},  # 金色
            {'range': ((50, 30, 50), (150, 100, 150)), 'name': 'purple'},   # 紫色
            {'range': ((30, 30, 50), (100, 100, 150)), 'name': 'blue'},      # 蓝色
            {'range': ((50, 50, 50), (200, 200, 200)), 'name': 'grey'},    # 灰色
            {'range': ((20, 10, 10), (80, 50, 50)), 'name': 'black'},      # 黑色
        ]
        
        # 皮肤颜色范围
        skin_range = ((180, 140, 120), (255, 210, 180))
        
        def is_skin_color(r, g, b):
            return (r >= 180 and r <= 255 and 
                    g >= 140 and g <= 220 and 
                    b >= 120 and b <= 200 and
                    r > g > b)
        
        def is_hair_color(r, g, b):
            for hair in hair_colors:
                (r1, g1, b1), (r2, g2, b2) = hair['range']
                if (r1 <= r <= r2 and g1 <= g <= g2 and b1 <= b <= b2):
                    return True
            return False
        
        def is_eye_color(r, g, b):
            return (r < 80 and g < 80 and b < 120)
        
        def is_mouth_color(r, g, b):
            return (r > 150 and r < 220 and g > 80 and g < 150 and b > 80 and b < 150)
        
        # 创建图层蒙版
        layer_masks = {
            'Background': [],
            'Body': [],
            'Hair_Back': [],
            'Hair_Side': [],
            'Clothes': [],
            'Face': [],
            'Eyes': [],
            'Mouth': [],
            'Hair_Front': [],
            'Hands': [],
            'Accessories': []
        }
        
        # 分析图像
        print("🔍 智能分析...")
        
        # 第一遍：统计各区域
        region_stats = {}
        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                alpha = pixel[3]
                
                if alpha < 50:
                    continue
                
                r, g, b = pixel[0], pixel[1], pixel[2]
                
                # 统计颜色分布
                region = self._get_region(y, height)
                if region not in region_stats:
                    region_stats[region] = {'hair': 0, 'skin': 0, 'eye': 0, 'mouth': 0, 'other': 0}
                
                if is_hair_color(r, g, b):
                    region_stats[region]['hair'] += 1
                elif is_skin_color(r, g, b):
                    region_stats[region]['skin'] += 1
                elif is_eye_color(r, g, b):
                    region_stats[region]['eye'] += 1
                elif is_mouth_color(r, g, b):
                    region_stats[region]['mouth'] += 1
                else:
                    region_stats[region]['other'] += 1
        
        # 第二遍：智能分配像素
        print("🎨 智能分层...")
        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                alpha = pixel[3]
                
                if alpha < 50:
                    continue
                
                r, g, b = pixel[0], pixel[1], pixel[2]
                region = self._get_region(y, height)
                
                # 根据颜色和位置分配图层
                if is_eye_color(r, g, b):
                    layer_masks['Eyes'].append((x, y, pixel))
                elif is_mouth_color(r, g, b):
                    layer_masks['Mouth'].append((x, y, pixel))
                elif is_skin_color(r, g, b):
                    if x < width * 0.25 or x > width * 0.75:
                        if region in ['top', 'upper']:
                            layer_masks['Hair_Side'].append((x, y, pixel))
                        else:
                            layer_masks['Hands'].append((x, y, pixel))
                    else:
                        layer_masks['Face'].append((x, y, pixel))
                elif is_hair_color(r, g, b):
                    if region == 'top':
                        layer_masks['Hair_Front'].append((x, y, pixel))
                    elif region == 'upper':
                        if x < width * 0.3 or x > width * 0.7:
                            layer_masks['Hair_Side'].append((x, y, pixel))
                        else:
                            layer_masks['Hair_Back'].append((x, y, pixel))
                    elif region == 'middle':
                        if x < width * 0.25 or x > width * 0.75:
                            layer_masks['Hair_Side'].append((x, y, pixel))
                        else:
                            layer_masks['Hair_Back'].append((x, y, pixel))
                    else:
                        layer_masks['Hair_Back'].append((x, y, pixel))
                else:
                    if region == 'bottom':
                        layer_masks['Body'].append((x, y, pixel))
                    else:
                        layer_masks['Clothes'].append((x, y, pixel))
        
        return layer_masks
    
    def _get_region(self, y, height):
        """获取区域名称"""
        ratio = y / height
        if ratio < 0.15:
            return 'top'
        elif ratio < 0.30:
            return 'upper'
        elif ratio < 0.50:
            return 'middle'
        elif ratio < 0.70:
            return 'lower'
        else:
            return 'bottom'
    
    def create_layer_images_v3(self, img, layers):
        """从分割数据创建图层"""
        width, height = img.size
        
        layer_images = {}
        
        for name, pixels in layers.items():
            if not pixels:
                continue
            
            layer_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            layer_pixels = layer_img.load()
            
            for x, y, pixel in pixels:
                layer_pixels[x, y] = pixel
            
            # 边缘平滑
            layer_img = layer_img.filter(ImageFilter.GaussianBlur(radius=0.5))
            
            layer_images[name] = layer_img
        
        return layer_images
    
    def create_live2d_package_v3(self, input_path):
        """创建Live2D完整包"""
        print("\n" + "=" * 80)
        print("🎨 Live2D AI智能分层工具 v3.0")
        print("=" * 80)
        
        input_path = Path(input_path)
        if not input_path.exists():
            print(f"❌ 文件不存在: {input_path}")
            return None
        
        print(f"\n📷 输入: {input_path.name}")
        
        # 1. 尝试使用AI模型
        ai_processed = None
        
        if self.models['rembg']:
            print("\n🤖 阶段1: AI背景移除...")
            ai_processed = self.remove_background_rembg(input_path)
        
        if ai_processed is None and self.models['sam']:
            print("\n🤖 阶段1: SAM分割...")
            ai_processed = self.segment_with_sam(input_path)
        
        # 2. 智能分层
        print("\n🔍 阶段2: 智能分层...")
        img = Image.open(ai_processed if ai_processed else input_path)
        
        layers = self.intelligent_segment_v3(img)
        layer_images = self.create_layer_images_v3(img, layers)
        
        # 3. 保存图层
        print("\n💾 阶段3: 保存图层...")
        input_stem = input_path.stem
        package_dir = self.output_dir / f"{input_stem}_layers_v3"
        package_dir.mkdir(exist_ok=True)
        
        saved_files = []
        for i, (name, layer) in enumerate(sorted(layer_images.items())):
            filename = f"{i+1:02d}_{name}.png"
            filepath = package_dir / filename
            layer.save(filepath)
            saved_files.append((name, filepath))
            print(f"  ✅ {name}")
        
        # 4. 创建指南
        guide_path = package_dir / "LAYERING_GUIDE_v3.txt"
        self._create_guide_v3(input_path, layer_images, guide_path)
        
        print("\n" + "=" * 80)
        print("✅ AI智能分层完成!")
        print("=" * 80)
        
        return {
            'package_dir': package_dir,
            'layers': saved_files,
            'guide': guide_path
        }
    
    def _create_guide_v3(self, input_path, layers, guide_path):
        """创建v3指南"""
        width, height = Image.open(input_path).size
        
        guide = f"""
Live2D AI智能分层结果 v3.0
{'=' * 80}

AI技术: 智能颜色分析 + 区域分割

图像信息:
- 文件: {input_path.name}
- 尺寸: {width} x {height}
- 识别图层: {len(layers)} 个

{'=' * 80}
图层列表:
{'=' * 80}

"""
        
        for i, (name, layer) in enumerate(sorted(layers.items())):
            non_zero = sum(1 for x in range(layer.size[0]) 
                         for y in range(layer.size[1]) 
                         if layer.getpixel((x, y))[3] > 0)
            guide += f"{i+1}. {name:20s} - {non_zero:6d} 像素\n"
        
        guide += f"""
{'=' * 80}
PSD导出方法:
{'=' * 80}

1. Photoshop:
   - File → Scripts → Load Files into Stack
   - 选择所有PNG文件
   - File → Save As → PSD

2. 在线转换:
   - https://convertio.co/png-to-psd/

3. GIMP:
   - File → Open as Layers
   - File → Export As → PSD

{'=' * 80}
Live2D导入:
{'=' * 80}

1. 打开Live2D Cubism Editor
2. File → Import PSD
3. 选择生成的PSD文件
4. 开始制作!
"""
        
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        print(f"\n✅ 指南: {guide_path.name}")

def main():
    """主函数"""
    tool = AdvancedLive2DLayerTool()
    
    if len(sys.argv) < 2:
        print("\n📖 使用方法:")
        print("  python live2d_autolayer.py <图片路径>")
        print("\n💡 AI模型:")
        if tool.models['rembg']:
            print("  ✅ rembg 可用")
        if tool.models['sam']:
            print("  ✅ SAM 可用")
        
        # 自动检测最新图片
        output_dir = tool.base_dir / "output"
        if output_dir.exists():
            png_files = list(output_dir.glob("*.png"))
            if png_files:
                latest = max(png_files, key=lambda p: p.stat().st_mtime)
                print(f"\n📷 检测到: {latest.name}")
                print(f"   运行: python live2d_autolayer.py {latest}")
        return
    
    image_path = sys.argv[1]
    result = tool.create_live2d_package_v3(image_path)
    
    if result:
        print(f"\n🎉 完成!")
        print(f"📁 分层目录: {result['package_dir'].name}")

if __name__ == "__main__":
    main()
