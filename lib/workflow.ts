export type WorkflowMode = 'wizard' | 'expert';

export type WorkflowStep = 
  | 'concept'
  | 'character-image'
  | 'psd-plan'
  | 'pose-design'
  | 'texture-settings'
  | 'rigging'
  | 'physics'
  | 'expression'
  | 'preview'
  | 'export';

export interface WorkflowState {
  mode: WorkflowMode;
  currentStep: WorkflowStep;
  completedSteps: Set<WorkflowStep>;
  concept?: string;
  characterImage?: string;
  psdPlan?: string;
  poseDesign?: string;
  textureSettings?: string;
  rigging?: string;
  physics?: string;
  expression?: string;
}

export const WORKFLOW_STEPS: WorkflowStep[] = [
  'concept',
  'character-image',
  'psd-plan',
  'pose-design',
  'texture-settings',
  'rigging',
  'physics',
  'expression',
  'preview',
  'export'
];

export const STEP_DISPLAY_NAMES: Record<WorkflowStep, string> = {
  'concept': '概念设计',
  'character-image': '角色立绘',
  'psd-plan': 'PSD规划',
  'pose-design': '姿势设计',
  'texture-settings': '纹理设置',
  'rigging': '绑定设置',
  'physics': '物理效果',
  'expression': '表情制作',
  'preview': '预览调试',
  'export': '导出发布'
};

export class Live2DWorkflow {
  private state: WorkflowState;

  constructor() {
    this.state = {
      mode: 'wizard',
      currentStep: 'concept',
      completedSteps: new Set()
    };
  }

  getState(): WorkflowState {
    return {
      ...this.state,
      completedSteps: new Set(this.state.completedSteps)
    };
  }

  getCurrentStep(): WorkflowStep {
    return this.state.currentStep;
  }

  getMode(): WorkflowMode {
    return this.state.mode;
  }

  switchToWizard(): void {
    this.state.mode = 'wizard';
  }

  switchToExpert(): void {
    this.state.mode = 'expert';
  }

  nextStep(): WorkflowStep {
    const currentIndex = WORKFLOW_STEPS.indexOf(this.state.currentStep);
    if (currentIndex < WORKFLOW_STEPS.length - 1) {
      this.state.currentStep = WORKFLOW_STEPS[currentIndex + 1];
    }
    return this.state.currentStep;
  }

  prevStep(): WorkflowStep {
    const currentIndex = WORKFLOW_STEPS.indexOf(this.state.currentStep);
    if (currentIndex > 0) {
      this.state.currentStep = WORKFLOW_STEPS[currentIndex - 1];
    }
    return this.state.currentStep;
  }

  goToStep(step: WorkflowStep): void {
    if (WORKFLOW_STEPS.includes(step)) {
      this.state.currentStep = step;
    } else {
      throw new Error(`Invalid step: ${step}`);
    }
  }

  skipStep(): WorkflowStep {
    return this.nextStep();
  }

  markStepComplete(step?: WorkflowStep): void {
    const targetStep = step ?? this.state.currentStep;
    if (WORKFLOW_STEPS.includes(targetStep)) {
      this.state.completedSteps.add(targetStep);
    } else {
      throw new Error(`Invalid step: ${targetStep}`);
    }
  }

  isStepComplete(step: WorkflowStep): boolean {
    return this.state.completedSteps.has(step);
  }

  getProgress(): number {
    return (this.state.completedSteps.size / WORKFLOW_STEPS.length) * 100;
  }

  setConcept(concept: string): void {
    this.state.concept = concept;
  }

  setCharacterImage(imagePath: string): void {
    this.state.characterImage = imagePath;
  }

  setPsdPlan(plan: string): void {
    this.state.psdPlan = plan;
  }

  setPoseDesign(design: string): void {
    this.state.poseDesign = design;
  }

  setTextureSettings(settings: string): void {
    this.state.textureSettings = settings;
  }

  setRigging(rigging: string): void {
    this.state.rigging = rigging;
  }

  setPhysics(physics: string): void {
    this.state.physics = physics;
  }

  setExpression(expression: string): void {
    this.state.expression = expression;
  }

  parseCommand(command: string): { action: string; params?: Record<string, string> } {
    const parts = command.trim().toLowerCase().split(/\s+/);
    if (parts.length === 0) {
      throw new Error('Empty command');
    }

    const action = parts[0];
    const params: Record<string, string> = {};

    for (let i = 1; i < parts.length; i++) {
      const part = parts[i];
      if (part.includes('=')) {
        const [key, value] = part.split('=');
        params[key] = value;
      }
    }

    return { action, params };
  }

