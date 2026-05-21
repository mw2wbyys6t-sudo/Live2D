#!/usr/bin/env python3
"""
Live2D Master Agent - 免费图像生成器
版本: 2.0
特点: 完全免费，无需API密钥，开箱即用
支持的免费服务:
1. Hugging Face Inference (免费)
2. Gradio Spaces (免费)
3. Pollinations.ai (完全免费，无需注册)
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional, Dict, Any
import subprocess


class FreeImageGenerator:
    """完全免费的图像生成器"""
    
    def __init__(self):
        self.output_dir = Path.cwd() / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # 免费服务列表（按优先级排序）
        self.providers = [
            {
                "name": "Pollinations.ai",
                "url": "https://image.pollinations.ai/prompt/{prompt}",
                "description": "完全免费，无需注册，无限制",
                "requires_key": False
            },
            {
                "name": "Hugging Face (AnythingV5)",
                "model": "stablediffusionapi/anything-v5",
                "description": "免费推理，高质量动漫",
                "requires_key": False
            }
        ]
    
    def print_header(self):
        print()
        print("=" * 70)
        print("🎨 Live2D Master Agent - 免费图像生成器")
        print("=" * 70)
        print()
        print("✨ 完全免费，无需API密钥，开箱即用！")
        print()
    
    def print_success(self, msg: str):
        print(f"✅ {msg}")
    
    def print_error(self, msg: str):
        print(f"❌ {msg}")
    
    def print_info(self, msg: str):
        print(f"ℹ️ {msg}")
    
    def generate_with_pollinations(self, prompt: str, width: int = 1024, height: int = 1024) -> Optional[str]:
        """
        使用 Pollinations.ai 生成图片
        完全免费，无需注册，无限制
        """
        self.print_info("使用 Pollinations.ai 生成图片...")
        
        try:
            # 构建URL
            full_prompt = f"{prompt}, {width}x{height}"
            encoded_prompt = urllib.parse.quote(full_prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            
            self.print_info(f"请求URL: {url}")
            self.print_info("正在生成，请稍候...")
            
            # 下载图片
            output_path = self.output_dir / f"pollinations_{int(time.time())}.png"
            
            # 添加请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=120) as response:
                with open(output_path, 'wb') as f:
                    f.write(response.read())
            
            self.print_success(f"图片已保存: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.print_error(f"Pollinations.ai 生成失败: {e}")
            return None
    
    def generate_with_huggingface(self, prompt: str, negative_prompt: str = "") -> Optional[str]:
        """
        使用 Hugging Face 免费推理
        无需API密钥的模型
        """
        self.print_info("使用 Hugging Face 免费推理...")
        
        try:
            # 尝试使用 requests 库
            try:
                import requests
            except ImportError:
                self.print_info("安装 requests 库...")
                subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"])
                import requests
            
            # 使用公开的推理端点
            api_url = "https://api-inference.huggingface.co/models/stablediffusionapi/anything-v5"
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "negative_prompt": negative_prompt,
                    "width": 1024,
                    "height": 1024
                }
            }
            
            self.print_info("发送请求...")
            response = requests.post(api_url, json=payload, timeout=120)
            
            if response.status_code == 200:
                # 保存图片
                output_path = self.output_dir / f"hf_anythingv5_{int(time.time())}.png"
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                self.print_success(f"图片已保存: {output_path}")
                return str(output_path)
            else:
                self.print_error(f"Hugging Face 返回错误: {response.status_code}")
                return None
                
        except Exception as e:
            self.print_error(f"Hugging Face 生成失败: {e}")
            return None
    
    def generate_with_gradio_space(self, prompt: str) -> Optional[str]:
        """
        使用公开的 Gradio Space
        完全免费
        """
        self.print_info("使用 Gradio Space 生成图片...")
        
        try:
            # 尝试使用 gradio_client
            try:
                from gradio_client import Client
            except ImportError:
                self.print_info("安装 gradio_client 库...")
                subprocess.run([sys.executable, "-m", "pip", "install", "gradio_client", "-q"])
                from gradio_client import Client
            
            # 使用公开的 AnythingV5 Space
            self.print_info("连接到 Gradio Space...")
            client = Client("stablediffusionapi/anything-v5")
            
            self.print_info("生成图片...")
            result = client.predict(
                prompt,
                "",  # negative prompt
                fn_index=0
            )
            
            if result and isinstance(result, str):
                # 复制到输出目录
                import shutil
                output_path = self.output_dir / f"gradio_{int(time.time())}.png"
                shutil.copy(result, output_path)
                
                self.print_success(f"图片已保存: {output_path}")
                return str(output_path)
            
            return None
            
        except Exception as e:
            self.print_error(f"Gradio Space 生成失败: {e}")
            return None
    
    def generate(self, prompt: str, negative_prompt: str = "") -> Optional[str]:
        """
        自动尝试所有免费服务
        """
        print()
        self.print_info("开始生成图片...")
        self.print_info(f"提示词: {prompt[:100]}...")
        print()
        
        # 方案1: Pollinations.ai (最可靠)
        result = self.generate_with_pollinations(prompt)
        if result:
            return result
        
        print()
        self.print_info("Pollinations.ai 失败，尝试 Hugging Face...")
        
        # 方案2: Hugging Face
        result = self.generate_with_huggingface(prompt, negative_prompt)
        if result:
            return result
        
        print()
        self.print_info("Hugging Face 失败，尝试 Gradio Space...")
        
        # 方案3: Gradio Space
        result = self.generate_with_gradio_space(prompt)
        if result:
            return result
        
        self.print_error("所有免费服务都失败了")
        return None


def generate_live2d_character(
    character_description: str = "anime girl, cute kawaii style, pink long hair, JK uniform",
    output_dir: Optional[str] = None
) -> Optional[str]:
    """
    生成 Live2D 角色立绘
    完全免费，无需任何配置
    
    参数:
        character_description: 角色描述
        output_dir: 输出目录（可选）
    
    返回:
        生成的图片路径
    """
    # 构建完整提示词
    positive_prompt = f"""
{character_description},
beautiful face, big expressive eyes,
perfect for Live2D rigging, clean layer separation,
isolated character on white background,
sharp clean lines, vibrant colors, ultra detailed,
masterpiece, award-winning quality, professional artwork,
anime art style, high quality render
""".strip().replace('\n', ' ')
    
    negative_prompt = """
