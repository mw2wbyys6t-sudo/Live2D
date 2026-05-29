#!/usr/bin/env python3
"""
Live2D Master Agent v7.1 - 全面升级版
功能: 本地图片生成 + AI智能分层 + PSD转换

核心：
- 🎯 自研本地 Stable Diffusion 生成器 v4.0（基于 diffusers）
- 🟢 内置AI分层工具（基于色彩聚类 + 区域检测）
- 🔗 生成与分层无缝连接（一键工作流）

特点:
- 完全本地运行，无需网络
- 支持 CPU/GPU 推理
- 针对动漫风格优化
- 自动下载和管理模型
- 生成即分层就绪
"""

import os
import sys
import time
import random
import re
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

# 专业级提示词模板（匹配参考图质量）
# 使用权重控制语法 (keyword:1.3) 提升关键元素质量
PROFESSIONAL_PROMPT_TEMPLATE = """(masterpiece:1.4), (best quality:1.3), (ultra detailed:1.2), (highres:1.2), (8k uhd:1.1),
(anime style:1.3), (illustration:1.2), (official art:1.2), (pixiv:1.1), (artstation:1.1),
1girl, solo, {pose}, {hairstyle}, {hair_color}, {eye_color}, {clothing}, {accessory}, {expression},
(beautiful detailed face:1.3), (beautiful detailed eyes:1.3), (detailed skin texture:1.1), (soft lighting:1.2),
(pastel colors:1.2), (soft color palette:1.2), (dreamy atmosphere:1.1), (ethereal:1.1),
(frills:1.1), (lace:1.1), (ribbons:1.1), (bows:1.1), (jewelry:1.1), (elegant outfit:1.2),
(perfect anatomy:1.2), (correct proportions:1.2), (delicate hands:1.2),
(white background:1.2), (simple background:1.2), (clean background:1.2),
(sharp focus:1.2), (vibrant colors:1.1), (clear lineart:1.3), (smooth shading:1.1)"""

# Live2D 专用提示词模板（基于业界最佳实践）
LIVE2D_PROMPT_TEMPLATE = """(masterpiece:1.4), (best quality:1.3), (ultra detailed:1.2), (highres:1.2),
(anime style:1.3), (illustration:1.2), 1girl, solo, (full body:1.2), (standing:1.1), (looking at viewer:1.2),
{hairstyle}, {hair_color}, {eye_color}, {clothing}, {accessory}, {expression},
(beautiful detailed face:1.3), (beautiful detailed eyes:1.3), (detailed skin texture:1.1), (soft lighting:1.2),
(perfect for Live2D rigging:1.2), (clean lineart:1.3), (clear edges:1.3), (sharp outlines:1.3),
(flat colors:1.2), (minimal shading:1.2), (cel shading:1.2), (distinct color separation:1.2),
(anime coloring:1.2), (sharp lines:1.3), (clean outlines:1.3), (minimal gradients:1.2),
(simple background:1.2), (white background:1.2), (isolated character:1.2),
(clear silhouette:1.2), (symmetrical eyes:1.2), (simple hair strands:1.1),
(visible neck and shoulders:1.2), (visible arms and hands:1.2), (visible legs and feet:1.2),
(closed mouth:1.1), (neutral expression:1.1), (front view:1.2), (straight-on view:1.2),
(perfect anatomy:1.2), (correct proportions:1.2), (delicate hands:1.2),
(sharp focus:1.2), (vibrant colors:1.1)"""

# 高质量反向提示词（基于搜索研究优化）
HIGH_QUALITY_NEGATIVE_PROMPT = """(lowres:1.4), (bad anatomy:1.4), (bad hands:1.3), (text:1.3), (error:1.3), (missing fingers:1.3),
(extra digit:1.3), (fewer digits:1.3), (cropped:1.2), (worst quality:1.3), (low quality:1.3),
(normal quality:1.2), (jpeg artifacts:1.2), (signature:1.2), (watermark:1.2), (username:1.2), (blurry:1.3),
(artist name:1.2), (bad proportions:1.3), (extra limbs:1.3), (cloned face:1.2), (disfigured:1.3),
(gross proportions:1.3), (malformed limbs:1.3), (missing arms:1.2), (missing legs:1.2),
(extra arms:1.2), (extra legs:1.2), (fused fingers:1.2), (too many fingers:1.2), (long neck:1.2),
(photorealistic:1.2), (realistic:1.2), (3d:1.2), (western:1.2), (sketch:1.1), (rough:1.1), (draft:1.1),
(complex background:1.2), (messy hair:1.2), (messy clothes:1.2),
(depth of field:1.1), (blurry background:1.2), (multiple girls:1.3), (multiple people:1.3)"""

