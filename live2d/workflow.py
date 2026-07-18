#!/usr/bin/env python3
"""
Live2D Master Agent - Unified Workflow Engine (v9.0)

Full pipeline: Text-to-Image → QA → Optimize → Layer → PSD → 52-layer mapping → Pet

P0-3 FIX: Uses KMeansLayerer (v6) as default layerer.
P1-2 FIX: Cleans up temporary files on failure.
P1-4 FIX: Uses configurable timeout from config.
DEF-003: Seedream/ARK provider integrated.
DEF-004: 52-layer standard mapping with parameter/physics config.
DEF-007: Unified logging throughout.
"""

import os
import sys
import time
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, Callable

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

from live2d.version import __version__, FULL_VERSION_STRING
from live2d.config import config
from live2d.logger import get_logger
from live2d.image_gen.router import ProviderRouter, get_router
from live2d.layering.kmeans import KMeansLayerer
from live2d.layering.layers52 import Layer52Generator
from live2d.layering.part_identifier import PartIdentifier
from live2d.psd.creator import PSDCreator
from live2d.psd.validator import PSDValidator
from live2d.pet.animator import DesktopPetAnimator
from live2d.qa.engine import QAEngine
from live2d.security import sanitize_prompt, validate_image_path

log = get_logger("workflow")


