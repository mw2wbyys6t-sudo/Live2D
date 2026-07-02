#!/usr/bin/env python3
"""
Live2D Master Agent - 兼容性安装脚本

自动检测 Python 版本和操作系统，安装可用的依赖，跳过当前环境不支持的包。

用法:
    python install.py
    python install.py --full    # 尝试安装所有依赖（包括可选）
"""
import os
import sys
import subprocess
import platform
from pathlib import Path


CORE_DEPS = [
    "Pillow>=10.0.0",
    "numpy>=1.24.0",
    "requests>=2.31.0",
    "urllib3>=2.0.0",
    "httpx>=0.24.0",
    "psd-tools>=1.9.0",
    "scipy>=1.10.0",
    "scikit-learn>=1.3.0",
]

OPTIONAL_DEPS = [
    "opencv-python>=4.8.0",
    "onnxruntime>=1.14.0",
    "rembg[cpu]>=2.0.0",
]


def _get_project_root() -> Path:
    return Path(__file__).resolve().parent


def get_python_version() -> tuple[int, int]:
    return sys.version_info.major, sys.version_info.minor


def run_pip(args: list[str]) -> int:
    """使用当前解释器的 pip 安装，避免 Windows pip launcher 问题。"""
    cmd = [sys.executable, "-m", "pip"] + args
    print(f"> {' '.join(cmd)}")
    return subprocess.run(cmd).returncode


def install_package(package: str) -> bool:
    """安装单个包，失败时返回 False 但不中断流程。"""
    print(f"\n[INSTALL] {package}")
    code = run_pip(["install", "--upgrade", package])
    if code != 0:
        print(f"[WARN] 安装失败（跳过）: {package}")
        return False
    print(f"[OK] {package}")
    return True


def install_pygame(py_major: int, py_minor: int) -> bool:
    """根据 Python 版本选择合适的 pygame 包。"""
    if py_major == 3 and py_minor >= 14:
        pkg = "pygame-ce>=2.5.0"
    else:
        pkg = "pygame>=2.5.0"
    print(f"\n[INSTALL] 桌面桌宠渲染库: {pkg}")
    code = run_pip(["install", "--upgrade", pkg])
    if code != 0:
        print("[WARN] 桌面桌宠依赖安装失败，桌宠功能可能不可用")
        return False
    print(f"[OK] {pkg}")
    return True


def write_env_example() -> None:
    """如果 .env 不存在，复制示例文件。"""
    root = _get_project_root()
    env_file = root / ".env"
    example_file = root / ".env.example"
    skill_example = root / ".trae" / "skills" / "live2d-master-agent" / ".env.example"

    if env_file.exists():
        return

    source = example_file if example_file.exists() else skill_example
    if source.exists():
        env_file.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"[OK] 已创建 {env_file}")


def main() -> int:
    py_major, py_minor = get_python_version()
    print("=" * 60)
    print(" Live2D Master Agent - 兼容性安装脚本")
    print("=" * 60)
    print(f"Python 版本: {platform.python_version()}")
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"项目根目录: {_get_project_root()}")
    print("=" * 60)

    if py_major < 3 or (py_major == 3 and py_minor < 8):
        print("[ERROR] 需要 Python 3.8 或更高版本")
        return 1

    if py_major == 3 and py_minor >= 14:
        print("\n[INFO] 检测到 Python 3.14+，部分可选依赖可能没有预编译包。")
        print("       本脚本会先安装核心依赖，再尝试安装可选依赖。\n")

    # 升级 pip 自身，减少 launcher 错误
    print("\n[STEP 1/4] 升级 pip...")
    run_pip(["install", "--upgrade", "pip"])

    # 安装核心依赖
    print("\n[STEP 2/4] 安装核心依赖...")
    failed_core = []
    for dep in CORE_DEPS:
        if not install_package(dep):
            failed_core.append(dep)

    if failed_core:
        print("\n[ERROR] 以下核心依赖安装失败，项目可能无法正常运行:")
        for dep in failed_core:
            print(f"  - {dep}")
        print("\n建议:")
        print("  1. 使用 Python 3.11 或 3.12（兼容性最好）")
        print("  2. 安装 Microsoft C++ Build Tools（Windows）")
        return 1

    # 安装桌面桌宠依赖
    print("\n[STEP 3/4] 安装桌面桌宠依赖...")
    install_pygame(py_major, py_minor)

    # 安装可选依赖
    print("\n[STEP 4/4] 安装可选依赖（失败会自动跳过）...")
    install_full = "--full" in sys.argv
    for dep in OPTIONAL_DEPS:
        if not install_package(dep):
            if install_full:
                print(f"[WARN] {dep} 安装失败，但 --full 模式继续")
            else:
                print(f"[INFO] 跳过 {dep}，不影响核心功能")

    write_env_example()

    print("\n" + "=" * 60)
    print(" 安装完成")
    print("=" * 60)
    print("\n现在可以运行:")
    print("  python live2d_agent.py        # 交互式终端 Agent")
    print("  python master_tool.py \"描述\"   # 命令行模式")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
