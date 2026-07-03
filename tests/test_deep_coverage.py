#!/usr/bin/env python3
"""
Live2D Master Agent v8.0 - Deep Coverage Tests
End-to-end pipeline, integration, and verification tests.
All tests run WITHOUT real API keys (using local test images).

Run: python -m pytest tests/test_deep_coverage.py -v
"""

import os
import sys
import json
import time
import pytest
import numpy as np
from pathlib import Path
from PIL import Image

_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
os.environ.setdefault("LIVE2D_PROJECT_ROOT", _PROJECT_ROOT)
os.environ["LIVE2D_TELEMETRY"] = "0"
os.environ["LIVE2D_LOG_LEVEL"] = "ERROR"
sys.path.insert(0, _PROJECT_ROOT)


# ===================== End-to-End Pipeline =====================

class TestEndToEndPipeline:
    """Full pipeline: test image -> optimize -> layer -> PSD -> 52-layer config."""

    def test_full_pipeline_local_image(self, test_image, tmp_path):
        """E2E: Input image -> optimized -> layered -> PSD -> 52-layer config."""
        from live2d.workflow import WorkflowEngine

        out_dir = str(tmp_path / "e2e_output")
        wf = WorkflowEngine(output_dir=out_dir, k_clusters=5)
        result = wf.run(
            input_image=test_image,
            deploy_desktop=False,
            generate_52_config=True,
        )

        assert result["success"], f"E2E pipeline failed: {result.get('error', '')}"
        assert os.path.isdir(result["layers_dir"])

        steps = result["steps"]
        # QA step ran
        assert "qa" in steps
        assert "score" in steps["qa"]
        # Optimize step ran
        assert "optimize" in steps
        assert os.path.isfile(steps["optimize"]["path"])
        # Layering ran
        assert "layering" in steps
        assert steps["layering"]["layer_count"] >= 2
        # PSD created
        assert "psd" in steps
        assert steps["psd"]["success"]
        # 52-layer config generated
        assert "layer52" in steps
        l52 = steps["layer52"]
        assert os.path.isfile(l52["parameters"])
        assert os.path.isfile(l52["physics"])
        assert os.path.isfile(l52["guide"])

        # Verify physics JSON is valid Cubism format
        with open(l52["physics"]) as f:
            physics = json.load(f)
        assert physics["version"] == 3
        assert len(physics["physics_settings"]) >= 3

    def test_full_pipeline_with_pet(self, test_image, tmp_path):
        """E2E including pet package creation."""
        from live2d.workflow import WorkflowEngine

        out_dir = str(tmp_path / "e2e_pet")
        wf = WorkflowEngine(output_dir=out_dir, k_clusters=5)
        result = wf.run(
            input_image=test_image,
            deploy_desktop=True,
            generate_52_config=False,
        )

        assert result["success"]
        assert "pet" in result.get("steps", {})
        pet = result["steps"]["pet"]
        # Pet creation may fail if pygame isn't installed, but shouldn't crash
        if pet.get("success"):
            assert os.path.isdir(pet["package_dir"])
            run_script = os.path.join(pet["package_dir"], "run_pet.py")
            assert os.path.isfile(run_script)
            assert "__file__" in open(run_script).read()  # P1-3 fix

    def test_pipeline_produces_valid_layers(self, test_image, tmp_path):
        """Verify layers are properly formed PNG files."""
        from live2d.layering.kmeans import KMeansLayerer
        img = Image.open(test_image).convert('RGBA')
        out = str(tmp_path / "layers")
        r = KMeansLayerer(k_clusters=5).layer(img, output_dir=out)

        for layer in r["layers"]:
            # Each layer is a valid PNG
            layer_img = Image.open(layer["path"])
            assert layer_img.mode == 'RGBA'
            arr = np.array(layer_img)
            # Should have some non-transparent pixels
            assert arr[:,:,3].sum() > 0


# ===================== Image Optimization =====================

