import { 
  Live2DWorkflowState, 
  WorkflowMode,
  STEP_NAMES,
  CharacterConcept,
  PsdLayerPlan,
  QAReport,
  CubismParamConfig,
  PhysicsConfig,
  RiggingGuide
} from './types';

export class Live2DWorkflow {
  private state: Live2DWorkflowState;

  constructor(initialState?: Partial<Live2DWorkflowState>) {
    this.state = {
      mode: 'wizard',
      currentStep: 1,
      completed: [false, false, false, false, false, false, false, false],
      artifacts: {},
      ...initialState
    };
  }

  getState(): Live2DWorkflowState {
    return { ...this.state };
  }

  getCurrentStep(): number {
    return this.state.currentStep;
  }

  getMode(): WorkflowMode {
    return this.state.mode;
  }

  getCurrentStepName(): string {
    return STEP_NAMES[this.state.currentStep - 1] || '';
  }

  switchToWizard(): void {
    this.state.mode = 'wizard';
  }

  switchToExpert(): void {
    this.state.mode = 'expert';
  }

  nextStep(): void {
    if (this.state.currentStep < 8) {
      this.state.currentStep++;
    }
  }

  prevStep(): void {
    if (this.state.currentStep > 1) {
      this.state.currentStep--;
    }
  }

  goToStep(step: number): void {
    if (step >= 1 && step <= 8) {
      this.state.currentStep = step;
    }
  }

  skipStep(): void {
    this.state.completed[this.state.currentStep - 1] = true;
    if (this.state.currentStep < 8) {
      this.state.currentStep++;
    }
  }

  markStepComplete(step: number): void {
    if (step >= 1 && step <= 8) {
      this.state.completed[step - 1] = true;
    }
  }

  markCurrentStepComplete(): void {
    this.markStepComplete(this.state.currentStep);
  }

  isStepComplete(step: number): boolean {
    return this.state.completed[step - 1] || false;
  }

  getProgress(): { completed: number; total: number } {
    const completed = this.state.completed.filter(c => c).length;
    return { completed, total: 8 };
  }

  setConcept(concept: CharacterConcept): void {
    this.state.artifacts.concept = concept;
  }

  setCharacterImage(imagePath: string): void {
    this.state.artifacts.characterImage = imagePath;
  }

  setPsdPlan(plan: PsdLayerPlan): void {
    this.state.artifacts.psdPlan = plan;
  }

  setPsdFile(filePath: string): void {
    this.state.artifacts.psdFile = filePath;
  }

  setQAReport(report: QAReport): void {
    this.state.artifacts.qaReport = report;
  }

  setCubismParams(params: CubismParamConfig): void {
    this.state.artifacts.cubismParams = params;
  }

  setPhysicsConfig(config: PhysicsConfig): void {
    this.state.artifacts.physicsConfig = config;
  }

  setRiggingGuide(guide: RiggingGuide): void {
    this.state.artifacts.riggingGuide = guide;
  }

  reset(): void {
    this.state = {
      mode: 'wizard',
      currentStep: 1,
      completed: [false, false, false, false, false, false, false, false],
      artifacts: {}
    };
  }

  parseCommand(input: string): { action: string; params?: any } {
    const lower = input.toLowerCase().trim();
    
    if (lower.includes('下一步') || lower.includes('继续') || lower === 'next') {
      return { action: 'nextStep' };
    }
    if (lower.includes('上一步') || lower.includes('返回') || lower === 'prev') {
      return { action: 'prevStep' };
    }
    if (lower.includes('跳过') || lower === 'skip') {
      return { action: 'skipStep' };
    }
    if (lower.includes('专家模式') || lower.includes('expert')) {
      return { action: 'switchToExpert' };
    }
    if (lower.includes('向导模式') || lower.includes('wizard')) {
      return { action: 'switchToWizard' };
    }
    if (lower.includes('重置') || lower.includes('重新开始') || lower === 'reset') {
      return { action: 'reset' };
    }
    if (lower.includes('查看进度') || lower.includes('进度')) {
      return { action: 'showProgress' };
    }
    
    const stepMatch = lower.match(/步骤?\s*(\d+)/);
    if (stepMatch) {
      return { action: 'goToStep', params: { step: parseInt(stepMatch[1]) } };
    }
    
    return { action: 'input', params: { value: input } };
  }

  getWizardPrompt(): string {
    const step = this.state.currentStep;
    const stepName = this.getCurrentStepName();
    
    const prompts: Record<number, string> = {
      1: `[步骤 1/8] ${stepName}\n\n请告诉我：\n1. 角色类型（VTuber/动漫女孩/Q版/其他）\n2. 主要特征（发型、发色、服装风格等）\n3. 整体氛围（可爱/优雅/酷/其他）\n\n或者说"跳过此步"如果你已经有立绘了。`,
      2: `[步骤 2/8] ${stepName}\n\n请描述你想要的立绘风格，或者上传参考图片。我会帮你生成适合 Live2D 的角色立绘。`,
      3: `[步骤 3/8] ${stepName}\n\n请上传你的角色立绘，我会帮你规划完整的 PSD 图层结构。`,
      4: `[步骤 4/8] ${stepName}\n\n请上传你的角色图片，我会帮你转换成基本的分层 PSD。`,
      5: `[步骤 5/8] ${stepName}\n\n请上传你的 PSD 文件，我会检查是否符合 Live2D 规范。`,
      6: `[步骤 6/8] ${stepName}\n\n我会根据你的 PSD 设计 Cubism 参数配置。`,
      7: `[步骤 7/8] ${stepName}\n\n请告诉我角色的动态部件（头发长度、是否有耳朵/尾巴等），我会提供物理参数建议。`,
      8: `[步骤 8/8] ${stepName}\n\n我会提供完整的 Rigging 操作指南！`
    };
    
    return prompts[step] || '请告诉我你想做什么。';
  }

  getExpertPrompt(): string {
    const progress = this.getProgress();
    let progressText = '当前进度：\n';
    STEP_NAMES.forEach((name, i) => {
      const done = this.state.completed[i] ? '✓' : ' ';
      progressText += `- [${done}] 步骤 ${i + 1}: ${name}\n`;
    });
    
    return `已切换到专家模式。🔧\n\n${progressText}\n可用任务：\n1. [2] 生成角色立绘\n2. [3] 规划 PSD 分层\n3. [4] 图片转 PSD\n4. [5] 检查 PSD 文件\n5. [6] 设计 Cubism 参数\n6. [7] 物理设置建议\n7. [8] Rigging 指导\n8. [向导模式] 回到向导模式\n\n你想做什么？`;
  }
}

export const createWorkflow = (initialState?: Partial<Live2DWorkflowState>) => {
  return new Live2DWorkflow(initialState);
};
