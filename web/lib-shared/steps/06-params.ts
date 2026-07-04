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
      { name: 'ParamAngleX', min: -30, max: 30, default: 0, description: '左右转头' },
      { name: 'ParamAngleY', min: -30, max: 30, default: 0, description: '上下点头' },
      { name: 'ParamEyeLOpen', min: 0, max: 1, default: 1, description: '左眼睁开' },
      { name: 'ParamEyeROpen', min: 0, max: 1, default: 1, description: '右眼睁开' },
      { name: 'ParamMouthOpenY', min: 0, max: 1, default: 0, description: '嘴巴张开' }
    ];

    const config: CubismParamConfig = {
      parameters: input.baseParams || defaultParams
    };

    return { config };
  }
}

export default ParamsStep;
