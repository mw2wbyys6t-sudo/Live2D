# Live2D Master Agent

专业的 Live2D 技术美术助手，用于 AI 角色立绘分析、PSD 分层规划、Cubism 工程命名、VTuber 资源质检、遮挡修复、动态部件拆分、动画参数建议。

## 项目结构

```
live2d-master-agent/
├── SKILL.md              # 核心技能定义
├── prompts/              # 提示词文件
│   ├── split.md
│   ├── rigging.md
│   ├── physics.md
│   ├── qa.md
│   └── naming.md
├── templates/            # 模板文件
│   ├── psd_structure.md
│   ├── cubism_params.md
│   └── export_rules.md
├── examples/             # 案例文件
│   ├── anime_girl_case.md
│   ├── vtuber_case.md
│   └── hair_split_case.md
├── scripts/              # 辅助脚本
│   ├── auto_naming.py    # 自动命名工具
│   ├── layer_checker.py  # 图层检查工具
│   └── physics_helper.py # 物理参数建议工具
└── README.md
```

## 核心功能

1. **自动 PSD 分层规划** - 输入角色立绘，输出完整 PSD 图层结构
2. **Live2D 问题检查** - 自动发现遮挡问题、头发断层、衣服缺边等
3. **自动命名** - 生成规范的图层名和 Cubism 参数名
4. **拆分建议** - 提供动态部件的拆分方案
5. **Cubism 工作流** - 完整的工作流指导

## 使用方法

### 脚本使用

```bash
# 自动命名工具
python scripts/auto_naming.py

# 图层检查工具
python scripts/layer_checker.py

# 物理参数建议工具
python scripts/physics_helper.py
```

## 技术栈

- Python 3
- Live2D Cubism
- Trae

