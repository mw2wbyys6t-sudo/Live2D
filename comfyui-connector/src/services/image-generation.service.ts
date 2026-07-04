import * as fs from 'fs';
import * as path from 'path';
import { v4 as uuidv4 } from 'uuid';
import { ComfyUIConnector } from '../connectors/comfyui.connector';
import { GenerationInput, GenerationResult, GenerationProgress } from '../types';

export class ImageGenerationService {
  private connector: ComfyUIConnector;
  private autoSave: boolean;
  private autoCleanup: boolean;
  private maxRetries: number;
  private retryDelay: number;

  constructor(connector: ComfyUIConnector, options?: {
    autoSave?: boolean;
    autoCleanup?: boolean;
    maxRetries?: number;
    retryDelay?: number;
  }) {
    this.connector = connector;
    this.autoSave = options?.autoSave ?? true;
    this.autoCleanup = options?.autoCleanup ?? true;
    this.maxRetries = options?.maxRetries ?? 3;
    this.retryDelay = options?.retryDelay ?? 5000;
  }

  async generate(input: GenerationInput): Promise<GenerationResult> {
    const startTime = Date.now();

    try {
      if (!input.prompt?.positive) {
        return {
          success: false,
          error: 'Positive prompt is required'
        };
      }

      let imageName: string | null = null;
      let maskName: string | null = null;

      if (input.image) {
        if (!fs.existsSync(input.image)) {
          return {
            success: false,
            error: `Input image not found: ${input.image}`
          };
        }
        const uploadResult = await this.connector.uploadImage(input.image);
        imageName = uploadResult.name;
      }

      if (input.mask) {
        if (!fs.existsSync(input.mask)) {
          return {
            success: false,
            error: `Mask image not found: ${input.mask}`
          };
        }
        const uploadResult = await this.connector.uploadImage(input.mask, 'mask');
        maskName = uploadResult.name;
      }

      const workflow = this.buildWorkflow(input, imageName, maskName);

      const { prompt_id } = await this.connector.queuePrompt(workflow);

      const result = await this.waitForCompletion(prompt_id);

      const duration = Date.now() - startTime;

      if (result.success && result.image_path) {
        if (this.autoCleanup) {
          await this.connector.cleanupTempFiles();
        }

        return {
          success: true,
          image_path: result.image_path,
          images: result.images,
          details: {
            prompt_id,
            status: 'completed',
            duration,
            seed: input.seed
          }
        };
      } else {
        return {
          success: false,
          error: result.error || 'Generation failed',
          details: {
            prompt_id,
            status: 'failed',
            duration
          }
        };
      }
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Unknown error occurred',
        details: {
          prompt_id: 'unknown',
          status: 'failed',
          duration: Date.now() - startTime
        }
      };
    }
  }

  private buildWorkflow(input: GenerationInput, imageName: string | null, maskName: string | null): object {
    const workflow: any = {};
    const seed = input.seed || Math.floor(Math.random() * 999999999);

    workflow['1'] = {
      class_type: 'CheckpointLoaderSimple',
      inputs: {
        ckpt_name: 'sd_xl_base_1.0.safetensors'
      }
    };

    workflow['2'] = {
      class_type: 'CLIPTextEncode',
      inputs: {
        text: input.prompt.positive,
        clip: ['1', 1]
      }
    };

    workflow['3'] = {
      class_type: 'CLIPTextEncode',
      inputs: {
        text: input.prompt.negative || 'low quality, blurry, deformed',
        clip: ['1', 1]
      }
    };

    if (imageName && maskName) {
      workflow['4'] = {
        class_type: 'LoadImage',
        inputs: {
          image: imageName
        }
      };

      workflow['5'] = {
        class_type: 'LoadImage',
        inputs: {
          image: maskName
        }
      };

      workflow['6'] = {
        class_type: 'KSampler',
        inputs: {
          seed: seed,
          steps: input.steps || 20,
          cfg: input.cfg || 7.0,
          sampler_name: 'euler',
          scheduler: 'normal',
          positive: ['2', 0],
          negative: ['3', 0],
          latent_image: ['9', 0]
        }
      };

      workflow['9'] = {
        class_type: 'VAEEncode',
        inputs: {
          pixels: ['4', 0],
          mask: ['5', 0],
          vae: ['1', 2]
        }
      };

      workflow['10'] = {
        class_type: 'VAEDecode',
        inputs: {
          samples: ['6', 0],
          vae: ['1', 2]
        }
      };
    } else if (imageName) {
      workflow['4'] = {
        class_type: 'LoadImage',
        inputs: {
          image: imageName
        }
      };

      workflow['6'] = {
        class_type: 'KSampler',
        inputs: {
          seed: seed,
          steps: input.steps || 20,
          cfg: input.cfg || 7.0,
          sampler_name: 'euler',
          scheduler: 'normal',
          positive: ['2', 0],
          negative: ['3', 0],
          latent_image: ['8', 0]
        }
      };

      workflow['8'] = {
        class_type: 'VAEEncode',
        inputs: {
          pixels: ['4', 0],
          vae: ['1', 2]
        }
      };

      workflow['10'] = {
        class_type: 'VAEDecode',
        inputs: {
          samples: ['6', 0],
          vae: ['1', 2]
        }
      };
    } else {
      const width = input.width || 1024;
      const height = input.height || 1024;

      workflow['4'] = {
        class_type: 'EmptyLatentImage',
        inputs: {
          batch_size: 1,
          height: height,
          width: width,
          seed: seed
        }
      };

      workflow['6'] = {
        class_type: 'KSampler',
        inputs: {
          seed: seed,
          steps: input.steps || 20,
          cfg: input.cfg || 7.0,
          sampler_name: 'euler',
          scheduler: 'normal',
          positive: ['2', 0],
          negative: ['3', 0],
          latent_image: ['4', 0]
        }
      };

      workflow['10'] = {
        class_type: 'VAEDecode',
        inputs: {
          samples: ['6', 0],
          vae: ['1', 2]
        }
      };
    }

    workflow['11'] = {
      class_type: 'SaveImage',
      inputs: {
        filename_prefix: `generated_${uuidv4().slice(0, 8)}`,
        images: ['10', 0]
      }
    };

    return workflow;
  }

  private async waitForCompletion(promptId: string, maxWaitTime: number = 300000): Promise<{
    success: boolean;
    image_path?: string;
    images?: string[];
    error?: string;
  }> {
    const startTime = Date.now();

    while (Date.now() - startTime < maxWaitTime) {
      const history = await this.connector.getHistory(promptId);

      if (history && history.outputs) {
        const outputImages: string[] = [];

        for (const [nodeId, nodeOutput] of Object.entries(history.outputs)) {
          if (nodeOutput?.images) {
            for (const imageInfo of nodeOutput.images) {
              const imagePath = imageInfo.filename;
              const imageUrl = `/view?filename=${imagePath}&type=output`;
              const fullPath = this.connector.getOutputImagePath(imagePath);

              if (fs.existsSync(fullPath)) {
                outputImages.push(fullPath);
              }

              try {
                const downloadedPath = await this.connector.downloadImage(imageUrl);
                outputImages.push(downloadedPath);
              } catch (error) {
                console.error(`Failed to download image ${imagePath}:`, error);
              }
            }
          }
        }

        if (outputImages.length > 0) {
          return {
            success: true,
            image_path: outputImages[0],
            images: outputImages
          };
        } else {
          return {
            success: false,
            error: 'No output images found'
          };
        }
      }

      const queueInfo = await this.connector.getQueueInfo();
      const currentItem = queueInfo.find(item => item.prompt_id === promptId);

      if (!currentItem) {
        await this.sleep(this.retryDelay);
      } else if (currentItem.status === 'running') {
        const progress = await this.connector.getProgress(promptId);
        console.log(`Generation progress: ${progress.progress}%`);
        await this.sleep(this.retryDelay);
      } else if (currentItem.status === 'failed') {
        return {
          success: false,
          error: 'Generation failed'
        };
      }
    }

    return {
      success: false,
      error: 'Timeout waiting for generation to complete'
    };
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async getGenerationStatus(promptId: string): Promise<GenerationProgress> {
    const history = await this.connector.getHistory(promptId);

    if (history) {
      return {
        prompt_id: promptId,
        progress: 100,
        status: 'completed'
      };
    }

    const queueInfo = await this.connector.getQueueInfo();
    const currentItem = queueInfo.find(item => item.prompt_id === promptId);

    if (!currentItem) {
      return {
        prompt_id: promptId,
        progress: 0,
        status: 'queued'
      };
    }

    const mappedStatus: 'queued' | 'running' | 'completed' | 'failed' =
      currentItem.status === 'pending' ? 'queued' : currentItem.status;

    return {
      prompt_id: promptId,
      progress: currentItem.progress || 0,
      status: mappedStatus
    };
  }
}
