# Live2D Master Agent v9.0

> **从一句话描述到可动 Live2D 角色，全程 AI 辅助的完整生产线。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-v9.0.0-green.svg)]()
[![Tests](https://img.shields.io/badge/tests-149%20passed-brightgreen.svg)]()

---

## 这是什么？

Live2D Master Agent 是一个面向创作者的工具集，帮助你把角色创意快速变成 Live2D 可用的分层素材。

**一句话说明**：输入角色描述或图片，自动完成图像生成、图层拆分、PSD 导出、Cubism 参数配置，还能一键部署为桌面桌宠。

适合人群：

- 想做 Live2D 虚拟主播但不懂拆分的画师
- 需要快速产出角色分层素材的内容创作者
- 想用 AI 辅助 Live2D 工作流的技术美术
- 想给自己的桌面加一只动态桌宠的用户

---

## 三分钟上手

```bash
# 1. 安装依赖
python3 install.py

# 2. 用一句话生成角色并自动拆分图层
python3 master_tool.py "蓝发猫耳少女，白色背景"

# 3. 或者用已有图片拆分图层、生成 PSD 和 Cubism 配置
python3 live2d_workflow.py --input character.png --output ./output --k 5
```

> 默认使用 Pollinations 免费图像生成，无需 API Key，开箱即用。

---

## 主要功能

| 功能 | 说明 |
|------|------|
| **AI 角色生成** | 输入中文或英文描述，自动生成角色立绘 |
| **智能图层拆分** | 基于 K-means 颜色聚类，把角色拆成头发、脸部、身体等图层 |
| **PSD 导出** | 生成 Adobe Photoshop 可直接打开的多图层 PSD 文件 |
| **Cubism 标准配置** | 自动生成 52 层标准映射、`parameters.json`、`physics3.json` |
| **桌面桌宠** | 一键打包为可运行的桌面宠物，支持 Windows / macOS / Linux |
| **Web 质检工具** | 可视化检查 PSD 结构和 Live2D 规范合规性 |

---

## 五种使用方式

### 1. 交互式 Agent（推荐新手）

```bash
python3 live2d_agent.py
```

启动后会看到菜单，支持直接输入数字或自然语言：

```text
[1] 生成角色
[2] 拆分图层
[3] 部署桌宠
[4] 一键完成全部流程
[5] 设置
[0] 退出
```

### 2. 一站式命令行

```bash
# 生成角色 + 拆分 + PSD + Cubism 配置
python3 master_tool.py "可爱的猫娘，粉色头发"

# 如果你已有图片，用端到端工作流处理
python3 live2d_workflow.py --input character.png --output ./output
```

### 3. 端到端工作流

```bash
# 从图片到完整 Live2D 素材
python3 live2d_workflow.py --input character.png --output ./output --k 5 --deploy-desktop
```

常用参数：

| 参数 | 说明 |
|------|------|
| `--input PATH` | 输入图片路径 |
| `--output DIR` | 输出目录 |
| `--k N` | 图层数量，3-20，默认 8 |
| `--deploy-desktop` | 同时生成桌面桌宠 |
| `--provider pollinations` | 免费生成（默认） |
| `--provider seedream` | 火山 Seedream 高质量生成 |

### 4. Web UI

```bash
cd web
npm install
npm run dev
```

浏览器打开 `http://localhost:3000`，可上传 PSD 检测结构问题，或把图片转为 PSD。

### 5. Trae IDE Skill

在 Trae IDE 中加载 `.trae/skills/live2d-master-agent/` 目录，即可在编辑器内用自然语言调用：

- "帮我生成一个 Live2D 角色"
- "把这张图拆分成 Live2D 图层"
- "检查这个 PSD 是否符合 Live2D 规范"

---

## 运行后会得到什么？

```text
output/layers_<时间戳>/
  optimized_*.png         # 去背景后的优化原图
  layer_000.png           # 拆分后的独立图层（RGBA）
  layer_001.png
  ...
  preview.png             # 图层叠加预览
  character.psd           # Photoshop 多图层文件
  layer_mapping.json      # 图层到 52 层标准的映射
  parameters.json         # Cubism 参数定义
  physics3.json           # 物理效果配置（头发、身体、呼吸）
  52_LAYER_GUIDE.txt      # 52 层标准参考
  pet_packages/<名称>/    # 桌面桌宠包（如果加了 --deploy-desktop）
    run_pet.py            # 直接双击运行
    pet_config.json       # 动画配置
    layers/               # 图层素材
```

---

## 配置 API Key（可选）

默认免费方案无需配置。如需更高质量的火山 Seedream 生成，可复制示例文件并填写密钥：

```bash
cp .env.example .env
```

编辑 `.env`：

```env
# 火山引擎 ARK / Seedream（可选）
ARK_API_KEY=your-api-key-here
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3

# 输出目录
OUTPUT_DIR=./output

# Go API 服务端口（可选）
GO_API_PORT=8080
```

---

## 环境要求

- **Python**: 3.8 或更高版本（推荐 3.11 / 3.12）
- **Node.js**: 18+（仅使用 Web UI 时需要）
- **操作系统**: Windows、macOS、Linux

核心依赖会自动安装：Pillow、numpy、requests、psd-tools、scikit-learn、cryptography、rich 等。

---

## 测试

项目包含 149 项测试，全部无需真实 API Key：

```bash
python3 -m pytest tests/ -q
```

---

## 项目亮点

- **开箱即用**：默认 Pollinations 免费生成，零配置跑通全流程
- **中文友好**：CLI、Agent、提示词都支持中文输入
- **安全可靠**：Fernet 加密存储、路径安全校验、PSD 防恶意文件校验
- **测试完善**：149 项测试覆盖，无需外部 API Key
- **生态完整**：CLI + Agent + Web UI + Trae Skill + Go API 多入口

---

## 技术架构

项目采用「Python 核心 + Go API + Next.js Web UI + Trae Skill」的多层架构：

```text
Live2D/
├── live2d/                     # Python 核心包
│   ├── workflow.py             # 状态机工作流引擎
│   ├── image_gen/              # 图像生成 Provider 路由
│   │   ├── pollinations.py     # 免费 Provider（无需 Key）
│   │   ├── seedream.py         # 火山 Seedream / ARK
│   │   └── sensenova.py        # SenseNova
│   ├── layering/               # 图层拆分与 Live2D 标准
│   │   ├── kmeans.py           # K-means v6 默认分层
│   │   ├── layers52.py         # 52 层 Cubism 标准
│   │   └── part_identifier.py  # 颜色/位置启发式部件识别
│   ├── psd/                    # PSD 生成与校验
│   │   ├── creator.py          # PSD / PNG 包创建
│   │   ├── parser.py           # PSD 解析（带炸弹防护）
│   │   └── validator.py        # PSD 合法性校验
│   ├── pet/                    # 桌面桌宠
│   │   ├── animator.py         # 桌宠包生成
│   │   └── runner.py           # 实时预览运行器
│   ├── qa/engine.py            # 图像质量评估
│   ├── security.py             # 路径/提示词/文件名安全校验
│   ├── secure_storage.py       # Fernet + PBKDF2 加密存储
│   └── logger.py               # 统一日志 + 敏感信息脱敏
├── api/                        # Go REST API（Gin 框架）
│   ├── main.go                 # API 入口
│   ├── config/config.go        # 动态超时配置
│   ├── handlers/handlers.go    # HTTP 接口
│   └── services/python_bridge.go # Python 桥接调用
├── web/                        # Next.js 前端工具
├── .trae/skills/live2d-master-agent/  # Trae IDE Skill
├── tests/                      # 149 项测试套件
├── scripts/                    # 辅助脚本
├── docs/                       # 文档
└── examples/                   # 示例案例与素材
```

### 数据流

```text
用户输入（描述 / 图片）
    ↓
图像生成 Provider → 角色立绘
    ↓
图像优化（去背景、增强）
    ↓
K-means 图层拆分 → layer_000.png ~ layer_NNN.png
    ↓
PSD 导出 + 52 层标准映射 + Cubism 参数/物理配置
    ↓
可选：桌面桌宠包 / Go API 服务 / Web UI 质检
```

### 安全设计

- **加密存储**：API Key 使用 Fernet（AES-128-CBC + HMAC-SHA256）加密，密钥经 PBKDF2-HMAC-SHA256 派生
- **路径防护**：禁止 `..`、空字节、危险字符，防止目录遍历
- **PSD 防护**：校验文件魔数、尺寸上限、图层数量，防止 zip bomb
- **提示词清洗**：过滤 `rm -rf`、`eval`、`exec` 等危险注入模式
- **日志脱敏**：自动隐藏 `sk-*`、Bearer Token、JWT 等敏感信息

---

## 文档导航

- [快速入门](docs/QUICKSTART.md)
- [完整使用说明](USAGE.md)
- [用户指南](docs/USER_GUIDE.md)
- [最佳实践](docs/BEST_PRACTICES.md)
- [常见问题](docs/FAQ.md)
- [更新日志](CHANGELOG.md)

---

## 许可证

MIT License
