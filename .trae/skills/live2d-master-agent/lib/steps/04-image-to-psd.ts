export interface ImageToPsdStepInput {
  imagePath: string;
  outputPath?: string;
  layerCount?: number;
}

export interface ImageToPsdStepOutput {
  psdPath: string;
  layerCount: number;
  width: number;
  height: number;
}

export class ImageToPsdStep {
  async execute(input: ImageToPsdStepInput): Promise<ImageToPsdStepOutput> {
    const psdPath = input.outputPath || `output/converted-${Date.now()}.psd`;
    
    return {
      psdPath,
      layerCount: input.layerCount || 5,
      width: 1024,
      height: 1024
    };
  }
}

export default ImageToPsdStep;