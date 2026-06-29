#!/usr/bin/env python3
"""
生成专家模式测试用的上下文文件。

用途：
- 汇总项目核心文档、代码片段、配置与不足点
- 文件大小目标约 400KB，用于测试新模型对大型上下文的理解与专家分析能力

运行方式：
    python scripts/generate_expert_context.py
"""
import os
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "EXPERT_CONTEXT.md"

# 目标大小（字节）
TARGET_SIZE = 400 * 1024

# 文件列表：(相对路径, 最大读取行数, 说明)
# 行数 None 表示完整读取
FILES = [
    # ===== 项目概览文档 =====
    ("README.md", None, "项目主文档"),
    ("USAGE.md", None, "使用说明"),
    ("docs/PROJECT_STRUCTURE.md", None, "项目结构说明"),
    ("docs/USER_GUIDE.md", 350, "完整使用教程（节选）"),
    ("docs/FAQ.md", 300, "常见问题（节选）"),
    ("docs/LIMITATIONS.md", None, "已知限制"),
    ("docs/BEST_PRACTICES.md", 250, "最佳实践（节选）"),
    ("docs/QUICKSTART.md", 200, "快速入门（节选）"),
    ("docs/SEE_THROUGH_INTEGRATION.md", 200, "See-through 集成指南（节选）"),
    ("CHANGELOG.md", 300, "更新日志（节选）"),
    ("创作申明", None, "作者声明"),

    # ===== Skill 核心 =====
    (".trae/skills/live2d-master-agent/SKILL.md", 350, "Trae Skill 定义"),
    (".trae/skills/live2d-master-agent/README.md", 200, "Skill README（节选）"),
    (".trae/skills/live2d-master-agent/ARCHITECTURE.md", 200, "架构说明（节选）"),
    (".trae/skills/live2d-master-agent/VERSION_INFO.json", None, "版本信息"),

    # ===== 核心代码接口 =====
    (".trae/skills/live2d-master-agent/core/interfaces.py", None, "核心接口定义"),
    (".trae/skills/live2d-master-agent/core/workflow_engine.py", 200, "工作流引擎（节选）"),

    # ===== 主要入口/工具（节选） =====
    (".trae/skills/live2d-master-agent/master_tool.py", 350, "一站式工具箱（节选）"),
    (".trae/skills/live2d-master-agent/live2d_agent.py", 300, "交互式 Agent（节选）"),
    (".trae/skills/live2d-master-agent/live2d_workflow.py", 300, "端到端工作流（节选）"),
    (".trae/skills/live2d-master-agent/local_image_generator.py", 300, "本地图像生成器（节选）"),
    (".trae/skills/live2d-master-agent/live2d_desktop_pet.py", 280, "桌面桌宠（节选）"),
    (".trae/skills/live2d-master-agent/config.py", 280, "安全配置加载器（节选）"),
    (".trae/skills/live2d-master-agent/secure_storage.py", 250, "加密存储模块（节选）"),
    (".trae/skills/live2d-master-agent/live2d_layer_v6.py", 250, "v6.0 K-means 分层（节选）"),
    (".trae/skills/live2d-master-agent/install_comfyui_advanced.py", 200, "See-through 安装器（节选）"),

    # ===== Go API =====
    (".trae/skills/live2d-master-agent/api/main.go", 180, "Go API 入口（节选）"),
    (".trae/skills/live2d-master-agent/api/handlers/handlers.go", 180, "HTTP 处理器（节选）"),

    # ===== 根目录包装器 =====
    ("live2d_agent.py", 120, "根目录 Agent 包装器"),
    ("master_tool.py", 120, "根目录工具箱包装器"),
    ("install.py", 150, "兼容性安装脚本"),
    ("requirements.txt", None, "Python 依赖"),

    # ===== Web UI =====
    ("web/package.json", None, "Web UI 依赖"),
    ("web/pages/index.tsx", 280, "Web 主页（节选）"),
    ("web/components/WorkflowTracker.tsx", 250, "工作流跟踪组件"),
    ("web/lib-shared/types.ts", 250, "共享类型定义"),
    ("web/lib-shared/workflow.ts", 250, "共享工作流类型"),
    ("web/lib/psd-parser.ts", 250, "PSD 解析器（节选）"),
    ("web/lib/qa-engine.ts", 250, "QA 引擎（节选）"),
    ("web/lib/image-to-psd.ts", 200, "图片转 PSD（节选）"),
    ("web/rules/index.ts", 180, "规则引擎入口（节选）"),
    ("web/rules/critical-layers.ts", 150, "关键图层规则"),
    ("web/components/ChatAssistant.tsx", 200, "聊天助手组件（节选）"),

    # ===== 测试与辅助脚本 =====
    ("tests/test_workflow.py", 150, "根目录测试包装器"),
    (".trae/skills/live2d-master-agent/test_full_coverage.py", 280, "全覆盖测试（节选）"),
    (".trae/skills/live2d-master-agent/test_deep_coverage.py", 280, "深度测试（节选）"),
    (".trae/skills/live2d-master-agent/scripts/seedream_image_generate.py", 280, "Seedream 生成脚本（节选）"),
    (".trae/skills/live2d-master-agent/scripts/qa_engine_enhanced.py", 280, "质量检查引擎（节选）"),
    (".trae/skills/live2d-master-agent/scripts/layer_checker.py", 220, "图层检查器（节选）"),
    (".trae/skills/live2d-master-agent/scripts/parameter_designer_enhanced.py", 220, "参数设计器（节选）"),
    (".trae/skills/live2d-master-agent/scripts/physics_helper.py", 220, "物理设置助手（节选）"),

    # ===== 提示词与模板 =====
    ("prompts/image_generation.md", 250, "图像生成提示词（节选）"),
    ("prompts/split.md", 200, "分层提示词（节选）"),
    ("templates/psd_structure.md", 200, "PSD 结构模板（节选）"),
    ("examples/anime_girl_case.md", 200, "案例：动漫女孩（节选）"),

    # ===== ComfyUI Connector =====
    ("comfyui-connector/src/connectors/comfyui.connector.ts", 250, "ComfyUI 连接器（节选）"),
    ("comfyui-connector/src/services/image-generation.service.ts", 250, "图像生成服务（节选）"),
    ("comfyui-connector/package.json", None, "Connector 依赖"),

    # ===== TypeScript 共享库 =====
    ("lib/seedream-service.ts", 250, "Seedream 服务（节选）"),
    ("lib/steps/02-image-gen.ts", 250, "图像生成步骤（节选）"),
    ("lib/workflow.ts", 200, "共享工作流（节选）"),

    # ===== 其他关键模块 =====
    (".trae/skills/live2d-master-agent/api/models/models.go", 150, "Go API 模型"),
    (".trae/skills/live2d-master-agent/api/services/python_bridge.go", 200, "Python 桥接服务（节选）"),
    (".trae/skills/live2d-master-agent/advanced_generation_pipeline.py", 200, "高级生成管线（节选）"),

    # ===== 配置示例 =====
    (".trae/skills/live2d-master-agent/.env.example", None, "环境变量示例"),
]


