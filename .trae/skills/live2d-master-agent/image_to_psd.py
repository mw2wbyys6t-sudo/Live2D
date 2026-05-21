#!/usr/bin/env python3
"""
Live2D Master Agent - 图片转 PSD 工具
版本: 2.0
功能: 将角色图片转换为分层 PSD 文件
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional, Dict, List, Any

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("❌ 需要安装 Pillow: pip install pillow")

try:
    import psd_tools
    HAS_PSD = True
except ImportError:
    HAS_PSD = False


class ImageToPSDConverter:
    """图片转 PSD 转换器"""
    
    def __init__(self):
        self.output_dir = Path.cwd() / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # Live2D 角色分层模板
        self.layer_template = {
            '基础': ['身体', '皮肤', '躯干', '腿部', '脚部'],
            '服装': ['内衣', '衬衫', '裙子', '外套', '袜子', '鞋子', '配饰'],
            '头部': ['脸部', '眼睛', '嘴巴', '鼻子', '耳朵', '眉毛', '睫毛'],
            '头发': ['后发', '侧发', '刘海', '发饰', '呆毛'],
            '效果': ['阴影', '高光', '透明层']
        }
    
    def print_header(self):
        """打印标题"""
        print()
        print("=" * 70)
        print("🎨 Live2D Master Agent - 图片转 PSD")
        print("=" * 70)
        print()
    
    def print_info(self, msg: str):
        print(f"ℹ️  {msg}")
    
    def print_success(self, msg: str):
        print(f"✅ {msg}")
    
    def print_error(self, msg: str):
        print(f"❌ {msg}")
    
    def print_warning(self, msg: str):
        print(f"⚠️  {msg}")
    
    def check_dependencies(self) -> bool:
        """检查依赖"""
        print("🔍 检查依赖...")
        
        if not HAS_PIL:
            self.print_error("Pillow 未安装")
            print("请运行: pip install pillow")
            return False
        
        self.print_success("依赖检查通过")
        return True
    
    def load_image(self, image_path: str) -> Optional[Image.Image]:
        """加载图片"""
        try:
            img = Image.open(image_path)
            
            # 转换为 RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            self.print_success(f"图片加载成功: {img.size[0]}x{img.size[1]}")
            return img
            
        except Exception as e:
            self.print_error(f"图片加载失败: {e}")
            return None
    
    def generate_layer_plan(self, image: Image.Image) -> List[Dict[str, Any]]:
        """生成图层规划"""
        print()
        self.print_info("生成图层规划...")
        
        width, height = image.size
        
        # 根据图片尺寸决定分层
        if width >= 2000 or height >= 2000:
            layer_count = 15  # 高清图片更多分层
        elif width >= 1000 or height >= 1000:
            layer_count = 10
        else:
            layer_count = 6
        
        print(f"  将创建 {layer_count} 个图层")
        
        # 生成图层列表
        layers = [
            {"name": "整体参考", "type": "参考", "可见": True},
            {"name": "后头发", "type": "头发", "可见": True},
            {"name": "身体", "type": "身体", "可见": True},
            {"name": "服装_主体", "type": "服装", "可见": True},
            {"name": "前头发", "type": "头发", "可见": True},
            {"name": "脸部", "type": "头部", "可见": True},
            {"name": "眼睛", "type": "头部", "可见": True},
            {"name": "嘴巴", "type": "头部", "可见": True},
            {"name": "刘海", "type": "头发", "可见": True},
            {"name": "配饰", "type": "配饰", "可见": True},
        ]
        
        return layers[:layer_count]
    
    def create_psd_structure(self, image_path: str, layers: List[Dict]) -> Optional[str]:
        """创建 PSD 结构"""
        try:
            # 如果 psd_tools 可用，创建真实 PSD
            if HAS_PSD:
                return self._create_real_psd(image_path, layers)
            else:
                # 否则创建替代方案
                return self._create_alternative(image_path, layers)
                
        except Exception as e:
            self.print_error(f"PSD 创建失败: {e}")
            return None
    
    def _create_real_psd(self, image_path: str, layers: List[Dict]) -> Optional[str]:
        """使用 psd_tools 创建真实 PSD"""
        try:
            from psd_tools import PSDImage
            from psd_tools.api.layers import PixelLayer
            
            img = Image.open(image_path)
            width, height = img.size
            
            # 创建 PSD
            psd = PSDImage.new('RGB', (width, height))
            
            # 添加图层
            for i, layer_info in enumerate(layers):
                # 创建每个图层的图像
                layer_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                # 这里应该是实际的分割逻辑，简化版本复制原图
                layer_img.paste(img, (0, 0))
                
                # 添加到 PSD
                layer = PixelLayer.frompil(psd, layer_img)
                layer.name = layer_info['name']
                layer.visible = layer_info['visible']
            
            # 保存 PSD
            output_path = self.output_dir / f"live2d_layers_{int(time.time())}.psd"
            psd.save(str(output_path))
            
            self.print_success(f"PSD 保存成功: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.print_warning(f"psd_tools 创建失败: {e}")
            return self._create_alternative(image_path, layers)
    
    def _create_alternative(self, image_path: str, layers: List[Dict]) -> Optional[str]:
        """创建替代方案 - 输出规划文件和分层指南"""
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            # 创建分层指南文件
            output_dir = self.output_dir / f"psd_plan_{int(time.time())}"
            output_dir.mkdir(exist_ok=True)
            
            # 保存原图
            img.save(output_dir / "reference.png")
            
            # 保存分层模板
            template_file = output_dir / "layer_guide.txt"
            with open(template_file, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write("Live2D PSD 分层指南\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"原图尺寸: {width} x {height}\n")
                f.write(f"图层数量: {len(layers)}\n\n")
                
                f.write("图层结构:\n")
                f.write("-" * 50 + "\n")
                for i, layer in enumerate(layers):
                    f.write(f"{i+1}. {layer['name']} ({layer['type']})\n")
                    f.write(f"   - 可见: {'是' if layer['visible'] else '否'}\n")
                
                f.write("\n" + "=" * 50 + "\n")
                f.write("分层步骤:\n")
                f.write("=" * 50 + "\n")
                f.write("""
