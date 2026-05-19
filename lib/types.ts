export type WorkflowMode = 'create' | 'edit' | 'export' | 'preview' | 'debug';

export interface CharacterConcept {
  id: string;
  name: string;
  gender: 'male' | 'female' | 'neutral';
  style: 'anime' | 'manga' | 'cartoon' | 'realistic' | 'chibi';
  ageRange: 'child' | 'teen' | 'young_adult' | 'adult';
  expression: 'default' | 'happy' | 'sad' | 'angry' | 'surprised' | 'sleepy';
  accessories: string[];
  description: string;
  referenceImages: string[];
  createdAt: Date;
  updatedAt: Date;
}

export interface PsdLayer {
  id: string;
  name: string;
  type: 'normal' | 'folder' | 'smart_object';
  path: string;
  visible: boolean;
  locked: boolean;
  opacity: number;
  blendMode: string;
  width: number;
  height: number;
  x: number;
  y: number;
  children?: PsdLayer[];
}

export interface PsdLayerPlan {
  id: string;
  characterId: string;
  originalPsdPath: string;
  layers: PsdLayer[];
  layerMapping: Record<string, string>;
  version: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface QAIssue {
  id: string;
  type: 'critical' | 'warning' | 'info';
  category: 'layer_naming' | 'layer_structure' | 'draw_order' | 'transparency' | 'empty_layer' | 'missing_layer' | 'duplicate_layer';
  message: string;
  layerPath?: string;
  layerId?: string;
  suggestion: string;
  severity: number;
}

export interface QAReport {
  id: string;
  psdLayerPlanId: string;
  issues: QAIssue[];
  totalIssues: number;
  criticalCount: number;
  warningCount: number;
  infoCount: number;
  score: number;
  generatedAt: Date;
}

export interface CubismParam {
  id: string;
  name: string;
  type: 'bool' | 'float' | 'int';
  default: number;
  min: number;
  max: number;
  key: string;
}

export interface CubismParamConfig {
  id: string;
  characterId: string;
  parameters: CubismParam[];
  parameterGroups: {
    id: string;
    name: string;
    paramIds: string[];
  }[];
  version: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface PhysicsParticle {
  id: string;
  name: string;
  x: number;
  y: number;
  size: number;
  gravity: number;
  friction: number;
  stiffness: number;
}

export interface PhysicsConfig {
  id: string;
  characterId: string;
  particles: PhysicsParticle[];
  constraints: {
    id: string;
    from: string;
    to: string;
    stiffness: number;
  }[];
  settings: {
    windEnabled: boolean;
    windForce: number;
    gravityEnabled: boolean;
    gravityForce: number;
  };
  version: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface RiggingBone {
  id: string;
  name: string;
  parentId?: string;
  x: number;
  y: number;
  angle: number;
  scaleX: number;
  scaleY: number;
  length: number;
}

export interface RiggingGuide {
  id: string;
  characterId: string;
  bones: RiggingBone[];
  boneGroups: {
    id: string;
    name: string;
    boneIds: string[];
  }[];
  ikChains: {
    id: string;
    name: string;
    boneIds: string[];
    targetX: number;
    targetY: number;
  }[];
  version: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface UserPreferences {
  id: string;
  userId: string;
  defaultWorkflowMode: WorkflowMode;
  theme: 'light' | 'dark' | 'system';
  language: 'zh-CN' | 'en-US' | 'ja-JP';
  autoSaveEnabled: boolean;
  autoSaveInterval: number;
  showHiddenLayers: boolean;
  showGrid: boolean;
  snapToGrid: boolean;
  gridSize: number;
  defaultExportFormat: 'png' | 'jpg' | 'webp' | 'gif';
  exportQuality: number;
  createdAt: Date;
  updatedAt: Date;
}

export type WorkflowStep = 'concept' | 'psd_import' | 'layer_analysis' | 'qa_check' | 'rigging' | 'physics' | 'preview' | 'export';

export interface Live2DWorkflowState {
  id: string;
  characterId: string;
  currentStep: WorkflowStep;
  completedSteps: WorkflowStep[];
  isDirty: boolean;
  lastSavedAt: Date;
  createdAt: Date;
  updatedAt: Date;
}

export const STEP_NAMES: Record<WorkflowStep, string> = {
  concept: '角色概念设计',
  psd_import: 'PSD导入',
  layer_analysis: '图层分析',
  qa_check: 'QA检查',
  rigging: '骨骼绑定',
  physics: '物理设置',
  preview: '预览',
  export: '导出',
};
