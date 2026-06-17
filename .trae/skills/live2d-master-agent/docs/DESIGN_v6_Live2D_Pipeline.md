# Live2D Production Pipeline v6.0 设计文档

## 文档信息

- **版本**: v6.0
- **日期**: 2026-05-30
- **状态**: 设计评审中
- **作者**: AI Assistant

---

## 1. 执行摘要

本设计文档描述将 Live2D Master Agent 从当前的命令行工具升级为**模块化生产管道（Production Pipeline）**的架构方案。核心目标是实现：

```
一句需求 → 角色规划 → Prompt生成 → 模型调用 → 质量评估 → 自动修正 → PSD规划 → Live2D生产建议
```

采用**渐进式增强**策略，在保持现有代码兼容的前提下，引入 Node Layer、Workflow Layer、Agent Layer 三层架构。

---

## 2. 现状分析

### 2.1 现有能力

| 组件 | 文件 | 状态 | 复用价值 |
|------|------|------|---------|
| 本地图片生成 | `local_image_generator.py` | v5.0 | ⭐⭐⭐⭐⭐ |
| 主控工具 | `master_tool.py` | v8.0 | ⭐⭐⭐⭐ |
| 高级管道 | `advanced_generation_pipeline.py` | v1.0 | ⭐⭐⭐⭐ |
| ComfyUI集成 | `comfyui_integration.py` | v1.0 | ⭐⭐⭐⭐⭐ |
| 质量评估 | `scripts/qa_engine_enhanced.py` | v1.0 | ⭐⭐⭐⭐⭐ |
| 参数设计 | `scripts/parameter_designer_enhanced.py` | v1.0 | ⭐⭐⭐⭐⭐ |
| 提示词工程 | [`prompts/image_generation.md`](../../../../prompts/image_generation.md) | - | ⭐⭐⭐⭐ |
| PSD结构模板 | [`templates/psd_structure.md`](../../../../templates/psd_structure.md) | - | ⭐⭐⭐⭐⭐ |
| Cubism参数模板 | [`templates/cubism_params.md`](../../../../templates/cubism_params.md) | - | ⭐⭐⭐⭐⭐ |
| Go API服务 | `api/` | v7.0 | ⭐⭐⭐⭐ |

### 2.2 现有痛点

1. **功能耦合**：生成、评估、分层逻辑分散在不同文件，缺乏统一编排
2. **人机交互**：用户需手动选择参数，无法"一句需求"自动完成
3. **质量不可控**：生成后无自动评估，不合格图片需人工筛选
4. **模型单一**：仅支持本地 SD + ComfyUI，无法利用云端高质量模型
5. **工作流缺失**：没有预置工作流，每次需手动组合功能

---

## 3. 架构设计

### 3.1 总体架构

```
┌─────────────────────────────────────────────────────────────┐
│                     Agent Layer                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Live2DAgent                                        │   │
│  │  - 需求解析 → 选择工作流 → 调度节点 → 人机交互      │   │
│  │  - 状态管理：INIT → GENERATING → REVIEW → ...      │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   Workflow Layer                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Workflow A│  │Workflow B│  │Workflow C│  │Workflow D│   │
│  │角色概念  │  │Live2D立绘│  │生产准备  │  │VTuber完整│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                    Node Layer                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │Character │ │Live2DRule│ │Composition│ │Prompt    │      │
│  │   Node   │ │   Node   │ │   Node   │ │ Builder  │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │  Image   │ │ Quality  │ │  Repair  │ │   PSD    │      │
│  │ Provider │ │  Check   │ │   Node   │ │ Planner  │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│  ┌──────────┐ ┌──────────┐                                  │
│  │ Cubism   │ │ Reference│                                  │
│  │ Planner  │ │  Style   │                                  │
│  └──────────┘ └──────────┘                                  │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 设计原则

1. **渐进式增强**：现有文件保持不变，新功能通过新增目录实现
2. **单一职责**：每个 Node 只做一件事，通过接口通信
3. **可组合性**：Workflow 由 Node 组合而成，Agent 由 Workflow 组合而成
4. **人在回路**：每步生成后暂停，用户确认后再继续（用户要求）
5. **省钱优先**：优先使用本地模型 / TRAE内置大模型，云端模型作为可选

---

## 4. Node Layer 详细设计

### 4.1 核心抽象

```python
# pipeline/core/node.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class NodeContext:
    """节点间传递的上下文"""
    data: Dict[str, Any]           # 节点输出数据
    metadata: Dict[str, Any]       # 元信息（时间戳、版本等）
    user_input: Optional[str]      # 用户原始输入
    checkpoint: Optional[str]      # 断点信息（用于恢复）

