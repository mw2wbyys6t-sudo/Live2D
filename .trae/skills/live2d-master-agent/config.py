#!/usr/bin/env python3
"""
Live2D Master Agent 配置加载器
自动加载环境变量和 API 配置
"""

import os
from pathlib import Path
from typing import Optional

class Config:
    _instance = None
    _config_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._config_loaded:
            self._load_config()
            self._config_loaded = True
    
    def _load_config(self):
        self._load_env_file()
        self._set_defaults()
    
    def _load_env_file(self):
        env_paths = [
            Path(__file__).parent / ".env",
            Path.cwd() / ".env",
            Path.home() / ".trae-cn" / "skills" / "live2d-master-agent" / ".env",
        ]
        
        for env_path in env_paths:
            if env_path.exists():
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip()
                            if key and value and key not in os.environ:
                                os.environ[key] = value
                break
    
    def _set_defaults(self):
        defaults = {
            "ARK_API_KEY": "",
            "ARK_BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
            "SEEDREAM_DEFAULT_VERSION": "5.0",
            "SEEDREAM_DEFAULT_SIZE": "2048x2048",
            "SEEDREAM_DEFAULT_QUALITY": "high",
            "OUTPUT_DIR": "./output",
            "MAX_PSD_SIZE_MB": "50",
        }
        
        for key, value in defaults.items():
            if key not in os.environ:
                os.environ[key] = value
    
    @property
    def ark_api_key(self) -> Optional[str]:
        return os.getenv("ARK_API_KEY") or None
    
    @property
    def ark_base_url(self) -> str:
        return os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
    
    @property
    def seedream_version(self) -> str:
        return os.getenv("SEEDREAM_DEFAULT_VERSION", "5.0")
    
    @property
    def seedream_size(self) -> str:
        return os.getenv("SEEDREAM_DEFAULT_SIZE", "2048x2048")
    
    @property
    def seedream_quality(self) -> str:
        return os.getenv("SEEDREAM_DEFAULT_QUALITY", "high")
    
    @property
    def output_dir(self) -> Path:
        return Path(os.getenv("OUTPUT_DIR", "./output"))
    
    @property
    def max_psd_size_mb(self) -> int:
        return int(os.getenv("MAX_PSD_SIZE_MB", "50"))
    
    @property
    def has_api_key(self) -> bool:
        return bool(self.ark_api_key)
    
    def get_model_name(self, version: Optional[str] = None) -> str:
        version = version or self.seedream_version
        models = {
            "4.0": "doubao-seedream-4-0-250828",
            "4.5": "doubao-seedream-4-5-251128",
            "5.0": "doubao-seedream-5-0-260128",
        }
        return models.get(version, models["5.0"])
    
    def __repr__(self) -> str:
        return (
            f"Config(\n"
            f"  api_key={'***' + self.ark_api_key[-8:] if self.ark_api_key else 'Not configured'},\n"
            f"  base_url='{self.ark_base_url}',\n"
            f"  seedream_version='{self.seedream_version}',\n"
            f"  seedream_size='{self.seedream_size}',\n"
            f"  has_api_key={self.has_api_key}\n"
            f")"
        )

config = Config()

if __name__ == "__main__":
    print("Live2D Master Agent 配置信息:")
    print(config)
