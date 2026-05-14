# Live2D Master Agent

专业的 Live2D 技术美术助手，用于 **AI 角色立绘生成、分析、PSD 分层规划、Cubism 工程命名、VTuber 资源质检、遮挡修复、动态部件拆分、动画参数建议**。

---

## 项目结构

```
live2d-master-agent/
├── SKILL.md              # 核心技能定义
├── prompts/              # 提示词文件
│   ├── split.md          # PSD 分层规划提示词
│   ├── rigging.md        # Cubism 绑定提示词
│   ├── physics.md        # 物理设置提示词
│   ├── qa.md             # 质量检查提示词
│   ├── naming.md         # 命名提示词
│   └── image_generation.md  # ✨ 图片生成提示词
├── templates/            # 模板文件
│   ├── psd_structure.md
│   ├── cubism_params.md
│   └── export_rules.md
├── examples/             # 案例文件
│   ├── anime_girl_case.md
│   ├── vtuber_case.md
│   ├── hair_split_case.md
│   └── image_generation_examples.md  # ✨ 图片生成示例
├── scripts/              # 辅助脚本
│   ├── auto_naming.py    # 自动命名工具
│   ├── layer_checker.py  # 图层检查工具
│   └── physics_helper.py # 物理参数建议工具
├── output/               # ✨ 输出文件目录
│   └── psd_layering_plan_vtuber_twintail.md
├── TEST_REPORT.md        # 测试报告
└── README.md
```

---

## 核心功能

### 1. ✨ 角色立绘生成 (新增)
- 根据提示词生成高质量的 Live2D 角色立绘
- 支持多种风格：可爱、优雅、Q版、兽耳等
- 提供完整的提示词模板和示例
- 自动确保图片适合 Live2D 绑定

### 2. 自动 PSD 分层规划
- 输入角色立绘，输出完整 PSD 图层结构
- 包含层级顺序、分组建议、Draw Order
- 支持多种角色类型：VTuber、动漫女孩、Q版等

### 3. Live2D 资源质检
- 自动发现遮挡问题、头发断层、衣服缺边等
- 检查眼睛不对称、嘴型完整性、耳朵缺失
- 检查图层命名规范

### 4. 自动命名工具
- 生成符合 Live2D 规范的图层名
- 生成标准的 Cubism 参数名
- 支持左右标识（l/r）和序号自动填充

### 5. 物理参数建议工具
- 为头发、耳朵、尾巴、丝带等提供物理参数
- 包含重力、风力、回复力、阻尼等完整参数

### 6. Cubism 绑定建议
- Warp Deformer 和 Rotation Deformer 设置建议
- Mesh 设置指导
- 完整的工作流程

---

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

### 角色立绘生成

1. 查看提示词模板：[prompts/image_generation.md](prompts/image_generation.md)
2. 查看示例：[examples/image_generation_examples.md](examples/image_generation_examples.md)
3. 使用提示词生成你的角色立绘

### PSD 分层规划

1. 描述你的角色（类型、发型、配件等）
2. 获得完整的分层方案和绑定建议
3. 示例方案已保存在：[output/psd_layering_plan_vtuber_twintail.md](output/psd_layering_plan_vtuber_twintail.md)

---

## 快速开始

### 角色立绘生成流程

```
步骤 1: 选择角色类型和风格
步骤 2: 使用提示词模板生成立绘
步骤 3: 使用分层规划功能获得 PSD 分层方案
步骤 4: 在 Photoshop 中按照方案分层
步骤 5: 导入 Cubism 进行绑定
```

---

## 技术栈

- Python 3
- Live2D Cubism
- Trae

