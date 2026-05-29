#!/usr/bin/env python3
"""
Live2D Master Agent v6.3 - SD WebUI 集成版
功能: 多源图片生成 + See-through专业分层 + PSD转换

集成：
- 🔴 Stable Diffusion WebUI (推荐，最高质量)
- 🟡 Pollinations.ai (备用，无网络依赖)
- 🟢 See-through (SIGGRAPH 2026分层技术)

改进:
- 多源智能选择（SD WebUI > Pollinations）
- Live2D优化提示词
- 更好的错误处理
"""

import os
import sys
import time
import random
import re
import urllib.request
import urllib.parse
from pathlib import Path
import argparse

# 尝试导入 SD WebUI 集成
try:
    from sd_webui_integration import (
        StableDiffusionWebUIClient,
        optimize_prompt_for_live2d
    )
    HAS_SD_WEBUI = True
except ImportError:
    HAS_SD_WEBUI = False
    print("⚠️ SD WebUI 集成模块不可用")

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

# Live2D 优化的发型 - 避免过于复杂的卷发
LIVE2D_HAIRSTYLES = [
    'straight hair', 'long straight hair', 'short straight hair',
    'medium hair', 'ponytail', 'twintails', 'side ponytail',
    'bob cut', 'hime cut', 'bangs', 'blunt bangs'
]

# Live2D 优化的姿势 - 确保完整身体可见
LIVE2D_POSES = [
    'standing', 'full body', 'looking at viewer',
    'arms at sides', 'straight-on view'
]

# 高质量动漫风格提示词模板（匹配参考图质量）
HIGH_QUALITY_PROMPT_TEMPLATE = """masterpiece, best quality, ultra detailed, highres, 8k uhd,
anime style, illustration, pixiv, artstation,
1girl, solo, {hairstyle}, {hair_color}, {eye_color}, {clothing}, {accessory}, {expression},
beautiful detailed face, beautiful detailed eyes, detailed skin texture, soft lighting,
pastel colors, soft color palette, dreamy atmosphere, ethereal,
frills, lace, ribbons, bows, jewelry, elegant outfit,
idol costume, stage dress, sparkling, glitter,
perfect anatomy, correct proportions, delicate hands,
white background, simple background, clean background"""

# Live2D 专用提示词模板（在高质量基础上添加 Live2D 优化）
LIVE2D_PROMPT_TEMPLATE = """masterpiece, best quality, ultra detailed, highres,
anime style, illustration, 1girl, solo, full body, standing, looking at viewer,
{hairstyle}, {hair_color}, {eye_color}, {clothing}, {accessory}, {expression},
beautiful detailed face, beautiful detailed eyes, detailed skin texture, soft lighting,
perfect for Live2D rigging, clean lineart, clear edges, sharp outlines,
flat colors, minimal shading, cel shading, distinct color separation,
simple background, white background, isolated character,
clear silhouette, symmetrical eyes, simple hair strands,
visible neck and shoulders, visible arms and hands, visible legs and feet,
closed mouth, neutral expression, front view, straight-on view,
perfect anatomy, correct proportions, delicate hands"""

# 高质量反向提示词
HIGH_QUALITY_NEGATIVE_PROMPT = """lowres, bad anatomy, bad hands, text, error, missing fingers,
extra digit, fewer digits, cropped, worst quality, low quality,
normal quality, jpeg artifacts, signature, watermark, username, blurry,
artist name, bad proportions, extra limbs, cloned face, disfigured,
gross proportions, malformed limbs, missing arms, missing legs,
extra arms, extra legs, fused fingers, too many fingers, long neck,
photorealistic, realistic, 3d, western, sketch, rough, draft"""

# Live2D 反向提示词
LIVE2D_NEGATIVE_PROMPT = """blurry, low quality, low resolution, pixelated, noisy, grainy,
distorted, deformed, bad anatomy, bad hands, bad face, bad eyes,
extra fingers, missing fingers, fused fingers, too many fingers,
bad proportions, extra limbs, long neck, bad feet, bad ears,
ugly, disgusting, horror, watermark, text, signature, logo,
complex background, messy hair, messy clothes,
photorealistic, realistic, 3d, ugly eyes, deformed eyes, closed eyes,
depth of field, blurry background, multiple girls, multiple people,
profile view, side view, back view, turned away,
open mouth, talking, shouting, laughing, crying,
dynamic pose, action pose, jumping, running, sitting, lying down,
partial body, cropped, off-screen, out of frame"""


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


