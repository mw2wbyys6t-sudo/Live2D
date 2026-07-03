import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { QAIssue, LayerStats } from '../lib/qa-engine';

const ErrorIcon = React.memo(() => (
  <svg className="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
  </svg>
));
ErrorIcon.displayName = 'ErrorIcon';

const WarningIcon = React.memo(() => (
  <svg className="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
  </svg>
));
WarningIcon.displayName = 'WarningIcon';

const InfoIcon = React.memo(() => (
  <svg className="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
  </svg>
));
InfoIcon.displayName = 'InfoIcon';

const ChevronDownIcon = React.memo(() => (
  <svg className="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
    <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
  </svg>
));
ChevronDownIcon.displayName = 'ChevronDownIcon';

const CopyIcon = React.memo(() => (
  <svg className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
    <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
    <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
  </svg>
));
CopyIcon.displayName = 'CopyIcon';

interface QAResultProps {
  score: number;
  issues: QAIssue[];
  warnings: QAIssue[];
  suggestions: string[];
  layer_stats?: LayerStats;
  summary?: {
    totalLayers: number;
    visibleLayers: number;
    hiddenLayers: number;
    groups: number;
    hasMissingCritical: boolean;
    hasNamingIssues: boolean;
    hasStructuralIssues: boolean;
  };
}

const getScoreColor = (s: number): string => {
  if (s >= 80) return 'text-emerald-400';
  if (s >= 60) return 'text-yellow-400';
  return 'text-red-400';
};

const getScoreBg = (s: number): string => {
  if (s >= 80) return 'from-emerald-500/20 to-emerald-600/10';
  if (s >= 60) return 'from-yellow-500/20 to-yellow-600/10';
  return 'from-red-500/20 to-red-600/10';
};

const getSeverityColor = (severity: string): string => {
  switch (severity) {
    case 'error': return 'text-red-400 bg-red-500/10 border-red-500/20';
    case 'warning': return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20';
    default: return 'text-blue-400 bg-blue-500/10 border-blue-500/20';
  }
};

const getSeverityIcon = (severity: string): React.ReactNode => {
  switch (severity) {
    case 'error': return <ErrorIcon />;
    case 'warning': return <WarningIcon />;
    default: return <InfoIcon />;
  }
};

