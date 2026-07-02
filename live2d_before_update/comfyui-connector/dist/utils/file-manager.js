"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.FileManager = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
class FileManager {
    constructor(outputDirectory = './output', tempDirectory = './temp', maxCacheAge = 86400000) {
        this.outputDirectory = outputDirectory;
        this.tempDirectory = tempDirectory;
        this.maxCacheAge = maxCacheAge;
        this.ensureDirectories();
    }
    ensureDirectories() {
        if (!fs.existsSync(this.outputDirectory)) {
            fs.mkdirSync(this.outputDirectory, { recursive: true });
        }
        if (!fs.existsSync(this.tempDirectory)) {
            fs.mkdirSync(this.tempDirectory, { recursive: true });
        }
    }
    async saveImage(imageBuffer, filename, subDirectory) {
        const directory = subDirectory ? path.join(this.outputDirectory, subDirectory) : this.outputDirectory;
        if (!fs.existsSync(directory)) {
            fs.mkdirSync(directory, { recursive: true });
        }
        const filePath = path.join(directory, filename);
        fs.writeFileSync(filePath, imageBuffer);
        return filePath;
    }
    async loadImage(filePath) {
        if (!fs.existsSync(filePath)) {
            throw new Error(`File not found: ${filePath}`);
        }
        return fs.readFileSync(filePath);
    }
    async deleteFile(filePath) {
        if (fs.existsSync(filePath)) {
            fs.unlinkSync(filePath);
        }
    }
    async copyFile(source, destination) {
        if (!fs.existsSync(source)) {
            throw new Error(`Source file not found: ${source}`);
        }
        const destDir = path.dirname(destination);
        if (!fs.existsSync(destDir)) {
            fs.mkdirSync(destDir, { recursive: true });
        }
        fs.copyFileSync(source, destination);
    }
    async listFiles(directory, extension) {
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
    async getFileInfo(filePath) {
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
    async cleanupOldFiles(directory, maxAge = this.maxCacheAge) {
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
            if (age >= maxAge) {
                fs.unlinkSync(filePath);
                deletedCount++;
            }
        }
        return deletedCount;
    }
    async createTempFile(data, prefix = 'temp', extension = 'png') {
        const filename = `${prefix}_${Date.now()}.${extension}`;
        const filePath = path.join(this.tempDirectory, filename);
        fs.writeFileSync(filePath, data);
        return filePath;
    }
    async clearTempFiles() {
        return this.cleanupOldFiles(this.tempDirectory, 0);
    }
    getOutputDirectory() {
        return this.outputDirectory;
    }
    getTempDirectory() {
        return this.tempDirectory;
    }
    setOutputDirectory(directory) {
        this.outputDirectory = directory;
        this.ensureDirectories();
    }
    setTempDirectory(directory) {
        this.tempDirectory = directory;
        this.ensureDirectories();
    }
}
exports.FileManager = FileManager;
//# sourceMappingURL=file-manager.js.map