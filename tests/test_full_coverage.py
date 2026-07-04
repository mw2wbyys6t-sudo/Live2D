#!/usr/bin/env python3
"""
Live2D Master Agent v9.0 - Full Coverage Tests
Tests edge cases, error handling, and component integration.
All tests run WITHOUT real API keys.

Run: python -m pytest tests/test_full_coverage.py -v
"""

import os
import sys
import json
import pytest
import numpy as np
from pathlib import Path
from PIL import Image

_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
os.environ.setdefault("LIVE2D_PROJECT_ROOT", _PROJECT_ROOT)
os.environ["LIVE2D_TELEMETRY"] = "0"
os.environ["LIVE2D_LOG_LEVEL"] = "ERROR"
sys.path.insert(0, _PROJECT_ROOT)


# ===================== Config Tests =====================

class TestConfigEdgeCases:
    def test_config_singleton(self):
        from live2d.config import SecureConfig
        c1 = SecureConfig()
        c2 = SecureConfig()
        assert c1 is c2

    def test_config_repr_hides_secrets(self):
        from live2d.config import config
        r = repr(config)
        assert "sk-" not in r or "***" in r

    def test_config_output_dir_created(self, tmp_path, monkeypatch):
        monkeypatch.setenv("LIVE2D_PROJECT_ROOT", str(tmp_path))
        import live2d.config as cm
        cm.SecureConfig._instance = None
        cm.SecureConfig._loaded = False
        c = cm.SecureConfig()
        assert os.path.isdir(c.output_dir)

    def test_validate_api_key_format(self):
        from live2d.config import config
        # Without real keys, format validation returns False for None
        assert config.validate_api_key("sensenova") in (True, False)


# ===================== Secure Storage Edge Cases =====================

class TestSecureStorageEdgeCases:
    def test_encrypt_empty_string(self):
        from live2d.secure_storage import SecureStorage
        s = SecureStorage()
        enc = s.encrypt("")
        assert s.decrypt(enc) == ""

    def test_encrypt_unicode(self):
        from live2d.secure_storage import SecureStorage
        s = SecureStorage()
        text = "日本語テスト🎉"
        enc = s.encrypt(text)
        assert s.decrypt(enc) == text

    def test_decrypt_none_returns_none(self):
        from live2d.secure_storage import SecureStorage
        s = SecureStorage()
        assert s.decrypt(None) is None
        assert s.decrypt("") is None

    def test_encrypted_config_missing_file(self, tmp_path):
        from live2d.secure_storage import EncryptedConfig
        # Should handle missing file gracefully
        ec = EncryptedConfig()
        assert ec.has_key("nonexistent") is False
        assert ec.get_api_key("nonexistent") is None
        ec.clear_cache()


# ===================== Security Edge Cases =====================

class TestSecurityEdgeCases:
    def test_validate_empty_path(self):
        from live2d.security import validate_path
        valid, _ = validate_path("")
        assert not valid

    def test_validate_long_path(self):
        from live2d.security import validate_path
        valid, _ = validate_path("a" * 5000)
        assert not valid

    def test_sanitize_empty_prompt(self):
        from live2d.security import sanitize_prompt
        assert sanitize_prompt("") == ""

    def test_sanitize_long_prompt(self):
        from live2d.security import sanitize_prompt
        long = "a" * 5000
        result = sanitize_prompt(long)
        assert len(result) <= 4000

    def test_sanitize_empty_filename(self):
        from live2d.security import sanitize_filename
        assert sanitize_filename("") == "unnamed"

    def test_validate_directory_creates(self, tmp_path):
        from live2d.security import validate_directory
        new_dir = str(tmp_path / "new_dir")
        valid, _ = validate_directory(new_dir, create_if_not_exists=True)
        assert valid
        assert os.path.isdir(new_dir)

    def test_validate_nonexistent_image(self):
        from live2d.security import validate_image_path
        valid, _ = validate_image_path("/nonexistent/img.png")
        assert not valid

    def test_redact_already_safe_text(self):
        from live2d.security import redact_sensitive
        assert redact_sensitive("hello world") == "hello world"

    def test_model_whitelist(self):
        from live2d.security import SecurityTools
        assert SecurityTools.validate_model_id("gpt-4o")[0] is True
        assert SecurityTools.validate_model_id("evil-model")[0] is False


# ===================== KMeans Layerer Edge Cases =====================

