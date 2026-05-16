import { useState } from 'react';

interface LayerInfo {
  index: number;
  name: string;
  visible: boolean;
  opacity: number;
  depth: number;
  isGroup: boolean;
  bounds: { width: number; height: number };
  issues?: string[];
}

interface LayerTreeProps {
  layers: LayerInfo[];
  onLayerClick?: (layer: LayerInfo) => void;
}

function LayerItem({ layer, depth }: { layer: LayerInfo; depth: number }) {
  const [expanded, setExpanded] = useState(true);

  const hasIssues = (layer.issues?.length || 0) > 0;
  const indent = depth * 20;

  return (
    <div>
      <div
        className={`
          flex items-center gap-2 px-3 py-1.5 text-sm rounded cursor-pointer
          transition-colors duration-100
          ${layer.visible ? 'text-gray-200 hover:bg-gray-700/50' : 'text-gray-500 hover:bg-gray-700/30'}
          ${hasIssues ? 'bg-yellow-500/5 border-l-2 border-yellow-500' : ''}
        `}
        style={{ paddingLeft: `${12 + indent}px` }}
      >
        <span className="text-xs text-gray-600 w-6 shrink-0">{layer.index + 1}</span>

        <span className="shrink-0 text-xs">
          {layer.isGroup ? '📁' : layer.visible ? '👁️' : '👁️‍🗨️'}
        </span>

        <span className={`truncate flex-1 ${layer.isGroup ? 'font-medium text-pink-300' : ''}`}>
          {layer.name}
        </span>

        {hasIssues && (
          <span className="shrink-0 w-2 h-2 rounded-full bg-yellow-500" title={layer.issues?.join(', ')} />
        )}

        <span className="text-xs text-gray-600 shrink-0">
          {layer.bounds.width}x{layer.bounds.height}
        </span>

        {layer.opacity < 1 && (
          <span className="text-xs text-gray-600 shrink-0">
            {Math.round(layer.opacity * 100)}%
          </span>
        )}
      </div>
    </div>
  );
}

export default function LayerTree({ layers, onLayerClick }: LayerTreeProps) {
  const [filter, setFilter] = useState<'all' | 'visible' | 'hidden' | 'issues'>('all');

  if (!layers || layers.length === 0) {
    return (
      <div className="text-center py-6 sm:py-8 text-gray-500">
        <p className="text-2xl sm:text-3xl mb-2">📑</p>
        <p className="text-xs sm:text-sm">上传 PSD 文件后显示图层结构</p>
      </div>
    );
  }

  const filteredLayers = layers.filter(l => {
    switch (filter) {
      case 'visible': return l.visible;
      case 'hidden': return !l.visible;
      case 'issues': return (l.issues?.length || 0) > 0;
      default: return true;
    }
  });

  const counts = {
    all: layers.length,
    visible: layers.filter(l => l.visible).length,
    hidden: layers.filter(l => !l.visible).length,
    issues: layers.filter(l => (l.issues?.length || 0) > 0).length,
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-1 px-2 sm:px-3 py-1.5 sm:py-2 border-b border-gray-700/50 shrink-0">
        <span className="text-xs sm:text-sm font-medium text-gray-300 mr-2">图层</span>
        {(['all', 'visible', 'hidden', 'issues'] as const).map(key => (
          <button
            key={key}
            onClick={() => setFilter(key)}
            className={`
              text-xs px-2 sm:px-2.5 py-1 rounded-full transition-colors
              ${filter === key
                ? 'bg-pink-500/20 text-pink-300'
                : 'text-gray-500 hover:text-gray-300 hover:bg-gray-700'
              }
            `}
          >
            {key === 'all' ? '全' : key === 'visible' ? '可见' : key === 'hidden' ? '隐藏' : '问题'}
            <span className="ml-0.5 sm:ml-1 text-xs opacity-60">
              {counts[key]}
            </span>
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-y-auto">
        {filteredLayers.length === 0 ? (
          <div className="text-center py-6 sm:py-8 text-gray-500 text-xs sm:text-sm">
            没有匹配的图层
          </div>
        ) : (
          filteredLayers.map(layer => (
            <div key={layer.index} onClick={() => onLayerClick?.(layer)}>
              <LayerItem layer={layer} depth={layer.depth} />
            </div>
          ))
        )}
      </div>

      <div className="text-xs text-gray-600 px-2 sm:px-3 py-1 sm:py-1.5 border-t border-gray-700/50 shrink-0">
        共 {layers.length} 个图层，可见 {counts.visible}，隐藏 {counts.hidden}
      </div>
    </div>
  );
}