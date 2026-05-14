import { useState } from 'react';
import type { NextPage } from 'next';
import Head from 'next/head';
import UploadArea from '../components/UploadArea';
import LayerTree from '../components/LayerTree';
import QAResultPanel from '../components/QAResultPanel';
import RiskScore from '../components/RiskScore';
import { QAResult } from '../lib/qa-engine';

type AppView = 'upload' | 'result';

const Home: NextPage = () => {
  const [view, setView] = useState<AppView>('upload');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fileInfo, setFileInfo] = useState<{ name: string; size: number; width: number; height: number } | undefined>();
  const [result, setResult] = useState<QAResult | null>(null);

  const handleUpload = async (file: File) => {
    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('psd', file);

      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });

      const json = await response.json();

      if (!json.success) {
        setError(json.error || '分析失败');
        setLoading(false);
        return;
      }

      setFileInfo(json.fileInfo);
      setResult(json.data);
      setView('result');
    } catch (err: any) {
      setError(err.message || '上传失败');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setView('upload');
    setFileInfo(undefined);
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-[#0f0f13] text-white">
      <Head>
        <title>Live2D PSD QA Assistant</title>
        <meta name="description" content="Web版 Live2D PSD 质量检测工具" />
        <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🎨</text></svg>" />
      </Head>

      <header className="border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🎨</span>
            <div>
              <h1 className="text-lg font-bold text-pink-400">Live2D PSD QA</h1>
              <p className="text-xs text-gray-500">Web版 PSD 质量检测工具</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {result && (
              <button
                onClick={handleReset}
                className="text-xs text-gray-400 hover:text-white px-3 py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors"
              >
                ↺ 重新分析
              </button>
            )}
            <a
              href="/"
              className="text-xs text-gray-500 hover:text-gray-300"
            >
              v1.0.0
            </a>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6">
        {error && (
          <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg flex items-start gap-2">
            <span className="shrink-0">❌</span>
            <div>
              <p className="text-sm text-red-400 font-medium">分析失败</p>
              <p className="text-xs text-red-300/70 mt-0.5">{error}</p>
            </div>
            <button onClick={() => setError(null)} className="ml-auto shrink-0 text-gray-500 hover:text-white text-xs">
              ✕
            </button>
          </div>
        )}

        {view === 'upload' && !loading && (
          <div className="max-w-lg mx-auto mt-16">
            <div className="text-center mb-8">
              <p className="text-5xl mb-4">🎨</p>
              <h2 className="text-2xl font-bold text-white mb-2">
                Live2D PSD 质量检测
              </h2>
              <p className="text-sm text-gray-400">
                上传 PSD 文件，自动检查 Live2D 风险并生成优化报告
              </p>
            </div>
            <UploadArea onUpload={handleUpload} loading={loading} />
            <div className="mt-8 grid grid-cols-3 gap-4 text-center text-xs text-gray-500">
              <div className="p-3 bg-gray-800/50 rounded-lg">
                <p className="text-lg mb-1">🔍</p>
                <p>图层命名检查</p>
              </div>
              <div className="p-3 bg-gray-800/50 rounded-lg">
                <p className="text-lg mb-1">📊</p>
                <p>结构完整性</p>
              </div>
              <div className="p-3 bg-gray-800/50 rounded-lg">
                <p className="text-lg mb-1">⚡</p>
                <p>Live2D 兼容性</p>
              </div>
            </div>
          </div>
        )}

        {loading && (
          <div className="max-w-lg mx-auto mt-16">
            <UploadArea onUpload={handleUpload} loading={loading} fileInfo={fileInfo} />
          </div>
        )}

        {view === 'result' && result && (
          <div className="grid grid-cols-12 gap-4" style={{ height: 'calc(100vh - 120px)' }}>
            <div className="col-span-3 bg-gray-900/50 border border-gray-800 rounded-xl overflow-hidden flex flex-col">
              <div className="p-4 border-b border-gray-800 shrink-0">
                <h2 className="text-xs text-gray-500 uppercase tracking-wider font-medium mb-2">文件信息</h2>
                {fileInfo && (
                  <div className="space-y-1 text-sm">
                    <p className="text-gray-300 truncate" title={fileInfo.name}>
                      📄 {fileInfo.name}
                    </p>
                    <p className="text-gray-500 text-xs">
                      {fileInfo.width} × {fileInfo.height}
                    </p>
                  </div>
                )}
              </div>
              <div className="flex-1 overflow-hidden">
                <LayerTree
                  layers={result.issues.map(i => ({
                    index: result.issues.indexOf(i),
                    name: i.layer || 'unknown',
                    visible: true,
                    opacity: 1,
                    depth: 0,
                    isGroup: false,
                    bounds: { width: 0, height: 0 },
                    issues: [i.title],
                  }))}
                />
              </div>
            </div>

            <div className="col-span-6 bg-gray-900/50 border border-gray-800 rounded-xl overflow-hidden flex flex-col">
              <QAResultPanel
                issues={result.issues}
                suggestions={result.suggestions}
                summary={result.summary}
              />
            </div>

            <div className="col-span-3 bg-gray-900/50 border border-gray-800 rounded-xl p-4">
              <h2 className="text-xs text-gray-500 uppercase tracking-wider font-medium mb-4">风险评分</h2>
              <RiskScore
                total={result.score.total}
                naming={result.score.naming}
                structure={result.score.structure}
                completeness={result.score.completeness}
                convention={result.score.convention}
              />

              <div className="mt-6 pt-4 border-t border-gray-800">
                <h3 className="text-xs text-gray-500 uppercase tracking-wider font-medium mb-3">快捷操作</h3>
                <div className="space-y-2">
                  <button
                    onClick={() => {
                      const text = JSON.stringify(result, null, 2);
                      navigator.clipboard.writeText(text);
                    }}
                    className="w-full text-xs text-gray-400 hover:text-white bg-gray-800 hover:bg-gray-700 px-3 py-2 rounded-lg transition-colors text-left"
                  >
                    📋 复制报告 JSON
                  </button>
                  <button
                    onClick={handleReset}
                    className="w-full text-xs text-gray-400 hover:text-white bg-gray-800 hover:bg-gray-700 px-3 py-2 rounded-lg transition-colors text-left"
                  >
                    ↺ 分析新的 PSD
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Home;