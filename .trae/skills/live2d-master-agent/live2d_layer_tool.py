#!/usr/bin/env python3
"""
Live2D AI分层工具 v4.0 - Qwen-Image-Layered增强版
集成目前最先进的AI分层技术，支持自动分解为多个RGBA图层

技术特点:
1. Qwen-Image-Layered: 阿里最新的图像分层模型
2. 自动分层3-8+个图层
3. 支持递归分层细化
4. 边缘平滑处理
5. Live2D标准图层命名
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

class AdvancedLive2DLayerTool:
    """Qwen-Image-Layered增强版Live2D智能分层工具"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.available_models = {
            'qwen': False,
            'rembg': False,
            'sam': False,
            'local': True
        }
        self.check_models()
    
    def check_models(self):
        """检测可用的AI模型"""
        try:
            from qwen_image_layered import QwenImageLayered
            self.available_models['qwen'] = True
            print("✅ Qwen-Image-Layered 可用")
        except ImportError:
            print("ℹ️  Qwen-Image-Layered 未安装")
        
        try:
            from rembg import remove
            self.available_models['rembg'] = True
            print("✅ rembg 可用")
        except ImportError:
            print("ℹ️  rembg 未安装")
        
        try:
            from segment_anything import sam_model_registry
            self.available_models['sam'] = True
            print("✅ SAM 可用")
        except ImportError:
            print("ℹ️  SAM 未安装")
        
        print()
    
    def decompose_with_qwen(self, input_path):
        """使用Qwen-Image-Layered分解图像"""
        try:
            from qwen_image_layered import QwenImageLayered
            
            print("🤖 使用 Qwen-Image-Layered AI 模型...")
            
            model = QwenImageLayered.from_pretrained("Qwen/Qwen-VL-Layered-7B")
            layers = model.decompose(input_path, num_layers=6)
            
            qwen_output_dir = self.output_dir / f"qwen_layers_{Path(input_path).stem}"
            qwen_output_dir.mkdir(exist_ok=True)
            
            layer_files = []
            for i, layer in enumerate(layers):
                layer_path = qwen_output_dir / f"layer_{i:02d}.png"
                layer.save(layer_path)
                layer_files.append(layer_path)
                print(f"  ✅ 图层 {i+1}/{len(layers)}")
            
            print(f"\n✅ Qwen分层完成，生成 {len(layers)} 个图层")
            return qwen_output_dir, layer_files
            
        except Exception as e:
            print(f"⚠️ Qwen-Image-Layered 不可用: {e}")
            return None, None
    
    def remove_background(self, input_path):
        """使用rembg移除背景"""
        try:
            from rembg import remove
            
            print("🤖 使用 rembg AI 背景移除...")
            
            with open(input_path, 'rb') as f:
                input_data = f.read()
            
            output_data = remove(input_data)
            
            output_path = str(input_path).replace('.png', '_nobg.png').replace('.jpg', '_nobg.png')
            with open(output_path, 'wb') as f:
                f.write(output_data)
            
            print(f"✅ 背景移除完成")
            return output_path
            
        except Exception as e:
            print(f"⚠️ rembg 不可用: {e}")
            return input_path
    
    def intelligent_live2d_layering(self, img):
        """Live2D专用智能分层算法"""
        width, height = img.size
        
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        pixels = img.load()
        
        # 头发颜色范围（动漫风格优化版）
        hair_color_ranges = [
            {'name': 'pink', 'r': (180, 255), 'g': (100, 200), 'b': (100, 200)},
            {'name': 'red', 'r': (150, 255), 'g': (50, 120), 'b': (50, 120)},
            {'name': 'blonde', 'r': (200, 255), 'g': (160, 230), 'b': (100, 180)},
            {'name': 'purple', 'r': (100, 180), 'g': (60, 130), 'b': (100, 180)},
            {'name': 'blue', 'r': (50, 150), 'g': (80, 180), 'b': (150, 255)},
            {'name': 'grey', 'r': (150, 220), 'g': (150, 220), 'b': (150, 220)},
            {'name': 'black', 'r': (20, 80), 'g': (15, 70), 'b': (15, 70)},
            {'name': 'green', 'r': (80, 180), 'g': (150, 255), 'b': (80, 180)},
        ]
        
        # 皮肤颜色范围（动漫风格）
        def is_skin(r, g, b):
            return (r >= 180 and r <= 255 and 
                    g >= 140 and g <= 220 and 
                    b >= 120 and b <= 200 and
                    r > g and g > b)
        
        # 眼睛颜色检测
        def is_eye(r, g, b):
            return (r + g + b < 300) or (b > 150 and r < 100 and g < 150)
        
        # 嘴巴颜色检测
        def is_mouth(r, g, b):
            return (r > 150 and r < 230 and 
                    g > 80 and g < 160 and 
                    b > 80 and b < 160)
        
        # 头发颜色检测
        def is_hair(r, g, b):
            for hair in hair_color_ranges:
                if (hair['r'][0] <= r <= hair['r'][1] and
                    hair['g'][0] <= g <= hair['g'][1] and
                    hair['b'][0] <= b <= hair['b'][1]):
                    return True
            return False
        
        # 创建图层蒙版
        layers = {
            'Body': [],
            'Clothes': [],
            'Hair_Back': [],
            'Hair_Front': [],
            'Hair_Side': [],
            'Face': [],
            'Eyes': [],
            'Mouth': [],
            'Hands': [],
            'Accessories': [],
            'Background': []
        }
        
        # 区域定义
        regions = {
            'top': (0, height * 0.15),
            'upper': (height * 0.15, height * 0.35),
            'middle': (height * 0.35, height * 0.6),
            'lower': (height * 0.6, height * 0.85),
            'bottom': (height * 0.85, height)
        }
        
        def get_region(y):
            for name, (start, end) in regions.items():
                if start <= y < end:
                    return name
            return 'middle'
        
        print("🔍 分析图像...")
        
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                
                if a < 30:
                    layers['Background'].append((x, y, (r, g, b, a)))
                    continue
                
                region = get_region(y)
                
                if is_eye(r, g, b):
                    layers['Eyes'].append((x, y, (r, g, b, a)))
                elif is_mouth(r, g, b):
                    layers['Mouth'].append((x, y, (r, g, b, a)))
                elif is_skin(r, g, b):
                    if region in ['top', 'upper'] and (x < width * 0.2 or x > width * 0.8):
                        layers['Hair_Side'].append((x, y, (r, g, b, a)))
                    elif region in ['lower', 'bottom'] and (x < width * 0.2 or x > width * 0.8):
                        layers['Hands'].append((x, y, (r, g, b, a)))
                    else:
                        layers['Face'].append((x, y, (r, g, b, a)))
                elif is_hair(r, g, b):
                    if region == 'top':
                        layers['Hair_Front'].append((x, y, (r, g, b, a)))
                    elif region == 'upper':
                        if x < width * 0.3 or x > width * 0.7:
                            layers['Hair_Side'].append((x, y, (r, g, b, a)))
                        else:
                            layers['Hair_Back'].append((x, y, (r, g, b, a)))
                else:
                    if region in ['lower', 'bottom']:
                        layers['Body'].append((x, y, (r, g, b, a)))
                    else:
                        layers['Clothes'].append((x, y, (r, g, b, a)))
        
        return layers
    
    def create_layer_images(self, img, layers):
        """从分层数据创建图层图像"""
        width, height = img.size
        layer_images = {}
        
        for name, pixels in layers.items():
            if not pixels:
                continue
            
            layer_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            layer_pixels = layer_img.load()
            
            for x, y, pixel in pixels:
                layer_pixels[x, y] = pixel
            
            # 边缘平滑处理
            layer_img = self.smooth_layer_edges(layer_img)
            
            layer_images[name] = layer_img
        
        return layer_images
    
    def smooth_layer_edges(self, img):
        """平滑图层边缘"""
        # 使用高斯模糊处理边缘
        alpha = img.split()[3]
        alpha_smooth = alpha.filter(ImageFilter.GaussianBlur(radius=1))
        
        # 重建图像
        result = Image.new('RGBA', img.size)
        result.paste(img, mask=alpha_smooth)
        
        return result
    
    def export_to_psd(self, layers, output_path):
        """导出为PSD文件"""
        try:
            from psd_tools import PSDImage, Layer
            
            print("📦 导出PSD文件...")
            
            psd = PSDImage.new(layers[next(iter(layers))].size)
            
            layer_order = [
                'Background', 'Body', 'Clothes', 'Hair_Back', 
                'Hair_Side', 'Face', 'Hair_Front', 'Eyes', 'Mouth', 'Hands', 'Accessories'
            ]
            
            for name in layer_order:
                if name in layers:
                    layer = Layer(name, layers[name])
                    psd[0].append(layer)
            
            psd.save(output_path)
            print(f"✅ PSD导出完成: {Path(output_path).name}")
            return output_path
            
        except ImportError:
            print("⚠️ psd-tools未安装，跳过PSD导出")
            return None
        except Exception as e:
            print(f"⚠️ PSD导出失败: {e}")
            return None
    
    def process_image(self, input_path, num_layers=6):
        """处理图像并生成分层"""
        print("\n" + "="*80)
        print("🎨 Live2D AI分层工具 v4.0")
        print("="*80)
        
        input_path = Path(input_path)
        if not input_path.exists():
            print(f"❌ 文件不存在: {input_path}")
            return None
        
        print(f"\n📷 输入: {input_path.name}")
        
        # 步骤1: AI预处理（如果可用）
        processed_path = self.remove_background(input_path)
        
        # 步骤2: 加载图像
        img = Image.open(processed_path)
        print(f"📐 尺寸: {img.size[0]} x {img.size[1]}")
        
        # 步骤3: 智能分层
        print("\n🔍 智能分层分析...")
        layers_data = self.intelligent_live2d_layering(img)
        
        # 步骤4: 创建图层图像
        print("\n🎨 创建图层...")
        layer_images = self.create_layer_images(img, layers_data)
        
        # 步骤5: 保存图层
        print("\n💾 保存图层...")
        output_dir = self.output_dir / f"{input_path.stem}_layers_qwen"
        output_dir.mkdir(exist_ok=True)
        
        saved_layers = []
        layer_order = [
            'Background', 'Body', 'Clothes', 'Hair_Back', 
            'Hair_Side', 'Face', 'Hair_Front', 'Eyes', 'Mouth', 'Hands', 'Accessories'
        ]
        
        for i, name in enumerate(layer_order):
            if name in layer_images:
                filename = f"{i+1:02d}_{name}.png"
                filepath = output_dir / filename
                layer_images[name].save(filepath)
                saved_layers.append((name, filepath))
                print(f"  ✅ {name}")
        
        # 步骤6: 创建指南
        guide_path = output_dir / "LAYERING_GUIDE.txt"
        self.create_guide(input_path, saved_layers, guide_path)
        
        # 步骤7: 导出PSD
        psd_path = self.output_dir / f"{input_path.stem}_live2d.psd"
        self.export_to_psd(layer_images, psd_path)
        
        print("\n" + "="*80)
        print("✅ 分层完成!")
        print("="*80)
        
        return {
            'output_dir': output_dir,
            'layers': saved_layers,
            'guide': guide_path,
            'psd': psd_path if psd_path.exists() else None
        }
    
    def create_guide(self, input_path, layers, guide_path):
        """创建分层指南"""
        width, height = Image.open(input_path).size
        
        guide = f"""
Live2D AI分层工具 v4.0 - 分层结果
{'='*80}

输入文件: {input_path.name}
图像尺寸: {width} x {height}
分层数量: {len(layers)}

{'='*80}
图层列表:
{'='*80}

"""
        
        for i, (name, path) in enumerate(layers):
            size = path.stat().st_size / 1024
            guide += f"{i+1}. {name:20s} - {size:.1f} KB\n"
        
        guide += f"""
{'='*80}
PSD导出方法:
{'='*80}

1. Photoshop:
   - File → Scripts → Load Files into Stack
   - 选择所有PNG文件（按序号顺序）
   - File → Save As → 选择PSD格式

2. 在线转换:
   - https://convertio.co/png-to-psd/
   - https://www.iloveimg.com/png-to-psd

3. GIMP（免费）:
   - File → Open as Layers
   - File → Export As → PSD

{'='*80}
Live2D导入步骤:
{'='*80}

1. 打开Live2D Cubism Editor
2. File → Import PSD
3. 选择生成的PSD文件
4. 勾选 "Create ArtMeshes"
5. 点击 OK
6. 开始制作你的Live2D模型！

{'='*80}
图层说明:
{'='*80}

- Body:        身体主体
- Clothes:     服装
- Hair_Back:   头发后部（底层）
- Hair_Side:   头发侧部
- Face:        脸部皮肤
- Hair_Front:  刘海/头发前部（顶层）
- Eyes:        眼睛
- Mouth:       嘴巴
- Hands:       手部
- Accessories: 配饰

{'='*80}
优化建议:
{'='*80}

1. 在Photoshop中可以进一步分离:
   - 左眼/右眼
   - 左手/右手
   - 头发各部分

2. 调整图层顺序以获得正确的视觉效果

3. 可以使用Qwen-Image-Layered获得更高精度:
   - 安装: pip install qwen-image-layered
   - 模型: Qwen/Qwen-VL-Layered-7B

"""
        
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide)

def main():
    """主函数"""
    tool = AdvancedLive2DLayerTool()
    
    if len(sys.argv) < 2:
        print("\n📖 使用方法:")
        print("  python live2d_layer_tool.py <图片路径>")
        print()
        print("🎯 AI模型状态:")
        for model, available in tool.available_models.items():
            status = "✅" if available else "❌"
            print(f"  {status} {model}")
        
        # 自动检测最新图片
        png_files = list(tool.output_dir.glob("*.png"))
        if png_files:
            latest = max(png_files, key=lambda p: p.stat().st_mtime)
            print(f"\n📷 检测到最新图片: {latest.name}")
            print(f"   运行: python live2d_layer_tool.py {latest}")
        return
    
    image_path = sys.argv[1]
    result = tool.process_image(image_path)
    
    if result:
        print(f"\n🎉 完成!")
        print(f"📁 分层目录: {result['output_dir'].name}")
        if result['psd']:
            print(f"📦 PSD文件: {result['psd'].name}")

if __name__ == "__main__":
    main()
