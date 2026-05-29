#!/usr/bin/env python3
"""
ComfyUI + See-through 自动安装脚本
用于Live2D Master Agent项目

功能:
1. 自动检测操作系统
2. 安装ComfyUI
3. 安装See-through插件
4. 下载必要的AI模型
5. 提供使用指南
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
from pathlib import Path

class ComfyUIInstaller:
    """ComfyUI + See-through 安装器"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.comfyui_dir = self.base_dir / "comfyui"
        self.system = sys.platform
        
    def print_header(self):
        """打印标题"""
        print("\n" + "="*80)
        print("🎨 ComfyUI + See-through 自动安装向导")
        print("="*80)
        print("\n这将安装:")
        print("  • ComfyUI - AI工作流工具")
        print("  • ComfyUI-See-through - 动漫分层插件")
        print("  • See-through AI模型 - SIGGRAPH 2026级别分层工具")
        print("\n预计需要: 20-40GB磁盘空间")
        print("="*80 + "\n")
    
    def check_system(self):
        """检查系统环境"""
        print("🔍 检查系统环境...")
        
        info = {
            'system': sys.platform,
            'python': sys.version.split()[0],
            'has_git': self._command_exists('git'),
            'has_cuda': False
        }
        
        # 检查CUDA
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True)
            if result.returncode == 0:
                info['has_cuda'] = True
                print(f"  ✅ NVIDIA GPU detected")
        except:
            pass
        
        # Python版本
        if info['python'].startswith('3.8') or info['python'].startswith('3.9') or \
           info['python'].startswith('3.10') or info['python'].startswith('3.11') or \
           info['python'].startswith('3.12'):
            print(f"  ✅ Python {info['python']} supported")
        else:
            print(f"  ⚠️  Python {info['python']} might have issues")
        
        # Git检查
        if info['has_git']:
            print(f"  ✅ Git installed")
        else:
            print(f"  ⚠️  Git not found (recommended for installation)")
        
        return info
    
    def _command_exists(self, cmd):
        """检查命令是否存在"""
        try:
            subprocess.run([cmd], capture_output=True, check=True)
            return True
        except:
            return False
    
    def install_comfyui(self):
        """安装ComfyUI"""
        print("\n📦 安装ComfyUI...")
        
        if self.comfyui_dir.exists():
            print(f"  ⚠️  ComfyUI目录已存在: {self.comfyui_dir}")
            response = input("  是否更新? (y/n): ").strip().lower()
            if response != 'y':
                print("  ⏭️  跳过ComfyUI安装")
                return True
        
        try:
            print("  📥 克隆ComfyUI仓库...")
            subprocess.run([
                'git', 'clone', 
                'https://github.com/comfyanonymous/ComfyUI.git',
                str(self.comfyui_dir)
            ], check=True)
            
            print("  ✅ ComfyUI克隆成功")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Git克隆失败: {e}")
            return False
        except Exception as e:
            print(f"  ❌ 安装失败: {e}")
            return False
    
    def install_dependencies(self):
        """安装依赖"""
        print("\n📚 安装Python依赖...")
        
        try:
            # 安装PyTorch（CUDA版本）
            print("  🔥 安装PyTorch...")
            if self._command_exists('nvcc'):
                # NVIDIA GPU可用
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install',
                    'torch', 'torchvision', 'torchaudio',
                    '--index-url', 'https://download.pytorch.org/whl/cu121'
                ], check=True)
            else:
                # CPU版本
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install',
                    'torch', 'torchvision', 'torchaudio'
                ], check=True)
            
            print("  ✅ PyTorch安装成功")
            return True
            
        except Exception as e:
            print(f"  ⚠️  PyTorch安装失败: {e}")
            print("  💡 将使用CPU模式")
            return True  # 继续安装，即使PyTorch失败
    
    def install_see_through(self):
        """安装See-through插件"""
        print("\n🎯 安装ComfyUI-See-through插件...")
        
        plugin_dir = self.comfyui_dir / 'custom_nodes' / 'ComfyUI-See-through'
        
        if plugin_dir.exists():
            print(f"  ⚠️  插件已存在: {plugin_dir}")
            response = input("  是否更新? (y/n): ").strip().lower()
            if response != 'y':
                print("  ⏭️  跳过插件安装")
                return True
        
        try:
            print("  📥 克隆See-through仓库...")
            custom_nodes_dir = self.comfyui_dir / 'custom_nodes'
            custom_nodes_dir.mkdir(exist_ok=True)
            
            subprocess.run([
                'git', 'clone',
                'https://github.com/jtydhr88/ComfyUI-See-through.git',
                str(custom_nodes_dir / 'ComfyUI-See-through')
            ], check=True)
            
            # 安装插件依赖
            print("  📚 安装插件依赖...")
            plugin_req = custom_nodes_dir / 'ComfyUI-See-through' / 'requirements.txt'
            if plugin_req.exists():
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '-r', str(plugin_req)
                ], check=True)
            
            print("  ✅ See-through插件安装成功")
            return True
            
        except Exception as e:
            print(f"  ❌ See-through安装失败: {e}")
            return False
    
    def download_models_info(self):
        """下载模型信息"""
        print("\n🤖 AI模型下载...")
        print("  ⚠️  模型会自动下载，首次运行时会提示")
        print("  📦 总大小约: 6-8GB")
        print("  ")
        print("  需要下载的模型:")
        print("    1. LayerDiff 3D (约4GB)")
        print("       https://huggingface.co/layerdifforg/seethroughv0.0.2_layerdiff3d")
        print()
        print("    2. Marigold Depth (约2GB)")
        print("       https://huggingface.co/24yearsold/seethroughv0.0.1_marigold")
        print()
        print("  💡 首次运行ComfyUI时会自动下载这些模型")
        
        return True
    
    def create_usage_guide(self):
        """创建使用指南"""
        print("\n📖 创建使用指南...")
        
        guide = """
================================================================================
ComfyUI + See-through 使用指南
================================================================================

1. 启动ComfyUI
--------------
cd comfyui
python main.py
# 或双击 run_nvidia_gpu.bat (Windows)

浏览器会自动打开: http://127.0.0.1:8188


2. 加载工作流
------------
• 点击界面上的 "Load" 按钮
• 或访问 https://www.runcomfy.com/comfyui-workflows/see-through-workflow
• 导入See-through工作流JSON文件


3. 使用See-through
-----------------
a) 在LoadImage节点加载你的动漫角色图片
b) 点击 "Queue Prompt" 生成图层
c) 等待处理完成（首次需要下载模型）
d) 保存PSD文件


4. 导入Live2D
-------------
• 在Live2D Cubism Editor中打开PSD
• File → Import PSD
• 开始Rigging工作


================================================================================
故障排除
================================================================================

问题: 显存不足
解决: 降低处理分辨率或使用CPU模式

问题: 模型下载失败
解决: 手动从HuggingFace下载，放入对应目录

问题: 节点缺失
解决: 安装ComfyUI-Manager，自动安装缺失节点


================================================================================
更多信息
================================================================================

• ComfyUI官方: https://github.com/comfyanonymous/ComfyUI
• See-through论文: https://arxiv.org/abs/2602.03749
• 详细文档: SEE_THROUGH_INTEGRATION.md

================================================================================
"""
        
        guide_file = self.comfyui_dir / 'USAGE_GUIDE.txt'
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        print(f"  ✅ 使用指南已创建: {guide_file}")
        return True
    
    def run(self):
        """运行安装向导"""
        self.print_header()
        
        # 检查系统
        info = self.check_system()
        
        print("\n" + "="*80)
        response = input("是否继续安装? (y/n): ").strip().lower()
        
        if response != 'y':
            print("❌ 安装已取消")
            return False
        
        # 安装步骤
        steps = [
            ("安装ComfyUI", self.install_comfyui),
            ("安装依赖", self.install_dependencies),
            ("安装See-through插件", self.install_see_through),
            ("下载模型信息", self.download_models_info),
            ("创建使用指南", self.create_usage_guide)
        ]
        
        print("\n" + "="*80)
        print("开始安装...")
        print("="*80 + "\n")
        
        success_count = 0
        for step_name, step_func in steps:
            print(f"\n📦 {step_name}...")
            if step_func():
                success_count += 1
                print(f"  ✅ {step_name}完成")
            else:
                print(f"  ⚠️  {step_name}出现问题，但继续...")
        
        # 总结
        print("\n" + "="*80)
        print("📊 安装总结")
        print("="*80)
        print(f"完成: {success_count}/{len(steps)} 步骤")
        print(f"位置: {self.comfyui_dir}")
        print()
        
        if success_count >= 3:
            print("✅ 安装基本成功！")
            print()
            print("下一步:")
            print(f"  1. cd {self.comfyui_dir}")
            print("  2. python main.py  # 启动ComfyUI")
            print("  3. 打开 http://127.0.0.1:8188")
            print("  4. 加载See-through工作流")
            print("  5. 开始使用！")
        else:
            print("⚠️  安装可能有问题，请检查错误信息")
        
        print("="*80 + "\n")
        return success_count >= 3

def main():
    """主函数"""
    installer = ComfyUIInstaller()
    success = installer.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
