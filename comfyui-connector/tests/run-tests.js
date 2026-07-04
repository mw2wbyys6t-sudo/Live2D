#!/usr/bin/env node

/**
 * ComfyUI 连接器测试运行器
 * 
 * 运行所有测试：
 *   node tests/run-tests.js
 * 
 * 运行特定测试：
 *   node tests/run-tests.js --connection
 *   node tests/run-tests.js --upload
 *   node tests/run-tests.js --workflow
 *   node tests/run-tests.js --unit
 *   node tests/run-tests.js --all
 * 
 * 选项：
 *   --host <ip>       ComfyUI 主机地址
 *   --port <port>     ComfyUI 端口
 *   --skip-slow       跳过慢速测试
 *   --no-clear        测试前不清屏
 *   --watch           以监视模式运行
 */

const path = require('path');
const fs = require('fs');
const { execSync, spawn } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const TESTS_DIR = __dirname;

const TEST_SCRIPTS = {
  connection: {
    name: '连接检测',
    file: 'test-connection.js',
    description: '检测 ComfyUI 是否运行'
  },
  upload: {
    name: '图片上传/下载',
    file: 'test-upload-download.js',
    description: '测试图片上传和下载功能'
  },
  workflow: {
    name: '完整工作流',
    file: 'test-full-workflow.js',
    description: '测试完整生成工作流'
  },
  unit: {
    name: '单元测试',
    file: 'connector.test.js',
    description: 'Jest 单元测试'
  }
};

function printBanner() {
  if (!process.argv.includes('--no-clear')) {
    console.clear();
  }
  console.log('');
  console.log('  ╔══════════════════════════════════════════════════╗');
  console.log('  ║       ComfyUI 连接器 - 完整测试套件             ║');
  console.log('  ╚══════════════════════════════════════════════════╝');
  console.log('');
  console.log(`  📁 项目目录: ${ROOT}`);
  console.log(`  🕐 测试时间: ${new Date().toLocaleString('zh-CN')}`);
  console.log('');
}

function printAvailableTests() {
  console.log('  可用测试:');
  console.log('');
  Object.entries(TEST_SCRIPTS).forEach(([key, test]) => {
    console.log(`    --${key.padEnd(12)} ${test.name.padEnd(16)} ${test.description}`);
  });
  console.log('');
  console.log('    --all                  运行所有测试');
  console.log('');
}

function getArgs() {
  const args = process.argv.slice(2);

  const result: any = {
    tests: [],
    host: '127.0.0.1',
    port: 8188,
    skipSlow: false
  };

  if (args.length === 0 || args.includes('--all')) {
    result.tests = Object.keys(TEST_SCRIPTS);
    return result;
  }

  for (const arg of args) {
    if (arg === '--skip-slow') {
      result.skipSlow = true;
    } else if (arg.startsWith('--host=')) {
      result.host = arg.split('=')[1];
    } else if (arg.startsWith('--port=')) {
      result.port = parseInt(arg.split('=')[1]);
    } else if (arg.startsWith('--')) {
      const testName = arg.replace('--', '');
      if (TEST_SCRIPTS[testName]) {
        result.tests.push(testName);
      } else if (testName === 'all') {
        result.tests = Object.keys(TEST_SCRIPTS);
      }
    }
  }

  // Handle --host <value> and --port <value> separately
  const hostIndex = args.indexOf('--host');
  if (hostIndex !== -1 && hostIndex + 1 < args.length) {
    result.host = args[hostIndex + 1];
  }
  const portIndex = args.indexOf('--port');
  if (portIndex !== -1 && portIndex + 1 < args.length) {
    result.port = parseInt(args[portIndex + 1]);
  }

  return result;
}

function runScript(scriptName, extraArgs = []) {
  return new Promise((resolve, reject) => {
    const testInfo = TEST_SCRIPTS[scriptName];
    if (!testInfo) {
      reject(new Error(`Unknown test: ${scriptName}`));
      return;
    }

    const scriptPath = path.join(TESTS_DIR, testInfo.file);

    if (!fs.existsSync(scriptPath)) {
      console.log(`  ⚠️  测试文件不存在: ${scriptPath}`);
      resolve({ passed: false, error: 'File not found' });
      return;
    }

    console.log('\n' + '  ' + '─'.repeat(60));
    console.log(`  🎯 运行测试: ${testInfo.name}`);
    console.log(`  📄 脚本: ${testInfo.file}`);
    console.log('  ' + '─'.repeat(60) + '\n');

    const args: string[] = [];
    if (extraArgs.includes('--skip-slow') || process.argv.includes('--skip-slow')) {
      args.push('--skip-slow-tests');
    }
    args.push(`--host=${extraArgs.find(a => a.startsWith('--host='))?.split('=')[1] || '127.0.0.1'}`);
    args.push(`--port=${extraArgs.find(a => a.startsWith('--port='))?.split('=')[1] || '8188'}`);

    const child = spawn('node', [scriptPath, ...args], {
      cwd: ROOT,
      stdio: 'inherit',
      env: { ...process.env, FORCE_COLOR: '1' }
    });

    child.on('close', (code: number) => {
      resolve({ passed: code === 0, exitCode: code });
    });

    child.on('error', (err: Error) => {
      reject(err);
    });
  });
}

