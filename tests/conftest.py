#!/usr/bin/env python3
"""
Live2D Master Agent v8.0 - Test Configuration and Shared Fixtures

All tests run WITHOUT requiring real API keys:
- HTTP requests are mocked
- All file operations use temp directories
- Tests verify functionality, not external services
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

import pytest
import numpy as np
from PIL import Image

# Ensure project root is in path
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
os.environ.setdefault("LIVE2D_PROJECT_ROOT", _PROJECT_ROOT)
os.environ["LIVE2D_TELEMETRY"] = "0"
os.environ["LIVE2D_LOG_LEVEL"] = "ERROR"  # Quiet during tests
sys.path.insert(0, _PROJECT_ROOT)


@pytest.fixture
def project_root():
    return Path(_PROJECT_ROOT)


@pytest.fixture
def tmp_output(tmp_path):
    """Temporary output directory."""
    out = tmp_path / "output"
    out.mkdir()
    return str(out)


@pytest.fixture
def test_image(tmp_path):
    """Create a synthetic test character image (512x512 RGBA)."""
    img = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    # Head (skin color circle)
    draw.ellipse([156, 50, 356, 250], fill=(255, 210, 190, 255))
    # Hair (dark color on top)
    draw.ellipse([140, 30, 372, 160], fill=(60, 40, 80, 255))
    # Eyes (white + iris + pupil)
    draw.ellipse([200, 130, 235, 160], fill=(255, 255, 255, 255))
    draw.ellipse([277, 130, 312, 160], fill=(255, 255, 255, 255))
    draw.ellipse([210, 138, 228, 155], fill=(80, 120, 200, 255))
    draw.ellipse([287, 138, 305, 155], fill=(80, 120, 200, 255))
    draw.ellipse([215, 142, 223, 150], fill=(20, 20, 30, 255))
    draw.ellipse([292, 142, 300, 150], fill=(20, 20, 30, 255))
    # Mouth
    draw.ellipse([240, 190, 272, 210], fill=(200, 80, 100, 255))
    # Body
    draw.rectangle([190, 245, 322, 420], fill=(100, 120, 200, 255))
    # Neck
    draw.rectangle([235, 220, 277, 260], fill=(255, 210, 190, 255))
    # Blush
    draw.ellipse([170, 165, 200, 185], fill=(255, 150, 160, 120))
    draw.ellipse([312, 165, 342, 185], fill=(255, 150, 160, 120))
    # White background
    bg = Image.new('RGBA', (512, 512), (255, 255, 255, 255))
    bg.paste(img, (0, 0), img)
    path = tmp_path / "test_character.png"
    bg.save(path)
    return str(path)


@pytest.fixture
def test_layers_dir(tmp_path, test_image):
    """Create a directory with test layer PNGs."""
    layers_dir = tmp_path / "layers"
    layers_dir.mkdir()
    img = Image.open(test_image).convert('RGBA')
    arr = np.array(img)
    # Create 4 simple layers (background, hair, face, body)
    colors = [
        ("layer_000.png", np.array([255, 255, 255, 255]), 0.12),  # white bg
        ("layer_001.png", np.array([60, 40, 80, 255]), 0.35),     # hair (dark)
        ("layer_002.png", np.array([255, 210, 190, 255]), 0.2),   # skin
        ("layer_003.png", np.array([100, 120, 200, 255]), 0.18),  # clothes
    ]
    for fname, target_color, thresh in colors:
        layer = np.zeros_like(arr)
        diff = np.abs(arr[:,:,:3].astype(float) - target_color[:3].astype(float)).sum(axis=2)
        mask = diff < 80
        layer[mask] = arr[mask]
        Image.fromarray(layer, 'RGBA').save(layers_dir / fname)
    preview = img.copy()
    preview.save(layers_dir / "preview.png")
    return str(layers_dir)


@pytest.fixture
def mock_requests(monkeypatch):
    """Mock requests to avoid real HTTP calls. Returns a mock object."""
    class MockResponse:
        def __init__(self, status_code=200, content=None, json_data=None, headers=None):
            self.status_code = status_code
            self._content = content or b'\x89PNG\r\n\x1a\n' + b'\x00' * 100
            self._json_data = json_data or {"data": [{"url": "https://example.com/img.png"}]}
            self.headers = headers or {"Content-Type": "image/png"}

        @property
        def content(self):
            return self._content

        def json(self):
            return self._json_data

        def raise_for_status(self):
            if self.status_code >= 400:
                from requests import HTTPError
                raise HTTPError(f"HTTP {self.status_code}")

    class MockRequests:
        def __init__(self):
            self.calls = []
            self._response = MockResponse()

        def get(self, url, **kwargs):
            self.calls.append(("GET", url, kwargs))
            return self._response

        def post(self, url, **kwargs):
            self.calls.append(("POST", url, kwargs))
            # For image gen APIs, return a small PNG
            png_header = b'\x89PNG\r\n\x1a\n'
            return MockResponse(
                content=png_header + b'\x00' * 200,
                json_data={"data": [{"b64_json": "iVBORw0KGgoAAAANSUhEUgAA==", "url": ""}]}
            )

        def set_response(self, **kwargs):
            self._response = MockResponse(**kwargs)

    mock = MockRequests()
    import requests as req_module
    monkeypatch.setattr(req_module, "get", mock.get)
    monkeypatch.setattr(req_module, "post", mock.post)
    return mock


# Ensure config loads as singleton fresh for each test
@pytest.fixture(autouse=True)
def reset_config():
    """Reset config singleton between tests."""
    import live2d.config as cfg_mod
    cfg_mod.SecureConfig._instance = None
    cfg_mod.SecureConfig._loaded = False
    yield
    cfg_mod.SecureConfig._instance = None
    cfg_mod.SecureConfig._loaded = False
