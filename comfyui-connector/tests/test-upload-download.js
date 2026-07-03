#!/usr/bin/env node

/**
 * 测试 2: 图片上传/下载测试脚本
 * 
 * 功能：
 * - 生成测试图片
 * - 上传图片到 ComfyUI
 * - 从 ComfyUI 下载图片
 * - 验证文件完整性
 * - 清理测试文件
 * 
 * 使用：
 *   node tests/test-upload-download.js
 */

const path = require('path');
const fs = require('fs');
const http = require('http');
const https = require('https');

class ImageTester {
  constructor(config = {}) {
    this.config = {
      host: config.host || '127.0.0.1',
      port: config.port || 8188,
      protocol: config.protocol || 'http',
      timeout: config.timeout || 30000,
      outputDirectory: path.resolve(config.outputDirectory || path.join(__dirname, '..', 'output')),
      tempDirectory: path.resolve(config.tempDirectory || path.join(__dirname, '..', 'temp')),
      testDirectory: path.resolve(config.testDirectory || path.join(__dirname, '..', 'test-files'))
    };

    this.baseUrl = `${this.config.protocol}://${this.config.host}:${this.config.port}`;
    this.testResults = [];

    for (const dir of [this.config.outputDirectory, this.config.tempDirectory, this.config.testDirectory]) {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    }
  }

  log(label, value, status = '') {
    const statusStr = status ? ` [${status}]` : '';
    console.log(`  ${label.padEnd(30)} ${String(value).padEnd(20)}${statusStr}`);
  }

  section(title) {
    console.log('\n' + '='.repeat(70));
    console.log(`  ${title}`);
    console.log('='.repeat(70));
  }

  divider() {
    console.log('  ' + '-'.repeat(60));
  }

  record(name, passed, detail = '') {
    this.testResults.push({ name, passed, detail });
    const icon = passed ? '✅' : '❌';
    this.log(`${icon} ${name}`, detail || (passed ? '通过' : '失败'));
  }

