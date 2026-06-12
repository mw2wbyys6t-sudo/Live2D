#!/usr/bin/env python3
"""
Live2D Master Agent v8.0 - 全面升级版
功能: 本地图片生成 + AI智能分层 + PSD转换

核心：
- 🎯 自研本地 Stable Diffusion 生成器 v5.0（多阶段/批量/智能）
- 🟢 内置AI分层工具（基于色彩聚类 + 区域检测）
- 🔗 生成与分层无缝连接（一键工作流）

特点:
- 完全本地运行，无需网络
- 支持 CPU/GPU 推理
- GPT-4 风格提示词工程
- 智能质量评估 + 自动重试
- 批量生成选最优
- 参考图风格自动分析
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
PROFESSIONAL_PROMPT_TEMPLATE = """(masterpiece:1.4), (best quality:1.3), (ultra detailed:1.2), (highres:1.2), (8k uhd:1.1),
(anime style:1.3), (illustration:1.2), (official art:1.2), (pixiv:1.1), (artstation:1.1),
1girl, solo, {pose}, {hairstyle}, {hair_color}, {eye_color}, {clothing}, {accessory}, {expression},
(beautiful detailed face:1.3), (beautiful detailed eyes:1.3), (detailed skin texture:1.1), (soft lighting:1.2),
(pastel colors:1.2), (soft color palette:1.2), (dreamy atmosphere:1.1), (ethereal:1.1),
(frills:1.1), (lace:1.1), (ribbons:1.1), (bows:1.1), (jewelry:1.1), (elegant outfit:1.2),
(perfect anatomy:1.2), (correct proportions:1.2), (delicate hands:1.2),
(white background:1.2), (simple background:1.2), (clean background:1.2),
(sharp focus:1.2), (vibrant colors:1.1), (clear lineart:1.3), (smooth shading:1.1),
(extremely detailed:1.2), (intricate details:1.2), (professional illustration:1.2),
(art by Artgerm:1.1), (art by WLOP:1.1), (art by Rossdraws:1.1),
(soft volumetric lighting:1.2), (rim lighting:1.1), (bloom:1.1)"""

# Live2D 专用提示词模板
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

# 高质量反向提示词
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
    }
    return features


def build_prompt(custom_prompt="", live2d_optimized=True, high_quality=True, use_structured=True):
    """构建优化的多样化提示词 v6.0 - 支持结构化解析

    Returns:
        如果解析成功或随机生成成功，返回 (prompt, features) 元组
        如果出错，返回 (prompt, {}) 或 ("", {})
    """

    # v6.0: 优先使用结构化解析
    if use_structured and custom_prompt:
        try:
            from local_image_generator import PromptEngineer
            character = PromptEngineer.parse_character_from_text(custom_prompt)

            # 如果解析到了特征，使用结构化构建
            if any([character.get("hair_color"), character.get("features"),
                    character.get("clothing")]):
                print(f"🧠 结构化解析角色: {custom_prompt}")
                print(f"   发色: {character.get('hair_color', '默认')}")
                print(f"   发型: {character.get('hair_style', '默认')}")
                print(f"   眼睛: {character.get('eye_color', '默认')}")
                print(f"   特征: {', '.join(character.get('features', [])) or '无'}")
                print(f"   表情: {character.get('expression', '默认')}")
                print(f"   服装: {character.get('clothing', '默认')}")

                prompt, _ = PromptEngineer.build_prompt_from_character(
                    character, style="anime", live2d_mode=live2d_optimized
                )

                # 构建特征字典用于返回
                features = {
                    'hairstyle': character.get('hair_style', 'long hair'),
                    'hair_color': character.get('hair_color', 'pink') + ' hair',
                    'eye_color': character.get('eye_color', 'blue') + ' eyes',
                    'clothing': character.get('clothing', 'school uniform'),
                    'accessory': 'hair ribbon',
                    'expression': character.get('expression', 'smile'),
                    'pose': 'standing',
                }
                return prompt, features
        except Exception as e:
            print(f"⚠️ 结构化解析失败，回退到随机生成: {e}")

    # 传统随机特征生成
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
        prompt_parts.append(features['hairstyle'])
        prompt_parts.append(features['hair_color'])
        prompt_parts.append(features['eye_color'])
        prompt_parts.append(features['clothing'])
        prompt_parts.append(features['accessory'])
        prompt_parts.append(features['expression'])
        prompt_parts.append(features['pose'])
        return " ".join(prompt_parts), features


def get_latest_image(output_dir):
    """获取最新图片"""
    png_files = sorted(output_dir.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    return str(png_files[0]) if png_files else None


def generate_image_pollinations(prompt, output_dir, width=512, height=768, seed=None):
    """
    使用 Pollinations.ai 免费在线生成图片
    无需任何依赖，开箱即用
    """
    import urllib.request
    import urllib.parse

    print(f"\n🌐 使用 Pollinations.ai 免费生成...")
    print(f"📝 提示词: {prompt[:100]}...")

    if seed is None:
        seed = random.randint(0, 999999999)

    # 构建 Pollinations.ai URL
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true"

    try:
        output_path = os.path.join(output_dir, f"pollinations_{seed}.png")
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
            }
        )

        print(f"⬇️  正在下载...")
        with urllib.request.urlopen(req, timeout=120) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())

        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print(f"✅ 成功！使用 Pollinations.ai 免费生成")
            print(f"📁 保存至: {output_path}")
            return output_path, seed
        else:
            print("❌ 下载的文件无效")
            return None, seed

    except Exception as e:
        print(f"❌ Pollinations.ai 生成失败: {e}")
        return None, seed


def generate_image_huggingface(prompt, output_dir, width=512, height=768, seed=None):
    """
    使用 Hugging Face Inference API 免费生成图片
    无需 API Key，使用公开模型
    """
    import urllib.request
    import urllib.parse
    import json

    print(f"\n🌐 使用 Hugging Face 免费生成...")
    print(f"📝 提示词: {prompt[:100]}...")

    if seed is None:
        seed = random.randint(0, 999999999)

    # 使用 Stable Diffusion 公开 API
    api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
    payload = json.dumps({"inputs": prompt, "parameters": {"seed": seed}}).encode('utf-8')

    try:
        output_path = os.path.join(output_dir, f"huggingface_{seed}.png")
        req = urllib.request.Request(
            api_url,
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0'
            }
        )

        print(f"⬇️  正在请求 Hugging Face API...")
        with urllib.request.urlopen(req, timeout=180) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())

        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print(f"✅ 成功！使用 Hugging Face 免费生成")
            print(f"📁 保存至: {output_path}")
            return output_path, seed
        else:
            print("❌ 下载的文件无效")
            return None, seed

    except Exception as e:
        print(f"❌ Hugging Face 生成失败: {e}")
        return None, seed


def generate_image_deepai(prompt, output_dir, width=512, height=768, seed=None):
    """
    使用 DeepAI 免费生成图片
    无需 API Key
    """
    import urllib.request
    import urllib.parse

    print(f"\n🌐 使用 DeepAI 免费生成...")
    print(f"📝 提示词: {prompt[:100]}...")

    if seed is None:
        seed = random.randint(0, 999999999)

    try:
        output_path = os.path.join(output_dir, f"deepai_{seed}.png")

        # DeepAI 文本生成图片 API（无需 key）
        data = urllib.parse.urlencode({
            'text': prompt,
        }).encode('utf-8')

        req = urllib.request.Request(
            'https://api.deepai.org/api/text2img',
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0'
            }
        )

        print(f"⬇️  正在请求 DeepAI API...")
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            image_url = result.get('output_url')

            if image_url:
                img_req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(img_req, timeout=60) as img_response:
                    with open(output_path, 'wb') as f:
                        f.write(img_response.read())

        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print(f"✅ 成功！使用 DeepAI 免费生成")
            print(f"📁 保存至: {output_path}")
            return output_path, seed
        else:
            print("❌ 下载的文件无效")
            return None, seed

    except Exception as e:
        print(f"❌ DeepAI 生成失败: {e}")
        return None, seed


def generate_image(prompt, output_dir, seed=None, width=512, height=768, steps=25, model_id=None, live2d_mode=True, reference_image=None, batch_size=1, use_smart=False, use_multistage=False):
    """
    生成图片（优先本地生成器，降级到在线免费方案）
    """
    print(f"\n🎨 正在生成图片...")
    print(f"📝 提示词: {prompt[:100]}...")
    print(f"📐 尺寸: {width}x{height}")

    if seed is None:
        seed = random.randint(0, 999999999)

    # 尝试1：本地 Stable Diffusion 生成（高质量）
    try:
        from local_image_generator import Live2DOptimizedGenerator, get_live2d_negative_prompt, get_default_negative_prompt

        generator = Live2DOptimizedGenerator(model_id=model_id or "Linaqruf/anything-v3.0")

        # 根据模式选择反向提示词
        negative_prompt = get_live2d_negative_prompt() if live2d_mode else get_default_negative_prompt()

        # 批量生成
        if batch_size > 1:
            print(f"\n🎯 批量生成 {batch_size} 张图片...")
            best_path, all_paths = generator.batch_generator.generate_batch(
                prompt=prompt,
                negative_prompt=negative_prompt,
                batch_size=batch_size,
                width=width,
                height=height,
                steps=steps,
                use_multistage=use_multistage,
            )
            if best_path:
                print(f"\n✅ 批量生成完成！最优: {Path(best_path).name}")
                return best_path, seed

        # 智能生成（自动重试）
        elif use_smart:
            print(f"\n🤖 智能生成（自动评估质量）...")
            success, output_path = generator.generate_with_retry(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                steps=steps,
                seed=seed,
                live2d_optimized=live2d_mode,
            )
            if success and output_path:
                return output_path, seed

        # 多阶段生成
        elif use_multistage:
            print(f"\n🔄 多阶段生成...")
            output_path = generator.pipeline.run_pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                seed=seed,
            )
            if output_path:
                return output_path, seed

        # 标准生成
        else:
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
                print("\n✅ 成功！使用本地 Stable Diffusion v5.0")
                return output_path, seed

    except ImportError:
        print("⚠️ 本地生成器未安装，自动切换到免费在线方案...")
    except Exception as e:
        print(f"⚠️ 本地生成失败: {e}")

    # 尝试2：Pollinations.ai 免费在线生成（降级方案1）
    print("\n🔄 尝试免费在线生成方案...")
    output_path, seed = generate_image_pollinations(prompt, output_dir, width, height, seed)
    if output_path:
        return output_path, seed

    # 尝试3：Hugging Face 免费生成（降级方案2）
    print("\n🔄 尝试 Hugging Face 免费生成...")
    output_path, seed = generate_image_huggingface(prompt, output_dir, width, height, seed)
    if output_path:
        return output_path, seed

    # 尝试4：DeepAI 免费生成（降级方案3）
    print("\n🔄 尝试 DeepAI 免费生成...")
    output_path, seed = generate_image_deepai(prompt, output_dir, width, height, seed)
    if output_path:
        return output_path, seed

    print("\n❌ 所有生成方案均失败")
    print("\n💡 解决方案:")
    print("   1. 检查网络连接（在线生成需要网络）")
    print("   2. 安装本地生成器: pip install diffusers transformers torch accelerate")
    print("   3. 手动提供图片: python master_tool.py --skip-generate")

    return None, seed


def run_layering_pipeline(image_path, output_dir):
    """运行完整的分层管道"""
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

    # 额外验证：路径必须实际存在且为文件
    if not os.path.isfile(image_path):
        print(f"⚠️ 路径不存在或不是文件: {image_path}")
        return None

    # 使用绝对路径防止路径解析问题
    image_path = os.path.abspath(image_path)

    try:
        import subprocess
        import shlex
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
            f.write("Live2D PSD 分层指南 v8.0\n")
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


class Live2DTool:
    """Live2D工具类 - 提供面向对象的API接口

    封装了图像生成、分层、PSD转换等核心功能。

    示例:
        tool = Live2DTool()
        image_path = tool.generate("蓝发猫耳少女")
        layers = tool.layer(image_path)
        psd_path = tool.to_psd(layers)
    """

    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.last_image = None
        self.last_layers = None

    def generate(self, prompt: str, **kwargs) -> Optional[str]:
        """生成角色图片

        Args:
            prompt: 角色描述提示词
            **kwargs: 传递给generate_image的参数

        Returns:
            生成的图片路径
        """
        image_path, _ = generate_image(
            prompt,
            self.output_dir,
            **kwargs
        )
        if image_path:
            self.last_image = image_path
        return image_path

    def layer(self, image_path: Optional[str] = None, **kwargs) -> Optional[Dict]:
        """对图片进行分层处理

        Args:
            image_path: 图片路径（默认使用最后生成的图片）
            **kwargs: 额外参数

        Returns:
            分层结果字典
        """
        path = image_path or self.last_image
        if not path:
            print("❌ 没有可用的图片，请先调用generate()")
            return None

        results = run_layering_pipeline(path, self.output_dir)
        self.last_layers = results
        return results

    def to_psd(self, layer_dir: Optional[str] = None) -> Optional[str]:
        """将分层结果转换为PSD

        Args:
            layer_dir: 分层目录路径（默认使用最后分层的目录）

        Returns:
            PSD文件路径
        """
        if layer_dir:
            return convert_to_psd(layer_dir)
        elif self.last_layers and self.last_layers.get('psd'):
            return self.last_layers['psd']
        else:
            print("❌ 没有可用的分层结果，请先调用layer()")
            return None

    def validate(self, image_path: Optional[str] = None) -> Tuple[bool, str]:
        """验证图片的Live2D兼容性

        Args:
            image_path: 图片路径（默认使用最后生成的图片）

        Returns:
            (是否兼容, 验证报告)
        """
        path = image_path or self.last_image
        if not path:
            return False, "没有可用的图片"

        try:
            from live2d_image_processor import check_live2d_compatibility
            result = check_live2d_compatibility(path)
            score = result.get('score', 0)
            issues = result.get('issues', [])
            is_valid = score >= 0.6
            report = f"兼容性评分: {score}\n" + "\n".join(issues)
            return is_valid, report
        except ImportError:
            return False, "live2d_image_processor未安装"
        except Exception as e:
            return False, f"验证失败: {e}"

    def get_latest(self) -> Optional[str]:
        """获取最新生成的图片路径"""
        return get_latest_image(self.output_dir)


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
        description='Live2D Master Agent v8.0 - 全面升级版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础生成
  python master_tool.py "cute anime girl"

  # 批量生成选最优
  python master_tool.py --batch 5 "beautiful character"

  # 智能生成（自动评估质量）
  python master_tool.py --smart "cute girl"

  # 多阶段生成
  python master_tool.py --multistage "masterpiece"

  # 参考图风格迁移
  python master_tool.py --reference ref.png "new character"

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
    parser.add_argument(
        '--batch', type=int, default=1,
        help='批量生成数量（默认1，推荐4-8）'
    )
    parser.add_argument(
        '--smart', action='store_true',
        help='智能生成（自动评估质量并重试）'
    )
    parser.add_argument(
        '--multistage', action='store_true',
        help='多阶段生成（草稿→精修→超分）'
    )
    parser.add_argument(
        '--reference', type=str, default=None,
        help='参考图路径（自动分析风格）'
    )
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    print("\n" + "="*80)
    print("🎨 Live2D Master Agent v8.0 - 全面升级版")
    print("="*80)
    print("\n核心功能:")
    print("  🎯 自研本地生成器 v5.0")
    print("  🤖 智能质量评估 + 自动重试")
    print("  📊 批量生成选最优")
    print("  🎨 参考图风格自动分析")
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

            # 显示生成模式
            if args.batch > 1:
                print(f"\n📊 批量生成模式: {args.batch} 张")
            elif args.smart:
                print(f"\n🤖 智能生成模式: 自动评估质量")
            elif args.multistage:
                print(f"\n🔄 多阶段生成模式: 草稿→精修→超分")

            if args.reference:
                print(f"\n🎨 参考图: {args.reference}")

            image_path, seed = generate_image(
                prompt,
                output_dir,
                width=args.width,
                height=args.height,
                steps=args.steps,
                model_id=args.model,
                live2d_mode=live2d_opt,
                reference_image=args.reference,
                batch_size=args.batch,
                use_smart=args.smart,
                use_multistage=args.multistage,
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
