package config

import (
	"encoding/json"
	"os"
	"path/filepath"
)

type Config struct {
	Server   ServerConfig   `json:"server"`
	SDWebUI  SDWebUIConfig  `json:"sd_webui"`
	Python   PythonConfig   `json:"python"`
	Output   OutputConfig   `json:"output"`
	ComfyUI  ComfyUIConfig  `json:"comfyui"`
}

type ServerConfig struct {
	Host string `json:"host"`
	Port int    `json:"port"`
}

type SDWebUIConfig struct {
	BaseURL      string `json:"base_url"`
	Timeout      int    `json:"timeout"`
	Enabled      bool   `json:"enabled"`
}

type PythonConfig struct {
	PythonPath   string `json:"python_path"`
	ScriptsDir   string `json:"scripts_dir"`
}

type OutputConfig struct {
	BaseDir      string `json:"base_dir"`
	MaxFileSize  int64  `json:"max_file_size"`
}

type ComfyUIConfig struct {
	BaseDir      string `json:"base_dir"`
	Enabled      bool   `json:"enabled"`
}

func DefaultConfig() *Config {
	baseDir, _ := filepath.Abs(filepath.Join(".."))
	
	return &Config{
		Server: ServerConfig{
			Host: "0.0.0.0",
			Port: 8080,
		},
		SDWebUI: SDWebUIConfig{
			BaseURL: "http://127.0.0.1:7860",
			Timeout: 300,
			Enabled: true,
		},
		Python: PythonConfig{
			PythonPath: "python3",
			ScriptsDir: baseDir,
		},
		Output: OutputConfig{
			BaseDir:     filepath.Join(baseDir, "output"),
			MaxFileSize: 50 * 1024 * 1024,
		},
		ComfyUI: ComfyUIConfig{
			BaseDir: filepath.Join(baseDir, "comfyui"),
			Enabled: false,
		},
	}
}

func LoadConfig(path string) (*Config, error) {
	cfg := DefaultConfig()
	
	if path == "" {
		return cfg, nil
	}
	
	data, err := os.ReadFile(path)
	if err != nil {
		return cfg, nil
	}
	
	if err := json.Unmarshal(data, cfg); err != nil {
		return cfg, err
	}
	
	return cfg, nil
}
