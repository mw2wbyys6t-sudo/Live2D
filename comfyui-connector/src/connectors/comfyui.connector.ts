import axios, { AxiosInstance } from 'axios';
import FormData from 'form-data';
import * as fs from 'fs';
import * as path from 'path';
import { v4 as uuidv4 } from 'uuid';
import {
  ComfyUIConfig,
  GenerationInput,
  GenerationResult,
  HealthCheckResult,
  QueueItem,
  UploadResponse,
  ComfyUIHistory,
  GenerationProgress
} from '../types';

export class ComfyUIConnector {
  private client: AxiosInstance;
  private config: ComfyUIConfig;
  private outputDirectory: string;
  private tempDirectory: string;

  constructor(config?: Partial<ComfyUIConfig>) {
    this.config = {
      host: config?.host || '127.0.0.1',
      port: config?.port || 8188,
      protocol: config?.protocol || 'http',
      timeout: config?.timeout || 60000,
      outputDirectory: config?.outputDirectory || './output',
      tempDirectory: config?.tempDirectory || './temp'
    };

    const baseURL = `${this.config.protocol}://${this.config.host}:${this.config.port}`;
    this.client = axios.create({
      baseURL,
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    this.outputDirectory = this.config.outputDirectory;
    this.tempDirectory = this.config.tempDirectory;
    this.ensureDirectories();
  }

  private ensureDirectories(): void {
    if (!fs.existsSync(this.outputDirectory)) {
      fs.mkdirSync(this.outputDirectory, { recursive: true });
    }
    if (!fs.existsSync(this.tempDirectory)) {
      fs.mkdirSync(this.tempDirectory, { recursive: true });
    }
  }

  private getApiUrl(endpoint: string): string {
    return `${this.config.protocol}://${this.config.host}:${this.config.port}${endpoint}`;
  }

  async checkHealth(): Promise<HealthCheckResult> {
    try {
      const response = await this.client.get('/system_stats');
      return {
        success: true,
        connected: true,
        version: response.data.version || 'unknown',
        queue_size: response.data.queue_size || 0
      };
    } catch (error: any) {
      return {
        success: false,
        connected: false,
        error: error.message || 'Connection failed'
      };
    }
  }

  async uploadImage(imagePath: string, imageType: string = 'input'): Promise<UploadResponse> {
    try {
      const form = new FormData();
      form.append('image', fs.createReadStream(imagePath));
      form.append('type', imageType);

      const response = await this.client.post('/upload/image', form, {
        headers: form.getHeaders()
      });

      return response.data;
    } catch (error: any) {
      throw new Error(`Failed to upload image: ${error.message}`);
    }
  }

  async queuePrompt(promptWorkflow: object): Promise<{ prompt_id: string; number: number }> {
    try {
      const response = await this.client.post('/prompt', {
        prompt: promptWorkflow
      });
      return response.data;
    } catch (error: any) {
      throw new Error(`Failed to queue prompt: ${error.message}`);
    }
  }

  async getQueueInfo(): Promise<QueueItem[]> {
    try {
      const response = await this.client.get('/queue');
      const runningPrompts = response.data.running || [];
      const pendingPrompts = response.data.queue || [];

      const items: QueueItem[] = [];

      runningPrompts.forEach((item: any) => {
        items.push({
          prompt_id: item.prompt_id,
          status: 'running',
          progress: item.prompt?.progress || 0
        });
      });

      pendingPrompts.forEach((item: any, index: number) => {
        items.push({
          prompt_id: item.prompt_id,
          status: 'pending',
          progress: (index / (pendingPrompts.length + 1)) * 100
        });
      });

      return items;
    } catch (error: any) {
      throw new Error(`Failed to get queue info: ${error.message}`);
    }
  }

  async getHistory(promptId: string): Promise<ComfyUIHistory | null> {
    try {
      const response = await this.client.get(`/history/${promptId}`);
      return response.data[promptId] || null;
    } catch (error: any) {
      if (error.response?.status === 404) {
        return null;
      }
      throw new Error(`Failed to get history: ${error.message}`);
    }
  }

  async getProgress(promptId: string): Promise<GenerationProgress> {
    try {
      const response = await this.client.get(`/progress`);
      return {
        prompt_id: promptId,
        progress: response.data.value || 0,
        status: response.data.status === 'success' ? 'completed' : 'running'
      };
    } catch (error: any) {
      return {
        prompt_id: promptId,
        progress: 0,
        status: 'failed',
        message: error.message
      };
    }
  }

  async interruptExecution(): Promise<void> {
    try {
      await this.client.post('/interrupt');
    } catch (error: any) {
      throw new Error(`Failed to interrupt execution: ${error.message}`);
    }
  }

  async clearQueue(): Promise<void> {
    try {
      await this.client.post('/queue/clear');
    } catch (error: any) {
      throw new Error(`Failed to clear queue: ${error.message}`);
    }
  }

  getOutputImagePath(filename: string): string {
    return path.join(this.outputDirectory, filename);
  }

  async downloadImage(imageUrl: string, savePath?: string): Promise<string> {
    try {
      const filename = path.basename(imageUrl);
      const outputPath = savePath || path.join(this.outputDirectory, filename);

      const response = await this.client.get(imageUrl, {
        responseType: 'arraybuffer'
      });

      fs.writeFileSync(outputPath, Buffer.from(response.data));
      return outputPath;
    } catch (error: any) {
      throw new Error(`Failed to download image: ${error.message}`);
    }
  }

  async cleanupTempFiles(): Promise<void> {
    try {
      const files = fs.readdirSync(this.tempDirectory);
      for (const file of files) {
        const filePath = path.join(this.tempDirectory, file);
        fs.unlinkSync(filePath);
      }
    } catch (error: any) {
      console.error(`Failed to cleanup temp files: ${error.message}`);
    }
  }

  getConfig(): ComfyUIConfig {
    return { ...this.config };
  }

  setOutputDirectory(directory: string): void {
    this.outputDirectory = directory;
    this.config.outputDirectory = directory;
    this.ensureDirectories();
  }

  setTempDirectory(directory: string): void {
    this.tempDirectory = directory;
    this.config.tempDirectory = directory;
    this.ensureDirectories();
  }
}
