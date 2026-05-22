# 🔐 GitHub 认证问题解决方案

## 问题描述

在当前环境中执行 `git push` 时出现错误：

```
fatal: could not read Username for 'https://github.com': terminal prompts disabled
```

这是因为Git无法进行交互式登录。

---

## ✅ 解决方案

### 方案1：使用Personal Access Token（推荐）

#### 步骤1：创建Personal Access Token

1. 访问：https://github.com/settings/tokens
2. 点击：**Generate new token** → **Generate new token (classic)**
3. 设置Token名称（例如：`live2d-upload`）
4. **勾选权限**：`repo` (所有仓库权限)
5. 点击：**Generate token**
6. ⭐ **立即复制Token**（刷新页面后会消失）

#### 步骤2：配置Git使用Token

在终端中运行：

```bash
# 配置Git记住凭据（仅限个人设备）
git config --global credential.helper store

# 第一次推送时，Username输入你的GitHub用户名
# Password输入刚才的Personal Access Token
```

#### 步骤3：再次推送

```bash
cd /workspace/.trae/skills/live2d-master-agent
git push -u origin main
```

---

### 方案2：使用SSH方式

#### 步骤1：检查是否有SSH密钥

```bash
ls -la ~/.ssh/
```

#### 步骤2：生成SSH密钥（如果没有）

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# 按回车接受默认位置
# 输入密码（可选）

cat ~/.ssh/id_ed25519.pub
# 复制公钥内容
```

#### 步骤3：在GitHub添加SSH公钥

1. 访问：https://github.com/settings/keys
2. 点击：**New SSH key**
3. Title：填写描述（如：`My Laptop`）
4. Key：粘贴刚才复制的公钥
5. 点击：**Add SSH key**

#### 步骤4：更改远程仓库为SSH方式

```bash
cd /workspace/.trae/skills/live2d-master-agent

# 先移除HTTPS方式的origin
git remote remove origin

# 添加SSH方式的origin
git remote add origin git@github.com:mw2wbyys6t-sudo/Live2d--master--Agent.git

# 推送
git push -u origin main
```

---

### 方案3：在其他终端手动执行（最简单）

#### 步骤1：打开本地终端

在您的电脑上打开终端或命令提示符

#### 步骤2：克隆仓库（或拉取最新）

```bash
cd /workspace/.trae/skills/live2d-master-agent
# 或者克隆
# git clone https://github.com/mw2wbyys6t-sudo/Live2d--master--Agent.git
```

#### 步骤3：执行推送命令

```bash
cd /workspace/.trae/skills/live2d-master-agent

git remote add origin https://github.com/mw2wbyys6t-sudo/Live2d--master--Agent.git
git branch -M main
git push -u origin main
```

#### 步骤4：输入GitHub凭据

- **Username**: `mw2wbyys6t-sudo`
- **Password**: 您的GitHub密码或Personal Access Token

---

### 方案4：使用GitHub CLI

#### 安装GitHub CLI

**macOS:**
```bash
brew install gh
```

**Windows:**
```bash
winget install GitHub CLI
```

**Linux:**
```bash
sudo apt install gh
```

#### 登录GitHub

```bash
gh auth login
# 选择 HTTPS
# 选择 Yes 登录浏览器
# 完成认证
```

#### 推送

```bash
cd /workspace/.trae/skills/live2d-master-agent
gh repo set-default mw2wbyys6t-sudo/Live2d--master--Agent
git push -u origin main
```

---

## 📝 快速参考命令

### 检查当前状态

```bash
cd /workspace/.trae/skills/live2d-master-agent

# 查看远程仓库
git remote -v

# 查看提交历史
git log --oneline

# 查看状态
git status
```

### 凭据配置

```bash
# 记住凭据（7天有效）
git config --global credential.helper "cache --timeout 604800"

# 或永久记住
git config --global credential.helper store
```

---

## ⚠️ 注意事项

1. **Personal Access Token安全**：不要泄露给他人
2. **SSH密钥**：不要与他人分享私钥（id_ed25519）
3. **选择方案**：根据您的设备和偏好选择最适合的方案

---

## 🎯 推荐流程（最适合新手）

1. **创建Personal Access Token**（步骤1）
2. **配置Git凭据**（步骤2）
3. **再次推送**（步骤3）

这三步最简单，不需要额外安装软件！

---

**有疑问？** 查看GitHub官方文档：https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github
