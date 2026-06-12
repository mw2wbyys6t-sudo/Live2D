#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Live2D Master Agent - Interactive CLI Entry Point
Just run this script and the Agent will guide you through all operations

Usage:
    python live2d_agent.py

Supports natural language conversation, e.g.:
    - "I want a cat girl"
    - "Generate a mecha character"
    - "Deploy desktop pet"
    - "Use my image"

Note: Agent interface is in English for terminal compatibility.
You can describe characters in any language (English recommended for terminals).
"""

import sys
import os
import argparse
from pathlib import Path

# 确保可以导入同级模块
sys.path.insert(0, str(Path(__file__).parent))


def print_banner():
    """打印欢迎界面"""
    print(r"""
============================================================

     Live2D Master Agent v7.1
     Your Live2D Assistant - Tell me what you want

============================================================
""")


def print_menu():
    """打印主菜单（英文，兼容终端）"""
    print("""
[1] Generate Character  - Generate a character from description
[2] Layer Separation    - Split image into Live2D layers
[3] Desktop Pet         - Deploy as animated desktop pet
[4] Full Workflow       - Generate + Layer + Pet in one go
[5] Settings            - API keys, output directory
[6] Help                - Usage guide
[0] Exit                - Quit

Tip: You can also type English commands directly:
     "generate a cat girl" / "layer my image" / "deploy pet"
