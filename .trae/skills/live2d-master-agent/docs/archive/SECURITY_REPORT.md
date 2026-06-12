# 🔒 Live2D Master Agent - 安全审查报告

**审查日期**: 2026-05-29  
**审查版本**: v6.3  
**审查范围**: Python 工具链 + Go API 服务  

---

## 📋 执行摘要

本次安全审查发现了 **3 个中等风险** 和 **4 个低风险** 问题。没有发现严重或高危漏洞。所有问题都可以通过代码改进修复，不会影响现有功能。

**总体评估**: 🟡 中等风险 - 建议修复后使用

---

## 🔴 发现的问题

### 问题 1: HTTP 服务器缺少超时设置 [中等]

**规则**: GO-HTTP-001  
**位置**: `api/main.go`  
**严重性**: 中

**问题描述**:  
Go API 服务使用 `gin.Default()` 启动，没有配置 `http.Server` 的超时参数。这可能导致：
- 慢速 HTTP 攻击 (Slowloris)
- 连接耗尽 (Connection Exhaustion)
- 资源泄漏

**当前代码**:
```go
r := gin.Default()
// ... 注册路由 ...
r.Run(addr)  // 使用默认 http.Server，超时为 0
```

**修复建议**:
```go
server := &http.Server{
    Addr:              addr,
    Handler:           r,
    ReadHeaderTimeout: 5 * time.Second,
    ReadTimeout:       30 * time.Second,
    WriteTimeout:      30 * time.Second,
    IdleTimeout:       120 * time.Second,
    MaxHeaderBytes:    1 << 20, // 1MB
}
server.ListenAndServe()
```

---

### 问题 2: 路径遍历检查不够严谨 [中等]

**规则**: GO-PATH-001 / FLASK-PATH-001  
**位置**: `api/handlers/handlers.go:191-199`  
**严重性**: 中

**问题描述**:  
`isPathSafe` 函数使用字符串前缀匹配检查路径安全性，这种方法不够严谨：

```go
func isPathSafe(path, baseDir string) bool {
    absPath, _ := filepath.Abs(path)
    absBase, _ := filepath.Abs(baseDir)
    return len(absPath) >= len(absBase) && absPath[:len(absBase)] == absBase
}
```

**风险**:  
- 符号链接可能绕过检查
- 路径规范化不够严格

**修复建议**:
```go
func isPathSafe(path, baseDir string) bool {
    absPath, err := filepath.Abs(path)
    if err != nil {
        return false
    }
    absBase, err := filepath.Abs(baseDir)
    if err != nil {
        return false
    }
    
    // 使用 filepath.Rel 进行更严格的检查
    rel, err := filepath.Rel(absBase, absPath)
    if err != nil {
        return false
    }
    
    // 确保相对路径不包含 ..
    return !strings.HasPrefix(rel, "..") && rel != ".."
}
```

---

### 问题 3: Python 桥接层命令注入风险 [中等]

**规则**: GO-INJECT-002 / FLASK-INJECT-002  
**位置**: `api/services/python_bridge.go:37, 73`  
**严重性**: 中

**问题描述**:  
`exec.Command` 使用用户提供的 `imagePath` 作为参数：

```go
cmd := exec.Command(pb.cfg.Python.PythonPath, scriptPath, imagePath)
```

虽然 `exec.Command` 在 Go 中不调用 shell，但如果 `imagePath` 包含特殊字符或以 `-` 开头，可能被 Python 脚本解析为命令行选项。

**修复建议**:
```go
// 验证 imagePath 不包含危险字符
func validateImagePath(path string) error {
    if strings.Contains(path, ";") || strings.Contains(path, "&") || 
       strings.Contains(path, "|") || strings.Contains(path, "$") {
        return fmt.Errorf("路径包含非法字符")
    }
    if strings.HasPrefix(filepath.Base(path), "-") {
        return fmt.Errorf("文件名不能以 - 开头")
    }
    return nil
}
```

---

### 问题 4: 缺少请求体大小限制 [低]

**规则**: GO-HTTP-002  
**位置**: `api/handlers/handlers.go`  
**严重性**: 低

**问题描述**:  
API 端点没有限制请求体大小，可能导致内存耗尽。

