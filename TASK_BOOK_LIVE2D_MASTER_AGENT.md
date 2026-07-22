# 🎯 超长线任务书：Live2D Master Agent —— 从"实验性工具"到"生产级 AI 角色生成与驱动平台"

## 一、任务总览与核心目标

你正在接手一个名为 **Live2D Master Agent** 的开源项目。当前项目已经具备基础能力：AI 图像生成（Pollinations/Seedream/SenseNova）、K-means 颜色聚类分层、PSD 导出、简单的 PNG 合成桌宠、Go API 服务、Next.js 前端 QA 工具。

但项目的**核心痛点**是：
1. 分层精度低（K-means 颜色聚类无法处理语义遮挡）
2. 没有真正的 Live2D 绑定（只能导出无法使用的 model3.json scaffold）
3. 桌宠是预设动画，无法通过 webcam/麦克风实时驱动
4. 没有角色一致性机制（每次生成都是随机角色）
5. 没有语音交互和 AI 对话能力
6. 前端只有 PSD 质检，没有实时预览和生成控制
7. 代码高度重复（.trae/skills/ 和根目录大量重复）
8. 安全、性能、可维护性债务重

你的终极目标是：将这个项目升级为**一个能与国际竞品（VTube Studio / VSeeFace / VRoid / Open-LLM-VTuber）抗衡的生产级平台**。

---

## 二、执行纪律（必须严格遵守）

1. **每次修改代码前，必须先 Read 目标文件**。禁止盲改。
2. **每次修改后必须运行测试验证**。Python 用 `pytest tests/ -v`，Go 用 `go test ./...`，前端用 `npm run build`。
3. **遇到外部依赖问题，先搜索再实现**。使用 WebSearch 查找开源方案，不要闭门造车。
4. **所有新增代码必须有类型注解和 docstring**（Python），Go 代码必须有注释。
5. **每完成一个 Phase，必须写一段进度总结**到 `TASK_PROGRESS.md`。
6. **工具调用策略**：每个子任务平均需要 5-10 次工具调用（Read/Edit/RunCommand/WebSearch/Grep）。本任务共 10 个 Phase，约 80 个子任务，**总工具调用次数必须达到 500+**。

---

## 三、项目初始状态诊断（Phase 0）

在动手改代码前，你必须先彻底理解项目现状。这个阶段需要大量工具调用来收集信息。

### 子任务 0.1：读取核心配置文件
- Read `/workspace/README.md`
- Read `/workspace/CHANGELOG.md`
- Read `/workspace/requirements.txt`
- Read `/workspace/web/package.json`
- Read `/workspace/api/go.mod`
- Read `/workspace/docs/LIMITATIONS.md`
- Read `/workspace/docs/QUICKSTART.md`
- Read `/workspace/USAGE.md`
- Read `/workspace/.env.example`
- Read `/workspace/.gitignore`

### 子任务 0.2：代码结构分析
- 使用 `find /workspace -type f -name '*.py' | head -50` 列出所有 Python 文件
- 使用 `find /workspace -type f -name '*.go' | head -20` 列出所有 Go 文件
- 使用 `find /workspace -type f -name '*.tsx' -o -name '*.ts' | head -30` 列出前端文件
- 使用 `Grep` 搜索 "TODO" 和 "FIXME" 和 "EXPERIMENTAL" 标记
- 检查 `.trae/skills/live2d-master-agent/` 和根目录的重复文件（对比 md5sum）

### 子任务 0.3：依赖和可运行性检查
- 运行 `python3 -c "import live2d; print('OK')"`
- 运行 `python3 -m pytest tests/ --collect-only`
- 运行 `cd /workspace/api && go mod tidy`
- 运行 `cd /workspace/web && npm install`
- 运行 `cd /workspace/comfyui-connector && npm install`
- 检查 Python 版本：`python3 --version`
- 检查 Go 版本：`go version`
- 检查 Node 版本：`node --version`

