#!/usr/bin/env python3
"""
DeformerHierarchy + ParameterSet brutal tests.

Covers:
- DeformerHierarchy: empty input, single layer, full 52-layer set, repeated names,
  tree structure validation, flatten pre-order, determinism
- ParameterSet: standard parameter integrity, group queries, missing group,
  id uniqueness, default value ranges
"""

import pytest

from live2d.rigging.deformers import DeformerHierarchy
from live2d.rigging.parameters import ParameterSet, STANDARD_PARAMETERS


# ---------------- DeformerHierarchy ----------------

class TestDeformerHierarchyStructure:
    def test_build_returns_root_node(self):
        dh = DeformerHierarchy()
        tree = dh.build([])
        assert tree["id"] == "Root"
        assert tree["type"] == "warp"
        assert "children" in tree

    def test_root_has_head_and_body(self):
        dh = DeformerHierarchy()
        tree = dh.build([])
        ids = [c["id"] for c in tree["children"]]
        assert "Head" in ids
        assert "Body" in ids

    def test_head_contains_required_groups(self):
        dh = DeformerHierarchy()
        tree = dh.build([])
        head = next(c for c in tree["children"] if c["id"] == "Head")
        head_ids = {c["id"] for c in head["children"]}
        for required in ["Face", "HairFront", "HairBack", "LeftEye", "RightEye", "Mouth", "EyebrowGroup"]:
            assert required in head_ids, f"missing head child: {required}"

    def test_body_contains_required_groups(self):
        dh = DeformerHierarchy()
        tree = dh.build([])
        body = next(c for c in tree["children"] if c["id"] == "Body")
        body_ids = {c["id"] for c in body["children"]}
        for required in ["Neck", "Chest", "Clothes"]:
            assert required in body_ids, f"missing body child: {required}"

    def test_empty_layer_list_does_not_crash(self):
        dh = DeformerHierarchy()
        tree = dh.build([])
        assert tree["id"] == "Root"

    def test_single_layer(self):
        dh = DeformerHierarchy()
        tree = dh.build(["Background"])
        assert tree["id"] == "Root"

    def test_full_52_layer_set(self):
        dh = DeformerHierarchy()
        layer_names = [f"layer_{i}" for i in range(52)]
        tree = dh.build(layer_names)
        assert tree["id"] == "Root"

    def test_repeated_layer_names(self):
        dh = DeformerHierarchy()
        tree = dh.build(["Face", "Face", "Face"])
        assert tree["id"] == "Root"

    def test_special_character_layer_names(self):
        dh = DeformerHierarchy()
        tree = dh.build(["脸_基础", "头发_后", "Eye_White_R"])
        assert tree["id"] == "Root"


class TestDeformerHierarchyFlatten:
    def test_flatten_returns_pre_order(self):
        dh = DeformerHierarchy()
        tree = dh.build([])
        flat = dh.flatten(tree)
        # Root first, then Head, then Head's children, then Body, etc.
        assert flat[0]["id"] == "Root"
        assert flat[1]["id"] == "Head"
        # Face should come before Body in pre-order
        face_idx = next(i for i, n in enumerate(flat) if n["id"] == "Face")
        body_idx = next(i for i, n in enumerate(flat) if n["id"] == "Body")
        assert face_idx < body_idx

    def test_flatten_includes_all_nodes(self):
        dh = DeformerHierarchy()
        tree = dh.build([])
        flat = dh.flatten(tree)
        # All nodes should appear exactly once
        all_ids = [n["id"] for n in flat]
        assert len(all_ids) == len(set(all_ids)), "duplicate ids in flatten"

    def test_flatten_count_matches_tree(self):
        dh = DeformerHierarchy()
        tree = dh.build([])

        def count(node):
            return 1 + sum(count(c) for c in node.get("children", []))

        expected = count(tree)
        assert len(dh.flatten(tree)) == expected

    def test_flatten_empty_tree(self):
        dh = DeformerHierarchy()
        # Manually construct minimal tree
        tree = {"id": "Empty", "type": "warp", "children": []}
        flat = dh.flatten(tree)
        assert len(flat) == 1
        assert flat[0]["id"] == "Empty"

    def test_flatten_handles_missing_children_key(self):
        dh = DeformerHierarchy()
        tree = {"id": "Leaf", "type": "warp"}  # no children
        flat = dh.flatten(tree)
        assert len(flat) == 1