function runJestTests() {
  return new Promise((resolve, reject) => {
    console.log('\n' + '  ' + '─'.repeat(60));
    console.log('  🎯 运行测试: 单元测试 (Jest)');
    console.log('  📄 配置: tests/connector.test.js');
    console.log('  ' + '─'.repeat(60) + '\n');

    const child = spawn('npx', ['jest', '--config', path.join(ROOT, 'jest.config.js'), '--verbose'], {
      cwd: ROOT,
      stdio: 'inherit',
      env: { ...process.env, FORCE_COLOR: '1' }
    });

    child.on('close', (code: number) => {
      resolve({ passed: code === 0, exitCode: code });
    });

    child.on('error', (err: Error) => {
      reject(err);
    });
  });
}

async function main() {
  printBanner();

  const config = getArgs();

  if (config.tests.length === 0) {
    printAvailableTests();
    console.log('  请指定要运行的测试:\n');
    console.log('    node tests/run-tests.js --connection');
    console.log('    node tests/run-tests.js --all');
    console.log('');
    return;
  }

  const extraArgs = [
    `--host=${config.host}`,
    `--port=${config.port}`,
    ...(config.skipSlow ? ['--skip-slow'] : [])
  ];

  console.log(`  📡 ComfyUI 地址: http://${config.host}:${config.port}`);
  console.log(`  🧪 测试数量: ${config.tests.length}`);
  console.log('');

  const results: any[] = [];
  let allPassed = true;

  for (const testName of config.tests) {
    try {
      if (testName === 'unit') {
        const result = await runJestTests();
        results.push({ name: TEST_SCRIPTS[testName].name, ...result });
        allPassed = allPassed && result.passed;
      } else {
        const result = await runScript(testName, extraArgs);
        results.push({ name: TEST_SCRIPTS[testName].name, ...result });
        allPassed = allPassed && result.passed;
      }
    } catch (error: any) {
      results.push({ name: TEST_SCRIPTS[testName]?.name || testName, passed: false, error: error.message });
      allPassed = false;
    }
  }

  // Final summary
  console.log('');
  console.log('  ╔══════════════════════════════════════════════════╗');
  console.log('  ║          测试总结                                ║');
  console.log('  ╚══════════════════════════════════════════════════╝');
  console.log('');

  const passedCount = results.filter(r => r.passed).length;
  const totalCount = results.length;

  results.forEach(r => {
    const icon = r.passed ? '✅' : '❌';
    const exitInfo = r.exitCode !== undefined ? ` (exit: ${r.exitCode})` : '';
    const errorInfo = r.error ? ` - ${r.error}` : '';
    console.log(`  ${icon} ${r.name.padEnd(25)} ${r.passed ? '通过' : '失败'}${exitInfo}${errorInfo}`);
  });

  console.log('');
  console.log(`  📊 汇总: ${passedCount}/${totalCount} 通过`);
  console.log(`  📈 通过率: ${((passedCount / totalCount) * 100).toFixed(1)}%`);
  console.log('');

  if (allPassed) {
    console.log('  🎉 全部测试通过！');
    console.log('  ');
    console.log('  ComfyUI 连接器已完全就绪，可以集成到 Photoshop 插件！');
    console.log('  ');
    console.log('  更多信息:');
    console.log('    README:    https://github.com/your-repo/comfyui-connector');
    console.log('    API 文档:  node tests/test-connection.js --help');
  } else {
    console.log('  ⚠️  部分测试未通过');
    console.log('  ');
    console.log('  建议排查:');
    results.filter(r => !r.passed).forEach(r => {
      console.log(`    ❌ ${r.name}`);
    });
    console.log('');
    console.log('  常见问题:');
    console.log('    1. ComfyUI 未启动');
    console.log('    2. 端口配置错误');
    console.log('    3. 网络不通');
  }

  console.log('');
  process.exit(allPassed ? 0 : 1);
}

main().catch(console.error);