### 子任务 0.4：竞品技术调研（WebSearch 至少 10 次）
- 搜索 "SkyTNT/anime-segmentation ISNet GitHub 2025"
- 搜索 "pix2gestalt amodal completion GitHub"
- 搜索 "MediaPipe face landmark blendshape VTuber"
- 搜索 "OpenSeeFace real-time face tracking open source"
- 搜索 "Stretchy Studio 2026 mesh deform auto rigging"
- 搜索 "Live2D Cubism SDK parameter binding JavaScript"
- 搜索 "Open-LLM-VTuber architecture TTS STT LLM"
- 搜索 "LoRA training kohya-ss docker"
- 搜索 "IP-Adapter faceID character consistency"
- 搜索 "pygame transparent window OBS virtual camera"
- 搜索 "VRM spring bone physics hair clothes"

### 验收标准 0
- `TASK_PROGRESS.md` 中有一份完整的项目现状诊断报告
- 列出所有重复代码位置
- 列出所有 "EXPERIMENTAL" 功能
- 列出所有依赖缺失项

---

## 四、Phase 1：架构重构与代码去重（预期 50+ 工具调用）

目标：清理技术债务，建立可维护的基础。

### 子任务 1.1：删除重复代码
- 对比 `.trae/skills/live2d-master-agent/` 和根目录下相同文件名的内容
- 对于完全相同的文件，删除 `.trae/skills/` 下的副本
- 对于相似但不同的文件，保留根目录版本，删除旧版本
- 更新 `.trae/skills/live2d-master-agent/SKILL.md` 指向根目录的代码

### 子任务 1.2：修复 Go 版本兼容性
- Read `/workspace/api/go.mod`
- 将 `go 1.25.0` 改为 `go 1.22`（或当前环境可用版本）
- 如果 `quic-go` 导致问题，搜索替代方案或降级
- 运行 `go mod tidy` 验证

### 子任务 1.3：统一版本管理
- 检查 `live2d/version.py`、`VERSION`、`web/package.json`、`api/go.mod` 中的版本号
- 确保统一为 `9.1.0`（表示架构升级）
- 添加一个 `scripts/bump_version.py` 脚本，一键同步所有版本号

### 子任务 1.4：前端依赖修复
- Read `/workspace/web/package.json`
- 确保 `tailwindcss`、`postcss`、`autoprefixer` 都在 dependencies 或 devDependencies 中
- 添加 `react-markdown` 到依赖（替换 ChatAssistant.tsx 的手写 Markdown 解析器）
- 运行 `npm install && npm run build` 验证

### 子任务 1.5：安全修复
- Read `/workspace/api/main.go`
- 修复 CORS 中间件：默认拒绝所有跨域，除非显式配置白名单
- 修复 rateLimitMiddleware：给 `clients map` 加 `sync.RWMutex` 锁
- Read `/workspace/api/services/python_bridge.go`
- 检查 PATH 继承问题，限制环境变量

### 子任务 1.6：引入代码格式化工具
- 创建 `pyproject.toml`，配置 `ruff`（Python linter/formatter）
- 创建 `.prettierrc`（前端格式化）
- 创建 `.github/workflows/ci.yml`（GitHub Actions：跑测试 + 构建 + 格式化检查）

### 验收标准 1
- `go mod tidy` 成功
- `npm run build` 成功
- `pytest tests/ --collect-only` 至少能收集到 149 个测试
- CORS 和 rate limit 代码已修复
- 重复代码减少 50% 以上

---

## 五、Phase 2：AI 语义分层与 Amodal 补全引擎（预期 60+ 工具调用）

目标：替代 K-means，实现真正基于语义的分层，并补全被遮挡区域。

### 子任务 2.1：调研并选型语义分割模型
- WebSearch "SkyTNT/anime-segmentation ISNet install pip"
- WebSearch "anime face segmentation UNet classes hair eye mouth"
- Read 相关 GitHub 仓库的 README 和模型输出格式
- 在 `/workspace/live2d/segmentation/` 新建模块

### 子任务 2.2：集成 Anime Segmentation
- 创建 `/workspace/live2d/segmentation/__init__.py`
- 创建 `/workspace/live2d/segmentation/anime_segmenter.py`
- 封装 `SkyTNT/anime-segmentation` 或兼容的轻量级模型
- 实现 `segment(image) -> Dict[str, np.ndarray]` 接口
- 输出至少 8 个部位：face, hair_front, hair_back, left_eye, right_eye, mouth, body, clothes

