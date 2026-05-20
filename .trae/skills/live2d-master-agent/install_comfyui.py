#!/usr/bin/env python3
"""
Live2D Master Agent - ComfyUI 自动化安装工具
版本: 1.0
功能: 自动安装 ComfyUI、配置工作流、下载模型
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, Any
import platform
import shutil


class ComfyUISetup:
    """ComfyUI 安装器类"""
    
    def __init__(self, install_dir: Optional[str] = None):
        if install_dir is None:
            self.install_dir = Path.cwd() / "Live2D-ComfyUI"
        else:
            self.install_dir = Path(install_dir)
        
        self.comfyui_dir = self.install_dir / "ComfyUI"
        self.models_dir = self.comfyui_dir / "models" / "checkpoints"
        self.config_dir = Path(__file__).parent
        
    def print_header(self):
        """打印标题"""
        print()
        print("=" * 60)
        print("🎨 Live2D Master Agent - ComfyUI 安装器")
        print("=" * 60)
        print()
    
    def print_success(self, message: str):
        """打印成功消息"""
        print(f"✅ {message}")
    
    def print_warning(self, message: str):
        """打印警告消息"""
        print(f"⚠️ {message}")
    
    def print_error(self, message: str):
        """打印错误消息"""
        print(f"❌ {message}")
    
    def print_info(self, message: str):
        """打印信息"""
        print(f"ℹ️ {message}")
    
    def check_system(self) -> bool:
        """检查系统要求"""
        self.print_info("检查系统要求...")
        
        # 检查 Python
        try:
            python_version = subprocess.check_output(
                ["python", "--version"], 
                text=True, 
                stderr=subprocess.STDOUT
            ).strip()
            print(f"  Python: {python_version}")
        except (subprocess.SubprocessError, FileNotFoundError):
            try:
                python_version = subprocess.check_output(
                    ["python3", "--version"], 
                    text=True, 
                    stderr=subprocess.STDOUT
                ).strip()
                print(f"  Python: {python_version}")
            except:
                self.print_error("未找到 Python 3，请先安装 Python 3.10+")
                print("   下载地址: https://www.python.org/downloads/")
                return False
        
        # 检查 Git
        try:
            git_version = subprocess.check_output(
                ["git", "--version"], 
                text=True, 
                stderr=subprocess.STDOUT
            ).strip()
            print(f"  Git: {git_version}")
        except (subprocess.SubprocessError, FileNotFoundError):
            self.print_error("未找到 Git，请先安装 Git")
            print("   下载地址: https://git-scm.com/downloads")
            return False
        
        self.print_success("系统检查通过！")
        return True
    
    def create_directory(self) -> bool:
        """创建安装目录"""
        self.print_info(f"创建安装目录: {self.install_dir}")
        try:
            self.install_dir.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.print_error(f"创建目录失败: {e}")
            return False
    
    def clone_comfyui(self) -> bool:
        """克隆 ComfyUI 仓库"""
        self.print_info("正在克隆 ComfyUI...")
        
        if self.comfyui_dir.exists():
            self.print_warning("ComfyUI 已存在，跳过克隆")
            return True
        
        try:
            subprocess.run(
                ["git", "clone", "https://github.com/comfyanonymous/ComfyUI.git"],
                cwd=self.install_dir,
                check=True
            )
            self.print_success("ComfyUI 克隆完成！")
            return True
        except subprocess.SubprocessError as e:
            self.print_error(f"克隆失败: {e}")
            return False
    
    def install_dependencies(self) -> bool:
        """安装依赖"""
        self.print_info("正在安装依赖...")
        
        if not self.comfyui_dir.exists():
            self.print_error("ComfyUI 目录不存在")
            return False
        
        # 创建虚拟环境
        venv_dir = self.comfyui_dir / "venv"
        if not venv_dir.exists():
            self.print_info("创建虚拟环境...")
            try:
                python_cmd = self._get_python_cmd()
                subprocess.run(
                    [python_cmd, "-m", "venv", "venv"],
                    cwd=self.comfyui_dir,
                    check=True
                )
            except subprocess.SubprocessError as e:
                self.print_error(f"创建虚拟环境失败: {e}")
                return False
        
        # 激活虚拟环境并安装依赖
        self.print_info("安装 Python 依赖...")
        try:
            python_cmd = self._get_venv_python()
            requirements_file = self.comfyui_dir / "requirements.txt"
            
            if not requirements_file.exists():
                self.print_error("未找到 requirements.txt")
                return False
            
            subprocess.run(
                [python_cmd, "-m", "pip", "install", "--upgrade", "pip"],
                cwd=self.comfyui_dir,
                check=True
            )
            
            subprocess.run(
                [python_cmd, "-m", "pip", "install", "-r", "requirements.txt"],
                cwd=self.comfyui_dir,
                check=True
            )
            
            self.print_success("依赖安装完成！")
            return True
            
        except subprocess.SubprocessError as e:
            self.print_error(f"依赖安装失败: {e}")
            return False
    
    def _get_python_cmd(self) -> str:
        """获取 Python 命令"""
        if platform.system() == "Windows":
            return "python"
        else:
            return "python3"
    
    def _get_venv_python(self) -> str:
        """获取虚拟环境中的 Python 命令"""
        venv_dir = self.comfyui_dir / "venv"
        if platform.system() == "Windows":
            return str(venv_dir / "Scripts" / "python.exe")
        else:
            return str(venv_dir / "bin" / "python")
    
    def create_launch_scripts(self) -> bool:
        """创建启动脚本"""
        self.print_info("创建启动脚本...")
        
        try:
            # Windows 脚本
            if platform.system() == "Windows":
                bat_content = '''@echo off
cd /d %~dp0ComfyUI
call venv\\Scripts\\activate.bat
python main.py --listen
pause
'''
                bat_file = self.install_dir / "start_comfyui.bat"
                bat_file.write_text(bat_content, encoding='utf-8')
            else:
                # Linux/macOS 脚本
                sh_content = '''#!/bin/bash
cd "$(dirname "$0")/ComfyUI"
source venv/bin/activate
python main.py --listen
'''
                sh_file = self.install_dir / "start_comfyui.sh"
                sh_file.write_text(sh_content, encoding='utf-8')
                sh_file.chmod(0o755)
            
            self.print_success("启动脚本创建完成！")
            return True
            
        except Exception as e:
            self.print_error(f"创建启动脚本失败: {e}")
            return False
    
    def create_prompt_templates(self) -> bool:
        """创建提示词模板"""
        self.print_info("创建提示词模板...")
        
        try:
            template_content = '''# Live2D 专用提示词模板

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
'''
            template_file = self.install_dir / "prompts.txt"
            template_file.write_text(template_content, encoding='utf-8')
            
            self.print_success("提示词模板创建完成！")
            return True
            
        except Exception as e:
            self.print_error(f"创建提示词模板失败: {e}")
            return False
    
    def create_readme(self) -> bool:
        """创建 README"""
        self.print_info("创建使用说明...")
        
        try:
            readme_content = '''# Live2D Master Agent - ComfyUI 配置

## 🚀 快速开始

### Windows
双击运行 `start_comfyui.bat`

### Linux/macOS
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
'''
            readme_file = self.install_dir / "README.md"
            readme_file.write_text(readme_content, encoding='utf-8')
            
            self.print_success("README 创建完成！")
            return True
            
        except Exception as e:
            self.print_error(f"创建 README 失败: {e}")
            return False
    
    def show_model_download_info(self):
        """显示模型下载信息"""
        print()
        self.print_warning("注意：CivitAI 模型需要账号，请手动下载")
        print()
        self.print_info("下载链接:")
        print("  - AnythingV5: https://civitai.com/models/9409")
        print("  - CounterfeitV3: https://civitai.com/models/4468")
        print("  - PastelMix: https://civitai.com/models/39759")
        print()
        self.print_warning(f"模型下载后请放到: {self.models_dir}/")
    
    def run(self) -> bool:
        """运行安装流程"""
        self.print_header()
        
        print(f"安装目录: {self.install_dir}")
        print()
        
        if not self.check_system():
            return False
        
        if not self.create_directory():
            return False
        
        if not self.clone_comfyui():
            return False
        
        if not self.install_dependencies():
            return False
        
        if not self.create_launch_scripts():
            return False
        
        if not self.create_prompt_templates():
            return False
        
        if not self.create_readme():
            return False
        
        self.show_model_download_info()
        
        print()
        print("=" * 60)
        self.print_success("ComfyUI 安装完成！")
        print("=" * 60)
        print()
        print("下一步:")
        print("  1. 下载推荐模型（参考上面的链接）")
        print(f"  2. 将模型放到 {self.models_dir}/")
        print("  3. 运行启动脚本")
        print("  4. 访问 http://127.0.0.1:8188")
        print("  5. 生成图片后导入到 Live2D Master Agent")
        print()
        
        return True


def main():
    """主函数"""
    install_dir = None
    if len(sys.argv) > 1:
        install_dir = sys.argv[1]
    
    setup = ComfyUISetup(install_dir)
    success = setup.run()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