def read_file(rel_path: str, max_lines: int | None) -> str:
    """读取文件内容，限制行数。"""
    full_path = PROJECT_ROOT / rel_path
    if not full_path.exists():
        return f"\n> ⚠️ 文件不存在：{rel_path}\n"
    try:
        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception as e:
        return f"\n> ⚠️ 读取失败：{rel_path}，原因：{e}\n"

    total_lines = len(lines)
    if max_lines and total_lines > max_lines:
        kept = lines[:max_lines]
        omitted = total_lines - max_lines
        kept.append(f"\n...（省略后续 {omitted} 行，原文件共 {total_lines} 行）...\n")
        content = "".join(kept)
    else:
        content = "".join(lines)

    return content


def build_context() -> str:
    """构建上下文文本。"""
    parts = []
    parts.append("# Live2D Master Agent - 专家模式上下文\n")
    parts.append(
        f"\n> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        "> 用途：测试新模型对大型项目上下文的理解、更新点识别与不足点解决能力\n"
        "> 目标大小：约 400KB\n"
    )

    parts.append("\n## 评估任务（请新模型在完整阅读上下文后回答）\n")
    parts.append(
        """
1. **更新点分析**：基于当前项目状态，列出 5-10 个最有价值的下一步功能更新或优化点，按优先级排序。
2. **不足点识别**：从代码质量、架构设计、安全性、可维护性、用户体验、性能等维度，找出当前项目的主要不足。
3. **解决方案设计**：针对每个不足点，给出具体的、可落地的解决方案，包括代码/配置改动建议。
4. **路线图建议**：如果让你负责 v7.3 / v8.0 版本，你会如何规划迭代路线？
5. **专家模式验证**：评估当前 `SKILL.md` 中的专家模式设计是否合理，是否需要补充新的命令或工作流。
"""
    )

    parts.append("\n---\n")

    for rel_path, max_lines, description in FILES:
        parts.append(f"\n## {description}\n")
        parts.append(f"**文件**：`{rel_path}`\n")
        parts.append("```\n")
        parts.append(read_file(rel_path, max_lines))
        parts.append("\n```\n")

    # 尾部补充已知问题与 TODO
    parts.append("\n## 项目当前已知问题汇总\n")
    parts.append(
        """
- 前端 `web/lib/` 与 `web/lib-shared/` 存在重复代码，需要统一或清理。
- 根目录包装器（`live2d_agent.py` 等）与 `.trae/skills/.../` 下真实实现存在重复包装逻辑。
- `See-through` 集成为规划功能，当前实际分层仍以 K-means 聚类为主，质量与商业工具差距较大。
- 桌面桌宠未真正使用 Live2D Cubism SDK，而是基于 pygame 的简易动画，扩展性有限。
- Go API 服务与 Python 脚本通过命令行桥接，存在性能开销和安全边界问题。
- 部分文档中的文件引用仍指向旧位置（如根目录测试脚本），需要持续同步。
- 未配置 CI/CD，依赖人工验证 TypeScript 编译和 Python 语法。
- `.env` / `.env.encrypted` 不在版本控制中，新用户首次使用容易遗漏 API 配置。
"""
    )

    return "".join(parts)


def main():
    context = build_context()
    OUTPUT_FILE.write_text(context, encoding="utf-8")
    size = OUTPUT_FILE.stat().st_size
    print(f"✅ 已生成：{OUTPUT_FILE}")
    print(f"   大小：{size:,} bytes ({size / 1024:.1f} KB)")
    print(f"   目标：{TARGET_SIZE:,} bytes ({TARGET_SIZE / 1024:.1f} KB)")
    if size > TARGET_SIZE * 1.15:
        print("⚠️ 超出目标 15%，建议减少某些文件的 max_lines")
    elif size < TARGET_SIZE * 0.7:
        print("ℹ️ 低于目标 30%，可适当增加内容")
    else:
        print("✅ 大小在目标范围内")


if __name__ == "__main__":
    main()
