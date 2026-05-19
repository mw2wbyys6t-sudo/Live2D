import type { PsdLayer, PsdLayerPlan } from '../types';

export interface PsdPlanStepInput {
  characterId: string;
  imagePath: string;
  layerStructure?: PsdLayer[];
}

export interface PsdPlanStepOutput {
  plan: PsdLayerPlan;
}

export class PsdPlanStep {
  async execute(input: PsdPlanStepInput): Promise<PsdPlanStepOutput> {
    const defaultLayers: PsdLayer[] = [
      {
        name: 'Body',
        group: 'body',
        drawOrder: 100,
        description: '身体基础层'
      },
      {
        name: 'Face',
        group: 'face',
        drawOrder: 200,
        description: '脸部基础层'
      },
      {
        name: 'Hair',
        group: 'hair',
        drawOrder: 300,
        description: '头发基础层'
      }
    ];

    const plan: PsdLayerPlan = {
      layers: input.layerStructure || defaultLayers,
      recommendations: [
        '确保每个部件都有独立图层',
        '按 Draw Order 从大到小排列',
        '使用规范的英文命名'
      ]
    };

    return { plan };
  }
}

export default PsdPlanStep;
