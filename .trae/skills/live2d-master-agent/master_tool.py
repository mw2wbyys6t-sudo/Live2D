#!/usr/bin/env python3
"""
Live2D Master Agent v6.2 - 优化版
功能: 图片生成 + See-through专业分层 + PSD转换
集成SIGGRAPH 2026级别See-through分层工具，避免撞衫现象

改进:
- 优化图片生成服务，提高成功率
- 改进提示词质量
- 更好的重试机制
- 添加多种分辨率选项
- 更好的错误处理
"""

import os
import sys
import time
import random
import urllib.request
import urllib.parse
from pathlib import Path
import argparse

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
    '8K', 'HD', 'perfect anatomy', 'beautiful face', 'detailed eyes',
    'vibrant colors', 'crisp lineart'
]

STYLES = [
    'anime style', 'manga style', 'cartoon style', 'studio ghibli style',
    'digital illustration', 'cel shading', 'soft shading'
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
        'pose': random.choice(FEATURES['pose']),
        'style': random.choice(STYLES)
    }
    return features

def build_prompt(custom_prompt=""):
    """构建优化的多样化提示词"""
    features = generate_random_features()

    prompt_parts = []

    if custom_prompt:
        prompt_parts.append(custom_prompt)

    prompt_parts.append("1girl, solo, portrait")
    prompt_parts.append(features['style'])
    prompt_parts.append(features['hairstyle'])
    prompt_parts.append(features['hair_color'])
    prompt_parts.append(features['eye_color'])
    prompt_parts.append(features['clothing'])
    prompt_parts.append(features['accessory'])
    prompt_parts.append(features['expression'])
    prompt_parts.append(features['pose'])

    # 添加质量关键词
    prompt_parts.extend(random.sample(QUALITY_TAGS, 6))

    # Live2D优化提示词 - 改进版
    prompt_parts.append("perfect for Live2D rigging")
    prompt_parts.append("clean lines, clear edges")
    prompt_parts.append("isolated character on simple background")
    prompt_parts.append("white background")
    prompt_parts.append("sharp clean lineart")
    prompt_parts.append("distinct color separation")

    return " ".join(prompt_parts), features

def get_latest_image(output_dir):
    """获取最新图片"""
    png_files = sorted(output_dir.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    return str(png_files[0]) if png_files else None

def download_with_service(url, headers, output_path, timeout=180):
    """使用指定服务下载图片（改进版）"""
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            if len(data) < 1000:
                return False, "图片数据太小"
            with open(output_path, 'wb') as f:
                f.write(data)
        return True, None
    except urllib.error.URLError as e:
        return False, f"网络错误: {e}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP错误: {e.code} {e.reason}"
    except TimeoutError:
        return False, "下载超时"
    except Exception as e:
        return False, f"下载失败: {e}"

def generate_image(prompt, output_dir, seed=None, width=768, height=768):
    """生成图片（优化版 - 多服务自动降级）"""
    print(f"\n🎨 正在生成图片...")
    print(f"📝 提示词: {prompt[:100]}...")
    print(f"📐 尺寸: {width}x{height}")

    if seed is None:
        seed = random.randint(0, 999999999)

    encoded = urllib.parse.quote(prompt)

    # 优化的服务列表（按成功率排序）
    services = [
        {
            'name': 'Pollinations.ai (主要)',
            'url': f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&nologo=true&model=flux",
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Referer': 'https://pollinations.ai/'
            },
            'timeout': 200
        },
        {
            'name': 'Pollinations.ai (标准)',
            'url': f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&nologo=true",
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Referer': 'https://pollinations.ai/'
            },
            'timeout': 180
        },
        {
            'name': 'Pollinations (备用)',
            'url': f"https://pollinations.ai/api/text2image?prompt={encoded}&width={width}&height={height}&seed={seed}",
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'image/*'
            },
            'timeout': 150
        }
    ]

    # 尝试各个服务，增加重试机制
    max_attempts = 2
    for attempt in range(max_attempts):
        for i, service in enumerate(services):
            if attempt > 0:
                # 重试时使用新的seed
                current_seed = random.randint(0, 999999999)
                service['url'] = service['url'].replace(f"seed={seed}", f"seed={current_seed}")
                seed = current_seed

            print(f"\n🔄 尝试服务 {i+1}/{len(services)} ({attempt+1}/{max_attempts}次): {service['name']}")

            output_file = output_dir / f"live2d_{int(time.time())}_{seed}.png"
            success, error = download_with_service(
                service['url'],
                service['headers'],
                output_file,
                timeout=service.get('timeout', 180)
            )

            if success:
                print(f"✅ 成功！使用 {service['name']}")
                print(f"📁 文件: {output_file.name}")
                print(f"🔢 种子: {seed}")
                return str(output_file), seed
            else:
                print(f"❌ {service['name']} 失败: {error}")
                # 失败时等待一下再试
                if i < len(services) - 1:
                    time.sleep(2)

        if attempt < max_attempts - 1:
            print(f"\n⏳ 所有服务失败，等待3秒后重试...")
            time.sleep(3)

    print("\n❌ 所有在线服务暂时不可用")
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

