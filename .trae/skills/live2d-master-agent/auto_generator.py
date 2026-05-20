#!/usr/bin/env python3
"""
Live2D Master Agent - 完全自动化的图像生成工具
版本: 2.0
特点: 自动检测环境、自动安装依赖、智能选择最佳方案
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, Any
import platform
import time


class AutoImageGenerator:
    """自动图像生成器 - 智能选择最佳方案"""
    
    def __init__(self):
        self.workspace_dir = Path.cwd()
        self.output_dir = self.workspace_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # 方案优先级（从高到低）
        self.priority_order = [
            "comfyui_local",
            "seedream_api", 
            "playground_ai",
            "manual_input"
        ]
        
        # 当前选中的方案
        self.selected_provider = None
        
    def print_header(self):
        """打印标题"""
        print()
        print("=" * 70)
        print("🎨 Live2D Master Agent - 智能图像生成器")
        print("=" * 70)
        print()
        print("自动检测环境，选择最佳图像生成方案")
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
    
    def check_comfyui(self) -> bool:
        """检查 ComfyUI 是否已安装"""
        comfyui_dir = self.workspace_dir / "Live2D-ComfyUI" / "ComfyUI"
        return comfyui_dir.exists()
    
    def check_seedream_api(self) -> bool:
        """检查 Seedream API 是否已配置"""
        api_key = os.getenv("ARK_API_KEY")
        return bool(api_key)
    
    def check_comfyui_running(self) -> bool:
        """检查 ComfyUI 是否正在运行"""
        try:
            import requests
            response = requests.get("http://127.0.0.1:8188/system_stats", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def detect_best_option(self) -> str:
        """检测最佳图像生成方案"""
        self.print_info("正在检测可用的图像生成方案...")
        print()
        
        available = []
        
        # 检查 ComfyUI 是否运行中
        if self.check_comfyui_running():
            available.append("comfyui_local")
            self.print_success("✓ ComfyUI 正在运行")
        else:
            # 检查 ComfyUI 是否已安装
            if self.check_comfyui():
                available.append("comfyui_local")
                self.print_info("✓ ComfyUI 已安装（未运行）")
            else:
                self.print_warning("✗ ComfyUI 未安装")
        
        # 检查 Seedream API
        if self.check_seedream_api():
            available.append("seedream_api")
            self.print_success("✓ Seedream API 已配置")
        else:
            self.print_warning("✗ Seedream API 未配置")
        
        # Playground AI（始终可用）
        available.append("playground_ai")
        self.print_info("✓ Playground AI（在线免费）")
        
        # 手动输入（始终可用）
        available.append("manual_input")
        self.print_info("✓ 手动上传图片")
        
        print()
        
        # 选择优先级最高的方案
        for option in self.priority_order:
            if option in available:
                self.print_success(f"选中方案: {self._get_option_name(option)}")
                return option
        
        return "manual_input"
    
    def _get_option_name(self, option: str) -> str:
        """获取方案名称"""
        names = {
            "comfyui_local": "ComfyUI（本地，最高质量）",
            "seedream_api": "Seedream API（快速，中等质量）",
            "playground_ai": "Playground AI（在线免费）",
            "manual_input": "手动上传图片"
        }
        return names.get(option, option)
    
    def install_comfyui(self) -> bool:
        """自动安装 ComfyUI"""
        self.print_info("正在自动安装 ComfyUI...")
        
        try:
            # 检查 Python
            result = subprocess.run(
                ["python", "--version"], 
                capture_output=True, 
                text=True
            )
            if result.returncode != 0:
                self.print_error("未找到 Python")
                return False
            
            # 检查 Git
            result = subprocess.run(
                ["git", "--version"], 
                capture_output=True, 
                text=True
            )
            if result.returncode != 0:
                self.print_error("未找到 Git")
                return False
            
            # 克隆仓库
            comfyui_dir = self.workspace_dir / "Live2D-ComfyUI"
            comfyui_dir.mkdir(exist_ok=True)
            
            if not (comfyui_dir / "ComfyUI").exists():
                self.print_info("克隆 ComfyUI...")
                subprocess.run(
                    ["git", "clone", "https://github.com/comfyanonymous/ComfyUI.git"],
                    cwd=comfyui_dir,
                    check=True
                )
            
            # 创建虚拟环境
            venv_dir = comfyui_dir / "ComfyUI" / "venv"
            if not venv_dir.exists():
                self.print_info("创建虚拟环境...")
                subprocess.run(
                    ["python", "-m", "venv", "venv"],
                    cwd=comfyui_dir / "ComfyUI",
                    check=True
                )
            
            # 安装依赖
            self.print_info("安装依赖...")
            if platform.system() == "Windows":
                python_path = str(venv_dir / "Scripts" / "python.exe")
            else:
                python_path = str(venv_dir / "bin" / "python")
            
            subprocess.run(
                [python_path, "-m", "pip", "install", "--upgrade", "pip"],
                cwd=comfyui_dir / "ComfyUI",
                check=True
            )
            
            subprocess.run(
                [python_path, "-m", "pip", "install", "-r", "requirements.txt"],
                cwd=comfyui_dir / "ComfyUI",
                check=True
            )
            
            self.print_success("ComfyUI 安装完成！")
            return True
            
        except Exception as e:
            self.print_error(f"安装失败: {e}")
            return False
    
    def download_model(self, model_name: str = "AnythingV5") -> bool:
        """自动下载模型（简化版）"""
        self.print_info(f"正在下载 {model_name} 模型...")
        
        # 创建模型目录
        models_dir = self.workspace_dir / "Live2D-ComfyUI" / "ComfyUI" / "models" / "checkpoints"
        models_dir.mkdir(parents=True, exist_ok=True)
        
        # 提示用户手动下载（因为需要登录）
        self.print_warning("提示：CivitAI 模型需要登录账号下载")
        print()
        print("推荐模型下载链接:")
        print("  • AnythingV5: https://civitai.com/models/9409")
        print("  • CounterfeitV3: https://civitai.com/models/4468")
        print("  • PastelMix: https://civitai.com/models/39759")
        print()
        print(f"下载后请将模型文件放到: {models_dir}")
        print()
        
        # 等待用户确认
        input("下载完成后按 Enter 继续...")
        
        # 检查模型是否已下载
        model_files = list(models_dir.glob("*.safetensors")) + list(models_dir.glob("*.ckpt"))
        if model_files:
            self.print_success(f"找到 {len(model_files)} 个模型")
            return True
        else:
            self.print_warning("未找到模型文件")
            return False
    
    def start_comfyui(self) -> bool:
        """启动 ComfyUI"""
        self.print_info("启动 ComfyUI...")
        
        comfyui_dir = self.workspace_dir / "Live2D-ComfyUI" / "ComfyUI"
        
        try:
            if platform.system() == "Windows":
                python_path = str(comfyui_dir / "venv" / "Scripts" / "python.exe")
            else:
                python_path = str(comfyui_dir / "venv" / "bin" / "python")
            
            # 启动进程
            self.comfyui_process = subprocess.Popen(
                [python_path, "main.py", "--listen"],
                cwd=comfyui_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 等待启动
            self.print_info("等待 ComfyUI 启动...")
            time.sleep(10)
            
            # 检查是否启动成功
            if self.check_comfyui_running():
                self.print_success("ComfyUI 启动成功！")
                self.print_success("访问地址: http://127.0.0.1:8188")
                return True
            else:
                self.print_error("ComfyUI 启动失败")
                return False
                
        except Exception as e:
            self.print_error(f"启动失败: {e}")
            return False
    
    def generate_with_comfyui(self, prompt: str, negative_prompt: str) -> Optional[str]:
        """使用 ComfyUI 生成图片"""
        try:
            import requests
            
            # 构建提示
            comfy_prompt = {
                "1": {
                    "inputs": {
                        "seed": -1,
                        "steps": 30,
                        "cfg": 7.0,
                        "sampler_name": "euler",
                        "scheduler": "normal",
                        "positive": ["7", 0],
                        "negative": ["8", 0],
                        "latent_image": ["16", 0]
                    },
                    "class_type": "KSampler"
                },
                "7": {
                    "inputs": {"text": prompt, "clip": ["18", 1]},
                    "class_type": "CLIPTextEncode"
                },
                "8": {
                    "inputs": {"text": negative_prompt, "clip": ["18", 1]},
                    "class_type": "CLIPTextEncode"
                },
                "16": {
                    "inputs": {"width": 2048, "height": 2048, "batch_size": 1},
                    "class_type": "EmptyLatentImage"
                },
                "18": {
                    "inputs": {"ckpt_name": "auto"},
                    "class_type": "CheckpointLoaderSimple"
                },
                "9": {
                    "inputs": {"vae": ["10", 0], "samples": ["1", 0]},
                    "class_type": "VAEDecode"
                },
                "10": {"inputs": {"vae_name": "auto"}, "class_type": "VAELoader"},
                "11": {
                    "inputs": {"filename_prefix": "Live2D_Character", "images": ["9", 0]},
                    "class_type": "SaveImage"
                }
            }
            
            self.print_info("发送生成请求...")
            response = requests.post(
                "http://127.0.0.1:8188/prompt",
                json={"prompt": comfy_prompt},
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                self.print_success(f"请求已提交: {result.get('prompt_id')}")
                
                # 等待生成
                self.print_info("正在生成图片，请稍候...")
                time.sleep(30)
                
                # 获取结果
                history = requests.get("http://127.0.0.1:8188/history").json()
                for key in reversed(list(history.keys())):
                    outputs = history[key].get("outputs", {})
                    for node_output in outputs.values():
                        if "images" in node_output:
                            for img in node_output["images"]:
                                filename = img["filename"]
                                download_url = f"http://127.0.0.1:8188/view?filename={filename}&type=output"
                                img_response = requests.get(download_url)
                                
                                output_path = self.output_dir / filename
                                with open(output_path, 'wb') as f:
                                    f.write(img_response.content)
                                
                                self.print_success(f"图片已保存: {output_path}")
                                return str(output_path)
                
                self.print_error("未找到生成的图片")
                return None
            else:
                self.print_error(f"请求失败: {response.status_code}")
                return None
                
        except ImportError:
            self.print_error("需要安装 requests 库")
            return None
        except Exception as e:
            self.print_error(f"生成失败: {e}")
            return None
    
    def generate_with_seedream(self, prompt: str) -> Optional[str]:
        """使用 Seedream API 生成图片"""
        try:
            import requests
            import httpx
            
            api_key = os.getenv("ARK_API_KEY")
            url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            body = {
                "model": "doubao-seedream-5-0-260128",
                "prompt": prompt,
                "size": "2048x2048"
            }
            
            self.print_info("发送请求到 Seedream API...")
            response = requests.post(url, headers=headers, json=body, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                if "data" in result and len(result["data"]) > 0:
                    image_url = result["data"][0]["url"]
                    img_response = requests.get(image_url)
                    
                    output_path = self.output_dir / f"seedream_{int(time.time())}.png"
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    
                    self.print_success(f"图片已保存: {output_path}")
                    return str(output_path)
            
            self.print_error("生成失败")
            return None
            
        except Exception as e:
            self.print_error(f"生成失败: {e}")
            return None
    
    def guide_playground_ai(self):
        """引导用户使用 Playground AI"""
        print()
        print("=" * 50)
        print("🎨 Playground AI 使用指南")
        print("=" * 50)
        print()
        print("1. 访问: https://playground.com/")
        print("2. 注册免费账号")
        print("3. 使用以下提示词生成:")
        print()
        print("正向提示词:")
        print("anime girl, cute kawaii style, beautiful face,")
        print("big expressive eyes, long flowing pink hair,")
        print("perfect for Live2D rigging, clean layer separation,")
        print("isolated character on white background")
        print()
        print("负向提示词:")
        print("blurry, low quality, bad anatomy, multiple characters")
        print()
        print("4. 下载生成的图片")
        print("5. 回到这里继续")
        print("=" * 50)
        print()
        
        input("准备好后按 Enter 继续...")
        
        # 让用户输入图片路径
        while True:
            path = input("请输入图片路径: ").strip()
            if path and Path(path).exists():
                output_path = self.output_dir / Path(path).name
                import shutil
                shutil.copy(path, output_path)
                self.print_success(f"图片已复制到: {output_path}")
                return str(output_path)
            elif path.lower() == "skip":
                return None
            else:
                self.print_error("文件不存在，请重新输入（输入 skip 跳过）")
    
    def get_manual_input(self) -> Optional[str]:
        """手动输入图片路径"""
        print()
        self.print_info("请提供角色立绘图片")
        print("支持格式: PNG, JPG, JPEG")
        print()
        
        while True:
            path = input("图片路径: ").strip()
            if path and Path(path).exists():
                output_path = self.output_dir / Path(path).name
                import shutil
                shutil.copy(path, output_path)
                self.print_success(f"图片已复制到: {output_path}")
                return str(output_path)
            elif path.lower() == "skip":
                return None
            else:
                self.print_error("文件不存在，请重新输入（输入 skip 跳过）")
    
    def run(self):
        """主运行函数"""
        self.print_header()
        
        # 检测最佳方案
        self.selected_provider = self.detect_best_option()
        print()
        
        # 获取提示词
        self.print_info("请输入角色描述（留空使用默认）")
        character_desc = input("角色描述: ").strip()
        
        if not character_desc:
            character_desc = "anime girl, cute kawaii style, pink long hair, JK uniform"
        
        # 构建完整提示词
        positive_prompt = f"""
{character_desc},
beautiful face, big expressive eyes,
perfect for Live2D rigging, clean layer separation,
isolated character on white background,
sharp clean lines, vibrant colors, ultra detailed,
masterpiece, award-winning quality, professional artwork,
4K resolution, high quality render, anime art style
""".strip()
        
        negative_prompt = """
