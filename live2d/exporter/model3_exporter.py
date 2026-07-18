#!/usr/bin/env python3
"""Generate Cubism model3.json and companion files."""

import json
import time
from pathlib import Path
from typing import Dict, List

from PIL import Image

from live2d.exporter.texture_atlas import TextureAtlas
from live2d.logger import get_logger

log = get_logger("exporter.model3")


class Model3Exporter:
    """Export a Cubism model3.json scaffold plus textures and expressions."""

    def __init__(self, max_atlas_size: int = 2048):
        self.max_atlas_size = max_atlas_size

    def export(
        self,
        layers: Dict[str, Image.Image],
        output_dir: str,
        character_name: str = "character",
    ) -> Dict[str, str]:
        """Generate model3.json, textures, physics reference, expressions.

        Note: .moc3 is intentionally not generated here because it is a
        proprietary binary. Users import PSD + model3.json into Cubism Editor
        to produce the final .moc3.
        """
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        # Pack textures
        atlas = TextureAtlas(max_size=self.max_atlas_size)
        atlas_result = atlas.pack(layers)
        texture_files = []
        for idx, atlas_img in enumerate(atlas_result["atlases"]):
            texture_path = out / f"{character_name}.texture_{idx:02d}.png"
            atlas_img.save(texture_path)
            texture_files.append(f"{character_name}.texture_{idx:02d}.png")

        # Build parameter list from standard set
        from live2d.rigging.parameters import ParameterSet
        params = ParameterSet()
        param_list = [{"Id": p["id"], "Value": p["default"]} for p in params.values()]

        # Eye-blink and lip-sync groups
        groups = [
            {"Target": "Parameter", "Name": "EyeBlink", "Ids": ["ParamEyeLOpen", "ParamEyeROpen"]},
            {"Target": "Parameter", "Name": "LipSync", "Ids": ["ParamMouthOpenY"]},
        ]

        # Expressions
        expressions_dir = out / "expressions"
        expressions_dir.mkdir(exist_ok=True)
        expressions = []
        for exp_name, values in [
            ("smile", {"ParamMouthOpenY": 0.2, "ParamEyeLOpen": 0.9, "ParamEyeROpen": 0.9}),
            ("surprised", {"ParamMouthOpenY": 0.8, "ParamEyeLOpen": 1.0, "ParamEyeROpen": 1.0}),
            ("angry", {"ParamBrowLY": -0.8, "ParamBrowRY": -0.8, "ParamMouthForm": -0.5}),
        ]:
            exp_path = expressions_dir / f"{exp_name}.exp3.json"
            exp_data = {
                "Type": "Live2D Expression",
                "FadeInTime": 0.5,
                "FadeOutTime": 0.5,
                "Parameters": [{"Id": k, "Value": v} for k, v in values.items()],
            }
            exp_path.write_text(json.dumps(exp_data, ensure_ascii=False, indent=2), encoding="utf-8")
            expressions.append({"Name": exp_name, "File": f"expressions/{exp_name}.exp3.json"})

        # Physics reference
        physics_file = f"{character_name}.physics3.json"
        physics_path = out / physics_file
        from live2d.layering.layers52 import STANDARD_PHYSICS
        physics_path.write_text(json.dumps(STANDARD_PHYSICS, ensure_ascii=False, indent=2), encoding="utf-8")

        # model3.json
        model3 = {
            "Version": 3.0,
            "FileReferences": {
                "Moc": f"{character_name}.moc3",
                "Textures": texture_files,
                "Physics": physics_file,
                "Expressions": expressions,
            },
            "Groups": groups,
            "HitAreas": [],
            "Parameters": param_list,
        }
        model3_path = out / f"{character_name}.model3.json"
        model3_path.write_text(json.dumps(model3, ensure_ascii=False, indent=2), encoding="utf-8")

        # Human-readable notes
        guide_path = out / "README_RIGGING.txt"
        guide_path.write_text(
            f"Live2D Rigging Output for '{character_name}'\n"
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            "This package contains model3.json + textures + physics.\n"
            "Import the PSD into Cubism Editor, then load this model3.json\n"
            "as a reference to generate the final .moc3 file.\n",
            encoding="utf-8",
        )

        return {
            "model3_json": str(model3_path),
            "texture": str(out / texture_files[0]) if texture_files else "",
            "textures": [str(out / f) for f in texture_files],
            "physics": str(physics_path),
            "guide": str(guide_path),
            "output_dir": str(out),
        }
