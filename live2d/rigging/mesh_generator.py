#!/usr/bin/env python3
"""Generate deformable triangular meshes from RGBA layer images."""

from typing import Dict, List, Tuple

import cv2
import numpy as np
from PIL import Image
from scipy.spatial import Delaunay
from scipy.spatial import QhullError

from live2d.logger import get_logger

log = get_logger("rigging.mesh")


class MeshGenerator:
    """Create a triangulated mesh from an opaque region of an image."""

    def __init__(self, internal_spacing: int = 24, contour_spacing: int = 12):
        self.internal_spacing = max(4, internal_spacing)
        self.contour_spacing = max(4, contour_spacing)

    def generate(self, image: Image.Image) -> Dict:
        """Return dict with vertices (N,2) and indices (list of 3-int tuples)."""
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        arr = np.array(image)
        alpha = arr[:, :, 3]
        h, w = alpha.shape

        mask = (alpha > 128).astype(np.uint8)
        if mask.sum() == 0:
            return {"vertices": np.zeros((0, 2), dtype=float), "indices": []}

        # Contour points
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_pts: List[Tuple[float, float]] = []
        for cnt in contours:
            cnt = cnt.squeeze()
            if cnt.ndim < 2 or len(cnt) < 3:
                continue
            arclen = cv2.arcLength(cnt, True)
            eps = self.contour_spacing / arclen if arclen > 0 else 0.01
            approx = cv2.approxPolyDP(cnt, eps * arclen, True).squeeze()
            if approx.ndim == 1:
                approx = approx[np.newaxis, :]
            for pt in approx:
                contour_pts.append((float(pt[0]), float(pt[1])))

        # Internal grid points
        ys, xs = np.where(mask > 0)
        if len(xs) == 0:
            return {"vertices": np.zeros((0, 2), dtype=float), "indices": []}
        x_min, x_max = int(xs.min()), int(xs.max())
        y_min, y_max = int(ys.min()), int(ys.max())

        grid_pts: List[Tuple[float, float]] = []
        for y in range(y_min, y_max + 1, self.internal_spacing):
            for x in range(x_min, x_max + 1, self.internal_spacing):
                if 0 <= y < h and 0 <= x < w and mask[y, x] > 0:
                    grid_pts.append((float(x), float(y)))

        vertices = contour_pts + grid_pts
        if len(vertices) < 3:
            return {"vertices": np.zeros((0, 2), dtype=float), "indices": []}

        pts = np.array(vertices, dtype=float)
        # Remove near-duplicate points that can make qhull degenerate
        rounded = np.round(pts, decimals=3)
        _, unique_idx = np.unique(rounded, axis=0, return_index=True)
        pts = pts[np.sort(unique_idx)]
        if len(pts) < 3:
            return {"vertices": np.zeros((0, 2), dtype=float), "indices": []}

        # Detect collinear points (all on a single line): Delaunay cannot
        # triangulate 1-dimensional inputs and will raise QhullError.
        x_range = pts[:, 0].max() - pts[:, 0].min()
        y_range = pts[:, 1].max() - pts[:, 1].min()
        if x_range < 1e-6 or y_range < 1e-6:
            return {"vertices": np.zeros((0, 2), dtype=float), "indices": []}

        try:
            tri = Delaunay(pts)
        except (QhullError, ValueError, RuntimeError) as e:
            log.debug(f"Delaunay failed ({e}); returning empty mesh")
            return {"vertices": np.zeros((0, 2), dtype=float), "indices": []}
        indices = tri.simplices.tolist()

        # Remove triangles whose centroid falls outside the mask
        kept = []
        for t in indices:
            cx = int(round(pts[t].mean(axis=0)[0]))
            cy = int(round(pts[t].mean(axis=0)[1]))
            cx = max(0, min(w - 1, cx))
            cy = max(0, min(h - 1, cy))
            if mask[cy, cx] > 0:
                kept.append(tuple(int(i) for i in t))

        return {"vertices": pts, "indices": kept}
