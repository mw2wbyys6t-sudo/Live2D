import type { CharacterConcept } from '../types';

export interface ConceptStepInput {
  description: string;
  referenceImages?: string[];
}

export interface ConceptStepOutput {
  concept: CharacterConcept;
}

export class ConceptStep {
  async execute(input: ConceptStepInput): Promise<ConceptStepOutput> {
    const concept: CharacterConcept = {
      id: `concept-${Date.now()}`,
      name: '未命名角色',
      gender: 'neutral',
      style: 'anime',
      ageRange: 'young_adult',
      expression: 'default',
      accessories: [],
      description: input.description,
      referenceImages: input.referenceImages || [],
      createdAt: new Date(),
      updatedAt: new Date()
    };
    
    return { concept };
  }
}

export default ConceptStep;