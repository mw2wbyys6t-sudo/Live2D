import type { CubismParam, CubismParamConfig } from '../types';

export interface ParamsStepInput {
  characterId: string;
  baseParams?: CubismParam[];
}

export interface ParamsStepOutput {
  config: CubismParamConfig;
}

export class ParamsStep {
  async execute(input: ParamsStepInput): Promise<ParamsStepOutput> {
    const defaultParams: CubismParam[] = [
      { id: 'param-eye-blink', name: 'EyeBlink', type: 'float', default: 0, min: 0, max: 1, key: 'PARAM_EYE_BLINK' },
      { id: 'param-eye-ball-x', name: 'EyeBallX', type: 'float', default: 0, min: -1, max: 1, key: 'PARAM_EYE_BALL_X' },
      { id: 'param-eye-ball-y', name: 'EyeBallY', type: 'float', default: 0, min: -1, max: 1, key: 'PARAM_EYE_BALL_Y' },
      { id: 'param-mouth-open', name: 'MouthOpen', type: 'float', default: 0, min: 0, max: 1, key: 'PARAM_MOUTH_OPEN' },
      { id: 'param-brow-up', name: 'BrowUp', type: 'float', default: 0, min: -1, max: 1, key: 'PARAM_BROW_UP' },
      { id: 'param-body-angle', name: 'BodyAngle', type: 'float', default: 0, min: -30, max: 30, key: 'PARAM_BODY_ANGLE' }
    ];

    const config: CubismParamConfig = {
      id: `params-${Date.now()}`,
      characterId: input.characterId,
      parameters: input.baseParams || defaultParams,
      parameterGroups: [
        { id: 'group-face', name: '面部参数', paramIds: ['param-eye-blink', 'param-eye-ball-x', 'param-eye-ball-y', 'param-mouth-open', 'param-brow-up'] },
        { id: 'group-body', name: '身体参数', paramIds: ['param-body-angle'] }
      ],
      version: '1.0.0',
      createdAt: new Date(),
      updatedAt: new Date()
    };

    return { config };
  }
}

export default ParamsStep;