package handlers

import (
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/gin-gonic/gin"

	"live2d-api/config"
	"live2d-api/models"
	"live2d-api/services"
)

type Handler struct {
	cfg            *config.Config
	imageGenerator *services.ImageGenerator
	pythonBridge   *services.PythonBridge
	cache          *services.RequestCache
	startTime      time.Time
}

func NewHandler(cfg *config.Config, imageGenerator *services.ImageGenerator, cache *services.RequestCache) *Handler {
	h := &Handler{
		cfg:            cfg,
		imageGenerator: imageGenerator,
		pythonBridge:   services.NewPythonBridge(cfg),
		cache:          cache,
		startTime:      time.Now(),
	}

	// 启动缓存清理守护进程
	if cache != nil {
		cache.StartCleanupDaemon(5 * time.Minute)
	}

	return h
}

// HealthCheck 健康检查
func (h *Handler) HealthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Message: "Live2D API 服务正常运行",
		Data: map[string]interface{}{
			"version": "v7.1-go",
			"uptime":  time.Since(h.startTime).String(),
		},
	})
}

// GetSystemStatus 获取系统状态
func (h *Handler) GetSystemStatus(c *gin.Context) {
	var services []models.ServiceStatus

	// 本地生成器状态
	localAvailable, localMsg := h.imageGenerator.CheckLocalGeneratorStatus()
	services = append(services, models.ServiceStatus{
		Name:        "local_generator",
		Available:   localAvailable,
		Version:     localMsg,
		LastChecked: time.Now(),
	})

	// Python 环境
	pyOK, pyIssues := h.pythonBridge.CheckPythonEnvironment()
	pyStatus := "正常"
	if !pyOK {
		pyStatus = "异常: " + strings.Join(pyIssues, ", ")
	}
	services = append(services, models.ServiceStatus{
		Name:        "python_env",
		Available:   pyOK,
		Version:     pyStatus,
		LastChecked: time.Now(),
	})

	// See-through 状态
	seeThroughOK := h.pythonBridge.CheckSeeThroughInstalled()
	services = append(services, models.ServiceStatus{
		Name:        "see_through",
		Available:   seeThroughOK,
		Version:     "SIGGRAPH 2026",
		LastChecked: time.Now(),
	})

	// 缓存服务状态
	if h.cache != nil {
		_ = h.cache.Stats() // 调用Stats保持接口一致性
		services = append(services, models.ServiceStatus{
			Name:        "request_cache",
			Available:   true,
			Version:     "enabled",
			LastChecked: time.Now(),
		})
	}

	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Data: models.SystemStatus{
			Services: services,
			Version:  "v7.1-go",
			Uptime:   time.Since(h.startTime).String(),
		},
	})
}

// GenerateImage 生成图片（支持缓存）
func (h *Handler) GenerateImage(c *gin.Context) {
	var req models.GenerateImageRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, models.Response{
			Success: false,
			Error:   "请求参数错误: " + err.Error(),
		})
		return
	}

	// 尝试从缓存获取
	var result *models.GenerateImageResponse
	var fromCache bool

	if h.cache != nil && req.Seed != 0 {
		result, fromCache = h.cache.Get(req.Prompt, req.Width, req.Height, req.Seed, req.ModelID)
	}

	if !fromCache {
		// 缓存未命中，生成图片
		var err error
		result, err = h.imageGenerator.GenerateImage(req)
		if err != nil {
			c.JSON(http.StatusInternalServerError, models.Response{
				Success: false,
				Error:   "图片生成失败: " + err.Error(),
			})
			return
		}

		// 将结果存入缓存
		if h.cache != nil && req.Seed != 0 {
			h.cache.Set(req.Prompt, req.Width, req.Height, req.Seed, req.ModelID, result)
		}
	}

	response := models.Response{
		Success: true,
		Message: "图片生成成功",
		Data:    result,
	}

	if fromCache {
		response.Message = "图片生成成功（来自缓存）"
		response.Data = map[string]interface{}{
			"result":     result,
			"from_cache": true,
		}
	}

	c.JSON(http.StatusOK, response)
}

// GetModels 获取可用模型列表
func (h *Handler) GetModels(c *gin.Context) {
	availableModels := h.imageGenerator.GetAvailableModels()
	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Message: "获取模型列表成功",
		Data:    availableModels,
	})
}

// CreatePSDPlan 创建 PSD 分层规划
func (h *Handler) CreatePSDPlan(c *gin.Context) {
	var req models.PSDLayerRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, models.Response{
			Success: false,
			Error:   "请求参数错误: " + err.Error(),
		})
		return
	}

	result, err := h.pythonBridge.CreatePSDPlan(req.ImagePath)
	if err != nil {
		c.JSON(http.StatusInternalServerError, models.Response{
			Success: false,
			Error:   "PSD分层失败: " + err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Message: "PSD分层规划创建成功",
		Data:    result,
	})
}

