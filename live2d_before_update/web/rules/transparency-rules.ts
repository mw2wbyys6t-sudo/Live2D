import { PSDLayer } from '../lib/psd-parser';
import { LayerRule, LayerCheckResult } from './layer-types';

export const semiTransparentRule: LayerRule = {
  id: 'semi-transparent-layers',
  name: '半透明图层检测',
  category: 'convention',
  severity: 'warning',
  description: '检测使用了半透明度的图层',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const semiTransparentLayers = layers.filter(layer => 
      layer.visible && layer.opacity > 0 && layer.opacity < 0.9
    );

    if (semiTransparentLayers.length > 0) {
      result.passed = false;
      result.issues.push({
        details: `发现 ${semiTransparentLayers.length} 个半透明图层`,
        expected: '图层透明度应为 100% 或 0%',
        actual: semiTransparentLayers.map(l => 
          `${l.name} (${Math.round(l.opacity * 100)}%)`
        ).join(', '),
      });
      result.suggestions.push(
        '将半透明效果合并到像素中而非使用图层透明度',
        'Cubism 中使用参数控制透明度更灵活',
        '半透明可能导致渲染不一致'
      );
    }

    return result;
  },
};

export const transparencyContaminationRule: LayerRule = {
  id: 'transparency-contamination',
  name: '透明度污染检测',
  category: 'performance',
  severity: 'info',
  description: '检测可能导致渲染问题的透明度设置',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const criticalLayers = ['face_base', 'face_shadow', 'eye_l', 'eye_r', 'mouth_base'];
    const transparentCritical = layers.filter(layer => {
      const name = layer.name.toLowerCase().trim();
      const isCritical = criticalLayers.some(c => name.includes(c));
      return isCritical && layer.opacity < 1 && layer.opacity > 0;
    });

    if (transparentCritical.length > 0) {
      result.passed = false;
      result.issues.push({
        details: `关键图层存在透明度设置: ${transparentCritical.map(l => l.name).join(', ')}`,
        expected: '关键图层透明度应为 100%',
        actual: transparentCritical.map(l => 
          `${l.name} (${Math.round(l.opacity * 100)}%)`
        ).join(', '),
      });
      result.suggestions.push(
        '将关键图层的透明度烘焙到像素中',
        '关键层透明度问题会影响整体渲染效果'
      );
    }

    const lowOpacityLayers = layers.filter(layer => 
      layer.visible && layer.opacity > 0 && layer.opacity < 0.5
    );

    if (lowOpacityLayers.length > 3) {
      result.suggestions.push(
        `有 ${lowOpacityLayers.length} 个图层透明度低于 50%，检查是否必要`
      );
    }

    return result;
  },
};
