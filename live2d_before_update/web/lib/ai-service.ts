export interface AIConfig {
  provider: 'openai' | 'anthropic' | 'custom' | 'none';
  apiKey: string;
  apiUrl: string;
  model: string;
  enabled: boolean;
}

export interface AIMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface AIResponse {
  content?: string;
  error?: string;
}

const DEFAULT_CONFIG: AIConfig = {
  provider: 'none',
  apiKey: '',
  apiUrl: '',
  model: 'gpt-3.5-turbo',
  enabled: false,
};

export function getAIConfig(): AIConfig {
  if (typeof window === 'undefined') return DEFAULT_CONFIG;
  try {
    const stored = localStorage.getItem('live2d_ai_config');
    if (stored) {
      return { ...DEFAULT_CONFIG, ...JSON.parse(stored) };
    }
  } catch {
    // ignore parse error
  }
  return DEFAULT_CONFIG;
}

export function saveAIConfig(config: AIConfig): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('live2d_ai_config', JSON.stringify(config));
}

export function buildSystemPrompt(qaResult?: unknown): string {
  const basePrompt = `你是 Live2D PSD 质量检测专家助手。你的职责是：
1. 分析 PSD 文件的质量检测结果
2. 提供专业的 Live2D 建模建议
3. 解答 PSD 分层、命名规范、结构优化等问题
4. 给出具体的修复步骤和最佳实践

请用中文回答，保持专业但友好的语气。使用 Markdown 格式让回答更易读。`;

  if (!qaResult) return basePrompt;

  return `${basePrompt}\n\n当前检测上下文：\n${JSON.stringify(qaResult, null, 2)}`;
}

export async function callAIAPI(
  messages: AIMessage[],
  config: AIConfig
): Promise<AIResponse> {
  if (!config.enabled || !config.apiKey) {
    return { error: 'AI API 未配置或未启用' };
  }

  try {
    let url = config.apiUrl;
    let body: Record<string, unknown> = {};
    let headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    switch (config.provider) {
      case 'openai':
        url = url || 'https://api.openai.com/v1/chat/completions';
        headers['Authorization'] = `Bearer ${config.apiKey}`;
        body = {
          model: config.model || 'gpt-3.5-turbo',
          messages,
          temperature: 0.7,
          max_tokens: 2000,
        };
        break;

      case 'anthropic':
        url = url || 'https://api.anthropic.com/v1/messages';
        headers['x-api-key'] = config.apiKey;
        headers['anthropic-version'] = '2023-06-01';
        body = {
          model: config.model || 'claude-3-haiku-20240307',
          max_tokens: 2000,
          messages: messages.filter(m => m.role !== 'system').map(m => ({
            role: m.role,
            content: m.content,
          })),
          system: messages.find(m => m.role === 'system')?.content,
        };
        break;

      case 'custom':
        headers['Authorization'] = `Bearer ${config.apiKey}`;
        body = {
          model: config.model,
          messages,
          temperature: 0.7,
          max_tokens: 2000,
        };
        break;

      default:
        return { error: '未知的 AI 提供商' };
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return {
        error: `API 请求失败 (${response.status}): ${errorData.error?.message || response.statusText}`,
      };
    }

    const data = await response.json();

    let content = '';
    if (config.provider === 'anthropic') {
      content = data.content?.[0]?.text || '';
    } else {
      content = data.choices?.[0]?.message?.content || '';
    }

    return { content };
  } catch (err: unknown) {
    if (err instanceof Error) {
      if (err.name === 'AbortError') {
        return { error: '请求超时，请稍后重试' };
      }
      return { error: `请求失败: ${err.message}` };
    }
    return { error: '未知错误' };
  }
}
