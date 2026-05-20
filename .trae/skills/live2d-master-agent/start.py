#!/usr/bin/env python3
"""
Live2D Master Agent 快速启动脚本
自动检测 API 配置并提供相应功能
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    from config import config
except ImportError:
    print("⚠️ 配置加载失败，使用默认配置")
    config = None

def print_banner():
    print()
    print("=" * 60)
    print("🎨 Live2D Master Agent v3.0")
    print("=" * 60)
    print()

def check_api_status():
    if config and config.has_api_key:
        print("✅ API 状态: 已配置")
        print(f"   API Key: ***{config.ark_api_key[-8:]}")
        print(f"   模型版本: {config.seedream_version}")
        print(f"   默认分辨率: {config.seedream_size}")
        return True
    else:
        print("⚠️ API 状态: 未配置")
        print("   图像生成功能需要 API 密钥")
        return False

def print_available_features(has_api: bool):
    print()
    print("📋 可用功能:")
    print()
    
    features = [
        ("🖼️ 图像生成", has_api, "使用 Seedream 5.0 生成高质量立绘"),
        ("🔍 PSD 质量检查", True, "检查 PSD 文件是否符合 Live2D 规范"),
        ("📋 分层规划", True, "提供详细的 PSD 分层建议"),
        ("⚙️ 参数设计", True, "设计 Cubism 参数配置"),
        ("🌊 物理设置", True, "计算物理参数"),
        ("🎯 Rigging 指导", True, "提供绑定操作指南"),
        ("📝 命名规范", True, "检查和生成规范命名"),
        ("🎭 遮挡分析", True, "分析图层遮挡关系"),
    ]
    
    for name, available, desc in features:
        status = "✅" if available else "❌"
        print(f"  {status} {name}")
        print(f"      {desc}")
    print()

def print_quick_commands():
    print("💡 快速命令:")
    print()
    print("  生成角色立绘:")
    print("    generate anime girl, pink hair, JK uniform")
    print()
    print("  检查 PSD 文件:")
    print("    check psd /path/to/file.psd")
    print()
    print("  规划分层:")
    print("    plan layers for anime character")
    print()
    print("  设置物理:")
    print("    setup physics for long hair character")
    print()

def print_no_api_guide():
    print()
    print("📚 无 API 使用指南:")
    print()
    print("  即使没有 API，以下功能仍可正常使用:")
    print("  - PSD 质量检查")
    print("  - 分层规划")
    print("  - 参数设计")
    print("  - 物理设置")
    print("  - Rigging 指导")
    print()
    print("  详细说明请查看: NO_API_GUIDE.md")
    print()

def main():
    print_banner()
    
    has_api = check_api_status()
    
    print_available_features(has_api)
    
    if not has_api:
        print_no_api_guide()
    
    print_quick_commands()
    
    print("=" * 60)
    print("准备就绪！输入命令开始使用")
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
