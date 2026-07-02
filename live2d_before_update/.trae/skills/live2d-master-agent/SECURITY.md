# Live2D Master Agent - 安全指南

## API密钥安全

### 加密存储方案

本项目使用 **Fernet 对称加密** 保护API密钥：

- **算法**: AES-128-CBC + HMAC-SHA256
- **密钥派生**: PBKDF2-HMAC-SHA256（100,000次迭代）
- **盐值来源**: 系统环境信息（主机名、用户名、操作系统）
- **绑定机器**: 加密文件仅在当前机器可解密

### 密钥存储架构

```
.env (明文，仅本地)  →  .env.encrypted (加密文件)
        ↓                        ↓
   SecureConfig              EncryptedConfig
   (私有字典存储)           (Fernet加密存储)
        ↓                        ↓
   不写入os.environ          解密后缓存到内存
```

### 安全特性

1. **SecureConfig单例模式**: 全局唯一实例，密钥存储在私有字典
2. **不泄露到环境变量**: 敏感键（API_KEY、SECRET_KEY等）不写入`os.environ`
3. **加密文件保护**: `.env.encrypted`使用Fernet加密，绑定当前机器
4. **内存安全清理**: 程序退出时自动覆盖和清除内存中的密钥
5. **repr安全**: `print(config)`不会暴露完整密钥
6. **格式验证**: `validate_api_key()`检查密钥格式有效性

### 使用方式

```python
from config import config

# 获取API密钥（安全方式）
api_key = config.sensenova_api_key

# 验证密钥格式
is_valid = config.validate_api_key("sensenova")

# 加密存储密钥
config.store_api_key_encrypted("sensenova", "sk-xxxxx")
```

## Go后端安全

### 安全中间件

1. **输入验证中间件**: Content-Type验证、路径遍历防护、User-Agent检查
2. **速率限制中间件**: 每IP每分钟60请求限制
3. **安全响应头**: X-Content-Type-Options、X-Frame-Options、CSP等
4. **请求体大小限制**: 防止大请求攻击

### Python脚本沙箱

1. **超时控制**: 5分钟执行超时，自动终止子进程
2. **环境变量过滤**: 只传递必要的环境变量，不泄露敏感信息
3. **输出脱敏**: `sanitizeOutput()`正则替换API密钥等敏感信息
4. **路径验证**: `validatePath()`防止命令注入和路径遍历
5. **进程组隔离**: 使用`Setpgid`创建独立进程组，便于终止

## 文件保护

### .gitignore规则

```
.env
.env.*
*.encrypted
```

### 文件权限

- `.env`: 600（仅所有者可读写）
- `.env.encrypted`: 600（仅所有者可读写）

## 安全检查清单

- [x] API密钥不硬编码在源码中
- [x] .env文件已加入.gitignore
- [x] .env.encrypted已从git跟踪中移除
- [x] SecureConfig不将密钥写入os.environ
- [x] Go后端有输入验证和速率限制
- [x] Python脚本执行有沙箱隔离
- [x] 输出脱敏防止密钥泄露
- [x] 程序退出时清理内存中的密钥
