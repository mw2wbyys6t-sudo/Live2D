export * from './layer-types';
export * from './critical-layers';
export * from './eye-rules';
export * from './mouth-rules';
export * from './empty-layer-rules';
export * from './transparency-rules';
export * from './naming-rules';
export * from './draw-order-rules';
export * from './convention-rules';

import { LayerRule } from './layer-types';

export const allRules: LayerRule[] = [
  require('./critical-layers').neckBaseRule,
  require('./critical-layers').faceBaseRule,
  require('./critical-layers').faceShadowRule,
  require('./critical-layers').hairBackRule,
  require('./eye-rules').eyeHighlightRule,
  require('./eye-rules').eyeSymmetryRule,
  require('./mouth-rules').mouthCompletenessRule,
  require('./mouth-rules').mouthLayeringRule,
  require('./empty-layer-rules').emptyLayerRule,
  require('./empty-layer-rules').zeroSizeLayerRule,
  require('./empty-layer-rules').offscreenLayerRule,
  require('./transparency-rules').semiTransparentRule,
  require('./transparency-rules').transparencyContaminationRule,
  require('./naming-rules').namingConventionRule,
  require('./naming-rules').duplicateNameRule,
  require('./naming-rules').layerNameFormatRule,
  require('./draw-order-rules').drawOrderRiskRule,
  require('./draw-order-rules').symmetryDrawOrderRule,
  require('./draw-order-rules').layerGroupStructureRule,
  require('./convention-rules').blendModeRule,
  require('./convention-rules').colorModeRule,
  require('./convention-rules').canvasSizeRule,
  require('./convention-rules').hiddenLayerRule,
];