const QAResult = React.memo(function QAResult({
  score,
  issues,
  warnings,
  suggestions,
  layer_stats,
}: QAResultProps) {
  const [expandedIssues, setExpandedIssues] = useState<Set<string>>(new Set());
  const [expandedWarnings, setExpandedWarnings] = useState<Set<string>>(new Set());
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    setExpandedIssues(new Set(issues.slice(0, 3).map(i => i.id)));
    setExpandedWarnings(new Set(warnings.slice(0, 2).map(w => w.id)));
  }, [issues, warnings]);

  const toggleIssue = useCallback((id: string) => {
    setExpandedIssues(prev => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  }, []);

  const toggleWarning = useCallback((id: string) => {
    setExpandedWarnings(prev => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  }, []);

  const handleCopy = useCallback(async () => {
    const text = JSON.stringify({ score, issues, warnings, suggestions }, null, 2);
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      const textarea = document.createElement('textarea');
      textarea.textContent = text;
      textarea.setAttribute('readonly', '');
      textarea.style.cssText = 'position:fixed;opacity:0;pointer-events:none;';
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand('copy');
      } finally {
        document.body.removeChild(textarea);
      }
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }, [score, issues, warnings, suggestions]);

  const scoreColor = useMemo(() => getScoreColor(score), [score]);
  const scoreBg = useMemo(() => getScoreBg(score), [score]);

  const hasAnyContent = issues.length > 0 || warnings.length > 0 || suggestions.length > 0;

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <div className="shrink-0 p-3 sm:p-4 md:p-6 border-b border-gray-800/50 bg-gradient-to-r from-gray-900/50 to-transparent">
        <div className="flex items-center justify-between gap-2">
          <div className="min-w-0">
            <h2 className="text-base sm:text-lg font-semibold text-white mb-1">质量检测报告</h2>
            <p className="text-xs sm:text-sm text-gray-500">基于 23 项 QA 规则的分析结果</p>
          </div>
          <button
            onClick={handleCopy}
            aria-label={copied ? '已复制报告' : '复制报告'}
            className={`
              flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-1.5 sm:py-2 rounded-lg sm:rounded-xl text-xs sm:text-sm font-medium
              transition-colors duration-300 shrink-0
              ${copied
                ? 'bg-emerald-500/20 text-emerald-400'
                : 'bg-gray-800/50 text-gray-400 hover:text-white hover:bg-gray-800'
              }
            `}
          >
            {copied ? (
              <>
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="hidden sm:inline">已复制</span>
              </>
            ) : (
              <>
                <CopyIcon />
                <span className="hidden sm:inline">复制报告</span>
              </>
            )}
          </button>
        </div>

        <div className="mt-4 sm:mt-6 flex flex-col sm:flex-row items-start sm:items-end gap-3 sm:gap-4">
          <div className={`
            relative px-4 sm:px-6 py-3 sm:py-4 rounded-xl sm:rounded-2xl
            bg-gradient-to-br ${scoreBg}
            border border-white/5
            backdrop-blur-xl flex items-center gap-4
          `}>
            <div className="relative flex-shrink-0">
              <svg className="w-20 h-20 sm:w-24 sm:h-24 transform -rotate-90">
                <circle
                  cx="40"
                  cy="40"
                  r="36"
                  stroke="#374151"
                  strokeWidth="4"
                  fill="none"
                />
                <circle
                  cx="40"
                  cy="40"
                  r="36"
                  stroke={score >= 80 ? '#34d399' : score >= 60 ? '#fbbf24' : '#f87171'}
                  strokeWidth="4"
                  fill="none"
                  strokeLinecap="round"
                  strokeDasharray={`${(score / 100) * 226.2} 226.2`}
                  className="transition-all duration-1000 ease-out"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <p className={`text-2xl sm:text-3xl font-bold ${scoreColor}`}>{score}</p>
                <p className="text-xs text-gray-500">分</p>
              </div>
            </div>
            
            <div className="flex-1 min-w-0">
              <p className="text-sm sm:text-base font-semibold text-white mb-1">
                {score >= 80 ? '✅ 优秀' : score >= 60 ? '⚠️ 良好' : '❌ 需改进'}
              </p>
              <p className="text-xs text-gray-500">
                {score >= 80 
                  ? '这是一个高质量的 PSD 文件！' 
                  : score >= 60 
                    ? '有小幅改进空间，请关注以下问题' 
                    : '需要重点修复几个关键问题'}
              </p>
              {layer_stats && (
                <div className="mt-2 text-xs text-gray-400">
                  共 {layer_stats.total} 个图层 · {layer_stats.groups} 个组
                </div>
              )}
            </div>
          </div>

          <div className="flex-1 grid grid-cols-3 gap-2 sm:gap-3 w-full">
            <div className="bg-red-500/10 border border-red-500/20 rounded-lg sm:rounded-xl p-2 sm:p-3 text-center">
              <p className="text-xl sm:text-2xl font-bold text-red-400">{issues.length}</p>
              <p className="text-xs text-gray-500">严重问题</p>
              {issues.length > 0 && (
                <div className="mt-1 w-full h-1 bg-red-500/30 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-red-500 rounded-full"
                    style={{ width: `${Math.min((issues.length / Math.max(issues.length + warnings.length + suggestions.length, 1)) * 100, 100)}%` }}
                  />
                </div>
              )}
            </div>
            <div className="bg-yellow-500/10 border border-yellow-500/20 rounded-lg sm:rounded-xl p-2 sm:p-3 text-center">
              <p className="text-xl sm:text-2xl font-bold text-yellow-400">{warnings.length}</p>
              <p className="text-xs text-gray-500">警告</p>
              {warnings.length > 0 && (
                <div className="mt-1 w-full h-1 bg-yellow-500/30 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-yellow-500 rounded-full"
                    style={{ width: `${Math.min((warnings.length / Math.max(issues.length + warnings.length + suggestions.length, 1)) * 100, 100)}%` }}
                  />
                </div>
              )}
            </div>
            <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg sm:rounded-xl p-2 sm:p-3 text-center">
              <p className="text-xl sm:text-2xl font-bold text-blue-400">{suggestions.length}</p>
              <p className="text-xs text-gray-500">优化建议</p>
              {suggestions.length > 0 && (
                <div className="mt-1 w-full h-1 bg-blue-500/30 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-blue-500 rounded-full"
                    style={{ width: `${Math.min((suggestions.length / Math.max(issues.length + warnings.length + suggestions.length, 1)) * 100, 100)}%` }}
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-3 sm:p-4 md:p-6 space-y-4 sm:space-y-6">
        {issues.length > 0 && (
          <div className="space-y-2 sm:space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-1 h-5 sm:h-6 bg-gradient-to-b from-red-500 to-red-600 rounded-full" />
              <h3 className="text-xs sm:text-sm font-semibold text-white uppercase tracking-wider">
                严重问题 ({issues.length})
              </h3>
            </div>
            <div className="space-y-2">
              {issues.map((issue, idx) => (
                <div
                  key={issue.id}
                  className={`
                    rounded-lg sm:rounded-xl border overflow-hidden
                    transition-all duration-300
                    ${getSeverityColor(issue.severity)}
                    hover:shadow-lg hover:shadow-red-500/5
                  `}
                  style={{ animationDelay: `${idx * 50}ms` }}
                >
                  <button
                    onClick={() => toggleIssue(issue.id)}
                    className="w-full px-3 sm:px-4 py-2.5 sm:py-3 flex items-center justify-between hover:bg-white/5 transition-colors"
                  >
                    <div className="flex items-center gap-2 sm:gap-3">
                      <div className={`${issue.severity === 'error' ? 'text-red-400' : 'text-yellow-400'}`}>
                        {getSeverityIcon(issue.severity)}
                      </div>
                      <div className="text-left min-w-0 flex-1">
                        <p className="font-medium text-white text-xs sm:text-sm truncate">{issue.title}</p>
                        {issue.layer && (
                          <p className="text-xs text-gray-500 mt-0.5 truncate">{issue.layer}</p>
                        )}
                      </div>
                    </div>
                    <div className={`transition-transform duration-200 ${expandedIssues.has(issue.id) ? 'rotate-180' : ''}`}>
                      <ChevronDownIcon />
                    </div>
                  </button>
                  
                  <div className={`
                    overflow-hidden transition-all duration-300
                    ${expandedIssues.has(issue.id) ? 'max-h-[500px] opacity-100' : 'max-h-0 opacity-0'}
                  `}>
                    <div className="px-3 sm:px-4 pb-3 sm:pb-4 pt-2 border-t border-white/5">
                      <p className="text-xs sm:text-sm text-gray-400 mb-2 sm:mb-3">{issue.description}</p>
                      
                      {issue.expected && issue.actual && (
                        <div className="grid grid-cols-2 gap-2 sm:gap-3 mb-2 sm:mb-3">
                          <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-2 sm:p-3">
                            <p className="text-xs text-emerald-400 mb-1">预期</p>
                            <p className="text-xs sm:text-sm text-white truncate">{issue.expected}</p>
                          </div>
                          <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-2 sm:p-3">
                            <p className="text-xs text-red-400 mb-1">实际</p>
                            <p className="text-xs sm:text-sm text-white truncate">{issue.actual}</p>
                          </div>
                        </div>
                      )}
                      
                      {issue.suggestion && (
                        <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-2 sm:p-3">
                          <p className="text-xs text-blue-400 mb-1">修复建议</p>
                          <p className="text-xs sm:text-sm text-gray-300">{issue.suggestion}</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {warnings.length > 0 && (
          <div className="space-y-2 sm:space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-1 h-5 sm:h-6 bg-gradient-to-b from-yellow-500 to-yellow-600 rounded-full" />
              <h3 className="text-xs sm:text-sm font-semibold text-white uppercase tracking-wider">
                警告 ({warnings.length})
              </h3>
            </div>
            <div className="space-y-2">
              {warnings.map((warning, idx) => (
                <div
                  key={warning.id}
                  className={`
                    rounded-lg sm:rounded-xl border overflow-hidden
                    transition-all duration-300
                    ${getSeverityColor(warning.severity)}
                    hover:shadow-lg hover:shadow-yellow-500/5
                  `}
                  style={{ animationDelay: `${idx * 50}ms` }}
                >
                  <button
                    onClick={() => toggleWarning(warning.id)}
                    className="w-full px-3 sm:px-4 py-2.5 sm:py-3 flex items-center justify-between hover:bg-white/5 transition-colors"
                  >
                    <div className="flex items-center gap-2 sm:gap-3">
                      <div className="text-yellow-400">
                        {getSeverityIcon(warning.severity)}
                      </div>
                      <div className="text-left min-w-0 flex-1">
                        <p className="font-medium text-white text-xs sm:text-sm truncate">{warning.title}</p>
                        {warning.layer && (
                          <p className="text-xs text-gray-500 mt-0.5 truncate">{warning.layer}</p>
                        )}
                      </div>
                    </div>
                    <div className={`transition-transform duration-200 ${expandedWarnings.has(warning.id) ? 'rotate-180' : ''}`}>
                      <ChevronDownIcon />
                    </div>
                  </button>
                  
                  <div className={`
                    overflow-hidden transition-all duration-300
                    ${expandedWarnings.has(warning.id) ? 'max-h-[500px] opacity-100' : 'max-h-0 opacity-0'}
                  `}>
                    <div className="px-3 sm:px-4 pb-3 sm:pb-4 pt-2 border-t border-white/5">
                      <p className="text-xs sm:text-sm text-gray-400 mb-2 sm:mb-3">{warning.description}</p>
                      
                      {warning.suggestion && (
                        <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-2 sm:p-3">
                          <p className="text-xs text-blue-400 mb-1">建议</p>
                          <p className="text-xs sm:text-sm text-gray-300">{warning.suggestion}</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {suggestions.length > 0 && (
          <div className="space-y-2 sm:space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-1 h-5 sm:h-6 bg-gradient-to-b from-blue-500 to-blue-600 rounded-full" />
              <h3 className="text-xs sm:text-sm font-semibold text-white uppercase tracking-wider">
                优化建议 ({suggestions.length})
              </h3>
            </div>
            <div className="space-y-2">
              {suggestions.map((suggestion, idx) => (
                <div
                  key={idx}
                  className="bg-blue-500/5 border border-blue-500/20 rounded-lg sm:rounded-xl p-3 sm:p-4 hover:bg-blue-500/10 transition-colors"
                  style={{ animationDelay: `${idx * 50}ms` }}
                >
                  <div className="flex items-start gap-2 sm:gap-3">
                    <div className="text-blue-400 mt-0.5 shrink-0">
                      <InfoIcon />
                    </div>
                    <p className="text-xs sm:text-sm text-gray-300">{suggestion}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {!hasAnyContent && (
          <div className="flex flex-col items-center justify-center py-10 sm:py-16 text-center">
            <div className="w-16 h-16 sm:w-20 sm:h-20 mb-4 sm:mb-6 rounded-full bg-gradient-to-br from-emerald-500/20 to-emerald-600/10 flex items-center justify-center">
              <svg className="w-8 h-8 sm:w-10 sm:h-10 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-lg sm:text-xl font-semibold text-white mb-2">完美！</h3>
            <p className="text-gray-500 text-xs sm:text-sm max-w-md px-2">
              您的 PSD 文件通过了所有 QA 检查，没有发现问题。这是一个高质量的 Live2D 模型源文件。
            </p>
          </div>
        )}
      </div>

      {layer_stats && (
        <div className="shrink-0 p-4 border-t border-gray-800/50 bg-gray-900/30">
          <div className="grid grid-cols-4 gap-3 text-center">
            <div>
              <p className="text-lg font-semibold text-white">{layer_stats.total || 0}</p>
              <p className="text-xs text-gray-500">总图层</p>
            </div>
            <div>
              <p className="text-lg font-semibold text-emerald-400">{layer_stats.visible || 0}</p>
              <p className="text-xs text-gray-500">可见</p>
            </div>
            <div>
              <p className="text-lg font-semibold text-purple-400">{layer_stats.groups || 0}</p>
              <p className="text-xs text-gray-500">分组</p>
            </div>
            <div>
              <p className="text-lg font-semibold text-pink-400">{issues.length}</p>
              <p className="text-xs text-gray-500">问题</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
});

QAResult.displayName = 'QAResult';

export default QAResult;
