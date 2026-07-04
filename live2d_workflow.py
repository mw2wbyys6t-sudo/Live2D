#!/usr/bin/env python3
"""
Live2D Master Agent v9.0 - End-to-End Workflow
Pipeline: Generate → QA → Optimize → Layer → PSD → 52-layer config → Pet
"""

import os
import sys
import argparse
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


def main():
    from live2d.version import FULL_VERSION_STRING, __version__
    from live2d.workflow import WorkflowEngine

    parser = argparse.ArgumentParser(
        description=f"Live2D Master Agent v{__version__} - Complete Workflow Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python live2d_workflow.py "cute anime girl"
  python live2d_workflow.py -i character.png
  python live2d_workflow.py "cat girl" --deploy-desktop --k 12
  python live2d_workflow.py "anime boy" -o output/my_character
        """
    )
    parser.add_argument("prompt", nargs="?", default="", help="Character description")
    parser.add_argument("--input", "-i", help="Input image path (skip generation)")
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--deploy-desktop", action="store_true", help="Create desktop pet package")
    parser.add_argument("--k", type=int, default=12, help="K-means clusters (default: 12)")
    parser.add_argument("--provider", "-p",
                        choices=["auto", "pollinations", "sensenova", "seedream"],
                        default="auto", help="Image provider")
    parser.add_argument("--width", "-W", type=int, default=1024)
    parser.add_argument("--height", "-H", type=int, default=1024)
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--version", "-V", action="version", version=FULL_VERSION_STRING)

    args = parser.parse_args()

    if not args.prompt and not args.input:
        parser.print_help()
        print("\nError: Provide a prompt or --input image path", file=sys.stderr)
        sys.exit(1)

    provider = None if args.provider == "auto" else args.provider
    engine = WorkflowEngine(
        output_dir=args.output,
        k_clusters=args.k,
        provider=provider,
        width=args.width,
        height=args.height,
    )

    result = engine.run(
        prompt=args.prompt,
        input_image=args.input,
        deploy_desktop=args.deploy_desktop,
        seed=args.seed,
    )

    if result["success"]:
        print(f"\n[SUCCESS] Output: {result.get('layers_dir', '')}")
        if args.deploy_desktop and "pet" in result.get("steps", {}):
            pet = result["steps"]["pet"]
            if pet.get("success"):
                print(f"[PET] Package: {pet.get('package_dir', '')}")
        sys.exit(0)
    else:
        print(f"\n[FAILED] {result.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
