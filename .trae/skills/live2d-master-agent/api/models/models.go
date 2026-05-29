package models

import "time"

// 通用响应结构
type Response struct {
	Success bool        `json:"success"`
	Message string      `json:"message,omitempty"`
	Data    interface{} `json:"data,omitempty"`
	Error   string      `json:"error,omitempty"`
}

// 图片生成请求
type GenerateImageRequest struct {
	Prompt      string `json:"prompt" binding:"required"`
	Width       int    `json:"width"`
	Height      int    `json:"height"`
	Seed        int    `json:"seed"`
	ModelID     string `json:"model_id,omitempty"`
	NoLive2DOpt bool   `json:"no_live2d_opt,omitempty"`
	Quality     string `json:"quality,omitempty"`
	Steps       int    `json:"steps,omitempty"`
}

// 图片生成响应
type GenerateImageResponse struct {
	ImagePath string            `json:"image_path"`
	ImageURL  string            `json:"image_url"`
	Seed      int               `json:"seed"`
	Width     int               `json:"width"`
	Height    int               `json:"height"`
	Source    string            `json:"source"`
	Features  map[string]string `json:"features,omitempty"`
	CreatedAt time.Time         `json:"created_at"`
}

// PSD分层请求
type PSDLayerRequest struct {
	ImagePath     string `json:"image_path" binding:"required"`
	OutputDir     string `json:"output_dir,omitempty"`
	UseAI         bool   `json:"use_ai"`
	UseSeeThrough bool   `json:"use_see_through"`
}

// PSD分层响应
type PSDLayerResponse struct {
	PlanDir    string    `json:"plan_dir"`
	PSDPath    string    `json:"psd_path"`
	LayerCount int       `json:"layer_count"`
	Layers     []string  `json:"layers"`
	CreatedAt  time.Time `json:"created_at"`
}

// 服务状态
type ServiceStatus struct {
	Name        string    `json:"name"`
	Available   bool      `json:"available"`
	Version     string    `json:"version,omitempty"`
	LastChecked time.Time `json:"last_checked"`
}

// 系统状态
type SystemStatus struct {
	Services []ServiceStatus `json:"services"`
	Version  string          `json:"version"`
	Uptime   string          `json:"uptime"`
}

// See-through 工作流请求
type SeeThroughRequest struct {
	ImagePath  string `json:"image_path" binding:"required"`
	ComfyUIDir string `json:"comfyui_dir,omitempty"`
}

// See-through 工作流响应
type SeeThroughResponse struct {
	TaskID    string    `json:"task_id"`
	Status    string    `json:"status"`
	OutputDir string    `json:"output_dir,omitempty"`
	Message   string    `json:"message"`
	CreatedAt time.Time `json:"created_at"`
}

// 任务状态
type TaskStatus struct {
	TaskID    string    `json:"task_id"`
	Status    string    `json:"status"`
	Progress  int       `json:"progress"`
	Result    string    `json:"result,omitempty"`
	Error     string    `json:"error,omitempty"`
	UpdatedAt time.Time `json:"updated_at"`
}
