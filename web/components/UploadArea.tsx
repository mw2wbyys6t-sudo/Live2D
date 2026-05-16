import { useState, useCallback, useRef } from 'react';
import { formatSize } from '../lib/utils';

interface UploadAreaProps {
  onUpload: (file: File) => void;
  loading: boolean;
  fileInfo?: { name: string; size: number; width: number; height: number };
}

const UploadIcon = () => (
  <svg className="w-16 h-16" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="8" y="12" width="48" height="40" rx="4" stroke="currentColor" strokeWidth="2" />
    <path d="M8 24C8 24 16 20 32 20C48 20 56 24 56 24" stroke="currentColor" strokeWidth="2" />
    <path d="M20 36L32 28L44 36" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M32 28V44" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
  </svg>
);

const FileIcon = () => (
  <svg className="w-12 h-12" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M10 6C10 4.89543 10.8954 4 12 4H28L38 14V42C38 43.1046 37.1046 44 36 44H12C10.8954 44 10 43.1046 10 42V6Z" fill="currentColor" fillOpacity="0.1" stroke="currentColor" strokeWidth="2" />
    <path d="M28 4V14H38" stroke="currentColor" strokeWidth="2" />
  </svg>
);

const CheckIcon = () => (
  <svg className="w-8 h-8" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="16" cy="16" r="14" stroke="currentColor" strokeWidth="2" />
    <path d="M10 16L14 20L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const SpinnerIcon = () => (
  <svg className="w-12 h-12 animate-spin" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="24" cy="24" r="20" stroke="currentColor" strokeWidth="4" strokeOpacity="0.2" />
    <path d="M44 24C44 35.0457 35.0457 44 24 44" stroke="currentColor" strokeWidth="4" strokeLinecap="round" />
  </svg>
);

