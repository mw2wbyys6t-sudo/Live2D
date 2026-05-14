import { PSDFileInfo, PSDLayer } from './psd-parser';

// ============================================================
// 类型定义
// ============================================================

export interface QAIssue {
  id: string;
  severity: 'error' | 'warning' | 'info';
  category: IssueCategory;
  title: string;
  description: string;
  layer?: string;
  suggestion: string;
  rule: string;
}

export type IssueCategory =
  | 'naming'
  | 'structure'
  | 'visibility'
  | 'bounds'
  | 'symmetry'
  | 'completeness'
  | 'performance'
  | 'convention';

export interface QAScore {
  total: number;
  naming: number;
  structure: number;
  completeness: number;
  convention: number;
}

export interface QAResult {
  score: QAScore;
  issues: QAIssue[];
  suggestions: string[];
  summary: {
    totalLayers: number;
    visibleLayers: number;
    hiddenLayers: number;
    groups: number;
    hasMissingCritical: boolean;
    hasNamingIssues: boolean;
    hasStructuralIssues: boolean;
  };
}

// ============================================================
// Live2D 命名规范
// ============================================================

const LIVE2D_LAYER_PATTERNS = [
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

const CRITICAL_LAYERS = [
  { name: 'face_base', description: '脸部基础层' },
  { name: 'face_shadow', description: '脸部阴影层' },
];

const EYE_LAYERS = [
  { pattern: /^eye_[lr]/i, description: '眼睛层（左右配对）' },
];

const MOUTH_LAYERS = [
  { pattern: /^mouth_[aiueo]/i, description: '嘴型层（a/i/u/e/o）' },
];

const HAIR_LAYERS = [
  { pattern: /^hair_front_\d+/i, description: '前发层' },
  { pattern: /^hair_back_\d+/i, description: '后发层' },
  { pattern: /^hair_side_\d+/i, description: '侧发层' },
];

const SYMMETRY_PAIRS = [
  { left: /^eye_l/i, right: /^eye_r/i, name: '眼睛' },
  { left: /^eyebrow_l/i, right: /^eyebrow_r/i, name: '眉毛' },
  { left: /^arm_l/i, right: /^arm_r/i, name: '手臂' },
  { left: /^leg_l/i, right: /^leg_r/i, name: '腿' },
  { left: /^ear_l/i, right: /^ear_r/i, name: '耳朵' },
  { left: /^hand_l/i, right: /^hand_r/i, name: '手' },
];

// ============================================================
// QA 引擎核心
// ============================================================

export class QAEngine {
  private issues: QAIssue[] = [];
  private suggestions: Set<string> = new Set();
  private psd: PSDFileInfo;

  constructor(psd: PSDFileInfo) {
    this.psd = psd;
  }

  analyze(): QAResult {
    this.issues = [];
    this.suggestions = new Set();

    if (!this.psd.valid) {
      this.addIssue({
        id: 'psd_invalid',
        severity: 'error',
        category: 'structure',
        title: 'PSD 文件无效',
        description: this.psd.error || '无法解析 PSD 文件',
        suggestion: '请确保上传有效的 PSD 文件',
        rule: 'PSD-001',
      });
      return this.buildResult();
    }

    this.checkNamingConvention();
    this.checkCriticalLayers();
    this.checkEyeSymmetry();
    this.checkMouthCompleteness();
    this.checkHairStructure();
    this.checkLayerVisibility();
    this.checkLayerBounds();
    this.checkSymmetryPairs();
    this.checkCanvasSize();
    this.checkLayerDepth();
    this.checkBlendModes();
    this.checkOpacity();
    this.checkEmptyLayers();
    this.checkDuplicateNames();
    this.checkColorMode();

    return this.buildResult();
  }

  // ============================================================
  // 检查规则
  // ============================================================

  private checkNamingConvention() {
    let namedCount = 0;
    let unnamedCount = 0;

    for (const layer of this.psd.layers) {
      const isStandard = LIVE2D_LAYER_PATTERNS.some(p => p.test(layer.name.trim()));

      if (!isStandard) {
        unnamedCount++;
        this.addIssue({
          id: `naming_${layer.index}`,
          severity: 'warning',
          category: 'naming',
          title: '图层命名不规范',
          description: `图层 "${layer.name}" 不符合 Live2D 命名规范`,
          layer: layer.name,
          suggestion: `建议重命名为标准格式，例如: hair_front_01, face_base, eye_l_white`,
          rule: 'Naming-001',
        });
      } else {
        namedCount++;
      }
    }

    if (unnamedCount > 0) {
      this.suggestions.add(`将 ${unnamedCount} 个不规范图层重命名为 Live2D 标准格式`);
    }

    if (namedCount === 0 && this.psd.layers.length > 0) {
      this.addIssue({
        id: 'naming_all',
        severity: 'error',
        category: 'naming',
        title: '所有图层命名不规范',
        description: '没有图层符合 Live2D 命名规范，将导致 Cubism 导入困难',
        suggestion: '建议按照 Live2D PSD 命名规范重新命名所有图层',
        rule: 'Naming-002',
      });
    }
  }

  private checkCriticalLayers() {
    const layerNames = this.psd.layers.map(l => l.name.toLowerCase().trim());
    const layerSet = new Set(layerNames);

    for (const critical of CRITICAL_LAYERS) {
      if (!layerSet.has(critical.name)) {
        this.addIssue({
          id: `missing_${critical.name}`,
          severity: 'error',
          category: 'completeness',
          title: `缺少关键图层: ${critical.name}`,
          description: `${critical.description}（${critical.name}）未找到，可能导致脸部绑定问题`,
          suggestion: `请添加 "${critical.name}" 图层，这是 Live2D 绑定的必需图层`,
          rule: 'Critical-001',
        });
      }
    }
  }

  private checkEyeSymmetry() {
    const leftEyes = this.psd.layers.filter(l => /^eye_l/i.test(l.name.trim()));
    const rightEyes = this.psd.layers.filter(l => /^eye_r/i.test(l.name.trim()));

    if (leftEyes.length === 0 && rightEyes.length === 0) {
      this.addIssue({
        id: 'eyes_missing',
        severity: 'warning',
        category: 'completeness',
        title: '缺少眼睛图层',
        description: '未检测到眼睛图层（eye_l / eye_r）',
        suggestion: '建议添加左右眼睛图层，并按照 eye_l_* / eye_r_* 格式命名',
        rule: 'Eye-001',
      });
      return;
    }

    if (leftEyes.length !== rightEyes.length) {
      this.addIssue({
        id: 'eyes_asymmetric_count',
        severity: 'error',
        category: 'symmetry',
        title: '眼睛图层数量不对称',
        description: `左眼 ${leftEyes.length} 层，右眼 ${rightEyes.length} 层`,
        layer: leftEyes[0]?.name || rightEyes[0]?.name,
        suggestion: '左右眼睛的图层结构应完全对称',
        rule: 'Eye-002',
      });
    }

    const leftNames = new Set(leftEyes.map(l => l.name.replace(/^eye_l/i, '').toLowerCase()));
    const rightNames = new Set(rightEyes.map(l => l.name.replace(/^eye_r/i, '').toLowerCase()));

    const missingInRight = [...leftNames].filter(n => n && !rightNames.has(n));
    if (missingInRight.length > 0) {
      this.addIssue({
        id: 'eyes_asymmetric_structure',
        severity: 'warning',
        category: 'symmetry',
        title: '眼睛子图层结构不对称',
        description: `右眼缺少子图层: ${missingInRight.join(', ')}`,
        suggestion: '左右眼睛的子图层结构必须完全一致',
        rule: 'Eye-003',
      });
    }
  }

  private checkMouthCompleteness() {
    const mouthShapes = ['a', 'i', 'u', 'e', 'o'];
    const foundShapes = new Set<string>();

    for (const layer of this.psd.layers) {
      const name = layer.name.trim().toLowerCase();
      for (const shape of mouthShapes) {
        if (name === `mouth_${shape}` || name.startsWith(`mouth_${shape}_`)) {
          foundShapes.add(shape);
        }
      }
    }

    if (foundShapes.size === 0) {
      const hasMouth = this.psd.layers.some(l => /^mouth/i.test(l.name.trim()));
      if (!hasMouth) {
        this.addIssue({
          id: 'mouth_missing',
          severity: 'warning',
          category: 'completeness',
          title: '缺少嘴型图层',
          description: '未检测到任何嘴型图层',
          suggestion: '建议添加 mouth_base 和 mouth_a/i/u/e/o 图层',
          rule: 'Mouth-001',
        });
      }
      return;
    }

    const missingShapes = mouthShapes.filter(s => !foundShapes.has(s));
    if (missingShapes.length > 0) {
      this.addIssue({
        id: 'mouth_incomplete',
        severity: 'warning',
        category: 'completeness',
        title: '嘴型不完整',
        description: `缺少嘴型: ${missingShapes.join(', ')}（应有 a/i/u/e/o）`,
        suggestion: `建议添加 mouth_${missingShapes.join(', mouth_')} 图层以支持完整的口型动画`,
        rule: 'Mouth-002',
      });
    }

    if (foundShapes.size >= 3) {
      this.suggestions.add(`嘴型图层完整（${foundShapes.size}/5），支持基础口型同步`);
    }
  }

  private checkHairStructure() {
    const hairLayers = this.psd.layers.filter(l =>
      /^hair_\w+/i.test(l.name.trim())
    );

    if (hairLayers.length === 0) {
      this.addIssue({
        id: 'hair_missing',
        severity: 'warning',
        category: 'completeness',
        title: '缺少头发图层',
        description: '未检测到头发图层（hair_front / hair_back / hair_side）',
        suggestion: '建议将头发拆分为前发、后发、侧发等多个图层',
        rule: 'Hair-001',
      });
      return;
    }

    const frontHair = hairLayers.filter(l => /^hair_front/i.test(l.name.trim()));
    const backHair = hairLayers.filter(l => /^hair_back/i.test(l.name.trim()));
    const sideHair = hairLayers.filter(l => /^hair_side/i.test(l.name.trim()));

    if (frontHair.length === 0) {
      this.addIssue({
        id: 'hair_no_front',
        severity: 'warning',
        category: 'structure',
        title: '缺少前发图层',
        description: '头发中没有前发（hair_front）分层',
        suggestion: '建议将前发独立分层，便于设置物理和参数',
        rule: 'Hair-002',
      });
    }

    if (backHair.length === 0) {
      this.addIssue({
        id: 'hair_no_back',
        severity: 'info',
        category: 'structure',
        title: '缺少后发图层',
        description: '头发中没有后发（hair_back）分层',
        suggestion: '建议将后发独立分层，避免遮挡身体',
        rule: 'Hair-003',
      });
    }

    if (frontHair.length >= 3) {
      this.suggestions.add(`前发有 ${frontHair.length} 层，建议为刘海设置独立物理`);
    }

    if (sideHair.length > 0) {
      this.suggestions.add('侧发建议绑定 ParamAngleZ 参数');
    }
  }

  private checkLayerVisibility() {
    const hiddenLayers = this.psd.layers.filter(l => !l.visible);

    if (hiddenLayers.length > 0) {
      this.addIssue({
        id: 'hidden_layers',
        severity: 'info',
        category: 'visibility',
        title: '存在隐藏图层',
        description: `有 ${hiddenLayers.length} 个图层被隐藏: ${hiddenLayers.slice(0, 5).map(l => l.name).join(', ')}${hiddenLayers.length > 5 ? '...' : ''}`,
        suggestion: '检查隐藏图层是否需要保留，隐藏图层在 Cubism 中可能不会被导入',
        rule: 'Visibility-001',
      });
    }
  }

  private checkLayerBounds() {
    const offscreenLayers = this.psd.layers.filter(l =>
      l.visible &&
      l.bounds.width > 0 &&
      l.bounds.height > 0 &&
      (l.bounds.right < 0 || l.bounds.bottom < 0 ||
       l.bounds.left > this.psd.width || l.bounds.top > this.psd.height)
    );

    if (offscreenLayers.length > 0) {
      this.addIssue({
        id: 'offscreen_layers',
        severity: 'warning',
        category: 'bounds',
        title: '图层超出画布边界',
        description: `${offscreenLayers.length} 个图层完全在画布外部: ${offscreenLayers.slice(0, 3).map(l => l.name).join(', ')}`,
        suggestion: '检查这些图层的位置，确保它们在画布范围内',
        rule: 'Bounds-001',
      });
    }

    const zeroSizeLayers = this.psd.layers.filter(l =>
      l.bounds.width === 0 && l.bounds.height === 0 && l.visible
    );

    if (zeroSizeLayers.length > 0) {
      this.addIssue({
        id: 'zero_size_layers',
        severity: 'warning',
        category: 'bounds',
        title: '存在空尺寸图层',
        description: `${zeroSizeLayers.length} 个可见图层尺寸为 0x0`,
        suggestion: '检查这些图层是否为空图层或像素数据丢失',
        rule: 'Bounds-002',
      });
    }
  }

  private checkSymmetryPairs() {
    for (const pair of SYMMETRY_PAIRS) {
      const leftLayers = this.psd.layers.filter(l => pair.left.test(l.name.trim()));
      const rightLayers = this.psd.layers.filter(l => pair.right.test(l.name.trim()));

      if (leftLayers.length === 0 && rightLayers.length === 0) continue;

      if (leftLayers.length === 0 || rightLayers.length === 0) {
        const side = leftLayers.length === 0 ? '左' : '右';
        this.addIssue({
          id: `symmetry_${pair.name}`,
          severity: 'error',
          category: 'symmetry',
          title: `${pair.name}缺少${side}侧`,
          description: `仅检测到${side === '左' ? '右' : '左'}侧${pair.name}图层`,
          suggestion: `${pair.name}需要左右对称，请添加缺失的${side}侧图层`,
          rule: 'Symmetry-001',
        });
      }
    }
  }

  private checkCanvasSize() {
    if (this.psd.width < 500 || this.psd.height < 500) {
      this.addIssue({
        id: 'canvas_small',
        severity: 'info',
        category: 'convention',
        title: '画布尺寸偏小',
        description: `画布尺寸为 ${this.psd.width}x${this.psd.height}，建议使用更大的画布`,
        suggestion: '建议画布尺寸至少 1024x1024 或更高分辨率',
        rule: 'Canvas-001',
      });
    }

    if (this.psd.width !== this.psd.height) {
      this.addIssue({
        id: 'canvas_not_square',
        severity: 'info',
        category: 'convention',
        title: '画布不是正方形',
        description: `画布尺寸为 ${this.psd.width}x${this.psd.height}`,
        suggestion: 'Live2D 通常使用正方形画布（如 1024x1024），方便后续绑定',
        rule: 'Canvas-002',
      });
    }
  }

  private checkLayerDepth() {
    const maxDepth = Math.max(...this.psd.layers.map(l => l.depth), 0);

    if (maxDepth > 5) {
      this.addIssue({
        id: 'layer_depth',
        severity: 'warning',
        category: 'structure',
        title: '图层嵌套过深',
        description: `图层最大嵌套深度为 ${maxDepth} 层`,
        suggestion: '建议将图层嵌套控制在 5 层以内，Cubism 导入时层级太深可能导致问题',
        rule: 'Depth-001',
      });
    }
  }

  private checkBlendModes() {
    const nonNormalBlend = this.psd.layers.filter(l =>
      l.blendMode !== 'norm' && l.visible
    );

    if (nonNormalBlend.length > 0) {
      this.addIssue({
        id: 'blend_modes',
        severity: 'warning',
        category: 'convention',
        title: '存在非 Normal 混合模式',
        description: `${nonNormalBlend.length} 个图层使用非 Normal 混合模式: ${nonNormalBlend.slice(0, 3).map(l => `${l.name}(${l.blendMode})`).join(', ')}`,
        suggestion: 'Cubism 不支持图层混合模式，建议在导出前将所有图层改为 Normal',
        rule: 'Blend-001',
      });
    }
  }

  private checkOpacity() {
    const transparentLayers = this.psd.layers.filter(l =>
      l.visible && l.opacity < 0.9 && l.opacity > 0
    );

    if (transparentLayers.length > 0) {
      this.addIssue({
        id: 'layer_opacity',
        severity: 'info',
        category: 'convention',
        title: '存在半透明图层',
        description: `${transparentLayers.length} 个图层的透明度低于 90%`,
        suggestion: '建议使用图层像素的透明度而非图层透明度，Cubism 中参数控制更灵活',
        rule: 'Opacity-001',
      });
    }
  }

  private checkEmptyLayers() {
    const emptyLayers = this.psd.layers.filter(l =>
      l.channels === 0 || (l.bounds.width === 0 && l.bounds.height === 0)
    );

    if (emptyLayers.length > 0) {
      this.addIssue({
        id: 'empty_layers',
        severity: 'info',
        category: 'structure',
        title: '存在空图层',
        description: `${emptyLayers.length} 个图层可能为空: ${emptyLayers.slice(0, 3).map(l => l.name).join(', ')}`,
        suggestion: '检查并清理空图层，减少 PSD 文件大小',
        rule: 'Empty-001',
      });
    }
  }

  private checkDuplicateNames() {
    const nameCount = new Map<string, number>();
    for (const layer of this.psd.layers) {
      const name = layer.name.trim().toLowerCase();
      nameCount.set(name, (nameCount.get(name) || 0) + 1);
    }

    const duplicates = [...nameCount.entries()].filter(([_, count]) => count > 1);
    if (duplicates.length > 0) {
      this.addIssue({
        id: 'duplicate_names',
        severity: 'error',
        category: 'naming',
        title: '存在重复图层名',
        description: `${duplicates.length} 个图层名重复: ${duplicates.slice(0, 5).map(([name, count]) => `${name}(${count}x)`).join(', ')}`,
        suggestion: 'Cubism 中图层名必须唯一，请重命名重复的图层',
        rule: 'Naming-003',
      });
    }
  }

  private checkColorMode() {
    if (this.psd.colorMode !== 3 && this.psd.colorMode !== 10) {
      this.addIssue({
        id: 'color_mode',
        severity: 'warning',
        category: 'convention',
        title: '颜色模式不是 RGB',
        description: `当前颜色模式: ${this.psd.colorModeName}`,
        suggestion: 'Live2D Cubism 推荐使用 RGB 颜色模式的 PSD 文件',
        rule: 'Color-001',
      });
    }
  }

  // ============================================================
  // 辅助方法
  // ============================================================

  private addIssue(issue: QAIssue) {
    this.issues.push(issue);
  }

  private buildResult(): QAResult {
    const visibleCount = this.psd.layers.filter(l => l.visible).length;
    const hiddenCount = this.psd.layers.filter(l => !l.visible).length;

    const hasMissingCritical = this.issues.some(i =>
      i.category === 'completeness' && i.severity === 'error'
    );
    const hasNamingIssues = this.issues.some(i => i.category === 'naming');
    const hasStructuralIssues = this.issues.some(i => i.category === 'structure');

    const score = this.calculateScore();

    return {
      score,
      issues: this.issues,
      suggestions: [...this.suggestions],
      summary: {
        totalLayers: this.psd.layers.length,
        visibleLayers: visibleCount,
        hiddenLayers: hiddenCount,
        groups: this.psd.groups.length,
        hasMissingCritical,
        hasNamingIssues,
        hasStructuralIssues,
      },
    };
  }

  private calculateScore(): QAScore {
    const weights = { naming: 0.30, structure: 0.25, completeness: 0.25, convention: 0.20 };

    const scoreNaming = this.calculateCategoryScore('naming');
    const scoreStructure = this.calculateCategoryScore('structure');
    const scoreCompleteness = this.calculateCategoryScore('completeness');
    const scoreConvention = this.calculateCategoryScore('convention');

    const total = Math.round(
      scoreNaming * weights.naming +
      scoreStructure * weights.structure +
      scoreCompleteness * weights.completeness +
      scoreConvention * weights.convention
    );

    return {
      total: Math.min(100, Math.max(0, total)),
      naming: Math.min(100, Math.max(0, scoreNaming)),
      structure: Math.min(100, Math.max(0, scoreStructure)),
      completeness: Math.min(100, Math.max(0, scoreCompleteness)),
      convention: Math.min(100, Math.max(0, scoreConvention)),
    };
  }

  private calculateCategoryScore(category: IssueCategory): number {
    const categoryIssues = this.issues.filter(i => i.category === category);

    if (categoryIssues.length === 0) return 100;

    const baseScore = 100;
    let deductions = 0;

    for (const issue of categoryIssues) {
      switch (issue.severity) {
        case 'error':
          deductions += 25;
          break;
        case 'warning':
          deductions += 10;
          break;
        case 'info':
          deductions += 3;
          break;
      }
    }

    return Math.max(0, baseScore - deductions);
  }
}

export function analyzePSD(psd: PSDFileInfo): QAResult {
  const engine = new QAEngine(psd);
  return engine.analyze();
}