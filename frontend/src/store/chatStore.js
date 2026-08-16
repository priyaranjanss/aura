// Chat state — messages, status, and the send action (Zustand).
import { create } from 'zustand';
import { sendChatMessage } from '../services/api';

const makeMessage = (role, content, extra = {}) => ({
  id: crypto.randomUUID(),
  role,
  content,
  ...extra,
});

export const useChatStore = create((set, get) => ({
  // List of { id, role: 'user'|'assistant', content, isError? }
  messages: [],

  // 'idle' | 'thinking'
  status: 'idle',

  /**
   * Send a message to the backend, append the reply, and handle errors.
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
        status: 'idle',
      }));
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