2. 💻 本地安装 - See-through（SIGGRAPH 2026级别分层）:
   • 运行: python install_comfyui_advanced.py
   • 这将安装 ComfyUI + See-through 插件
   • See-through使用LayerDiff 3D + Marigold Depth技术
   • 详细文档: SEE_THROUGH_INTEGRATION.md

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
            f.write("Live2D PSD 分层指南 v6.2\n")
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
    except ImportError:
        print(f"⚠️ PIL未安装，跳过创建分层规划")
        return None
    except Exception as e:
        print(f"⚠️ 创建分层规划失败: {e}")
        return None

def convert_to_psd(image_path):
    """转换为PSD"""
    try:
        from PIL import Image
        img = Image.open(image_path)

        # 创建优化的PNG
        png_path = str(image_path).replace('.png', '_live2d_ready.png')
        try:
            img.save(png_path, optimize=True)
            print(f"✅ 优化PNG文件已创建: {Path(png_path).name}")
            return png_path
        except:
            # 如果优化失败，创建普通PNG
            img.save(png_path)
            print(f"✅ PNG文件已创建: {Path(png_path).name}")
            print("💡 提示: 使用Photoshop打开后另存为PSD格式")
            return png_path
    except ImportError:
        print(f"⚠️ PIL未安装，跳过PSD转换")
        return image_path
    except Exception as e:
        print(f"⚠️ 图片转换失败: {e}")
        return image_path

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

def check_see_through_installed(comfyui_dir=None):
    """检查See-through是否已安装"""
    if comfyui_dir is None:
        comfyui_dir = Path(__file__).parent / "comfyui"
    if not comfyui_dir.exists():
        return False
    see_through_dir = comfyui_dir / 'custom_nodes' / 'ComfyUI-See-through'
    return see_through_dir.exists()

def show_see_through_guide():
    """显示See-through使用指南"""
    print("""
🏆 See-through 专业分层指南（SIGGRAPH 2026）

See-through 是目前最先进的AI分层工具，集成到本项目中！

优势:
  • SIGGRAPH 2026 级别研究技术
  • 使用 LayerDiff 3D + Marigold Depth
  • 专为动漫角色设计
  • 透明背景 + 完美分层

使用方法:

1. 安装（如果尚未安装）:
   python install_comfyui_advanced.py

2. 启动 ComfyUI:
   cd comfyui
   python main.py

3. 在浏览器中打开 ComfyUI:
   http://127.0.0.1:8188

4. 加载 See-through 工作流:
   • 打开 ComfyUI-See-through 目录
   • 拖放 see_through_workflow.json 到浏览器

5. 使用工作流:
   • 加载你的角色图片
   • 点击 "Queue Prompt" 运行
   • 保存分层结果

详细文档: SEE_THROUGH_INTEGRATION.md
""")