class BaseNode(ABC):
    """所有节点的基类"""
    
    def __init__(self, name: str, config: Dict = None):
        self.name = name
        self.config = config or {}
        self.state = "idle"  # idle → running → success/failed
    
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
```

### 4.2 节点清单

#### 4.2.1 Character Node

```python
# pipeline/nodes/character_node.py
class CharacterNode(BaseNode):
    """角色设定节点：将自然语言需求解析为结构化角色设定"""
    
    def execute(self, context: NodeContext) -> NodeContext:
        user_input = context.user_input
        
        # 使用 LLM 解析角色设定
        character_profile = self._parse_character(user_input)
        
        context.data["character"] = character_profile
        return self.on_success(context)
    
    def _parse_character(self, text: str) -> Dict:
        """解析为结构化角色设定"""
        return {
            "name": "",
            "age_group": "teen/young_adult/adult",
            "gender": "female/male/ambiguous",
            "hair": {"color": "", "style": "", "length": ""},
            "eyes": {"color": "", "shape": ""},
            "clothing": {"style": "", "colors": [], "details": ""},
            "personality": "",
            "style": "anime/semi_realistic/vtuber/live2d_ready",
            "pose_preference": "standing/sitting/dynamic",
            "expression": "neutral/smile/serious/cute"
        }
```

**输入**: 自然语言描述（如"我要一个蓝发猫耳少女"）
**输出**: 结构化角色设定 JSON
**依赖**: 本地 LLM（通过 TRAE 内置模型）或 OpenAI API

#### 4.2.2 Live2D Rule Node

```python
# pipeline/nodes/live2d_rule_node.py
class Live2DRuleNode(BaseNode):
    """Live2D规范约束节点：确保生成结果适合Live2D制作"""
    
    RULES = {
        "visibility": [
            "neck_visible",           # 脖子可见
            "both_shoulders_visible", # 双肩可见
            "no_excessive_occlusion"  # 无过度遮挡
        ],
        "separation": [
            "arms_separable",         # 手臂可分离
            "hair_layers_clear",      # 头发分层清晰
            "clothing_separable"      # 服装可分离
        ],
        "technical": [
            "no_transparent_clothing", # 无透明服装
            "no_complex_patterns",     # 无复杂图案
            "solid_background",        # 纯色背景
            "front_facing_or_3_4"      # 正面或3/4侧面
        ]
    }
    
    def execute(self, context: NodeContext) -> NodeContext:
        character = context.data.get("character", {})
        
        # 根据角色设定生成 Live2D 约束
        constraints = self._generate_constraints(character)
        
        context.data["live2d_constraints"] = constraints
        return self.on_success(context)
```

**输入**: 角色设定 JSON
**输出**: Live2D 约束列表（用于 Prompt 生成）

#### 4.2.3 Composition Node

```python
# pipeline/nodes/composition_node.py
class CompositionNode(BaseNode):
    """构图节点：确定镜头、视角、站姿"""
    
    COMPOSITION_TEMPLATES = {
        "portrait": {
            "camera": "medium_shot",
            "angle": "eye_level",
            "pose": "standing_front",
            "framing": "waist_up"
        },
        "full_body": {
            "camera": "full_shot", 
            "angle": "slight_high",
            "pose": "standing",
            "framing": "full_body"
        },
        "live2d_optimized": {
            "camera": "medium_shot",
            "angle": "eye_level",
            "pose": "standing_front",
            "framing": "chest_up",
            "background": "solid_white"
        }
    }
    
    def execute(self, context: NodeContext) -> NodeContext:
        character = context.data.get("character", {})
        style = character.get("style", "anime")
        
        # 选择构图模板
        composition = self._select_composition(style, character)
        
        context.data["composition"] = composition
        return self.on_success(context)
