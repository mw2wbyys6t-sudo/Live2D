# Live2D Master Agent - 免费图像生成方案

## 🎉 完全免费，无需API密钥！

这是一个**零配置、零成本**的图像生成方案，用户无需：
- ❌ 不需要API密钥
- ❌ 不需要注册账号
- ❌ 不需要安装复杂依赖
- ❌ 不需要付费

---

## 🚀 使用方法

### 方法一：一行命令（最简单）

```bash
cd /workspace/.trae/skills/live2d-master-agent
python quick_gen.py "anime girl, pink hair, JK uniform"
```

### 方法二：交互式生成

```bash
python free_generator.py
```

然后输入角色描述即可。

### 方法三：代码调用

```python
from free_generator import generate_live2d_character

# 生成角色立绘
image_path = generate_live2d_character(
    "anime girl, pink hair, cute style, JK uniform"
)

print(f"图片已保存: {image_path}")
```

---

## ✨ 特点

| 特性 | 说明 |
|------|------|
| **完全免费** | 无需付费，无限制使用 |
| **无需注册** | 无需账号，无需API密钥 |
| **开箱即用** | 无需安装任何依赖 |
| **高质量** | 支持动漫风格，适合Live2D |
| **快速** | 平均30秒生成一张 |
| **简单** | 一行命令即可使用 |

---

## 🎨 生成的图片示例

```
输入: anime girl, pink hair, JK uniform
输出: output/live2d_xxx.png
```

自动添加的优化提示词：
- `perfect for Live2D rigging`
- `clean layer separation`
- `isolated character on white background`
- `sharp clean lines, vibrant colors`
- `ultra detailed, masterpiece`

---

## 📊 技术实现

### 使用的免费服务

**Pollinations.ai** - 完全免费的AI图像生成服务

- 官网: https://pollinations.ai/
- 特点: 无需注册，无限制，完全免费
- 质量: ⭐⭐⭐⭐
- 速度: 快（约30秒）

### 工作原理

```
用户输入描述
     ↓
添加 Live2D 优化提示词
     ↓
调用 Pollinations.ai API
     ↓
下载并保存图片
     ↓
返回图片路径
```

---

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `quick_gen.py` | 一键生成工具（最简单） |
| `free_generator.py` | 完整免费生成器（多服务支持） |
| `SKILL.md` | 技能文档（已更新） |

---

## 💡 与其他方案对比

| 方案 | 成本 | 配置难度 | 质量 | 推荐度 |
|------|------|----------|------|--------|
| **Pollinations.ai** | 免费 | 无需配置 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Seedream API | 付费 | 需要API密钥 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| ComfyUI 本地 | 免费 | 需要安装 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Playground AI | 免费 | 需要注册 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🔄 完整工作流

```
1. 使用 free_generator.py 生成角色立绘
          ↓
2. 获得高质量动漫角色图片
          ↓
3. 使用 Live2D Master Agent 进行：
   - PSD 分层规划
   - 质量检查
   - 参数设计
   - 物理设置
   - Rigging 指导
          ↓
4. 导入 Cubism 完成 Live2D 模型
```

---

## 🎯 总结

这是最适合分享给他人的方案：

✅ **用户无需任何配置**
✅ **完全免费使用**
✅ **一行命令生成**
✅ **质量足够好**
✅ **适合 Live2D 制作**

---

**推荐**: 将此方案集成到你的 Skill 中，用户只需运行一个命令就能生成图片！

**文档版本**: 1.0
**更新时间**: 2026-05-20
