package handlers

import (
	"net/http"
	"os"
	"path/filepath"
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
	startTime      time.Time
}

func NewHandler(cfg *config.Config) *Handler {
	return &Handler{
		cfg:            cfg,
		imageGenerator: services.NewImageGenerator(cfg),
		pythonBridge:   services.NewPythonBridge(cfg),
		startTime:      time.Now(),
	}
}

// HealthCheck 健康检查
func (h *Handler) HealthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Message: "Live2D API 服务正常运行",
		Data: map[string]interface{}{
			"version": "v6.3-go",
			"uptime":  time.Since(h.startTime).String(),
		},
	})
}

// GetSystemStatus 获取系统状态
func (h *Handler) GetSystemStatus(c *gin.Context) {
	// 检查各个服务状态
	var services []models.ServiceStatus

	// SD WebUI 状态
	sdAvailable, sdMsg := h.imageGenerator.CheckSDWebUIStatus()
	services = append(services, models.ServiceStatus{
		Name:        "sd_webui",
		Available:   sdAvailable,
		Version:     sdMsg,
		LastChecked: time.Now(),
	})

	// Pollinations 状态
	pollAvailable, pollMsg := h.imageGenerator.CheckPollinationsStatus()
	services = append(services, models.ServiceStatus{
		Name:        "pollinations",
		Available:   pollAvailable,
		Version:     pollMsg,
		LastChecked: time.Now(),
	})

	// Python 环境
	pyOK, _ := h.pythonBridge.CheckPythonEnvironment()
	pyStatus := "正常"
	if !pyOK {
		pyStatus = "异常"
	}
	services = append(services, models.ServiceStatus{
		Name:        "python_env",
		Available:   pyOK,
		Version:     pyStatus,
		LastChecked: time.Now(),
	})

	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Data: models.SystemStatus{
			Services: services,
			Version:  "v6.3-go",
			Uptime:   time.Since(h.startTime).String(),
		},
	})
}

// GenerateImage 生成图片
func (h *Handler) GenerateImage(c *gin.Context) {
	var req models.GenerateImageRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, models.Response{
			Success: false,
			Error:   "请求参数错误: " + err.Error(),
		})
		return
	}

	result, err := h.imageGenerator.GenerateImage(req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, models.Response{
			Success: false,
			Error:   "图片生成失败: " + err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Message: "图片生成成功",
		Data:    result,
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
	filepath := filepath.Join(h.cfg.Output.BaseDir, filename)
	if !isPathSafe(filepath, h.cfg.Output.BaseDir) {
		c.JSON(http.StatusForbidden, models.Response{
			Success: false,
			Error:   "非法的文件路径",
		})
		return
	}

	// 检查文件是否存在
	if _, err := os.Stat(filepath); os.IsNotExist(err) {
		c.JSON(http.StatusNotFound, models.Response{
			Success: false,
			Error:   "文件不存在",
		})
		return
	}

	c.File(filepath)
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
	return len(absPath) >= len(absBase) && absPath[:len(absBase)] == absBase
}

// GetAPIInfo 获取 API 信息
func (h *Handler) GetAPIInfo(c *gin.Context) {
	c.JSON(http.StatusOK, models.Response{
		Success: true,
		Data: map[string]interface{}{
			"name":        "Live2D Master Agent API",
			"version":     "v6.3-go",
			"description": "Live2D 图片生成与分层 API 服务",
			"endpoints": []map[string]string{
				{"method": "GET", "path": "/api/health", "desc": "健康检查"},
				{"method": "GET", "path": "/api/status", "desc": "系统状态"},
				{"method": "POST", "path": "/api/generate", "desc": "生成图片"},
				{"method": "POST", "path": "/api/psd-plan", "desc": "创建PSD分层规划"},
				{"method": "POST", "path": "/api/see-through", "desc": "运行See-through工作流"},
				{"method": "GET", "path": "/api/scripts", "desc": "获取Python脚本列表"},
				{"method": "GET", "path": "/output/:filename", "desc": "获取输出文件"},
			},
		},
	})
}
