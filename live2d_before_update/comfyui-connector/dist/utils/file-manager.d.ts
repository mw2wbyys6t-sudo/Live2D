export declare class FileManager {
    private outputDirectory;
    private tempDirectory;
    private maxCacheAge;
    constructor(outputDirectory?: string, tempDirectory?: string, maxCacheAge?: number);
    private ensureDirectories;
    saveImage(imageBuffer: Buffer, filename: string, subDirectory?: string): Promise<string>;
    loadImage(filePath: string): Promise<Buffer>;
    deleteFile(filePath: string): Promise<void>;
    copyFile(source: string, destination: string): Promise<void>;
    listFiles(directory: string, extension?: string): Promise<string[]>;
    getFileInfo(filePath: string): Promise<{
        path: string;
        name: string;
        size: number;
        created: Date;
        modified: Date;
    } | null>;
    cleanupOldFiles(directory: string, maxAge?: number): Promise<number>;
    createTempFile(data: Buffer, prefix?: string, extension?: string): Promise<string>;
    clearTempFiles(): Promise<number>;
    getOutputDirectory(): string;
    getTempDirectory(): string;
    setOutputDirectory(directory: string): void;
    setTempDirectory(directory: string): void;
}
//# sourceMappingURL=file-manager.d.ts.map