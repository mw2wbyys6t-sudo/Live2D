import { PSDLayer } from '../lib/psd-parser';
import { LayerRule, LayerCheckResult, SYMMETRY_PAIRS } from './layer-types';

export const drawOrderRiskRule: LayerRule = {
  id: 'draw-order-risk',
  name: '绘制顺序风险检测',
  category: 'structure',
  severity: 'warning',
  description: '检测可能导致渲染问题的绘制顺序',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const faceRelatedLayers = layers.filter(l => 
      /^(face|eye|mouth|nose|eyebrow|head)/i.test(l.name.trim())
    );
    const hairLayers = layers.filter(l => 
      /^hair/i.test(l.name.trim())
    );
    const bodyLayers = layers.filter(l => 
      /^(body|neck|torso|skirt|arm|leg)/i.test(l.name.trim())
    );

    if (faceRelatedLayers.length > 0 && hairLayers.length > 0) {
      const faceIndices = faceRelatedLayers.map(l => l.index);
      const hairFrontLayers = hairLayers.filter(l => /front/i.test(l.name));
      const hairBackLayers = hairLayers.filter(l => /back/i.test(l.name));

      const minFaceIndex = Math.min(...faceIndices);

      for (const hair of hairBackLayers) {
        if (hair.index < minFaceIndex) {
          result.issues.push({
            layer: hair.name,
            details: `后发层 "${hair.name}" 在脸相关图层之前`,
            expected: '后发层应在身体层之后',
            actual: `后发层索引: ${hair.index}, 最小脸部层索引: ${minFaceIndex}`,
          });
        }
      }

      for (const hair of hairFrontLayers) {
        if (hair.index > Math.max(...faceIndices)) {
          result.issues.push({
            layer: hair.name,
            details: `前发层 "${hair.name}" 在所有脸相关图层之后`,
            expected: '前发层应在眼睛/眉毛等图层之前或之后适当位置',
            actual: `前发层索引: ${hair.index}`,
          });
        }
      }
    }

    if (bodyLayers.length > 0 && faceRelatedLayers.length > 0) {
      const bodyIndices = bodyLayers.map(l => l.index);
      const faceIndices = faceRelatedLayers.map(l => l.index);

      const maxBodyIndex = Math.max(...bodyIndices);
      const minFaceIndex = Math.min(...faceIndices);

      if (maxBodyIndex > minFaceIndex) {
        result.suggestions.push(
          '检查身体层和脸部的绘制顺序是否正确',
          '脸部层通常应该在身体层的上方'
        );
      }
    }

    if (result.issues.length > 0) {
      result.passed = false;
      result.suggestions.push(
        '调整图层顺序确保正确的遮挡关系',
        '在 Photoshop 中拖动图层调整顺序'
      );
    }

    return result;
  },
};

export const symmetryDrawOrderRule: LayerRule = {
  id: 'symmetry-draw-order',
  name: '对称图层绘制顺序检测',
  category: 'symmetry',
  severity: 'warning',
  description: '检查对称图层的绘制顺序是否一致',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    for (const pair of SYMMETRY_PAIRS) {
      const leftLayers = layers.filter(l => pair.left.test(l.name.trim()));
      const rightLayers = layers.filter(l => pair.right.test(l.name.trim()));

      if (leftLayers.length === 0 || rightLayers.length === 0) {
        continue;
      }

      const leftIndices = leftLayers.map(l => l.index).sort((a, b) => a - b);
      const rightIndices = rightLayers.map(l => l.index).sort((a, b) => a - b);

      if (leftIndices.length === rightIndices.length) {
        for (let i = 0; i < leftIndices.length; i++) {
          const diff = Math.abs(leftIndices[i] - rightIndices[i]);
          if (diff > 2) {
            result.issues.push({
              details: `${pair.name}对称图层绘制顺序不一致`,
              expected: `${pair.name}的对应子图层应相近`,
              actual: `左${pair.name}[${i}]: ${leftIndices[i]}, 右${pair.name}[${i}]: ${rightIndices[i]}`,
            });
          }
        }
      }
    }

    if (result.issues.length > 0) {
      result.passed = false;
      result.suggestions.push(
        '确保左右对称图层的绘制顺序一致',
        '在 Photoshop 中选择对应图层组调整顺序'
      );
    }

    return result;
  },
};

export const layerGroupStructureRule: LayerRule = {
  id: 'layer-group-structure',
  name: '图层组结构检测',
  category: 'structure',
  severity: 'info',
  description: '检查图层组的嵌套结构',
  check: (layers: PSDLayer[]) => {
    const result: LayerCheckResult = {
      passed: true,
      issues: [],
      suggestions: [],
    };

    const groups = layers.filter(l => l.isGroup && !l.isGroupEnd);
    const groupEnds = layers.filter(l => l.isGroupEnd);

    if (groups.length !== groupEnds.length) {
      result.issues.push({
        details: '图层组数量不匹配',
        expected: `组开始: ${groups.length}, 组结束: ${groupEnds.length}`,
        actual: '数量不一致',
      });
    }

    const maxNestingDepth = calculateNestingDepth(layers);
    if (maxNestingDepth > 5) {
      result.passed = false;
      result.issues.push({
        details: `图层嵌套过深: ${maxNestingDepth} 层`,
        expected: '嵌套深度 <= 5',
        actual: `当前深度: ${maxNestingDepth}`,
      });
      result.suggestions.push(
        '减少图层组嵌套深度',
        '过深的嵌套可能导致 Cubism 导入问题'
      );
    }

    if (groups.length > 0) {
      result.suggestions.push(
        `发现 ${groups.length} 个图层组，建议为每个部件创建独立组`
      );
    }

    return result;
  },
};

function calculateNestingDepth(layers: PSDLayer[]): number {
  let currentDepth = 0;
  let maxDepth = 0;

  for (const layer of layers) {
    if (layer.isGroup && !layer.isGroupEnd) {
      currentDepth++;
      maxDepth = Math.max(maxDepth, currentDepth);
    } else if (layer.isGroupEnd) {
      currentDepth = Math.max(0, currentDepth - 1);
    }
  }

  return maxDepth;
}
