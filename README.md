# 🎭 Live2D 全流程服务生成器

> **一句话**：输入一句话，AI 生成你的专属桌面伙伴。会眨眼、会呼吸、会跟着鼠标看。

<div align="center">

[![在线体验](https://img.shields.io/badge/🚀_在线体验-点击这里-ff69b4?style=for-the-badge)](https://mw2wbyys6t-sudo.github.io/Live2D/)
[![GitHub](https://img.shields.io/badge/GitHub-仓库-667eea?style=for-the-badge)](https://github.com/mw2wbyys6t-sudo/Live2D)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)]()

</div>

---

## 🚀 先体验，再决定

**👉 [点击这里在线体验](https://mw2wbyys6t-sudo.github.io/Live2D/)** — 浏览器内直接生成角色，实时预览动画效果，无需安装任何东西。

可体验的功能：
- 🎨 **AI 生成角色**（Pollinations 免费 API，无需 Key）
- 👁 **实时预览动画**（眨眼、呼吸、鼠标跟随、表情切换）
- 🖱️ **互动演示**（点击角色、拖拽移动）
- 💾 **下载桌宠包**（Windows 可直接运行）

---

## ✅ 能做什么 / ⚠️ 不能做什么

> 诚实说明，避免误解。

### ✅ 已经实现

| 功能 | 说明 |
|---|---|
| 🤖 AI 角色生成 | Pollinations（免费）/ Seedream / SenseNova 三家 Provider |
| 🎨 自动拆层 | K-means 颜色聚类，自动拆成 12-15 个图层 |
| 👁 桌宠动画 | 眨眼 / 呼吸 / 身体摇摆 / 头发摆动 / 鼠标跟随 |
| 😊 表情系统 | 微笑 / 惊讶 / 生气 等基础表情 |
| 🖱️ 交互 | 点击互动 / 拖拽移动 / 自动漫游 |
| 💻 桌面桌宠 | Windows 双击运行，透明窗口，置顶显示 |
| 🎭 角色管理 | 多角色切换，角色库管理 |
| 📦 PSD 导出 | Photoshop 多图层，可手动进一步编辑 |
| 🧪 自动化测试 | 149 项测试全部通过 |

### ⚠️ 已知局限

| 局限 | 说明 |
|---|---|
| **不是真正的 Live2D 模型** | 桌宠使用 PNG 图层合成动画，不是 Cubism MOC3 模型 |
| **不能直接用于 VTubeStudio 直播** | 如需 VTuber 直播，需在 Cubism Editor 中手动完成绑定 |
| **分层靠颜色聚类** | K-means 按颜色分组，无法精确区分"头发 vs 皮肤"（颜色接近会混） |
| **动画是 2D 合成** | 不是网格变形，是整体平移/缩放，效果比专业 Live2D 简单 |
| **生成质量依赖 AI Provider** | 第三方 API 风格不稳定 |

### 🔮 开发中

- 更好的语义分层（See-through / Qwen-Image-Layered 集成）
- 更多表情和动作
- macOS / Linux 版本
- 自定义服装/配饰
- 语音互动
- 社区角色分享

---

## 👀 适合谁用？

| 人群 | 为什么适合 |
|---|---|
| **二次元爱好者** | 快速拥有专属桌面伙伴，不用等建模师排期 |
| **VTuber 新人** | 先做桌宠试水，再决定是否投入 Live2D 建模 |
| **桌宠玩家** | 厌倦了模板角色，想要 AI 生成的独一无二的伙伴 |
| **独立开发者** | 想给你的软件加个可爱的吉祥物 |
| **技术美术** | 研究 AI + 角色生成工作流，可二次开发 |

---

## 🎯 三分钟上手

```bash
# 1. 安装依赖
python3 install.py

# 2. 一句话生成你的桌宠
python3 master_tool.py "蓝发猫耳少女，白色背景" --pet

# 3. 运行桌宠
cd output/pet_*/
./run_pet.sh   # macOS/Linux
run_pet.bat    # Windows
```

> 💡 默认使用 **Pollinations 免费图像生成**，无需 API Key，开箱即用。

### 其他使用方式

<details>
<summary>📦 交互式 Agent（新手友好）</summary>

```bash
python3 live2d_agent.py
```

会弹出菜单：生成角色 / 拆分图层 / 打包桌宠 / 一键全流程。

</details>

<details>
<summary>🌐 Web UI 可视化</summary>

```bash
cd web && npm install && npm run dev
# 浏览器打开 http://localhost:3000
```

支持：图片上传 / 角色生成 / 动画预览 / 桌宠下载。

</details>

<details>
<summary>⚙️ Go API 服务 / Python 工作流引擎</summary>

```bash
# Go API
cd api && go run main.go    # POST /api/generate | /api/layer | /api/pet

# Python 工作流
from live2d.workflow import WorkflowEngine
engine = WorkflowEngine(output_dir="./output")
result = engine.run(prompt="银发狐妖少女", deploy_desktop=True)
```

</details>

---

## 📦 跑完能得到什么？

```
output/
├── pet_<时间戳>/                      # ⭐ 桌宠包（直接运行）
│   ├── run_pet.py / run_pet.bat / run_pet.sh
│   ├── pet_config.json                # 动画配置
│   ├── layers/                        # 拆分后的独立图层
│   └── README.txt                     # 使用说明
│
├── layers_<时间戳>/
│   ├── layer_000.png ~ layer_NNN.png  # 拆分后的独立图层（RGBA）
│   ├── preview.png                     # 图层叠加预览
│   └── character.psd                   # Photoshop 多图层文件
│
└── rigged_<时间戳>/                    # 实验性：Cubism 素材包
    ├── character.model3.json
    ├── character.texture_00~07.png
    ├── character.physics3.json
    └── expressions/                    # 表情文件
```

---

## 🎮 桌宠操作说明

| 操作 | 效果 |
|---|---|
| **鼠标悬停** | 角色会看向鼠标 |
| **点击角色** | 触发互动表情 |
| **拖拽** | 移动角色位置 |
| **右键** | 弹出菜单（换角色/暂停/设置/退出） |
| **ESC** | 退出桌宠 |

---

## 🛠️ 项目结构速览

```
AI 桌宠生成器
├── 🐍 live2d/
│   ├── generation/     # AI 图像生成（多 Provider）
│   ├── layering/       # 图层拆分（K-means + 部位识别）
│   ├── pet/            # 🎯 桌宠核心（动画 + 打包 + 运行）
│   ├── rigging/        # ⚗️ 实验性：Cubism 自动绑定
│   ├── exporter/       # 导出（纹理图集 / model3.json / PSD）
│   ├── qa/             # 质量检测
│   └── workflow.py     # 全流程编排
├── 🔷 api/             # Go REST API（Gin 框架）
├── ⚛️ web/             # Next.js 前端（React + Tailwind）
├── 📘 lib/             # TypeScript 类型定义
├── 🎨 comfyui-connector/  # ComfyUI 集成
├── 🧪 tests/           # 自动化测试
├── 📚 docs/            # 文档 + 在线演示页
└── 🎯 examples/        # 示例产物
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

149 项测试覆盖：图像生成、图层拆分、网格生成、纹理打包、桌宠打包、边界场景（1×1 像素 / 全透明 / 共线点崩溃 / 多页纹理分页）等。

---

## 📖 文档导航

| 文档 | 内容 |
|---|---|
| [快速入门](docs/QUICKSTART.md) | 5 分钟跑通全流程 |
| [完整使用说明](USAGE.md) | 所有命令和参数详解 |
| [桌宠指南](docs/PET_GUIDE.md) | 桌宠使用与自定义 |
| [常见问题](docs/FAQ.md) | 遇到问题先看这里 |
| [更新日志](CHANGELOG.md) | 版本迭代历史 |

---

## 🤝 相关生态

- **[See-through](https://github.com/shitagaki-lab/see-through)** — SIGGRAPH 2024，学术级语义分层
- **[Qwen-Image-Layered](https://qwenlayered.com/)** — 阿里 Qwen，通用分层图像生成
- **[Textoon](https://arxiv.org/abs/2404.02072)** — 阿里达摩院，文生 Live2D 研究原型
- **[pixi-live2d-display](https://www.npmjs.com/package/@naari3/pixi-live2d-display)** — Web Live2D 运行时
- **[Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber)** — AI VTuber 完整框架

---

## ⭐ 项目亮点

- 🆓 **开箱即用**：默认 Pollinations 免费生成，零配置跑通
- 🇨🇳 **中文友好**：CLI / Agent / 文档全中文
- 🛡️ **安全可靠**：Fernet 加密 / 路径防护 / PSD 炸弹防护 / 日志脱敏
- 🧪 **测试完善**：149 项自动化测试
- 🎨 **真·AI 生成**：每个角色都是独一无二的
- 🖱️ **即下即用**：桌宠包双击运行，无需安装

### 路线图

```
✅ Phase 1 — AI 图生 + K-means 分层 + PSD + 桌宠 v1 + 149 项测试
🔮 Phase 2 — 语义分层（See-through）+ 更多表情动作 + macOS/Linux + 社区
🔮 Phase 3 — 自定义服装 + 语音互动 + 多宠物 + 手机版
🔮 Phase 4+ — 专业 Live2D 绑定 + VTuber 直播集成
```

---

## 📄 许可证

MIT License — 可自由商用、修改、分发，保留版权声明即可。

---

<div align="center">

**如果这个项目对你有帮助，别忘了点个 Star ⭐**

Made with ❤️ by AI 桌宠生成器 Team

</div>
