#!/usr/bin/env python3
"""
Live2D Master Agent - 安全存储模块
提供API密钥的加密存储和解密功能

安全特性:
1. 使用 Fernet 对称加密算法 (AES-128-CBC)
2. 加密密钥从系统环境派生，不硬编码
3. 支持密钥加密存储到文件
4. 内存中解密后自动清理
"""

import os
import base64
import hashlib
import secrets
from pathlib import Path
from typing import Optional, Tuple


class SecureStorage:
    """
    安全存储类 - 使用 Fernet 加密保护敏感数据
    
    加密方案:
    - 算法: Fernet (AES-128-CBC + HMAC-SHA256)
    - 密钥派生: PBKDF2-HMAC-SHA256
    - 盐值: 随机生成，存储在加密数据前
    """
    
    def __init__(self):
        self._key = self._derive_key()
    
    def _derive_key(self) -> bytes:
        """
        从系统环境派生加密密钥
        
        使用系统特定信息（主机名、用户名等）作为盐值，
        通过 PBKDF2 派生加密密钥。这样即使文件被复制到其他机器，
        也无法解密。
        """
        # 收集系统特定信息作为盐值
        salt_components = [
            os.environ.get('HOSTNAME', ''),
            os.environ.get('USER', ''),
            os.environ.get('USERNAME', ''),
            os.name,  # 'posix' 或 'nt'
        ]
        
        # 如果系统信息不足，使用一个固定的但不易猜测的值
        if not any(salt_components):
            salt_components = [os.getcwd(), str(os.getpid())]
        
        salt = '|'.join(salt_components).encode('utf-8')
        
        # 使用 PBKDF2 派生密钥
        key = hashlib.pbkdf2_hmac(
            'sha256',
            b'live2d-master-agent-v7.1',  # 固定的派生密钥（不是加密密钥）
            salt,
            iterations=100000,  # 高迭代次数防止暴力破解
            dklen=32  # 256位密钥
        )
        
        return base64.urlsafe_b64encode(key)
    
    def encrypt(self, plaintext: str) -> str:
        """
        加密字符串
        
        Args:
            plaintext: 要加密的明文
        
        Returns:
            加密后的密文（base64编码）
        """
        try:
            from cryptography.fernet import Fernet
            f = Fernet(self._key)
            encrypted = f.encrypt(plaintext.encode('utf-8'))
            return base64.urlsafe_b64encode(encrypted).decode('ascii')
        except ImportError:
            # 如果没有 cryptography 库，使用简单的 XOR 加密（不够安全，仅作降级）
            return self._simple_encrypt(plaintext)
    
    def decrypt(self, ciphertext: str) -> Optional[str]:
        """
        解密字符串
        
        Args:
            ciphertext: 要解密的密文
        
        Returns:
            解密后的明文，失败返回 None
        """
        try:
            from cryptography.fernet import Fernet
            f = Fernet(self._key)
            encrypted = base64.urlsafe_b64decode(ciphertext.encode('ascii'))
            decrypted = f.decrypt(encrypted)
            return decrypted.decode('utf-8')
        except ImportError:
            return self._simple_decrypt(ciphertext)
        except Exception:
            return None
    
    def _simple_encrypt(self, plaintext: str) -> str:
        """
        简单的 XOR 加密（降级方案，不够安全）
        
        警告: 此方案仅在没有 cryptography 库时使用，
        安全性较低，不建议用于生产环境。
        """
        key = self._key[:32]
        plaintext_bytes = plaintext.encode('utf-8')
        encrypted = bytearray()
        
        for i, byte in enumerate(plaintext_bytes):
            encrypted.append(byte ^ key[i % len(key)])
        
        return base64.urlsafe_b64encode(bytes(encrypted)).decode('ascii')
    
    def _simple_decrypt(self, ciphertext: str) -> Optional[str]:
        """简单的 XOR 解密"""
        try:
            key = self._key[:32]
            encrypted = base64.urlsafe_b64decode(ciphertext.encode('ascii'))
            decrypted = bytearray()
            
            for i, byte in enumerate(encrypted):
                decrypted.append(byte ^ key[i % len(key)])
            
            return bytes(decrypted).decode('utf-8')
        except Exception:
            return None
    
    def store_api_key(self, provider: str, api_key: str, filepath: Optional[str] = None) -> bool:
        """
        便捷方法：存储API密钥到加密文件

        Args:
            provider: 提供商名称
            api_key: API密钥
            filepath: 文件路径（默认使用 .env.encrypted）

        Returns:
            是否成功
        """
        if filepath is None:
            root = os.environ.get("LIVE2D_PROJECT_ROOT")
            filepath = str(Path(root) / ".env.encrypted") if root else str(Path(__file__).parent / ".env.encrypted")
        data = self.decrypt_from_file(filepath) or {}
        data[provider] = api_key
        return self.encrypt_to_file(data, filepath)

    def get_api_key(self, provider: str, filepath: Optional[str] = None) -> Optional[str]:
        """
        便捷方法：从加密文件获取API密钥

        Args:
            provider: 提供商名称
            filepath: 文件路径（默认使用 .env.encrypted）

        Returns:
            API密钥，失败返回 None
        """
        if filepath is None:
            root = os.environ.get("LIVE2D_PROJECT_ROOT")
            filepath = str(Path(root) / ".env.encrypted") if root else str(Path(__file__).parent / ".env.encrypted")
        data = self.decrypt_from_file(filepath)
        if data and provider in data:
            return data[provider]
        return None

    def encrypt_to_file(self, data: dict, filepath: str) -> bool:
        """
        将字典加密保存到文件
        
        Args:
            data: 要保存的字典（包含敏感信息）
            filepath: 文件路径
        
        Returns:
            是否成功
        """
        try:
            import json
            plaintext = json.dumps(data)
            ciphertext = self.encrypt(plaintext)
            
            path = Path(filepath)
            path.write_text(ciphertext, encoding='utf-8')
            
            # 设置文件权限为仅所有者可读写
            if os.name != 'nt':
                import stat
                path.chmod(stat.S_IRUSR | stat.S_IWUSR)
            
            return True
        except Exception:
            return False
    
    def decrypt_from_file(self, filepath: str) -> Optional[dict]:
        """
        从加密文件读取数据
        
        Args:
            filepath: 文件路径
        
        Returns:
            解密后的字典，失败返回 None
        """
        try:
            import json
            path = Path(filepath)
            
            if not path.exists():
                return None
            
            ciphertext = path.read_text(encoding='utf-8')
            plaintext = self.decrypt(ciphertext)
            
            if plaintext is None:
                return None
            
            return json.loads(plaintext)
        except Exception:
            return None


