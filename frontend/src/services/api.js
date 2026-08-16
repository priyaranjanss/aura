// API service — all backend calls go through this module.
import axios from 'axios';

// Backend origin. The API and TTS audio live here; responses carry relative
// audio paths (/static/audio/...), which callers absolutize against this.
export const API_BASE_URL = 'http://127.0.0.1:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

/**
 * Send a user message to the backend chat endpoint.
 * @param {string} message - the user's text
 * @param {Array<{role: string, content: string}>} history - prior messages
 * @returns {Promise<{reply: string, type: string, success: boolean, audio_url: ?string}>}
 */
export async function sendChatMessage(message, history = [], options = {}) {
  const { confirm = false, lang = 'en' } = options;
  const { data } = await api.post('/api/chat', {
    message,
    history: history.map((m) => ({ role: m.role, content: m.content })),
    confirm,
    lang,
  });
  return data;
}

/**
 * Tell the backend the audio file was played so it can delete it.
 * @param {string} audioUrl - the audio_url from a chat reply
 */
export async function deleteAudioFile(audioUrl) {
  const filename = audioUrl.split('/').pop();
  await api.delete(`/api/audio/${filename}`);
}
