#!/usr/bin/env python3
"""
Model3Exporter brutal tests - validates JSON structure and file integrity.

Covers:
- Empty layers (degenerate case)
- Single layer
- Many layers (multi-texture)
- JSON schema (Version, FileReferences, Groups, Parameters)
- File existence on disk
- Texture file naming
- Expression files (smile, surprised, angry)
- Physics file content
- Special character names
- README_RIGGING.txt generation
- Round-trip JSON parseability
"""

import json
from pathlib import Path

import pytest
from PIL import Image

from live2d.exporter.model3_exporter import Model3Exporter


def make_layer(size, color=(255, 0, 0, 255)):
    return Image.new("RGBA", size, color)


# ---------------- Schema validation ----------------

class TestModel3ExporterSchema:
    def test_model3_json_has_required_top_level_keys(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path), character_name="test")
        with open(result["model3_json"], encoding="utf-8") as f:
            data = json.load(f)
        assert "Version" in data
        assert "FileReferences" in data
        assert "Groups" in data
        assert "HitAreas" in data
        assert "Parameters" in data

    def test_model3_json_version_is_3(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        with open(result["model3_json"], encoding="utf-8") as f:
            data = json.load(f)
        assert data["Version"] == 3.0

    def test_file_references_has_required_keys(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        with open(result["model3_json"], encoding="utf-8") as f:
            data = json.load(f)
        fr = data["FileReferences"]
        assert "Moc" in fr
        assert "Textures" in fr
        assert "Physics" in fr
        assert "Expressions" in fr

    def test_groups_contain_eye_blink_and_lipsync(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        with open(result["model3_json"], encoding="utf-8") as f:
            data = json.load(f)
        group_names = {g["Name"] for g in data["Groups"]}
        assert "EyeBlink" in group_names
        assert "LipSync" in group_names

    def test_eye_blink_uses_correct_param_ids(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        with open(result["model3_json"], encoding="utf-8") as f:
            data = json.load(f)
        blink = next(g for g in data["Groups"] if g["Name"] == "EyeBlink")
        assert "ParamEyeLOpen" in blink["Ids"]
        assert "ParamEyeROpen" in blink["Ids"]

    def test_lipsync_uses_mouth_param(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        with open(result["model3_json"], encoding="utf-8") as f:
            data = json.load(f)
        lipsync = next(g for g in data["Groups"] if g["Name"] == "LipSync")
        assert "ParamMouthOpenY" in lipsync["Ids"]

    def test_parameters_have_id_and_value(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        with open(result["model3_json"], encoding="utf-8") as f:
            data = json.load(f)
        assert len(data["Parameters"]) > 0
        for p in data["Parameters"]:
            assert "Id" in p
            assert "Value" in p
            assert isinstance(p["Value"], (int, float))

    def test_moc_reference_includes_moc3_extension(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path), character_name="hero")
        with open(result["model3_json"], encoding="utf-8") as f:
            data = json.load(f)
        assert data["FileReferences"]["Moc"].endswith(".moc3")
        assert "hero" in data["FileReferences"]["Moc"]


# ---------------- File integrity ----------------

class TestModel3ExporterFiles:
    def test_model3_json_file_exists(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        assert Path(result["model3_json"]).exists()

    def test_texture_files_exist(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32)),
                  "face": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        for tex_path in result["textures"]:
            assert Path(tex_path).exists()

    def test_physics_file_exists(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        assert Path(result["physics"]).exists()

    def test_readme_exists(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        # guide is README_RIGGING.txt
        assert "guide" in result
        assert Path(result["guide"]).exists()

    def test_expression_files_exist(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        with open(result["model3_json"], encoding="utf-8") as f:
            data = json.load(f)
        for exp in data["FileReferences"]["Expressions"]:
            exp_path = Path(result["model3_json"]).parent / exp["File"]
            assert exp_path.exists(), f"missing expression file: {exp_path}"

    def test_expression_count(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        with open(result["model3_json"], encoding="utf-8") as f:
            data = json.load(f)
        # Should have 3 expressions: smile, surprised, angry
        assert len(data["FileReferences"]["Expressions"]) == 3

    def test_expression_names(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        with open(result["model3_json"], encoding="utf-8") as f:
            data = json.load(f)
        names = {e["Name"] for e in data["FileReferences"]["Expressions"]}
        assert "smile" in names
        assert "surprised" in names
        assert "angry" in names

    def test_expression_json_schema(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        with open(result["model3_json"], encoding="utf-8") as f:
            data = json.load(f)
        for exp in data["FileReferences"]["Expressions"]:
            exp_path = Path(result["model3_json"]).parent / exp["File"]
            with open(exp_path, encoding="utf-8") as ef:
                exp_data = json.load(ef)
            assert exp_data["Type"] == "Live2D Expression"
            assert "FadeInTime" in exp_data
            assert "FadeOutTime" in exp_data
            assert "Parameters" in exp_data
            for p in exp_data["Parameters"]:
                assert "Id" in p
                assert "Value" in p

    def test_physics_json_is_valid(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        with open(result["physics"], encoding="utf-8") as f:
            physics = json.load(f)
        assert "version" in physics
        assert "physics_settings" in physics


# ---------------- Edge cases ----------------

class TestModel3ExporterEdgeCases:
    def test_empty_layers(self, tmp_path):
        exporter = Model3Exporter()
        result = exporter.export({}, output_dir=str(tmp_path))
        # Should still produce a valid model3.json
        assert Path(result["model3_json"]).exists()
        with open(result["model3_json"], encoding="utf-8") as f:
            data = json.load(f)
        assert data["Version"] == 3.0

    def test_single_layer(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"only": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        assert Path(result["model3_json"]).exists()
        assert len(result["textures"]) >= 1

    def test_special_character_name(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"脸": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path), character_name="角色_01")
        assert Path(result["model3_json"]).exists()
        # Filename should contain the character_name
        assert "角色_01" in Path(result["model3_json"]).name

    def test_many_layers_produce_textures(self, tmp_path):
        exporter = Model3Exporter(max_atlas_size=128)
        layers = {f"l{i:03d}": make_layer((50, 50)) for i in range(20)}
        result = exporter.export(layers, output_dir=str(tmp_path))
        # Multiple textures may be produced due to multi-page atlas
        assert len(result["textures"]) >= 1
        for tex in result["textures"]:
            assert Path(tex).exists()

    def test_character_name_with_spaces(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path), character_name="My Character")
        assert Path(result["model3_json"]).exists()

    def test_round_trip_json_parseable(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        # Re-read and ensure no JSON parse errors
        with open(result["model3_json"], encoding="utf-8") as f:
            json.load(f)
        with open(result["physics"], encoding="utf-8") as f:
            json.load(f)

    def test_output_dir_created_if_not_exists(self, tmp_path):
        exporter = Model3Exporter()
        nested = tmp_path / "nested" / "deep" / "path"
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(nested))
        assert nested.exists()
        assert Path(result["model3_json"]).exists()


class TestModel3ExporterReturnDict:
    def test_return_dict_has_required_keys(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        for key in ["model3_json", "texture", "textures", "physics", "guide", "output_dir"]:
            assert key in result, f"missing key in return dict: {key}"

    def test_texture_is_first_texture(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        if result["textures"]:
            assert result["texture"] == result["textures"][0]

    def test_output_dir_matches_input(self, tmp_path):
        exporter = Model3Exporter()
        layers = {"bg": make_layer((32, 32))}
        result = exporter.export(layers, output_dir=str(tmp_path))
        assert result["output_dir"] == str(tmp_path)
