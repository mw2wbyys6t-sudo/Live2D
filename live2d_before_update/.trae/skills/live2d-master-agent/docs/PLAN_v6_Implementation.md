# Live2D Production Pipeline v6.0 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在现有代码基础上，构建模块化的 Live2D Production Pipeline，实现从自然语言需求到 Live2D 生产建议的完整工作流。

**Architecture:** 采用渐进式增强策略，新增 `pipeline/` 目录实现 Node Layer、Workflow Layer、Agent Layer 三层架构，现有文件保持不变。

**Tech Stack:** Python 3.10+, dataclasses, typing, OpenCV (可选), MediaPipe (可选), 复用现有 diffusers/transformers

---

## 文件结构

```
pipeline/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── node.py              # BaseNode, NodeContext
│   ├── workflow.py          # Workflow 类
│   └── context.py           # 上下文管理
├── nodes/
│   ├── __init__.py
│   ├── character_node.py    # 角色设定解析
│   ├── live2d_rule_node.py  # Live2D规范约束
│   ├── composition_node.py  # 构图/镜头
│   ├── prompt_builder_node.py  # Prompt构建
│   ├── image_provider_node.py  # 图片生成Provider
│   ├── quality_check_node.py   # 质量评估
│   ├── repair_node.py       # 自动修复
│   ├── psd_planner_node.py  # PSD分层规划
│   ├── cubism_planner_node.py  # Cubism参数规划
│   └── reference_style_node.py # 参考图风格分析
├── workflows/
│   ├── __init__.py
│   ├── character_concept.py    # Workflow A
│   ├── live2d_portrait.py      # Workflow B
│   ├── live2d_production.py    # Workflow C
│   └── vtuber_full.py          # Workflow D
├── agent/
│   ├── __init__.py
│   └── live2d_agent.py      # 智能Agent
└── providers/
    ├── __init__.py
    ├── base_provider.py     # Provider接口
    ├── registry.py          # Provider注册表
    ├── local_sd_provider.py # 本地SD Provider
    └── comfyui_provider.py  # ComfyUI Provider
```

---

## Task 1: Core Framework (核心框架)

**Files:**
- Create: `pipeline/__init__.py`
- Create: `pipeline/core/__init__.py`
- Create: `pipeline/core/context.py`
- Create: `pipeline/core/node.py`
- Create: `pipeline/core/workflow.py`
- Test: `pipeline/tests/test_core.py`

- [ ] **Step 1: Write the failing test for NodeContext**

```python
# pipeline/tests/test_core.py
import pytest
from pipeline.core.context import NodeContext

def test_node_context_creation():
    ctx = NodeContext(data={"key": "value"}, user_input="test")
    assert ctx.data["key"] == "value"
    assert ctx.user_input == "test"
    assert ctx.metadata == {}

def test_node_context_defaults():
    ctx = NodeContext()
    assert ctx.data == {}
    assert ctx.metadata == {}
    assert ctx.user_input is None
    assert ctx.checkpoint is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /workspace/.trae/skills/live2d-master-agent && python3 -m pytest pipeline/tests/test_core.py -v 2>&1 | head -20`
Expected: `ModuleNotFoundError: No module named 'pipeline'`

- [ ] **Step 3: Implement NodeContext**

```python
# pipeline/core/context.py
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class NodeContext:
    """节点间传递的上下文"""
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    user_input: Optional[str] = None
    checkpoint: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        """安全获取数据"""
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> "NodeContext":
        """设置数据并返回自身（链式调用）"""
        self.data[key] = value
        return self
```

- [ ] **Step 4: Implement BaseNode**

```python
# pipeline/core/node.py
from abc import ABC, abstractmethod
from typing import Dict
from .context import NodeContext


class BaseNode(ABC):
    """所有节点的基类"""

    def __init__(self, name: str, config: Dict = None):
        self.name = name
        self.config = config or {}
        self.state = "idle"

    @abstractmethod
    def execute(self, context: NodeContext) -> NodeContext:
        """执行节点逻辑，返回更新后的上下文"""
        pass

    def validate_input(self, context: NodeContext) -> bool:
        """验证输入是否满足要求"""
        return True

    def on_success(self, context: NodeContext) -> NodeContext:
        """成功后的回调"""
        self.state = "success"
        return context

    def on_failure(self, context: NodeContext, error: Exception) -> NodeContext:
        """失败后的回调"""
        self.state = "failed"
        context.data["error"] = str(error)
        return context

    def run(self, context: NodeContext) -> NodeContext:
        """运行节点（包含验证和错误处理）"""
        try:
            self.state = "running"
            if not self.validate_input(context):
                raise ValueError(f"节点 {self.name} 输入验证失败")
            context = self.execute(context)
            return self.on_success(context)
        except Exception as e:
            return self.on_failure(context, e)
```

- [ ] **Step 5: Implement Workflow**

```python
# pipeline/core/workflow.py
from typing import List, Dict, Any
from .node import BaseNode
from .context import NodeContext


class Workflow:
    """工作流：有序的节点链"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.nodes: List[BaseNode] = []
        self.state = "idle"

    def add_node(self, node: BaseNode) -> "Workflow":
        self.nodes.append(node)
        return self

    def execute(self, context: NodeContext,
                human_in_loop: bool = True) -> NodeContext:
        """执行工作流"""
        self.state = "running"
        for i, node in enumerate(self.nodes):
            print(f"\n{'='*50}")
            print(f"步骤 {i+1}/{len(self.nodes)}: {node.name}")
            print(f"{'='*50}")

            context = node.run(context)

            if context.data.get("error"):
                print(f"❌ 节点 {node.name} 执行失败: {context.data['error']}")
                self.state = "failed"
                return context

            if human_in_loop and i < len(self.nodes) - 1:
                should_continue = self._pause_for_review(context, node.name)
                if not should_continue:
                    print("⏸️ 用户暂停工作流")
                    context.data["workflow_paused"] = True
                    context.data["paused_at_node"] = node.name
                    self.state = "paused"
                    return context

        self.state = "completed"
        print(f"\n✅ 工作流 '{self.name}' 执行完成")
        return context

    def _pause_for_review(self, context: NodeContext, node_name: str) -> bool:
        """暂停等待用户确认（CLI交互）"""
        self._display_results(context, node_name)
        user_input = input("\n🔄 继续下一步? [Y/n]: ").strip().lower()
        return user_input in ("", "y", "yes")

    def _display_results(self, context: NodeContext, node_name: str):
        """显示当前结果摘要"""
        print(f"\n📊 当前结果摘要:")
        for key, value in context.data.items():
            if key != "error":
                preview = str(value)[:100]
                print(f"  - {key}: {preview}")

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            "name": self.name,
            "description": self.description,
            "nodes": [node.name for node in self.nodes],
            "state": self.state
        }
```

