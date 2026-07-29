package services

import (
	"fmt"
	"math/rand"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"live2d-api/config"
	"live2d-api/models"
)

type ImageGenerator struct {
	cfg *config.Config
}

func NewImageGenerator(cfg *config.Config) *ImageGenerator {
	return &ImageGenerator{
		cfg: cfg,
	}
}

// GenerateImage 生成图片，使用自研本地生成器（保持向后兼容）
func (g *ImageGenerator) GenerateImage(req models.GenerateImageRequest) (*models.GenerateImageResponse, error) {
	// 设置默认值
	if req.Width <= 0 {
		req.Width = 512
	}
	if req.Height <= 0 {
		req.Height = 768
	}
	if req.Seed == 0 {
		req.Seed = rand.Intn(999999999)
	}

	return g.generateWithLocalGenerator(req)
}

// GenerateWithCharacter 使用角色一致性和语义分割生成（v10.0）
func (g *ImageGenerator) GenerateWithCharacter(req models.GenerateRequest) (*models.GenerateImageResponse, error) {
	// 设置默认值
	if req.Width <= 0 {
		req.Width = 1024
	}
	if req.Height <= 0 {
		req.Height = 1024
	}
	if req.Seed == 0 {
		req.Seed = rand.Intn(999999999)
	}
	if !req.UseSemantic {
		req.UseSemantic = true // 默认使用语义分割
	}

	// 优先使用 workflow.py 新工作流
	resp, err := g.generateWithWorkflow(req)
	if err == nil {
		return resp, nil
	}

	// 回退到本地生成器
	fmt.Fprintf(os.Stderr, "[WARN] 工作流生成失败，回退到本地生成器: %v\n", err)
	legacyReq := models.GenerateImageRequest{
		Prompt:  req.Prompt,
		Width:   req.Width,
		Height:  req.Height,
		Seed:    req.Seed,
		ModelID: req.ModelID,
	}
	return g.generateWithLocalGenerator(legacyReq)
}

// generateWithWorkflow 使用 core/workflow.py 新工作流
func (g *ImageGenerator) generateWithWorkflow(req models.GenerateRequest) (*models.GenerateImageResponse, error) {
	scriptPath := filepath.Join(g.cfg.Python.ScriptsDir, "core", "workflow.py")
	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("工作流脚本不存在: %s", scriptPath)
	}

	// 构建参数
	args := []string{
		scriptPath,
		"--width", fmt.Sprintf("%d", req.Width),
		"--height", fmt.Sprintf("%d", req.Height),
		"--seed", fmt.Sprintf("%d", req.Seed),
	}

	if req.CharacterID != "" {
		args = append(args, "--character-id", req.CharacterID)
	}
	if req.UseSemantic {
		args = append(args, "--semantic")
	} else {
		args = append(args, "--no-semantic")
	}
	if req.ExportLive2D {
		args = append(args, "--live2d-export")
	}
	if req.DeployDesktop {
		args = append(args, "--deploy-desktop")
	}

	// 添加提示词
	prompt := req.Prompt
	if prompt != "" {
		const maxPromptLen = 4000
		if len(prompt) > maxPromptLen {
			prompt = prompt[:maxPromptLen]
		}
		if strings.HasPrefix(prompt, "-") {
			prompt = " " + prompt
		}
		args = append(args, "--", prompt)
	}

	cmd := exec.Command(g.cfg.Python.PythonPath, args...)
	cmd.Dir = g.cfg.Python.ScriptsDir
	cmd.Env = append(os.Environ(),
		"PYTHONIOENCODING=utf-8",
		"PYTHONPATH="+g.cfg.Python.ScriptsDir,
	)

	// 工作流超时更长
	timeout := g.cfg.GetPythonTimeout() * 3
	done := make(chan struct{})
	var output []byte
	var err error

	go func() {
		output, err = cmd.CombinedOutput()
		close(done)
	}()

	select {
	case <-done:
	case <-time.After(timeout):
		if cmd.Process != nil {
			cmd.Process.Kill()
		}
		return nil, fmt.Errorf("工作流执行超时（限制%d秒）", int(timeout.Seconds()))
	}

	if err != nil {
		fmt.Fprintf(os.Stderr, "[ERROR] 工作流执行失败: %v\n输出: %s\n", err, string(output))
		return nil, fmt.Errorf("工作流执行失败")
	}

	// 解析输出
	outputPath := g.parseOutputPath(string(output))
	if outputPath == "" {
		return nil, fmt.Errorf("无法从输出中解析图片路径")
	}
	if !filepath.IsAbs(outputPath) {
		outputPath = filepath.Join(g.cfg.Python.ScriptsDir, outputPath)
	}

	return &models.GenerateImageResponse{
		ImagePath: outputPath,
		ImageURL:  "/output/" + filepath.Base(outputPath),
		Seed:      req.Seed,
		Width:     req.Width,
		Height:    req.Height,
		Source:    "workflow_v10",
		CreatedAt: time.Now(),
	}, nil
}

