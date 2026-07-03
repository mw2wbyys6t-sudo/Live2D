import { PSDFileInfo, PSDLayer } from './psd-parser';
import { 
  allRules, 
  LayerRule, 
  LayerCheckResult,
  LayerIssue 
} from '../rules';

export interface QAIssue {
  id: string;
  severity: 'error' | 'warning' | 'info';
  category: IssueCategory;
  title: string;
  description: string;
  layer?: string;
  suggestion: string;
  rule: string;
  expected?: string;
  actual?: string;
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
  symmetry: number;
  visibility: number;
  performance: number;
}

export interface LayerStats {
  total: number;
  visible: number;
  hidden: number;
  groups: number;
  empty: number;
  semiTransparent: number;
  nonNormalBlend: number;
  offscreen: number;
  duplicateNames: number;
}

export interface QAResult {
  score: QAScore;
  issues: QAIssue[];
  warnings: QAIssue[];
  suggestions: string[];
  layer_stats: LayerStats;
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

export interface EnhancedQAResult {
  score: number;
  issues: QAIssue[];
  warnings: QAIssue[];
  suggestions: string[];
  layer_stats: LayerStats;
}

export class QAEngine {
  private issues: QAIssue[] = [];
  private warnings: QAIssue[] = [];
  private suggestions: Set<string> = new Set();
  private psd: PSDFileInfo;
  private layerStats: LayerStats;
  private rules: LayerRule[];

  constructor(psd: PSDFileInfo, customRules?: LayerRule[]) {
    this.psd = psd;
    this.rules = customRules || allRules;
    this.layerStats = this.initLayerStats();
  }

  private initLayerStats(): LayerStats {
    return {
      total: this.psd.layers.length,
      visible: this.psd.layers.filter(l => l.visible).length,
      hidden: this.psd.layers.filter(l => !l.visible).length,
      groups: this.psd.groups.length,
      empty: 0,
      semiTransparent: 0,
      nonNormalBlend: 0,
      offscreen: 0,
      duplicateNames: 0,
    };
  }

  analyze(): QAResult {
    this.issues = [];
    this.warnings = [];
    this.suggestions = new Set();
    this.layerStats = this.initLayerStats();

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

    this.runAllRules();

    this.layerStats.empty = this.psd.layers.filter(l =>
      l.channels === 0 || (l.bounds.width === 0 && l.bounds.height === 0)
    ).length;

    this.layerStats.semiTransparent = this.psd.layers.filter(l =>
      l.visible && l.opacity > 0 && l.opacity < 0.9
    ).length;

    this.layerStats.nonNormalBlend = this.psd.layers.filter(l =>
      l.visible && l.blendMode !== 'norm' && l.blendMode !== 'norma'
    ).length;

    this.layerStats.offscreen = this.psd.layers.filter(l =>
      l.visible && l.bounds.width > 0 && l.bounds.height > 0 &&
      (l.bounds.right < 0 || l.bounds.bottom < 0 ||
       l.bounds.left > this.psd.width || l.bounds.top > this.psd.height)
    ).length;

    const nameCount = new Map<string, number>();
    for (const layer of this.psd.layers) {
      const name = layer.name.trim().toLowerCase();
      nameCount.set(name, (nameCount.get(name) || 0) + 1);
    }
    this.layerStats.duplicateNames = [...nameCount.entries()].filter(
      ([_, count]) => count > 1
    ).length;

    return this.buildResult();
  }

