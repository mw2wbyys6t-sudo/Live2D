import { Live2DWorkflowState } from './types';

const STORAGE_KEY = 'live2d-workflow-session';

export class SessionManager {
  private currentState: Live2DWorkflowState | null = null;
  private storageKey: string;

  constructor(key: string = STORAGE_KEY) {
    this.storageKey = key;
  }

  save(state: Live2DWorkflowState): void {
    try {
      const serialized = this.serialize(state);
      localStorage.setItem(this.storageKey, serialized);
      this.currentState = state;
    } catch (error) {
      console.error('Failed to save session:', error);
      throw new Error('Session save failed');
    }
  }

  load(): Live2DWorkflowState | null {
    try {
      const stored = localStorage.getItem(this.storageKey);
      if (!stored) {
        return null;
      }
      this.currentState = this.deserialize(stored);
      return this.currentState;
    } catch (error) {
      console.error('Failed to load session:', error);
      return null;
    }
  }

  clear(): void {
    try {
      localStorage.removeItem(this.storageKey);
      this.currentState = null;
    } catch (error) {
      console.error('Failed to clear session:', error);
      throw new Error('Session clear failed');
    }
  }

  serialize(state: Live2DWorkflowState): string {
    return JSON.stringify(state, (key, value) => {
      if (value instanceof Date) {
        return {
          __type: 'Date',
          value: value.toISOString(),
        };
      }
      return value;
    });
  }

  deserialize(serialized: string): Live2DWorkflowState {
    return JSON.parse(serialized, (key, value) => {
      if (value && typeof value === 'object' && value.__type === 'Date') {
        return new Date(value.value);
      }
      return value;
    });
  }

  getState(): Live2DWorkflowState | null {
    return this.currentState;
  }

  hasSession(): boolean {
    try {
      return localStorage.getItem(this.storageKey) !== null;
    } catch {
      return false;
    }
  }
}