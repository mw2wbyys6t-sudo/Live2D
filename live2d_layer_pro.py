#!/usr/bin/env python3
"""
Live2D Master Agent v8.0 - Pro Layer Tool
This is now an alias for v6 K-means (the Pro/AI layering requires See-through ComfyUI).
See install_comfyui_advanced.py for See-through SIGGRAPH 2026 layering.
"""

import os
import sys
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
    from live2d.version import FULL_VERSION_STRING
    print(FULL_VERSION_STRING)
    print("\n[INFO] 'Pro' layering redirects to v6 K-means (default).")
    print("       For See-through AI layering (SIGGRAPH 2026):")
    print("       python install_comfyui_advanced.py")
    print()
    # Delegate to v6
    sys.argv[0] = "live2d_layer_v6.py"
    from live2d_layer_v6 import main as v6_main
    v6_main()


if __name__ == "__main__":
    main()
