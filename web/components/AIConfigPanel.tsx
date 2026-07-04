import { useState, useCallback } from 'react';
import { AIConfig, getAIConfig, saveAIConfig } from '../lib/ai-service';

interface AIConfigPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

const PROVIDER_OPTIONS = [
  { value: 'none', label: '使用本地规则（默认）', desc: '不调用外部 API，使用内置规则回答' },
  { value: 'openai', label: 'OpenAI', desc: 'GPT-3.5 / GPT-4 系列模型' },
  { value: 'anthropic', label: 'Anthropic', desc: 'Claude 系列模型' },
  { value: 'custom', label: '自定义 API', desc: '兼容 OpenAI 格式的自定义接口' },
] as const;

const MODEL_SUGGESTIONS: Record<string, string[]> = {
  openai: ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo'],
  anthropic: ['claude-3-haiku-20240307', 'claude-3-sonnet-20240229', 'claude-3-opus-20240229'],
  custom: [''],
};

export default function AIConfigPanel({ isOpen, onClose }: AIConfigPanelProps) {
  const [config, setConfig] = useState<AIConfig>(getAIConfig);
  const [showKey, setShowKey] = useState(false);
  const [testStatus, setTestStatus] = useState<'idle' | 'testing' | 'success' | 'error'>('idle');
  const [testMessage, setTestMessage] = useState('');

  const handleSave = useCallback(() => {
    saveAIConfig(config);
    onClose();
  }, [config, onClose]);

  const handleTest = useCallback(async () => {
    if (!config.enabled || !config.apiKey) {
      setTestStatus('error');
      setTestMessage('请先启用并填写 API Key');
      return;
    }

    setTestStatus('testing');
    setTestMessage('正在测试连接...');

    try {
      const { callAIAPI } = await import('../lib/ai-service');
      const response = await callAIAPI(
        [
          { role: 'system', content: '你是一个测试助手，请回复"连接成功"' },
          { role: 'user', content: '测试连接' },
        ],
        config
      );

      if (response.error) {
        setTestStatus('error');
        setTestMessage(response.error);
      } else {
        setTestStatus('success');
        setTestMessage('连接成功！API 配置正确');
      }
    } catch {
      setTestStatus('error');
      setTestMessage('测试失败，请检查网络连接');
    }
  }, [config]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="relative w-full max-w-md bg-gray-900 border border-gray-700 rounded-2xl shadow-2xl overflow-hidden animate-scale-in">
        <div className="p-5 border-b border-gray-800">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white">AI API 配置</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-800"
              aria-label="关闭"
            >
              ✕
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-1">配置外部 AI API 以获得更智能的回答</p>
        </div>

        <div className="p-5 space-y-4 max-h-[60vh] overflow-y-auto">
          {/* 启用开关 */}
          <div className="flex items-center justify-between p-3 bg-gray-800/50 rounded-xl">
            <div>
              <p className="text-sm font-medium text-white">启用 AI API</p>
              <p className="text-xs text-gray-500">开启后将调用外部 AI 服务</p>
            </div>
            <button
              onClick={() => setConfig(prev => ({ ...prev, enabled: !prev.enabled }))}
              className={`relative w-12 h-6 rounded-full transition-colors ${
                config.enabled ? 'bg-pink-500' : 'bg-gray-700'
              }`}
              aria-label={config.enabled ? '禁用 AI API' : '启用 AI API'}
            >
              <span
                className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${
                  config.enabled ? 'translate-x-7' : 'translate-x-1'
                }`}
              />
            </button>
          </div>

          {/* 提供商选择 */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">AI 提供商</label>
            <div className="space-y-2">
              {PROVIDER_OPTIONS.map(option => (
                <button
                  key={option.value}
                  onClick={() =>
                    setConfig(prev => ({
                      ...prev,
                      provider: option.value as AIConfig['provider'],
                      model: MODEL_SUGGESTIONS[option.value]?.[0] || '',
                    }))
                  }
                  className={`w-full text-left p-3 rounded-xl border transition-all ${
                    config.provider === option.value
                      ? 'border-pink-500/50 bg-pink-500/10'
                      : 'border-gray-700 bg-gray-800/30 hover:border-gray-600'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-4 h-4 rounded-full border-2 flex items-center justify-center ${
                        config.provider === option.value
                          ? 'border-pink-500'
                          : 'border-gray-600'
                      }`}
                    >
                      {config.provider === option.value && (
                        <div className="w-2 h-2 bg-pink-500 rounded-full" />
                      )}
                    </div>
                    <div>
                      <p className="text-sm font-medium text-white">{option.label}</p>
                      <p className="text-xs text-gray-500">{option.desc}</p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* API 配置 */}
          {config.provider !== 'none' && (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  API Key
                  <span className="text-red-400 ml-1">*</span>
                </label>
                <div className="relative">
                  <input
                    type={showKey ? 'text' : 'password'}
                    value={config.apiKey}
                    onChange={e => setConfig(prev => ({ ...prev, apiKey: e.target.value }))}
                    placeholder="sk-..."
                    className="w-full bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-2.5 text-sm text-white placeholder-gray-600 focus:outline-none focus:border-pink-500/50 pr-10"
                  />
                  <button
                    onClick={() => setShowKey(!showKey)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white text-xs"
                    aria-label={showKey ? '隐藏 API Key' : '显示 API Key'}
                  >
                    {showKey ? '🙈' : '👁️'}
                  </button>
                </div>
                <p className="text-xs text-gray-600 mt-1">API Key 仅存储在本地浏览器中</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  API 地址
                  <span className="text-gray-600 ml-1">(可选)</span>
                </label>
                <input
                  type="text"
                  value={config.apiUrl}
                  onChange={e => setConfig(prev => ({ ...prev, apiUrl: e.target.value }))}
                  placeholder="https://api.openai.com/v1/chat/completions"
                  className="w-full bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-2.5 text-sm text-white placeholder-gray-600 focus:outline-none focus:border-pink-500/50"
                />
                <p className="text-xs text-gray-600 mt-1">留空使用默认地址</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">模型</label>
                <input
                  type="text"
                  value={config.model}
                  onChange={e => setConfig(prev => ({ ...prev, model: e.target.value }))}
                  placeholder="gpt-3.5-turbo"
                  list="model-suggestions"
                  className="w-full bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-2.5 text-sm text-white placeholder-gray-600 focus:outline-none focus:border-pink-500/50"
                />
                <datalist id="model-suggestions">
                  {(MODEL_SUGGESTIONS[config.provider] || []).map(m => (
                    <option key={m} value={m} />
                  ))}
                </datalist>
              </div>

              {/* 测试连接 */}
              <div className="pt-2">
                <button
                  onClick={handleTest}
                  disabled={testStatus === 'testing'}
                  className={`w-full py-2.5 rounded-xl text-sm font-medium transition-all ${
                    testStatus === 'success'
                      ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                      : testStatus === 'error'
                      ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                      : 'bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700'
                  }`}
                >
                  {testStatus === 'testing' ? (
                    <span className="flex items-center justify-center gap-2">
                      <span className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                      测试中...
                    </span>
                  ) : testStatus === 'success' ? (
                    '✓ 连接成功'
                  ) : testStatus === 'error' ? (
                    '✗ 连接失败'
                  ) : (
                    '测试连接'
                  )}
                </button>
                {testMessage && (
                  <p
                    className={`text-xs mt-2 text-center ${
                      testStatus === 'success' ? 'text-emerald-400' : 'text-red-400'
                    }`}
                  >
                    {testMessage}
                  </p>
                )}
              </div>
            </>
          )}
        </div>

        <div className="p-5 border-t border-gray-800 flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 py-2.5 rounded-xl text-sm font-medium text-gray-400 hover:text-white bg-gray-800/50 hover:bg-gray-800 transition-colors"
          >
            取消
          </button>
          <button
            onClick={handleSave}
            className="flex-1 py-2.5 rounded-xl text-sm font-medium text-white bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 transition-all shadow-lg shadow-pink-500/20"
          >
            保存配置
          </button>
        </div>
      </div>
    </div>
  );
}