def build_prompt(custom_prompt="", live2d_optimized=True, high_quality=True):
    """构建优化的多样化提示词
    
    Args:
        custom_prompt: 用户自定义提示词
        live2d_optimized: 是否使用 Live2D 优化模式
        high_quality: 是否使用高质量提示词（参考图风格）
    """
    features = generate_random_features()

    if live2d_optimized:
        # 使用 Live2D 专用模板（包含高质量关键词）
        hairstyle = random.choice(LIVE2D_HAIRSTYLES)
        prompt = LIVE2D_PROMPT_TEMPLATE.format(
            hairstyle=hairstyle,
            hair_color=features['hair_color'],
            eye_color=features['eye_color'],
            clothing=features['clothing'],
            accessory=features['accessory'],
            expression=features['expression']
        )
        # 清理多余空白
        prompt = ' '.join(prompt.split())
        return prompt, features
    elif high_quality:
        # 高质量模式（匹配参考图风格）
        prompt = HIGH_QUALITY_PROMPT_TEMPLATE.format(
            hairstyle=features['hairstyle'],
            hair_color=features['hair_color'],
            eye_color=features['eye_color'],
            clothing=features['clothing'],
            accessory=features['accessory'],
            expression=features['expression']
        )
        # 添加用户自定义提示词
        if custom_prompt:
            prompt = custom_prompt + ", " + prompt
        prompt = ' '.join(prompt.split())
        return prompt, features
    else:
        # 自由模式
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
        prompt_parts.extend(random.sample(QUALITY_TAGS, 6))
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


def generate_image_pollinations(prompt, output_dir, seed=None, width=768, height=768):
    """使用 Pollinations.ai 生成图片（降级方案）"""
    print("\n📡 使用 Pollinations.ai (降级方案)...")

    if seed is None:
        seed = random.randint(0, 999999999)

    encoded = urllib.parse.quote(prompt)

    services = [
        {
            'name': 'Pollinations.ai (主要)',
            'url': f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&nologo=true&model=flux",
            'timeout': 200
        },
        {
            'name': 'Pollinations.ai (标准)',
            'url': f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&nologo=true",
            'timeout': 180
        }
    ]

    max_attempts = 2
    for attempt in range(max_attempts):
        for service in services:
            if attempt > 0:
                current_seed = random.randint(0, 999999999)
                service['url'] = service['url'].replace(f"seed={seed}", f"seed={current_seed}")
                seed = current_seed

            print(f"\n🔄 尝试 {service['name']} ({attempt+1}/{max_attempts})")

            output_file = output_dir / f"live2d_poll_{int(time.time())}_{seed}.png"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
            }

            success, error = download_with_service(
                service['url'], headers, output_file, timeout=service['timeout']
            )

            if success:
                print(f"✅ 成功！使用 {service['name']}")
                print(f"📁 文件: {output_file.name}")
                print(f"🔢 种子: {seed}")
                return str(output_file), seed
            else:
                print(f"❌ {service['name']} 失败: {error}")

        if attempt < max_attempts - 1:
            print("\n⏳ 等待3秒后重试...")
            time.sleep(3)

    return None, seed


def generate_image_local(prompt, output_dir, seed=None, width=512, height=768, steps=25):
    """
    使用本地 Stable Diffusion 生成图片（自研工具）
    """
    print("\n🎯 尝试本地 Stable Diffusion 生成...")

    try:
        from local_image_generator import LocalImageGenerator, get_default_negative_prompt

        generator = LocalImageGenerator()
        success, output_path = generator.generate(
            prompt=prompt,
            negative_prompt=get_default_negative_prompt(),
            width=width,
            height=height,
            steps=steps,
            seed=seed,
        )

        if success and output_path:
            print("\n✅ 成功！使用本地 Stable Diffusion")
            return output_path, seed or int(time.time()) % 1000000

    except ImportError:
        print("⚠️ 本地生成器未安装，跳过...")
    except Exception as e:
        print(f"⚠️ 本地生成失败: {e}")

    return None, seed


