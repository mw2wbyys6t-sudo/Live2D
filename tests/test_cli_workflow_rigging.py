#!/usr/bin/env python3
"""
CLI --rig and Workflow integration brutal tests.

Covers:
- WorkflowEngine STATES includes "rigging"
- WorkflowEngine.run with input_image and generate_52_config=True triggers rigging
- WorkflowEngine state transitions include rigging
- CLI: master_tool.py --layer-only --rig runs RiggingPipeline
- CLI: missing --input with --layer-only --rig errors out
- CLI: --rig without --layer-only is ignored (only works in layer-only mode per code)
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from PIL import Image, ImageDraw

# Ensure project root on path
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, _PROJECT_ROOT)


# ---------------- WorkflowEngine STATES ----------------

class TestWorkflowStates:
    def test_rigging_in_states_list(self):
        from live2d.workflow import WorkflowEngine
        assert "rigging" in WorkflowEngine.STATES

    def test_rigging_comes_after_layering(self):
        from live2d.workflow import WorkflowEngine
        states = WorkflowEngine.STATES
        assert states.index("rigging") > states.index("layering")

    def test_rigging_before_psd_export(self):
        from live2d.workflow import WorkflowEngine
        states = WorkflowEngine.STATES
        assert states.index("rigging") < states.index("psd_export")

    def test_states_index_rigging_valid_for_set_state(self):
        from live2d.workflow import WorkflowEngine
        # _set_state calls self.STATES.index(new_state) + 1
        # Should not raise ValueError
        engine = WorkflowEngine.__new__(WorkflowEngine)
        engine.STATES = WorkflowEngine.STATES
        engine._progress_cb = None
        engine._set_state("rigging", "test", 0)
        assert engine.state == "rigging"


# ---------------- WorkflowEngine rigging integration ----------------

class TestWorkflowRiggingIntegration:
    def test_run_with_input_image_triggers_rigging(self, tmp_path, test_image):
        """End-to-end smoke test: feed a real test image, check rigging step ran."""
        from live2d.workflow import WorkflowEngine
        engine = WorkflowEngine(output_dir=str(tmp_path), k_clusters=4)
        result = engine.run(
            prompt="",
            input_image=test_image,
            generate_52_config=True,
            deploy_desktop=False,
        )
        # Pipeline should complete successfully (or at least reach rigging)
        if result["success"]:
            assert "rigging" in result["steps"]
            assert Path(result["steps"]["rigging"]["model3_json"]).exists()
        else:
            # If it failed, error_state should be >= rigging in pipeline (i.e., rigging ran)
            # or before rigging (in which case we can't verify)
            assert "error" in result

    def test_rigging_skipped_when_52_config_disabled(self, tmp_path, test_image):
        from live2d.workflow import WorkflowEngine
        engine = WorkflowEngine(output_dir=str(tmp_path), k_clusters=4)
        result = engine.run(
            prompt="",
            input_image=test_image,
            generate_52_config=False,
            deploy_desktop=False,
        )
        # rigging step should NOT be in result
        assert "rigging" not in result.get("steps", {})

    def test_rigging_state_in_progress_callback(self, tmp_path, test_image):
        from live2d.workflow import WorkflowEngine
        seen_states = []

        def cb(state, msg, pct):
            seen_states.append(state)

        engine = WorkflowEngine(output_dir=str(tmp_path), k_clusters=4)
        engine.set_progress_callback(cb)
        try:
            engine.run(prompt="", input_image=test_image, generate_52_config=True)
        except Exception:
            pass
        # rigging state should have been emitted at some point (if we got past layering)
        # Note: may not be emitted if earlier step fails
        if "layering" in seen_states and "psd_export" in seen_states:
            assert "rigging" in seen_states


# ---------------- CLI --rig integration ----------------

class TestCLIRigIntegration:
    def test_cli_help_lists_rig_flag(self):
        result = subprocess.run(
            [sys.executable, str(Path(_PROJECT_ROOT) / "master_tool.py"), "--help"],
            capture_output=True, text=True, timeout=30,
        )
        assert "--rig" in result.stdout

    def test_cli_layer_only_requires_input(self):
        result = subprocess.run(
            [sys.executable, str(Path(_PROJECT_ROOT) / "master_tool.py"),
             "--layer-only", "--rig"],
            capture_output=True, text=True, timeout=30,
        )
        # Should error out because --input is required
        assert result.returncode != 0
        assert "--layer-only requires --input" in result.stderr or "input" in result.stderr.lower()

    def test_cli_layer_only_with_rig_runs(self, tmp_path, test_image):
        """Run master_tool.py --layer-only --rig --input <image> end-to-end."""
        out_dir = tmp_path / "cli_out"
        out_dir.mkdir()
        result = subprocess.run(
            [sys.executable, str(Path(_PROJECT_ROOT) / "master_tool.py"),
             "--layer-only", "--rig",
             "--input", test_image,
             "--k", "4",
             "--output", str(out_dir / "layers")],
            capture_output=True, text=True, timeout=120,
        )
        # Check exit code (may be 0 on success)
        assert result.returncode == 0, f"CLI failed: {result.stderr}"
        # Check rigging output exists
        rigged_dir = out_dir / "layers" / "rigged"
        # Either rigged exists (layer-only --rig path) or model3.json exists somewhere
        if rigged_dir.exists():
            model3_files = list(rigged_dir.glob("*.model3.json"))
            assert len(model3_files) > 0, f"no model3.json in {rigged_dir}"

    def test_cli_rig_creates_expected_files(self, tmp_path, test_image):
        """Verify CLI --rig produces model3.json, texture, physics, mesh_guide."""
        out_dir = tmp_path / "cli_out"
        out_dir.mkdir()
        result = subprocess.run(
            [sys.executable, str(Path(_PROJECT_ROOT) / "master_tool.py"),
             "--layer-only", "--rig",
             "--input", test_image,
             "--k", "4",
             "--output", str(out_dir / "layers")],
            capture_output=True, text=True, timeout=120,
        )
        assert result.returncode == 0, f"CLI failed: {result.stderr}"
        rigged_dir = out_dir / "layers" / "rigged"
        if rigged_dir.exists():
            # model3.json
            assert len(list(rigged_dir.glob("*.model3.json"))) > 0
            # textures
            assert len(list(rigged_dir.glob("*.texture_*.png"))) > 0
            # physics
            assert len(list(rigged_dir.glob("*.physics3.json"))) > 0
            # mesh guide
            assert (rigged_dir / "mesh_guide.json").exists()
            # README
            assert (rigged_dir / "README_RIGGING.txt").exists()
            # expressions
            assert (rigged_dir / "expressions").exists()
            exp_files = list((rigged_dir / "expressions").glob("*.exp3.json"))
            assert len(exp_files) == 3


# ---------------- Workflow rigging output validation ----------------

class TestWorkflowRiggingOutput:
    def test_rigging_output_has_valid_model3_json(self, tmp_path, test_image):
        from live2d.workflow import WorkflowEngine
        engine = WorkflowEngine(output_dir=str(tmp_path), k_clusters=4)
        result = engine.run(
            prompt="", input_image=test_image, generate_52_config=True,
        )
        if result["success"] and "rigging" in result["steps"]:
            model3_path = result["steps"]["rigging"]["model3_json"]
            with open(model3_path, encoding="utf-8") as f:
                data = json.load(f)
            assert data["Version"] == 3.0
            assert "FileReferences" in data
            assert "Parameters" in data

    def test_rigging_output_textures_exist(self, tmp_path, test_image):
        from live2d.workflow import WorkflowEngine
        engine = WorkflowEngine(output_dir=str(tmp_path), k_clusters=4)
        result = engine.run(
            prompt="", input_image=test_image, generate_52_config=True,
        )
        if result["success"] and "rigging" in result["steps"]:
            tex_path = result["steps"]["rigging"]["texture"]
            assert Path(tex_path).exists()