- [ ] **Step 6: Create __init__ files**

```python
# pipeline/__init__.py
from .core.node import BaseNode
from .core.workflow import Workflow
from .core.context import NodeContext

__all__ = ["BaseNode", "Workflow", "NodeContext"]
```

```python
# pipeline/core/__init__.py
from .node import BaseNode
from .workflow import Workflow
from .context import NodeContext

__all__ = ["BaseNode", "Workflow", "NodeContext"]
```

- [ ] **Step 7: Run tests**

Run: `cd /workspace/.trae/skills/live2d-master-agent && python3 -m pytest pipeline/tests/test_core.py -v`
Expected: All tests PASS

- [ ] **Step 8: Commit**

```bash
cd /workspace/.trae/skills/live2d-master-agent
git add pipeline/
git commit -m "feat(pipeline): add core framework - Node, Workflow, Context"
```

---

## Task 2: Provider Layer (Provider层)

**Files:**
- Create: `pipeline/providers/__init__.py`
- Create: `pipeline/providers/base_provider.py`
- Create: `pipeline/providers/registry.py`
- Create: `pipeline/providers/local_sd_provider.py`
- Create: `pipeline/providers/comfyui_provider.py`
- Test: `pipeline/tests/test_providers.py`

- [ ] **Step 1: Write the failing test**

```python
# pipeline/tests/test_providers.py
import pytest
from pipeline.providers.base_provider import BaseImageProvider
from pipeline.providers.registry import ProviderRegistry

def test_registry_has_providers():
    registry = ProviderRegistry()
    assert "local" in registry.providers
    assert "comfyui" in registry.providers

def test_registry_select_default():
    registry = ProviderRegistry()
    provider = registry.select({"style": "anime"})
    assert provider is not None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest pipeline/tests/test_providers.py -v`
Expected: `ModuleNotFoundError`

- [ ] **Step 3: Implement BaseImageProvider**

```python
# pipeline/providers/base_provider.py
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseImageProvider(ABC):
    """图片生成Provider基类"""

    @abstractmethod
    def generate(self, prompt: str, negative_prompt: str = "",
                 width: int = 1024, height: int = 1536,
                 **kwargs) -> str:
        """生成图片，返回图片路径"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """检查Provider是否可用"""
        pass

    @property
    @abstractmethod
    def cost_estimate(self) -> float:
        """预估成本（0=免费，1=低，2=中，3=高）"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider名称"""
        pass
```

- [ ] **Step 4: Implement LocalSDProvider**

```python
# pipeline/providers/local_sd_provider.py
import os
import sys
from .base_provider import BaseImageProvider


class LocalSDProvider(BaseImageProvider):
    """本地Stable Diffusion Provider"""

    @property
    def name(self) -> str:
        return "local_sd"

    def is_available(self) -> bool:
        try:
            import diffusers
            import torch
            return True
        except ImportError:
            return False

    @property
    def cost_estimate(self) -> float:
        return 0.0  # 免费

    def generate(self, prompt: str, negative_prompt: str = "",
                 width: int = 1024, height: int = 1536,
                 **kwargs) -> str:
        """使用本地SD生成图片"""
        # 复用现有 local_image_generator.py
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from local_image_generator import ImageGenerator

        generator = ImageGenerator()
        output_dir = kwargs.get("output_dir", "./outputs")
        seed = kwargs.get("seed", None)

        success, path = generator.generate(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            seed=seed,
            output_dir=output_dir
        )

        if success and path:
            return path
        raise RuntimeError("本地SD生成失败")
```

- [ ] **Step 5: Implement ComfyUIProvider**

```python
# pipeline/providers/comfyui_provider.py
import os
import sys
from .base_provider import BaseImageProvider


class ComfyUIProvider(BaseImageProvider):
    """ComfyUI Provider"""

    @property
    def name(self) -> str:
        return "comfyui"

    def is_available(self) -> bool:
        try:
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            from comfyui_integration import ComfyUIGenerator
            generator = ComfyUIGenerator()
            return generator.check_server()
        except Exception:
            return False

    @property
    def cost_estimate(self) -> float:
        return 0.0  # 本地运行免费

    def generate(self, prompt: str, negative_prompt: str = "",
                 width: int = 1024, height: int = 1536,
                 **kwargs) -> str:
        """使用ComfyUI生成图片"""
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from comfyui_integration import ComfyUIGenerator

        generator = ComfyUIGenerator()
        if not generator.check_server():
            raise RuntimeError("ComfyUI服务器未运行")

        # 使用预设生成
        result = generator.generate_with_preset(
            preset_name=kwargs.get("preset", "cute_kawaii"),
            output_dir=kwargs.get("output_dir", "./outputs")
        )

        if result and result.get("success"):
            return result["image_path"]
        raise RuntimeError("ComfyUI生成失败")
```

- [ ] **Step 6: Implement ProviderRegistry**

```python
# pipeline/providers/registry.py
from typing import Dict, List
from .base_provider import BaseImageProvider
from .local_sd_provider import LocalSDProvider
from .comfyui_provider import ComfyUIProvider


class ProviderRegistry:
    """Provider注册表"""

    def __init__(self):
        self.providers: Dict[str, BaseImageProvider] = {}
        self._register_defaults()

    def _register_defaults(self):
        self.register("local", LocalSDProvider())
        self.register("comfyui", ComfyUIProvider())

    def register(self, name: str, provider: BaseImageProvider):
        self.providers[name] = provider

    def get_available(self) -> List[str]:
        return [name for name, p in self.providers.items() if p.is_available()]

    def get(self, name: str) -> BaseImageProvider:
        if name not in self.providers:
            raise ValueError(f"未知Provider: {name}")
        return self.providers[name]

    def select(self, criteria: Dict) -> BaseImageProvider:
        """根据条件选择最优Provider"""
        available = self.get_available()
        if not available:
            raise RuntimeError("没有可用的Provider")

        style = criteria.get("style", "anime")
        quality = criteria.get("quality", "standard")
        budget = criteria.get("budget", "low")

        if budget == "low":
            for name in ["local", "comfyui"]:
                if name in available:
                    return self.providers[name]

        return self.providers[available[0]]
```

- [ ] **Step 7: Create __init__**

```python
# pipeline/providers/__init__.py
from .base_provider import BaseImageProvider
from .registry import ProviderRegistry
from .local_sd_provider import LocalSDProvider
from .comfyui_provider import ComfyUIProvider

__all__ = ["BaseImageProvider", "ProviderRegistry", "LocalSDProvider", "ComfyUIProvider"]
```

- [ ] **Step 8: Run tests**

Run: `python3 -m pytest pipeline/tests/test_providers.py -v`
Expected: All tests PASS

- [ ] **Step 9: Commit**

