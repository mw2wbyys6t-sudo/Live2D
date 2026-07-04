#!/usr/bin/env python3
"""
Live2D Master Agent - 工作流全面测试脚本
测试目标：发现运行时问题，记录并保存供后续系统性优化

测试覆盖：
1. 模块导入测试
2. 配置加载测试
3. 安全功能测试
4. 图像处理测试
5. 分层功能测试
6. 桌宠功能测试
7. 工作流集成测试
8. API服务测试

使用方法：
    python test_workflow.py [--verbose] [--save-report]

输出：
    - 控制台实时结果
    - test_report_TIMESTAMP.json - 详细测试报告
    - test_issues_TIMESTAMP.md - 问题清单
"""

import sys
import os
import json
import time
import traceback
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

# 测试配置
TEST_CONFIG = {
    "verbose": False,
    "save_report": True,
    "test_image_size": (512, 512),
    "test_output_dir": "./test_output",
}

# 全局测试结果
TEST_RESULTS = {
    "start_time": None,
    "end_time": None,
    "total_tests": 0,
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "issues": [],
    "modules_tested": [],
}


def log(msg: str, level: str = "INFO"):
    """记录日志"""
    prefix = {"INFO": "[ℹ️]", "PASS": "[✅]", "FAIL": "[❌]", "WARN": "[⚠️]", "SKIP": "[⏭️]"}.get(level, "[ℹ️]")
    print(f"{prefix} {msg}")
    if level == "FAIL":
        TEST_RESULTS["issues"].append({"level": level, "message": msg, "time": datetime.now().isoformat()})


def test_module_import(module_name: str, required: bool = True) -> bool:
    """测试模块导入"""
    TEST_RESULTS["total_tests"] += 1
    try:
        __import__(module_name)
        TEST_RESULTS["passed"] += 1
        TEST_RESULTS["modules_tested"].append({"name": module_name, "status": "passed", "required": required})
        log(f"模块导入成功: {module_name}", "PASS")
        return True
    except ImportError as e:
        if required:
            TEST_RESULTS["failed"] += 1
            log(f"模块导入失败: {module_name} - {e}", "FAIL")
        else:
            TEST_RESULTS["skipped"] += 1
            log(f"可选模块缺失: {module_name} - {e}", "SKIP")
        TEST_RESULTS["modules_tested"].append({"name": module_name, "status": "failed" if required else "skipped", "error": str(e), "required": required})
        return False
    except Exception as e:
        TEST_RESULTS["failed"] += 1
        log(f"模块导入异常: {module_name} - {e}", "FAIL")
        TEST_RESULTS["modules_tested"].append({"name": module_name, "status": "error", "error": str(e), "required": required})
        return False


def test_security_functions() -> bool:
    """测试安全功能"""
    log("\n" + "="*60)
    log("测试安全功能模块")
    log("="*60)
    
    TEST_RESULTS["total_tests"] += 1
    try:
        from security_fixes import validate_path, sanitize_prompt, validate_image_path
        
        # 测试路径验证
        ok, msg = validate_path("./test.png", "/workspace")
        assert ok == True, f"正常路径验证失败: {msg}"
        
        ok, msg = validate_path("../../../etc/passwd", "/workspace")
        assert ok == False, f"路径遍历攻击未被阻止"
        
        # 测试提示词清理
        clean = sanitize_prompt("test; rm -rf /")
        assert ";" not in clean, f"危险字符未被清理: {clean}"
        
        # 测试图像路径验证（替代 validate_file_upload）
        ok, msg = validate_image_path("test.exe")
        assert ok == False, f"危险文件扩展名未被阻止"
        
        TEST_RESULTS["passed"] += 1
        log("安全功能测试通过", "PASS")
        return True
    except Exception as e:
        TEST_RESULTS["failed"] += 1
        log(f"安全功能测试失败: {e}", "FAIL")
        traceback.print_exc()
        return False


