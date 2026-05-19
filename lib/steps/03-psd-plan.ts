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
        id: 'layer-body',
        name: 'Body',
        type: 'normal',
        path: 'Body',
        visible: true,
        locked: false,
        opacity: 100,
        blendMode: 'normal',
        width: 1024,
        height: 1024,
        x: 0,
        y: 0
      },
      {
        id: 'layer-face',
        name: 'Face',
        type: 'normal',
        path: 'Face',
        visible: true,
        locked: false,
        opacity: 100,
        blendMode: 'normal',
        width: 512,
        height: 512,
        x: 256,
        y: 128
      },
      {
        id: 'layer-hair',
        name: 'Hair',
        type: 'normal',
        path: 'Hair',
        visible: true,
        locked: false,
        opacity: 100,
        blendMode: 'normal',
        width: 512,
        height: 512,
        x: 256,
        y: 64
      }
    ];

    const plan: PsdLayerPlan = {
      id: `plan-${Date.now()}`,
      characterId: input.characterId,
      originalPsdPath: input.imagePath,
      layers: input.layerStructure || defaultLayers,
      layerMapping: {},
      version: '1.0.0',
      createdAt: new Date(),
      updatedAt: new Date()
    };

    return { plan };
  }
}

export default PsdPlanStep;