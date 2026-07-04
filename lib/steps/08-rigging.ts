import type { RiggingGuide } from '../types';

export interface RiggingStepInput {
  characterId: string;
}

export interface RiggingStepOutput {
  guide: RiggingGuide;
}

export class RiggingStep {
  async execute(input: RiggingStepInput): Promise<RiggingStepOutput> {
    const guide: RiggingGuide = {
      steps: [
        '1. 导入 PSD 文件到 Cubism Editor',
        '2. 设置画布尺寸和定位',
        '3. 为每个部件创建 ArtMesh',
        '4. 添加 Warp Deformer 和 Rotation Deformer',
        '5. 配置参数关键帧',
        '6. 设置物理效果',
        '7. 导出为 model3.json'
      ],
      tips: [
        '保持 Draw Order 正确',
        '使用对称功能节省时间',
        '先测试再导出'
      ],
      bestPractices: [
        '使用规范的参数名称',
        '合理设置变形器范围',
        '定期保存工程文件'
      ]
    };

    return { guide };
  }
}

export default RiggingStep;
