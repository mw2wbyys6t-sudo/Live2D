#!/usr/bin/env python3
"""
Live2D Master Agent - K-Means Layer Separation (v6, DEFAULT per P0-3 fix)

Uses K-means clustering on image colors to separate character into layers.
P0-3 FIX: This is the DEFAULT layerer (not live2d_layer_pro).
"""

import os
import time
from pathlib import Path
from typing import Optional, List, Dict, Tuple

from PIL import Image
import numpy as np

from live2d.logger import get_logger

log = get_logger("layering")

# Optional dependencies with graceful degradation
try:
    from sklearn.cluster import KMeans as SKLearnKMeans
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    log.debug("scikit-learn not available, using fallback quantization")

try:
    import scipy.ndimage as ndi
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


class KMeansLayerer:
    """K-means color clustering for Live2D layer separation (v6).

    P0-3: This is the default layerer, replacing the buggy call to layer_pro.
    """

    def __init__(
        self,
        k_clusters: int = 12,
        alpha_threshold: int = 10,
        min_layer_area_ratio: float = 0.001,
        output_dir: Optional[str] = None,
    ):
        self.k_clusters = max(3, min(k_clusters, 20))
        self.alpha_threshold = alpha_threshold
        self.min_layer_area_ratio = min_layer_area_ratio
        self.output_dir = Path(output_dir) if output_dir else None

    def layer(
        self,
        image: Image.Image,
        output_dir: Optional[str] = None,
        label_layers: bool = True,
    ) -> Dict:
        """Perform K-means layering on an image.

        Returns dict with keys: layers, output_dir, preview_path, guide_path.
        """
        out_dir = Path(output_dir) if output_dir else self.output_dir
        if out_dir is None:
            out_dir = Path.cwd() / "output" / f"layers_{int(time.time())}"
        out_dir.mkdir(parents=True, exist_ok=True)

        log.info(f"K-means layering: k={self.k_clusters}, input={image.size}")

        # Convert to RGBA
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        img_array = np.array(image)
        h, w = img_array.shape[:2]

        # Separate alpha mask
        alpha = img_array[:, :, 3]
        opaque_mask = alpha > self.alpha_threshold

        # Get opaque pixels for clustering
        rgb_pixels = img_array[opaque_mask][:, :3].astype(np.float64)

        if len(rgb_pixels) == 0:
            log.warning("No opaque pixels found in image")
            return {"layers": [], "output_dir": str(out_dir), "layer_count": 0}

        # Determine actual k (can't have more clusters than pixels)
        actual_k = min(self.k_clusters, len(rgb_pixels))

        # Run K-means or fallback
        if HAS_SKLEARN and actual_k >= 3:
            labels_flat = self._sklearn_kmeans(rgb_pixels, actual_k)
        else:
            labels_flat = self._simple_quantization(rgb_pixels, actual_k)

        # Reconstruct label map
        label_map = np.full((h, w), -1, dtype=np.int32)
        label_map[opaque_mask] = labels_flat

        # Calculate cluster colors (centers)
        unique_labels = sorted(set(labels_flat.tolist()))
        cluster_colors = {}
        for label in unique_labels:
            mask = labels_flat == label
            if mask.any():
                cluster_colors[label] = rgb_pixels[mask].mean(axis=0).astype(np.uint8)

        # Remove tiny layers (noise)
        min_pixels = int(h * w * self.min_layer_area_ratio)
        layer_info = []
        for label in unique_labels:
            pixel_count = int(np.sum(label_map == label))
            if pixel_count < min_pixels:
                continue
            layer_info.append({
                "label": int(label),
                "pixel_count": pixel_count,
                "color": tuple(int(c) for c in cluster_colors.get(label, (128, 128, 128))),
            })

        # Sort by area (largest first)
        layer_info.sort(key=lambda x: x["pixel_count"], reverse=True)

        # Export layers as PNG files
        exported_layers = []
        for idx, info in enumerate(layer_info):
            label = info["label"]
            layer_arr = np.zeros((h, w, 4), dtype=np.uint8)
            mask = label_map == label
            layer_arr[mask] = img_array[mask]
            layer_path = out_dir / f"layer_{idx:03d}.png"
            Image.fromarray(layer_arr, 'RGBA').save(layer_path)
            info["path"] = str(layer_path)
            info["index"] = idx
            exported_layers.append(info)

        # Save preview
        preview_path = out_dir / "preview.png"
        image.save(preview_path)

        # Generate layer guide
        guide_path = self._write_guide(out_dir, exported_layers, image.size)

        log.success(f"Created {len(exported_layers)} layers in {out_dir}")

        return {
            "layers": exported_layers,
            "output_dir": str(out_dir),
            "preview_path": str(preview_path),
            "guide_path": str(guide_path),
            "layer_count": len(exported_layers),
            "k_clusters": actual_k,
        }

    def _sklearn_kmeans(self, pixels: np.ndarray, k: int) -> np.ndarray:
        """Run sklearn KMeans clustering."""
        log.debug(f"Running sklearn KMeans with k={k}, n_pixels={len(pixels)}")
        # Subsample for large images to speed up clustering
        max_pixels = 100_000
        if len(pixels) > max_pixels:
            indices = np.random.choice(len(pixels), max_pixels, replace=False)
            sample_pixels = pixels[indices]
        else:
            sample_pixels = pixels
            indices = None

        kmeans = SKLearnKMeans(n_clusters=k, random_state=42, n_init=10, max_iter=100)
        kmeans.fit(sample_pixels)

        # Predict labels for all pixels
        if indices is not None:
            labels = kmeans.predict(pixels)
        else:
            labels = kmeans.labels_

        return labels.astype(np.int32)

    def _simple_quantization(self, pixels: np.ndarray, k: int) -> np.ndarray:
        """Fallback color quantization when sklearn is not available."""
        log.debug(f"Using simple quantization, k={k}")
        # Bits per channel to achieve ~k colors
        bits = max(2, int(np.log2(k ** (1/3))))
        factor = 256 // (2 ** bits)
        quantized = (pixels // factor) * factor
        # Assign labels to unique colors
        unique_colors, inverse = np.unique(quantized, axis=0, return_inverse=True)
        return inverse.astype(np.int32)

    def _write_guide(self, out_dir: Path, layers: List[Dict], size: Tuple[int, int]) -> str:
        """Write a layer guide text file."""
        guide_path = out_dir / "LAYER_GUIDE.txt"
        w, h = size
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write("Live2D Master Agent v9.0 - K-Means Layer Guide\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Image size: {w}x{h}\n")
            f.write(f"Clusters (k): {self.k_clusters}\n")
            f.write(f"Layers exported: {len(layers)}\n\n")
            f.write("Layers (by area, largest first):\n")
            f.write("-" * 60 + "\n")
            for layer in layers:
                r, g, b = layer["color"]
                f.write(f"  {layer['index']:3d}. layer_{layer['index']:03d}.png  "
                        f"pixels={layer['pixel_count']:>8,}  "
                        f"color=RGB({r:3d},{g:3d},{b:3d})\n")
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
    k_clusters: int = 12,
) -> Dict:
    """Convenience function: layer an image file and export PNG layers.

    P0-3: Uses KMeansLayerer (v6) by default.
    """
    img = Image.open(input_path).convert('RGBA')
    if output_dir is None:
        p = Path(input_path)
        output_dir = str(p.parent / f"{p.stem}_layers")
    layerer = KMeansLayerer(k_clusters=k_clusters)
    return layerer.layer(img, output_dir=output_dir)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Live2D K-Means Layer Tool v6 (Default)")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", nargs="?", default=None, help="Output directory")
    parser.add_argument("--k", type=int, default=12, help="Number of clusters (default: 12)")
    args = parser.parse_args()

    result = layer_image_file(args.input, args.output, k_clusters=args.k)
    print(f"\nLayering complete: {result['layer_count']} layers in {result['output_dir']}")
