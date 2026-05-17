import React, { useState, useRef, useCallback, useEffect } from 'react';

const parseMarkdown = (text: string): React.ReactNode => {
  const parts: React.ReactNode[] = [];
  let remaining = text;
  let key = 0;

  while (remaining.length > 0) {
    const boldMatch = remaining.match(/\*\*(.+?)\*\*/);
    const codeMatch = remaining.match(/`([^`]+)`/);
    const codeBlockMatch = remaining.match(/```(\w+)?\n([\s\S]*?)```/);
    const listMatch = remaining.match(/^(\s*•\s.+?)(?=\n|$)/);
    const bulletMatch = remaining.match(/^(\s*\d+\.\s.+?)(?=\n|$)/);
    const headerMatch = remaining.match(/^###\s(.+)$/m);
    const lineBreakMatch = remaining.match(/^\n/);

    const codeBlockIndex = codeBlockMatch?.index ?? Infinity;
    const boldIndex = boldMatch?.index ?? Infinity;
    const codeIndex = codeMatch?.index ?? Infinity;

    if (codeBlockMatch && codeBlockIndex < boldIndex && codeBlockIndex < codeIndex) {
      const [full, lang, content] = codeBlockMatch;
      parts.push(
        <pre key={`code-${key++}`} className="bg-gray-900 rounded-lg p-3 overflow-x-auto text-sm text-gray-300 font-mono border border-gray-700">
          <code>{content.trim()}</code>
        </pre>
      );
      remaining = remaining.slice(full.length);
    } else if (boldMatch && boldIndex < codeIndex) {
      const [full, content] = boldMatch;
      const before = remaining.slice(0, boldIndex);
      if (before) {
        parts.push(<span key={`text-${key++}`}>{before}</span>);
      }
      parts.push(<strong key={`bold-${key++}`} className="text-white font-semibold">{content}</strong>);
      remaining = remaining.slice(boldIndex + full.length);
    } else if (codeMatch) {
      const [full, content] = codeMatch;
      const before = remaining.slice(0, codeIndex);
      if (before) {
        parts.push(<span key={`text-${key++}`}>{before}</span>);
      }
      parts.push(
        <code key={`inline-code-${key++}`} className="bg-gray-700 rounded px-1.5 py-0.5 text-xs text-pink-400 font-mono">
          {content}
        </code>
      );
      remaining = remaining.slice(codeIndex + full.length);
    } else if (headerMatch) {
      const [full, content] = headerMatch;
      parts.push(<h4 key={`header-${key++}`} className="text-white font-semibold text-base mt-2 mb-1">{content}</h4>);
      remaining = remaining.slice(full.length);
    } else if (listMatch) {
      const [full, content] = listMatch;
      parts.push(
        <div key={`list-${key++}`} className="flex items-start gap-2 text-gray-300">
          <span className="text-pink-400 mt-0.5">•</span>
          <span>{content.slice(2)}</span>
        </div>
      );
      remaining = remaining.slice(full.length);
    } else if (bulletMatch) {
      const [full, content] = bulletMatch;
      const numMatch = content.match(/^(\d+)\./);
      const num = numMatch ? numMatch[1] : '';
      parts.push(
        <div key={`bullet-${key++}`} className="flex items-start gap-2 text-gray-300">
          <span className="text-purple-400 mt-0.5 font-medium">{num}.</span>
          <span>{content.slice(num.length + 2)}</span>
        </div>
      );
      remaining = remaining.slice(full.length);
    } else if (lineBreakMatch) {
      parts.push(<br key={`br-${key++}`} />);
      remaining = remaining.slice(1);
    } else {
      parts.push(<span key={`text-${key++}`}>{remaining}</span>);
      break;
    }
  }

  return parts;
};

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
    warnings: Array<{
      id: string;
      severity: 'error' | 'warning' | 'info';
      title: string;
      description: string;
      layer?: string;
      suggestion: string;
      expected?: string;
      actual?: string;
    }>;
    layer_stats?: {
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
    summary?: {
      totalLayers: number;
      visibleLayers: number;
      hiddenLayers: number;
      groups: number;
      hasMissingCritical: boolean;
      hasNamingIssues: boolean;
      hasStructuralIssues: boolean;
    };
  };
}

const SendIcon = () => (
  <svg className="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
    <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
  </svg>
);

const SparklesIcon = () => (
  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M12 3l1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5L12 3z" />
    <path d="M19 15l1 3 1-3 3-1-3-1-1-3-1 3-3 1 3 1z" />
  </svg>
);

export default function ChatAssistant({ qaResult }: ChatAssistantProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: '你好！我是 Live2D PSD 质量检测助手 ✨\n\n我可以帮你：\n• 分析检测结果和问题\n• 提供针对性的修复建议\n• 解答 Live2D 制作相关问题\n\n上传 PSD 文件后，我们开始吧！',
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
        response = `📊 **检测结果分析**\n\n`;
        response += `**综合评分**: ${score}/100\n\n`;
        
        if (score >= 80) {
          response += '✅ **优秀** - 这是一个高质量的 PSD 文件！\n\n';
        } else if (score >= 60) {
          response += '⚠️ **良好** - 有一些小问题需要优化。\n\n';
        } else {
          response += '❌ **需改进** - 需要重点修复几个关键问题。\n\n';
        }

        if (issues.length > 0) {
          response += `**🔴 严重问题 (${issues.length}个)**\n`;
          issues.slice(0, 3).forEach((issue, i) => {
            response += `${i + 1}. ${issue.title}\n`;
          });
          if (issues.length > 3) response += `... 还有 ${issues.length - 3} 个问题\n`;
          response += '\n';
        }

        if (warnings.length > 0) {
          response += `**🟡 警告 (${warnings.length}个)** - 建议逐步优化\n\n`;
        }

        response += '需要我详细解释某个问题吗？';
      } else if (userQuery.includes('修复') || userQuery.includes('改') || userQuery.includes('解决')) {
        const issueToFix = issues.find(i => 
          userQuery.includes(i.title.toLowerCase()) || 
          userQuery.includes(i.layer?.toLowerCase() || '')
        );
        if (issueToFix) {
          response = `🔧 **修复指导: "${issueToFix.title}"**\n\n`;
          response += '**问题描述:**\n';
          response += `${issueToFix.description}\n\n`;
          response += '**修复步骤:**\n';
          response += `${issueToFix.suggestion}\n\n`;
          
          if (issueToFix.expected && issueToFix.actual) {
            response += `**预期:** ${issueToFix.expected}\n`;
            response += `**当前:** ${issueToFix.actual}\n\n`;
          }
          response += '还有其他问题需要帮助吗？';
        } else {
          response = '请告诉我具体是哪个问题，例如："如何修复 neck_base 问题？"';
        }
      } else if (userQuery.includes('什么是') || userQuery.includes('为什么') || userQuery.includes('怎么') || userQuery.includes('如何') || userQuery.includes('介绍')) {
        response = '💡 **Live2D 知识解答**\n\n';
        
        if (userQuery.includes('neck') || userQuery.includes('颈部')) {
          response += '**neck_base (颈部基础层)** 是 Live2D 模型的核心层：\n\n';
          response += '• 定义颈部运动的基础\n';
          response += '• 位置：face_base 下方、身体上方\n';
          response += '• 影响头部旋转和倾斜\n';
          response += '• 命名规范：使用下划线 `neck_base`\n';
        } else if (userQuery.includes('mouth') || userQuery.includes('嘴') || userQuery.includes('口型')) {
          response += '**嘴型图层** 对口型同步至关重要：\n\n';
          response += '• **标准五型**: a, i, u, e, o\n';
          response += '• 建议添加: teeth(牙齿), lip(嘴唇)\n';
          response += '• 每个口型独立分层\n';
          response += '• 便于后续参数绑定\n';
        } else if (userQuery.includes('命名') || userQuery.includes('name')) {
          response += '**命名规范建议**:\n\n';
          response += '• 使用英文：face_base, eye_l\n';
          response += '• 左右对称：`_l` / `_r` 后缀\n';
          response += '• 层级清晰：`hair_front_01`\n';
          response += '• 避免特殊字符和中文\n';
        } else if (userQuery.includes('混合模式') || userQuery.includes('blend')) {
          response += '**混合模式注意事项**:\n\n';
          response += '• Cubism Editor **仅支持 Normal**\n';
          response += '• 其他模式会失效\n';
          response += '• 建议：效果直接烘焙到像素\n';
          response += '• 或拆分图层处理\n';
        } else if (userQuery.includes('透明度')) {
          response += '**透明度处理建议**:\n\n';
          response += '• 关键图层保持 100% 透明度\n';
          response += '• 透明度效果可接受\n';
          response += '• 注意：半透明会影响渲染\n';
        } else {
          response += '**Live2D PSD 最佳实践**:\n\n';
          response += '✅ RGB 颜色模式\n';
          response += '✅ 画布 1024×1024 或 2048×2048\n';
          response += '✅ 部件独立分层\n';
          response += '✅ 规范命名\n';
          response += '✅ Normal 混合模式\n';
        }
      } else {
        response = '🤔 我可以帮你分析这个 PSD！\n\n';
        response += '试试这样问我：\n\n';
        response += '• "📊 分析一下报告"\n';
        response += '• "🔧 如何修复这个问题？"\n';
        response += '• "💡 什么是 neck_base？"\n';
        response += '• "📝 分层规范是什么？"\n';
      }
    } else {
      response = '👋 请先上传 PSD 文件！\n\n';
      response += '上传后我可以帮你：\n\n';
      response += '• 📊 分析检测结果\n';
      response += '• 🔧 提供修复建议\n';
      response += '• 💡 解答制作问题\n\n';
      response += '你也可以问我关于 Live2D 的一般问题：\n';
      response += '• 如何正确分层？\n';
      response += '• 命名规范是什么？\n';
      response += '• 画布尺寸建议？';
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
    <div className="flex flex-col h-full bg-gradient-to-br from-gray-900/50 via-gray-900/30 to-gray-800/30 border border-gray-800/50 rounded-xl sm:rounded-2xl overflow-hidden backdrop-blur-xl min-h-[400px]">
      <div className="shrink-0 p-3 sm:p-5 border-b border-gray-800/50 bg-gradient-to-r from-pink-500/5 via-purple-500/5 to-blue-500/5">
        <div className="flex items-center gap-2 sm:gap-3">
          <div className="relative">
            <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl sm:rounded-2xl bg-gradient-to-br from-pink-500 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-pink-500/30">
              <SparklesIcon />
            </div>
            <div className="absolute -bottom-1 -right-1 w-3.5 h-3.5 sm:w-4 sm:h-4 bg-emerald-500 rounded-full border-2 border-gray-900 animate-pulse" />
          </div>
          <div>
            <h3 className="text-sm sm:text-base font-semibold text-white mb-0.5">AI 助手</h3>
            <p className="text-xs text-gray-500 flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />
              Live2D 质量顾问
            </p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-5 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={msg.id}
            className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'} animate-fade-in`}
            style={{ animationDelay: `${idx * 50}ms` }}
          >
            <div
              className={`shrink-0 w-10 h-10 rounded-2xl flex items-center justify-center text-sm shadow-lg ${
                msg.role === 'user'
                  ? 'bg-gradient-to-br from-pink-500 to-rose-600 text-white'
                  : 'bg-gradient-to-br from-purple-500 to-indigo-600 text-white'
              }`}
            >
              {msg.role === 'user' ? (
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              ) : (
                <SparklesIcon />
              )}
            </div>
            <div
              className={`max-w-[85%] sm:max-w-[80%] rounded-xl sm:rounded-2xl p-3 sm:p-4 ${
                msg.role === 'user'
                  ? 'bg-gradient-to-br from-pink-500/20 to-rose-500/10 border border-pink-500/20'
                  : 'bg-gray-800/60 border border-gray-700/50 backdrop-blur-sm'
              }`}
            >
              <div className="text-xs sm:text-sm text-gray-200 leading-relaxed">
                {msg.role === 'assistant' ? parseMarkdown(msg.content) : msg.content}
              </div>
              <div className="text-xs text-gray-600 mt-2 flex items-center gap-1">
                {msg.timestamp.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="flex gap-3 animate-fade-in">
            <div className="shrink-0 w-10 h-10 rounded-2xl bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center text-white shadow-lg">
              <SparklesIcon />
            </div>
            <div className="bg-gray-800/60 border border-gray-700/50 backdrop-blur-sm rounded-2xl p-4">
              <div className="flex gap-1.5">
                <span className="w-2 h-2 bg-pink-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '100ms' }} />
                <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '200ms' }} />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {!qaResult && messages.length === 1 && (
        <div className="px-5 pb-3">
          <p className="text-xs text-gray-500 mb-2 text-center">快捷提问</p>
          <div className="flex flex-wrap gap-2 justify-center">
            <button
              onClick={() => handleQuickAsk('如何正确分层？')}
              className="text-xs px-3 py-1.5 bg-gray-800/50 hover:bg-gray-800 text-gray-400 hover:text-white rounded-lg border border-gray-700/50 hover:border-gray-600 transition-all hover:shadow-lg hover:shadow-gray-500/10"
            >
              📝 分层规范
            </button>
            <button
              onClick={() => handleQuickAsk('命名规范是什么？')}
              className="text-xs px-3 py-1.5 bg-gray-800/50 hover:bg-gray-800 text-gray-400 hover:text-white rounded-lg border border-gray-700/50 hover:border-gray-600 transition-all hover:shadow-lg hover:shadow-gray-500/10"
            >
              🏷️ 命名规则
            </button>
            <button
              onClick={() => handleQuickAsk('画布尺寸建议多少？')}
              className="text-xs px-3 py-1.5 bg-gray-800/50 hover:bg-gray-800 text-gray-400 hover:text-white rounded-lg border border-gray-700/50 hover:border-gray-600 transition-all hover:shadow-lg hover:shadow-gray-500/10"
            >
              📐 画布尺寸
            </button>
          </div>
        </div>
      )}

      {qaResult && messages.length === 1 && (
        <div className="px-5 pb-3">
          <p className="text-xs text-gray-500 mb-2 text-center">快速分析</p>
          <div className="flex flex-wrap gap-2 justify-center">
            <button
              onClick={() => handleQuickAsk('分析一下这个报告')}
              className="text-xs px-3 py-1.5 bg-gradient-to-r from-pink-500/20 to-purple-500/20 hover:from-pink-500/30 hover:to-purple-500/30 text-pink-300 hover:text-pink-200 rounded-lg border border-pink-500/20 hover:border-pink-500/30 transition-all"
            >
              📊 分析报告
            </button>
            <button
              onClick={() => handleQuickAsk('主要问题是什么？')}
              className="text-xs px-3 py-1.5 bg-gradient-to-r from-red-500/20 to-orange-500/20 hover:from-red-500/30 hover:to-orange-500/30 text-red-300 hover:text-red-200 rounded-lg border border-red-500/20 hover:border-red-500/30 transition-all"
            >
              🔴 主要问题
            </button>
            <button
              onClick={() => handleQuickAsk('如何优先修复？')}
              className="text-xs px-3 py-1.5 bg-gradient-to-r from-emerald-500/20 to-teal-500/20 hover:from-emerald-500/30 hover:to-teal-500/30 text-emerald-300 hover:text-emerald-200 rounded-lg border border-emerald-500/20 hover:border-emerald-500/30 transition-all"
            >
              ⚡ 优先修复
            </button>
          </div>
        </div>
      )}

      <div className="shrink-0 p-3 sm:p-5 border-t border-gray-800/50 bg-gradient-to-t from-gray-900/50 to-transparent backdrop-blur-sm">
        <div className="flex gap-2 sm:gap-3">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="问我关于 PSD 或 Live2D 的问题..."
            className="flex-1 bg-gray-800/60 border border-gray-700/50 rounded-lg sm:rounded-xl px-3 sm:px-4 py-2 sm:py-3 text-xs sm:text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-pink-500/50 focus:bg-gray-800/80 transition-all backdrop-blur-sm"
          />
          <button
            onClick={handleSend}
            disabled={!inputValue.trim() || isTyping}
            className={`shrink-0 px-3 sm:px-5 py-2 sm:py-3 rounded-lg sm:rounded-xl text-xs sm:text-sm font-medium transition-all shadow-lg ${
              inputValue.trim() && !isTyping
                ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white hover:from-pink-600 hover:to-purple-700 shadow-pink-500/30 hover:shadow-pink-500/50 active:scale-95'
                : 'bg-gray-700 text-gray-500 cursor-not-allowed'
            }`}
          >
            <SendIcon />
          </button>
        </div>
      </div>
    </div>
  );
}
