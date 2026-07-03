# Live2D Master Skill - 设计文档

**日期:** 2026-05-19  
**版本:** 1.0  
**作者:** Live2D Community

---

## 概述

将现有 Live2D Master Agent 项目包装成一个完整的 Trae Skill，以对话交互为主，Web 界面为辅，为个人创作者提供从概念到 Live2D 模型的端到端制作体验。

### 核心目标

- ✅ 让用户在短时间内获得可用的 Live2D 模型
- ✅ 向导式 + 专家模式的混合体验
- ✅ 完整的 8 步制作流程
- ✅ 智能状态跟踪和进度保存

---

## 1. 设计原则

### 1.1 以对话为主，Web 为辅
- **主要交互方式:** Trae 自然语言对话
- **Web 界面用途:** 文件上传、图片预览、简单的图层查看、进度展示
- **状态同步:** 会话状态在对话和 Web 之间保持一致

### 1.2 混合模式
- **向导模式（默认）:** 8 步完整流程，逐步引导
- **专家模式:** 任务清单，自由选择
- **随时切换:** 用户可以在任何时候切换模式或跳转步骤

### 1.3 快速完成
- 每个步骤都有明确的目标和输出
- 提供高质量的默认选项和模板
- 记录用户偏好，后续使用更快捷

---

## 2. 8 步工作流

### 步骤 1: 概念设定
- **目标:** 确定角色的基本设定
- **输入:** 角色类型、特征、风格偏好
- **输出:** 角色设定文档
- **提示词:** 使用 `prompts/image_generation.md`

### 步骤 2: 立绘生成
- **目标:** 生成适合 Live2D 的角色立绘
- **输入:** 步骤 1 的设定或用户提供的参考
- **输出:** 高质量角色立绘图片
- **工具:** Seedream / ComfyUI 集成

### 步骤 3: PSD 分层规划
- **目标:** 根据立绘规划 PSD 图层结构
- **输入:** 角色立绘图片
- **输出:** 完整的分层方案文档（包含 Draw Order、命名规范）
- **提示词:** 使用 `prompts/split.md`

### 步骤 4: 图片转 PSD
- **目标:** 将普通图片转换为基本的分层 PSD
- **输入:** 角色立绘 + 步骤 3 的分层方案
- **输出:** 初始 PSD 文件
- **工具:** Web 界面的 `ImageToPsd` 组件

### 步骤 5: PSD 质检
- **目标:** 检查 PSD 是否符合 Live2D 规范
- **输入:** PSD 文件
- **输出:** 质检报告（问题清单 + 修改建议）
- **工具:** `web/lib/qa-engine.ts`

### 步骤 6: Cubism 参数设计
- **目标:** 设计 Cubism 工程的参数配置
- **输入:** 质检通过的 PSD
- **输出:** Cubism 参数配置文档
- **提示词:** 使用 `prompts/naming.md`、`templates/cubism_params.md`

### 步骤 7: 物理设置
- **目标:** 为动态部件提供物理参数
- **输入:** 角色特征（头发长度、是否有耳朵/尾巴等）
- **输出:** 物理参数配置（重力、风力、回复力、阻尼等）
- **提示词:** 使用 `prompts/physics.md`
- **工具:** `scripts/physics_helper.py`

### 步骤 8: Rigging 指导
- **目标:** 提供完整的绑定操作指南
- **输入:** 所有前面的输出
- **输出:** 详细的 Rigging 操作指南 + 最佳实践
- **提示词:** 使用 `prompts/rigging.md`

---

## 3. 系统架构

### 3.1 状态管理

```typescript
// 会话状态类型定义
interface Live2DWorkflowState {
  mode: 'wizard' | 'expert'
  currentStep: number  // 1-8
  completed: boolean[]  // 8 个布尔值，表示各步骤是否完成
  artifacts: {
    concept?: CharacterConcept
    characterImage?: string  // base64 或文件路径
    psdPlan?: PsdLayerPlan
    psdFile?: string  // 文件路径
    qaReport?: QAReport
    cubismParams?: CubismParamConfig
    physicsConfig?: PhysicsConfig
    riggingGuide?: RiggingGuide
  }
  preferences?: UserPreferences
}

interface CharacterConcept {
  type: 'vtuber' | 'anime-girl' | 'chibi' | 'other'
  features: string[]
  style: 'cute' | 'elegant' | 'cool' | 'other'
  description: string
}

interface UserPreferences {
  style: string
  defaultParams: Record<string, any>
}
```

