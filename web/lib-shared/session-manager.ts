import { Live2DWorkflowState } from './types';

const STORAGE_KEY = 'live2d-workflow-state';

export class SessionManager {
  private inMemoryState: Live2DWorkflowState | null = null;

  getDefaultState(): Live2DWorkflowState {
    return {
      mode: 'wizard',
      currentStep: 1,
      completed: [false, false, false, false, false, false, false, false],
      artifacts: {}
    };
  }

  load(): Live2DWorkflowState {
    if (this.inMemoryState) {
      return this.inMemoryState;
    }
    try {
      const serialized = typeof localStorage !== 'undefined' 
        ? localStorage.getItem(STORAGE_KEY) 
        : null;
      if (serialized) {
        const parsed = JSON.parse(serialized) as Live2DWorkflowState;
        this.inMemoryState = parsed;
        return parsed;
      }
    } catch (e) {
      console.warn('Failed to load workflow state', e);
    }
    const defaultState = this.getDefaultState();
    this.inMemoryState = defaultState;
    return defaultState;
  }

  save(state: Live2DWorkflowState): void {
    this.inMemoryState = state;
    try {
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      }
    } catch (e) {
      console.warn('Failed to save workflow state', e);
    }
  }

  clear(): void {
    this.inMemoryState = null;
    try {
      if (typeof localStorage !== 'undefined') {
        localStorage.removeItem(STORAGE_KEY);
      }
    } catch (e) {
      console.warn('Failed to clear workflow state', e);
    }
  }

  serialize(state: Live2DWorkflowState): string {
    return JSON.stringify(state);
  }

  deserialize(serialized: string): Live2DWorkflowState {
    return JSON.parse(serialized);
  }
}

export const sessionManager = new SessionManager();
