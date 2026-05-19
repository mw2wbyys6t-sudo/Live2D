export interface ImageGenStepInput {
  prompt: string;
  negativePrompt?: string;
  width?: number;
  height?: number;
  style?: ImageStyle;
  resolution?: ResolutionPreset;
  quality?: QualityLevel;
  seed?: number;
  steps?: number;
  cfgScale?: number;
  sampler?: string;
  model?: string;
}

export type ImageStyle = 
  | 'anime' 
  | 'realistic' 
  | 'cel-shaded' 
  | 'watercolor' 
  | 'pixel-art' 
  | '3d-render' 
  | 'oil-painting';

export type ResolutionPreset = 
  | 'square-512' 
  | 'square-768' 
  | 'square-1024' 
  | 'square-1280'
  | 'portrait-512x768' 
  | 'portrait-768x1024' 
  | 'portrait-1024x1536'
  | 'landscape-768x512' 
  | 'landscape-1024x768' 
  | 'landscape-1536x1024';

export type QualityLevel = 'draft' | 'standard' | 'high' | 'ultra';

export interface ImageGenStepOutput {
  imagePath: string;
  imageUrl: string;
  seed: number;
  settings: ImageGenStepInput;
  generationTime: number;
  modelUsed: string;
}

const RESOLUTION_MAP: Record<ResolutionPreset, { width: number; height: number }> = {
  'square-512': { width: 512, height: 512 },
  'square-768': { width: 768, height: 768 },
  'square-1024': { width: 1024, height: 1024 },
  'square-1280': { width: 1280, height: 1280 },
  'portrait-512x768': { width: 512, height: 768 },
  'portrait-768x1024': { width: 768, height: 1024 },
  'portrait-1024x1536': { width: 1024, height: 1536 },
  'landscape-768x512': { width: 768, height: 512 },
  'landscape-1024x768': { width: 1024, height: 768 },
  'landscape-1536x1024': { width: 1536, height: 1024 },
};

const QUALITY_SETTINGS: Record<QualityLevel, { steps: number; cfg: number }> = {
  'draft': { steps: 15, cfg: 5.5 },
  'standard': { steps: 25, cfg: 7.0 },
  'high': { steps: 35, cfg: 7.5 },
  'ultra': { steps: 50, cfg: 8.0 },
};

const STYLE_PREFIXES: Record<ImageStyle, string> = {
  'anime': 'anime style, beautiful detailed anime artwork, anime aesthetic, sharp clean lines, vibrant colors, studio quality animation cel',
  'realistic': 'hyperrealistic, photorealistic, highly detailed, lifelike, cinematic lighting, professional photography',
  'cel-shaded': 'cel shaded, flat colors, clean outlines, 2D animation style, Toon shader, bold lines',
  'watercolor': 'watercolor painting, soft brush strokes, watercolor wash, delicate colors, artistic texture',
  'pixel-art': 'pixel art, retro 8-bit style, pixel perfect, nostalgic gaming aesthetic, crisp pixels',
  '3d-render': '3D render, blender, octane render, realistic materials, ray tracing, cinematic',
  'oil-painting': 'oil painting, brush strokes, classic art style, textured canvas, masterful technique',
};

const NEGATIVE_PROMPT_BASE = 'low quality, blurry, distorted, pixelated, ugly, deformed, bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, missing limb, floating limbs, disconnected limbs, malformed hands, long neck, bad proportions, watermark, text, signature, logo, cropped, out of frame';

export class ImageGenStep {
  private getResolution(preset: ResolutionPreset): { width: number; height: number } {
    return RESOLUTION_MAP[preset] || { width: 1024, height: 1024 };
  }

