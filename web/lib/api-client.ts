import type {
  Character,
  CharacterCreate,
  ChatMessage,
  ExportFormat,
  Expression,
  GenerationRequest,
  GenerationResult,
  GenerationStep,
  SystemStatus,
} from '../types';

const DEFAULT_BASE_URL =
  typeof window !== 'undefined'
    ? (window as unknown as { __LIVE2D_API_URL__?: string }).__LIVE2D_API_URL__ ||
      'http://localhost:8080'
    : 'http://localhost:8080';

export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: unknown,
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export interface APIClientOptions {
  baseURL?: string;
  timeoutMs?: number;
  onUnauthorized?: () => void;
}

export class APIClient {
  readonly baseURL: string;
  private readonly timeoutMs: number;
  private readonly onUnauthorized?: () => void;

  constructor(options: APIClientOptions = {}) {
    this.baseURL = options.baseURL || DEFAULT_BASE_URL;
    this.timeoutMs = options.timeoutMs ?? 60_000;
    this.onUnauthorized = options.onUnauthorized;
  }

  // ---------- internal ----------

  private async request<T>(
    path: string,
    init: RequestInit = {},
    timeoutMs?: number,
  ): Promise<T> {
    const controller = new AbortController();
    const timeout = setTimeout(
      () => controller.abort(),
      timeoutMs ?? this.timeoutMs,
    );
    try {
      const res = await fetch(`${this.baseURL}${path}`, {
        ...init,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          ...(init.headers || {}),
        },
      });
      if (res.status === 401) {
        this.onUnauthorized?.();
      }
      if (!res.ok) {
        let data: unknown = undefined;
        try {
          data = await res.json();
        } catch {
          // ignore
        }
        throw new APIError(
          `Request failed: ${res.status} ${res.statusText}`,
          res.status,
          data,
        );
      }
      if (res.status === 204) {
        return undefined as T;
      }
      const ct = res.headers.get('content-type') || '';
      if (ct.includes('application/json')) {
        return (await res.json()) as T;
      }
      return (await res.text()) as unknown as T;
    } catch (err) {
      if (err instanceof APIError) throw err;
      if (err instanceof DOMException && err.name === 'AbortError') {
        throw new APIError('Request timed out', 408);
      }
      throw new APIError(
        err instanceof Error ? err.message : 'Network error',
        0,
      );
    } finally {
      clearTimeout(timeout);
    }
  }

  private async requestBlob(path: string, init: RequestInit = {}): Promise<Blob> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.timeoutMs);
    try {
      const res = await fetch(`${this.baseURL}${path}`, {
        ...init,
        signal: controller.signal,
      });
      if (!res.ok) {
        throw new APIError(
          `Download failed: ${res.status} ${res.statusText}`,
          res.status,
        );
      }
      return await res.blob();
    } catch (err) {
      if (err instanceof APIError) throw err;
      throw new APIError(
        err instanceof Error ? err.message : 'Network error',
        0,
      );
    } finally {
      clearTimeout(timeout);
    }
  }

  // ---------- characters ----------

  async getCharacters(): Promise<Character[]> {
    return this.request<Character[]>('/api/characters');
  }

  async createCharacter(data: CharacterCreate): Promise<Character> {
    const form = new FormData();
    form.append('name', data.name);
    if (data.description) form.append('description', data.description);
    if (data.personality) form.append('personality', data.personality);
    if (data.appearance) form.append('appearance', data.appearance);
    if (data.colorPalette) {
      form.append('colorPalette', JSON.stringify(data.colorPalette));
    }
    if (data.referenceImages) {
      for (const f of data.referenceImages) {
        form.append('referenceImages', f);
      }
    }
    // multipart - do not set content-type, let the browser set boundary
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.timeoutMs);
    try {
      const res = await fetch(`${this.baseURL}/api/characters`, {
        method: 'POST',
        body: form,
        signal: controller.signal,
      });
      if (!res.ok) {
        throw new APIError(
          `Create failed: ${res.status} ${res.statusText}`,
          res.status,
        );
      }
      return (await res.json()) as Character;
    } finally {
      clearTimeout(timeout);
    }
  }

  async getCharacter(id: string): Promise<Character> {
    return this.request<Character>(`/api/characters/${encodeURIComponent(id)}`);
  }

  async updateCharacter(
    id: string,
    data: Partial<Character>,
  ): Promise<Character> {
    return this.request<Character>(
      `/api/characters/${encodeURIComponent(id)}`,
      {
        method: 'PATCH',
        body: JSON.stringify(data),
      },
    );
  }

  async deleteCharacter(id: string): Promise<void> {
    await this.request<void>(`/api/characters/${encodeURIComponent(id)}`, {
      method: 'DELETE',
    });
  }

  // ---------- generation ----------

  async generateImage(req: GenerationRequest): Promise<GenerationResult> {
    return this.request<GenerationResult>('/api/generate', {
      method: 'POST',
      body: JSON.stringify(req),
    });
  }

  async generateStream(
    req: GenerationRequest,
    onProgress: (step: GenerationStep) => void,
  ): Promise<GenerationResult> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10 * 60_000);
    try {
      const res = await fetch(`${this.baseURL}/api/generate/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(req),
        signal: controller.signal,
      });
      if (!res.ok || !res.body) {
        throw new APIError(
          `Stream failed: ${res.status} ${res.statusText}`,
          res.status,
        );
      }
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      let result: GenerationResult | null = null;
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';
        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed.startsWith('data:')) continue;
          const payload = trimmed.slice(5).trim();
          if (!payload) continue;
          try {
            const parsed = JSON.parse(payload) as {
              type: 'step' | 'result' | 'error';
              step?: GenerationStep;
              result?: GenerationResult;
              error?: string;
            };
            if (parsed.type === 'step' && parsed.step) {
              onProgress(parsed.step);
            } else if (parsed.type === 'result' && parsed.result) {
              result = parsed.result;
            } else if (parsed.type === 'error') {
              throw new APIError(parsed.error || 'Stream error', 500);
            }
          } catch (err) {
            if (err instanceof APIError) throw err;
            // ignore malformed lines
          }
        }
      }
      if (!result) {
        throw new APIError('Stream ended without result', 500);
      }
      return result;
    } finally {
      clearTimeout(timeout);
    }
  }

  // ---------- chat ----------

  async chat(
    messages: ChatMessage[],
    onChunk: (text: string) => void,
    characterId?: string,
  ): Promise<void> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 2 * 60_000);
    try {
      const res = await fetch(`${this.baseURL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages, characterId }),
        signal: controller.signal,
      });
      if (!res.ok || !res.body) {
        throw new APIError(
          `Chat failed: ${res.status} ${res.statusText}`,
          res.status,
        );
      }
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';
        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed.startsWith('data:')) continue;
          const payload = trimmed.slice(5).trim();
          if (!payload) continue;
          if (payload === '[DONE]') return;
          try {
            const parsed = JSON.parse(payload) as {
              chunk?: string;
              error?: string;
            };
            if (parsed.error) {
              throw new APIError(parsed.error, 500);
            }
            if (parsed.chunk) onChunk(parsed.chunk);
          } catch (err) {
            if (err instanceof APIError) throw err;
          }
        }
      }
    } finally {
      clearTimeout(timeout);
    }
  }

  // ---------- export ----------

  async exportModel(
    characterId: string,
    format: ExportFormat,
  ): Promise<Blob> {
    return this.requestBlob(
      `/api/export?characterId=${encodeURIComponent(
        characterId,
      )}&format=${encodeURIComponent(format)}`,
    );
  }

  // ---------- expressions ----------

  async getExpressions(characterId?: string): Promise<Expression[]> {
    const q = characterId ? `?characterId=${encodeURIComponent(characterId)}` : '';
    return this.request<Expression[]>(`/api/expressions${q}`);
  }

  // ---------- health ----------

  async healthCheck(): Promise<boolean> {
    try {
      const res = await fetch(`${this.baseURL}/api/health`, {
        signal: AbortSignal.timeout?.(5000),
      });
      return res.ok;
    } catch {
      return false;
    }
  }

  async getStatus(): Promise<SystemStatus | null> {
    try {
      return await this.request<SystemStatus>('/api/status', undefined, 5000);
    } catch {
      return null;
    }
  }
}

export const apiClient = new APIClient();
