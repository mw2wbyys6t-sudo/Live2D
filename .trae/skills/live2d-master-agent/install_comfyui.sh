#!/bin/bash
# ==============================================================================
# Live2D Master Agent - ComfyUI 一键安装脚本
# 版本: 1.0
# 功能: 自动安装 ComfyUI 和 Live2D 专用工作流
# ==============================================================================

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印标题
print_header() {
    echo ""
    echo -e "${BLUE}========================================================${NC}"
    echo -e "${BLUE}🎨 Live2D Master Agent - ComfyUI 安装器${NC}"
    echo -e "${BLUE}========================================================${NC}"
    echo ""
}

# 打印成功消息
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# 打印警告消息
print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

# 打印错误消息
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 打印信息
print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# 检查系统要求
check_system() {
    print_info "检查系统要求..."
    
    # 检查 Python
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        print_error "未找到 Python 3，请先安装 Python 3.10+"
        echo "下载地址: https://www.python.org/downloads/"
        exit 1
    fi
    
    # 检查 Git
    if ! command -v git &> /dev/null; then
        print_error "未找到 Git，请先安装 Git"
        echo "下载地址: https://git-scm.com/downloads"
        exit 1
    fi
    
    print_success "系统检查通过！"
}

# 获取 Python 命令
get_python_cmd() {
    if command -v python3 &> /dev/null; then
        echo "python3"
    elif command -v python &> /dev/null; then
        echo "python"
    else
        echo "python3"
    fi
}

# 创建安装目录
create_install_dir() {
    local install_dir="$1"
    if [ ! -d "$install_dir" ]; then
        mkdir -p "$install_dir"
    fi
    cd "$install_dir"
}

# 克隆 ComfyUI
clone_comfyui() {
    local install_dir="$1"
    print_info "正在克隆 ComfyUI..."
    
    if [ -d "$install_dir/ComfyUI" ]; then
        print_warning "ComfyUI 已存在，跳过克隆"
    else
        git clone https://github.com/comfyanonymous/ComfyUI.git
        print_success "ComfyUI 克隆完成！"
    fi
}

# 安装依赖
install_dependencies() {
    local python_cmd=$(get_python_cmd)
    print_info "正在安装依赖..."
    
    cd ComfyUI
    
    if [ ! -d "venv" ]; then
        print_info "创建虚拟环境..."
        "$python_cmd" -m venv venv
    fi
    
    # 激活虚拟环境
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
        # Windows
        source venv/Scripts/activate || true
        if [ ! $? -eq 0 ]; then
            . venv/Scripts/activate
        fi
    else
        # Linux/macOS
        source venv/bin/activate || true
        if [ ! $? -eq 0 ]; then
            . venv/bin/activate
        fi
    fi
    
    # 升级 pip
    pip install --upgrade pip
    
    # 安装依赖
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        print_error "未找到 requirements.txt"
        exit 1
    fi
    
    print_success "依赖安装完成！"
}

# 下载推荐模型
download_models() {
    print_info "正在下载推荐模型..."
    
    local models_dir="ComfyUI/models/checkpoints"
    mkdir -p "$models_dir"
    
    # 模型列表
    declare -A models
    models["AnythingV5"]="https://civitai.com/api/download/models/9409"
    models["CounterfeitV3"]="https://civitai.com/api/download/models/4468"
    models["PastelMix"]="https://civitai.com/api/download/models/39759"
    
    print_warning "注意：CivitAI 模型需要账号，请手动下载"
    print_warning "下载链接:"
    echo "  - AnythingV5: https://civitai.com/models/9409"
    echo "  - CounterfeitV3: https://civitai.com/models/4468"
    echo "  - PastelMix: https://civitai.com/models/39759"
    echo ""
    print_warning "模型下载后请放到: $models_dir/"
}

# 创建启动脚本
create_start_script() {
    print_info "创建启动脚本..."
    
    # Windows
    cat > start_comfyui.bat << 'EOF'
@echo off
cd ComfyUI
call venv\Scripts\activate.bat
python main.py --listen
pause
EOF
    
    # Linux/macOS
    cat > start_comfyui.sh << 'EOF'
#!/bin/bash
cd ComfyUI
source venv/bin/activate
python main.py --listen
EOF
    
    chmod +x start_comfyui.sh
    
    print_success "启动脚本创建完成！"
}

# 创建工作流文件
create_workflows() {
    print_info "创建 Live2D 专用工作流..."
    
    local workflows_dir="ComfyUI/custom_nodes"
    mkdir -p "$workflows_dir"
    
    cat > live2d_workflow.json << 'EOF'
{
  "name": "Live2D Character Generator",
  "description": "生成适合 Live2D 的高质量动漫角色立绘",
  "workflow": {
    "nodes": [
      {
        "id": 1,
        "type": "KSampler",
        "inputs": {
          "model": ["model", 0],
          "seed": ["seed", 0],
          "steps": ["steps", 0],
          "cfg": ["cfg", 0],
          "sampler_name": ["sampler_name", 0],
          "scheduler": ["scheduler", 0],
          "positive": ["clip", 0],
          "negative": ["clip", 1],
          "latent_image": ["empty_latent", 0]
        }
      }
    ],
    "defaults": {
      "seed": -1,
      "steps": 30,
      "cfg": 7.0,
      "width": 2048,
      "height": 2048,
      "model": "AnythingV5.safetensors"
    }
  }
}
EOF
    
    print_success "工作流文件创建完成！"
}