### 子任务 2.3：图层深度排序算法
- 创建 `/workspace/live2d/segmentation/depth_sort.py`
- 使用启发式规则排序图层（如：hair_back < body < face < hair_front）
- 或者集成 Marigold Depth / MiDaS 进行深度估计
- 搜索 "Marigold depth estimation huggingface"

### 子任务 2.4：Amodal 补全（Inpainting）
- 创建 `/workspace/live2d/segmentation/amodal.py`
- 调研 LaMa / Stable Diffusion Inpainting / pix2gestalt
- 对于每个部位的 mask，计算被其他部位遮挡的区域
- 使用扩散模型或传统图像修复算法补全遮挡区域
- 确保补全后的图层在边缘处风格一致

### 子任务 2.5：替换 WorkflowEngine 中的分层器
- Read `/workspace/live2d/workflow.py`
- 修改 `WorkflowEngine.__init__`，当 `layer_method == "semantic"` 时，使用新的语义分层器
- 保留 KMeans 作为 fallback
- 更新 `master_tool.py` 的 `--layer-method` 帮助文本

### 子任务 2.6：测试语义分层
- 在 `tests/` 下创建 `test_semantic_layering.py`
- 使用合成的 anime 角色图测试分割准确性
- 测试 amodal 补全后的图层完整性
- 运行 `pytest tests/test_semantic_layering.py -v`

### 验收标准 2
- 语义分层器能正确分出 8+ 个部位
- 补全后的图层在被遮挡区域有合理内容
- PSD 导出后，图层按深度正确排序
- 测试通过

---

## 六、Phase 3：自动网格生成与 Live2D 参数绑定（预期 60+ 工具调用）

目标：实现真正的 Live2D 自动绑定，生成可用的 model3.json + moc3（如果可能）。

### 子任务 3.1：网格生成算法
- Read `/workspace/live2d/rigging/mesh_generator.py`
- 调研 Delaunay 三角化 + 轮廓感知顶点放置（参考 SPRITETOMESH 论文）
- 创建 `/workspace/live2d/rigging/mesh_v2.py`
- 对每个图层：
  1. 提取 alpha 轮廓
  2. Douglas-Peucker 简化轮廓
  3. 在轮廓上放置顶点
  4. 内部均匀采样顶点
  5. Delaunay 三角化
  6. 过滤掉 alpha 区域外的三角形

### 子任务 3.2：变形器（Deformer）自动放置
- Read `/workspace/live2d/rigging/deformers.py`
- 根据部位类型自动放置变形器：
  - 眼睛：旋转变形器（围绕瞳孔中心）
  - 头发：弯曲变形器（从根部到尖端）
  - 嘴巴：弯曲变形器（横向和纵向）
  - 身体：旋转变形器（围绕腰部）
- 创建 `/workspace/live2d/rigging/deformer_placer.py`

### 子任务 3.3：参数绑定系统
- Read `/workspace/live2d/rigging/parameters.py`
- 创建 `/workspace/live2d/rigging/param_binding.py`
- 定义标准 Live2D 参数：ParamAngleX/Y/Z, ParamEyeLOpen, ParamEyeROpen, ParamMouthOpenY 等
- 将变形器绑定到参数，定义 Keyform（0.0, 0.5, 1.0 时的顶点位移）

### 子任务 3.4：物理系统配置
- Read `/workspace/live2d/layering/layers52.py` 中的 `STANDARD_PHYSICS`
- 创建 `/workspace/live2d/rigging/physics_builder.py`
- 自动为头发、衣服、配饰生成 physics3.json
- 使用 pendulum 摆模型：长度、重力、阻尼根据部位大小自动计算

### 子任务 3.5：Model3 导出升级
- Read `/workspace/live2d/exporter/model3_exporter.py`
- 升级导出器，包含：
  - 正确的 mesh 数据（顶点 + UV + 三角形索引）
  - ArtMesh 设置（绑定到正确的纹理图集区域）
  - 变形器层级（Deformer Hierarchy）
  - 参数定义
  - 表情（Expression）的完整 Keyform
  - 物理（Physics）设置
