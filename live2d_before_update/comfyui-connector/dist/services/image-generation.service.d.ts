import { ComfyUIConnector } from '../connectors/comfyui.connector';
import { GenerationInput, GenerationResult, GenerationProgress } from '../types';
export declare class ImageGenerationService {
    private connector;
    private autoSave;
    private autoCleanup;
    private maxRetries;
    private retryDelay;
    constructor(connector: ComfyUIConnector, options?: {
        autoSave?: boolean;
        autoCleanup?: boolean;
        maxRetries?: number;
        retryDelay?: number;
    });
    generate(input: GenerationInput): Promise<GenerationResult>;
    private buildWorkflow;
    private waitForCompletion;
    private sleep;
    getGenerationStatus(promptId: string): Promise<GenerationProgress>;
}
//# sourceMappingURL=image-generation.service.d.ts.map