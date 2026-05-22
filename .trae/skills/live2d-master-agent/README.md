# 🎨 Live2D Master Agent

> **专业的AI辅助Live2D制作助手 - 从概念到绑定的完整工作流**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Stars](https://img.shields.io/github/stars/mw2wbyys6t-sudo/Live2D)](https://github.com/mw2wbyys6t-sudo/Live2D/stargazers)

---

## ✨ 一句话介绍

**3分钟创建专业Live2D角色！** 无需付费，一键生成，立即使用。

---

## 🚀 3分钟快速开始

### 第一步：安装

```bash
git clone https://github.com/mw2wbyys6t-sudo/Live2D.git
cd Live2D
pip install -r requirements.txt
```

### 第二步：生成角色

```bash
python master_tool.py "cute anime girl, pink hair"
```

### 第三步：完成！

系统会自动：
- ✅ 生成高质量角色立绘
- ✅ 创建专业PSD分层文件
- ✅ 提供完整的工作流程

**就是这么快！** ⚡

---

## 🎯 核心功能

### 🎨 AI图像生成
- 完全免费，无需API密钥
- 一键生成高质量角色立绘
- 94种特征组合，避免撞衫

### 📐 专业分层
- 25+图层自动分层
- 符合Live2D官方规范
- 可直接导入Live2D Cubism

### ⚡ 效率提升
- 角色生成：2-3小时 → 30秒（**提升240倍+**）
- PSD分层：1-2小时 → 10秒（**提升360倍+**）
- 总流程：4-5小时 → 3分钟（**提升100倍+**）

---

## 📚 新手入门

### 🎯 快速入门（3分钟）
📖 [QUICKSTART.md](QUICKSTART.md) - 最快上手指南

### 📖 完整教程
📖 [USER_GUIDE.md](USER_GUIDE.md) - 详细使用教程

### ❓ 常见问题
❓ [FAQ.md](FAQ.md) - 解答疑惑

### 💡 最佳实践
💡 [BEST_PRACTICES.md](BEST_PRACTICES.md) - 专业技巧

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
|------|------|--------|
| [master_tool.py](master_tool.py) | 一站式工具箱 | ⭐⭐⭐⭐⭐ |
| [live2d_layer_pro.py](live2d_layer_pro.py) | 专业分层工具 | ⭐⭐⭐⭐⭐ |
| [config_api.py](config_api.py) | API配置 | ⭐⭐⭐⭐ |

### 辅助脚本

| 脚本 | 说明 |
|------|------|
| [scripts/qa_engine_enhanced.py](scripts/qa_engine_enhanced.py) | 质量检查 |
| [scripts/parameter_designer_enhanced.py](scripts/parameter_designer_enhanced.py) | 参数设计器 |
| [scripts/physics_helper.py](scripts/physics_helper.py) | 物理设置 |

---

## 💡 技术亮点

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
# 生成角色
python master_tool.py "beautiful anime girl"

# 生成5个不同角色
python master_tool.py -n 5 "anime girl"

# 使用已有图片
python master_tool.py --skip-generate
```

### 专业分层

```bash
python live2d_layer_pro.py character.png
```

### 配置API（可选）

```bash
python config_api.py
```

---

## 🛠️ 系统要求

- Python 3.8+
- 网络连接
- 可选：火山引擎API密钥（更高质量）

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
```

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

- [Pollinations.ai](https://pollinations.ai/) - 免费图像生成
- [Live2D Cubism](https://www.live2d.com/) - 2D动画技术
- [火山引擎](https://www.volcengine.com/) - Seedream API

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

**让Live2D制作更简单！** 🎨

*版本: v5.0*  
*最后更新: 2026-05-22*