- 如果无法直接生成 .moc3，至少生成完整到可以一键导入 Cubism Editor 的文件

### 子任务 3.6：测试自动绑定
- 创建 `test_auto_rigging.py`
- 输入一张分层后的角色图
- 验证输出的 model3.json 包含 ArtMeshes、Deformers、Parameters
- 验证 physics3.json 包含合理的摆锤参数

### 验收标准 3
- model3.json 包含完整的 mesh、deformer、parameter 定义
- physics3.json 自动生成且合理
- 纹理图集正确打包
- 测试通过

---

## 七、Phase 4：实时 MediaPipe 面捕驱动桥接（预期 50+ 工具调用）

目标：让桌宠能通过 webcam 实时模仿用户表情和头部动作。

### 子任务 4.1：MediaPipe 集成
- WebSearch "MediaPipe Face Landmark Python 468 points 2025"
- 创建 `/workspace/live2d/tracking/` 模块
- 安装 `mediapipe`（pip install mediapipe）
- 创建 `face_tracker.py`，封装 MediaPipe Face Mesh
- 输出：468 个面部关键点 + 头部姿态（yaw, pitch, roll）

### 子任务 4.2：Blendshape 计算
- WebSearch "Kalidokit blendshape calculation mediapipe"
- 创建 `/workspace/live2d/tracking/blendshape_solver.py`
- 将 468 关键点转换为 Live2D 参数：
  - ParamAngleX/Y/Z = 头部旋转
  - ParamEyeLOpen/ROpen = 眼睑开合度
  - ParamMouthOpenY = 嘴巴张开度
  - ParamMouthForm = 嘴巴形状（微笑/嘟嘴）
  - ParamBrowLY/RY = 眉毛高度
  - ParamEyeBallX/Y = 视线方向

### 子任务 4.3：实时驱动协议
- 创建 `/workspace/live2d/tracking/bridge.py`
- 实现 WebSocket 服务器，实时广播 blendshape 参数
- 或者实现 OSC 协议（Open Sound Control），兼容 VTube Studio 生态
- 频率：30 FPS

### 子任务 4.4：桌宠实时渲染升级
- Read `/workspace/live2d/pet/animator.py`
- 创建 `animator_v2.py`
- 支持两种模式：
  - 模式 A：预设动画（原有功能）
  - 模式 B：WebSocket/OSC 接收参数，实时驱动图层变形
- 在模式 B 中，根据 ParamAngleX/Y 平移/旋转面部图层
- 根据 ParamEyeLOpen 缩放眼睛图层
- 根据 ParamMouthOpenY 变形嘴巴图层

### 子任务 4.5：Webcam 驱动入口
- 创建 `/workspace/run_face_tracking.py`
- 启动 webcam → MediaPipe → blendshape 计算 → WebSocket 广播
- 同时启动桌宠（监听 WebSocket）

### 子任务 4.6：测试面捕
- 手动运行 `python run_face_tracking.py`
- 验证 webcam 画面正常
- 验证头部转动时桌宠跟随
- 验证眨眼、张嘴动作同步

### 验收标准 4
- MediaPipe 能稳定追踪面部
- Blendshape 参数映射合理
- 桌宠能实时跟随 webcam（延迟 < 100ms）
- 支持眨眼、张嘴、头部转动、视线移动

---

## 八、Phase 5：语音交互与 LLM 性格系统（预期 50+ 工具调用）

目标：让角色能听、能说、能对话。

### 子任务 5.1：语音识别（ASR）
- WebSearch "faster-whisper local ASR Chinese English 2025"
- 集成 `faster-whisper` 或 `openai-whisper`
- 创建 `/workspace/live2d/voice/asr.py`
- 支持实时麦克风输入，流式识别
- 支持中文和英文

