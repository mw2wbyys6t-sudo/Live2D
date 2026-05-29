package services

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"live2d-api/config"
	"live2d-api/models"
)

type PythonBridge struct {
	cfg *config.Config
}

func NewPythonBridge(cfg *config.Config) *PythonBridge {
	return &PythonBridge{cfg: cfg}
}

// GenerateImageViaPython 通过 Python 脚本生成图片
func (pb *PythonBridge) GenerateImageViaPython(prompt string, width, height, seed int) (string, error) {
	scriptPath := filepath.Join(pb.cfg.Python.ScriptsDir, "master_tool.py")
	
	args := []string{
		scriptPath,
		"--width", fmt.Sprintf("%d", width),
		"--height", fmt.Sprintf("%d", height),
	}
	
	if prompt != "" {
		args = append(args, prompt)
	}

	cmd := exec.Command(pb.cfg.Python.PythonPath, args...)
	cmd.Dir = pb.cfg.Python.ScriptsDir
	
	output, err := cmd.CombinedOutput()
	if err != nil {
		return "", fmt.Errorf("Python脚本执行失败: %v\n输出: %s", err, string(output))
	}

	// 解析输出找到生成的图片路径
	outputStr := string(output)
	lines := strings.Split(outputStr, "\n")
	
	for _, line := range lines {
		if strings.Contains(line, "文件:") || strings.Contains(line, "output/") {
			// 尝试提取路径
			parts := strings.Fields(line)
			for _, part := range parts {
				if strings.HasSuffix(part, ".png") {
					return filepath.Join(pb.cfg.Python.ScriptsDir, part), nil
				}
			}
		}
	}

	return "", fmt.Errorf("无法从输出中解析图片路径")
}

// CreatePSDPlan 通过 Python 创建 PSD 分层规划
func (pb *PythonBridge) CreatePSDPlan(imagePath string) (*models.PSDLayerResponse, error) {
	scriptPath := filepath.Join(pb.cfg.Python.ScriptsDir, "live2d_layer_pro.py")
	
	// 如果 live2d_layer_pro.py 不存在，尝试 v6
	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		scriptPath = filepath.Join(pb.cfg.Python.ScriptsDir, "live2d_layer_v6.py")
	}

	cmd := exec.Command(pb.cfg.Python.PythonPath, scriptPath, imagePath)
	cmd.Dir = pb.cfg.Python.ScriptsDir
	
	output, err := cmd.CombinedOutput()
	if err != nil {
		return nil, fmt.Errorf("PSD分层脚本执行失败: %v\n输出: %s", err, string(output))
	}

	// 构建响应
	layers := []string{
		"Background - 背景",
		"ArtMesh/Body - 身体",
		"ArtMesh/Neck - 脖子",
		"ArtMesh/Clothes - 服装",
		"ArtMesh/Head - 头部",
		"ArtMesh/Face_Base - 脸部基础",
		"ArtMesh/Hair_Back - 头发后部",
		"ArtMesh/Hair_Side_L - 头发左侧",
		"ArtMesh/Hair_Side_R - 头发右侧",
		"ArtMesh/Hair_Front - 头发前部",
		"ArtMesh/Hair_Bangs - 刘海",
		"ArtMesh/Brow_L - 左眉毛",
		"ArtMesh/Brow_R - 右眉毛",
		"ArtMesh/EyeL_White - 左眼白",
		"ArtMesh/EyeL_Iris - 左虹膜",
		"ArtMesh/EyeL_Highlight - 左眼高光",
		"ArtMesh/EyeR_White - 右眼白",
		"ArtMesh/EyeR_Iris - 右虹膜",
		"ArtMesh/EyeR_Highlight - 右眼高光",
		"ArtMesh/Mouth_Outer - 嘴巴外形",
		"ArtMesh/Accessories - 配饰",
	}

	outputDir := filepath.Join(pb.cfg.Output.BaseDir, fmt.Sprintf("psd_plan_%d", time.Now().Unix()))
	
	return &models.PSDLayerResponse{
		PlanDir:    outputDir,
		LayerCount: len(layers),
		Layers:     layers,
		CreatedAt:  time.Now(),
	}, nil
}

// RunSeeThroughWorkflow 运行 See-through 工作流
func (pb *PythonBridge) RunSeeThroughWorkflow(imagePath string) (*models.SeeThroughResponse, error) {
	// 检查 ComfyUI 是否安装
	comfyuiDir := pb.cfg.ComfyUI.BaseDir
	if _, err := os.Stat(comfyuiDir); os.IsNotExist(err) {
		return &models.SeeThroughResponse{
			Status:  "error",
			Message: "ComfyUI 未安装，请先运行 install_comfyui_advanced.py",
		}, nil
	}

	// 检查 See-through 是否安装
	seeThroughDir := filepath.Join(comfyuiDir, "custom_nodes", "ComfyUI-See-through")
	if _, err := os.Stat(seeThroughDir); os.IsNotExist(err) {
		return &models.SeeThroughResponse{
			Status:  "error",
			Message: "See-through 未安装，请先运行 install_comfyui_advanced.py",
		}, nil
	}

	return &models.SeeThroughResponse{
		TaskID:    fmt.Sprintf("st_%d", time.Now().Unix()),
		Status:    "pending",
		Message:   "请手动启动 ComfyUI 并加载 See-through 工作流",
		CreatedAt: time.Now(),
	}, nil
}

// CheckPythonEnvironment 检查 Python 环境
func (pb *PythonBridge) CheckPythonEnvironment() (bool, []string) {
	var issues []string

	// 检查 Python 可执行文件
	cmd := exec.Command(pb.cfg.Python.PythonPath, "--version")
	_, err := cmd.CombinedOutput()
	if err != nil {
		issues = append(issues, fmt.Sprintf("Python 不可用: %v", err))
		return false, issues
	}

	// 检查关键依赖
	deps := []string{"PIL", "numpy", "requests"}
	for _, dep := range deps {
		cmd := exec.Command(pb.cfg.Python.PythonPath, "-c", fmt.Sprintf("import %s", dep))
		if err := cmd.Run(); err != nil {
			issues = append(issues, fmt.Sprintf("缺少依赖: %s", dep))
		}
	}

	return len(issues) == 0, issues
}

// GetPythonScripts 获取可用的 Python 脚本列表
func (pb *PythonBridge) GetPythonScripts() []map[string]string {
	scripts := []map[string]string{}
	
	scriptFiles := []struct {
		Name string
		Desc string
	}{
		{"master_tool.py", "主工具 - 图片生成和PSD转换"},
		{"sd_webui_integration.py", "SD WebUI 集成模块"},
		{"live2d_layer_pro.py", "AI 分层工具 (Pro)"},
		{"live2d_layer_v6.py", "AI 分层工具 (v6)"},
		{"install_comfyui_advanced.py", "ComfyUI + See-through 安装器"},
		{"config_api.py", "API 配置工具"},
	}

	for _, sf := range scriptFiles {
		path := filepath.Join(pb.cfg.Python.ScriptsDir, sf.Name)
		if _, err := os.Stat(path); err == nil {
			scripts = append(scripts, map[string]string{
				"name":        sf.Name,
				"description": sf.Desc,
				"path":        path,
				"available":   "true",
			})
		} else {
			scripts = append(scripts, map[string]string{
				"name":        sf.Name,
				"description": sf.Desc,
				"path":        path,
				"available":   "false",
			})
		}
	}

	return scripts
}
