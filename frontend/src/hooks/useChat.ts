/**
 * useChat — Custom hook for chatbot state management
 *
 * Manages:
 * - Message history
 * - Loading state while waiting for bot response
 * - Error state
 * - Sending messages to the backend
 */

import { useState, useCallback } from 'react';
import type { Message, ChatResponse } from '../types';
import { sendMessage } from '../utils/api';

// Generate a simple unique ID for each message
const generateId = () => `msg_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;

// The welcome message shown at the start
const WELCOME_MESSAGE: Message = {
  id: 'welcome',
  text: '🎓 Welcome! I am the Smart India Hackathon Education Chatbot. Ask me anything about admissions, fees, hostel, exams, scholarships, and more! You can ask in English, Hindi, Tamil, Telugu, or any supported Indian language.',
  sender: 'bot',
  timestamp: new Date(),
};

export function useChat() {
  // All messages in the conversation
  const [messages, setMessages] = useState<Message[]>([WELCOME_MESSAGE]);

  // Is a request in progress?
  const [isLoading, setIsLoading] = useState(false);

  // Error message to show if request fails
  const [error, setError] = useState<string | null>(null);

  /**
   * Send a user message and get a bot response.
   * Implements the full 10-step pipeline via the backend.
   */
  const sendUserMessage = useCallback(async (text: string) => {
    if (!text.trim() || isLoading) return;

    // Clear any previous error
    setError(null);

    // Add user's message to chat immediately
    const userMessage: Message = {
      id: generateId(),
      text: text.trim(),
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Call the Django backend — 10-step pipeline runs here
      const response: ChatResponse = await sendMessage(text.trim());

      // Build the bot message with metadata
      const botMessage: Message = {
        id: generateId(),
        text: response.response,
        sender: 'bot',
        timestamp: new Date(),
        metadata: {
          detectedLanguage: response.detected_language,
          languageCode: response.language_code,
          intent: response.intent,
          confidence: response.confidence,
          englishQuery: response.english_query,
          translationMethod: response.translation_method,
          processingTimeMs: response.processing_time_ms,
        },
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      // Show error in chat
      const errorMessage: Message = {
        id: generateId(),
        text: '⚠️ Could not connect to the server. Make sure the Django backend is running on port 8000.',
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
      setError('Backend not reachable. Run: python manage.py runserver');
    } finally {
      setIsLoading(false);
    }
  }, [isLoading]);

  /** Clear all messages and start fresh */
  const clearChat = useCallback(() => {
    setMessages([WELCOME_MESSAGE]);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendUserMessage,
    clearChat,
  };
}