""")


def get_input(prompt: str = "\nEnter your choice (0-6 or command): ") -> str:
    """Get user input"""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\n👋 Goodbye!")
        sys.exit(0)


def detect_intent(user_input: str) -> str:
    """
    Detect user intent
    Returns: 'generate', 'layer', 'pet', 'workflow', 'settings', 'help', 'exit'
    Supports both English and Chinese keywords for terminal compatibility
    """
    user_input_lower = user_input.lower().strip()

    # Exit
    if user_input in ['0', 'exit', 'quit', 'q', 'bye', 'goodbye', '退出', '再见']:
        return 'exit'

    # Generate character
    if any(kw in user_input_lower for kw in [
        'generate', 'create', 'make', 'draw', 'gen', 'g ', '生成', '创建', '做', '画', '生成角色', '1'
    ]):
        return 'generate'

    # Layer separation
    if any(kw in user_input_lower for kw in [
        'layer', 'separate', 'split', 'layers', '分层', '分割', '拆分', '图层', '2'
    ]):
        return 'layer'

    # Desktop pet
    if any(kw in user_input_lower for kw in [
        'pet', 'desktop', 'deploy', '桌宠', '宠物', '桌面', '部署', '3'
    ]):
        return 'pet'

    # Full workflow
    if any(kw in user_input_lower for kw in [
        'workflow', 'full', 'all', 'complete', '一键', '完整', '全部', '4'
    ]):
        return 'workflow'

    # Settings
    if any(kw in user_input_lower for kw in [
        'settings', 'config', 'setup', 'key', 'api', '设置', '配置', '密钥', '5'
    ]):
        return 'settings'

    # Help
    if any(kw in user_input_lower for kw in [
        'help', 'h', 'how', 'usage', 'guide', '帮助', '说明', '怎么用', '6'
    ]):
        return 'help'

    # Default: if contains character description keywords, treat as generate
    character_keywords = [
        'anime', 'girl', 'boy', 'character', 'cat', 'maid', 'witch', 'knight',
        '少女', '少年', '女孩', '男孩', '角色', '人物', '猫娘', '女仆', '巫女'
    ]
    if any(kw in user_input_lower for kw in character_keywords):
        return 'generate'

    return 'unknown'


def handle_generate():
    """Handle character generation request"""
    print("\n🎨 Character Generation")
    print("-" * 50)

    description = get_input("Describe your character (e.g., silver hair witch, purple eyes, kimono): ")
    if not description:
        print("❌ Description cannot be empty")
        return

    print(f"\n🎯 Generating character: {description}")
    print("⏳ This may take a while...\n")

    # Call master_tool.py
    import subprocess
    result = subprocess.run(
        [sys.executable, 'master_tool.py', description],
        capture_output=False,
        text=True
    )

    if result.returncode == 0:
        print("\n✅ Character generated successfully!")

        # Ask if continue to layer separation
        continue_layer = get_input("\nLayer separation now? [y/n]: ").lower()
        if continue_layer in ['y', 'yes']:
            handle_layer_from_output()
    else:
        print("\n❌ Generation failed. Check network or install local model")


def handle_layer_from_output():
    """Find latest image in output dir and layer it"""
    output_dir = Path('output')
    if not output_dir.exists():
        print("❌ Output directory not found")
        return

    # Find latest character image
    images = list(output_dir.glob('*.png')) + list(output_dir.glob('*.jpg'))
    if not images:
        print("❌ No generated images found")
        return

    latest_image = max(images, key=lambda p: p.stat().st_mtime)
    print(f"\n📐 Layering latest image: {latest_image.name}")

    handle_layer_image(str(latest_image))


def handle_layer_image(image_path: str = None):
    """Handle image layer separation"""
    if not image_path:
        image_path = get_input("Enter image path: ").strip().strip('"')

    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return

    print(f"\n📐 Layering: {image_path}")
    print("⏳ Processing...\n")

    import subprocess
    result = subprocess.run(
        [sys.executable, 'live2d_workflow.py', '--input', image_path, '--output', 'output/workflow'],
        capture_output=False,
        text=True
    )

    if result.returncode == 0:
        print("\n✅ Layer separation complete!")

        # Ask if deploy desktop pet
        continue_pet = get_input("\nDeploy desktop pet now? [y/n]: ").lower()
        if continue_pet in ['y', 'yes']:
            handle_pet_from_layer()
    else:
        print("\n❌ Layer separation failed")


def handle_pet_from_layer():
    """Deploy desktop pet from latest layer output"""
    # Find latest layer directory
    output_dir = Path('output')
    layer_dirs = list(output_dir.glob('workflow/layers_*'))

    if not layer_dirs:
        print("❌ No layer results found")
        return

    latest_layer = max(layer_dirs, key=lambda p: p.stat().st_mtime)

    pet_name = get_input("Name your pet (default: MyPet): ").strip()
    if not pet_name:
        pet_name = "MyPet"

    print(f"\n🐱 Deploying pet: {pet_name}")
    print("⏳ Generating animation frames...\n")

    import subprocess
    result = subprocess.run(
        [sys.executable, 'live2d_desktop_pet.py', '--layers-dir', str(latest_layer), '--output', f'output/pet_{pet_name}'],
        capture_output=False,
        text=True
    )

    if result.returncode == 0:
        print(f"\n✅ Pet '{pet_name}' deployed!")
        print(f"📁 Location: output/pet_{pet_name}/")
        print(f"🚀 Run: python output/pet_{pet_name}/run_pet.py")
    else:
        print("\n❌ Pet deployment failed")


def handle_workflow():
    """Handle full workflow"""
    print("\n🚀 Full Workflow (Describe → Generate → Layer → Pet)")
    print("-" * 50)

    description = get_input("Describe your character: ")
    if not description:
        print("❌ Description cannot be empty")
        return

    pet_name = get_input("Name your pet (default: MyPet): ").strip()
    if not pet_name:
        pet_name = "MyPet"

    print(f"\n🚀 Starting full workflow...")
    print(f"📝 Character: {description}")
    print(f"🐱 Pet name: {pet_name}")
    print("\n⏳ Step 1/4: Generating character...")

    import subprocess

    # Step 1: Generate
    result = subprocess.run(
        [sys.executable, 'master_tool.py', description],
        capture_output=False,
        text=True
    )

    if result.returncode != 0:
        print("\n❌ Character generation failed")
        return

    # Find latest generated image
    output_dir = Path('output')
    images = list(output_dir.glob('*.png')) + list(output_dir.glob('*.jpg'))
    if not images:
        print("❌ No generated images found")
        return
    latest_image = max(images, key=lambda p: p.stat().st_mtime)

    print("\n⏳ Step 2/4: Image optimization...")
    print("⏳ Step 3/4: Smart layering...")

    # Step 2-3: Layer
    result = subprocess.run(
        [sys.executable, 'live2d_workflow.py', '--input', str(latest_image), '--output', 'output/workflow'],
        capture_output=False,
        text=True
    )

    if result.returncode != 0:
        print("\n❌ Layer separation failed")
        return

    # Find layer directory
    layer_dirs = list(output_dir.glob('workflow/layers_*'))
    if not layer_dirs:
        print("❌ No layer results found")
        return
    latest_layer = max(layer_dirs, key=lambda p: p.stat().st_mtime)

    print("\n⏳ Step 4/4: Deploying pet...")

    # Step 4: Pet
    result = subprocess.run(
        [sys.executable, 'live2d_desktop_pet.py', '--layers-dir', str(latest_layer), '--output', f'output/pet_{pet_name}'],
        capture_output=False,
        text=True
    )

    if result.returncode == 0:
        print("\n" + "=" * 50)
        print("🎉 Full workflow complete!")
        print("=" * 50)
        print(f"🎨 Character image: {latest_image}")
        print(f"📐 Layer result: {latest_layer}")
        print(f"🐱 Pet location: output/pet_{pet_name}/")
        print(f"🚀 Run command: python output/pet_{pet_name}/run_pet.py")
        print("=" * 50)
    else:
        print("\n❌ Pet deployment failed")


def handle_settings():
    """Handle settings"""
    print("\n⚙️ Settings")
    print("-" * 50)
    print("""