def generate_image(prompt, output_dir, seed=None, width=768, height=768, sd_webui_url=None, use_local=False):
    """
    生成图片（多源智能选择）
    优先级：本地 SD > SD WebUI API > Pollinations
    """
    print(f"\n🎨 正在生成图片...")
    print(f"📝 提示词: {prompt[:100]}...")
    print(f"📐 尺寸: {width}x{height}")

    if seed is None:
        seed = random.randint(0, 999999999)

    # 源1：本地 Stable Diffusion（自研工具）
    if use_local:
        result, seed = generate_image_local(prompt, output_dir, seed, width, height)
        if result:
            return result, seed

    # 源2：Stable Diffusion WebUI API
    if HAS_SD_WEBUI:
        print("\n🔴 尝试 Stable Diffusion WebUI (本地API)...")
        sd_url = sd_webui_url or "http://127.0.0.1:7860"
        sd_client = StableDiffusionWebUIClient(sd_url)

        if sd_client.is_available():
            optimized_prompt = optimize_prompt_for_live2d(prompt)
            result = sd_client.generate_image(
                optimized_prompt,
                width=width,
                height=height,
                seed=seed,
                steps=30
            )

            if result["status"] == "success":
                output_file = output_dir / f"live2d_sd_{int(time.time())}_{seed}.png"
                if sd_client.save_image_from_base64(result["images"][0], output_file):
                    print("\n✅ 成功！使用 Stable Diffusion WebUI")
                    return str(output_file), seed
            else:
                print(f"⚠️ SD WebUI 生成失败: {result.get('message', 'Unknown error')}")

    # 源3：降级到 Pollinations.ai
    print("\n📡 降级到 Pollinations.ai...")
    return generate_image_pollinations(prompt, output_dir, seed, width, height)


def show_alternatives():
    """显示备选方案"""
    print("""
💡 备选方案:

1. 🟢 Stable Diffusion WebUI (推荐，最高质量):
   • 本地部署，完全免费
   • 支持海量模型和扩展
   • 一键启动: python launch.py --api --listen
   • 地址: https://github.com/AUTOMATIC1111/stable-diffusion-webui

2. 🌐 在线工具:
   • https://pollinations.ai (主要推荐)
   • https://huggingface.co/spaces/black-forest-labs/FLUX.1-schnell
   • https://puter.com/ai/image-generator

3. 💻 See-through 专业分层（SIGGRAPH 2026）:
   • 运行: python install_comfyui_advanced.py
   • 详细文档: SEE_THROUGH_INTEGRATION.md

4. 📁 使用已有图片:
   将图片放到 output/ 目录后运行:
   python master_tool.py --skip-generate
""")


def create_psd_plan(image_path, output_dir):
    """创建PSD分层规划"""
    try:
        from PIL import Image
        img = Image.open(image_path)
        plan_dir = output_dir / f"psd_plan_{int(time.time())}"
        plan_dir.mkdir(exist_ok=True)
        img.save(plan_dir / "reference.png")

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
            f.write("Live2D PSD 分层指南 v6.3\n")
            f.write("="*50 + "\n")
            f.write(f"图片尺寸: {img.size[0]}x{img.size[1]}\n")
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

        png_path = str(image_path).replace('.png', '_live2d_ready.png')
        try:
            img.save(png_path, optimize=True)
            print(f"✅ 优化PNG文件已创建: {Path(png_path).name}")
            return png_path
        except:
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


def validate_image_path(image_path):
    """验证图片路径安全，防止命令注入"""
    if not image_path or not isinstance(image_path, str):
        return False, "路径不能为空"
    # 检查非法字符
    if re.search(r'[;&|`$\x00]', image_path):
        return False, "路径包含非法字符"
    # 检查文件名是否以 - 开头
    if os.path.basename(image_path).startswith('-'):
        return False, "文件名不能以 - 开头"
    return True, None


def run_ai_layer_tool(image_path):
    """运行AI分层工具"""
    # 验证路径安全
    is_valid, error_msg = validate_image_path(image_path)
    if not is_valid:
        print(f"⚠️ 路径验证失败: {error_msg}")
        return False

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

