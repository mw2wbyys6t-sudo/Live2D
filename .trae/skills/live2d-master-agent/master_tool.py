#!/usr/bin/env python3
"""
Live2D Master Agent v5.0 - 多样化增强版
功能: 图片生成 + PSD转换 + 智能分层
与Live2D分层工具完美兼容，避免撞衫现象
"""

import os
import sys
import time
import random
import urllib.request
import urllib.parse
from pathlib import Path

# 多样化特征库 - 避免撞衫
FEATURES = {
    'hairstyle': [
        'long hair', 'short hair', 'medium hair', 'ponytail', 'twintails',
        'bun', 'drill hair', 'bob cut', 'pixie cut', 'side ponytail',
        'half up', 'messy hair', 'straight hair', 'wavy hair', 'curly hair'
    ],
    'hair_color': [
        'pink hair', 'purple hair', 'blue hair', 'green hair', 'red hair',
        'orange hair', 'blonde hair', 'silver hair', 'white hair', 'black hair',
        'brown hair', 'grey hair', 'gradient hair', 'pastel pink', 'neon green'
    ],
    'eye_color': [
        'blue eyes', 'green eyes', 'brown eyes', 'purple eyes', 'red eyes',
        'golden eyes', 'silver eyes', 'pink eyes', 'amber eyes', 'cyan eyes'
    ],
    'clothing': [
        'school uniform', 'serafuku', 'sailor uniform', 'casual clothes',
        'dress', 'skirt', 'kimono', 'maid outfit', 'punk style', 'gothic',
        'lolita fashion', 'business suit', 'sportswear', 'winter coat'
    ],
    'accessories': [
        'hair ribbon', 'hair bow', 'headband', 'glasses', 'eyepatch', 'hat',
        'earrings', 'necklace', 'bracelet', 'choker', 'scarf', 'gloves'
    ],
    'expression': [
        'smile', 'happy', 'cute', 'gentle', 'shy', 'blushing', 'serious',
        'cool', 'confident', 'playful', 'cheerful', 'sleepy', 'surprised'
    ],
    'pose': [
        'standing', 'sitting', 'waving', 'peace sign', 'hands on hips',
        'arms crossed', 'looking at viewer', 'three quarter view', 'cute pose'
    ]
}

QUALITY_TAGS = [
    'masterpiece', 'best quality', 'ultra detailed', 'high resolution',
    '8K', 'HD', 'perfect anatomy', 'beautiful face', 'detailed eyes'
]

def generate_random_features():
    """生成随机特征组合，避免撞衫"""
    features = {
        'hairstyle': random.choice(FEATURES['hairstyle']),
        'hair_color': random.choice(FEATURES['hair_color']),
        'eye_color': random.choice(FEATURES['eye_color']),
        'clothing': random.choice(FEATURES['clothing']),
        'accessory': random.choice(FEATURES['accessories']),
        'expression': random.choice(FEATURES['expression']),
        'pose': random.choice(FEATURES['pose'])
    }
    return features

def build_prompt(custom_prompt=""):
    """构建多样化提示词"""
    features = generate_random_features()
    
    prompt_parts = []
    
    if custom_prompt:
        prompt_parts.append(custom_prompt)
    
    prompt_parts.append("1girl, solo")
    prompt_parts.append(features['hairstyle'])
    prompt_parts.append(features['hair_color'])
    prompt_parts.append(features['eye_color'])
    prompt_parts.append(features['clothing'])
    prompt_parts.append(features['accessory'])
    prompt_parts.append(features['expression'])
    prompt_parts.append(features['pose'])
    
    # 添加质量关键词
    prompt_parts.extend(random.sample(QUALITY_TAGS, 5))
    
    # Live2D优化提示词
    prompt_parts.append("perfect for Live2D rigging")
    prompt_parts.append("clean layer separation")
    prompt_parts.append("isolated character")
    prompt_parts.append("white background")
    prompt_parts.append("sharp clean lines")
    
    return " ".join(prompt_parts), features