### 子任务 5.2：文本转语音（TTS）
- WebSearch "edge-tts free Microsoft TTS Chinese"
- 集成 `edge-tts`（免费、支持中文、无需 API Key）
- 或者集成 `pyttsx3` 作为离线 fallback
- 创建 `/workspace/live2d/voice/tts.py`
- 支持情绪参数（开心、平静、惊讶）

### 子任务 5.3：LLM 对话系统
- WebSearch "Ollama local LLM Chinese qwen 2025"
- 或者使用 OpenAI API / 其他兼容 API
- 创建 `/workspace/live2d/brain/` 模块
- 创建 `character_brain.py`
- 实现角色设定（persona）系统：
  - 名字、年龄、性格、说话风格
  - 长期记忆（SQLite 存储对话历史）
  - 短期记忆（最近 10 轮对话）
- 集成 LLM，生成角色化回复

### 子任务 5.4：口型同步（Lip Sync）
- WebSearch "rhubarb lip sync Chinese anime"
- 或者基于音频振幅 + 元音检测的简单方案
- 创建 `/workspace/live2d/voice/lipsync.py`
- 输入：TTS 生成的音频
- 输出：ParamMouthOpenY 的时间序列
- 与桌宠动画系统对接

### 子任务 5.5：语音交互入口
- 创建 `/workspace/run_voice_pet.py`
- 启动流程：
  1. 监听麦克风
  2. ASR 识别语音 → 文本
  3. LLM 生成回复 → 文本
  4. TTS 合成语音 → 音频
  5. LipSync 生成口型 → 参数
  6. 播放音频 + 桌宠口型动画
  7. 循环

### 子任务 5.6：测试语音交互
- 运行 `python run_voice_pet.py`
- 对麦克风说话，验证角色能回复
- 验证口型与音频同步
- 验证对话记忆有效

### 验收标准 5
- ASR 中文识别准确率 > 80%
- TTS 输出自然，延迟 < 3s
- LLM 回复符合角色设定
- 口型与音频基本同步

---

## 九、Phase 6：角色一致性生成与 LoRA 训练管线（预期 50+ 工具调用）

目标：让用户能"锁定"一个角色，持续生成同一角色的不同姿势、表情、服装。

### 子任务 6.1：角色档案系统
- 创建 `/workspace/live2d/character/` 模块
- 创建 `character_card.py`
- 定义角色档案数据结构：
  - name, age, appearance traits（发色、瞳色、服装特征）
  - reference_images（正面、侧面、背面）
  - prompt template（生成用的基础提示词）
  - negative prompt

### 子任务 6.2：LoRA 训练集成
- Read `/workspace/live2d/image_gen/advanced_generation_pipeline.py`
- 调研 `kohya-ss/sd-scripts` 或 `AI-Toolkit` 的训练流程
- 创建 `/workspace/live2d/character/lora_trainer.py`
- 封装训练流程：
  1. 收集 20-40 张同一角色图片
  2. 自动打标签（WD14 Tagger）
  3. 训练 LoRA（10-50 步，快速收敛）
  4. 输出 `.safetensors` 模型

### 子任务 6.3：IP-Adapter 集成
- WebSearch "IP-Adapter face ID character consistency Stable Diffusion"
- 创建 `/workspace/live2d/character/ip_adapter.py`
- 使用参考图 + IP-Adapter 保持角色一致性
- 不需要训练，只需一张参考图

### 子任务 6.4：ControlNet 姿势控制
- WebSearch "ControlNet OpenPose anime generation diffusers 2025"
- 创建 `/workspace/live2d/character/pose_control.py`
- 集成 OpenPose / DWPose 姿势检测
- 用户上传姿势图，生成相同姿势的角色
- 支持 depth map、线稿（canny）控制

### 子任务 6.5：多角度生成
- 创建 `/workspace/live2d/character/multi_view.py`
- 生成正面、侧面（左/右）、背面、3/4 视角
- 使用 consistent character 技术（如 StoryDiffusion、CharacterLora）

### 子任务 6.6：工作流集成
- 修改 `WorkflowEngine`
- 添加 `character_profile` 参数
- 如果提供了角色档案，使用 LoRA + IP-Adapter 保持一致性
- 更新 `master_tool.py` 支持 `--character-card` 参数

