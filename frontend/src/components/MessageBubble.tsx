/**
 * MessageBubble — Displays a single chat message (user or bot)
 *
 * Bot messages optionally show a metadata panel with:
 * - Detected language
 * - Intent classified by Rasa
 * - Translation method used (IndicTrans vs Google Translate)
 * - Processing time
 */

import { useState } from 'react';
import type { Message } from '../types';

interface Props {
  message: Message;
}

// Map translation method codes to readable labels + badge colors
const TRANSLATION_METHOD_LABELS: Record<string, { label: string; color: string }> = {
  indicTrans: { label: 'IndicTrans (Hindi)', color: 'bg-orange-100 text-orange-700' },
  googleTranslate: { label: 'Google Translate', color: 'bg-blue-100 text-blue-700' },
  none: { label: 'No translation (English)', color: 'bg-green-100 text-green-700' },
};

export function MessageBubble({ message }: Props) {
  const isUser = message.sender === 'user';
  // Toggle to show/hide metadata details
  const [showMeta, setShowMeta] = useState(false);

  const formatTime = (date: Date) =>
    date.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });

  const methodInfo = message.metadata
    ? TRANSLATION_METHOD_LABELS[message.metadata.translationMethod] || TRANSLATION_METHOD_LABELS.none
    : null;

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}>
      <div className={`max-w-[80%] ${isUser ? 'items-end' : 'items-start'} flex flex-col gap-1`}>

        {/* Avatar + Name */}
        <div className={`flex items-center gap-2 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
          <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 ${
            isUser ? 'bg-indigo-600 text-white' : 'bg-slate-700 text-white'
          }`}>
            {isUser ? 'U' : 'AI'}
          </div>
          <span className="text-xs text-slate-400">{formatTime(message.timestamp)}</span>
        </div>

        {/* Message bubble */}
        <div className={`rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
          isUser
            ? 'bg-indigo-600 text-white rounded-tr-sm'
            : 'bg-white border border-slate-200 text-slate-800 rounded-tl-sm shadow-sm'
        }`}>
          {message.text}
        </div>

        {/* Metadata panel — only for bot messages with metadata */}
        {!isUser && message.metadata && (
          <div className="ml-9">
            <button
              onClick={() => setShowMeta(!showMeta)}
              className="text-xs text-slate-400 hover:text-slate-600 transition-colors"
            >
              {showMeta ? '▲ Hide details' : '▼ Show pipeline details'}
            </button>

            {showMeta && (
              <div className="mt-1 p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs space-y-1.5">
                {/* Language Detection */}
                <div className="flex items-center gap-2">
                  <span className="text-slate-500 w-28 flex-shrink-0">🌐 Language:</span>
                  <span className="font-medium text-slate-700">
                    {message.metadata.detectedLanguage} ({message.metadata.languageCode})
                  </span>
                </div>

                {/* Translation Method */}
                <div className="flex items-center gap-2">
                  <span className="text-slate-500 w-28 flex-shrink-0">🔄 Translated via:</span>
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${methodInfo?.color}`}>
                    {methodInfo?.label}
                  </span>
                </div>

                {/* English Query (after translation) */}
                {message.metadata.languageCode !== 'en' && (
                  <div className="flex items-start gap-2">
                    <span className="text-slate-500 w-28 flex-shrink-0">📝 In English:</span>
                    <span className="text-slate-600 italic">"{message.metadata.englishQuery}"</span>
                  </div>
                )}

                {/* Rasa Intent */}
                <div className="flex items-center gap-2">
                  <span className="text-slate-500 w-28 flex-shrink-0">🎯 Intent:</span>
                  <span className="font-mono text-indigo-600 font-medium">{message.metadata.intent}</span>
                  <span className="text-slate-400">({(message.metadata.confidence * 100).toFixed(0)}%)</span>
                </div>

                {/* Processing Time */}
                <div className="flex items-center gap-2">
                  <span className="text-slate-500 w-28 flex-shrink-0">⚡ Time:</span>
                  <span className="text-slate-600">{message.metadata.processingTimeMs}ms</span>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
