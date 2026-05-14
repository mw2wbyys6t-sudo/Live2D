import { PSDLayer } from '../lib/psd-parser';
import { LayerRule, LayerCheckResult, MOUTH_SHAPES } from './layer-types';

export const mouthCompletenessRule: LayerRule = {
  id: 'mouth-completeness',
  name: '嘴型完整性检测',
  category: 'completeness',
  severity: 'error',
  description: '检查口型图层是否完整（a/i/u/e/o）',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const mouthBase = layers.find(layer => 
      /^mouth_base$/i.test(layer.name.trim())
    );

    if (!mouthBase) {
      result.passed = false;
      result.issues.push({
        details: '缺少嘴型基础层 (mouth_base)',
        expected: 'mouth_base',
        actual: '未找到',
      });
      result.suggestions.push('添加 mouth_base 图层作为口型基础');
    }

    const foundShapes: string[] = [];
    for (const layer of layers) {
      const name = layer.name.trim().toLowerCase();
      for (const shape of MOUTH_SHAPES) {
        if (name === `mouth_${shape}` || name.startsWith(`mouth_${shape}_`)) {
          foundShapes.push(shape);
          break;
        }
      }
    }

    const missingShapes = MOUTH_SHAPES.filter(s => !foundShapes.includes(s));

    if (missingShapes.length > 0) {
      result.passed = false;
      result.issues.push({
        details: `缺少嘴型: ${missingShapes.join(', ')}`,
        expected: `mouth_${MOUTH_SHAPES.join(', mouth_')}`,
        actual: `只有 ${foundShapes.join(', ') || '无'}`,
      });

      if (missingShapes.length >= 3) {
        result.suggestions.push(
          `添加缺失的嘴型图层: ${missingShapes.map(s => `mouth_${s}`).join(', ')}`,
          '完整的口型是口型同步的基础'
        );
      } else {
        result.suggestions.push(
          `建议添加缺失的嘴型: ${missingShapes.join(', ')}`
        );
      }
    }

    if (result.passed && foundShapes.length >= 5) {
      result.suggestions.push('嘴型图层完整，支持完整的口型同步');
    }

    return result;
  },
};

export const mouthLayeringRule: LayerRule = {
  id: 'mouth-layering',
  name: '嘴型分层结构检测',
  category: 'structure',
  severity: 'warning',
  description: '检查嘴型是否有正确的分层结构',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const mouthLayers = layers.filter(layer => 
      /^mouth/i.test(layer.name.trim())
    );

    if (mouthLayers.length === 0) {
      return result;
    }

    const hasTeeth = mouthLayers.some(l => 
      /teeth|dental|tooth/i.test(l.name.trim())
    );
    const hasLip = mouthLayers.some(l => 
      /lip/i.test(l.name.trim())
    );
    const hasTongue = mouthLayers.some(l => 
      /tongue| язык/i.test(l.name.trim())
    );

    if (mouthLayers.length >= 3 && !hasTeeth) {
      result.suggestions.push(
        '建议将牙齿拆分为独立图层 (mouth_teeth_upper, mouth_teeth_lower)'
      );
    }

    if (mouthLayers.length >= 2 && !hasLip) {
      result.suggestions.push(
        '建议将嘴唇拆分为上下两层 (mouth_lip_upper, mouth_lip_lower)'
      );
    }

    if (mouthLayers.length >= 4 && !hasTongue) {
      result.suggestions.push(
        '考虑添加舌头图层 (mouth_tongue) 以支持更丰富的表情'
      );
    }

    return result;
  },
};