class WorkflowEngine:
    """JSON-state-machine-based workflow engine.

    Pipeline states:
    1. idle -> generating -> qa_check -> optimizing -> layering -> psd_export -> mapping -> done
    Each state transition is logged and state is serializable.
    """

    STATES = ["idle", "generating", "qa_check", "optimizing", "layering",
              "rigging", "psd_export", "mapping", "pet_deploy", "done", "error"]

    def __init__(
        self,
        output_dir: Optional[str] = None,
        k_clusters: int = 12,
        provider: Optional[str] = None,
        width: int = 1024,
        height: int = 1024,
    ):
        self.output_dir = Path(output_dir or config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.k_clusters = k_clusters
        self.provider_name = provider
        self.width = width
        self.height = height

        # Initialize components
        self.router = get_router(config)
        self.qa_engine = QAEngine()
        self.kmeans_layerer = KMeansLayerer(k_clusters=k_clusters)
        self.layer52_gen = Layer52Generator()
        self.psd_creator = PSDCreator()
        self.part_identifier = PartIdentifier()

        # Workflow state
        self.state = "idle"
        self._temp_files = []  # P1-2: track temp files for cleanup
        self._progress_cb: Optional[Callable[[str, str, float], None]] = None

    def set_progress_callback(self, cb: Callable[[str, str, float], None]):
        """Set progress callback: cb(state, message, percent_0_100)."""
        self._progress_cb = cb

    def _set_state(self, new_state: str, message: str = "", percent: float = 0):
        self.state = new_state
        log.step(self.STATES.index(new_state) + 1, len(self.STATES), message)
        if self._progress_cb:
            self._progress_cb(new_state, message, percent)

    def _track_temp(self, filepath: str):
        """P1-2: Track a temporary file for cleanup."""
        self._temp_files.append(filepath)

    def _cleanup_temp(self):
        """P1-2: Remove temporary files after workflow completion or failure."""
        for fpath in self._temp_files:
            try:
                if os.path.exists(fpath):
                    os.remove(fpath)
                    log.debug(f"Cleaned temp file: {fpath}")
            except OSError as e:
                log.debug(f"Failed to clean temp file {fpath}: {e}")
        self._temp_files.clear()

    def run(
        self,
        prompt: str = "",
        input_image: Optional[str] = None,
        deploy_desktop: bool = False,
        auto_fallback: bool = True,
        generate_52_config: bool = True,
        negative_prompt: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Run the complete Live2D creation pipeline.

        Args:
            prompt: Text description for image generation (if no input_image)
            input_image: Path to existing character image (skip generation)
            deploy_desktop: Whether to create desktop pet package
            auto_fallback: Auto-fallback between providers/libraries
            generate_52_config: Generate 52-layer standard config files
            negative_prompt: Negative prompt for generation
            seed: Random seed for reproducibility

        Returns:
            Result dict with paths and status info
        """
        result = {"version": __version__, "success": False, "steps": {}}
        temp_generated = None

        # Validate inputs before the pipeline try/except
        if not input_image and not prompt:
            raise RuntimeError("Either prompt or input_image must be provided")
        if input_image:
            valid, reason = validate_image_path(input_image)
            if not valid:
                raise RuntimeError(f"Invalid input image: {reason}")

        try:
            log.section(f"Live2D Master Agent v{__version__}")

            # === Step 1: Generate or load image ===
            if input_image:
                self._set_state("generating", f"Loading input image: {input_image}", 5)
                character_path = input_image
                log.info(f"Using provided image: {input_image}")
            else:
                self._set_state("generating", f"Generating character: {prompt[:60]}...", 5)
                safe_prompt = sanitize_prompt(prompt)
                timestamp = int(time.time())
                gen_output = str(self.output_dir / f"character_{timestamp}.png")
                self._track_temp(gen_output)

                gen_result = self.router.generate(
                    prompt=safe_prompt,
                    output_path=gen_output,
                    width=self.width,
                    height=self.height,
                    provider=self.provider_name,
                    negative_prompt=negative_prompt,
                    seed=seed,
                    auto_fallback=auto_fallback,
                )
                character_path = gen_result.image_path
                temp_generated = character_path
                result["steps"]["generate"] = {
                    "provider": gen_result.provider,
                    "model": gen_result.model,
                    "path": character_path,
                    "elapsed": gen_result.elapsed_seconds,
                }
                log.success(f"Image generated: {character_path}")

            # Load the character image
            character_img = Image.open(character_path).convert('RGBA')
            log.info(f"Image size: {character_img.size}")

            # === Step 2: Quality assessment ===
            self._set_state("qa_check", "Running quality assessment", 25)
            qa_result = self.qa_engine.assess_image(character_img)
            result["steps"]["qa"] = {
                "score": qa_result.score,
                "valid": qa_result.valid,
                "issues": [i.to_dict() for i in qa_result.issues],
            }
            log.info(f"Quality score: {qa_result.score}/100 (valid={qa_result.valid})")
            for issue in qa_result.issues:
                if issue.severity.value == "error":
                    log.warning(f"  [ERROR] {issue.message}")
                elif issue.severity.value == "warning":
                    log.warning(f"  [WARN]  {issue.message}")

            # === Step 3: Image optimization ===
            self._set_state("optimizing", "Optimizing image (background removal, enhancement)", 45)
            optimized_img = self._optimize_image(character_img)
            # Save optimized version (output artifact, not temp)
            timestamp = int(time.time())
            optimized_path = str(self.output_dir / f"optimized_{timestamp}.png")
            optimized_img.save(optimized_path)
            result["steps"]["optimize"] = {"path": optimized_path}
            log.info("Image optimized: background removed, contrast enhanced")

            # === Step 4: Layer separation ===
            self._set_state("layering", f"K-means layering (k={self.k_clusters})", 60)
            layers_output = str(self.output_dir / f"layers_{timestamp}")
            layer_result = self.kmeans_layerer.layer(optimized_img, output_dir=layers_output)

            # Identify parts
            layers_with_parts = self.part_identifier.identify_layers(
                layer_result["layers"], optimized_img.height, optimized_img.width
            )
            result["steps"]["layering"] = {
                "output_dir": layers_output,
                "layer_count": layer_result["layer_count"],
                "preview": layer_result["preview_path"],
            }
            log.success(f"Layering complete: {layer_result['layer_count']} layers")

            # === Step 4b: Automatic rigging ===
            if generate_52_config:
                self._set_state("rigging", "Automatic rigging", 70)
                from collections import OrderedDict
                from live2d.rigging.pipeline import RiggingPipeline
                layers_for_rig = OrderedDict()
                for info in layer_result["layers"]:
                    path = info["path"]
                    name = info.get("name") or Path(path).stem
                    layers_for_rig[name] = Image.open(path)
                rig_output = str(self.output_dir / f"rigged_{timestamp}")
                rig_result = RiggingPipeline().run(
                    layers_for_rig,
                    output_dir=rig_output,
                    character_name="generated_character",
                )
                result["steps"]["rigging"] = {
                    "output_dir": rig_output,
                    "model3_json": rig_result["model3_json"],
                    "texture": rig_result["texture"],
                }
                log.success(f"Rigging complete: {rig_result['model3_json']}")

            # === Step 5: PSD export ===
            self._set_state("psd_export", "Creating PSD file", 75)
            psd_output = str(Path(layers_output) / "character.psd")
            psd_result = self.psd_creator.create_psd(layers_output, psd_output)
            result["steps"]["psd"] = psd_result
            log.success(f"PSD created: {psd_result.get('psd_path', 'N/A')}")

            # === Step 6: 52-layer mapping (DEF-004) ===
            if generate_52_config:
                self._set_state("mapping", "Generating 52-layer standard config", 85)
                mapping = self.layer52_gen.map_layers_to_standard(layers_with_parts)
                configs = self.layer52_gen.generate_config_files(
                    mapping, layers_output, character_name="generated_character"
                )
                result["steps"]["layer52"] = {
                    "mapping": configs.get("layer_mapping"),
                    "parameters": configs.get("parameters"),
                    "physics": configs.get("physics"),
                    "guide": configs.get("guide"),
                    "mapped_count": mapping["mapped_layers"],
                    "missing_required": len(mapping["missing_required"]),
                }
                log.info(f"52-layer config: {mapping['mapped_layers']}/52 mapped")

            # === Step 7: Desktop pet (optional) ===
            if deploy_desktop:
                self._set_state("pet_deploy", "Creating desktop pet package", 95)
                pet_result = self._create_pet(layers_output)
                result["steps"]["pet"] = pet_result

            self._set_state("done", "Workflow complete!", 100)
            result["success"] = True
            result["character_image"] = character_path
            result["layers_dir"] = layers_output
            result["output_dir"] = str(self.output_dir)

        except Exception as e:
            self._set_state("error", f"Error: {e}", 0)
            log.error(f"Workflow failed: {e}", exc_info=True)
            result["success"] = False
            result["error"] = str(e)
            result["error_state"] = self.state
        finally:
            # P1-2: Clean up temporary files (but keep final outputs)
            self._cleanup_temp()

        log.section("Workflow Summary")
        if result["success"]:
            log.success(f"Pipeline complete! Output: {result.get('layers_dir', '')}")
        else:
            log.error(f"Pipeline failed at state '{result.get('error_state', '?')}': {result.get('error', '')}")

        return result

    def _optimize_image(self, img: Image.Image) -> Image.Image:
        """Optimize image for Live2D layering:
        - Background removal (threshold or rembg)
        - Contrast enhancement
        - Sharpness enhancement
        - Mild color quantization
        """
        result = img.copy()

        # Background removal (simple threshold on corners)
        if result.mode == 'RGBA':
            data = np.array(result)
            r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
            # Sample corner pixels to detect background color
            corners = np.vstack([
                data[:20, :20, :3].reshape(-1, 3),
                data[:20, -20:, :3].reshape(-1, 3),
                data[-20:, :20, :3].reshape(-1, 3),
                data[-20:, -20:, :3].reshape(-1, 3),
            ])
            bg_color = np.median(corners, axis=0)

            # Create alpha mask from color distance to background
            rgb = data[:,:,:3].astype(float)
            dist = np.sqrt(((rgb - bg_color) ** 2).sum(axis=2))
            # Pixels very close to bg color become transparent; smooth ramp at boundary
            alpha_ramp = (255.0 * (dist - 25) / 25.0)
            alpha_ramp = np.clip(alpha_ramp, 0, 255)
            alpha_new = np.where(dist < 25, 0, np.where(dist < 50, alpha_ramp, 255)).astype(np.uint8)
            # Also respect existing alpha
            data[:,:,3] = np.minimum(a, alpha_new)
            result = Image.fromarray(data, 'RGBA')

        # Contrast enhancement
        enhancer = ImageEnhance.Contrast(result)
        result = enhancer.enhance(1.3)

        # Sharpness enhancement
        enhancer = ImageEnhance.Sharpness(result)
        result = enhancer.enhance(1.8)

        # Color quantization (mild - reduce to help K-means)
        result = result.convert('P', palette=Image.Palette.ADAPTIVE, colors=64).convert('RGBA')

        return result

    def _create_pet(self, layers_dir: str) -> Dict:
        """Create desktop pet package."""
        try:
            animator = DesktopPetAnimator(layers_dir)
            animator.load_layers()
            pet_output = str(Path(layers_dir).parent / "pet_packages")
            return animator.create_pet_package(pet_output)
        except Exception as e:
            log.warning(f"Pet creation failed (non-fatal): {e}")
            return {"success": False, "error": str(e)}


# Convenience function
def run_workflow(
    prompt: str = "",
    input_image: Optional[str] = None,
    output_dir: Optional[str] = None,
    deploy_desktop: bool = False,
    k_clusters: int = 12,
    provider: Optional[str] = None,
    **kwargs
) -> Dict:
    """Run the Live2D workflow with default settings."""
    engine = WorkflowEngine(output_dir=output_dir, k_clusters=k_clusters, provider=provider)
    return engine.run(prompt=prompt, input_image=input_image, deploy_desktop=deploy_desktop, **kwargs)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=f"Live2D Master Agent v{__version__}")
    parser.add_argument("prompt", nargs="?", default="", help="Character description")
    parser.add_argument("--input", "-i", help="Input image path (skip generation)")
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--deploy-desktop", action="store_true", help="Create desktop pet")
    parser.add_argument("--k", type=int, default=12, help="K-means clusters (default: 12)")
    parser.add_argument("--provider", choices=["pollinations", "sensenova", "seedream", "auto"],
                        default="auto", help="Image provider")
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--version", "-V", action="version", version=FULL_VERSION_STRING)
    args = parser.parse_args()

    if not args.prompt and not args.input:
        parser.print_help()
        sys.exit(1)

    wf = WorkflowEngine(output_dir=args.output, k_clusters=args.k,
                        provider=None if args.provider == "auto" else args.provider,
                        width=args.width, height=args.height)
    result = wf.run(
        prompt=args.prompt,
        input_image=args.input,
        deploy_desktop=args.deploy_desktop,
    )
    sys.exit(0 if result["success"] else 1)
