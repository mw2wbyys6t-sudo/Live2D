# 🎭 Live2D Master Agent v10.0

> **一句话**：输入一句话，AI 生成你的专属虚拟主播——支持实时面部捕捉、语音对话、表情联动、桌宠运行。

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge)](https://python.org)
[![Go](https://img.shields.io/badge/Go-1.21+-00ADD8?style=for-the-badge)](https://go.dev)
[![Next.js](https://img.shields.io/badge/Next.js-16-black?style=for-the-badge)](https://nextjs.org)
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-green?style=for-the-badge)](https://creativecommons.org/licenses/by/4.0/)
[![Version](https://img.shields.io/badge/Version-10.0-ff69b4?style=for-the-badge)]()

</div>

---

## ✨ v10.0 重大升级

| 功能 | v9.0 | **v10.0** |
|------|------|-----------|
| 图像分层 | K-means 颜色聚类 | **SAM+ISNet 语义分割 + Amodal 补全** |
| Live2D 导出 | 空脚手架 model3.json | **完整 Cubism4 模型包（28 表情 + 物理 + 骨骼）** |
| 桌宠驱动 | 预设循环动画 | **MediaPipe 面部捕捉 + 麦克风音频驱动** |
| 角色一致性 | ❌ 每次随机变脸 | **角色卡 + 参考图锚定 + Embedding 锁定** |
| AI 对话 | ❌ 无 | **LLM 流式对话 + TTS 语音 + 情绪联动** |
| 前端工作台 | PSD 质检单页 | **8 页面一站式工作台** |
| 代码架构 | 双目录冗余 | **模块化 6 层架构** |
| 部署 | 手动 | **Docker + 一键安装 + CI/CD** |

---

## 🚀 三分钟上手

### 一键安装（推荐）

```bash
# Windows: 双击 install.bat
# macOS/Linux:
bash install.sh

# 或直接用 Python:
python install.py
```

安装程序会自动：
1. 检测 Python/Node/Go 环境
2. 安装所有 Python 依赖
3. 安装 npm 依赖（Web 前端）
4. 编译 Go API 服务器
5. 创建 .env 配置文件
6. 验证安装

### 快速生成

```bash
# 一句话生成角色（免费 Pollinations，无需 API Key）
python -m core.cli generate "蓝发猫耳少女，白色背景，日系赛璐璐风格" --deploy-desktop

# 运行桌宠
python -m core.cli pet

# 启动 Web 工作台
cd web && npm run dev
# 打开 http://localhost:3000

# 启动 API 服务器
cd api && ./live2d-api
# API 在 http://localhost:8080
```

### Docker 部署

```bash
docker compose up -d
# Web: http://localhost:3000  API: http://localhost:8080
```

---

## 🏗️ 项目架构

```
Live2D-Master-Agent/
├── core/                    # 🐍 Python 核心内核
│   ├── segment_engine/      #   语义分割（SAM+ISNet+Amodal）
│   ├── image_gen/           #   AI 图像生成（Pollinations/Seedream/SenseNova）
│   ├── character/           #   角色一致性系统（卡片+Embedding）
│   ├── psd/                 #   PSD 读写与校验
│   ├── qa/                  #   质量检测引擎
│   ├── utils/               #   图像/文件工具集
│   ├── config.py            #   安全配置管理
│   ├── workflow.py          #   全流程编排引擎
│   └── cli.py               #   命令行入口
├── live2d_builder/          # 🦴 Live2D Cubism4 构建管线
│   ├── mesh/                #   Delaunay 网格生成 + UV 展开
│   ├── bones/               #   36 骨骼层级 + 变形器
│   ├── blendshapes/         #   28 标准表情参数
│   ├── physics/             #   头发/裙摆/呼吸物理
│   ├── exporter/            #   model3.json + physics3.json + 纹理图集
│   └── validator/           #   模型合法性校验
├── drivers/                 # 🎯 实时驱动层
│   ├── face_tracker/        #   MediaPipe 468 关键点 → BlendShape 映射
│   ├── audio/               #   麦克风采集 + 音量/音调分析
│   ├── desktop_pet/         #   跨平台透明窗口桌宠
│   └── live2d_runtime/      #   软件 Live2D 渲染器（参数驱动）
├── llm_bridge/              # 💬 AI 对话网关
│   ├── providers/           #   OpenAI/Anthropic/Ollama 多模型
│   ├── tts/                 #   Edge TTS（免费）/ OpenAI TTS
│   ├── asr/                 #   Whisper/FunASR 语音识别
│   ├── emotion/             #   情绪分析（7 类→表情+动作）
│   └── chat_session.py      #   对话管理 + 语音指令
├── api/                     # 🔷 Go REST API（Gin 高性能）
│   ├── handlers/            #   路由处理（角色/生成/聊天/WebSocket）
│   ├── services/            #   业务逻辑（Python桥接/缓存/WS Hub）
│   ├── models/              #   数据模型
│   └── config/              #   配置管理
├── web/                     # ⚛️ Next.js 工作台
│   ├── pages/               #   8 页面（仪表盘/角色/生成/分层/Live2D/预览/聊天/导出）
│   ├── components/          #   24+ React 组件
│   ├── lib/                 #   API 客户端/WS/Live2D 播放器
│   └── types/               #   TypeScript 类型定义
├── assets/                  # 📦 资产存储
│   ├── characters/          #   角色卡片 JSON
│   ├── models/              #   AI 模型权重
│   └── output/              #   生成产物
├── scripts/                 # 🔧 工具脚本（模型下载等）
├── deploy/                  # 🚀 部署配置（Docker）
├── tests/                   # 🧪 测试套件（unit/integration/e2e）
├── docs/                    # 📚 文档
├── install.py / .sh / .bat  # 🔨 一键安装程序
├── Dockerfile               # 🐳 容器化
└── docker-compose.yml       #   多服务编排
```

---

## 🎯 核心功能

### 1. AI 角色生成
- **多 Provider**：Pollinations（免费）/ Seedream（火山引擎）/ SenseNova（商汤）
- **生产级 Prompt**：4096×4096 透明背景、正面朝向、五官对称、赛璐璐风格
- **自动 QA**：边缘清晰度、颜色分离度、背景检测

### 2. 语义分层引擎
- **ISNet Anime-Segmentation**：二次元主体精准抠图
- **SAM**：实例语义分层（头发/五官/衣物/配饰）
- **Amodal Completion**：遮挡区域像素补全（被头发遮挡的脸部等）
- **18 层标准顺序**：头皮→后发→中发→前发→眉毛→眼睛→口鼻→脸→颈→上衣→内衣→手臂→手→裙摆→腿→配饰→兽耳/尾→特效

### 3. Live2D Cubism4 自动绑定
- **Delaunay 三角网格**自动生成（边界细分+内部网格）
- **36 骨骼**标准层级自动排布
- **28 BlendShape**：眨眼、微笑、生气、惊讶、哭泣、嘴型 A/I/U/E/O 等
- **物理引擎**：头发摆动、裙摆飘动、呼吸、兽耳/尾巴弹性
- **导出**：model3.json + physics3.json + 28 个 exp3.json + 纹理图集 + Cubism 导入指南

### 4. 实时面部捕捉
- **MediaPipe Face Mesh** 468 个人脸关键点
- **ARKit BlendShape** → Live2D 参数映射（52 系数）
- **指数平滑** + 死区滤波，低延迟 ≤75ms
- **麦克风**：RMS 音量 → 嘴型开合，基频 → 语调情绪
- **跨平台**：Windows/macOS/Linux 透明悬浮窗口

### 5. 角色一致性锁定
- **角色卡**：JSON 存档脸型/五官/配色/体型/服装/人设
- **参考图锚定**：正面/侧面/背面三视图约束生成
- **Embedding 锁定**：CLIP/颜色直方图特征注入 Prompt
- **换装系统**：同角色多套穿搭，主体形象不偏移

### 6. LLM 对话 + 语音 + 情绪联动
- **多模型**：OpenAI GPT-4o / Claude 3 / Ollama 本地 Qwen
- **流式输出**：逐字显示，实时情绪分析
- **免费 TTS**：微软 Edge TTS（中文晓晓/日语 Nanami/英文 Aria）
- **ASR**：Whisper/FunASR 本地语音识别
- **7 类情绪** → 表情 + 肢体参数联动
- **语音指令**：「换衣服」「晃头发」「收起桌宠」

### 7. Web 一站式工作台
| 页面 | 功能 |
|------|------|
| Dashboard | 总览、快捷入口、系统状态 |
| Characters | 角色卡 CRUD、参考图上传、历史存档 |
| Generate | Prompt 编辑、Provider 选择、实时进度 WS |
| Layers | 分层可视化、拖拽排序、蒙版预览、PSD 导出 |
| Live2D | 骨骼树、参数滑块、物理调试、模型导出 |
| Preview | PixiJS 实时预览、Webcam 捕捉开关 |
| Chat | 聊天界面、语音输入、表情联动 |
| Export | PSD/PNG/模型包/桌宠包/角色卡导出 |

---

## 🔧 配置 API Key

默认使用 Pollinations 免费生成，无需配置。如需高质量生成或 LLM 对话，编辑 `.env`：

```env
# 图像生成（可选）
ARK_API_KEY=your-volcengine-key
SENSENOVA_API_KEY=your-sensenova-key

# LLM 对话（可选，不设则无法聊天）
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini

# 或使用本地 Ollama（免费）
# 无需 Key，只需 ollama serve + ollama pull qwen2.5:3b
```

---

## 🧪 测试

```bash
# 运行全部测试
python -m pytest tests/ -v

# 带覆盖率
python -m pytest tests/ -v --cov=core --cov=drivers --cov=llm_bridge --cov=live2d_builder --cov-report=term

# Go 测试
cd api && go test ./... -v

# 前端构建检查
cd web && npm run build
```

---

## 📖 文档

| 文档 | 内容 |
|------|------|
| [快速入门](docs/QUICKSTART.md) | 5 分钟跑通全流程 |
| [用户指南](docs/USER_GUIDE.md) | 完整功能使用说明 |
| [常见问题](docs/FAQ.md) | 遇到问题先看这里 |
| [已知局限](docs/LIMITATIONS.md) | 功能边界说明 |
| [架构设计](docs/ARCHITECTURE.md) | 技术架构详解 |
| [部署指南](docs/DEPLOY.md) | 云端/本地部署教程 |
| [开发规范](docs/CODE_STANDARD.md) | 代码贡献指南 |

---

## 🤝 相关开源生态

- [MediaPipe](https://mediapipe.dev/) — 实时面部/手势捕捉
- [Segment Anything](https://github.com/facebookresearch/segment-anything) — 通用语义分割
- [anime-segmentation](https://github.com/SkyTNT/anime-segmentation) — 二次元专用分割
- [pixi-live2d-display](https://github.com/nicxfer/pixi-live2d-display) — Web Live2D 渲染
- [Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber) — AI VTuber 框架
- [VTube Studio](https://github.com/DenchiSoft/VTubeStudio) — 专业 VTuber 软件

---

## 📄 许可证

本项目采用 **[CC BY 4.0（知识共享 署名 4.0 国际）](https://creativecommons.org/licenses/by/4.0/deed.zh-hans)** 许可协议。

### 你可以（自由创作）✅
- **分享** — 在任何媒介以任何形式复制、发行本作品
- **改编** — 修改、转换、二次创作、生成衍生作品（包括 Live2D 模型、角色形象、代码二次开发等）
- **商用** — 允许将本作品及衍生作品用于商业目的

### 你必须（保留产权）📌
- **署名** — 必须保留原作者 **Live2D Master Agent Team** 的版权声明与署名
- **标注许可** — 必须明确标注本作品采用的 CC BY 4.0 许可协议
- **注明更改** — 若对作品进行了修改、二次创作，必须明确说明所做的更改

### 产权声明 ©️
- 本项目所有原始内容（代码、文档、模型、角色形象、视觉资产）的**著作权与产权归原作者 Live2D Master Agent Team 所有**
- 任何形式的二次创作、分发、商用，均须在显著位置保留原版权声明
- 衍生作品须继续以相同或兼容的署名许可协议发布

> 简而言之：**保留我的署名与产权，欢迎你自由创作、改编、商用**。

### 完整法律文本
- 中文版：https://creativecommons.org/licenses/by/4.0/deed.zh-hans
- 英文版：https://creativecommons.org/licenses/by/4.0/legalcode

---

<div align="center">

**Made with ❤️ by Live2D Master Agent Team**

</div>
