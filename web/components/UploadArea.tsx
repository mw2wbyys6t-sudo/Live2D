import { useState, useCallback, useRef } from 'react';

interface UploadAreaProps {
  onUpload: (file: File) => void;
  loading: boolean;
  fileInfo?: { name: string; size: number; width: number; height: number };
}

export default function UploadArea({ onUpload, loading, fileInfo }: UploadAreaProps) {
  const [dragOver, setDragOver] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file && file.name.toLowerCase().endsWith('.psd')) {
      onUpload(file);
    }
  }, [onUpload]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onUpload(file);
    }
  }, [onUpload]);

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
  };

  return (
    <div
      className={`
        relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer
        transition-all duration-200
        ${dragOver
          ? 'border-pink-400 bg-pink-500/10'
          : 'border-gray-600 bg-gray-800/50 hover:border-pink-500/50 hover:bg-gray-800'
        }
        ${loading ? 'pointer-events-none opacity-60' : ''}
      `}
      onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
      onDragLeave={() => setDragOver(false)}
      onDrop={handleDrop}
      onClick={() => fileRef.current?.click()}
    >
      <input
        ref={fileRef}
        type="file"
        accept=".psd"
        onChange={handleFileSelect}
        className="hidden"
      />

      {loading ? (
        <div className="py-4">
          <div className="inline-block w-10 h-10 border-2 border-pink-500 border-t-transparent rounded-full animate-spin mb-3" />
          <p className="text-gray-400">正在分析 PSD 文件...</p>
        </div>
      ) : fileInfo ? (
        <div className="py-2">
          <div className="text-4xl mb-2">📄</div>
          <p className="text-white font-medium mb-1">{fileInfo.name}</p>
          <p className="text-sm text-gray-400">
            {formatSize(fileInfo.size)} &middot; {fileInfo.width}x{fileInfo.height}
          </p>
          <p className="text-xs text-gray-500 mt-2">点击或拖拽以更换文件</p>
        </div>
      ) : (
        <div className="py-4">
          <div className="text-5xl mb-3 opacity-50">📂</div>
          <p className="text-gray-300 font-medium mb-1">
            上传 PSD 文件
          </p>
          <p className="text-sm text-gray-500">
            拖拽 PSD 文件到此处，或点击选择文件
          </p>
          <p className="text-xs text-gray-600 mt-2">
            支持 Photoshop PSD 格式 &middot; 最大 50MB
          </p>
        </div>
      )}
    </div>
  );
}