**修复建议**:
```go
// 在路由注册时添加限制
r.Use(func(c *gin.Context) {
    // 限制请求体为 10MB
    c.Request.Body = http.MaxBytesReader(c.Writer, c.Request.Body, 10<<20)
    c.Next()
})
```

---

### 问题 5: 缺少安全响应头 [低]

**规则**: GO-HTTP-004 / FLASK-HEADERS-001  
**位置**: `api/main.go`  
**严重性**: 低

**问题描述**:  
HTTP 响应缺少安全头：
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Content-Security-Policy`

**修复建议**:
```go
r.Use(func(c *gin.Context) {
    c.Header("X-Content-Type-Options", "nosniff")
    c.Header("X-Frame-Options", "DENY")
    c.Header("Content-Security-Policy", "default-src 'self'")
    c.Next()
})
```

---

### 问题 6: 网络请求缺少重定向限制 [低]

**规则**: GO-SSRF-001  
**位置**: `api/services/image_generator.go`  
**严重性**: 低

**问题描述**:  
HTTP 客户端没有限制重定向次数，可能被用于 SSRF 攻击。

**修复建议**:
```go
httpClient := &http.Client{
    Timeout: 200 * time.Second,
    CheckRedirect: func(req *http.Request, via []*http.Request) error {
        if len(via) >= 5 {
            return fmt.Errorf("too many redirects")
        }
        return nil
    },
}
```

---

### 问题 7: Python 代码中的 subprocess 风险 [低]

**规则**: FLASK-INJECT-002  
**位置**: `master_tool.py:407-422`  
**严重性**: 低

**问题描述**:  
`subprocess.run` 调用外部脚本时，虽然使用了列表参数（安全），但缺少对 `image_path` 的验证：

```python
result = subprocess.run(
    [sys.executable, 'live2d_layer_pro.py', image_path],
    capture_output=True,
    text=True,
    timeout=120
)
```

**修复建议**:
```python
import re

def validate_image_path(path):
    """验证图片路径安全"""
    if not path or not isinstance(path, str):
        return False
    # 检查非法字符
    if re.search(r'[;&|`$]', path):
        return False
    # 检查路径是否在允许范围内
    allowed_base = Path(__file__).parent / "output"
    try:
        path_obj = Path(path).resolve()
        allowed_base = allowed_base.resolve()
        return str(path_obj).startswith(str(allowed_base))
    except:
        return False
```

---

## ✅ 安全实践（已正确实现）

### 1. 没有硬编码密钥
- ✅ Python 代码中没有硬编码 API Key
- ✅ Go 代码中没有硬编码密钥
- ✅ 使用环境变量和配置文件管理敏感信息

### 2. 安全的文件服务
- ✅ `ServeOutput` 函数实现了路径安全检查
- ✅ 使用 `filepath.Join` 而不是字符串拼接

### 3. 安全的子进程调用
- ✅ Python 代码使用列表参数而非字符串
- ✅ Go 代码使用 `exec.Command` 而非 `sh -c`
- ✅ 没有使用 `shell=True`

### 4. 没有危险的反序列化
- ✅ 没有使用 `pickle`、`yaml.load` 等危险函数
- ✅ 使用 `json` 进行安全的序列化

### 5. 没有 eval/exec
- ✅ 代码中没有 `eval()` 或 `exec()` 的使用

---

## 🔧 修复优先级

| 优先级 | 问题 | 影响 | 修复难度 |
|--------|------|------|---------|
| 🔴 P1 | HTTP 超时设置 | DoS 风险 | 简单 |
| 🔴 P1 | 路径遍历检查 | 文件泄露 | 简单 |
| 🟡 P2 | 命令注入防护 | 代码执行 | 中等 |
| 🟡 P2 | 请求体限制 | DoS 风险 | 简单 |
| 🟢 P3 | 安全响应头 | XSS/点击劫持 | 简单 |
| 🟢 P3 | 重定向限制 | SSRF | 简单 |
| 🟢 P3 | Python 路径验证 | 代码执行 | 简单 |

---

## 📚 参考

- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [Go Security Best Practices](https://go.dev/doc/security/)
- [Flask Security Documentation](https://flask.palletsprojects.com/en/stable/security/)

---

**报告生成时间**: 2026-05-29  
**审查工具**: security-best-practices skill + 手动代码审查
