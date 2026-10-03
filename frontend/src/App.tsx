/**
 * App — Root component of the Language Agnostic AI Chatbot
 *
 * Assembles:
 *   - ChatHeader (title bar)
 *   - ChatWindow (message list)
 *   - ChatInput  (text input + send button)
 *
 * State is managed via the useChat() hook.
 */

import { ChatHeader } from './components/ChatHeader';
import { ChatWindow } from './components/ChatWindow';
import { ChatInput } from './components/ChatInput';
import { useChat } from './hooks/useChat';

function App() {
  const { messages, isLoading, error, sendUserMessage, clearChat } = useChat();

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl h-[90vh] flex flex-col rounded-2xl overflow-hidden shadow-2xl border border-slate-700">

        {/* Top bar */}
        <ChatHeader onClear={clearChat} />

        {/* Pipeline info strip */}
        <div className="bg-indigo-900 bg-opacity-60 px-4 py-2 flex items-center gap-4 text-xs text-indigo-300 flex-shrink-0 overflow-x-auto">
          <span className="flex items-center gap-1 whitespace-nowrap">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
            Language Detection
          </span>
          <span className="text-indigo-600">→</span>
          <span className="flex items-center gap-1 whitespace-nowrap">
            <span className="w-1.5 h-1.5 rounded-full bg-orange-400" />
            IndicTrans / Google Translate
          </span>
          <span className="text-indigo-600">→</span>
          <span className="flex items-center gap-1 whitespace-nowrap">
            <span className="w-1.5 h-1.5 rounded-full bg-green-400" />
            Rasa NLU
          </span>
          <span className="text-indigo-600">→</span>
          <span className="flex items-center gap-1 whitespace-nowrap">
            <span className="w-1.5 h-1.5 rounded-full bg-yellow-400" />
            FAQ Retrieval
          </span>
          <span className="text-indigo-600">→</span>
          <span className="flex items-center gap-1 whitespace-nowrap">
            <span className="w-1.5 h-1.5 rounded-full bg-pink-400" />
            Translate Back
          </span>
        </div>

        {/* Error banner */}
        {error && (
          <div className="bg-red-50 border-b border-red-200 px-4 py-2 text-xs text-red-600 flex items-center gap-2 flex-shrink-0">
            <svg className="w-4 h-4 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            {error}
          </div>
        )}

        {/* Messages */}
        <ChatWindow messages={messages} isLoading={isLoading} />

        {/* Input */}
        <ChatInput onSend={sendUserMessage} isLoading={isLoading} />
      </div>
    </div>
  );
}

export default App;