// generateWithLocalGenerator 使用自研本地生成器生成图片
func (g *ImageGenerator) generateWithLocalGenerator(req models.GenerateImageRequest) (*models.GenerateImageResponse, error) {
	scriptPath := filepath.Join(g.cfg.Python.ScriptsDir, "local_image_generator.py")

	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("本地生成器脚本不存在: %s", scriptPath)
	}

	args := []string{
		scriptPath,
		"--width", fmt.Sprintf("%d", req.Width),
		"--height", fmt.Sprintf("%d", req.Height),
		"--steps", "25",
		"--seed", fmt.Sprintf("%d", req.Seed),
		"--quality", "standard",
	}

	if req.ModelID != "" {
		args = append(args, "--model", req.ModelID)
	}

	if !req.NoLive2DOpt {
		// 默认启用Live2D优化
	}

	if req.Prompt != "" {
		const maxPromptLen = 4000
		prompt := req.Prompt
		if len(prompt) > maxPromptLen {
			prompt = prompt[:maxPromptLen]
		}
		if strings.HasPrefix(prompt, "-") {
			prompt = " " + prompt
		}
		args = append(args, "--", prompt)
	}

	cmd := exec.Command(g.cfg.Python.PythonPath, args...)
	cmd.Dir = g.cfg.Python.ScriptsDir
	cmd.Env = append(os.Environ(),
		"PYTHONIOENCODING=utf-8",
	)

	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Fprintf(os.Stderr, "[ERROR] 本地生成器执行失败: %v\n输出: %s\n", err, string(output))
		return nil, fmt.Errorf("本地生成器执行失败，请检查服务端日志")
	}

	outputStr := string(output)
	outputPath := g.parseOutputPath(outputStr)

	if outputPath == "" {
		return nil, fmt.Errorf("无法从输出中解析图片路径")
	}

	if !filepath.IsAbs(outputPath) {
		outputPath = filepath.Join(g.cfg.Python.ScriptsDir, outputPath)
	}

	return &models.GenerateImageResponse{
		ImagePath: outputPath,
		ImageURL:  "/output/" + filepath.Base(outputPath),
		Seed:      req.Seed,
		Width:     req.Width,
		Height:    req.Height,
		Source:    "local_generator_v3",
		CreatedAt: time.Now(),
	}, nil
}

// parseOutputPath 从输出中解析图片路径
func (g *ImageGenerator) parseOutputPath(output string) string {
	lines := strings.Split(output, "\n")

	for _, line := range lines {
		if strings.Contains(line, "文件:") || strings.Contains(line, "图片已保存:") ||
			strings.Contains(line, "character_") || strings.Contains(line, "optimized_") {
			parts := strings.Fields(line)
			for _, part := range parts {
				if strings.HasSuffix(part, ".png") {
					return part
				}
			}
		}
	}

	// 尝试从output目录查找最新文件
	outputDir := filepath.Join(g.cfg.Python.ScriptsDir, "output")
	if files, err := os.ReadDir(outputDir); err == nil {
		var latestFile os.DirEntry
		var latestTime time.Time
		for _, file := range files {
			if strings.HasSuffix(file.Name(), ".png") {
				if info, err := file.Info(); err == nil {
					if info.ModTime().After(latestTime) {
						latestTime = info.ModTime()
						latestFile = file
					}
				}
			}
		}
		if latestFile != nil {
			return filepath.Join(outputDir, latestFile.Name())
		}
	}

	return ""
}

// CheckLocalGeneratorStatus 检查本地生成器状态
func (g *ImageGenerator) CheckLocalGeneratorStatus() (bool, string) {
	scriptPath := filepath.Join(g.cfg.Python.ScriptsDir, "local_image_generator.py")
	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		return false, "本地生成器脚本不存在"
	}

	// 检查新工作流
	workflowPath := filepath.Join(g.cfg.Python.ScriptsDir, "core", "workflow.py")
	if _, err := os.Stat(workflowPath); err == nil {
		return true, "v10.0 工作流就绪"
	}

	cmd := exec.Command(g.cfg.Python.PythonPath, "-c", "import diffusers; import torch; import PIL")
	output, err := cmd.CombinedOutput()
	if err != nil {
		return false, fmt.Sprintf("缺少依赖: %s", string(output))
	}

	return true, "本地生成器就绪"
}

// GetAvailableModels 获取可用模型列表
func (g *ImageGenerator) GetAvailableModels() []map[string]interface{} {
	return []map[string]interface{}{
		{
			"id":       "Linaqruf/anything-v3.0",
			"name":     "Anything V3",
			"desc":     "通用动漫风格",
			"size":     "约 4GB",
			"type":     "sd15",
			"quality":  "standard",
		},
		{
			"id":       "stablediffusionapi/anything-v5",
			"name":     "Anything V5",
			"desc":     "高质量动漫",
			"size":     "约 4GB",
			"type":     "sd15",
			"quality":  "high",
		},
		{
			"id":       "gsdf/Counterfeit-V3.0",
			"name":     "Counterfeit V3",
			"desc":     "细腻画风",
			"size":     "约 4GB",
			"type":     "sd15",
			"quality":  "ultra",
		},
		{
			"id":       "Meina/MeinaMix",
			"name":     "MeinaMix",
			"desc":     "萌系风格",
			"size":     "约 4GB",
			"type":     "sd15",
			"quality":  "high",
		},
		{
			"id":       "andite/pastel-mix",
			"name":     "Pastel Mix",
			"desc":     "柔和色彩",
			"size":     "约 4GB",
			"type":     "sd15",
			"quality":  "high",
		},
		{
			"id":       "WarriorMama777/OrangeMixs",
			"name":     "AbyssOrangeMix",
			"desc":     "丰富色彩",
			"size":     "约 4GB",
			"type":     "sd15",
			"quality":  "high",
		},
		{
			"id":       "Vsukiyaki/ShiitakeMix",
			"name":     "Shiitake-Mix",
			"desc":     "SDXL高质量动漫",
			"size":     "约 7GB",
			"type":     "sdxl",
			"quality":  "ultra",
		},
	}
}