export default function UploadArea({ onUpload, loading, fileInfo }: UploadAreaProps) {
  const [dragOver, setDragOver] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file && file.name.toLowerCase().endsWith('.psd')) {
      setIsSuccess(true);
      setTimeout(() => setIsSuccess(false), 2000);
      onUpload(file);
    }
  }, [onUpload]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setIsSuccess(true);
      setTimeout(() => setIsSuccess(false), 2000);
      onUpload(file);
    }
  }, [onUpload]);

  return (
    <div
      className={`
        relative overflow-hidden rounded-xl sm:rounded-2xl
        transition-all duration-500 ease-out
        ${dragOver
          ? 'bg-gradient-to-br from-pink-500/20 via-purple-500/20 to-blue-500/20 border-2 border-pink-400/50 scale-[1.01] sm:scale-[1.02]'
          : 'bg-gradient-to-br from-gray-800/40 via-gray-800/30 to-gray-800/20 border-2 border-dashed border-gray-600/50 hover:border-gray-500/60 hover:from-gray-800/50'
        }
        ${loading ? 'pointer-events-none' : 'cursor-pointer touch-manipulation'}
        ${isSuccess ? 'bg-gradient-to-br from-green-500/20 to-emerald-500/20 border-green-400/50' : ''}
        backdrop-blur-xl
      `}
      onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
      onDragLeave={() => setDragOver(false)}
      onDrop={handleDrop}
      onClick={() => !loading && fileRef.current?.click()}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-pink-500/5 via-transparent to-purple-500/5 pointer-events-none" />
      
      <div className="absolute -top-16 -right-16 w-32 h-32 sm:-top-24 sm:-right-24 sm:w-48 sm:h-48 bg-gradient-to-br from-pink-500/20 to-purple-500/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-16 -left-16 w-32 h-32 sm:-bottom-24 sm:-left-24 sm:w-48 sm:h-48 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-full blur-3xl pointer-events-none" />

      <input
        ref={fileRef}
        type="file"
        accept=".psd"
        onChange={handleFileSelect}
        className="hidden"
      />

      {loading ? (
        <div className="py-12 px-4 sm:py-16 sm:px-8 flex flex-col items-center justify-center animate-pulse">
          <div className="text-pink-400 mb-3 sm:mb-4">
            <SpinnerIcon />
          </div>
          <p className="text-gray-300 font-medium text-base sm:text-lg mb-2">正在分析 PSD 文件</p>
          <p className="text-gray-500 text-xs sm:text-sm">请稍候...</p>
          
          <div className="mt-6 sm:mt-8 w-full max-w-xs h-1 bg-gray-700/50 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-pink-500 to-purple-500 rounded-full animate-progress" />
          </div>
        </div>
      ) : fileInfo ? (
        <div className="py-8 px-4 sm:py-12 sm:px-8 flex flex-col items-center justify-center">
          <div className="text-green-400 mb-3 sm:mb-4 transform scale-110">
            <CheckIcon />
          </div>
          <p className="text-white font-semibold text-base sm:text-lg mb-2 truncate max-w-[80%]" title={fileInfo.name}>
            {fileInfo.name}
          </p>
          <div className="flex flex-wrap items-center justify-center gap-2 sm:gap-4 text-xs sm:text-sm text-gray-400 mb-3 sm:mb-4">
            <span className="px-2 py-1 sm:px-3 sm:py-1 bg-gray-700/50 rounded-lg">{formatSize(fileInfo.size)}</span>
            <span className="px-2 py-1 sm:px-3 sm:py-1 bg-gray-700/50 rounded-lg">{fileInfo.width} × {fileInfo.height}</span>
          </div>
          <p className="text-xs text-gray-500 mt-3 sm:mt-4 flex items-center gap-2">
            <span className="w-2 h-2 bg-pink-400 rounded-full animate-pulse" />
            点击或拖拽以更换文件
          </p>
        </div>
      ) : (
        <div className="py-10 px-4 sm:py-16 sm:px-8 flex flex-col items-center justify-center">
          <div className={`mb-4 sm:mb-6 transition-all duration-500 ${dragOver ? 'text-pink-400 scale-110' : 'text-gray-500'}`}>
            <UploadIcon />
          </div>
          
          <h3 className="text-lg sm:text-xl font-semibold text-white mb-2 sm:mb-3">
            {dragOver ? '释放以上传' : '上传 PSD 文件'}
          </h3>
          
          <p className="text-gray-400 text-center mb-4 sm:mb-6 max-w-md text-xs sm:text-sm">
            {dragOver 
              ? '文件正在被拖拽到此处' 
              : '拖拽 PSD 文件到此处，或点击选择文件'}
          </p>
          
          <div className="flex flex-wrap items-center justify-center gap-2 text-xs text-gray-500">
            <span className="px-2 py-1 sm:px-3 sm:py-1.5 bg-gray-700/50 rounded-lg border border-gray-600/30 flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              PSD
            </span>
            <span className="px-2 py-1 sm:px-3 sm:py-1.5 bg-gray-700/50 rounded-lg border border-gray-600/30">
              最大 50MB
            </span>
          </div>

          <div className="mt-6 sm:mt-8 flex flex-wrap items-center justify-center gap-4 sm:gap-6 text-xs text-gray-600">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 sm:w-8 sm:h-8 bg-pink-500/10 rounded-lg flex items-center justify-center">
                <svg className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-pink-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <span>本地处理</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 sm:w-8 sm:h-8 bg-purple-500/10 rounded-lg flex items-center justify-center">
                <svg className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <span>即时分析</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 sm:w-8 sm:h-8 bg-blue-500/10 rounded-lg flex items-center justify-center">
                <svg className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <span>AI 辅助</span>
            </div>
          </div>
        </div>
      )}

      {dragOver && (
        <div className="absolute inset-0 bg-gradient-to-br from-pink-500/30 to-purple-500/30 flex items-center justify-center backdrop-blur-sm">
          <div className="text-center">
            <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-white/20 flex items-center justify-center">
              <svg className="w-10 h-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <p className="text-white font-semibold text-lg">释放以上传 PSD</p>
          </div>
        </div>
      )}
    </div>
  );
}
