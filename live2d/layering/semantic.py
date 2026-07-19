#!/usr/bin/env python3
"""
Live2D Master Agent - Semantic Layer Separation (DEFAULT)

Uses anime-segmentation model for proper semantic part separation.
This replaces the K-means color clustering approach which produces
meaningless layer names (layer_000.png) that don't work for animations.

Supported semantic parts (from anime-segmentation):
- background, face, hair, eyes, mouth, eyebrows, skin, clothes, etc.

Fallback: If anime-segmentation is not available, falls back to K-means.
"""

import os
import time
from pathlib import Path
from typing import Optional, List, Dict, Tuple

from PIL import Image
import numpy as np

from live2d.logger import get_logger
from live2d.layering.kmeans import KMeansLayerer

log = get_logger("layering.semantic")


class SemanticLayerer:
    """Semantic segmentation based layer separation for anime characters."""

    # Semantic part names and their color codes
    SEMANTIC_PARTS = {
        0: "background",
        1: "hair",
        2: "face",
        3: "skin",
        4: "eyes",
        5: "eyebrows",
        6: "mouth",
        7: "clothes",
        8: "accessories",
        9: "other",
    }

    # Part name -> animation group mapping (for desktop pet)
    PART_TO_GROUP = {
        "hair": "hair_front",
        "hair_front": "hair_front",
        "hair_back": "hair_back",
        "face": "face",
        "skin": "face",
        "eyes": "eyes",
        "eyebrows": "eyebrows",
        "mouth": "mouth",
        "clothes": "body_swing",
        "accessories": "body_static",
        "other": "body_static",
        "background": "body_static",
    }

    def __init__(
        self,
        output_dir: Optional[str] = None,
        alpha_threshold: int = 10,
        min_layer_area_ratio: float = 0.002,
        device: str = "auto",
    ):
        self.output_dir = Path(output_dir) if output_dir else None
        self.alpha_threshold = alpha_threshold
        self.min_layer_area_ratio = min_layer_area_ratio
        self.device = device
        self._model = None
        self._has_model = False

    def _load_model(self):
        """Load anime-segmentation model with graceful fallback.
        
        Note: anime-segmentation is a HuggingFace model repo, not a package.
        We use segment-anything (SAM) library to load the fine-tuned weights.
        """
        try:
            # Try segment-anything first (the correct way)
            from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
            import torch

            log.info("Loading anime-segmentation SAM model...")
            
            model_type = "vit_h"
            sam_checkpoint = None
            
            # Check common cache locations
            possible_paths = [
                os.path.expanduser("~/.cache/huggingface/hub/models--anime-segmentation--sam-vit-huge-anime/snapshots/*/sam_vit_h_anime.pth"),
                os.path.expanduser("~/.cache/anime-segmentation/sam_vit_h_anime.pth"),
                os.path.expanduser("~/models/sam_vit_h_anime.pth"),
            ]
            
            import glob
            for pattern in possible_paths:
                matches = glob.glob(pattern)
                if matches:
                    sam_checkpoint = matches[0]
                    break

            if sam_checkpoint is None:
                log.info("Downloading anime-segmentation model from HuggingFace...")
                try:
                    from huggingface_hub import hf_hub_download
                    sam_checkpoint = hf_hub_download(
                        repo_id="anime-segmentation/sam-vit-huge-anime",
                        filename="sam_vit_h_anime.pth",
                        local_dir=os.path.expanduser("~/.cache/anime-segmentation"),
                    )
                    log.info(f"Model downloaded to: {sam_checkpoint}")
                except Exception as e:
                    log.warning(f"Failed to download model: {e}")
                    log.info("Will fall back to K-means layering")
                    self._has_model = False
                    return

            device = "cuda" if torch.cuda.is_available() and self.device == "auto" else "cpu"
            if self.device != "auto":
                device = self.device

            log.info(f"Loading SAM model from {sam_checkpoint} on {device}...")
            sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
            sam.to(device=device)
            
            self._mask_generator = SamAutomaticMaskGenerator(sam)
            self._has_model = True
            log.success(f"anime-segmentation SAM model loaded on {device}")

        except ImportError as e:
            log.warning(f"segment-anything not installed: {e}")
            log.info("Install with: pip install segment-anything")
            log.info("Falling back to K-means layering")
            self._has_model = False
        except Exception as e:
            log.warning(f"Failed to load anime-segmentation: {e}")
            log.info("Falling back to K-means layering")
            self._has_model = False

    def _segment_with_sam(self, image: Image.Image) -> List[Dict]:
        """Segment image using SAM anime model."""
        if not self._has_model:
            self._load_model()
        
        if not self._has_model:
            return []

        try:
            image_np = np.array(image.convert('RGB'))
            masks = self._mask_generator.generate(image_np)
            return masks
        except Exception as e:
            log.error(f"SAM segmentation failed: {e}")
            return []

    def _classify_mask(self, mask: Dict, image: Image.Image) -> str:
        """Classify a mask into a semantic part based on position and color."""
        img_arr = np.array(image.convert('RGBA'))
        h, w = img_arr.shape[:2]
        
        mask_arr = mask["segmentation"]
        if mask_arr.sum() == 0:
            return "other"

        y_indices, x_indices = np.where(mask_arr)
        centroid_y = y_indices.mean() / h
        centroid_x = x_indices.mean() / w
        
        pixels = img_arr[mask_arr][:, :3]
        mean_color = tuple(pixels.mean(axis=0).astype(int))
        
        area_ratio = mask_arr.sum() / (h * w)

        if centroid_y < 0.35 and area_ratio > 0.05:
            return "hair"
        elif 0.25 < centroid_y < 0.55 and area_ratio > 0.03:
            return "face"
        elif 0.35 < centroid_y < 0.48 and 0.3 < centroid_x < 0.7 and area_ratio < 0.03:
            if mean_color[0] > 200 and mean_color[1] > 200 and mean_color[2] > 200:
                return "eyes"
            else:
                return "face"
        elif 0.45 < centroid_y < 0.55 and 0.35 < centroid_x < 0.65 and area_ratio < 0.015:
            return "mouth"
        elif 0.28 < centroid_y < 0.40 and 0.3 < centroid_x < 0.7 and area_ratio < 0.01:
            return "eyebrows"
        elif centroid_y > 0.45 and area_ratio > 0.05:
            return "clothes"
        elif 0.3 < centroid_y < 0.55:
            return "skin"
        elif centroid_y < 0.3:
            return "hair"
        else:
            return "other"

    def layer(
        self,
        image: Image.Image,
        output_dir: Optional[str] = None,
        label_layers: bool = True,
    ) -> Dict:
        """Perform semantic layering on an image.
        
        Returns dict with keys: layers, output_dir, preview_path, guide_path.
        Each layer has a semantic part name (hair, eyes, mouth, etc.).
        """
        out_dir = Path(output_dir) if output_dir else self.output_dir
        if out_dir is None:
            out_dir = Path.cwd() / "output" / f"layers_{int(time.time())}"
        out_dir.mkdir(parents=True, exist_ok=True)

        log.info(f"Semantic layering: input={image.size}")

        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        img_array = np.array(image)
        h, w = img_array.shape[:2]
        alpha = img_array[:, :, 3]
        opaque_mask = alpha > self.alpha_threshold

        masks = self._segment_with_sam(image)
        
        if not masks:
            log.info("Semantic segmentation failed, falling back to K-means")
            kmeans = KMeansLayerer(k_clusters=12, output_dir=str(out_dir))
            return kmeans.layer(image, output_dir=str(out_dir))

        part_layers = {}
        for mask in masks:
            part_name = self._classify_mask(mask, image)
            
            if part_name not in part_layers:
                part_layers[part_name] = np.zeros((h, w), dtype=bool)
            
            part_layers[part_name] |= mask["segmentation"]

        min_pixels = int(h * w * self.min_layer_area_ratio)
        exported_layers = []
        
        for part_name, mask in part_layers.items():
            pixel_count = int(mask.sum())
            if pixel_count < min_pixels:
                continue

            layer_arr = np.zeros((h, w, 4), dtype=np.uint8)
            layer_arr[mask] = img_array[mask]
            
            layer_path = out_dir / f"{part_name}.png"
            Image.fromarray(layer_arr, 'RGBA').save(layer_path)

            pixels = img_array[mask][:, :3]
            mean_color = tuple(pixels.mean(axis=0).astype(int))

            exported_layers.append({
                "name": part_name,
                "part_name": part_name,
                "path": str(layer_path),
                "pixel_count": pixel_count,
                "color": mean_color,
            })

        preview_path = out_dir / "preview.png"
        image.save(preview_path)

        guide_path = self._write_guide(out_dir, exported_layers, image.size)

        log.success(f"Created {len(exported_layers)} semantic layers in {out_dir}")

        return {
            "layers": exported_layers,
            "output_dir": str(out_dir),
            "preview_path": str(preview_path),
            "guide_path": str(guide_path),
            "layer_count": len(exported_layers),
            "method": "semantic",
        }

    def _write_guide(self, out_dir: Path, layers: List[Dict], size: Tuple[int, int]) -> str:
        """Write a layer guide text file."""
        guide_path = out_dir / "LAYER_GUIDE.txt"
        w, h = size
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write("Live2D Master Agent - Semantic Layer Guide\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Image size: {w}x{h}\n")
            f.write(f"Layers exported: {len(layers)}\n")
            f.write(f"Method: Semantic Segmentation\n\n")
            
            f.write("Layers (semantic parts):\n")
            f.write("-" * 60 + "\n")
            for layer in layers:
                r, g, b = layer["color"]
                f.write(f"  {layer['name']:12s}  pixels={layer['pixel_count']:>8,}  "
                        f"color=RGB({r:3d},{g:3d},{b:3d})\n")
            
            f.write("\nAnimation Group Mapping:\n")
            f.write("-" * 60 + "\n")
            for layer in layers:
                group = self.PART_TO_GROUP.get(layer["name"], "body_static")
                f.write(f"  {layer['name']:12s} -> {group}\n")
            
            f.write("\nImporting into Live2D Cubism Editor:\n")
            f.write("-" * 60 + "\n")
            f.write("1. Open Cubism Editor\n")
            f.write("2. File -> Import PSD or import layers as textures\n")
            f.write("3. Arrange layers from back to front\n")
            f.write("4. Create ArtMeshes for each part\n")
            f.write("5. Set up deformation parameters\n")
        
        return str(guide_path)


def layer_image_file(
    input_path: str,
    output_dir: Optional[str] = None,
) -> Dict:
    """Convenience function: layer an image file using semantic segmentation."""
    img = Image.open(input_path).convert('RGBA')
    if output_dir is None:
        p = Path(input_path)
        output_dir = str(p.parent / f"{p.stem}_layers")
    layerer = SemanticLayerer(output_dir=output_dir)
    return layerer.layer(img, output_dir=output_dir)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Live2D Semantic Layer Tool")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", nargs="?", default=None, help="Output directory")
    args = parser.parse_args()

    result = layer_image_file(args.input, args.output)
    print(f"\nSemantic layering complete: {result['layer_count']} layers in {result['output_dir']}")
    print("\nLayers:")
    for layer in result["layers"]:
        print(f"  - {layer['name']}: {layer['path']}")
