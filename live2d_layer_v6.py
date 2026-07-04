#!/usr/bin/env python3
"""
Live2D Master Agent v9.0 - K-means Layer Separator (v6, DEFAULT)
P0-3 FIX: This is the default layer separation tool.
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
        description=f"Live2D Layer Tool v6 (K-means) - v{__version__}",
        epilog="Example: python live2d_layer_v6.py character.png --k 12"
    )
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", nargs="?", default=None, help="Output directory")
    parser.add_argument("--k", type=int, default=12, help="Number of clusters (default: 12)")
    parser.add_argument("--with-52", action="store_true", help="Generate 52-layer standard config")
    parser.add_argument("--version", "-V", action="version", version=FULL_VERSION_STRING)

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"[ERROR] File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    from live2d.layering.kmeans import layer_image_file
    print(f"\n{FULL_VERSION_STRING}")
    print(f"Layering: {args.input} (k={args.k})")

    result = layer_image_file(args.input, args.output, k_clusters=args.k)
    print(f"\n[OK] {result['layer_count']} layers created in: {result['output_dir']}")

    if args.with_52:
        from live2d.layering.layers52 import Layer52Generator
        from live2d.layering.part_identifier import PartIdentifier
        from PIL import Image

        img = Image.open(args.input).convert('RGBA')
        gen = Layer52Generator()
        pid = PartIdentifier()
        layers_with_parts = pid.identify_layers(result['layers'], img.height, img.width)
        mapping = gen.map_layers_to_standard(layers_with_parts)
        configs = gen.generate_config_files(mapping, result['output_dir'])
        print(f"[OK] 52-layer config generated: {configs.get('guide', '')}")


if __name__ == "__main__":
    main()
