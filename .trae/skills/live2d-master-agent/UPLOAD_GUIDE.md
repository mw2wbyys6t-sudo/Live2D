# 🚀 一键上传GitHub - 简易指南

## 方案A：使用助手脚本（推荐）

### 步骤1：在GitHub创建仓库

1. 访问：https://github.com/new
2. 仓库名：`live2d-master-agent`
3. 描述：`专业的AI辅助Live2D制作助手`
4. 选择：`Public`（公开）
5. **不要勾选**任何初始化选项
6. 点击：`Create repository`

### 步骤2：运行助手脚本

回到终端，运行：

```bash
cd /workspace/.trae/skills/live2d-master-agent
python upload_to_github.py
```

### 步骤3：按照提示操作

脚本会引导您输入GitHub用户名，然后自动推送！

---

## 方案B：手动命令行

如果您想手动操作，按以下步骤：

### 1️⃣ 确保在正确目录

```bash
cd /workspace/.trae/skills/live2d-master-agent
```

### 2️⃣ 关联GitHub仓库（请替换 YOUR_USERNAME）

```bash
git remote add origin https://github.com/YOUR_USERNAME/live2d-master-agent.git
```

### 3️⃣ 重命名分支为main

```bash
git branch -M main
```

### 4️⃣ 推送到GitHub

```bash
git push -u origin main
```

---

## 💡 登录提示

当您运行 `git push` 时，GitHub会提示登录：

- **用户名**: 您的GitHub用户名
- **密码/Token**: 推荐使用Personal Access Token

### 获取Token：

1. 访问：https://github.com/settings/tokens
2. 点击：`Generate new token` (classic)
3. 勾选：`repo` 权限
4. 生成并复制Token
5. 在密码处粘贴Token

---

## ✅ 上传成功后

您的仓库链接将是：
```
https://github.com/YOUR_USERNAME/live2d-master-agent
```

### 下一步：

1. 在TRAE社区分享链接
2. 邀请好友使用
3. 继续优化项目

---

## 🆘 遇到问题？

### 问题1：提示 "remote origin already exists"

**解决：**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/live2d-master-agent.git
```

### 问题2：权限被拒绝

**解决：**
- 确保仓库已创建
- 检查用户名和Token是否正确
- 使用Personal Access Token而不是密码

### 问题3：其他错误

查看更详细的指南：
- [QUICK_START_GITHUB.md](QUICK_START_GITHUB.md)
- [GITHUB_SETUP.md](GITHUB_SETUP.md)

---

**祝上传顺利！** 🎊