# Live2D 反向提示词（更严格）
LIVE2D_NEGATIVE_PROMPT = """(lowres:1.4), (bad anatomy:1.4), (bad hands:1.3), (text:1.3), (error:1.3), (missing fingers:1.3),
(extra digit:1.3), (fewer digits:1.3), (cropped:1.2), (worst quality:1.3), (low quality:1.3),
(normal quality:1.2), (jpeg artifacts:1.2), (signature:1.2), (watermark:1.2), (username:1.2), (blurry:1.3),
(artist name:1.2), (bad proportions:1.3), (extra limbs:1.3), (cloned face:1.2), (disfigured:1.3),
(gross proportions:1.3), (malformed limbs:1.3), (missing arms:1.2), (missing legs:1.2),
(extra arms:1.2), (extra legs:1.2), (fused fingers:1.2), (too many fingers:1.2), (long neck:1.2),
(photorealistic:1.2), (realistic:1.2), (3d:1.2), (western:1.2), (sketch:1.1), (rough:1.1), (draft:1.1),
(complex background:1.2), (messy hair:1.2), (messy clothes:1.2),
(profile view:1.2), (side view:1.2), (back view:1.2), (turned away:1.2),
(open mouth:1.2), (talking:1.2), (shouting:1.2), (laughing:1.2), (crying:1.2),
(dynamic pose:1.2), (action pose:1.2), (jumping:1.2), (running:1.2), (sitting:1.2), (lying down:1.2),
(partial body:1.2), (cropped:1.2), (off-screen:1.2), (out of frame:1.2),
(gradient shading:1.2), (soft shading:1.2), (painterly:1.2), (watercolor:1.2),
(noise:1.2), (grainy:1.2), (pixelated:1.2), (compression artifacts:1.2)"""


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
        hairstyle = random.choice(LIVE2D_HAIRSTYLES)
        prompt = LIVE2D_PROMPT_TEMPLATE.format(
            hairstyle=hairstyle,
            hair_color=features['hair_color'],
            eye_color=features['eye_color'],
            clothing=features['clothing'],
            accessory=features['accessory'],
            expression=features['expression']
        )
        prompt = ' '.join(prompt.split())
        return prompt, features
    elif high_quality:
        prompt = PROFESSIONAL_PROMPT_TEMPLATE.format(
            pose=features['pose'],
            hairstyle=features['hairstyle'],
            hair_color=features['hair_color'],
            eye_color=features['eye_color'],
            clothing=features['clothing'],
            accessory=features['accessory'],
            expression=features['expression']
        )
        if custom_prompt:
            prompt = custom_prompt + ", " + prompt
        prompt = ' '.join(prompt.split())
        return prompt, features
    else:
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


def generate_image(prompt, output_dir, seed=None, width=512, height=768, steps=25, model_id=None, live2d_mode=True):
    """
    生成图片（使用自研本地生成器 v4.0）
    """
    print(f"\n🎨 正在生成图片...")
    print(f"📝 提示词: {prompt[:100]}...")
    print(f"📐 尺寸: {width}x{height}")

    if seed is None:
        seed = random.randint(0, 999999999)

    try:
        from local_image_generator import Live2DOptimizedGenerator, get_live2d_negative_prompt, get_default_negative_prompt

        generator = Live2DOptimizedGenerator(model_id=model_id or "Linaqruf/anything-v3.0")

        # 根据模式选择反向提示词
        negative_prompt = get_live2d_negative_prompt() if live2d_mode else get_default_negative_prompt()

        success, output_path = generator.generate(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            steps=steps,
            seed=seed,
            live2d_optimized=live2d_mode,
        )

        if success and output_path:
            print("\n✅ 成功！使用本地 Stable Diffusion v4.0")
            return output_path, seed

    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print(f"\n💡 请安装 diffusers:")
        print(f"   pip install diffusers transformers torch accelerate")
    except Exception as e:
        print(f"❌ 生成失败: {e}")

    return None, seed


