import { ComfyUIConfig, HealthCheckResult, QueueItem, UploadResponse, ComfyUIHistory, GenerationProgress } from '../types';
export declare class ComfyUIConnector {
    private client;
    private config;
    private outputDirectory;
    private tempDirectory;
    constructor(config?: Partial<ComfyUIConfig>);
    private ensureDirectories;
    private getApiUrl;
    checkHealth(): Promise<HealthCheckResult>;
    uploadImage(imagePath: string, imageType?: string): Promise<UploadResponse>;
    queuePrompt(promptWorkflow: object): Promise<{
        prompt_id: string;
        number: number;
    }>;
    getQueueInfo(): Promise<QueueItem[]>;
    getHistory(promptId: string): Promise<ComfyUIHistory | null>;
    getProgress(promptId: string): Promise<GenerationProgress>;
    interruptExecution(): Promise<void>;
    clearQueue(): Promise<void>;
    getOutputImagePath(filename: string): string;
    downloadImage(imageUrl: string, savePath?: string): Promise<string>;
    cleanupTempFiles(): Promise<void>;
    getConfig(): ComfyUIConfig;
    setOutputDirectory(directory: string): void;
    setTempDirectory(directory: string): void;
}
//# sourceMappingURL=comfyui.connector.d.ts.map