#!/usr/bin/env python3
"""
Live2D Master Agent - 云端资源管理器 v1.0
提供一键下载所有依赖、模型、工具的功能
支持国内镜像加速下载
"""

import os
import sys
import time
import hashlib
import json
import shutil
import zipfile
import tarfile
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class ResourceType(Enum):
    """资源类型"""
    PYTHON_PACKAGE = "python_package"
    HUGGINGFACE_MODEL = "huggingface_model"
    REMBG_MODEL = "rembg_model"
    GITHUB_REPO = "github_repo"
    PRETRAINED_WEIGHTS = "pretrained_weights"
    TOOL_BINARIES = "tool_binaries"
    CONFIG_FILE = "config_file"


class DownloadStatus(Enum):
    """下载状态"""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    VERIFYING = "verifying"
    EXTRACTING = "extracting"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Resource:
    """资源定义"""
    id: str
    name: str
    description: str
    resource_type: ResourceType
    size_mb: float
    required: bool = False
    priority: int = 100

    # 下载信息
    url: str = ""
    alternative_urls: List[str] = field(default_factory=list)
    checksum: str = ""
    checksum_algorithm: str = "sha256"

    # 安装信息
    install_path: str = ""
    install_script: str = ""
    post_install_script: str = ""
    dependencies: List[str] = field(default_factory=list)

    # 元数据
    version: str = "latest"
    tags: List[str] = field(default_factory=list)
    notes: str = ""


class OSType(Enum):
    """操作系统类型"""
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    UNKNOWN = "unknown"