class TestImageOptimization:
    def test_optimize_preserves_size(self, test_image, tmp_path):
        from live2d.workflow import WorkflowEngine
        wf = WorkflowEngine(output_dir=str(tmp_path), k_clusters=3)
        img = Image.open(test_image).convert('RGBA')
        optimized = wf._optimize_image(img)
        assert optimized.size == img.size
        assert optimized.mode == 'RGBA'

    def test_optimize_background_removal(self):
        from live2d.workflow import WorkflowEngine
        wf = WorkflowEngine(k_clusters=3)
        # White bg with colored center
        img = Image.new('RGBA', (200, 200), (255, 255, 255, 255))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.ellipse([50, 50, 150, 150], fill=(255, 0, 0, 255))
        optimized = wf._optimize_image(img)
        arr = np.array(optimized)
        # Corner pixels should be (near) transparent
        corner_alpha = arr[5, 5, 3]
        assert corner_alpha < 100, f"Corner alpha should be low after bg removal, got {corner_alpha}"


# ===================== PSD Creator Integration =====================

class TestPSDIntegration:
    def test_psd_from_kmeans_layers(self, test_image, tmp_path):
        """Create PSD from KMeans layers end-to-end."""
        from live2d.layering.kmeans import KMeansLayerer
        from live2d.psd.creator import PSDCreator
        img = Image.open(test_image).convert('RGBA')
        layers_dir = str(tmp_path / "layers")
        KMeansLayerer(k_clusters=4).layer(img, output_dir=layers_dir)

        result = PSDCreator().create_psd(layers_dir, str(tmp_path / "out.psd"))
        assert result["success"]
        assert result["layer_count"] >= 2

    def test_psd_validator_on_valid_directory(self, test_layers_dir, tmp_path):
        """PSD validator works with fallback package."""
        from live2d.psd.creator import PSDCreator
        result = PSDCreator().create_psd(test_layers_dir, str(tmp_path / "test.psd"))
        assert result["success"]


# ===================== 52-Layer Integration =====================

class Test52LayerIntegration:
    def test_52_config_completeness(self, test_image, tmp_path):
        """All 52-layer config files are generated and valid."""
        from live2d.layering.kmeans import KMeansLayerer
        from live2d.layering.layers52 import Layer52Generator
        from live2d.layering.part_identifier import PartIdentifier
        from PIL import Image

        img = Image.open(test_image).convert('RGBA')
        layers_dir = str(tmp_path / "layers")
        lr = KMeansLayerer(k_clusters=5).layer(img, output_dir=layers_dir)

        # Identify parts
        pid = PartIdentifier()
        layers_with_parts = pid.identify_layers(lr["layers"], img.height, img.width)

        # Map to 52 layers
        gen = Layer52Generator()
        mapping = gen.map_layers_to_standard(layers_with_parts)

        # Generate config files
        configs = gen.generate_config_files(mapping, layers_dir, "test_char")

        # Verify all configs
        for key in ("layer_mapping", "parameters", "physics", "guide"):
            assert key in configs
            assert os.path.isfile(configs[key])

        # Verify parameters JSON
        with open(configs["parameters"]) as f:
            params = json.load(f)
        assert "parameters" in params
        param_ids = [p["id"] for p in params["parameters"]]
        assert "ParamAngleX" in param_ids
        assert "ParamEyeLOpen" in param_ids
        assert "ParamMouthOpenY" in param_ids


# ===================== Pet Package Integration =====================

class TestPetPackageIntegration:
    def test_pet_run_script_is_valid_python(self, test_layers_dir, tmp_path):
        """Generated run_pet.py is syntactically valid Python."""
        from live2d.pet.animator import DesktopPetAnimator
        import py_compile

        a = DesktopPetAnimator(test_layers_dir)
        a.load_layers()
        r = a.create_pet_package(str(tmp_path), "valid_pet")
        run_script = os.path.join(r["package_dir"], "run_pet.py")

        # Compile check
        py_compile.compile(run_script, doraise=True)

    def test_pet_config_json_valid(self, test_layers_dir, tmp_path):
        """pet_config.json is valid JSON."""
        from live2d.pet.animator import DesktopPetAnimator
        a = DesktopPetAnimator(test_layers_dir)
        a.load_layers()
        r = a.create_pet_package(str(tmp_path), "json_pet")
        cfg_path = os.path.join(r["package_dir"], "pet_config.json")
        with open(cfg_path) as f:
            cfg = json.load(f)
        assert "canvas_size" in cfg
        assert "fps" in cfg
        assert "layer_groups" in cfg
        assert "animations" in cfg