blurry, low quality, bad anatomy, bad hands,
multiple characters, complex background,
merged layers, overlapping parts, text, watermark
""".strip()
        
        # 根据选中的方案执行
        result_path = None
        
        if self.selected_provider == "comfyui_local":
            # 检查是否运行中
            if not self.check_comfyui_running():
                # 检查是否已安装
                if not self.check_comfyui():
                    # 自动安装
                    if self.install_comfyui():
                        self.download_model()
                    else:
                        self.print_warning("ComfyUI 安装失败，尝试其他方案")
                        self.selected_provider = "seedream_api" if self.check_seedream_api() else "playground_ai"
                else:
                    # 启动 ComfyUI
                    if self.download_model():
                        self.start_comfyui()
            
            if self.check_comfyui_running():
                result_path = self.generate_with_comfyui(positive_prompt, negative_prompt)
        
        if result_path is None and self.selected_provider == "seedream_api":
            result_path = self.generate_with_seedream(positive_prompt)
        
        if result_path is None:
            # 回退到在线方案
            self.print_warning("本地方案不可用，使用在线方案")
            result_path = self.guide_playground_ai()
        
        if result_path is None:
            # 最后回退到手动输入
            result_path = self.get_manual_input()
        
        # 后续处理
        if result_path:
            print()
            print("=" * 50)
            self.print_success("图像生成完成！")
            print("=" * 50)
            print()
            print(f"图片位置: {result_path}")
            print()
            print("下一步:")
            print("  1. 查看生成的图片")
            print("  2. 进行 PSD 分层规划")
            print("  3. 使用 Live2D Master Agent 进行质量检查")
            print()
            
            # 自动生成角色设定文档
            self.generate_concept_doc(result_path, character_desc)
    
    def generate_concept_doc(self, image_path: str, character_desc: str):
        """生成角色设定文档"""
        doc_content = f"""# 角色设定文档

## 基本信息

| 项目 | 内容 |
|------|------|
| 描述 | {character_desc} |
| 图片 | {Path(image_path).name} |
| 生成时间 | {time.strftime('%Y-%m-%d %H:%M:%S')} |
| 生成方式 | {self._get_option_name(self.selected_provider)} |

## 分层规划建议

### 头部图层
- hair_front_01 - 前发
- hair_back_01 - 后发
- face_base - 脸部基础
- eye_l_white / eye_r_white - 眼白
- eye_l_iris / eye_r_iris - 虹膜
- mouth_base - 嘴巴基础

### 身体图层
- body_front - 身体前部
- body_back - 身体后部
- skirt_01 - 裙子
- arm_front_l / arm_front_r - 手臂

## 后续步骤

1. 将图片导入 Photoshop
2. 按照上述分层进行切割
3. 使用 Live2D Master Agent 进行质量检查
4. 导入 Cubism 进行绑定
"""
        
        doc_path = self.output_dir / "character_concept.md"
        doc_path.write_text(doc_content, encoding='utf-8')
        self.print_success(f"角色设定文档已生成: {doc_path}")


def main():
    """主函数"""
    generator = AutoImageGenerator()
    generator.run()


if __name__ == "__main__":
    main()
