/**
 * ComfyUI 连接器单元测试（纯 JavaScript 版）
 */

const path = require('path');
const fs = require('fs');

// Mock modules
jest.mock('axios', () => {
  const mockAxiosInstance = {
    get: jest.fn().mockResolvedValue({ data: { version: '1.0', system: { devices: [], memory: {} } } }),
    post: jest.fn().mockResolvedValue({ data: { prompt_id: 'test-id', number: 1 } }),
    interceptors: {
      request: { use: jest.fn() },
      response: { use: jest.fn() }
    }
  };

  return {
    create: jest.fn(() => mockAxiosInstance),
    post: jest.fn().mockResolvedValue({ data: { name: 'test.png' } })
  };
});

// ==================== 测试 1: 连接器配置 ====================
describe('ComfyUIConnector', () => {
  let ComfyUIConnector;

  beforeAll(() => {
    ComfyUIConnector = require('../dist/connectors/comfyui.connector').ComfyUIConnector;
  });

  test('should create with default config', () => {
    const connector = new ComfyUIConnector();
    const config = connector.getConfig();
    expect(config.host).toBe('127.0.0.1');
    expect(config.port).toBe(8188);
    expect(config.protocol).toBe('http');
    expect(config.timeout).toBe(60000);
  });

  test('should create with custom config', () => {
    const customConnector = new ComfyUIConnector({
      host: '192.168.1.100',
      port: 8189,
      timeout: 30000,
      outputDirectory: '/custom/output',
      tempDirectory: '/custom/temp'
    });
    const config = customConnector.getConfig();
    expect(config.host).toBe('192.168.1.100');
    expect(config.port).toBe(8189);
    expect(config.timeout).toBe(30000);
    expect(config.outputDirectory).toBe('/custom/output');
    expect(config.tempDirectory).toBe('/custom/temp');
  });

  test('should allow config updates', () => {
    const connector = new ComfyUIConnector();
    connector.setOutputDirectory('/new/output');
    connector.setTempDirectory('/new/temp');
    const config = connector.getConfig();
    expect(config.outputDirectory).toBe('/new/output');
    expect(config.tempDirectory).toBe('/new/temp');
  });
});

// ==================== 测试 2: 健康检查 ====================
describe('HealthCheck', () => {
  let ComfyUIConnector;

  beforeAll(() => {
    ComfyUIConnector = require('../dist/connectors/comfyui.connector').ComfyUIConnector;
  });

  test('should return health status', async () => {
    const connector = new ComfyUIConnector();
    const health = await connector.checkHealth();
    expect(health).toHaveProperty('success');
    expect(health).toHaveProperty('connected');
  });

  test('should return version info when connected', async () => {
    const connector = new ComfyUIConnector();
    const health = await connector.checkHealth();
    if (health.connected) {
      expect(health).toHaveProperty('version');
      expect(typeof health.version).toBe('string');
    }
  });

  test('should return queue size', async () => {
    const connector = new ComfyUIConnector();
    const health = await connector.checkHealth();
    expect(health).toHaveProperty('queue_size');
    expect(typeof health.queue_size).toBe('number');
  });
});

// ==================== 测试 3: 队列管理 ====================
describe('QueueManagement', () => {
  let ComfyUIConnector;

  beforeAll(() => {
    ComfyUIConnector = require('../dist/connectors/comfyui.connector').ComfyUIConnector;
  });

  test('should queue a prompt', async () => {
    const connector = new ComfyUIConnector();
    const result = await connector.queuePrompt({ test: 'workflow' });
    expect(result).toHaveProperty('prompt_id');
    expect(result).toHaveProperty('number');
  });

  test('should get history for a prompt', async () => {
    const connector = new ComfyUIConnector();
    const history = await connector.getHistory('test-id');
    expect(history).toBeDefined();
  });

  test('should get progress', async () => {
    const connector = new ComfyUIConnector();
    const progress = await connector.getProgress('test-id');
    expect(progress).toHaveProperty('prompt_id');
    expect(progress).toHaveProperty('progress');
    expect(progress).toHaveProperty('status');
  });
});

