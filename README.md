# 🎭 Live2D Master Agent v9.0

> **从一句话描述到可动 Live2D 角色，全程 AI 驱动的完整端到端生产线。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![Version](https://img.shields.io/badge/version-v9.0.0-purple.svg)]()
[![Tests](https://img.shields.io/badge/tests-279%20passed-brightgreen.svg)]()
[![Rigging](https://img.shields.io/badge/Auto--Rigging-Phase%20✅-ff69b4.svg)]()
[![Cubism 5](https://img.shields.io/badge/Cubism-5.x-ff8c00.svg)]()

---

## ✨ 这是什么？

**Live2D Master Agent 是国内首个开源的 AI 驱动 Live2D 全自动生成工具链。**

输入一句角色描述或一张图片，AI 自动完成：图像生成 → 背景去除 → K-means 颜色聚类分层 → 52 层 Cubism 标准映射 → **自动 ArtMesh 网格生成 → 自动 Warp Deformer 层级构建 → model3.json 导出** → PSD 导出 → 桌面桌宠一键部署。

**一句话说明**：从文案到可动 Live2D 模型，**3 分钟搞定**。

### 🎯 适合谁用？

| 人群 | 痛点 | 我们的方案 |
|---|---|---|
| VTuber / 虚拟主播 | 找画师+建模师太贵、周期长 | AI 一键生成，当天出道 |
| Live2D 建模师 | 拆层、拉网格太机械 | AI 做粗模，你做精修 |
| 独立游戏开发者 | 需要大量 Live2D NPC | 批量生成，统一风格 |
| 桌宠爱好者 | 想要专属桌宠但不会建模 | 一键生成，双击运行 |
| 技术美术 | 想探索 AI + Live2D 工作流 | 完整开源，可二次开发 |

---

## 🚀 三分钟上手

```bash
# 1. 安装依赖
python3 install.py

# 2. 一句话生成角色 + 自动拆层 + 自动Rigging
python3 master_tool.py "蓝发猫耳少女，白色背景" --rig

# 3. 或者用已有图片端到端处理
python3 master_tool.py --input character.png --layer-only --rig
```

> 💡 默认使用 **Pollinations 免费图像生成**，无需 API Key，开箱即用。
> 支持 **火山 Seedream / SenseNova** 等多家 Provider 切换。

---

## 🏆 核心功能

### Phase 1 ✅ 已发布：图像 → 分层 → PSD → 桌宠

| 功能 | 说明 |
|------|------|
| **🤖 AI 角色生成** | 中英文描述 → 立绘，支持 Pollinations / Seedream / SenseNova 三家 Provider |
| **🎨 智能图层拆分** | K-means v6 颜色聚类，自动拆分成头发/脸部/身体/衣服等独立图层 |
| **📄 PSD 导出** | 生成 Adobe Photoshop 原生多图层 PSD，直接拖进 Cubism Editor |
| **📐 52 层标准映射** | 自动映射到 Live2D Cubism 官方 52 层标准结构 |
| **⚙️ Cubism 配置** | 自动生成 parameters.json / physics3.json / 表情文件 |
| **🐱 桌面桌宠** | 一键打包为桌面宠物，Windows / macOS / Linux 三端支持 |
| **🔍 质量评估** | AI 质检图像质量，自动识别模糊、色差、构图问题 |
| **🛡️ 安全加固** | Fernet 加密存储、路径防护、PSD 炸弹防护、日志脱敏 |

### Phase 2 ✅ 已发布：自动 Rigging（本项目核心亮点）⭐⭐⭐

| 功能 | 说明 |
|------|------|
| **🔺 自动 ArtMesh** | 基于轮廓提取 + Delaunay 三角剖分，自动生成三角形网格 |
| **🌳 Warp Deformer 树** | 自动构建 Root → Head/Body → Face/Hair/Eye/Mouth 多层变形器层级 |
| **📊 16+ 标准参数** | 自动生成 ParamAngleX/Y/Z、EyeOpen、MouthOpen 等标准 Live2D 参数 |
| **🗂️ 多页纹理图集** | shelf-packing 算法，自动分页打包，支持超大图层 |
| **📦 model3.json 导出** | 输出 Cubism 5.x 兼容的 model3.json + 多张纹理 + physics3.json |
| **😀 表情自动生成** | 内置 smile / surprised / angry 三种表情模板 |
| **📝 mesh_guide.json** | 生成网格元数据指南，方便后续手动调整 |

### Phase 3 🔮 规划中：语义分割 + Amodal + 口型同步 + Web运行时

- 🔍 **AI 语义分割**：用 ISNet/UNet 替代 K-means，精准识别头发/眼睛/嘴巴部件
- 🧩 **Amodal 补全**：自动补全被遮挡的后发、身体背面，达到真·分层效果
- 👄 **ARKit 52 口型同步**：语音驱动 52 个 blendshape，远超原生 2 参数
- 🌐 **Web 运行时**：集成 pixi-live2d-display，浏览器实时预览

---

## 🎮 五种使用方式

### 1. 命令行一站式（最快）

```bash
# 文本生成角色 + 自动分层 + 自动Rigging
python3 master_tool.py "粉色长发的魔法少女" --rig

# 已有图片 → 分层 + Rigging
python3 master_tool.py --input my_character.png --layer-only --rig

# 列出可用 Provider
python3 master_tool.py --list-providers
```

### 2. 交互式 Agent（新手友好）

```bash
python3 live2d_agent.py
```

```text
╔══════════════════════════════════╗
║  Live2D Master Agent v9.0       ║
╠══════════════════════════════════╣
║  [1] 生成角色                    ║
║  [2] 拆分图层                    ║
║  [3] 自动 Rigging               ║
║  [4] 部署桌宠                    ║
║  [5] 一键完成全部流程            ║
║  [0] 退出                        ║
╚══════════════════════════════════╝
```

### 3. 端到端工作流引擎

```python
from live2d.workflow import WorkflowEngine

engine = WorkflowEngine(output_dir="./output")
result = engine.run(
    prompt="银发狐妖少女",
    generate_52_config=True,    # 生成52层标准 + 自动Rigging
    deploy_desktop=True,        # 同时生成桌宠
)
print(result["steps"]["rigging"]["model3_json"])
```

### 4. Web UI 可视化工具

```bash
cd web && npm install && npm run dev
```

浏览器打开 `http://localhost:3000`，功能包括：
- 🖼️ 图片上传 → PSD 在线转换
- 🌳 图层树可视化检查
- ✅ Live2D 规范合规性检测
- 📊 QA 质检结果面板
- 📈 工作流进度追踪

### 5. Go API 服务

```bash
cd api && go run main.go
# POST /api/generate  { prompt, options }
# POST /api/layer     { image_base64, k_clusters }
# POST /api/rig       { layers }
```

### 6. Trae IDE Skill（开发者）

在 Trae IDE 中加载 `.trae/skills/live2d-master-agent/`，自然语言调用：

> "帮我生成一个蓝发猫娘 Live2D 角色，然后自动 rigging"

---

## 📦 运行后你会得到什么？

```text
output/
├── layers_<timestamp>/
│   ├── optimized_*.png             # 去背景优化原图
│   ├── layer_000.png ~ layer_NNN.png  # 拆分后的独立图层（RGBA）
│   ├── preview.png                 # 图层叠加预览
│   ├── character.psd               # Photoshop 多图层文件
│   ├── layer_mapping.json          # 52层标准映射
│   ├── parameters.json             # Cubism 参数定义
│   ├── physics3.json               # 物理效果配置
│   └── 52_LAYER_GUIDE.txt          # 52层参考指南
│
├── rigged_<timestamp>/             # ⭐ 自动 Rigging 输出
│   ├── character.model3.json       # Cubism model3.json
│   ├── character.texture_00.png    # 纹理图集（多页）
│   ├── character.texture_01.png
│   ├── character.physics3.json     # 物理配置
│   ├── mesh_guide.json             # 网格元数据
│   ├── README_RIGGING.txt          # 使用说明
│   └── expressions/                # 表情文件
│       ├── smile.exp3.json
│       ├── surprised.exp3.json
│       └── angry.exp3.json
│
└── pet_packages/<name>/            # 桌面桌宠包
    ├── run_pet.py                  # 双击运行
    ├── pet_config.json             # 动画配置
    └── layers/                     # 图层素材
```

---

## 🛠️ 技术架构

```
Live2D Master Agent v9.0
├── 🐍 Python 核心（live2d/）
│   ├── workflow.py              # 状态机工作流引擎（12个状态）
│   ├── image_gen/               # 图像生成路由（3家Provider）
│   │   ├── pollinations.py      # 免费 Provider
│   │   ├── seedream.py          # 火山 Seedream
│   │   └── sensenova.py         # SenseNova
│   ├── layering/                # 图层拆分与标准映射
│   │   ├── kmeans.py            # K-means v6 分层
│   │   ├── layers52.py          # 52层标准 + 参数 + 物理
│   │   └── part_identifier.py   # 部件识别
│   ├── rigging/                 # ⭐ 自动 Rigging（Phase 2）
│   │   ├── mesh_generator.py    # Delaunay三角剖分 + 轮廓提取
│   │   ├── deformers.py         # Warp Deformer 层级树
│   │   ├── parameters.py        # 16+ Live2D标准参数
│   │   └── pipeline.py          # Rigging 编排流水线
│   ├── exporter/                # ⭐ 导出器（Phase 2）
│   │   ├── texture_atlas.py     # 多页 shelf-packing 纹理图集
│   │   └── model3_exporter.py   # Cubism model3.json 导出
│   ├── psd/                     # PSD 生成/解析/校验
│   ├── pet/                     # 桌面桌宠
│   ├── qa/engine.py             # 图像质量评估
│   ├── security.py              # 安全校验
│   └── secure_storage.py        # Fernet 加密存储
│
├── 🔷 Go API（api/）              # Gin 框架 REST API
│   ├── handlers/                 # HTTP 接口层
│   ├── services/                 # Python 桥接 + 缓存
│   └── config/                   # 动态配置
│
├── ⚛️ Next.js 前端（web/）        # React + Tailwind
│   ├── components/               # AI配置面板 / 图层树 / QA面板
│   ├── pages/                    # 首页 / 上传 / 结果
│   └── rules/                    # 8类验证规则引擎
│
├── 📘 TypeScript 工作流（lib/）   # 8步流水线类型定义
│   └── steps/                    # 01概念 → 02图生 → ... → 08Rigging
│
├── 🎨 ComfyUI Connector           # ComfyUI 集成服务
│
├── 🧪 测试（tests/）              # 279 项测试
│   ├── test_mesh_generator.py     # MeshGenerator 暴力测试（23项）
│   ├── test_deformers_parameters.py  # Deformer + 参数测试（29项）
│   ├── test_texture_atlas.py      # 纹理图集测试（22项）
│   ├── test_model3_exporter.py    # 导出器测试（27项）
│   ├── test_rigging_pipeline.py   # 端到端测试（16项）
│   ├── test_cli_workflow_rigging.py  # CLI+集成测试（13项）
│   └── ...
│
├── 📚 文档（docs/）               # 快速入门 / 最佳实践 / FAQ
├── 📝 脚本（scripts/）            # 命名助手 / 层检查 / 参数设计
├── 🎯 示例（examples/）           # VTuber / 猫娘 / 发片案例
└── 🔌 .trae/skills/              # Trae IDE Skill 插件
```

### 状态机流水线

```
idle → generating → qa_check → optimizing → layering → rigging → psd_export
                                                                     ↓
                                                              mapping → pet_deploy → done
                                                                     ↓
                                                                  error（自动清理临时文件）
```

---

## 🔧 配置 API Key（可选）

默认免费方案无需配置。如需更高质量，复制 `.env.example` 为 `.env` 并填写：

```env
# 火山引擎 ARK / Seedream（可选，高质量生成）
ARK_API_KEY=your-api-key-here
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3

# SenseNova（可选）
SENSENOVA_KEY_ID=your-key-id
SENSENOVA_KEY_SECRET=your-key-secret

# 输出目录
OUTPUT_DIR=./output

# Go API 服务端口
GO_API_PORT=8080
```

---

## 📋 环境要求

| 组件 | 最低版本 | 推荐版本 |
|------|----------|----------|
| Python | 3.8 | 3.11 / 3.12 |
| Node.js | 18 | 20 LTS |
| Go（API服务） | 1.20 | 1.22 |
| 操作系统 | Windows / macOS / Linux | — |

**自动安装的核心依赖**：
Pillow、numpy、opencv-python、scipy、requests、psd-tools、scikit-learn、cryptography、rich、pygame（桌宠）

---

## 🧪 测试

项目包含 **279 项自动化测试**，全部无需真实 API Key：

```bash
# 全量测试
python3 -m pytest tests/ -v

# 只跑 Rigging 相关测试
python3 -m pytest tests/test_mesh_generator.py tests/test_rigging_pipeline.py -v
```

> **暴力测试覆盖**：1x1像素 / 全透明 / 共线点崩溃 / 多页纹理分页 / 1024×1024大图 / L形U形环形 / 特殊字符层名 / 共线点QhullError防护 / ...

---

## 🛡️ 安全设计

| 防护 | 实现方式 |
|------|----------|
| **加密存储** | Fernet (AES-128-CBC + HMAC-SHA256) + PBKDF2-HMAC-SHA256 密钥派生 |
| **路径防护** | 禁止 `..`、空字节、危险字符，防止目录遍历攻击 |
| **PSD 防护** | 校验魔数、尺寸上限、图层数量，防止 zip bomb |
| **提示词清洗** | 过滤 `rm -rf`、`eval`、`exec` 等危险注入模式 |
| **日志脱敏** | 自动隐藏 `sk-*`、Bearer Token、JWT 等敏感信息 |

详见 [SECURITY.md](.trae/skills/live2d-master-agent/SECURITY.md)

---

## 📖 文档导航

| 文档 | 内容 |
|------|------|
| [快速入门](docs/QUICKSTART.md) | 5分钟跑通全流程 |
| [完整使用说明](USAGE.md) | 所有命令和参数详解 |
| [用户指南](docs/USER_GUIDE.md) | 从入门到精通 |
| [最佳实践](docs/BEST_PRACTICES.md) | 出高质量结果的技巧 |
| [常见问题](docs/FAQ.md) | 遇到问题先看这里 |
| [Rigging 指南](docs/RIGGING_GUIDE.md) | 自动 Rigging 原理与调优 |
| [更新日志](CHANGELOG.md) | 版本迭代历史 |

---

## 🤝 相关项目与生态

### 我们参考/推荐的开源项目

- **[Textoon](https://github.com/Human3DAIGC/Textoon)** — 阿里通义实验室，学术界首个文生 Live2D 系统
- **[Qwen-Image-Layered](https://qwenlayered.com/)** — 阿里 Qwen，图像分层 + Amodal 补全一站式
- **[Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber)** — AI VTuber 完整框架
- **[UniRig](https://github.com/VAST-AI-Research/UniRig)** — 3D 自动 Rigging，思路可迁移到 2D
- **[anime-segmentation](https://github.com/SkyTNT/anime-segmentation)** — 动漫角色语义分割
- **[pixi-live2d-display](https://www.npmjs.com/package/@naari3/pixi-live2d-display)** — Web 运行时
- **[awesome-digital-human-live2d](https://github.com/wan-h/awesome-digital-human-live2d)** — 最全资源索引

---

## 📈 路线图

```
✅ Phase 1 (v6-v8)  — 图像生成 + K-means分层 + PSD导出 + 52层映射 + 桌宠
✅ Phase 2 (v9.0)   — 自动ArtMesh + Warp Deformer树 + model3.json导出 + 暴力测试
🔮 Phase 3          — AI语义分割 + Amodal补全 + ARKit口型同步 + Web运行时
🔮 Phase 4          — 语音驱动 + 表情识别 + 实时动捕 + MCP 接入
🔮 Phase 5          — 云端部署 + 模型市场 + 协作功能
```

---

## ⭐ 项目亮点

- **🆓 开箱即用**：默认 Pollinations 免费生成，零配置跑通全流程
- **🇨🇳 中文友好**：CLI、Agent、提示词、文档全中文支持
- **🛡️ 安全可靠**：Fernet 加密、路径防护、PSD 炸弹防护、日志脱敏
- **🧪 测试完善**：279 项自动化测试，覆盖边界情况与暴力测试
- **🔧 多入口**：CLI + Agent + Web UI + Go API + Trae Skill 五种使用方式
- **🎯 真·自动 Rigging**：国内开源少有的完整自动网格 + Deformer 方案
- **📦 Cubism 5.x 兼容**：输出标准 model3.json，直接导入 Cubism Editor

---

## 📄 许可证

MIT License — 可自由商用、修改、分发，保留版权声明即可。

---

<div align="center">

**如果这个项目对你有帮助，别忘了点个 Star ⭐**

Made with ❤️ by Live2D Master Agent Team

</div>
