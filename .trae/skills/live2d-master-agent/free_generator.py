#!/usr/bin/env python3
"""
Live2D Master Agent - 免费图像生成器
版本: 3.1 (增强网络稳定性)
特点: 完全免费，无需API密钥，开箱即用
支持的免费服务:
1. Pollinations.ai (主服务，完全免费)
2. Hugging Face Inference (免费)
3. 多个备用服务自动切换
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
import socket
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import subprocess


class FreeImageGenerator:
    """完全免费的图像生成器（增强网络稳定性）"""
    
    def __init__(self, max_retries: int = 3, timeout: int = 120):
        self.output_dir = Path.cwd() / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.max_retries = max_retries
        self.timeout = timeout
        
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
    
    def check_network(self) -> Tuple[bool, str]:
        """
        检查网络连接状态
        返回: (是否正常, 状态信息)
        """
        self.print_info("🔍 检查网络连接...")
        
        # 检查 DNS 解析
        try:
            socket.setdefaulttimeout(5)
            socket.gethostbyname("pollinations.ai")
            self.print_info("✅ DNS 解析正常")
        except socket.gaierror as e:
            return False, f"DNS 解析失败: {e}"
        
        # 检查主要服务
        services = [
            ("Pollinations.ai", "https://image.pollinations.ai"),
            ("Hugging Face", "https://api-inference.huggingface.co"),
        ]
        
        for name, url in services:
            try:
                req = urllib.request.Request(url, method='HEAD')
                req.add_header('User-Agent', 'Mozilla/5.0')
                urllib.request.urlopen(req, timeout=5)
                self.print_info(f"✅ {name} 可访问")
                return True, f"{name} 服务正常"
            except Exception as e:
                self.print_info(f"⚠️ {name} 暂时不可用: {str(e)[:50]}")
        
        return False, "所有服务暂时不可用"
    
    def print_header(self):
        print()
        print("=" * 70)
        print("🎨 Live2D Master Agent - 免费图像生成器 (增强网络稳定性)")
        print("=" * 70)
        print()
        print("✨ 完全免费，无需API密钥，开箱即用！")
        print("🔒 包含自动重试和备用服务切换机制")
        print()
    
    def print_success(self, msg: str):
        print(f"✅ {msg}")
    
    def print_error(self, msg: str):
        print(f"❌ {msg}")
    
    def print_info(self, msg: str):
        print(f"ℹ️ {msg}")
    
    def generate_with_pollinations(self, prompt: str, width: int = 768, height: int = 768) -> Optional[str]:
        """
        使用 Pollinations.ai 生成图片
        完全免费，无需注册，无限制
        包含自动重试机制
        """
        self.print_info("🤖 使用 Pollinations.ai 生成图片...")
        self.print_info("💡 提示：如果网络不稳定，会自动重试...")
        
        # 构建提示词
        full_prompt = f"{prompt}, perfect for Live2D rigging, clean layer separation, isolated character on white background, sharp clean lines, vibrant colors, ultra detailed, masterpiece"
        encoded_prompt = urllib.parse.quote(full_prompt)
        
        # Pollinations API URL
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={int(time.time()) % 1000000}"
        
        # 下载图片
        output_path = self.output_dir / f"pollinations_{int(time.time())}.png"
        
        # 添加浏览器请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://pollinations.ai/'
        }
        
        # 重试机制
        for attempt in range(1, self.max_retries + 1):
            try:
                if attempt > 1:
                    self.print_info(f"🔄 第 {attempt} 次尝试 (共 {self.max_retries} 次)...")
                    time.sleep(3)  # 等待 3 秒后重试
                
                self.print_info(f"正在连接服务器... (尝试 {attempt}/{self.max_retries})")
                
                req = urllib.request.Request(url, headers=headers)
                
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    data = response.read()
                    
                    # 检查是否返回了错误信息
                    if len(data) < 1000:  # 通常错误响应很小
                        try:
                            error_json = json.loads(data)
                            if 'error' in error_json:
                                error_msg = error_json.get('message', 'Unknown error')
                                self.print_error(f"⚠️ 服务器返回错误: {error_msg}")
                                if attempt < self.max_retries:
                                    continue  # 继续重试
                                else:
                                    return None
                        except:
                            pass
                    
                    with open(output_path, 'wb') as f:
                        f.write(data)
                    
                    # 验证图片
                    try:
                        from PIL import Image
                        img = Image.open(output_path)
                        img.verify()
                        self.print_success(f"✅ 图片已保存: {output_path}")
                        return str(output_path)
                    except Exception as e:
                        self.print_error(f"⚠️ 生成的图片无效: {e}")
                        if attempt < self.max_retries:
                            continue
                        else:
                            return None
                            
            except urllib.error.HTTPError as e:
                error_msg = e.read().decode('utf-8', errors='ignore')
                self.print_error(f"⚠️ HTTP 错误 {e.code}: {error_msg[:100]}")
                if attempt < self.max_retries:
                    continue
                else:
                    return None
                    
            except (urllib.error.URLError, socket.timeout, ConnectionError) as e:
                self.print_error(f"⚠️ 网络错误: {str(e)[:100]}")
                if attempt < self.max_retries:
                    continue
                else:
                    return None
                    
            except Exception as e:
                self.print_error(f"❌ 生成失败: {str(e)[:100]}")
                if attempt < self.max_retries:
                    continue
                else:
                    return None
        
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
        包含网络状态检查和自动重试
        """
        print()
        self.print_info("🚀 开始生成图片...")
        self.print_info(f"📝 提示词: {prompt[:100]}...")
        print()
        
        # 先检查网络状态
        network_ok, network_msg = self.check_network()
        if not network_ok:
            self.print_error(f"⚠️ 网络连接可能不稳定: {network_msg}")
            self.print_info("💡 继续尝试连接...")
        print()
        
        # 方案1: Pollinations.ai (最可靠)
        result = self.generate_with_pollinations(prompt)
        if result:
            return result
        
        # 方案2: Hugging Face
        print()
        self.print_info("🔄 Pollinations.ai 失败，尝试 Hugging Face...")
        result = self.generate_with_huggingface(prompt, negative_prompt)
        if result:
            return result
        
        # 方案3: Gradio Space
        print()
        self.print_info("🔄 Hugging Face 失败，尝试 Gradio Space...")
        result = self.generate_with_gradio_space(prompt)
        if result:
            return result
        
        self.print_error("❌ 所有免费服务都无法连接")
        
        print()
        print("=" * 70)
        print("💡 备选方案:")
        print("=" * 70)
        print()
        print("🌐 在线生成（无需安装，推荐）:")
        print("   1. https://pollinations.ai - 直接在网页上生成")
        print("   2. https://playground.com - Playground AI")
        print("   3. https://leonardo.ai - Leonardo AI")
        print()
        print("💻 本地生成（最高质量）:")
        print("   python install_comfyui.py")
        print()
        print("🔑 API 配置:")
        print("   python config_api.py")
        print()
        print("📖 查看详细方案: FREE_SOLUTIONS.md")
        print("=" * 70)
        print()
        print("💡 常见问题解决:")
        print("   • 检查网络连接是否正常")
        print("   • 稍后再试，服务可能暂时过载")
        print("   • 使用 VPN 或代理服务器")
        print("   • 尝试直接访问网页版")
        
        return None