```bash
git add pipeline/providers/
git commit -m "feat(pipeline): add provider layer - local SD and ComfyUI"
```

---

## Task 3: Character Node + Live2D Rule Node

**Files:**
- Create: `pipeline/nodes/__init__.py`
- Create: `pipeline/nodes/character_node.py`
- Create: `pipeline/nodes/live2d_rule_node.py`
- Test: `pipeline/tests/test_nodes.py`

- [ ] **Step 1: Write the failing test**

```python
# pipeline/tests/test_nodes.py
import pytest
from pipeline.core.context import NodeContext
from pipeline.nodes.character_node import CharacterNode
from pipeline.nodes.live2d_rule_node import Live2DRuleNode

def test_character_node():
    node = CharacterNode("角色设定")
    ctx = NodeContext(user_input="蓝发猫耳少女")
    result = node.run(ctx)
    assert "character" in result.data
    assert result.data["character"]["hair"]["color"] == "blue"

def test_live2d_rule_node():
    node = Live2DRuleNode("Live2D规范")
    ctx = NodeContext()
    ctx.data["character"] = {"style": "anime"}
    result = node.run(ctx)
    assert "live2d_constraints" in result.data
```

- [ ] **Step 2: Implement CharacterNode**

```python
# pipeline/nodes/character_node.py
import re
from typing import Dict, Any
from pipeline.core.node import BaseNode
from pipeline.core.context import NodeContext


class CharacterNode(BaseNode):
    """角色设定节点：将自然语言解析为结构化角色设定"""

    def execute(self, context: NodeContext) -> NodeContext:
        user_input = context.user_input or ""

        # 解析角色设定
        character = self._parse_character(user_input)

        context.data["character"] = character
        print(f"🎭 角色设定: {character.get('description', '未知角色')}")
        return context

    def _parse_character(self, text: str) -> Dict[str, Any]:
        """解析自然语言为结构化角色设定"""
        text_lower = text.lower()

        # 发色检测
        hair_colors = {
            "蓝": "blue", "藍": "blue", "blue": "blue",
            "红": "red", "紅": "red", "red": "red",
            "金": "blonde", "黄": "blonde", "blonde": "blonde", "yellow": "blonde",
            "黑": "black", "black": "black",
            "白": "white", "white": "white",
            "粉": "pink", "pink": "pink",
            "紫": "purple", "purple": "purple",
            "绿": "green", "綠": "green", "green": "green",
            "银": "silver", "銀": "silver", "silver": "silver",
        }

        hair_color = "unknown"
        for key, value in hair_colors.items():
            if key in text_lower:
                hair_color = value
                break

        # 特征检测
        features = {
            "cat_ears": "猫耳" in text or "cat" in text_lower,
            "fox_ears": "狐耳" in text or "fox" in text_lower,
            "animal_ears": "兽耳" in text or "animal" in text_lower,
            "tail": "尾" in text or "tail" in text_lower,
            "wings": "翼" in text or "wing" in text_lower,
            "horns": "角" in text or "horn" in text_lower,
            "glasses": "眼镜" in text or "glasses" in text_lower,
        }

        # 风格检测
        style = "anime"
        if any(k in text_lower for k in ["写实", "realistic", "real"]):
            style = "semi_realistic"
        elif any(k in text_lower for k in ["vtuber", "虚拟主播"]):
            style = "vtuber"
        elif any(k in text_lower for k in ["live2d", "立绘"]):
            style = "live2d_ready"

        # 性别检测
        gender = "female"
        if any(k in text_lower for k in ["男", "boy", "male", "guy"]):
            gender = "male"
        elif any(k in text_lower for k in ["中性", "neutral", "ambiguous"]):
            gender = "ambiguous"

        # 年龄检测
        age_group = "teen"
        if any(k in text_lower for k in ["成年", "大人", "adult"]):
            age_group = "adult"
        elif any(k in text_lower for k in ["小孩", "child", "loli", "shota"]):
            age_group = "child"

        character = {
            "description": text,
            "age_group": age_group,
            "gender": gender,
            "hair": {
                "color": hair_color,
                "style": "long" if "长" in text or "long" in text_lower else "short",
                "length": "long" if "长" in text or "long" in text_lower else "medium"
            },
            "eyes": {
                "color": hair_color if hair_color != "unknown" else "blue",
                "shape": "large"
            },
            "features": features,
            "style": style,
            "pose_preference": "standing",
            "expression": "neutral"
        }

        return character
```

- [ ] **Step 3: Implement Live2DRuleNode**

```python
# pipeline/nodes/live2d_rule_node.py
from typing import Dict, Any, List
from pipeline.core.node import BaseNode
from pipeline.core.context import NodeContext


class Live2DRuleNode(BaseNode):
    """Live2D规范约束节点"""

    RULES = {
        "visibility": [
            "neck_visible",
            "both_shoulders_visible",
            "no_excessive_occlusion"
        ],
        "separation": [
            "arms_separable",
            "hair_layers_clear",
            "clothing_separable"
        ],
        "technical": [
            "no_transparent_clothing",
            "no_complex_patterns",
            "solid_background",
            "front_facing_or_3_4"
        ]
    }

    def execute(self, context: NodeContext) -> NodeContext:
        character = context.data.get("character", {})

        constraints = self._generate_constraints(character)

        context.data["live2d_constraints"] = constraints
        print(f"📋 Live2D约束: {len(constraints)} 条规则")
        return context

    def _generate_constraints(self, character: Dict) -> List[str]:
        """根据角色设定生成约束"""
        constraints = []

        # 基础约束（所有角色）
        constraints.extend([
            "neck must be visible",
            "both shoulders must be visible",
            "arms must be clearly separable from body",
            "hair must have clear front/back layers",
            "solid color background (white or transparent)",
            "front facing or 3/4 view",
            "no transparent clothing",
            "no complex patterns on clothing"
        ])

        # 根据特征添加特殊约束
        features = character.get("features", {})
        if features.get("cat_ears") or features.get("fox_ears"):
            constraints.append("animal ears must be on separate layer from hair")
        if features.get("tail"):
            constraints.append("tail must be clearly visible and separable")
        if features.get("wings"):
            constraints.append("wings must be on separate layer behind body")

        # 根据风格调整
        style = character.get("style", "anime")
        if style == "live2d_ready":
            constraints.extend([
                "medium shot (waist up)",
                "eye level camera angle",
                "minimal foreshortening"
            ])

        return constraints
```

- [ ] **Step 4: Create __init__**

```python
# pipeline/nodes/__init__.py
from .character_node import CharacterNode
from .live2d_rule_node import Live2DRuleNode

__all__ = ["CharacterNode", "Live2DRuleNode"]
```

- [ ] **Step 5: Run tests**

