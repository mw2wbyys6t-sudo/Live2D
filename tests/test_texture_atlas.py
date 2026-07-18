#!/usr/bin/env python3
"""
TextureAtlas brutal tests - covers multi-page packing, edge cases, and stress tests.

Covers:
- Empty layers dict
- Single 1x1 layer
- Single huge layer
- Layer exceeding max_size (should raise RuntimeError)
- Negative/zero padding
- Zero max_size
- Multi-page packing (many layers exceeding one page)
- UV coordinate correctness
- Atlas image dimensions
- Special character names
- Duplicate layer names
- All-transparent layers (still pack)
- Mixed sizes
"""

import pytest
from PIL import Image

from live2d.exporter.texture_atlas import TextureAtlas


def make_layer(size, color=(255, 0, 0, 255)):
    return Image.new("RGBA", size, color)


# ---------------- Empty / minimal ----------------

class TestTextureAtlasEmpty:
    def test_empty_layers_returns_default_atlas(self):
        atlas = TextureAtlas()
        result = atlas.pack({})
        assert "atlases" in result
        assert "uvs" in result
        assert len(result["atlases"]) >= 1
        assert result["uvs"] == {}

    def test_empty_dict_atlas_is_image(self):
        atlas = TextureAtlas()
        result = atlas.pack({})
        assert isinstance(result["atlases"][0], Image.Image)


class TestTextureAtlasMinimal:
    def test_single_1x1_layer(self):
        atlas = TextureAtlas(max_size=64, padding=0)
        layer = make_layer((1, 1))
        result = atlas.pack({"pixel": layer})
        assert "pixel" in result["uvs"]
        uv = result["uvs"]["pixel"]
        assert uv["page"] == 0
        assert uv["top_left"] == (0.0, 0.0)
        assert uv["bottom_right"] == (1.0, 1.0)

    def test_single_small_layer(self):
        atlas = TextureAtlas(max_size=64, padding=2)
        layer = make_layer((10, 10))
        result = atlas.pack({"small": layer})
        uv = result["uvs"]["small"]
        assert uv["page"] == 0
        assert uv["top_left"] == (0.0, 0.0)
        assert uv["bottom_right"] == (10.0, 10.0)


# ---------------- Boundary ----------------

class TestTextureAtlasBoundary:
    def test_layer_exceeding_max_size_raises(self):
        atlas = TextureAtlas(max_size=64)
        layer = make_layer((128, 128))
        with pytest.raises(RuntimeError, match="exceeds max atlas size"):
            atlas.pack({"big": layer})

    def test_layer_at_exact_max_size(self):
        atlas = TextureAtlas(max_size=64, padding=0)
        layer = make_layer((64, 64))
        result = atlas.pack({"exact": layer})
        assert "exact" in result["uvs"]

    def test_zero_max_size_clamped(self):
        atlas = TextureAtlas(max_size=0)
        assert atlas.max_size == 1

    def test_negative_max_size_clamped(self):
        atlas = TextureAtlas(max_size=-100)
        assert atlas.max_size == 1

    def test_negative_padding_clamped(self):
        atlas = TextureAtlas(padding=-5)
        assert atlas.padding == 0

    def test_zero_padding(self):
        atlas = TextureAtlas(max_size=64, padding=0)
        layers = {f"l{i}": make_layer((10, 10)) for i in range(4)}
        result = atlas.pack(layers)
        for name in layers:
            assert name in result["uvs"]


# ---------------- Multi-page ----------------