### 3.2 核心组件

```
lib/
├── workflow.ts              # 工作流协调器
├── types.ts                 # 类型定义
├── session-manager.ts       # 会话状态管理
└── steps/
    ├── 01-concept.ts        # 步骤 1: 概念设定
    ├── 02-image-gen.ts      # 步骤 2: 立绘生成
    ├── 03-psd-plan.ts       # 步骤 3: PSD 分层规划
    ├── 04-image-to-psd.ts   # 步骤 4: 图片转 PSD
    ├── 05-qa.ts             # 步骤 5: PSD 质检
    ├── 06-params.ts         # 步骤 6: Cubism 参数设计
    ├── 07-physics.ts        # 步骤 7: 物理设置
    └── 08-rigging.ts        # 步骤 8: Rigging 指导
```

### 3.3 工作流协调器 (`workflow.ts`)

**主要职责:**
- 管理当前状态（步骤、模式）
- 处理用户指令（"下一步"、"跳过"、"切换模式"、"跳转"等）
- 调用对应的步骤模块
- 保存和恢复会话状态

**主要方法:**
```typescript
class Live2DWorkflow {
  constructor(initialState?: Partial<Live2DWorkflowState>)
  
  // 状态查询
  getState(): Live2DWorkflowState
  getCurrentStep(): number
  getMode(): 'wizard' | 'expert'
  
  // 模式切换
  switchToWizard(): void
  switchToExpert(): void
  
  // 步骤导航
  nextStep(): void
  prevStep(): void
  goToStep(step: number): void
  skipStep(): void
  
  // 步骤执行
  async executeStep(input: any): Promise<any>
  
  // 状态持久化
  saveState(): string  // 序列化状态
  loadState(serialized: string): void
}
```

---

## 4. 交互设计

### 4.1 向导模式

**开始新流程的对话示例:**
```
用户: 我想做一个 Live2D 模型
助手: 太好了！让我们开始吧。📋

[步骤 1/8] 概念设定

请告诉我：
1. 角色类型（VTuber/动漫女孩/Q版/其他）
2. 主要特征（发型、发色、服装风格等）
3. 整体氛围（可爱/优雅/酷/其他）

或者说"跳过此步"如果你已经有立绘了。
```

**步骤完成后的提示:**
```
助手: 太棒了！[步骤 1] 已完成！✅

角色设定已保存。

接下来：
- 说"下一步"继续到立绘生成
- 说"我想先做 XX"跳转到其他步骤
- 说"切换到专家模式"查看所有可用任务
```

### 4.2 专家模式

**切换到专家模式:**
```
用户: 切换到专家模式
助手: 好的！已切换到专家模式。🔧

当前进度：
- [✓] 步骤 1: 概念设定
- [ ] 步骤 2: 立绘生成
- [ ] 步骤 3: PSD 分层规划
- [ ] 步骤 4: 图片转 PSD
- [ ] 步骤 5: PSD 质检
- [ ] 步骤 6: Cubism 参数设计
- [ ] 步骤 7: 物理设置
- [ ] 步骤 8: Rigging 指导

可用任务：
1. [2] 生成角色立绘
2. [3] 规划 PSD 分层
3. [4] 图片转 PSD
4. [5] 检查 PSD 文件
5. [6] 设计 Cubism 参数
6. [7] 物理设置建议
7. [8] Rigging 指导
8. [向导模式] 回到向导模式

你想做什么？
```

### 4.3 跳转和中断

**跳转到特定步骤:**
```
用户: 我想先做 PSD 质检
助手: 没问题！跳到步骤 5 - PSD 质检。

请上传你的 PSD 文件，我会帮你检查是否符合 Live2D 规范。
```

**跳过步骤:**
```
用户: 跳过此步
助手: 好的，跳过步骤 1。

你已经有立绘了吗？请上传，或者说"下一步"继续。
```

---

## 5. 文件组织

### 5.1 项目结构

