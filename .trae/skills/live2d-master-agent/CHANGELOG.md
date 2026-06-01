# 📋 Live2D Master Agent - 更新日志

记录项目的所有重要更新和变更。

---

## v7.1 (2026-06-01) - 工作流优化

### ✨ 基于多维度信息整合的工作流升级

**信息来源：**
- Live2D官方文档 (docs.live2d.com)
- B站社区实践 (bilibili.com)
- GitHub开源项目

### 🎯 `live2d_workflow.py` 升级至 v2.1

- **新增官方PSD标准**
  - 画布高度: 3000-8000px
  - 头部大小: ≥1000px
  - 分辨率: 300dpi
  - 颜色模式: RGB, 8bit/channel, sRGB
  - ArtMesh边距: 1px

- **扩展图层顺序至49层官方标准**
  - 头发分层: 后/侧发左/侧发右/刘海/呆毛/高光/阴影
  - 眼睛分层: 眼白/眼珠/瞳孔/高光/上下睫毛
  - 嘴巴分层: 口腔/舌头/牙齿/下嘴唇/上嘴唇
  - 身体分层: 脖子/胸腔/腰臀/四肢
  - 服装分层: 内衣/外衣/饰品
  - 阴影分层: 头到身体/衣服

- **扩展部件颜色映射**
  - 从5个基础部件扩展至25+精细部件
  - 基于B站拆分标准和官方文档
  - 支持左右对称部件独立识别

- **新增官方标准质量评估**
  - 画布尺寸检查 (权重30%)
  - 边缘清晰度检查 (权重30%)
  - 颜色数量检查 (权重20%)
  - 格式规范检查 (权重20%)
  - 综合评分: 0-100分

- **更新分层指南**
  - 基于官方标准的导入步骤
  - 49层标准图层顺序参考
  - 官方标准注意事项
  - 文件命名规范

- **更新README说明**
  - 官方标准要求说明
  - 导入方法优化
  - 注意事项清单

---

## v7.0 (2026-05-30) - 重大更新

### ✨ 核心升级：图片生成能力全面增强

- **新增商汤SenseNova云端生成**
  - OpenAI兼容API接口
  - 高质量动漫风格生成
  - 智能尺寸映射（适配API限制）

- **新增Live2D分层专用生成模式**
  - `--live2d-rig` 参数启用
  - 6大维度提示词优化（全身照/部件分离/遮挡补全/分层友好/对称性/绑定就绪）
  - 结构化角色解析（中文/英文关键词自动提取）

- **新增一键生成→自动分层**
  - `--auto-layer` 参数启用
  - 生成后自动调用分层工具
  - 支持专业版（pro）和基础版（v6）两种分层工具

- **新增7维度Live2D分层质量评估**
  - 全身可见性、部件边界清晰度、对称性
  - 边缘清晰度、颜色平坦度、背景纯净度、遮挡完整性

- **新增多Provider路由**
  - 自动检测可用Provider
  - 本地SD / 商汤SenseNova 智能选择

- **安全审计修复**
  - 修复7项安全问题（路径遍历/命令注入/信息泄露等）
  - API Key环境变量管理
  - `.env` 文件支持

---

## v6.3 (2026-05-29)

### ✨ 重大新功能：Stable Diffusion WebUI 集成

- **创建 sd_webui_integration.py**
  - 🎯 完整的 Stable Diffusion WebUI API 客户端
  - 🎯 自动检测服务可用性
  - 🎯 内置 Live2D 优化提示词和反向提示词
  - 🎯 支持自定义采样器、步数、CFG 等参数
  - 🎯 智能错误处理和重试机制

- **更新 master_tool.py** (v6.3)
  - 🎯 多源智能选择：SD WebUI > Pollinations
  - 🎯 新增 `--sd-webui-url` 参数
  - 🎯 自动降级到 Pollinations（当 SD WebUI 不可用时）
  - 🎯 更好的用户提示和使用指南
  - 🎯 所有现有功能保留，向后兼容

- **创建 OPENSOURCE_INTEGRATION.md**
  - 🎯 完整的开源项目研究报告
  - 🎯 SD WebUI 集成详细文档
  - 🎯 ComfyUI API 集成方案
  - 🎯 推荐模型和配置指南

### 🎯 核心架构改进

- 多引擎设计：支持本地和云端生成
- 灵活降级：本地不可用时自动使用在线服务
- 前后连接通：API 级别的完整集成

### 📚 文档更新

- 创建 [OPENSOURCE_INTEGRATION.md](OPENSOURCE_INTEGRATION.md)
- 更新 [README.md](README.md)
- 更新 [CHANGELOG.md](CHANGELOG.md)

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
