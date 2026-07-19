# 🎭 Live2D Master Agent

> **一句话**：输入一张角色图，AI 自动拆层 + 自动 Rigging，3 分钟生成可导入 Cubism Editor 的 Live2D 模型。

<div align="center">

[![在线体验](https://img.shields.io/badge/🚀_在线体验-点击这里-ff69b4?style=for-the-badge)](https://mw2wbyys6t-sudo.github.io/Live2D/)
[![GitHub](https://img.shields.io/badge/GitHub-仓库-667eea?style=for-the-badge)](https://github.com/mw2wbyys6t-sudo/Live2D)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)]()

</div>

<div align="center">
  <img src="examples/assets/layer_demo_overview.png" alt="AI自动分层效果" width="700">
  <p><em>左：输入原图 → 右：AI 自动拆分的 15 个图层</em></p>
</div>

---

## 🚀 先体验，再决定

**👉 [点击这里在线体验](https://mw2wbyys6t-sudo.github.io/Live2D/)** — 浏览器内直接生成 Live2D 风格立绘，无需安装任何东西。

可体验的功能：
- 🎨 **在线生成角色**（Pollinations 免费 API，无需 Key）
- 🔍 **AI 自动分层**（K-means 颜色聚类演示）
- 🎭 **Live2D 模型实时互动**（鼠标跟随、表情切换、参数调节）
- 📦 **下载真实 AI 产物**（model3.json / 纹理图集 / 分层 PNG）

---

## ✅ 能做什么 / ⚠️ 不能做什么

> 诚实说明，避免误解。

### ✅ 已经实现

| 功能 | 说明 |
|---|---|
| 🤖 AI 角色生成 | Pollinations（免费）/ Seedream / SenseNova 三家 Provider |
| 🎨 自动拆层 | K-means 颜色聚类，自动拆成 12-15 个图层 |
| 📐 52 层标准映射 | 自动映射到 Live2D Cubism 官方 52 层结构 |
| 🔺 自动 ArtMesh 网格 | Delaunay 三角剖分 + 轮廓提取 |
| 🌳 自动 Warp Deformer 树 | Root → Head/Body → Face/Eye/Mouth 完整层级 |
| 📦 model3.json 导出 | Cubism 5 兼容（参数/物理/表情/纹理） |
| 📄 PSD 导出 | Photoshop 多图层，直接拖进 Cubism Editor |
| 🐱 桌面桌宠 | 一键打包，Win/macOS/Linux 三端 |
| 🧪 279 项测试 | 全部通过，无需 API Key |

### ⚠️ 已知局限

| 局限 | 说明 |
|---|---|
| **不含 .moc3** | 输出的 model3.json 需在 Cubism Editor 中手动生成 MOC3 才能运行时播放 |
| **分层靠颜色** | K-means 按颜色聚类，无法理解"头发 vs 皮肤"（颜色接近会混） |
| **生成质量依赖 Provider** | 第三方 API 风格不稳定 |

### 🔮 开发中（Phase 3）

- AI 语义分割（按部位理解，替代 K-means）
- Amodal 补全（自动补全被遮挡部分）
- ARKit 52 口型同步
- Web 端在线生成

---

## 👀 适合谁用？

| 人群 | 痛点 | 方案 |
|---|---|---|
| **VTuber / 虚拟主播** | 找画师+建模太贵、周期长 | AI 粗模，快速出道 |
| **Live2D 建模师** | 拆层、拉网格太机械 | AI 做粗模，你做精修 |
| **独立游戏开发者** | 需要大量 Live2D NPC | 批量生成，统一风格 |
| **桌宠爱好者** | 想要专属桌宠但不会建模 | 一键生成，即开即用 |
| **技术美术** | 想探索 AI + Live2D 工作流 | 完整开源，可二开 |

---

## 🎯 三分钟上手

```bash
# 1. 安装依赖
python3 install.py

# 2. 一句话生成角色 + 自动拆层 + 自动 Rigging
python3 master_tool.py "蓝发猫耳少女，白色背景" --rig

# 3. 或者用已有图片端到端处理
python3 master_tool.py --input character.png --layer-only --rig
```

> 💡 默认使用 **Pollinations 免费图像生成**，无需 API Key，开箱即用。

### 其他使用方式

<details>
<summary>📦 交互式 Agent（新手友好）</summary>

```bash
python3 live2d_agent.py
```

会弹出菜单：生成角色 / 拆分图层 / 自动 Rigging / 部署桌宠 / 一键全流程。

</details>

<details>
<summary>🌐 Web UI 可视化</summary>

```bash
cd web && npm install && npm run dev
# 浏览器打开 http://localhost:3000
```

支持：图片上传转 PSD / 图层树可视化 / 规范合规检测 / QA 质检面板。

</details>

<details>
<summary>⚙️ Go API 服务 / Python 工作流引擎 / Trae Skill</summary>

```bash
# Go API
cd api && go run main.go    # POST /api/generate | /api/layer | /api/rig

# Python 工作流
from live2d.workflow import WorkflowEngine
engine = WorkflowEngine(output_dir="./output")
result = engine.run(prompt="银发狐妖少女", generate_52_config=True)

# Trae IDE Skill：在 Trae 中加载 .trae/skills/live2d-master-agent/
# 然后说："帮我生成一个蓝发猫娘 Live2D 角色，然后自动 rigging"
```

</details>

---

## 📦 跑完能得到什么？

```
output/
├── layers_<时间戳>/
│   ├── layer_000.png ~ layer_NNN.png   # 拆分后的独立图层（RGBA）
│   ├── preview.png                      # 图层叠加预览
│   ├── character.psd                    # Photoshop 多图层文件
│   ├── layer_mapping.json               # 52 层标准映射
│   └── parameters.json                  # Cubism 参数定义
│
├── rigged_<时间戳>/                      # ⭐ 自动 Rigging 输出
│   ├── character.model3.json            # Cubism model3.json
│   ├── character.texture_00~07.png      # 8 张纹理图集
│   ├── character.physics3.json          # 物理配置
│   ├── mesh_guide.json                  # 网格元数据
│   └── expressions/                     # 表情（smile/surprised/angry）
│
└── pet_packages/<name>/                 # 桌面桌宠包
    ├── run_pet.py                       # 双击运行
    └── layers/                          # 图层素材
```

直接把 `rigged/` 拖进 Cubism Editor 就能看到自动生成的网格和变形器。

---

## 🛠️ 项目结构速览

```
Live2D Master Agent
├── 🐍 live2d/          # Python 核心：工作流 / 图生 / 分层 / Rigging / 导出 / 桌宠
├── 🔷 api/             # Go REST API（Gin 框架）
├── ⚛️ web/             # Next.js 前端（React + Tailwind）
├── 📘 lib/             # TypeScript 8 步流水线类型
├── 🎨 comfyui-connector/  # ComfyUI 集成
├── 🧪 tests/           # 279 项自动化测试
├── 📚 docs/            # 文档 + 在线演示页
├── 🎯 examples/        # 真实案例产物（VTuber / 猫娘 / 发片）
└── 🔌 .trae/skills/    # Trae IDE Skill 插件
```

---

## 🔧 配置 API Key（可选）

默认免费方案无需配置。如需更高质量，复制 `.env.example` 为 `.env`：

```env
# 火山引擎 ARK / Seedream（可选，高质量生成）
ARK_API_KEY=your-api-key-here
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3

# SenseNova（可选）
SENSENOVA_KEY_ID=your-key-id
SENSENOVA_KEY_SECRET=your-key-secret
```

---

## 📋 环境要求

| 组件 | 最低版本 | 推荐 |
|---|---|---|
| Python | 3.8 | 3.11 / 3.12 |
| Node.js（Web UI） | 18 | 20 LTS |
| Go（API 服务） | 1.20 | 1.22 |
| 操作系统 | Win / macOS / Linux | — |

---

## 🧪 测试

```bash
python3 -m pytest tests/ -v
```

279 项测试全部无需 API Key，覆盖边界场景：1×1 像素 / 全透明 / 共线点崩溃 / 多页纹理分页 / 1024×1024 大图 / L/U/环形轮廓 / 特殊字符层名 等。

---

## 📖 文档导航

| 文档 | 内容 |
|---|---|
| [快速入门](docs/QUICKSTART.md) | 5 分钟跑通全流程 |
| [完整使用说明](USAGE.md) | 所有命令和参数详解 |
| [用户指南](docs/USER_GUIDE.md) | 从入门到精通 |
| [最佳实践](docs/BEST_PRACTICES.md) | 出高质量结果的技巧 |
| [常见问题](docs/FAQ.md) | 遇到问题先看这里 |
| [Rigging 指南](docs/RIGGING_GUIDE.md) | 自动 Rigging 原理与调优 |
| [更新日志](CHANGELOG.md) | 版本迭代历史 |

---

## 🤝 相关生态

- **[Textoon](https://github.com/Human3DAIGC/Textoon)** — 阿里通义，学术界首个文生 Live2D 系统
- **[Qwen-Image-Layered](https://qwenlayered.com/)** — 阿里 Qwen，图像分层 + Amodal 补全
- **[Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber)** — AI VTuber 完整框架
- **[pixi-live2d-display](https://www.npmjs.com/package/@naari3/pixi-live2d-display)** — Web 运行时
- **[awesome-digital-human-live2d](https://github.com/wan-h/awesome-digital-human-live2d)** — 最全资源索引

---

## ⭐ 项目亮点

- 🆓 **开箱即用**：默认 Pollinations 免费生成，零配置跑通
- 🇨🇳 **中文友好**：CLI / Agent / 文档全中文
- 🛡️ **安全可靠**：Fernet 加密 / 路径防护 / PSD 炸弹防护 / 日志脱敏
- 🧪 **测试完善**：279 项自动化测试
- 🎯 **真·自动 Rigging**：国内开源少有的完整网格 + Deformer 方案
- 📦 **Cubism 5.x 兼容**：输出标准 model3.json，直接导入编辑器

### 路线图

```
✅ Phase 1 — 图生 + K-means 分层 + PSD + 52 层映射 + 桌宠
✅ Phase 2 — 自动 ArtMesh + Warp Deformer 树 + model3.json + 暴力测试
🔮 Phase 3 — 语义分割 + Amodal 补全 + ARKit 口型同步 + Web 运行时
🔮 Phase 4+ — 语音驱动 + 表情识别 + 实时动捕 + 云端部署
```

---

## 📄 许可证

MIT License — 可自由商用、修改、分发，保留版权声明即可。

---

<div align="center">

**如果这个项目对你有帮助，别忘了点个 Star ⭐**

Made with ❤️ by Live2D Master Agent Team

</div>
