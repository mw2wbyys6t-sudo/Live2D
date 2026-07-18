#!/usr/bin/env python3
"""
MeshGenerator brutal tests - covers edge cases, exceptions, and complex shapes.

Covers:
- Empty / fully transparent images
- 1x1 pixel images
- Fully opaque images
- Tiny regions
- Thin strips (1px wide / tall)
- Multi-component regions (disconnected blobs)
- Complex concave shapes (L-shape, U-shape, ring)
- Large images
- Mode conversions (RGB, L, P -> RGBA)
- Idempotency / determinism
- Output schema validation
"""

import numpy as np
import pytest
from PIL import Image, ImageDraw

from live2d.rigging.mesh_generator import MeshGenerator


# ---------------- Helpers ----------------

def make_image(size, mode="RGBA", fill=(0, 0, 0, 0)):
    return Image.new(mode, size, fill)


def draw_filled(width, height, polygon, color=(255, 0, 0, 255)):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.polygon(polygon, fill=color)
    return img


# ---------------- Edge cases ----------------

class TestMeshGeneratorEdgeCases:
    def test_empty_image_1x1_transparent(self):
        mg = MeshGenerator()
        img = make_image((1, 1), fill=(0, 0, 0, 0))
        result = mg.generate(img)
        assert len(result["vertices"]) == 0
        assert result["indices"] == []
        assert isinstance(result["vertices"], np.ndarray)

    def test_empty_image_large_transparent(self):
        mg = MeshGenerator()
        img = make_image((256, 256), fill=(0, 0, 0, 0))
        result = mg.generate(img)
        assert len(result["vertices"]) == 0
        assert result["indices"] == []

    def test_single_opaque_pixel(self):
        mg = MeshGenerator()
        img = make_image((10, 10), fill=(0, 0, 0, 0))
        img.putpixel((5, 5), (255, 0, 0, 255))
        result = mg.generate(img)
        # 1 pixel cannot form a triangle; vertices may be empty or fewer than 3
        assert len(result["vertices"]) < 3
        assert result["indices"] == []

    def test_two_pixel_blob(self):
        mg = MeshGenerator()
        img = make_image((10, 10), fill=(0, 0, 0, 0))
        img.putpixel((5, 5), (255, 0, 0, 255))
        img.putpixel((5, 6), (255, 0, 0, 255))
        result = mg.generate(img)
        # Cannot triangulate 2 distinct points (need 3 minimum)
        assert len(result["vertices"]) <= 3
        # If vertices==3 but centroid outside mask, indices should be empty
        for t in result["indices"]:
            assert len(t) == 3

    def test_three_pixel_triangle(self):
        mg = MeshGenerator()
        img = make_image((20, 20), fill=(0, 0, 0, 0))
        img.putpixel((5, 5), (255, 0, 0, 255))
        img.putpixel((7, 5), (255, 0, 0, 255))
        img.putpixel((6, 7), (255, 0, 0, 255))
        result = mg.generate(img)
        # Should produce at most 1 triangle (and indices may be empty if dedup removes points)
        if len(result["vertices"]) >= 3:
            for t in result["indices"]:
                assert len(t) == 3
                for i in t:
                    assert 0 <= i < len(result["vertices"])

    def test_fully_opaque_image(self):
        mg = MeshGenerator()
        img = make_image((64, 64), fill=(255, 0, 0, 255))
        result = mg.generate(img)
        assert len(result["vertices"]) >= 3
        assert len(result["indices"]) > 0
        # All triangle centroids must be inside mask
        arr = np.array(img)
        alpha = arr[:, :, 3]
        mask = (alpha > 128).astype(np.uint8)
        for t in result["indices"]:
            pts = result["vertices"][list(t)]
            cx = int(round(pts[:, 0].mean()))
            cy = int(round(pts[:, 1].mean()))
            cx = max(0, min(63, cx))
            cy = max(0, min(63, cy))
            assert mask[cy, cx] > 0

    def test_extreme_large_image(self):
        mg = MeshGenerator(internal_spacing=64, contour_spacing=24)
        img = make_image((1024, 1024), fill=(255, 0, 0, 255))
        result = mg.generate(img)
        assert len(result["vertices"]) >= 3
        assert len(result["indices"]) > 0

    def test_thin_horizontal_strip(self):
        mg = MeshGenerator()
        img = make_image((100, 4), fill=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 1, 99, 1], fill=(255, 0, 0, 255))
        result = mg.generate(img)
        # Should not crash; triangle count may be low
        assert isinstance(result["vertices"], np.ndarray)

    def test_thin_vertical_strip(self):
        mg = MeshGenerator()
        img = make_image((4, 100), fill=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([1, 0, 1, 99], fill=(255, 0, 0, 255))
        result = mg.generate(img)
        assert isinstance(result["vertices"], np.ndarray)


class TestMeshGeneratorComplexShapes:
    def test_concave_L_shape(self):
        # L-shape: left column [10,50]x[10,90] + bottom row [10,90]x[60,90]
        # Removed region: x in (50,90), y in (10,60)
        img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([10, 10, 50, 90], fill=(255, 0, 0, 255))
        draw.rectangle([10, 60, 90, 90], fill=(255, 0, 0, 255))
        mg = MeshGenerator()
        result = mg.generate(img)
        assert len(result["vertices"]) >= 3
        assert len(result["indices"]) > 0
        # Validate no triangle centroid in the transparent (removed) region
        arr = np.array(img)
        alpha = arr[:, :, 3]
        mask = (alpha > 128).astype(np.uint8)
        h, w = mask.shape
        for t in result["indices"]:
            pts = result["vertices"][list(t)]
            cx = int(round(pts[:, 0].mean()))
            cy = int(round(pts[:, 1].mean()))
            cx = max(0, min(w - 1, cx))
            cy = max(0, min(h - 1, cy))
            assert mask[cy, cx] > 0, f"centroid ({cx},{cy}) outside L-shape"

    def test_U_shape(self):
        # U-shape with hole in the middle (connected only at bottom)
        img = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([10, 10, 110, 110], fill=(255, 0, 0, 255))
        draw.rectangle([40, 10, 80, 80], fill=(0, 0, 0, 0))
        mg = MeshGenerator()
        result = mg.generate(img)
        assert len(result["vertices"]) >= 3
        # Check no triangle centroid in the carved-out region
        for t in result["indices"]:
            pts = result["vertices"][list(t)]
            cx = int(round(pts[:, 0].mean()))
            cy = int(round(pts[:, 1].mean()))
            if 40 < cx < 80 and 10 < cy < 80:
                # Should not be possible: that region has alpha=0
                arr = np.array(img)
                assert arr[cy, cx, 3] > 128

    def test_ring_shape(self):
        # Annulus
        img = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([10, 10, 190, 190], fill=(255, 0, 0, 255))
        draw.ellipse([60, 60, 140, 140], fill=(0, 0, 0, 0))
        mg = MeshGenerator()
        result = mg.generate(img)
        assert len(result["vertices"]) >= 3

    def test_two_disconnected_blobs(self):
        img = Image.new("RGBA", (200, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([10, 10, 80, 80], fill=(255, 0, 0, 255))
        draw.ellipse([120, 10, 190, 80], fill=(0, 255, 0, 255))
        mg = MeshGenerator()
        result = mg.generate(img)
        # Delaunay may bridge both blobs; ensure no triangle centroid outside mask
        arr = np.array(img)
        alpha = arr[:, :, 3]
        mask = (alpha > 128).astype(np.uint8)
        for t in result["indices"]:
            pts = result["vertices"][list(t)]
            cx = int(round(pts[:, 0].mean()))
            cy = int(round(pts[:, 1].mean()))
            cx = max(0, min(199, cx))
            cy = max(0, min(99, cy))
            assert mask[cy, cx] > 0

    def test_many_disconnected_blobs(self):
        img = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        for cx, cy in [(50, 50), (150, 80), (250, 200), (350, 100), (100, 300), (300, 350)]:
            draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(255, 0, 0, 255))
        mg = MeshGenerator()
        result = mg.generate(img)
        arr = np.array(img)
        mask = (arr[:, :, 3] > 128).astype(np.uint8)
        for t in result["indices"]:
            pts = result["vertices"][list(t)]
            cx = int(round(pts[:, 0].mean()))
            cy = int(round(pts[:, 1].mean()))
            cx = max(0, min(399, cx))
            cy = max(0, min(399, cy))
            assert mask[cy, cx] > 0


class TestMeshGeneratorInputModes:
    def test_rgb_image_input(self):
        mg = MeshGenerator()
        img = Image.new("RGB", (64, 64), (255, 0, 0))
        result = mg.generate(img)
        # RGB has no alpha channel; convert("RGBA") gives alpha=255 (opaque)
        assert len(result["vertices"]) >= 3
        assert len(result["indices"]) > 0

    def test_l_image_input(self):
        mg = MeshGenerator()
        img = Image.new("L", (64, 64), 128)
        result = mg.generate(img)
        # Grayscale; convert to RGBA should give opaque
        assert len(result["vertices"]) >= 3

    def test_p_image_input(self):
        mg = MeshGenerator()
        img = Image.new("P", (64, 64), 0)
        result = mg.generate(img)
        assert isinstance(result["vertices"], np.ndarray)


class TestMeshGeneratorDeterminism:
    def test_same_input_same_output(self):
        mg = MeshGenerator()
        img1 = draw_filled(100, 100, [(10, 10), (90, 10), (90, 90), (10, 90)])
        img2 = draw_filled(100, 100, [(10, 10), (90, 10), (90, 90), (10, 90)])
        r1 = mg.generate(img1)
        r2 = mg.generate(img2)
        assert len(r1["vertices"]) == len(r2["vertices"])
        assert len(r1["indices"]) == len(r2["indices"])
        np.testing.assert_array_equal(r1["vertices"], r2["vertices"])

    def test_constructor_clamps_invalid_spacing(self):
        mg = MeshGenerator(internal_spacing=0, contour_spacing=-5)
        # Spacing clamped to minimum 4
        assert mg.internal_spacing == 4
        assert mg.contour_spacing == 4
        # Should still produce a valid result
        img = draw_filled(64, 64, [(10, 10), (50, 10), (50, 50), (10, 50)])
        result = mg.generate(img)
        assert len(result["vertices"]) >= 3


class TestMeshGeneratorOutputSchema:
    def test_output_keys_present(self):
        mg = MeshGenerator()
        img = draw_filled(64, 64, [(10, 10), (50, 10), (50, 50), (10, 50)])
        result = mg.generate(img)
        assert "vertices" in result
        assert "indices" in result

    def test_vertices_dtype_float(self):
        mg = MeshGenerator()
        img = draw_filled(64, 64, [(10, 10), (50, 10), (50, 50), (10, 50)])
        result = mg.generate(img)
        assert result["vertices"].dtype == float

    def test_indices_within_bounds(self):
        mg = MeshGenerator()
        img = draw_filled(64, 64, [(10, 10), (50, 10), (50, 50), (10, 50)])
        result = mg.generate(img)
        n = len(result["vertices"])
        for t in result["indices"]:
            assert len(t) == 3
            for i in t:
                assert 0 <= i < n

    def test_vertices_within_image_bounds(self):
        mg = MeshGenerator()
        img = draw_filled(64, 64, [(10, 10), (50, 10), (50, 50), (10, 50)])
        result = mg.generate(img)
        for x, y in result["vertices"]:
            assert 0 <= x <= 63
            assert 0 <= y <= 63
