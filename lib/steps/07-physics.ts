import type { PhysicsConfig, PhysicsParticle } from '../types';

export interface PhysicsStepInput {
  characterId: string;
  baseParticles?: PhysicsParticle[];
}

export interface PhysicsStepOutput {
  config: PhysicsConfig;
}

export class PhysicsStep {
  async execute(input: PhysicsStepInput): Promise<PhysicsStepOutput> {
    const defaultParticles: PhysicsParticle[] = [
      { id: 'particle-hair-left', name: 'HairLeft', x: 256, y: 100, size: 10, gravity: 0.5, friction: 0.1, stiffness: 0.8 },
      { id: 'particle-hair-right', name: 'HairRight', x: 768, y: 100, size: 10, gravity: 0.5, friction: 0.1, stiffness: 0.8 },
      { id: 'particle-ribbon', name: 'Ribbon', x: 512, y: 80, size: 8, gravity: 0.3, friction: 0.15, stiffness: 0.6 }
    ];

    const config: PhysicsConfig = {
      id: `physics-${Date.now()}`,
      characterId: input.characterId,
      particles: input.baseParticles || defaultParticles,
      constraints: [
        { id: 'constraint-hair-left', from: 'particle-hair-left', to: 'head', stiffness: 0.7 },
        { id: 'constraint-hair-right', from: 'particle-hair-right', to: 'head', stiffness: 0.7 },
        { id: 'constraint-ribbon', from: 'particle-ribbon', to: 'head', stiffness: 0.5 }
      ],
      settings: {
        windEnabled: true,
        windForce: 0.2,
        gravityEnabled: true,
        gravityForce: 0.1
      },
      version: '1.0.0',
      createdAt: new Date(),
      updatedAt: new Date()
    };

    return { config };
  }
}

export default PhysicsStep;