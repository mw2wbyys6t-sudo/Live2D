#!/usr/bin/env python3
"""
Live2D Master Agent v9.0 - Main Image Generation + Layer Tool
P0-3 FIX: Uses K-means v6 layerer by default (not layer_pro)
P2-3 FIX: Supports --version flag
P1-1 FIX: Proper imports, no circular dependencies
"""

import os
import sys
import argparse
from pathlib import Path

# Fix encoding for Windows terminals
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

    parser = argparse.ArgumentParser(
        description=f"Live2D Master Agent v{__version__} - AI Character Image Generator + Layer Separator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python master_tool.py "cute anime girl with pink hair"
  python master_tool.py "blue hair cat girl" --width 1024 --height 1024
  python master_tool.py "anime boy" --provider pollinations
  python master_tool.py --input character.png --layer-only
  python master_tool.py --list-providers
        """
    )
    parser.add_argument("prompt", nargs="?", default="", help="Character description")
    parser.add_argument("--width", "-W", type=int, default=1024, help="Image width")
    parser.add_argument("--height", "-H", type=int, default=1024, help="Image height")
    parser.add_argument("--output", "-o", help="Output image path")
    parser.add_argument("--provider", "-p",
                        choices=["auto", "pollinations", "sensenova", "seedream"],
                        default="auto", help="Image provider")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--layer-only", action="store_true",
                        help="Only run layer separation on --input image")
    parser.add_argument("--input", "-i", help="Input image for layering (skip generation)")
    parser.add_argument("--k", type=int, default=12, help="K-means clusters (default: 12)")
    parser.add_argument("--version", "-V", action="version", version=FULL_VERSION_STRING)
    parser.add_argument("--list-providers", action="store_true", help="List available providers")
    parser.add_argument("--no-layer", action="store_true", help="Skip layer separation")
    parser.add_argument("--rig", action="store_true",
                        help="Run automatic rigging after layer separation")
    parser.add_argument("--pet", action="store_true",
                        help="Generate desktop pet package (full workflow)")
    parser.add_argument("--layer-method", choices=["semantic", "kmeans"],
                        default="semantic", help="Layer separation method")

    args = parser.parse_args()

    if args.list_providers:
        from live2d.image_gen.router import get_router
        router = get_router()
        print(f"\n{FULL_VERSION_STRING}")
        print("\nAvailable providers:")
        for info in router.get_provider_info():
            status = "READY" if info.get("available") else "NOT CONFIGURED"
            key_note = " (free)" if not info.get("requires_key") else " (requires API key)"
            print(f"  [{status}] {info.get('display_name', info['name'])}{key_note}")
        print("\nFree provider (Pollinations.ai) works without any API key.")
        return

    if args.layer_only:
        if not args.input:
            parser.error("--layer-only requires --input <image_path>")
        if args.layer_method == "semantic":
            from live2d.layering.semantic import layer_image_file
        else:
            from live2d.layering.kmeans import layer_image_file
        result = layer_image_file(args.input, args.output)
        print(f"\nLayer separation complete: {result['layer_count']} layers")

        if args.rig:
            print("\nRunning automatic rigging...")
            from collections import OrderedDict
            from live2d.rigging.pipeline import RiggingPipeline
            from PIL import Image as _PI
            layers = OrderedDict()
            for info in result["layers"]:
                path = info["path"]
                name = info.get("name") or Path(path).stem
                layers[name] = _PI.open(path)
            rig_result = RiggingPipeline().run(
                layers,
                output_dir=str(Path(result["output_dir"]) / "rigged"),
                character_name="character",
            )
            print(f"[OK] Rigged output: {rig_result['output_dir']}")
            print(f"     model3.json: {rig_result['model3_json']}")

        print(f"Output: {result['output_dir']}")
        return

    if not args.prompt:
        parser.print_help()
        print("\nError: Provide a prompt or use --input with --layer-only", file=sys.stderr)
        sys.exit(1)

    if args.pet:
        from live2d.workflow import WorkflowEngine
        from live2d.logger import get_logger
        log = get_logger("master_tool")
        log.section(FULL_VERSION_STRING)
        
        provider = None if args.provider == "auto" else args.provider
        out_dir = args.output or str(Path(_PROJECT_ROOT) / "output")
        
        engine = WorkflowEngine(
            output_dir=out_dir,
            k_clusters=args.k,
            provider=provider,
            width=args.width,
            height=args.height,
            layer_method=args.layer_method,
        )
        result = engine.run(
            prompt=args.prompt,
            deploy_desktop=True,
        )
        
        if result.get("success"):
            pet_info = result.get("steps", {}).get("pet", {})
            print(f"\n[OK] Desktop pet generated!")
            if pet_info.get("package_dir"):
                print(f"     Package: {pet_info['package_dir']}")
                print(f"     Run: {Path(pet_info['package_dir']) / 'run_pet.sh'}")
            print(f"     Output dir: {result.get('output_dir')}")
        else:
            print(f"\n[ERROR] Failed: {result.get('error', 'Unknown error')}", file=sys.stderr)
            sys.exit(1)
        return

    from live2d.image_gen.router import get_router
    from live2d.logger import get_logger
    log = get_logger("master_tool")
    log.section(FULL_VERSION_STRING)

    router = get_router()
    available = router.get_available_providers()
    if not available:
        print("ERROR: No image providers available. Check internet connection.", file=sys.stderr)
        sys.exit(1)

    print(f"Using: {', '.join(p['name'] for p in available)}")
    print(f"Prompt: {args.prompt[:80]}")

    output_path = args.output
    import time as _time
    if not output_path:
        out_dir = Path(_PROJECT_ROOT) / "output"
        out_dir.mkdir(exist_ok=True)
        output_path = str(out_dir / f"generated_{int(_time.time())}.png")

    try:
        provider = None if args.provider == "auto" else args.provider
        result = router.generate(
            prompt=args.prompt,
            output_path=output_path,
            width=args.width,
            height=args.height,
            provider=provider,
            seed=args.seed,
        )
        print(f"\n[OK] Image saved: {result.image_path}")
        print(f"     Provider: {result.provider} ({result.model})")
        print(f"     Time: {result.elapsed_seconds:.1f}s")

        if not args.no_layer:
            print(f"\nRunning {args.layer_method} layer separation...")
            if args.layer_method == "semantic":
                from live2d.layering.semantic import layer_image_file
            else:
                from live2d.layering.kmeans import layer_image_file
            layer_result = layer_image_file(result.image_path, k_clusters=args.k)
            print(f"[OK] {layer_result['layer_count']} layers in {layer_result['output_dir']}")

    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
