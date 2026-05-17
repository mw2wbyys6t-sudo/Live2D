import { useState, useCallback, useRef } from 'react';
import { createPSDFromImage } from '../lib/image-to-psd';
import { formatSize } from '../lib/utils';
import { validateImageFile, sanitizeFileName, MAX_FILE_SIZE, MAX_IMAGE_DIMENSION, withTimeout } from '../lib/security';

const ImageIcon = () => (
  <svg className="w-16 h-16" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="8" y="12" width="48" height="40" rx="4" stroke="currentColor" strokeWidth="2" />
    <circle cx="24" cy="26" r="4" stroke="currentColor" strokeWidth="2" />
    <path d="M8 40L22 28L32 38L42 30L56 42" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const CheckCircleIcon = () => (
  <svg className="w-8 h-8" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="16" cy="16" r="14" stroke="currentColor" strokeWidth="2" />
    <path d="M10 16L14 20L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const SpinnerIcon = () => (
  <svg className="w-6 h-6 animate-spin" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="24" cy="24" r="20" stroke="currentColor" strokeWidth="4" strokeOpacity="0.2" />
    <path d="M44 24C44 35.0457 35.0457 44 24 44" stroke="currentColor" strokeWidth="4" strokeLinecap="round" />
  </svg>
);

const ALLOWED_TYPES = ['image/png', 'image/jpeg', 'image/webp', 'image/gif', 'image/bmp'];

export default function ImageToPsd() {
  const [dragOver, setDragOver] = useState(false);
  const [image, setImage] = useState<{ file: File; dataUrl: string } | null>(null);
  const [converting, setConverting] = useState(false);
  const [done, setDone] = useState(false);
  const [psdName, setPsdName] = useState('');
  const [error, setError] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback(async (file: File) => {
    setError(null);
    setDone(false);
    setPsdName('');

    if (file.size > MAX_FILE_SIZE) {
      setError('文件大小超过限制 (最大 50MB)');
      return;
    }

    if (!ALLOWED_TYPES.includes(file.type)) {
      setError('不支持的文件格式，请上传 PNG、JPG、WEBP、GIF 或 BMP 图片');
      return;
    }

    const valid = await validateImageFile(file);
    if (!valid) {
      setError('文件内容不是有效的图片格式');
      return;
    }

    const dataUrl = URL.createObjectURL(file);
    setImage({ file, dataUrl });
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, [handleFile]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  }, [handleFile]);

  const handleConvert = useCallback(async () => {
    if (!image) return;
    setConverting(true);
    setError(null);

    try {
      const img = await withTimeout(
        new Promise<HTMLImageElement>((resolve, reject) => {
          const img = new Image();
          img.src = image.dataUrl;
          img.onload = () => resolve(img);
          img.onerror = () => reject(new Error('图片加载失败'));
        }),
        10000,
        '图片加载超时'
      );

      if (img.width > MAX_IMAGE_DIMENSION || img.height > MAX_IMAGE_DIMENSION) {
        throw new Error(`图片尺寸过大，最大支持 ${MAX_IMAGE_DIMENSION}x${MAX_IMAGE_DIMENSION}`);
      }

      const canvas = document.createElement('canvas');
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext('2d');
      if (!ctx) throw new Error('无法创建 Canvas');

      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, img.width, img.height);
      ctx.drawImage(img, 0, 0);

      const imageData = ctx.getImageData(0, 0, img.width, img.height);
      const baseName = sanitizeFileName(image.file.name.replace(/\.[^.]+$/, ''));
      const psdBuffer = createPSDFromImage(imageData, img.width, img.height, baseName);

      const blob = new Blob([psdBuffer], { type: 'image/vnd.adobe.photoshop' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${baseName}.psd`;
      a.style.display = 'none';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      setPsdName(`${baseName}.psd`);
      setDone(true);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      setError(msg || '转换失败，请重试');
    }
    setConverting(false);
  }, [image]);

  const handleReset = useCallback(() => {
    if (image?.dataUrl) URL.revokeObjectURL(image.dataUrl);
    setImage(null);
    setDone(false);
    setPsdName('');
    setError(null);
  }, [image]);

  return (
    <div className="w-full max-w-lg mx-auto">
      <div className="text-center mb-4 sm:mb-6">
        <p className="text-4xl sm:text-5xl mb-3 sm:mb-4">📷</p>
        <h2 className="text-xl sm:text-2xl font-bold text-white mb-2">
          图片转 PSD
        </h2>
        <p className="text-xs sm:text-sm text-gray-400">
          上传图片，自动转换为 Photoshop PSD 文件
        </p>
      </div>

      {error && (
        <div className="mb-3 sm:mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg flex items-start gap-2">
          <span className="shrink-0">❌</span>
          <p className="text-xs sm:text-sm text-red-300 flex-1">{error}</p>
          <button onClick={() => setError(null)} className="text-gray-500 hover:text-white text-xs">✕</button>
        </div>
      )}

      <div
        className={`
          relative overflow-hidden rounded-xl sm:rounded-2xl
          transition-all duration-500 ease-out
          ${dragOver
            ? 'bg-gradient-to-br from-emerald-500/20 via-teal-500/20 to-cyan-500/20 border-2 border-emerald-400/50 scale-[1.01] sm:scale-[1.02]'
            : 'bg-gradient-to-br from-gray-800/40 via-gray-800/30 to-gray-800/20 border-2 border-dashed border-gray-600/50 hover:border-gray-500/60 hover:from-gray-800/50'
          }
          ${converting ? 'pointer-events-none' : 'cursor-pointer touch-manipulation'}
          backdrop-blur-xl
        `}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => !converting && !image && fileRef.current?.click()}
      >
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 via-transparent to-cyan-500/5 pointer-events-none" />

        <div className="absolute -top-16 -right-16 w-32 h-32 sm:-top-24 sm:-right-24 sm:w-48 sm:h-48 bg-gradient-to-br from-emerald-500/20 to-cyan-500/20 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-16 -left-16 w-32 h-32 sm:-bottom-24 sm:-left-24 sm:w-48 sm:h-48 bg-gradient-to-br from-teal-500/20 to-emerald-500/20 rounded-full blur-3xl pointer-events-none" />

        <input
          ref={fileRef}
          type="file"
          accept=".png,.jpg,.jpeg,.webp,.gif,.bmp"
          onChange={handleFileSelect}
          className="hidden"
        />

        {converting ? (
          <div className="py-12 px-4 sm:py-16 sm:px-8 flex flex-col items-center justify-center animate-pulse">
            <div className="text-emerald-400 mb-3 sm:mb-4">
              <SpinnerIcon />
            </div>
            <p className="text-gray-300 font-medium text-base sm:text-lg mb-2">正在转换图片</p>
            <p className="text-gray-500 text-xs sm:text-sm">生成 PSD 文件中...</p>
            <div className="mt-6 sm:mt-8 w-full max-w-xs h-1 bg-gray-700/50 rounded-full overflow-hidden">
              <div className="h-full bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-full animate-progress" />
            </div>
          </div>
        ) : image ? (
          <div className="py-4 px-4 sm:py-6 sm:px-8 flex flex-col items-center">
            <div className="relative w-full max-w-[280px] aspect-video mb-4 rounded-lg overflow-hidden bg-gray-900/50 border border-gray-700/50">
              <img
                src={image.dataUrl}
                alt={image.file.name}
                className="w-full h-full object-contain"
              />
            </div>
            <p className="text-white font-semibold text-sm sm:text-base mb-2 truncate max-w-[80%]" title={image.file.name}>
              {image.file.name}
            </p>
            <div className="flex flex-wrap items-center justify-center gap-2 text-xs text-gray-400 mb-4">
              <span className="px-2 py-1 bg-gray-700/50 rounded-lg">{formatSize(image.file.size)}</span>
              <span className="px-2 py-1 bg-gray-700/50 rounded-lg">
                <span id="img-dims">加载中...</span>
              </span>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={(e) => { e.stopPropagation(); handleReset(); }}
                className="px-3 py-2 rounded-lg text-xs font-medium bg-gray-700 text-gray-300 hover:bg-gray-600 transition-colors"
              >
                重新选择
              </button>
              <button
                onClick={(e) => { e.stopPropagation(); handleConvert(); }}
                className="px-4 py-2 rounded-lg text-xs font-medium bg-gradient-to-r from-emerald-500 to-teal-600 text-white hover:from-emerald-600 hover:to-teal-700 shadow-lg shadow-emerald-500/30 active:scale-95 transition-all"
              >
                转换为 PSD
              </button>
            </div>
            {done && (
              <div className="mt-4 flex items-center gap-2 text-emerald-400 text-xs">
                <CheckCircleIcon />
                <span>{psdName} 已下载</span>
              </div>
            )}
          </div>
        ) : (
          <div className="py-10 px-4 sm:py-16 sm:px-8 flex flex-col items-center justify-center">
            <div className={`mb-4 sm:mb-6 transition-all duration-500 ${dragOver ? 'text-emerald-400 scale-110' : 'text-gray-500'}`}>
              <ImageIcon />
            </div>

            <h3 className="text-lg sm:text-xl font-semibold text-white mb-2 sm:mb-3">
              {dragOver ? '释放以上传' : '上传图片文件'}
            </h3>

            <p className="text-gray-400 text-center mb-4 sm:mb-6 max-w-md text-xs sm:text-sm">
              {dragOver
                ? '图片正在被拖拽到此处'
                : '拖拽图片到此处，或点击选择文件'}
            </p>

            <div className="flex flex-wrap items-center justify-center gap-2 text-xs text-gray-500">
              <span className="px-2 py-1 sm:px-3 sm:py-1.5 bg-gray-700/50 rounded-lg border border-gray-600/30 flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                PNG / JPG / WEBP
              </span>
              <span className="px-2 py-1 sm:px-3 sm:py-1.5 bg-gray-700/50 rounded-lg border border-gray-600/30">
                最大 50MB
              </span>
            </div>

            <div className="mt-6 sm:mt-8 flex flex-wrap items-center justify-center gap-4 sm:gap-6 text-xs text-gray-600">
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 sm:w-8 sm:h-8 bg-emerald-500/10 rounded-lg flex items-center justify-center">
                  <svg className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                  </svg>
                </div>
                <span>一键转换</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 sm:w-8 sm:h-8 bg-teal-500/10 rounded-lg flex items-center justify-center">
                  <svg className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-teal-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <span>本地处理</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 sm:w-8 sm:h-8 bg-cyan-500/10 rounded-lg flex items-center justify-center">
                  <svg className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <span>即时下载</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {done && (
        <div className="mt-4 p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-lg flex items-center gap-2">
          <CheckCircleIcon />
          <div className="flex-1 min-w-0">
            <p className="text-sm text-emerald-400 font-medium">转换完成</p>
            <p className="text-xs text-emerald-300/70 truncate">{psdName} 已自动下载</p>
          </div>
        </div>
      )}
    </div>
  );
}