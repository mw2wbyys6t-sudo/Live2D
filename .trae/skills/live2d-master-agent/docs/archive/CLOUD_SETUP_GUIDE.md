# ☁️ Live2D Master Agent - 云端资源管理与部署指南

> **一键搞定所有依赖和资源下载！** 自动国内镜像加速，无需手动配置，开箱即用。

---

## 🚀 快速开始（3步安装）

### 方法1：一键安装脚本（推荐）

```bash
# Windows 用户
install.bat

# macOS/Linux 用户
chmod +x install.sh
./install.sh

# 或直接运行 Python 脚本
python install.py
```

### 方法2：使用云端资源管理器

```bash
# 查看所有可用资源
python cloud_resource_manager.py list

# 快速开始（最小安装）
python cloud_resource_manager.py quickstart

# 安装所有必需资源
python cloud_resource_manager.py install --all

# 按类别安装
python cloud_resource_manager.py install --category python
python cloud_resource_manager.py install --category rembg
```

---

## 📦 资源清单

### 必需的依赖（默认安装）

| 资源 | 说明 | 大小 |
|------|------|------|
| Pillow | Python图像处理库 | ~45MB |
| NumPy | 数值计算库 | ~25MB |
| Requests | HTTP请求库 | ~2MB |

### 推荐的增强功能（可选）

| 资源 | 说明 | 大小 | 用途 |
|------|------|------|------|
| psd-tools | PSD文件处理 | ~10MB | PSD生成 |
| SciPy | 科学计算 | ~60MB | 分层优化 |
| Scikit-learn | 机器学习库 | ~30MB | K-means分层 |
| RemBG | AI背景去除 | ~15MB | 背景去除 |

### AI模型（可选）

| 资源 | 说明 | 大小 |
|------|------|------|
| rembg-u2net | 通用人物分割 | ~176MB |
| rembg-u2netp | 轻量版分割模型 | ~4.5MB |
| segment-anything | Meta SAM轻量模型 | ~375MB |

---

## 🎯 资源管理器命令详解

### 1. 列出资源

```bash
# 查看所有资源及其状态
python cloud_resource_manager.py list

# 按类别筛选
python cloud_resource_manager.py list --category python
python cloud_resource_manager.py list --category rembg
python cloud_resource_manager.py list --category models
```

输出示例：
```
====================================================================================================
📦 Live2D Master Agent - 资源清单
====================================================================================================

🐍 Python 依赖包
----------------------------------------------------------------------------------------------------
   [✓] [✅] Pillow                           45.0MB  Python 图像处理库
   [✓] [✅] NumPy                            25.0MB  数值计算库
   [✓] [✅] Requests                          2.0MB  HTTP 请求库
   [ ] [☑️] psd-tools                        10.0MB  PSD 文件处理库
   [ ] [☑️] scipy                            60.0MB  科学计算库
   ...

🧠 rembg AI 模型
----------------------------------------------------------------------------------------------------
   [ ] [☑️] rembg-u2net                     176.0MB  rembg 通用人物分割模型
   [ ] [☑️] rembg-u2netp                      4.5MB  rembg 轻量版分割模型
   ...
```

### 2. 快速开始模式

```bash
python cloud_resource_manager.py quickstart
```

这个模式会：
- 安装核心依赖（Pillow, NumPy, Requests）
- 询问是否需要安装增强功能
- 推荐使用商汤云端生成（无需下载大模型）

### 3. 安装指定资源

```bash
# 安装单个资源
python cloud_resource_manager.py install --ids psd-tools

# 安装多个资源
python cloud_resource_manager.py install --ids psd-tools scipy scikit-learn

# 按类别安装
python cloud_resource_manager.py install --category python
python cloud_resource_manager.py install --category rembg
```

---

## 🌏 国内镜像加速

资源管理器自动配置了国内镜像，大幅提升下载速度：

| 类型 | 镜像源 |
|------|--------|
| PyPI | 清华源、阿里源、中科大源、豆瓣源 |
| GitHub | ghproxy、gh.api.99988866.xyz |
| Hugging Face | hf-mirror、hf-mirror.tuna.tsinghua.edu.cn |

无需手动配置，系统会自动尝试多个镜像源，直到下载成功！

---

## 📋 下载状态持久化

资源管理器会记录下载状态：
- `✓` 已完成
- `-` 已跳过
- ` ` 未开始

状态保存在 `.cache/cloud_resources/download_status.json`，下次安装时会自动跳过已完成的资源。

---

## 💡 最佳实践

### 场景1：VTuber制作（推荐配置）

```bash
# 核心功能
python cloud_resource_manager.py quickstart

# 增强功能（建议选择 3）
# 选择 PSD处理 + 分层增强 + AI背景去除
```

### 场景2：开发环境（完整安装）

```bash
# 安装所有可选依赖
python cloud_resource_manager.py install --ids psd-tools scipy scikit-learn rembg

# 安装常用AI模型
python cloud_resource_manager.py install --ids rembg-u2netp
```

### 场景3：快速演示（最小化安装）

```bash
python cloud_resource_manager.py quickstart
# 选择 1：只安装 PSD 处理
```

---

## 🔧 配置文件

### .env 配置（可选）

如果需要使用云端生成功能：

```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env
# SENSENOVA_API_KEY=your_api_key_here
```

### 环境变量说明

| 变量 | 说明 | 默认值 |
|------|------|--------|
| SENSENOVA_API_KEY | 商汤 SenseNova API Key | - |
| ARK_API_KEY | 火山引擎 API Key | - |
| OUTPUT_DIR | 输出目录 | ./output |

---

## 📊 系统要求

| 配置 | 最低要求 | 推荐配置 |
|------|---------|---------|
| Python | 3.8+ | 3.10+ |
| 内存 | 4GB | 8GB+ |
| 磁盘 | 2GB | 10GB+ |
| 网络 | 有 | 稳定连接 |

---

## ❓ FAQ

### Q: 下载很慢或失败怎么办？
A: 资源管理器会自动尝试多个国内镜像源，请耐心等待。如果某个镜像持续失败，系统会自动切换到下一个。

### Q: 如何重新下载某个资源？
A: 可以直接重新运行安装命令，或删除 `.cache/cloud_resources/download_status.json` 中对应的记录。

### Q: 必须安装所有AI模型吗？
A: 不是。推荐使用商汤云端生成，无需下载任何大模型。只有在需要本地背景去除等功能时才需要安装。

### Q: 可以在没有网络的环境中使用吗？
A: 可以，但需要提前下载好所有依赖和模型，并且需要使用本地SD生成（需要额外模型）。

---

## 📝 更新日志

### v1.0 (2026-06-01)
- ✨ 新增云端资源管理器
- ✨ 支持国内镜像自动加速
- ✨ 一键安装脚本
- ✨ 下载状态持久化
- ✨ 官方标准质量评估

---

## 📖 相关文档

- [README.md](README.md) - 项目主文档
- [QUICKSTART.md](QUICKSTART.md) - 3分钟快速入门
- [CHANGELOG.md](CHANGELOG.md) - 更新日志
- [FAQ.md](FAQ.md) - 常见问题

---

**享受便捷的云端资源管理！** ☁️

