"""Live2D automatic rigging package."""

from live2d.rigging.deformers import DeformerHierarchy
from live2d.rigging.mesh_generator import MeshGenerator
from live2d.rigging.parameters import ParameterSet
from live2d.rigging.pipeline import RiggingPipeline

__all__ = ["DeformerHierarchy", "MeshGenerator", "ParameterSet", "RiggingPipeline"]
