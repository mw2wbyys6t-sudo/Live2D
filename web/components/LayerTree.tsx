import React, { useState, useMemo, useCallback } from 'react';

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

const LayerItem = React.memo(function LayerItem({ layer, depth }: { layer: LayerInfo; depth: number }) {
  const hasIssues = (layer.issues?.length || 0) > 0;
  const indent = depth * 20;

  return (
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

      <span className="shrink-0 text-xs" aria-hidden="true">
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
  );
});

LayerItem.displayName = 'LayerItem';

const LayerTree = React.memo(function LayerTree({ layers, onLayerClick }: LayerTreeProps) {
  const [filter, setFilter] = useState<'all' | 'visible' | 'hidden' | 'issues'>('all');

  const filteredLayers = useMemo(() => {
    if (!layers || layers.length === 0) return [];
    switch (filter) {
      case 'visible': return layers.filter(l => l.visible);
      case 'hidden': return layers.filter(l => !l.visible);
      case 'issues': return layers.filter(l => (l.issues?.length || 0) > 0);
      default: return layers;
    }
  }, [layers, filter]);

  const counts = useMemo(() => {
    if (!layers || layers.length === 0) {
      return { all: 0, visible: 0, hidden: 0, issues: 0 };
    }
    return {
      all: layers.length,
      visible: layers.filter(l => l.visible).length,
      hidden: layers.filter(l => !l.visible).length,
      issues: layers.filter(l => (l.issues?.length || 0) > 0).length,
    };
  }, [layers]);

  const handleFilterClick = useCallback((key: typeof filter) => {
    setFilter(key);
  }, []);

  const handleLayerClick = useCallback((layer: LayerInfo) => {
    onLayerClick?.(layer);
  }, [onLayerClick]);

  if (!layers || layers.length === 0) {
    return (
      <div className="text-center py-6 sm:py-8 text-gray-500">
        <p className="text-2xl sm:text-3xl mb-2">📑</p>
        <p className="text-xs sm:text-sm">上传 PSD 文件后显示图层结构</p>
      </div>
    );
  }

  const filterButtons: { key: typeof filter; label: string }[] = [
    { key: 'all', label: '全' },
    { key: 'visible', label: '可见' },
    { key: 'hidden', label: '隐藏' },
    { key: 'issues', label: '问题' },
  ];

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-1 px-2 sm:px-3 py-1.5 sm:py-2 border-b border-gray-700/50 shrink-0">
        <span className="text-xs sm:text-sm font-medium text-gray-300 mr-2">图层</span>
        {filterButtons.map(({ key, label }) => (
          <button
            key={key}
            onClick={() => handleFilterClick(key)}
            className={`
              text-xs px-2 sm:px-2.5 py-1 rounded-full transition-colors
              ${filter === key
                ? 'bg-pink-500/20 text-pink-300'
                : 'text-gray-500 hover:text-gray-300 hover:bg-gray-700'
              }
            `}
          >
            {label}
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
            <button
              key={layer.index}
              onClick={() => handleLayerClick(layer)}
              className="w-full text-left focus-visible:ring-2 focus-visible:ring-pink-400 focus-visible:ring-inset"
              aria-label={`图层: ${layer.name}`}
            >
              <LayerItem layer={layer} depth={layer.depth} />
            </button>
          ))
        )}
      </div>

      <div className="text-xs text-gray-600 px-2 sm:px-3 py-1 sm:py-1.5 border-t border-gray-700/50 shrink-0">
        共 {layers.length} 个图层，可见 {counts.visible}，隐藏 {counts.hidden}
      </div>
    </div>
  );
});

LayerTree.displayName = 'LayerTree';

export default LayerTree;
