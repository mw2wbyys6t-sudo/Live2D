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

// GenerateImage 生成图片，使用自研本地生成器
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

	// 使用自研本地生成器
	return g.generateWithLocalGenerator(req)
}

// generateWithLocalGenerator 使用自研本地生成器生成图片
func (g *ImageGenerator) generateWithLocalGenerator(req models.GenerateImageRequest) (*models.GenerateImageResponse, error) {
	scriptPath := filepath.Join(g.cfg.Python.ScriptsDir, "local_image_generator.py")

	// 检查脚本是否存在
	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("本地生成器脚本不存在: %s", scriptPath)
	}

	// 构建命令参数
	args := []string{
		scriptPath,
		"--width", fmt.Sprintf("%d", req.Width),
		"--height", fmt.Sprintf("%d", req.Height),
		"--steps", "25",
		"--seed", fmt.Sprintf("%d", req.Seed),
		"--quality", "standard",
	}

	// 如果指定了模型
	if req.ModelID != "" {
		args = append(args, "--model", req.ModelID)
	}

	// 启用Live2D优化模式（默认）
	if !req.NoLive2DOpt {
		// 默认启用Live2D优化
	}

	// 添加提示词
	if req.Prompt != "" {
		args = append(args, req.Prompt)
	}

	// 执行生成命令
	cmd := exec.Command(g.cfg.Python.PythonPath, args...)
	cmd.Dir = g.cfg.Python.ScriptsDir
	cmd.Env = append(os.Environ(),
		"PYTHONIOENCODING=utf-8",
	)

	output, err := cmd.CombinedOutput()
	if err != nil {
		return nil, fmt.Errorf("本地生成器执行失败: %v\n输出: %s", err, string(output))
	}

	// 解析输出找到生成的图片路径
	outputStr := string(output)
	outputPath := g.parseOutputPath(outputStr)

	if outputPath == "" {
		return nil, fmt.Errorf("无法从输出中解析图片路径")
	}

	// 确保路径是绝对路径
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
		// 查找 "文件:" 或 "图片已保存:" 行
		if strings.Contains(line, "文件:") || strings.Contains(line, "图片已保存:") {
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

	// 检查Python环境
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
