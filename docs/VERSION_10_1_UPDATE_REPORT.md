# Live2D Master Agent v10.1 补丁版更新报告

> 版本：v10.1.0（v10.0 的补丁迭代，非大版本重构）
> 日期：2026-08-06
> 依据：实跑全链路 + 静态接口审查 + ADR 与架构文档中明确标注的"下个迭代（v10.1）待落地项"
> 原则：**不新增 Roadmap 中的 v11/v12 功能，不改 18 层顺序（ADR-003 单向门），不改三栈架构（ADR-002）**

---

## 一、为什么出 v10.1 而不是 v11

v10.0 的核心代码（17 个核心模块、平均 380 行/文件）**已经写完了**——网格生成、UV 展开、骨骼绑定、变形器、28 参数、28 表情、物理配置、texture atlas 烘焙、model3.json 导出、Cubism 兼容性校验全部是真实现，0 个 `NotImplementedError`，0 个 TODO 占位。

**问题不是"没实现"，而是"接口对不上，全链路跑不通"**。通过沙箱实跑（Python 3.14 + KMeans/语义双路径）确认：只要修掉 3 个 P0 级接口错位 + 2 个安装 BUG，主链路就能从头跑到尾，导出的 model3.json 能通过 Cubism 4 的 schema 校验（28 参数、28 表情、physics3.json、texture atlas 全部齐全）。

这正是一次**补丁版**该做的事：接通已写好的模块，落地架构文档中明确要求但"待补"的 7 条 Fitness Function 和 2 个契约测试。

---

## 二、v10.0 实跑诊断（按链路顺序）

### 2.1 实跑环境

- Python 3.14.4（当前最新稳定版）
- 测试图片：1024×1024 简笔角色（模拟用户生成结果）
- 两条路径各跑一遍：① KMeans 分层（`--no-semantic`）② 语义分割（默认）

### 2.2 实跑发现的 P0 级 BUG（必导致流水线中断）

