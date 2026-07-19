#!/usr/bin/env python3
"""
Live2D Master Agent - Desktop Pet Animator (P1-3 FIXED: script-relative paths)

P1-3 FIX: run_pet.py uses script directory (__file__) to locate resources,
so the pet package can be moved to any directory and still find its layers.

Generates a self-contained pet package with:
- Animated swing, breathing, blinking, expressions
- Click/drag interaction
- Self-contained run_pet.py + run_pet.bat
"""

import os
import sys
import math
import time
import json
import shutil
from pathlib import Path
from typing import Optional, Dict, List, Tuple

from PIL import Image
import numpy as np

from live2d.logger import get_logger
from live2d.security import sanitize_filename, validate_directory

log = get_logger("pet")


class DesktopPetAnimator:
    """Creates animated desktop pet from layered PNGs."""

    # Animation configuration
    ANIMATION_CONFIG = {
        "fps": 60,
        "body_swing_amplitude": 3.0,
        "body_swing_speed": 0.8,
        "breath_amplitude": 1.5,
        "breath_speed": 0.4,
        "blink_interval_min": 3.0,
        "blink_interval_max": 6.0,
        "blink_duration": 0.15,
        "hair_swing_multiplier": 1.8,
        "expression_change_interval": 10.0,
    }

    # Part group definitions for animation (English keyword matching)
    PART_GROUPS = {
        "body_static": ["body", "chest", "torso", "neck", "necklace", "clothes"],
        "body_swing": ["body", "chest", "clothes", "torso", "waist"],
        "hair_back": ["hair_back", "hair_shadow"],
        "hair_front": ["hair_front", "bangs", "ahoge", "sidehair"],
        "face": ["face", "skin", "nose", "ear", "blush"],
        "eyes": ["eye", "iris", "pupil", "highlight", "eye_white", "whites"],
        "mouth": ["mouth", "lip", "teeth", "tongue"],
        "eyebrows": ["eyebrow", "brow"],
        "arms": ["arm", "hand"],
        "legs": ["leg", "foot", "thigh", "calf"],
    }

    # Chinese part name -> animation group mapping
    # Used when part_identifier provides Chinese part names
    CHINESE_PART_TO_GROUP = {
        "头发": "hair_front",
        "头发_亮": "hair_front",
        "皮肤": "face",
        "脸": "face",
        "眼睛_白": "eyes",
        "眼睛_瞳": "eyes",
        "眉毛": "eyebrows",
        "嘴巴": "mouth",
        "衣服": "body_swing",
        "衣服_暗": "body_swing",
        "腮红": "face",
        "鼻子": "face",
        "阴影": "body_static",
        "未分类": "body_static",
    }

    EXPRESSIONS = {
        "normal": {"mouth_scale": 1.0, "eye_open": 1.0, "blush": False},
        "happy": {"mouth_scale": 1.1, "eye_open": 0.7, "blush": True, "mouth_width": 1.1},
        "shy": {"mouth_scale": 0.9, "eye_open": 0.6, "blush": True},
        "surprised": {"mouth_scale": 1.3, "eye_open": 1.2, "mouth_width": 1.2},
        "sleepy": {"mouth_scale": 0.8, "eye_open": 0.3, "blush": False},
    }

    def __init__(self, layers_dir: str, config: Optional[Dict] = None):
        self.layers_dir = Path(layers_dir)
        self.config = {**self.ANIMATION_CONFIG, **(config or {})}
        if not self.layers_dir.is_dir():
            raise FileNotFoundError(f"Layers directory not found: {layers_dir}")
        self.layers: List[Dict] = []
        self.classified = {}

    def load_layers(self) -> List[Dict]:
        """Load and classify all layer PNGs."""
        self.layers = []
        layer_files = sorted(self.layers_dir.glob("layer_*.png"))
        if not layer_files:
            layer_files = sorted([f for f in self.layers_dir.glob("*.png")
                                  if f.name not in ("preview.png", "composite_preview.png")])

        for lf in layer_files:
            img = Image.open(lf).convert('RGBA')
            group = self._classify_layer(lf.stem, img)
            self.layers.append({
                "name": lf.stem,
                "path": str(lf),
                "image": img,
                "size": img.size,
                "group": group,
            })

        # Group layers
        self.classified = {}
        for layer in self.layers:
            g = layer["group"]
            self.classified.setdefault(g, []).append(layer)

        log.info(f"Loaded {len(self.layers)} layers, groups: {list(self.classified.keys())}")
        return self.layers

    def apply_part_mapping(self, part_mapping: Dict[str, str]) -> None:
        """Apply Chinese part name mapping to reclassify layers.

        Args:
            part_mapping: dict of {layer_name: chinese_part_name}
        """
        for layer in self.layers:
            name = layer["name"]
            if name in part_mapping:
                chinese_name = part_mapping[name]
                group = self.CHINESE_PART_TO_GROUP.get(chinese_name, "body_static")
                layer["group"] = group
                layer["part_name"] = chinese_name

        # Rebuild classified groups
        self.classified = {}
        for layer in self.layers:
            g = layer["group"]
            self.classified.setdefault(g, []).append(layer)

        log.info(f"Applied part mapping, groups now: {list(self.classified.keys())}")

    def _classify_layer(self, name: str, img: Image.Image) -> str:
        """Classify a layer into an animation group."""
        name_lower = name.lower()
        # Check each group's keywords
        for group, keywords in self.PART_GROUPS.items():
            for kw in keywords:
                if kw in name_lower:
                    return group
        return "body_static"

    def create_pet_package(self, output_dir: str, pet_name: str = "live2d_pet") -> Dict:
        """P1-3 FIX: Create a self-contained pet package using script-relative paths.

        The generated run_pet.py uses os.path.dirname(os.path.abspath(__file__))
        to locate resource files, so the package works from ANY directory.
        """
        valid, reason = validate_directory(output_dir, create_if_not_exists=True)
        if not valid:
            return {"success": False, "error": reason}

        out = Path(output_dir)
        pet_name = sanitize_filename(pet_name)
        pkg_dir = out / pet_name
        pkg_dir.mkdir(parents=True, exist_ok=True)

        # layers subdirectory
        layers_pkg = pkg_dir / "layers"
        layers_pkg.mkdir(exist_ok=True)

        # Copy layers
        for layer in self.layers:
            shutil.copy2(layer["path"], layers_pkg / Path(layer["path"]).name)

        # Save composite preview for sizing
        if self.layers:
            w, h = self.layers[0]["size"]
        else:
            w, h = 256, 384

        # Save config
        pet_config = {
            "name": pet_name,
            "canvas_size": [w, h],
            "fps": self.config["fps"],
            "layer_groups": {g: [l["name"] for l in layers] for g, layers in self.classified.items()},
            "animations": self.config,
            "expressions": list(self.EXPRESSIONS.keys()),
        }
        config_path = pkg_dir / "pet_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(pet_config, f, ensure_ascii=False, indent=2)

        # P1-3 FIX: Generate run_pet.py that uses __file__ for resource paths
        run_script = self._generate_run_script(pet_name)
        run_path = pkg_dir / "run_pet.py"
        run_path.write_text(run_script, encoding='utf-8')

        # Windows batch launcher
        bat_path = pkg_dir / "run_pet.bat"
        bat_path.write_text(f'@echo off\ncd /d "%~dp0"\npython run_pet.py\npause\n', encoding='utf-8')

        # Shell launcher
        sh_path = pkg_dir / "run_pet.sh"
        sh_path.write_text('#!/bin/bash\ncd "$(dirname "$0")"\npython3 run_pet.py\n', encoding='utf-8')
        os.chmod(sh_path, 0o755)

        # README for the pet package
        readme = pkg_dir / "README.txt"
        readme.write_text(
            f"{pet_name} - Live2D Desktop Pet\n"
            f"========================\n\n"
            f"Run: python run_pet.py\n"
            f"Or double-click run_pet.bat (Windows) / run_pet.sh (Mac/Linux)\n\n"
            f"Controls:\n"
            f"  - Click pet: Happy expression\n"
            f"  - Drag pet: Move to new position\n"
            f"  - Right-click / ESC: Exit\n"
            f"  - Pet auto-moves every 10 seconds\n",
            encoding='utf-8'
        )

        log.success(f"Pet package created: {pkg_dir}")
        return {
            "success": True,
            "package_dir": str(pkg_dir),
            "run_script": str(run_path),
            "layer_count": len(self.layers),
        }

    def _generate_run_script(self, pet_name: str) -> str:
        """Generate run_pet.py from template file.
        
        Reads pet_runner_template.py and replaces __PET_NAME__ placeholder.
        This avoids f-string curly-brace conflicts with generated code.
        """
        template_path = Path(__file__).parent / "pet_runner_template.py"
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        return template.replace('__PET_NAME__', pet_name)


def create_pet_package(layers_dir: str, output_dir: Optional[str] = None,
                       pet_name: str = "live2d_pet") -> Dict:
    """Convenience function: create a desktop pet package from layer directory."""
    if output_dir is None:
        output_dir = str(Path(layers_dir).parent / "pet_packages")
    animator = DesktopPetAnimator(layers_dir)
    animator.load_layers()
    return animator.create_pet_package(output_dir, pet_name)