def test_image_processing() -> bool:
    """测试图像处理功能"""
    log("\n" + "="*60)
    log("测试图像处理功能")
    log("="*60)
    
    TEST_RESULTS["total_tests"] += 1
    try:
        from PIL import Image
        import numpy as np
        
        # 创建测试图像
        test_img = Image.new('RGBA', TEST_CONFIG["test_image_size"], (255, 200, 180, 255))
        
        # 测试图像基本操作
        assert test_img.size == TEST_CONFIG["test_image_size"], "图像尺寸错误"
        assert test_img.mode == 'RGBA', "图像模式错误"
        
        # 测试numpy转换
        arr = np.array(test_img)
        assert arr.shape == (512, 512, 4), f"numpy数组形状错误: {arr.shape}"
        
        TEST_RESULTS["passed"] += 1
        log("图像处理基础测试通过", "PASS")
        return True
    except Exception as e:
        TEST_RESULTS["failed"] += 1
        log(f"图像处理测试失败: {e}", "FAIL")
        traceback.print_exc()
        return False


def test_layering_functions() -> bool:
    """测试分层功能"""
    log("\n" + "="*60)
    log("测试智能分层功能")
    log("="*60)
    
    TEST_RESULTS["total_tests"] += 1
    try:
        from PIL import Image
        import numpy as np
        from sklearn.cluster import KMeans
        
        # 创建测试图像（模拟角色）
        img = Image.new('RGBA', (256, 256), (255, 255, 255, 0))
        pixels = np.array(img)
        
        # 添加一些颜色区域模拟身体部位
        pixels[50:100, 50:150] = [255, 220, 200, 255]  # 脸
        pixels[100:200, 50:150] = [200, 50, 50, 255]    # 衣服
        pixels[20:50, 60:140] = [100, 50, 30, 255]      # 头发
        
        # 测试K-means聚类
        flat_pixels = pixels.reshape(-1, 4)
        non_transparent = flat_pixels[flat_pixels[:, 3] > 0]
        
        if len(non_transparent) > 0:
            kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
            kmeans.fit(non_transparent[:, :3])
            log(f"K-means聚类成功: {len(kmeans.cluster_centers_)} 个簇", "PASS")
        
        TEST_RESULTS["passed"] += 1
        log("分层功能基础测试通过", "PASS")
        return True
    except Exception as e:
        TEST_RESULTS["failed"] += 1
        log(f"分层功能测试失败: {e}", "FAIL")
        traceback.print_exc()
        return False


def test_desktop_pet() -> bool:
    """测试桌面桌宠功能"""
    log("\n" + "="*60)
    log("测试桌面桌宠功能")
    log("="*60)
    
    TEST_RESULTS["total_tests"] += 1
    try:
        from live2d_desktop_pet import DesktopPetAnimator
        
        # 创建临时目录结构
        with tempfile.TemporaryDirectory() as tmpdir:
            layers_dir = Path(tmpdir) / "test_layers"
            layers_dir.mkdir()
            output_dir = Path(tmpdir) / "test_output"
            
            # 创建一些测试图层
            from PIL import Image
            for name in ["脸_基础", "头发_刘海", "眼睛_左"]:
                img = Image.new('RGBA', (100, 100), (255, 200, 180, 255))
                img.save(layers_dir / f"{name}.png")
            
            # 测试初始化
            animator = DesktopPetAnimator(str(layers_dir), str(output_dir))
            assert len(animator.layer_groups) > 0, "图层组为空"
            
            # 测试动画配置生成
            config = animator.create_animation_config()
            assert "animations" in config, "动画配置缺少animations字段"
            assert "expressions" in config, "动画配置缺少expressions字段"
            
            TEST_RESULTS["passed"] += 1
            log("桌面桌宠功能测试通过", "PASS")
            return True
    except Exception as e:
        TEST_RESULTS["failed"] += 1
        log(f"桌面桌宠测试失败: {e}", "FAIL")
        traceback.print_exc()
        return False


def test_workflow_integration() -> bool:
    """测试工作流集成"""
    log("\n" + "="*60)
    log("测试工作流集成")
    log("="*60)
    
    TEST_RESULTS["total_tests"] += 1
    try:
        from live2d_workflow import Live2DWorkflow
        
        # 测试初始化
        workflow = Live2DWorkflow()
        
        # 验证PSD标准
        assert "format" in workflow.PSD_STANDARD, "PSD标准缺少format字段"
        assert workflow.PSD_STANDARD["format"] == "PSD", "PSD格式错误"
        
        # 验证图层顺序
        assert len(workflow.LIVE2D_LAYER_ORDER) > 0, "图层顺序为空"
        assert "脸_基础" in workflow.LIVE2D_LAYER_ORDER, "缺少脸_基础图层"
        
        # 验证部件颜色映射
        assert len(workflow.PART_COLOR_RANGES) > 0, "部件颜色映射为空"
        
        TEST_RESULTS["passed"] += 1
        log("工作流集成测试通过", "PASS")
        return True
    except Exception as e:
        TEST_RESULTS["failed"] += 1
        log(f"工作流集成测试失败: {e}", "FAIL")
        traceback.print_exc()
        return False


