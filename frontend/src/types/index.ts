/**
 * TypeScript type definitions for the Language Agnostic AI Chatbot
 */

/** A single message in the chat window */
export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  metadata?: MessageMetadata;
}

/** Extra info shown for bot messages (language, intent, etc.) */
export interface MessageMetadata {
  detectedLanguage: string;
  languageCode: string;
  intent: string;
  confidence: number;
  englishQuery: string;
  translationMethod: 'indicTrans' | 'googleTranslate' | 'none';
  processingTimeMs: number;
}

/** What we POST to the backend */
export interface ChatRequest {
  message: string;
}

/** What the backend returns */
export interface ChatResponse {
  response: string;
  detected_language: string;
  language_code: string;
  intent: string;
  confidence: number;
  entities: Entity[];
  english_query: string;
  translation_method: 'indicTrans' | 'googleTranslate' | 'none';
  processing_time_ms: number;
}

/** Rasa entity extracted from text */
export interface Entity {
  entity: string;
  value: string;
  confidence: number;
}

/** Badge color mapping for translation methods */
export type TranslationMethodDisplay = {
  label: string;
  color: string;
};
