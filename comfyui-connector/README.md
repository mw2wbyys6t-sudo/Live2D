# ComfyUI Connector - 本地 AI 绘图连接器

🎨 **Photoshop 插件专用本地 ComfyUI AI 绘图连接器**

---

## 📋 功能特性

- ✅ **本地运行** - 无需云端 API，使用本地 ComfyUI
- ✅ **无需 API Key** - 完全免费，无第三方费用
- ✅ **实时检测** - 自动检测 ComfyUI 是否运行
- ✅ **自动保存** - 生成结果自动保存到本地
- ✅ **批量生成** - 支持批量图片生成
- ✅ **进度追踪** - 实时显示生成进度
- ✅ **TypeScript** - 完整的类型支持
- ✅ **模块化设计** - 易于集成和扩展

---

## 🚀 快速开始

### 安装

```bash
npm install
```

### 构建

```bash
npm run build
```

### 使用示例

```typescript
import { ComfyUIConnector, ImageGenerationService } from 'comfyui-connector';

async function main() {
  const connector = new ComfyUIConnector({
    host: '127.0.0.1',
    port: 8188
  });

  const service = new ImageGenerationService(connector);

  const result = await service.generate({
    prompt: {
      positive: 'beautiful landscape, mountains, sunset',
      negative: 'low quality, blurry'
    },
    width: 1024,
    height: 1024,
    steps: 20
  });

  if (result.success) {
    console.log('Image generated:', result.image_path);
  } else {
    console.error('Generation failed:', result.error);
  }
}

main();
```

---

## 📖 API 文档

### ComfyUIConnector

基础连接器类，用于与 ComfyUI API 通信。

#### 构造函数

```typescript
new ComfyUIConnector(config?: ComfyUIConfig)
```

**配置选项：**

- `host` - ComfyUI 主机地址（默认：127.0.0.1）
- `port` - ComfyUI 端口（默认：8188）
- `protocol` - 协议类型（默认：http）
- `timeout` - 请求超时时间（默认：60000ms）
- `outputDirectory` - 输出目录（默认：./output）
- `tempDirectory` - 临时文件目录（默认：./temp）

#### 方法

**checkHealth()** - 检测 ComfyUI 连接状态

```typescript
const health = await connector.checkHealth();
console.log(health.connected); // true/false
```

**uploadImage(imagePath)** - 上传图片到 ComfyUI

```typescript
const uploadResult = await connector.uploadImage('/path/to/image.png');
console.log(uploadResult.name); // uploaded filename
```

**queuePrompt(workflow)** - 添加生成任务到队列

```typescript
const { prompt_id } = await connector.queuePrompt(workflow);
```

**getHistory(promptId)** - 获取生成历史

```typescript
const history = await connector.getHistory(prompt_id);
```

**getQueueInfo()** - 获取队列信息

```typescript
const queue = await connector.getQueueInfo();
```

**interruptExecution()** - 中断当前执行

```typescript
await connector.interruptExecution();
```

**clearQueue()** - 清空队列

```typescript
await connector.clearQueue();
```

---

### ImageGenerationService

图片生成服务，提供高级的图片生成功能。

#### 构造函数

```typescript
new ImageGenerationService(connector, options?)
```

**选项：**

- `autoSave` - 自动保存（默认：true）
- `autoCleanup` - 自动清理临时文件（默认：true）
- `maxRetries` - 最大重试次数（默认：3）
- `retryDelay` - 重试延迟（默认：5000ms）

#### 方法

**generate(input)** - 生成图片

```typescript
const result = await service.generate({
  image?: '/path/to/input.png',      // 输入图片（可选）
  mask?: '/path/to/mask.png',       // 蒙版图片（可选）
  prompt: {
    positive: 'positive prompt',     // 正面提示词
    negative: 'negative prompt'      // 负面提示词
  },
  width?: 1024,                      // 宽度（可选）
  height?: 1024,                      // 高度（可选）
  steps?: 20,                        // 采样步数（可选）
  cfg?: 7.0,                         // CFG 值（可选）
  seed?: 12345                       // 随机种子（可选）
});
```

**返回值：**

```typescript
{
  success: true,
  image_path: '/path/to/output.png',
  images?: ['/path/to/output.png'],
  error?: 'error message',
  details?: {
    prompt_id: 'prompt_id',
    status: 'completed' | 'failed',
    duration: 12345,
    seed: 12345
  }
}
```

**getGenerationStatus(promptId)** - 获取生成状态

