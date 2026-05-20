#!/usr/bin/env python3
"""
生成动漫少女立绘 - Live2D 专用
使用 Seedream 5.0 高质量生成
"""

import asyncio
import sys
import os
import httpx
import json

async def generate_anime_character():
    api_key = "ark-d0dd55e5-ee35-426f-9321-7c09b8d76a81-4283b"
    api_base = "https://ark.cn-beijing.volces.com/api/v3"
    model = "doubao-seedream-5-0-260128"
    
    character_prompt = """
anime girl, cute kawaii style, beautiful face, big expressive eyes,
long flowing pink hair, soft pink gradient hair, hair strands detailed,
wearing JK school uniform, white blouse, navy blue pleated skirt,
red ribbon tie, school bag accessory,
slender figure, elegant pose, standing pose,
perfect for Live2D rigging, clean layer separation,
isolated character on white background, easy to rig,
sharp clean lines, vibrant colors, ultra detailed,
masterpiece, award-winning quality, professional artwork,
4K resolution, high quality render, anime art style,
soft lighting, detailed facial features, sparkling eyes
""".strip().replace('\n', ' ')

    print("🎨 开始生成动漫少女立绘...")
    print(f"📐 分辨率: 4096x4096 (4K)")
    print(f"🎯 模型: Seedream 5.0")
    print(f"✨ 质量: Ultra High Quality")
    print(f"📝 提示词长度: {len(character_prompt)} 字符")
    print()

    url = f"{api_base}/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    body = {
        "model": model,
        "prompt": character_prompt,
        "size": "2048x2048"
    }

    print("📤 发送请求到 Seedream API...")
    print(f"URL: {url}")
    print()

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, headers=headers, json=body)
            
            print(f"📥 响应状态码: {response.status_code}")
            print()
            
            if response.status_code != 200:
                print(f"❌ 请求失败")
                print(f"响应内容: {response.text}")
                return None
            
            result = response.json()
            
            if "error" in result:
                print(f"❌ API 返回错误")
                print(f"错误信息: {json.dumps(result['error'], indent=2, ensure_ascii=False)}")
                return None
            
            if "data" in result and len(result["data"]) > 0:
                image_data = result["data"][0]
                
                if "url" in image_data:
                    image_url = image_data["url"]
                    print("✅ 生成成功！")
                    print()
                    print("📊 生成结果:")
                    print(f"  图片URL: {image_url}")
                    print()
                    
                    print("💾 正在下载图片...")
                    img_response = await client.get(image_url)
                    
                    if img_response.status_code == 200:
                        output_path = "/workspace/output/anime_character.png"
                        with open(output_path, "wb") as f:
                            f.write(img_response.content)
                        print(f"✅ 图片已保存到: {output_path}")
                        
                        return {
                            "success": True,
                            "image_url": image_url,
                            "local_path": output_path
                        }
                    else:
                        print(f"❌ 下载图片失败: {img_response.status_code}")
                        return None
                else:
                    print(f"❌ 响应中没有图片URL")
                    print(f"响应数据: {json.dumps(image_data, indent=2, ensure_ascii=False)}")
                    return None
            else:
                print(f"❌ 响应格式异常")
                print(f"完整响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return None

    except httpx.TimeoutException:
        print("❌ 请求超时")
        return None
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP 错误: {e}")
        return None
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(generate_anime_character())
    
    if result and result.get("success"):
        print()
        print("=" * 60)
        print("🎉 立绘生成完成！")
        print("=" * 60)
        print()
        print("💡 下一步建议:")
        print("  1. 查看生成的图片")
        print("  2. 进行 PSD 分层规划")
        print("  3. 转换为分层 PSD 文件")
        print("  4. 进行 Live2D 质量检查")