// RunSeeThrough 运行 See-through 工作流
func (h *Handler) RunSeeThrough(c *gin.Context) {
	var req models.SeeThroughRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, models.Response{
			Success: false,
			Error:   "请求参数错误: " + err.Error(),
		})
		return
	}

	result, err := h.pythonBridge.RunSeeThroughWorkflow(req.ImagePath)
	if err != nil {
		c.JSON(http.StatusInternalServerError, models.Response{
			Success: false,
			Error:   "See-through 工作流启动失败: " + err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Message: "See-through 工作流状态",
		Data:    result,
	})
}

// GetPythonScripts 获取 Python 脚本列表
func (h *Handler) GetPythonScripts(c *gin.Context) {
	scripts := h.pythonBridge.GetPythonScripts()
	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Data:    scripts,
	})
}

// ServeOutput 提供输出文件访问
func (h *Handler) ServeOutput(c *gin.Context) {
	filename := c.Param("filename")
	if filename == "" {
		c.JSON(http.StatusBadRequest, models.Response{
			Success: false,
			Error:   "文件名不能为空",
		})
		return
	}

	// 安全检查：防止目录遍历
	filePath := filepath.Join(h.cfg.Output.BaseDir, filename)
	if !isPathSafe(filePath, h.cfg.Output.BaseDir) {
		c.JSON(http.StatusForbidden, models.Response{
			Success: false,
			Error:   "非法的文件路径",
		})
		return
	}

	// 检查文件是否存在
	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		c.JSON(http.StatusNotFound, models.Response{
			Success: false,
			Error:   "文件不存在",
		})
		return
	}

	// 添加缓存控制头
	c.Header("Cache-Control", "public, max-age=3600")
	c.File(filePath)
}

// isPathSafe 检查路径是否在允许的目录内
func isPathSafe(path, baseDir string) bool {
	absPath, err := filepath.Abs(path)
	if err != nil {
		return false
	}
	absBase, err := filepath.Abs(baseDir)
	if err != nil {
		return false
	}

	rel, err := filepath.Rel(absBase, absPath)
	if err != nil {
		return false
	}

	return !strings.HasPrefix(rel, "..") && rel != ".."
}

// GetAPIInfo 获取 API 信息
func (h *Handler) GetAPIInfo(c *gin.Context) {
	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Data: map[string]interface{}{
			"name":        "Live2D Master Agent API",
			"version":     "v7.1-go",
			"description": "Live2D 图片生成与分层 API 服务（高性能优化版）",
			"features": []string{
				"连接池优化",
				"并发处理支持",
				"请求缓存",
				"Gzip压缩",
			},
			"endpoints": []map[string]string{
				{"method": "GET", "path": "/api/health", "desc": "健康检查"},
				{"method": "GET", "path": "/api/status", "desc": "系统状态"},
				{"method": "GET", "path": "/api/info", "desc": "API信息"},
				{"method": "GET", "path": "/api/models", "desc": "获取可用模型列表"},
				{"method": "POST", "path": "/api/generate", "desc": "生成图片（支持缓存）"},
				{"method": "POST", "path": "/api/psd-plan", "desc": "创建PSD分层规划"},
				{"method": "POST", "path": "/api/see-through", "desc": "运行See-through工作流"},
				{"method": "GET", "path": "/api/scripts", "desc": "获取Python脚本列表"},
				{"method": "GET", "path": "/api/cache/stats", "desc": "缓存统计"},
				{"method": "POST", "path": "/api/cache/clear", "desc": "清除缓存"},
				{"method": "GET", "path": "/output/:filename", "desc": "获取输出文件"},
			},
		},
	})
}

// GetCacheStats 获取缓存统计
func (h *Handler) GetCacheStats(c *gin.Context) {
	if h.cache == nil {
		c.JSON(http.StatusOK, models.Response{
			Success: true,
			Data: map[string]interface{}{
				"enabled": false,
				"message": "缓存服务未启用",
			},
		})
		return
	}

	stats := h.cache.Stats()
	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Data:    stats,
	})
}

// ClearCache 清除缓存
func (h *Handler) ClearCache(c *gin.Context) {
	if h.cache == nil {
		c.JSON(http.StatusOK, models.Response{
			Success: true,
			Message: "缓存服务未启用",
		})
		return
	}

	h.cache.Clear()
	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Message: "缓存已清除",
	})
}