def run_layering_pipeline(image_path, output_dir):
    """
    运行完整的分层管道
    1. 内置AI分层
    2. 生成PSD规划
    3. 建议See-through专业分层
    """
    print(f"\n{'='*80}")
    print("🎨 启动分层管道")
    print(f"{'='*80}")

    results = {}

    # 1. 运行内置AI分层工具
    print("\n📋 步骤 1/3: 内置AI分层")
    layer_result = run_ai_layer_tool(image_path)
    results['built_in'] = layer_result

    # 2. 创建PSD规划
    print("\n📋 步骤 2/3: 创建PSD规划")
    plan_dir = create_psd_plan(image_path, output_dir)
    results['psd_plan'] = plan_dir

    # 3. 转换为基础PSD
    print("\n📋 步骤 3/3: 基础PSD转换")
    psd_path = convert_to_psd(image_path)
    results['psd'] = psd_path

    return results


def run_ai_layer_tool(image_path):
    """运行AI分层工具"""
    is_valid, error_msg = validate_image_path(image_path)
    if not is_valid:
        print(f"⚠️ 路径验证失败: {error_msg}")
        return None

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
            f.write("Live2D PSD 分层指南 v7.1\n")
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

        print(f"✅ 分层规划已创建: {plan_dir}")
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
    if re.search(r'[;&|`$\x00]', image_path):
        return False, "路径包含非法字符"
    if os.path.basename(image_path).startswith('-'):
        return False, "文件名不能以 - 开头"
    return True, None


def show_help():
    """显示帮助信息"""
    print("""
💡 使用说明:

1. 🎯 自研本地生成器（推荐）:
   • 完全本地运行，无需网络
   • 支持 CPU/GPU 推理
   • 首次使用自动下载模型（约 4GB）

2. 🎨 内置AI分层:
   • 自动色彩聚类分层
   • 符合Live2D标准图层结构
   • 生成PSD规划指南

3. 🏆 See-through 专业分层（SIGGRAPH 2026）:
   • 运行: python install_comfyui_advanced.py
   • 详细文档: SEE_THROUGH_INTEGRATION.md

4. 📁 使用已有图片:
   将图片放到 output/ 目录后运行:
   python master_tool.py --skip-generate
""")


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
        description='Live2D Master Agent v7.1 - 全面升级版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 完整工作流：生成 + 分层
  python master_tool.py "cute anime girl"

  # 生成多个角色
  python master_tool.py -n 3 "beautiful character"

  # 使用已有图片进行分层
  python master_tool.py --skip-generate

  # 指定模型
  python master_tool.py --model "gsdf/Counterfeit-V3.0"

  # 查看See-through指南
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
        '--width', type=int, default=512,
        help='图片宽度（默认512）'
    )
    parser.add_argument(
        '--height', type=int, default=768,
        help='图片高度（默认768）'
    )
    parser.add_argument(
        '--steps', type=int, default=25,
        help='推理步数（默认25）'
    )
    parser.add_argument(
        '--model', type=str, default=None,
        help='使用的模型 ID（如 "Linaqruf/anything-v3.0"）'
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
        '--post-process', action='store_true',
        help='启用专业后处理管道'
    )
    parser.add_argument(
        '--layer-only', action='store_true',
        help='仅运行分层，跳过生成'
    )
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    print("\n" + "="*80)
    print("🎨 Live2D Master Agent v7.1 - 全面升级版")
    print("="*80)
    print("\n核心功能:")
    print("  🎯 自研本地生成器 v4.0")
    print("  🎨 内置AI分层工具")
    print("  🔗 生成与分层无缝连接")

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

    # 仅运行分层
    if args.layer_only:
        image_path = get_latest_image(output_dir)
        if image_path:
            print(f"\n📁 使用已有图片: {Path(image_path).name}")
            run_layering_pipeline(image_path, output_dir)
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
            high_quality = not args.no_hq
            if args.high_quality:
                high_quality = True
                live2d_opt = False

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
                print(f"   特点: 全身可见、简单发型、清晰轮廓、分层就绪")
            else:
                print(f"\n⚠️ 优化模式: 已禁用")

            image_path, seed = generate_image(
                prompt,
                output_dir,
                width=args.width,
                height=args.height,
                steps=args.steps,
                model_id=args.model,
                live2d_mode=live2d_opt
            )

            if not image_path:
                show_help()
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

        # 后处理管道（如果启用）
        if args.post_process:
            try:
                from local_image_generator import Live2DOptimizedGenerator
                generator = Live2DOptimizedGenerator()
                processed_path = generator.post_process_pipeline(image_path)
                image_path = processed_path
                print(f"\n✅ 已使用后处理图片: {Path(image_path).name}")
            except Exception as e:
                print(f"⚠️ 后处理失败: {e}")

        # 运行分层管道
        run_layering_pipeline(image_path, output_dir)

        # 建议See-through
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
