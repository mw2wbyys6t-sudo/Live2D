#!/usr/bin/env python3
"""
Live2D Master Agent v9.0 - Interactive CLI Agent
Menu-driven interactive interface for the full Live2D pipeline.
"""

import os
import sys
import time
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

_PROJECT_ROOT = str(Path(__file__).resolve().parent)
os.environ.setdefault("LIVE2D_PROJECT_ROOT", _PROJECT_ROOT)
sys.path.insert(0, _PROJECT_ROOT)


def print_banner():
    from live2d.version import FULL_VERSION_STRING
    print()
    print("=" * 60)
    print(f"  {FULL_VERSION_STRING}")
    print("  AI-Powered Live2D Character Creation Pipeline")
    print("=" * 60)


def print_menu():
    print("""
Commands:
  1. Generate character image + auto-layer (full pipeline)
  2. Generate image only
  3. Layer an existing image
  4. Create desktop pet from layers
  5. Quality check an image/PSD
  6. Configure API keys
  7. List available providers
  0. Exit

Or type a natural language prompt directly (e.g. "cute pink hair anime girl")
""")


def cmd_full_pipeline():
    from live2d.workflow import WorkflowEngine
    prompt = input("Character description: ").strip()
    if not prompt:
        print("Cancelled.")
        return
    k = input("K-means clusters [12]: ").strip()
    k_clusters = int(k) if k.isdigit() else 12
    deploy = input("Create desktop pet? [y/N]: ").strip().lower() == 'y'

    engine = WorkflowEngine(k_clusters=k_clusters)
    result = engine.run(prompt=prompt, deploy_desktop=deploy)
    if result["success"]:
        print(f"\n[SUCCESS] Layers: {result.get('layers_dir', '')}")
    else:
        print(f"\n[FAILED] {result.get('error', 'Unknown error')}")


def cmd_generate_only():
    from live2d.image_gen.router import get_router
    prompt = input("Character description: ").strip()
    if not prompt:
        print("Cancelled.")
        return
    router = get_router()
    out_dir = Path(_PROJECT_ROOT) / "output"
    out_dir.mkdir(exist_ok=True)
    out_path = str(out_dir / f"generated_{int(time.time())}.png")
    try:
        result = router.generate(prompt=prompt, output_path=out_path)
        print(f"\n[OK] Saved: {result.image_path}")
    except Exception as e:
        print(f"[ERROR] {e}")


def cmd_layer_existing():
    from live2d.layering.kmeans import layer_image_file
    path = input("Path to image: ").strip()
    if not path or not os.path.isfile(path):
        print("File not found.")
        return
    k = input("K-means clusters [12]: ").strip()
    k_clusters = int(k) if k.isdigit() else 12
    result = layer_image_file(path, k_clusters=k_clusters)
    print(f"\n[OK] {result['layer_count']} layers in: {result['output_dir']}")


def cmd_create_pet():
    from live2d.pet.animator import create_pet_package
    layers_dir = input("Path to layers directory: ").strip()
    if not layers_dir or not os.path.isdir(layers_dir):
        print("Directory not found.")
        return
    name = input("Pet name [live2d_pet]: ").strip() or "live2d_pet"
    result = create_pet_package(layers_dir, pet_name=name)
    if result.get("success"):
        print(f"\n[OK] Pet package: {result['package_dir']}")
        print(f"     Run: cd {result['package_dir']} && python run_pet.py")
    else:
        print(f"[ERROR] {result.get('error', 'Unknown error')}")


def cmd_quality_check():
    from live2d.qa.engine import QAEngine
    from live2d.psd.validator import PSDValidator
    from PIL import Image

    path = input("Path to image or PSD: ").strip()
    if not path or not os.path.exists(path):
        print("File not found.")
        return

    ext = Path(path).suffix.lower()
    if ext == '.psd':
        validator = PSDValidator()
        result = validator.validate(path)
    else:
        engine = QAEngine()
        img = Image.open(path).convert('RGBA')
        result = engine.assess_image(img)
        result = result.to_dict()

    print(f"\nQA Result: {'PASS' if result.get('valid', result.get('score', 0) >= 60) else 'FAIL'}")
    print(f"Score: {result.get('score', '?')}/100")
    for issue in result.get("issues", []):
        sev = issue.get("severity", "info").upper()
        print(f"  [{sev}] {issue.get('message', '')}")


def cmd_config():
    from config_api import main as config_main
    config_main()


def cmd_list_providers():
    from live2d.image_gen.router import get_router
    router = get_router()
    print("\nAvailable providers:")
    for info in router.get_provider_info():
        status = "READY" if info.get("available") else "NOT SET UP"
        key_note = " (free)" if not info.get("requires_key") else " (needs API key)"
        print(f"  [{status}] {info.get('display_name', info['name'])}{key_note}")
    print("\nPollinations.ai is free and always available.")


def main():
    print_banner()

    # Check imports work
    try:
        from live2d.image_gen.router import get_router
        router = get_router()
        available = [p["name"] for p in router.get_available_providers()]
        print(f"\n  Ready. Providers: {', '.join(available) or 'none (check internet)'}")
    except Exception as e:
        print(f"\n  Warning: {e}")

    while True:
        print_menu()
        try:
            choice = input("live2d> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not choice:
            continue
        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            cmd_full_pipeline()
        elif choice == "2":
            cmd_generate_only()
        elif choice == "3":
            cmd_layer_existing()
        elif choice == "4":
            cmd_create_pet()
        elif choice == "5":
            cmd_quality_check()
        elif choice == "6":
            cmd_config()
        elif choice == "7":
            cmd_list_providers()
        elif not choice[0].isdigit():
            # Treat as natural language prompt
            from live2d.workflow import WorkflowEngine
            engine = WorkflowEngine()
            result = engine.run(prompt=choice)
            if result["success"]:
                print(f"\n[SUCCESS] {result.get('layers_dir', '')}")
            else:
                print(f"\n[FAILED] {result.get('error', '')}")
        else:
            print("Unknown option.")


if __name__ == "__main__":
    main()
