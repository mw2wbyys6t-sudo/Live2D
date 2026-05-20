@echo off
chcp 65001 >nul
REM ============================================================================
REM Live2D Master Agent - ComfyUI 一键安装脚本 (Windows)
REM 版本: 1.0
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ========================================================
echo ^|  🎨 Live2D Master Agent - ComfyUI 安装器             ^|
echo ========================================================
echo.

REM 设置安装目录
if "%~1"=="" (
    set INSTALL_DIR=.\Live2D-ComfyUI
) else (
    set INSTALL_DIR=%~1
)

echo 安装目录: %INSTALL_DIR%
echo.

REM 检查系统要求
echo ℹ️ 检查系统要求...

REM 检查 Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 未找到 Python 3，请先安装 Python 3.10+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo.

REM 检查 Git
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 未找到 Git，请先安装 Git
    echo 下载地址: https://git-scm.com/downloads
    pause
    exit /b 1
)

git --version
echo.

echo ✅ 系统检查通过！
echo.

REM 创建安装目录
echo ℹ️ 创建安装目录...
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)
cd /d "%INSTALL_DIR%"

REM 克隆 ComfyUI
echo ℹ️ 正在克隆 ComfyUI...
if exist "ComfyUI" (
    echo ⚠️ ComfyUI 已存在，跳过克隆
) else (
    git clone https://github.com/comfyanonymous/ComfyUI.git
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ 克隆失败
        pause
        exit /b 1
    )
    echo ✅ ComfyUI 克隆完成！
)
echo.

REM 安装依赖
echo ℹ️ 正在安装依赖...
cd ComfyUI
if not exist "venv" (
    echo ℹ️ 创建虚拟环境...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo ℹ️ 升级 pip...
python -m pip install --upgrade pip

echo ℹ️ 安装依赖...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo ❌ 未找到 requirements.txt
    pause
    exit /b 1
)

echo ✅ 依赖安装完成！
echo.

cd ..

REM 创建启动脚本
echo ℹ️ 创建启动脚本...
(
    echo @echo off
    echo cd /d %%~dp0ComfyUI
    echo call venv\Scripts\activate.bat
    echo python main.py --listen
    echo pause
) > start_comfyui.bat

echo ✅ 启动脚本创建完成！
echo.

REM 创建提示词模板
echo ℹ️ 创建提示词模板...
(
    echo # Live2D 专用提示词模板
    echo.
    echo ## 基础模板
    echo anime girl, cute kawaii style,
    echo beautiful face, big expressive eyes,
    echo long flowing pink hair, soft pink gradient hair,
    echo hair strands detailed, wearing JK school uniform,
    echo white blouse, navy blue pleated skirt, red ribbon tie,
    echo slender figure, elegant pose, standing pose,
    echo perfect for Live2D rigging, clean layer separation,
    echo isolated character on white background, easy to rig,
    echo sharp clean lines, vibrant colors, ultra detailed,
    echo masterpiece, award-winning quality, professional artwork,
    echo 4K resolution, high quality render, anime art style,
    echo soft lighting, detailed facial features, sparkling eyes
    echo.
    echo ## 负向提示词
    echo blurry, low quality, bad anatomy, bad hands,
    echo multiple characters, complex background,
    echo merged layers, overlapping parts, extra fingers,
    echo mutated, deformed, disfigured, lowres,
    echo text, watermark, signature, logo,
    echo worst quality, low quality, normal quality,
    echo jpeg artifacts, blurry, out of focus
) > prompts.txt

echo ✅ 提示词模板创建完成！
echo.

REM 创建 README
echo ℹ️ 创建使用说明...
(
    echo # Live2D Master Agent - ComfyUI 配置
    echo.
    echo ## 🚀 快速开始
    echo.
    echo 双击运行 `start_comfyui.bat`
    echo.
    echo 然后在浏览器访问: http://127.0.0.1:8188
    echo.
    echo ## 📥 安装模型
    echo.
    echo 1. 访问 CivitAI: https://civitai.com/
    echo 2. 注册账号
    echo 3. 下载推荐模型:
    echo    - AnythingV5: https://civitai.com/models/9409
    echo    - CounterfeitV3: https://civitai.com/models/4468
    echo    - PastelMix: https://civitai.com/models/39759
    echo 4. 将模型放到 `ComfyUI\models\checkpoints\` 目录
    echo.
    echo ## 🎨 使用提示词模板
    echo.
    echo 查看 `prompts.txt` 中的 Live2D 专用提示词模板
) > README.md

echo ✅ README 创建完成！
echo.

echo ========================================================
echo ^|  ✅ ComfyUI 安装完成！                           ^|
echo ========================================================
echo.
echo 下一步:
echo   1. 下载推荐模型（参考上面的链接）
echo   2. 将模型放到 %INSTALL_DIR%\ComfyUI\models\checkpoints\
echo   3. 运行 start_comfyui.bat
echo   4. 访问 http://127.0.0.1:8188
echo   5. 生成图片后导入到 Live2D Master Agent
echo.
pause
