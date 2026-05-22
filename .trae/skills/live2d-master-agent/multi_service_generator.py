#!/usr/bin/env python3
"""
Live2D 图片生成器 - 多服务自动降级版
当主服务不可用时自动切换到备用服务

支持的服务:
1. Pollinations.ai - 主要服务
2. Puter.js - 备用服务1
3. Hugging Face API - 备用服务2
4. Local ComfyUI - 备用服务3（需本地安装）

自动降级机制:
- 尝试服务1 → 失败 → 尝试服务2 → 失败 → 尝试服务3 → 失败 → 提示用户备选方案
"""

import os
import sys
import random
import time
import urllib.request
import urllib.parse
import json
from pathlib import Path

class MultiServiceImageGenerator:
    """多服务图片生成器"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # 服务列表（按优先级排序）
        self.services = [
            {
                'name': 'Pollinations.ai',
                'url': 'https://image.pollinations.ai/prompt/{prompt}?width={width}&height={height}&seed={seed}',
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                    'Referer': 'https://pollinations.ai/'
                },
                'enabled': True
            },
            {
                'name': 'Puter.js',
                'url': 'https://api.puter.com/v1/ai/image/generate',
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Content-Type': 'application/json'
                },
                'enabled': True,
                'method': 'POST',
                'json': True
            },
            {
                'name': 'Hugging Face',
                'url': 'https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell',
                'headers': {
                    'User-Agent': 'Mozilla/5.0',
                    'Authorization': 'Bearer hf_placeholder_token',
                    'Content-Type': 'application/json'
                },
                'enabled': True,
                'method': 'POST',
                'json': True
            }
        ]
        
        # Live2D优化提示词
        self.live2d_optimizations = [
            "perfect for Live2D rigging",
            "clean layer separation",
            "isolated character",
            "white background",
            "sharp clean lines",
            "vibrant colors",
            "ultra detailed",
            "masterpiece",
            "anime style",
            "beautiful face",
            "detailed eyes"
        ]
        
        # 多样化特征库
        self.features = {
            'hairstyle': ['long hair', 'short hair', 'twintails', 'ponytail', 'bob cut', 'curly hair', 'wavy hair'],
            'hair_color': ['pink hair', 'purple hair', 'blue hair', 'blonde hair', 'silver hair', 'black hair', 'brown hair'],
            'eye_color': ['blue eyes', 'green eyes', 'purple eyes', 'golden eyes', 'pink eyes', 'brown eyes'],
            'clothing': ['school uniform', 'dress', 'casual clothes', 'kimono', 'maid outfit', 'sweater'],
            'accessory': ['hair ribbon', 'glasses', 'headband', 'earrings', 'hat'],
            'expression': ['smile', 'cute', 'shy', 'cool', 'happy', 'gentle']
        }
    
    def build_prompt(self, custom_prompt=""):
        """构建多样化提示词"""
        parts = []
        
        if custom_prompt:
            parts.append(custom_prompt)
        
        # 添加随机特征
        for category in self.features:
            parts.append(random.choice(self.features[category]))
        
        # 添加质量和优化关键词
        parts.extend(self.live2d_optimizations)
        
        return " ".join(parts)
    
    def generate_seed(self):
        """生成随机种子"""
        return random.randint(0, 999999999)
    
    def download_with_service(self, service, prompt, width=768, height=768):
        """使用指定服务下载图片"""
        seed = self.generate_seed()
        
        try:
            if service.get('method', 'GET') == 'GET':
                # GET请求
                encoded_prompt = urllib.parse.quote(prompt)
                url = service['url'].format(
                    prompt=encoded_prompt,
                    width=width,
                    height=height,
                    seed=seed
                )
                
                req = urllib.request.Request(url, headers=service['headers'])
                with urllib.request.urlopen(req, timeout=60) as response:
                    data = response.read()
                    if len(data) < 1000:
                        return None, seed, "图片数据太小"
                    return data, seed, None
            
            elif service.get('method') == 'POST':
                # POST请求（JSON）
                if service['name'] == 'Puter.js':
                    payload = json.dumps({
                        "prompt": prompt,
                        "width": width,
                        "height": height
                    })
                else:
                    payload = json.dumps({
                        "inputs": prompt,
                        "parameters": {
                            "width": width,
                            "height": height,
                            "seed": seed
                        }
                    })
                
                req = urllib.request.Request(
                    service['url'],
                    data=payload.encode('utf-8'),
                    headers=service['headers'],
                    method='POST'
                )
                
                with urllib.request.urlopen(req, timeout=60) as response:
                    data = response.read()
                    if service.get('json'):
                        # 处理JSON响应
                        try:
                            result = json.loads(data)
                            if 'image' in result:
                                # Base64编码的图片
                                import base64
                                return base64.b64decode(result['image']), seed, None
                            elif 'url' in result:
                                # 返回图片URL
                                img_url = result['url']
                                img_req = urllib.request.Request(img_url, headers={'User-Agent': service['headers']['User-Agent']})
                                with urllib.request.urlopen(img_req, timeout=30) as img_response:
                                    return img_response.read(), seed, None
                        except:
                            # 可能是直接的图片数据
                            if len(data) > 1000:
                                return data, seed, None
                    return None, seed, "无法解析响应"
            
            return None, seed, "不支持的请求方法"
        
        except Exception as e:
            return None, seed, str(e)
    
    def generate_image(self, custom_prompt=""):
        """生成图片（自动降级）"""
        print("\n" + "="*70)
        print("🎨 多服务图片生成器")
        print("="*70)
        
        # 构建提示词
        prompt = self.build_prompt(custom_prompt)
        print(f"\n📝 提示词: {prompt[:80]}...")
        
        # 尝试各个服务
        for i, service in enumerate(self.services):
            if not service['enabled']:
                continue
            
            print(f"\n🔄 尝试服务 {i+1}/{len(self.services)}: {service['name']}")
            
            data, seed, error = self.download_with_service(service, prompt)
            
            if data:
                # 保存图片
                filename = f"live2d_{int(time.time())}_{service['name'].replace(' ', '_')}.png"
                filepath = self.output_dir / filename
                
                with open(filepath, 'wb') as f:
                    f.write(data)
                
                print(f"✅ 成功! 使用 {service['name']}")
                print(f"📁 文件: {filename}")
                print(f"🔢 种子: {seed}")
                return str(filepath), seed, service['name']
            
            else:
                print(f"❌ {service['name']} 失败: {error}")
        
        # 所有服务都失败
        print("\n" + "="*70)
        print("⚠️  所有在线服务暂时不可用")
        print("="*70)
        return None, None, None
    
    def show_alternatives(self):
        """显示备选方案"""
        print("\n" + "="*70)
        print("💡 备选方案")
        print("="*70)
        print("""
