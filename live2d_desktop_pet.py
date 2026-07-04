#!/usr/bin/env python3
"""
Live2D Master Agent v9.0 - Desktop Pet Creator & Runner
P1-3 FIX: Generated pet uses script-relative paths (works from any directory)
"""

import os
import sys
import argparse
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

_PROJECT_ROOT = str(Path(__file__).resolve().parent)
os.environ.setdefault("LIVE2D_PROJECT_ROOT", _PROJECT_ROOT)
sys.path.insert(0, _PROJECT_ROOT)


def main():
    from live2d.version import FULL_VERSION_STRING, __version__

    parser = argparse.ArgumentParser(
        description=f"Live2D Master Agent v{__version__} - Desktop Pet",
    )
    parser.add_argument("--layers-dir", "-d", required=True, help="Directory containing layer PNGs")
    parser.add_argument("--output", "-o", help="Output pet package directory")
    parser.add_argument("--name", "-n", default="live2d_pet", help="Pet name")
    parser.add_argument("--run", action="store_true", help="Run pet immediately after creating")
    parser.add_argument("--version", "-V", action="version", version=FULL_VERSION_STRING)

    args = parser.parse_args()

    layers_dir = args.layers_dir
    if not os.path.isdir(layers_dir):
        print(f"[ERROR] Layers directory not found: {layers_dir}", file=sys.stderr)
        sys.exit(1)

    from live2d.pet.animator import DesktopPetAnimator, create_pet_package
    print(f"\n{FULL_VERSION_STRING}")
    print(f"Creating desktop pet from: {layers_dir}")

    try:
        result = create_pet_package(layers_dir, args.output, args.name)
        if result["success"]:
            print(f"\n[OK] Pet package created: {result['package_dir']}")
            print(f"     Run with: cd {result['package_dir']} && python run_pet.py")
            print(f"     Or double-click run_pet.bat (Windows)")

            if args.run:
                print("\nStarting pet...")
                from live2d.pet.runner import PetRunner
                runner = PetRunner(layers_dir)
                runner.run()
        else:
            print(f"[ERROR] {result.get('error', 'Unknown error')}", file=sys.stderr)
            sys.exit(1)
    except ImportError:
        print("[ERROR] pygame not installed. Run: pip install pygame", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
