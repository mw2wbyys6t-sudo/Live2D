import { PSDLayer } from '../lib/psd-parser';

export interface LayerRule {
  id: string;
  name: string;
  category: string;
  severity: 'error' | 'warning' | 'info';
  description: string;
  check: (
    layers: PSDLayer[],
    psdWidth: number,
    psdHeight: number,
    colorMode?: number
  ) => LayerCheckResult;
}

export interface LayerCheckResult {
  passed: boolean;
  issues: LayerIssue[];
  suggestions: string[];
}

export interface LayerIssue {
  layer?: string;
  details: string;
  expected?: string;
  actual?: string;
}

export const CRITICAL_LAYERS = {
  neck_base: {
    patterns: [/^neck_base$/i, /^body_neck$/i],
    description: '颈部基础层',
    required: true,
  },
  face_base: {
    patterns: [/^face_base$/i],
    description: '脸部基础层',
    required: true,
  },
  face_shadow: {
    patterns: [/^face_shadow$/i, /^face_shade$/i],
    description: '脸部阴影层',
    required: true,
  },
  hair_back: {
    patterns: [/^hair_back/i, /^back_hair/i],
    description: '后发层',
    required: true,
  },
};

export const MOUTH_SHAPES = ['a', 'i', 'u', 'e', 'o'];

export const SYMMETRY_PAIRS = [
  { left: /^eye_l/i, right: /^eye_r/i, name: '眼睛' },
  { left: /^eyebrow_l/i, right: /^eyebrow_r/i, name: '眉毛' },
  { left: /^arm_l/i, right: /^arm_r/i, name: '手臂' },
  { left: /^leg_l/i, right: /^leg_r/i, name: '腿' },
  { left: /^ear_l/i, right: /^ear_r/i, name: '耳朵' },
  { left: /^hand_l/i, right: /^hand_r/i, name: '手' },
];

export const LIVE2D_NAMING_PATTERNS = [
  /^hair_front_\d+$/i,
  /^hair_back_\d+$/i,
  /^hair_side_\d+$/i,
  /^hair_top_\d+$/i,
  /^hair_\w+_\d+$/i,
  /^face_base$/i,
  /^face_shadow$/i,
  /^face_\w+$/i,
  /^eye_[lr]_\w+$/i,
  /^eye_[lr]$/i,
  /^eyebrow_[lr]_\w+$/i,
  /^eyebrow_[lr]$/i,
  /^mouth_base$/i,
  /^mouth_[aiueo]$/i,
  /^mouth_\w+$/i,
  /^nose_\w*$/i,
  /^neck_base$/i,
  /^body_\w*$/i,
  /^body_\w+_\d+$/i,
  /^skirt_\w*$/i,
  /^skirt_\w+_\d+$/i,
  /^arm_[lr]_\w*$/i,
  /^arm_[lr]_\w+_\d+$/i,
  /^leg_[lr]_\w*$/i,
  /^hand_[lr]_\w*$/i,
  /^accessory_\w+$/i,
  /^accessory_\w+_\d+$/i,
  /^ribbon_\w*$/i,
  /^ribbon_\w+_\d+$/i,
  /^bow_\w*$/i,
  /^bow_\w+_\d+$/i,
  /^tail_\w*$/i,
  /^ear_[lr]_\w*$/i,
  /^ear_[lr]$/i,
];
