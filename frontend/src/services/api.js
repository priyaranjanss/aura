// API service — all backend calls go through this module.
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8001',
  timeout: 30000,
});

/**
 * Send a user message to the backend chat endpoint.
 * @param {string} message - the user's text
 * @param {Array<{role: string, content: string}>} history - prior messages
 * @returns {Promise<{reply: string, type: string, success: boolean, audio_url: ?string}>}
 */
export async function sendChatMessage(message, history = []) {
  const { data } = await api.post('/api/chat', {
    message,
    history: history.map((m) => ({ role: m.role, content: m.content })),
  });
  return data;
}