```typescript
const status = await service.getGenerationStatus(promptId);
console.log(status.progress); // 0-100
console.log(status.status); // 'queued' | 'running' | 'completed' | 'failed'
```

---

### FileManager

文件管理工具，用于处理本地文件操作。

#### 构造函数

```typescript
new FileManager(
  outputDirectory?: string,
  tempDirectory?: string,
  maxCacheAge?: number
)
```

#### 方法

**saveImage(buffer, filename)** - 保存图片

```typescript
const path = await fileManager.saveImage(buffer, 'output.png');
```

**loadImage(filePath)** - 加载图片

```typescript
const buffer = await fileManager.loadImage('/path/to/image.png');
```

**listFiles(directory, extension?)** - 列出文件

```typescript
const files = await fileManager.listFiles('./output', '.png');
```

**cleanupOldFiles(directory, maxAge?)** - 清理旧文件

```typescript
const deletedCount = await fileManager.cleanupOldFiles('./temp', 86400000);
```

---

## 🔧 配置示例

### 基础配置

```typescript
const connector = new ComfyUIConnector({
  host: '127.0.0.1',
  port: 8188,
  timeout: 120000
});
```

### 自定义目录

```typescript
const connector = new ComfyUIConnector({
  outputDirectory: '/my/projects/output',
  tempDirectory: '/my/projects/temp'
});
```

### 带选项的服务

```typescript
const service = new ImageGenerationService(connector, {
  autoSave: true,
  autoCleanup: false,
  maxRetries: 5,
  retryDelay: 3000
});
```

---

## 📁 项目结构

```
comfyui-connector/
├── src/
│   ├── connectors/
│   │   └── comfyui.connector.ts    # ComfyUI 连接器
│   ├── services/
│   │   └── image-generation.service.ts  # 图片生成服务
│   ├── utils/
│   │   └── file-manager.ts         # 文件管理工具
│   ├── types/
│   │   └── index.ts               # TypeScript 类型定义
│   └── index.ts                    # 主入口文件
├── config/                         # 配置文件
├── examples/                       # 使用示例
├── tests/                          # 测试文件
├── dist/                          # 编译输出
├── package.json
├── tsconfig.json
└── README.md
```

---

## 🧪 测试

```bash
npm test
```

---

## ⚙️ ComfyUI 要求

1. **安装 ComfyUI**
   - 下载并安装 ComfyUI
   - 启动 ComfyUI 服务

2. **确保服务运行**
   - 默认地址：`http://127.0.0.1:8188`
   - 确保端口未被占用

3. **安装模型**（可选）
   - 下载所需的 Stable Diffusion 模型
   - 放置到 ComfyUI 的 `models/checkpoints` 目录

---

## 🎯 常见用例

### 1. 文本生成图片

```typescript
const result = await service.generate({
  prompt: {
    positive: 'a beautiful sunset over mountains',
    negative: 'low quality, blurry, deformed'
  },
  width: 1024,
  height: 1024,
  steps: 30
});
```

### 2. 图片到图片转换

```typescript
const result = await service.generate({
  image: '/path/to/input.png',
  prompt: {
    positive: 'stylized version of this image',
    negative: 'low quality'
  },
  strength: 0.7
});
```

### 3. 局部重绘（Inpainting）

```typescript
const result = await service.generate({
  image: '/path/to/base.png',
  mask: '/path/to/mask.png',
  prompt: {
    positive: 'new content for masked area',
    negative: 'artifacts'
  }
});
```

### 4. 检查连接状态

```typescript
const health = await connector.checkHealth();
if (health.connected) {
  console.log('ComfyUI is running!');
  console.log('Version:', health.version);
} else {
  console.error('Cannot connect to ComfyUI');
}
```

---

## 🐛 故障排除

### 连接失败

1. 确保 ComfyUI 已启动
2. 检查防火墙设置
3. 验证端口 8188 是否可用

### 生成超时

1. 增加超时时间：`timeout: 300000`
2. 减少采样步数：`steps: 15`
3. 使用更简单的提示词

### 内存不足

1. 减小图片尺寸：`width: 512, height: 512`
2. 使用更小的模型
3. 清理临时文件：`connector.cleanupTempFiles()`

---

## 📄 License

MIT License - 详见 LICENSE 文件

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📚 相关资源

- [ComfyUI 官方文档](https://github.com/comfyanonymous/ComfyUI)
- [Stable Diffusion](https://github.com/CompVis/stable-diffusion)
- [TypeScript](https://www.typescriptlang.org/)
