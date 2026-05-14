import { PSDLayer } from '../lib/psd-parser';
import { LayerRule, LayerCheckResult, CRITICAL_LAYERS } from './layer-types';

export const neckBaseRule: LayerRule = {
  id: 'neck-base-missing',
  name: '颈部基础层检测',
  category: 'completeness',
  severity: 'error',
  description: '检查是否存在颈部基础层 (neck_base)',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const hasNeckBase = layers.some(layer => 
      CRITICAL_LAYERS.neck_base.patterns.some(p => p.test(layer.name.trim()))
    );

    if (!hasNeckBase) {
      result.passed = false;
      result.issues.push({
        details: '缺少颈部基础层 (neck_base)',
        expected: 'neck_base 或 body_neck',
        actual: '未找到',
      });
      result.suggestions.push(
        '添加 neck_base 图层用于颈部绑定',
        '颈部层应位于 face_base 下方，身体上方'
      );
    }

    return result;
  },
};

export const faceBaseRule: LayerRule = {
  id: 'face-base-missing',
  name: '脸部基础层检测',
  category: 'completeness',
  severity: 'error',
  description: '检查是否存在脸部基础层 (face_base)',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const hasFaceBase = layers.some(layer => 
      CRITICAL_LAYERS.face_base.patterns.some(p => p.test(layer.name.trim()))
    );

    if (!hasFaceBase) {
      result.passed = false;
      result.issues.push({
        details: '缺少脸部基础层 (face_base)',
        expected: 'face_base',
        actual: '未找到',
      });
      result.suggestions.push(
        '添加 face_base 图层用于脸部绑定',
        '脸部层是所有面部元素的父层级'
      );
    }

    return result;
  },
};

export const faceShadowRule: LayerRule = {
  id: 'face-shadow-missing',
  name: '脸部阴影层检测',
  category: 'completeness',
  severity: 'error',
  description: '检查是否存在脸部阴影层 (face_shadow)',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const hasFaceShadow = layers.some(layer => 
      CRITICAL_LAYERS.face_shadow.patterns.some(p => p.test(layer.name.trim()))
    );

    if (!hasFaceShadow) {
      result.passed = false;
      result.issues.push({
        details: '缺少脸部阴影层 (face_shadow)',
        expected: 'face_shadow 或 face_shade',
        actual: '未找到',
      });
      result.suggestions.push(
        '添加 face_shadow 图层用于阴影效果',
        '阴影层应覆盖在 face_base 上'
      );
    }

    return result;
  },
};

export const hairBackRule: LayerRule = {
  id: 'hair-back-missing',
  name: '后发层检测',
  category: 'completeness',
  severity: 'error',
  description: '检查是否存在后发层 (hair_back)',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const hairBackLayers = layers.filter(layer => 
      CRITICAL_LAYERS.hair_back.patterns.some(p => p.test(layer.name.trim()))
    );

    if (hairBackLayers.length === 0) {
      result.passed = false;
      result.issues.push({
        details: '缺少后发层 (hair_back)',
        expected: 'hair_back_01, hair_back_02 等',
        actual: '未找到',
      });
      result.suggestions.push(
        '添加 hair_back 图层用于后部头发',
        '后发层应位于身体后方，避免遮挡角色'
      );
    }

    return result;
  },
};
