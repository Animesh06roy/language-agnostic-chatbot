/**
 * API utility functions
 * Communicates with the Django backend at localhost:8000
 */

import axios from 'axios';
import type { ChatRequest, ChatResponse } from '../types';

// Base URL for the Django backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create an axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

/**
 * Send a message to the chatbot backend.
 * The 10-step NLP pipeline runs on the server side.
 */
export async function sendMessage(message: string): Promise<ChatResponse> {
  const request: ChatRequest = { message };

  const response = await apiClient.post<ChatResponse>('/api/chat/', request);
  return response.data;
}

/**
 * Check if the backend is alive.
 * Returns true if the server responds, false otherwise.
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await apiClient.get('/api/chat/');
    return response.status === 200;
  } catch {
    return false;
  }
}