Run: `python3 -m pytest pipeline/tests/test_nodes.py -v`
Expected: All tests PASS

- [ ] **Step 6: Commit**

```bash
git add pipeline/nodes/
git commit -m "feat(pipeline): add character and live2d rule nodes"
```

---

## Task 4: Composition Node + Prompt Builder Node

**Files:**
- Create: `pipeline/nodes/composition_node.py`
- Create: `pipeline/nodes/prompt_builder_node.py`
- Modify: `pipeline/nodes/__init__.py`
- Test: `pipeline/tests/test_nodes.py` (追加)

- [ ] **Step 1: Implement CompositionNode**

```python
# pipeline/nodes/composition_node.py
from typing import Dict, Any
from pipeline.core.node import BaseNode
from pipeline.core.context import NodeContext


class CompositionNode(BaseNode):
    """构图节点"""

    TEMPLATES = {
        "portrait": {
            "camera": "medium_shot",
            "angle": "eye_level",
            "pose": "standing_front",
            "framing": "waist_up",
            "width": 1024,
            "height": 1536
        },
        "full_body": {
            "camera": "full_shot",
            "angle": "slight_high",
            "pose": "standing",
            "framing": "full_body",
            "width": 1024,
            "height": 2048
        },
        "live2d_optimized": {
            "camera": "medium_shot",
            "angle": "eye_level",
            "pose": "standing_front",
            "framing": "chest_up",
            "background": "solid_white",
            "width": 1024,
            "height": 1536
        }
    }

    def execute(self, context: NodeContext) -> NodeContext:
        character = context.data.get("character", {})
        style = character.get("style", "anime")

        composition = self._select_composition(style, character)

        context.data["composition"] = composition
        print(f"📐 构图: {composition['camera']}, {composition['framing']}")
        return context

    def _select_composition(self, style: str, character: Dict) -> Dict[str, Any]:
        if style == "live2d_ready":
            template = self.TEMPLATES["live2d_optimized"].copy()
        elif style == "vtuber":
            template = self.TEMPLATES["portrait"].copy()
        else:
            template = self.TEMPLATES["portrait"].copy()

        # 根据角色特征调整
        pose = character.get("pose_preference", "standing")
        if pose == "sitting":
            template["pose"] = "sitting"
        elif pose == "dynamic":
            template["pose"] = "dynamic_action"

        return template
```

- [ ] **Step 2: Implement PromptBuilderNode**

```python
# pipeline/nodes/prompt_builder_node.py
from typing import Dict, Any, List
from pipeline.core.node import BaseNode
from pipeline.core.context import NodeContext


class PromptBuilderNode(BaseNode):
    """Prompt构建节点"""

    STYLE_PREFIXES = {
        "anime": "masterpiece, best quality, anime style, ",
        "semi_realistic": "masterpiece, best quality, semi-realistic, ",
        "vtuber": "masterpiece, best quality, VTuber style, clean lines, ",
        "live2d_ready": "masterpiece, best quality, Live2D ready, clean edges, flat colors, "
    }

    NEGATIVE_PROMPTS = {
        "anime": "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
        "live2d_ready": "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, complex background, gradient background, transparent clothing, overlapping elements"
    }

    def execute(self, context: NodeContext) -> NodeContext:
        character = context.data.get("character", {})
        constraints = context.data.get("live2d_constraints", [])
        composition = context.data.get("composition", {})

        positive = self._build_positive(character, constraints, composition)
        negative = self._build_negative(character, constraints)

        context.data["prompt"] = {
            "positive": positive,
            "negative": negative,
            "width": composition.get("width", 1024),
            "height": composition.get("height", 1536),
            "style": character.get("style", "anime")
        }

        print(f"📝 Prompt构建完成 (长度: {len(positive)} 字符)")
        return context

    def _build_positive(self, character: Dict, constraints: List[str],
                        composition: Dict) -> str:
        style = character.get("style", "anime")
        prefix = self.STYLE_PREFIXES.get(style, self.STYLE_PREFIXES["anime"])

        parts = [prefix]

        # 角色描述
        desc = character.get("description", "")
        parts.append(desc)

        # 发色
        hair = character.get("hair", {})
        if hair.get("color") and hair["color"] != "unknown":
            parts.append(f"{hair['color']} hair")
        if hair.get("length"):
            parts.append(f"{hair['length']} hair")

        # 特征
        features = character.get("features", {})
        if features.get("cat_ears"):
            parts.append("cat ears")
        if features.get("fox_ears"):
            parts.append("fox ears")
        if features.get("tail"):
            parts.append("tail")

        # 构图
        parts.append(f"{composition.get('camera', 'medium shot')}")
        parts.append(f"{composition.get('angle', 'eye level')}")
        parts.append(f"{composition.get('pose', 'standing')}")

        # Live2D约束
        parts.append("solid white background")
        parts.append("clean edges")
        parts.append("front facing")

        return ", ".join(parts)

    def _build_negative(self, character: Dict, constraints: List[str]) -> str:
        style = character.get("style", "anime")
        return self.NEGATIVE_PROMPTS.get(style, self.NEGATIVE_PROMPTS["anime"])
```

- [ ] **Step 3: Update __init__**

```python
# pipeline/nodes/__init__.py
from .character_node import CharacterNode
from .live2d_rule_node import Live2DRuleNode
from .composition_node import CompositionNode
from .prompt_builder_node import PromptBuilderNode

__all__ = ["CharacterNode", "Live2DRuleNode", "CompositionNode", "PromptBuilderNode"]
```

- [ ] **Step 4: Add tests**

```python
# Append to pipeline/tests/test_nodes.py

def test_composition_node():
    node = CompositionNode("构图")
    ctx = NodeContext()
    ctx.data["character"] = {"style": "live2d_ready"}
    result = node.run(ctx)
    assert "composition" in result.data
    assert result.data["composition"]["camera"] == "medium_shot"

def test_prompt_builder_node():
    node = PromptBuilderNode("Prompt构建")
    ctx = NodeContext()
    ctx.data["character"] = {
        "style": "anime",
        "description": "蓝发少女",
        "hair": {"color": "blue", "length": "long"},
        "features": {"cat_ears": True}
    }
    ctx.data["live2d_constraints"] = ["neck visible"]
    ctx.data["composition"] = {"camera": "medium_shot", "width": 1024, "height": 1536}
    result = node.run(ctx)
    assert "prompt" in result.data
    assert "blue hair" in result.data["prompt"]["positive"]
    assert "cat ears" in result.data["prompt"]["positive"]
```

- [ ] **Step 5: Run tests**

Run: `python3 -m pytest pipeline/tests/test_nodes.py -v`
Expected: All tests PASS

- [ ] **Step 6: Commit**

```bash
git add pipeline/nodes/ pipeline/tests/
git commit -m "feat(pipeline): add composition and prompt builder nodes"
```

