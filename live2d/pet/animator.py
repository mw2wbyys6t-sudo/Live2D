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

    # Part group definitions for animation
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
        """P1-3 FIX: Generate run_pet.py that uses SCRIPT-RELATIVE paths.

        CRITICAL: The script uses os.path.dirname(os.path.abspath(__file__))
        to find resources, NOT os.getcwd(). This means the pet package
        can be moved to any directory and still work.
        """
        return f'''#!/usr/bin/env python3
"""
{pet_name} - Live2D Desktop Pet
Generated by Live2D Master Agent v8.0

P1-3 FIX: Uses __file__-relative paths so this script works
from ANY working directory.

Controls:
  Left-click pet   -> Happy expression
  Drag pet         -> Move to position
  Right-click/ESC  -> Exit
"""

import os
import sys
import math
import random
import time

# P1-3 FIX: Use SCRIPT directory, NOT current working directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LAYERS_DIR = os.path.join(SCRIPT_DIR, "layers")
CONFIG_PATH = os.path.join(SCRIPT_DIR, "pet_config.json")

# Change to script dir to ensure resource loading works
os.chdir(SCRIPT_DIR)

import json
import pygame

def load_config():
    """Load pet configuration (script-relative)."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {{
            "name": "{pet_name}",
            "canvas_size": [256, 384],
            "fps": 60,
            "layer_groups": {{}},
            "animations": {{
                "body_swing_amplitude": 3.0,
                "body_swing_speed": 0.8,
                "breath_amplitude": 1.5,
                "breath_speed": 0.4,
                "blink_interval_min": 3.0,
                "blink_interval_max": 6.0,
                "blink_duration": 0.15,
                "hair_swing_multiplier": 1.8,
                "expression_change_interval": 10.0,
            }}
        }}

def load_layers(layers_dir):
    """Load all layer PNGs (script-relative path)."""
    layers = []
    if not os.path.isdir(layers_dir):
        # Create a simple default pet
        return [create_default_pet_layer()]
    for fname in sorted(os.listdir(layers_dir)):
        if fname.endswith(".png"):
            path = os.path.join(layers_dir, fname)
            try:
                surf = pygame.image.load(path).convert_alpha()
                layers.append((fname, surf))
            except Exception:
                pass
    return layers if layers else [create_default_pet_layer()]

def create_default_pet_layer():
    """Create a simple colored circle as default pet."""
    surf = pygame.Surface((128, 128), pygame.SRCALPHA)
    pygame.draw.circle(surf, (255, 200, 200), (64, 64), 50)
    pygame.draw.circle(surf, (100, 100, 200), (48, 54), 8)
    pygame.draw.circle(surf, (100, 100, 200), (80, 54), 8)
    pygame.draw.circle(surf, (255, 150, 150), (64, 75), 12, 2)
    return ("default", surf)

def clamp(val, low, high):
    return max(low, min(high, val))

def main():
    pygame.init()

    config = load_config()
    w, h = config.get("canvas_size", [256, 384])
    fps = config.get("fps", 60)
    anim = config.get("animations", {{}})

    # Create transparent frameless window
    screen = pygame.display.set_mode((w, h), pygame.NOFRAME | pygame.SRCALPHA)
    pygame.display.set_caption(config.get("name", "{pet_name}"))

    clock = pygame.time.Clock()
    layers = load_layers(LAYERS_DIR)

    # Position on screen (clamp so pet always fits even on small displays)
    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h
    pet_x = clamp(screen_w // 2 - w // 2, 0, max(0, screen_w - w))
    pet_y = clamp(screen_h - h - 100, 0, max(0, screen_h - h))

    # Animation state
    start_time = time.time()
    next_blink = start_time + random.uniform(
        anim.get("blink_interval_min", 3),
        anim.get("blink_interval_max", 6))
    blink_until = 0
    next_expression = start_time + anim.get("expression_change_interval", 10)
    next_move = start_time + 10
    expression = "normal"
    dragging = False
    drag_offset = (0, 0)

    running = True
    while running:
        now = time.time()
        t = now - start_time
        dt = clock.tick(fps) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    # Check if click is on pet
                    dragging = True
                    drag_offset = (mx - pet_x, my - pet_y)
                    expression = "happy"
                    next_expression = now + 2
                elif event.button == 3:
                    running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mx, my = event.pos
                    pet_x = clamp(mx - drag_offset[0], 0, max(0, screen_w - w))
                    pet_y = clamp(my - drag_offset[1], 0, max(0, screen_h - h))

        # Auto-move (clamp target range to avoid crash on small screens)
        if now > next_move and not dragging:
            max_x = max(50, screen_w - w - 50)
            pet_x = random.randint(min(50, max_x), max_x)
            next_move = now + random.uniform(8, 15)

        # Blink logic
        eye_open = 1.0
        if now < blink_until:
            blink_progress = (blink_until - now) / anim.get("blink_duration", 0.15)
            eye_open = blink_progress
        elif now > next_blink:
            blink_until = now + anim.get("blink_duration", 0.15)
            next_blink = now + random.uniform(
                anim.get("blink_interval_min", 3),
                anim.get("blink_interval_max", 6))

        # Expression changes
        if now > next_expression:
            expression = random.choice(["normal", "happy", "shy", "normal", "normal"])
            next_expression = now + random.uniform(8, 15)

        # Clear screen
        screen.fill((0, 0, 0, 0))

        # Calculate animation offsets
        swing = math.sin(t * anim.get("body_swing_speed", 0.8)) * anim.get("body_swing_amplitude", 3)
        breath = math.sin(t * anim.get("breath_speed", 0.4)) * anim.get("breath_amplitude", 1.5)
        hair_swing = swing * anim.get("hair_swing_multiplier", 1.8)

        # Draw layers with offsets
        for name, surf in layers:
            name_l = name.lower()
            offset_x, offset_y = 0, breath

            # Apply swing based on layer type
            if any(kw in name_l for kw in ["hair", "bangs", "ahoge"]):
                offset_x = hair_swing
            elif any(kw in name_l for kw in ["body", "clothes", "chest"]):
                offset_x = swing * 0.5

            # Eye blink: scale eye layers vertically
            draw_surf = surf
            if eye_open < 0.9 and any(kw in name_l for kw in ["eye", "iris", "pupil"]):
                sw, sh = surf.get_size()
                new_h = max(1, int(sh * eye_open))
                draw_surf = pygame.transform.scale(surf, (sw, new_h))
                offset_y += (sh - new_h) // 2

            screen.blit(draw_surf, (pet_x + offset_x, pet_y + offset_y))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
'''


def create_pet_package(layers_dir: str, output_dir: Optional[str] = None,
                       pet_name: str = "live2d_pet") -> Dict:
    """Convenience function: create a desktop pet package from layer directory."""
    if output_dir is None:
        output_dir = str(Path(layers_dir).parent / "pet_packages")
    animator = DesktopPetAnimator(layers_dir)
    animator.load_layers()
    return animator.create_pet_package(output_dir, pet_name)
