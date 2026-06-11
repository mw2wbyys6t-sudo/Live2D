import sys
import importlib
from typing import Dict, List, Tuple

REQUIRED_MODULES = {
    'core': [
        ('PIL', 'Pillow'),
        ('numpy', 'numpy'),
        ('requests', 'requests'),
        ('urllib3', 'urllib3'),
    ],
    'image_processing': [
        ('cv2', 'opencv-python'),
        ('scipy', 'scipy'),
        ('sklearn', 'scikit-learn'),
    ],
    'psd_export': [
        ('psd_tools', 'psd-tools'),
    ],
    'desktop_pet': [
        ('pygame', 'pygame'),
    ],
}

def check_dependencies() -> Tuple[Dict[str, bool], List[str]]:
    """检查所有依赖是否安装"""
    results = {}
    missing = []
    
    for category, modules in REQUIRED_MODULES.items():
        all_installed = True
        for module_name, package_name in modules:
            try:
                importlib.import_module(module_name)
            except ImportError:
                all_installed = False
                missing.append(f"  {package_name} (模块名: {module_name})")
        results[category] = all_installed
    
    return results, missing

def print_dependency_report() -> bool:
    """打印依赖检查报告并返回是否所有依赖都已安装"""
    print("=" * 70)
    print("📦 Live2D Master Agent - 依赖检查")
    print("=" * 70)
    
    results, missing = check_dependencies()
    
    categories = {
        'core': '核心依赖',
        'image_processing': '图像处理',
        'psd_export': 'PSD导出',
        'desktop_pet': '桌面桌宠',
    }
    
    all_installed = True
    for category, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"\n{status_icon} {categories[category]}")
    
    if missing:
        print("\n❌ 缺少以下依赖:")
        for pkg in missing:
            print(pkg)
        print("\n💡 安装命令:")
        print("  pip install Pillow numpy requests urllib3 opencv-python scipy scikit-learn psd-tools pygame")
        print("\n⚠️  注意: pygame 需要系统依赖 (Linux):")
        print("  sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev")
        all_installed = False
    else:
        print("\n✅ 所有依赖已安装完成！")
    
    print("\n" + "=" * 70)
    return all_installed

def ensure_dependencies(required_categories: List[str] = None) -> bool:
    """确保指定类别的依赖已安装"""
    if required_categories is None:
        required_categories = list(REQUIRED_MODULES.keys())
    
    results, missing = check_dependencies()
    
    missing_pkgs = []
    for category in required_categories:
        if category in REQUIRED_MODULES and not results.get(category, False):
            for module_name, package_name in REQUIRED_MODULES[category]:
                try:
                    importlib.import_module(module_name)
                except ImportError:
                    missing_pkgs.append(package_name)
    
    if missing_pkgs:
        print(f"❌ 缺少必需依赖: {', '.join(missing_pkgs)}")
        return False
    
    return True

if __name__ == "__main__":
    print_dependency_report()
    sys.exit(0 if ensure_dependencies() else 1)