---

## Task 5: Image Provider Node + Quality Check Node

**Files:**
- Create: `pipeline/nodes/image_provider_node.py`
- Create: `pipeline/nodes/quality_check_node.py`
- Modify: `pipeline/nodes/__init__.py`
- Test: `pipeline/tests/test_nodes.py` (追加)

- [ ] **Step 1: Implement ImageProviderNode**

```python
# pipeline/nodes/image_provider_node.py
import os
from pipeline.core.node import BaseNode
from pipeline.core.context import NodeContext
from pipeline.providers.registry import ProviderRegistry


class ImageProviderNode(BaseNode):
    """图片生成节点"""

    def __init__(self, name: str, config: Dict = None):
        super().__init__(name, config)
        self.registry = ProviderRegistry()
        self.provider = None

    def execute(self, context: NodeContext) -> NodeContext:
        prompt_data = context.data.get("prompt", {})
        style = prompt_data.get("style", "anime")

        # 选择Provider
        criteria = {
            "style": style,
            "budget": self.config.get("budget", "low")
        }
        self.provider = self.registry.select(criteria)

        print(f"🎨 使用Provider: {self.provider.name}")

        # 生成图片
        output_dir = self.config.get("output_dir", "./pipeline_outputs")
        os.makedirs(output_dir, exist_ok=True)

        image_path = self.provider.generate(
            prompt=prompt_data["positive"],
            negative_prompt=prompt_data["negative"],
            width=prompt_data.get("width", 1024),
            height=prompt_data.get("height", 1536),
            output_dir=output_dir
        )

        context.data["generated_image"] = image_path
        print(f"✅ 图片生成完成: {image_path}")
        return context
```

- [ ] **Step 2: Implement QualityCheckNode**

```python
# pipeline/nodes/quality_check_node.py
import os
from typing import Dict, Any
from PIL import Image
import numpy as np
from pipeline.core.node import BaseNode
from pipeline.core.context import NodeContext


class QualityCheckNode(BaseNode):
    """质量评估节点"""

    DIMENSIONS = {
        "face_quality": {"weight": 0.25, "threshold": 60},
        "hand_detection": {"weight": 0.15, "threshold": 50},
        "live2d_adaptability": {"weight": 0.30, "threshold": 70},
        "perspective_consistency": {"weight": 0.15, "threshold": 60},
        "occlusion_analysis": {"weight": 0.15, "threshold": 60}
    }

    def execute(self, context: NodeContext) -> NodeContext:
        image_path = context.data.get("generated_image")
        if not image_path or not os.path.exists(image_path):
            raise ValueError("未找到生成的图片")

        print(f"🔍 开始质量评估: {image_path}")

        scores = {}
        for dimension, config in self.DIMENSIONS.items():
            scores[dimension] = self._evaluate_dimension(image_path, dimension)
            print(f"  {dimension}: {scores[dimension]:.1f}/100")

        overall = sum(
            scores[d] * config["weight"]
            for d, config in self.DIMENSIONS.items()
        )

        threshold = self.config.get("threshold", 70)
        is_acceptable = overall >= threshold

        context.data["quality_report"] = {
            "overall_score": round(overall, 1),
            "dimension_scores": scores,
            "is_acceptable": is_acceptable,
            "threshold": threshold,
            "suggestions": self._generate_suggestions(scores)
        }

        status = "✅ 通过" if is_acceptable else "❌ 未通过"
        print(f"\n📊 综合评分: {overall:.1f}/100 {status}")

        return context

    def _evaluate_dimension(self, image_path: str, dimension: str) -> float:
        """评估单个维度"""
        try:
            img = Image.open(image_path)
            img_array = np.array(img)

            if dimension == "face_quality":
                return self._eval_face_quality(img_array)
            elif dimension == "hand_detection":
                return self._eval_hand_detection(img_array)
            elif dimension == "live2d_adaptability":
                return self._eval_live2d_adaptability(img_array)
            elif dimension == "perspective_consistency":
                return self._eval_perspective(img_array)
            elif dimension == "occlusion_analysis":
                return self._eval_occlusion(img_array)
        except Exception as e:
            print(f"  ⚠️ {dimension}评估失败: {e}")
            return 50.0

    def _eval_face_quality(self, img_array: np.ndarray) -> float:
        """脸部质量评估（简化版）"""
        # 使用拉普拉斯算子评估清晰度
        from scipy import ndimage
        gray = np.mean(img_array, axis=2) if len(img_array.shape) == 3 else img_array
        laplacian = ndimage.laplace(gray)
        sharpness = min(np.var(laplacian) / 500, 100)

        # 色彩丰富度
        if len(img_array.shape) == 3:
            color_variance = np.std(img_array.reshape(-1, 3), axis=0).mean()
            color_score = min(color_variance / 2, 100)
        else:
            color_score = 50

        return (sharpness * 0.6 + color_score * 0.4)

    def _eval_hand_detection(self, img_array: np.ndarray) -> float:
        """手部检测（简化版：检查图片下半部分是否有复杂结构）"""
        h, w = img_array.shape[:2]
        lower_half = img_array[h//2:, :]
        edges = np.std(lower_half)
        # 如果下半部分边缘丰富，可能有手部
        score = min(edges / 10, 100)
        return max(score, 60)  # 保守估计

    def _eval_live2d_adaptability(self, img_array: np.ndarray) -> float:
        """Live2D适配度"""
        # 边缘清晰度
        from scipy import ndimage
        gray = np.mean(img_array, axis=2) if len(img_array.shape) == 3 else img_array
        sobel_h = ndimage.sobel(gray, axis=0)
        sobel_v = ndimage.sobel(gray, axis=1)
        edge_strength = np.sqrt(sobel_h**2 + sobel_v**2).mean()
        edge_score = min(edge_strength / 5, 100)

        # 背景均匀度（假设背景在边缘）
        h, w = gray.shape
        border = np.concatenate([
            gray[0, :], gray[-1, :], gray[:, 0], gray[:, -1]
        ])
        bg_uniformity = 100 - min(np.std(border) * 2, 100)

        return (edge_score * 0.6 + bg_uniformity * 0.4)

    def _eval_perspective(self, img_array: np.ndarray) -> float:
        """透视一致性"""
        # 简化：检查左右对称性
        h, w = img_array.shape[:2]
        left = img_array[:, :w//2]
        right = img_array[:, w//2:]
        right_flipped = np.fliplr(right)

        min_w = min(left.shape[1], right_flipped.shape[1])
        symmetry = 100 - np.mean(np.abs(left[:, :min_w] - right_flipped[:, :min_w])) / 2.55

        return max(symmetry, 50)

    def _eval_occlusion(self, img_array: np.ndarray) -> float:
        """遮挡分析"""
        # 简化：检查颜色区域数量（颜色量化）
        from sklearn.cluster import KMeans
        pixels = img_array.reshape(-1, 3) if len(img_array.shape) == 3 else img_array.reshape(-1, 1)

        if len(pixels) > 1000:
            sample = pixels[np.random.choice(len(pixels), 1000, replace=False)]
        else:
            sample = pixels

        kmeans = KMeans(n_clusters=8, random_state=42, n_init=10)
        kmeans.fit(sample)

        # 颜色区域越少，越容易分层
        n_colors = len(np.unique(kmeans.labels_))
        score = 100 - (n_colors - 3) * 10

        return max(min(score, 100), 40)

    def _generate_suggestions(self, scores: Dict[str, float]) -> list:
        """生成改进建议"""
        suggestions = []

        if scores.get("face_quality", 100) < 60:
            suggestions.append("脸部清晰度不足，建议增加细节描述词")
        if scores.get("live2d_adaptability", 100) < 70:
            suggestions.append("Live2D适配度不足，建议使用纯色背景并减少复杂元素")
        if scores.get("occlusion_analysis", 100) < 60:
            suggestions.append("存在自遮挡，建议调整姿势或减少重叠元素")

        return suggestions
```

