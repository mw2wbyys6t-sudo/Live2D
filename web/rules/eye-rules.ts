import { PSDLayer } from '../lib/psd-parser';
import { LayerRule, LayerCheckResult } from './layer-types';

export const eyeHighlightRule: LayerRule = {
  id: 'eye-highlight-standalone',
  name: '眼睛高光独立层检测',
  category: 'structure',
  severity: 'warning',
  description: '检查眼睛高光是否为独立图层',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const eyeLayers = layers.filter(layer => 
      /^eye_[lr]/i.test(layer.name.trim())
    );

    if (eyeLayers.length === 0) {
      result.passed = false;
      result.issues.push({
        details: '未找到眼睛图层',
        expected: 'eye_l_*, eye_r_*',
        actual: '未找到',
      });
      result.suggestions.push('添加眼睛图层');
      return result;
    }

    const leftEyes = layers.filter(layer => /^eye_l/i.test(layer.name.trim()));
    const rightEyes = layers.filter(layer => /^eye_r/i.test(layer.name.trim()));

    const checkHighlight = (eyeLayer: PSDLayer, side: string) => {
      const eyeName = eyeLayer.name.toLowerCase();
      
      const hasHighlightPart = 
        /highlight/i.test(eyeName) ||
        /glare/i.test(eyeName) ||
        /sparkle/i.test(eyeName) ||
        /reflection/i.test(eyeName);

      if (hasHighlightPart) {
        const baseEyeName = eyeName.replace(/_(highlight|glare|sparkle|reflection).*$/i, '');
        const hasSeparateHighlight = layers.some(l => 
          new RegExp(`^eye_${side === 'l' ? 'l' : 'r'}_.*(highlight|glare|sparkle|reflection)`, 'i').test(l.name) &&
          l.name.toLowerCase() !== eyeName
        );

        if (!hasSeparateHighlight) {
          result.passed = false;
          result.issues.push({
            layer: eyeLayer.name,
            details: `高光未独立分层 ("${eyeLayer.name}")`,
            expected: 'eye_l_highlight 作为独立图层',
            actual: '高光可能与其他眼部元素混合',
          });
          result.suggestions.push(
            '将眼睛高光拆分为独立图层 (eye_l_highlight, eye_r_highlight)',
            '独立高光层便于绑定参数动画'
          );
        }
      }
    };

    leftEyes.forEach(eye => checkHighlight(eye, 'l'));
    rightEyes.forEach(eye => checkHighlight(eye, 'r'));

    if (result.passed) {
      const hasHighlightLayers = layers.some(l => 
        /eye_[lr]_highlight/i.test(l.name.trim())
      );
      
      if (!hasHighlightLayers && (leftEyes.length > 0 || rightEyes.length > 0)) {
        result.suggestions.push(
          '建议添加独立的高光图层 (eye_l_highlight, eye_r_highlight) 用于眼睛闪烁效果'
        );
      }
    }

    return result;
  },
};

export const eyeSymmetryRule: LayerRule = {
  id: 'eye-symmetry',
  name: '眼睛对称性检测',
  category: 'symmetry',
  severity: 'error',
  description: '检查左右眼睛图层结构是否对称',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const leftEyes = layers.filter(layer => /^eye_l/i.test(layer.name.trim()));
    const rightEyes = layers.filter(layer => /^eye_r/i.test(layer.name.trim()));

    if (leftEyes.length === 0 && rightEyes.length === 0) {
      result.passed = false;
      result.issues.push({
        details: '缺少眼睛图层',
        expected: 'eye_l_*, eye_r_*',
        actual: '未找到',
      });
      return result;
    }

    if (leftEyes.length !== rightEyes.length) {
      result.passed = false;
      result.issues.push({
        details: `左右眼睛图层数量不一致`,
        expected: `左眼 ${rightEyes.length} 层 (与右眼一致)`,
        actual: `左眼 ${leftEyes.length} 层，右眼 ${rightEyes.length} 层`,
      });
      result.suggestions.push('确保左右眼睛的图层数量一致');
    }

    const leftNames = new Set(leftEyes.map(l => 
      l.name.replace(/^eye_l/i, '').toLowerCase()
    ));
    const rightNames = new Set(rightEyes.map(l => 
      l.name.replace(/^eye_r/i, '').toLowerCase()
    ));

    const missingInRight = [...leftNames].filter(n => n && !rightNames.has(n));
    const missingInLeft = [...rightNames].filter(n => n && !leftNames.has(n));

    if (missingInRight.length > 0) {
      result.passed = false;
      result.issues.push({
        details: `右眼缺少子图层: ${missingInRight.join(', ')}`,
        expected: missingInRight.map(n => `eye_r${n}`).join(', '),
        actual: '未找到',
      });
    }

    if (missingInLeft.length > 0) {
      result.passed = false;
      result.issues.push({
        details: `左眼缺少子图层: ${missingInLeft.join(', ')}`,
        expected: missingInLeft.map(n => `eye_l${n}`).join(', '),
        actual: '未找到',
      });
    }

    if (!result.passed) {
      result.suggestions.push('确保左右眼睛的子图层结构完全对称');
    }

    return result;
  },
};
