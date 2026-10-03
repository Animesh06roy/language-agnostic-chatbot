/**
 * ChatInput — Text input box and Send button
 *
 * Features:
 * - Press Enter to send (Shift+Enter for newline)
 * - Disabled while bot is responding
 * - Sample question buttons for quick testing
 */

import { useState, type KeyboardEvent, useRef, useEffect } from 'react';

interface Props {
  onSend: (message: string) => void;
  isLoading: boolean;
}

// Sample questions users can click to quickly test different languages and intents
const SAMPLE_QUESTIONS = [
  { label: 'Hostel fees?', text: 'What are the hostel fees?' },
  { label: 'Exams?', text: 'When are the semester exams?' },
  { label: 'हिंदी में', text: 'छात्रवृत्ति के लिए कैसे आवेदन करें?' },   // Hindi: How to apply for scholarship?
  { label: 'Placements?', text: 'What is the average placement package?' },
  { label: 'Attendance?', text: 'How much attendance is required?' },
];

export function ChatInput({ onSend, isLoading }: Props) {
  const [inputText, setInputText] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Focus the input on mount
  useEffect(() => {
    textareaRef.current?.focus();
  }, []);

  const handleSend = () => {
    const text = inputText.trim();
    if (!text || isLoading) return;
    onSend(text);
    setInputText('');
    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  // Enter sends, Shift+Enter adds newline
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Auto-resize textarea as user types
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputText(e.target.value);
    const ta = e.target;
    ta.style.height = 'auto';
    ta.style.height = `${Math.min(ta.scrollHeight, 120)}px`;
  };

  const handleSampleClick = (text: string) => {
    if (isLoading) return;
    onSend(text);
  };

  return (
    <div className="border-t border-slate-200 bg-white">
      {/* Sample question chips */}
      <div className="px-4 pt-3 pb-1 flex flex-wrap gap-2">
        <span className="text-xs text-slate-400 self-center">Try:</span>
        {SAMPLE_QUESTIONS.map(q => (
          <button
            key={q.label}
            onClick={() => handleSampleClick(q.text)}
            disabled={isLoading}
            className="text-xs px-3 py-1 rounded-full bg-slate-100 hover:bg-indigo-50 hover:text-indigo-600 text-slate-600 border border-slate-200 hover:border-indigo-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {q.label}
          </button>
        ))}
      </div>

      {/* Input row */}
      <div className="flex items-end gap-2 p-4 pt-2">
        <textarea
          ref={textareaRef}
          value={inputText}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder="Ask in any language — English, Hindi, Tamil..."
          rows={1}
          disabled={isLoading}
          className="flex-1 resize-none rounded-xl border border-slate-300 px-4 py-2.5 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-slate-50 disabled:cursor-not-allowed transition-all"
          style={{ minHeight: '44px', maxHeight: '120px' }}
        />

        {/* Send Button */}
        <button
          onClick={handleSend}
          disabled={isLoading || !inputText.trim()}
          className="flex-shrink-0 w-11 h-11 rounded-xl bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-300 text-white flex items-center justify-center transition-colors disabled:cursor-not-allowed"
          aria-label="Send message"
        >
          {isLoading ? (
            /* Small spinner on button when loading */
            <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeOpacity="0.3" />
              <path d="M12 2a10 10 0 0 1 10 10" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
            </svg>
          ) : (
            /* Send arrow icon */
            <svg className="w-5 h-5 translate-x-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 2L11 13" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M22 2L15 22 11 13 2 9l20-7z" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          )}
        </button>
      </div>
    </div>
  );
}
