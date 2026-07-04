import { PSDLayer } from '../lib/psd-parser';
import { LayerRule, LayerCheckResult } from './layer-types';

export const blendModeRule: LayerRule = {
  id: 'blend-modes',
  name: '混合模式检测',
  category: 'convention',
  severity: 'warning',
  description: '检测非 Normal 混合模式的图层',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const nonNormalLayers = layers.filter(l => 
      l.visible && l.blendMode !== 'norm' && l.blendMode !== 'norma'
    );

    if (nonNormalLayers.length > 0) {
      result.passed = false;
      result.issues.push({
        details: `发现 ${nonNormalLayers.length} 个使用非 Normal 混合模式的图层`,
        expected: '所有图层使用 Normal 混合模式',
        actual: nonNormalLayers.slice(0, 5).map(l => 
          `${l.name} (${l.blendMode})`
        ).join(', '),
      });
      result.suggestions.push(
        '将所有图层改为 Normal 混合模式',
        'Cubism 不支持图层混合模式',
        '在 Photoshop 中使用 "图层 > 拼合图像" 然后重新分层'
      );
    }

    return result;
  },
};

export const colorModeRule: LayerRule = {
  id: 'color-mode',
  name: '颜色模式检测',
  category: 'convention',
  severity: 'warning',
  description: '检查 PSD 文件颜色模式是否为 RGB',
  check: (layers: PSDLayer[], psdWidth?: number, psdHeight?: number, colorMode?: number) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const colorModeNames: Record<number, string> = {
      0: 'Bitmap',
      1: 'Grayscale',
      2: 'Indexed',
      3: 'RGB',
      4: 'CMYK',
      7: 'Multichannel',
      8: 'Duotone',
      9: 'Lab',
      10: 'RGB',
    };

    const modeName = colorMode !== undefined ? colorModeNames[colorMode] || 'Unknown' : 'Unknown';

    if (colorMode !== undefined && colorMode !== 3 && colorMode !== 10) {
      result.passed = false;
      result.issues.push({
        details: `PSD 颜色模式为 ${modeName} 而非 RGB`,
        expected: 'RGB 颜色模式',
        actual: modeName,
      });
      result.suggestions.push(
        '将 PSD 转换为 RGB 颜色模式',
        'Live2D 推荐使用 RGB 颜色模式'
      );
    }

    return result;
  },
};

export const canvasSizeRule: LayerRule = {
  id: 'canvas-size',
  name: '画布尺寸检测',
  category: 'convention',
  severity: 'info',
  description: '检查画布尺寸是否符合 Live2D 规范',
  check: (layers: PSDLayer[], psdWidth?: number, psdHeight?: number) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    if (psdWidth === undefined || psdHeight === undefined) {
      return result;
    }

    if (psdWidth < 512 || psdHeight < 512) {
      result.passed = false;
      result.issues.push({
        details: `画布尺寸偏小: ${psdWidth}x${psdHeight}`,
        expected: '至少 1024x1024',
        actual: `${psdWidth}x${psdHeight}`,
      });
      result.suggestions.push(
        '建议使用至少 1024x1024 的画布',
        '更大的画布可以获得更精细的绑定效果'
      );
    }

    if (psdWidth !== psdHeight) {
      result.issues.push({
        details: `画布不是正方形: ${psdWidth}x${psdHeight}`,
        expected: '正方形画布',
        actual: `${psdWidth}x${psdHeight}`,
      });
      result.suggestions.push(
        'Live2D 通常使用正方形画布',
        '正方形画布便于后续绑定和导出'
      );
    }

    if (psdWidth >= 2048 && psdHeight >= 2048) {
      result.suggestions.push('画布尺寸充足，支持高质量绑定');
    }

    return result;
  },
};

export const hiddenLayerRule: LayerRule = {
  id: 'hidden-layers',
  name: '隐藏图层检测',
  category: 'visibility',
  severity: 'info',
  description: '检测隐藏的图层',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const hiddenLayers = layers.filter(l => !l.visible);

    if (hiddenLayers.length > 0) {
      result.issues.push({
        details: `发现 ${hiddenLayers.length} 个隐藏图层`,
        expected: '所有需要的图层应该可见',
        actual: hiddenLayers.slice(0, 5).map(l => l.name).join(', ') + 
               (hiddenLayers.length > 5 ? '...' : ''),
      });
      result.suggestions.push(
        '检查隐藏图层是否需要保留',
        '隐藏图层在 Cubism 中可能不会被导入',
        '考虑删除不需要的隐藏图层'
      );
    }

    return result;
  },
};