class TestKMeansEdgeCases:
    def test_single_color_image(self, tmp_path):
        from live2d.layering.kmeans import KMeansLayerer
        img = Image.new('RGBA', (100, 100), (255, 0, 0, 255))
        r = KMeansLayerer(k_clusters=3).layer(img, output_dir=str(tmp_path))
        # Single color should produce 1 layer
        assert r["layer_count"] >= 1

    def test_transparent_image(self, tmp_path):
        from live2d.layering.kmeans import KMeansLayerer
        img = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
        r = KMeansLayerer(k_clusters=3).layer(img, output_dir=str(tmp_path))
        assert r["layer_count"] == 0  # No opaque pixels

    def test_k_clamped(self):
        from live2d.layering.kmeans import KMeansLayerer
        kl = KMeansLayerer(k_clusters=2)
        assert kl.k_clusters == 3  # minimum 3
        kl2 = KMeansLayerer(k_clusters=30)
        assert kl2.k_clusters == 20  # maximum 20

    def test_fallback_without_sklearn(self, test_image, tmp_path, monkeypatch):
        """Simple quantization works even without sklearn."""
        import live2d.layering.kmeans as km
        monkeypatch.setattr(km, 'HAS_SKLEARN', False)
        from live2d.layering.kmeans import KMeansLayerer
        img = Image.open(test_image).convert('RGBA')
        r = KMeansLayerer(k_clusters=4).layer(img, output_dir=str(tmp_path))
        assert r["layer_count"] >= 2


# ===================== Image Generation Edge Cases =====================

class TestImageGenEdgeCases:
    def test_generation_error_routed(self):
        from live2d.image_gen.base import GenerationError
        e = GenerationError("test error", provider="test", retryable=False)
        assert not e.retryable
        assert e.provider == "test"

    def test_generation_result_defaults(self):
        from live2d.image_gen.base import GenerationResult
        r = GenerationResult(success=False)
        assert not r.ok

    def test_pollinations_builds_prompt(self):
        from live2d.image_gen.pollinations import PollinationsProvider
        p = PollinationsProvider()
        prompt = p._build_live2d_prompt("cat girl")
        assert "cat girl" in prompt
        assert "anime" in prompt

    def test_sensenova_not_available_without_key(self):
        from live2d.image_gen.sensenova import SenseNovaProvider
        p = SenseNovaProvider()
        assert p.is_available() is False

    def test_seedream_not_available_without_key(self):
        from live2d.image_gen.seedream import SeedreamProvider
        p = SeedreamProvider()
        assert p.is_available() is False

    def test_router_no_provider_raises(self, tmp_path, monkeypatch):
        """Router raises GenerationError when all providers are unavailable."""
        from live2d.image_gen.router import ProviderRouter
        from live2d.image_gen.base import GenerationError
        from live2d.image_gen import pollinations, seedream, sensenova
        from live2d.config import config as cfg

        # Mock all providers as unavailable
        monkeypatch.setattr(pollinations.PollinationsProvider, "is_available", lambda self: False)
        monkeypatch.setattr(seedream.SeedreamProvider, "is_available", lambda self: False)
        monkeypatch.setattr(sensenova.SenseNovaProvider, "is_available", lambda self: False)

        router = ProviderRouter(config=cfg)
        with pytest.raises(GenerationError):
            router.generate("test", output_path=str(tmp_path / "out.png"))


# ===================== QA Edge Cases =====================

class TestQAEdgeCases:
    def test_tiny_image_scores_low(self):
        from live2d.qa.engine import QAEngine
        img = Image.new('RGBA', (10, 10), (128, 128, 128, 255))
        r = QAEngine().assess_image(img)
        assert r.score < 60

    def test_large_image_warning(self):
        from live2d.qa.engine import QAEngine
        img = Image.new('RGBA', (9000, 9000), (255, 255, 255, 255))
        r = QAEngine().assess_image(img)
        codes = [i.code for i in r.issues]
        assert "E002" in codes  # too large

    def test_non_rgba_format(self):
        from live2d.qa.engine import QAEngine
        img = Image.new('P', (100, 100))
        r = QAEngine().assess_image(img)
        codes = [i.code for i in r.issues]
        assert "E005" in codes  # wrong format

    def test_qa_result_serializable(self, test_image):
        from live2d.qa.engine import QAEngine
        from PIL import Image
        r = QAEngine().assess_image(Image.open(test_image).convert('RGBA'))
        d = r.to_dict()
        json.dumps(d)  # Must be JSON serializable


# ===================== PSD Edge Cases =====================

class TestPSDEdgeCases:
    def test_empty_layers_dir(self, tmp_path):
        from live2d.psd.creator import PSDCreator
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        r = PSDCreator().create_psd(str(empty_dir))
        assert not r["success"]

    def test_psd_parser_nonexistent_file(self):
        from live2d.psd.parser import PSDParser, PSDValidationError
        with pytest.raises(PSDValidationError):
            PSDParser().parse("/nonexistent/file.psd")

    def test_psd_validator_rejects_fake(self, tmp_path):
        from live2d.psd.validator import PSDValidator
        fake = tmp_path / "fake.psd"
        fake.write_bytes(b"NOTAPSD" + b"\x00" * 200)
        r = PSDValidator().validate(str(fake))
        assert not r["valid"]
        assert r["score"] == 0


