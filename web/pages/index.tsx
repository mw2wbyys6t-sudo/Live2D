import { useState, useCallback } from 'react';
import type { NextPage } from 'next';
import Head from 'next/head';
import UploadArea from '../components/UploadArea';
import LayerTree from '../components/LayerTree';
import QAResult from '../components/QAResult';
import ChatAssistant from '../components/ChatAssistant';
import ImageToPsd from '../components/ImageToPsd';
import { parsePSD } from '../lib/psd-parser';
import { analyzePSD, getEnhancedResult, QAIssue } from '../lib/qa-engine';
import { getErrorMessage } from '../lib/utils';

type AppView = 'upload' | 'result';
type AppMode = 'qa' | 'convert';

const Home: NextPage = () => {
  const [view, setView] = useState<AppView>('upload');
  const [mode, setMode] = useState<AppMode>('qa');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fileInfo, setFileInfo] = useState<{ name: string; size: number; width: number; height: number } | undefined>();
  const [result, setResult] = useState<{
    score: number;
    issues: QAIssue[];
    warnings: QAIssue[];
    suggestions: string[];
    layer_stats: {
      total: number;
      visible: number;
      hidden: number;
      groups: number;
      empty: number;
      semiTransparent: number;
      nonNormalBlend: number;
      offscreen: number;
      duplicateNames: number;
    };
    summary: {
      totalLayers: number;
      visibleLayers: number;
      hiddenLayers: number;
      groups: number;
      hasMissingCritical: boolean;
      hasNamingIssues: boolean;
      hasStructuralIssues: boolean;
    };
  } | null>(null);

  const handleUpload = useCallback(async (file: File) => {
    setLoading(true);
    setError(null);

    if (file.size > 50 * 1024 * 1024) {
      setError('文件大小超过限制 (最大 50MB)');
      setLoading(false);
      return;
    }

    try {
      const buffer = await file.arrayBuffer();
      const psdInfo = parsePSD(buffer);

      if (!psdInfo.valid) {
        const errorInfo = getErrorMessage(psdInfo.error);
        setError(`${errorInfo.title}: ${errorInfo.message}\n\n建议: ${errorInfo.suggestion}`);
        setLoading(false);
        return;
      }

      const qaResult = analyzePSD(psdInfo);
      const enhanced = getEnhancedResult(qaResult);

      setFileInfo({
        name: file.name,
        size: file.size,
        width: psdInfo.width,
        height: psdInfo.height,
      });

      setResult({
        score: enhanced.score,
        issues: enhanced.issues,
        warnings: enhanced.warnings,
        suggestions: enhanced.suggestions,
        layer_stats: enhanced.layer_stats,
        summary: qaResult.summary,
      });

      setView('result');
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      const errorInfo = getErrorMessage(msg);
      setError(`${errorInfo.title}: ${errorInfo.message}\n\n建议: ${errorInfo.suggestion}`);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleReset = useCallback(() => {
    setView('upload');
    setFileInfo(undefined);
    setResult(null);
    setError(null);
  }, []);

  return (
    <div className="min-h-screen bg-[#0f0f13] text-white sm:min-h-[100vh]">
      <Head>
        <title>Live2D PSD QA Assistant</title>
        <meta name="description" content="Web版 Live2D PSD 质量检测工具" />
        <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🎨</text></svg>" />
      </Head>

      <header className="border-b border-gray-800 sticky top-0 z-50 bg-[#0f0f13]/95 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-3 sm:px-4 py-2 sm:py-3 flex items-center justify-between">
          <div className="flex items-center gap-2 sm:gap-3">
            <span className="text-xl sm:text-2xl">🎨</span>
            <div className="hidden sm:block">
              <h1 className="text-base sm:text-lg font-bold text-pink-400">Live2D PSD QA</h1>
              <p className="text-xs text-gray-500">Web版 PSD 质量检测工具</p>
            </div>
            <div className="sm:hidden">
              <h1 className="text-base font-bold text-pink-400">Live2D QA</h1>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="flex bg-gray-800 rounded-lg p-0.5 mr-2">
              <button
                onClick={() => { setMode('qa'); setError(null); }}
                className={`text-xs px-2 sm:px-3 py-1 sm:py-1.5 rounded-md transition-all ${mode === 'qa' ? 'bg-pink-500 text-white shadow-sm' : 'text-gray-400 hover:text-white'}`}
              >
                PSD 检测
              </button>
              <button
                onClick={() => { setMode('convert'); setError(null); }}
                className={`text-xs px-2 sm:px-3 py-1 sm:py-1.5 rounded-md transition-all ${mode === 'convert' ? 'bg-emerald-500 text-white shadow-sm' : 'text-gray-400 hover:text-white'}`}
              >
                图片转PSD
              </button>
            </div>
            {result && (
              <button
                onClick={handleReset}
                className="text-xs sm:text-sm text-gray-400 hover:text-white px-2 sm:px-3 py-1 sm:py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors"
              >
                ↺ 重新分析
              </button>
            )}
            <span className="hidden sm:block text-xs text-gray-500">v2.0.0</span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-3 sm:px-4 py-4 sm:py-6">
        {error && (
          <div className="mb-3 sm:mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg flex items-start gap-2">
            <span className="shrink-0">❌</span>
            <div className="flex-1 min-w-0">
              <p className="text-sm text-red-400 font-medium">分析失败</p>
              <p className="text-xs text-red-300/70 mt-0.5 break-all">{error}</p>
            </div>
            <button onClick={() => setError(null)} className="ml-auto shrink-0 text-gray-500 hover:text-white text-xs">
              ✕
            </button>
          </div>
        )}

        {view === 'upload' && !loading && mode === 'qa' && (
          <div className="flex flex-col lg:flex-row gap-4 lg:gap-6" style={{ height: 'calc(100vh - 120px)' }}>
            <div className="lg:w-[60%] flex items-center justify-center lg:justify-start">
              <div className="w-full max-w-lg px-2">
                <div className="text-center mb-4 sm:mb-8">
                  <p className="text-4xl sm:text-5xl mb-3 sm:mb-4">🎨</p>
                  <h2 className="text-xl sm:text-2xl font-bold text-white mb-2">
                    Live2D PSD 质量检测
                  </h2>
                  <p className="text-xs sm:text-sm text-gray-400">
                    上传 PSD 文件，自动检查 Live2D 风险并生成优化报告
                  </p>
                </div>
                <UploadArea onUpload={handleUpload} loading={loading} />
                <div className="mt-4 sm:mt-8 grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-4 text-center text-xs text-gray-500">
                  <div className="p-2 sm:p-3 bg-gray-800/50 rounded-lg">
                    <p className="text-base sm:text-lg mb-1">🔍</p>
                    <p>图层命名</p>
                  </div>
                  <div className="p-2 sm:p-3 bg-gray-800/50 rounded-lg">
                    <p className="text-base sm:text-lg mb-1">📊</p>
                    <p>结构完整性</p>
                  </div>
                  <div className="p-2 sm:p-3 bg-gray-800/50 rounded-lg">
                    <p className="text-base sm:text-lg mb-1">⚡</p>
                    <p>对称性</p>
                  </div>
                  <div className="p-2 sm:p-3 bg-gray-800/50 rounded-lg">
                    <p className="text-base sm:text-lg mb-1">🎯</p>
                    <p>风险评分</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="lg:w-[40%] lg:min-w-[360px]">
              <ChatAssistant qaResult={undefined} />
            </div>
          </div>
        )}

        {view === 'upload' && !loading && mode === 'convert' && (
          <div className="flex items-center justify-center" style={{ height: 'calc(100vh - 120px)' }}>
            <ImageToPsd />
          </div>
        )}

        {loading && (
          <div className="max-w-lg mx-auto mt-8 sm:mt-16 px-2">
            <UploadArea onUpload={handleUpload} loading={loading} fileInfo={fileInfo} />
          </div>
        )}

        {view === 'result' && result && (
          <div className="flex flex-col xl:flex-row gap-3 sm:gap-4" style={{ height: 'calc(100vh - 100px)' }}>
            <div className="hidden lg:block w-64 bg-gray-900/50 border border-gray-800 rounded-xl overflow-hidden flex flex-col">
              <div className="p-3 sm:p-4 border-b border-gray-800 shrink-0">
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
                  layers={result.issues.map((i, idx) => ({
                    index: idx,
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

            <div className="flex-1 lg:flex-[1.5] bg-gray-900/50 border border-gray-800 rounded-xl overflow-hidden flex flex-col min-h-[400px] sm:min-h-[500px]">
              <QAResult
                score={result.score}
                issues={result.issues}
                warnings={result.warnings}
                suggestions={result.suggestions}
                layer_stats={result.layer_stats}
                summary={result.summary}
              />
            </div>

            <div className="xl:w-[360px]">
              <ChatAssistant qaResult={result} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Home;