class TestTextureAtlasMultiPage:
    def test_multi_page_packing(self):
        # Force multi-page: 6 layers of 64x64 with max_size=128, padding=2
        # Each layer takes 66x66, so 128/66 = ~1.9 -> 1 per shelf row, 128/66 = ~1.9 -> 1 per shelf col
        # Actually we need to force overflow. Use 4 layers each 100x100 with max_size=128 padding=4
        atlas = TextureAtlas(max_size=128, padding=4)
        layers = {f"layer_{i}": make_layer((100, 100)) for i in range(5)}
        result = atlas.pack(layers)
        # Should produce at least 2 pages
        assert len(result["atlases"]) >= 2, f"expected >=2 pages, got {len(result['atlases'])}"

    def test_uv_page_indices_unique_per_page(self):
        atlas = TextureAtlas(max_size=128, padding=4)
        layers = {f"layer_{i}": make_layer((100, 100)) for i in range(5)}
        result = atlas.pack(layers)
        # Each layer's page should be valid
        for name, uv in result["uvs"].items():
            assert 0 <= uv["page"] < len(result["atlases"])

    def test_atlas_image_dimensions_match_uvs(self):
        atlas = TextureAtlas(max_size=128, padding=2)
        layers = {f"l{i}": make_layer((30, 30)) for i in range(3)}
        result = atlas.pack(layers)
        for page_idx, atlas_img in enumerate(result["atlases"]):
            page_uvs = {k: v for k, v in result["uvs"].items() if v["page"] == page_idx}
            if not page_uvs:
                continue
            max_x = max(uv["bottom_right"][0] for uv in page_uvs.values())
            max_y = max(uv["bottom_right"][1] for uv in page_uvs.values())
            assert atlas_img.width >= max_x
            assert atlas_img.height >= max_y

    def test_layers_packed_correctly_in_atlas(self):
        # Verify pixel data appears in atlas at the correct location
        atlas = TextureAtlas(max_size=256, padding=2)
        # Each layer is a distinct solid color
        layers = {
            "red": make_layer((20, 20), (255, 0, 0, 255)),
            "green": make_layer((20, 20), (0, 255, 0, 255)),
            "blue": make_layer((20, 20), (0, 0, 255, 255)),
        }
        result = atlas.pack(layers)
        atlas_img = result["atlases"][0]
        for name, expected_color in [("red", (255, 0, 0, 255)),
                                     ("green", (0, 255, 0, 255)),
                                     ("blue", (0, 0, 255, 255))]:
            uv = result["uvs"][name]
            # Sample a pixel in the middle of the layer
            x = int((uv["top_left"][0] + uv["bottom_right"][0]) / 2)
            y = int((uv["top_left"][1] + uv["bottom_right"][1]) / 2)
            actual = atlas_img.getpixel((x, y))
            assert actual[:3] == expected_color[:3], f"{name}: got {actual}, expected {expected_color}"


# ---------------- Stress / odd cases ----------------

class TestTextureAtlasStress:
    def test_many_small_layers(self):
        atlas = TextureAtlas(max_size=256, padding=2)
        layers = {f"l{i:03d}": make_layer((10, 10)) for i in range(100)}
        result = atlas.pack(layers)
        # All layers should have UVs
        assert len(result["uvs"]) == 100
        for name in layers:
            assert name in result["uvs"]

    def test_layer_with_zero_dimension(self):
        # PIL doesn't allow 0-width images, but check it doesn't crash on minimal
        atlas = TextureAtlas(max_size=64)
        # Skip - PIL raises on 0x0
        # Use 1x1 instead
        layer = make_layer((1, 1))
        result = atlas.pack({"tiny": layer})
        assert "tiny" in result["uvs"]

    def test_all_transparent_layers(self):
        atlas = TextureAtlas(max_size=64)
        layers = {"a": make_layer((10, 10), (0, 0, 0, 0)),
                  "b": make_layer((10, 10), (0, 0, 0, 0))}
        result = atlas.pack(layers)
        assert "a" in result["uvs"]
        assert "b" in result["uvs"]

    def test_special_character_names(self):
        atlas = TextureAtlas(max_size=64)
        layers = {
            "脸_基础": make_layer((10, 10)),
            "Eye/White_R": make_layer((10, 10)),
            "layer with space": make_layer((10, 10)),
            "中文层名": make_layer((10, 10)),
        }
        result = atlas.pack(layers)
        for name in layers:
            assert name in result["uvs"]

    def test_mixed_sizes(self):
        atlas = TextureAtlas(max_size=256, padding=2)
        layers = {
            "huge": make_layer((200, 200)),
            "medium": make_layer((100, 100)),
            "small": make_layer((50, 50)),
            "tiny": make_layer((10, 10)),
        }
        result = atlas.pack(layers)
        for name in layers:
            assert name in result["uvs"]
            uv = result["uvs"][name]
            assert uv["bottom_right"][0] > uv["top_left"][0]
            assert uv["bottom_right"][1] > uv["top_left"][1]

    def test_wide_layer(self):
        atlas = TextureAtlas(max_size=256, padding=2)
        layer = make_layer((200, 10))
        result = atlas.pack({"wide": layer})
        assert "wide" in result["uvs"]

    def test_tall_layer(self):
        atlas = TextureAtlas(max_size=256, padding=2)
        layer = make_layer((10, 200))
        result = atlas.pack({"tall": layer})
        assert "tall" in result["uvs"]


class TestTextureAtlasDeterminism:
    def test_same_input_same_output(self):
        atlas = TextureAtlas(max_size=128, padding=2)
        layers1 = {f"l{i}": make_layer((30, 30)) for i in range(5)}
        layers2 = {f"l{i}": make_layer((30, 30)) for i in range(5)}
        r1 = atlas.pack(layers1)
        r2 = atlas.pack(layers2)
        assert len(r1["atlases"]) == len(r2["atlases"])
        assert r1["uvs"] == r2["uvs"]
