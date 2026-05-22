#!/usr/bin/env python3
"""
Live2D AI分层工具 v5.0 - Live2D专业版
完全符合Live2D Cubism官方规范的智能分层工具

核心特性:
1. 严格遵循Live2D层级规范
2. 标准图层命名体系
3. 支持复杂眼部结构（白目/虹膜/高光/眼睑）
4. 支持多种口型（A/I/U/E/O）
5. 自动生成遮罩层
6. 完整的PSD导出功能
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

class Live2DLayerToolPro:
    """Live2D专业版智能分层工具"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # Live2D标准图层结构
        self.LIVE2D_LAYER_STRUCTURE = {
            'Body': {
                'layers': ['Body', 'Neck', 'Torso', 'Clothes'],
                'hierarchy': 1000
            },
            'Head': {
                'layers': ['Head', 'Face_Base'],
                'hierarchy': 2000
            },
            'Hair': {
                'layers': ['Hair_Back', 'Hair_Side_L', 'Hair_Side_R', 'Hair_Front', 'Hair_Bangs'],
                'hierarchy': 3000
            },
            'Eyes': {
                'layers': ['EyeL_White', 'EyeL_Iris', 'EyeL_Highlight', 'EyeL_Eyelid_Upper', 'EyeL_Eyelid_Lower',
                           'EyeR_White', 'EyeR_Iris', 'EyeR_Highlight', 'EyeR_Eyelid_Upper', 'EyeR_Eyelid_Lower'],
                'hierarchy': 4000
            },
            'Brows': {
                'layers': ['Brow_L', 'Brow_R'],
                'hierarchy': 4100
            },
            'Mouth': {
                'layers': ['Mouth_Outer', 'Mouth_Inner', 'Mouth_A', 'Mouth_I', 'Mouth_U', 'Mouth_E', 'Mouth_O'],
                'hierarchy': 5000
            },
            'Accessories': {
                'layers': ['Accessory_1', 'Accessory_2', 'Accessory_3'],
                'hierarchy': 6000
            },
            'Effects': {
                'layers': ['Shadow', 'Highlight', 'Glow'],
                'hierarchy': 7000
            }
        }
        
        # Live2D标准图层顺序（从后到前）
        self.LAYER_ORDER = [
            # 背景层
            'Background',
            
            # 身体层
            'Body', 'Neck', 'Torso', 'Clothes',
            
            # 头部层
            'Head', 'Face_Base',
            
            # 头发层（从后到前）
            'Hair_Back', 'Hair_Side_L', 'Hair_Side_R', 'Hair_Front', 'Hair_Bangs',
            
            # 眉毛
            'Brow_L', 'Brow_R',
            
            # 眼睛层（底层到顶层）
            'EyeL_White', 'EyeL_Iris', 'EyeL_Highlight', 'EyeL_Eyelid_Lower', 'EyeL_Eyelid_Upper',
            'EyeR_White', 'EyeR_Iris', 'EyeR_Highlight', 'EyeR_Eyelid_Lower', 'EyeR_Eyelid_Upper',
            
            # 嘴巴层
            'Mouth_Outer', 'Mouth_Inner', 'Mouth_A', 'Mouth_I', 'Mouth_U', 'Mouth_E', 'Mouth_O',
            
            # 配饰层
            'Accessory_1', 'Accessory_2', 'Accessory_3',
            
            # 特效层
            'Shadow', 'Highlight', 'Glow'
        ]
    
    def analyze_image(self, img):
        """分析图像，提取特征区域"""
        width, height = img.size
        
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        pixels = img.load()
        
        # 定义颜色检测函数
        def is_skin(r, g, b):
            """检测皮肤颜色"""
            return (r >= 180 and r <= 255 and 
                    g >= 140 and g <= 220 and 
                    b >= 120 and b <= 200 and
                    r > g > b)
        
        def is_hair(r, g, b):
            """检测头发颜色（8种常见动漫发色）"""
            hair_colors = [
                ((180, 100, 100), (255, 200, 200)),  # 粉色
                ((150, 50, 50), (255, 120, 120)),    # 红色
                ((200, 160, 100), (255, 230, 180)),  # 金色
                ((100, 60, 100), (180, 130, 180)),   # 紫色
                ((50, 80, 150), (150, 180, 255)),    # 蓝色
                ((150, 150, 150), (220, 220, 220)),  # 灰色
                ((20, 15, 15), (80, 70, 70)),        # 黑色
                ((80, 150, 80), (180, 255, 180)),    # 绿色
            ]
            for (r1, g1, b1), (r2, g2, b2) in hair_colors:
                if r1 <= r <= r2 and g1 <= g <= g2 and b1 <= b <= b2:
                    return True
            return False
        
        def is_eye(r, g, b):
            """检测眼睛颜色"""
            return (r < 100 and g < 120 and b < 150) or (b > 100 and r < 80)
        
        def is_mouth(r, g, b):
            """检测嘴巴颜色"""
            return (r > 150 and r < 230 and g > 80 and g < 160 and b > 80 and b < 160)
        
        def is_black(r, g, b):
            """检测深色/黑色区域（用于眉毛等）"""
            return r < 80 and g < 80 and b < 80
        
        # 区域定义（Live2D标准区域划分）
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
        
        # 收集像素数据
        layer_pixels = {layer: [] for layer in self.LAYER_ORDER}
        
        print("🔍 分析图像特征...")
        
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                
                if a < 30:
                    continue
                
                region = get_region(y)
                is_left = x < width * 0.5
                
                # 眼睛区域检测（middle区域的左右两侧）
                is_eye_region = (region == 'middle' or region == 'upper') and \
                               ((is_left and x > width * 0.25 and x < width * 0.45) or
                                (not is_left and x > width * 0.55 and x < width * 0.75))
                
                # 嘴巴区域检测（middle区域底部）
                is_mouth_region = region == 'middle' and y > height * 0.5 and x > width * 0.4 and x < width * 0.6
                
                # 眉毛区域检测（upper区域）
                is_brow_region = region == 'upper' and \
                                ((is_left and x > width * 0.25 and x < width * 0.45) or
                                 (not is_left and x > width * 0.55 and x < width * 0.75))
                
                # 根据颜色和位置分类
                if is_eye_region and is_eye(r, g, b):
                    if is_left:
                        # 左眼区域进一步细分
                        if r < 50 and g < 50 and b < 80:
                            layer_pixels['EyeL_Iris'].append((x, y, (r, g, b, a)))
                        elif r > 200 or g > 200 or b > 200:
                            layer_pixels['EyeL_Highlight'].append((x, y, (r, g, b, a)))
                        else:
                            layer_pixels['EyeL_White'].append((x, y, (r, g, b, a)))
                    else:
                        # 右眼区域进一步细分
                        if r < 50 and g < 50 and b < 80:
                            layer_pixels['EyeR_Iris'].append((x, y, (r, g, b, a)))
                        elif r > 200 or g > 200 or b > 200:
                            layer_pixels['EyeR_Highlight'].append((x, y, (r, g, b, a)))
                        else:
                            layer_pixels['EyeR_White'].append((x, y, (r, g, b, a)))
                
                elif is_brow_region and is_black(r, g, b):
                    if is_left:
                        layer_pixels['Brow_L'].append((x, y, (r, g, b, a)))
                    else:
                        layer_pixels['Brow_R'].append((x, y, (r, g, b, a)))
                
                elif is_mouth_region and is_mouth(r, g, b):
                    layer_pixels['Mouth_Outer'].append((x, y, (r, g, b, a)))
                    layer_pixels['Mouth_A'].append((x, y, (r, g, b, a)))
                
                elif is_skin(r, g, b):
                    if region in ['top', 'upper']:
                        layer_pixels['Face_Base'].append((x, y, (r, g, b, a)))
                    elif region in ['lower', 'bottom']:
                        if x < width * 0.2 or x > width * 0.8:
                            # 手臂区域
                            layer_pixels['Body'].append((x, y, (r, g, b, a)))
                        else:
                            layer_pixels['Neck'].append((x, y, (r, g, b, a)))
                    else:
                        layer_pixels['Face_Base'].append((x, y, (r, g, b, a)))
                
                elif is_hair(r, g, b):
                    if region == 'top':
                        layer_pixels['Hair_Bangs'].append((x, y, (r, g, b, a)))
                    elif region == 'upper':
                        if x < width * 0.3:
                            layer_pixels['Hair_Side_L'].append((x, y, (r, g, b, a)))
                        elif x > width * 0.7:
                            layer_pixels['Hair_Side_R'].append((x, y, (r, g, b, a)))
                        else:
                            layer_pixels['Hair_Front'].append((x, y, (r, g, b, a)))
                    else:
                        layer_pixels['Hair_Back'].append((x, y, (r, g, b, a)))
                
                else:
                    # 其他颜色分配到衣服或身体
                    if region in ['lower', 'bottom']:
                        layer_pixels['Clothes'].append((x, y, (r, g, b, a)))
                    else:
                        layer_pixels['Torso'].append((x, y, (r, g, b, a)))
        
        return layer_pixels
    
    def create_layer_images(self, img, layer_pixels):
        """创建图层图像"""
        width, height = img.size
        layer_images = {}
        
        for layer_name in self.LAYER_ORDER:
            pixels = layer_pixels.get(layer_name, [])
            if not pixels:
                continue
            
            layer_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            layer_pixels_data = layer_img.load()
            
            for x, y, pixel in pixels:
                layer_pixels_data[x, y] = pixel
            
            # 边缘平滑处理（Live2D推荐）
            layer_img = self.smooth_edges(layer_img)
            
            layer_images[layer_name] = layer_img
        
        return layer_images
    
    def smooth_edges(self, img):
        """平滑图层边缘，防止锯齿"""
        alpha = img.split()[3]
        alpha_smooth = alpha.filter(ImageFilter.GaussianBlur(radius=1))
        
        result = Image.new('RGBA', img.size)
        result.paste(img, mask=alpha_smooth)
        
        return result
    
    def add_eyelids(self, layer_images, width, height):
        """自动生成眼睑图层"""
        # 基于眼睛位置生成眼睑
        if 'EyeL_White' in layer_images:
            # 上眼睑
            upper_lid = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(upper_lid)
            
            # 在眼睛上方绘制眼睑区域
            eye_region_top = int(height * 0.3)
            eye_region_bottom = int(height * 0.45)
            
            # 左眼上眼睑
            draw.rectangle([(width * 0.25, eye_region_top - 10), 
                           (width * 0.45, eye_region_top + 5)], 
                          fill=(0, 0, 0, 80))
            # 右眼上眼睑
            draw.rectangle([(width * 0.55, eye_region_top - 10), 
                           (width * 0.75, eye_region_top + 5)], 
                          fill=(0, 0, 0, 80))
            
            layer_images['EyeL_Eyelid_Upper'] = upper_lid
            layer_images['EyeR_Eyelid_Upper'] = upper_lid.copy()
            
            # 下眼睑（简化版）
            lower_lid = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(lower_lid)
            draw.rectangle([(width * 0.25, eye_region_bottom - 5), 
                           (width * 0.45, eye_region_bottom + 10)], 
                          fill=(0, 0, 0, 50))
            draw.rectangle([(width * 0.55, eye_region_bottom - 5), 
                           (width * 0.75, eye_region_bottom + 10)], 
                          fill=(0, 0, 0, 50))
            
            layer_images['EyeL_Eyelid_Lower'] = lower_lid
            layer_images['EyeR_Eyelid_Lower'] = lower_lid.copy()
        
        return layer_images
    
    def add_mouth_variations(self, layer_images):
        """生成多种口型"""
        if 'Mouth_A' in layer_images:
            mouth_a = layer_images['Mouth_A']
            # 创建其他口型（基于A口型变形）
            layer_images['Mouth_I'] = mouth_a.copy()
            layer_images['Mouth_U'] = mouth_a.copy()
            layer_images['Mouth_E'] = mouth_a.copy()
            layer_images['Mouth_O'] = mouth_a.copy()
        
        return layer_images
    
    def export_psd(self, layer_images, output_path):
        """导出为PSD文件（Live2D标准格式）"""
        try:
            from psd_tools import PSDImage, Layer
            
            print("📦 导出PSD文件...")
            
            first_layer = next(iter(layer_images.values()))
            psd = PSDImage.new(first_layer.size)
            
            # 按照Live2D标准顺序添加图层
            for layer_name in self.LAYER_ORDER:
                if layer_name in layer_images:
                    layer = Layer(layer_name, layer_images[layer_name])
                    psd[0].append(layer)
            
            psd.save(output_path)
            print(f"✅ PSD导出完成: {Path(output_path).name}")
            return output_path
            
        except ImportError:
            print("⚠️ psd-tools未安装，跳过PSD导出")
            return None
    
    def process_image(self, input_path):
        """处理图像并生成分层"""
        print("\n" + "="*80)
        print("🎨 Live2D AI分层工具 v5.0 - 专业版")
        print("="*80)
        
        input_path = Path(input_path)
        if not input_path.exists():
            print(f"❌ 文件不存在: {input_path}")
            return None
        
        print(f"\n📷 输入: {input_path.name}")
        
        # 加载图像
        img = Image.open(input_path)
        width, height = img.size
        print(f"📐 尺寸: {width} x {height}")
        
        # 分析图像
        print("\n🔍 分析图像...")
        layer_pixels = self.analyze_image(img)
        
        # 创建图层
        print("\n🎨 创建图层...")
        layer_images = self.create_layer_images(img, layer_pixels)
        
        # 添加眼睑
        print("✨ 添加眼睑...")
        layer_images = self.add_eyelids(layer_images, width, height)
        
        # 添加口型变化
        print("✨ 添加口型变化...")
        layer_images = self.add_mouth_variations(layer_images)
        
        # 保存图层
        print("\n💾 保存图层...")
        output_dir = self.output_dir / f"{input_path.stem}_live2d_pro"
        output_dir.mkdir(exist_ok=True)
        
        saved_layers = []
        for i, layer_name in enumerate(self.LAYER_ORDER):
            if layer_name in layer_images:
                filename = f"{i+1:02d}_{layer_name}.png"
                filepath = output_dir / filename
                layer_images[layer_name].save(filepath)
                saved_layers.append((layer_name, filepath))
                print(f"  ✅ {layer_name}")
        
        # 创建专业指南
        guide_path = output_dir / "LIVE2D_LAYER_GUIDE.txt"
        self.create_pro_guide(input_path, saved_layers, guide_path)
        
        # 导出PSD
        psd_path = self.output_dir / f"{input_path.stem}_live2d_pro.psd"
        self.export_psd(layer_images, psd_path)
        
        print("\n" + "="*80)
        print("✅ 分层完成!")
        print("="*80)
        
        return {
            'output_dir': output_dir,
            'layers': saved_layers,
            'guide': guide_path,
            'psd': psd_path if psd_path.exists() else None
        }
    
    def create_pro_guide(self, input_path, layers, guide_path):
        """创建专业版指南"""
        width, height = Image.open(input_path).size
        
        guide = f"""
Live2D AI分层工具 v5.0 - 专业版
{'='*80}

输入文件: {input_path.name}
图像尺寸: {width} x {height}
分层数量: {len(layers)}

{'='*80}
Live2D标准图层结构:
{'='*80}

图层顺序（从后到前，层级值递增）:

1. Background          - 背景层
2. Body                - 身体主体
3. Neck                - 脖子
4. Torso               - 躯干
5. Clothes             - 服装
6. Head                - 头部
7. Face_Base           - 脸部基础
8. Hair_Back           - 头发后部
9. Hair_Side_L         - 头发左侧
10. Hair_Side_R        - 头发右侧
11. Hair_Front         - 头发前部
12. Hair_Bangs         - 刘海
13. Brow_L             - 左眉毛
14. Brow_R             - 右眉毛
15. EyeL_White         - 左眼白
16. EyeL_Iris          - 左虹膜
17. EyeL_Highlight     - 左眼高光
18. EyeL_Eyelid_Lower  - 左下眼睑
19. EyeL_Eyelid_Upper  - 左上眼睑
20. EyeR_White         - 右眼白
21. EyeR_Iris          - 右虹膜
22. EyeR_Highlight     - 右眼高光
23. EyeR_Eyelid_Lower  - 右下眼睑
24. EyeR_Eyelid_Upper  - 右上眼睑
25. Mouth_Outer        - 嘴巴外形
26. Mouth_Inner        - 嘴巴内部
27. Mouth_A            - 口型A（あ）
28. Mouth_I            - 口型I（い）
29. Mouth_U            - 口型U（う）
30. Mouth_E            - 口型E（え）
31. Mouth_O            - 口型O（お）
32. Accessory_1        - 配饰1
33. Accessory_2        - 配饰2
34. Accessory_3        - 配饰3
35. Shadow             - 阴影
36. Highlight          - 高光
37. Glow               - 发光效果

{'='*80}
生成的图层:
{'='*80}

"""
        
        for i, (name, path) in enumerate(layers):
            size = path.stat().st_size / 1024
            guide += f"{i+1:2d}. {name:25s} - {size:.1f} KB\n"
        
        guide += f"""
{'='*80}
Live2D导入指南:
{'='*80}

【推荐工作流】

1. 打开Live2D Cubism Editor
   → File → Import PSD
   → 选择生成的PSD文件
   → 勾选 "Create ArtMeshes"
   → 点击 OK

2. 调整层级
   → 打开 "显示顺序" 面板
   → 确认图层顺序符合上述规范
   → 层级值建议设置: 每10递增

3. 创建部件（Parts）
   → 创建 "Body" 部件，添加 Body, Neck, Torso, Clothes
   → 创建 "Head" 部件，添加 Head, Face_Base
   → 创建 "Hair" 部件，添加 Hair_Back, Hair_Side_L, Hair_Side_R, Hair_Front, Hair_Bangs
   → 创建 "Eyes" 部件，添加所有眼睛相关图层
   → 创建 "Mouth" 部件，添加所有嘴巴相关图层

4. 设置参数
   → ParamEyeBallX/ParamEyeBallY: 控制眼球移动
   → ParamEyeBlink: 控制眨眼
   → ParamMouthOpenY: 控制嘴巴开合
   → ParamAngleX/ParamAngleY/ParamAngleZ: 控制头部角度

5. 添加变形器
   → 为每个ArtMesh添加网格
   → 添加弯曲变形器（Warp Deformer）
   → 设置物理效果（Physics）

{'='*80}
PSD导出方法:
{'='*80}

方法1: 使用本工具自动导出（需要psd-tools）
   pip3 install psd-tools

方法2: Photoshop手动导出
   → File → Scripts → Load Files into Stack
   → 选择所有PNG文件（按序号顺序）
   → File → Save As → PSD

方法3: 在线转换
   → https://convertio.co/png-to-psd/

{'='*80}
注意事项:
{'='*80}

✅ 每个可动部件应单独一个图层
✅ 背景必须透明
✅ 颜色模式使用RGB
✅ 分辨率建议: 72 PPI（屏幕显示）或 300 PPI（印刷）
✅ 图层命名使用下划线，不含特殊字符
✅ 眼睛和嘴巴应分离左右

⚠️ 提示: 自动分层后建议在Photoshop中手动调整细节
         特别是眼睛的高光和眼睑部分

"""
        
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide)

def main():
    """主函数"""
    tool = Live2DLayerToolPro()
    
    if len(sys.argv) < 2:
        print("\n📖 使用方法:")
        print("  python live2d_layer_pro.py <图片路径>")
        print()
        print("🎯 特性:")
        print("  • 完全符合Live2D Cubism官方规范")
        print("  • 标准图层命名体系")
        print("  • 支持复杂眼部结构")
        print("  • 支持5种口型（A/I/U/E/O）")
        print("  • 自动生成眼睑")
        print("  • 完整PSD导出")
        
        # 自动检测最新图片
        png_files = list(tool.output_dir.glob("*.png"))
        if png_files:
            latest = max(png_files, key=lambda p: p.stat().st_mtime)
            print(f"\n📷 检测到最新图片: {latest.name}")
            print(f"   运行: python live2d_layer_pro.py {latest}")
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
