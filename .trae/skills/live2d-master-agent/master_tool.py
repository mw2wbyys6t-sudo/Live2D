#!/usr/bin/env python3
"""
Live2D Master Agent - 一站式工具箱 v3.1 (优化版)
功能: 整合所有功能，一步到位生成 Live2D 角色
优化内容: 
- 代码精简
- 网络稳定性增强
- 用户体验提升
- 自动降级机制完善
"""

import os
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional, List, Dict


class Live2DMaster:
    """Live2D 一站式工具 - 优化版"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.generated_image = None
    
    def log(self, msg: str, type: str = "info"):
        """统一日志输出"""
        prefixes = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
            "action": "🔧",
            "progress": "⏳"
        }
        print(f"{prefixes.get(type, 'ℹ️')} {msg}")
    
    def _get_latest_image(self) -> Optional[str]:
        """获取最新的图片文件"""
        png_files = sorted(self.output_dir.glob("*.png"), 
                          key=lambda p: p.stat().st_mtime, reverse=True)
        return str(png_files[0]) if png_files else None
    
    def _download_image(self, url: str, output_path: Path, headers: Dict = None, 
                       max_retries: int = 3) -> bool:
        """带重试的图片下载"""
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Referer': 'https://pollinations.ai/'
            }
        
        for attempt in range(max_retries):
            try:
                self.log(f"下载尝试 {attempt + 1}/{max_retries}...", "progress")
                req = urllib.request.Request(url, headers=headers)
                
                with urllib.request.urlopen(req, timeout=120) as response:
                    data = response.read()
                    if len(data) < 1000:
                        self.log(f"文件太小({len(data)} bytes),重试...", "warning")
                        continue
                    
                    with open(output_path, 'wb') as f:
                        f.write(data)
                    return True
                    
            except Exception as e:
                self.log(f"下载失败: {str(e)[:50]}", "error")
                if attempt < max_retries - 1:
                    wait = (attempt + 1) * 2
                    self.log(f"等待 {wait} 秒后重试...", "info")
                    time.sleep(wait)
        
        return False
    
    def _build_prompt(self, prompt: str) -> str:
        """构建优化的Live2D提示词"""
        optimizations = [
            "perfect for Live2D rigging",
            "clean layer separation",
            "isolated character on white background",
            "sharp clean lines",
            "vibrant colors",
            "ultra detailed",
            "masterpiece"
        ]
        suffix = ", " + ", ".join(optimizations)
        return f"{prompt}{suffix}" if suffix not in prompt else prompt
    
    def generate_image(self, prompt: str) -> Optional[str]:
        """综合图片生成 - 优化版"""
        self.log("开始生成图片...", "action")
        
        # 尝试主服务
        result = self._try_pollinations(prompt)
        if result:
            return result
        
        # 显示备选方案
        self._show_fallback_options()
        return None
    
    def _try_pollinations(self, prompt: str) -> Optional[str]:
        """尝试 Pollinations.ai"""
        try:
            self.log("使用 Pollinations.ai (免费)...", "info")
            
            full_prompt = self._build_prompt(prompt)
            encoded = urllib.parse.quote(full_prompt)
            seed = int(time.time()) % 1000000
            url = f"https://image.pollinations.ai/prompt/{encoded}?width=768&height=768&seed={seed}"
            
            output_file = self.output_dir / f"live2d_pollinations_{int(time.time())}.png"
            
            if self._download_image(url, output_file):
                self.log(f"图片生成成功: {output_file.name}", "success")
                self.generated_image = str(output_file)
                return str(output_file)
            
        except Exception as e:
            self.log(f"Pollinations.ai 失败: {str(e)[:50]}", "error")
        
        return None
    
    def _show_fallback_options(self):
        """显示备选方案"""
        self.log("主服务暂时不可用", "warning")
        self.log("\n💡 备选方案:", "info")
        self.log("\n🌐 在线生成:", "action")
        self.log("   1. 访问 https://pollinations.ai")
        self.log("   2. 访问 https://playground.com")
        self.log("   3. 访问 https://leonardo.ai")
        self.log("\n💻 本地部署:", "action")
        self.log("   python install_comfyui.py")
        self.log("\n🔑 API配置:", "action")
        self.log("   python config_api.py")
        self.log("\n📁 已有图片:", "action")
        latest = self._get_latest_image()
        if latest:
            self.log(f"   可用图片: {Path(latest).name}")
            self.log("   使用: python master_tool.py --skip-generate")
    
    def convert_to_psd(self, image_path: str) -> Optional[str]:
        """转换为Live2D可用的PSD文件"""
        try:
            from live2d_psd_converter import Live2DPSDConverter
            
            self.log("转换为PSD文件...", "action")
            converter = Live2DPSDConverter()
            psd_path = converter.convert(image_path)
            
            if psd_path:
                self.log(f"PSD文件生成: {Path(psd_path).name}", "success")
                return psd_path
            
        except ImportError:
            self.log("PSD转换器未找到", "error")
        except Exception as e:
            self.log(f"PSD转换失败: {str(e)[:50]}", "error")
        
        return None
    
    def create_psd_plan(self, image_path: str) -> Optional[str]:
        """创建PSD分层规划"""
        try:
            from PIL import Image
            
            img = Image.open(image_path)
            plan_dir = self.output_dir / f"psd_plan_{int(time.time())}"
            plan_dir.mkdir(exist_ok=True)
            img.save(plan_dir / "reference.png")
            
            layers = [
                ("ArtMesh/Body", "身体"),
                ("ArtMesh/Hair_Back", "头发后部"),
                ("ArtMesh/Clothes", "服装"),
                ("ArtMesh/Hair_Side", "头发侧部"),
                ("ArtMesh/Face", "脸部"),
                ("ArtMesh/Eyes", "眼睛"),
                ("ArtMesh/Mouth", "嘴巴"),
                ("ArtMesh/Hair_Front", "头发前部"),
                ("ArtMesh/Hands", "手"),
                ("ArtMesh/Accessories", "配饰")
            ]
            
            with open(plan_dir / "LAYER_GUIDE.txt", 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\nLive2D PSD 分层指南\n" + "=" * 60 + "\n\n")
                f.write(f"图片尺寸: {img.size[0]} x {img.size[1]}\n\n")
                for name, desc in layers:
                    f.write(f"  {name} - {desc}\n")
            
            self.log(f"分层规划: {plan_dir.name}", "success")
            return str(plan_dir)
            
        except Exception as e:
            self.log(f"创建规划失败: {str(e)[:50]}", "error")
            return None
    
    def run(self, prompt: str = None, skip_generate: bool = False):
        """运行完整流程"""
        print("\n" + "=" * 70)
        print("🎨 Live2D Master Agent v3.1")
        print("=" * 70 + "\n")
        
        # 获取图片
        image_path = None
        
        if skip_generate:
            image_path = self._get_latest_image()
            if image_path:
                self.log(f"使用已有图片: {Path(image_path).name}", "info")
            else:
                self.log("output/ 目录中没有图片", "error")
                return
        else:
            if not prompt:
                prompt = input("请输入角色描述: ").strip() or "anime girl, cute, pink hair"
            
            self.log(f"提示词: {prompt[:50]}..." if len(prompt) > 50 else f"提示词: {prompt}", "info")
            image_path = self.generate_image(prompt)
            
        if not image_path:
            return
        
        # 创建PSD规划和转换
        self.create_psd_plan(image_path)
        self.convert_to_psd(image_path)
        
        # 完成提示
        print("\n" + "=" * 70)
        self.log("Live2D角色制作准备完成!", "success")
        print("=" * 70)
        self.log(f"\n生成文件:", "action")
        self.log(f"  📷 {Path(image_path).name}")
        self.log(f"  📋 psd_plan_*/LAYER_GUIDE.txt")
        self.log(f"  🎨 {Path(image_path).stem}_live2d.psd (可直接导入Live2D)")
        self.log("\n下一步:", "action")
        self.log("  1. 查看生成的图片")
        self.log("  2. 直接导入PSD到Live2D Cubism")
        self.log("  3. 查看 docs/RIGGING_GUIDE.md 获取绑定指南")


def main():
    """主函数"""
    tool = Live2DMaster()
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print("""
🎨 Live2D Master Agent v3.1

使用方法:
  python master_tool.py              # 一键生成(默认提示词)
  python master_tool.py "提示词"     # 自定义提示词
  python master_tool.py --skip-generate  # 使用已有图片
  python master_tool.py -h           # 显示帮助
            """)
        elif sys.argv[1] in ['--skip-generate', '-s']:
            tool.run(skip_generate=True)
        else:
            tool.run(prompt=" ".join(sys.argv[1:]))
    else:
        tool.run()


if __name__ == "__main__":
    main()