def test_image_generator() -> bool:
    """测试图像生成器"""
    log("\n" + "="*60)
    log("测试图像生成器")
    log("="*60)
    
    TEST_RESULTS["total_tests"] += 1
    try:
        from local_image_generator import ModelConfig, ProviderRouter
        
        # 测试模型配置
        models = list(ModelConfig.MODELS.keys())
        assert len(models) > 0, "模型列表为空"
        log(f"可用模型数量: {len(models)}", "INFO")
        
        # 测试Provider路由
        router = ProviderRouter()
        providers = router.get_available_providers()
        log(f"可用Provider: {providers}", "INFO")
        
        TEST_RESULTS["passed"] += 1
        log("图像生成器测试通过", "PASS")
        return True
    except Exception as e:
        TEST_RESULTS["failed"] += 1
        log(f"图像生成器测试失败: {e}", "FAIL")
        traceback.print_exc()
        return False


def test_cloud_resources() -> bool:
    """测试云端资源管理"""
    log("\n" + "="*60)
    log("测试云端资源管理")
    log("="*60)
    
    TEST_RESULTS["total_tests"] += 1
    try:
        from cloud_resource_manager import CloudResourceManager, ResourceType
        
        # 测试资源类型
        resource_types = list(ResourceType)
        assert len(resource_types) > 0, "资源类型为空"
        log(f"资源类型: {[r.value for r in resource_types]}", "INFO")
        
        # 测试资源列表
        manager = CloudResourceManager()
        assert len(manager.RESOURCES) > 0, "资源列表为空"
        log(f"可用资源数量: {len(manager.RESOURCES)}", "INFO")
        
        TEST_RESULTS["passed"] += 1
        log("云端资源管理测试通过", "PASS")
        return True
    except Exception as e:
        TEST_RESULTS["failed"] += 1
        log(f"云端资源管理测试失败: {e}", "FAIL")
        traceback.print_exc()
        return False


def test_master_tool() -> bool:
    """测试主工具"""
    log("\n" + "="*60)
    log("测试主工具")
    log("="*60)
    
    TEST_RESULTS["total_tests"] += 1
    try:
        from master_tool import FEATURES
        
        # 测试特征库
        total_features = sum(len(v) for v in FEATURES.values())
        assert total_features > 0, "特征库为空"
        log(f"特征库总数: {total_features}", "INFO")
        log(f"特征类别: {list(FEATURES.keys())}", "INFO")
        
        TEST_RESULTS["passed"] += 1
        log("主工具测试通过", "PASS")
        return True
    except Exception as e:
        TEST_RESULTS["failed"] += 1
        log(f"主工具测试失败: {e}", "FAIL")
        traceback.print_exc()
        return False


def run_all_tests():
    """运行所有测试"""
    log("\n" + "="*70)
    log("Live2D Master Agent - 工作流全面测试")
    log("="*70)
    log(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"测试目录: {os.getcwd()}")
    log("="*70)
    
    TEST_RESULTS["start_time"] = datetime.now().isoformat()
    
    # 1. 模块导入测试
    log("\n" + "="*60)
    log("阶段 1: 模块导入测试")
    log("="*60)
    
    required_modules = [
        "live2d_workflow",
        "live2d_desktop_pet",
        "local_image_generator",
        "master_tool",
        "cloud_resource_manager",
        "security_fixes",
    ]
    
    optional_modules = [
        "live2d_layer_v6",
        "live2d_layer_pro",
        "live2d_image_processor",
        "live2d_layer_bilibili",
    ]
    
    for mod in required_modules:
        test_module_import(mod, required=True)
    
    for mod in optional_modules:
        test_module_import(mod, required=False)
    
    # 2. 功能测试
    test_security_functions()
    test_image_processing()
    test_layering_functions()
    test_desktop_pet()
    test_workflow_integration()
    test_image_generator()
    test_cloud_resources()
    test_master_tool()
    
    # 结束测试
    TEST_RESULTS["end_time"] = datetime.now().isoformat()
    
    # 输出总结
    log("\n" + "="*70)
    log("测试总结")
    log("="*70)
    log(f"总测试数: {TEST_RESULTS['total_tests']}")
    log(f"通过: {TEST_RESULTS['passed']}", "PASS")
    log(f"失败: {TEST_RESULTS['failed']}", "FAIL" if TEST_RESULTS['failed'] > 0 else "PASS")
    log(f"跳过: {TEST_RESULTS['skipped']}", "WARN" if TEST_RESULTS['skipped'] > 0 else "PASS")
    log(f"问题数: {len(TEST_RESULTS['issues'])}", "WARN" if len(TEST_RESULTS['issues']) > 0 else "PASS")
    
    # 保存报告
    if TEST_CONFIG["save_report"]:
        save_reports()
    
    return TEST_RESULTS["failed"] == 0