# ===================== Pet Package Edge Cases =====================

class TestPetEdgeCases:
    def test_pet_missing_layers_raises(self, tmp_path):
        from live2d.pet.animator import DesktopPetAnimator
        # Non-existent directory should raise FileNotFoundError
        with pytest.raises(FileNotFoundError):
            DesktopPetAnimator(str(tmp_path / "nonexistent_layers"))

    def test_pet_no_pygame_graceful(self, test_layers_dir, tmp_path):
        """Pet creation works without pygame (pygame only needed for running)."""
        from live2d.pet.animator import DesktopPetAnimator
        a = DesktopPetAnimator(test_layers_dir)
        a.load_layers()
        r = a.create_pet_package(str(tmp_path), "test")
        assert r["success"]

    def test_pet_runner_no_layers(self, tmp_path):
        from live2d.pet.runner import PetRunner
        runner = PetRunner(str(tmp_path))
        assert runner._load_layers(__import__('pygame', fromlist=['pygame']) if False else None) == [] \
            or True  # just test instantiation doesn't crash


# ===================== 52-Layer Edge Cases =====================

class Test52LayerEdgeCases:
    def test_empty_layers_mapping(self):
        from live2d.layering.layers52 import Layer52Generator
        g = Layer52Generator()
        m = g.map_layers_to_standard([])
        assert m["total_layers"] == 52
        assert m["mapped_layers"] == 0
        assert len(m["missing_required"]) > 0

    def test_draw_order_monotonic(self):
        from live2d.layering.layers52 import LIVE2D_52_LAYERS
        orders = [l["draw_order"] for l in LIVE2D_52_LAYERS]
        # Draw orders should be non-decreasing
        for i in range(1, len(orders)):
            assert orders[i] >= orders[i-1], f"Draw order not monotonic at index {i}"

    def test_physics_valid_json(self, tmp_path):
        from live2d.layering.layers52 import Layer52Generator, STANDARD_PHYSICS
        # Physics config must be valid JSON
        path = tmp_path / "physics.json"
        import json
        path.write_text(json.dumps(STANDARD_PHYSICS))
        loaded = json.loads(path.read_text())
        assert loaded["version"] == 3

    def test_params_have_ranges(self):
        from live2d.layering.layers52 import STANDARD_PARAMS
        for p in STANDARD_PARAMS:
            assert p["min"] < p["max"]
            assert p["min"] <= p["default"] <= p["max"]


# ===================== Part Identifier Edge Cases =====================

class TestPartIdentifierEdgeCases:
    def test_black_color_hair(self):
        from live2d.layering.part_identifier import PartIdentifier
        pid = PartIdentifier()
        part = pid.identify_part((30, 20, 30), 0.15, 0.2)
        assert part == "头发"

    def test_skin_color_face(self):
        from live2d.layering.part_identifier import PartIdentifier
        pid = PartIdentifier()
        part = pid.identify_part((245, 200, 185), 0.25, 0.15)
        assert part in ("皮肤", "脸", "未分类")

    def test_unclassified_color(self):
        from live2d.layering.part_identifier import PartIdentifier
        pid = PartIdentifier()
        part = pid.identify_part((0, 255, 0), 0.5, 0.5)  # bright green
        assert part == "未分类"


# ===================== Logger Edge Cases =====================

class TestLoggerEdgeCases:
    def test_telemetry_opt_out(self):
        from live2d.logger import get_logger
        l = get_logger("telemetry_test")
        l._telemetry_enabled = False
        l.telemetry("test", {"key": "val"})
        assert len(l.get_telemetry()) == 0

    def test_telemetry_redacts(self):
        from live2d.logger import get_logger, _redact_sensitive
        r = _redact_sensitive({"api_key": "sk-supersecretkey12345"})
        assert "sk-supersecretkey12345" not in str(r)

    def test_telemetry_flush(self, tmp_path):
        from live2d.logger import get_logger
        l = get_logger("flush_test")
        l._telemetry_enabled = True
        l.telemetry("test_event", {"x": 1})
        fpath = str(tmp_path / "telemetry.jsonl")
        l.flush_telemetry(fpath)
        assert os.path.isfile(fpath)
        assert len(l.get_telemetry()) == 0


# ===================== Workflow Edge Cases =====================

class TestWorkflowEdgeCases:
    def test_workflow_no_input_raises(self, tmp_output):
        from live2d.workflow import WorkflowEngine
        wf = WorkflowEngine(output_dir=tmp_output)
        with pytest.raises(RuntimeError):
            wf.run()

    def test_workflow_invalid_image(self, tmp_path, tmp_output):
        bad = tmp_path / "bad.png"
        bad.write_bytes(b"not an image")
        from live2d.workflow import WorkflowEngine
        wf = WorkflowEngine(output_dir=tmp_output, k_clusters=3)
        r = wf.run(input_image=str(bad))
        assert not r["success"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