  getWizardPrompt(): string {
    const currentStep = this.state.currentStep;
    const stepName = STEP_DISPLAY_NAMES[currentStep];
    const progress = Math.round(this.getProgress());

    const prompts: Record<WorkflowStep, string> = {
      'concept': `当前步骤：${stepName} (进度 ${progress}%)\n\n请描述您想要创建的 Live2D 角色概念，包括：\n- 角色类型（如少女、动物、幻想生物等）\n- 风格特点（可爱、写实、赛博朋克等）\n- 服装和配饰\n- 性格特点\n- 其他特殊要求`,
      'character-image': `当前步骤：${stepName} (进度 ${progress}%)\n\n请提供角色立绘图片，或描述立绘的具体要求：\n- 姿势角度\n- 色彩方案\n- 分辨率要求\n- 是否需要参考图`,
      'psd-plan': `当前步骤：${stepName} (进度 ${progress}%)\n\n请提供 PSD 分层规划方案：\n- 图层结构设计\n- 可动部分划分\n- 表情图层规划\n- 服装分层方案`,
      'pose-design': `当前步骤：${stepName} (进度 ${progress}%)\n\n请设计角色姿势：\n- 默认站姿\n- 常用动作（眨眼、微笑等）\n- 特殊姿势需求\n- 骨骼绑定要点`,
      'texture-settings': `当前步骤：${stepName} (进度 ${progress}%)\n\n请设置纹理参数：\n- 纹理分辨率\n- UV 展开方式\n- 材质属性\n- 光影效果`,
      'rigging': `当前步骤：${stepName} (进度 ${progress}%)\n\n请配置绑定参数：\n- 骨骼结构\n- 权重分配\n- 变形器设置\n- 面部追踪`,
      'physics': `当前步骤：${stepName} (进度 ${progress}%)\n\n请设置物理效果：\n- 头发摆动\n- 衣服褶皱\n- 饰品晃动\n- 物理参数调优`,
      'expression': `当前步骤：${stepName} (进度 ${progress}%)\n\n请设计表情系统：\n- 基础表情（喜、怒、哀、乐）\n- 特殊表情\n- 表情切换方式\n- 口型同步`,
      'preview': `当前步骤：${stepName} (进度 ${progress}%)\n\n请预览并调试：\n- 动作流畅度\n- 表情自然度\n- 物理效果\n- 性能优化`,
      'export': `当前步骤：${stepName} (进度 ${progress}%)\n\n请选择导出格式：\n- Live2D Model (.model3.json)\n- Unity 包\n- Unreal 包\n- 其他格式需求`
    };

    return prompts[currentStep] || `当前步骤：${stepName}`;
  }

  getExpertPrompt(): string {
    const currentStep = this.state.currentStep;
    const stepName = STEP_DISPLAY_NAMES[currentStep];
    const progress = Math.round(this.getProgress());
    const completedSteps = Array.from(this.state.completedSteps).map(s => STEP_DISPLAY_NAMES[s]).join(', ');

    return `【专家模式】当前步骤：${stepName} (进度 ${progress}%)

已完成步骤：${completedSteps || '无'}

可用命令：
- next / prev / goto <步骤名> - 步骤导航
- complete - 标记当前步骤完成
- set <属性>=<值> - 设置属性
- mode wizard/expert - 切换模式
- progress - 查看进度
- state - 查看状态

当前可设置属性：
${!this.state.concept ? '- concept: 角色概念描述' : ''}
${!this.state.characterImage ? '- characterImage: 立绘图片路径' : ''}
${!this.state.psdPlan ? '- psdPlan: PSD规划方案' : ''}
${!this.state.poseDesign ? '- poseDesign: 姿势设计' : ''}
${!this.state.textureSettings ? '- textureSettings: 纹理设置' : ''}
${!this.state.rigging ? '- rigging: 绑定设置' : ''}
${!this.state.physics ? '- physics: 物理效果设置' : ''}
${!this.state.expression ? '- expression: 表情设置' : ''}

请输入命令或直接提供${stepName}的相关内容...`;
  }

  reset(): void {
    this.state = {
      mode: 'wizard',
      currentStep: 'concept',
      completedSteps: new Set()
    };
  }

  canProceed(): boolean {
    const step = this.state.currentStep;
    const requiredData: Record<WorkflowStep, string | undefined> = {
      'concept': this.state.concept,
      'character-image': this.state.characterImage,
      'psd-plan': this.state.psdPlan,
      'pose-design': this.state.poseDesign,
      'texture-settings': this.state.textureSettings,
      'rigging': this.state.rigging,
      'physics': this.state.physics,
      'expression': this.state.expression,
      'preview': undefined,
      'export': undefined
    };

    if (this.state.mode === 'wizard') {
      return requiredData[step] !== undefined && requiredData[step] !== '';
    }
    return true;
  }

  getNextAvailableSteps(): WorkflowStep[] {
    if (this.state.mode === 'expert') {
      return WORKFLOW_STEPS.filter(s => s !== this.state.currentStep);
    }
    const currentIndex = WORKFLOW_STEPS.indexOf(this.state.currentStep);
    return currentIndex < WORKFLOW_STEPS.length - 1 
      ? [WORKFLOW_STEPS[currentIndex + 1]] 
      : [];
  }
}
