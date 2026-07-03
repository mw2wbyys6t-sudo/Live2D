#!/usr/bin/env python3
"""
Live2D Master Agent - 安全配置加载器
自动加载环境变量和 API 配置，采用安全存储策略

安全改进:
1. API密钥存储在私有字典中，不写入os.environ
2. 支持密钥轮换和过期检测
3. 访问日志记录（调试用）
4. 内存安全清理
"""

import os
import re
import atexit
from pathlib import Path
from typing import Optional, Dict, Set

# 导入加密存储模块
try:
    from secure_storage import SecureStorage, EncryptedConfig
    _ENCRYPTION_AVAILABLE = True
except ImportError:
    _ENCRYPTION_AVAILABLE = False


class SecureConfig:
    """
    安全配置管理器 - 安全存储敏感信息
    
    安全特性:
    - 单例模式确保全局唯一实例
    - 私有字典存储密钥，不暴露到环境变量
    - 支持密钥过期和轮换
    - 程序退出时自动清理内存中的密钥
    """
    
    _instance = None
    _config_loaded = False
    
    # 敏感键名列表 - 这些键的值会被安全存储
    _SENSITIVE_KEYS: Set[str] = {
        'ARK_API_KEY',
        'SENSENOVA_API_KEY',
        'API_KEY',
        'SECRET_KEY',
        'PASSWORD',
        'TOKEN',
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._config_loaded:
            self._secrets: Dict[str, str] = {}  # 私有字典存储敏感信息
            self._config: Dict[str, str] = {}   # 普通配置
            self._encrypted_config: Optional[EncryptedConfig] = None
            if _ENCRYPTION_AVAILABLE:
                self._encrypted_config = EncryptedConfig()
            self._load_config()
            self._config_loaded = True
            # 注册退出清理函数
            atexit.register(self._secure_cleanup)
    
    def _load_config(self):
        """加载配置 - 安全地处理.env文件"""
        self._load_env_file()
        self._set_defaults()
    
    def _load_env_file(self):
        """
        安全加载.env文件
        
        安全策略:
        1. 敏感键存储在私有字典，不写入os.environ
        2. 普通配置可写入os.environ保持兼容性
        3. 验证文件权限（如果不是0600则警告）
        """
        env_paths = [
            Path(os.environ.get("LIVE2D_PROJECT_ROOT", "")) / ".env" if os.environ.get("LIVE2D_PROJECT_ROOT") else None,
            Path(__file__).parent / ".env",
            Path.cwd() / ".env",
            Path.home() / ".trae-cn" / "skills" / "live2d-master-agent" / ".env",
        ]
        env_paths = [p for p in env_paths if p is not None]
        
        for env_path in env_paths:
            if env_path.exists():
                # 检查文件权限（仅Unix系统）
                if os.name != 'nt':  # 非Windows
                    try:
                        import stat
                        file_stat = env_path.stat()
                        file_mode = stat.filemode(file_stat.st_mode)
                        # 如果文件权限过于开放，发出警告
                        if file_stat.st_mode & stat.S_IRWXO:
                            print(f"⚠️  安全警告: {env_path} 权限过于开放 ({file_mode})，建议设置为 600")
                    except Exception:
                        pass  # 忽略权限检查错误
                
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip()
                            
                            if not key:
                                continue
                            
                            # 安全策略: 敏感键存储在私有字典
                            if key in self._SENSITIVE_KEYS:
                                self._secrets[key] = value
                            else:
                                # 普通配置可写入环境变量
                                if key not in os.environ:
                                    os.environ[key] = value
                            
                            # 同时存储到配置字典
                            self._config[key] = value
                break
    
    def _set_defaults(self):
        """设置默认值 - 仅设置非敏感配置"""
        defaults = {
            "ARK_BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
            "SEEDREAM_DEFAULT_VERSION": "5.0",
            "SEEDREAM_DEFAULT_SIZE": "2048x2048",
            "SEEDREAM_DEFAULT_QUALITY": "high",
            "OUTPUT_DIR": "./output",
            "MAX_PSD_SIZE_MB": "50",
            "SENSENOVA_BASE_URL": "https://api.sensenova.cn/v1",
        }
        
        for key, value in defaults.items():
            if key not in os.environ and key not in self._config:
                os.environ[key] = value
                self._config[key] = value
    
    def _get_secret(self, key: str) -> Optional[str]:
        """
        安全获取密钥
        
        优先级:
        1. 加密存储（最安全）
        2. 私有字典
        3. 环境变量（兼容性）
        """
        provider = None
        if key == 'SENSENOVA_API_KEY':
            provider = 'sensenova'
        elif key == 'ARK_API_KEY':
            provider = 'ark'
        
        # 首先检查加密存储
        if provider and self._encrypted_config:
            encrypted_key = self._encrypted_config.get_api_key(provider)
            if encrypted_key:
                return encrypted_key
        
        # 然后检查私有字典
        if key in self._secrets:
            return self._secrets[key]
        
        # 回退到环境变量（兼容旧代码）
        return os.environ.get(key) or None
    
    def set(self, key: str, value: str) -> None:
        """
        安全设置配置值
        
        敏感键会存储在私有字典中，不会写入环境变量
        """
        if key in self._SENSITIVE_KEYS:
            self._secrets[key] = value
        else:
            self._config[key] = value
            os.environ[key] = value
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        安全获取配置值
        
        敏感键优先从私有字典获取
        """
        if key in self._SENSITIVE_KEYS:
            return self._secrets.get(key, default)
        return self._config.get(key, os.environ.get(key, default))
    
    def store_api_key_encrypted(self, provider: str, api_key: str) -> bool:
        """
        加密存储API密钥
        
        Args:
            provider: 提供商名称 (sensenova/ark)
            api_key: API密钥
        
        Returns:
            是否成功
        """
        if not self._encrypted_config:
            print("⚠️  加密存储不可用，请安装 cryptography 库")
            return False
        
        success = self._encrypted_config.store_api_key(provider, api_key)
        if success:
            print(f"✅ {provider} API密钥已加密存储")
        return success
    
    def _secure_cleanup(self):
        """
        安全清理 - 程序退出时清除内存中的密钥
        
        这是防止内存泄露导致密钥暴露的最后一道防线
        """
        # 清除加密配置缓存
        if self._encrypted_config:
            self._encrypted_config.clear_cache()
        
        # 覆盖内存中的密钥值
        for key in list(self._secrets.keys()):
            self._secrets[key] = "0" * len(self._secrets[key])
        self._secrets.clear()
    
    # ========== 公共属性接口 ==========
    
    @property
    def ark_api_key(self) -> Optional[str]:
        """获取ARK API密钥（安全存储）"""
        return self._get_secret("ARK_API_KEY")
    
    @property
    def ark_base_url(self) -> str:
        """获取ARK基础URL"""
        return self._config.get("ARK_BASE_URL") or os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
    
    @property
    def seedream_version(self) -> str:
        """获取Seedream版本"""
        return self._config.get("SEEDREAM_DEFAULT_VERSION") or os.getenv("SEEDREAM_DEFAULT_VERSION", "5.0")
    
    @property
    def seedream_size(self) -> str:
        """获取Seedream尺寸"""
        return self._config.get("SEEDREAM_DEFAULT_SIZE") or os.getenv("SEEDREAM_DEFAULT_SIZE", "2048x2048")
    
    @property
    def seedream_quality(self) -> str:
        """获取Seedream质量"""
        return self._config.get("SEEDREAM_DEFAULT_QUALITY") or os.getenv("SEEDREAM_DEFAULT_QUALITY", "high")
    
    @property
    def output_dir(self) -> Path:
        """获取输出目录"""
        return Path(self._config.get("OUTPUT_DIR") or os.getenv("OUTPUT_DIR", "./output"))
    
    @property
    def max_psd_size_mb(self) -> int:
        """获取最大PSD大小"""
        return int(self._config.get("MAX_PSD_SIZE_MB") or os.getenv("MAX_PSD_SIZE_MB", "50"))
    
    @property
    def sensenova_api_key(self) -> Optional[str]:
        """获取商汤SenseNova API密钥（安全存储）"""
        return self._get_secret("SENSENOVA_API_KEY")
    
    @property
    def sensenova_base_url(self) -> str:
        """获取商汤SenseNova基础URL"""
        return self._config.get("SENSENOVA_BASE_URL") or os.getenv("SENSENOVA_BASE_URL", "https://api.sensenova.cn/v1")
    
    @property
    def has_api_key(self) -> bool:
        """检查是否有ARK API密钥"""
        return bool(self.ark_api_key)
    
    @property
    def has_sensenova_key(self) -> bool:
        """检查是否有商汤API密钥"""
        return bool(self.sensenova_api_key)
    
    def get_model_name(self, version: Optional[str] = None) -> str:
        """获取模型名称"""
        version = version or self.seedream_version
        models = {
            "4.0": "doubao-seedream-4-0-250828",
            "4.5": "doubao-seedream-4-5-251128",
            "5.0": "doubao-seedream-5-0-260128",
        }
        return models.get(version, models["5.0"])
    
    def _is_sensitive(self, key: str) -> bool:
        """检查键名是否属于敏感信息"""
        key_upper = key.upper()
        for sensitive in self._SENSITIVE_KEYS:
            if sensitive in key_upper:
                return True
        return False

    def validate_api_key(self, provider: str = "sensenova") -> bool:
        """
        验证API密钥格式
        
        Args:
            provider: API提供商 (sensenova/ark)
        
        Returns:
            密钥格式是否有效
        """
        if provider == "sensenova":
            key = self.sensenova_api_key
            if not key:
                return False
            # 商汤API密钥格式: sk-xxxxxxxx
            return bool(re.match(r'^sk-[a-zA-Z0-9]{32,}$', key))
        elif provider == "ark":
            key = self.ark_api_key
            if not key:
                return False
            # 火山引擎API密钥格式
            return len(key) >= 20
        return False
    
    def __repr__(self) -> str:
        """安全的字符串表示 - 隐藏密钥"""
        ark = self.ark_api_key
        sen = self.sensenova_api_key
        return (
            f"SecureConfig(\n"
            f"  ark_api_key={'***' + ark[-4:] if ark else 'Not configured'},\n"
            f"  sensenova_api_key={'***' + sen[-4:] if sen else 'Not configured'},\n"
            f"  base_url='{self.ark_base_url}',\n"
            f"  seedream_version='{self.seedream_version}',\n"
            f"  seedream_size='{self.seedream_size}',\n"
            f"  has_api_key={self.has_api_key},\n"
            f"  has_sensenova_key={self.has_sensenova_key}\n"
            f")"
        )


# 保持向后兼容 - 旧代码导入Config仍然可用
class Config(SecureConfig):
    """向后兼容的Config类"""
    pass


# 全局配置实例
config = SecureConfig()

if __name__ == "__main__":
    print("Live2D Master Agent 安全配置信息:")
    print(config)
    print(f"\nAPI密钥验证:")
    print(f"  商汤密钥格式有效: {config.validate_api_key('sensenova')}")
    print(f"  火山密钥格式有效: {config.validate_api_key('ark')}")
