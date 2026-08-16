// Chat state — messages, status, and the send action (Zustand).
import { create } from 'zustand';
import { sendChatMessage, deleteAudioFile, API_BASE_URL } from '../services/api';

const makeMessage = (role, content, extra = {}) => ({
  id: crypto.randomUUID(),
  role,
  content,
  ...extra,
});

export const useChatStore = create((set, get) => ({
  // List of { id, role: 'user'|'assistant', content, isError?, analysis? }
  messages: [],

  // 'idle' | 'listening' | 'thinking' | 'speaking'
  status: 'idle',

  // The audio element currently playing a spoken reply (kept so it isn't
  // garbage-collected before playback finishes).
  audio: null,

  /** Update the live status (used by the mic button). */
  setStatus: (status) => set({ status }),

  /**
   * Send a message to the backend, append the reply, play TTS audio, and
   * handle errors.
   * @param {string} text - the user's message
   */
  sendMessage: async (text) => {
    const trimmed = text.trim();
    if (!trimmed || get().status === 'thinking') return;

    set((state) => ({
      messages: [...state.messages, makeMessage('user', trimmed)],
      status: 'thinking',
    }));

    try {
      const data = await sendChatMessage(trimmed, get().messages);
      set((state) => ({
        messages: [
          ...state.messages,
          makeMessage('assistant', data.reply, {
            type: data.type,
            analysis: data.analysis,
            isError: data.success === false,
          }),
        ],
        status: data.audio_url ? 'speaking' : 'idle',
      }));

      if (data.audio_url) {
        // The backend returns a relative path (/static/audio/...) — absolutize
        // it against the backend so it plays in dev (frontend on :5173) and
        // when served by the backend itself.
        const absoluteUrl = data.audio_url.startsWith('http')
          ? data.audio_url
          : `${API_BASE_URL}${data.audio_url}`;
        const audio = new Audio(absoluteUrl);
        const finish = () => {
          set({ status: 'idle', audio: null });
          // The file was played (or failed) — tell the backend to delete it.
          deleteAudioFile(data.audio_url).catch(() => {});
        };
        audio.onended = finish;
        audio.onerror = finish;
        set({ audio });
        audio.play().catch(finish);
      }
    } catch (error) {
      console.error('[chat] request failed:', error);
      set((state) => ({
        messages: [
          ...state.messages,
          makeMessage(
            'assistant',
            "Sorry, I couldn't reach the backend. Make sure it's running on port 8001.",
            { isError: true }
          ),
        ],
        status: 'idle',
      }));
    }
  },

  /** Clear the conversation. */
  clearMessages: () => set({ messages: [], status: 'idle' }),
}));
