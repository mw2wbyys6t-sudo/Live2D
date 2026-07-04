#!/usr/bin/env bash
set -e

# ============================================================
# ComfyUI 一键安装脚本
# 用于配合 comfyui-connector 使用
# ============================================================

VERSION="1.0.0"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_banner() {
  echo ''
  echo '  ╔══════════════════════════════════════════════════╗'
  echo '  ║       ComfyUI 一键安装脚本 v'$VERSION'              ║'
  echo '  ║       Live2D Master Agent - 配套工具            ║'
  echo '  ╚══════════════════════════════════════════════════╝'
  echo ''
}

print_step() {
  echo -e "${BLUE}[${1}/${4}]${NC} ${2}..."
  if [ -n "$3" ]; then
    sleep "$3"
  fi
}

print_ok() {
  echo -e "  ${GREEN}✅ ${1}${NC}"
}

print_warn() {
  echo -e "  ${YELLOW}⚠️  ${1}${NC}"
}

print_err() {
  echo -e "  ${RED}❌ ${1}${NC}"
}

check_prerequisites() {
  print_step 1 6 "检查系统环境" 0.5

  # 检查 Python
  if command -v python3 &>/dev/null; then
    PYTHON=$(command -v python3)
    print_ok "Python3: $($PYTHON --version)"
  elif command -v python &>/dev/null; then
    PYTHON=$(command -v python)
    print_ok "Python: $($PYTHON --version)"
  else
    print_err "未找到 Python3，请先安装 Python 3.10+"
    exit 1
  fi

  # 检查 Git
  if command -v git &>/dev/null; then
    print_ok "Git: $(git --version)"
  else
    print_err "未找到 Git，请先安装 Git"
    exit 1
  fi

  # 检查 Node.js (用于连接器)
  if command -v node &>/dev/null; then
    print_ok "Node.js: $(node --version)"
  else
    print_warn "未找到 Node.js，连接器将无法编译"
  fi

  # 检查 pip
  if $PYTHON -m pip --version &>/dev/null; then
    print_ok "pip: 可用"
  else
    print_err "未找到 pip"
    exit 1
  fi
}

install_comfyui() {
  local INSTALL_DIR="${1:-$HOME/ComfyUI}"
  print_step 2 6 "安装 ComfyUI 到 ${INSTALL_DIR}" 0.5

  if [ -d "$INSTALL_DIR" ]; then
    print_warn "ComfyUI 已存在于 ${INSTALL_DIR}"
    read -p "  是否重新安装？(y/N): " REINSTALL
    if [ "$REINSTALL" != "y" ] && [ "$REINSTALL" != "Y" ]; then
      print_ok "使用已安装的 ComfyUI"
      return
    fi
    rm -rf "$INSTALL_DIR"
  fi

  echo "  克隆 ComfyUI 仓库..."
  git clone https://github.com/comfyanonymous/ComfyUI.git "$INSTALL_DIR" 2>&1 | tail -1

  if [ $? -eq 0 ]; then
    print_ok "ComfyUI 克隆成功"
  else
    print_err "ComfyUI 克隆失败"
    exit 1
  fi
}

setup_python_env() {
  local INSTALL_DIR="$1"
  print_step 3 6 "配置 Python 环境" 2

  cd "$INSTALL_DIR"

  # 创建虚拟环境
  if [ ! -d "venv" ]; then
    $PYTHON -m venv venv
    print_ok "虚拟环境创建成功"
  else
    print_ok "虚拟环境已存在"
  fi

  # 激活虚拟环境
  source venv/bin/activate

  # 安装依赖
  print_ok "安装 ComfyUI 依赖（这可能需要几分钟）..."
  pip install --upgrade pip -q 2>&1 | tail -1
  pip install -r requirements.txt -q 2>&1 | tail -5

  print_ok "Python 依赖安装完成"
}

install_models() {
  local INSTALL_DIR="$1"
  print_step 4 6 "下载基础模型" 1

  local MODELS_DIR="$INSTALL_DIR/models/checkpoints"

  if [ ! -d "$MODELS_DIR" ]; then
    mkdir -p "$MODELS_DIR"
  fi

  # 检查已有模型
  local MODEL_COUNT=$(ls "$MODELS_DIR"/*.safetensors 2>/dev/null | wc -l)

  if [ "$MODEL_COUNT" -gt 0 ]; then
    print_ok "已有 $MODEL_COUNT 个模型文件"
    return
  fi

  print_warn "跳过模型下载（模型较大，需要手动下载）"
  print_warn "建议下载: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0"
  echo ""
  echo "  将 .safetensors 文件放入: $MODELS_DIR"
}

setup_connector() {
  local CONNECTOR_DIR="/workspace/comfyui-connector"
  print_step 5 6 "配置 comfyui-connector" 0.5

  if [ -d "$CONNECTOR_DIR" ]; then
    cd "$CONNECTOR_DIR"
    if [ -f "package.json" ]; then
      npm install --silent 2>&1 | tail -1
      npx tsc 2>&1 | tail -1
      print_ok "comfyui-connector 编译成功"
    fi
  else
    print_warn "comfyui-connector 目录不存在，跳过"
  fi
}

test_connection() {
  print_step 6 6 "测试 ComfyUI 连接" 1

  echo ""
  echo "  等待 ComfyUI 启动..."
  echo "  启动命令: cd ~/ComfyUI && python main.py"
  echo ""

  # 尝试连接
  for i in $(seq 1 10); do
    if curl -s --connect-timeout 2 http://127.0.0.1:8188/system_stats > /dev/null 2>&1; then
      print_ok "ComfyUI 连接成功！"

      # 运行连接器测试
      if [ -f "/workspace/comfyui-connector/node_modules/.package-lock.json" ]; then
        cd /workspace/comfyui-connector
        node tests/test-connection.js 2>&1 | tail -10
      fi
      return
    fi
    sleep 2
  done

  print_warn "ComfyUI 未在 127.0.0.1:8188 运行"
  print_warn "请手动启动后重试: cd ~/ComfyUI && python main.py"
}

print_summary() {
  echo ''
  echo '  ╔══════════════════════════════════════════════════╗'
  echo '  ║           安装完成！                             ║'
  echo '  ╚══════════════════════════════════════════════════╝'
  echo ''
  echo '  📁 ComfyUI 位置: ~/ComfyUI'
  echo '  📁 连接器位置: /workspace/comfyui-connector'
  echo ''
  echo '  🚀 启动 ComfyUI:'
  echo '    cd ~/ComfyUI'
  echo '    python main.py'
  echo ''
  echo '  🎯 使用连接器:'
  echo '    cd /workspace/comfyui-connector'
  echo '    node tests/test-connection.js'
  echo '    node tests/run-tests.js --all'
  echo ''
  echo '  📝 完整工作流:'
  echo '    1. python main.py                    # 启动 ComfyUI'
  echo '    2. node tests/test-connection.js     # 测试连接'
  echo '    3. node examples/basic-usage.ts      # 生成图片'
  echo ''
}

# ============================================================
# 主流程
# ============================================================

main() {
  print_banner

  local INSTALL_DIR="${1:-$HOME/ComfyUI}"

  check_prerequisites
  install_comfyui "$INSTALL_DIR"
  setup_python_env "$INSTALL_DIR"
  install_models "$INSTALL_DIR"
  setup_connector
  test_connection
  print_summary
}

main "$@"