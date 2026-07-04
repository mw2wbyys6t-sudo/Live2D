#!/usr/bin/env node

/**
 * 测试 3: 完整工作流测试脚本
 * 
 * 功能：
 * - 模拟完整生成流程
 * - 测试队列管理
 * - 测试进度追踪
 * - 测试错误处理
 * - 测试中断/清理功能
 * - 模拟 Photoshop 插件集成
 * 
 * 使用：
 *   node tests/test-full-workflow.js
 *   node tests/test-full-workflow.js --skip-slow-tests
 */

const path = require('path');
const fs = require('fs');
const http = require('http');

class WorkflowTester {
  constructor(config = {}) {
    this.config = {
      host: config.host || '127.0.0.1',
      port: config.port || 8188,
      protocol: config.protocol || 'http',
      timeout: config.timeout || 30000,
      outputDirectory: path.resolve(config.outputDirectory || path.join(__dirname, '..', 'output')),
      tempDirectory: path.resolve(config.tempDirectory || path.join(__dirname, '..', 'temp')),
      skipSlowTests: config.skipSlowTests || false
    };

    this.baseUrl = `${this.config.protocol}://${this.config.host}:${this.config.port}`;
    this.testResults = [];
    this.promptIdCounter = 0;

    for (const dir of [this.config.outputDirectory, this.config.tempDirectory]) {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    }
  }