```

#### 4.2.4 Prompt Builder Node

```python
# pipeline/nodes/prompt_builder_node.py
class PromptBuilderNode(BaseNode):
    """Prompt构建节点：将结构化信息转换为AI生成提示词"""
    
    TEMPLATES = {
        "anime": "...",           # 复用 ../../../../prompts/image_generation.md
        "semi_realistic": "...",
        "vtuber": "...",
        "live2d_ready": "..."    # 复用 BEST_PRACTICES.md
    }
    
    def execute(self, context: NodeContext) -> NodeContext:
        character = context.data.get("character", {})
        constraints = context.data.get("live2d_constraints", {})
        composition = context.data.get("composition", {})
        
        # 构建正向提示词
        positive = self._build_positive_prompt(character, constraints, composition)
        
        # 构建负向提示词
        negative = self._build_negative_prompt(constraints)
        
        context.data["prompt"] = {
            "positive": positive,
            "negative": negative,
            "width": composition.get("width", 1024),
            "height": composition.get("height", 1536),
            "style": character.get("style", "anime")
        }
        return self.on_success(context)
```

**输入**: 角色设定 + Live2D约束 + 构图
**输出**: 完整的正负向提示词 + 尺寸参数

#### 4.2.5 Image Provider Node

```python
# pipeline/nodes/image_provider_node.py
class ImageProviderNode(BaseNode):
    """图片生成节点：统一接口，支持多种Provider"""
    
    def __init__(self, name: str, config: Dict = None):
        super().__init__(name, config)
        self.provider = self._init_provider()
    
    def _init_provider(self):
        provider_type = self.config.get("provider", "local")
        
        providers = {
            "local": LocalSDProvider(),      # 复用 local_image_generator.py
            "comfyui": ComfyUIProvider(),    # 复用 comfyui_integration.py
            "seedream": SeedreamProvider(),  # 新增（API调用）
            "flux": FluxProvider(),          # 新增（本地/API）
            "gpt_image": GPTImageProvider()  # 新增（OpenAI API）
        }
        
        return providers.get(provider_type, providers["local"])
    
    def execute(self, context: NodeContext) -> NodeContext:
        prompt = context.data.get("prompt", {})
        
        # 调用Provider生成图片
        image_path = self.provider.generate(
            prompt=prompt["positive"],
            negative_prompt=prompt["negative"],
            width=prompt["width"],
            height=prompt["height"]
        )
        
        context.data["generated_image"] = image_path
        return self.on_success(context)
```

**Provider 接口设计**:

```python
# pipeline/providers/base_provider.py
class BaseImageProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, negative_prompt: str, 
                 width: int, height: int, **kwargs) -> str:
        """生成图片，返回图片路径"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查Provider是否可用"""
        pass
    
    @property
    @abstractmethod
    def cost_estimate(self) -> float:
        """预估成本（用于路由决策）"""
        pass