[1] Set SenseNova API key (optional, for high quality generation)
[2] Set output directory
[3] Back to main menu
    """)

    choice = get_input("Select: ")

    if choice == '1':
        key = get_input("Enter SenseNova API key: ").strip()
        if key:
            # Save to .env file
            with open('.env', 'a', encoding='utf-8') as f:
                f.write(f"\nSENSENOVA_API_KEY={key}\n")
            print("✅ API key saved")
            # Set permission (Unix)
            try:
                os.chmod('.env', 0o600)
            except:
                pass
    elif choice == '2':
        dir_path = get_input("Enter output directory (default: ./output): ").strip()
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
            with open('.env', 'a', encoding='utf-8') as f:
                f.write(f"\nOUTPUT_DIR={dir_path}\n")
            print(f"✅ Output directory set to: {dir_path}")


def handle_help():
    """Show help"""
    print("""
📖 Live2D Master Agent Guide

🎯 Quick Start:
   Just type your character description, e.g.:
   - "cute cat girl with pink hair"
   - "mecha style boy character"
   - "witch in kimono"

📋 Menu Options:
   [1] Generate Character - AI generate character art
   [2] Layer Separation - Split image into Live2D layers
   [3] Desktop Pet - Deploy as animated desktop pet
   [4] Full Workflow - One-click from description to pet
   [5] Settings - Configure API key and output directory

💡 Tips:
   - No API key needed (uses free online services)
   - API key provides higher quality generation
   - Output files saved to output/ directory

🔧 FAQ:
   Q: Generation failed?
   A: Check network, or install local model (pip install diffusers transformers torch)

   Q: How to get SenseNova API key?
   A: Visit https://platform.sensenova.cn to register
""")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Live2D Master Agent')
    parser.add_argument('--quick', '-q', help='Quick mode: generate character (e.g., -q "cat girl")')
    parser.add_argument('--layer', '-l', help='Quick layer: specify image path')
    parser.add_argument('--pet', '-p', help='Quick deploy: specify layer directory')
    parser.add_argument('--workflow', '-w', help='Full workflow: specify character description')
    args = parser.parse_args()

    # Quick modes
    if args.quick:
        print(f"🚀 Quick generate: {args.quick}")
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
        pet_name = "MyPet"
        print(f"🚀 Full workflow: {description}")
        # Simplified full workflow
        import subprocess
        subprocess.run([sys.executable, 'master_tool.py', description])
        return

    # Interactive mode
    print_banner()

    while True:
        print_menu()
        user_input = get_input()

        if not user_input:
            continue

        intent = detect_intent(user_input)

        if intent == 'exit':
            print("\n👋 Thanks for using Live2D Master Agent. Goodbye!")
            break
        elif intent == 'generate':
            # If user input contains description, use it directly
            if len(user_input) > 10 and not user_input.isdigit():
                print(f"\n🎨 Generating character: {user_input}")
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
            print("\n🤔 I didn't understand...")
            print("You can:")
            print("  - Describe a character (e.g., 'pink hair girl')")
            print("  - Enter number to select function (1-6)")
            print("  - Type 'help' for detailed guide")


def handle_pet_from_path(layer_path: str):
    """Deploy desktop pet from specified path"""
    if not os.path.exists(layer_path):
        print(f"❌ Path not found: {layer_path}")
        return

    pet_name = get_input("Name your pet (default: MyPet): ").strip() or "MyPet"

    import subprocess
    result = subprocess.run(
        [sys.executable, 'live2d_desktop_pet.py', '--layers-dir', layer_path, '--output', f'output/pet_{pet_name}'],
        capture_output=False,
        text=True
    )

    if result.returncode == 0:
        print(f"\n✅ Pet '{pet_name}' deployed!")


if __name__ == '__main__':
    main()
