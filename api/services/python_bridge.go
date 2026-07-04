package services

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"
	"syscall"
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

// validatePath validates path safety, preventing command injection and path traversal
func validatePath(path string) error {
	if path == "" {
		return fmt.Errorf("路径不能为空")
	}
	// Block dangerous characters (command injection)
	if matched, _ := regexp.MatchString(`[;&|*$\x00]`, path); matched {
		return fmt.Errorf("路径包含非法字符")
	}
	// Block paths starting with - (argument injection)
	if strings.HasPrefix(filepath.Base(path), "-") {
		return fmt.Errorf("文件名不能以 - 开头")
	}
	return nil
}

// executePythonScript safely executes a Python script with configurable timeout (P1-4)
func (pb *PythonBridge) executePythonScript(scriptPath string, args []string, timeout time.Duration) ([]byte, error) {
	if err := validatePath(scriptPath); err != nil {
		return nil, fmt.Errorf("脚本路径验证失败: %v", err)
	}
	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("脚本不存在: %s", scriptPath)
	}

	fullArgs := append([]string{scriptPath}, args...)

	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	cmd := exec.CommandContext(ctx, pb.cfg.Python.PythonPath, fullArgs...)
	cmd.Dir = pb.cfg.Python.ScriptsDir

	cmd.Env = []string{
		"PYTHONIOENCODING=utf-8",
		"PYTHONPATH=" + pb.cfg.Python.ScriptsDir,
		"HOME=" + os.Getenv("HOME"),
		"PATH=" + os.Getenv("PATH"),
		"LANG=" + os.Getenv("LANG"),
		"LIVE2D_PROJECT_ROOT=" + pb.cfg.Python.ScriptsDir,
	}

	if runtime.GOOS != "windows" {
		cmd.SysProcAttr = &syscall.SysProcAttr{
			Setpgid: true,
		}
	}

	output, err := cmd.CombinedOutput()
	if ctx.Err() == context.DeadlineExceeded {
		if cmd.Process != nil {
			syscall.Kill(-cmd.Process.Pid, syscall.SIGKILL)
		}
		return nil, fmt.Errorf("脚本执行超时（限制%d秒）", int(timeout.Seconds()))
	}
	if err != nil {
		sanitizedOutput := sanitizeOutput(string(output))
		return nil, fmt.Errorf("脚本执行失败: %v\n输出: %s", err, sanitizedOutput)
	}

	return output, nil
}

// sanitizeOutput redacts sensitive information from output
func sanitizeOutput(output string) string {
	patterns := []string{
		`sk-[a-zA-Z0-9]{20,}`,
		`api[_-]?key["\s]*[:=]["\s]*[^\s"]+`,
		`secret["\s]*[:=]["\s]*[^\s"]+`,
		`password["\s]*[:=]["\s]*[^\s"]+`,
		`token["\s]*[:=]["\s]*[^\s"]+`,
	}
	result := output
	for _, pattern := range patterns {
		re := regexp.MustCompile(pattern)
		result = re.ReplaceAllString(result, "[REDACTED]")
	}
	return result
}

// GenerateImageViaPython generates image via Python script with configurable timeout (P1-4)
func (pb *PythonBridge) GenerateImageViaPython(prompt string, width, height, seed int) (string, error) {
	scriptPath := filepath.Join(pb.cfg.Python.ScriptsDir, "master_tool.py")

	args := []string{
		"--width", fmt.Sprintf("%d", width),
		"--height", fmt.Sprintf("%d", height),
		"--no-layer",
	}
	if seed > 0 {
		args = append(args, "--seed", fmt.Sprintf("%d", seed))
	}
	if prompt != "" {
		if strings.HasPrefix(prompt, "-") {
			prompt = " " + prompt
		}
		args = append(args, "--", prompt)
	}

	// P1-4: Use configurable timeout
	timeout := pb.cfg.GetPythonTimeout()
	output, err := pb.executePythonScript(scriptPath, args, timeout)
	if err != nil {
		return "", err
	}

	outputStr := string(output)
	lines := strings.Split(outputStr, "\n")
	for _, line := range lines {
		if strings.Contains(line, ".png") {
			parts := strings.Fields(line)
			for _, part := range parts {
				cleaned := strings.Trim(part, "[]:(),'\"`")
				if strings.HasSuffix(cleaned, ".png") {
					// Try both relative to script dir and absolute
					if filepath.IsAbs(cleaned) {
						if _, err := os.Stat(cleaned); err == nil {
							return cleaned, nil
						}
					}
					absPath := filepath.Join(pb.cfg.Python.ScriptsDir, cleaned)
					if _, err := os.Stat(absPath); err == nil {
						return absPath, nil
					}
				}
			}
		}
	}
	return "", fmt.Errorf("无法从输出中解析图片路径")
}

