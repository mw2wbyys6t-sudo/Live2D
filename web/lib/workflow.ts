export type WorkflowStep = string;

export const WORKFLOW_STEPS: WorkflowStep[] = [
  'upload',
  'analyze',
  'review',
  'export',
];

export const STEP_DISPLAY_NAMES: Record<WorkflowStep, string> = {
  upload: '上传文件',
  analyze: '分析检测',
  review: '查看报告',
  export: '导出结果',
};

interface WorkflowState {
  currentStep: WorkflowStep;
  completedSteps: WorkflowStep[];
  mode: 'wizard' | 'expert';
}

export class Live2DWorkflow {
  private state: WorkflowState;

  constructor() {
    this.state = {
      currentStep: WORKFLOW_STEPS[0],
      completedSteps: [],
      mode: 'wizard',
    };
  }

  getState(): WorkflowState {
    return { ...this.state };
  }

  reset(): void {
    this.state = {
      currentStep: WORKFLOW_STEPS[0],
      completedSteps: [],
      mode: 'wizard',
    };
  }

  goToStep(step: WorkflowStep): void {
    if (WORKFLOW_STEPS.includes(step)) {
      this.state.currentStep = step;
    }
  }

  markStepComplete(): void {
    if (!this.state.completedSteps.includes(this.state.currentStep)) {
      this.state.completedSteps.push(this.state.currentStep);
    }
  }

  nextStep(): void {
    const currentIndex = WORKFLOW_STEPS.indexOf(this.state.currentStep);
    if (currentIndex < WORKFLOW_STEPS.length - 1) {
      this.state.currentStep = WORKFLOW_STEPS[currentIndex + 1];
    }
  }

  switchToExpert(): void {
    this.state.mode = 'expert';
  }

  switchToWizard(): void {
    this.state.mode = 'wizard';
  }
}
