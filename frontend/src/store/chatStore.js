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
  // List of { id, role: 'user'|'assistant', content, isError?, analysis?, image_url? }
  messages: [],

  // 'idle' | 'listening' | 'thinking' | 'speaking'
  status: 'idle',

  // The audio element currently playing a spoken reply (kept so it isn't
  // garbage-collected before playback finishes).
  audio: null,

  // Set when the backend asks for confirmation of a dangerous action.
  pendingConfirm: null, // { message, prompt }

  // Settings
  settingsOpen: false,
  voiceEnabled: true,
  lang: 'en',

  /** Update the live status (used by the mic button). */
  setStatus: (status) => set({ status }),

  /** Open/close the settings panel. */
  setSettingsOpen: (open) => set({ settingsOpen: open }),

  /** Toggle spoken replies on/off. */
  setVoiceEnabled: (enabled) => set({ voiceEnabled: enabled }),

  /** Change the TTS language ('en' | 'hi'). */
  setLang: (lang) => set({ lang }),

  /** Answer the pending confirmation dialog. */
  confirmPending: (confirmed) => {
    const { pendingConfirm } = get();
    if (!pendingConfirm) return;
    set({ pendingConfirm: null });
    if (confirmed) {
      get().sendMessage(pendingConfirm.message, { confirm: true });
    }
  },

  /**
   * Send a message to the backend, append the reply, play TTS audio, and
   * handle errors.
   * @param {string} text - the user's message
   * @param {{confirm?: boolean}} options - re-send after confirming a
   *   dangerous action
   */
  sendMessage: async (text, options = {}) => {
    const trimmed = text.trim();
    if (!trimmed || get().status === 'thinking') return;

    set((state) => ({
      messages: [...state.messages, makeMessage('user', trimmed)],
      status: 'thinking',
    }));

    try {
      const data = await sendChatMessage(trimmed, get().messages, {
        confirm: options.confirm ?? false,
        lang: get().lang,
      });

      // Dangerous action: the backend asks for confirmation first.
      if (data.requires_confirmation) {
        set((state) => ({
          messages: [
            ...state.messages,
            makeMessage('assistant', data.reply, {
              type: data.type,
              analysis: data.analysis,
            }),
          ],
          status: data.audio_url ? 'speaking' : 'idle',
          pendingConfirm: { message: trimmed, prompt: data.reply },
        }));
        if (data.audio_url && get().voiceEnabled) {
          get().playAudio(data.audio_url);
        }
        return;
      }

      set((state) => ({
        messages: [
          ...state.messages,
          makeMessage('assistant', data.reply, {
            type: data.type,
            analysis: data.analysis,
            isError: data.success === false,
            image_url: data.image_url,
          }),
        ],
        status: data.audio_url && get().voiceEnabled ? 'speaking' : 'idle',
      }));

      if (data.audio_url && get().voiceEnabled) {
        get().playAudio(data.audio_url);
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

  /**
   * Play a spoken reply. The backend returns a relative path
   * (/static/audio/...) — absolutize it against the backend so it plays in
   * dev (frontend on :5173) and when served by the backend itself.
   */
  playAudio: (audioUrl) => {
    const absoluteUrl = audioUrl.startsWith('http')
      ? audioUrl
      : `${API_BASE_URL}${audioUrl}`;
    const audio = new Audio(absoluteUrl);
    const finish = () => {
      set({ status: 'idle', audio: null });
      // The file was played (or failed) — tell the backend to delete it.
      deleteAudioFile(audioUrl).catch(() => {});
    };
    audio.onended = finish;
    audio.onerror = finish;
    set({ audio });
    audio.play().catch(finish);
  },

  /** Clear the conversation. */
  clearMessages: () => set({ messages: [], status: 'idle', pendingConfirm: null }),
}));