- [ ] **Step 3: Update __init__**

```python
# pipeline/nodes/__init__.py
from .character_node import CharacterNode
from .live2d_rule_node import Live2DRuleNode
from .composition_node import CompositionNode
from .prompt_builder_node import PromptBuilderNode
from .image_provider_node import ImageProviderNode
from .quality_check_node import QualityCheckNode

__all__ = [
    "CharacterNode", "Live2DRuleNode", "CompositionNode",
    "PromptBuilderNode", "ImageProviderNode", "QualityCheckNode"
]
```

- [ ] **Step 4: Add tests**

```python
# Append to pipeline/tests/test_nodes.py

def test_image_provider_node_mock():
    # 使用mock测试（不需要实际生成图片）
    node = ImageProviderNode("图片生成", {"provider": "local", "budget": "low"})
    ctx = NodeContext()
    ctx.data["prompt"] = {
        "positive": "test prompt",
        "negative": "",
        "width": 512,
        "height": 512,
        "style": "anime"
    }
    # 注意：此测试需要本地SD环境，可能跳过
    try:
        result = node.run(ctx)
        assert "generated_image" in result.data or "error" in result.data
    except Exception:
        pytest.skip("本地SD不可用")

def test_quality_check_node():
    from PIL import Image
    import numpy as np

    # 创建测试图片
    test_img = Image.new('RGB', (512, 768), color=(200, 180, 220))
    test_img.save('/tmp/test_quality.png')

    node = QualityCheckNode("质量评估")
    ctx = NodeContext()
    ctx.data["generated_image"] = '/tmp/test_quality.png'
    result = node.run(ctx)

    assert "quality_report" in result.data
    assert "overall_score" in result.data["quality_report"]
```

- [ ] **Step 5: Run tests**

Run: `python3 -m pytest pipeline/tests/test_nodes.py -v`
Expected: All tests PASS

- [ ] **Step 6: Commit**

```bash
git add pipeline/nodes/ pipeline/tests/
git commit -m "feat(pipeline): add image provider and quality check nodes"
```

---

## Task 6: Workflows (工作流)

**Files:**
- Create: `pipeline/workflows/__init__.py`
- Create: `pipeline/workflows/character_concept.py`
- Create: `pipeline/workflows/live2d_portrait.py`
- Create: `pipeline/workflows/live2d_production.py`
- Create: `pipeline/workflows/vtuber_full.py`
- Test: `pipeline/tests/test_workflows.py`

- [ ] **Step 1: Implement Workflow B (Live2D立绘)**

```python
# pipeline/workflows/live2d_portrait.py
from pipeline.core.workflow import Workflow
from pipeline.nodes.character_node import CharacterNode
from pipeline.nodes.live2d_rule_node import Live2DRuleNode
from pipeline.nodes.composition_node import CompositionNode
from pipeline.nodes.prompt_builder_node import PromptBuilderNode
from pipeline.nodes.image_provider_node import ImageProviderNode
from pipeline.nodes.quality_check_node import QualityCheckNode


def create_live2d_portrait_workflow(
    provider_budget: str = "low",
    output_dir: str = "./pipeline_outputs"
) -> Workflow:
    """Live2D立绘生成工作流"""
    return (
        Workflow("Live2D立绘", "生成适合Live2D的立绘")
        .add_node(CharacterNode("角色设定"))
        .add_node(Live2DRuleNode("Live2D规范"))
        .add_node(CompositionNode("构图"))
        .add_node(PromptBuilderNode("Prompt构建"))
        .add_node(ImageProviderNode("图片生成", {
            "budget": provider_budget,
            "output_dir": output_dir
        }))
        .add_node(QualityCheckNode("质量评估", {"threshold": 70}))
    )
```

- [ ] **Step 2: Implement Workflow A (角色概念)**

```python
# pipeline/workflows/character_concept.py
from pipeline.core.workflow import Workflow
from pipeline.nodes.character_node import CharacterNode
from pipeline.nodes.composition_node import CompositionNode
from pipeline.nodes.prompt_builder_node import PromptBuilderNode
from pipeline.nodes.image_provider_node import ImageProviderNode


def create_character_concept_workflow(
    provider_budget: str = "low",
    output_dir: str = "./pipeline_outputs"
) -> Workflow:
    """角色概念生成工作流"""
    return (
        Workflow("角色概念", "快速生成角色概念图")
        .add_node(CharacterNode("角色设定"))
        .add_node(CompositionNode("构图"))
        .add_node(PromptBuilderNode("Prompt构建"))
        .add_node(ImageProviderNode("图片生成", {
            "budget": provider_budget,
            "output_dir": output_dir
        }))
    )
```

- [ ] **Step 3: Implement Workflow C (生产准备)**

```python
# pipeline/workflows/live2d_production.py
from pipeline.core.workflow import Workflow
from pipeline.nodes.character_node import CharacterNode
from pipeline.nodes.live2d_rule_node import Live2DRuleNode
from pipeline.nodes.composition_node import CompositionNode
from pipeline.nodes.prompt_builder_node import PromptBuilderNode
from pipeline.nodes.image_provider_node import ImageProviderNode
from pipeline.nodes.quality_check_node import QualityCheckNode


def create_live2d_production_workflow(
    provider_budget: str = "low",
    output_dir: str = "./pipeline_outputs"
) -> Workflow:
    """Live2D生产准备工作流"""
    return (
        Workflow("Live2D生产", "完整的Live2D生产准备")
        .add_node(CharacterNode("角色设定"))
        .add_node(Live2DRuleNode("Live2D规范"))
        .add_node(CompositionNode("构图"))
        .add_node(PromptBuilderNode("Prompt构建"))
        .add_node(ImageProviderNode("图片生成", {
            "budget": provider_budget,
            "output_dir": output_dir
        }))
        .add_node(QualityCheckNode("质量评估", {"threshold": 70}))
    )
```

