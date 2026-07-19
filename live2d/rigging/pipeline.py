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
        """Run rigging on ordered layers and export model files.
        
        NOTE: This is EXPERIMENTAL functionality.
        - Mesh geometry is generated but NOT bound to parameters
        - Deformer hierarchy is a template, not fully functional
        - Output is a scaffold, not a usable Live2D model
        - MOC3 file cannot be generated (requires Cubism Editor)
        """
        log.warning("=" * 60)
        log.warning("EXPERIMENTAL FEATURE: Auto-Rigging")
        log.warning("This generates a model scaffold, not a usable Live2D model.")
        log.warning("Mesh geometry is created but not bound to parameters.")
        log.warning("MOC3 export requires Cubism Editor (not generated here).")
        log.warning("=" * 60)
        
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

        # 4. Save mesh metadata guide (includes actual vertex data for inspection)
        guide_path = out / "mesh_guide.json"
        mesh_meta = {}
        for name, mesh in meshes.items():
            vertices = mesh["vertices"]
            indices = mesh["indices"]
            mesh_meta[name] = {
                "vertex_count": int(len(vertices)),
                "triangle_count": int(len(indices) // 3),
                "vertices": [[float(v[0]), float(v[1])] for v in vertices],
                "indices": [int(i) for i in indices],
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
            "experimental": True,
        }