def generate_live2d_character(
    character_description: str = "anime girl, cute kawaii style, pink long hair, JK uniform",
    output_dir: Optional[str] = None,
    max_retries: int = 3
) -> Optional[str]:
    """
    生成 Live2D 角色立绘
    完全免费，无需任何配置
    
    参数:
        character_description: 角色描述
        output_dir: 输出目录（可选）
        max_retries: 最大重试次数（默认 3 次）
    
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
    
    # 创建生成器（带重试机制）
    generator = FreeImageGenerator(max_retries=max_retries)
    
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
    print("💡 提示: 网络不稳定时会自动重试最多 3 次")
    print()
    
    character_desc = input("角色描述: ").strip()
    
    if not character_desc:
        character_desc = "anime girl, cute kawaii style, pink long hair, JK uniform"
    
    print()
    print("=" * 70)
    print("🎨 开始生成...")
    print("=" * 70)
    
    # 生成
    result = generate_live2d_character(character_desc, max_retries=3)
    
    print()
    print("=" * 70)
    
    if result:
        generator.print_success("🎉 生成成功！")
        print()
        print(f"📁 图片位置: {result}")
        print()
        print("下一步:")
        print("  1. 📷 查看生成的图片")
        print("  2. 📋 进行 PSD 分层规划")
        print("  3. ✅ 使用 Live2D Master Agent 进行质量检查")
        
        # 添加 ComfyUI 安装提示
        print()
        print("💡 想要更高质量？")
        if check_comfyui_installed():
            print("  🖥️ ComfyUI 已安装，可使用本地最高质量:")
            print("     python comfyui_integration.py")
        else:
            print("  🖥️ 一键安装本地最高质量方案 ComfyUI:")
            print("     python install_comfyui.py")
        print()
        
    else:
        generator.print_error("❌ 生成失败")
        print()
        print("💡 解决方案:")
        print("  🌐 直接访问网页版:")
        print("     1. https://pollinations.ai")
        print("     2. https://playground.com")
        print("     3. https://leonardo.ai")
        print()
        print("  💻 安装本地生成工具:")
        print("     python install_comfyui.py")
        print()
        print("  🔑 配置 API Key:")
        print("     python config_api.py")
        print()
        print("📖 查看详细方案: FREE_SOLUTIONS.md")
        print("=" * 70)
        print()


if __name__ == "__main__":
    main()