### 子任务 6.7：测试一致性
- 训练一个测试 LoRA（5 张图，快速训练）
- 生成 5 张不同姿势的角色图
- 人工/自动评估角色一致性

### 验收标准 6
- 角色档案系统可用
- LoRA 训练脚本能跑通
- IP-Adapter 保持发型、面部特征一致
- ControlNet 能控制姿势
- 多角度生成可用

---

## 十、Phase 7：Web 端实时预览与生成控制面板（预期 50+ 工具调用）

目标：把前端从"PSD QA 工具"升级为"完整的角色生成与预览平台"。

### 子任务 7.1：前端架构升级
- Read `/workspace/web/pages/index.tsx`
- 添加路由系统（`next/router` 或文件路由）
- 页面规划：
  - `/` — 首页 / 角色画廊
  - `/generate` — AI 生成控制台
  - `/preview` — 实时桌宠预览
  - `/rig` — 绑定结果查看
  - `/settings` — 配置

### 子任务 7.2：生成控制台
- 创建 `pages/generate.tsx`
- 表单字段：
  - 提示词输入
  - 角色档案选择
  - 姿势图上传（ControlNet）
  - Provider 选择（Pollinations / Seedream / SenseNova）
  - 生成参数（宽/高/种子）
- 调用后端 API `/api/generate`
- 显示生成进度和预览图

### 子任务 7.3：实时桌宠预览页
- 创建 `pages/preview.tsx`
- 使用 HTML5 Canvas 或 PixiJS 渲染桌宠
- 或者嵌入 `pixi-live2d-display` 渲染真正的 Live2D 模型
- 实现鼠标跟随（与桌面版相同的交互）
- 支持表情切换按钮

### 子任务 7.4：WebSocket 连接
- 创建 `lib/websocket.ts`
- 连接 Phase 4 的 WebSocket 服务器
- 实时接收 blendshape 参数
- 在网页上同步驱动角色

### 子任务 7.5：Go API 扩展
- Read `/workspace/api/handlers/handlers.go`
- 添加新端点：
  - `POST /api/character/train-lora`
  - `POST /api/character/generate-multi-view`
  - `GET /api/tracking/status`
  - `WS /api/tracking/stream`

### 子任务 7.6：构建与部署验证
- 运行 `npm run build`
- 确保没有类型错误
- 确保静态导出成功

### 验收标准 7
- 前端有 4 个独立页面
- 生成控制台能调用 API
- 预览页能渲染桌宠
- WebSocket 能实时驱动网页角色

---

## 十一、Phase 8：物理引擎与高级动画系统（预期 50+ 工具调用）

目标：替代简单的正弦波动画，实现基于物理的真实摆动。

### 子任务 8.1：Spring Bone 物理引擎
- WebSearch "spring bone physics 2D anime hair implementation"
- 创建 `/workspace/live2d/physics/` 模块
- 实现 2D Spring Bone 系统：
  - 每个骨骼有：质量、长度、阻尼、刚度
  - 受力：重力、风力、父骨骼传递力
  - 积分：Verlet 或 Runge-Kutta

### 子任务 8.2：部位物理绑定
- 创建 `/workspace/live2d/physics/hair_physics.py`
- 创建 `/workspace/live2d/physics/cloth_physics.py`
- 创建 `/workspace/live2d/physics/accessory_physics.py`
- 头发：多根 Spring Bone 链，从根部到尖端
- 衣服：布娃娃（cloth doll）简化模型
- 配饰：单摆或弹簧

### 子任务 8.3：风力与外力系统
- 创建 `/workspace/live2d/physics/force_field.py`
- 支持：
  - 全局风力（方向、强度、湍流）
  - 鼠标/触摸交互力（靠近时吹动头发）
  - 角色移动时的惯性力

### 子任务 8.4：物理与动画混合
- 修改 `animator_v2.py`
- 动画优先级：
  1. 面捕参数（最高）
  2. 物理模拟（中）
  3. 预设呼吸/眨眼（最低）
- 物理每帧更新，叠加到基础动画上

