import { PSDLayer } from '../lib/psd-parser';
import { LayerRule, LayerCheckResult, LIVE2D_NAMING_PATTERNS } from './layer-types';

export const namingConventionRule: LayerRule = {
  id: 'naming-convention',
  name: '图层命名规范检测',
  category: 'naming',
  severity: 'warning',
  description: '检查图层命名是否符合 Live2D 规范',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    let standardCount = 0;
    const nonStandardLayers: string[] = [];

    for (const layer of layers) {
      const isStandard = LIVE2D_NAMING_PATTERNS.some(p => p.test(layer.name.trim()));
      
      if (isStandard) {
        standardCount++;
      } else {
        nonStandardLayers.push(layer.name);
      }
    }

    if (nonStandardLayers.length > 0) {
      result.passed = false;
      result.issues.push({
        details: `${nonStandardLayers.length} 个图层不符合 Live2D 命名规范`,
        expected: '使用标准命名: hair_front_01, face_base, eye_l_white 等',
        actual: nonStandardLayers.slice(0, 5).join(', ') + (nonStandardLayers.length > 5 ? '...' : ''),
      });
      result.suggestions.push(
        '重命名图层以符合 Live2D 规范',
        `当前 ${standardCount}/${layers.length} 个图层符合规范`,
        '参考 Live2D PSD 命名指南进行重命名'
      );
    }

    if (standardCount === 0 && layers.length > 0) {
      result.issues.push({
        details: '所有图层都不符合 Live2D 命名规范',
        expected: '至少有一个标准命名的图层',
        actual: '0 个标准图层',
      });
    }

    return result;
  },
};

export const duplicateNameRule: LayerRule = {
  id: 'duplicate-names',
  name: '重复图层名检测',
  category: 'naming',
  severity: 'error',
  description: '检查是否存在重复的图层名称',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const nameCount = new Map<string, { count: number; layers: string[] }>();
    
    for (const layer of layers) {
      const name = layer.name.trim().toLowerCase();
      if (!nameCount.has(name)) {
        nameCount.set(name, { count: 0, layers: [] });
      }
      const entry = nameCount.get(name)!;
      entry.count++;
      entry.layers.push(layer.name);
    }

    const duplicates = [...nameCount.entries()].filter(([_, data]) => data.count > 1);

    if (duplicates.length > 0) {
      result.passed = false;
      result.issues.push({
        details: `发现 ${duplicates.length} 组重复图层名`,
        expected: '每个图层名唯一',
        actual: duplicates.slice(0, 5).map(([name, data]) => 
          `"${name}" (${data.count}次)`
        ).join(', '),
      });
      result.suggestions.push(
        '重命名重复的图层使其唯一',
        'Cubism 中图层名必须唯一'
      );
    }

    return result;
  },
};

export const layerNameFormatRule: LayerRule = {
  id: 'layer-name-format',
  name: '图层名格式检测',
  category: 'naming',
  severity: 'info',
  description: '检查图层命名格式是否规范',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const issues: string[] = [];

    for (const layer of layers) {
      const name = layer.name;
      
      if (name.includes('  ')) {
        issues.push(`${layer.name}: 包含多余空格`);
      }
      
      if (name.startsWith(' ') || name.endsWith(' ')) {
        issues.push(`${layer.name}: 名称首尾有空格`);
      }
      
      if (/[^\w_\-]/.test(name.replace(/\s/g, ''))) {
        issues.push(`${layer.name}: 包含特殊字符`);
      }
      
      if (name.length > 50) {
        issues.push(`${layer.name}: 名称过长 (${name.length}字符)`);
      }
    }

    if (issues.length > 0) {
      result.issues.push({
        details: `发现 ${issues.length} 个命名格式问题`,
        expected: '图层名应简洁、无多余空格、无特殊字符',
        actual: issues.slice(0, 3).join('; '),
      });
      result.suggestions.push(
        '清理图层名称中的多余字符',
        '建议图层名控制在 30 字符以内'
      );
    }

    return result;
  },
};