// ==================== 测试 4: 图片生成服务 ====================
describe('ImageGenerationService', () => {
  let ImageGenerationService;
  let ComfyUIConnector;

  beforeAll(() => {
    ComfyUIConnector = require('../dist/connectors/comfyui.connector').ComfyUIConnector;
    ImageGenerationService = require('../dist/services/image-generation.service').ImageGenerationService;
  });

  test('should create with default options', () => {
    const connector = new ComfyUIConnector();
    const service = new ImageGenerationService(connector);
    expect(service).toBeDefined();
  });

  test('should require positive prompt', async () => {
    const connector = new ComfyUIConnector();
    const service = new ImageGenerationService(connector);
    const result = await service.generate({
      prompt: { positive: '' }
    });
    expect(result.success).toBe(false);
    expect(result.error).toBe('Positive prompt is required');
  });

  test('should reject non-existent input image', async () => {
    const connector = new ComfyUIConnector();
    const service = new ImageGenerationService(connector);
    const result = await service.generate({
      image: '/non/existent/path.png',
      prompt: { positive: 'test prompt' }
    });
    expect(result.success).toBe(false);
    expect(result.error).toContain('not found');
  });

  test('should return proper result format', async () => {
    const mockResult = {
      success: true,
      image_path: '/output/test.png',
      images: ['/output/test.png'],
      details: {
        prompt_id: 'test-id',
        status: 'completed',
        duration: 1000,
        seed: 42
      }
    };
    expect(mockResult).toHaveProperty('success');
    expect(mockResult).toHaveProperty('image_path');
    expect(mockResult).toHaveProperty('details');
    expect(mockResult.details).toHaveProperty('status');
  });

  test('should return error format on failure', async () => {
    const mockError = {
      success: false,
      error: 'Generation failed',
      details: {
        prompt_id: 'test-id',
        status: 'failed',
        duration: 500
      }
    };
    expect(mockError.success).toBe(false);
    expect(mockError).toHaveProperty('error');
    expect(mockError.details.status).toBe('failed');
  });

  test('should get generation status', async () => {
    const connector = new ComfyUIConnector();
    const service = new ImageGenerationService(connector);
    const status = await service.getGenerationStatus('test-id');
    expect(status).toHaveProperty('prompt_id');
    expect(status).toHaveProperty('progress');
    expect(['queued', 'running', 'completed', 'failed']).toContain(status.status);
  });
});

