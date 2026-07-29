import { Application, Container, Sprite, Texture, Assets } from 'pixi.js';
import type { Model3Json, ParameterDef } from '../types';

interface LayerEntry {
  name: string;
  sprite: Sprite;
  baseX: number;
  baseY: number;
  paramBindings?: Array<{
    param: string;
    scaleX?: number;
    scaleY?: number;
    rotate?: number;
  }>;
}

export interface Live2DPlayerOptions {
  backgroundColor?: number;
  backgroundAlpha?: number;
  antialias?: boolean;
  resolution?: number;
  autoStart?: boolean;
}

const STANDARD_PARAMS: ParameterDef[] = [
  { id: 'ParamAngleX', name: 'Angle X', min: -30, max: 30, default: 0, group: 'Head' },
  { id: 'ParamAngleY', name: 'Angle Y', min: -30, max: 30, default: 0, group: 'Head' },
  { id: 'ParamAngleZ', name: 'Angle Z', min: -30, max: 30, default: 0, group: 'Head' },
  { id: 'ParamEyeLOpen', name: 'Eye L Open', min: 0, max: 1, default: 1, group: 'Eyes' },
  { id: 'ParamEyeROpen', name: 'Eye R Open', min: 0, max: 1, default: 1, group: 'Eyes' },
  { id: 'ParamEyeBallX', name: 'Eye Ball X', min: -1, max: 1, default: 0, group: 'Eyes' },
  { id: 'ParamEyeBallY', name: 'Eye Ball Y', min: -1, max: 1, default: 0, group: 'Eyes' },
  { id: 'ParamMouthForm', name: 'Mouth Form', min: -1, max: 1, default: 0, group: 'Mouth' },
  { id: 'ParamMouthOpenY', name: 'Mouth Open', min: 0, max: 1, default: 0, group: 'Mouth' },
  { id: 'ParamBrowLY', name: 'Brow L Y', min: -1, max: 1, default: 0, group: 'Brows' },
  { id: 'ParamBrowRY', name: 'Brow R Y', min: -1, max: 1, default: 0, group: 'Brows' },
  { id: 'ParamBodyAngleX', name: 'Body Angle X', min: -10, max: 10, default: 0, group: 'Body' },
  { id: 'ParamBreath', name: 'Breath', min: 0, max: 1, default: 0, group: 'Body' },
];

/**
 * Browser-side Live2D-like player using PixiJS.
 *
 * This is NOT a full Live2D Cubism runtime — it composites PNG layers with
 * parameter-driven transforms for preview/debug in the browser. For full
 * Cubism rendering, a production build would ship the official Cubism SDK
 * Web runtime; this class keeps the preview and builder pages functional
 * without external binary deps.
 */
export class Live2DPlayer {
  private app: Application | null = null;
  private readonly canvas: HTMLCanvasElement;
  private readonly options: Live2DPlayerOptions;
  private root: Container | null = null;
  private layers: LayerEntry[] = [];
  private params: Map<string, number> = new Map();
  private targetParams: Map<string, number> = new Map();
  private expressions: Map<string, Record<string, number>> = new Map();
  private currentExpression = 'default';
  private running = false;
  private frameCallbacks: Array<() => void> = [];
  private tickerFn: ((dt: number) => void) | null = null;
  private model3: Model3Json | null = null;
  private _fps = 0;
  private _frames = 0;
  private _lastFpsTime = 0;
  private readonly lerpSpeed = 0.15;

  constructor(canvas: HTMLCanvasElement, options: Live2DPlayerOptions = {}) {
    this.canvas = canvas;
    this.options = {
      backgroundColor: 0x000000,
      backgroundAlpha: 0,
      antialias: true,
      resolution: window.devicePixelRatio || 1,
      autoStart: false,
      ...options,
    };
    for (const p of STANDARD_PARAMS) {
      this.params.set(p.id, p.default);
      this.targetParams.set(p.id, p.default);
    }
  }

  async loadModel(modelUrl: string): Promise<void> {
    this.destroy();
    const app = new Application({
      view: this.canvas,
      width: this.canvas.clientWidth || 512,
      height: this.canvas.clientHeight || 512,
      backgroundColor: this.options.backgroundColor,
      backgroundAlpha: this.options.backgroundAlpha,
      antialias: this.options.antialias,
      resolution: this.options.resolution,
      autoDensity: true,
      autoStart: false,
    });
    this.app = app;
    this.root = new Container();
    app.stage.addChild(this.root);

    await this.loadModel3(modelUrl);

    if (this.options.autoStart) {
      this.start();
    }
  }

  private async loadModel3(modelUrl: string): Promise<void> {
    const baseUrl = modelUrl.substring(0, modelUrl.lastIndexOf('/') + 1);
    const res = await fetch(modelUrl);
    if (!res.ok) throw new Error(`Failed to load model3.json: ${res.status}`);
    const model3 = (await res.json()) as Model3Json;
    this.model3 = model3;

    const textures = model3.FileReferences.Textures || [];
    for (let i = 0; i < textures.length; i++) {
      const texUrl = textures[i].startsWith('http')
        ? textures[i]
        : baseUrl + textures[i];
      try {
        const tex = (await Assets.load(texUrl)) as Texture;
        const sprite = new Sprite(tex);
        sprite.anchor.set(0.5, 0.5);
        sprite.x = (this.app!.renderer.width / (this.options.resolution || 1)) / 2;
        sprite.y = (this.app!.renderer.height / (this.options.resolution || 1)) / 2;
        this.root!.addChild(sprite);
        this.layers.push({
          name: `layer_${i}`,
          sprite,
          baseX: sprite.x,
          baseY: sprite.y,
        });
      } catch (err) {
        // eslint-disable-next-line no-console
        console.warn(`Failed to load texture ${texUrl}:`, err);
      }
    }
  }