```
live2d-master-agent/
├── SKILL.md                          # 技能定义（更新）
├── README.md                         # 项目说明
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-05-19-live2d-master-skill-design.md  # 本文档
├── lib/                              # 新增：核心库
│   ├── types.ts                      # 类型定义
│   ├── workflow.ts                   # 工作流协调器
│   ├── session-manager.ts            # 会话管理
│   └── steps/
│       ├── index.ts                  # 步骤模块导出
│       ├── 01-concept.ts
│       ├── 02-image-gen.ts
│       ├── 03-psd-plan.ts
│       ├── 04-image-to-psd.ts
│       ├── 05-qa.ts
│       ├── 06-params.ts
│       ├── 07-physics.ts
│       └── 08-rigging.ts
├── prompts/                          # 已有：提示词
│   ├── image_generation.md
│   ├── split.md
│   ├── rigging.md
│   ├── physics.md
│   ├── qa.md
│   └── naming.md
├── templates/                        # 已有：模板
│   ├── psd_structure.md
│   ├── cubism_params.md
│   └── export_rules.md
├── examples/                         # 已有：示例
│   ├── anime_girl_case.md
│   ├── vtuber_case.md
│   ├── hair_split_case.md
│   └── image_generation_examples.md
├── scripts/                          # 已有：Python 脚本
│   ├── auto_naming.py
│   ├── layer_checker.py
│   ├── physics_helper.py
│   └── seedream_image_generate.py
├── comfyui-connector/                # 已有：ComfyUI 连接器
│   └── src/index.ts
└── web/                              # 已有：Web 界面
    ├── components/
    │   ├── UploadArea.tsx            # 已有
    │   ├── ImageToPsd.tsx            # 已有
    │   ├── QAResultPanel.tsx         # 已有
    │   ├── ChatAssistant.tsx         # 已有
    │   └── WorkflowTracker.tsx       # 新增：进度跟踪组件
    ├── lib/
    │   ├── psd-parser.ts             # 已有
    │   ├── qa-engine.ts              # 已有
    │   └── image-to-psd.ts           # 已有
    └── pages/index.tsx               # 已有（更新）
```

### 5.2 输出文件

所有生成的文件保存到 `output/` 目录，按项目组织：
```
output/
└── {project-name}/
    ├── concept.md
    ├── character.png
    ├── psd-plan.md
    ├── character.psd
    ├── qa-report.md
    ├── cubism-params.md
    ├── physics-config.json
    └── rigging-guide.md
```

---

## 6. Web 界面增强

### 6.1 新增组件：WorkflowTracker

显示当前进度：
- 8 个步骤的可视化进度条
- 当前步骤高亮显示
- 已完成步骤打钩
- 点击步骤可以跳转（在专家模式下）

### 6.2 增强主页面

在 `web/pages/index.tsx` 中添加：
- 工作流状态展示区
- 快捷上传区
- 输出文件浏览器
- 与 Trae 对话的集成入口

---

## 7. 实施优先级

### Phase 1: 核心基础
- 更新 `SKILL.md`
- 创建类型定义 (`types.ts`)
- 实现会话管理 (`session-manager.ts`)
- 实现工作流协调器 (`workflow.ts`)

### Phase 2: 步骤实现
- 步骤 1-8 的各个模块
- 整合现有提示词和模板
- 连接现有 Python 脚本

### Phase 3: Web 增强
- 创建 `WorkflowTracker` 组件
- 更新主页面
- 文件上传和预览优化

### Phase 4: 测试和优化
- 端到端测试
- 用户体验优化
- 文档完善

---

## 8. 成功标准

- ✅ 用户可以通过对话完成从概念到 Live2D 模型的完整流程
- ✅ 支持向导模式和专家模式自由切换
- ✅ 8 个步骤都有明确的输出和质量检查
- ✅ Web 界面作为辅助提供良好的文件处理体验
- ✅ 进度保存和恢复功能正常工作
- ✅ 完整的文档和示例

---

## 附录

### A. 快速参考命令

| 命令 | 功能 |
|------|------|
| "我想做一个 Live2D 模型" | 开始新的向导流程 |
| "下一步" / "继续" | 进入下一个步骤 |
| "跳过此步" | 跳过当前步骤 |
| "上一步" / "返回" | 回到上一个步骤 |
| "我想先做步骤 X" | 跳转到指定步骤 |
| "切换到专家模式" | 切换到专家模式 |
| "回到向导模式" | 切换回向导模式 |
| "保存进度" | 保存当前状态 |
| "查看进度" | 显示当前进度 |

### B. 相关资源

- 提示词：`prompts/` 目录
- 模板：`templates/` 目录
- 示例：`examples/` 目录
- Web 工具：`web/` 目录
