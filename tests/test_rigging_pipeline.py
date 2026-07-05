#!/usr/bin/env python3
"""
RiggingPipeline end-to-end brutal tests.

Covers:
- Empty layers dict
- Single layer
- Many layers (52-layer simulation)
- Real character image
- All-transparent layers (should be skipped)
- Mixed empty/non-empty layers
- Output file integrity
- Mesh guide JSON
- Deformer tree present
- Parameter count
- Special character names in pipeline
- Re-running pipeline (idempotency on output dir)
"""

import json
from collections import OrderedDict
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

from live2d.rigging.pipeline import RiggingPipeline


def make_layer(size, color=(255, 0, 0, 255)):
    return Image.new("RGBA", size, color)


def make_character_image(size=(256, 256)):
    """Create a synthetic character-like image with multiple colored regions."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Background
    draw.rectangle([0, 0, size[0], size[1]], fill=(255, 255, 255, 255))
    # Head
    draw.ellipse([80, 40, 180, 140], fill=(255, 210, 190, 255))
    # Hair
    draw.ellipse([70, 30, 190, 100], fill=(60, 40, 80, 255))
    # Eyes
    draw.ellipse([100, 80, 120, 100], fill=(255, 255, 255, 255))
    draw.ellipse([140, 80, 160, 100], fill=(255, 255, 255, 255))
    draw.ellipse([105, 85, 115, 95], fill=(80, 120, 200, 255))
    draw.ellipse([145, 85, 155, 95], fill=(80, 120, 200, 255))
    # Mouth
    draw.ellipse([115, 115, 145, 135], fill=(200, 80, 100, 255))
    # Body
    draw.rectangle([95, 140, 165, 220], fill=(100, 120, 200, 255))
    return img


def split_to_layers(img):
    """Split an image into 4 simple color-based layers."""
    import numpy as np
    arr = np.array(img)
    layers = OrderedDict()
    color_specs = [
        ("background", np.array([255, 255, 255, 255])),
        ("hair", np.array([60, 40, 80, 255])),
        ("skin", np.array([255, 210, 190, 255])),
        ("clothes", np.array([100, 120, 200, 255])),
    ]
    for name, target in color_specs:
        layer = np.zeros_like(arr)
        diff = np.abs(arr[:, :, :3].astype(float) - target[:3].astype(float)).sum(axis=2)
        mask = diff < 60
        layer[mask] = arr[mask]
        layers[name] = Image.fromarray(layer, "RGBA")
    return layers


# ---------------- Basic ----------------

class TestRiggingPipelineBasic:
    def test_run_with_empty_layers(self, tmp_path):
        pipeline = RiggingPipeline()
        result = pipeline.run(OrderedDict(), output_dir=str(tmp_path / "rigged"))
        assert Path(result["output_dir"]).exists()
        assert Path(result["model3_json"]).exists()
        assert Path(result["physics"]).exists()
        assert Path(result["mesh_guide"]).exists()

    def test_run_with_single_layer(self, tmp_path):
        pipeline = RiggingPipeline()
        layers = OrderedDict([("bg", make_layer((64, 64)))])
        result = pipeline.run(layers, output_dir=str(tmp_path / "rigged"))
        assert Path(result["model3_json"]).exists()
        assert Path(result["mesh_guide"]).exists()

    def test_run_with_many_layers(self, tmp_path):
        pipeline = RiggingPipeline()
        layers = OrderedDict((f"layer_{i:02d}", make_layer((32, 32))) for i in range(20))
        result = pipeline.run(layers, output_dir=str(tmp_path / "rigged"))
        assert Path(result["model3_json"]).exists()
        # All non-empty layers should have meshes
        assert len(result["meshes"]) == 20


# ---------------- Real image ----------------

class TestRiggingPipelineRealImage:
    def test_run_with_synthetic_character(self, tmp_path):
        img = make_character_image()
        layers = split_to_layers(img)
        pipeline = RiggingPipeline()
        result = pipeline.run(layers, output_dir=str(tmp_path / "rigged"),
                              character_name="test_char")
        assert Path(result["model3_json"]).exists()
        assert Path(result["mesh_guide"]).exists()
        # At least one layer should have a mesh
        assert len(result["meshes"]) > 0

    def test_mesh_guide_has_correct_schema(self, tmp_path):
        img = make_character_image()
        layers = split_to_layers(img)
        pipeline = RiggingPipeline()
        result = pipeline.run(layers, output_dir=str(tmp_path / "rigged"))
        with open(result["mesh_guide"], encoding="utf-8") as f:
            guide = json.load(f)
        for name, meta in guide.items():
            assert "vertex_count" in meta
            assert "triangle_count" in meta
            assert isinstance(meta["vertex_count"], int)
            assert isinstance(meta["triangle_count"], int)

    def test_mesh_counts_match_result(self, tmp_path):
        img = make_character_image()
        layers = split_to_layers(img)
        pipeline = RiggingPipeline()
        result = pipeline.run(layers, output_dir=str(tmp_path / "rigged"))
        with open(result["mesh_guide"], encoding="utf-8") as f:
            guide = json.load(f)
        for name, mesh in result["meshes"].items():
            assert guide[name]["vertex_count"] == len(mesh["vertices"])
            assert guide[name]["triangle_count"] == len(mesh["indices"])


# ---------------- Edge cases ----------------

class TestRiggingPipelineEdgeCases:
    def test_all_transparent_layers(self, tmp_path):
        pipeline = RiggingPipeline()
        layers = OrderedDict([
            ("empty1", make_layer((32, 32), (0, 0, 0, 0))),
            ("empty2", make_layer((32, 32), (0, 0, 0, 0))),
        ])
        result = pipeline.run(layers, output_dir=str(tmp_path / "rigged"))
        # No meshes should be produced
        assert len(result["meshes"]) == 0
        # But model3.json should still be created
        assert Path(result["model3_json"]).exists()

    def test_mixed_empty_and_filled_layers(self, tmp_path):
        pipeline = RiggingPipeline()
        layers = OrderedDict([
            ("empty", make_layer((32, 32), (0, 0, 0, 0))),
            ("filled", make_layer((32, 32), (255, 0, 0, 255))),
        ])
        result = pipeline.run(layers, output_dir=str(tmp_path / "rigged"))
        # Only the filled layer should have a mesh
        assert "filled" in result["meshes"]
        assert "empty" not in result["meshes"]

    def test_special_character_names(self, tmp_path):
        pipeline = RiggingPipeline()
        layers = OrderedDict([
            ("脸_基础", make_layer((32, 32))),
            ("头发_后", make_layer((32, 32))),
            ("Eye/White_R", make_layer((32, 32))),
        ])
        result = pipeline.run(layers, output_dir=str(tmp_path / "rigged"),
                              character_name="角色_01")
        assert Path(result["model3_json"]).exists()
        # All layers should have meshes
        assert len(result["meshes"]) == 3

    def test_deformer_tree_present(self, tmp_path):
        pipeline = RiggingPipeline()
        layers = OrderedDict([("bg", make_layer((32, 32)))])
        result = pipeline.run(layers, output_dir=str(tmp_path / "rigged"))
        tree = result["deformers"]
        assert tree["id"] == "Root"
        assert "children" in tree

    def test_parameter_count(self, tmp_path):
        pipeline = RiggingPipeline()
        layers = OrderedDict([("bg", make_layer((32, 32)))])
        result = pipeline.run(layers, output_dir=str(tmp_path / "rigged"))
        assert result["parameter_count"] >= 16

    def test_run_creates_output_dir(self, tmp_path):
        pipeline = RiggingPipeline()
        nested = tmp_path / "deep" / "nested" / "rigged"
        layers = OrderedDict([("bg", make_layer((32, 32)))])
        result = pipeline.run(layers, output_dir=str(nested))
        assert nested.exists()

    def test_run_with_extremely_small_layers(self, tmp_path):
        pipeline = RiggingPipeline()
        layers = OrderedDict([
            ("tiny", make_layer((1, 1))),
            ("small", make_layer((2, 2))),
        ])
        result = pipeline.run(layers, output_dir=str(tmp_path / "rigged"))
        # Should not crash
        assert Path(result["model3_json"]).exists()

    def test_textures_list_returned(self, tmp_path):
        pipeline = RiggingPipeline()
        layers = OrderedDict([("bg", make_layer((32, 32)))])
        result = pipeline.run(layers, output_dir=str(tmp_path / "rigged"))
        assert isinstance(result["textures"], list)
        assert len(result["textures"]) >= 1
        for tex in result["textures"]:
            assert Path(tex).exists()


# ---------------- Idempotency ----------------

class TestRiggingPipelineIdempotency:
    def test_re_run_overwrites_output(self, tmp_path):
        pipeline = RiggingPipeline()
        layers = OrderedDict([("bg", make_layer((32, 32)))])
        out = tmp_path / "rigged"
        result1 = pipeline.run(layers, output_dir=str(out))
        result2 = pipeline.run(layers, output_dir=str(out))
        # Same paths
        assert result1["model3_json"] == result2["model3_json"]
        # Files exist
        assert Path(result2["model3_json"]).exists()

    def test_two_pipelines_same_output(self, tmp_path):
        layers = OrderedDict([("bg", make_layer((32, 32)))])
        out = tmp_path / "rigged"
        p1 = RiggingPipeline()
        r1 = p1.run(layers, output_dir=str(out))
        p2 = RiggingPipeline()
        r2 = p2.run(layers, output_dir=str(out))
        # Parameter counts should match
        assert r1["parameter_count"] == r2["parameter_count"]