  private buildPrompt(input: ImageGenStepInput): string {
    const stylePrefix = input.style ? STYLE_PREFIXES[input.style] : STYLE_PREFIXES['anime'];
    
    const qualityKeywords = input.quality === 'ultra' 
      ? '8K, ultra detailed, masterpiece, award-winning, professional artwork, stunning visuals'
      : input.quality === 'high'
      ? '4K, highly detailed, high quality, professional artwork, beautiful composition'
      : input.quality === 'standard'
      ? 'high quality, detailed, clean artwork, good composition'
      : 'good quality, decent detail';

    const live2dKeywords = 'perfect for Live2D rigging, clean layer separation, isolated character, solid background, easy to rig';

    return `${stylePrefix}, ${input.prompt}, ${qualityKeywords}, ${live2dKeywords}`;
  }

  private buildNegativePrompt(input: ImageGenStepInput): string {
    const additionalNegatives: Record<ImageStyle, string> = {
      'anime': '3d, realistic, photo, photograph, text, watermark',
      'realistic': 'cartoon, anime, drawing, sketch, text, watermark',
      'cel-shaded': 'realistic, 3d render, photorealistic, text, watermark',
      'watercolor': 'digital art, 3d render, photorealistic, text, sharp edges',
      'pixel-art': 'smooth, anti-aliased, 3d, realistic, text',
      '3d-render': '2d, flat, cartoon, hand-drawn, text, watermark',
      'oil-painting': 'digital art, 3d render, photorealistic, text, watermark',
    };

    const styleNegatives = input.style ? additionalNegatives[input.style] : '';
    return `${NEGATIVE_PROMPT_BASE}${styleNegatives ? `, ${styleNegatives}` : ''}${input.negativePrompt ? `, ${input.negativePrompt}` : ''}`;
  }

  async execute(input: ImageGenStepInput): Promise<ImageGenStepOutput> {
    const startTime = Date.now();
    
    const seed = input.seed ?? Math.floor(Math.random() * 1000000);
    const resolution = this.getResolution(input.resolution || 'square-1024');
    const quality = QUALITY_SETTINGS[input.quality || 'standard'];
    
    const width = input.width || resolution.width;
    const height = input.height || resolution.height;
    const steps = input.steps || quality.steps;
    const cfg = input.cfgScale || quality.cfg;
    const sampler = input.sampler || 'euler';
    const model = input.model || 'sd_xl_base_1.0.safetensors';

    const finalPrompt = this.buildPrompt(input);
    const finalNegativePrompt = this.buildNegativePrompt(input);

    try {
      const result = await this.generateImage({
        prompt: finalPrompt,
        negativePrompt: finalNegativePrompt,
        width,
        height,
        seed,
        steps,
        cfg,
        sampler,
        model,
      });

      const generationTime = Date.now() - startTime;

      return {
        imagePath: result.imagePath,
        imageUrl: result.imageUrl,
        seed,
        settings: {
          ...input,
          width,
          height,
          steps,
          cfgScale: cfg,
          sampler,
          model,
        },
        generationTime,
        modelUsed: model,
      };
    } catch (error) {
      console.error('Image generation failed:', error);
      
      return {
        imagePath: `output/character-${seed}.png`,
        imageUrl: `https://neeko-copilot.bytedance.net/api/text2image?prompt=${encodeURIComponent(finalPrompt)}&image_size=portrait_16_9`,
        seed,
        settings: {
          ...input,
          width,
          height,
          steps,
          cfgScale: cfg,
          sampler,
          model,
        },
        generationTime: Date.now() - startTime,
        modelUsed: 'fallback',
      };
    }
  }

  private async generateImage(params: {
    prompt: string;
    negativePrompt: string;
    width: number;
    height: number;
    seed: number;
    steps: number;
    cfg: number;
    sampler: string;
    model: string;
  }): Promise<{ imagePath: string; imageUrl: string }> {
    const imagePath = `output/character-${params.seed}.png`;
    const imageUrl = `https://neeko-copilot.bytedance.net/api/text2image?prompt=${encodeURIComponent(params.prompt)}&image_size=portrait_16_9`;

    return { imagePath, imageUrl };
  }
}

export default ImageGenStep;
