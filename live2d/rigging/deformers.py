#!/usr/bin/env python3
"""Live2D-style deformer hierarchy generator."""

from typing import Dict, List

from live2d.logger import get_logger

log = get_logger("rigging.deformers")


class DeformerHierarchy:
    """Build a tree of warp/rotation deformers matching common layer groups."""

    GROUP_DEFORMERS = {
        "hair_back": "HairBack",
        "hair_front": "HairFront",
        "face": "Face",
        "eyes": "EyeGroup",
        "eyelashes": "EyeGroup",
        "eyebrows": "EyebrowGroup",
        "mouth": "Mouth",
        "nose": "Nose",
        "ears": "EarGroup",
        "body": "Body",
        "clothes": "Clothes",
        "arms_back": "ArmBackGroup",
        "legs": "LegGroup",
        "bg": "Background",
    }

    def build(self, layer_names: List[str]) -> Dict:
        """Return a deformer tree covering standard layer groups."""
        root = {"id": "Root", "type": "warp", "children": []}
        head = {"id": "Head", "type": "warp", "children": []}
        body = {"id": "Body", "type": "warp", "children": []}

        root["children"].append(head)
        root["children"].append(body)

        head["children"].append({"id": "Face", "type": "warp", "children": []})
        head["children"].append({"id": "HairFront", "type": "warp", "children": []})
        head["children"].append({"id": "HairBack", "type": "warp", "children": []})
        head["children"].append({"id": "LeftEye", "type": "rotation", "children": []})
        head["children"].append({"id": "RightEye", "type": "rotation", "children": []})
        head["children"].append({"id": "Mouth", "type": "warp", "children": []})
        head["children"].append({"id": "EyebrowGroup", "type": "warp", "children": []})

        body["children"].append({"id": "Neck", "type": "warp", "children": []})
        body["children"].append({"id": "Chest", "type": "warp", "children": []})
        body["children"].append({"id": "Clothes", "type": "warp", "children": []})

        return root

    def flatten(self, tree: Dict) -> List[Dict]:
        """Return tree nodes in pre-order."""
        result = [tree]
        for child in tree.get("children", []):
            result.extend(self.flatten(child))
        return result
