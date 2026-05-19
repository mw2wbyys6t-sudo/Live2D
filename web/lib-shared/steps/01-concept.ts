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
      type: 'anime-girl',
      features: [],
      style: 'cute',
      description: input.description
    };
    
    return { concept };
  }
}

export default ConceptStep;