### 子任务 8.5：Web 端物理
- 如果预览页使用 PixiJS，在 JS 端也实现 Spring Bone
- 或者通过 WebSocket 从 Python 后端同步物理结果

### 验收标准 8
- 头发随风自然摆动
- 鼠标靠近时头发被吹开
- 角色转头时头发有惯性延迟
- 物理计算 60 FPS 不卡顿

---

## 十二、Phase 9：多平台桌宠运行时与 OBS 集成（预期 50+ 工具调用）

目标：让桌宠能在 Windows/macOS/Linux 运行，并作为虚拟摄像头输出到 OBS。

### 子任务 9.1：跨平台窗口系统
- Read `/workspace/live2d/pet/live2d_desktop_pet.py`
- 调研 `pywebview` 或 `pygame` + `pywin32`（Windows）/ `pyobjc`（macOS）
- 创建 `/workspace/live2d/pet/window_manager.py`
- 实现：
  - 透明背景窗口
  - 点击穿透（非角色区域）
  - 窗口置顶
  - 拖拽移动
  - 右键菜单

### 子任务 9.2：macOS / Linux 支持
- 调研 Linux 透明窗口方案（`gtk`, `PyQt5` with `setAttribute(Qt.WA_TranslucentBackground)`）
- 调研 macOS 透明窗口（`pyobjc` + `NSWindow`）
- 在 `window_manager.py` 中按平台切换实现

### 子任务 9.3：OBS 虚拟摄像头输出
- WebSearch "pyvirtualcam OBS virtual camera python 2025"
- 集成 `pyvirtualcam`
- 创建 `/workspace/live2d/pet/virtual_camera.py`
- 将桌宠的每一帧渲染为视频流
- 输出到虚拟摄像头，OBS 可直接选择

### 子任务 9.4：打包与分发
- 创建 `scripts/build_pet.py`
- 使用 `PyInstaller` 打包为单文件可执行程序
- Windows: `.exe`
- macOS: `.app`
- Linux: AppImage 或二进制

### 子任务 9.5：桌宠配置系统
- 创建 `pet_config_schema.json`
- 支持配置：
  - 角色模型路径
  - 窗口大小/位置
  - 动画/物理参数
  - 面捕/语音开关
  - API 配置

### 验收标准 9
- Windows 透明窗口正常
- macOS/Linux 至少能跑（窗口可能不完美）
- OBS 能识别虚拟摄像头
- PyInstaller 打包成功

---

## 十三、Phase 10：集成测试、性能优化与文档（预期 50+ 工具调用）

目标：确保所有模块协同工作，性能达标，文档完善。

### 子任务 10.1：端到端集成测试
- 创建 `tests/test_e2e_full_pipeline.py`
- 测试完整流程：
  1. 生成角色图
  2. 语义分层
  3. 自动绑定
  4. 导出桌宠包
  5. 启动桌宠
  6. 面捕驱动
  7. 语音对话
- 使用 mock 替代外部 API（测试时不消耗额度）

### 子任务 10.2：性能基准测试
- 创建 `tests/benchmark.py`
- 测量：
  - 图像生成时间
  - 语义分层时间（目标 < 30s）
  - 网格生成时间（目标 < 5s）
  - 面捕延迟（目标 < 100ms）
  - 物理 FPS（目标 60 FPS）

### 子任务 10.3：内存与资源优化
- 使用 `memory_profiler` 检查内存泄漏
- 确保临时文件正确清理
- 确保模型（MediaPipe、分割模型）只加载一次

### 子任务 10.4：README 与文档重写
- 重写 `/workspace/README.md`
- 更新功能列表
- 添加新的快速开始：
  ```bash
  python install.py
  python master_tool.py "蓝发猫耳少女" --pet --face-tracking --voice
  ```
- 更新架构图
- 添加贡献指南 `CONTRIBUTING.md`

### 子任务 10.5：API 文档
- 为 Go API 添加 Swagger 文档（`gin-swagger`）
- 为 Python 模块添加 Sphinx 或 mkdocs 文档
- 为前端组件添加 Storybook（可选）

