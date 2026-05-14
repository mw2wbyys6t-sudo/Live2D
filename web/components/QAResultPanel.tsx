import { QAIssue } from '../lib/qa-engine';

interface QAResultPanelProps {
  issues: QAIssue[];
  suggestions: string[];
  summary: {
    totalLayers: number;
    visibleLayers: number;
    hiddenLayers: number;
    groups: number;
    hasMissingCritical: boolean;
    hasNamingIssues: boolean;
    hasStructuralIssues: boolean;
  };
}

function IssueCard({ issue }: { issue: QAIssue }) {
  const severityColors = {
    error: { bg: 'bg-red-500/10', border: 'border-red-500/30', text: 'text-red-400', icon: '🔴', badge: '错误' },
    warning: { bg: 'bg-yellow-500/10', border: 'border-yellow-500/30', text: 'text-yellow-400', icon: '🟡', badge: '警告' },
    info: { bg: 'bg-blue-500/10', border: 'border-blue-500/30', text: 'text-blue-400', icon: '🔵', badge: '提示' },
  };

  const style = severityColors[issue.severity];

  return (
    <div className={`${style.bg} border ${style.border} rounded-lg p-3`}>
      <div className="flex items-start gap-2">
        <span className="shrink-0 mt-0.5">{style.icon}</span>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className={`text-xs font-medium ${style.text}`}>
              [{style.badge}]
            </span>
            <span className="text-xs text-gray-500">{issue.rule}</span>
            <span className="text-xs text-gray-600">{issue.category}</span>
          </div>
          <p className="text-sm text-gray-200 font-medium">{issue.title}</p>
          <p className="text-xs text-gray-400 mt-1">{issue.description}</p>
          {issue.layer && (
            <p className="text-xs text-pink-400 mt-1">
              图层: {issue.layer}
            </p>
          )}
          <p className="text-xs text-green-400 mt-1">
            💡 {issue.suggestion}
          </p>
        </div>
      </div>
    </div>
  );
}

export default function QAResultPanel({ issues, suggestions, summary }: QAResultPanelProps) {
  const errorCount = issues.filter(i => i.severity === 'error').length;
  const warningCount = issues.filter(i => i.severity === 'warning').length;
  const infoCount = issues.filter(i => i.severity === 'info').length;

  const categories = [...new Set(issues.map(i => i.category))];

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-3 border-b border-gray-700/50 shrink-0">
        <div className="flex items-center gap-3">
          <h3 className="text-sm font-medium text-gray-200">QA 检查结果</h3>
          <span className="text-xs text-gray-500">{issues.length} 个问题</span>
          {errorCount > 0 && (
            <span className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded-full">
              {errorCount} 错误
            </span>
          )}
          {warningCount > 0 && (
            <span className="text-xs bg-yellow-500/20 text-yellow-400 px-2 py-0.5 rounded-full">
              {warningCount} 警告
            </span>
          )}
        </div>

        <div className="flex gap-4 mt-2 text-xs text-gray-500">
          <span>📦 {summary.totalLayers} 图层</span>
          <span>👁️ {summary.visibleLayers} 可见</span>
          <span>📁 {summary.groups} 分组</span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {issues.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-4xl mb-2">✨</p>
            <p className="text-gray-400 font-medium">未发现任何问题</p>
            <p className="text-xs text-gray-500 mt-1">PSD 文件符合 Live2D 规范</p>
          </div>
        ) : (
          <>
            {categories.map(cat => (
              <div key={cat}>
                <p className="text-xs text-gray-600 font-medium uppercase tracking-wider mb-1 mt-3 first:mt-0">
                  {cat === 'naming' ? '命名规范' : cat === 'structure' ? '图层结构' : cat === 'completeness' ? '完整性' : cat === 'symmetry' ? '对称性' : cat === 'visibility' ? '可见性' : cat === 'bounds' ? '边界' : cat === 'convention' ? '规范' : cat === 'performance' ? '性能' : cat}
                </p>
                {issues.filter(i => i.category === cat).map(issue => (
                  <IssueCard key={issue.id} issue={issue} />
                ))}
              </div>
            ))}
          </>
        )}

        {suggestions.length > 0 && (
          <div className="mt-4 pt-4 border-t border-gray-700/50">
            <p className="text-xs text-gray-500 font-medium uppercase tracking-wider mb-2">
              💡 优化建议
            </p>
            <div className="space-y-1">
              {suggestions.map((s, i) => (
                <p key={i} className="text-xs text-green-400 flex items-start gap-2">
                  <span className="shrink-0 mt-0.5">→</span>
                  <span>{s}</span>
                </p>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}