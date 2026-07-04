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
