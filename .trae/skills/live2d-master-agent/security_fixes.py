#!/usr/bin/env python3
"""
Live2D Master Agent - 安全修复模块
修复安全审计中发现的漏洞
"""

import os
import sys
from pathlib import Path
from typing import Optional, Tuple


def validate_path(path: str, base_dir: Optional[str] = None) -> Tuple[bool, str]:
    """
    安全路径验证 - 防止路径遍历攻击
    
    Args:
        path: 要验证的路径
        base_dir: 允许的基础目录，默认为当前脚本目录
    
    Returns:
        (是否有效, 错误消息)
    """
    if not path:
        return False, "路径不能为空"
    
    # 检查非法字符
    dangerous_chars = [';', '&', '|', '*', '$', '\0']
    for char in dangerous_chars:
        if char in path:
            return False, f"路径包含非法字符: {char}"
    
    # 检查路径前缀攻击
    if path.startswith('-'):
        return False, "路径不能以 '-' 开头"
    
    # 解析路径
    try:
        resolved_path = Path(path).resolve()
    except Exception as e:
        return False, f"路径解析失败: {e}"
    
    # 检查是否在允许的目录内
    if base_dir:
        base_path = Path(base_dir).resolve()
        try:
            resolved_path.relative_to(base_path)
        except ValueError:
            return False, f"路径不在允许的目录内: {resolved_path}"
    
    # 检查路径长度
    if len(str(resolved_path)) > 4096:
        return False, "路径过长"
    
    return True, str(resolved_path)


def validate_image_path(image_path: str) -> Tuple[bool, str]:
    """
    验证图片路径（增强版）
    """
    # 基础验证
    is_valid, msg = validate_path(image_path)
    if not is_valid:
        return False, msg
    
    # 额外验证：必须是文件且存在
    if not os.path.isfile(image_path):
        return False, f"路径不存在或不是文件: {image_path}"
    
    # 验证文件扩展名
    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.gif')
    if not image_path.lower().endswith(valid_extensions):
        return False, f"不支持的文件格式，支持: {valid_extensions}"
    
    # 验证文件大小（最大50MB）
    max_size = 50 * 1024 * 1024
    try:
        file_size = os.path.getsize(image_path)
        if file_size > max_size:
            return False, f"文件过大（最大50MB），当前: {file_size/1024/1024:.1f}MB"
    except Exception as e:
        return False, f"无法获取文件大小: {e}"
    
    return True, image_path


def validate_model_id(model_id: str) -> Tuple[bool, str]:
    """
    验证模型ID（白名单验证）
    
    防止下载和执行不受信任的模型文件
    """
    # 允许的模型白名单
    allowed_models = {
        # SD 1.5 模型
        "Linaqruf/anything-v3.0",
        "stablediffusionapi/anything-v5",
        "gsdf/Counterfeit-V3.0",
        "Meina/MeinaMix",
        "andite/pastel-mix",
        "WarriorMama777/OrangeMixs",
        # SDXL 模型
        "Vsukiyaki/ShiitakeMix",
        "NovaAnimeXL",
    }
    
    if not model_id:
        return False, "模型ID不能为空"
    
    # 检查是否在白名单中
    if model_id not in allowed_models:
        return False, f"模型不在白名单中: {model_id}\n允许的模型: {list(allowed_models)}"
    
    return True, model_id


def sanitize_prompt(prompt: str, max_length: int = 4000) -> str:
    """
    清理提示词，防止命令注入
    
    Args:
        prompt: 原始提示词
        max_length: 最大长度
    
    Returns:
        清理后的提示词
    """
    if not prompt:
        return ""
    
    # 限制长度
    if len(prompt) > max_length:
        prompt = prompt[:max_length]
    
    # 移除危险字符
    dangerous_patterns = [
        (';', ''),
        ('&', ''),
        ('|', ''),
        ('`', ''),
        ('$(', ''),
        ('${', ''),
        ('\\', ''),
        ('\n', ' '),
        ('\r', ' '),
    ]
    
    for old, new in dangerous_patterns:
        prompt = prompt.replace(old, new)
    
    # 如果以 '-' 开头，添加空格前缀
    if prompt.startswith('-'):
        prompt = ' ' + prompt
    
    return prompt.strip()


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，防止路径遍历
    
    Args:
        filename: 原始文件名
    
    Returns:
        安全的文件名
    """
    if not filename:
        return "unnamed"
    
    # 移除路径分隔符
    filename = filename.replace('/', '_').replace('\\', '_')
    
    # 移除危险字符
    dangerous_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '\0']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    # 限制长度
    if len(filename) > 255:
        filename = filename[:255]
    
    # 移除前导点（防止隐藏文件）
    while filename.startswith('.'):
        filename = filename[1:]
    
    # 确保不为空
    if not filename:
        filename = "unnamed"
    
    return filename


def validate_directory(directory: str, create_if_not_exists: bool = False) -> Tuple[bool, str]:
    """
    验证目录路径
    
    Args:
        directory: 目录路径
        create_if_not_exists: 如果不存在是否创建
    
    Returns:
        (是否有效, 目录路径)
    """
    # 基础验证
    is_valid, msg = validate_path(directory)
    if not is_valid:
        return False, msg
    
    # 检查是否为目录
    if not os.path.isdir(directory):
        if create_if_not_exists:
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                return False, f"无法创建目录: {e}"
        else:
            return False, f"目录不存在: {directory}"
    
    return True, directory


def secure_subprocess_args(args: list) -> list:
    """
    安全处理子进程参数
    
    Args:
        args: 原始参数列表
    
    Returns:
        安全的参数列表
    """
    secure_args = []
    for arg in args:
        if isinstance(arg, str):
            # 清理参数
            arg = sanitize_prompt(arg)
            # 如果参数以 '-' 开头且不是已知选项，添加前缀
            if arg.startswith('-') and not arg.startswith('--'):
                # 检查是否是单个字符选项（如 -v, -h）
                if len(arg) == 2 and arg[1].isalpha():
                    secure_args.append(arg)
                else:
                    # 可能是恶意参数，添加引号保护
                    secure_args.append(f"'{arg}'")
            else:
                secure_args.append(arg)
        else:
            secure_args.append(arg)
    
    return secure_args


# ==================== 使用示例 ====================
if __name__ == "__main__":
    print("🔒 安全验证模块测试")
    print("=" * 60)
    
    # 测试路径验证
    test_path = "../etc/passwd"
    is_valid, msg = validate_path(test_path, base_dir=os.getcwd())
    print(f"\n路径验证测试: {test_path}")
    print(f"  结果: {'✅ 有效' if is_valid else '❌ 无效'}")
    print(f"  消息: {msg}")
    
    # 测试模型验证
    test_model = "Linaqruf/anything-v3.0"
    is_valid, msg = validate_model_id(test_model)
    print(f"\n模型验证测试: {test_model}")
    print(f"  结果: {'✅ 有效' if is_valid else '❌ 无效'}")
    print(f"  消息: {msg}")
    
    # 测试提示词清理
    test_prompt = "evil; rm -rf / --dangerous-option"
    cleaned = sanitize_prompt(test_prompt)
    print(f"\n提示词清理测试:")
    print(f"  原始: {test_prompt}")
    print(f"  清理后: {cleaned}")
    
    print("\n" + "=" * 60)
    print("✅ 安全验证模块加载完成")

