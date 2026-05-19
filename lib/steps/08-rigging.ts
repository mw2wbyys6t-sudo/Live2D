import type { RiggingGuide, RiggingBone } from '../types';

export interface RiggingStepInput {
  characterId: string;
  baseBones?: RiggingBone[];
}

export interface RiggingStepOutput {
  guide: RiggingGuide;
}

export class RiggingStep {
  async execute(input: RiggingStepInput): Promise<RiggingStepOutput> {
    const defaultBones: RiggingBone[] = [
      { id: 'bone-head', name: 'Head', x: 512, y: 128, angle: 0, scaleX: 1, scaleY: 1, length: 64 },
      { id: 'bone-neck', name: 'Neck', x: 512, y: 256, angle: 0, scaleX: 1, scaleY: 1, length: 32, parentId: 'bone-head' },
      { id: 'bone-body', name: 'Body', x: 512, y: 400, angle: 0, scaleX: 1, scaleY: 1, length: 128, parentId: 'bone-neck' },
      { id: 'bone-arm-left', name: 'ArmLeft', x: 256, y: 350, angle: -30, scaleX: 1, scaleY: 1, length: 100, parentId: 'bone-body' },
      { id: 'bone-arm-right', name: 'ArmRight', x: 768, y: 350, angle: 30, scaleX: 1, scaleY: 1, length: 100, parentId: 'bone-body' },
      { id: 'bone-eye-left', name: 'EyeLeft', x: 420, y: 100, angle: 0, scaleX: 1, scaleY: 1, length: 20, parentId: 'bone-head' },
      { id: 'bone-eye-right', name: 'EyeRight', x: 604, y: 100, angle: 0, scaleX: 1, scaleY: 1, length: 20, parentId: 'bone-head' }
    ];

    const guide: RiggingGuide = {
      id: `rigging-${Date.now()}`,
      characterId: input.characterId,
      bones: input.baseBones || defaultBones,
      boneGroups: [
        { id: 'group-face', name: '面部骨骼', boneIds: ['bone-head', 'bone-eye-left', 'bone-eye-right'] },
        { id: 'group-body', name: '身体骨骼', boneIds: ['bone-neck', 'bone-body'] },
        { id: 'group-arms', name: '手臂骨骼', boneIds: ['bone-arm-left', 'bone-arm-right'] }
      ],
      ikChains: [
        { id: 'ik-arm-left', name: '左臂IK', boneIds: ['bone-arm-left'], targetX: 150, targetY: 500 },
        { id: 'ik-arm-right', name: '右臂IK', boneIds: ['bone-arm-right'], targetX: 874, targetY: 500 }
      ],
      version: '1.0.0',
      createdAt: new Date(),
      updatedAt: new Date()
    };

    return { guide };
  }
}

export default RiggingStep;