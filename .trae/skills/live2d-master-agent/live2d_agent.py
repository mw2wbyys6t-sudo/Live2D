#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Live2D Master Agent - 交互式CLI入口
用户只需运行这个脚本，Agent会引导完成所有操作

使用方法:
    python live2d_agent.py

支持自然语言对话，例如:
    - "我想做一个猫耳少女"
    - "帮我生成一个机甲角色"
    - "我要部署桌面宠物"
    - "使用我提供的图片"
"""

import sys
import os
import argparse
from pathlib import Path

# 确保可以导入同级模块
sys.path.insert(0, str(Path(__file__).parent))


def print_banner():
    """打印欢迎界面"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🎨 Live2D Master Agent v7.1                             ║
║     你的Live2D制作助手 - 告诉我你想要什么                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


def print_menu():
    """打印主菜单"""
    print("""
📋 我可以帮你：

  [1] 🎨 生成角色形象（告诉我你想要什么角色）
  [2] 📐 图片分层（把你提供的图片分成Live2D图层）
  [3] 🐱 部署桌面宠物（从分层结果生成可动的桌宠）
  [4] 🚀 完整工作流（从描述到桌宠，一键完成）
  [5] ⚙️  设置（API密钥、输出目录等）
  [6] ❓ 帮助（查看使用说明）
  [0] 🚪 退出

💡 你也可以直接输入自然语言，例如："帮我做一个银发巫女"
""")


