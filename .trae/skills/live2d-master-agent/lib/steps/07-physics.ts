import type { PhysicsConfig, PhysicsPart } from '../types';

export interface PhysicsStepInput {
  characterId: string;
  baseParts?: PhysicsPart[];
}

export interface PhysicsStepOutput {
  config: PhysicsConfig;
}

export class PhysicsStep {
  async execute(input: PhysicsStepInput): Promise<PhysicsStepOutput> {
    const defaultParts: PhysicsPart[] = [
      { name: 'hair', gravity: 0.5, wind: 0.2, restitution: 0.8, damping: 0.9 },
      { name: 'ears', gravity: 0.3, wind: 0.1, restitution: 0.7, damping: 0.85 },
      { name: 'tail', gravity: 0.6, wind: 0.3, restitution: 0.85, damping: 0.92 }
    ];

    const config: PhysicsConfig = {
      parts: input.baseParts || defaultParts
    };

    return { config };
  }
}

export default PhysicsStep;