See-through 是目前最先进的AI分层工具，已集成到本项目中！

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
        description='Live2D Master Agent v6.3 - SD WebUI 集成版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python master_tool.py "cute anime girl"
  python master_tool.py -n 3 "beautiful character"
  python master_tool.py --width 1024 --height 1024
  python master_tool.py --skip-generate
  python master_tool.py --see-through
  python master_tool.py --sd-webui-url http://192.168.1.100:7860
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
    parser.add_argument(
        '--sd-webui-url', type=str, default=None,
        help='Stable Diffusion WebUI 地址（默认 http://127.0.0.1:7860）'
    )
    parser.add_argument(
        '--no-live2d-opt', action='store_true',
        help='禁用 Live2D 优化模式（生成更自由的风格）'
    )
    parser.add_argument(
        '--full-body', action='store_true',
        help='生成全身图片（推荐用于 Live2D）'
    )
    parser.add_argument(
        '--optimize', action='store_true',
        help='生成后自动优化图片（轮廓增强、背景处理）'
    )
    parser.add_argument(
        '--check', action='store_true',
        help='检查已有图片的 Live2D 兼容性'
    )
    parser.add_argument(
        '--high-quality', action='store_true',
        help='高质量模式（匹配参考图风格，推荐）'
    )
    parser.add_argument(
        '--no-hq', action='store_true',
        help='禁用高质量模式（使用普通质量）'
    )
    parser.add_argument(
        '--local', action='store_true',
        help='使用本地 Stable Diffusion 生成（自研工具，需安装 diffusers）'
    )
    parser.add_argument(
        '--model', type=str, default=None,
        help='本地生成使用的模型 ID（如 "Linaqruf/anything-v3.0"）'
    )
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    print("\n" + "="*80)
    print("🎨 Live2D Master Agent v6.3 - SD WebUI 集成版")
    print("="*80)

    # 显示See-through指南
    if args.see_through:
        show_see_through_guide()
        return

    # 检查已有图片的 Live2D 兼容性
    if args.check:
        image_path = get_latest_image(output_dir)
        if image_path:
            try:
                from live2d_image_processor import check_live2d_compatibility
                check_live2d_compatibility(image_path)
            except ImportError:
                print("⚠️ 请先安装 Pillow: pip install Pillow")
        else:
            print("❌ output/ 目录中没有图片")
        return

    # 生成多个多样化角色
    for n in range(args.number):
        print(f"\n{'='*80}")
        print(f"🎯 角色 {n+1}/{args.number}")
        print(f"{'='*80}")

        # 获取图片
        image_path = None

        if args.skip_generate:
            image_path = get_latest_image(output_dir)
            if image_path:
                print(f"📁 使用已有图片: {Path(image_path).name}")
            else:
                print("❌ output/ 目录中没有图片")
                print("💡 请先将图片放到 output/ 目录，或使用默认生成模式")
                return
        else:
            custom_prompt = ' '.join(args.prompt) if args.prompt else ''
            
            # 根据参数选择模式
            live2d_opt = not args.no_live2d_opt
            high_quality = not args.no_hq  # 默认启用高质量
            if args.high_quality:
                high_quality = True
                live2d_opt = False  # 高质量模式下禁用 Live2D 优化
            
            if args.full_body:
                custom_prompt += ", full body, standing"
            
            prompt, features = build_prompt(custom_prompt, live2d_optimized=live2d_opt, high_quality=high_quality)

            print(f"\n🔖 随机特征:")
            for key, value in features.items():
                print(f"   • {key}: {value}")
            
            if high_quality:
                print(f"\n✨ 高质量模式: 已启用")
                print(f"   特点: 精细细节、柔和光影、梦幻风格")
            elif live2d_opt:
                print(f"\n✨ Live2D 优化模式: 已启用")
                print(f"   特点: 全身可见、简单发型、清晰轮廓")
            else:
                print(f"\n⚠️ 优化模式: 已禁用")

            image_path, seed = generate_image(
                prompt,
                output_dir,
                width=args.width,
                height=args.height,
                sd_webui_url=args.sd_webui_url,
                use_local=args.local
            )

            if not image_path:
                show_alternatives()
                return

        # 自动优化图片（如果启用）
        if args.optimize:
            try:
                from live2d_image_processor import auto_optimize_for_live2d
                optimized_path = auto_optimize_for_live2d(image_path, output_dir)
                image_path = optimized_path
                print(f"\n✅ 已使用优化后的图片: {Path(image_path).name}")
            except ImportError:
                print("⚠️ 自动优化需要 Pillow，请安装: pip install Pillow")
            except Exception as e:
                print(f"⚠️ 自动优化失败: {e}")

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
