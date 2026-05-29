# 📋 Live2D Master Agent - 更新日志

记录项目的所有重要更新和变更。

---

## v6.2 (2026-05-29)

### ✨ 核心优化：图片生成工具

- **重大优化 master_tool.py** (v6.2)
  - 🎯 新增：智能重试机制，大幅提升图片生成成功率
  - 🎯 新增：3个服务端（包括Flux模型）自动降级+双重重试
  - 🎯 新增：可自定义图片分辨率（--width, --height）
  - 🎯 新增：多样化风格系统（7种艺术风格）
  - 🎯 优化：提示词质量提升，更适合Live2D制作
  - 🎯 优化：更长的超时时间，避免网络波动导致失败
  - 🎯 优化：更智能的错误处理和用户提示

### 🗑️ 冗余文件清理

- 移除：删除旧版 `install_comfyui.py`（已被v2.0替代）
- 优化：项目结构更简洁，减少混淆

### 📚 文档同步

- 更新：[README.md](README.md)
- 更新：[CHANGELOG.md](CHANGELOG.md)

---

## v6.1 (2026-05-29)

### ✨ 新功能

- **创建 live2d_layer_v6.py**
  - K-means聚类分层工具
  - 优雅降级机制（无numpy时用PIL方案）
  - 完整命令行参数支持

- **创建 create_test_image.py**
  - 测试图像生成工具
  - 用于快速验证工具链

### 🔧 优化改进

- **优化 install_comfyui_advanced.py** (v2.0)
  - 增加非交互模式 (`--yes`)
  - 改进日志记录系统
  - 更好的错误处理和超时控制
  - 支持Git拉取更新现有安装

- **优化 master_tool.py** (v6.1)
  - 改进argparse参数解析
  - 更好的错误处理和用户提示
  - 添加 `--comfyui-dir` 参数
  - 更清晰的输出信息

- **更新 .gitignore**
  - 添加测试文件和临时文件忽略
  - 配置ComfyUI和日志文件忽略

### 📚 文档更新

- 创建 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- 更新 [README.md](README.md)
- 所有文档版本同步

---

## v6.0 (2026-05-29)

### ✨ 重大更新

- **集成 See-through AI分层工具**
  - SIGGRAPH 2026 级别技术
  - LayerDiff 3D + Marigold Depth
  - ComfyUI自动安装脚本

- **创建多个文档**
  - [GITHUB_RESEARCH.md](GITHUB_RESEARCH.md) - GitHub项目研究
  - [SEE_THROUGH_INTEGRATION.md](SEE_THROUGH_INTEGRATION.md) - See-through集成指南
  - 更新 [LIMITATIONS.md](LIMITATIONS.md)
  - 更新 [README.md](README.md)

### 📁 新增文件

- `install_comfyui_advanced.py` - See-through安装器
- `GITHUB_RESEARCH.md` - 研究报告
- `SEE_THROUGH_INTEGRATION.md` - 集成指南

---

## v5.0 (2026-05-22)

### ✨ 核心功能

- 多样化特征系统（94种特征组合）
- 多服务自动降级机制
- 安全API配置工具
- 完整文档体系

### 📚 新增文档

- QUICKSTART.md - 快速入门
- USER_GUIDE.md - 用户指南
- FAQ.md - 常见问题
- BEST_PRACTICES.md - 最佳实践
- LIMITATIONS.md - 限制说明

---

## v4.0 (2026-05-xx)

### ✨ 基础功能

- AI图像生成
- 自动PSD转换
- 基础分层工具

---

## 💡 版本历史说明

- **v6.x** - See-through集成，专业分层时代
- **v5.x** - 多样化特征，安全优化
- **v4.x** - 基础功能实现
- **v3.x** - 早期开发阶段
- **v2.x** - 原型阶段
- **v1.x** - 概念验证

---

## 🔄 更新建议

每次版本升级时：
1. 备份现有项目
2. 更新依赖: `pip install -r requirements.txt`
3. 查看 CHANGELOG 了解变更
4. 阅读相关文档