| # | 位置 | 现象 | 根因 | 影响面 |
|---|------|------|------|--------|
| **P0-1** | [workflow.py:299](file:///workspace/core/workflow.py#L299) | `AttributeError: 'SemanticSegmenter' object has no attribute 'layer'` | `SemanticLayerer = SemanticSegmenter`（[semantic.py:729](file:///workspace/core/segment_engine/semantic.py#L729)）只定义了 `.segment()` 返回 `Dict[str, np.ndarray]`（mask 字典），workflow 却调用 `.layer(img)` 并期望返回 `{layers:[...], output_dir, layer_count, method, ...}` 结构 | **默认配置直接崩溃**——因为 `use_semantic_segmentation=True` 是默认值，所有用户第一次跑都会在这里炸 |
| **P0-2** | [workflow.py:343](file:///workspace/core/workflow.py#L343) | rigging 成功后 `KeyError: 'texture'` | `RiggingPipeline.run()` → `Live2DBuilder.build()` → `Model3Exporter.export()` 返回的键是 `textures`（复数，`List[str]`），workflow 写成了 `"texture": rig_result["texture"]`（单数） | 即使 KMeans 路径绕过 P0-1，rigging 完成后仍在这一步炸，导致 PSD 导出、52 层配置、桌宠打包全部中断 |
| **P0-3** | [workflow.py:375-398](file:///workspace/core/workflow.py#L375-L398) | `export_live2d=True` 时导出空模型（69 字节纹理、2 字节 meshes.json） | 代码把 `export_layers: OrderedDict[str, PIL.Image]` 直接传给 `Model3Exporter.export(builder_result, ...)`，但 export() 期望第一个参数是 `Live2DBuilder.build()` 的完整输出字典（含 meshes/uvs/bones/deformers）。实际上 **Step 4b (rigging) 已经正确调用了 builder.build() 并导出了 model3.json**，Step 6b 是冗余且参数错误的重复调用 | 用户看到两个输出目录，其中一个是空壳模型，容易误以为是"生成的模型不能用" |

### 2.3 实跑发现的 P1 级 BUG（功能受损但不崩溃）

| # | 位置 | 现象 | 根因 |
|---|------|------|------|
| **P1-1** | install.py | Python 3.14 下安装 `psd-tools==1.9.29` 失败 | install.py 锁死了 1.9.29，该版本缺少 Cython 文件无法在 3.14 编译；`psd-tools>=1.16`（实测 1.17.4）有 3.14 预编译 wheel；requirements.txt 已经正确写了 `>=1.9.0`，是 install.py 的硬锁与 requirements 不一致 |
| **P1-2** | 安装文档 / install.py | `triangle` 包在 3.14 编译失败 | 项目实际使用的是 `scipy.spatial.Delaunay`（[generator.py:19](file:///workspace/live2d_builder/mesh/generator.py#L19)），根本不需要 `triangle` 这个 C 库；但它出现在安装依赖链里，安装时会报错 |
| **P1-3** | [workflow.py:109](file:///workspace/core/workflow.py#L109) | `LayerComposer` 实例化了但从未调用 | `self.layer_composer = LayerComposer()` 创建了对象，但 run() 方法里完全没用过；LayerComposer 本应是语义分割 mask → 可绑定图层图像的桥接器，缺失导致语义路径即使修好 P0-1 也缺少"mask 合成 RGBA 图层"这一步 |
| **P1-4** | SemanticSegmenter 后端 | "No ISNet backend available; using HSV color fallback" | ISNet 模型权重未随安装脚本下载（`install_models.py` 可选），语义分割回退到 HSV 颜色聚类，导致分割质量等同于 KMeans 甚至更差；这是"可用但效果打折"，不是崩溃 |

### 2.4 P2 级质量问题（不影响功能但影响体验，v10.1 顺手修）

| # | 问题 | 位置 |
|---|------|------|
| P2-1 | Texture atlas 利用率 ~25%，9 个图层独占 9 张贴图 | [pipeline.py:264](file:///workspace/live2d_builder/pipeline.py#L264) UV packer 给每个 mesh 单独分页，未做多 mesh 合批 |
| P2-2 | 52 层标准映射只有 9/52（KMeans）或 8/52（HSV 回退）命中 | [layers52.py:242](file:///workspace/core/segment_engine/layers52.py#L242) 启发式匹配对无意义的颜色聚簇层无法映射 |
| P2-3 | 注释写"32-bone hierarchy"但 ADR-003 定义 36 骨骼 | [pipeline.py:271](file:///workspace/live2d_builder/pipeline.py#L271) 注释与 ADR 不一致（代码实际由 [bones.py](file:///workspace/live2d_builder/rig/bones.py) 决定，需确认骨骼数并更新注释） |
| P2-4 | 桌宠驱动（`_create_pet`）传 `layers_output` 给 `DesktopPetAnimator`，但桌宠实际期望的是包含 KMeans 导出的 layer_*.png 的目录——rigging 输出目录和 layers 目录不是同一个 | [workflow.py:402](file:///workspace/core/workflow.py#L402) |

### 2.5 已验证通过的模块（证明不是"没写完"）

以下模块在沙箱实跑中**全部通过**，产出物符合预期：

- ✅ QA 引擎：评分、问题检测、severity 分级（65/100，正确识别出尺寸/清晰度警告）
- ✅ 图像优化：背景去除、对比度增强、锐化、轻度量化
- ✅ KMeans 分层：k=12，实际产出 9 个非空层 + preview.png，输出格式与下游完全对齐
- ✅ Delaunay 网格生成：9/9 层成功生成三角网格
- ✅ UV 展开：9 个 mesh 全部打包（虽然利用率低，但结构正确）
- ✅ 骨骼层级构建（KMeans 路径 6 骨、语义路径 11 骨）
- ✅ 变形器：语义路径识别到 hair 层时自动创建 2 个 warp deformer
- ✅ 28 参数配置、28 表情生成
- ✅ 物理系统：头发/身体/呼吸物理正确构建
- ✅ Texture 烘焙：9 张 baked 纹理正确输出
- ✅ model3.json 导出：Version 3，FileReferences/Textures/Physics/Expressions/Groups/HitAreas 结构完整
- ✅ 模型校验：model3.json + physics3.json + 28 个 exp3.json 全部通过 schema 校验
- ✅ PSD 导出：9 层 PSD 正常生成
- ✅ 52 层配置：4 个配置文件（layer_mapping.json、parameters、physics、guide）正确写出

---

## 三、v10.1 修复范围

### 3.1 P0 修复（主链路接通，必做）

#### Fix-1：SemanticLayerer 补全 `.layer()` 适配器方法

**文件**：[semantic.py](file:///workspace/core/segment_engine/semantic.py)

**方案**：在 `SemanticSegmenter` 类上新增 `layer(self, image, output_dir=None)` 方法，内部调用 `self.segment(image)` 获取 mask 字典，然后：

1. 按 ADR-003 的 18 层标准顺序过滤有效 mask
2. 将每个 mask 与原图合成 RGBA 图层（透明背景 + mask 作为 alpha）
3. 保存为独立 PNG 到 `output_dir`（命名 `layer_NN_partname.png`，与 KMeans 输出一致）
4. 生成 preview.png（合成预览）
5. 返回与 `KMeansLayerer.layer()` **完全相同结构**的 dict：
   ```python
   {
       "success": True,
       "method": "semantic",   # isnet 可用时；HSV 回退时为 "semantic_hsv_fallback"
       "layers": [{"index", "name", "path", "size", "pixel_count"}, ...],
       "layer_count": N,
       "output_dir": str,
       "preview_path": str,
       "composite_preview": str,
       "k_clusters": 0,
       "segmentation_mask": None,
   }
   ```
6. ISNet 模型不可用时，维持现有 HSV fallback 逻辑，但也要包装成上述统一格式返回

**验收**：`python -m core.workflow "anime girl" --semantic` 不崩溃，layers 目录中文件能被 PSDCreator 和 RiggingPipeline 正常读取。

#### Fix-2：修正 rig_result 键名 `"texture"` → `"textures"`

**文件**：[workflow.py:340-344](file:///workspace/core/workflow.py#L340-L344)

**方案**：
```python
result["steps"]["rigging"] = {
    "output_dir": rig_output,
    "model3_json": rig_result["model3_json"],
    "textures": rig_result.get("textures", []),   # 修复：复数，列表
    "texture": rig_result.get("textures", [""])[0] if rig_result.get("textures") else "",  # 向后兼容保留单数
}
```

**验收**：KMeans 路径跑完 rigging 后不再抛 KeyError，PSD/52 层步骤正常执行。

#### Fix-3：删除/修复 Step 6b 冗余的 live2d_export

**文件**：[workflow.py:375-398](file:///workspace/core/workflow.py#L375-L398)

**方案**：Step 4b（rigging）已经通过 `RiggingPipeline.run()` → `Live2DBuilder.build()` → `Model3Exporter.export()` 完整导出了 model3.json + textures + physics + expressions + meshes + guide。Step 6b 是重复且参数错传的代码——它传 raw layers 而不是 builder_result。

**处理方式**：删除 Step 6b 整个 `if self.export_live2d:` 块，把 `export_live2d` 参数改为控制 Step 4b 是否执行（目前 Step 4b 由 `generate_52_config` 控制，逻辑有交叉）。

**新的参数语义**：
- `generate_52_config=True`：执行 Step 4b（rigging）+ Step 6（52 层配置）
- `export_live2d=True`：隐式触发 rigging（如果尚未执行），并将结果路径加入最终 result
- 两者不再导出两份空模型

### 3.2 P1 修复（质量与兼容性）

#### Fix-4：安装脚本 psd-tools 版本锁放宽

**文件**：install.py

**方案**：将硬锁 `psd-tools==1.9.29` 改为 `psd-tools>=1.9.0`（与 requirements.txt 一致），安装时优先装最新版；若 1.9.x 在某个 Python 版本下编译失败，自动 fallback 到 `psd-tools>=1.16`（有预编译 wheel 的版本）。

#### Fix-5：移除 `triangle` 依赖

**文件**：install.py、requirements.txt（如果列了）

**方案**：网格生成使用 `scipy.spatial.Delaunay`，不需要 `triangle` C 库。从所有安装入口移除 `triangle`。

#### Fix-6：补全 LayerComposer 在语义路径中的调用

**文件**：[workflow.py:297-306](file:///workspace/core/workflow.py#L297-L306)

**方案**：在语义分割得到 mask 字典后、写入图层 PNG 前，调用 `self.layer_composer.compose(masks, optimized_img)` 执行：
- Amodal 补全（对 ADR-003 定义的 5 个部位：hair_back、hair_mid、clothes_top、clothes_inner、neck）
- 边缘抗锯齿
- 颜色连续性保障（对接 FF-3 ΔE ≤ 15）

这是把 LayerComposer 从"实例化了但没调用"变成"真正参与管线"。

#### Fix-7：ISNet 模型权重自动下载提示

**文件**：semantic.py `__init__`

**方案**：当检测到 ISNet backend 不可用时，在 WARNING 日志中给出明确提示：
```
WARNING  ISNet model weights not found. To enable high-quality semantic segmentation, run:
         python scripts/download_models.py --isnet
         Falling back to HSV color segmentation (quality = KMeans equivalent).
```
避免用户误以为"语义分割开了但没效果"。

### 3.3 P2 修复（注释、小问题）

- **P2-3**：确认 [bones.py](file:///workspace/live2d_builder/rig/bones.py) 实际骨骼数（读代码验证），将 pipeline.py:271 注释改为正确数字
- **P2-4**：桌宠 `_create_pet` 传参核查——确保传给 DesktopPetAnimator 的目录包含 layer_*.png
- **P2-1**：UV atlas 合批——修改 UV packer 配置，允许多个 mesh 打到同一张 atlas（目标 ≤4 张贴图，利用率 ≥ 60%），这是 v10.1 内可做的优化，不改数据结构
- **P2-2**：在语义分割路径下，52 层映射利用分割出的 part_name（如 hair_back、face、eyes 等）直接映射到标准层 ID，而不是走颜色启发式

### 3.4 Fitness Functions 落地（架构文档明确要求 v10.1 完成）

架构文档 [index.md:221](file:///workspace/docs/architecture/index.md#L221) 明确点名：

> FF-1、FF-4、FF-5、FF-7、FF-8、FF-10、FF-16 共 7 条 Fitness Functions 当前仍以"待补测试"存在，需在下个迭代（v10.1）前全部以 CI 可执行脚本形式落地；否则等于腐化没有报警。

| FF ID | 名称 | 落地形式 | 验收方式 |
|-------|------|----------|----------|
| FF-1 | 三栈依赖方向正确性 | `scripts/lint_architecture.py` | AST/import 扫描：Python 不 import Go/TS 包；Go 不 import Python 源码；前端不读磁盘；反向依赖 0 容忍 |
| FF-4 | Go API p95 延迟 | `api/` benchmark 测试 | `/api/health`、`/api/character/list` 元接口 p95 ≤ 80ms |
| FF-5 | 端到端面捕 p95 延迟 | 延迟 budget 单测 | 摄像头帧→ParamAngleX 更新 p95 ≤ 75ms |
| FF-8 | LLM Provider 降级成功率 | Fallback 集成测试 | 人为注入 503/429，Router 切下一级成功率 100% |
| FF-10 | 桌宠 60fps 稳定度 | `pet.py` perf counter | 5 分钟窗口 fps<58 的秒数 ≤ 5 秒 |
| FF-15 | License 与署名完整性 | `scripts/check-license-bundle.sh` | 产物中 MIT License 全文与根目录 LICENSE 逐字节一致 |
| FF-16 | Go→Python 命令注入安全 | `services/python_bridge_test.go` | 路径/参数污染用例 0 逃逸 |

### 3.5 契约测试落地（ADR-003 明确要求 v10.1 完成）

| 测试文件 | 目的 | 验收阈值 |
|----------|------|----------|
| `tests/unit/test_layer_order_contract.py` | 18 层顺序契约 | `STANDARD_LAYER_ORDER`、PSD 写出顺序、model3 `renderOrder` 三者 1:1 严格一致，错层 0 容忍 |
| `tests/integration/test_tearing.py` | 动作撕裂自动回归 | ParamAngleX=±30° 时脸部/脖子混合 Alpha 空洞像素占比 ≤ 0.5% |

---

## 四、不做什么（v10.1 明确不纳入）

以下内容**全部属于 v11/v12 Roadmap**（ADR-007 ComfyUI、ADR-008 全身 VRM、ADR-009 换装），v10.1 不动：

- ❌ 全身 56 骨骼（ADR-008 v12 范围）
- ❌ MMDEngine / MMD 整合
- ❌ Spine 2D 动画 IK
- ❌ See-through Phase 2/3
- ❌ ComfyUI 本地推理路线（ADR-007 v11 范围）
- ❌ 衣服换装系统（ADR-009 v12 范围）
- ❌ 18 层顺序调整（ADR-003 单向门，任何变动须升大版本 + 改 ADR）
- ❌ 三栈架构调整（ADR-002）
- ❌ License 变更（ADR-001 Rev.3 MIT 保留）

---

## 五、发布验收 Checklist

v10.1 合并前，以下全部必须为 YES：

- [ ] `python -m core.workflow "anime girl with blue hair"` （默认语义分割）跑完全流程，success=True
- [ ] `python -m core.workflow --no-semantic "anime girl"` （KMeans）跑完全流程，success=True
- [ ] `python -m core.workflow -i test.png --live2d-export` 产出的 model3.json 通过 `ModelValidator.validate_all()`
- [ ] 导出的 model3.json 中 `Version == 3`，`FileReferences.Textures` 非空，`FileReferences.Physics` 存在，`Expressions` 有 28 个
- [ ] 输出目录中**只有一份** model3.json（不是 Step 4b + Step 6b 的两份）
- [ ] `pip install -r requirements.txt` 在 Python 3.10/3.11/3.12/3.14 四个版本下全部成功（无 triangle/psd-tools 编译失败）
- [ ] `python install.py` 在上述四个 Python 版本下全部成功
- [ ] `python scripts/lint_architecture.py` 返回 exit code 0（FF-1）
- [ ] `pytest tests/unit/test_layer_order_contract.py` 全通过
- [ ] `pytest tests/integration/test_tearing.py` 全通过
- [ ] 7 个 FF 脚本全部纳入 CI（PR 阻断级）
- [ ] 桌宠 `python -m core.cli pet --model <dir>` 能启动，fps 稳定 ≥ 58（FF-10）

---

## 六、工作量预估

| 类别 | 内容 | 预估 |
|------|------|------|
| P0 修复 | Fix-1/2/3（3 个接口错位） | 0.5 天 |
| P1 修复 | Fix-4/5/6/7（安装+LayerComposer+提示） | 0.5 天 |
| P2 修复 | 注释、UV 合批、52 层映射优化 | 0.5 天 |
| FF 落地 | 7 个 Fitness Function 脚本 | 1.5 天 |
| 契约测试 | 2 个测试文件 | 1 天 |
| CI 集成 + 跨版本安装验证 | GitHub Actions 矩阵 | 0.5 天 |
| 实跑回归 + 文档更新 | 版本号、CHANGELOG | 0.5 天 |
| **合计** | | **5 天**（单人） |

---

## 七、版本号与发布说明

- 版本号：v10.0.0 → **v10.1.0**（语义化版本：MINOR 更新，新增 FF/测试但不破坏 ADR）
- 全版本字符串：`v10.1.0-patch`
- model3.json 版本仍为 Cubism 4 的 Version: 3（无变化，Cubism 兼容）
- 用户可见的变化：
  1. 默认语义分割路径不再崩溃
  2. 生成产物只有一份 model3.json（不再有"空壳模型"迷惑用户）
  3. Python 3.14 可以正常 `pip install` 和 `python install.py`
  4. 安装时不再出现 triangle 编译错误
  5. 语义分割质量提升（LayerComposer Amodal 补全生效）
  6. UV atlas 利用率提升，模型加载更快