  setParameter(name: string, value: number): void {
    this.targetParams.set(name, value);
  }

  setParameters(params: Record<string, number>): void {
    for (const [k, v] of Object.entries(params)) {
      if (typeof v === 'number') this.targetParams.set(k, v);
    }
  }

  setExpression(name: string): void {
    this.currentExpression = name;
    const exp = this.expressions.get(name);
    if (!exp) return;
    for (const [k, v] of Object.entries(exp)) {
      this.targetParams.set(k, v);
    }
  }

  get currentExpressionName(): string {
    return this.currentExpression;
  }

  registerExpression(name: string, params: Record<string, number>): void {
    this.expressions.set(name, params);
  }

  getParameter(name: string): number {
    return this.params.get(name) ?? 0;
  }

  getAllParameters(): Record<string, number> {
    const out: Record<string, number> = {};
    this.params.forEach((v, k) => {
      out[k] = v;
    });
    return out;
  }

  get fps(): number {
    return this._fps;
  }

  get modelMeta(): Model3Json | null {
    return this.model3;
  }

  resize(width: number, height: number): void {
    if (!this.app) return;
    this.app.renderer.resize(width, height);
    // re-center layers
    for (const layer of this.layers) {
      layer.baseX = width / 2;
      layer.baseY = height / 2;
    }
  }

  start(): void {
    if (this.running || !this.app) return;
    this.running = true;
    this._lastFpsTime = performance.now();
    this._frames = 0;
    this.tickerFn = (dt: number) => this.update(dt);
    this.app.ticker.add(this.tickerFn);
    this.app.start();
  }

  stop(): void {
    if (!this.running || !this.app) return;
    this.running = false;
    if (this.tickerFn) {
      this.app.ticker.remove(this.tickerFn);
      this.tickerFn = null;
    }
    this.app.stop();
  }

  private update(deltaFrames: number): void {
    const dt = deltaFrames / 60;
    // lerp toward targets
    this.targetParams.forEach((target, key) => {
      const current = this.params.get(key) ?? target;
      const next = current + (target - current) * Math.min(1, this.lerpSpeed * 60 * dt);
      this.params.set(key, next);
    });

    // apply to layers
    const angleX = this.params.get('ParamAngleX') ?? 0;
    const angleY = this.params.get('ParamAngleY') ?? 0;
    const angleZ = this.params.get('ParamAngleZ') ?? 0;
    const bodyX = this.params.get('ParamBodyAngleX') ?? 0;
    const breath = this.params.get('ParamBreath') ?? 0;
    const time = performance.now() * 0.001;
    const breathVal = breath + Math.sin(time * 1.5) * 0.5 + 0.5;

    for (let i = 0; i < this.layers.length; i++) {
      const layer = this.layers[i];
      const depthFactor = i / Math.max(1, this.layers.length - 1);
      const px = depthFactor * angleX * 2;
      const py = depthFactor * angleY * 2;
      layer.sprite.x = layer.baseX + px + bodyX * 1.5;
      layer.sprite.y = layer.baseY + py + (i === 0 ? breathVal * -2 : 0);
      layer.sprite.rotation = (angleZ * Math.PI) / 180 * 0.3;
      layer.sprite.skew.x = (angleX * Math.PI) / 180 * 0.15 * depthFactor;
      layer.sprite.skew.y = (angleY * Math.PI) / 180 * 0.15 * depthFactor;
    }

    this._frames++;
    const now = performance.now();
    if (now - this._lastFpsTime >= 1000) {
      this._fps = Math.round(
        (this._frames * 1000) / (now - this._lastFpsTime),
      );
      this._frames = 0;
      this._lastFpsTime = now;
    }

    for (const cb of this.frameCallbacks) {
      try {
        cb();
      } catch (err) {
        // eslint-disable-next-line no-console
        console.error('Frame callback error:', err);
      }
    }
  }

  onFrame(callback: () => void): void {
    this.frameCallbacks.push(callback);
  }

  offFrame(callback: () => void): void {
    const idx = this.frameCallbacks.indexOf(callback);
    if (idx >= 0) this.frameCallbacks.splice(idx, 1);
  }

  destroy(): void {
    this.stop();
    this.frameCallbacks = [];
    this.layers = [];
    this.params.clear();
    this.targetParams.clear();
    this.expressions.clear();
    if (this.app) {
      this.app.destroy(true, { children: true, texture: true, baseTexture: true });
      this.app = null;
    }
    this.root = null;
    this.model3 = null;
  }

  get stage(): Container | null {
    return this.root;
  }

  get pixiApp(): Application | null {
    return this.app;
  }
}
