#!/usr/bin/env node

/**
 * 测试 1: ComfyUI 连接检测脚本
 * 
 * 功能：
 * - 检测本地 ComfyUI 是否运行
 * - 获取系统信息和版本
 * - 检查队列状态
 * - 生成详细报告
 * 
 * 使用：
 *   node tests/test-connection.js
 *   node tests/test-connection.js --host 192.168.1.100 --port 8188
 */

const path = require('path');
const fs = require('fs');

// 模拟 ComfyUIConnector 进行测试（不依赖 TypeScript 编译）
class ComfyUIConnector {
  constructor(config = {}) {
    this.config = {
      host: config.host || '127.0.0.1',
      port: config.port || 8188,
      protocol: config.protocol || 'http',
      timeout: config.timeout || 60000,
      outputDirectory: config.outputDirectory || path.join(__dirname, '..', 'output'),
      tempDirectory: config.tempDirectory || path.join(__dirname, '..', 'temp')
    };

    this.baseUrl = `${this.config.protocol}://${this.config.host}:${this.config.port}`;

    if (!fs.existsSync(this.config.outputDirectory)) {
      fs.mkdirSync(this.config.outputDirectory, { recursive: true });
    }
    if (!fs.existsSync(this.config.tempDirectory)) {
      fs.mkdirSync(this.config.tempDirectory, { recursive: true });
    }
  }

  async checkHealth() {
    try {
      const http = require('http');
      return new Promise((resolve) => {
        const req = http.get(`${this.baseUrl}/system_stats`, { timeout: 5000 }, (res) => {
          let data = '';
          res.on('data', (chunk) => data += chunk);
          res.on('end', () => {
            try {
              const json = JSON.parse(data);
              resolve({
                success: true,
                connected: true,
                version: json.version || 'unknown',
                queue_size: json.system?.queue_size || 0,
                devices: json.system?.devices || [],
                os: json.system?.os || 'unknown',
                ram: json.system?.memory || {},
                detail: json
              });
            } catch (e) {
              resolve({
                success: false,
                connected: false,
                error: 'Invalid response format'
              });
            }
          });
        });
        req.on('error', (err) => {
          resolve({
            success: false,
            connected: false,
            error: err.message
          });
        });
        req.on('timeout', () => {
          req.destroy();
          resolve({
            success: false,
            connected: false,
            error: 'Connection timeout'
          });
        });
      });
    } catch (error) {
      return {
        success: false,
        connected: false,
        error: error.message
      };
    }
  }

