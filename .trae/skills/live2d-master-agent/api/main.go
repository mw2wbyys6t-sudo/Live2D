package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"runtime"
	"time"

	"github.com/gin-contrib/gzip"
	"github.com/gin-gonic/gin"

	"live2d-api/config"
	"live2d-api/handlers"
	"live2d-api/services"
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

	// 设置最大并发数为 CPU 核心数的 2 倍
	runtime.GOMAXPROCS(runtime.NumCPU() * 2)

	// 确保输出目录存在
	os.MkdirAll(cfg.Output.BaseDir, 0755)

	// 设置 Gin 模式
	gin.SetMode(gin.ReleaseMode)

	// 创建路由
	r := gin.Default()

	// ========== 性能优化中间件 ==========

	// Gzip 压缩中间件（提升响应速度）
	r.Use(gzip.Gzip(gzip.DefaultCompression))

	// 请求体大小限制中间件
	r.Use(func(c *gin.Context) {
		c.Request.Body = http.MaxBytesReader(c.Writer, c.Request.Body, cfg.Server.MaxRequestBodySize)
		c.Next()
	})

	// 请求超时中间件
	r.Use(func(c *gin.Context) {
		c.Request.Header.Set("Connection", "keep-alive")
		c.Next()
	})

	// 安全响应头中间件
	r.Use(func(c *gin.Context) {
		c.Header("X-Content-Type-Options", "nosniff")
		c.Header("X-Frame-Options", "DENY")
		c.Header("X-XSS-Protection", "1; mode=block")
		c.Header("Referrer-Policy", "strict-origin-when-cross-origin")
		c.Header("Content-Security-Policy", "default-src 'self'")
		c.Header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
		c.Next()
	})

	// CORS 中间件
	r.Use(func(c *gin.Context) {
		origin := c.Request.Header.Get("Origin")
		if origin != "" {
			// 生产环境中应使用白名单验证 origin
			allowedOrigins := cfg.Server.AllowedOrigins
			if len(allowedOrigins) == 0 || contains(allowedOrigins, origin) {
				c.Header("Access-Control-Allow-Origin", origin)
				c.Header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
				c.Header("Access-Control-Allow-Headers", "Content-Type, Authorization")
				c.Header("Access-Control-Allow-Credentials", "true")
			}
		}
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(http.StatusNoContent)
			return
		}
		c.Next()
	})

	// ========== 创建服务和处理器 ==========

	// 创建图像生成服务（带缓存）
	imageService := services.NewImageGenerator(cfg)
	cacheService := services.NewRequestCache(cfg.Cache)
	
	// 创建处理器
	h := handlers.NewHandler(cfg, imageService, cacheService)

	// ========== 注册路由 ==========
	setupRoutes(r, h)

	// ========== 启动服务器 ==========
	addr := fmt.Sprintf("%s:%d", cfg.Server.Host, cfg.Server.Port)

	printServerInfo(cfg, addr)

	// 配置高性能 HTTP 服务器
	server := &http.Server{
		Addr:              addr,
		Handler:           r,
		ReadHeaderTimeout: cfg.Server.ReadHeaderTimeout,
		ReadTimeout:       cfg.Server.ReadTimeout,
		WriteTimeout:      cfg.Server.WriteTimeout,
		IdleTimeout:       cfg.Server.IdleTimeout,
		MaxHeaderBytes:    cfg.Server.MaxHeaderBytes,
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
		api.GET("/models", h.GetModels)
		api.POST("/generate", h.GenerateImage)
		api.POST("/psd-plan", h.CreatePSDPlan)
		api.POST("/see-through", h.RunSeeThrough)
		api.GET("/scripts", h.GetPythonScripts)
		api.GET("/cache/stats", h.GetCacheStats)
		api.POST("/cache/clear", h.ClearCache)
	}

	// 静态文件服务（带缓存）
	r.GET("/output/:filename", h.ServeOutput)

	// 根路径
	r.GET("/", h.GetAPIInfo)
}

func printServerInfo(cfg *config.Config, addr string) {
	fmt.Println("\n" + "="*80)
	fmt.Println("║     🎨 Live2D Master Agent API v7.1 (Go Edition)           ║")
	fmt.Println("║     高性能优化版本 - 支持连接池、并发处理、请求缓存          ║")
	fmt.Println("="*80)
	fmt.Printf("║  服务地址: http://%s\n", addr)
	fmt.Printf("║  输出目录: %s\n", cfg.Output.BaseDir)
	fmt.Printf("║  Python:   %s\n", cfg.Python.PythonPath)
	fmt.Printf("║  最大并发: %d\n", runtime.NumCPU()*2)
	fmt.Printf("║  缓存大小: %dMB\n", cfg.Cache.MaxSizeMB)
	fmt.Println("="*80)
	fmt.Println("║  API 端点:                                                   ║")
	fmt.Println("║    GET  /api/health      - 健康检查                         ║")
	fmt.Println("║    GET  /api/status      - 系统状态                         ║")
	fmt.Println("║    GET  /api/info        - API信息                          ║")
	fmt.Println("║    GET  /api/models      - 可用模型列表                     ║")
	fmt.Println("║    POST /api/generate    - 生成图片（支持缓存）              ║")
	fmt.Println("║    POST /api/psd-plan    - PSD分层规划                      ║")
	fmt.Println("║    POST /api/see-through - See-through工作流                ║")
	fmt.Println("║    GET  /api/scripts     - Python脚本列表                   ║")
	fmt.Println("║    GET  /api/cache/stats - 缓存统计                         ║")
	fmt.Println("║    POST /api/cache/clear - 清除缓存                         ║")
	fmt.Println("║    GET  /output/:file    - 获取输出文件                     ║")
	fmt.Println("="*80)
	fmt.Println()
}

func contains(slice []string, item string) bool {
	for _, s := range slice {
		if s == item {
			return true
		}
	}
	return false
}