def get_latest_image(output_dir):
    """获取最新图片"""
    png_files = sorted(output_dir.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    return str(png_files[0]) if png_files else None

def download_with_service(url, headers, output_path):
    """使用指定服务下载图片"""
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read()
            if len(data) < 1000:
                return False, "图片数据太小"
            with open(output_path, 'wb') as f:
                f.write(data)
        return True, None
    except Exception as e:
        return False, str(e)

def generate_image(prompt, output_dir, seed=None):
    """生成图片（多服务自动降级）"""
    print(f"\n✅ 正在生成图片...")
    print(f"📝 提示词: {prompt[:80]}...")
    
    if seed is None:
        seed = random.randint(0, 999999999)
    
    encoded = urllib.parse.quote(prompt)
    
    # 服务列表（按优先级排序）
    services = [
        {
            'name': 'Pollinations.ai',
            'url': f"https://image.pollinations.ai/prompt/{encoded}?width=768&height=768&seed={seed}",
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Referer': 'https://pollinations.ai/'
            }
        },
        {
            'name': 'Pollinations (备用)',
            'url': f"https://pollinations.ai/api/text2image?prompt={encoded}&width=768&height=768&seed={seed}",
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'image/*'
            }
        }
    ]
    
    # 尝试各个服务
    for i, service in enumerate(services):
        print(f"\n🔄 尝试服务 {i+1}/{len(services)}: {service['name']}")
        
        output_file = output_dir / f"live2d_{int(time.time())}.png"
        success, error = download_with_service(service['url'], service['headers'], output_file)
        
        if success:
            print(f"✅ 成功! 使用 {service['name']}")
            print(f"📁 文件: {output_file.name}")
            print(f"🔢 种子: {seed}")
            return str(output_file), seed
        else:
            print(f"❌ {service['name']} 失败: {error}")
    
    print("❌ 所有在线服务暂时不可用")
    return None, seed

def show_alternatives():
    """显示备选方案"""
    print("""

💡 备选方案:

1. 🌐 在线工具:
   • https://pollinations.ai (主要推荐)
   • https://huggingface.co/spaces/black-forest-labs/FLUX.1-schnell
   • https://puter.com/ai/image-generator
   • https://www.playground.com/
   • https://leonardo.ai/

2. 💻 本地安装:
   • ComfyUI + Stable Diffusion
     运行: python install_comfyui.py

3. 📁 使用已有图片:
   将图片放到 output/ 目录后运行:
   python master_tool.py --skip-generate

4. 🔑 配置API:
   运行: python config_api.py
   配置火山引擎Seedream API Key
    """)

