# 🔒 Live2D Master Agent - 安全指南

> **保护你的API密钥和敏感数据**

---

## 📋 安全特性概览

| 特性 | 版本 | 说明 |
|------|------|------|
| 加密存储 | v7.1+ | API密钥使用Fernet加密存储 |
| 私有字典 | v7.1+ | 密钥不写入os.environ |
| 内存清理 | v7.1+ | 程序退出时自动清除密钥 |
| 输入验证 | v7.1+ | 路径遍历和命令注入防护 |
| 日志脱敏 | v7.1+ | 自动隐藏日志中的密钥 |
| 速率限制 | v7.1+ | API请求频率限制 |
| 安全响应头 | v7.1+ | HTTP安全头配置 |

---

## 🔐 API密钥安全

### 加密存储

项目使用 **Fernet (AES-128-CBC)** 加密存储API密钥：

```python
from config import config

# 加密存储API密钥
config.store_api_key_encrypted('sensenova', 'sk-your-key-here')

# 自动读取（解密）
api_key = config.sensenova_api_key
```

**安全特性：**
- 密钥派生使用 **PBKDF2-HMAC-SHA256**，100,000次迭代
- 盐值基于系统信息（主机名、用户名）
- 加密文件权限设置为 **600**（仅所有者可读写）

### 文件位置

| 文件 | 说明 | 是否提交到Git |
|------|------|---------------|
| `.env` | 环境变量文件 | ❌ 否（.gitignore保护） |
| `.env.encrypted` | 加密后的密钥 | ❌ 否（.gitignore保护） |
| `.env.example` | 配置模板 | ✅ 是 |

### 最佳实践

1. **永远不要提交 `.env` 文件**
   ```bash
   # 确认.gitignore包含
   echo ".env" >> .gitignore
   echo ".env.encrypted" >> .gitignore
   ```

2. **定期更换API密钥**
   ```bash
   # 更新密钥
   python -c "from config import config; config.store_api_key_encrypted('sensenova', 'sk-new-key')"
   ```

3. **检查文件权限**
   ```bash
   # Linux/Mac
   chmod 600 .env .env.encrypted
   
   # 验证
   ls -la .env*
   ```

---

## 🛡️ 输入安全

### 路径遍历防护

所有文件操作都经过路径验证：

```python
from security_fixes import validate_path

# 安全的文件操作
safe_path = validate_path(user_input_path)
if safe_path:
    with open(safe_path, 'r') as f:
        content = f.read()
```

**防护措施：**
- 禁止 `..` 路径遍历
- 禁止绝对路径
- 禁止特殊字符 (`;`, `&`, `|`, `*`)
- 路径长度限制 (4096字符)

### 命令注入防护

Python脚本执行使用安全参数传递：

```go
// Go后端执行Python脚本
cmd := exec.CommandContext(ctx, pythonPath, args...)
cmd.Env = []string{
    "PYTHONIOENCODING=utf-8",
    // 不传递包含密钥的环境变量
}
```

**防护措施：**
- 使用 `--` 分隔选项和参数
- 禁止提示词以 `-` 开头
- 超时控制（5分钟）
- 输出脱敏处理

---

## 📊 日志安全

### 自动脱敏

日志中的敏感信息自动被隐藏：

```go
// 脱敏函数
func sanitizeOutput(output string) string {
    patterns := []string{
        `sk-[a-zA-Z0-9]{20,}`,           // API密钥
        `api[_-]?key["\s]*[:=]["\s]*[^\s"]+`,
        `secret["\s]*[:=]["\s]*[^\s"]+`,
        `password["\s]*[:=]["\s]*[^\s"]+`,
        `token["\s]*[:=]["\s]*[^\s"]+`,
    }
    // 替换为 [REDACTED]
}
```

**示例：**
```
原始: Error: sk-9JrYWS8XkB3JcryclGXF6K89CgpOlJvI failed
脱敏: Error: [REDACTED] failed
```

---

## 🌐 网络安全

### 安全响应头

API服务自动配置安全响应头：

| 响应头 | 值 | 说明 |
|--------|-----|------|
| X-Content-Type-Options | nosniff | 防止MIME嗅探 |
| X-Frame-Options | DENY | 禁止iframe嵌入 |
| X-XSS-Protection | 1; mode=block | XSS防护 |
| Content-Security-Policy | default-src 'self' | CSP策略 |
| Strict-Transport-Security | max-age=31536000 | HSTS |

### 速率限制

API请求频率限制：
- 每分钟最多 **60** 请求
- 超过限制返回 **429** 状态码
- 自动清理过期记录

### CORS配置

跨域请求白名单验证：

```go
allowedOrigins := cfg.Server.AllowedOrigins
if contains(allowedOrigins, origin) {
    // 允许跨域
}
```

---

## 🔍 安全审计

### 代码审查清单

- [ ] API密钥不硬编码在代码中
- [ ] 敏感信息不写入日志
- [ ] 文件操作经过路径验证
- [ ] 用户输入经过清理
- [ ] 网络请求使用HTTPS
- [ ] 错误信息不暴露内部细节

### 定期安全检查

```bash
# 检查是否有密钥泄露
grep -r "sk-" --include="*.py" --include="*.go" --include="*.md" .

# 检查.gitignore配置
cat .gitignore | grep -E "\.env|secret|key"

# 检查文件权限
ls -la .env* 2>/dev/null
```

---

## 🚨 安全事件响应

### 如果API密钥泄露

1. **立即撤销密钥**
   - 登录商汤/火山引擎控制台
   - 删除或禁用泄露的密钥

2. **生成新密钥**
   ```python
   from config import config
   config.store_api_key_encrypted('sensenova', 'sk-new-key')
   ```

3. **检查日志**
   ```bash
   # 查看最近的API调用
   grep "sensenova" logs/*.log
   ```

4. **更新.gitignore**
   ```bash
   echo ".env*" >> .gitignore
   git rm --cached .env .env.encrypted
   ```

---

## 📞 报告安全问题

如果发现安全漏洞，请：

1. **不要**在公开渠道披露
2. 发送邮件至项目维护者
3. 或创建私有GitHub Security Advisory

---

**保持安全，保护你的创作！** 🔒

*版本: v7.1*
*最后更新: 2026-06-12*
