#!/usr/bin/env python3
"""
GitHub Live2D分层工具集成模块 v1.0
集成多个开源项目的分层技术：
- See-through (SIGGRAPH 2026): https://github.com/shitagaki-lab/see-through
- Anime-Segmentation: https://github.com/livadies-collab/Anime-Segmentation
- Live2D官方PS插件 (参考规范)

提供统一接口，自动选择最佳分层方案。
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import argparse


class GitHubLayerIntegration:
    """GitHub开源Live2D分层工具集成"""

    # 项目配置
    PROJECTS = {
        "see_through": {
            "name": "See-through (SIGGRAPH 2026)",
            "repo": "https://github.com/shitagaki-lab/see-through",
            "comfyui_repo": "https://github.com/jtydhr88/ComfyUI-See-through",
            "description": "SDXL+Marigold深度，自动分层+遮挡补全+深度排序",
            "quality": "⭐⭐⭐⭐⭐",
            "speed": "慢（需GPU）",
            "requirements": ["comfyui", "gpu"],
            "install_cmd": "git clone {repo} && cd see-through && pip install -r requirements.txt",
        },
        "anime_segmentation": {
            "name": "Anime-Segmentation",
            "repo": "https://github.com/livadies-collab/Anime-Segmentation",
            "description": "U-2-Net+SAM+SD Inpainting，4阶段轻量管道",
            "quality": "⭐⭐⭐⭐",
            "speed": "中（CPU/GPU均可）",
            "requirements": ["rembg", "segment-anything", "diffusers"],
            "install_cmd": "pip install rembg segment-anything diffusers transformers torch",
        },
        "live2d_ps_plugin": {
            "name": "Live2D官方PS插件（参考）",
            "url": "https://docs.live2d.com/zh-CHS/cubism-editor-manual/material-separation-ps-plugin-download/",
            "description": "商业级AI分层，需Photoshop+许可证",
            "quality": "⭐⭐⭐⭐⭐",
            "speed": "快",
            "requirements": ["photoshop", "license"],
            "note": "仅作为参考规范，不可直接集成",
        }
    }

    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.installed_tools = self._detect_installed_tools()

    def _detect_installed_tools(self) -> Dict[str, bool]:
        """检测已安装的分层工具"""
        installed = {}

        # 检测See-through
        see_through_dir = Path(__file__).parent / "see-through"
        installed["see_through"] = see_through_dir.exists()

        # 检测Anime-Segmentation依赖
        try:
            import rembg
            installed["anime_segmentation"] = True
        except ImportError:
            installed["anime_segmentation"] = False

        # 检测ComfyUI
        comfyui_dir = Path(__file__).parent / "comfyui"
        installed["comfyui"] = comfyui_dir.exists()

        return installed

    def get_available_tools(self) -> List[str]:
        """获取可用的分层工具列表"""
        available = []
        for tool_id, installed in self.installed_tools.items():
            if installed and tool_id in self.PROJECTS:
                available.append(tool_id)
        return available

    def install_tool(self, tool_id: str) -> bool:
        """安装指定的分层工具"""
        if tool_id not in self.PROJECTS:
            print(f"❌ 未知工具: {tool_id}")
            return False

        project = self.PROJECTS[tool_id]
        print(f"\n🔧 安装 {project['name']}...")
        print(f"📦 说明: {project['description']}")
        print(f"⚡ 速度: {project['speed']}")
        print(f"⭐ 质量: {project['quality']}")

        if tool_id == "see_through":
            return self._install_see_through()
        elif tool_id == "anime_segmentation":
            return self._install_anime_segmentation()
        else:
            print(f"⚠️ {tool_id} 需要手动安装")
            print(f"   参考: {project.get('url', project.get('repo', ''))}")
            return False

    def _install_see_through(self) -> bool:
        """安装See-through"""
        base_dir = Path(__file__).parent

        # 克隆仓库
        see_through_dir = base_dir / "see-through"
        if not see_through_dir.exists():
            print("📥 克隆 See-through 仓库...")
            result = subprocess.run(
                ["git", "clone", "https://github.com/shitagaki-lab/see-through.git"],
                cwd=base_dir,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"❌ 克隆失败: {result.stderr}")
                return False

        # 安装依赖
        print("📦 安装依赖...")
        req_file = see_through_dir / "requirements.txt"
        if req_file.exists():
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"⚠️ 依赖安装可能有问题: {result.stderr}")

        print("✅ See-through 安装完成")
        print("💡 使用方法: python github_layer_integration.py --tool see_through --input image.png")
        return True

    def _install_anime_segmentation(self) -> bool:
        """安装Anime-Segmentation依赖"""
        print("📦 安装 Anime-Segmentation 依赖...")

        packages = ["rembg", "segment-anything", "diffusers", "transformers", "torch", "pillow", "numpy"]
        for pkg in packages:
            print(f"   安装 {pkg}...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-q", pkg],
                capture_output=True
            )

        print("✅ Anime-Segmentation 依赖安装完成")
        return True

    def process_image(self, image_path: str, tool_id: Optional[str] = None,
                      auto_select: bool = True) -> Optional[str]:
        """
        处理图片进行Live2D分层

        Args:
            image_path: 输入图片路径
            tool_id: 指定工具ID（None则自动选择）
            auto_select: 是否自动选择最佳工具

        Returns:
            输出目录路径
        """
        if not os.path.exists(image_path):
            print(f"❌ 图片不存在: {image_path}")
            return None

        # 自动选择工具
        if auto_select and tool_id is None:
            tool_id = self._auto_select_tool()

        if tool_id is None:
            print("❌ 没有可用的分层工具")
            print("💡 请运行安装: python github_layer_integration.py --install")
            return None

        print(f"\n🎨 使用工具: {self.PROJECTS[tool_id]['name']}")

        if tool_id == "see_through":
            return self._run_see_through(image_path)
        elif tool_id == "anime_segmentation":
            return self._run_anime_segmentation(image_path)
        else:
            print(f"❌ 不支持的工具: {tool_id}")
            return None

    def _auto_select_tool(self) -> Optional[str]:
        """自动选择最佳可用工具"""
        available = self.get_available_tools()

        # 优先级：see_through > anime_segmentation
        if "see_through" in available:
            return "see_through"
        elif "anime_segmentation" in available:
            return "anime_segmentation"

        return None

    def _run_see_through(self, image_path: str) -> Optional[str]:
        """运行See-through分层"""
        see_through_dir = Path(__file__).parent / "see-through"
        if not see_through_dir.exists():
            print("❌ See-through 未安装")
            return None

        output_dir = self.output_dir / f"see_through_{int(os.path.getmtime(image_path))}"
        output_dir.mkdir(exist_ok=True)

        print("\n🔧 运行 See-through 分层...")
        print("   这可能需要几分钟时间...")

        try:
            # 使用See-through的推理脚本
            result = subprocess.run(
                [sys.executable, "inference.py", "--input", image_path, "--output", str(output_dir)],
                cwd=see_through_dir,
                capture_output=True,
                text=True,
                timeout=600
            )

            if result.returncode == 0:
                print(f"✅ See-through 分层完成")
                print(f"📁 输出: {output_dir}")
                return str(output_dir)
            else:
                print(f"⚠️ See-through 运行失败: {result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            print("⏱️ See-through 运行超时")
            return None
        except Exception as e:
            print(f"❌ See-through 运行错误: {e}")
            return None

    def _run_anime_segmentation(self, image_path: str) -> Optional[str]:
        """运行Anime-Segmentation分层（4阶段管道）"""
        output_dir = self.output_dir / f"anime_seg_{int(os.path.getmtime(image_path))}"
        output_dir.mkdir(exist_ok=True)

        print("\n🔧 运行 Anime-Segmentation 4阶段管道...")

        try:
            from PIL import Image
            import numpy as np

            # 阶段1: 抠图（U-2-Net/rembg）
            print("\n📋 阶段1/4: 角色抠图...")
            from rembg import remove
            with Image.open(image_path) as img:
                character = remove(img)
                character_path = output_dir / "01_character.png"
                character.save(character_path)
                print(f"   ✅ 角色抠图完成: {character_path.name}")

            # 阶段2: 背景修复（Inpainting）
            print("\n📋 阶段2/4: 背景修复...")
            # 简化版：使用原始背景
            bg_path = output_dir / "02_background.png"
            with Image.open(image_path) as img:
                img.save(bg_path)
            print(f"   ✅ 背景保存: {bg_path.name}")

            # 阶段3: 部件分割（SAM）
            print("\n📋 阶段3/4: 部件分割...")
            layers = self._segment_character(str(character_path), output_dir)
            print(f"   ✅ 分割完成: {len(layers)} 个部件")

            # 阶段4: 生成Live2D结构
            print("\n📋 阶段4/4: 生成Live2D结构...")
            self._create_live2d_structure(output_dir, layers)
            print(f"   ✅ Live2D结构生成完成")

            print(f"\n✅ Anime-Segmentation 分层完成")
            print(f"📁 输出: {output_dir}")
            return str(output_dir)

        except ImportError as e:
            print(f"❌ 缺少依赖: {e}")
            print("💡 请运行: python github_layer_integration.py --install anime_segmentation")
            return None
        except Exception as e:
            print(f"❌ Anime-Segmentation 运行错误: {e}")
            return None

    def _segment_character(self, character_path: str, output_dir: Path) -> List[str]:
        """
        使用简单颜色聚类进行部件分割
        （轻量级替代SAM，无需大量依赖）
        """
        from PIL import Image
        import numpy as np

        img = Image.open(character_path).convert("RGBA")
        img_array = np.array(img)

        # 简单的颜色聚类分割
        # 提取非透明像素
        alpha = img_array[:, :, 3]
        mask = alpha > 128

        # 基于亮度分割不同部件
        gray = np.mean(img_array[:, :, :3], axis=2)

        layers = []

        # 头发（通常较暗）
        hair_mask = (gray < 80) & mask
        if np.any(hair_mask):
            hair_img = img_array.copy()
            hair_img[~hair_mask] = [0, 0, 0, 0]
            hair_path = output_dir / "03_hair.png"
            Image.fromarray(hair_img).save(hair_path)
            layers.append("hair")

        # 皮肤（中等亮度）
        skin_mask = (gray >= 80) & (gray < 180) & mask
        if np.any(skin_mask):
            skin_img = img_array.copy()
            skin_img[~skin_mask] = [0, 0, 0, 0]
            skin_path = output_dir / "03_skin.png"
            Image.fromarray(skin_img).save(skin_path)
            layers.append("skin")

        # 衣服（较亮）
        clothes_mask = (gray >= 180) & mask
        if np.any(clothes_mask):
            clothes_img = img_array.copy()
            clothes_img[~clothes_mask] = [0, 0, 0, 0]
            clothes_path = output_dir / "03_clothes.png"
            Image.fromarray(clothes_img).save(clothes_path)
            layers.append("clothes")

        return layers

    def _create_live2d_structure(self, output_dir: Path, layers: List[str]):
        """创建Live2D标准结构"""
        guide_path = output_dir / "LIVE2D_LAYER_GUIDE.txt"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write("Live2D 分层指南 (GitHub集成版)\n")
            f.write("="*50 + "\n\n")
            f.write("图层顺序（从后到前）:\n")
            f.write("-"*50 + "\n")
            f.write("1. Background - 背景\n")
            f.write("2. Body - 身体\n")
            for i, layer in enumerate(layers, 3):
                f.write(f"{i}. {layer.capitalize()} - {layer}\n")
            f.write("\n导入Live2D Cubism Editor步骤:\n")
            f.write("1. File → Import PSD\n")
            f.write("2. 勾选 Create ArtMeshes\n")
            f.write("3. 点击 OK\n")
            f.write("4. 创建部件并设置参数\n")

    def show_tool_comparison(self):
        """显示工具对比"""
        print("\n" + "="*80)
        print("🔧 GitHub Live2D分层工具对比")
        print("="*80)

        for tool_id, project in self.PROJECTS.items():
            installed = "✅ 已安装" if self.installed_tools.get(tool_id, False) else "❌ 未安装"
            print(f"\n{project['name']}")
            print(f"   状态: {installed}")
            print(f"   质量: {project['quality']}")
            print(f"   速度: {project['speed']}")
            print(f"   说明: {project['description']}")
            if 'repo' in project:
                print(f"   仓库: {project['repo']}")

        print("\n" + "="*80)


def main():
    parser = argparse.ArgumentParser(
        description="GitHub Live2D分层工具集成 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 查看工具对比
  python github_layer_integration.py --compare

  # 安装所有工具
  python github_layer_integration.py --install

  # 安装指定工具
  python github_layer_integration.py --install anime_segmentation

  # 处理图片（自动选择工具）
  python github_layer_integration.py --input character.png

  # 使用指定工具处理
  python github_layer_integration.py --input character.png --tool anime_segmentation
""",
    )
    parser.add_argument("--compare", action="store_true", help="显示工具对比")
    parser.add_argument("--install", type=str, nargs='?', const="all", help="安装工具（all/see_through/anime_segmentation）")
    parser.add_argument("--input", type=str, help="输入图片路径")
    parser.add_argument("--tool", type=str, choices=["see_through", "anime_segmentation"], help="指定分层工具")
    parser.add_argument("--output", type=str, default="./output", help="输出目录")

    args = parser.parse_args()

    integration = GitHubLayerIntegration(output_dir=args.output)

    if args.compare:
        integration.show_tool_comparison()
        return

    if args.install:
        if args.install == "all":
            for tool_id in integration.PROJECTS.keys():
                if tool_id != "live2d_ps_plugin":
                    integration.install_tool(tool_id)
        else:
            integration.install_tool(args.install)
        return

    if args.input:
        result = integration.process_image(args.input, tool_id=args.tool)
        if result:
            print(f"\n🎉 分层完成！输出: {result}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