blurry, low quality, bad anatomy, bad hands,
multiple characters, complex background,
merged layers, overlapping parts, text, watermark
""".strip().replace('\n', ' ')
    
    # 创建生成器
    generator = FreeImageGenerator()
    
    if output_dir:
        generator.output_dir = Path(output_dir)
        generator.output_dir.mkdir(exist_ok=True)
    
    # 生成图片
    return generator.generate(positive_prompt, negative_prompt)


def check_comfyui_installed() -> bool:
    """检查 ComfyUI 是否已安装"""
    comfyui_dir = Path(__file__).parent / "Live2D-ComfyUI" / "ComfyUI"
    return comfyui_dir.exists()


def main():
    """主函数"""
    generator = FreeImageGenerator()
    generator.print_header()
    
    print("请输入角色描述（留空使用默认）:")
    print("示例: anime girl, pink hair, JK uniform")
    print()
    
    character_desc = input("角色描述: ").strip()
    
    if not character_desc:
        character_desc = "anime girl, cute kawaii style, pink long hair, JK uniform"
    
    print()
    print("=" * 50)
    
    # 生成
    result = generate_live2d_character(character_desc)
    
    print()
    print("=" * 50)
    
    if result:
        generator.print_success("生成成功！")
        print()
        print(f"图片位置: {result}")
        print()
        print("下一步:")
        print("  1. 查看生成的图片")
        print("  2. 进行 PSD 分层规划")
        print("  3. 使用 Live2D Master Agent 进行质量检查")
        
        # 添加 ComfyUI 安装提示
        print()
        print("💡 想要更高质量？")
        if check_comfyui_installed():
            print("  - 🖥️ ComfyUI 已安装，可使用本地最高质量:")
            print("     python comfyui_integration.py")
        else:
            print("  - 🖥️ 一键安装本地最高质量方案 ComfyUI:")
            print("     python install_comfyui.py")
        print()
        
    else:
        generator.print_error("生成失败")
        print()
        print("备选方案:")
        print("  1. 访问 https://playground.com/ 免费生成")
        print("  2. 访问 https://leonardo.ai/ 免费生成")
        print("  3. 手动上传已有图片")
        
        # 添加 ComfyUI 安装提示
        print()
        print("💡 或者一键安装本地最高质量方案:")
        print("     python install_comfyui.py")
        print()


if __name__ == "__main__":
    main()