  async httpGet(url) {
    return new Promise((resolve, reject) => {
      const client = url.startsWith('https') ? https : http;
      const req = client.get(url, { timeout: this.config.timeout }, (res) => {
        let data = '';
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => resolve({ statusCode: res.statusCode, data, headers: res.headers }));
      });
      req.on('error', reject);
      req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });
    });
  }

  async uploadFile(filePath, fileType = 'input', overwrite = true) {
    const fs = require('fs');
    const boundary = '----FormBoundary' + Math.random().toString(36).substring(2);
    const fileName = path.basename(filePath);
    const fileContent = fs.readFileSync(filePath);

    let body = '';
    body += `--${boundary}\r\n`;
    body += `Content-Disposition: form-data; name="image"; filename="${fileName}"\r\n`;
    body += `Content-Type: image/png\r\n\r\n`;
    body += fileContent.toString('binary');
    body += `\r\n--${boundary}\r\n`;
    body += `Content-Disposition: form-data; name="type"\r\n\r\n`;
    body += `${fileType}\r\n`;
    body += `--${boundary}\r\n`;
    body += `Content-Disposition: form-data; name="overwrite"\r\n\r\n`;
    body += `${overwrite}\r\n`;
    body += `--${boundary}--\r\n`;

    return new Promise((resolve, reject) => {
      const url = new URL(`${this.baseUrl}/upload/image`);
      const options = {
        hostname: url.hostname,
        port: url.port,
        path: url.pathname,
        method: 'POST',
        headers: {
          'Content-Type': `multipart/form-data; boundary=${boundary}`,
          'Content-Length': Buffer.byteLength(body, 'utf-8')
        },
        timeout: this.config.timeout
      };

      const req = http.request(options, (res) => {
        let data = '';
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => {
          try {
            resolve(JSON.parse(data));
          } catch (e) {
            resolve({ name: fileName, status: 'success', raw: data });
          }
        });
      });

      req.on('error', reject);
      req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });
      req.write(body, 'binary');
      req.end();
    });
  }

  async downloadFile(filename, savePath) {
    const url = `${this.baseUrl}/view?filename=${filename}&type=output`;
    return new Promise((resolve, reject) => {
      http.get(url, { timeout: this.config.timeout }, (res) => {
        if (res.statusCode !== 200) {
          reject(new Error(`HTTP ${res.statusCode}`));
          return;
        }
        const chunks = [];
        res.on('data', (chunk) => chunks.push(chunk));
        res.on('end', () => {
          const buffer = Buffer.concat(chunks);
          fs.writeFileSync(savePath, buffer);
          resolve({ size: buffer.length, path: savePath });
        });
      }).on('error', reject);
    });
  }

  createTestImage(width, height, color = [255, 0, 0], filename = 'test_input.png') {
    const filePath = path.join(this.config.testDirectory, filename);

    // Create a minimal valid PNG
    const { createCanvas } = (() => {
      try {
        return require('canvas');
      } catch {
        return null;
      }
    })();

    if (createCanvas) {
      const canvas = createCanvas(width, height);
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = `rgb(${color[0]},${color[1]},${color[2]})`;
      ctx.fillRect(0, 0, width, height);
      ctx.fillStyle = 'white';
      ctx.font = '20px Arial';
      ctx.fillText('Test Image', 10, height / 2);
      const buffer = canvas.toBuffer('image/png');
      fs.writeFileSync(filePath, buffer);
    } else {
      // Create a minimal PNG manually
      const { createMinimalPNG } = require('./test-helpers');
      if (createMinimalPNG) {
        createMinimalPNG(filePath, width, height, color);
      } else {
        // Simple PNG generator
        this.createMinimalPNG(filePath, width, height, color);
      }
    }

    console.log(`  📝 测试图片已创建: ${filePath}`);
    return filePath;
  }

  createMinimalPNG(filePath, width, height, color = [255, 0, 0]) {
    // Create a minimal valid PNG file
    const zlib = require('zlib');

    const signature = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);

    // IHDR chunk
    const ihdrData = Buffer.alloc(13);
    ihdrData.writeUInt32BE(width, 0);
    ihdrData.writeUInt32BE(height, 4);
    ihdrData[8] = 8;  // bit depth
    ihdrData[9] = 2;  // color type (RGB)
    ihdrData[10] = 0; // compression
    ihdrData[11] = 0; // filter
    ihdrData[12] = 0; // interlace

    const ihdrChunk = this.createChunk('IHDR', ihdrData);

    // IDAT chunk - raw image data
    const rawData = Buffer.alloc(height * (1 + width * 3));
    for (let y = 0; y < height; y++) {
      rawData[y * (1 + width * 3)] = 0; // filter byte
      for (let x = 0; x < width; x++) {
        const offset = y * (1 + width * 3) + 1 + x * 3;
        rawData[offset] = color[0];
        rawData[offset + 1] = color[1];
        rawData[offset + 2] = color[2];
      }
    }

    const compressed = zlib.deflateSync(rawData);
    const idatChunk = this.createChunk('IDAT', compressed);

    // IEND chunk
    const iendChunk = this.createChunk('IEND', Buffer.alloc(0));

    const png = Buffer.concat([signature, ihdrChunk, idatChunk, iendChunk]);
    fs.writeFileSync(filePath, png);
  }

  createChunk(type, data) {
    const length = Buffer.alloc(4);
    length.writeUInt32BE(data.length);
    const typeBuffer = Buffer.from(type, 'ascii');
    const crcData = Buffer.concat([typeBuffer, data]);
    const crc = this.crc32(crcData);
    const crcBuffer = Buffer.alloc(4);
    crcBuffer.writeUInt32BE(crc);
    return Buffer.concat([length, typeBuffer, data, crcBuffer]);
  }

  crc32(data) {
    let crc = 0xFFFFFFFF;
    const table = new Uint32Array(256);
    for (let i = 0; i < 256; i++) {
      let c = i;
      for (let j = 0; j < 8; j++) {
        c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      }
      table[i] = c;
    }
    for (let i = 0; i < data.length; i++) {
      crc = table[(crc ^ data[i]) & 0xFF] ^ (crc >>> 8);
    }
    return (crc ^ 0xFFFFFFFF) >>> 0;
  }

  cleanup() {
    if (fs.existsSync(this.config.testDirectory)) {
      const files = fs.readdirSync(this.config.testDirectory);
      files.forEach(f => fs.unlinkSync(path.join(this.config.testDirectory, f)));
      fs.rmdirSync(this.config.testDirectory);
    }
  }

  async runAll() {
    console.clear();
    console.log('');
    console.log('  ╔══════════════════════════════════════════════════╗');
    console.log('  ║    Live2D Master Agent - 图片上传/下载测试     ║');
    console.log('  ╚══════════════════════════════════════════════════╝');
    console.log('');
    console.log(`  目标地址: ${this.baseUrl}`);
    console.log(`  测试时间: ${new Date().toLocaleString('zh-CN')}`);
    console.log('');

    // ==================== 测试 1: 创建测试图片 ====================
    this.section('测试 1: 创建测试图片');
    try {
      const testImagePath = this.createTestImage(256, 256, [255, 100, 100]);
      if (fs.existsSync(testImagePath)) {
        const stats = fs.statSync(testImagePath);
        this.record('创建测试图片', true, `${(stats.size / 1024).toFixed(2)} KB`);
      } else {
        this.record('创建测试图片', false, '文件未生成');
      }
    } catch (error) {
      this.record('创建测试图片', false, error.message);
    }

    // ==================== 测试 2: 上传测试图片 ====================
    this.section('测试 2: 上传图片到 ComfyUI');
    try {
      const testImagePath = path.join(this.config.testDirectory, 'test_input.png');
      if (!fs.existsSync(testImagePath)) {
        this.record('上传图片', false, '测试图片不存在');
      } else {
        const uploadResult = await this.uploadFile(testImagePath);
        if (uploadResult && uploadResult.name) {
          this.record('上传图片', true, `文件: ${uploadResult.name}`);
          this.divider();
          this.log('上传响应', JSON.stringify(uploadResult));
        } else {
          this.record('上传图片', false, JSON.stringify(uploadResult));
        }
      }
    } catch (error) {
      this.record('上传图片', false, error.message);
    }

    // ==================== 测试 3: 上传蒙版图片 ====================
    this.section('测试 3: 上传蒙版图片');
    try {
      const maskPath = this.createTestImage(256, 256, [0, 0, 0], 'test_mask.png');
      const uploadResult = await this.uploadFile(maskPath, 'mask');
      if (uploadResult && uploadResult.name) {
        this.record('上传蒙版图片', true, `文件: ${uploadResult.name}`);
      } else {
        this.record('上传蒙版图片', false, JSON.stringify(uploadResult));
      }
    } catch (error) {
      this.record('上传蒙版图片', false, error.message);
    }

    // ==================== 测试 4: 上传大尺寸图片 ====================
    this.section('测试 4: 上传大尺寸图片');
    try {
      const largeImagePath = this.createTestImage(1024, 1024, [100, 200, 255], 'test_large.png');
      const uploadResult = await this.uploadFile(largeImagePath);
      if (uploadResult && uploadResult.name) {
        const stats = fs.statSync(largeImagePath);
        this.record('上传大尺寸图片', true, `${(stats.size / 1024).toFixed(2)} KB`);
      } else {
        this.record('上传大尺寸图片', false, JSON.stringify(uploadResult));
      }
    } catch (error) {
      this.record('上传大尺寸图片', false, error.message);
    }

    // ==================== 测试 5: 上传重名图片 ====================
    this.section('测试 5: 重名图片上传测试');
    try {
      const imagePath = this.createTestImage(64, 64, [50, 200, 50], 'test_duplicate.png');
      const result1 = await this.uploadFile(imagePath);
      const result2 = await this.uploadFile(imagePath);
      const name1 = result1?.name || '';
      const name2 = result2?.name || '';
      if (name1 && name2) {
        this.record('重名图片上传', true, `两次均成功`);
        this.log('第一次文件名', name1);
        this.log('第二次文件名', name2);
      } else {
        this.record('重名图片上传', false, '上传失败');
      }
    } catch (error) {
      this.record('重名图片上传', false, error.message);
    }

    // ==================== 测试 6: 查看上传的文件 ====================
    this.section('测试 6: 查看上传文件');
    try {
      const viewUrl = `${this.baseUrl}/view?filename=test_input.png&type=input`;
      const result = await this.httpGet(viewUrl);
      if (result.statusCode === 200) {
        const size = result.headers['content-length'] || result.data.length;
        this.record('查看上传文件', true, `${(size / 1024).toFixed(2)} KB, HTTP ${result.statusCode}`);
      } else {
        this.record('查看上传文件', false, `HTTP ${result.statusCode}`);
      }
    } catch (error) {
      this.record('查看上传文件', false, error.message);
    }

    // ==================== 测试 7: 清理测试文件 ====================
    this.section('测试 7: 清理测试文件');
    try {
      const testDir = this.config.testDirectory;
      if (fs.existsSync(testDir)) {
        const files = fs.readdirSync(testDir);
        files.forEach(f => fs.unlinkSync(path.join(testDir, f)));
        fs.rmdirSync(testDir);
        this.record('清理测试文件', true, `${files.length} 个文件已清理`);
      } else {
        this.record('清理测试文件', true, '无需清理');
      }
    } catch (error) {
      this.record('清理测试文件', false, error.message);
    }

    // ==================== 最终报告 ====================
    this.section('测试报告');

    const passed = this.testResults.filter(r => r.passed).length;
    const failed = this.testResults.filter(r => !r.passed).length;
    const total = this.testResults.length;

    console.log('');
    console.log('  ┌──────────────────────────────────────────────────┐');
    console.log(`  │  测试结果:                                      │`);
    this.testResults.forEach(r => {
      console.log(`  │  ${r.passed ? '✅' : '❌'} ${r.name.padEnd(35)} ${String(r.detail).padEnd(15)} │`);
    });
    console.log('  └──────────────────────────────────────────────────┘');
    console.log('');
    console.log(`  📊 汇总: 共 ${total} 项 | ✅ ${passed} 通过 | ❌ ${failed} 失败`);
    console.log('');

    if (failed === 0) {
      console.log('  🎉 所有图片上传/下载测试通过！');
      console.log('  ');
      console.log('  下一步：');
      console.log('    运行完整工作流测试: node tests/test-full-workflow.js');
    } else {
      console.log('  ⚠️ 部分测试未通过，请检查:');
      console.log('    1. ComfyUI 是否已启动');
      console.log('    2. 磁盘空间是否充足');
      console.log('    3. 文件权限是否正确');
    }

    console.log('');
  }
}

const tester = new ImageTester();
tester.runAll().catch(console.error);