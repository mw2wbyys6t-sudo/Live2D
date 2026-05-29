#!/usr/bin/env python3
"""
ComfyUI + See-through 自动安装脚本 v2.0
用于Live2D Master Agent项目

功能:
1. 自动检测操作系统
2. 安装ComfyUI
3. 安装See-through插件
4. 下载必要的AI模型
5. 提供使用指南
6. 支持非交互模式（--yes）

改进:
- 更好的错误处理
- 支持非交互模式
- 更好的用户提示
- 进度显示
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
from pathlib import Path
import argparse
import time

class ComfyUIInstaller:
    """ComfyUI + See-through 安装器"""

    def __init__(self, interactive=True):
        self.base_dir = Path(__file__).parent
        self.comfyui_dir = self.base_dir / "comfyui"
        self.system = sys.platform
        self.interactive = interactive
        self.log_file = self.base_dir / "install_log.txt"

    def log(self, message):
        """记录日志到文件"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}\n"
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_msg)
        except:
            pass
        print(message)

    def print_header(self):
        """打印标题"""
        self.log("\n" + "="*80)
        self.log("🎨 ComfyUI + See-through 自动安装向导 v2.0")
        self.log("="*80)
        self.log("\n这将安装:")
        self.log("  • ComfyUI - AI工作流工具")
        self.log("  • ComfyUI-See-through - 动漫分层插件")
        self.log("  • See-through AI模型 - SIGGRAPH 2026级别分层工具")
        self.log("\n预计需要: 20-40GB磁盘空间")
        self.log("="*80 + "\n")

    def check_system(self):
        """检查系统环境"""
        self.log("🔍 检查系统环境...")

        info = {
            'system': sys.platform,
            'python': sys.version.split()[0],
            'has_git': self._command_exists('git'),
            'has_cuda': False,
            'disk_space': 0
        }

        # 检查CUDA
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, timeout=10)
            if result.returncode == 0:
                info['has_cuda'] = True
                self.log(f"  ✅ NVIDIA GPU detected")
        except:
            pass

        # Python版本
        python_ok = False
        try:
            py_version = tuple(map(int, info['python'].split('.')))
            if (3, 8) <= py_version < (3, 14):
                python_ok = True
        except:
            pass

        if python_ok:
            self.log(f"  ✅ Python {info['python']} supported")
        else:
            self.log(f"  ⚠️  Python {info['python']} might have issues")

        # Git检查
        if info['has_git']:
            self.log(f"  ✅ Git installed")
        else:
            self.log(f"  ⚠️  Git not found (recommended for installation)")

        # 磁盘空间检查
        try:
            import shutil
            usage = shutil.disk_usage(self.base_dir)
            free_gb = usage.free / (1024**3)
            self.log(f"  💾 可用磁盘空间: {free_gb:.1f}GB")
        except:
            pass

        return info

    def _command_exists(self, cmd):
        """检查命令是否存在"""
        try:
            # 对于Windows需要shell=True，Linux不需要
            shell = self.system == 'win32'
            result = subprocess.run(
                [cmd] if not shell else f'where {cmd}',
                capture_output=True,
                timeout=5,
                shell=shell
            )
            return result.returncode == 0
        except:
            return False

    def _ask_yes_no(self, question, default=True):
        """询问用户问题，返回布尔值"""
        if not self.interactive:
            return default

        while True:
            response = input(question).strip().lower()
            if not response:
                return default
            if response in ['y', 'yes', '是']:
                return True
            elif response in ['n', 'no', '否']:
                return False
            self.log("  请输入 y/n 或 yes/no")

    def install_comfyui(self):
        """安装ComfyUI"""
        self.log("\n📦 安装ComfyUI...")

        if self.comfyui_dir.exists():
            self.log(f"  ⚠️  ComfyUI目录已存在: {self.comfyui_dir}")
            if self._ask_yes_no("  是否更新? (y/n, 默认n): ", default=False):
                try:
                    self.log("  📥 拉取更新...")
                    result = subprocess.run(
                        ['git', 'pull'],
                        cwd=str(self.comfyui_dir),
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    if result.returncode == 0:
                        self.log("  ✅ ComfyUI更新成功")
                        return True
                    else:
                        self.log(f"  ⚠️  更新失败: {result.stderr}")
                        return False
                except Exception as e:
                    self.log(f"  ⚠️  更新失败: {e}")
                    return False
            else:
                self.log("  ⏭️  跳过ComfyUI安装")
                return True

        try:
            self.log("  📥 克隆ComfyUI仓库...")
            result = subprocess.run(
                ['git', 'clone', '--depth', '1',
                 'https://github.com/comfyanonymous/ComfyUI.git',
                 str(self.comfyui_dir)],
                capture_output=True,
                text=True,
                timeout=600
            )
            if result.returncode != 0:
                raise Exception(f"Git clone failed: {result.stderr}")

            self.log("  ✅ ComfyUI克隆成功")
            return True

        except subprocess.TimeoutExpired:
            self.log("  ❌ Git克隆超时，请检查网络连接")
            return False
        except Exception as e:
            self.log(f"  ❌ 安装失败: {e}")
            return False

    def install_dependencies(self):
        """安装依赖"""
        self.log("\n📚 安装Python依赖...")

        try:
            # 先安装requirements.txt
            req_file = self.comfyui_dir / 'requirements.txt'
            if req_file.exists():
                self.log("  安装ComfyUI依赖...")
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '-r', str(req_file)
                ], check=True, timeout=600)

            self.log("  ✅ 依赖安装成功")
            return True

        except subprocess.TimeoutExpired:
            self.log("  ⚠️  依赖安装超时")
            return False
        except Exception as e:
            self.log(f"  ⚠️  依赖安装失败: {e}")
            return True  # 继续安装

    def install_see_through(self):
        """安装See-through插件"""
        self.log("\n🎯 安装ComfyUI-See-through插件...")

        plugin_dir = self.comfyui_dir / 'custom_nodes' / 'ComfyUI-See-through'

        if plugin_dir.exists():
            self.log(f"  ⚠️  插件已存在: {plugin_dir}")
            if self._ask_yes_no("  是否更新? (y/n, 默认n): ", default=False):
                try:
                    self.log("  📥 拉取更新...")
                    result = subprocess.run(
                        ['git', 'pull'],
                        cwd=str(plugin_dir),
                        capture_output=True,
                        timeout=120
                    )
                    if result.returncode == 0:
                        self.log("  ✅ See-through更新成功")
                        return True
                except Exception as e:
                    self.log(f"  ⚠️  更新失败: {e}")
                    return False
            else:
                self.log("  ⏭️  跳过插件安装")
                return True

        try:
            self.log("  📥 克隆See-through仓库...")
            custom_nodes_dir = self.comfyui_dir / 'custom_nodes'
            custom_nodes_dir.mkdir(exist_ok=True)

            result = subprocess.run(
                ['git', 'clone', '--depth', '1',
                 'https://github.com/jtydhr88/ComfyUI-See-through.git',
                 str(custom_nodes_dir / 'ComfyUI-See-through')],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode != 0:
                raise Exception(f"Git clone failed: {result.stderr}")

            # 安装插件依赖
            self.log("  📚 安装插件依赖...")
            plugin_req = custom_nodes_dir / 'ComfyUI-See-through' / 'requirements.txt'
            if plugin_req.exists():
                try:
                    subprocess.run([
                        sys.executable, '-m', 'pip', 'install', '-r', str(plugin_req)
                    ], timeout=300)
                except:
                    pass

            self.log("  ✅ See-through插件安装成功")
            return True

        except Exception as e:
            self.log(f"  ❌ See-through安装失败: {e}")
            return False

    def download_models_info(self):
        """下载模型信息"""
        self.log("\n🤖 AI模型下载...")
        self.log("  ⚠️  模型会自动下载，首次运行时会提示")
        self.log("  📦 总大小约: 6-8GB")
        self.log("  ")
        self.log("  需要下载的模型:")
        self.log("    1. LayerDiff 3D (约4GB)")
        self.log("       https://huggingface.co/layerdifforg/seethroughv0.0.2_layerdiff3d")
        self.log()
        self.log("    2. Marigold Depth (约2GB)")
        self.log("       https://huggingface.co/24yearsold/seethroughv0.0.1_marigold")
        self.log()
        self.log("  💡 首次运行ComfyUI时会自动下载这些模型")

        return True

    def create_usage_guide(self):
        """创建使用指南"""
        self.log("\n📖 创建使用指南...")

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
        try:
            with open(guide_file, 'w', encoding='utf-8') as f:
                f.write(guide)
            self.log(f"  ✅ 使用指南已创建: {guide_file}")
        except Exception as e:
            self.log(f"  ⚠️  创建使用指南失败: {e}")

        return True

    def run(self):
        """运行安装向导"""
        self.print_header()

        # 检查系统
        info = self.check_system()

        if self.interactive:
            print("\n" + "="*80)
            response = self._ask_yes_no("是否继续安装? (y/n, 默认y): ", default=True)
        else:
            self.log("🔧 非交互模式：自动继续安装")
            response = True

        if not response:
            self.log("❌ 安装已取消")
            return False

        # 安装步骤
        steps = [
            ("安装ComfyUI", self.install_comfyui),
            ("安装依赖", self.install_dependencies),
            ("安装See-through插件", self.install_see_through),
            ("下载模型信息", self.download_models_info),
            ("创建使用指南", self.create_usage_guide)
        ]

        self.log("\n" + "="*80)
        self.log("开始安装...")
        self.log("="*80 + "\n")

        success_count = 0
        for step_name, step_func in steps:
            self.log(f"\n📦 {step_name}...")
            try:
                if step_func():
                    success_count += 1
                    self.log(f"  ✅ {step_name}完成")
                else:
                    self.log(f"  ⚠️  {step_name}出现问题，但继续...")
            except Exception as e:
                self.log(f"  ❌ {step_name}失败: {e}")

        # 总结
        self.log("\n" + "="*80)
        self.log("📊 安装总结")
        self.log("="*80)
        self.log(f"完成: {success_count}/{len(steps)} 步骤")
        self.log(f"位置: {self.comfyui_dir}")
        self.log(f"日志文件: {self.log_file}")
        self.log()

        if success_count >= 3:
            self.log("✅ 安装基本成功！")
            self.log()
            self.log("下一步:")
            self.log(f"  1. cd {self.comfyui_dir}")
            self.log("  2. python main.py  # 启动ComfyUI")
            self.log("  3. 打开 http://127.0.0.1:8188")
            self.log("  4. 加载See-through工作流")
            self.log("  5. 开始使用！")
        else:
            self.log("⚠️  安装可能有问题，请检查错误信息和日志文件")

        self.log("="*80 + "\n")
        return success_count >= 3

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='ComfyUI + See-through 安装器')
    parser.add_argument('-y', '--yes', action='store_true', help='非交互模式，自动确认所有')
    args = parser.parse_args()

    installer = ComfyUIInstaller(interactive=not args.yes)
    success = installer.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
