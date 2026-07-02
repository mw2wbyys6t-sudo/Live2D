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
import { neckBaseRule, faceBaseRule, faceShadowRule, hairBackRule } from './critical-layers';
import { eyeHighlightRule, eyeSymmetryRule } from './eye-rules';
import { mouthCompletenessRule, mouthLayeringRule } from './mouth-rules';
import { emptyLayerRule, zeroSizeLayerRule, offscreenLayerRule } from './empty-layer-rules';
import { semiTransparentRule, transparencyContaminationRule } from './transparency-rules';
import { namingConventionRule, duplicateNameRule, layerNameFormatRule } from './naming-rules';
import { drawOrderRiskRule, symmetryDrawOrderRule, layerGroupStructureRule } from './draw-order-rules';
import { blendModeRule, colorModeRule, canvasSizeRule, hiddenLayerRule } from './convention-rules';

export const allRules: LayerRule[] = [
  neckBaseRule,
  faceBaseRule,
  faceShadowRule,
  hairBackRule,
  eyeHighlightRule,
  eyeSymmetryRule,
  mouthCompletenessRule,
  mouthLayeringRule,
  emptyLayerRule,
  zeroSizeLayerRule,
  offscreenLayerRule,
  semiTransparentRule,
  transparencyContaminationRule,
  namingConventionRule,
  duplicateNameRule,
  layerNameFormatRule,
  drawOrderRiskRule,
  symmetryDrawOrderRule,
  layerGroupStructureRule,
  blendModeRule,
  colorModeRule,
  canvasSizeRule,
  hiddenLayerRule,
];