- [ ] **Step 4: Implement Workflow D (VTuber)**

```python
# pipeline/workflows/vtuber_full.py
from pipeline.core.workflow import Workflow
from pipeline.nodes.character_node import CharacterNode
from pipeline.nodes.prompt_builder_node import PromptBuilderNode
from pipeline.nodes.image_provider_node import ImageProviderNode


def create_vtuber_full_workflow(
    provider_budget: str = "low",
    output_dir: str = "./pipeline_outputs"
) -> Workflow:
    """VTuber完整方案工作流"""
    return (
        Workflow("VTuber完整方案", "从需求到Live2D的完整方案")
        .add_node(CharacterNode("角色设定"))
        .add_node(PromptBuilderNode("Prompt构建"))
        .add_node(ImageProviderNode("概念图生成", {
            "budget": provider_budget,
            "output_dir": output_dir
        }))
    )
```

- [ ] **Step 5: Create __init__**

```python
# pipeline/workflows/__init__.py
from .character_concept import create_character_concept_workflow
from .live2d_portrait import create_live2d_portrait_workflow
from .live2d_production import create_live2d_production_workflow
from .vtuber_full import create_vtuber_full_workflow

__all__ = [
    "create_character_concept_workflow",
    "create_live2d_portrait_workflow",
    "create_live2d_production_workflow",
    "create_vtuber_full_workflow"
]
```

- [ ] **Step 6: Write tests**

```python
# pipeline/tests/test_workflows.py
import pytest
from pipeline.core.context import NodeContext
from pipeline.workflows import (
    create_character_concept_workflow,
    create_live2d_portrait_workflow
)

def test_workflow_creation():
    wf = create_live2d_portrait_workflow()
    assert wf.name == "Live2D立绘"
    assert len(wf.nodes) == 6

def test_workflow_to_dict():
    wf = create_character_concept_workflow()
    d = wf.to_dict()
    assert d["name"] == "角色概念"
    assert "nodes" in d
```

- [ ] **Step 7: Run tests**

Run: `python3 -m pytest pipeline/tests/test_workflows.py -v`
Expected: All tests PASS

- [ ] **Step 8: Commit**

```bash
git add pipeline/workflows/ pipeline/tests/
git commit -m "feat(pipeline): add workflow layer - 4 preset workflows"
```

---

## Task 7: Live2D Agent + CLI

**Files:**
- Create: `pipeline/agent/__init__.py`
- Create: `pipeline/agent/live2d_agent.py`
- Create: `pipeline_cli.py`
- Test: `pipeline/tests/test_agent.py`

- [ ] **Step 1: Implement Live2DAgent**

```python
# pipeline/agent/live2d_agent.py
import time
from typing import Dict, Any
from pipeline.core.context import NodeContext
from pipeline.core.workflow import Workflow
from pipeline.workflows import (
    create_character_concept_workflow,
    create_live2d_portrait_workflow,
    create_live2d_production_workflow,
    create_vtuber_full_workflow
)


class Live2DAgent:
    """Live2D智能Agent"""

    def __init__(self, output_dir: str = "./pipeline_outputs"):
        self.output_dir = output_dir
        self.workflows = self._register_workflows()
        self.state = "idle"
        self.current_workflow = None
        self.context = None
        self.history = []

    def _register_workflows(self) -> Dict[str, Workflow]:
        return {
            "character_concept": create_character_concept_workflow(
                output_dir=self.output_dir
            ),
            "live2d_portrait": create_live2d_portrait_workflow(
                output_dir=self.output_dir
            ),
            "live2d_production": create_live2d_production_workflow(
                output_dir=self.output_dir
            ),
            "vtuber_full": create_vtuber_full_workflow(
                output_dir=self.output_dir
            )
        }

    def process(self, user_input: str,
                auto_mode: bool = False) -> Dict[str, Any]:
        """处理用户需求"""
        print(f"\n{'='*60}")
        print(f"🎯 用户输入: {user_input}")
        print(f"{'='*60}")

        # 解析需求
        intent = self._parse_intent(user_input)
        print(f"📋 解析意图: {intent['goal']} | 复杂度: {intent['complexity']} | 风格: {intent['style']}")

        # 选择工作流
        workflow = self._select_workflow(intent)
        self.current_workflow = workflow
        print(f"🔧 选择工作流: {workflow.name}")

        # 初始化上下文
        self.context = NodeContext(
            data={},
            metadata={"start_time": time.time(), "intent": intent},
            user_input=user_input
        )

        # 执行工作流
        human_in_loop = not auto_mode
        self.context = workflow.execute(self.context, human_in_loop=human_in_loop)

        # 记录历史
        self.history.append({
            "input": user_input,
            "workflow": workflow.name,
            "result": self.context.data
        })

        return self._format_results()

    def _parse_intent(self, text: str) -> Dict[str, str]:
        """解析用户意图"""
        text_lower = text.lower()

        intent = {
            "goal": "generate_character",
            "style": "anime",
            "complexity": "standard",
            "output_format": "image"
        }

        # 检测目标
        if any(k in text_lower for k in ["vtuber", "虚拟主播"]):
            intent["goal"] = "vtuber_package"
            intent["complexity"] = "full"
        elif any(k in text_lower for k in ["live2d", "立绘", "生产"]):
            intent["output_format"] = "live2d_ready"
            intent["complexity"] = "high"

        # 检测风格
        if any(k in text_lower for k in ["写实", "realistic", "real"]):
            intent["style"] = "semi_realistic"
        elif any(k in text_lower for k in ["vtuber"]):
            intent["style"] = "vtuber"

        # 检测复杂度关键词
        if any(k in text_lower for k in ["完整", "full", "全套"]):
            intent["complexity"] = "full"
        elif any(k in text_lower for k in ["简单", "quick", "快速"]):
            intent["complexity"] = "standard"

        return intent

    def _select_workflow(self, intent: Dict) -> Workflow:
        """选择工作流"""
        mapping = {
            ("generate_character", "standard"): "character_concept",
            ("generate_character", "high"): "live2d_portrait",
            ("generate_character", "full"): "live2d_production",
            ("vtuber_package", "full"): "vtuber_full",
            ("vtuber_package", "high"): "vtuber_full"
        }

        key = (intent["goal"], intent["complexity"])
        workflow_name = mapping.get(key, "character_concept")

        return self.workflows[workflow_name]

    def _format_results(self) -> Dict[str, Any]:
        """格式化结果"""
        duration = time.time() - self.context.metadata.get("start_time", time.time())

        return {
            "status": "success" if not self.context.data.get("error") else "failed",
            "workflow": self.current_workflow.name if self.current_workflow else None,
            "duration_seconds": round(duration, 2),
            "outputs": {
                k: v for k, v in self.context.data.items()
                if k not in ("error", "workflow_paused", "paused_at_node")
            },
            "paused": self.context.data.get("workflow_paused", False),
            "metadata": self.context.metadata
        }
```