  private runAllRules() {
    for (const rule of this.rules) {
      try {
        const result: LayerCheckResult = rule.check(
          this.psd.layers,
          this.psd.width,
          this.psd.height,
          this.psd.colorMode
        );

        for (const issue of result.issues) {
          const qaIssue: QAIssue = {
            id: `${rule.id}_${this.issues.length + this.warnings.length}`,
            severity: rule.severity,
            category: rule.category as IssueCategory,
            title: rule.name,
            description: issue.details,
            layer: issue.layer,
            suggestion: '',
            rule: rule.id.toUpperCase(),
            expected: issue.expected,
            actual: issue.actual,
          };

          if (rule.severity === 'error') {
            this.addIssue(qaIssue);
          } else {
            this.addWarning(qaIssue);
          }
        }

        for (const suggestion of result.suggestions) {
          this.suggestions.add(suggestion);
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        this.addIssue({
          id: `${rule.id}_error`,
          severity: 'error',
          category: 'structure',
          title: `${rule.name} 检测异常`,
          description: `规则 "${rule.name}" 执行时发生错误: ${errorMessage}`,
          suggestion: '请检查 PSD 文件是否正常，或联系开发者',
          rule: rule.id.toUpperCase(),
        });
      }
    }
  }

  private addIssue(issue: QAIssue) {
    issue.suggestion = this.getSuggestionForIssue(issue);
    this.issues.push(issue);
  }

  private addWarning(warning: QAIssue) {
    warning.suggestion = this.getSuggestionForIssue(warning);
    this.warnings.push(warning);
  }

  private getSuggestionForIssue(issue: QAIssue): string {
    const suggestions: Record<string, string[]> = {
      'neck-base-missing': [
        '添加 neck_base 图层用于颈部绑定',
        '颈部层应位于 face_base 下方，身体上方'
      ],
      'face-base-missing': [
        '添加 face_base 图层用于脸部绑定',
        '脸部层是所有面部元素的父层级'
      ],
      'face-shadow-missing': [
        '添加 face_shadow 图层用于阴影效果',
        '阴影层应覆盖在 face_base 上'
      ],
      'hair-back-missing': [
        '添加 hair_back 图层用于后部头发',
        '后发层应位于身体后方，避免遮挡角色'
      ],
      'eye-symmetry': [
        '确保左右眼睛的图层数量一致',
        '左右眼睛的子图层结构必须完全对称'
      ],
      'eye-highlight-standalone': [
        '将眼睛高光拆分为独立图层 (eye_l_highlight, eye_r_highlight)',
        '独立高光层便于绑定参数动画'
      ],
      'mouth-completeness': [
        '添加缺失的嘴型图层',
        '完整的口型是口型同步的基础'
      ],
      'empty-layers': [
        '检查并清理空图层以减小文件大小',
        '删除不需要的空图层'
      ],
      'zero-size-layers': [
        '删除或修复零尺寸图层',
        '零尺寸图层会导致渲染问题'
      ],
      'offscreen-layers': [
        '将图层移回画布范围内',
        '画布外图层在 Cubism 中可能不可见'
      ],
      'semi-transparent-layers': [
        '将半透明效果合并到像素中而非使用图层透明度',
        'Cubism 中使用参数控制透明度更灵活'
      ],
      'transparency-contamination': [
        '将关键图层的透明度烘焙到像素中',
        '关键层透明度问题会影响整体渲染效果'
      ],
      'naming-convention': [
        '重命名图层以符合 Live2D 规范',
        '参考 Live2D PSD 命名指南进行重命名'
      ],
      'duplicate-names': [
        '重命名重复的图层使其唯一',
        'Cubism 中图层名必须唯一'
      ],
      'draw-order-risk': [
        '调整图层顺序确保正确的遮挡关系',
        '在 Photoshop 中拖动图层调整顺序'
      ],
      'symmetry-draw-order': [
        '确保左右对称图层的绘制顺序一致',
        '在 Photoshop 中选择对应图层组调整顺序'
      ],
      'blend-modes': [
        '将所有图层改为 Normal 混合模式',
        'Cubism 不支持图层混合模式'
      ],
      'color-mode': [
        '将 PSD 转换为 RGB 颜色模式',
        'Live2D 推荐使用 RGB 颜色模式'
      ],
      'canvas-size': [
        '建议使用至少 1024x1024 的画布',
        '更大的画布可以获得更精细的绑定效果'
      ],
    };

    return suggestions[issue.id]?.[0] || issue.suggestion || '请根据问题描述进行修复';
  }

  private buildResult(): QAResult {
    const visibleCount = this.psd.layers.filter(l => l.visible).length;
    const hiddenCount = this.psd.layers.filter(l => !l.visible).length;

    const hasMissingCritical = this.issues.some(i =>
      (i.category === 'completeness' || i.category === 'structure') && i.severity === 'error'
    );
    const hasNamingIssues = this.issues.some(i => i.category === 'naming');
    const hasStructuralIssues = this.issues.some(i =>
      ['structure', 'bounds', 'symmetry'].includes(i.category)
    );

    const score = this.calculateScore();

    return {
      score,
      issues: this.issues,
      warnings: this.warnings,
      suggestions: [...this.suggestions],
      layer_stats: this.layerStats,
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
    const errorDeduction = 20;
    const warningDeduction = 10;
    const infoDeduction = 5;

    const baseScore = 100;
    let totalDeductions = 0;

    const errors = this.issues.filter(i => i.severity === 'error');
    const warnings = this.issues.filter(i => i.severity === 'warning');
    const infos = [...this.issues, ...this.warnings].filter(i => i.severity === 'info');

    totalDeductions += errors.length * errorDeduction;
    totalDeductions += warnings.length * warningDeduction;
    totalDeductions += infos.length * infoDeduction;

    const scoreByCategory = this.calculateScoreByCategory();
    const combinedScore = Math.max(0, baseScore - totalDeductions);

    return {
      total: Math.min(100, combinedScore),
      naming: scoreByCategory.naming,
      structure: scoreByCategory.structure,
      completeness: scoreByCategory.completeness,
      convention: scoreByCategory.convention,
      symmetry: scoreByCategory.symmetry,
      visibility: scoreByCategory.visibility,
      performance: scoreByCategory.performance,
    };
  }

  private calculateScoreByCategory(): Record<string, number> {
    const categories: IssueCategory[] = [
      'naming', 'structure', 'completeness', 'convention',
      'symmetry', 'visibility', 'performance', 'bounds'
    ];

    const scores: Record<string, number> = {};
    const baseScore = 100;

    for (const category of categories) {
      const categoryIssues = this.issues.filter(i => i.category === category);
      const categoryWarnings = this.warnings.filter(i => i.category === category);

      let deductions = 0;
      deductions += categoryIssues.length * 20;
      deductions += categoryWarnings.length * 10;

      scores[category] = Math.max(0, baseScore - deductions);
    }

    return scores;
  }
}

export function analyzePSD(psd: PSDFileInfo): QAResult {
  const engine = new QAEngine(psd);
  return engine.analyze();
}

export function getEnhancedResult(result: QAResult): EnhancedQAResult {
  return {
    score: result.score.total,
    issues: result.issues,
    warnings: result.warnings,
    suggestions: result.suggestions,
    layer_stats: result.layer_stats,
  };
}
