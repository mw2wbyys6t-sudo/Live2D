export interface QAIssueType {
  id: string;
  severity: 'error' | 'warning' | 'info';
  category: string;
  title: string;
  description: string;
  layer?: string;
  suggestion: string;
  rule: string;
  expected?: string;
  actual?: string;
}

interface LayerStats {
  total: number;
  visible: number;
  hidden: number;
  groups: number;
  empty: number;
  semiTransparent: number;
  nonNormalBlend: number;
  offscreen: number;
  duplicateNames: number;
}

interface Summary {
  totalLayers: number;
  visibleLayers: number;
  hiddenLayers: number;
  groups: number;
  hasMissingCritical: boolean;
  hasNamingIssues: boolean;
  hasStructuralIssues: boolean;
}

interface QAResultProps {
  score: number;
  issues: QAIssueType[];
  warnings: QAIssueType[];
  suggestions: string[];
  layer_stats: LayerStats;
  summary: Summary;
}

const severityConfig = {
  error: {
    bg: 'bg-red-500/10',
    border: 'border-red-500/30',
    text: 'text-red-400',
    bgBadge: 'bg-red-500/20',
    icon: '🔴',
    label: '严重',
    colorClass: 'border-red-500/50',
  },
  warning: {
    bg: 'bg-yellow-500/10',
    border: 'border-yellow-500/30',
    text: 'text-yellow-400',
    bgBadge: 'bg-yellow-500/20',
    icon: '🟡',
    label: '警告',
    colorClass: 'border-yellow-500/50',
  },
  info: {
    bg: 'bg-blue-500/10',
    border: 'border-blue-500/30',
    text: 'text-blue-400',
    bgBadge: 'bg-blue-500/20',
    icon: '💡',
    label: '建议',
    colorClass: 'border-blue-500/50',
  },
};

const categoryLabels: Record<string, string> = {
  naming: '命名规范',
  structure: '图层结构',
  completeness: '完整性',
  symmetry: '对称性',
  visibility: '可见性',
  bounds: '边界',
  convention: '规范',
  performance: '性能',
};

