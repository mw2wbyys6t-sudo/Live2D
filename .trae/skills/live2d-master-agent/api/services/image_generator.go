package services

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"math/rand"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"

	"live2d-api/config"
	"live2d-api/models"
)

type ImageGenerator struct {
	cfg        *config.Config
	httpClient *http.Client
}

func NewImageGenerator(cfg *config.Config) *ImageGenerator {
	return &ImageGenerator{
		cfg: cfg,
		httpClient: &http.Client{
			Timeout: time.Duration(cfg.SDWebUI.Timeout) * time.Second,
		},
	}
}

// GenerateImage 生成图片，智能选择来源
func (g *ImageGenerator) GenerateImage(req models.GenerateImageRequest) (*models.GenerateImageResponse, error) {
	// 设置默认值
	if req.Width <= 0 {
		req.Width = 768
	}
	if req.Height <= 0 {
		req.Height = 768
	}
	if req.Seed == 0 {
		req.Seed = rand.Intn(999999999)
	}

	// 尝试 SD WebUI（如果启用且用户未明确禁用）
	if g.cfg.SDWebUI.Enabled && (req.UseSDWebUI == nil || *req.UseSDWebUI) {
		result, err := g.generateWithSDWebUI(req)
		if err == nil {
			return result, nil
		}
		// SD WebUI 失败，降级到 Pollinations
		fmt.Printf("SD WebUI 失败，降级到 Pollinations: %v\n", err)
	}

	// 使用 Pollinations.ai
	return g.generateWithPollinations(req)
}

// generateWithSDWebUI 使用 Stable Diffusion WebUI 生成图片
func (g *ImageGenerator) generateWithSDWebUI(req models.GenerateImageRequest) (*models.GenerateImageResponse, error) {
	baseURL := g.cfg.SDWebUI.BaseURL
	if req.SDWebUIURL != "" {
		baseURL = req.SDWebUIURL
	}

	// 检查服务可用性
	healthURL := strings.TrimRight(baseURL, "/") + "/sdapi/v1/health"
	resp, err := g.httpClient.Get(healthURL)
	if err != nil || resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("SD WebUI 服务不可用")
	}

	// 构建请求
	payload := map[string]interface{}{
		"prompt":           optimizePromptForLive2D(req.Prompt),
		"negative_prompt":  getNegativePromptForLive2D(),
		"width":            req.Width,
		"height":           req.Height,
		"steps":            30,
		"sampler_name":     "DPM++ 2M Karras",
		"cfg_scale":        7.5,
		"seed":             req.Seed,
		"batch_size":       1,
		"n_iter":           1,
		"send_images":      true,
		"save_images":      false,
	}

	payloadBytes, err := json.Marshal(payload)
	if err != nil {
		return nil, err
	}

	// 发送请求
	txt2imgURL := strings.TrimRight(baseURL, "/") + "/sdapi/v1/txt2img"
	resp, err = g.httpClient.Post(txt2imgURL, "application/json", bytes.NewBuffer(payloadBytes))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("SD WebUI API 错误: %s", string(body))
	}

	// 解析响应
	var result struct {
		Images     []string `json:"images"`
		Parameters map[string]interface{} `json:"parameters"`
		Info       string   `json:"info"`
	}

	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, err
	}

	if len(result.Images) == 0 {
		return nil, fmt.Errorf("SD WebUI 未返回图片")
	}

	// 保存图片
	outputPath, err := g.saveBase64Image(result.Images[0], req.Seed)
	if err != nil {
		return nil, err
	}

	return &models.GenerateImageResponse{
		ImagePath: outputPath,
		ImageURL:  "/output/" + filepath.Base(outputPath),
		Seed:      req.Seed,
		Width:     req.Width,
		Height:    req.Height,
		Source:    "sd_webui",
		CreatedAt: time.Now(),
	}, nil
}

