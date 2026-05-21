#!/usr/bin/env python3
"""
Live2D Master Agent - 一站式工具箱
版本: 3.0
功能: 综合所有功能，一步到位生成 Live2D 角色
"""

import os
import sys
import time
import urllib.request
import urllib.parse
import subprocess
from pathlib import Path
from typing import Optional, List, Dict

class Live2DMaster:
    """Live2D 一站式工具"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # 生成的图片路径
        self.generated_image = None
    
    def print_header(self):
        """打印标题"""
        print()
        print("=" * 70)
        print("🎨 Live2D Master Agent - 一站式工具箱 v3.0")
        print("=" * 70)
        print()
    
    def print_success(self, msg: str):
        print(f"✅ {msg}")
    
    def print_error(self, msg: str):
        print(f"❌ {msg}")
    
    def print_warning(self, msg: str):
        print(f"⚠️  {msg}")
    
    def print_info(self, msg: str):
        print(f"ℹ️  {msg}")
    
    # ============ 图片生成功能 ============
    
    def test_service(self, name: str, test_func) -> bool:
        """测试服务是否可用"""
        try:
            print(f"  测试 {name}...", end=" ")
            result = test_func()
            if result:
                print("✅")
                return True
            else:
                print("❌")
                return False
        except Exception as e:
            print(f"❌ ({str(e)[:30]})")
            return False
    
    def generate_with_pollinations(self, prompt: str) -> Optional[str]:
        """使用 Pollinations.ai 生成"""
        try:
            print("🤖 使用 Pollinations.ai...")
            
            # 构建提示词
            full_prompt = f"{prompt}, perfect for Live2D rigging, clean layer separation, isolated character on white background, sharp clean lines, vibrant colors, ultra detailed, masterpiece"
            encoded = urllib.parse.quote(full_prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded}?width=768&height=768&seed={int(time.time()) % 1000000}"
            
            # 下载
            output_file = self.output_dir / f"live2d_{int(time.time())}.png"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://pollinations.ai/'
            }
            
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=120) as response:
                with open(output_file, 'wb') as f:
                    f.write(response.read())
            
            self.generated_image = str(output_file)
            return str(output_file)
            
        except Exception as e:
            self.print_error(f"Pollinations.ai 失败: {str(e)}")
            return None
    
    def generate_offline(self, prompt: str) -> Optional[str]:
        """离线模式 - 使用已生成的图片"""
        print("💡 离线模式")
        
        # 查找最新的输出图片
        png_files = sorted(self.output_dir.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
        
        if png_files:
            latest = png_files[0]
            self.generated_image = str(latest)
            return str(latest)
        
        self.print_error("没有找到可用的图片")
        return None
    
    def generate_image(self, prompt: str) -> Optional[str]:
        """综合图片生成"""
        print("🎨 开始生成图片...")
        print()
        
        # 尝试 Pollinations.ai
        result = self.generate_with_pollinations(prompt)
        if result:
            return result
        
        # 尝试其他方案
        print()
        print("⚠️ 在线生成服务暂时不可用")
        print()
        print("💡 备选方案:")
        print()
        print("🌐 在线生成（推荐，无需安装）:")
        print("   1. 访问 https://pollinations.ai 生成图片")
        print("   2. 访问 https://playground.com")
        print("   3. 访问 https://leonardo.ai (免费额度)")
        print()
        print("💻 本地最高质量:")
        print("   python install_comfyui.py")
        print()
        print("🔑 API Key 配置:")
        print("   python config_api.py")
        print()
        print("📖 查看详细解决方案: FREE_SOLUTIONS.md")
        print()
        print("📁 请将生成的图片放到 output/ 目录中")
        print("   然后运行: python master_tool.py --skip-generate")
        
        return None
    
    # ============ PSD 功能 ============
    
    def create_psd_plan(self, image_path: str) -> Optional[str]:
        """创建 PSD 分层规划"""
        try:
            from PIL import Image
            
            img = Image.open(image_path)
            width, height = img.size
            
            print()
            print("📋 生成 PSD 分层规划...")
            
            # 创建规划目录
            plan_dir = self.output_dir / f"psd_plan_{int(time.time())}"
            plan_dir.mkdir(exist_ok=True)
            
            # 保存原图
            img.save(plan_dir / "reference.png")
            
            # 生成图层指南
            guide_file = plan_dir / "LAYER_GUIDE.txt"
            with open(guide_file, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("Live2D PSD 分层指南\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"📐 图片尺寸: {width} x {height}\n\n")
                
                f.write("📁 推荐图层结构:\n")
                f.write("-" * 60 + "\n")
                
                layers = [
                    ("1. ArtMesh/身体", "身体、躯干"),
                    ("2. ArtMesh/头发_后", "后部头发"),
                    ("3. ArtMesh/服装", "主体服装"),
                    ("4. ArtMesh/头发_侧", "侧面头发"),
                    ("5. ArtMesh/脸", "脸部"),
                    ("6. ArtMesh/眼睛", "眼睛（左右）"),
                    ("7. ArtMesh/嘴巴", "嘴巴"),
                    ("8. ArtMesh/头发_前", "刘海"),
                    ("9. ArtMesh/手", "手部"),
                    ("10. ArtMesh/配饰", "装饰物"),
                ]
                
                for name, desc in layers:
                    f.write(f"  {name}\n    说明: {desc}\n\n")
                
                f.write("-" * 60 + "\n")
                f.write("\n📝 Photoshop 操作步骤:\n")
                f.write("-" * 60 + "\n")
                f.write("""
