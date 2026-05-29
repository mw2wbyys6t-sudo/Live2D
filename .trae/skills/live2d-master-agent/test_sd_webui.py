#!/usr/bin/env python3
"""
测试 SD WebUI 集成
简单的测试脚本，验证集成是否正常工作
"""

import sys
from pathlib import Path

print("=" * 60)
print("🎯 Live2D Master Agent v6.3 - SD WebUI 集成测试")
print("=" * 60)

# 测试 1：检查 sd_webui_integration.py 是否存在
print("\n[1/4] 检查 SD WebUI 集成模块...")
sd_module = Path(__file__).parent / "sd_webui_integration.py"
if sd_module.exists():
    print("✅ sd_webui_integration.py 存在")
else:
    print("❌ sd_webui_integration.py 不存在")
    sys.exit(1)

# 测试 2：尝试导入模块
print("\n[2/4] 测试导入 SD WebUI 集成...")
try:
    from sd_webui_integration import (
        StableDiffusionWebUIClient,
        optimize_prompt_for_live2d,
        get_negative_prompt_for_live2d
    )
    print("✅ 模块导入成功")
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

# 测试 3：测试提示词优化
print("\n[3/4] 测试提示词优化...")
test_prompt = "cute anime girl"
optimized = optimize_prompt_for_live2d(test_prompt)
negative = get_negative_prompt_for_live2d()
print(f"✅ 提示词优化完成")
print(f"   原始: {test_prompt}")
print(f"   优化后（部分）: {optimized[:100]}...")
print(f"   反向提示词（部分）: {negative[:100]}...")

# 测试 4：检查 SD WebUI 服务（可选）
print("\n[4/4] 检查 SD WebUI 服务状态...")
client = StableDiffusionWebUIClient()

print("测试地址: http://127.0.0.1:7860")

service_available = client.is_available(force_check=True)

print("\n" + "=" * 60)
print("📊 测试总结")
print("=" * 60)

if service_available:
    print("✅ 恭喜！SD WebUI 服务可用！")
    print("   你可以使用 Stable Diffusion WebUI 来生成高质量图片！")
else:
    print("⚠️ SD WebUI 服务当前不可用（这是正常的）")
    print("   Pollinations.ai 将作为降级方案自动使用")

print("\n💡 安装 SD WebUI（可选，但推荐）:")
print("   1. 克隆 Stable Diffusion WebUI:")
print("      git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui")
print("\n   2. 下载动漫风格模型到 models/Stable-diffusion/")
print("\n   3. 启动服务:")
print("      cd stable-diffusion-webui && python launch.py --api --listen")
print("\n   4. 然后运行:")
print("      python master_tool.py \"cute anime girl\"")

print("\n✅ 集成测试完成！")
print("=" * 60)
