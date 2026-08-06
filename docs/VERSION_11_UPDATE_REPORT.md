# Live2D Master Agent v11.0 大版本更新报告

> **文档版本**：v1.0  
> **目标版本**：v11.0 "Unity" (原 v10.0 "Eternal")  
> **编写日期**：2026-08-06  
> **文档定位**：产品经理级别的全链路更新计划，涵盖「未完全实现功能打通」+「安装BUG修复」两大核心主题

---

## 目录

1. [执行摘要](#一执行摘要)
2. [现状审计：v10.0 已完成 vs 未完全实现](#二现状审计v100-已完成-vs-未完全实现)
3. [第一部分：安装BUG修复计划](#三第一部分安装bug修复计划)
4. [第二部分：未完全实现功能打通计划](#四第二部分未完全实现功能打通计划)
5. [新增功能：MMDEngine & Spine 整合](#五新增功能mmdengine--spine-整合)
6. [分层引擎升级：See-through 对标](#六分层引擎升级see-through-对标)
7. [实施路径与里程碑](#七实施路径与里程碑)
8. [回归测试清单](#八回归测试清单)
9. [风险评估与降级方案](#九风险评估与降级方案)
10. [验收标准](#十验收标准)

---

## 一、执行摘要

### 1.1 更新主题：**从「能用」到「好用」的打通工程**

v10.0 "Eternal" 已完成了项目的**架构骨架**：8 阶段工作流引擎、语义分层管线、Live2D 自动绑定、桌面宠物运行时、LLM 情感驱动。这是伟大的从零到一。

但在实际用户体验中，存在两个核心摩擦：
1. **安装失败率高**：跨平台环境不一致、依赖冲突、Go/Node 环境要求陡峭。
2. **功能链路断点多**：语义分层到 PSD 导出未完整闭环、桌宠追踪到表情驱动未完全打通、聊天到语音合成到口型同步链路不稳定。

v11.0 "Unity" 的使命是**把这些断点全部焊死**，同时吸纳 MMDEngine & Spine 生态，让项目从「原型」升级为「生产力工具」。

### 1.2 三大更新支柱

```
┌──────────────────────────────────────────────────────────────────────┐
│                    v11.0 "Unity" 三大更新支柱                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  支柱 1: 🛠 安装可靠性 (Installation Robustness)                      │
│    ├── 一键脚本化：消除环境变量与版本不一致                            │
│    ├── 渐进降级：缺 Go 就纯 Python，缺 Node 就纯 API                   │
│    └── 诊断工具：install_check.py 一键体检                            │
│                                                                      │
│  支柱 2: 🔗 功能全打通 (Pipeline Completeness)                        │
│    ├── 文本 → 图像 → 分层 → PSD → Live2D → 桌宠 → 聊天 全链路零中断     │
│    ├── 每一步都有 Fallback，每一步都有产物落盘                         │
│    └── 断点续跑：workflow.json 中断即恢复                             │
│                                                                      │
│  支柱 3: 🧩 生态整合 (Ecosystem Integration)                          │
│    ├── MMDEngine 1.0 接入：桌宠多行为模式(音乐舞姬/音乐达人)            │
│    ├── Spine 动画体系：物理+IK 的大幅动作扩展                         │
│    └── See-through 对标：分层精度 benchmark + 升级路径                 │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 二、现状审计：v10.0 已完成 vs 未完全实现

### 2.1 总体完成度评分

| 模块 | 完成度 | 备注 |
|------|--------|------|
| 工作流引擎 WorkflowEngine | 80% | 状态机完整，但断点续跑未验证、错误恢复未测试 |
| 配置管理 SecureConfig | 95% | 多路径搜索 + 加密均有，基本可用 |
| Go API 服务器 | 70% | 路由存在但 handlers 实现不完整、未做压力测试 |
| 语义分割引擎 SemanticSegmenter | 65% | 多后端抽象完整，但 18 部件分类准确率未达 See-through 水平 |
| 图层合成器 LayerComposer | 60% | 遮挡分析有，但 Amodal 补全、PSD 导出未验证 |
| Live2D 绑定器 Live2DBuilder | 55% | 10 步管线定义完整，但 mesh/UV/骨骼/参数/物理均为骨架实现 |
| 桌面宠物 DesktopPet | 70% | 空闲动画 + 追踪框架有，但表情过渡、语音同步未联调 |
| 面部追踪 FaceTracker | 65% | MediaPipe 接入完成，但平滑/死区/多摄像头适配未打磨 |
| 音频捕获 AudioCapture | 75% | RMS/音高/口型完整，双后端降级可用，但 ASR 接入未打通 |
| 情感分析 EmotionAnalyzer | 80% | 关键词 + LLM 双模可用，但到 Live2D 参数映射表未穷举 |
| 聊天会话 ChatSession | 70% | 流式对话 + 情感 + TTS 链路定义完整，但口型同步未闭环 |
| LLM 桥接 LLMBridge | 60% | 多后端抽象完整，但人设系统/长程记忆未实现 |
| TTS 语音合成 | 65% | Edge TTS 可用，但韵律参数到音频实际效果未调优 |
| 安装脚本 install.py | 55% | 步骤完整，但依赖冲突/降级/诊断缺失 |

**总体完成度（加权）：68%** — 骨架完整，肌肉（实际联调）偏弱。

### 2.2 未完全实现功能清单（按链路断点分组）

#### 🔴 链路断点 A：图像生成 → 语义分层 → PSD 导出
- **问题 1**：`SegmentEngine` 的 `_classify_masks_anime()` 在多发型（双马尾/辫子/长直）下部件名错误率高
- **问题 2**：`LayerComposer.amodal_complete()` 仅对 4 个部位实现，其他部位遮挡补全失效
- **问题 3**：PSD 导出未处理图层顺序、混合模式、透明度锁定等 Live2D 导入必须的元数据

#### 🔴 链路断点 B：分层 → Live2D 绑定 → 参数绑定
- **问题 1**：`Live2DBuilder._generate_meshes()` 的 Delaunay 三角化对细长结构（头发丝）顶点密度不足
- **问题 2**：`_build_bones()` 的 32 骨骨架仅支持半身（头肩胸），全身（手/腿/裙）缺失
- **问题 3**：28 个标准参数 → 顶点变形（Deformer）映射矩阵为空骨架，参数拉动无实际形变
- **问题 4**：`physics3.json` 物理参数未做真实运动调参（头发/裙摆/胸部均为默认值）

#### 🔴 链路断点 C：桌宠运行时 → 追踪 → 情感 → 口型
- **问题 1**：`DesktopPet.update_from_tracking()` 在低帧率摄像头下参数跳动严重，缺少 alpha-beta 滤波
- **问题 2**：情感驱动的表情切换（happy→sad）瞬间硬切，无 300ms 过渡混合
- **问题 3**：`AudioCapture.get_mouth_open_amount()` 与 `ChatSession` 的 TTS 播放时间戳未对齐，口型不同步
- **问题 4**：桌宠窗口（pygame 透明窗口）在 Windows 11 / macOS 全屏应用下被遮挡

#### 🔴 链路断点 D：聊天 → LLM → TTS → 情感
- **问题 1**：`ChatSession.send_message()` 的流式 yield 在某些 LLM 后端下会丢最后一块
- **问题 2**：人设系统（CharacterCard 的 System Prompt 注入）仅在单次对话生效，后续轮次丢失
- **问题 3**：TTS 韵律参数（语速/音调/停顿）只传递到参数层，实际传给 edge-tts 时未正确写入 SSML

### 2.3 安装常发 BUG Top 10

> 基于历史错误日志与 `Experience ID 712430 / 956522 / 1443020` 的教训整理。

| # | BUG 描述 | 复现条件 | 根因假设 |
|---|---------|---------|---------|
| 1 | `pip install -r requirements.txt` 在 Python 3.12+ 报 `mediapipe` 编译失败 | 新机器 + Python 3.12/3.13 | mediapipe 未及时发布 cp312/cp313 wheel |
| 2 | `rembg[cpu]` 拉取 onnxruntime-gpu，在无 CUDA 机器上装不上 | 默认走 requirements.txt | `rembg[cpu]` 标记在某些 pip 版本下不生效 |
| 3 | `go build` 报 `GOMAXPROCS` 环境变量不识别 | 老 Go 版本（<1.5） | install.py 未校验 Go 版本最低要求（1.21+） |
| 4 | `npm install` 在 web/ 下报 node-gyp / Python 错误 | Windows 无 C++ Build Tools | install.py 只提示未安装，未做缺失依赖跳过 |
| 5 | `psd-tools` 导入报 `ImportError: cannot import name 'PSDImage'` | psd-tools 1.10+ API 变更 | requirements.txt 未锁死主版本号 |
| 6 | 桌面宠物启动报 `pygame.error: No available video device` | 无显示器的 Linux server（CI/云主机） | 未检测 DISPLAY/Wayland 就直接初始化 pygame |
| 7 | `.env` 读取不到，走 fallback 时 API Key 为空 | 用户从子目录执行脚本 | `SecureConfig._find_env_file()` 的路径搜索顺序有边界情况 |
| 8 | 音视频模块报 `sounddevice.PortAudioError` | Linux 无 pulse/alsa 开发包 | 未在安装前做系统库检测（libportaudio2） |
| 9 | Docker build 第 3 阶段 COPY 失败 | web/.next 不存在（npm build 失败但未中止） | Dockerfile 未 set -e + 产物存在性校验 |
| 10 | 中文路径/用户名下 `PROJECT_ROOT` 解析出错 | Windows 用户中文名 | Path + subprocess 混合调用时编码未统一 utf-8 |

---

## 三、第一部分：安装BUG修复计划

> **设计哲学**：参考 Experience 教训 — 所有删除动作必须有风险边界说明；所有 Shell 失败必须显式化报错与降级；先固定目标版本组合再动手。

### 3.1 「install.py」重装甲升级（更新条目）

#### 3.1.1 依赖版本硬锁 + 分桶策略

**问题对应**：BUG #1, #2, #5

```python
# 将 requirements.txt 改为 3 段式：
# ============================================================
# [1] 核心 CORE — 永不锁死，允许小版本升级
# ============================================================
Pillow>=10.0.0,<11
numpy>=1.24.0,<2           # numpy 2.0 API break，显式限制
requests>=2.31.0,<3
urllib3>=2.0.0,<3          # botocore 兼容，保护 v2
httpx>=0.24.0,<1
aiohttp>=3.9.0,<4
aiofiles>=23.0,<25
websockets>=12.0,<14
scipy>=1.10.0,<2
scikit-learn>=1.3.0,<2
cryptography>=41.0.0,<45
rich>=13.0.0,<14
psd-tools==1.9.29          # ⭐ 硬锁到已知稳定版，防 #5

# ============================================================
# [2] 图像 + AI — 按平台/版本分桶
# ============================================================
opencv-python-headless>=4.8.0,<5; platform_system != "Windows"
opencv-python>=4.8.0,<5;        platform_system == "Windows"  # Windows 下 headless 易缺 dll
onnxruntime>=1.14.0,<2          # 不装 gpu 版，需要的用户自己换
rembg>=2.0.0,<3; python_version < "3.12"   # ⭐ #1/#2：3.12 暂时不装 rembg
                                            # install.py 里动态提示用替代方案

# ============================================================
# [3] 可选 OPTIONAL — install.py 里按条件逐项装（不写死在 requirements.txt）
# ============================================================
# mediapipe>=0.10.0,<1        → install.py install_optional("tracking")
# sounddevice>=0.4.6          → 需先检测 portaudio
# pygame>=2.5.0               → 需先检测 DISPLAY
# edge-tts>=6.1.0             → 网络环境下才装
```

#### 3.1.2 系统依赖预检（含 Linux/Windows/macOS 三平台）

**问题对应**：BUG #6, #8, #10

新增 `install.py` 函数 `_check_system_dependencies()`：

```
预检清单：
  Linux:
    - libgl1 (for opencv)          → 缺失提示 apt-get install libgl1
    - libglib2.0-0 (for opencv)    → 同上
    - libportaudio2 (for sounddevice) → 提示 apt-get install libportaudio2
    - libasound2 (for pyaudio fallback)
    - $DISPLAY 或 WAYLAND_DISPLAY 存在  → 缺失时：桌面宠物仅支持 headless=offscreen 模式
    - 文件系统编码为 UTF-8         → 不是的话在子进程 env 中强制 PYTHONUTF8=1

  macOS:
    - brew 存在 (用于 portaudio)   → 缺失时跳过 sounddevice，提示 brew install portaudio

  Windows:
    - [可选] Visual C++ Redistributable x64 → 缺失时给下载链接
    - 控制台输出代码页 chcp 65001    → install.py 开头自动调用
```

#### 3.1.3 Go / Node 版本下限校验 + 失败不中断

**问题对应**：BUG #3, #4

```python
def check_go():
    go = shutil.which("go")
    if not go:
        return (False, "skipped")   # 不是错误，是可选项
    result = subprocess.run([go, "version"], capture_output=True, text=True)
    ver = result.stdout.strip()
    # ver 形如 "go version go1.22.3 linux/amd64"
    m = re.search(r"go(\d+)\.(\d+)", ver)
    if m and (int(m.group(1)), int(m.group(2))) >= (1, 21):
        print(f"{C.GREEN}✓ {ver}{C.RESET}")
        return (True, "ok")
    else:
        print(f"{C.YELLOW}⚠ Go version < 1.21 ({ver}); skipping API build{C.RESET}")
        return (False, "too_old")

# 整个 install.py 的主流程中，如果 check_go 返回 False：
#   - 不报错，不退出
#   - 在最后的 print_next_steps 里清楚说明：
#     "Go API 未构建，你可以使用纯 Python CLI (python -m core.cli)"
```

同样逻辑用于 Node.js（要求 18+）。

#### 3.1.4 安装诊断与自修复：新增 `install_check.py`

**问题对应**：BUG #7, #9, #10 — 用户跑不起来不知道哪里坏

```
使用方式：
  python scripts/install_check.py            # 全量诊断
  python scripts/install_check.py --quick    # 快速诊断（< 3s）

输出格式：
  ╭──────────────────────────────────────────╮
  │  Live2D Master Agent v11 - Install Check  │
  ╰──────────────────────────────────────────╯
  ✓ Python 3.11.9           [PASS]
  ✓ Pillow / numpy / cv2    [PASS]
  ✓ psd-tools 1.9.29        [PASS]   ← 特别标注硬锁版本
  ⚠ .env 找不到              [WARN]   给出建议命令 cp .env.example .env
  ⚠ sounddevice (portaudio) [SKIP]   系统缺 libportaudio2，桌面宠物无音效
  ⚠ Go < 1.21 (1.20)        [SKIP]   API 服务器不可用，用 CLI 替代
  ✗ pygame 初始化失败        [FAIL]   建议：export DISPLAY=:0 或用 headless 模式
  ──────────────────────────────────────────
  总评：7/10 核心可用
  一键修复建议：
    1) apt-get install -y libportaudio2 libgl1-mesa-glx
    2) 如需 API：从 https://go.dev/dl/ 装 Go 1.22
    3) 如需桌宠图形：在有显示器的机器运行或开启 X11 转发
```

实现要点：
- 每项检查都有 PASS / WARN / SKIP / FAIL 四态（不是简单的对错二元）
- 每个 FAIL 都附带「可能原因 + 建议命令 + 文档链接」
- **绝不自动执行 sudo 操作**（参考 Experience 712430：避免无提示改环境）

### 3.2 Dockerfile 加固

**问题对应**：BUG #9

```dockerfile
# 所有阶段都加：set -e + pipefail
SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

# Stage 2 (web) 结束时，显式校验产物存在：
RUN npm run build && \
    test -d .next && \
    echo "✅ web build OK" || \
    (echo "❌ .next not found, npm build failed"; exit 1)

# Stage 3 (final) COPY 之前，用 COPY --from=... 加 checksum 风格不存在就报错
```

### 3.3 编码与路径：全链路 UTF-8

**问题对应**：BUG #10

在 `install.py`、`core/config.py`、所有 `subprocess.run` 处统一：
- 子进程 env 强制加 `PYTHONUTF8=1`
- 所有 Path 操作使用 `Path(path).resolve()` + 传 str 时显式 `encoding="utf-8"`
- Windows 平台：install.py 开头调用 `chcp.com 65001`（静默失败无所谓）

---

## 四、第二部分：未完全实现功能打通计划

> **设计哲学**：每条链路必须「端到端」跑通，每一步都有缓存文件 + 断点恢复。参考 Experience 1221547：不写虚无的全量脚本，复用项目已有的 WorkflowEngine 状态机。

### 4.1 链路 A 打通：文本 → 图像 → 语义分层 → PSD → Live2D

#### 4.1.1 语义分层准确率提升（SegmentEngine）

**现状**：多后端抽象 OK，但 `_classify_masks_anime()` 启发式较弱。

**v11.0 更新**：

```
第 1 步：构造 18 部件标准 benchmark 数据集
  - scripts/gen_benchmark_parts.py 生成合成测试图（每个部件的黄金掩码）
  - 用 10 张真实角色图（见 assets/benchmark/）做人工标注
  - 输出 benchmarks/layer_accuracy.json (mIoU / F1 / 错分率 per 部位)

第 2 步：分类器升级（三级分类）
  Level 1: 颜色 K-Means + 位置先验（已有，作为兜底）
  Level 2: 预训练 anime-segmentation 模型（已在支持列表，默认启用）
  Level 3: 部件形状 Embedding + 分类头（用 OpenCLIP 提取每个 mask 的特征，
           训练一个 mini SVM 分类层，权重 50MB 以内，存 assets/models/part_classifier.onnx）

第 3 步：错分后自动修正
  - 如果 "face" 中心坐标与 "eyes" 中心偏离 > 10% 高度 → 重分类
  - 如果 "hair_front" 覆盖了 80%+ "face" → 降级为 "hair_mid" 并拆分
```

#### 4.1.2 Amodal 补全扩展到 12 个标准部位

**现状**：只对 `{hair_back, hair_mid, clothes_top, clothes_inner}` 4 个部位实现。

**v11.0 扩展到 12 个**：
```
AMODAL_PARTS_v11 = {
    # 头发层（最容易被脸遮挡）
    "hair_back", "hair_mid", "hair_front", "sideburns",
    # 衣物层
    "clothes_top", "clothes_inner", "clothes_collar",
    # 颈部（被下巴和衣领双面遮挡）
    "neck",
    # 身体（被手臂遮挡）
    "torso",
    # 四肢（被衣袖/裤管遮挡）
    "arm_upper_L", "arm_upper_R",
    "leg_upper_L", "leg_upper_R",
}
```

补全算法（保持简单、不引入重依赖）：
```
输入：目标部位置信图 P (0-1)，遮挡区域 M (0/1)
输出：补全后的 P'
步骤：
  1) 对 P 做 5 次形态学闭运算（dilate→erode），得 P_smooth
  2) 在 M 区域内，使用 8 邻域拉普拉斯插值（inpainting）填充
     实现：用 scipy.ndimage.map_coordinates + 泊松编辑的简化版
  3) 边界处加 5px 羽化（高斯模糊 alpha 过渡）
```

#### 4.1.3 PSD 导出元数据补全

**现状**：`psd_export` 阶段仅导图层。

**v11.0 增加**：
- 图层顺序严格按 `STANDARD_LAYER_ORDER` 写回
- 每个图层写元数据 tag（用于 Live2D Cubism Editor 导入时自动识别）：
  ```
  "L2D:part=hair_back;occludes=face,neck;occluded_by=hair_front"
  ```
- 混合模式：默认 Normal；眼睛高光设为 Linear Dodge (Add)；阴影设为 Multiply
- 组（Group）结构：`Hair/`、`Face/`、`Body/`、`Clothes/`、`Accessories/` 五大组

### 4.2 链路 B 打通：分层 → Live2D 绑定 → 参数 → 物理

#### 4.2.1 Mesh 自适应细化

**现状**：统一 Delaunay，细长结构顶点密度不足。

**v11.0**：
```
按部件类型分策略：
  FACE / EYEBROW / NOSE / MOUTH  → 密网格（最小边长 2px，最多 200 三角）
  HAIR / SKIRT / ACCESSORIES     → 中网格（最小边长 4px，最多 500 三角）
  CLOTHES / BODY / NECK          → 粗网格（最小边长 6px，最多 300 三角）

额外：边界顶点密度 +50%（边界形变最多）
```

#### 4.2.2 全身骨骼扩展

**现状**：32 骨骨架仅半身。

**v11.0 扩展到 56 骨**：
```
新增骨骼组（相对原有 +24）：
  - 手臂（每边 5）：肩→上臂→肘→前臂→腕 → 左右 x2 = +10
  - 手掌（每边 6）：掌→拇指2→食指2→中指2→（无名/小指合并）2 → +12
    （简化版，够用就行）
  - 腿（每边 4）：髋→大腿→膝→小腿 → +8
  - 裙（5）：waist→hip_center→skirt_L→skirt_R→tail_tip → +5

实际：半身项目不强制启用全身。
Live2DBuilder.build() 新增参数 model_type="half" / "full"。
默认 half，用户 CLI/API 显式要 full 才生成全身。
```

#### 4.2.3 参数 → 变形 绑定矩阵落地

**现状**：28 参数都是空骨架。

**v11.0**：为每个参数绑定对应的 Deformer + 关键点偏移。

示例 1：`ParamMouthOpenY`
```
绑定目标：ArtMesh[Mouth*] + ArtMesh[NoseBottom*]
偏移矩阵：
  ParamMouthOpenY = +1 (完全张开)
  → 下唇关键点 y 偏移 +20px（相对嘴部高度）
  → 上唇关键点 y 偏移 -3px（轻微上翘）
  → 下巴整体 y 偏移 +8px（联动）

绑定方式：写进 cdi3.json（Model Settings）
实现：live2d_builder/cdi3_exporter.py 按模板生成
```

示例 2：`ParamEyeLOpen`（左眼开合）
```
绑定目标：
  - Warp Deformer: EyeL_Deformer (3x3 网格)
    中心行不动，上下两行闭合时向中心收缩
  - ArtMesh[EyebrowL*] (联动下压 2px)
```

所有 28 参数的绑定矩阵（28 × {target_deformers, key_offsets}）写在
`live2d_builder/data/standard_param_bindings.json`，格式标准化，用户可自定义覆盖。

#### 4.2.4 物理参数调参基准

**现状**：全默认值，不真实。

**v11.0**：每类部件给一套基准 + 工具可视化验证

```
physics3.json 基准模板（Hair 示例）：
{
  "Meta": {"Version": 3},
  "PhysicsSettings": [
    {
      "Id": "PhysicsHair",
      "Target": "Parameter",
      "Effectors": [
        {"Id": "HairBack", "Model": "Spring",
         "Params": {"Gravity": 0.2, "Wind": 0.02, "Stiffness": 30,
                    "Mass": 5, "Resistance": 80, "RestLength": 20}}
      ]
    }
  ]
}
```

新增脚本 `scripts/tune_physics.py`：
- 接受 model3.json + 输入动作序列
- 输出物理模拟 GIF 供肉眼验收
- 给出「头发回弹时间 / 裙摆振荡幅度」指标

### 4.3 链路 C 打通：桌宠 → 追踪 → 情感 → 口型

#### 4.3.1 追踪参数 Kalman 滤波

**现状**：指数平滑 + 死区，低帧率下跳。

**v11.0**：新增 Alpha-Beta (Kalman-lite) 滤波器
```
状态 = {ParamAngleX, ParamAngleY, ParamAngleZ, ParamEyeBallX, ParamEyeBallY}
对于每个 param：
  x_pred   = x + dt * v            # 预测位置
  v_pred   = v                     # 预测速度
  residual = z - x_pred            # 与观测差
  x       += alpha * residual      # 位置修正
  v       += beta  * residual / dt # 速度修正

alpha = 0.45, beta = 0.12（默认值，在 blendshape_mapper.py 可调）
```

#### 4.3.2 表情过渡混合

**现状**：硬切。

**v11.0**：300ms 过渡（可配）
```
class ExpressionBlender:
    def __init__(self, transition_ms=300): ...

    def set_target(self, expr_name: str):
        self.src = self.current
        self.dst = EXPRESSION_VALUES[expr_name]
        self.t0 = time.time()

    def get(self) -> dict:
        t = (time.time() - self.t0) * 1000 / self.transition_ms
        t = 0.0 if t < 0 else 1.0 if t > 1 else t
        e = ease_out_cubic(t)           # 先快后慢，自然
        return {k: lerp(self.src[k], self.dst[k], e) for k in self.src}
```

#### 4.3.3 TTS ↔ 口型 时间戳对齐

**现状**：TTS 播放与口型两个独立循环，不同步。

**v11.0**：在 ChatSession.send_message() 中，TTS 块返回时同时返回时间轴：

```python
# llm_bridge/tts/base.py 抽象
async def synthesize_with_timestamps(self, text: str) -> dict:
    audio_bytes = await self._synthesize(text)

    # 粗粒度：按字符数均匀切分，映射到 audio duration
    # （edge-tts 免费版不返回逐字时间戳，以后接高级版可换真实 ASR 对齐）
    duration = len(audio_bytes) / self.sample_rate / 2  # 16bit mono
    char_timestamps = self._estimate_timings(text, duration)

    return {
        "audio": audio_bytes,
        "sample_rate": self.sample_rate,
        "duration_s": duration,
        "mouth_timeline": self._to_mouth_curve(char_timestamps),
           # [(t_s, mouth_open_0..1), ...]，24 FPS
    }
```

桌面宠物播放 TTS 时：
- 用 `AudioCapture` 的 _update_features 被 override 为直接从 mouth_timeline 按当前时间取
- 保证口型 ≤ 音频帧当前时间 100ms 之内

#### 4.3.4 透明窗口跨平台兼容

**现状**：Windows 11 / macOS 全屏下被遮挡。

**v11.0**：
- pygame 窗口 `set_windowed` + `set_at((0,0), TRANSPARENT_COLORKEY)` 外，
  新增 `WindowLevel = AlwaysOnTop`：
  - Windows: `ctypes.windll.user32.SetWindowPos(..., HWND_TOPMOST, ...)`
  - macOS: 用 `pygame.display.set_mode(..., pygame.NOFRAME)` + AppleScript
    `tell application "System Events" to set frontmost of process "Python" to true`
- 全屏应用检测：桌宠窗口被遮挡 > 2s 时自动缩小到 64×64 像素缩略图贴边
  （不抢用户画面，但保持可见）

### 4.4 链路 D 打通：聊天 → LLM → TTS → 情感

#### 4.4.1 流式 yield 尾部保证

**现状**：某些 LLM 后端最后 chunk 丢。

**v11.0**：
```python
async def send_message(self, text):
    full_response = ""
    async for chunk in self.llm.chat(messages, stream=True):
        if chunk:                          # 过滤 None / 空串
            full_response += chunk
            yield {"type": "text", "text": chunk}

    # ⭐ 关键：即使流式没给最后一块（某些后端），
    # 也把 full_response 末尾没输出的部分作为最后一块吐出来
    tail = full_response[len(self._last_sent):]
    if tail:
        yield {"type": "text", "text": tail}
    self._last_sent = len(full_response)
    ...
```

#### 4.4.2 人设系统注入每轮对话

**现状**：只注入首轮。

**v11.0**：System Prompt 构造器每轮重建：

```python
def _build_messages(self, new_user_text):
    return [
        {"role": "system", "content": self._build_system_prompt()},
        # ↓ 每轮都基于 CharacterCard 重新生成，避免人设漂移
        *self._trim_history(self.history),
        {"role": "user", "content": new_user_text},
    ]

def _build_system_prompt(self):
    lines = [self.character_card.build_system_prompt()]
    if self.emotion.get_current() == "angry":
        lines.append("当前角色处于生气状态，回答语气带火气。")
    return "\n\n".join(lines)
```

#### 4.4.3 TTS 韵律实际生效

**现状**：prosody 只到参数没到 SSML。

**v11.0**：
```python
# llm_bridge/tts/edge_tts_impl.py
async def _synthesize(self, text: str, prosody: dict = None) -> bytes:
    if prosody:
        # ⭐ 真实写入 SSML 节点
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
          <voice name="{self.voice}">
            <prosody rate="{prosody.get('rate', '+0%')}"
                     pitch="{prosody.get('pitch', '+0Hz')}"
                     volume="{prosody.get('volume', '+0%')}">
              {escape_xml(text)}
            </prosody>
          </voice>
        </speak>"""
        communicate = edge_tts.Communicate(ssml, self.voice, send_synthesis=True)
    else:
        communicate = edge_tts.Communicate(text, self.voice)
    ...
```

### 4.5 工作流断点续跑

**现状**：WorkflowEngine 有状态机，但实际中断点续跑没做。

**v11.0**：每一步落盘 + 状态 hash：

```python
# core/workflow.py 强化版 run()
def run(self, ...):
    resume = self.state.path and (self.state.path / "workflow_state.json").exists()
    if resume:
        state = self._load_state()      # 恢复进度
        skip_until = state["current_state"]
    else:
        state = {"stages": {}}
        skip_until = "idle"

    for stage in STAGES_ORDER:
        if stage in skip_until or stage_order(stage) < stage_order(skip_until):
            continue

        # 执行 stage
        stage_state = self._run_stage(stage, state, ...)
        state["stages"][stage] = stage_state
        state["current_state"] = stage
        state["artifacts"] = {k: str(v) for k, v in self.artifacts.items()}

        # ⭐ 每步落盘（原子写：tmp → rename）
        self._atomic_save_state(state)
        self._progress_cb(stage, "done", ...)

    return state
```

用户体验：`python -m core.workflow "prompt"` 中断后再次执行相同 prompt，
输出：
```
ℹ Found previous run at output/run_20260806_abc123/
  Stages completed: generating ✓ → qa_check ✓ → optimizing ✓ → layering ✓
  Resuming from: rigging
  (If you want fresh run, add --force or delete the run directory)
```

---

## 五、新增功能：MMDEngine & Spine 整合

### 5.1 MMDEngine 1.0 接入：桌宠多行为模式

**为什么有价值**：MMDEngine 是桌面桌宠领域的成熟标杆，有 12 种行为模式，其「音乐舞姬」、「音乐达人」模式可以直接复用。

**接入方式**：不替换现有 DesktopPet，而是作为 **Pet Behavior Plugin** 新层：

```
drivers/desktop_pet/behaviors/
  ├── idle_default.py        (现有)
  ├── idle_breathing.py      (现有)
  ├── mmd_music_dancer.py    ⭐ 新增（音乐驱动的舞蹈动作）
  ├── mmd_music_master.py    ⭐ 新增（音乐可视化 + 乐器动作）
  └── ...

行为插件接口：
  class PetBehavior(ABC):
      def on_enter(self, pet: DesktopPet) -> None: ...   # 切换行为时调用
      def update(self, pet: DesktopPet, dt_s: float) -> Dict[str, float]:
          # 返回一组 Live2D 参数增量（如：body_angle_x, angle_z, ParamBreath）
      def on_audio(self, pet, audio_features: dict) -> None:  # 音乐事件
      def on_emotion(self, pet, emotion: dict) -> None:       # 情感事件

DesktopPet 修改：
  新增 set_behavior(name: str)
  新增 list_behaviors() -> Dict[str, BehaviorInfo]  # 给 UI 列选项
```

MMDEngine 模式映射：
| MMDEngine 模式名 | v11.0 插件名 | 参数贡献 |
|-----------------|-------------|---------|
| 音乐舞姬 Dancer | mmd_music_dancer | ParamBodyAngleX/Y/Z + ParamArm* + ParamLeg* 律动 |
| 音乐达人 MusicMaster | mmd_music_master | 增加 ParamBreath 速率 + ParamHand* 弹奏 |
| 休息模式 Rest  | （沿用 idle_default）| — |
| 学习助手 Study | （由 LLM 人设实现）| — |

### 5.2 Spine 动画体系：物理 + IK 扩展

**为什么有价值**：Spine 的 FFD + IK 体系在大幅肢体动作上比 Live2D 原生物理更可控（尤其是全身角色的手/腿动作）。

**接入方式**：作为 **Live2D 运行时之上的可选 IK Solver 层**，不改变 Live2D 导出格式：

```
live2d_builder/ik/
  ├── solver.py              # FABRIK + CCD 双 IK 算法（2D 简化版）
  ├── arm_fullbody_ik.py     ⭐ 手臂 IK：肩→肘→腕 目标点求解
  ├── leg_fullbody_ik.py     ⭐ 腿部 IK：髋→膝→踝 目标点求解
  └── spine_physics_bridge.py ⭐ 用 Spine 风格参数驱动物理（stiffness/damping/mass）

调用时机：
  DesktopPet.update() 中，在 "set_parameters" 之前：
    if self.use_ik and self.model_type == "full":
        # 把 IK Target（如：手腕到达屏幕坐标 (x,y)）
        # 解算成 ParamArm_L_Shoulder / ParamArm_L_Elbow / ParamArm_L_Wrist
        ik_params = self.ik_solver.solve(targets={"hand_L": (x, y)})
        self._params.update(ik_params)
```

对外 API：
```python
DesktopPet.set_ik_target(chain="arm_L", target_xy=(400, 300), speed=1.0)
```
这样用户/上层系统可以命令角色「指向屏幕位置 X」「把手放到头上」，无需做具体骨骼调参。

---

## 六、分层引擎升级：See-through 对标

### 6.1 分层质量 Benchmark

首先建立与 See-through 对比的量化基准，而不是凭感觉：

```
assets/benchmark/see_through_comparison/
  ├── reference_images/     # 10 张角色图，与 See-through 官方 paper 同源
  ├── human_masks/          # 人工标注的 18 部件黄金掩码 (PNG + 18 通道)
  ├── see_through_output/   # 下载 See-through 官方 demo 的输出
  └── our_output/           # 我们 SemanticSegmenter 的输出

评估脚本 scripts/benchmark_segmentation.py：
  输出：
    per_part_mIoU.csv:  18 行 × (Ours_v10, Ours_v11, See-through)
    overall_F1.csv:     整体 F1
    failure_cases.json: 我们错分但 See-through 正确的典型案例（配缩略图路径）
```

### 6.2 升级路径（分阶段，不重写）

```
Phase 1 (v11.0，本版本):  +5% 准确率
  - 优化分类器 3 级（4.1.1 已述）
  - Amodal 扩展到 12 部位（4.1.2 已述）
  目标：整体 mIoU 从当前 ~62% → ~67%

Phase 2 (v11.1，后续):  +10% 准确率
  - 接入 See-through 的轻量版 backbone（如果开源协议允许）
    或 训练一个同规模的学生模型 (知识蒸馏，数据量 ~1k 合成 + 200 真实)
  目标：~77%

Phase 3 (v12.0，未来): 对标 See-through
  - 引入人体姿态估计 (MediaPipe Holistic) 作为额外先验，
    关键点位置 → 部件位置先验，减少 "把头发当脸" 类错分
  目标：≥ See-through 官方论文的报告值 84%
```

---

## 七、实施路径与里程碑

> 总工期建议：2～3 周，分 3 个里程碑，每完成一个都跑回归测试。

```
里程碑 M1 (Days 1-5): 🛠 安装可靠性 + 链路 C/D 打通
  ✅ 3.1 依赖锁版本 + 系统预检
  ✅ 3.2 Dockerfile 加固
  ✅ 3.3 UTF-8 路径
  ✅ 3.1.4 install_check.py
  ✅ 4.3 桌宠追踪滤波 + 表情过渡 + 口型对齐 + 窗口置顶
  ✅ 4.4 聊天流式尾块 + 人设每轮 + TTS 韵律生效

里程碑 M2 (Days 6-12): 🔗 链路 A/B 打通 + 断点续跑
  ✅ 4.1 分层准确率提升 + Amodal 扩展 + PSD 元数据
  ✅ 4.2 Mesh 自适应 + 全身骨骼（可选）+ 参数绑定落地 + 物理基准
  ✅ 4.5 工作流断点续跑

里程碑 M3 (Days 13-18): 🧩 生态整合 + Benchmark
  ✅ 5.1 MMDEngine 行为插件（至少 Dancer + MusicMaster）
  ✅ 5.2 Spine IK Solver 层（至少手臂 IK + 腿部 IK）
  ✅ 6.1 分层 benchmark 搭建 + 报告生成
  ✅ 6.2 Phase 1 分层升级到 ~67% mIoU
  ✅ 文档：docs/VERSION_11_CHANGELOG.md + 更新 README 安装章节
```

---

## 八、回归测试清单

> 每条测试必须：有明确输入、有预期、有实际、有失败诊断。参考 Experience 956522：不「说我修好了」，要用测试说话。

### 8.1 安装测试（4 场景 × 3 平台 = 12 条）

| # | 场景 | 预期 | 诊断脚本 |
|---|------|------|---------|
| 1 | Linux 新环境 + Python 3.11 + 有 Go + 有 Node + 有显示器 | `python install.py -y` 后 `install_check.py` 10/10 PASS | scripts/test_matrix/install_full_linux.sh |
| 2 | Linux 容器 + Python 3.12 + 无 Go + 无 Node + 无 DISPLAY | 8/10 PASS（桌宠 headless，API 跳过），exit 0 | scripts/test_matrix/install_minimal_headless.sh |
| 3 | Windows 11 + Python 3.11 + 中文用户名 | install_check 6+/10 能用，无编码错误 | scripts/test_matrix/install_win.ps1 |
| 4 | macOS 14 + M 芯片 + brew 缺 portaudio | 9/10 PASS，skip 提示正确 | scripts/test_matrix/install_macos.sh |

### 8.2 端到端链路测试（6 条）

```
E2E-1: 文本→桌宠
  in:  python -m core.workflow "蓝发猫耳少女" --deploy-desktop --output-dir test_outputs/e2e1
  out: test_outputs/e2e1/ 下存在
         character.png  character.psd  live2d/model.model3.json  pet/state.json
  断言: live2d/model.model3.json 中 "Parameters" 数量 >= 28
         pet/state.json 中 "layers" 数量 >= 12
  失败诊断:
    - 缺 character.png → 看 workflow 日志生成阶段
    - 缺 .psd         → 看 psd_export 阶段的 layer_composer 日志
    - 缺 model3.json  → 看 rigging 阶段 Live2DBuilder 日志

E2E-2: 断点续跑
  1) 运行 E2E-1，在 "optimizing" 阶段 Ctrl+C 中断
  2) 再次运行同命令
  断言: 控制台显示 "Resuming from: layering"，总耗时 < 首次 50%

E2E-3: 桌宠 + 追踪（需要摄像头的机器，可手动测）
  1) python -m drivers.desktop_pet.runner --tracking
  2) 面对摄像头左右转头
  断言: ParamAngleY 实时变化，且 30 FPS 下角速度不突变（滤波生效）

E2E-4: 桌宠 + 聊天 + TTS + 口型
  python -m drivers.desktop_pet.runner --chat --tts
  用户输入 "你好呀！"
  断言:
    - 文本输出流式（能看到逐字）
    - 情感输出 happy (>= 0.6 置信度)
    - 音频播放期间 mouth_open 曲线 > 0.1 时间 ≥ 音频时长×0.6

E2E-5: Go API + Web（需要 Go + Node）
  1) cd api && ./live2d-api &
  2) cd web && npm run dev &
  3) curl http://localhost:8080/api/health  → status:ok
  4) curl http://localhost:8080/api/characters → []
  断言: 浏览器打开 http://localhost:3000/characters 不报错（Dashboard.length 已在上文出现过）

E2E-6: MMDEngine Dancer 行为
  python -m drivers.desktop_pet.runner --behavior mmd_music_dancer \
         --audio assets/audio/sample_bgm.mp3
  断言: ParamBodyAngleX / ParamAngleZ 按节拍变化（FFT 峰值与参数峰值对齐）
```

### 8.3 分层质量 Benchmark

```
BENCH-1: v11 vs v10 vs See-through
  python scripts/benchmark_segmentation.py
  断言: Ours_v11 overall mIoU - Ours_v10 >= +5%
  产物: docs/benchmark_segmentation_report.md (含 CSV + 柱状图)
```

---

## 九、风险评估与降级方案

| 风险 | 概率 | 影响 | 降级方案 |
|------|------|------|---------|
| `part_classifier.onnx` 训练数据不足，准确率不达预期 | 中 | 中 | Phase 1 不启用 Level 3，只用 Level 1+2，Phase 2 补数据 |
| Live2D 参数绑定 28×N 手工定义工作量大 | 高 | 中 | 先只绑定 TOP 12 高频参数：EyeX/Y, EyeLOpen/EyeROpen, MouthOpenY, MouthForm, AngleX/Y/Z, BodyAngleX, Breath。其余 16 参数在 v11.1 补齐 |
| Spine IK 算法 2D 简化版解算不收敛（极端角度） | 低 | 低 | 阈值：CCD 迭代 > 20 次 未收敛 → 跳过本帧 IK 修正，沿用参数原值 |
| Windows/macOS 下 pygame 透明窗口 + 置顶 依然被全屏应用挡 | 中 | 低 | 提供「嵌入桌面」模式：桌宠绘制到桌面壁纸的 Windows ShGetDesktopWindow / macOS NSDesktopWindow，不抢任何层级；但无法接收鼠标点击（纯展示） |
| 安装脚本新增系统依赖预检后，在稀有发行版（Alpine/Gentoo）包名不匹配 | 中 | 低 | 预检失败时输出："SKIP: 无法识别你系统的包管理器，请手动安装 {libgl1, portaudio}；这不会影响核心功能" （不阻断） |
| rembg / mediapipe 在 3.12 长期不发 wheel | 中 | 中 | 提供 Docker 镜像 `live2d-master-agent:v11-py311` 作为推荐方式；install.py 在 3.12 下自动跳过这两个包并输出一行建议（而不是报错） |

---

## 十、验收标准

> 最终产品经理（你）盖章的十条 PASS 条件：

1. **安装成功率**：在全新 Linux 22.04 / Win 11 / macOS 14 三台裸机上各执行 1 次 `python install.py -y` → `install_check.py` **≥ 8/10**（允许桌宠/API 等可选跳过）。
2. **端到端链路**：`python -m core.workflow "猫耳少女" --deploy-desktop` 跑完后产物完整，Live2D 参数 ≥ 28 个，桌宠能启动。
3. **断点续跑**：中途 kill 后重跑，显示 Resuming 且总时长 < 首次 50%。
4. **分层准确率**：benchmark 报告中 v11 整体 mIoU ≥ v10 + 5%。
5. **情感→表情**：`EmotionAnalyzer.analyze("今天开心到飞起！").expression` → `happy`，且 300ms 过渡不硬切。
6. **聊天口型同步**：TTS 音频时长与 mouth_open 曲线的激活区间 ≥ 60% 重合。
7. **MMDEngine Dancer**：播放 BGM 期间身体摆动角度与 BGM 节拍互相关 ≥ 0.5。
8. **Spine IK**：手臂 IK 求解从肩 (0,0)→腕 (100,100)，迭代 ≤ 10 次，误差 ≤ 1px。
9. **UTF-8 兼容**：Windows 中文用户名（路径含 Unicode）下 install.py 不抛编码异常。
10. **诊断可解释**：任意依赖缺失时 `install_check.py` 输出的建议命令直接复制即可修复（不是模糊提示）。

满足以上 **≥ 9/10** 条，v11.0 正式发布，打 tag `v11.0`，并把本报告中 `docs/VERSION_11_UPDATE_REPORT.md` 作为附件与 Release Notes 一同发布。

---

> **文档结束**  
> 本报告为 v11.0 "Unity" 的单一真相来源。任何实施与本报告冲突时，先更新本报告，再改代码。