```

#### 4.2.6 Quality Check Node

```python
# pipeline/nodes/quality_check_node.py
class QualityCheckNode(BaseNode):
    """质量评估节点：全面评估图片是否适合Live2D"""
    
    DIMENSIONS = {
        "face_quality": {
            "weight": 0.25,
            "checks": ["symmetry", "clarity", "proportion"]
        },
        "hand_detection": {
            "weight": 0.15,
            "checks": ["presence", "finger_count", "pose_normality"]
        },
        "live2d_adaptability": {
            "weight": 0.30,
            "checks": ["edge_clarity", "background_purity", "color_separation"]
        },
        "perspective_consistency": {
            "weight": 0.15,
            "checks": ["body_alignment", "proportion_consistency"]
        },
        "occlusion_analysis": {
            "weight": 0.15,
            "checks": ["self_occlusion", "layer_separability"]
        }
    }
    
    def execute(self, context: NodeContext) -> NodeContext:
        image_path = context.data.get("generated_image")
        
        # 运行所有评估维度
        scores = {}
        for dimension, config in self.DIMENSIONS.items():
            scores[dimension] = self._evaluate_dimension(image_path, dimension)
        
        # 计算综合评分
        overall = sum(
            scores[d] * config["weight"] 
            for d, config in self.DIMENSIONS.items()
        )
        
        context.data["quality_report"] = {
            "overall_score": overall,
            "dimension_scores": scores,
            "is_acceptable": overall >= self.config.get("threshold", 70),
            "suggestions": self._generate_suggestions(scores)
        }
        return self.on_success(context)
```

**评估技术参考**:
- 脸部质量：使用 OpenCV DNN 人脸检测 + 对称性分析
- 手部检测：使用 MediaPipe Hands 或 YOLOv8-pose
- Live2D适配度：边缘检测（Canny）+ 背景均匀度分析 + 颜色量化
- 透视一致性：人体关键点检测 + 比例分析
- 遮挡分析：实例分割（SAM）+ 层级关系推断

#### 4.2.7 Repair Node

```python
# pipeline/nodes/repair_node.py
class RepairNode(BaseNode):
    """修复节点：根据质量报告自动修正"""
    
    MAX_RETRIES = 3
    
    def execute(self, context: NodeContext) -> NodeContext:
        quality_report = context.data.get("quality_report", {})
        
        if quality_report.get("is_acceptable", False):
            context.data["repaired"] = False
            return self.on_success(context)
        
        # 自动修复策略
        for attempt in range(self.MAX_RETRIES):
            strategy = self._select_repair_strategy(quality_report)
            
            if strategy == "prompt_rebuild":
                context = self._rebuild_prompt(context)
            elif strategy == "regenerate":
                context = self._regenerate(context)
            elif strategy == "inpaint":
                context = self._inpaint_repair(context)
            
            # 重新评估
            # ... 调用 QualityCheckNode
            
            if context.data.get("quality_report", {}).get("is_acceptable"):
                context.data["repaired"] = True
                context.data["repair_attempts"] = attempt + 1
                return self.on_success(context)
        
        # 修复失败
        context.data["repaired"] = False
        context.data["repair_failed"] = True
        return self.on_success(context)  # 仍返回，让用户决定
    
    def _select_repair_strategy(self, report: Dict) -> str:
        """根据质量报告选择修复策略"""
        scores = report.get("dimension_scores", {})
        
        if scores.get("face_quality", 100) < 50:
            return "prompt_rebuild"  # 脸部问题 → 重构Prompt
        elif scores.get("live2d_adaptability", 100) < 50:
            return "regenerate"      # 整体不适配 → 重新生成
        elif scores.get("hand_detection", 100) < 50:
            return "inpaint"         # 手部问题 → 局部重绘
        else:
            return "prompt_rebuild"
