import * as fs from 'fs';
import * as path from 'path';

export class FileManager {
  private outputDirectory: string;
  private tempDirectory: string;
  private maxCacheAge: number;

  constructor(outputDirectory: string = './output', tempDirectory: string = './temp', maxCacheAge: number = 86400000) {
    this.outputDirectory = outputDirectory;
    this.tempDirectory = tempDirectory;
    this.maxCacheAge = maxCacheAge;
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

  async saveImage(imageBuffer: Buffer, filename: string, subDirectory?: string): Promise<string> {
    const directory = subDirectory ? path.join(this.outputDirectory, subDirectory) : this.outputDirectory;

    if (!fs.existsSync(directory)) {
      fs.mkdirSync(directory, { recursive: true });
    }

    const filePath = path.join(directory, filename);
    fs.writeFileSync(filePath, imageBuffer);
    return filePath;
  }

  async loadImage(filePath: string): Promise<Buffer> {
    if (!fs.existsSync(filePath)) {
      throw new Error(`File not found: ${filePath}`);
    }
    return fs.readFileSync(filePath);
  }

  async deleteFile(filePath: string): Promise<void> {
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }
  }

  async copyFile(source: string, destination: string): Promise<void> {
    if (!fs.existsSync(source)) {
      throw new Error(`Source file not found: ${source}`);
    }

    const destDir = path.dirname(destination);
    if (!fs.existsSync(destDir)) {
      fs.mkdirSync(destDir, { recursive: true });
    }

    fs.copyFileSync(source, destination);
  }

  async listFiles(directory: string, extension?: string): Promise<string[]> {
    if (!fs.existsSync(directory)) {
      return [];
    }

    const files = fs.readdirSync(directory);

    if (extension) {
      return files
        .filter(file => path.extname(file) === extension)
        .map(file => path.join(directory, file));
    }

    return files.map(file => path.join(directory, file));
  }

  async getFileInfo(filePath: string): Promise<{
    path: string;
    name: string;
    size: number;
    created: Date;
    modified: Date;
  } | null> {
    if (!fs.existsSync(filePath)) {
      return null;
    }

    const stats = fs.statSync(filePath);
    return {
      path: filePath,
      name: path.basename(filePath),
      size: stats.size,
      created: stats.birthtime,
      modified: stats.mtime
    };
  }

  async cleanupOldFiles(directory: string, maxAge: number = this.maxCacheAge): Promise<number> {
    if (!fs.existsSync(directory)) {
      return 0;
    }

    const files = fs.readdirSync(directory);
    let deletedCount = 0;
    const now = Date.now();

    for (const file of files) {
      const filePath = path.join(directory, file);
      const stats = fs.statSync(filePath);
      const age = now - stats.mtime.getTime();

      if (age > maxAge) {
        fs.unlinkSync(filePath);
        deletedCount++;
      }
    }

    return deletedCount;
  }

  async createTempFile(data: Buffer, prefix: string = 'temp', extension: string = 'png'): Promise<string> {
    const filename = `${prefix}_${Date.now()}.${extension}`;
    const filePath = path.join(this.tempDirectory, filename);
    fs.writeFileSync(filePath, data);
    return filePath;
  }

  async clearTempFiles(): Promise<number> {
    return this.cleanupOldFiles(this.tempDirectory, 0);
  }

  getOutputDirectory(): string {
    return this.outputDirectory;
  }

  getTempDirectory(): string {
    return this.tempDirectory;
  }

  setOutputDirectory(directory: string): void {
    this.outputDirectory = directory;
    this.ensureDirectories();
  }

  setTempDirectory(directory: string): void {
    this.tempDirectory = directory;
    this.ensureDirectories();
  }
}