1. 打开 reference.png
2. 创建图层组并按上述结构命名
3. 使用钢笔工具或快速选择工具分离各部分
4. 将每个部分放到对应图层
5. 保存为 PSD 格式
6. 在 Live2D Cubism 中导入

⚠️ 注意事项:
- 保持图层命名规范（避免中文）
- 使用图层蒙版便于调整
- 不要使用图层样式
- 确保分辨率一致
""")
            
            self.print_success(f"分层规划已保存: {plan_dir}")
            return str(plan_dir)
            
        except ImportError:
            self.print_error("需要安装 Pillow: pip install pillow")
            return None
        except Exception as e:
            self.print_error(f"创建分层规划失败: {e}")
            return None
    
    # ============ 主流程 ============
    
    def run(self, prompt: str = None, skip_generate: bool = False):
        """运行完整流程"""
        self.print_header()
        
        # 1. 获取或生成图片
        image_path = None
        
        if skip_generate:
            # 使用已存在的图片
            png_files = sorted(self.output_dir.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
            if png_files:
                image_path = str(png_files[0])
                print(f"📷 使用已有图片: {image_path}")
            else:
                self.print_error("output/ 目录中没有图片")
                return
        else:
            # 生成新图片
            if not prompt:
                print("请输入角色描述:")
                prompt = input("> ").strip() or "anime girl, cute, pink hair, JK uniform"
            
            print(f"🎯 提示词: {prompt}")
            image_path = self.generate_image(prompt)
        
        if not image_path:
            print()
            print("💡 提示: 你可以:")
            print("  1. 手动上传图片到 output/ 目录")
            print("  2. 使用其他方式生成图片")
            print("  3. 然后运行: python master_tool.py --skip-generate")
            return
        
        # 2. 创建 PSD 分层规划
        psd_plan = self.create_psd_plan(image_path)
        
        # 3. 完成
        print()
        print("=" * 70)
        print("🎉 Live2D 角色制作准备完成！")
        print("=" * 70)
        print()
        print("📁 生成的文件:")
        print(f"  📷 图片: {image_path}")
        if psd_plan:
            print(f"  📋 分层规划: {psd_plan}")
        print()
        print("💡 下一步:")
        print("  1. 查看生成的图片")
        print("  2. 按照 LAYER_GUIDE.txt 进行 Photoshop 分层")
        print("  3. 质量检查: python scripts/qa_engine_enhanced.py")
        print("  4. 参数设计: python scripts/parameter_designer_enhanced.py")
        print("  5. 查看 Rigging 指南: docs/RIGGING_GUIDE.md")
        print()
    
    def help(self):
        """显示帮助"""
        self.print_header()
        print("""
📖 使用方法:

1. 一键生成（使用默认提示词）:
   python master_tool.py

2. 自定义提示词生成:
   python master_tool.py "anime girl, blue hair"

3. 使用已有图片（跳过生成）:
   python master_tool.py --skip-generate

4. 查看其他工具:
   - 快速生成: python quick_gen.py "提示词"
   - PSD 分层: python image_to_psd.py
   - API 配置: python config_api.py
   - ComfyUI: python install_comfyui.py
""")


def main():
    """主函数"""
    tool = Live2DMaster()
    
    # 解析参数
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            tool.help()
        elif sys.argv[1] in ['--skip-generate', '-s']:
            tool.run(skip_generate=True)
        else:
            prompt = " ".join(sys.argv[1:])
            tool.run(prompt=prompt)
    else:
        tool.run()


if __name__ == "__main__":
    main()