```

#### 4.2.8 PSD Planner Node

```python
# pipeline/nodes/psd_planner_node.py
class PSDPlannerNode(BaseNode):
    """PSD规划节点：预测分层结构"""
    
    LAYER_HIERARCHY = {
        "hair_back": {"z_index": 0, "parts": ["hair_back"]},
        "body": {"z_index": 1, "parts": ["body", "clothes"]},
        "face": {"z_index": 2, "parts": ["face_base"]},
        "eyes": {"z_index": 3, "parts": ["eye_left", "eye_right"]},
        "mouth": {"z_index": 4, "parts": ["mouth"]},
        "hair_front": {"z_index": 5, "parts": ["hair_front", "hair_side"]},
        "accessories": {"z_index": 6, "parts": ["accessories"]}
    }
    
    def execute(self, context: NodeContext) -> NodeContext:
        image_path = context.data.get("generated_image")
        character = context.data.get("character", {})
        
        # 分析图片，预测分层
        layer_plan = self._analyze_for_layers(image_path, character)
        
        context.data["psd_plan"] = layer_plan
        return self.on_success(context)
    
    def _analyze_for_layers(self, image_path: str, character: Dict) -> Dict:
        """分析图片并生成分层建议"""
        # 复用 live2d_layer_pro.py 的分层逻辑
        # 结合角色设定优化分层策略
        return {
            "layers": self.LAYER_HIERARCHY,
            "estimated_complexity": "medium",
            "special_notes": [],
            "color_regions": {}  # 各区域主色调
        }
```

#### 4.2.9 Cubism Planner Node

```python
# pipeline/nodes/cubism_planner_node.py
class CubismPlannerNode(BaseNode):
    """Cubism参数规划节点：生成Live2D参数建议"""
    
    def execute(self, context: NodeContext) -> NodeContext:
        character = context.data.get("character", {})
        psd_plan = context.data.get("psd_plan", {})
        
        # 生成参数建议
        params = self._generate_cubism_params(character, psd_plan)
        
        context.data["cubism_params"] = params
        return self.on_success(context)
    
    def _generate_cubism_params(self, character: Dict, psd_plan: Dict) -> Dict:
        """生成Cubism参数配置"""
        # 复用 scripts/parameter_designer_enhanced.py
        return {
            "parameters": {
                "AngleX": {"range": [-30, 30], "importance": "high"},
                "AngleY": {"range": [-30, 30], "importance": "high"},
                "AngleZ": {"range": [-30, 30], "importance": "medium"},
                "BodyX": {"range": [-10, 10], "importance": "medium"},
                "EyeOpen": {"range": [0, 1], "importance": "high"},
                "MouthOpen": {"range": [0, 1], "importance": "high"}
            },
            "physics": {
                "hair": {"strength": 0.5, "damping": 0.7},
                "accessories": {"strength": 0.3, "damping": 0.8}
            },
            "expressions": ["neutral", "smile", "surprised", "sad"]
        }
```

#### 4.2.10 Reference Style Node（已有，复用）

复用现有的 `ReferenceStyleAnalyzer` 类，包装为 Node 接口。

---

## 5. Workflow Layer 详细设计

### 5.1 工作流抽象

```python
# pipeline/core/workflow.py
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
        for i, node in enumerate(self.nodes):
            print(f"\n{'='*50}")
            print(f"步骤 {i+1}/{len(self.nodes)}: {node.name}")
            print(f"{'='*50}")
            
            # 执行节点
            context = node.execute(context)
            
            # 人在回路：暂停等待用户确认
            if human_in_loop and i < len(self.nodes) - 1:
                should_continue = self._pause_for_review(context, node.name)
                if not should_continue:
                    print("⏸️ 用户暂停工作流")
                    context.data["workflow_paused"] = True
                    context.data["paused_at_node"] = node.name
                    return context
        
        self.state = "completed"
        return context
    
    def _pause_for_review(self, context: NodeContext, node_name: str) -> bool:
        """暂停等待用户确认"""
        # 显示当前结果
        self._display_results(context, node_name)
        
        # 等待用户输入（CLI交互）
        user_input = input("\n🔄 继续下一步? [Y/n/modify]: ").strip().lower()
        
        if user_input in ("", "y", "yes"):
            return True
        elif user_input == "n":
            return False
        elif user_input == "modify":
            context = self._handle_modification(context, node_name)
            return True
        return True
```

### 5.2 预置工作流

#### 5.2.1 Workflow A: 角色概念生成

```python
# pipeline/workflows/character_concept.py
def create_character_concept_workflow() -> Workflow:
    """角色概念生成工作流"""
    return (
        Workflow("角色概念", "快速生成角色概念图")
        .add_node(CharacterNode("角色设定"))
        .add_node(CompositionNode("构图"))
        .add_node(PromptBuilderNode("Prompt构建"))
        .add_node(ImageProviderNode("图片生成", {"provider": "local"}))
    )
