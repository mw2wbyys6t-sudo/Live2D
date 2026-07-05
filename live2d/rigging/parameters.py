#!/usr/bin/env python3
"""Standard Live2D parameter definitions and bindings."""

from typing import Dict, List


STANDARD_PARAMETERS: List[Dict] = [
    {"id": "ParamAngleX", "name": "角度X", "min": -30, "max": 30, "default": 0, "groups": ["head", "hair_front", "hair_back"]},
    {"id": "ParamAngleY", "name": "角度Y", "min": -30, "max": 30, "default": 0, "groups": ["head", "hair_front"]},
    {"id": "ParamAngleZ", "name": "角度Z", "min": -30, "max": 30, "default": 0, "groups": ["head", "hair_front", "hair_back"]},
    {"id": "ParamBodyAngleX", "name": "身体旋转X", "min": -10, "max": 10, "default": 0, "groups": ["body", "clothes"]},
    {"id": "ParamBodyAngleY", "name": "身体旋转Y", "min": -10, "max": 10, "default": 0, "groups": ["body", "clothes"]},
    {"id": "ParamEyeLOpen", "name": "左眼开闭", "min": 0, "max": 1, "default": 1, "groups": ["eyes"]},
    {"id": "ParamEyeROpen", "name": "右眼开闭", "min": 0, "max": 1, "default": 1, "groups": ["eyes"]},
    {"id": "ParamEyeBallX", "name": "眼球X", "min": -1, "max": 1, "default": 0, "groups": ["eyes"]},
    {"id": "ParamEyeBallY", "name": "眼球Y", "min": -1, "max": 1, "default": 0, "groups": ["eyes"]},
    {"id": "ParamMouthOpenY", "name": "口开闭", "min": 0, "max": 1, "default": 0, "groups": ["mouth"]},
    {"id": "ParamMouthForm", "name": "口形状", "min": -1, "max": 1, "default": 0, "groups": ["mouth"]},
    {"id": "ParamBrowLY", "name": "左眉上下", "min": -1, "max": 1, "default": 0, "groups": ["eyebrows"]},
    {"id": "ParamBrowRY", "name": "右眉上下", "min": -1, "max": 1, "default": 0, "groups": ["eyebrows"]},
    {"id": "ParamBreath", "name": "呼吸", "min": 0, "max": 1, "default": 0.5, "groups": ["body", "clothes"]},
    {"id": "ParamHairFrontX", "name": "前发X", "min": -15, "max": 15, "default": 0, "groups": ["hair_front"]},
    {"id": "ParamHairBackX", "name": "后发X", "min": -15, "max": 15, "default": 0, "groups": ["hair_back"]},
]


class ParameterSet(dict):
    """Dict-like container of standard Live2D parameters."""

    def __init__(self):
        super().__init__({p["id"]: p for p in STANDARD_PARAMETERS})

    def for_group(self, group: str) -> List[Dict]:
        """Return parameters that affect a given group."""
        if not isinstance(group, str):
            raise TypeError(f"group must be a string, got {type(group).__name__}")
        return [p for p in self.values() if group in p.get("groups", [])]
