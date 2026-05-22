# 📁 项目文件索引

本页面列出了Live2D Master Agent项目的所有核心文件，方便快速访问。

---

## 📋 核心文档

| 文件 | 说明 | 优先级 |
|------|------|--------|
| [README.md](README.md) | 项目主README文档（推荐先看） | ⭐⭐⭐⭐⭐ |
| [SKILL.md](SKILL.md) | 技能定义和详细使用说明 | ⭐⭐⭐⭐⭐ |
| [GITHUB_SETUP.md](GITHUB_SETUP.md) | GitHub仓库初始化指南 | ⭐⭐⭐⭐ |
| [CHANGELOG.md](CHANGELOG.md) | 版本更新记录 | ⭐⭐⭐ |

---

## 🚀 核心工具

| 文件 | 说明 | 推荐使用场景 |
|------|------|-------------|
| [master_tool.py](master_tool.py) | 一站式工具箱（推荐） | 日常使用、快速生成 |
| [live2d_layer_pro.py](live2d_layer_pro.py) | 专业版AI智能分层 | 专业分层、高质量PSD |
| [config_api.py](config_api.py) | API配置工具 | 配置API密钥 |
| [config.py](config.py) | 配置模块 | 系统配置 |
| [install_ai_models.py](install_ai_models.py) | AI模型安装脚本 | 首次安装 |

---

## 📚 辅助脚本 (scripts/)

| 文件 | 说明 |
|------|------|
| [qa_engine_enhanced.py](scripts/qa_engine_enhanced.py) | 增强质量检查引擎 |
| [parameter_designer_enhanced.py](scripts/parameter_designer_enhanced.py) | 参数设计器 |
| [physics_helper.py](scripts/physics_helper.py) | 物理设置助手 |
| [layer_checker.py](scripts/layer_checker.py) | 图层检查工具 |
| [auto_naming.py](scripts/auto_naming.py) | 自动命名工具 |
| [seedream_image_generate.py](scripts/seedream_image_generate.py) | Seedream图像生成（需API） |

---

## 📖 文档

| 文件 | 说明 |
|------|------|
| [docs/RIGGING_GUIDE.md](docs/RIGGING_GUIDE.md) | 完整Rigging指南 |
| [AI_LAYERING_GUIDE.md](AI_LAYERING_GUIDE.md) | AI分层指南 |
| [CHANGELOG.md](CHANGELOG.md) | 版本更新记录 |
| [security_best_practices_report.md](security_best_practices_report.md) | 安全审计报告 |
| [功能审查报告.md](功能审查报告.md) | 功能审查报告 |
| [全面审查报告.md](全面审查报告.md) | 全面审查报告 |
| [TRAE_SOLO技能创作赛_参赛报告.md](TRAE_SOLO技能创作赛_参赛报告.md) | TRAE参赛报告 |
| [社区参赛帖.md](社区参赛帖.md) | 社区发帖模板 |

---

## 📝 提示词 (prompts/)

| 文件 | 说明 |
|------|------|
| [image_generation.md](prompts/image_generation.md) | 图像生成提示词 |
| [qa.md](prompts/qa.md) | 质量检查提示词 |
| [rigging.md](prompts/rigging.md) | Rigging提示词 |
| [physics.md](prompts/physics.md) | 物理设置提示词 |
| [split.md](prompts/split.md) | 分层提示词 |
| [naming.md](prompts/naming.md) | 命名提示词 |

---

## 📋 模板 (templates/)

| 文件 | 说明 |
|------|------|
| [psd_structure.md](templates/psd_structure.md) | PSD结构模板 |
| [cubism_params.md](templates/cubism_params.md) | Cubism参数模板 |
| [export_rules.md](templates/export_rules.md) | 导出规则模板 |

---

## 🔧 配置

| 文件 | 说明 |
|------|------|
| [.env.example](.env.example) | 环境变量示例模板 |
| [.gitignore](.gitignore) | Git忽略规则 |

---

## 📦 其他集成

| 文件 | 说明 |
|------|------|
| [install_comfyui.py](install_comfyui.py) | ComfyUI安装脚本 |
| [comfyui_integration.py](comfyui_integration.py) | ComfyUI集成 |
| [live2d_workflow.json](live2d_workflow.json) | Live2D工作流配置 |

---

## 📊 快速使用指南

### 入门级使用

1. **快速生成角色**：
   ```bash
   python master_tool.py "cute anime girl"
   ```

2. **使用已有图片**：
   ```bash
   python master_tool.py --skip-generate
   ```

### 进阶级使用

1. **专业分层**：
   ```bash
   python live2d_layer_pro.py character.png
   ```

2. **质量检查**：
   ```bash
   python scripts/qa_engine_enhanced.py
   ```

---

## 🔍 资源链接

- [TRAE社区](https://forum.trae.cn/c/37-category/37) - 参赛专区
- [GitHub仓库](待上传) - 源代码仓库
- [问题反馈](待添加) - 提交Issue

---

**最后更新**: 2026年5月22日