```

**流程**: Character → Composition → Prompt Builder → Image Provider

#### 5.2.2 Workflow B: Live2D立绘生成

```python
# pipeline/workflows/live2d_portrait.py
def create_live2d_portrait_workflow() -> Workflow:
    """Live2D立绘生成工作流"""
    return (
        Workflow("Live2D立绘", "生成适合Live2D的立绘")
        .add_node(CharacterNode("角色设定"))
        .add_node(Live2DRuleNode("Live2D规范"))
        .add_node(CompositionNode("构图"))
        .add_node(PromptBuilderNode("Prompt构建"))
        .add_node(ImageProviderNode("图片生成"))
        .add_node(QualityCheckNode("质量评估"))
    )
```

**流程**: Character → Live2D Rules → Composition → Prompt Builder → Image Provider → Quality Check

#### 5.2.3 Workflow C: Live2D生产准备

```python
# pipeline/workflows/live2d_production.py
def create_live2d_production_workflow() -> Workflow:
    """Live2D生产准备工作流"""
    return (
        Workflow("Live2D生产", "完整的Live2D生产准备")
        .add_node(CharacterNode("角色设定"))
        .add_node(Live2DRuleNode("Live2D规范"))
        .add_node(CompositionNode("构图"))
        .add_node(PromptBuilderNode("Prompt构建"))
        .add_node(ImageProviderNode("图片生成"))
        .add_node(QualityCheckNode("质量评估"))
        .add_node(RepairNode("自动修复"))
        .add_node(PSDPlannerNode("PSD规划"))
        .add_node(CubismPlannerNode("Cubism规划"))
    )
```

**流程**: Character → Live2D Rules → Composition → Prompt Builder → Image Provider → Quality Check → Repair → PSD Planner → Cubism Planner

#### 5.2.4 Workflow D: VTuber完整方案

```python
# pipeline/workflows/vtuber_full.py
def create_vtuber_full_workflow() -> Workflow:
    """VTuber完整方案工作流"""
    return (
        Workflow("VTuber完整方案", "从需求到Live2D的完整方案")
        .add_node(CharacterNode("角色设定"))
        .add_node(PromptBuilderNode("Prompt构建"))
        .add_node(ImageProviderNode("概念图生成"))
        .add_node(PSDPlannerNode("PSD规划"))
        .add_node(RepairNode("修正规划"))
        .add_node(CubismPlannerNode("Cubism规划"))
    )