// generateWithPollinations 使用 Pollinations.ai 生成图片
func (g *ImageGenerator) generateWithPollinations(req models.GenerateImageRequest) (*models.GenerateImageResponse, error) {
	encodedPrompt := strings.ReplaceAll(req.Prompt, " ", "%20")
	
	// 构建 URL
	url := fmt.Sprintf(
		"https://image.pollinations.ai/prompt/%s?width=%d&height=%d&seed=%d&nologo=true&model=flux",
		encodedPrompt, req.Width, req.Height, req.Seed,
	)

	// 下载图片
	httpClient := &http.Client{Timeout: 200 * time.Second}
	resp, err := httpClient.Get(url)
	if err != nil {
		return nil, fmt.Errorf("Pollinations 请求失败: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("Pollinations 返回状态码: %d", resp.StatusCode)
	}

	// 保存图片
	outputPath := filepath.Join(g.cfg.Output.BaseDir, fmt.Sprintf("live2d_poll_%d_%d.png", time.Now().Unix(), req.Seed))
	
	os.MkdirAll(g.cfg.Output.BaseDir, 0755)
	
	file, err := os.Create(outputPath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	_, err = io.Copy(file, resp.Body)
	if err != nil {
		return nil, err
	}

	return &models.GenerateImageResponse{
		ImagePath: outputPath,
		ImageURL:  "/output/" + filepath.Base(outputPath),
		Seed:      req.Seed,
		Width:     req.Width,
		Height:    req.Height,
		Source:    "pollinations",
		CreatedAt: time.Now(),
	}, nil
}

// saveBase64Image 保存 Base64 编码的图片
func (g *ImageGenerator) saveBase64Image(base64Data string, seed int) (string, error) {
	data, err := base64.StdEncoding.DecodeString(base64Data)
	if err != nil {
		return "", err
	}

	os.MkdirAll(g.cfg.Output.BaseDir, 0755)
	
	outputPath := filepath.Join(g.cfg.Output.BaseDir, fmt.Sprintf("live2d_sd_%d_%d.png", time.Now().Unix(), seed))
	
	if err := os.WriteFile(outputPath, data, 0644); err != nil {
		return "", err
	}

	return outputPath, nil
}

// optimizePromptForLive2D 优化提示词
func optimizePromptForLive2D(prompt string) string {
	prefix := "masterpiece, best quality, high quality, extremely detailed, " +
		"anime style, anime girl, solo, 1girl, clean lineart, clear edges, " +
		"simple background, white background, isolated character, " +
		"perfect for Live2D rigging, distinct color separation, "

	if strings.Contains(strings.ToLower(prompt), "anime") ||
		strings.Contains(strings.ToLower(prompt), "masterpiece") {
		return prompt + ", clean lineart, clear edges, perfect for Live2D rigging, distinct color separation"
	}

	return prefix + prompt
}

// getNegativePromptForLive2D 获取反向提示词
func getNegativePromptForLive2D() string {
	return "blurry, low quality, low resolution, pixelated, noisy, grainy, " +
		"distorted, deformed, bad anatomy, bad hands, bad face, bad eyes, " +
		"extra fingers, missing fingers, fused fingers, too many fingers, " +
		"bad proportions, extra limbs, long neck, bad feet, bad ears, " +
		"ugly, disgusting, horror, watermark, text, signature, logo, " +
		"simple background, messy hair, messy clothes, complex background, " +
		"photorealistic, realistic, 3d, ugly eyes, deformed eyes, closed eyes, " +
		"depth of field, blurry background, multiple girls, multiple people"
}

// CheckSDWebUIStatus 检查 SD WebUI 状态
func (g *ImageGenerator) CheckSDWebUIStatus() (bool, string) {
	baseURL := g.cfg.SDWebUI.BaseURL
	healthURL := strings.TrimRight(baseURL, "/") + "/sdapi/v1/health"
	
	resp, err := g.httpClient.Get(healthURL)
	if err != nil {
		return false, err.Error()
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		return true, "服务正常运行"
	}
	return false, fmt.Sprintf("HTTP %d", resp.StatusCode)
}

// CheckPollinationsStatus 检查 Pollinations 状态
func (g *ImageGenerator) CheckPollinationsStatus() (bool, string) {
	url := "https://image.pollinations.ai/prompt/test?width=64&height=64&seed=1&nologo=true"
	
	resp, err := g.httpClient.Get(url)
	if err != nil {
		return false, err.Error()
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		return true, "服务正常运行"
	}
	return false, fmt.Sprintf("HTTP %d", resp.StatusCode)
}