function IssueCard({ issue }: { issue: QAIssueType }) {
  const config = severityConfig[issue.severity];

  return (
    <div className={`${config.bg} border ${config.border} rounded-lg p-4 transition-all hover:scale-[1.01]`}>
      <div className="flex items-start gap-3">
        <span className="shrink-0 text-lg">{config.icon}</span>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2">
            <span className={`text-xs font-semibold px-2 py-0.5 rounded ${config.bgBadge} ${config.text}`}>
              {config.label}
            </span>
            <span className="text-xs font-mono text-gray-500">{issue.rule}</span>
            <span className="text-xs text-gray-600 capitalize">
              {categoryLabels[issue.category] || issue.category}
            </span>
          </div>
          
          <p className="text-sm font-medium text-gray-100 mb-1">{issue.title}</p>
          <p className="text-xs text-gray-400 mb-2">{issue.description}</p>

          {issue.expected && issue.actual && (
            <div className="flex gap-4 text-xs mb-2">
              <span className="text-green-400">
                期望: <span className="text-gray-300">{issue.expected}</span>
              </span>
              <span className="text-red-400">
                实际: <span className="text-gray-300">{issue.actual}</span>
              </span>
            </div>
          )}

          {issue.layer && (
            <p className="text-xs text-pink-400 mb-2">
              📎 图层: {issue.layer}
            </p>
          )}

          <div className={`border-l-2 ${config.border} pl-3 mt-2`}>
            <p className="text-xs text-green-400">
              💡 {issue.suggestion}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function WarningCard({ warning }: { warning: QAIssueType }) {
  const config = severityConfig[warning.severity];

  return (
    <div className={`${config.bg} border ${config.border} rounded-md p-3`}>
      <div className="flex items-start gap-2">
        <span className="shrink-0">{config.icon}</span>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className={`text-xs font-medium ${config.text}`}>
              {config.label}
            </span>
            <span className="text-xs text-gray-500">{warning.rule}</span>
          </div>
          <p className="text-xs text-gray-300">{warning.title}</p>
          <p className="text-xs text-gray-500 mt-1">{warning.description}</p>
          <p className="text-xs text-green-500/80 mt-1">
            💡 {warning.suggestion}
          </p>
        </div>
      </div>
    </div>
  );
}

function ScoreRing({ score }: { score: number }) {
  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const getScoreColor = () => {
    if (score >= 90) return { stroke: '#22c55e', text: 'text-green-400', label: '优秀' };
    if (score >= 70) return { stroke: '#eab308', text: 'text-yellow-400', label: '良好' };
    if (score >= 50) return { stroke: '#f97316', text: 'text-orange-400', label: '一般' };
    return { stroke: '#ef4444', text: 'text-red-400', label: '需改进' };
  };

  const colors = getScoreColor();

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-28 h-28">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-gray-700"
          />
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke={colors.stroke}
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-3xl font-bold ${colors.text}`}>{score}</span>
          <span className={`text-xs ${colors.text}`}>{colors.label}</span>
        </div>
      </div>
      <p className="text-sm text-gray-400 mt-2">风险评分</p>
    </div>
  );
}

function LayerStatsPanel({ stats }: { stats: LayerStats }) {
  const statItems = [
    { label: '总图层', value: stats.total, icon: '📦', color: 'text-gray-300' },
    { label: '可见', value: stats.visible, icon: '👁️', color: 'text-green-400' },
    { label: '隐藏', value: stats.hidden, icon: '👻', color: 'text-gray-500' },
    { label: '分组', value: stats.groups, icon: '📁', color: 'text-blue-400' },
  ];

  const issueItems = [
    { label: '空图层', value: stats.empty, icon: '⬜', severity: stats.empty > 0 ? 'warning' : 'ok' },
    { label: '半透明', value: stats.semiTransparent, icon: '🌫️', severity: stats.semiTransparent > 0 ? 'warning' : 'ok' },
    { label: '异常混合', value: stats.nonNormalBlend, icon: '🎨', severity: stats.nonNormalBlend > 0 ? 'error' : 'ok' },
    { label: '画布外', value: stats.offscreen, icon: '📍', severity: stats.offscreen > 0 ? 'warning' : 'ok' },
    { label: '重名', value: stats.duplicateNames, icon: '📋', severity: stats.duplicateNames > 0 ? 'error' : 'ok' },
  ];

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-2">
        {statItems.map((item) => (
          <div key={item.label} className="bg-gray-800/50 rounded-lg p-2 flex items-center gap-2">
            <span className="text-sm">{item.icon}</span>
            <div>
              <p className={`text-sm font-medium ${item.color}`}>{item.value}</p>
              <p className="text-xs text-gray-500">{item.label}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="border-t border-gray-700/50 pt-3">
        <p className="text-xs text-gray-500 font-medium mb-2">图层问题统计</p>
        <div className="space-y-1">
          {issueItems.map((item) => (
            <div key={item.label} className="flex items-center justify-between text-xs">
              <span className="text-gray-400">
                {item.icon} {item.label}
              </span>
              <span className={
                item.severity === 'error' ? 'text-red-400' :
                item.severity === 'warning' ? 'text-yellow-400' :
                'text-green-400'
              }>
                {item.value > 0 ? `${item.value} 个` : '✓ 无'}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function QAResult({
  score,
  issues,
  warnings,
  suggestions,
  layer_stats,
  summary
}: QAResultProps) {
  const errorCount = issues.length;
  const warningCount = warnings.length;
  const infoCount = suggestions.length;

  const errorCategories = [...new Set(issues.map(i => i.category))];
  const warningCategories = [...new Set(warnings.map(w => w.category))];

  const hasCritical = summary.hasMissingCritical;
  const hasNaming = summary.hasNamingIssues;
  const hasStructure = summary.hasStructuralIssues;

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-3 border-b border-gray-700/50 shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <h3 className="text-sm font-medium text-gray-200">QA 检查结果</h3>
            <div className="flex gap-2">
              {errorCount > 0 && (
                <span className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded-full border border-red-500/30">
                  🔴 {errorCount} 严重
                </span>
              )}
              {warningCount > 0 && (
                <span className="text-xs bg-yellow-500/20 text-yellow-400 px-2 py-0.5 rounded-full border border-yellow-500/30">
                  🟡 {warningCount} 警告
                </span>
              )}
              {infoCount > 0 && (
                <span className="text-xs bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded-full border border-blue-500/30">
                  💡 {infoCount} 建议
                </span>
              )}
            </div>
          </div>
          <ScoreRing score={score} />
        </div>

        <div className="flex gap-4 mt-3 text-xs">
          <span>📦 {summary.totalLayers} 图层</span>
          <span>👁️ {summary.visibleLayers} 可见</span>
          <span>📁 {summary.groups} 分组</span>
        </div>

        {(hasCritical || hasNaming || hasStructure) && (
          <div className="flex gap-2 mt-2">
            {hasCritical && (
              <span className="text-xs bg-red-500/10 text-red-400 px-2 py-0.5 rounded border border-red-500/20">
                ⚠️ 缺少关键图层
              </span>
            )}
            {hasNaming && (
              <span className="text-xs bg-yellow-500/10 text-yellow-400 px-2 py-0.5 rounded border border-yellow-500/20">
                📝 命名问题
              </span>
            )}
            {hasStructure && (
              <span className="text-xs bg-orange-500/10 text-orange-400 px-2 py-0.5 rounded border border-orange-500/20">
                🔧 结构问题
              </span>
            )}
          </div>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {errorCategories.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="w-2 h-2 rounded-full bg-red-500"></span>
              <p className="text-xs text-red-400 font-semibold uppercase tracking-wider">
                严重问题
              </p>
            </div>
            <div className="space-y-2">
              {errorCategories.map(cat => (
                <div key={cat}>
                  <p className="text-xs text-gray-500 font-medium mb-1 ml-4">
                    {categoryLabels[cat] || cat}
                  </p>
                  {issues.filter(i => i.category === cat).map(issue => (
                    <IssueCard key={issue.id} issue={issue} />
                  ))}
                </div>
              ))}
            </div>
          </div>
        )}

        {warningCategories.length > 0 && (
          <div className="border-t border-gray-700/30 pt-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="w-2 h-2 rounded-full bg-yellow-500"></span>
              <p className="text-xs text-yellow-400 font-semibold uppercase tracking-wider">
                警告
              </p>
            </div>
            <div className="space-y-2">
              {warningCategories.map(cat => (
                <div key={cat}>
                  <p className="text-xs text-gray-500 font-medium mb-1 ml-4">
                    {categoryLabels[cat] || cat}
                  </p>
                  {warnings.filter(w => w.category === cat).map(warning => (
                    <WarningCard key={warning.id} warning={warning} />
                  ))}
                </div>
              ))}
            </div>
          </div>
        )}

        {issues.length === 0 && warnings.length === 0 && (
          <div className="text-center py-12">
            <p className="text-5xl mb-3">✨</p>
            <p className="text-lg font-medium text-green-400">完美！</p>
            <p className="text-sm text-gray-400 mt-1">PSD 文件完全符合 Live2D 规范</p>
          </div>
        )}

        <div className="border-t border-gray-700/30 pt-4">
          <LayerStatsPanel stats={layer_stats} />
        </div>

        {suggestions.length > 0 && (
          <div className="border-t border-gray-700/30 pt-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="w-2 h-2 rounded-full bg-blue-500"></span>
              <p className="text-xs text-blue-400 font-semibold uppercase tracking-wider">
                优化建议
              </p>
            </div>
            <div className="space-y-2">
              {suggestions.map((s, i) => (
                <div key={i} className="bg-blue-500/5 border border-blue-500/20 rounded-lg p-3">
                  <p className="text-xs text-blue-300 flex items-start gap-2">
                    <span className="shrink-0 mt-0.5">💡</span>
                    <span>{s}</span>
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