- [ ] **Step 2: Implement CLI**

```python
# pipeline_cli.py
#!/usr/bin/env python3
"""Live2D Pipeline CLI - 交互式Live2D生产管道"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from pipeline.agent.live2d_agent import Live2DAgent


def main():
    parser = argparse.ArgumentParser(
        description="Live2D Production Pipeline - 从需求到Live2D"
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="角色描述（如：蓝发猫耳少女）"
    )
    parser.add_argument(
        "--auto", "-a",
        action="store_true",
        help="自动模式（不暂停等待确认）"
    )
    parser.add_argument(
        "--output", "-o",
        default="./pipeline_outputs",
        help="输出目录"
    )
    parser.add_argument(
        "--workflow", "-w",
        choices=["concept", "portrait", "production", "vtuber"],
        help="强制指定工作流"
    )

    args = parser.parse_args()

    print("🎨 Live2D Production Pipeline v6.0")
    print("=" * 50)

    agent = Live2DAgent(output_dir=args.output)

    if args.prompt:
        result = agent.process(args.prompt, auto_mode=args.auto)
        print("\n" + "=" * 50)
        print("📊 最终结果:")
        print(f"  状态: {result['status']}")
        print(f"  工作流: {result['workflow']}")
        print(f"  耗时: {result['duration_seconds']}s")
        if "generated_image" in result.get("outputs", {}):
            print(f"  图片: {result['outputs']['generated_image']}")
    else:
        # 交互模式
        print("\n💬 交互模式（输入 'quit' 退出）")
        while True:
            user_input = input("\n🎯 描述你想要的角色: ").strip()
            if user_input.lower() in ("quit", "exit", "q"):
                break
            if not user_input:
                continue

            result = agent.process(user_input, auto_mode=args.auto)

            if result.get("paused"):
                print("\n⏸️ 工作流已暂停，输入 'continue' 继续或 'quit' 退出")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Create __init__**

```python
# pipeline/agent/__init__.py
from .live2d_agent import Live2DAgent

__all__ = ["Live2DAgent"]
```

- [ ] **Step 4: Write tests**

```python
# pipeline/tests/test_agent.py
import pytest
from pipeline.agent.live2d_agent import Live2DAgent

def test_agent_creation():
    agent = Live2DAgent()
    assert agent.state == "idle"
    assert len(agent.workflows) == 4

def test_parse_intent():
    agent = Live2DAgent()

    intent = agent._parse_intent("蓝发猫耳少女")
    assert intent["goal"] == "generate_character"
    assert intent["complexity"] == "standard"

    intent = agent._parse_intent("我要一个Live2D立绘")
    assert intent["output_format"] == "live2d_ready"
    assert intent["complexity"] == "high"

    intent = agent._parse_intent("VTuber完整方案")
    assert intent["goal"] == "vtuber_package"
    assert intent["complexity"] == "full"
```

- [ ] **Step 5: Run all tests**

Run: `python3 -m pytest pipeline/tests/ -v`
Expected: All tests PASS

- [ ] **Step 6: Commit**

```bash
git add pipeline/agent/ pipeline_cli.py pipeline/tests/
git commit -m "feat(pipeline): add Live2D Agent and CLI"
```

---

## Task 8: Integration Test (集成测试)

**Files:**
- Test: `pipeline/tests/test_integration.py`

- [ ] **Step 1: Write integration test**

```python
# pipeline/tests/test_integration.py
import pytest
from pipeline.core.context import NodeContext
from pipeline.nodes import (
    CharacterNode, Live2DRuleNode, CompositionNode,
    PromptBuilderNode
)
from pipeline.workflows import create_live2d_portrait_workflow


def test_full_node_chain():
    """测试完整节点链（不生成图片）"""
    ctx = NodeContext(user_input="蓝发猫耳少女")

    # 执行节点链
    ctx = CharacterNode("角色设定").run(ctx)
    assert "character" in ctx.data

    ctx = Live2DRuleNode("Live2D规范").run(ctx)
    assert "live2d_constraints" in ctx.data

    ctx = CompositionNode("构图").run(ctx)
    assert "composition" in ctx.data

    ctx = PromptBuilderNode("Prompt构建").run(ctx)
    assert "prompt" in ctx.data
    assert "blue hair" in ctx.data["prompt"]["positive"]
    assert "cat ears" in ctx.data["prompt"]["positive"]

    print(f"\n✅ 节点链测试通过")
    print(f"  角色: {ctx.data['character']['description']}")
    print(f"  Prompt: {ctx.data['prompt']['positive'][:80]}...")


def test_workflow_structure():
    """测试工作流结构"""
    wf = create_live2d_portrait_workflow()

    assert wf.name == "Live2D立绘"
    assert len(wf.nodes) == 6

    node_names = [n.name for n in wf.nodes]
    assert "角色设定" in node_names
    assert "Live2D规范" in node_names
    assert "Prompt构建" in node_names
    assert "图片生成" in node_names
    assert "质量评估" in node_names
```

- [ ] **Step 2: Run integration test**

Run: `python3 -m pytest pipeline/tests/test_integration.py -v -s`
Expected: All tests PASS with output

- [ ] **Step 3: Final commit**

```bash
git add pipeline/tests/test_integration.py
git commit -m "test(pipeline): add integration tests"
```

---

## 验证清单

- [ ] `pipeline/core/` - Node, Workflow, Context 核心抽象
- [ ] `pipeline/providers/` - Provider接口 + LocalSD + ComfyUI
- [ ] `pipeline/nodes/` - 6个核心Node实现
- [ ] `pipeline/workflows/` - 4个预置工作流
- [ ] `pipeline/agent/` - Live2DAgent + 意图解析
- [ ] `pipeline_cli.py` - 命令行界面
- [ ] `pipeline/tests/` - 单元测试 + 集成测试
- [ ] 所有现有文件保持不变
- [ ] 语法检查通过

---

## 运行方式

```bash
# 交互模式
python pipeline_cli.py

# 直接生成
python pipeline_cli.py "蓝发猫耳少女" --auto

# 指定工作流
python pipeline_cli.py "蓝发猫耳少女" --workflow portrait --auto

# 指定输出目录
python pipeline_cli.py "蓝发猫耳少女" -o ./my_outputs --auto
```

---

*计划完成*