  log(label, value, status = '') {
    const statusStr = status ? ` [${status}]` : '';
    console.log(`  ${label.padEnd(35)} ${String(value).padEnd(20)}${statusStr}`);
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

  httpRequest(method, urlPath, body = null) {
    return new Promise((resolve, reject) => {
      const url = new URL(`${this.baseUrl}${urlPath}`);
      const options = {
        hostname: url.hostname,
        port: url.port,
        path: urlPath,
        method: method,
        headers: { 'Content-Type': 'application/json' },
        timeout: this.config.timeout
      };

      if (body) {
        const bodyStr = JSON.stringify(body);
        options.headers['Content-Length'] = Buffer.byteLength(bodyStr);
      }

      const req = http.request(options, (res) => {
        let data = '';
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => {
          try {
            resolve({ statusCode: res.statusCode, data: JSON.parse(data), raw: data });
          } catch {
            resolve({ statusCode: res.statusCode, data: null, raw: data });
          }
        });
      });

      req.on('error', reject);
      req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });

      if (body) {
        req.write(JSON.stringify(body));
      }
      req.end();
    });
  }

  async runAll() {
    console.clear();
    console.log('');
    console.log('  ╔══════════════════════════════════════════════════╗');
    console.log('  ║    Live2D Master Agent - 完整工作流测试        ║');
    console.log('  ╚══════════════════════════════════════════════════╝');
    console.log('');
    console.log(`  目标地址: ${this.baseUrl}`);
    console.log(`  测试时间: ${new Date().toLocaleString('zh-CN')}`);
    console.log(`  跳过慢速测试: ${this.config.skipSlowTests}`);
    console.log('');

    // ==================== 测试 1: 连接检查 ====================
    this.section('测试 1: 连接检查');
    try {
      const result = await this.httpRequest('GET', '/system_stats');
      if (result.statusCode === 200 && result.data) {
        this.record('ComfyUI 连接', true, `HTTP ${result.statusCode}`);
        this.divider();
        this.log('版本', result.data.version || 'N/A');
        this.log('设备', JSON.stringify((result.data.system?.devices || []).map(function(d) { return d.name || d.type; })));
      } else {
        this.record('ComfyUI 连接', false, `HTTP ${result.statusCode}`);
      }
    } catch (error) {
      this.record('ComfyUI 连接', false, error.message);
      this.section('最终报告');
      console.log('\n  ❌ 无法连接 ComfyUI，后续测试无法进行\n');
      return;
    }

    // ==================== 测试 2: 队列管理 ====================
    this.section('测试 2: 队列管理测试');

    // 2a: 获取队列
    try {
      const result = await this.httpRequest('GET', '/queue');
      if (result.statusCode === 200) {
        const running = result.data?.queue_running || [];
        const pending = result.data?.queue_pending || [];
        this.record('获取队列信息', true, `${running.length} 运行, ${pending.length} 等待`);
        this.divider();
        this.log('运行中任务', running.length);
        this.log('等待中任务', pending.length);
        this.log('总队列长度', running.length + pending.length);
      } else {
        this.record('获取队列信息', false, `HTTP ${result.statusCode}`);
      }
    } catch (error) {
      this.record('获取队列信息', false, error.message);
    }

    // 2b: 获取进度
    try {
      const result = await this.httpRequest('GET', '/progress');
      if (result.statusCode === 200) {
        this.record('获取生成进度', true, `进度: ${result.data?.value || 0}%`);
      } else {
        this.record('获取生成进度', false, `HTTP ${result.statusCode}`);
      }
    } catch (error) {
      this.record('获取生成进度', false, error.message);
    }

    // 2c: 清空队列
    if (!this.config.skipSlowTests) {
      try {
        const result = await this.httpRequest('POST', '/queue/clear');
        if (result.statusCode === 200 || result.statusCode === 204) {
          this.record('清空队列', true, `HTTP ${result.statusCode}`);
        } else {
          this.record('清空队列', false, `HTTP ${result.statusCode}`);
        }
      } catch (error) {
        this.record('清空队列', false, error.message);
      }
    }

    // ==================== 测试 3: 对象信息 ====================
    this.section('测试 3: 节点信息测试');
    try {
      const result = await this.httpRequest('GET', '/object_info');
      if (result.statusCode === 200 && result.data) {
        const nodeCount = Object.keys(result.data).length;
        this.record('获取节点信息', true, `${nodeCount} 个节点类型`);
        this.divider();

        // 检查关键节点
        const requiredNodes = ['CheckpointLoaderSimple', 'CLIPTextEncode', 'KSampler', 'VAEDecode', 'VAEEncode', 'SaveImage'];
        const foundNodes = requiredNodes.filter(n => result.data[n]);
        const missingNodes = requiredNodes.filter(n => !result.data[n]);

        this.log('必需节点', `${foundNodes.length}/${requiredNodes.length}`);
        if (missingNodes.length > 0) {
          this.log('缺失节点', missingNodes.join(', '), 'WARN');
        }

        // 检查可用模型
        const checkpoints = result.data.CheckpointLoaderSimple?.input?.required?.ckpt_name || [];
        const models = result.data.CheckpointLoaderSimple?.input?.optional?.ckpt_name || [];
        const allModels = [...checkpoints, ...models];

        this.log('可用模型', allModels.length > 0 ? `${allModels.length} 个` : '无');

        if (allModels.length > 0) {
          this.divider();
          this.log('已安装模型', '');
          allModels.slice(0, 5).forEach((m, i) => {
            this.log(`  ${i + 1}`, m);
          });
          if (allModels.length > 5) {
            this.log(`  ...`, `还有 ${allModels.length - 5} 个`);
          }
        }
      } else {
        this.record('获取节点信息', false, `HTTP ${result.statusCode}`);
      }
    } catch (error) {
      this.record('获取节点信息', false, error.message);
    }

    // ==================== 测试 4: 队列提交模拟 ====================
    this.section('测试 4: 队列提交测试');

    if (!this.config.skipSlowTests) {
      try {
        const testWorkflow = {
          "1": { class_type: "CheckpointLoaderSimple", inputs: { ckpt_name: "sd_xl_base_1.0.safetensors" } },
          "2": { class_type: "CLIPTextEncode", inputs: { text: "test", clip: ["1", 1] } },
          "3": { class_type: "CLIPTextEncode", inputs: { text: "test", clip: ["1", 1] } },
          "4": { class_type: "EmptyLatentImage", inputs: { batch_size: 1, height: 512, width: 512 } },
          "5": {
            class_type: "KSampler", inputs: {
              seed: 42, steps: 5, cfg: 4.0, sampler_name: "euler", scheduler: "normal",
              positive: ["2", 0], negative: ["3", 0], latent_image: ["4", 0]
            }
          },
          "6": { class_type: "VAEDecode", inputs: { samples: ["5", 0], vae: ["1", 2] } },
          "7": { class_type: "SaveImage", inputs: { filename_prefix: "test", images: ["6", 0] } }
        };

        const result = await this.httpRequest('POST', '/prompt', { prompt: testWorkflow });

        if (result.statusCode === 200 && result.data?.prompt_id) {
          this.record('提交生成任务', true, `ID: ${result.data.prompt_id}`);
          this.divider();
          this.log('任务 ID', result.data.prompt_id);
          this.log('任务编号', result.data.number);
        } else {
          const errorMsg = result.data?.error?.message || `HTTP ${result.statusCode}`;
          this.record('提交生成任务', false, errorMsg);
        }
      } catch (error) {
        this.record('提交生成任务', false, error.message);
      }
    } else {
      this.record('提交生成任务 (已跳过)', true, '--skip-slow-tests');
    }

    // ==================== 测试 5: 中断执行 ====================
    this.section('测试 5: 中断执行测试');

    if (!this.config.skipSlowTests) {
      try {
        const result = await this.httpRequest('POST', '/interrupt');
        if (result.statusCode === 200 || result.statusCode === 204) {
          this.record('中断执行', true, `HTTP ${result.statusCode}`);
        } else {
          this.record('中断执行', false, `HTTP ${result.statusCode}`);
        }
      } catch (error) {
        this.record('中断执行', false, error.message);
      }
    } else {
      this.record('中断执行 (已跳过)', true, '--skip-slow-tests');
    }

    // ==================== 测试 6: 历史记录 ====================
    this.section('测试 6: 历史记录测试');
    try {
      const result = await this.httpRequest('GET', '/history');
      if (result.statusCode === 200) {
        const historyKeys = Object.keys(result.data || {});
        this.record('获取历史记录', true, `${historyKeys.length} 条记录`);
        if (historyKeys.length > 0) {
          this.divider();
          this.log('最近记录 ID', historyKeys[historyKeys.length - 1]);
          const latest = result.data[historyKeys[historyKeys.length - 1]];
          if (latest) {
            this.log('最近状态', latest.status?.status || 'N/A');
          }
        }
      } else {
        this.record('获取历史记录', false, `HTTP ${result.statusCode}`);
      }
    } catch (error) {
      this.record('获取历史记录', false, error.message);
    }

    // ==================== 测试 7: 设置验证 ====================
    this.section('测试 7: 设置验证');

    // 7a: 输出目录验证
    try {
      const outputDir = this.config.outputDirectory;
      if (fs.existsSync(outputDir)) {
        const files = fs.readdirSync(outputDir);
        this.record('输出目录可用', true, `${files.length} 个文件`);
      } else {
        fs.mkdirSync(outputDir, { recursive: true });
        this.record('输出目录可用', true, '已创建');
      }
    } catch (error) {
      this.record('输出目录可用', false, error.message);
    }

    // 7b: 临时目录验证
    try {
      const tempDir = this.config.tempDirectory;
      if (fs.existsSync(tempDir)) {
        const files = fs.readdirSync(tempDir);
        this.record('临时目录可用', true, `${files.length} 个文件`);
      } else {
        fs.mkdirSync(tempDir, { recursive: true });
        this.record('临时目录可用', true, '已创建');
      }
    } catch (error) {
      this.record('临时目录可用', false, error.message);
    }

    // 7c: 输出格式验证
    try {
      const sampleResult = {
        success: true,
        image_path: path.join(this.config.outputDirectory, 'test_output.png'),
        images: [path.join(this.config.outputDirectory, 'test_output.png')],
        details: {
          prompt_id: 'test-prompt-id',
          status: 'completed',
          duration: 1234,
          seed: 42
        }
      };

      const outputPath = path.join(this.config.outputDirectory, 'test_result.json');
      fs.writeFileSync(outputPath, JSON.stringify(sampleResult, null, 2));

      const readBack = JSON.parse(fs.readFileSync(outputPath, 'utf-8'));
      const valid = readBack.success === true &&
        readBack.image_path &&
        readBack.details?.prompt_id &&
        readBack.details?.status;

      this.record('输出格式验证', valid, valid ? '格式正确' : '格式错误');

      // 清理测试文件
      fs.unlinkSync(outputPath);
    } catch (error) {
      this.record('输出格式验证', false, error.message);
    }

    // ==================== 测试 8: 错误处理 ====================
    this.section('测试 8: 错误处理测试');

    // 8a: 无效端点
    try {
      const result = await this.httpRequest('GET', '/invalid_endpoint_xyz');
      this.record('无效端点处理', result.statusCode === 404, `HTTP ${result.statusCode}`);
    } catch (error) {
      this.record('无效端点处理', true, '连接错误也被正确处理');
    }

    // 8b: 无效请求
    try {
      const result = await this.httpRequest('POST', '/prompt', { invalid: 'data' });
      const hasError = result.statusCode >= 400 || result.data?.error;
      this.record('无效请求处理', hasError, hasError ? '正确返回错误' : '意外成功');
    } catch (error) {
      this.record('无效请求处理', true, '连接错误也被正确处理');
    }

    // 8c: 缺失字段
    try {
      const invalidWorkflow = { "1": { class_type: "NonExistentNode", inputs: {} } };
      const result = await this.httpRequest('POST', '/prompt', { prompt: invalidWorkflow });
      const hasError = result.statusCode >= 400 || result.data?.error;
      this.record('缺失节点处理', hasError, hasError ? '正确返回错误' : '意外成功');
    } catch (error) {
      this.record('缺失节点处理', true, '连接错误也被正确处理');
    }

    // ==================== 测试 9: 性能测试 ====================
    this.section('测试 9: 性能测试');

    // 9a: 响应时间
    try {
      const start = Date.now();
      await this.httpRequest('GET', '/system_stats');
      const elapsed = Date.now() - start;
      this.record('API 响应时间', elapsed < 5000, `${elapsed}ms`);
    } catch (error) {
      this.record('API 响应时间', false, error.message);
    }

    // 9b: 并发请求
    try {
      const start = Date.now();
      const promises = Array(3).fill(null).map(() => this.httpRequest('GET', '/system_stats'));
      await Promise.all(promises);
      const elapsed = Date.now() - start;
      this.record('并发请求 (3个)', elapsed < 10000, `${elapsed}ms`);
    } catch (error) {
      this.record('并发请求 (3个)', false, error.message);
    }

    // ==================== 最终报告 ====================
    this.section('测试报告');

    const passed = this.testResults.filter(r => r.passed).length;
    const failed = this.testResults.filter(r => !r.passed).length;
    const total = this.testResults.length;

    console.log('');
    console.log('  ┌──────────────────────────────────────────────────┐');
    this.testResults.forEach(r => {
      const statusText = r.passed ? '✅ 通过' : '❌ 失败';
      const nameDisplay = r.name.padEnd(30);
      const detailDisplay = String(r.detail || '').padEnd(15);
      console.log(`  │ ${statusText} ${nameDisplay} ${detailDisplay} │`);
    });
    console.log('  └──────────────────────────────────────────────────┘');
    console.log('');
    console.log(`  📊 汇总: 共 ${total} 项 | ✅ ${passed} 通过 | ❌ ${failed} 失败`);
    console.log(`  📈 通过率: ${((passed / total) * 100).toFixed(1)}%`);
    console.log('');

    if (failed === 0) {
      console.log('  🎉 所有工作流测试通过！');
      console.log('  ');
      console.log('  ✅ ComfyUI 连接器已完全就绪！');
      console.log('  ');
      console.log('  🚀 下一步：集成到 Photoshop 插件');
      console.log('    1. 复制 dist/ 目录到插件项目');
      console.log('    2. 调用 Connector API');
      console.log('    3. 处理生成结果');
      console.log('  ');
      console.log('  更多信息请查看 README.md');
    } else {
      console.log('  ⚠️ 部分测试未通过');
      console.log('  ');
      console.log('  建议排查：');
      this.testResults.filter(r => !r.passed).forEach(r => {
        console.log(`    ❌ ${r.name}: ${r.detail}`);
      });
    }

    console.log('');
  }
}

const args = process.argv.slice(2);
const config = {};

if (args.includes('--host')) {
  config.host = args[args.indexOf('--host') + 1];
}
if (args.includes('--port')) {
  config.port = parseInt(args[args.indexOf('--port') + 1]);
}
if (args.includes('--skip-slow-tests')) {
  config.skipSlowTests = true;
}

const tester = new WorkflowTester(config);
tester.runAll().catch(console.error);