export type SeedreamVersion = '4.0' | '4.5' | '5.0';

export type SeedreamSize = 
  | '1024x1024' 
  | '2048x2048' 
  | '3072x3072' 
  | '4096x4096'
  | '1K' 
  | '2K' 
  | '3K' 
  | '4K';

export type OutputFormat = 'png' | 'jpeg';
export type ResponseFormat = 'url' | 'b64_json';

export interface SeedreamOptions {
  version?: SeedreamVersion;
  size?: SeedreamSize;
  outputFormat?: OutputFormat;
  responseFormat?: ResponseFormat;
  watermark?: boolean;
  timeout?: number;
  optimizePromptMode?: 'standard' | 'fast';
  enableWebSearch?: boolean;
  referenceImages?: string[];
  enableBatchGeneration?: boolean;
  maxImages?: number;
}

export interface SeedreamResult {
  success: boolean;
  images: Array<{
    name: string;
    url?: string;
    base64?: string;
  }>;
  error?: string;
  model: string;
  version: SeedreamVersion;
  generationTime: number;
}

const MODELS: Record<SeedreamVersion, string> = {
  '4.0': 'doubao-seedream-4-0-250828',
  '4.5': 'doubao-seedream-4-5-251128',
  '5.0': 'doubao-seedream-5-0-260128',
};

const VERSION_DESCRIPTIONS: Record<SeedreamVersion, string> = {
  '4.0': 'Seedream 4.0 - 稳定可靠，适合日常使用，响应快速',
  '4.5': 'Seedream 4.5 - 细节表现更好，复杂场景处理更优',
  '5.0': 'Seedream 5.0 - 当前最强版本！突破性创意表达和超高细节质量！',
};

const SUPPORTED_FIELDS: Record<SeedreamVersion, string[]> = {
  '4.0': ['size', 'response_format', 'watermark', 'image', 'sequential_image_generation', 'stream', 'optimize_prompt_options'],
  '4.5': ['size', 'response_format', 'watermark', 'image', 'sequential_image_generation', 'stream', 'optimize_prompt_options'],
  '5.0': ['size', 'response_format', 'watermark', 'image', 'sequential_image_generation', 'tools', 'output_format', 'stream', 'optimize_prompt_options'],
};

export class SeedreamService {
  private apiKey: string | null = null;
  private apiBase: string;

  constructor() {
    if (typeof window !== 'undefined') {
      this.apiKey = localStorage.getItem('seedream_api_key') || 
                    localStorage.getItem('ARK_API_KEY') ||
                    localStorage.getItem('MODEL_IMAGE_API_KEY');
    }
    this.apiBase = 'https://ark.cn-beijing.volces.com/api/v3';
  }

  setApiKey(key: string): void {
    this.apiKey = key;
    if (typeof window !== 'undefined') {
      localStorage.setItem('seedream_api_key', key);
    }
  }

  getVersionInfo(version: SeedreamVersion): { model: string; description: string; supportedFields: string[] } {
    return {
      model: MODELS[version],
      description: VERSION_DESCRIPTIONS[version],
      supportedFields: SUPPORTED_FIELDS[version],
    };
  }

  listVersions(): void {
    console.log('\n=== Seedream 可用版本 ===\n');
    for (const [version, desc] of Object.entries(VERSION_DESCRIPTIONS)) {
      const model = MODELS[version as SeedreamVersion];
      console.log(`版本 ${version}:`);
      console.log(`  模型名称: ${model}`);
      console.log(`  描述: ${desc}`);
      console.log(`  支持参数: ${SUPPORTED_FIELDS[version as SeedreamVersion].join(', ')}`);
    }
  }

  async generate(
    prompt: string,
    options: SeedreamOptions = {}
  ): Promise<SeedreamResult> {
    const startTime = Date.now();
    const version = options.version || '5.0';

    if (!this.apiKey) {
      return {
        success: false,
        images: [],
        error: '请设置 API Key',
        model: MODELS[version],
        version,
        generationTime: Date.now() - startTime,
      };
    }

    try {
      const body: Record<string, unknown> = {
        model: MODELS[version],
        prompt,
        size: options.size || '2048x2048',
        response_format: options.responseFormat || 'url',
        watermark: options.watermark ?? false,
      };

      if (version === '5.0' && options.outputFormat) {
        body.output_format = options.outputFormat;
      }

      const url = `${this.apiBase}/images/generations`;

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`,
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        return {
          success: false,
          images: [],
          error: `API 请求失败: ${response.status}`,
          model: MODELS[version],
          version,
          generationTime: Date.now() - startTime,
        };
      }

      const data = await response.json();
      const images: SeedreamResult['images'] = [];

      if (data.data && Array.isArray(data.data)) {
        for (let i = 0; i < data.data.length; i++) {
          const imageData = data.data[i];
          if (imageData.url) {
            images.push({ name: `image_${i}`, url: imageData.url });
          } else if (imageData.b64_json) {
            const mimeType = options.outputFormat === 'jpeg' ? 'image/jpeg' : 'image/png';
            images.push({ 
              name: `image_${i}`, 
              base64: `data:${mimeType};base64,${imageData.b64_json}` 
            });
          }
        }
      }

      return {
        success: images.length > 0,
        images,
        model: MODELS[version],
        version,
        generationTime: Date.now() - startTime,
      };

    } catch (error) {
      return {
        success: false,
        images: [],
        error: error instanceof Error ? error.message : String(error),
        model: MODELS[version],
        version,
        generationTime: Date.now() - startTime,
      };
    }
  }
}

export default SeedreamService;
