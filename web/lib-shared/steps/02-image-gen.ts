export interface ImageGenStepInput {
  prompt: string;
  negativePrompt?: string;
  width?: number;
  height?: number;
  style?: string;
}

export interface ImageGenStepOutput {
  imagePath: string;
  imageUrl: string;
  seed: number;
  settings: ImageGenStepInput;
}

export class ImageGenStep {
  async execute(input: ImageGenStepInput): Promise<ImageGenStepOutput> {
    const seed = Math.floor(Math.random() * 1000000);
    const imagePath = `output/character-${seed}.png`;
    const imageUrl = `https://api.example.com/image/${seed}`;
    
    return {
      imagePath,
      imageUrl,
      seed,
      settings: input
    };
  }
}

export default ImageGenStep;