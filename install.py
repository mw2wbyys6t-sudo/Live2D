#!/usr/bin/env python3
"""
Live2D Master Agent v9.0 - Installation Script

Automatically detects Python version and OS, installs core + optional dependencies.

Usage:
    python install.py
    python install.py --full    # Install all optional dependencies
    python install.py --check   # Check what's installed without installing
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

# P2-4 FIX: cryptography is now a REQUIRED dependency (no XOR fallback)
CORE_DEPS = [
    "Pillow>=10.0.0",
    "numpy>=1.24.0",
    "requests>=2.31.0",
    "urllib3>=2.0.0",
    "httpx>=0.24.0",
    "psd-tools>=1.9.0",
    "scipy>=1.10.0",
    "scikit-learn>=1.3.0",
    "cryptography>=41.0.0",   # P0-4/P2-4: REQUIRED for secure storage (no XOR fallback)
]

OPTIONAL_DEPS = [
    "opencv-python>=4.8.0",
    "onnxruntime>=1.14.0",
    "rembg[cpu]>=2.0.0",
]


def _get_project_root() -> Path:
    return Path(__file__).resolve().parent


def get_python_version() -> tuple:
    return sys.version_info.major, sys.version_info.minor


def run_pip(args: list) -> int:
    cmd = [sys.executable, "-m", "pip"] + args
    print(f"> {' '.join(cmd)}")
    return subprocess.run(cmd).returncode


def install_package(package: str) -> bool:
    print(f"\n[INSTALL] {package}")
    code = run_pip(["install", "--upgrade", package])
    if code != 0:
        print(f"[WARN] Failed to install (skipping): {package}")
        return False
    print(f"[OK] {package}")
    return True


def check_package(package: str) -> bool:
    """Check if a package is importable."""
    import importlib
    pkg_map = {
        "Pillow": "PIL",
        "numpy": "numpy",
        "requests": "requests",
        "urllib3": "urllib3",
        "httpx": "httpx",
        "psd-tools": "psd_tools",
        "scipy": "scipy",
        "scikit-learn": "sklearn",
        "cryptography": "cryptography",
        "opencv-python": "cv2",
        "onnxruntime": "onnxruntime",
        "pygame": "pygame",
        "pygame-ce": "pygame",
    }
    mod_name = pkg_map.get(package.split(">=")[0].split("==")[0], package.split(">=")[0])
    try:
        importlib.import_module(mod_name)
        return True
    except ImportError:
        return False


def install_pygame(py_major: int, py_minor: int) -> bool:
    if py_major == 3 and py_minor >= 14:
        pkg = "pygame-ce>=2.5.0"
    else:
        pkg = "pygame>=2.5.0"
    print(f"\n[INSTALL] Desktop pet renderer: {pkg}")
    code = run_pip(["install", "--upgrade", pkg])
    if code != 0:
        print("[WARN] pygame installation failed - desktop pet feature may not work")
        return False
    print(f"[OK] {pkg}")
    return True


def write_env_example() -> None:
    """Create .env.example and initial .env if they don't exist."""
    root = _get_project_root()
    env_example = root / ".env.example"
    env_file = root / ".env"

    example_content = """# Live2D Master Agent v9.0 Configuration
# Copy this file to .env and fill in your API keys

# === Optional API Keys (free Pollinations.ai works without keys) ===
# SenseNova (商汤日日新) - high quality cloud generation
SENSENOVA_API_KEY=

# Volcano Engine ARK / Seedream - ultra high quality (DEF-003)
ARK_API_KEY=

# === Output Configuration ===
OUTPUT_DIR=output

# === Logging ===
LIVE2D_LOG_LEVEL=INFO
LIVE2D_TELEMETRY=0

# === Go API Configuration ===
GO_API_HOST=0.0.0.0
GO_API_PORT=8080
GO_API_TIMEOUT=120
"""

    if not env_example.exists():
        env_example.write_text(example_content, encoding="utf-8")
        print(f"[OK] Created {env_example.name}")

    if not env_file.exists():
        env_file.write_text(example_content, encoding="utf-8")
        print(f"[OK] Created initial {env_file.name} (edit with your API keys)")


def main() -> int:
    py_major, py_minor = get_python_version()
    check_only = "--check" in sys.argv
    install_full = "--full" in sys.argv

    print("=" * 60)
    print(" Live2D Master Agent v9.0 - Installation")
    print("=" * 60)
    print(f"Python: {platform.python_version()}")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Project root: {_get_project_root()}")
    print("=" * 60)

    if py_major < 3 or (py_major == 3 and py_minor < 8):
        print("[ERROR] Python 3.8 or higher required")
        return 1

    if check_only:
        print("\n[CHECK] Checking installed packages...")
        all_ok = True
        for dep in CORE_DEPS:
            pkg_name = dep.split(">=")[0]
            ok = check_package(dep)
            status = "OK" if ok else "MISSING"
            if not ok:
                all_ok = False
            print(f"  [{status}] {pkg_name}")
        print(f"\n{'All core dependencies installed!' if all_ok else 'Some dependencies missing. Run: python install.py'}")
        return 0 if all_ok else 1

    # Upgrade pip
    print("\n[STEP 1/5] Upgrading pip...")
    run_pip(["install", "--upgrade", "pip"])

    # Install core dependencies
    print("\n[STEP 2/5] Installing core dependencies (includes cryptography)...")
    failed_core = []
    for dep in CORE_DEPS:
        if not install_package(dep):
            failed_core.append(dep)

    if failed_core:
        print("\n[ERROR] The following core dependencies failed to install:")
        for dep in failed_core:
            print(f"  - {dep}")
        print("\nRecommendations:")
        print("  1. Use Python 3.10, 3.11, or 3.12 for best compatibility")
        print("  2. On Windows: Install Microsoft C++ Build Tools")
        print("  3. Try: pip install --upgrade pip setuptools wheel")
        return 1

    # Install pygame
    print("\n[STEP 3/5] Installing desktop pet dependencies...")
    install_pygame(py_major, py_minor)

    # Optional deps
    print("\n[STEP 4/5] Installing optional dependencies (failures are non-fatal)...")
    for dep in OPTIONAL_DEPS:
        if not install_package(dep):
            if install_full:
                print(f"[WARN] {dep} failed, continuing (--full mode)")
            else:
                print(f"[INFO] Skipped {dep} (not required for core functionality)")

    # Setup config files
    print("\n[STEP 5/5] Setting up configuration...")
    write_env_example()

    # Create output directory
    out_dir = _get_project_root() / "output"
    out_dir.mkdir(exist_ok=True)

    # Quick import test
    print("\n[VERIFY] Testing core imports...")
    try:
        sys.path.insert(0, str(_get_project_root()))
        import live2d
        print(f"[OK] live2d package v{live2d.__version__} loaded")
    except Exception as e:
        print(f"[WARN] Import test failed (non-fatal): {e}")

    print("\n" + "=" * 60)
    print(" Installation Complete!")
    print("=" * 60)
    print("\nQuick start:")
    print('  python master_tool.py "cute anime girl with pink hair"')
    print("  python live2d_workflow.py --help")
    print("  python live2d_agent.py          # Interactive mode")
    print("\nAPI key setup (optional - free providers work without keys):")
    print("  python config_api.py")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
