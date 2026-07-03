interface RiskScoreProps {
  total: number;
  naming: number;
  structure: number;
  completeness: number;
  convention: number;
}

function ScoreRing({ value, label, size = 'md' }: { value: number; label: string; size?: 'sm' | 'md' | 'lg' }) {
  const radius = size === 'lg' ? 54 : size === 'md' ? 38 : 26;
  const strokeWidth = size === 'lg' ? 6 : size === 'md' ? 5 : 4;
  const normalizedRadius = radius - strokeWidth;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (value / 100) * circumference;

  const getColor = (v: number) => {
    if (v >= 90) return '#10b981';
    if (v >= 70) return '#f59e0b';
    if (v >= 50) return '#f97316';
    return '#ef4444';
  };

  const color = getColor(value);

  return (
    <div className="flex flex-col items-center">
      <svg width={radius * 2} height={radius * 2}>
        <circle
          stroke="#2e2e3a"
          fill="transparent"
          strokeWidth={strokeWidth}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
        <circle
          stroke={color}
          fill="transparent"
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={`${circumference} ${circumference}`}
          strokeDashoffset={strokeDashoffset}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
          transform={`rotate(-90 ${radius} ${radius})`}
          style={{ transition: 'stroke-dashoffset 0.5s ease' }}
        />
        <text
          x={radius}
          y={radius}
          textAnchor="middle"
          dominantBaseline="central"
          fill="#f1f1f3"
          fontSize={size === 'lg' ? 24 : size === 'md' ? 16 : 12}
          fontWeight="bold"
        >
          {value}
        </text>
      </svg>
      <span className={`${size === 'lg' ? 'text-sm' : 'text-xs'} text-gray-400 mt-1`}>{label}</span>
    </div>
  );
}

export default function RiskScore({ total, naming, structure, completeness, convention }: RiskScoreProps) {
  const getLevel = (score: number) => {
    if (score >= 90) return { label: '优秀', color: '#10b981', icon: '🟢' };
    if (score >= 70) return { label: '良好', color: '#f59e0b', icon: '🟡' };
    if (score >= 50) return { label: '需改进', color: '#f97316', icon: '🟠' };
    return { label: '差', color: '#ef4444', icon: '🔴' };
  };

  const level = getLevel(total);

  return (
    <div className="flex flex-col items-center">
      <ScoreRing value={total} label="" size="lg" />

      <div className="flex items-center gap-2 mt-2">
        <span className="text-lg">{level.icon}</span>
        <span className="text-lg font-bold" style={{ color: level.color }}>
          {total} 分
        </span>
        <span className="text-sm text-gray-400">{level.label}</span>
      </div>

      <div className="grid grid-cols-2 gap-3 mt-4 w-full max-w-[200px]">
        <ScoreRing value={naming} label="命名" size="sm" />
        <ScoreRing value={structure} label="结构" size="sm" />
        <ScoreRing value={completeness} label="完整性" size="sm" />
        <ScoreRing value={convention} label="规范" size="sm" />
      </div>
    </div>
  );
}