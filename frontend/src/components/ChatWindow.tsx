/**
 * ChatWindow — The scrollable area that displays all messages
 */

import { useEffect, useRef } from 'react';
import type { Message } from '../types';
import { MessageBubble } from './MessageBubble';
import { LoadingSpinner } from './LoadingSpinner';

interface Props {
  messages: Message[];
  isLoading: boolean;
}

export function ChatWindow({ messages, isLoading }: Props) {
  // Reference to the bottom of the message list for auto-scrolling
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom whenever new messages arrive
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto p-4 chat-scroll bg-slate-50">
      {/* Render each message */}
      {messages.map(message => (
        <MessageBubble key={message.id} message={message} />
      ))}

      {/* Loading indicator while bot is processing */}
      {isLoading && (
        <div className="flex justify-start mb-3">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-full bg-slate-700 flex items-center justify-center text-xs font-bold text-white flex-shrink-0">
              AI
            </div>
            <div className="bg-white border border-slate-200 rounded-2xl rounded-tl-sm shadow-sm">
              <LoadingSpinner />
            </div>
          </div>
        </div>
      )}

      {/* Invisible element at the bottom for scrolling */}
      <div ref={bottomRef} />
    </div>
  );
}
