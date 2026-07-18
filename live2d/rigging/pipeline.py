#!/usr/bin/env python3
"""End-to-end automatic rigging pipeline."""

import json
from pathlib import Path
from typing import Dict

from PIL import Image

from live2d.exporter.model3_exporter import Model3Exporter
from live2d.logger import get_logger
from live2d.rigging.deformers import DeformerHierarchy
from live2d.rigging.mesh_generator import MeshGenerator
from live2d.rigging.parameters import ParameterSet

log = get_logger("rigging.pipeline")


class RiggingPipeline:
    """Generate meshes, deformers, parameters and export model3 scaffold."""

    def __init__(self):
        self.mesh_generator = MeshGenerator()
        self.deformer_hierarchy = DeformerHierarchy()
        self.parameters = ParameterSet()
        self.exporter = Model3Exporter()

    def run(
        self,
        layers: Dict[str, Image.Image],
        output_dir: str,
        character_name: str = "character",
    ) -> Dict:
        """Run rigging on ordered layers and export model files."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        # 1. Generate a mesh per non-empty layer
        meshes: Dict[str, Dict] = {}
        for name, layer in layers.items():
            mesh = self.mesh_generator.generate(layer)
            if len(mesh["vertices"]) > 0:
                meshes[name] = mesh

        # 2. Build deformer hierarchy
        deformer_tree = self.deformer_hierarchy.build(list(layers.keys()))

        # 3. Export model3 scaffold
        export_result = self.exporter.export(layers, output_dir=str(out), character_name=character_name)

        # 4. Save mesh metadata guide
        guide_path = out / "mesh_guide.json"
        mesh_meta = {
            name: {
                "vertex_count": int(len(mesh["vertices"])),
                "triangle_count": int(len(mesh["indices"])),
            }
            for name, mesh in meshes.items()
        }
        guide_path.write_text(json.dumps(mesh_meta, ensure_ascii=False, indent=2), encoding="utf-8")

        return {
            "output_dir": str(out),
            "model3_json": export_result["model3_json"],
            "texture": export_result["texture"],
            "textures": export_result.get("textures", []),
            "physics": export_result["physics"],
            "mesh_guide": str(guide_path),
            "meshes": meshes,
            "deformers": deformer_tree,
            "parameter_count": len(self.parameters),
        }
