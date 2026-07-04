#!/usr/bin/env python3
"""
Live2D Test Image Generator
Generate a simple test character image for layer separation tool testing.

Usage:
    python create_test_image.py                    # default: output/test_character.png (512x512)
    python create_test_image.py -o my_char.png     # custom output filename (relative to output/)
    python create_test_image.py -s 1024            # custom size (1024x1024)
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("[ERROR] Pillow is required. Install it with: pip install Pillow")
    sys.exit(1)


def _get_project_root() -> Path:
    """返回项目根目录。根目录包装器通过 LIVE2D_PROJECT_ROOT 指定。"""
    return Path(os.environ.get("LIVE2D_PROJECT_ROOT", Path(__file__).parent))


def create_test_character(size: int = 512, output: str = "test_character.png"):
    """Generate a simple test character image with distinct color regions
    suitable for testing K-means / color-detection layer separation."""

    project_root = _get_project_root()
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / output

    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    u = size / 512  # unit scale

    # --- Hair (pink) ---
    draw.ellipse(
        [cx - 130 * u, cy - 200 * u, cx + 130 * u, cy - 20 * u],
        fill=(255, 182, 193, 255),
    )
    # Side hair strands
    draw.polygon(
        [
            (cx - 120 * u, cy - 80 * u),
            (cx - 150 * u, cy + 80 * u),
            (cx - 80 * u, cy + 60 * u),
        ],
        fill=(255, 160, 180, 255),
    )
    draw.polygon(
        [
            (cx + 120 * u, cy - 80 * u),
            (cx + 150 * u, cy + 80 * u),
            (cx + 80 * u, cy + 60 * u),
        ],
        fill=(255, 160, 180, 255),
    )

    # --- Face (skin tone) ---
    draw.ellipse(
        [cx - 90 * u, cy - 120 * u, cx + 90 * u, cy + 40 * u],
        fill=(255, 228, 196, 255),
    )

    # --- Eyes (blue) ---
    eye_y = cy - 40 * u
    for ex in [cx - 35 * u, cx + 35 * u]:
        # White
        draw.ellipse(
            [ex - 18 * u, eye_y - 12 * u, ex + 18 * u, eye_y + 12 * u],
            fill=(255, 255, 255, 255),
        )
        # Iris
        draw.ellipse(
            [ex - 10 * u, eye_y - 10 * u, ex + 10 * u, eye_y + 10 * u],
            fill=(70, 130, 230, 255),
        )
        # Pupil
        draw.ellipse(
            [ex - 5 * u, eye_y - 5 * u, ex + 5 * u, eye_y + 5 * u],
            fill=(20, 20, 60, 255),
        )
        # Highlight
        draw.ellipse(
            [ex - 2 * u, eye_y - 7 * u, ex + 4 * u, eye_y - 1 * u],
            fill=(255, 255, 255, 255),
        )

    # --- Mouth (small red arc) ---
    draw.arc(
        [cx - 15 * u, cy + 5 * u, cx + 15 * u, cy + 25 * u],
        start=0,
        end=180,
        fill=(220, 80, 80, 255),
        width=max(2, int(3 * u)),
    )

    # --- Neck ---
    draw.rectangle(
        [cx - 20 * u, cy + 35 * u, cx + 20 * u, cy + 65 * u],
        fill=(255, 228, 196, 255),
    )

    # --- Body / Clothes (school uniform — dark blue) ---
    body_top = cy + 60 * u
    draw.polygon(
        [
            (cx - 80 * u, body_top),
            (cx + 80 * u, body_top),
            (cx + 110 * u, cy + 220 * u),
            (cx - 110 * u, cy + 220 * u),
        ],
        fill=(50, 60, 120, 255),
    )
    # Collar (white)
    draw.polygon(
        [
            (cx - 40 * u, body_top),
            (cx, body_top + 50 * u),
            (cx + 40 * u, body_top),
        ],
        fill=(255, 255, 255, 255),
    )
    # Ribbon (red)
    draw.polygon(
        [
            (cx - 12 * u, body_top + 10 * u),
            (cx, body_top + 40 * u),
            (cx + 12 * u, body_top + 10 * u),
        ],
        fill=(200, 50, 50, 255),
    )

    # --- Arms ---
    draw.polygon(
        [
            (cx - 80 * u, body_top + 10 * u),
            (cx - 130 * u, cy + 200 * u),
            (cx - 100 * u, cy + 200 * u),
            (cx - 60 * u, body_top + 30 * u),
        ],
        fill=(50, 60, 120, 255),
    )
    draw.polygon(
        [
            (cx + 80 * u, body_top + 10 * u),
            (cx + 130 * u, cy + 200 * u),
            (cx + 100 * u, cy + 200 * u),
            (cx + 60 * u, body_top + 30 * u),
        ],
        fill=(50, 60, 120, 255),
    )

    # --- Hands (skin tone) ---
    draw.ellipse(
        [cx - 140 * u, cy + 190 * u, cx - 95 * u, cy + 220 * u],
        fill=(255, 228, 196, 255),
    )
    draw.ellipse(
        [cx + 95 * u, cy + 190 * u, cx + 140 * u, cy + 220 * u],
        fill=(255, 228, 196, 255),
    )

    # Save
    img.save(output_path, "PNG")
    abs_path = output_path.resolve()
    print(f"[OK] Test character image saved: {abs_path}")
    print(f"     Size: {size}x{size}px, transparent background")
    print(f"     Regions: hair(pink), face(skin), eyes(blue), clothes(navy), ribbon(red)")
    print()
    print("Next step — test layer separation:")
    print(f"  python live2d_layer_v6.py {abs_path}")
    return str(abs_path)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a test character image for Live2D layer separation testing."
    )
    parser.add_argument(
        "-o", "--output", default="test_character.png", help="Output filename under output/ (default: test_character.png)"
    )
    parser.add_argument(
        "-s", "--size", type=int, default=512, help="Image size in pixels (default: 512)"
    )
    args = parser.parse_args()
    create_test_character(args.size, args.output)


if __name__ == "__main__":
    main()