# 创建提示词模板
create_prompt_templates() {
    print_info "创建提示词模板..."
    
    cat > prompts.txt << 'EOF'
# Live2D 专用提示词模板

## 基础模板
anime girl, cute kawaii style,
beautiful face, big expressive eyes,
long flowing pink hair, soft pink gradient hair,
hair strands detailed, wearing JK school uniform,
white blouse, navy blue pleated skirt, red ribbon tie,
slender figure, elegant pose, standing pose,
perfect for Live2D rigging, clean layer separation,
isolated character on white background, easy to rig,
sharp clean lines, vibrant colors, ultra detailed,
masterpiece, award-winning quality, professional artwork,
4K resolution, high quality render, anime art style,
soft lighting, detailed facial features, sparkling eyes

## 负向提示词
blurry, low quality, bad anatomy, bad hands,
multiple characters, complex background,
merged layers, overlapping parts, extra fingers,
mutated, deformed, disfigured, lowres,
text, watermark, signature, logo,
worst quality, low quality, normal quality,
jpeg artifacts, blurry, out of focus

## 风格变体

### 可爱萌系
anime girl, cute kawaii, moe style,
big eyes, soft features, pastel colors,
gentle expression, happy, smiling

### 帅气中性
anime girl, cool style, tomboy,
sharp features, confident expression,
dark colors, dynamic pose

### 优雅精致
anime girl, elegant, refined,
detailed features, graceful pose,
vibrant colors, high fashion

### 奇幻魔法
anime girl, magical girl, fantasy,
sparkles, magical elements,
ethereal, mystical atmosphere
EOF
    
    print_success "提示词模板创建完成！"
}

# 创建 README
create_readme() {
    print_info "创建使用说明..."
    
    cat > README.md << 'EOF'
# Live2D Master Agent - ComfyUI 配置

## 🚀 快速开始

### 启动 ComfyUI

#### Windows
双击运行 `start_comfyui.bat`

#### Linux/macOS
```bash
./start_comfyui.sh
```

然后在浏览器访问: http://127.0.0.1:8188

## 📥 安装模型

1. 访问 CivitAI: https://civitai.com/
2. 注册账号
3. 下载推荐模型:
   - AnythingV5: https://civitai.com/models/9409
   - CounterfeitV3: https://civitai.com/models/4468
   - PastelMix: https://civitai.com/models/39759
4. 将模型放到 `ComfyUI/models/checkpoints/` 目录

## 🎨 使用提示词模板

查看 `prompts.txt` 中的 Live2D 专用提示词模板

## 📋 工作流程

1. 启动 ComfyUI
2. 选择模型（推荐 AnythingV5）
3. 输入提示词
4. 生成图片
5. 保存图片
6. 导入到 Live2D Master Agent 进行后续处理

## 📞 问题反馈

如有问题，请查看: https://github.com/comfyanonymous/ComfyUI
EOF
    
    print_success "README 创建完成！"
}

# 主函数
main() {
    print_header
    
    local install_dir="$1"
    if [ -z "$install_dir" ]; then
        install_dir="./Live2D-ComfyUI"
    fi
    
    echo ""
    print_info "安装目录: $install_dir"
    echo ""
    
    # 检查系统
    check_system
    
    # 创建目录
    print_info "创建安装目录..."
    create_install_dir "$install_dir"
    
    # 克隆 ComfyUI
    clone_comfyui "$install_dir"
    
    # 安装依赖
    install_dependencies
    
    # 创建启动脚本
    create_start_script
    
    # 创建工作流
    create_workflows
    
    # 创建提示词模板
    create_prompt_templates
    
    # 创建 README
    create_readme
    
    # 提示下载模型
    download_models
    
    echo ""
    echo -e "${GREEN}========================================================${NC}"
    echo -e "${GREEN}✅ ComfyUI 安装完成！${NC}"
    echo -e "${GREEN}========================================================${NC}"
    echo ""
    echo "下一步："
    echo "  1. 下载推荐模型（参考上面的链接）"
    echo "  2. 将模型放到 $install_dir/ComfyUI/models/checkpoints/"
    echo "  3. 运行启动脚本:"
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
        echo "     Windows: start_comfyui.bat"
    else
        echo "     Linux/macOS: ./start_comfyui.sh"
    fi
    echo "  4. 访问 http://127.0.0.1:8188"
    echo "  5. 生成图片后导入到 Live2D Master Agent"
    echo ""
}

# 运行主函数
main "$@"
