import { PSDLayer } from '../lib/psd-parser';
import { LayerRule, LayerCheckResult } from './layer-types';

export const emptyLayerRule: LayerRule = {
  id: 'empty-layers',
  name: '空图层检测',
  category: 'structure',
  severity: 'warning',
  description: '检测可能为空的图层',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const emptyLayers: PSDLayer[] = [];

    for (const layer of layers) {
      const isEmpty = 
        layer.channels === 0 ||
        (layer.bounds.width === 0 && layer.bounds.height === 0) ||
        (layer.bounds.width === 0 || layer.bounds.height === 0);

      if (isEmpty && layer.visible) {
        emptyLayers.push(layer);
      }
    }

    if (emptyLayers.length > 0) {
      result.passed = false;
      result.issues.push({
        details: `发现 ${emptyLayers.length} 个可能为空的图层`,
        expected: '有效的像素数据',
        actual: emptyLayers.map(l => `${l.name} (${l.bounds.width}x${l.bounds.height})`).join(', '),
      });
      result.suggestions.push(
        '检查并清理空图层以减小文件大小',
        '删除不需要的空图层'
      );
    }

    return result;
  },
};

export const zeroSizeLayerRule: LayerRule = {
  id: 'zero-size-layers',
  name: '零尺寸图层检测',
  category: 'bounds',
  severity: 'error',
  description: '检测尺寸为零的图层',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const zeroSizeLayers = layers.filter(layer => 
      layer.visible && layer.bounds.width === 0 && layer.bounds.height === 0
    );

    if (zeroSizeLayers.length > 0) {
      result.passed = false;
      result.issues.push({
        details: `发现 ${zeroSizeLayers.length} 个零尺寸图层`,
        expected: '图层尺寸 > 0',
        actual: zeroSizeLayers.map(l => l.name).join(', '),
      });
      result.suggestions.push(
        '删除或修复零尺寸图层',
        '零尺寸图层会导致渲染问题'
      );
    }

    return result;
  },
};

export const offscreenLayerRule: LayerRule = {
  id: 'offscreen-layers',
  name: '画布外图层检测',
  category: 'bounds',
  severity: 'warning',
  description: '检测完全在画布范围外的图层',
  check: (layers: PSDLayer[], psdWidth: number, psdHeight: number) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const offscreenLayers = layers.filter(layer => {
      if (!layer.visible || layer.bounds.width === 0 || layer.bounds.height === 0) {
        return false;
      }
      return (
        layer.bounds.right < 0 ||
        layer.bounds.bottom < 0 ||
        layer.bounds.left > psdWidth ||
        layer.bounds.top > psdHeight
      );
    });

    if (offscreenLayers.length > 0) {
      result.passed = false;
      result.issues.push({
        details: `发现 ${offscreenLayers.length} 个图层完全在画布外`,
        expected: `图层应在画布范围内 (0, 0) - (${psdWidth}, ${psdHeight})`,
        actual: offscreenLayers.slice(0, 3).map(l => 
          `${l.name} (${l.bounds.left}, ${l.bounds.top})`
        ).join(', ') + (offscreenLayers.length > 3 ? '...' : ''),
      });
      result.suggestions.push(
        '将图层移回画布范围内',
        '画布外图层在 Cubism 中可能不可见'
      );
    }

    return result;
  },
};
