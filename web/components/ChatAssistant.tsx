import { useState, useRef, useCallback, useEffect } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatAssistantProps {
  qaResult?: {
    score: number;
    issues: Array<{
      id: string;
      severity: 'error' | 'warning' | 'info';
      title: string;
      description: string;
      layer?: string;
      suggestion: string;
      expected?: string;
      actual?: string;
    }>;
    warnings: Array<any>;
    layer_stats?: any;
    summary?: any;
  };
}

export default function ChatAssistant({ qaResult }: ChatAssistantProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: '你好！我是 Live2D PSD 质量检测助手 👋\n\n上传 PSD 文件后，我可以帮你：\n• 分析检测结果\n• 提供修复建议\n• 解释问题的原因\n• 回答关于 Live2D 制作的问题',
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping, scrollToBottom]);

  const generateAIResponse = useCallback((userQuery: string) => {
    let response = '';

    if (qaResult) {
      const { score, issues, warnings, layer_stats } = qaResult;
      
      if (userQuery.includes('分析') || userQuery.includes('怎么样') || userQuery.includes('如何') || userQuery.includes('报告')) {
        response = `根据检测结果分析：\n\n**整体评分**: ${score}/100\n\n`;
        
        if (score >= 80) {
          response += '✅ 做得很好！这是一个质量较高的 PSD 文件。\n\n';
        } else if (score >= 60) {
          response += '⚠️ 还有一些需要改进的地方，但整体结构不错。\n\n';
        } else {
          response += '❌ 需要重点修复几个关键问题才能用于 Live2D 制作。\n\n';
        }

        if (issues.length > 0) {
          response += `**严重问题 (${issues.length}个):**\n`;
          issues.slice(0, 3).forEach((issue, i) => {
            response += `${i + 1}. ${issue.title} - ${issue.description}\n`;
          });
          if (issues.length > 3) response += `... 还有 ${issues.length - 3} 个问题\n\n`;
          else response += '\n';
        }

        if (warnings.length > 0) {
          response += `**警告 (${warnings.length}个):** 建议逐步优化\n\n`;
        }

        response += '**修复建议优先级：**\n';
        response += '1. 首先修复严重问题 (🔴)\n';
        response += '2. 然后处理警告 (🟡)\n';
        response += '3. 最后考虑优化建议 (💡)\n\n';
        response += '需要我详细解释某个问题吗？';
      } else if (userQuery.includes('修复') || userQuery.includes('改') || userQuery.includes('解决')) {
        const issueToFix = issues.find(i => userQuery.includes(i.title) || userQuery.includes(i.layer || ''));
        if (issueToFix) {
          response = `关于 **"${issueToFix.title}"** 的修复方法：\n\n`;
          response += '问题描述：\n';
          response += `• ${issueToFix.description}\n\n`;
          response += '修复建议：\n';
          response += `• ${issueToFix.suggestion}\n\n`;
          
          if (issueToFix.expected && issueToFix.actual) {
            response += `预期: ${issueToFix.expected}\n`;
            response += `实际: ${issueToFix.actual}\n\n`;
          }
          response += '还有其他问题需要我解释吗？';
        } else {
          response = '请告诉我具体是哪个问题，我可以给你更详细的修复指导！';
        }
      } else if (userQuery.includes('什么是') || userQuery.includes('为什么') || userQuery.includes('怎么') || userQuery.includes('如何')) {
        response = `这是一个很好的问题！\n\n`;
        
        if (userQuery.includes('neck_base') || userQuery.includes('颈部')) {
          response += '**neck_base** 是 Live2D 模型的核心层之一：\n';
          response += '• 它是颈部运动的基础层\n';
          response += '• 应该放在 face_base 下方、身体上方\n';
          response += '• 影响头部旋转和倾斜效果\n';
        } else if (userQuery.includes('mouth') || userQuery.includes('嘴') || userQuery.includes('口')) {
          response += '**嘴型图层** 对 Live2D 口型同步至关重要：\n';
          response += '• 标准口型：a/i/u/e/o (5个基本形)\n';
          response += '• 建议加上：teeth(牙齿)、lip(嘴唇)等\n';
          response += '• 每个口型独立分层，便于参数绑定\n';
        } else if (userQuery.includes('命名') || userQuery.includes('name')) {
          response += '**Live2D 命名规范** 建议：\n';
          response += '• 使用英文，如：face_base, eye_l, hair_front\n';
          response += '• 左右对称：eye_l / eye_r\n';
          response += '• 层级清晰：hair_front_01, hair_front_02\n';
        } else if (userQuery.includes('混合模式') || userQuery.includes('blend')) {
          response += '**混合模式问题**：\n';
          response += '• Live2D Cubism Editor 只支持 Normal 混合\n';
          response += '• 其他模式 (Multiply/Screen 等) 在导入后会失效\n';
          response += '• 建议将效果直接烘焙到像素中\n';
        } else {
          response += '关于 Live2D PSD 制作，最佳实践包括：\n';
          response += '1. ✅ 使用 RGB 颜色模式\n';
          response += '2. ✅ 画布尺寸建议 1024x1024 或 2048x2048\n';
          response += '3. ✅ 每个部件独立分层\n';
          response += '4. ✅ 关键图层命名规范\n';
          response += '5. ✅ 避免使用混合模式和图层透明度\n';
        }
      } else {
        response = '我可以帮你分析这个 PSD 文件的问题！\n\n';
        response += '你可以问我：\n';
        response += '• "分析一下这个报告"\n';
        response += '• "如何修复 xxx 问题？"\n';
        response += '• "什么是 neck_base？"\n';
        response += '• 或者任何关于 Live2D 制作的问题\n';
      }
    } else {
      response = '请先上传一个 PSD 文件，我就能帮你分析和解决问题了！\n\n';
      response += '你也可以问我关于 Live2D 制作的一般问题，比如：\n';
      response += '• 如何正确分层？\n';
      response += '• 命名规范是什么？\n';
      response += '• 画布尺寸建议多少？\n';
    }

    return response;
  }, [qaResult]);

  const handleSend = useCallback(async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    setTimeout(() => {
      const aiResponse = generateAIResponse(inputValue);
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: aiResponse,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, assistantMessage]);
      setIsTyping(false);
    }, 800);
  }, [inputValue, generateAIResponse]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }, [handleSend]);

  const handleQuickAsk = useCallback((question: string) => {
    setInputValue(question);
  }, []);

  return (
    <div className="flex flex-col h-full bg-gray-900/30 border border-gray-800 rounded-xl overflow-hidden">
      <div className="p-4 border-b border-gray-800 bg-gray-800/50">
        <div className="flex items-center gap-3">
          <span className="text-2xl">🤖</span>
          <div>
            <h3 className="text-sm font-semibold text-gray-200">AI 助手</h3>
            <p className="text-xs text-gray-500">Live2D PSD 制作顾问</p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
          >
            <div
              className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm ${
                msg.role === 'user'
                  ? 'bg-pink-500/20 text-pink-300'
                  : 'bg-blue-500/20 text-blue-300'
              }`}
            >
              {msg.role === 'user' ? '👤' : '🤖'}
            </div>
            <div
              className={`max-w-[85%] rounded-lg p-3 ${
                msg.role === 'user'
                  ? 'bg-pink-500/10 border border-pink-500/20'
                  : 'bg-gray-800/50 border border-gray-700/50'
              }`}
            >
              <div className="text-sm whitespace-pre-line text-gray-200">
                {msg.content}
              </div>
              <div className="text-xs text-gray-600 mt-1">
                {msg.timestamp.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="flex gap-3">
            <div className="shrink-0 w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center text-sm text-blue-300">
              🤖
            </div>
            <div className="bg-gray-800/50 border border-gray-700/50 rounded-lg p-3">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {!qaResult && messages.length === 1 && (
        <div className="px-4 pb-2">
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => handleQuickAsk('如何正确分层？')}
              className="text-xs px-3 py-1.5 bg-gray-800/50 hover:bg-gray-800 text-gray-400 hover:text-gray-200 rounded-lg transition-colors"
            >
              📝 如何正确分层？
            </button>
            <button
              onClick={() => handleQuickAsk('命名规范是什么？')}
              className="text-xs px-3 py-1.5 bg-gray-800/50 hover:bg-gray-800 text-gray-400 hover:text-gray-200 rounded-lg transition-colors"
            >
              🏷️ 命名规范
            </button>
            <button
              onClick={() => handleQuickAsk('画布尺寸建议多少？')}
              className="text-xs px-3 py-1.5 bg-gray-800/50 hover:bg-gray-800 text-gray-400 hover:text-gray-200 rounded-lg transition-colors"
            >
              📐 画布尺寸
            </button>
          </div>
        </div>
      )}

      {qaResult && messages.length === 1 && (
        <div className="px-4 pb-2">
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => handleQuickAsk('分析一下这个报告')}
              className="text-xs px-3 py-1.5 bg-gray-800/50 hover:bg-gray-800 text-gray-400 hover:text-gray-200 rounded-lg transition-colors"
            >
              📊 分析报告
            </button>
            <button
              onClick={() => handleQuickAsk('主要问题是什么？')}
              className="text-xs px-3 py-1.5 bg-gray-800/50 hover:bg-gray-800 text-gray-400 hover:text-gray-200 rounded-lg transition-colors"
            >
              🔴 主要问题
            </button>
            <button
              onClick={() => handleQuickAsk('如何优先修复？')}
              className="text-xs px-3 py-1.5 bg-gray-800/50 hover:bg-gray-800 text-gray-400 hover:text-gray-200 rounded-lg transition-colors"
            >
              ⚡ 优先修复
            </button>
          </div>
        </div>
      )}

      <div className="p-4 border-t border-gray-800 bg-gray-800/30">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="问我关于 PSD 或 Live2D 的问题..."
            className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-2.5 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-pink-500/50 transition-colors"
          />
          <button
            onClick={handleSend}
            disabled={!inputValue.trim() || isTyping}
            className={`px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${
              inputValue.trim() && !isTyping
                ? 'bg-pink-500 text-white hover:bg-pink-600'
                : 'bg-gray-700 text-gray-500 cursor-not-allowed'
            }`}
          >
            发送
          </button>
        </div>
      </div>
    </div>
  );
}
