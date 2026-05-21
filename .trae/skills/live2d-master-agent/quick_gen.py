#!/usr/bin/env python3
"""
Live2D Master Agent - 一键生成工具
版本: 3.1
特点: 完全免费，无需配置，一行命令生成图片
提示: 如需更高质量，可运行 python config_api.py 配置 API Key
"""

import sys
import urllib.request
import urllib.parse
import time
from pathlib import Path

def check_api_config() -> bool:
    """检查是否已配置 API Key"""
    try:
        from config import config
        return config.has_api_key
    except:
        return False


def check_comfyui_installed() -> bool:
    """检查 ComfyUI 是否已安装"""
    comfyui_dir = Path(__file__).parent / "Live2D-ComfyUI" / "ComfyUI"
    return comfyui_dir.exists()


def print_tips():
    """打印使用提示"""
    print()
    print("💡 提示:")
    print("  - 免费方案（当前使用）: Pollinations.ai")
    
    if check_api_config():
        print("  - 🔑 已配置 API Key，可使用更高质量的 Seedream:")
        print("     python scripts/seedream_image_generate.py --prompt \"描述\"")
    else:
        print("  - 想要更高质量？配置 API Key:")
        print("     python config_api.py")
    
    if check_comfyui_installed():
        print("  - 🖥️ ComfyUI 已安装，可使用本地最高质量:")
        print("     python comfyui_integration.py")
    else:
        print("  - 🖥️ 想要本地最高质量？一键安装 ComfyUI:")
        print("     python install_comfyui.py")
    
    print()


def try_pollinations(prompt: str, output_path: Path) -> str:
    """尝试使用 Pollinations.ai"""
    try:
        print("🤖 尝试 Pollinations.ai...")
        full_prompt = f"{prompt}, perfect for Live2D rigging, clean layer separation, isolated character on white background, sharp clean lines, vibrant colors, ultra detailed, masterpiece"
        encoded = urllib.parse.quote(full_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}"
        
        output_file = output_path / f"live2d_pollinations_{int(time.time())}.png"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/png,image/*;q=0.8',
            'Referer': 'https://pollinations.ai/'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=60) as response:
            with open(output_file, 'wb') as f:
                f.write(response.read())
        
        print("✅ Pollinations.ai 成功!")
        return str(output_file)
    except Exception as e:
        print(f"❌ Pollinations.ai 失败: {str(e)}")
        return None


def try_waifu_diffusion(prompt: str, output_path: Path) -> str:
    """尝试使用 Waifu Diffusion"""
    try:
        print("🤖 尝试 Waifu Diffusion (HuggingFace)...")
        import json
        import http.client
        
        conn = http.client.HTTPSConnection("api-inference.huggingface.co")
        data = json.dumps({
            "inputs": prompt,
            "parameters": {
                "width": 768,
                "height": 1024,
                "num_inference_steps": 20
            }
        })
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
        
        output_file = output_path / f"live2d_waifu_{int(time.time())}.png"
        
        conn.request("POST", "/models/cagliostrolab/animagine-xl-3.1", data, headers)
        res = conn.getresponse()
        
        if res.status == 200:
            with open(output_file, 'wb') as f:
                f.write(res.read())
            print("✅ Waifu Diffusion 成功!")
            return str(output_file)
    except Exception as e:
        print(f"❌ Waifu Diffusion 失败: {str(e)}")
    
    return None


def generate(prompt: str, output_dir: str = "./output") -> str:
    """
    一键生成图片 - 多服务自动切换
    
    参数:
        prompt: 角色描述
        output_dir: 输出目录
    
    返回:
        图片路径
    """
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print("🎨 开始生成...")
    
    # 按顺序尝试各个服务
    result = try_pollinations(prompt, output_path)
    if result:
        print(f"✅ 完成: {result}")
        print_tips()
        return result
    
    result = try_waifu_diffusion(prompt, output_path)
    if result:
        print(f"✅ 完成: {result}")
        print_tips()
        return result
    
    # 如果所有服务都失败，提示用户
    print()
    print("⚠️ 所有免费服务暂时不可用")
    print()
    print("💡 备选方案:")
    print("  1. 🌐 直接访问网页版:")
    print("     - https://pollinations.ai (推荐)")
    print("     - https://huggingface.co/spaces")
    print("     - https://civitai.com")
    print()
    print("  2. 💻 安装本地生成工具:")
    print("     python local_generator.py")
    print()
    print("  3. 🖥️ 使用 ComfyUI:")
    if check_comfyui_installed():
        print("     python comfyui_integration.py")
    else:
        print("     python install_comfyui.py")
    print()
    print("  4. 🔑 配置 API Key:")
    print("     python config_api.py")
    print()
    print("📖 查看详细解决方案: FREE_SOLUTIONS.md")
    
    raise Exception("所有免费服务暂时不可用，请尝试备选方案")


# 命令行使用
if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "anime girl, pink hair, JK uniform"
    
    generate(prompt)
