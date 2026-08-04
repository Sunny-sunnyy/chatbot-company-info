'use client';

import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Send, Bot, User, Image as ImageIcon } from 'lucide-react';
import { chatService, type ChatMessage } from '@/lib/api';

export default function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const question = input;

    setMessages((prev) => [...prev, { role: 'user', content: question }]);
    setMessages((prev) => [...prev, { role: 'assistant', content: '', sources: [] }]);
    setInput('');
    setIsLoading(true);

    try {
      await chatService.sendMessageStream(
        { query: question, session_id: sessionId || undefined },
        {
          onMeta: (sid) => {
            if (sid) setSessionId(sid);
          },
          onDelta: (delta) => {
            setMessages((prev) => {
              const next = [...prev];
              const last = next[next.length - 1];
              if (last && last.role === 'assistant') {
                next[next.length - 1] = { ...last, content: last.content + delta };
              }
              return next;
            });
          },
          onSources: (sources) => {
            setMessages((prev) => {
              const next = [...prev];
              const last = next[next.length - 1];
              if (last && last.role === 'assistant') {
                next[next.length - 1] = { ...last, sources };
              }
              return next;
            });
          },
          onDone: (payload) => {
            if (payload.session_id) setSessionId(payload.session_id);
          },
          onError: (message) => {
            setMessages((prev) => {
              const next = [...prev];
              const last = next[next.length - 1];
              if (last && last.role === 'assistant') {
                next[next.length - 1] = { ...last, content: message };
              }
              return next;
            });
          },
        }
      );
    } catch (error) {
      console.error('Error:', error);
      setMessages((prev) => {
        const next = [...prev];
        const last = next[next.length - 1];
        if (last && last.role === 'assistant') {
          next[next.length - 1] = { ...last, content: 'Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau.' };
        }
        return next;
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 to-green-100">
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-4 py-6">
          {messages.length === 0 ? (
            <div className="text-center py-12">
              <h2 className="text-xl font-semibold text-gray-700 mb-2">Xin chào! Tôi có thể giúp gì cho bạn?</h2>
              <p className="text-gray-500"> Hỏi tôi về dự án, kiến trúc, nội thất, hoặc tin tức của NMK</p>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message, index) => {
                const isStreamingPlaceholder =
                  message.role === 'assistant' &&
                  message.content.length === 0 &&
                  isLoading &&
                  index === messages.length - 1;

                return (
                <div key={index} className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  {message.role === 'assistant' && (
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 rounded-full bg-green-600 flex items-center justify-center">
                        <Bot className="w-5 h-5 text-white" />
                      </div>
                    </div>
                  )}
                  
                  <div className={`max-w-[70%] min-w-0 break-words rounded-2xl px-4 py-3 ${message.role === 'user' ? 'bg-green-600 text-white' : 'bg-white text-gray-800 shadow-md'}`}>
                    {message.role === 'assistant' ? (
                      isStreamingPlaceholder ? (
                        <div className="flex gap-1 py-1">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                        </div>
                      ) : (
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                          p: ({ children }) => <p className="my-1">{children}</p>,
                          strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
                          ul: ({ children }) => <ul className="list-disc pl-5 my-1 space-y-1">{children}</ul>,
                          ol: ({ children }) => <ol className="list-decimal pl-5 my-1 space-y-1">{children}</ol>,
                          li: ({ children }) => <li className="my-0.5">{children}</li>,
                          a: ({ href, children }) => (
                            <a href={href} target="_blank" rel="noreferrer" className="text-blue-600 underline break-words">
                              {children}
                            </a>
                          ),
                          code: ({ className, children }) => (
                            <code className={`${className ?? ''} bg-gray-100 px-1 py-0.5 rounded text-sm break-all`}>
                              {children}
                            </code>
                          ),
                          pre: ({ children }) => (
                            <pre className="bg-gray-100 p-2 rounded-lg overflow-x-auto my-2 text-sm">{children}</pre>
                          ),
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                      )
                    ) : (
                      <p className="whitespace-pre-wrap break-words">{message.content}</p>
                    )}

                    {/* Display images from sources */}
                    {message.role === 'assistant' && message.sources && message.sources.length > 0 && (
                      <div className="mt-3 space-y-2">
                        {message.sources
                          .filter(source => {
                            const metadata = source.metadata || {};
                            return metadata.interior_style_image_url || 
                                   metadata.architecture_type_image_url ||
                                   metadata.project_image_url || 
                                   metadata.project_thumbnail_url ||
                                   metadata.news_image_url ||
                                   metadata.news_thumbnail_url ||
                                   metadata.slide_image_url;
                          })
                          .slice(0, 3)
                          .map((source, idx) => {
                            const metadata = source.metadata || {};
                            const imageUrl = metadata.interior_style_image_url || 
                                           metadata.architecture_type_image_url ||
                                           metadata.project_image_url || 
                                           metadata.project_thumbnail_url ||
                                           metadata.news_image_url ||
                                           metadata.news_thumbnail_url ||
                                           metadata.slide_image_url;
                            
                            const title = metadata.interior_style_name || 
                                        metadata.architecture_type_name ||
                                        metadata.project_name || 
                                        metadata.news_title ||
                                        metadata.slide_title ||
                                        'Hình ảnh';
                            
                            return (
                              <div key={idx} className="border border-gray-200 rounded-lg overflow-hidden">
                                <img 
                                  src={imageUrl} 
                                  alt={title}
                                  className="w-full h-48 object-cover"
                                  loading="lazy"
                                  onError={(e) => {
                                    const target = e.target as HTMLImageElement;
                                    target.style.display = 'none';
                                  }}
                                />
                                <div className="p-2 bg-gray-50 flex items-center gap-1 text-xs text-gray-600">
                                  <ImageIcon className="w-3 h-3" />
                                  <span>{title}</span>
                                </div>
                              </div>
                            );
                          })}
                      </div>
                    )}
                  </div>

                  {message.role === 'user' && (
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center">
                        <User className="w-5 h-5 text-white" />
                      </div>
                    </div>
                  )}
                </div>
                );
              })}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </div>

      <div className="bg-white border-t border-gray-200">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input type="text" value={input} onChange={(e) => setInput(e.target.value)} placeholder="Nhập câu hỏi của bạn..." className="flex-1 px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent text-gray-800" disabled={isLoading}/>
            <button type="submit" disabled={isLoading || !input.trim()} className="px-6 py-3 bg-green-600 text-white rounded-full hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center gap-2">
              <Send className="w-5 h-5" />
              Gửi
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