```

---

## 6. Agent Layer 详细设计

### 6.1 Live2D Agent

```python
# pipeline/agent/live2d_agent.py
class Live2DAgent:
    """Live2D智能Agent：自动解析需求并编排工作流"""
    
    def __init__(self):
        self.workflows = self._register_workflows()
        self.state = "idle"
        self.current_workflow = None
        self.context = None
    
    def _register_workflows(self) -> Dict[str, Workflow]:
        return {
            "character_concept": create_character_concept_workflow(),
            "live2d_portrait": create_live2d_portrait_workflow(),
            "live2d_production": create_live2d_production_workflow(),
            "vtuber_full": create_vtuber_full_workflow()
        }
    
    def process(self, user_input: str) -> Dict:
        """处理用户需求"""
        print(f"🎯 用户输入: {user_input}")
        
        # 步骤1: 解析需求
        intent = self._parse_intent(user_input)
        print(f"📋 解析意图: {intent}")
        
        # 步骤2: 选择工作流
        workflow = self._select_workflow(intent)
        print(f"🔧 选择工作流: {workflow.name}")
        
        # 步骤3: 初始化上下文
        self.context = NodeContext(
            data={},
            metadata={"start_time": time.time()},
            user_input=user_input
        )
        
        # 步骤4: 执行工作流（人在回路）
        self.context = workflow.execute(self.context, human_in_loop=True)
        
        # 步骤5: 返回结果
        return self._format_results()
    
    def _parse_intent(self, text: str) -> Dict:
        """使用LLM解析用户意图"""
        # 简化的关键词匹配（实际使用LLM）
        intent = {
            "goal": "generate_character",
            "style": "anime",
            "complexity": "standard",
            "output_format": "image"
        }
        
        if "live2d" in text.lower() or "立绘" in text:
            intent["output_format"] = "live2d_ready"
            intent["complexity"] = "high"
        
        if "vtuber" in text.lower():
            intent["output_format"] = "vtuber_package"
            intent["complexity"] = "full"
        
        return intent
    
    def _select_workflow(self, intent: Dict) -> Workflow:
        """根据意图选择工作流"""
        mapping = {
            ("generate_character", "standard"): "character_concept",
            ("generate_character", "high"): "live2d_portrait",
            ("generate_character", "full"): "live2d_production",
            ("vtuber_package", "full"): "vtuber_full"
        }
        
        key = (intent["goal"], intent["complexity"])
        workflow_name = mapping.get(key, "character_concept")
        
        return self.workflows[workflow_name]
    
    def _format_results(self) -> Dict:
        """格式化最终结果"""
        return {
            "status": "success",
            "workflow": self.current_workflow.name if self.current_workflow else None,
            "outputs": self.context.data,
            "metadata": self.context.metadata
        }
```

---

## 7. Provider Router 设计

### 7.1 Provider 注册表

```python
# pipeline/providers/registry.py
class ProviderRegistry:
    """Provider注册表：管理所有可用的图片生成Provider"""
    
    def __init__(self):
        self.providers: Dict[str, BaseImageProvider] = {}
        self._register_defaults()
    
    def _register_defaults(self):
        """注册默认Provider"""
        self.register("local", LocalSDProvider())
        self.register("comfyui", ComfyUIProvider())
        self.register("seedream", SeedreamProvider())
        self.register("flux", FluxProvider())
    
    def register(self, name: str, provider: BaseImageProvider):
        self.providers[name] = provider
    
    def get_available(self) -> List[str]:
        """获取所有可用的Provider"""
        return [name for name, p in self.providers.items() if p.is_available()]
    
    def select(self, criteria: Dict) -> BaseImageProvider:
        """根据条件选择最优Provider"""
        available = self.get_available()
        
        # 选择策略
        style = criteria.get("style", "anime")
        quality = criteria.get("quality", "standard")
        budget = criteria.get("budget", "low")
        
        # 路由规则
        if budget == "low":
            return self.providers.get("local") or self.providers.get("comfyui")
        
        if style == "anime" and "seedream" in available:
            return self.providers["seedream"]
        
        if quality == "highest" and "flux" in available:
            return self.providers["flux"]
        
        return self.providers.get("local")
