import { useState, useRef, useEffect } from 'react';
import { useStore } from '../store';
import { aiApi } from '../api';
import { Send, Loader2, MessageSquare, Trash2 } from 'lucide-react';

export default function ChatInterface() {
  const { messages, addMessage, clearMessages, isChatLoading, setIsChatLoading, currentModel, setError } = useStore();
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isChatLoading) return;

    const userMessage = input.trim();
    setInput('');

    // Add user message
    addMessage({ role: 'user', content: userMessage });

    // Get AI response
    setIsChatLoading(true);
    setError(null);

    try {
      const response = await aiApi.chat(userMessage);
      addMessage({ role: 'assistant', content: response.data.response });
    } catch (err: any) {
      setError(err.message || 'Nie udało się uzyskać odpowiedzi');
      addMessage({
        role: 'assistant',
        content: 'Przepraszam, wystąpił błąd podczas przetwarzania Twojego zapytania.'
      });
    } finally {
      setIsChatLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleClear = async () => {
    try {
      await aiApi.clearHistory();
      clearMessages();
    } catch (err: any) {
      setError(err.message || 'Nie udało się wyczyścić historii');
    }
  };

  return (
    <div className="card flex flex-col h-[calc(100vh-220px)]">
      {/* Header */}
      <div className="flex items-center justify-between mb-4 pb-4 border-b border-gray-700">
        <div className="flex items-center space-x-2">
          <MessageSquare className="w-5 h-5 text-dreame-500" />
          <h2 className="text-lg font-semibold">Chat z Robotem</h2>
        </div>
        {messages.length > 0 && (
          <button
            onClick={handleClear}
            className="text-gray-400 hover:text-red-400 transition-colors"
            title="Wyczyść historię"
          >
            <Trash2 className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
        {messages.length === 0 && (
          <div className="text-center py-12">
            <MessageSquare className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-400 mb-2">Rozpocznij rozmowę z robotem</p>
            <p className="text-sm text-gray-500">
              Możesz pytać o status, wydawać polecenia lub po prostu rozmawiać
            </p>
            <div className="mt-6 space-y-2">
              <p className="text-sm text-gray-500">Przykłady:</p>
              <div className="flex flex-wrap gap-2 justify-center">
                <button
                  onClick={() => setInput('Posprzątaj salon')}
                  className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded-full text-sm transition-colors"
                >
                  "Posprzątaj salon"
                </button>
                <button
                  onClick={() => setInput('Jaki jest stan baterii?')}
                  className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded-full text-sm transition-colors"
                >
                  "Jaki jest stan baterii?"
                </button>
                <button
                  onClick={() => setInput('Wróć do stacji')}
                  className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded-full text-sm transition-colors"
                >
                  "Wróć do stacji"
                </button>
              </div>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-4 py-3 ${
                message.role === 'user'
                  ? 'bg-dreame-600 text-white'
                  : 'bg-gray-700 text-gray-100'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              {message.role === 'assistant' && (
                <p className="text-xs text-gray-400 mt-2">
                  Model: {currentModel === 'local' ? 'Lokalny' : currentModel}
                </p>
              )}
            </div>
          </div>
        ))}

        {isChatLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-700 rounded-lg px-4 py-3">
              <Loader2 className="w-5 h-5 text-dreame-500 animate-spin" />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="flex items-end space-x-3">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Napisz wiadomość do robota..."
          className="input resize-none"
          rows={2}
          disabled={isChatLoading}
        />
        <button
          onClick={handleSend}
          disabled={!input.trim() || isChatLoading}
          className="btn btn-primary flex-shrink-0 h-[72px] px-6 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isChatLoading ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            <Send className="w-5 h-5" />
          )}
        </button>
      </div>
    </div>
  );
}
