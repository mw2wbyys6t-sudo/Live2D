@echo off
chcp 65001 > nul
REM Live2D Master Agent - 一键安装脚本 (Windows)

echo.
echo ==========================================
echo 🎨 Live2D Master Agent - 一键安装
echo ==========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到 python，请先安装 Python 3.8+
    pause
    exit /b 1
)

python --version
python -c "import sys; print(f'✓ Python 版本: {sys.version_info.major}.{sys.version_info.minor}')"
python -c "import sys; sys.exit(1) if sys.version_info < (3,8) else sys.exit(0)"
if %errorlevel% neq 0 (
    echo ❌ Python 版本过低，需要 3.8+
    pause
    exit /b 1
)

cd /d "%~dp0"

echo.
echo ==========================================
echo 🚀 开始安装
echo ==========================================
echo.

python install.py

echo.
pause

