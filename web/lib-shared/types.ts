export type WorkflowMode = 'wizard' | 'expert';

export interface CharacterConcept {
  type: 'vtuber' | 'anime-girl' | 'chibi' | 'other';
  features: string[];
  style: 'cute' | 'elegant' | 'cool' | 'other';
  description: string;
}

export interface PsdLayer {
  name: string;
  group?: string;
  drawOrder: number;
  description: string;
}

export interface PsdLayerPlan {
  layers: PsdLayer[];
  recommendations: string[];
}

export interface QAIssue {
  severity: 'error' | 'warning' | 'info';
  message: string;
  suggestion: string;
}

export interface QAReport {
  issues: QAIssue[];
  overallScore: number;
  passed: boolean;
}

export interface CubismParam {
  name: string;
  min: number;
  max: number;
  default: number;
  description: string;
}

export interface CubismParamConfig {
  parameters: CubismParam[];
}

export interface PhysicsPart {
  name: string;
  gravity: number;
  wind: number;
  restitution: number;
  damping: number;
}

export interface PhysicsConfig {
  parts: PhysicsPart[];
}

export interface RiggingGuide {
  steps: string[];
  tips: string[];
  bestPractices: string[];
}

export interface UserPreferences {
  style: string;
  defaultParams: Record<string, any>;
}

export interface WorkflowArtifacts {
  concept?: CharacterConcept;
  characterImage?: string;
  psdPlan?: PsdLayerPlan;
  psdFile?: string;
  qaReport?: QAReport;
  cubismParams?: CubismParamConfig;
  physicsConfig?: PhysicsConfig;
  riggingGuide?: RiggingGuide;
}

export interface Live2DWorkflowState {
  mode: WorkflowMode;
  currentStep: number;
  completed: boolean[];
  artifacts: WorkflowArtifacts;
  preferences?: UserPreferences;
}

export const STEP_NAMES = [
  '概念设定',
  '立绘生成',
  'PSD 分层规划',
  '图片转 PSD',
  'PSD 质检',
  'Cubism 参数设计',
  '物理设置',
  'Rigging 指导'
] as const;

export type WorkflowStepNumber = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8;
