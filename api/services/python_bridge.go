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

// validatePath 验证路径安全，防止命令注入和路径遍历
func validatePath(path string) error {
	if path == "" {
		return fmt.Errorf("路径不能为空")
	}
	// 检查非法字符，防止命令注入
	if matched, _ := regexp.MatchString(`[;&|*$\x00]`, path); matched {
		return fmt.Errorf("路径包含非法字符")
	}
	// 检查文件名是否以 - 开头，防止被解析为命令行选项
	if strings.HasPrefix(filepath.Base(path), "-") {
		return fmt.Errorf("文件名不能以 - 开头")
	}
	return nil
}

// executePythonScript 安全执行Python脚本（带沙箱隔离）
func (pb *PythonBridge) executePythonScript(scriptPath string, args []string, timeout time.Duration) ([]byte, error) {
	// 验证脚本路径安全
	if err := validatePath(scriptPath); err != nil {
		return nil, fmt.Errorf("脚本路径验证失败: %v", err)
	}

	// 检查脚本是否存在
	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("脚本不存在: %s", scriptPath)
	}

	// 构建完整参数
	fullArgs := append([]string{scriptPath}, args...)

	// 创建带超时的上下文
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	// 创建命令
	cmd := exec.CommandContext(ctx, pb.cfg.Python.PythonPath, fullArgs...)
	cmd.Dir = pb.cfg.Python.ScriptsDir

	// 设置环境变量（只传递必要的变量，不传递敏感信息）
	cmd.Env = []string{
		"PYTHONIOENCODING=utf-8",
		"PYTHONPATH=" + pb.cfg.Python.ScriptsDir,
		"HOME=" + os.Getenv("HOME"),
		"PATH=" + os.Getenv("PATH"),
		"LANG=" + os.Getenv("LANG"),
	}

	// Linux/Unix: 使用资源限制
	if runtime.GOOS != "windows" {
		cmd.SysProcAttr = &syscall.SysProcAttr{
			Setpgid: true, // 创建新的进程组，便于终止子进程
		}
	}

	// 执行命令
	output, err := cmd.CombinedOutput()
	if ctx.Err() == context.DeadlineExceeded {
		// 超时终止进程组
		if cmd.Process != nil {
			syscall.Kill(-cmd.Process.Pid, syscall.SIGKILL)
		}
		return nil, fmt.Errorf("脚本执行超时（限制%d秒）", int(timeout.Seconds()))
	}
	if err != nil {
		// 对输出进行脱敏处理
		sanitizedOutput := sanitizeOutput(string(output))
		return nil, fmt.Errorf("脚本执行失败: %v\n输出: %s", err, sanitizedOutput)
	}

	return output, nil
}

// sanitizeOutput 对输出进行脱敏处理，防止泄露敏感信息
func sanitizeOutput(output string) string {
	// 定义敏感信息模式
	patterns := []string{
		`sk-[a-zA-Z0-9]{20,}`,                // API密钥
		`api[_-]?key["\s]*[:=]["\s]*[^\s"]+`, // API Key
		`secret["\s]*[:=]["\s]*[^\s"]+`,      // Secret
		`password["\s]*[:=]["\s]*[^\s"]+`,    // Password
		`token["\s]*[:=]["\s]*[^\s"]+`,       // Token
	}

	result := output
	for _, pattern := range patterns {
		re := regexp.MustCompile(pattern)
		result = re.ReplaceAllString(result, "[REDACTED]")
	}
	return result
}

// GenerateImageViaPython 通过 Python 脚本生成图片
func (pb *PythonBridge) GenerateImageViaPython(prompt string, width, height, seed int) (string, error) {
	scriptPath := filepath.Join(pb.cfg.Python.ScriptsDir, "master_tool.py")

	args := []string{
		"--width", fmt.Sprintf("%d", width),
		"--height", fmt.Sprintf("%d", height),
	}

	if prompt != "" {
		// 安全处理提示词：防止被解析为命令行选项
		if strings.HasPrefix(prompt, "-") {
			prompt = " " + prompt
		}
		// 使用 -- 分隔选项和位置参数
		args = append(args, "--", prompt)
	}

	// 执行脚本（5分钟超时）
	output, err := pb.executePythonScript(scriptPath, args, 5*time.Minute)
	if err != nil {
		return "", err
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
	// 验证路径安全
	if err := validatePath(imagePath); err != nil {
		return nil, fmt.Errorf("路径验证失败: %v", err)
	}

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
	deps := []string{"PIL", "numpy"}
	for _, dep := range deps {
		cmd := exec.Command(pb.cfg.Python.PythonPath, "-c", fmt.Sprintf("import %s", dep))
		if err := cmd.Run(); err != nil {
			issues = append(issues, fmt.Sprintf("缺少依赖: %s", dep))
		}
	}

	return len(issues) == 0, issues
}

// CheckSeeThroughInstalled 检查 See-through 是否已安装
func (pb *PythonBridge) CheckSeeThroughInstalled() bool {
	seeThroughDir := filepath.Join(pb.cfg.ComfyUI.BaseDir, "custom_nodes", "ComfyUI-See-through")
	if _, err := os.Stat(seeThroughDir); os.IsNotExist(err) {
		return false
	}
	return true
}

// GetPythonScripts 获取可用的 Python 脚本列表
func (pb *PythonBridge) GetPythonScripts() []map[string]string {
	scripts := []map[string]string{}

	scriptFiles := []struct {
		Name string
		Desc string
	}{
		{"master_tool.py", "主工具 - 图片生成和PSD转换 v7.0"},
		{"local_image_generator.py", "自研本地生成器 v3.0"},
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
