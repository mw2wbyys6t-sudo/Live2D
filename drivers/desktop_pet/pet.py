#!/usr/bin/env python3
"""
Live2D Desktop Pet - High-level runtime controller.

Integrates:
- DesktopPetWindow for transparent, frameless display
- DesktopPetAnimator for package generation
- FaceTracker + AudioCapture for real-time tracking and lip-sync
- Live2DRenderer for parameter-driven rendering

Supports two modes:
1. Idle/animatronic mode: procedural breathing, blinking, swing
2. Tracking mode: face-driven expression, gaze, head orientation,
   and voice lip-sync from microphone audio.
"""

import math
import time
import random
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any

from core.logger import get_logger
from drivers.desktop_pet.window import DesktopPetWindow
from drivers.desktop_pet.animator import DesktopPetAnimator

log = get_logger("pet")

try:
    import pygame
    _PYGAME_AVAILABLE = True
except ImportError:
    _PYGAME_AVAILABLE = False
    pygame = None  # type: ignore

try:
    from PIL import Image
    _PIL_AVAILABLE = True
except ImportError:
    _PIL_AVAILABLE = False
    Image = None  # type: ignore


class DesktopPet:
    """High-level desktop pet with real-time tracking and animation.

    Parameters
    ----------
    layers_dir : str or None
        Path to directory of layer PNGs (for layer-compositing mode).
    model_dir : str or None
        Path to a Live2D model3.json directory (for Live2DRenderer mode).
    width, height : int
        Window size.
    x, y : int
        Initial window position.
    """

    # Animation parameters
    IDLE_CONFIG = {
        "body_swing_amplitude": 3.0,
        "body_swing_speed": 0.8,
        "breath_amplitude": 1.5,
        "breath_speed": 0.4,
        "blink_interval_min": 3.0,
        "blink_interval_max": 6.0,
        "blink_duration": 0.15,
        "hair_swing_multiplier": 1.8,
    }

    EXPRESSIONS = {
        "normal": {"mouth_scale_y": 1.0, "mouth_scale_x": 1.0,
                   "eye_open": 1.0, "eye_scale_x": 1.0,
                   "eyebrow_angle": 0.0, "blush": 0.0},
        "happy": {"mouth_scale_y": 1.15, "mouth_scale_x": 1.1,
                  "eye_open": 0.7, "eye_scale_x": 0.9,
                  "eyebrow_angle": -0.15, "blush": 0.6},
        "shy": {"mouth_scale_y": 0.85, "mouth_scale_x": 0.9,
                "eye_open": 0.5, "eye_scale_x": 0.8,
                "eyebrow_angle": -0.2, "blush": 0.8},
        "surprised": {"mouth_scale_y": 1.3, "mouth_scale_x": 1.15,
                      "eye_open": 1.2, "eye_scale_x": 1.1,
                      "eyebrow_angle": 0.2, "blush": 0.0},
        "sleepy": {"mouth_scale_y": 0.7, "mouth_scale_x": 1.0,
                   "eye_open": 0.25, "eye_scale_x": 1.0,
                   "eyebrow_angle": 0.1, "blush": 0.0},
        "angry": {"mouth_scale_y": 0.7, "mouth_scale_x": 0.85,
                  "eye_open": 0.9, "eye_scale_x": 1.1,
                  "eyebrow_angle": 0.3, "blush": 0.4},
        "sad": {"mouth_scale_y": 0.9, "mouth_scale_x": 0.85,
                "eye_open": 0.8, "eye_scale_x": 0.95,
                "eyebrow_angle": -0.1, "blush": 0.0},
    }

    def __init__(
        self,
        layers_dir: Optional[str] = None,
        model_dir: Optional[str] = None,
        width: int = 300,
        height: int = 400,
        x: int = 100,
        y: int = 100,
        fps: int = 60,
    ):
        self.layers_dir = Path(layers_dir) if layers_dir else None
        self.model_dir = Path(model_dir) if model_dir else None
        self.width = width
        self.height = height
        self.fps = fps

        # Window
        self.window = DesktopPetWindow(width=width, height=height, x=x, y=y)

        # Layers (loaded as pygame surfaces)
        self._layers: List[Tuple[str, Any]] = []
        self._classified: Dict[str, List[Tuple[str, Any]]] = {}

        # Live2D renderer (optional)
        self._renderer = None
        if model_dir:
            try:
                from drivers.live2d_runtime.renderer import Live2DRenderer
                self._renderer = Live2DRenderer(str(model_dir), width, height)
                model3 = list(Path(model_dir).glob("*.model3.json"))
                if model3:
                    self._renderer.load_model(str(model3[0]))
            except Exception as e:
                log.warning(f"Could not load Live2D renderer: {e}")
                self._renderer = None

        # Tracking components (lazy)
        self._face_tracker = None
        self._audio_capture = None
        self._tracking_enabled = False
        self._lip_sync_enabled = False

        # Animation state
        self._params: Dict[str, float] = {
            "ParamAngleX": 0.0, "ParamAngleY": 0.0, "ParamAngleZ": 0.0,
            "ParamBodyAngleX": 0.0,
            "ParamEyeLOpen": 1.0, "ParamEyeROpen": 1.0,
            "ParamEyeBallX": 0.0, "ParamEyeBallY": 0.0,
            "ParamMouthOpenY": 0.0, "ParamMouthForm": 0.0,
            "ParamBrowLY": 0.0, "ParamBrowRY": 0.0,
            "ParamBreath": 0.5,
            "ParamCheek": 0.0,
        }
        self._prev_params: Dict[str, float] = dict(self._params)
        self._expression = "normal"
        self._expression_target = "normal"
        self._expression_transition_start = 0.0
        self._expression_transition_time = 0.3

        # Idle timers
        self._start_time = 0.0
        self._next_blink = 0.0
        self._blink_until = 0.0
        self._next_expression = 0.0

        # Smoothing for tracking params
        self._smooth_factor = 0.6

        self._running = False

    # ------------------------------------------------------------------
    # Tracking integration
    # ------------------------------------------------------------------

    def enable_tracking(self, camera_id: int = 0) -> bool:
        """Enable real-time face tracking.

        Returns True if tracking was successfully enabled.
        """
        try:
            from drivers.face_tracker.mediapipe_tracker import FaceTracker
            self._face_tracker = FaceTracker(camera_id=camera_id)
            self._face_tracker.start()
            self._tracking_enabled = self._face_tracker.is_running()
            if self._tracking_enabled:
                log.success("Face tracking enabled")
            return self._tracking_enabled
        except Exception as e:
            log.warning(f"Could not enable face tracking: {e}")
            return False

    def enable_lip_sync(self) -> bool:
        """Enable microphone audio capture for voice lip-sync."""
        try:
            from drivers.audio.capture import AudioCapture
            self._audio_capture = AudioCapture()
            self._audio_capture.start()
            self._lip_sync_enabled = self._audio_capture.is_running()
            if self._lip_sync_enabled:
                log.success("Voice lip-sync enabled")
            return self._lip_sync_enabled
        except Exception as e:
            log.warning(f"Could not enable lip-sync: {e}")
            return False

    def disable_tracking(self) -> None:
        """Disable face tracking and lip-sync."""
        if self._face_tracker:
            self._face_tracker.stop()
            self._face_tracker = None
        if self._audio_capture:
            self._audio_capture.stop()
            self._audio_capture = None
        self._tracking_enabled = False
        self._lip_sync_enabled = False

    def update_from_tracking(self, params: Dict[str, float]) -> None:
        """Apply Live2D parameters from external face tracking.

        Parameters
        ----------
        params : dict[str, float]
            Live2D parameter name -> value. These are smoothed against
            the previous frame and override idle animation values.
        """
        self._prev_params = dict(self._params)
        for key, value in params.items():
            if key in self._params:
                # Exponential smoothing toward tracking value
                self._params[key] = (
                    self._params[key] * self._smooth_factor
                    + value * (1.0 - self._smooth_factor)
                )

    # ------------------------------------------------------------------
    # Expression control
    # ------------------------------------------------------------------

    def set_expression(self, expression_name: str) -> None:
        """Set the current facial expression by name."""
        if expression_name in self.EXPRESSIONS:
            self._expression_target = expression_name
            self._expression_transition_start = time.time()
            log.debug(f"Expression -> {expression_name}")
        else:
            log.warning(f"Unknown expression: {expression_name}")

    def _update_expression_transition(self, now: float) -> Dict[str, float]:
        """Interpolate between current and target expression. Returns blend factors."""
        t = (now - self._expression_transition_start) / self._expression_transition_time
        t = max(0.0, min(1.0, t))
        if t >= 1.0:
            self._expression = self._expression_target

        src = self.EXPRESSIONS.get(self._expression, self.EXPRESSIONS["normal"])
        dst = self.EXPRESSIONS.get(self._expression_target, self.EXPRESSIONS["normal"])
        blended = {}
        for key in src:
            blended[key] = src[key] + (dst[key] - src[key]) * t
        return blended

    # ------------------------------------------------------------------
    # Layer loading
    # ------------------------------------------------------------------

    def load_layers(self) -> None:
        """Load layer PNGs from ``self.layers_dir`` as pygame surfaces."""
        if not _PYGAME_AVAILABLE or not self.layers_dir:
            return
        if not self.layers_dir.is_dir():
            log.warning(f"Layers dir not found: {self.layers_dir}")
            return

        self._layers = []
        for f in sorted(self.layers_dir.glob("*.png")):
            if f.name in ("preview.png", "composite_preview.png"):
                continue
            try:
                surf = pygame.image.load(str(f)).convert_alpha()
                name = f.stem
                self._layers.append((name, surf))
                group = self._classify_layer_name(name)
                self._classified.setdefault(group, []).append((name, surf))
            except Exception as e:
                log.debug(f"Could not load layer {f}: {e}")

        if self._layers and not self.model_dir:
            w, h = self._layers[0][1].get_size()
            self.width, self.height = w, h

        log.info(f"Loaded {len(self._layers)} layers for desktop pet")

    @staticmethod
    def _classify_layer_name(name: str) -> str:
        """Classify a layer by name keywords."""
        nl = name.lower()
        keyword_map = {
            "hair_front": ["hair_front", "bangs", "ahoge", "sidehair", "刘海", "前发"],
            "hair_back": ["hair_back", "后发", "后ろ髪"],
            "eyes": ["eye", "iris", "pupil", "highlight", "眼", "目"],
            "mouth": ["mouth", "lip", "teeth", "tongue", "嘴", "口"],
            "eyebrows": ["eyebrow", "brow", "眉"],
            "face": ["face", "skin", "nose", "ear", "blush", "脸", "颊"],
            "body": ["body", "chest", "clothes", "torso", "waist", "身体", "衣服"],
            "arm_l": ["left_arm", "左臂", "left hand", "左手"],
            "arm_r": ["right_arm", "右臂", "right hand", "右手"],
            "leg_l": ["left_leg", "左腿"],
            "leg_r": ["right_leg", "右腿"],
        }
        for group, kws in keyword_map.items():
            for kw in kws:
                if kw in nl:
                    return group
        return "body"

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Run the desktop pet main loop (blocking)."""
        if not _PYGAME_AVAILABLE:
            log.error("pygame is required. Install: pip install pygame")
            return

        self.window = DesktopPetWindow(
            width=self.width, height=self.height,
            x=self.window._x, y=self.window._y,
        )
        self.window.show()
        if not self.window.is_running():
            return

        if self.layers_dir and not self._layers:
            self.load_layers()

        self._start_time = time.time()
        self._next_blink = self._start_time + random.uniform(3.0, 6.0)
        self._next_expression = self._start_time + 8.0
        self._running = True

        # Tracking
        if self._tracking_enabled and self._face_tracker:
            from drivers.face_tracker.blendshape_mapper import BlendShapeMapper
            mapper = BlendShapeMapper(smoothing_factor=0.5)
        else:
            mapper = None

        while self._running and self.window.is_running():
            now = time.time()
            t = now - self._start_time
            self.window._clock.tick(self.fps) if self.window._clock else None

            # Process window events
            ev = self.window.handle_events()
            self._process_event(ev)

            # Update tracking data
            if mapper and self._face_tracker and self._face_tracker.is_running():
                landmarks = self._face_tracker.get_landmarks()
                if landmarks:
                    bs = self._face_tracker.get_blendshapes()
                    head_rot = self._face_tracker.get_head_rotation()
                    lm_data = dict(landmarks)
                    if head_rot:
                        lm_data["head_rotation"] = {
                            "pitch": head_rot["x"],
                            "yaw": head_rot["y"],
                            "roll": head_rot["z"],
                        }
                    live2d_params = mapper.map_to_live2d_params(bs, lm_data)
                    self.update_from_tracking(live2d_params)

            # Lip-sync from audio
            if self._lip_sync_enabled and self._audio_capture:
                mouth = self._audio_capture.get_mouth_open_amount()
                self._params["ParamMouthOpenY"] = mouth

            # Idle animation (when not tracking)
            if not self._tracking_enabled:
                self._apply_idle_animation(t, now)

            # Blink (always active as a safety net)
            self._apply_blink(now)

            # Expression transitions
            expr_blend = self._update_expression_transition(now)

            # Random expression changes in idle mode
            if not self._tracking_enabled and now > self._next_expression:
                self.set_expression(random.choice(
                    ["normal", "happy", "shy", "normal", "normal"]
                ))
                self._next_expression = now + random.uniform(8.0, 15.0)

            # Render
            if self._renderer:
                self._renderer.set_parameters(self._params)
                img = self._renderer.render()
                if _PYGAME_AVAILABLE and img is not None:
                    raw = img.tobytes("raw", "RGBA")
                    surf = pygame.image.fromstring(raw, img.size, "RGBA")
                    self.window.render_frame(surf)
            else:
                self._render_layers(t, expr_blend)

            self.window.update()
            self.window.flip()

        self.window.close()
        self.disable_tracking()
        log.info("Desktop pet stopped")

    def stop(self) -> None:
        """Request the main loop to exit."""
        self._running = False

    # ------------------------------------------------------------------
    # Idle / procedural animation
    # ------------------------------------------------------------------

    def _apply_idle_animation(self, t: float, now: float) -> None:
        """Compute idle procedural animation parameters."""
        cfg = self.IDLE_CONFIG
        swing = math.sin(t * cfg["body_swing_speed"]) * cfg["body_swing_amplitude"]
        breath = math.sin(t * cfg["breath_speed"]) * cfg["breath_amplitude"]

        self._params["ParamAngleZ"] = swing * 0.5
        self._params["ParamBodyAngleX"] = swing * 0.3
        self._params["ParamBreath"] = 0.5 + breath * 0.1
        # Hair swing is applied during rendering

    def _apply_blink(self, now: float) -> None:
        """Natural blink timer."""
        eye_open = 1.0
        if now < self._blink_until:
            eye_open = max(0.0, (self._blink_until - now) / 0.15)
        elif now > self._next_blink:
            self._blink_until = now + 0.15
            self._next_blink = now + random.uniform(3.0, 6.0)

        # Only override if tracking isn't controlling eyes
        if not self._tracking_enabled:
            self._params["ParamEyeLOpen"] = eye_open
            self._params["ParamEyeROpen"] = eye_open

    # ------------------------------------------------------------------
    # Layer-based rendering
    # ------------------------------------------------------------------

    def _render_layers(self, t: float, expr_blend: Dict[str, float]) -> None:
        """Render composite from loaded layers with parameter-driven transforms."""
        if not _PYGAME_AVAILABLE or self.window._screen is None:
            return

        cfg = self.IDLE_CONFIG
        swing = math.sin(t * cfg["body_swing_speed"]) * cfg["body_swing_amplitude"]
        breath = math.sin(t * cfg["breath_speed"]) * cfg["breath_amplitude"]
        hair_off = swing * cfg["hair_swing_multiplier"]

        eye_open = min(self._params.get("ParamEyeLOpen", 1.0),
                       self._params.get("ParamEyeROpen", 1.0))
        eye_open *= expr_blend.get("eye_open", 1.0)
        mouth_open = self._params.get("ParamMouthOpenY", 0.0)

        self.window._screen.fill((0, 0, 0, 0))

        for name, surf in self._layers:
            group = self._classify_layer_name(name)
            nl = name.lower()
            ox, oy = 0.0, breath

            if group in ("hair_front", "hair_back") or any(k in nl for k in ["hair", "bangs"]):
                ox = hair_off
            elif group == "body" or any(k in nl for k in ["body", "clothes"]):
                ox = swing * 0.5

            draw_surf = surf

            # Eye blink / squint
            if eye_open < 0.95 and any(k in nl for k in ["eye", "iris", "pupil"]):
                sw, sh = surf.get_size()
                eye_sx = expr_blend.get("eye_scale_x", 1.0)
                new_w = max(1, int(sw * eye_sx))
                new_h = max(1, int(sh * eye_open))
                draw_surf = pygame.transform.scale(surf, (new_w, new_h))
                ox += (sw - new_w) * 0.5
                oy += (sh - new_h) * 0.5

            # Mouth: open/close from params + expression
            if any(k in nl for k in ["mouth", "lip"]):
                sw, sh = surf.get_size()
                m_sy = expr_blend.get("mouth_scale_y", 1.0)
                m_sx = expr_blend.get("mouth_scale_x", 1.0)
                open_factor = 1.0 + mouth_open * 0.8
                new_w = max(1, int(sw * m_sx))
                new_h = max(1, int(sh * m_sy * open_factor))
                draw_surf = pygame.transform.scale(surf, (new_w, new_h))
                ox += (sw - new_w) * 0.5
                oy += (sh - new_h) * 0.5

            self.window._screen.blit(draw_surf, (ox, oy))

    # ------------------------------------------------------------------
    # Event processing
    # ------------------------------------------------------------------

    def _process_event(self, ev: Dict[str, Any]) -> None:
        """React to window events."""
        etype = ev.get("type")
        if etype == "quit":
            self._running = False
        elif etype == "click":
            self.set_expression("happy")
        elif etype == "right_click":
            # Cycle through expressions
            names = list(self.EXPRESSIONS.keys())
            idx = names.index(self._expression_target)
            self.set_expression(names[(idx + 1) % len(names)])
        elif etype == "key":
            key = ev.get("key")
            if _PYGAME_AVAILABLE and key == pygame.K_SPACE:
                self.set_expression("surprised")

    # ------------------------------------------------------------------
    # Animation package generation (delegates to DesktopPetAnimator)
    # ------------------------------------------------------------------

    @staticmethod
    def create_package(
        layers_dir: str,
        output_dir: str,
        pet_name: str = "live2d_pet",
    ) -> Dict:
        """Generate a standalone pet package. Convenience wrapper."""
        animator = DesktopPetAnimator(layers_dir)
        animator.load_layers()
        return animator.create_pet_package(output_dir, pet_name)
