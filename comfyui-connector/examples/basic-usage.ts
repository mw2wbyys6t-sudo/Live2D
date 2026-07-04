import { ComfyUIConnector, ImageGenerationService } from '../src';

async function exampleBasicGeneration() {
  console.log('=== 示例 1: 基础文本生成图片 ===\n');

  const connector = new ComfyUIConnector({
    host: '127.0.0.1',
    port: 8188,
    outputDirectory: './output',
    tempDirectory: './temp'
  });

  const service = new ImageGenerationService(connector);

  console.log('检测 ComfyUI 连接...');
  const health = await connector.checkHealth();

  if (!health.connected) {
    console.error('❌ 无法连接到 ComfyUI，请确保服务已启动');
    console.log('提示：运行 ComfyUI 后重试');
    return;
  }

  console.log('✅ ComfyUI 已连接');
  console.log(`版本: ${health.version}`);
  console.log(`队列长度: ${health.queue_size}\n`);

  console.log('开始生成图片...');
  console.log('提示词: 一个美丽的日落，山脉和湖泊\n');

  const result = await service.generate({
    prompt: {
      positive: 'a beautiful sunset over mountains and lake, golden hour lighting, highly detailed, 8k',
      negative: 'low quality, blurry, deformed, ugly, bad anatomy'
    },
    width: 1024,
    height: 1024,
    steps: 30,
    cfg: 7.0
  });

  if (result.success) {
    console.log('✅ 图片生成成功！');
    console.log(`输出路径: ${result.image_path}`);
    console.log(`生成耗时: ${result.details?.duration}ms`);
    console.log(`随机种子: ${result.details?.seed}`);
  } else {
    console.error('❌ 图片生成失败');
    console.error(`错误: ${result.error}`);
  }
}

async function exampleImageToImage() {
  console.log('\n=== 示例 2: 图片到图片转换 ===\n');

  const connector = new ComfyUIConnector();
  const service = new ImageGenerationService(connector);

  const inputImage = './input.png';

  console.log('开始图片转换...');
  console.log(`输入图片: ${inputImage}\n`);

  const result = await service.generate({
    image: inputImage,
    prompt: {
      positive: 'stylized anime version of this image, vibrant colors',
      negative: 'low quality, blurry, deformed'
    },
    steps: 25
  });

  if (result.success) {
    console.log('✅ 转换成功！');
    console.log(`输出路径: ${result.image_path}`);
  } else {
    console.error('❌ 转换失败');
    console.error(`错误: ${result.error}`);
  }
}

async function exampleInpainting() {
  console.log('\n=== 示例 3: 局部重绘 (Inpainting) ===\n');

  const connector = new ComfyUIConnector();
  const service = new ImageGenerationService(connector);

  console.log('开始局部重绘...');
  console.log('输入图片: ./base.png');
  console.log('蒙版图片: ./mask.png\n');

  const result = await service.generate({
    image: './base.png',
    mask: './mask.png',
    prompt: {
      positive: 'add flowers and butterflies in the masked area',
      negative: 'artifacts, low quality'
    },
    steps: 20
  });

  if (result.success) {
    console.log('✅ 局部重绘成功！');
    console.log(`输出路径: ${result.image_path}`);
  } else {
    console.error('❌ 局部重绘失败');
    console.error(`错误: ${result.error}`);
  }
}

async function exampleBatchGeneration() {
  console.log('\n=== 示例 4: 批量生成 ===\n');

  const connector = new ComfyUIConnector();
  const service = new ImageGenerationService(connector, {
    autoCleanup: false
  });

  const prompts = [
    'a cute cat, fluffy',
    'a happy dog, running',
    'a majestic lion, portrait'
  ];

  console.log(`开始批量生成 ${prompts.length} 张图片...\n`);

  const results = [];
  for (let i = 0; i < prompts.length; i++) {
    console.log(`生成第 ${i + 1}/${prompts.length} 张...`);

    const result = await service.generate({
      prompt: {
        positive: prompts[i],
        negative: 'low quality, blurry'
      },
      width: 512,
      height: 512,
      steps: 20
    });

    results.push(result);

    if (result.success) {
      console.log(`✅ 第 ${i + 1} 张完成: ${result.image_path}`);
    } else {
      console.error(`❌ 第 ${i + 1} 张失败: ${result.error}`);
    }
  }

  console.log('\n批量生成完成！');
  const successCount = results.filter(r => r.success).length;
  console.log(`成功: ${successCount}/${prompts.length}`);
}

async function main() {
  try {
    await exampleBasicGeneration();
  } catch (error) {
    console.error('示例执行失败:', error);
  }
}

if (require.main === module) {
  main();
}
