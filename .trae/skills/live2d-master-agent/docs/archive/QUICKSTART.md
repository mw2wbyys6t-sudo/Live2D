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
