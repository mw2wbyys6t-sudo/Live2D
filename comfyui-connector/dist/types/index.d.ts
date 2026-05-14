export interface ComfyUIConfig {
    host: string;
    port: number;
    protocol: 'http' | 'https';
    timeout: number;
    outputDirectory: string;
    tempDirectory: string;
}
export interface GenerationPrompt {
    positive: string;
    negative?: string;
}
export interface GenerationInput {
    image?: string;
    mask?: string;
    prompt: GenerationPrompt;
    width?: number;
    height?: number;
    steps?: number;
    cfg?: number;
    seed?: number;
}
export interface GenerationResult {
    success: boolean;
    image_path?: string;
    images?: string[];
    error?: string;
    details?: {
        prompt_id: string;
        status: string;
        duration?: number;
        seed?: number;
    };
}
export interface HealthCheckResult {
    success: boolean;
    connected: boolean;
    version?: string;
    queue_size?: number;
    error?: string;
}
export interface QueueItem {
    prompt_id: string;
    status: 'pending' | 'running' | 'completed' | 'failed';
    progress?: number;
    outputs?: any;
}
export interface UploadResponse {
    name: string;
    image_type: string;
}
export interface ComfyUIHistory {
    prompt_id: string;
    status: string;
    outputs: Record<string, any>;
}
export interface FileInfo {
    path: string;
    name: string;
    size: number;
    created: Date;
}
export interface GenerationProgress {
    prompt_id: string;
    progress: number;
    status: 'queued' | 'running' | 'completed' | 'failed';
    message?: string;
}
export interface ConnectorOptions {
    config?: Partial<ComfyUIConfig>;
    autoSave?: boolean;
    autoCleanup?: boolean;
    maxRetries?: number;
    retryDelay?: number;
}
//# sourceMappingURL=index.d.ts.map