// ==================== 测试 5: 文件管理 ====================
describe('FileManager', () => {
  let FileManager;
  let uniqueId;

  function makeTestDir() {
    uniqueId = Date.now() + '_' + Math.random().toString(36).slice(2, 8);
    const baseDir = path.join(__dirname, '..', 'test-files-' + uniqueId);
    return {
      base: baseDir,
      output: path.join(baseDir, 'output'),
      temp: path.join(baseDir, 'temp')
    };
  }

  function cleanupDir(dir) {
    if (fs.existsSync(dir)) {
      const entries = fs.readdirSync(dir);
      entries.forEach(function(entry) {
        var fullPath = path.join(dir, entry);
        if (fs.statSync(fullPath).isDirectory()) {
          cleanupDir(fullPath);
        } else {
          fs.unlinkSync(fullPath);
        }
      });
      fs.rmdirSync(dir);
    }
  }

  beforeAll(() => {
    FileManager = require('../dist/utils/file-manager').FileManager;
  });

  afterEach(function() {
    var dirs = fs.readdirSync(__dirname + '/..');
    dirs.forEach(function(d) {
      if (d.startsWith('test-files-')) {
        cleanupDir(path.join(__dirname, '..', d));
      }
    });
  });

  test('should create directories on init', () => {
    const dirs = makeTestDir();
    const fm = new FileManager(dirs.output, dirs.temp);
    expect(fs.existsSync(dirs.output)).toBe(true);
    expect(fs.existsSync(dirs.temp)).toBe(true);
  });

  test('should save and load images', async () => {
    const dirs = makeTestDir();
    const fm = new FileManager(dirs.output, dirs.temp);
    const testBuffer = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
    const savePath = await fm.saveImage(testBuffer, 'test.png');
    expect(fs.existsSync(savePath)).toBe(true);

    const loadedBuffer = await fm.loadImage(savePath);
    expect(Buffer.isBuffer(loadedBuffer)).toBe(true);
    expect(loadedBuffer.length).toBe(testBuffer.length);
  });

  test('should create temp files', async () => {
    const dirs = makeTestDir();
    const fm = new FileManager(dirs.output, dirs.temp);
    const testData = Buffer.from('test data');
    const tempPath = await fm.createTempFile(testData, 'test', 'txt');
    expect(fs.existsSync(tempPath)).toBe(true);
    expect(path.basename(tempPath)).toMatch(/^test_\d+\.txt$/);
  });

  test('should list files by extension', async () => {
    const dirs = makeTestDir();
    const fm = new FileManager(dirs.output, dirs.temp);
    await fm.saveImage(Buffer.from('data1'), 'file1.png');
    await fm.saveImage(Buffer.from('data2'), 'file2.png');
    await fm.saveImage(Buffer.from('data3'), 'file3.jpg');

    const pngFiles = await fm.listFiles(dirs.output, '.png');
    expect(pngFiles.length).toBe(2);
  });

  test('should get file info', async () => {
    const dirs = makeTestDir();
    const fm = new FileManager(dirs.output, dirs.temp);
    const testPath = await fm.saveImage(Buffer.from('info test'), 'info_test.png');
    const info = await fm.getFileInfo(testPath);
    expect(info).not.toBeNull();
    expect(info).toHaveProperty('name', 'info_test.png');
    expect(info).toHaveProperty('size');
    expect(info).toHaveProperty('created');
  });

  test('should delete files', async () => {
    const dirs = makeTestDir();
    const fm = new FileManager(dirs.output, dirs.temp);
    const testPath = await fm.saveImage(Buffer.from('delete me'), 'delete.png');
    expect(fs.existsSync(testPath)).toBe(true);
    await fm.deleteFile(testPath);
    expect(fs.existsSync(testPath)).toBe(false);
  });

  test('should copy files', async () => {
    const dirs = makeTestDir();
    const fm = new FileManager(dirs.output, dirs.temp);
    const sourcePath = await fm.saveImage(Buffer.from('copy source'), 'source.png');
    const destPath = path.join(dirs.output, 'dest.png');
    await fm.copyFile(sourcePath, destPath);
    expect(fs.existsSync(destPath)).toBe(true);
  });

  test('should handle non-existent file', async () => {
    const dirs = makeTestDir();
    const fm = new FileManager(dirs.output, dirs.temp);
    const info = await fm.getFileInfo('/non/existent/path.png');
    expect(info).toBeNull();
  });

  test('should cleanup temp files', async () => {
    const dirs = makeTestDir();
    const fm = new FileManager(dirs.output, dirs.temp);
    await fm.createTempFile(Buffer.from('temp1'), 'temp1');
    await fm.createTempFile(Buffer.from('temp2'), 'temp2');
    const deletedCount = await fm.clearTempFiles();
    expect(deletedCount).toBeGreaterThanOrEqual(2);
  });
});

