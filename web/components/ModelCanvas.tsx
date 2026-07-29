import { forwardRef, useEffect, useImperativeHandle, useRef } from 'react';
import { Live2DPlayer } from '../lib/live2d-player';
import type { ParamMap } from '../types';

export interface ModelCanvasHandle {
  player: Live2DPlayer | null;
  loadModel: (url: string) => Promise<void>;
  setParameters: (params: ParamMap) => void;
  setExpression: (name: string) => void;
  getFps: () => number;
  resize: (w: number, h: number) => void;
}

interface ModelCanvasProps {
  modelUrl?: string;
  className?: string;
  wireframe?: boolean;
  onReady?: (player: Live2DPlayer) => void;
  onFrame?: () => void;
}

const ModelCanvas = forwardRef<ModelCanvasHandle, ModelCanvasProps>(function ModelCanvas(
  { modelUrl, className = '', wireframe = false, onReady, onFrame },
  ref,
) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const playerRef = useRef<Live2DPlayer | null>(null);
  const onReadyRef = useRef(onReady);
  const onFrameRef = useRef(onFrame);
  onReadyRef.current = onReady;
  onFrameRef.current = onFrame;

  useImperativeHandle(ref, () => ({
    get player() {
      return playerRef.current;
    },
    async loadModel(url: string) {
      if (!playerRef.current) return;
      await playerRef.current.loadModel(url);
      playerRef.current.start();
    },
    setParameters(params: ParamMap) {
      playerRef.current?.setParameters(params);
    },
    setExpression(name: string) {
      playerRef.current?.setExpression(name);
    },
    getFps() {
      return playerRef.current?.fps ?? 0;
    },
    resize(w: number, h: number) {
      playerRef.current?.resize(w, h);
    },
  }));

  useEffect(() => {
    if (!canvasRef.current) return;
    const player = new Live2DPlayer(canvasRef.current, {
      backgroundAlpha: 0,
      autoStart: false,
    });
    playerRef.current = player;
    if (onFrameRef.current) {
      player.onFrame(onFrameRef.current);
    }
    onReadyRef.current?.(player);

    return () => {
      player.destroy();
      playerRef.current = null;
    };
  }, []);

  useEffect(() => {
    if (!modelUrl || !playerRef.current) return;
    let cancelled = false;
    playerRef.current
      .loadModel(modelUrl)
      .then(() => {
        if (!cancelled) {
          playerRef.current?.start();
        }
      })
      .catch(() => undefined);
    return () => {
      cancelled = true;
    };
  }, [modelUrl]);

  useEffect(() => {
    if (!containerRef.current || !playerRef.current) return;
    const ro = new ResizeObserver(() => {
      if (!containerRef.current || !playerRef.current) return;
      const r = containerRef.current.getBoundingClientRect();
      playerRef.current.resize(Math.floor(r.width), Math.floor(r.height));
    });
    ro.observe(containerRef.current);
    return () => ro.disconnect();
  }, []);

  return (
    <div
      ref={containerRef}
      className={`relative w-full h-full ${className}`}
      style={{
        backgroundImage:
          wireframe
            ? 'linear-gradient(rgba(139,92,246,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(139,92,246,0.08) 1px, transparent 1px)'
            : undefined,
        backgroundSize: wireframe ? '40px 40px' : undefined,
      }}
    >
      <canvas ref={canvasRef} className="w-full h-full block" />
    </div>
  );
});

export default ModelCanvas;
