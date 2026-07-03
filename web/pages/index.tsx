import { useState, useCallback, useMemo, useEffect, useRef } from 'react';
import type { NextPage } from 'next';
import dynamic from 'next/dynamic';
import UploadArea from '../components/UploadArea';
import LayerTree from '../components/LayerTree';
import QAResult from '../components/QAResult';
import SEO from '../components/SEO';
import ErrorBoundary from '../components/ErrorBoundary';
import WorkflowTracker from '../components/WorkflowTracker';
import { parsePSD } from '../lib/psd-parser';
import { analyzePSD, getEnhancedResult, QAIssue } from '../lib/qa-engine';
import { getErrorMessage } from '../lib/utils';
import { Live2DWorkflow } from '../lib/workflow';
import { STEP_NAMES } from '../lib/types';

const ChatAssistant = dynamic(() => import('../components/ChatAssistant'), {
  ssr: false,
  loading: () => (
    <div className="h-full min-h-[400px] bg-gray-900/50 border border-gray-800 rounded-xl animate-pulse" />
  ),
});

const ImageToPsd = dynamic(() => import('../components/ImageToPsd'), {
  ssr: false,
  loading: () => (
    <div className="h-[60vh] bg-gray-900/50 border border-gray-800 rounded-xl animate-pulse" />
  ),
});

type AppView = 'upload' | 'result';
type AppMode = 'qa' | 'convert';
type LoadingStage = 'idle' | 'loading' | 'parsing' | 'analyzing' | 'complete';