def create_psd_plan(image_path, output_dir):
    """创建PSD分层规划"""
    try:
        from PIL import Image
        img = Image.open(image_path)
        plan_dir = output_dir / f"psd_plan_{int(time.time())}"
        plan_dir.mkdir(exist_ok=True)
        img.save(plan_dir / "reference.png")
        
        # Live2D标准图层结构
        layers = [
            "Background - 背景",
            "ArtMesh/Body - 身体",
            "ArtMesh/Neck - 脖子",
            "ArtMesh/Clothes - 服装",
            "ArtMesh/Head - 头部",
            "ArtMesh/Face_Base - 脸部基础",
            "ArtMesh/Hair_Back - 头发后部",
            "ArtMesh/Hair_Side_L - 头发左侧",
            "ArtMesh/Hair_Side_R - 头发右侧",
            "ArtMesh/Hair_Front - 头发前部",
            "ArtMesh/Hair_Bangs - 刘海",
            "ArtMesh/Brow_L - 左眉毛",
            "ArtMesh/Brow_R - 右眉毛",
            "ArtMesh/EyeL_White - 左眼白",
            "ArtMesh/EyeL_Iris - 左虹膜",
            "ArtMesh/EyeL_Highlight - 左眼高光",
            "ArtMesh/EyeR_White - 右眼白",
            "ArtMesh/EyeR_Iris - 右虹膜",
            "ArtMesh/EyeR_Highlight - 右眼高光",
            "ArtMesh/Mouth_Outer - 嘴巴外形",
            "ArtMesh/Mouth_A - 口型A",
            "ArtMesh/Mouth_I - 口型I",
            "ArtMesh/Mouth_U - 口型U",
            "ArtMesh/Mouth_E - 口型E",
            "ArtMesh/Mouth_O - 口型O",
            "ArtMesh/Accessories - 配饰"
        ]
        
        with open(plan_dir / "LAYER_GUIDE.txt", 'w', encoding='utf-8') as f:
            f.write("Live2D PSD 分层指南 v5.0\n")
            f.write("="*50 + "\n")
            f.write(f"图片尺寸: {img.size[0]} x {img.size[1]}\n")
            f.write(f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("图层顺序（从后到前）:\n")
            f.write("-"*50 + "\n")
            for i, layer in enumerate(layers, 1):
                f.write(f"{i:2d}. {layer}\n")
            f.write("\n导入Live2D Cubism Editor步骤:\n")
            f.write("1. File → Import PSD\n")
            f.write("2. 勾选 Create ArtMeshes\n")
            f.write("3. 点击 OK\n")
            f.write("4. 创建部件并设置参数\n")
        
        print(f"✅ 分层规划已创建")
        return str(plan_dir)
    except Exception as e:
        print(f"⚠️ 创建分层规划失败: {e}")
        return None

def convert_to_psd(image_path):
    """转换为PSD"""
    try:
        from PIL import Image
        img = Image.open(image_path)
        
        # 尝试PSD导出
        psd_path = str(image_path).replace('.png', '_live2d.psd')
        try:
            img.save(psd_path)
            print(f"✅ PSD文件已创建: {Path(psd_path).name}")
            return psd_path
        except:
            # 如果PSD失败，创建优化后的PNG
            png_path = str(image_path).replace('.png', '_live2d_ready.png')
            img.save(png_path)
            print(f"✅ PNG文件已创建: {Path(png_path).name}")
            print("💡 提示: 使用Photoshop打开后另存为PSD格式")
            return png_path
    except Exception as e:
        print(f"⚠️ PSD转换失败: {e}")
        return None

def run_ai_layer_tool(image_path):
    """运行AI分层工具"""
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, 'live2d_layer_pro.py', image_path],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print("✅ AI智能分层完成")
            return True
        else:
            print(f"⚠️ AI分层工具运行失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"⚠️ 无法运行AI分层工具: {e}")
        return False

def main():
    """主函数"""
    base_dir = Path(__file__).parent
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)
    
    print("\n" + "=" * 70)
    print("🎨 Live2D Master Agent v5.0 - 多样化增强版")
    print("=" * 70)
    
    # 参数处理
    skip_generate = False
    custom_prompt = ""
    count = 1
    
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        i = 0
        while i < len(args):
            if args[i] == '--skip-generate':
                skip_generate = True
            elif args[i] == '-n':
                i += 1
                count = int(args[i])
            elif args[i] in ['-h', '--help']:
                print("""
使用方法:
  python master_tool.py                    # 默认生成1个随机角色
  python master_tool.py "提示词"           # 自定义提示词
  python master_tool.py -n 5              # 生成5个多样化角色
  python master_tool.py --skip-generate    # 使用已有图片

特性:
  • 多样化特征组合（避免撞衫）
  • 随机种子生成
  • 与Live2D分层工具完美兼容
  • 标准图层命名规范
                """)
                return
            else:
                custom_prompt = " ".join(args[i:])
                break
            i += 1
    
    # 生成多个多样化角色
    for n in range(count):
        print(f"\n--- 角色 {n+1}/{count} ---")
        
        # 获取图片
        image_path = None
        
        if skip_generate:
            image_path = get_latest_image(output_dir)
            if image_path:
                print(f"📁 使用已有图片: {Path(image_path).name}")
            else:
                print("❌ output/ 目录中没有图片")
                return
        else:
            # 构建多样化提示词
            prompt, features = build_prompt(custom_prompt)
            print(f"\n🔖 随机特征:")
            for key, value in features.items():
                print(f"   • {key}: {value}")
            
            image_path, seed = generate_image(prompt, output_dir)
            if not image_path:
                show_alternatives()
                return
        
        # 创建PSD规划
        create_psd_plan(image_path, output_dir)
        
        # 转换为PSD
        convert_to_psd(image_path)
        
        # 运行AI分层工具
        run_ai_layer_tool(image_path)
    
    print("\n" + "=" * 70)
    print("🎉 完成!")
    print("=" * 70)
    print("\n📁 输出文件:")
    print("  • live2d_*.png (原始图片)")
    print("  • live2d_*_live2d.psd (PSD文件)")
    print("  • live2d_*_live2d_pro/ (AI分层结果)")
    print("  • psd_plan_*/ (分层规划指南)")
    print("\n💡 下一步:")
    print("  1. 打开Live2D Cubism Editor")
    print("  2. File → Import PSD")
    print("  3. 开始制作你的Live2D模型!")

if __name__ == "__main__":
    main()