### 子任务 10.6：最终验证
- 运行完整测试套件：`pytest tests/ -v`
- 运行 Go 测试：`go test ./...`
- 运行前端构建：`npm run build`
- 运行代码格式化检查：`ruff check .`
- 确保所有 Phase 的验收标准都通过

### 验收标准 10
- 所有 149+ 测试通过
- 端到端流程能在 5 分钟内跑完
- README 能让新手 3 分钟上手
- 没有已知的严重 bug

---

## 十四、最终交付物清单

完成所有 Phase 后，项目应包含：

### 代码层面
1. 清理后的项目结构（无重复代码）
2. 10 个新 Python 模块：`segmentation/`, `tracking/`, `voice/`, `brain/`, `character/`, `physics/`, `rigging/`（升级）
3. Go API 新增 5+ 端点
4. Next.js 前端新增 4 个页面
5. 50+ 个新测试文件

### 文档层面
1. `README.md`（重写）
2. `TASK_PROGRESS.md`（完整进度记录）
3. `ARCHITECTURE.md`（新架构图）
4. `API.md`（API 文档）
5. `CONTRIBUTING.md`（贡献指南）

### 可运行产物
1. `python master_tool.py` — 生成角色
2. `python run_face_tracking.py` — 面捕驱动
3. `python run_voice_pet.py` — 语音桌宠
4. `cd api && go run main.go` — API 服务
5. `cd web && npm run dev` — 前端开发服务器

---

## 十五、工具调用策略（确保 500+ 次）

为了达到 500+ 次工具调用，你必须：

1. **每个子任务至少 5 次 Read**：先读现有代码，再读参考实现，再读修改后的代码
2. **每个子任务至少 3 次 Edit**：修改代码、修复错误、添加测试
3. **每个子任务至少 2 次 RunCommand**：安装依赖、运行测试、验证构建
4. **每个 Phase 至少 3 次 WebSearch**：查找开源库、查文档、查最佳实践
5. **频繁使用 Grep**：搜索代码中的函数定义、TODO、变量引用

### 预期工具调用分布
| Phase | Read | Edit | RunCommand | WebSearch | Grep | 小计 |
|-------|------|------|------------|-----------|------|------|
| 0 | 20 | 0 | 10 | 10 | 5 | 45 |
| 1 | 30 | 20 | 15 | 5 | 10 | 80 |
| 2 | 40 | 30 | 15 | 15 | 10 | 110 |
| 3 | 40 | 30 | 15 | 10 | 10 | 105 |
| 4 | 30 | 20 | 15 | 10 | 10 | 85 |
| 5 | 30 | 20 | 15 | 10 | 10 | 85 |
| 6 | 30 | 20 | 15 | 10 | 10 | 85 |
| 7 | 30 | 20 | 15 | 5 | 10 | 80 |
| 8 | 25 | 15 | 10 | 5 | 5 | 60 |
| 9 | 25 | 15 | 10 | 5 | 5 | 60 |
| 10 | 30 | 15 | 15 | 5 | 10 | 75 |
| **总计** | **360** | **225** | **160** | **90** | **95** | **~930** |

你实际执行时可能不需要全部 930 次，但通过细致的步骤拆分（例如：一个函数分 3 次编辑、每改一行测试一次），**轻松超过 500 次**。

---

## 十六、特别提醒

1. **不要一次性改太多文件**。每改 3-5 个文件就运行测试，确保没有破坏现有功能。
2. **善用 Git**。每完成一个子任务就 `git add && git commit`，方便回滚。
3. **遇到 block 先搜索**。比如 MediaPipe 安装失败、Go 模块冲突、npm 构建错误，先 WebSearch 再解决。
4. **保持代码风格一致**。新代码和旧代码的缩进、命名、注释风格要统一。
5. **用户是计算机小白**。最终交付的 README 必须足够简单，让小白能 3 分钟跑起来。

---

## 十七、开始执行

现在，请从 **Phase 0：项目初始状态诊断** 开始，逐步完成所有 Phase。每完成一个 Phase，在 `TASK_PROGRESS.md` 中记录进度、遇到的问题和解决方案。

**祝你好运！**