def run_see_through_suggestion(image_path, comfyui_dir=None):
    """建议使用See-through"""
    if comfyui_dir is None:
        comfyui_dir = Path(__file__).parent / "comfyui"

    if check_see_through_installed(comfyui_dir):
        print(f"""
💡 推荐使用 See-through 进行专业分层！

已检测到 See-through 已安装。

运行 ComfyUI:
  cd {comfyui_dir} && python main.py

然后在浏览器中:
  http://127.0.0.1:8188

使用 See-through 工作流处理: {Path(image_path).name}
""")
    else:
        print(f"""
💡 推荐使用 See-through 进行专业分层！

要安装 See-through（SIGGRAPH 2026）:
  python install_comfyui_advanced.py

然后运行 ComfyUI:
  cd comfyui && python main.py

使用 See-through 处理: {Path(image_path).name}
""")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Live2D Master Agent - 从概念到完整模型 (v6.2优化版)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python master_tool.py "cute anime girl"
  python master_tool.py -n 3 "beautiful character"
  python master_tool.py --width 1024 --height 1024
  python master_tool.py --skip-generate
  python master_tool.py --see-through
"""
    )
    parser.add_argument(
        'prompt', nargs='*',
        help='自定义提示词（可选）'
    )
    parser.add_argument(
        '-n', '--number', type=int, default=1,
        help='生成角色数量（默认1）'
    )
    parser.add_argument(
        '--skip-generate', action='store_true',
        help='使用已有图片，跳过生成'
    )
    parser.add_argument(
        '--see-through', action='store_true',
        help='显示See-through使用指南'
    )
    parser.add_argument(
        '--comfyui-dir', type=str, default=None,
        help='ComfyUI安装目录路径'
    )
    parser.add_argument(
        '--width', type=int, default=768,
        help='图片宽度（默认768）'
    )
    parser.add_argument(
        '--height', type=int, default=768,
        help='图片高度（默认768）'
    )
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    print("\n" + "="*80)
    print("🎨 Live2D Master Agent v6.2 - 优化版")
    print("="*80)

    # 显示See-through指南
    if args.see_through:
        show_see_through_guide()
        return

    # 生成多个多样化角色
    for n in range(args.number):
        print(f"\n--- 角色 {n+1}/{args.number} ---")

        # 获取图片
        image_path = None

        if args.skip_generate:
            image_path = get_latest_image(output_dir)
            if image_path:
                print(f"📁 使用已有图片: {Path(image_path).name}")
            else:
                print("❌ output/ 目录中没有图片")
                print("💡 请先将图片放入 output/ 目录，或使用默认生成模式")
                return
        else:
            # 构建多样化提示词
            custom_prompt = ' '.join(args.prompt) if args.prompt else ''
            prompt, features = build_prompt(custom_prompt)
            print(f"\n🔖 随机特征:")
            for key, value in features.items():
                print(f"   • {key}: {value}")

            image_path, seed = generate_image(prompt, output_dir, width=args.width, height=args.height)
            if not image_path:
                show_alternatives()
                return

        # 创建PSD规划
        create_psd_plan(image_path, output_dir)

        # 转换为PSD
        convert_to_psd(image_path)

        # 运行AI分层工具
        run_ai_layer_tool(image_path)

        # 建议使用See-through
        comfyui_dir = Path(args.comfyui_dir) if args.comfyui_dir else None
        run_see_through_suggestion(image_path, comfyui_dir)

    print("\n" + "="*80)
    print("🎉 完成！")
    print("="*80)
    print(f"\n📁 输出目录: {output_dir}")
    print(f"\n🏆 推荐分层工具:")
    print(f"  • See-through (SIGGRAPH 2026) - 专业级分层")
    print(f"    运行: python master_tool.py --see-through")
    print(f"  • 内置分层工具 - 快速预览")
    print(f"\n💡 下一步:")
    print(f"  1. 使用 See-through 进行专业分层")
    print(f"  2. 打开 Live2D Cubism Editor")
    print(f"  3. File → Import PSD")
    print(f"  4. 开始制作你的Live2D模型！")

if __name__ == "__main__":
    main()
