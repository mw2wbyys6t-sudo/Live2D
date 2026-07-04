#!/usr/bin/env python3
"""
Live2D Master Agent - Part Identifier
Identifies body parts from K-means clusters using color heuristics and position.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional

# Reference color ranges for Live2D parts (in RGB)
PART_COLOR_RANGES = {
    "头发": {"rgb_range": [(20, 20, 20), (100, 60, 40)], "y_range": (0.0, 0.45)},       # Hair: dark, top of image
    "头发_亮": {"rgb_range": [(200, 180, 100), (255, 240, 180)], "y_range": (0.0, 0.5)}, # Hair highlight
    "皮肤": {"rgb_range": [(220, 170, 150), (255, 220, 200)], "y_range": (0.2, 0.8)},    # Skin
    "脸": {"rgb_range": [(230, 190, 170), (255, 230, 220)], "y_range": (0.1, 0.4)},      # Face
    "眼睛_白": {"rgb_range": [(230, 230, 240), (255, 255, 255)], "y_range": (0.2, 0.35), "size_max": 0.05},
    "眼睛_瞳": {"rgb_range": [(20, 40, 80), (100, 120, 180)], "y_range": (0.22, 0.33), "size_max": 0.03},
    "眉毛": {"rgb_range": [(40, 30, 20), (120, 80, 60)], "y_range": (0.18, 0.28)},
    "嘴巴": {"rgb_range": [(180, 60, 80), (255, 120, 140)], "y_range": (0.32, 0.4), "size_max": 0.03},
    "衣服": {"rgb_range": [(50, 80, 150), (200, 180, 220)], "y_range": (0.35, 0.9)},      # Clothes
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

    def _score_part(
        self,
        color: Tuple[int, int, int],
        y_ratio: float,
        area_ratio: float,
        criteria: Dict,
    ) -> float:
        """Score how well a cluster matches a part definition."""
        score = 0.0

        # Color match (RGB distance to range center)
        rgb_min, rgb_max = criteria["rgb_range"]
        color_arr = np.array(color)
        min_arr = np.array(rgb_min)
        max_arr = np.array(rgb_max)
        center = (min_arr + max_arr) / 2.0
        radius = np.linalg.norm(max_arr - min_arr) / 2.0

        dist = np.linalg.norm(color_arr - center)
        if dist < radius * 1.5:
            color_score = max(0, 1.0 - dist / (radius * 1.5))
            score += color_score * 0.6
        elif np.all(color_arr >= min_arr - 20) and np.all(color_arr <= max_arr + 20):
            score += 0.1
        else:
            return -1.0  # Color out of range

        # Position match
        y_min, y_max = criteria.get("y_range", (0.0, 1.0))
        if y_min <= y_ratio <= y_max:
            # Closer to center of range = better score
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

        Each layer dict should have: color (RGB tuple), pixel_count.
        Adds 'part_name' key to each dict.
        """
        total_pixels = image_height * image_width
        total_pixels = max(total_pixels, 1)

        # We need centroid position from the actual image data
        # For now use area-based position heuristic: large dark regions at top = hair
        for layer in layers_info:
            color = layer.get("color", (128, 128, 128))
            area_ratio = layer.get("pixel_count", 0) / total_pixels
            # Estimate position from area ratio (rough heuristic)
            # Larger areas are more likely body/clothes
            if area_ratio > 0.2:
                y_ratio = 0.6  # likely body/clothes
            elif color[0] < 100 and color[1] < 80 and color[2] < 80:
                y_ratio = 0.2  # dark colors at top = hair
            else:
                y_ratio = 0.4  # face area default

            part_name = self.identify_part(color, y_ratio, area_ratio)
            layer["part_name"] = part_name

        return layers_info