1. 在 Photoshop 中打开 reference.png
2. 根据 layer_guide.txt 创建图层组
3. 使用快速选择工具分离各部分
4. 保存为 PSD 格式
5. 使用 Live2D Cubism 导入

提示:
- 每个图层应该是独立的元素
- 使用图层蒙版便于调整
- 确保图层命名规范
- 避免使用图层样式（会干扰 Live2D）
""")
            
            # 保存为单个分层 PNG
            for i, layer in enumerate(layers):
                layer_file = output_dir / f"layer_{i+1}_{layer['name']}.png"
                img.save(layer_file)
            
            self.print_success(f"分层规划已保存: {output_dir}")
            return str(output_dir)
            
        except Exception as e:
            self.print_error(f"替代方案创建失败: {e}")
            return None
    
    def convert(self, image_path: str) -> Optional[str]:
        """转换图片到 PSD"""
        if not self.check_dependencies():
            return None
        
        # 加载图片
        img = self.load_image(image_path)
        if not img:
            return None
        
        # 生成图层规划
        layers = self.generate_layer_plan(img)
        
        # 创建 PSD
        result = self.create_psd_structure(image_path, layers)
        
        return result
    
    def interactive_convert(self):
        """交互式转换"""
        self.print_header()
        
        # 获取图片路径
        print("请输入图片路径（留空使用 output/reference.png）:")
        image_path = input("图片路径: ").strip()
        
        if not image_path:
            default_path = self.output_dir / "reference.png"
            if default_path.exists():
                image_path = str(default_path)
            else:
                self.print_error("默认路径没有图片，请提供图片路径")
                return
        
        if not Path(image_path).exists():
            self.print_error(f"文件不存在: {image_path}")
            return
        
        # 执行转换
        print()
        result = self.convert(image_path)
        
        if result:
            print()
            self.print_success("转换完成！")
            print()
            print("📁 输出位置:", result)
            print()
            print("💡 下一步:")
            print("  1. 查看分层结果")
            print("  2. 使用 QA 工具检查: python scripts/qa_engine_enhanced.py")
            print("  3. 设计参数: python scripts/parameter_designer_enhanced.py")
        else:
            print()
            self.print_error("转换失败")


def main():
    """主函数"""
    converter = ImageToPSDConverter()
    
    # 命令行参数
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        result = converter.convert(image_path)
        
        if result:
            print()
            print(f"✅ 转换完成: {result}")
        else:
            print()
            print("❌ 转换失败")
            sys.exit(1)
    else:
        converter.interactive_convert()


if __name__ == "__main__":
    main()
