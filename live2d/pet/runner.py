#!/usr/bin/env python3
"""
Live2D Master Agent - Pet Runner
Runs a pet package directly (without generating a separate script).
Useful for immediate preview after layer generation.
"""

import os
import sys
import math
import random
import time
from pathlib import Path
from typing import Optional, List, Tuple


class PetRunner:
    """Run a desktop pet from a layers directory using pygame."""

    def __init__(self, layers_dir: str, width: int = 256, height: int = 384, fps: int = 60):
        self.layers_dir = Path(layers_dir)
        self.width = width
        self.height = height
        self.fps = fps
        self._running = False

    def run(self):
        """Run the pet window (blocking)."""
        try:
            import pygame
        except ImportError:
            print("pygame is required for desktop pet. Install: pip install pygame")
            return False

        pygame.init()

        # Load layers
        layers = self._load_layers(pygame)
        if not layers:
            print("No layer PNGs found")
            pygame.quit()
            return False

        # Auto-detect canvas size from layers
        w, h = layers[0][1].get_size()
        self.width, self.height = w, h

        screen = pygame.display.set_mode((w, h), pygame.NOFRAME | pygame.SRCALPHA)
        pygame.display.set_caption("Live2D Pet")
        clock = pygame.time.Clock()

        # Initial position (bottom-right area)
        info = pygame.display.Info()
        pet_x = info.current_w - w - 50
        pet_y = info.current_h - h - 80

        start = time.time()
        next_blink = start + random.uniform(3, 6)
        blink_end = 0
        dragging = False
        drag_off = (0, 0)
        next_move = start + 10
        expression = "normal"
        next_expr = start + 8

        self._running = True
        while self._running:
            now = time.time()
            t = now - start
            clock.tick(self.fps)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self._running = False
                elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    self._running = False
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    if ev.button == 1:
                        dragging = True
                        mx, my = ev.pos
                        drag_off = (mx, my)
                        expression = "happy"
                        next_expr = now + 2
                    elif ev.button == 3:
                        self._running = False
                elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    dragging = False
                elif ev.type == pygame.MOUSEMOTION and dragging:
                    mx, my = ev.pos
                    pet_x = mx - drag_off[0]
                    pet_y = my - drag_off[1]

            # Auto-move
            if now > next_move and not dragging:
                info2 = pygame.display.Info()
                pet_x = random.randint(20, max(20, info2.current_w - w - 20))
                next_move = now + random.uniform(8, 15)

            # Blink
            eye_open = 1.0
            if now < blink_end:
                eye_open = max(0, (blink_end - now) / 0.15)
            elif now > next_blink:
                blink_end = now + 0.15
                next_blink = now + random.uniform(3, 6)

            # Expression
            if now > next_expr:
                expression = random.choice(["normal", "happy", "shy", "normal"])
                next_expr = now + random.uniform(6, 12)

            # Animate
            swing = math.sin(t * 0.8) * 3.0
            breath = math.sin(t * 0.4) * 1.5
            hair_off = swing * 1.8

            screen.fill((0, 0, 0, 0))
            for name, surf in layers:
                nl = name.lower()
                ox, oy = 0, breath
                if any(k in nl for k in ["hair", "bangs"]):
                    ox = hair_off
                elif any(k in nl for k in ["body", "clothes"]):
                    ox = swing * 0.5

                draw_surf = surf
                if eye_open < 0.9 and any(k in nl for k in ["eye", "iris", "pupil"]):
                    sw2, sh2 = surf.get_size()
                    nh = max(1, int(sh2 * eye_open))
                    draw_surf = pygame.transform.scale(surf, (sw2, nh))
                    oy += (sh2 - nh) // 2

                screen.blit(draw_surf, (pet_x + ox, pet_y + oy))

            pygame.display.flip()

        pygame.quit()
        return True

    def _load_layers(self, pygame) -> List[Tuple[str, 'pygame.Surface']]:
        layers = []
        if not self.layers_dir.is_dir():
            return layers
        for f in sorted(self.layers_dir.glob("*.png")):
            if f.name in ("preview.png", "composite_preview.png"):
                continue
            try:
                surf = pygame.image.load(str(f)).convert_alpha()
                layers.append((f.stem, surf))
            except Exception:
                pass
        return layers
