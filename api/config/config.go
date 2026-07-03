package config

import (
	"encoding/json"
	"os"
	"path/filepath"
	"time"
)

type Config struct {
	Server   ServerConfig   `json:"server"`
	SDWebUI  SDWebUIConfig  `json:"sd_webui"`
	Python   PythonConfig   `json:"python"`
	Output   OutputConfig   `json:"output"`
	ComfyUI  ComfyUIConfig  `json:"comfyui"`
	Cache    CacheConfig    `json:"cache"`
}

type ServerConfig struct {
	Host                string        `json:"host"`
	Port                int           `json:"port"`
	MaxRequestBodySize  int64         `json:"max_request_body_size"`
	MaxHeaderBytes      int           `json:"max_header_bytes"`
	ReadTimeout         time.Duration `json:"read_timeout"`
	WriteTimeout        time.Duration `json:"write_timeout"`
	ReadHeaderTimeout   time.Duration `json:"read_header_timeout"`
	IdleTimeout         time.Duration `json:"idle_timeout"`
	AllowedOrigins      []string      `json:"allowed_origins"`
}

type SDWebUIConfig struct {
	BaseURL      string `json:"base_url"`
	Timeout      int    `json:"timeout"`
	Enabled      bool   `json:"enabled"`
}

type PythonConfig struct {
	PythonPath   string `json:"python_path"`
	ScriptsDir   string `json:"scripts_dir"`
	TimeoutSec   int    `json:"timeout_sec"` // P1-4: configurable Python script timeout
}

type OutputConfig struct {
	BaseDir      string `json:"base_dir"`
	MaxFileSize  int64  `json:"max_file_size"`
}

type ComfyUIConfig struct {
	BaseDir      string `json:"base_dir"`
	Enabled      bool   `json:"enabled"`
}

type CacheConfig struct {
	Enabled     int `json:"enabled"`
	MaxEntries  int `json:"max_entries"`
	MaxSizeMB   int `json:"max_size_mb"`
	TTLSeconds  int `json:"ttl_seconds"`
}

func DefaultConfig() *Config {
	// Resolve project root relative to this file (api/config/config.go -> api/.. = project root)
	baseDir, _ := filepath.Abs(filepath.Join("..", ".."))
	scriptsDir := baseDir

	return &Config{
		Server: ServerConfig{
			Host:                "0.0.0.0",
			Port:                8080,
			MaxRequestBodySize:  10 * 1024 * 1024, // 10MB
			MaxHeaderBytes:      1 * 1024 * 1024,  // 1MB
			ReadTimeout:         30 * time.Second,
			WriteTimeout:        180 * time.Second, // P1-4: increased to 3min for image gen
			ReadHeaderTimeout:   5 * time.Second,
			IdleTimeout:         120 * time.Second,
			AllowedOrigins:      []string{"*"}, // P0-CORS: default permissive, configurable
		},
		SDWebUI: SDWebUIConfig{
			BaseURL: "http://127.0.0.1:7860",
			Timeout: 300,
			Enabled: true,
		},
		Python: PythonConfig{
			PythonPath: "python3",
			ScriptsDir: scriptsDir,
			TimeoutSec: 120, // P1-4: default 2min, configurable
		},
		Output: OutputConfig{
			BaseDir:     filepath.Join(baseDir, "output"),
			MaxFileSize: 50 * 1024 * 1024,
		},
		ComfyUI: ComfyUIConfig{
			BaseDir: filepath.Join(baseDir, "comfyui"),
			Enabled: false,
		},
		Cache: CacheConfig{
			Enabled:    1,
			MaxEntries: 100,
			MaxSizeMB:  100,
			TTLSeconds: 3600,
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
		return cfg, nil // File not found is OK, use defaults
	}

	if err := json.Unmarshal(data, cfg); err != nil {
		return cfg, err
	}

	return cfg, nil
}

// GetPythonTimeout returns the Python timeout as time.Duration (P1-4)
func (c *Config) GetPythonTimeout() time.Duration {
	secs := c.Python.TimeoutSec
	if secs <= 0 {
		secs = 120 // default 2 minutes
	}
	return time.Duration(secs) * time.Second
}
