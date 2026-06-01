#!/bin/bash
# Live2D Master Agent - 一键安装脚本 (macOS/Linux)

echo ""
echo "=========================================="
echo "🎨 Live2D Master Agent - 一键安装"
echo "=========================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3，请先安装 Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "📋 Python 版本: $PYTHON_VERSION"

# 检查版本
python3 -c "
import sys
if sys.version_info < (3, 8):
    print('❌ Python 版本过低，需要 3.8+')
    sys.exit(1)
print('✓ Python 版本符合要求')
"
if [ $? -ne 0 ]; then
    exit 1
fi

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo ""
echo "=========================================="
echo "🚀 开始安装"
echo "=========================================="
echo ""

# 运行 Python 安装脚本
python3 install.py