// CreatePSDPlan creates PSD layer plan using v6 layerer by default (P0-3 fix)
func (pb *PythonBridge) CreatePSDPlan(imagePath string) (*models.PSDLayerResponse, error) {
	if err := validatePath(imagePath); err != nil {
		return nil, fmt.Errorf("路径验证失败: %v", err)
	}

	// P0-3 FIX: Default to v6 K-means layerer, not pro
	scriptPath := filepath.Join(pb.cfg.Python.ScriptsDir, "live2d_layer_v6.py")
	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		scriptPath = filepath.Join(pb.cfg.Python.ScriptsDir, "live2d_layer_pro.py")
	}

	// P1-4 FIX: Use configurable timeout
	timeout := pb.cfg.GetPythonTimeout()
	output, err := pb.executePythonScript(scriptPath, []string{imagePath}, timeout)
	if err != nil {
		return nil, fmt.Errorf("PSD分层脚本执行失败: %v\n输出: %s", err, sanitizeOutput(string(output)))
	}

	outputDir := filepath.Join(pb.cfg.Output.BaseDir, fmt.Sprintf("psd_plan_%d", time.Now().Unix()))
	os.MkdirAll(outputDir, 0755)

	// Standard 52 layers for response
	layers := []string{
		"Background - 背景", "Hair_Back - 头发_后", "Neck - 脖子",
		"Chest - 胸腔", "Waist_Hips - 腰臀",
		"Thigh_L - 大腿_左", "Thigh_R - 大腿_右",
		"Face_Base - 脸_基础", "Face_Blush - 脸_腮红",
		"EyeWhite_L - 眼白_左", "EyeWhite_R - 眼白_右",
		"Iris_L - 虹膜_左", "Iris_R - 虹膜_右",
		"Pupil_L - 瞳孔_左", "Pupil_R - 瞳孔_右",
		"Mouth_Cavity - 口腔", "Mouth_LowerLip - 下唇", "Mouth_UpperLip - 上唇",
		"Lash_Upper_L - 睫毛_上_左", "Lash_Upper_R - 睫毛_上_右",
		"Eyebrow_L - 眉毛_左", "Eyebrow_R - 眉毛_右",
		"Bangs - 刘海", "SideHair_L - 侧发_左", "SideHair_R - 侧发_右",
		"Clothes_Outer - 衣服_外层",
	}

	return &models.PSDLayerResponse{
		PlanDir:    outputDir,
		LayerCount: len(layers),
		Layers:     layers,
		CreatedAt:  time.Now(),
	}, nil
}

// RunSeeThroughWorkflow runs See-through workflow
func (pb *PythonBridge) RunSeeThroughWorkflow(imagePath string) (*models.SeeThroughResponse, error) {
	comfyuiDir := pb.cfg.ComfyUI.BaseDir
	if _, err := os.Stat(comfyuiDir); os.IsNotExist(err) {
		return &models.SeeThroughResponse{
			Status:  "error",
			Message: "ComfyUI 未安装，请先运行 python install_comfyui_advanced.py",
		}, nil
	}
	seeThroughDir := filepath.Join(comfyuiDir, "custom_nodes", "ComfyUI-See-through")
	if _, err := os.Stat(seeThroughDir); os.IsNotExist(err) {
		return &models.SeeThroughResponse{
			Status:  "error",
			Message: "See-through 未安装，请先运行 python install_comfyui_advanced.py",
		}, nil
	}
	return &models.SeeThroughResponse{
		TaskID:    fmt.Sprintf("st_%d", time.Now().Unix()),
		Status:    "pending",
		Message:   "请启动 ComfyUI 并加载 See-through 工作流",
		CreatedAt: time.Now(),
	}, nil
}

// CheckPythonEnvironment checks Python environment availability
func (pb *PythonBridge) CheckPythonEnvironment() (bool, []string) {
	var issues []string
	cmd := exec.Command(pb.cfg.Python.PythonPath, "--version")
	if _, err := cmd.CombinedOutput(); err != nil {
		issues = append(issues, fmt.Sprintf("Python 不可用: %v", err))
		return false, issues
	}
	deps := []string{"PIL", "numpy"}
	for _, dep := range deps {
		cmd := exec.Command(pb.cfg.Python.PythonPath, "-c", fmt.Sprintf("import %s", dep))
		if err := cmd.Run(); err != nil {
			issues = append(issues, fmt.Sprintf("缺少依赖: %s", dep))
		}
	}
	return len(issues) == 0, issues
}

// CheckSeeThroughInstalled checks if See-through is installed
func (pb *PythonBridge) CheckSeeThroughInstalled() bool {
	seeThroughDir := filepath.Join(pb.cfg.ComfyUI.BaseDir, "custom_nodes", "ComfyUI-See-through")
	_, err := os.Stat(seeThroughDir)
	return err == nil
}

// GetPythonScripts lists available Python scripts
func (pb *PythonBridge) GetPythonScripts() []map[string]string {
	scripts := []map[string]string{}
	scriptFiles := []struct {
		Name string
		Desc string
	}{
		{"master_tool.py", "主工具 - 图片生成+分层 v9.0"},
		{"live2d_workflow.py", "完整工作流引擎 v9.0"},
		{"live2d_layer_v6.py", "K-means 分层工具 v6 (默认)"},
		{"live2d_desktop_pet.py", "桌面桌宠创建工具"},
		{"config_api.py", "API 配置工具"},
		{"install_comfyui_advanced.py", "ComfyUI + See-through 安装器"},
	}
	for _, sf := range scriptFiles {
		path := filepath.Join(pb.cfg.Python.ScriptsDir, sf.Name)
		available := "true"
		if _, err := os.Stat(path); os.IsNotExist(err) {
			available = "false"
		}
		scripts = append(scripts, map[string]string{
			"name":        sf.Name,
			"description": sf.Desc,
			"path":        path,
			"available":   available,
		})
	}
	return scripts
}