def get_input(prompt: str = "
📝 你想做什么？") -> str:
    """获取用户输入"""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\n👋 再见！")
        sys.exit(0)


def detect_intent(user_input: str) -> str:
    """
    识别用户意图
    返回: 'generate', 'layer', 'pet', 'workflow', 'settings', 'help', 'exit'
    """
    user_input_lower = user_input.lower()
    
    # 退出
    if user_input in ['0', 'exit', 'quit', '退出', '再见', 'bye']:
        return 'exit'
    
    # 生成角色
    if any(kw in user_input_lower for kw in ['生成', '创建', '做', '画', '生成角色', '1']):
        return 'generate'
    
    # 分层
    if any(kw in user_input_lower for kw in ['分层', '分割', '拆分', '图层', '2']):
        return 'layer'
    
    # 桌宠
    if any(kw in user_input_lower for kw in ['桌宠', '宠物', '桌面', '部署', '3']):
        return 'pet'
    
    # 完整工作流
    if any(kw in user_input_lower for kw in ['完整', '一键', '全部', 'workflow', '4']):
        return 'workflow'
    
    # 设置
    if any(kw in user_input_lower for kw in ['设置', '配置', 'api', '密钥', '5']):
        return 'settings'
    
    # 帮助
    if any(kw in user_input_lower for kw in ['帮助', 'help', '说明', '怎么用', '6']):
        return 'help'
    
    # 默认：如果包含角色描述特征，认为是生成请求
    character_keywords = ['少女', '少年', '女孩', '男孩', '角色', '人物', 'anime', 'girl', 'boy', 'character']
    if any(kw in user_input_lower for kw in character_keywords):
        return 'generate'
    
    return 'unknown'


def handle_generate():
    """处理角色生成请求"""
    print("\n🎨 角色生成")
    print("-" * 50)
    
    description = get_input("请描述你想要的角色（例如：银发巫女，紫色眼睛，和服）：")
    if not description:
        print("❌ 描述不能为空")
        return
    
    print(f"\n🎯 正在生成角色：{description}")
    print("⏳ 这可能需要一些时间...\n")
    
    # 调用 master_tool.py
    import subprocess
    result = subprocess.run(
        [sys.executable, 'master_tool.py', description],
        capture_output=False,
        text=True
    )
    
    if result.returncode == 0:
        print("\n✅ 角色生成完成！")
        
        # 询问是否继续分层
        continue_layer = get_input("\n是否立即进行分层？[y/n]: ").lower()
        if continue_layer in ['y', 'yes', '是']:
            handle_layer_from_output()
    else:
        print("\n❌ 生成失败，请检查网络连接或安装本地模型")


def handle_layer_from_output():
    """从输出目录找到最新图片并分层"""
    output_dir = Path('output')
    if not output_dir.exists():
        print("❌ 没有找到输出目录")
        return
    
    # 找到最新的角色图片
    images = list(output_dir.glob('*.png')) + list(output_dir.glob('*.jpg'))
    if not images:
        print("❌ 没有找到生成的图片")
        return
    
    latest_image = max(images, key=lambda p: p.stat().st_mtime)
    print(f"\n📐 对最新图片进行分层：{latest_image.name}")
    
    handle_layer_image(str(latest_image))


def handle_layer_image(image_path: str = None):
    """处理图片分层"""
    if not image_path:
        image_path = get_input("请输入图片路径：").strip().strip('"')
    
    if not os.path.exists(image_path):
        print(f"❌ 文件不存在：{image_path}")
        return
    
    print(f"\n📐 正在分层：{image_path}")
    print("⏳ 处理中...\n")
    
    import subprocess
    result = subprocess.run(
        [sys.executable, 'live2d_workflow.py', '--input', image_path, '--output', 'output/workflow'],
        capture_output=False,
        text=True
    )
    
    if result.returncode == 0:
        print("\n✅ 分层完成！")
        
        # 询问是否部署桌宠
        continue_pet = get_input("\n是否立即部署桌面宠物？[y/n]: ").lower()
        if continue_pet in ['y', 'yes', '是']:
            handle_pet_from_layer()
    else:
        print("\n❌ 分层失败")


def handle_pet_from_layer():
    """从最新的分层结果部署桌宠"""
    # 找到最新的分层目录
    output_dir = Path('output')
    layer_dirs = list(output_dir.glob('workflow/layers_*'))
    
    if not layer_dirs:
        print("❌ 没有找到分层结果")
        return
    
    latest_layer = max(layer_dirs, key=lambda p: p.stat().st_mtime)
    
    pet_name = get_input("给桌宠起个名字（默认：我的桌宠）：").strip()
    if not pet_name:
        pet_name = "我的桌宠"
    
    print(f"\n🐱 正在部署桌宠：{pet_name}")
    print("⏳ 生成动画帧...\n")
    
    import subprocess
    result = subprocess.run(
        [sys.executable, 'live2d_desktop_pet.py', '--layers-dir', str(latest_layer), '--output', f'output/pet_{pet_name}'],
        capture_output=False,
        text=True
    )
    
    if result.returncode == 0:
        print(f"\n✅ 桌宠 '{pet_name}' 部署完成！")
        print(f"📁 位置：output/pet_{pet_name}/")
        print(f"🚀 运行：python output/pet_{pet_name}/run_pet.py")
    else:
        print("\n❌ 桌宠部署失败")


def handle_workflow():
    """处理完整工作流"""
    print("\n🚀 完整工作流（描述 → 生成 → 分层 → 桌宠）")
    print("-" * 50)
    
    description = get_input("请描述你想要的角色：")
    if not description:
        print("❌ 描述不能为空")
        return
    
    pet_name = get_input("给桌宠起个名字（默认：我的桌宠）：").strip()
    if not pet_name:
        pet_name = "我的桌宠"
    
    print(f"\n🚀 开始完整工作流...")
    print(f"📝 角色描述：{description}")
    print(f"🐱 桌宠名字：{pet_name}")
    print("\n⏳ 步骤1/4：生成角色...")
    
    import subprocess
    
    # 步骤1：生成
    result = subprocess.run(
        [sys.executable, 'master_tool.py', description],
        capture_output=False,
        text=True
    )
    
    if result.returncode != 0:
        print("\n❌ 角色生成失败")
        return
    
    # 找到最新生成的图片
    output_dir = Path('output')
    images = list(output_dir.glob('*.png')) + list(output_dir.glob('*.jpg'))
    if not images:
        print("❌ 未找到生成的图片")
        return
    latest_image = max(images, key=lambda p: p.stat().st_mtime)
    
    print("\n⏳ 步骤2/4：图像优化...")
    print("⏳ 步骤3/4：智能分层...")
    
    # 步骤2-3：分层
    result = subprocess.run(
        [sys.executable, 'live2d_workflow.py', '--input', str(latest_image), '--output', 'output/workflow'],
        capture_output=False,
        text=True
    )
    
    if result.returncode != 0:
        print("\n❌ 分层失败")
        return
    
    # 找到分层目录
    layer_dirs = list(output_dir.glob('workflow/layers_*'))
    if not layer_dirs:
        print("❌ 未找到分层结果")
        return
    latest_layer = max(layer_dirs, key=lambda p: p.stat().st_mtime)
    
    print("\n⏳ 步骤4/4：部署桌宠...")
    
    # 步骤4：桌宠
    result = subprocess.run(
        [sys.executable, 'live2d_desktop_pet.py', '--layers-dir', str(latest_layer), '--output', f'output/pet_{pet_name}'],
        capture_output=False,
        text=True
    )
    
    if result.returncode == 0:
        print("\n" + "=" * 50)
        print("🎉 完整工作流完成！")
        print("=" * 50)
        print(f"🎨 角色图片：{latest_image}")
        print(f"📐 分层结果：{latest_layer}")
        print(f"🐱 桌宠位置：output/pet_{pet_name}/")
        print(f"🚀 运行命令：python output/pet_{pet_name}/run_pet.py")
        print("=" * 50)
    else:
        print("\n❌ 桌宠部署失败")


def handle_settings():
    """处理设置"""
    print("\n⚙️ 设置")
    print("-" * 50)
    print("""
[1] 设置商汤SenseNova API密钥（可选，用于高质量生成）
[2] 设置输出目录
[3] 返回主菜单
    """)
    
    choice = get_input("请选择：")
    
    if choice == '1':
        key = get_input("请输入商汤SenseNova API密钥：").strip()
        if key:
            # 保存到 .env 文件
            with open('.env', 'a', encoding='utf-8') as f:
                f.write(f"\nSENSENOVA_API_KEY={key}\n")
            print("✅ API密钥已保存")
            # 设置权限（Unix）
            try:
                os.chmod('.env', 0o600)
            except:
                pass
    elif choice == '2':
        dir_path = get_input("请输入输出目录路径（默认：./output）：").strip()
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
            with open('.env', 'a', encoding='utf-8') as f:
                f.write(f"\nOUTPUT_DIR={dir_path}\n")
            print(f"✅ 输出目录已设置为：{dir_path}")


def handle_help():
    """显示帮助"""
    print("""
📖 Live2D Master Agent 使用指南

🎯 快速开始：
   直接输入你想要的角色描述，例如：
   - "帮我做一个粉色头发的猫耳少女"
   - "生成一个机甲风格的少年角色"
   - "我要一个穿和服的巫女"

📋 功能菜单：
   [1] 生成角色 - AI生成角色立绘
   [2] 图片分层 - 将图片分成Live2D图层
   [3] 部署桌宠 - 从分层结果生成桌面宠物
   [4] 完整工作流 - 从描述到桌宠一键完成
   [5] 设置 - 配置API密钥和输出目录

💡 提示：
   - 不需要API密钥也可以使用（使用免费在线服务）
   - 提供API密钥可以获得更高质量的生成结果
   - 生成的文件保存在 output/ 目录

🔧 常见问题：
   Q: 生成失败怎么办？
   A: 检查网络连接，或安装本地模型（pip install diffusers transformers torch）
   
   Q: 如何获得商汤API密钥？
   A: 访问 https://platform.sensenova.cn 注册获取
""")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Live2D Master Agent')
    parser.add_argument('--quick', '-q', help='快速模式：直接生成角色（例如：-q "猫耳少女"）')
    parser.add_argument('--layer', '-l', help='快速分层：指定图片路径')
    parser.add_argument('--pet', '-p', help='快速部署桌宠：指定分层目录')
    parser.add_argument('--workflow', '-w', help='完整工作流：指定角色描述')
    args = parser.parse_args()
    
    # 快速模式
    if args.quick:
        print(f"🚀 快速生成：{args.quick}")
        import subprocess
        subprocess.run([sys.executable, 'master_tool.py', args.quick])
        return
    
    if args.layer:
        handle_layer_image(args.layer)
        return
    
    if args.pet:
        handle_pet_from_path(args.pet)
        return
    
    if args.workflow:
        description = args.workflow
        pet_name = "我的桌宠"
        print(f"🚀 完整工作流：{description}")
        # 简化版完整工作流
        import subprocess
        subprocess.run([sys.executable, 'master_tool.py', description])
        return
    
    # 交互式模式
    print_banner()
    
    while True:
        print_menu()
        user_input = get_input()
        
        if not user_input:
            continue
        
        intent = detect_intent(user_input)
        
        if intent == 'exit':
            print("\n👋 感谢使用 Live2D Master Agent，再见！")
            break
        elif intent == 'generate':
            # 如果用户输入包含描述，直接使用
            if len(user_input) > 10 and not user_input.isdigit():
                print(f"\n🎨 生成角色：{user_input}")
                import subprocess
                subprocess.run([sys.executable, 'master_tool.py', user_input])
            else:
                handle_generate()
        elif intent == 'layer':
            handle_layer_image()
        elif intent == 'pet':
            handle_pet_from_layer()
        elif intent == 'workflow':
            handle_workflow()
        elif intent == 'settings':
            handle_settings()
        elif intent == 'help':
            handle_help()
        else:
            print("\n🤔 我不太明白你的意思...")
            print("你可以：")
            print("  - 直接描述角色（例如：'粉色头发的少女'）")
            print("  - 输入数字选择功能（1-6）")
            print("  - 输入 '帮助' 查看详细说明")


def handle_pet_from_path(layer_path: str):
    """从指定路径部署桌宠"""
    if not os.path.exists(layer_path):
        print(f"❌ 路径不存在：{layer_path}")
        return
    
    pet_name = get_input("给桌宠起个名字（默认：我的桌宠）：").strip() or "我的桌宠"
    
    import subprocess
    result = subprocess.run(
        [sys.executable, 'live2d_desktop_pet.py', '--layers-dir', layer_path, '--output', f'output/pet_{pet_name}'],
        capture_output=False,
        text=True
    )
    
    if result.returncode == 0:
        print(f"\n✅ 桌宠 '{pet_name}' 部署完成！")


if __name__ == '__main__':
    main()