1. 🌐 在线工具:
   • https://pollinations.ai (主要推荐)
   • https://huggingface.co/spaces/black-forest-labs/FLUX.1-schnell
   • https://puter.com/ai/image-generator
   • https://www.playground.com/
   • https://leonardo.ai/
   • https://civitai.com/
        
2. 💻 本地安装:
   • ComfyUI + Stable Diffusion
     运行: python install_comfyui.py
     启动: cd ~/ComfyUI && python main.py
        
3. 📁 使用已有图片:
   将图片放到 output/ 目录后运行:
   python master_tool.py --skip-generate
        
4. 🔑 配置API:
   运行: python config_api.py
   配置火山引擎Seedream API Key
        
5. 📱 移动端:
   • Dream by Wombo
   • MidJourney (Discord)
   • DALL-E (ChatGPT)
        """)

def main():
    """主函数"""
    generator = MultiServiceImageGenerator()
    
    custom_prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    
    filepath, seed, service = generator.generate_image(custom_prompt)
    
    if filepath:
        print("\n🎉 图片生成完成!")
        print(f"📁 文件位置: {filepath}")
        print(f"🔧 使用服务: {service}")
        print(f"🔢 种子: {seed}")
    else:
        generator.show_alternatives()

if __name__ == "__main__":
    main()