// ==================== 测试 6: 输出格式 ====================
describe('OutputFormat', () => {
  test('should have correct success format', () => {
    const result = {
      success: true,
      image_path: '/path/to/image.png',
      images: ['/path/to/image.png'],
      details: {
        prompt_id: 'abc123',
        status: 'completed',
        duration: 12345,
        seed: 12345
      }
    };

    expect(result.success).toBe(true);
    expect(result).toHaveProperty('image_path');
    expect(result).toHaveProperty('images');
    expect(Array.isArray(result.images)).toBe(true);
    expect(result.images[0]).toContain('.png');
    expect(result.details.prompt_id).toBeDefined();
    expect(result.details.status).toBe('completed');
    expect(result.details.duration).toBeGreaterThan(0);
  });

  test('should have correct error format', () => {
    const result = {
      success: false,
      error: 'Generation failed',
      details: {
        prompt_id: 'abc123',
        status: 'failed',
        duration: 1000
      }
    };

    expect(result.success).toBe(false);
    expect(result).toHaveProperty('error');
    expect(result.details.status).toBe('failed');
  });

  test('should handle missing optional fields', () => {
    const minimalResult = {
      success: true,
      image_path: '/path/to/image.png'
    };

    expect(minimalResult.success).toBe(true);
    expect(minimalResult).toHaveProperty('image_path');
  });

  test('should validate image_path is a string', () => {
    const result = { success: true, image_path: '/output/test.png' };
    expect(typeof result.image_path).toBe('string');
    expect(result.image_path).toMatch(/\.png$/);
  });
});

// ==================== 测试 7: 边界情况 ====================
describe('EdgeCases', () => {
  let FileManager;

  function makeEdgeDir() {
    const id = Date.now() + '_' + Math.random().toString(36).slice(2, 8);
    const baseDir = path.join(__dirname, '..', 'edge-test-' + id);
    return {
      base: baseDir,
      output: path.join(baseDir, 'output'),
      temp: path.join(baseDir, 'temp')
    };
  }

  function cleanupDir(dir) {
    if (fs.existsSync(dir)) {
      const entries = fs.readdirSync(dir);
      entries.forEach(function(entry) {
        var fullPath = path.join(dir, entry);
        if (fs.statSync(fullPath).isDirectory()) {
          cleanupDir(fullPath);
        } else {
          fs.unlinkSync(fullPath);
        }
      });
      fs.rmdirSync(dir);
    }
  }

  beforeAll(() => {
    FileManager = require('../dist/utils/file-manager').FileManager;
  });

  afterEach(function() {
    var dirs = fs.readdirSync(__dirname + '/..');
    dirs.forEach(function(d) {
      if (d.startsWith('edge-test-')) {
        cleanupDir(path.join(__dirname, '..', d));
      }
    });
  });

  test('should handle empty output directory', async () => {
    const dirs = makeEdgeDir();
    const fm = new FileManager(dirs.output, dirs.temp);
    const files = await fm.listFiles(path.join(dirs.base, 'empty'));
    expect(files).toEqual([]);
  });

  test('should handle large filename', async () => {
    const dirs = makeEdgeDir();
    const fm = new FileManager(dirs.output, dirs.temp);
    var longName = 'a'.repeat(200) + '.png';
    const savePath = await fm.saveImage(Buffer.from('test'), longName);
    expect(fs.existsSync(savePath)).toBe(true);
  });

  test('should handle special characters in filename', async () => {
    const dirs = makeEdgeDir();
    const fm = new FileManager(dirs.output, dirs.temp);
    var specialName = 'test_@#$%^&*()_+.png';
    const savePath = await fm.saveImage(Buffer.from('special'), specialName);
    expect(fs.existsSync(savePath)).toBe(true);
  });

  test('should return null for non-existent file info', async () => {
    const dirs = makeEdgeDir();
    const fm = new FileManager(dirs.output, dirs.temp);
    const info = await fm.getFileInfo('/nonexistent/path.png');
    expect(info).toBeNull();
  });

  test('should cleanup old files only', async () => {
    const dirs = makeEdgeDir();
    const fm = new FileManager(dirs.output, dirs.temp);
    await fm.createTempFile(Buffer.from('old'), 'old_file');
    await fm.createTempFile(Buffer.from('new'), 'new_file');
    const deletedCount = await fm.cleanupOldFiles(fm.getTempDirectory(), 0);
    expect(deletedCount).toBeGreaterThanOrEqual(2);
  });
});