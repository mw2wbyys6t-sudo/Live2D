#!/usr/bin/env python3
"""
Live2D Master Agent - API 配置工具
帮助用户方便地配置火山引擎 ARK API Key
"""

import os
import sys
from pathlib import Path

def get_env_path() -> Path:
    """获取 .env 文件路径"""
    return Path(__file__).parent / ".env"

def load_config() -> dict:
    """加载现有配置"""
    env_path = get_env_path()
    config = {}
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
    return config

def save_config(config: dict):
    """保存配置到 .env 文件"""
    env_path = get_env_path()
    with open(env_path, "w", encoding="utf-8") as f:
        f.write("# Live2D Master Agent 配置文件\n")
        f.write("# 火山引擎 ARK API 配置（可选）\n")
        f.write("# 注意：此文件包含敏感信息，请不要提交到版本控制！\n\n")
        
        # API 配置
        if "ARK_API_KEY" in config:
            f.write(f"ARK_API_KEY={config['ARK_API_KEY']}\n")
        if "ARK_BASE_URL" in config:
            f.write(f"ARK_BASE_URL={config['ARK_BASE_URL']}\n")
        
        # Seedream 默认配置
        f.write("\n# Seedream 默认配置\n")
        f.write(f"SEEDREAM_DEFAULT_VERSION={config.get('SEEDREAM_DEFAULT_VERSION', '5.0')}\n")
        f.write(f"SEEDREAM_DEFAULT_SIZE={config.get('SEEDREAM_DEFAULT_SIZE', '2048x2048')}\n")
        f.write(f"SEEDREAM_DEFAULT_QUALITY={config.get('SEEDREAM_DEFAULT_QUALITY', 'high')}\n")
        
        # 其他配置
        f.write("\n# 其他配置\n")
        f.write(f"OUTPUT_DIR={config.get('OUTPUT_DIR', './output')}\n")
        f.write(f"MAX_PSD_SIZE_MB={config.get('MAX_PSD_SIZE_MB', '50')}\n")
    
    print(f"✅ 配置已保存到: {env_path}")

def print_header():
    """打印标题"""
    print("\n" + "="*70)
    print("🎨 Live2D Master Agent - API 配置工具")
    print("="*70)
    print()

def show_current_status():
    """显示当前配置状态"""
    from config import config as cfg
    print("当前配置状态:")
    print("-" * 50)
    print(f"  API Key: {'已配置' if cfg.has_api_key else '未配置'}")
    if cfg.has_api_key:
        print(f"  Key 末尾: ...{cfg.ark_api_key[-8:]}")
    print(f"  Base URL: {cfg.ark_base_url}")
    print(f"  默认版本: {cfg.seedream_version}")
    print(f"  默认尺寸: {cfg.seedream_size}")
    print("-" * 50)
    print()

def configure_api_key():
    """配置 API Key"""
    print_header()
    print("📝 火山引擎 ARK API 配置")
    print()
    print("提示：")
    print("  1. 访问 https://www.volcengine.com/ 获取 API Key")
    print("  2. 或跳过配置，继续使用免费的 Pollinations.ai")
    print()
    
    current_config = load_config()
    api_key = input("请输入你的 ARK_API_KEY（直接回车跳过）: ").strip()
    
    if api_key:
        current_config["ARK_API_KEY"] = api_key
        
        base_url = input(f"请输入 ARK_BASE_URL（直接回车使用默认）: ").strip()
        if base_url:
            current_config["ARK_BASE_URL"] = base_url
        
        save_config(current_config)
        print()
        print("✅ API Key 配置成功！")
        print()
        print("现在你可以选择使用：")
        print("  1. Seedream（更高质量）: python scripts/seedream_image_generate.py --prompt \"描述\"")
        print("  2. 免费方案（默认）: python master_tool.py \"描述\"")
    else:
        print()
        print("⏭️  跳过 API 配置")
        print()
        print("继续使用免费方案:")
        print("  python master_tool.py \"你的描述\"")

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] in ["--status", "-s"]:
        print_header()
        show_current_status()
        return
    
    if len(sys.argv) > 1 and sys.argv[1] in ["--clear", "-c"]:
        env_path = get_env_path()
        if env_path.exists():
            env_path.unlink()
            print("✅ 已清除 API 配置")
        else:
            print("ℹ️  没有配置需要清除")
        return
    
    configure_api_key()

if __name__ == "__main__":
    main()
