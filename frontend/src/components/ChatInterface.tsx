import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Sparkles } from 'lucide-react';

interface ChatInterfaceProps {
  onSubmit: (question: string) => void;
  isLoading: boolean;
  sampleQueries: string[];
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  onSubmit,
  isLoading,
  sampleQueries,
}) => {
  const [input, setInput] = useState('');
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = 'auto';
      inputRef.current.style.height = `${inputRef.current.scrollHeight}px`;
    }
  }, [input]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSubmit(input.trim());
      setInput('');
    }
  };

  const handleSampleClick = (query: string) => {
    if (!isLoading) {
      setInput(query);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Sample Queries */}
      {sampleQueries.length > 0 && !input && (
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-3">
            <Sparkles className="w-4 h-4 text-primary-500" />
            <p className="text-sm font-medium text-gray-700">Try these questions:</p>
          </div>
          <div className="flex flex-wrap gap-2">
            {sampleQueries.slice(0, 5).map((query, index) => (
              <button
                key={index}
                onClick={() => handleSampleClick(query)}
                disabled={isLoading}
                className="px-3 py-2 text-sm bg-white border border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-left"
              >
                {query}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative flex items-end bg-white rounded-lg border-2 border-gray-300 focus-within:border-primary-500 transition-colors shadow-sm">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about your data... (e.g., 'Show me top 10 customers by revenue')"
            disabled={isLoading}
            rows={1}
            className="flex-1 px-4 py-3 bg-transparent border-none outline-none resize-none max-h-32 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="m-2 p-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
        <p className="mt-2 text-xs text-gray-500">
          Press Enter to send, Shift+Enter for new line
        </p>
      </form>
    </div>
  );
};

export default ChatInterface;

// Made with Bob