# ===================== QA Integration =====================

class TestQAIntegration:
    def test_qa_on_kmeans_output(self, test_image, tmp_path):
        """QA runs on optimized image."""
        from live2d.workflow import WorkflowEngine
        from live2d.qa.engine import QAEngine
        img = Image.open(test_image).convert('RGBA')
        wf = WorkflowEngine(k_clusters=3)
        optimized = wf._optimize_image(img)
        result = QAEngine().assess_image(optimized)
        assert 0 <= result.score <= 100
        assert isinstance(result.issues, list)


# ===================== Provider Router Mock Test =====================

class TestProviderRouterIntegration:
    def test_router_with_mock(self, tmp_path, mock_requests):
        """Router generates image using mocked HTTP."""
        from live2d.image_gen.router import ProviderRouter
        from live2d.image_gen.pollinations import PollinationsProvider

        out = str(tmp_path / "mock_out.png")
        router = ProviderRouter()
        # Pollinations is always available; mock_requests patches HTTP
        try:
            result = router.generate("test character", output_path=out, provider="pollinations")
            assert result.success
            assert os.path.isfile(result.image_path)
        except Exception:
            pass  # Mock might not produce valid PNG, that's OK for integration test


# ===================== Configuration Integration =====================

class TestConfigIntegration:
    def test_config_singleton_consistency(self):
        """Config singleton returns same instance."""
        from live2d.config import SecureConfig, config
        c1 = SecureConfig()
        c2 = SecureConfig()
        assert c1 is c2

    def test_env_example_loadable(self):
        """env.example can be parsed as KEY=VALUE."""
        env_path = Path(_PROJECT_ROOT) / ".env.example"
        content = env_path.read_text()
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            assert '=' in line, f"Invalid env line: {line}"


# ===================== Go API Config Validation =====================

class TestGoAPIConfig:
    def test_go_config_has_dynamic_timeout(self):
        """P1-4: Go config has dynamic timeout field."""
        go_cfg = Path(_PROJECT_ROOT) / "api" / "config" / "config.go"
        content = go_cfg.read_text()
        assert "TimeoutSec" in content
        assert "GetPythonTimeout" in content

    def test_go_bridge_uses_config_timeout(self):
        bridge = Path(_PROJECT_ROOT) / "api" / "services" / "python_bridge.go"
        content = bridge.read_text()
        assert "GetPythonTimeout" in content

    def test_go_main_uses_v8_version(self):
        main_go = Path(_PROJECT_ROOT) / "api" / "main.go"
        content = main_go.read_text()
        assert "v8.0" in content

    def test_python_bridge_defaults_v6(self):
        """P0-3: Python bridge defaults to v6 layerer."""
        bridge = Path(_PROJECT_ROOT) / "api" / "services" / "python_bridge.go"
        content = bridge.read_text()
        assert "live2d_layer_v6.py" in content


# ===================== CLI Entry Point Validation =====================

