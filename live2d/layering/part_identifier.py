#!/usr/bin/env python3
"""
Live2D Master Agent - Part Identifier
Identifies body parts from layer color and position.

Supports two modes:
1. Semantic layers (from SemanticLayerer): already have part_name, skip identification
2. K-means layers (from KMeansLayerer): compute real centroid from PNG alpha channel
"""

import numpy as np
from PIL import Image
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Reference color ranges for Live2D parts (in RGB)
# Supports both single range (rgb_range) and multiple ranges (rgb_ranges)
PART_COLOR_RANGES = {
    "头发": {"rgb_ranges": [[(20, 20, 20), (100, 60, 40)], [(150, 80, 100), (220, 160, 180)], [(80, 120, 180), (160, 200, 240)], [(180, 100, 160), (240, 180, 220)], [(60, 140, 80), (140, 200, 140)]], "y_range": (0.0, 0.45)},
    "头发_亮": {"rgb_range": [(200, 180, 100), (255, 240, 180)], "y_range": (0.0, 0.5)},
    "皮肤": {"rgb_range": [(220, 170, 150), (255, 220, 200)], "y_range": (0.2, 0.8)},
    "脸": {"rgb_range": [(230, 190, 170), (255, 230, 220)], "y_range": (0.1, 0.4)},
    "眼睛_白": {"rgb_range": [(230, 230, 240), (255, 255, 255)], "y_range": (0.2, 0.35), "size_max": 0.05},
    "眼睛_瞳": {"rgb_ranges": [[(20, 40, 80), (100, 120, 180)], [(150, 30, 30), (220, 80, 80)], [(30, 120, 60), (100, 200, 120)]], "y_range": (0.22, 0.33), "size_max": 0.03},
    "眉毛": {"rgb_range": [(40, 30, 20), (120, 80, 60)], "y_range": (0.18, 0.28)},
    "嘴巴": {"rgb_range": [(180, 60, 80), (255, 120, 140)], "y_range": (0.32, 0.4), "size_max": 0.03},
    "衣服": {"rgb_ranges": [[(50, 80, 150), (200, 180, 220)], [(180, 60, 80), (255, 140, 160)], [(60, 140, 80), (160, 220, 140)], [(200, 200, 200), (255, 255, 255)]], "y_range": (0.35, 0.9)},
    "衣服_暗": {"rgb_range": [(30, 50, 100), (100, 80, 120)], "y_range": (0.35, 0.9)},
    "腮红": {"rgb_range": [(255, 150, 160), (255, 200, 200)], "y_range": (0.28, 0.38), "size_max": 0.02},
    "鼻子": {"rgb_range": [(200, 140, 130), (240, 190, 180)], "y_range": (0.28, 0.36), "size_max": 0.01},
    "阴影": {"rgb_range": [(60, 50, 70), (130, 110, 130)], "y_range": (0.0, 1.0)},
}


class PartIdentifier:
    """Identifies body parts from layer color and position information."""

    def __init__(self):
        self.color_ranges = PART_COLOR_RANGES

    def identify_part(
        self,
        mean_color: Tuple[int, int, int],
        centroid_y_ratio: float,
        area_ratio: float = 1.0,
    ) -> str:
        """Identify a body part based on color, vertical position, and size.

        Args:
            mean_color: (R, G, B) tuple 0-255
            centroid_y_ratio: 0.0 (top) to 1.0 (bottom) vertical position
            area_ratio: fraction of total image area this layer occupies

        Returns:
            Best matching part name in Chinese
        """
        best_part = "未分类"
        best_score = -1.0

        for part_name, criteria in self.color_ranges.items():
            score = self._score_part(mean_color, centroid_y_ratio, area_ratio, criteria)
            if score > best_score:
                best_score = score
                best_part = part_name

        return best_part if best_score > 0 else "未分类"

    def _score_color_range(self, color_arr: np.ndarray, rgb_min: Tuple, rgb_max: Tuple) -> float:
        """Score color match against a single RGB range."""
        min_arr = np.array(rgb_min)
        max_arr = np.array(rgb_max)
        center = (min_arr + max_arr) / 2.0
        radius = np.linalg.norm(max_arr - min_arr) / 2.0
        if radius < 1.0:
            radius = 1.0

        dist = np.linalg.norm(color_arr - center)
        if dist < radius * 1.5:
            return max(0, 1.0 - dist / (radius * 1.5))
        elif np.all(color_arr >= min_arr - 20) and np.all(color_arr <= max_arr + 20):
            return 0.1
        return -1.0

    def _score_part(
        self,
        color: Tuple[int, int, int],
        y_ratio: float,
        area_ratio: float,
        criteria: Dict,
    ) -> float:
        """Score how well a cluster matches a part definition."""
        score = 0.0
        color_arr = np.array(color)

        # Color match: support both single range (rgb_range) and multiple ranges (rgb_ranges)
        best_color_score = -1.0
        if "rgb_ranges" in criteria:
            for rgb_min, rgb_max in criteria["rgb_ranges"]:
                cs = self._score_color_range(color_arr, rgb_min, rgb_max)
                if cs > best_color_score:
                    best_color_score = cs
        elif "rgb_range" in criteria:
            rgb_min, rgb_max = criteria["rgb_range"]
            best_color_score = self._score_color_range(color_arr, rgb_min, rgb_max)
        else:
            return -1.0

        if best_color_score < 0:
            return -1.0
        score += best_color_score * 0.6

        # Position match
        y_min, y_max = criteria.get("y_range", (0.0, 1.0))
        if y_min <= y_ratio <= y_max:
            y_center = (y_min + y_max) / 2
            y_span = (y_max - y_min) / 2
            if y_span > 0:
                y_score = max(0, 1.0 - abs(y_ratio - y_center) / y_span)
                score += y_score * 0.3
        else:
            score -= 0.2

        # Size constraint (some parts like eyes should be small)
        size_max = criteria.get("size_max")
        if size_max is not None and area_ratio > size_max * 3:
            score -= 0.5

        return score

    def identify_layers(self, layers_info: List[Dict], image_height: int, image_width: int) -> List[Dict]:
        """Identify parts for a list of layer info dicts.

        Each layer dict should have: color (RGB tuple), pixel_count, path.
        Adds 'part_name' key to each dict.

        Behavior:
        - If layer already has 'part_name' (from SemanticLayerer), keep it unchanged.
        - Otherwise, compute real centroid from PNG alpha channel for accurate position.
        """
        total_pixels = image_height * image_width
        total_pixels = max(total_pixels, 1)

        for layer in layers_info:
            # If already has semantic part_name, skip identification
            if layer.get("part_name"):
                continue

            color = layer.get("color", (128, 128, 128))
            area_ratio = layer.get("pixel_count", 0) / total_pixels

            # Compute real centroid from PNG alpha channel
            y_ratio = self._compute_centroid_y(layer.get("path"), image_height)

            part_name = self.identify_part(color, y_ratio, area_ratio)
            layer["part_name"] = part_name

        return layers_info

    def _compute_centroid_y(self, layer_path: Optional[str], image_height: int) -> float:
        """Compute the vertical centroid ratio from a layer's PNG alpha channel."""
        if not layer_path or not Path(layer_path).exists():
            return 0.5  # default fallback

        try:
            img = Image.open(layer_path).convert("RGBA")
            arr = np.array(img)
            alpha = arr[:, :, 3]
            opaque = alpha > 10
            if not opaque.any():
                return 0.5
            ys, xs = np.where(opaque)
            centroid_y = ys.mean() / image_height
            return float(centroid_y)
        except Exception:
            return 0.5