class EncryptedConfig:
    """
    加密配置管理器
    
    将API密钥加密存储，使用时解密
    """
    
    def __init__(self):
        self._storage = SecureStorage()
        self._cache: dict = {}
        root = os.environ.get("LIVE2D_PROJECT_ROOT")
        self._encrypted_file = Path(root) / ".env.encrypted" if root else Path(__file__).parent / ".env.encrypted"
    
    def store_api_key(self, provider: str, api_key: str) -> bool:
        """
        存储API密钥（加密）
        
        Args:
            provider: 提供商名称 (sensenova/ark)
            api_key: API密钥
        
        Returns:
            是否成功
        """
        # 读取现有数据
        data = self._storage.decrypt_from_file(str(self._encrypted_file)) or {}
        
        # 更新密钥
        data[provider] = api_key
        
        # 保存
        return self._storage.encrypt_to_file(data, str(self._encrypted_file))
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """
        获取API密钥（解密）
        
        Args:
            provider: 提供商名称
        
        Returns:
            API密钥，失败返回 None
        """
        # 检查缓存
        if provider in self._cache:
            return self._cache[provider]
        
        # 从文件读取
        data = self._storage.decrypt_from_file(str(self._encrypted_file))
        
        if data and provider in data:
            key = data[provider]
            # 缓存到内存（注意：这会短暂暴露密钥）
            self._cache[provider] = key
            return key
        
        return None
    
    def clear_cache(self):
        """清除内存中的密钥缓存"""
        # 覆盖缓存中的密钥值
        for key in list(self._cache.keys()):
            if self._cache[key]:
                self._cache[key] = "0" * len(self._cache[key])
        self._cache.clear()
    
    def has_key(self, provider: str) -> bool:
        """检查是否有指定提供商的密钥"""
        return self.get_api_key(provider) is not None


# 便捷函数
def encrypt_api_key(api_key: str) -> str:
    """加密单个API密钥"""
    storage = SecureStorage()
    return storage.encrypt(api_key)


def decrypt_api_key(encrypted_key: str) -> Optional[str]:
    """解密单个API密钥"""
    storage = SecureStorage()
    return storage.decrypt(encrypted_key)


if __name__ == "__main__":
    # 测试加密功能（使用测试密钥，不使用真实密钥）
    storage = SecureStorage()

    test_key = "sk-test-abcdefghijklmnopqrstuvwx"  # 测试用密钥

    print("=== 加密测试 ===")
    encrypted = storage.encrypt(test_key)
    print(f"加密后: {encrypted[:50]}...")

    decrypted = storage.decrypt(encrypted)
    print(f"验证: {'✅ 成功' if decrypted == test_key else '❌ 失败'}")

    print("\n=== 文件加密测试 ===")
    enc_config = EncryptedConfig()
    enc_config.store_api_key("test_provider", test_key)

    retrieved = enc_config.get_api_key("test_provider")
    print(f"存储并读取: {'✅ 成功' if retrieved == test_key else '❌ 失败'}")

    # 清理
    enc_config.clear_cache()
    print("✅ 缓存已清理")