  async getQueueInfo() {
    try {
      const http = require('http');
      return new Promise((resolve) => {
        http.get(`${this.baseUrl}/queue`, { timeout: 5000 }, (res) => {
          let data = '';
          res.on('data', (chunk) => data += chunk);
          res.on('end', () => {
            try {
              const json = JSON.parse(data);
              resolve({
                success: true,
                running: json.queue_running || [],
                pending: json.queue_pending || [],
                queue_size: (json.queue_running || []).length + (json.queue_pending || []).length
              });
            } catch (e) {
              resolve({ success: false, error: 'Invalid response' });
            }
          });
        }).on('error', (err) => {
          resolve({ success: false, error: err.message });
        });
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  async getObjectInfo() {
    try {
      const http = require('http');
      return new Promise((resolve) => {
        http.get(`${this.baseUrl}/object_info`, { timeout: 10000 }, (res) => {
          let data = '';
          res.on('data', (chunk) => data += chunk);
          res.on('end', () => {
            try {
              const json = JSON.parse(data);
              const nodeTypes = Object.keys(json);
              resolve({
                success: true,
                node_count: nodeTypes.length,
                node_types: nodeTypes.slice(0, 20),
                checkpoints: json.CheckpointLoaderSimple?.input?.required?.ckpt_name || []
              });
            } catch (e) {
              resolve({ success: false, error: 'Invalid response' });
            }
          });
        }).on('error', (err) => {
          resolve({ success: false, error: err.message });
        });
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
}

function printSection(title) {
  console.log('\n' + '='.repeat(70));
  console.log(`  ${title}`);
  console.log('='.repeat(70));
}

function printField(label, value, status = '') {
  const statusStr = status ? ` [${status}]` : '';
  console.log(`  ${label.padEnd(25)} ${String(value).padEnd(20)}${statusStr}`);
}

function printDivider() {
  console.log('  ' + '-'.repeat(60));
}

async function main() {
  const args = process.argv.slice(2);
  const hostIndex = args.indexOf('--host');
  const portIndex = args.indexOf('--port');

  const config = {
    host: hostIndex !== -1 ? args[hostIndex + 1] : '127.0.0.1',
    port: portIndex !== -1 ? parseInt(args[portIndex + 1]) : 8188
  };

  console.clear();
  console.log('');
  console.log('  ╔══════════════════════════════════════════════════╗');
  console.log('  ║      Live2D Master Agent - ComfyUI 连接检测     ║');
  console.log('  ╚══════════════════════════════════════════════════╝');
  console.log('');
  console.log(`  目标地址: http://${config.host}:${config.port}`);
  console.log(`  测试时间: ${new Date().toLocaleString('zh-CN')}`);
  console.log('');

  const connector = new ComfyUIConnector(config);

  // ==================== 测试 1: 连接检测 ====================
  printSection('测试 1: 连接检测');

  console.log('  正在连接 ComfyUI...');
  const health = await connector.checkHealth();

  if (health.connected) {
    printField('连接状态', '✅ 已连接', 'SUCCESS');
    printDivider();
    printField('版本号', health.version);
    printField('队列长度', health.queue_size);
    printField('操作系统', health.os);

    if (health.devices && health.devices.length > 0) {
      health.devices.forEach((device, i) => {
        const name = device.name || device.type || `Device ${i}`;
        printField(`设备 ${i + 1}`, name);
      });
    }

    if (health.ram) {
      const totalRam = health.ram.total ? `${(health.ram.total / 1024 / 1024 / 1024).toFixed(1)} GB` : 'N/A';
      const freeRam = health.ram.free ? `${(health.ram.free / 1024 / 1024 / 1024).toFixed(1)} GB` : 'N/A';
      printField('总内存', totalRam);
      printField('可用内存', freeRam);
    }
  } else {
    printField('连接状态', '❌ 连接失败', 'ERROR');
    printDivider();
    printField('错误信息', health.error);
    console.log('');
    console.log('  ⚠️ 请确保 ComfyUI 已启动:');
    console.log('    python main.py');
    console.log('');
    process.exit(1);
  }

  // ==================== 测试 2: 队列检测 ====================
  printSection('测试 2: 队列状态检测');

  const queueInfo = await connector.getQueueInfo();

  if (queueInfo.success) {
    printField('队列状态', '✅ 已获取', 'SUCCESS');
    printDivider();
    printField('正在运行任务', queueInfo.running.length);
    printField('等待中任务', queueInfo.pending.length);
    printField('总队列长度', queueInfo.queue_size);

    if (queueInfo.running.length > 0) {
      queueInfo.running.forEach((item, i) => {
        printField(`  运行中 ${i + 1}`, item.prompt_id || 'N/A');
      });
    }

    if (queueInfo.pending.length > 0) {
      queueInfo.pending.forEach((item, i) => {
        printField(`  等待中 ${i + 1}`, item.prompt_id || 'N/A');
      });
    }
  } else {
    printField('队列状态', '❌ 获取失败', 'ERROR');
    printField('错误', queueInfo.error);
  }

  // ==================== 测试 3: 节点信息检测 ====================
  printSection('测试 3: 节点信息检测');

  const objectInfo = await connector.getObjectInfo();

  if (objectInfo.success) {
    printField('节点信息', '✅ 已获取', 'SUCCESS');
    printDivider();
    printField('可用节点数量', objectInfo.node_count);

    console.log('  \n  可用节点类型（前 20 个）:');
    if (objectInfo.node_types && objectInfo.node_types.length > 0) {
      objectInfo.node_types.forEach((type, i) => {
        console.log(`    ${String(i + 1).padStart(2)}. ${type}`);
      });
    } else {
      console.log('    (无数据)');
    }

    if (objectInfo.checkpoints && objectInfo.checkpoints.length > 0) {
      printDivider();
      printField('可用模型', objectInfo.checkpoints.length);
      console.log('  \n  已安装的 Checkpoint 模型:');
      objectInfo.checkpoints.slice(0, 10).forEach((model, i) => {
        console.log(`    ${String(i + 1).padStart(2)}. ${model}`);
      });
      if (objectInfo.checkpoints.length > 10) {
        console.log(`    ... 还有 ${objectInfo.checkpoints.length - 10} 个`);
      }
    }
  } else {
    printField('节点信息', '❌ 获取失败', 'ERROR');
    printField('错误', objectInfo.error);
  }

  // ==================== 最终报告 ====================
  printSection('测试报告');

  const allPassed = health.connected && queueInfo.success && objectInfo.success;

  console.log('');
  console.log(`  测试结果:`);
  console.log(`  ┌──────────────────────────────────────────────────┐`);
  console.log(`  │  1. 连接检测         ${health.connected ? '✅ 通过' : '❌ 失败'}                              │`);
  console.log(`  │  2. 队列状态检测     ${queueInfo.success ? '✅ 通过' : '❌ 失败'}                              │`);
  console.log(`  │  3. 节点信息检测     ${objectInfo.success ? '✅ 通过' : '❌ 失败'}                              │`);
  console.log(`  └──────────────────────────────────────────────────┘`);
  console.log(`  `);
  console.log(`  总体状态: ${allPassed ? '✅ 全部通过' : '❌ 部分失败'}`);
  console.log(`  `);

  if (allPassed) {
    console.log(`  🎉 ComfyUI 连接器测试通过！可以正常使用！`);
    console.log(`  `);
    console.log(`  下一步：`);
    console.log(`    运行完整测试: node tests/test-full-workflow.js`);
  } else {
    console.log(`  ⚠️ 部分测试未通过，请检查 ComfyUI 状态`);
    console.log(`  `);
    console.log(`  常见问题：`);
    console.log(`    1. ComfyUI 未启动 -> 运行 python main.py`);
    console.log(`    2. 端口配置错误 -> 检查 --port 参数`);
    console.log(`    3. 网络不通 -> 检查 --host 参数`);
  }

  console.log('');
}

main().catch(console.error);