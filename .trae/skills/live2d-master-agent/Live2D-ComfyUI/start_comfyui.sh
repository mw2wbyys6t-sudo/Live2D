#!/bin/bash
# ComfyUI 启动脚本
# 自动检测 GPU/CPU 环境并选择最佳启动方式

echo "======================================"
echo "🎨 ComfyUI 启动器"
echo "======================================"
echo ""

# 进入 ComfyUI 目录
cd "$(dirname "$0")/ComfyUI"

# 激活虚拟环境
source venv/bin/activate

# 检测 NVIDIA GPU
echo "检测系统环境..."

if command -v nvidia-smi &> /dev/null; then
    if nvidia-smi &> /dev/null; then
        echo "✅ 检测到 NVIDIA GPU，将使用 GPU 加速"
        echo ""
        echo "启动 ComfyUI..."
        python main.py --listen --port 8188
    else
        echo "⚠️ NVIDIA 驱动未正常工作"
        echo "尝试使用 CPU 模式..."
        echo ""
        echo "启动 ComfyUI (CPU 模式)..."
        python main.py --listen --port 8188 --cpu-vae
    fi
else
    echo "⚠️ 未检测到 NVIDIA GPU"
    echo ""
    echo "可选方案:"
    echo "  1. 安装 NVIDIA GPU 和驱动 (推荐)"
    echo "  2. 使用 CPU 模式运行 (较慢)"
    echo "  3. 使用云端 ComfyUI 服务"
    echo ""
    read -p "是否使用 CPU 模式启动？(y/n): " choice
    
    if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
        echo ""
        echo "启动 ComfyUI (CPU 模式)..."
        echo "注意: CPU 模式速度较慢，请耐心等待"
        echo ""
        python main.py --listen --port 8188 --cpu-vae
    else
        echo ""
        echo "启动取消。"
        echo "如需更高质量图像，可使用免费方案:"
        echo "  python quick_gen.py \"你的描述\""
        exit 0
    fi
fi
