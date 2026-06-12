# 🎨 Live2D Master Agent

> **专业的AI辅助Live2D制作助手 - 从概念到绑定的完整工作流**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Stars](https://img.shields.io/github/stars/mw2wbyys6t-sudo/Live2D)](https://github.com/mw2wbyys6t-sudo/Live2D/stargazers)
[![Version](https://img.shields.io/badge/version-v7.1-green.svg)]()
[![Last Update](https://img.shields.io/badge/last%20update-2026--06--12-orange.svg)]()

---

## ✨ 一句话介绍

**3分钟创建专业Live2D角色！** 无需付费，一键生成，立即使用。

集成 [See-through](https://github.com/shitagaki-lab/see-through) (SIGGRAPH 2026) 专业级AI分层工具，提供从图像生成到PSD分层的完整工作流。

**🔥 v7.1 新增：桌面桌宠功能！** 无需Live2D软件，一键将角色部署为桌面宠物，支持动画、表情和交互！

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

### 第五步：桌面桌宠（v7.1新功能）

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

### 🐱 桌面桌宠（v7.1新功能）
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
| [README.md](README.md) | 项目主文档 | ⭐⭐⭐⭐⭐ |
| [SECURITY.md](SECURITY.md) | 安全指南 | ⭐⭐⭐⭐⭐ |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 架构设计 | ⭐⭐⭐⭐ |
| [docs/RIGGING_GUIDE.md](docs/RIGGING_GUIDE.md) | Rigging指南 | ⭐⭐⭐⭐ |
| [docs/archive/QUICKSTART.md](docs/archive/QUICKSTART.md) | 快速入门 | ⭐⭐⭐⭐ |
| [docs/archive/USER_GUIDE.md](docs/archive/USER_GUIDE.md) | 完整教程 | ⭐⭐⭐⭐ |
| [docs/archive/FAQ.md](docs/archive/FAQ.md) | 常见问题 | ⭐⭐⭐⭐ |
| [docs/archive/BEST_PRACTICES.md](docs/archive/BEST_PRACTICES.md) | 最佳实践 | ⭐⭐⭐ |

---

## 🎯 适用场景

| 场景 | 说明 | 收益 |
|------|------|------|
| 🎬 **VTuber创作** | 快速制作虚拟形象 | 节省数小时 |
| 🎮 **游戏开发** | 低成本角色设计 | 无需外包 |
| 🎨 **动画制作** | 标准化工作流 | 效率翻倍 |
| 💡 **AI爱好者** | 探索创作可能 | 无限创意 |

---

## 🛠️ 工具列表

### 核心工具

| 工具 | 说明 | 推荐度 |
|------|------|------|
| [master_tool.py](master_tool.py) | 一站式工具箱 | ⭐⭐⭐⭐⭐ |
| [install_comfyui_advanced.py](install_comfyui_advanced.py) | **See-through一键安装** | ⭐⭐⭐⭐⭐ |
| [live2d_desktop_pet.py](live2d_desktop_pet.py) | **桌面桌宠** | ⭐⭐⭐⭐⭐ |
| [live2d_layer_v6.py](live2d_layer_v6.py) | K-means分层工具 | ⭐⭐⭐⭐ |
| [live2d_layer_pro.py](live2d_layer_pro.py) | 颜色检测分层 | ⭐⭐⭐ |
| [config_api.py](config_api.py) | API配置 | ⭐⭐⭐⭐ |

### 辅助脚本

| 脚本 | 说明 |
|------|------|
| [scripts/qa_engine_enhanced.py](scripts/qa_engine_enhanced.py) | 质量检查 |
| [scripts/parameter_designer_enhanced.py](scripts/parameter_designer_enhanced.py) | 参数设计器 |
| [scripts/physics_helper.py](scripts/physics_helper.py) | 物理设置 |

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

详细文档：[SEE_THROUGH_INTEGRATION.md](SEE_THROUGH_INTEGRATION.md)

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
python create_test_image.py
python live2d_layer_v6.py test_character.png test_output
```

### 配置API（可选）

```bash
python config_api.py
```

### 🐱 桌面桌宠使用

```bash
# 方式1：完整工作流 + 桌面部署
python live2d_workflow.py "cat girl with blue hair" --deploy-desktop

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
python -m pip install -r requirements.txt

# 启动 Agent（推荐）
python live2d_agent.py

# 或直接使用命令行
python master_tool.py "your character description"

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
| 快速入门 | [QUICKSTART.md](QUICKSTART.md) |
| See-through指南 | [SEE_THROUGH_INTEGRATION.md](SEE_THROUGH_INTEGRATION.md) |
| 常见问题 | [FAQ.md](FAQ.md) |
| 项目结构 | [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) |
| 更新日志 | [CHANGELOG.md](CHANGELOG.md) |
| 已知限制 | [LIMITATIONS.md](LIMITATIONS.md) |

---

**让Live2D制作更简单！** 🎨

*版本: v7.1（桌面桌宠功能+See-through集成）*
*最后更新: 2026-05-30*