class CloudResourceManager:
    """云端资源管理器"""

    # 系统依赖命令（按操作系统分类）
    SYSTEM_DEPENDENCIES = {
        OSType.LINUX: {
            "description": "Linux 系统依赖",
            "package_manager": "apt-get",
            "install_command": "sudo apt-get update && sudo apt-get install -y",
            "packages": [
                "libsdl2-dev",
                "libsdl2-image-dev",
                "libsdl2-mixer-dev",
                "libsdl2-ttf-dev",
                "libjpeg-dev",
                "zlib1g-dev",
                "portaudio19-dev",
                "python3-dev",
                "python3-pip",
            ],
        },
        OSType.MACOS: {
            "description": "macOS 系统依赖",
            "package_manager": "brew",
            "install_command": "brew install",
            "packages": [
                "sdl2",
                "sdl2_image",
                "sdl2_mixer",
                "sdl2_ttf",
                "portaudio",
            ],
        },
        OSType.WINDOWS: {
            "description": "Windows 系统依赖",
            "package_manager": "choco",
            "install_command": "choco install",
            "packages": [
                "python",
                "git",
            ],
        },
    }

    # 资源清单
    RESOURCES = {
        # ====== Python 依赖包 ======
        "pillow": Resource(
            id="pillow",
            name="Pillow",
            description="Python 图像处理库",
            resource_type=ResourceType.PYTHON_PACKAGE,
            size_mb=45,
            required=True,
            priority=1,
            install_script="pip install Pillow>=10.0.0",
        ),
        "numpy": Resource(
            id="numpy",
            name="NumPy",
            description="数值计算库",
            resource_type=ResourceType.PYTHON_PACKAGE,
            size_mb=25,
            required=True,
            priority=1,
            install_script="pip install numpy>=1.24.0",
        ),
        "requests": Resource(
            id="requests",
            name="Requests",
            description="HTTP 请求库",
            resource_type=ResourceType.PYTHON_PACKAGE,
            size_mb=2,
            required=True,
            priority=1,
            install_script="pip install requests>=2.31.0",
        ),
        "urllib3": Resource(
            id="urllib3",
            name="urllib3",
            description="HTTP 请求库依赖",
            resource_type=ResourceType.PYTHON_PACKAGE,
            size_mb=3,
            required=True,
            priority=1,
            install_script="pip install urllib3>=2.0.0",
        ),
        "opencv_python": Resource(
            id="opencv_python",
            name="OpenCV-Python",
            description="计算机视觉库（用于边缘检测）",
            resource_type=ResourceType.PYTHON_PACKAGE,
            size_mb=70,
            required=False,
            priority=3,
            install_script="pip install opencv-python>=4.8.0",
        ),
        "psd_tools": Resource(
            id="psd_tools",
            name="PSD Tools",
            description="PSD 文件处理库",
            resource_type=ResourceType.PYTHON_PACKAGE,
            size_mb=10,
            required=False,
            priority=2,
            install_script="pip install psd-tools>=1.9.0",
        ),
        "scipy": Resource(
            id="scipy",
            name="SciPy",
            description="科学计算库",
            resource_type=ResourceType.PYTHON_PACKAGE,
            size_mb=60,
            required=False,
            priority=2,
            install_script="pip install scipy>=1.10.0",
        ),
        "scikit_learn": Resource(
            id="scikit_learn",
            name="Scikit-Learn",
            description="机器学习库（用于分层）",
            resource_type=ResourceType.PYTHON_PACKAGE,
            size_mb=30,
            required=False,
            priority=2,
            install_script="pip install scikit-learn>=1.3.0",
        ),
        "rembg": Resource(
            id="rembg",
            name="RemBG",
            description="AI 背景去除工具",
            resource_type=ResourceType.PYTHON_PACKAGE,
            size_mb=15,
            required=False,
            priority=3,
            install_script="pip install rembg[cpu]>=2.0.0",
        ),
        "onnxruntime": Resource(
            id="onnxruntime",
            name="ONNX Runtime",
            description="ONNX 运行时（rembg 依赖）",
            resource_type=ResourceType.PYTHON_PACKAGE,
            size_mb=100,
            required=False,
            priority=3,
            install_script="pip install onnxruntime>=1.14.0",
        ),
        "diffusers": Resource(
            id="diffusers",
            name="Diffusers",
            description="Stable Diffusion 库（本地生成用）",
            resource_type=ResourceType.PYTHON_PACKAGE,
            size_mb=20,
            required=False,
            priority=3,
            install_script="pip install diffusers transformers torch accelerate",
        ),
        "huggingface_hub": Resource(
            id="huggingface_hub",
            name="Hugging Face Hub",
            description="Hugging Face 模型下载库",
            resource_type=ResourceType.PYTHON_PACKAGE,
            size_mb=8,
            required=False,
            priority=2,
            install_script="pip install huggingface-hub>=0.17.0",
        ),

        # ====== rembg 模型 ======
        "rembg_u2net": Resource(
            id="rembg_u2net",
            name="RemBG U2Net",
            description="rembg 通用人物分割模型",
            resource_type=ResourceType.REMBG_MODEL,
            size_mb=176,
            required=False,
            priority=4,
            url="https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx",
            install_path="~/.u2net/u2net.onnx",
        ),
        "rembg_u2netp": Resource(
            id="rembg_u2netp",
            name="RemBG U2NetP",
            description="rembg 轻量版分割模型",
            resource_type=ResourceType.REMBG_MODEL,
            size_mb=4.5,
            required=False,
            priority=4,
            url="https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2netp.onnx",
            install_path="~/.u2net/u2netp.onnx",
        ),
        "rembg_u2net_human_seg": Resource(
            id="rembg_u2net_human_seg",
            name="RemBG U2Net Human Seg",
            description="rembg 人物专用分割模型",
            resource_type=ResourceType.REMBG_MODEL,
            size_mb=176,
            required=False,
            priority=4,
            url="https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_human_seg.onnx",
            install_path="~/.u2net/u2net_human_seg.onnx",
        ),

        # ====== 轻量预训练模型（可选） ======
        "segment_anything_vit_b": Resource(
            id="segment_anything_vit_b",
            name="SAM ViT-B",
            description="Meta SAM 轻量模型（用于分层）",
            resource_type=ResourceType.PRETRAINED_WEIGHTS,
            size_mb=375,
            required=False,
            priority=5,
            url="https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth",
            install_path="./models/sam_vit_b_01ec64.pth",
            notes="如果使用 Anime-Segmentation 工具需要此模型",
        ),
    }

    # 国内镜像源配置
    MIRRORS = {
        "pypi": [
            "https://pypi.tuna.tsinghua.edu.cn/simple",
            "https://mirrors.aliyun.com/pypi/simple/",
            "https://pypi.mirrors.ustc.edu.cn/simple/",
            "https://pypi.douban.com/simple/",
        ],
        "huggingface": [
            "https://hf-mirror.com",
            "https://hf-mirror.tuna.tsinghua.edu.cn",
        ],
        "github": [
            "https://github.com",
            "https://ghproxy.com/https://github.com",
            "https://gh.api.99988866.xyz/https://github.com",
        ],
    }

    # 下载状态跟踪
    download_status: Dict[str, DownloadStatus] = field(default_factory=dict)

    @staticmethod
    def detect_os() -> OSType:
        """检测当前操作系统类型"""
        sys_platform = sys.platform.lower()
        if sys_platform.startswith("win"):
            return OSType.WINDOWS
        elif sys_platform.startswith("darwin"):
            return OSType.MACOS
        elif sys_platform.startswith("linux"):
            return OSType.LINUX
        else:
            return OSType.UNKNOWN

    @staticmethod
    def get_os_name(os_type: OSType) -> str:
        """获取操作系统名称"""
        os_names = {
            OSType.WINDOWS: "Windows",
            OSType.MACOS: "macOS",
            OSType.LINUX: "Linux",
            OSType.UNKNOWN: "未知系统",
        }
        return os_names.get(os_type, "未知系统")

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.cache_dir = self.base_dir / ".cache" / "cloud_resources"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # 状态文件
        self.status_file = self.cache_dir / "download_status.json"
        self._load_status()

    def install_system_dependencies(self, os_type: OSType = None) -> bool:
        """安装系统级依赖"""
        if os_type is None:
            os_type = self.detect_os()

        if os_type == OSType.UNKNOWN:
            print("⚠️  无法识别操作系统，跳过系统依赖安装")
            return False

        print(f"\n{'=' * 100}")
        print(f"🔧 安装 {self.get_os_name(os_type)} 系统依赖")
        print(f"{'=' * 100}")

        deps = self.SYSTEM_DEPENDENCIES.get(os_type)
        if not deps:
            print(f"⚠️  没有为 {self.get_os_name(os_type)} 配置系统依赖")
            return False

        print(f"\n📋 需要安装的系统包:")
        for pkg in deps["packages"]:
            print(f"   • {pkg}")

        # 检查包管理器是否可用
        package_manager = deps["package_manager"]
        try:
            import subprocess
            result = subprocess.run(
                ["which" if os_type != OSType.WINDOWS else "where", package_manager],
                capture_output=True,
                text=True,
                shell=os_type == OSType.WINDOWS,
            )
            if result.returncode != 0:
                print(f"\n⚠️  未找到包管理器 {package_manager}")
                print(f"   请手动安装 {', '.join(deps['packages'])}")
                return False

            print(f"\n✅ 找到包管理器: {package_manager}")

        except Exception as e:
            print(f"\n⚠️  无法检查包管理器: {e}")
            return False

        # 执行安装
        print(f"\n🚀 开始安装系统依赖...")
        install_cmd = f"{deps['install_command']} {' '.join(deps['packages'])}"

        try:
            import subprocess
            result = subprocess.run(
                install_cmd,
                shell=True,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print("✅ 系统依赖安装成功！")
                return True
            else:
                print(f"❌ 安装失败:")
                print(f"   STDOUT: {result.stdout[:500]}")
                print(f"   STDERR: {result.stderr[:500]}")
                print(f"\n💡 请手动执行以下命令:")
                print(f"   {install_cmd}")
                return False

        except Exception as e:
            print(f"❌ 安装错误: {e}")
            print(f"\n💡 请手动执行以下命令:")
            print(f"   {install_cmd}")
            return False

    def _load_status(self):
        """加载下载状态"""
        if self.status_file.exists():
            try:
                with open(self.status_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.download_status = {
                        k: DownloadStatus(v) for k, v in data.items()
                    }
            except:
                self.download_status = {}
        else:
            self.download_status = {}

    def _save_status(self):
        """保存下载状态"""
        data = {k: v.value for k, v in self.download_status.items()}
        with open(self.status_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def list_resources(self, category: Optional[str] = None) -> List[Resource]:
        """列出所有资源"""
        resources = list(self.RESOURCES.values())
        
        if category:
            type_map = {
                "python": ResourceType.PYTHON_PACKAGE,
                "models": ResourceType.PRETRAINED_WEIGHTS,
                "rembg": ResourceType.REMBG_MODEL,
                "all": None,
            }
            filter_type = type_map.get(category.lower())
            if filter_type:
                resources = [r for r in resources if r.resource_type == filter_type]
        
        return sorted(resources, key=lambda r: (r.required, r.priority))

    def print_resource_list(self):
        """打印资源列表"""
        print("=" * 100)
        print("📦 Live2D Master Agent - 资源清单")
        print("=" * 100)

        resources = self.list_resources()
        
        # 按类型分组
        groups: Dict[ResourceType, List[Resource]] = {}
        for r in resources:
            if r.resource_type not in groups:
                groups[r.resource_type] = []
            groups[r.resource_type].append(r)
        
        # 打印
        type_names = {
            ResourceType.PYTHON_PACKAGE: "🐍 Python 依赖包",
            ResourceType.REMBG_MODEL: "🧠 rembg AI 模型",
            ResourceType.PRETRAINED_WEIGHTS: "🎨 预训练模型",
        }

        for res_type, res_list in groups.items():
            print(f"\n{type_names.get(res_type, res_type.value)}")
            print("-" * 100)
            
            for r in res_list:
                req_icon = "✅" if r.required else "☑️"
                status = self.download_status.get(r.id, DownloadStatus.PENDING)
                status_icon = {
                    DownloadStatus.COMPLETED: "✓",
                    DownloadStatus.SKIPPED: "-",
                    DownloadStatus.PENDING: " ",
                }.get(status, "?")
                
                print(f"  [{status_icon}] {req_icon} {r.name:<30} {r.size_mb:>6.1f}MB  {r.description}")

    def download_python_package(self, resource: Resource) -> bool:
        """下载并安装 Python 包"""
        print(f"\n📦 安装 Python 包: {resource.name}")
        print(f"   描述: {resource.description}")

        # 尝试使用国内镜像
        for mirror in self.MIRRORS["pypi"]:
            print(f"   尝试镜像: {mirror}")
            try:
                import subprocess
                cmd = resource.install_script.replace("pip install", f"pip install -i {mirror}")
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"   ✓ {resource.name} 安装成功！")
                    return True
                else:
                    print(f"   ✗ 安装失败，尝试下一个镜像...")
            except Exception as e:
                print(f"   ✗ 错误: {e}")

        # 最后尝试官方源
        print("   尝试官方源...")
        try:
            import subprocess
            subprocess.run(resource.install_script, shell=True, check=True)
            print(f"   ✓ {resource.name} 安装成功！")
            return True
        except Exception as e:
            print(f"   ✗ 安装失败: {e}")
            return False

    def download_file(self, resource: Resource) -> Optional[str]:
        """下载文件到本地"""
        print(f"\n📥 下载: {resource.name}")
        print(f"   大小: {resource.size_mb:.1f}MB")
        print(f"   描述: {resource.description}")

        urls_to_try = [resource.url] + resource.alternative_urls
        
        for url in urls_to_try:
            if not url:
                continue
            print(f"   尝试: {url[:60]}...")
            
            try:
                import requests
                from urllib.parse import urlparse
                
                # GitHub 镜像处理
                parsed = urlparse(url)
                if parsed.netloc == "github.com":
                    for mirror in self.MIRRORS["github"]:
                        if mirror != "https://github.com":
                            mirrored_url = url.replace("https://github.com", mirror)
                            print(f"   尝试镜像: {mirrored_url[:60]}...")
                            if self._try_download(mirrored_url, resource):
                                return str(self._get_local_path(resource))

                # 直接下载
                if self._try_download(url, resource):
                    return str(self._get_local_path(resource))
                    
            except Exception as e:
                print(f"   ✗ 下载失败: {e}")
                continue

        return None

    def _try_download(self, url: str, resource: Resource) -> bool:
        """尝试下载单个 URL"""
        import requests
        local_path = self._get_local_path(resource)
        local_path.parent.mkdir(parents=True, exist_ok=True)

        temp_path = local_path.with_suffix(local_path.suffix + ".download")

        try:
            response = requests.get(url, stream=True, timeout=300)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            start_time = time.time()

            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # 显示进度
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            speed = downloaded / (time.time() - start_time + 0.001)
                            print(f"\r   进度: {percent:5.1f}% ({downloaded/1024/1024:.1f}MB) - {speed/1024/1024:.1f}MB/s", end="")

            print()
            
            # 验证校验和
            if resource.checksum:
                print("   验证文件完整性...")
                if not self._verify_checksum(temp_path, resource.checksum, resource.checksum_algorithm):
                    print("   ✗ 校验失败！")
                    return False

            # 移动到最终位置
            shutil.move(str(temp_path), str(local_path))
            print(f"   ✓ 下载完成: {local_path.name}")
            return True
            
        except Exception as e:
            if temp_path.exists():
                temp_path.unlink()
            raise e

    def _get_local_path(self, resource: Resource) -> Path:
        """获取资源的本地路径"""
        if resource.install_path:
            path = Path(resource.install_path).expanduser()
            if not path.is_absolute():
                path = self.base_dir / path
            return path
        else:
            return self.cache_dir / resource.id / Path(resource.url).name

    def _verify_checksum(self, file_path: Path, expected_checksum: str, algorithm: str) -> bool:
        """验证文件校验和"""
        if not expected_checksum:
            return True

        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hash_obj.update(chunk)
        actual_checksum = hash_obj.hexdigest()
        return actual_checksum.lower() == expected_checksum.lower()

    def install_resource(self, resource: Resource) -> bool:
        """安装单个资源"""
        print(f"\n{'=' * 100}")
        print(f"🚀 处理资源: {resource.name}")
        print(f"{'=' * 100}")

        self.download_status[resource.id] = DownloadStatus.DOWNLOADING
        self._save_status()

        try:
            if resource.resource_type == ResourceType.PYTHON_PACKAGE:
                success = self.download_python_package(resource)
            elif resource.resource_type in [ResourceType.REMBG_MODEL, ResourceType.PRETRAINED_WEIGHTS]:
                success = self.download_file(resource) is not None
            else:
                print(f"   ⚠️  暂不支持的资源类型: {resource.resource_type}")
                success = False

            if success:
                self.download_status[resource.id] = DownloadStatus.COMPLETED
                if resource.post_install_script:
                    print(f"   📝 执行后安装脚本...")
                    import subprocess
                    subprocess.run(resource.post_install_script, shell=True)
            else:
                self.download_status[resource.id] = DownloadStatus.FAILED

            self._save_status()
            return success
            
        except Exception as e:
            print(f"   ✗ 错误: {e}")
            self.download_status[resource.id] = DownloadStatus.FAILED
            self._save_status()
            return False

    def install_batch(self, resource_ids: Optional[List[str]] = None, category: Optional[str] = None):
        """批量安装资源"""
        if resource_ids:
            resources = [self.RESOURCES[id] for id in resource_ids if id in self.RESOURCES]
        else:
            resources = self.list_resources(category)
        
        # 只安装 required 或用户选择的
        resources = [r for r in resources if r.required or (resource_ids and r.id in resource_ids)]
        
        if not resources:
            print("⚠️  没有需要安装的资源")
            return

        print(f"\n🎯 开始安装 {len(resources)} 个资源...")
        
        success_count = 0
        for resource in resources:
            if self.install_resource(resource):
                success_count += 1
        
        print(f"\n{'=' * 100}")
        print(f"📊 安装完成: {success_count}/{len(resources)} 成功")
        print(f"{'=' * 100}")

    def install_all(self):
        """安装所有 required 资源"""
        self.install_batch([r.id for r in self.RESOURCES.values() if r.required])

    def quick_start(self):
        """快速开始 - 最小安装"""
        print("🚀 Live2D Master Agent - 快速开始")
        print("\n本选项将安装以下核心资源：")
        print("  - Python 基础依赖（Pillow, NumPy, Requests）")
        print("  - PSD 处理库（可选）")
        print("  - 分层工具库（SciPy, Scikit-Learn, RemBG）")
        print("\n使用商汤 SenseNova 云端生成，无需下载大模型！")
        print("\n继续？(y/n): ", end="")
        
        try:
            choice = input().strip().lower()
            if choice != "y":
                print("已取消")
                return
            
            # 安装核心依赖
            self.install_batch(["pillow", "numpy", "requests"])
            
            print("\n💡 建议安装的增强功能：")
            print("  1) PSD 文件处理 (psd_tools)")
            print("  2) AI 分层增强 (scikit_learn, scipy, rembg)")
            print("  3) 全部安装")
            print("\n选择 (1/2/3/n): ", end="")
            
            choice = input().strip()
            if choice == "1":
                self.install_batch(["psd_tools"])
            elif choice == "2":
                self.install_batch(["psd_tools", "scipy", "scikit_learn", "rembg"])
                self.install_batch(["rembg_u2netp"])
            elif choice == "3":
                self.install_batch(["psd_tools", "scipy", "scikit_learn", "rembg"])
                self.install_batch(["rembg_u2netp"])
            
            print("\n✅ 快速开始安装完成！")
            print("\n📝 下一步：")
            print("  1. 复制 .env.example 为 .env")
            print("  2. 填入您的商汤 SenseNova API Key")
            print("  3. 运行: python local_image_generator.py --help")
            
        except KeyboardInterrupt:
            print("\n\n已取消")

    def full_auto_install(self):
        """完全自动化安装 - 一键到位，无需任何交互"""
        print("\n" + "=" * 100)
        print("🚀 Live2D Master Agent - 完全自动化安装")
        print("=" * 100)

        # 检测操作系统
        os_type = self.detect_os()
        os_name = self.get_os_name(os_type)
        print(f"\n🖥️  检测到操作系统: {os_name}")

        print("\n📦 正在安装完整功能包（推荐）...")
        print("   这将包含：")
        print("   - ✅ 基础依赖（Pillow, NumPy, Requests, urllib3）")
        print("   - ✅ PSD 处理库")
        print("   - ✅ 专业分层工具（scipy, scikit-learn, rembg）")
        print("   - ✅ OpenCV 边缘检测库")
        print("   - ✅ rembg 轻量AI模型（用于背景去除）")
        print("   - ⚙️  系统级依赖（根据操作系统自动安装）")
        print("\n⏳ 开始安装...\n")

        # 安装所有核心和推荐的 Python 依赖
        success = True

        # 阶段 0：安装系统依赖（仅 Linux 需要）
        if os_type == OSType.LINUX:
            print("\n" + "-" * 50)
            print("阶段 0/4: 安装系统级依赖")
            print("-" * 50)
            self.install_system_dependencies(os_type)

        # 阶段 1：必需依赖
        print("\n" + "-" * 50)
        print(f"阶段 {1 if os_type == OSType.LINUX else 1}/4: 安装基础依赖")
        print("-" * 50)
        for res_id in ["pillow", "numpy", "urllib3", "requests"]:
            if not self.install_resource(self.RESOURCES[res_id]):
                success = False

        # 阶段 2：推荐增强功能
        print("\n" + "-" * 50)
        print(f"阶段 {2 if os_type == OSType.LINUX else 2}/4: 安装推荐增强库")
        print("-" * 50)
        for res_id in ["psd_tools", "scipy", "scikit_learn", "onnxruntime", "rembg", "opencv_python"]:
            self.install_resource(self.RESOURCES[res_id])  # 即使失败也继续

        # 阶段 3：轻量模型
        print("\n" + "-" * 50)
        print(f"阶段 {3 if os_type == OSType.LINUX else 3}/4: 下载轻量AI模型")
        print("-" * 50)
        self.install_resource(self.RESOURCES["rembg_u2netp"])  # 即使失败也继续

        # 自动创建 .env 文件（如果不存在）
        env_example = self.base_dir / ".env.example"
        env_file = self.base_dir / ".env"
        if env_example.exists() and not env_file.exists():
            print("\n📝 自动创建配置文件...")
            try:
                import shutil
                shutil.copy(env_example, env_file)
                print(f"   ✓ 已创建 .env 文件")
                print(f"   💡 请记得填入您的 API Key！")
            except Exception as e:
                print(f"   ⚠️  无法创建 .env 文件: {e}")

        # 完成总结
        print("\n" + "=" * 100)
        print("✅ 安装完成！")
        print("=" * 100)
        print("\n🎉 您现在可以使用 Live2D Master Agent 的全部功能！")
        print("\n📖 快速开始命令：")
        print("   1. 查看帮助: python local_image_generator.py --help")
        print("   2. 生成测试角色: python local_image_generator.py --live2d-rig 'blue hair girl'")
        print("   3. 完整工作流测试: python live2d_workflow.py --help")
        print("\n⚙️  API 配置（可选）:")
        print("   编辑 .env 文件，填入商汤 SenseNova API Key 可获得更好的效果")
        print("\n" + "=" * 100 + "\n")
        return success


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Live2D Master Agent - 云端资源管理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 列出所有资源
  python cloud_resource_manager.py list

  # 快速开始（最小安装）
  python cloud_resource_manager.py quickstart

  # 安装所有必需资源
  python cloud_resource_manager.py install --all

  # 安装指定资源
  python cloud_resource_manager.py install --ids pillow numpy requests

  # 按类别安装
  python cloud_resource_manager.py install --category python
  python cloud_resource_manager.py install --category rembg
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", title="命令")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有可用资源")
    list_parser.add_argument("--category", type=str, help="按类别筛选 (python/rembg/models/all)")
    
    # install 命令
    install_parser = subparsers.add_parser("install", help="安装资源")
    install_parser.add_argument("--ids", type=str, nargs="+", help="资源 ID 列表")
    install_parser.add_argument("--category", type=str, help="按类别安装")
    install_parser.add_argument("--all", action="store_true", help="安装所有必需资源")
    
    # quickstart 命令
    subparsers.add_parser("quickstart", help="快速开始 - 最小安装")
    
    # full-auto 命令（推荐）
    subparsers.add_parser("full-auto", help="完全自动化安装 - 一键到位，推荐！")
    
    args = parser.parse_args()
    
    manager = CloudResourceManager()
    
    if args.command == "list":
        manager.print_resource_list()
    elif args.command == "quickstart":
        manager.quick_start()
    elif args.command == "full-auto":
        manager.full_auto_install()
    elif args.command == "install":
        if args.all:
            manager.install_all()
        elif args.ids:
            manager.install_batch(args.ids)
        elif args.category:
            manager.install_batch(category=args.category)
        else:
            print("⚠️  请指定 --all, --ids, 或 --category")
    else:
        parser.print_help()


if __name__ == "__main__":
    import argparse
    main()