```

### 7.2 Provider 实现

| Provider | 类型 | 成本 | 质量 | 适用场景 |
|----------|------|------|------|---------|
| local | 本地 | 免费 | 中等 | 快速迭代、草稿 |
| comfyui | 本地 | 免费 | 高 | 复杂工作流、精细控制 |
| seedream | API | 低 | 高 | 动漫风格、最终产出 |
| flux | 本地/API | 中 | 最高 | 写实风格、商业级 |
| gpt_image | API | 高 | 最高 | 特殊需求、快速原型 |

---

## 8. 升级路线

### V1: Prompt增强 + 基础Pipeline（当前阶段）

**目标**: 建立基础架构，实现 Workflow B

**任务**:
1. 创建 `pipeline/` 目录结构
2. 实现 BaseNode、Workflow、Agent 核心抽象
3. 实现 CharacterNode、Live2DRuleNode、PromptBuilderNode
4. 包装现有生成逻辑为 ImageProviderNode
5. 实现 Workflow B（Live2D立绘生成）
6. 更新 CLI 支持新工作流

**预计工作量**: 2-3 天

### V2: 质量评估 + 自动修复

**目标**: 实现 QualityCheckNode 和 RepairNode

**任务**:
1. 实现脸部质量评估（OpenCV DNN）
2. 实现手部检测（MediaPipe）
3. 实现 Live2D 适配度评估
4. 实现自动修复策略
5. 集成到 Workflow C

**预计工作量**: 3-4 天

### V3: 多模型路由

**目标**: 实现 Provider Router，支持云端模型

**任务**:
1. 实现 Seedream Provider
2. 实现 Flux Provider
3. 实现 Provider 自动选择逻辑
4. 添加成本估算和预算控制

**预计工作量**: 2-3 天

### V4: PSD规划 + Cubism规划

**目标**: 实现完整的生产准备工作流

**任务**:
1. 包装现有分层工具为 PSDPlannerNode
2. 包装参数设计工具为 CubismPlannerNode
3. 实现 Workflow C 和 D
4. 添加导出功能（PSD、JSON）

**预计工作量**: 2-3 天

### V5: 完整Agent

**目标**: 实现自然语言驱动的全自动流程

**任务**:
1. 实现需求解析 LLM
2. 实现工作流自动选择
3. 实现上下文记忆
4. 实现结果展示和导出

**预计工作量**: 3-4 天

---

## 9. 目录结构

```
live2d-master-agent/
├── pipeline/                          # 新增：核心管道框架
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── node.py                    # BaseNode 抽象
│   │   ├── workflow.py                # Workflow 类
│   │   └── context.py                 # NodeContext
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── character_node.py          # 角色设定
│   │   ├── live2d_rule_node.py        # Live2D规范
│   │   ├── composition_node.py        # 构图
│   │   ├── prompt_builder_node.py     # Prompt构建
│   │   ├── image_provider_node.py     # 图片生成
│   │   ├── quality_check_node.py      # 质量评估
│   │   ├── repair_node.py             # 自动修复
│   │   ├── psd_planner_node.py        # PSD规划
│   │   ├── cubism_planner_node.py     # Cubism规划
│   │   └── reference_style_node.py    # 参考图风格
│   ├── workflows/
│   │   ├── __init__.py
│   │   ├── character_concept.py       # Workflow A
│   │   ├── live2d_portrait.py         # Workflow B
│   │   ├── live2d_production.py       # Workflow C
│   │   └── vtuber_full.py             # Workflow D
│   ├── agent/
│   │   ├── __init__.py
│   │   └── live2d_agent.py            # Live2DAgent
│   └── providers/
│       ├── __init__.py
│       ├── base_provider.py           # Provider接口
│       ├── registry.py                # Provider注册表
│       ├── local_sd_provider.py       # 本地SD
│       ├── comfyui_provider.py        # ComfyUI
│       ├── seedream_provider.py       # Seedream API
│       └── flux_provider.py           # FLUX
│
├── 现有文件保持不变...
│
└── docs/
    └── DESIGN_v6_Live2D_Pipeline.md   # 本设计文档
```

---

## 10. 风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| 质量评估准确性不足 | 中 | 高 | 结合传统CV + CLIP + 规则，逐步迭代 |
| LLM解析不稳定 | 中 | 中 | 添加关键词回退，支持手动修正 |
| 云端API成本 | 低 | 中 | 默认使用本地模型，API作为可选 |
| 性能问题 | 低 | 中 | 节点懒加载，缓存中间结果 |
| 代码复杂度增长 | 中 | 低 | 保持模块化，单一职责 |

---

## 11. 成功标准

1. **功能**: 用户输入"我要一个蓝发猫耳少女"，系统自动完成角色设定→Prompt生成→图片生成→质量评估→输出结果
2. **质量**: 生成的图片 Live2D 适配度评分 >= 70
3. **体验**: 每步生成后暂停，用户可确认或修改
4. **成本**: 默认使用免费/低成本Provider
5. **扩展**: 新增 Provider 或 Node 无需修改核心代码

---

*文档结束*
