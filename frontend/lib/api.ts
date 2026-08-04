import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
}

export interface Source {
  text: string;
  metadata: {
    type?: string;
    interior_style_name?: string;
    interior_style_image_url?: string;
    architecture_type_name?: string;
    architecture_type_image_url?: string;
    project_name?: string;
    project_image_url?: string;
    project_thumbnail_url?: string;
    news_title?: string;
    news_image_url?: string;
    news_thumbnail_url?: string;
    slide_title?: string;
    slide_image_url?: string;
    [key: string]: unknown;
  };
  score: number;
}

export interface ChatRequest {
  query: string;
  session_id?: string;
}

export interface ChatResponse {
  answer: string;
  sources?: Source[];
  session_id: string;
}

export interface StreamHandlers {
  onMeta?: (sessionId: string) => void;
  onDelta?: (delta: string) => void;
  onSources?: (sources: Source[]) => void;
  onDone?: (payload: { answer?: string; session_id?: string }) => void;
  onError?: (message: string) => void;
}

export const chatService = {
  /**
   * Stream a chat message via SSE from POST /api/chat/openai.
   * Reads response.body with getReader() and parses SSE events from a buffer.
   */
  async sendMessageStream(request: ChatRequest, handlers: StreamHandlers): Promise<void> {
    let response: Response;
    try {
      response = await fetch(`${API_URL}/api/chat/openai`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
      });
    } catch (error) {
      console.error('Error sending message:', error);
      handlers.onError?.('Không thể kết nối đến máy chủ. Vui lòng thử lại sau.');
      return;
    }

    if (!response.ok) {
      let message = `HTTP ${response.status}`;
      try {
        const data = await response.json();
        if (data && data.detail) message = data.detail;
      } catch {
        // ignore non-JSON error body
      }
      handlers.onError?.(message);
      return;
    }

    if (!response.body) {
      handlers.onError?.('Không thể đọc phản hồi từ máy chủ.');
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    const handleBlock = (block: string) => {
      if (!block.trim()) return;
      let eventName = 'message';
      let dataStr = '';
      for (const line of block.split('\n')) {
        if (line.startsWith('event:')) eventName = line.slice(6).trim();
        else if (line.startsWith('data:')) dataStr += line.slice(5).trim();
      }
      if (!dataStr) return;
      let data: Record<string, unknown>;
      try {
        data = JSON.parse(dataStr);
      } catch {
        return;
      }
      switch (eventName) {
        case 'meta':
          handlers.onMeta?.(String(data.session_id ?? ''));
          break;
        case 'delta':
          handlers.onDelta?.(String(data.delta ?? ''));
          break;
        case 'sources':
          handlers.onSources?.((data.sources as Source[]) ?? []);
          break;
        case 'done':
          handlers.onDone?.({
            answer: data.answer !== undefined ? String(data.answer) : undefined,
            session_id: data.session_id !== undefined ? String(data.session_id) : undefined,
          });
          break;
        case 'error':
          handlers.onError?.(String(data.message ?? 'Đã xảy ra lỗi. Vui lòng thử lại sau.'));
          break;
        default:
          break;
      }
    };

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      let sepIndex: number;
      while ((sepIndex = buffer.indexOf('\n\n')) !== -1) {
        const block = buffer.slice(0, sepIndex);
        buffer = buffer.slice(sepIndex + 2);
        handleBlock(block);
      }
    }

    // Flush any remaining block without trailing separator
    if (buffer.trim()) handleBlock(buffer);
  },

  async healthCheck(): Promise<boolean> {
    try {
      const response = await axios.get(`${API_URL}/health`);
      return response.status === 200;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  },
};