const Home: NextPage = () => {
  const [view, setView] = useState<AppView>('upload');
  const [mode, setMode] = useState<AppMode>('qa');
  const [loadingStage, setLoadingStage] = useState<LoadingStage>('idle');
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

  const workflowRef = useRef<Live2DWorkflow>(new Live2DWorkflow());
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [expertMode, setExpertMode] = useState(false);
  const [completedSteps, setCompletedSteps] = useState<boolean[]>([false, false, false, false, false, false, false, false]);

  useEffect(() => {
    const workflow = workflowRef.current;
    const state = workflow.getState();
    setCurrentStepIndex(state.currentStep - 1);
    setCompletedSteps([...state.completed]);
    setExpertMode(state.mode === 'expert');
  }, []);

  const handleUpload = useCallback(async (file: File) => {
    setLoadingStage('loading');
    setError(null);

    if (file.size > 50 * 1024 * 1024) {
      setError('文件大小超过限制 (最大 50MB)');
      setLoadingStage('idle');
      return;
    }

    try {
      setLoadingStage('parsing');
      const buffer = await file.arrayBuffer();
      const psdInfo = parsePSD(buffer);

      if (!psdInfo.valid) {
        const errorInfo = getErrorMessage(psdInfo.error);
        setError(`${errorInfo.title}: ${errorInfo.message}\n\n建议: ${errorInfo.suggestion}`);
        setLoadingStage('idle');
        return;
      }

      setLoadingStage('analyzing');
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

      setLoadingStage('complete');
      setTimeout(() => setView('result'), 300);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      const errorInfo = getErrorMessage(msg);
      setError(`${errorInfo.title}: ${errorInfo.message}\n\n建议: ${errorInfo.suggestion}`);
      setLoadingStage('idle');
    }
  }, []);

  const handleReset = useCallback(() => {
    setView('upload');
    setFileInfo(undefined);
    setResult(null);
    setError(null);
  }, []);

  const handleSetMode = useCallback((newMode: AppMode) => {
    setMode(newMode);
    setError(null);
  }, []);

  const handleClearError = useCallback(() => setError(null), []);

  const handleWorkflowReset = useCallback(() => {
    const workflow = workflowRef.current;
    workflow.reset();
    setCurrentStepIndex(0);
    setCompletedSteps([false, false, false, false, false, false, false, false]);
    setExpertMode(false);
  }, []);

  const handleStepClick = useCallback((stepIndex: number) => {
    const workflow = workflowRef.current;
    
    if (expertMode || stepIndex <= currentStepIndex) {
      workflow.goToStep(stepIndex + 1);
      setCurrentStepIndex(stepIndex);
    }
  }, [expertMode, currentStepIndex]);

  const [touchStart, setTouchStart] = useState<number | null>(null);
  const [touchEnd, setTouchEnd] = useState<number | null>(null);

  const minSwipeDistance = 50;

  const onTouchStart = (e: React.TouchEvent) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    
    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;
    
    if (isLeftSwipe && expertMode) {
      if (currentStepIndex < 7) {
        handleStepClick(currentStepIndex + 1);
      }
    }
    
    if (isRightSwipe && expertMode) {
      if (currentStepIndex > 0) {
        handleStepClick(currentStepIndex - 1);
      }
    }
    
    setTouchStart(null);
    setTouchEnd(null);
  };

  const handleCompleteStep = useCallback(() => {
    const workflow = workflowRef.current;
    workflow.markCurrentStepComplete();
    setCompletedSteps([...workflow.getState().completed]);

    if (currentStepIndex < 7) {
      workflow.nextStep();
      setCurrentStepIndex(currentStepIndex + 1);
    }
  }, [currentStepIndex]);

  const handleToggleExpertMode = useCallback(() => {
    const workflow = workflowRef.current;
    const newMode = expertMode ? 'wizard' : 'expert';
    
    if (newMode === 'expert') {
      workflow.switchToExpert();
    } else {
      workflow.switchToWizard();
    }
    setExpertMode(!expertMode);
  }, [expertMode]);

  const layerTreeData = useMemo(() => {
    if (!result) return [];
    return result.issues.map((i, idx) => ({
      index: idx,
      name: i.layer || 'unknown',
      visible: true,
      opacity: 1,
      depth: 0,
      isGroup: false,
      bounds: { width: 0, height: 0 },
      issues: [i.title],
    }));
  }, [result?.issues]);

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-[#0f0f13] text-white sm:min-h-[100vh]">
      <SEO />

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
                onClick={() => handleSetMode('qa')}
                className={`text-xs px-2 sm:px-3 py-1 sm:py-1.5 rounded-md transition-all ${mode === 'qa' ? 'bg-pink-500 text-white shadow-sm' : 'text-gray-400 hover:text-white'}`}
              >
                PSD 检测
              </button>
              <button
                onClick={() => handleSetMode('convert')}
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
            <button
              onClick={handleToggleExpertMode}
              className={`text-xs sm:text-sm px-2 sm:px-3 py-1 sm:py-1.5 rounded-lg transition-colors ${expertMode ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30' : 'text-gray-400 hover:text-white bg-gray-800 hover:bg-gray-700'}`}
            >
              🔧 {expertMode ? '专家模式' : '向导模式'}
            </button>
            <button
              onClick={handleWorkflowReset}
              className="text-xs sm:text-sm text-gray-400 hover:text-white px-2 sm:px-3 py-1 sm:py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors"
            >
              🔄 重置工作流
            </button>
            <span className="hidden sm:block text-xs text-gray-500">v2.0.0</span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-3 sm:px-4 py-4 sm:py-6">
        {error && (
          <div className="mb-3 sm:mb-4 p-4 bg-red-500/10 border border-red-500/30 rounded-xl backdrop-blur-sm">
            <div className="flex items-start gap-3">
              <div className="shrink-0 w-10 h-10 rounded-full bg-red-500/20 flex items-center justify-center">
                <span className="text-xl">❌</span>
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm text-red-400 font-semibold">分析失败</p>
                  <button 
                    onClick={() => navigator.clipboard.writeText(error)}
                    className="text-xs text-gray-500 hover:text-white px-2 py-1 rounded-lg hover:bg-gray-700/50 transition-colors"
                    title="复制错误信息"
                  >
                    📋 复制
                  </button>
                </div>
                <p className="text-xs text-red-300/80 mt-1 leading-relaxed">{error}</p>
                
                {error.includes('大小超过') && (
                  <div className="mt-3 p-3 bg-white/5 rounded-lg border border-white/10">
                    <p className="text-xs text-gray-400 mb-2 flex items-center gap-1">
                      💡 <span className="font-medium">修复建议:</span>
                    </p>
                    <ul className="text-xs text-gray-300 space-y-1.5">
                      <li>• 尝试导出为更小的 PSD 格式</li>
                      <li>• 减小画布尺寸或分辨率</li>
                      <li>• 合并不需要的图层</li>
                      <li>• 导出前清理历史记录和缓存</li>
                    </ul>
                  </div>
                )}
                
                {error.includes('不是有效的 PSD') && (
                  <div className="mt-3 p-3 bg-white/5 rounded-lg border border-white/10">
                    <p className="text-xs text-gray-400 mb-2 flex items-center gap-1">
                      💡 <span className="font-medium">修复建议:</span>
                    </p>
                    <ul className="text-xs text-gray-300 space-y-1.5">
                      <li>• 确保文件是 .psd 格式（Photoshop 源文件）</li>
                      <li>• 不要上传 .psb（大型文档格式）</li>
                      <li>• 重新导出 PSD 文件</li>
                      <li>• 检查文件是否损坏</li>
                    </ul>
                  </div>
                )}
              </div>
              <button 
                onClick={handleClearError} 
                className="shrink-0 text-gray-500 hover:text-white p-2 rounded-lg hover:bg-gray-700/50 transition-colors"
                aria-label="关闭错误提示"
              >
                ✕
              </button>
            </div>
          </div>
        )}

        <div className="mb-3 sm:mb-4">
          <div
            onTouchStart={onTouchStart}
            onTouchMove={onTouchMove}
            onTouchEnd={onTouchEnd}
          >
            <WorkflowTracker
              currentStep={currentStepIndex + 1}
              completed={completedSteps}
              mode={expertMode ? 'expert' : 'wizard'}
              onStepClick={handleStepClick}
            />
          </div>
          <div className="mt-3 flex items-center justify-center gap-3">
            <button
              onClick={handleCompleteStep}
              disabled={currentStepIndex >= 7}
              className={`min-h-[48px] min-w-[48px] px-4 py-2 rounded-lg font-medium transition-all text-sm ${
                currentStepIndex >= 7
                  ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                  : 'bg-gradient-to-r from-pink-500 to-purple-500 text-white hover:from-pink-600 hover:to-purple-600 shadow-lg shadow-pink-500/25 active:scale-95'
              }`}
            >
              ✓ 完成当前步骤
            </button>
            {expertMode && (
              <p className="text-xs text-gray-600 sm:hidden">
                左右滑动切换步骤
              </p>
            )}
          </div>
        </div>

        {view === 'upload' && loadingStage === 'idle' && mode === 'qa' && (
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
                <UploadArea 
                  onUpload={handleUpload} 
                  loadingStage={loadingStage}
                  onError={setError}
                />
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
              <ChatAssistant />
            </div>
          </div>
        )}

        {view === 'upload' && loadingStage === 'idle' && mode === 'convert' && (
          <div className="flex items-center justify-center" style={{ height: 'calc(100vh - 120px)' }}>
            <ImageToPsd />
          </div>
        )}

        {loadingStage !== 'idle' && loadingStage !== 'complete' && (
          <div className="max-w-lg mx-auto mt-8 sm:mt-16 px-2">
            <UploadArea 
              onUpload={handleUpload} 
              loadingStage={loadingStage} 
              fileInfo={fileInfo}
              onError={setError}
            />
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
                <LayerTree layers={layerTreeData} />
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
    </ErrorBoundary>
  );
};

export default Home;