class TestDeformerHierarchyDeterminism:
    def test_same_input_same_output(self):
        dh = DeformerHierarchy()
        t1 = dh.build(["Face", "Hair"])
        t2 = dh.build(["Face", "Hair"])
        assert t1 == t2

    def test_different_inputs_same_structure(self):
        # build() ignores input layer_names currently - structure is fixed
        dh = DeformerHierarchy()
        t1 = dh.build([])
        t2 = dh.build(["A", "B", "C"])
        assert t1 == t2


# ---------------- ParameterSet ----------------

class TestParameterSetIntegrity:
    def test_standard_parameter_count(self):
        ps = ParameterSet()
        assert len(ps) == len(STANDARD_PARAMETERS)
        assert len(ps) >= 16  # at least 16 standard params

    def test_all_required_params_present(self):
        ps = ParameterSet()
        required = [
            "ParamAngleX", "ParamAngleY", "ParamAngleZ",
            "ParamBodyAngleX", "ParamBodyAngleY",
            "ParamEyeLOpen", "ParamEyeROpen",
            "ParamMouthOpenY", "ParamMouthForm",
            "ParamBrowLY", "ParamBrowRY",
            "ParamBreath",
        ]
        for p in required:
            assert p in ps, f"missing required parameter: {p}"

    def test_parameter_schema(self):
        ps = ParameterSet()
        for pid, p in ps.items():
            assert "id" in p
            assert "name" in p
            assert "min" in p
            assert "max" in p
            assert "default" in p
            assert "groups" in p
            assert p["min"] <= p["default"] <= p["max"], f"{pid}: default out of [min,max]"

    def test_unique_ids(self):
        ids = [p["id"] for p in STANDARD_PARAMETERS]
        assert len(ids) == len(set(ids)), "duplicate parameter ids"

    def test_dict_like_access(self):
        ps = ParameterSet()
        ps["ParamAngleX"]
        assert "ParamAngleX" in ps
        assert "NonExistentParam" not in ps

    def test_iteration(self):
        ps = ParameterSet()
        count = 0
        for _ in ps:
            count += 1
        assert count == len(STANDARD_PARAMETERS)


class TestParameterSetGroupQuery:
    def test_for_group_returns_list(self):
        ps = ParameterSet()
        result = ps.for_group("eyes")
        assert isinstance(result, list)
        assert len(result) > 0
        # All returned params should affect eyes
        for p in result:
            assert "eyes" in p["groups"]

    def test_for_group_eyes_includes_blink(self):
        ps = ParameterSet()
        result = ps.for_group("eyes")
        ids = {p["id"] for p in result}
        assert "ParamEyeLOpen" in ids
        assert "ParamEyeROpen" in ids

    def test_for_group_mouth_includes_open(self):
        ps = ParameterSet()
        result = ps.for_group("mouth")
        ids = {p["id"] for p in result}
        assert "ParamMouthOpenY" in ids
        assert "ParamMouthForm" in ids

    def test_for_group_unknown_returns_empty(self):
        ps = ParameterSet()
        result = ps.for_group("nonexistent_group")
        assert result == []

    def test_for_group_empty_string(self):
        ps = ParameterSet()
        result = ps.for_group("")
        assert result == []

    def test_for_group_none_raises(self):
        ps = ParameterSet()
        with pytest.raises(TypeError):
            ps.for_group(None)

    def test_for_group_all_standard_groups(self):
        ps = ParameterSet()
        groups = ["head", "hair_front", "hair_back", "body", "clothes",
                  "eyes", "mouth", "eyebrows"]
        for g in groups:
            result = ps.for_group(g)
            assert len(result) > 0, f"no params for group: {g}"
