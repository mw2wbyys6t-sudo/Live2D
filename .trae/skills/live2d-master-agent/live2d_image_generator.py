#!/usr/bin/env python3
"""
Live2D图片生成工具 v3.0 - 多样化增强版
确保生成的图片与Live2D分层工具兼容，同时避免撞衫现象

核心特性:
1. 多样化提示词模板系统
2. 随机种子生成（确保每次生成不同）
3. 丰富的角色特征组合（发型、发色、服装、配饰）
4. 与Live2D分层工具完美兼容
5. 避免千篇一律的生成结果
"""

import os
import sys
import random
import urllib.parse
import requests
from pathlib import Path
from datetime import datetime

class Live2DImageGenerator:
    """Live2D图片生成工具 - 多样化增强版"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # Live2D标准尺寸
        self.LIVE2D_SIZE = 768
        
        # 多样化特征库 - 避免撞衫
        self.FEATURES = {
            # 脸型
            'face_shape': [
                'oval face', 'round face', 'square face', 'heart shaped face', 
                'long face', 'diamond face', 'pear face'
            ],
            
            # 发型
            'hairstyle': [
                'long hair', 'short hair', 'medium hair', 'ponytail', 'twintails',
                'bun', 'ponytail', 'drill hair', 'bob cut', 'pixie cut',
                'side ponytail', 'half up', 'messy hair', 'straight hair',
                'wavy hair', 'curly hair', 'spiky hair', 'asymmetrical hair'
            ],
            
            # 发色
            'hair_color': [
                'pink hair', 'purple hair', 'blue hair', 'green hair', 'red hair',
                'orange hair', 'blonde hair', 'silver hair', 'white hair',
                'black hair', 'brown hair', 'grey hair', 'gradient hair',
                'two tone hair', 'dyed hair', 'pastel pink', 'neon green'
            ],
            
            # 眼睛颜色
            'eye_color': [
                'blue eyes', 'green eyes', 'brown eyes', 'purple eyes', 'red eyes',
                'golden eyes', 'silver eyes', 'pink eyes', 'amber eyes',
                'hazel eyes', 'cyan eyes', 'magenta eyes', 'heterochromia'
            ],
            
            # 服装风格
            'clothing': [
                'school uniform', 'serafuku', 'sailor uniform', 'gym uniform',
                'casual clothes', 't-shirt and jeans', 'hoodie', 'sweater',
                'dress', 'skirt', 'kimono', 'yukata', 'maid outfit',
                'cosplay', 'punk style', 'gothic', 'lolita fashion',
                'business suit', 'sportswear', 'swimsuit', 'winter coat'
            ],
            
            # 配饰
            'accessories': [
                'hair ribbon', 'hair bow', 'headband', 'hair clips', 'hairpin',
                'glasses', 'eyepatch', 'hat', 'beret', 'cap',
                'earrings', 'necklace', 'bracelet', 'choker',
                'scarf', 'bags', 'gloves', 'stockings', 'leg warmers'
            ],
            
            # 表情
            'expression': [
                'smile', 'happy', 'cute', 'gentle', 'shy', 'blushing',
                'serious', 'cool', 'confident', 'playful', 'cheerful',
                'sleepy', 'surprised', 'curious', 'determined', 'dreamy'
            ],
            
            # 姿势
            'pose': [
                'standing', 'sitting', 'leaning', 'waving', 'peace sign',
                'hands on hips', 'arms crossed', 'holding something',
                'looking at viewer', 'profile view', 'three quarter view',
                'dynamic pose', 'relaxed pose', 'cute pose', 'elegant pose'
            ],
            
            # 背景
            'background': [
                'white background', 'simple background', 'solid color background',
                'gradient background', 'studio background', 'transparent background'
            ],
            
            # 风格
            'style': [
                'anime style', 'manga style', 'kawaii', 'moé style',
                'digital painting', 'illustration', 'clean line art',
                'soft colors', 'vibrant colors', 'pastel colors'
            ]
        }
        
        # 质量关键词
        self.QUALITY_TAGS = [
            'masterpiece', 'best quality', 'ultra detailed', 'high resolution',
            '8K', 'HD', 'professional', 'studio quality', 'perfect anatomy',
            'beautiful face', 'detailed eyes', 'clean linework', 'smooth shading'
        ]
        
        # 负面提示词
        self.NEGATIVE_TAGS = [
            'lowres', 'bad anatomy', 'bad hands', 'text', 'error',
            'missing fingers', 'extra digit', 'fewer digits', 'cropped',
            'worst quality', 'low quality', 'normal quality', 'jpeg artifacts',
            'signature', 'watermark', 'username', 'blurry', 'out of focus',
            'deformed', 'ugly', 'disfigured', 'mutated'
        ]
    
    def generate_random_seed(self):
        """生成随机种子（确保每次不同）"""
        return random.randint(0, 999999999)
    
    def generate_random_features(self, custom_prompt=""):
        """随机选择特征组合，避免撞衫"""
        features = {
            'hairstyle': random.choice(self.FEATURES['hairstyle']),
            'hair_color': random.choice(self.FEATURES['hair_color']),
            'eye_color': random.choice(self.FEATURES['eye_color']),
            'clothing': random.choice(self.FEATURES['clothing']),
            'accessory': random.choice(self.FEATURES['accessories']),
            'expression': random.choice(self.FEATURES['expression']),
            'pose': random.choice(self.FEATURES['pose']),
            'style': random.choice(self.FEATURES['style'])
        }
        
        # 构建提示词
        prompt_parts = []
        
        # 添加自定义提示词
        if custom_prompt:
            prompt_parts.append(custom_prompt)
        
        # 添加角色描述
        prompt_parts.append("1girl, solo")
        prompt_parts.append(features['hairstyle'])
        prompt_parts.append(features['hair_color'])
        prompt_parts.append(features['eye_color'])
        prompt_parts.append(features['clothing'])
        prompt_parts.append(features['accessory'])
        prompt_parts.append(features['expression'])
        prompt_parts.append(features['pose'])
        prompt_parts.append(features['style'])
        
        # 添加质量关键词（随机选择部分）
        quality_tags = random.sample(self.QUALITY_TAGS, 6)
        prompt_parts.extend(quality_tags)
        
        # 添加Live2D优化提示词
        prompt_parts.append("perfect for Live2D rigging")
        prompt_parts.append("clean layer separation")
        prompt_parts.append("isolated character")
        prompt_parts.append("sharp clean lines")
        prompt_parts.append("vibrant colors")
        
        return " ".join(prompt_parts), features
    
    def generate_with_pollinations(self, prompt, seed=None):
        """使用Pollinations.ai生成图片"""
        try:
            # 添加随机种子
            if seed is None:
                seed = self.generate_random_seed()
            
            # 构建完整提示词
            full_prompt = f"{prompt}, seed:{seed}"
            
            # URL编码
            encoded = urllib.parse.quote(full_prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded}"
            
            # 设置请求头（避免403错误）
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/png,image/*;q=0.8',
                'Referer': 'https://pollinations.ai/'
            }
            
            print(f"🎨 正在生成图片...")
            print(f"📝 提示词: {full_prompt[:100]}...")
            
            # 请求图片
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
            
            # 保存图片
            timestamp = int(datetime.now().timestamp())
            filename = f"live2d_{timestamp}.png"
            filepath = self.output_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ 图片生成完成: {filename}")
            return filepath, seed
            
        except Exception as e:
            print(f"❌ 生成失败: {e}")
            return None, seed
    
    def generate_diverse_characters(self, count=3, custom_prompt=""):
        """生成多个多样化角色"""
        results = []
        
        print("\n" + "="*80)
        print("🎨 Live2D图片生成工具 - 多样化模式")
        print("="*80)
        print(f"\n📦 正在生成 {count} 个多样化角色...")
        
        for i in range(count):
            print(f"\n--- 角色 {i+1}/{count} ---")
            
            # 生成随机特征
            prompt, features = self.generate_random_seed(custom_prompt)
            
            # 生成图片
            filepath, seed = self.generate_with_pollinations(prompt)
            
            if filepath:
                results.append({
                    'filepath': filepath,
                    'seed': seed,
                    'features': features,
                    'prompt': prompt
                })
                
                # 显示特征信息
                print(f"🔖 特征:")
                for key, value in features.items():
                    print(f"   • {key}: {value}")
        
        print("\n" + "="*80)
        print(f"✅ 完成! 生成了 {len(results)} 个角色")
        print("="*80)
        
        return results
    
    def generate_single_character(self, custom_prompt="", seed=None):
        """生成单个角色"""
        print("\n" + "="*80)
        print("🎨 Live2D图片生成工具")
        print("="*80)
        
        # 生成随机特征
        prompt, features = self.generate_random_features(custom_prompt)
        
        # 添加自定义提示词
        if custom_prompt:
            prompt = f"{custom_prompt}, {prompt}"
        
        # 生成图片
        filepath, seed = self.generate_with_pollinations(prompt, seed)
        
        if filepath:
            print("\n📋 生成信息:")
            print(f"   种子: {seed}")
            print(f"   特征: {features}")
            print(f"   尺寸: {self.LIVE2D_SIZE}x{self.LIVE2D_SIZE}")
            print(f"   输出: {filepath}")
        
        print("\n" + "="*80)
        
        return {
            'filepath': filepath,
            'seed': seed,
            'features': features,
            'prompt': prompt
        }

def main():
    """主函数"""
    generator = Live2DImageGenerator()
    
    if len(sys.argv) < 2:
        print("\n📖 使用方法:")
        print("  python live2d_image_generator.py [选项] [提示词]")
        print()
        print("选项:")
        print("  -n, --count N    生成N个多样化角色（默认1）")
        print("  -s, --seed N     使用指定种子")
        print("  -d, --diverse    启用多样化模式")
        print()
        print("示例:")
        print("  python live2d_image_generator.py \"anime girl\"")
        print("  python live2d_image_generator.py -n 5 \"cute girl\"")
        print("  python live2d_image_generator.py -s 12345 \"pink hair girl\"")
        return
    
    # 解析参数
    import argparse
    parser = argparse.ArgumentParser(description='Live2D图片生成工具')
    parser.add_argument('prompt', nargs='?', default='', help='自定义提示词')
    parser.add_argument('-n', '--count', type=int, default=1, help='生成数量')
    parser.add_argument('-s', '--seed', type=int, default=None, help='随机种子')
    parser.add_argument('-d', '--diverse', action='store_true', help='多样化模式')
    
    args = parser.parse_args()
    
    if args.count > 1 or args.diverse:
        # 多样化模式
        results = generator.generate_diverse_characters(args.count, args.prompt)
        
        # 显示结果
        print("\n📊 生成结果:")
        for i, result in enumerate(results):
            print(f"\n{i+1}. {result['filepath'].name}")
            print(f"   种子: {result['seed']}")
            print(f"   发色: {result['features'].get('hair_color')}")
            print(f"   服装: {result['features'].get('clothing')}")
    
    else:
        # 单一生成
        result = generator.generate_single_character(args.prompt, args.seed)
        
        if result['filepath']:
            print(f"\n🎉 完成!")
            print(f"📁 文件: {result['filepath']}")
            print(f"🔢 种子: {result['seed']}")
            print(f"🎨 特征: {result['features']}")

if __name__ == "__main__":
    main()
