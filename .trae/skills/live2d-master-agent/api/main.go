package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"

	"live2d-api/config"
	"live2d-api/handlers"
)

func main() {
	// 命令行参数
	var (
		configPath = flag.String("config", "", "配置文件路径")
		host       = flag.String("host", "", "服务器地址")
		port       = flag.Int("port", 0, "服务器端口")
	)
	flag.Parse()

	// 加载配置
	cfg, err := config.LoadConfig(*configPath)
	if err != nil {
		log.Fatalf("加载配置失败: %v", err)
	}

	// 命令行参数覆盖配置
	if *host != "" {
		cfg.Server.Host = *host
	}
	if *port != 0 {
		cfg.Server.Port = *port
	}

	// 确保输出目录存在
	os.MkdirAll(cfg.Output.BaseDir, 0755)

	// 设置 Gin 模式
	gin.SetMode(gin.ReleaseMode)

	// 创建路由
	r := gin.Default()

	// 安全中间件：限制请求体大小，防止内存耗尽
	r.Use(func(c *gin.Context) {
		c.Request.Body = http.MaxBytesReader(c.Writer, c.Request.Body, 10<<20) // 10MB
		c.Next()
	})

	// 安全中间件：添加安全响应头
	r.Use(func(c *gin.Context) {
		c.Header("X-Content-Type-Options", "nosniff")
		c.Header("X-Frame-Options", "DENY")
		c.Header("X-XSS-Protection", "1; mode=block")
		c.Header("Referrer-Policy", "strict-origin-when-cross-origin")
		c.Next()
	})

	// 创建处理器
	h := handlers.NewHandler(cfg)

	// 注册路由
	setupRoutes(r, h)

	// 启动服务器
	addr := fmt.Sprintf("%s:%d", cfg.Server.Host, cfg.Server.Port)
	
	fmt.Println("╔══════════════════════════════════════════════════════════════╗")
	fmt.Println("║     🎨 Live2D Master Agent API v6.3 (Go Edition)            ║")
	fmt.Println("╠══════════════════════════════════════════════════════════════╣")
	fmt.Printf("║  服务地址: http://%s\n", addr)
	fmt.Printf("║  输出目录: %s\n", cfg.Output.BaseDir)
	fmt.Printf("║  SD WebUI: %s\n", cfg.SDWebUI.BaseURL)
	fmt.Printf("║  Python:   %s\n", cfg.Python.PythonPath)
	fmt.Println("╠══════════════════════════════════════════════════════════════╣")
	fmt.Println("║  API 端点:                                                   ║")
	fmt.Println("║    GET  /api/health     - 健康检查                          ║")
	fmt.Println("║    GET  /api/status     - 系统状态                          ║")
	fmt.Println("║    POST /api/generate   - 生成图片                          ║")
	fmt.Println("║    POST /api/psd-plan   - PSD分层规划                       ║")
	fmt.Println("║    POST /api/see-through - See-through工作流                ║")
	fmt.Println("║    GET  /api/scripts    - Python脚本列表                    ║")
	fmt.Println("║    GET  /output/:file   - 获取输出文件                      ║")
	fmt.Println("╚══════════════════════════════════════════════════════════════╝")
	fmt.Println()

	// 使用 http.Server 并配置超时，防止慢速攻击和资源耗尽
	server := &http.Server{
		Addr:              addr,
		Handler:           r,
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       30 * time.Second,
		WriteTimeout:      30 * time.Second,
		IdleTimeout:       120 * time.Second,
		MaxHeaderBytes:    1 << 20, // 1MB
	}

	if err := server.ListenAndServe(); err != nil {
		log.Fatalf("服务器启动失败: %v", err)
	}
}

func setupRoutes(r *gin.Engine, h *handlers.Handler) {
	// API 路由组
	api := r.Group("/api")
	{
		api.GET("/health", h.HealthCheck)
		api.GET("/status", h.GetSystemStatus)
		api.GET("/info", h.GetAPIInfo)
		api.POST("/generate", h.GenerateImage)
		api.POST("/psd-plan", h.CreatePSDPlan)
		api.POST("/see-through", h.RunSeeThrough)
		api.GET("/scripts", h.GetPythonScripts)
	}

	// 静态文件服务
	r.GET("/output/:filename", h.ServeOutput)

	// 根路径
	r.GET("/", h.GetAPIInfo)
}