def save_reports():
    """保存测试报告"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON 报告
    report_file = f"test_report_{timestamp}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(TEST_RESULTS, f, ensure_ascii=False, indent=2)
    log(f"测试报告已保存: {report_file}")
    
    # Markdown 问题清单
    issues_file = f"test_issues_{timestamp}.md"
    with open(issues_file, 'w', encoding='utf-8') as f:
        f.write("# Live2D Master Agent - 测试问题清单\n\n")
        f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 统计\n\n")
        f.write(f"- 总测试数: {TEST_RESULTS['total_tests']}\n")
        f.write(f"- 通过: {TEST_RESULTS['passed']}\n")
        f.write(f"- 失败: {TEST_RESULTS['failed']}\n")
        f.write(f"- 跳过: {TEST_RESULTS['skipped']}\n\n")
        
        f.write("## 模块状态\n\n")
        f.write("| 模块 | 状态 | 必需 | 错误 |\n")
        f.write("|------|------|------|------|\n")
        for mod in TEST_RESULTS['modules_tested']:
            status_emoji = {"passed": "✅", "failed": "❌", "skipped": "⏭️", "error": "⚠️"}.get(mod['status'], "❓")
            f.write(f"| {mod['name']} | {status_emoji} {mod['status']} | {'是' if mod.get('required', True) else '否'} | {mod.get('error', '-')} |\n")
        
        f.write("\n## 问题详情\n\n")
        if TEST_RESULTS['issues']:
            for i, issue in enumerate(TEST_RESULTS['issues'], 1):
                f.write(f"### 问题 {i}\n\n")
                f.write(f"- 级别: {issue['level']}\n")
                f.write(f"- 时间: {issue['time']}\n")
                f.write(f"- 描述: {issue['message']}\n\n")
        else:
            f.write("✅ 未发现严重问题\n")
        
        f.write("\n## 优化建议\n\n")
        f.write("根据测试结果，建议进行以下优化:\n\n")
        
        # 根据测试结果生成建议
        failed_modules = [m for m in TEST_RESULTS['modules_tested'] if m['status'] == 'failed' and m.get('required', True)]
        if failed_modules:
            f.write("### 高优先级\n\n")
            f.write("1. **修复必需模块导入失败**\n")
            for mod in failed_modules:
                f.write(f"   - {mod['name']}: {mod.get('error', '未知错误')}\n")
            f.write("\n")
        
        skipped_modules = [m for m in TEST_RESULTS['modules_tested'] if m['status'] == 'skipped']
        if skipped_modules:
            f.write("### 中优先级\n\n")
            f.write("1. **安装可选模块以启用完整功能**\n")
            for mod in skipped_modules:
                f.write(f"   - {mod['name']}: {mod.get('error', '未安装')}\n")
            f.write("\n")
        
        f.write("### 通用建议\n\n")
        f.write("1. 确保所有依赖已正确安装 (`pip install -r requirements.txt`)\n")
        f.write("2. 检查系统依赖（Linux需安装SDL2开发库）\n")
        f.write("3. 验证配置文件（`.env`中的API Key等）\n")
        f.write("4. 运行 `python install.py` 进行完整安装\n")
    
    log(f"问题清单已保存: {issues_file}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Live2D Master Agent 工作流测试")
    parser.add_argument("--verbose", action="store_true", help="详细输出")
    parser.add_argument("--no-save", action="store_true", help="不保存报告")
    args = parser.parse_args()
    
    TEST_CONFIG["verbose"] = args.verbose
    TEST_CONFIG["save_report"] = not args.no_save
    
    success = run_all_tests()
    sys.exit(0 if success else 1)