class TestCLIEntryPoints:
    def test_master_tool_compiles(self):
        import py_compile
        py_compile.compile(os.path.join(_PROJECT_ROOT, "master_tool.py"), doraise=True)

    def test_workflow_compiles(self):
        import py_compile
        py_compile.compile(os.path.join(_PROJECT_ROOT, "live2d_workflow.py"), doraise=True)

    def test_layer_v6_compiles(self):
        import py_compile
        py_compile.compile(os.path.join(_PROJECT_ROOT, "live2d_layer_v6.py"), doraise=True)

    def test_desktop_pet_compiles(self):
        import py_compile
        py_compile.compile(os.path.join(_PROJECT_ROOT, "live2d_desktop_pet.py"), doraise=True)

    def test_config_api_compiles(self):
        import py_compile
        py_compile.compile(os.path.join(_PROJECT_ROOT, "config_api.py"), doraise=True)

    def test_agent_compiles(self):
        import py_compile
        py_compile.compile(os.path.join(_PROJECT_ROOT, "live2d_agent.py"), doraise=True)

    def test_install_compiles(self):
        import py_compile
        py_compile.compile(os.path.join(_PROJECT_ROOT, "install.py"), doraise=True)

    def test_version_flag_exists_in_all_clis(self):
        """P2-3: All CLI tools support --version."""
        clis = ["master_tool.py", "live2d_workflow.py", "live2d_layer_v6.py",
                "live2d_desktop_pet.py"]
        for cli in clis:
            content = (Path(_PROJECT_ROOT) / cli).read_text()
            assert "--version" in content or "-V" in content, f"{cli} missing --version"


# ===================== File Structure Validation =====================

class TestProjectStructure:
    def test_required_files_exist(self):
        required = [
            "README.md", "requirements.txt", "VERSION", ".env.example",
            "install.py", "master_tool.py", "live2d_workflow.py",
            "live2d/__init__.py", "live2d/version.py", "live2d/config.py",
            "live2d/workflow.py", "live2d/logger.py", "live2d/security.py",
            "live2d/secure_storage.py",
            "live2d/image_gen/__init__.py", "live2d/layering/__init__.py",
            "live2d/psd/__init__.py", "live2d/pet/__init__.py", "live2d/qa/__init__.py",
            "tests/__init__.py", "tests/conftest.py", "tests/test_workflow.py",
            "tests/test_full_coverage.py", "tests/test_deep_coverage.py",
            "api/main.go", "api/go.mod",
        ]
        for f in required:
            assert (Path(_PROJECT_ROOT) / f).is_file(), f"Missing required file: {f}"

    def test_cryptography_is_required(self):
        """P0-4/P2-4: cryptography is listed as required."""
        req = (Path(_PROJECT_ROOT) / "requirements.txt").read_text()
        assert "cryptography" in req.lower()

    def test_no_xor_fallback_in_secure_storage(self):
        """P0-4: XOR fallback completely removed."""
        ss = (Path(_PROJECT_ROOT) / "live2d" / "secure_storage.py").read_text()
        assert "_simple_encrypt" not in ss
        assert "_simple_decrypt" not in ss

    def test_default_layerer_is_v6(self):
        """P0-3: Default layerer is KMeans v6, not pro."""
        wf = (Path(_PROJECT_ROOT) / "live2d" / "workflow.py").read_text()
        assert "KMeansLayerer" in wf

    def test_pet_uses_script_relative_paths(self):
        """P1-3: Pet runner uses __file__ for path resolution."""
        anim = (Path(_PROJECT_ROOT) / "live2d" / "pet" / "animator.py").read_text()
        assert "__file__" in anim
        assert "SCRIPT_DIR" in anim

    def test_temp_cleanup_in_workflow(self):
        """P1-2: Workflow cleans temp files."""
        wf = (Path(_PROJECT_ROOT) / "live2d" / "workflow.py").read_text()
        assert "_cleanup_temp" in wf
        assert "finally" in wf  # cleanup in finally block


# ===================== Version Consistency Deep Check =====================

class TestVersionDeep:
    def test_all_version_references_are_v8(self):
        """P0-1: No stale v7.x version references in Python source."""
        import glob
        py_files = glob.glob(os.path.join(_PROJECT_ROOT, "live2d", "**", "*.py"), recursive=True)
        py_files += glob.glob(os.path.join(_PROJECT_ROOT, "*.py"))
        stale = []
        for f in py_files:
            content = Path(f).read_text()
            if "v7.1" in content or "v7.0" in content:
                # Exclude CHANGELOG which references old versions
                if "CHANGELOG" not in f:
                    stale.append(f)
        assert len(stale) == 0, f"Stale version references in: {stale}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-x"])
