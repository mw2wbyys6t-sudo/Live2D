#!/usr/bin/env python3
"""Pack 52 RGBA layers into one or more texture atlases."""

from typing import Dict, List, Tuple

from PIL import Image

from live2d.logger import get_logger

log = get_logger("exporter.atlas")


class TextureAtlas:
    """Simple shelf-packing texture atlas with multi-page support."""

    def __init__(self, max_size: int = 2048, padding: int = 2):
        self.max_size = max(1, max_size)
        self.padding = max(0, padding)

    def pack(self, layers: Dict[str, Image.Image]) -> Dict:
        """Return atlas images and UV coordinates for each layer.

        Returns:
            {
                "atlases": [PIL.Image, ...],
                "uvs": {
                    layer_name: {
                        "page": int,
                        "top_left": (x, y),
                        "bottom_right": (x2, y2),
                    },
                    ...
                },
            }
        """
        if not layers:
            empty = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            return {"atlases": [empty], "uvs": {}}

        items = sorted(layers.items(), key=lambda kv: kv[1].height, reverse=True)

        pages: List[Dict[str, Tuple[int, int, int, int]]] = []
        current_page: Dict[str, Tuple[int, int, int, int]] = {}
        shelf_y = 0
        shelf_x = 0
        shelf_height = 0

        def _start_new_page():
            nonlocal current_page, shelf_y, shelf_x, shelf_height
            if current_page:
                pages.append(current_page)
            current_page = {}
            shelf_y = 0
            shelf_x = 0
            shelf_height = 0

        for name, img in items:
            if img.width > self.max_size or img.height > self.max_size:
                raise RuntimeError(
                    f"Layer {name} ({img.width}x{img.height}) exceeds max atlas size {self.max_size}"
                )
            w = img.width + self.padding
            h = img.height + self.padding

            if shelf_x + w > self.max_size and shelf_y + shelf_height + h <= self.max_size:
                shelf_y += shelf_height
                shelf_x = 0
                shelf_height = 0

            if shelf_y + h > self.max_size:
                _start_new_page()

            if shelf_x + w > self.max_size:
                shelf_y += shelf_height
                shelf_x = 0
                shelf_height = 0

            current_page[name] = (shelf_x, shelf_y, shelf_x + img.width, shelf_y + img.height)
            shelf_x += w
            shelf_height = max(shelf_height, h)

        if current_page:
            pages.append(current_page)

        atlases: List[Image.Image] = []
        uvs: Dict[str, Dict] = {}
        for page_idx, placements in enumerate(pages):
            if not placements:
                continue
            atlas_width = max(x2 for _, _, x2, _ in placements.values())
            atlas_height = max(y2 for _, _, _, y2 in placements.values())
            atlas = Image.new("RGBA", (atlas_width, atlas_height), (0, 0, 0, 0))
            for name, img in layers.items():
                if name not in placements:
                    continue
                x1, y1, x2, y2 = placements[name]
                atlas.paste(img, (x1, y1), img)
                uvs[name] = {
                    "page": page_idx,
                    "top_left": (float(x1), float(y1)),
                    "bottom_right": (float(x2), float(y2)),
                }
            atlases.append(atlas)

        return {"atlases": atlases, "uvs": uvs}
