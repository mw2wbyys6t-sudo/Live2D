#!/usr/bin/env python3
"""
Live2D Master Agent v9.0.0 - Professional AI-Assisted Live2D Creation Tool

Full pipeline: Text-to-Image → AI Layer Separation → PSD Export → QA → Desktop Pet / Go API

Usage:
    from live2d import Live2DWorkflow
    workflow = Live2DWorkflow()
    result = workflow.run("cute anime girl with pink hair")
"""

from live2d.version import __version__, get_version, get_version_string, FULL_VERSION_STRING

__all__ = [
    "__version__",
    "get_version",
    "get_version_string",
    "FULL_VERSION_STRING",
]

# Lazy imports for heavy modules
_lazy_imports = {
    "Live2DWorkflow": "live2d.workflow",
    "SecureConfig": "live2d.config",
    "SecureStorage": "live2d.secure_storage",
    "get_logger": "live2d.logger",
    "KMeansLayerer": "live2d.layering.kmeans",
    "Layer52Generator": "live2d.layering.layers52",
    "PSDCreator": "live2d.psd.creator",
    "PSDParser": "live2d.psd.parser",
    "DesktopPetAnimator": "live2d.pet.animator",
    "QAEngine": "live2d.qa.engine",
    "ProviderRouter": "live2d.image_gen.router",
}


def __getattr__(name):
    if name in _lazy_imports:
        import importlib
        module = importlib.import_module(_lazy_imports[name])
        return getattr(module, name)
    raise AttributeError(f"module 'live2d' has no attribute {name!r}")
