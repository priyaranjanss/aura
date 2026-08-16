// Settings modal: spoken replies toggle, TTS language, clear chat.
import { useChatStore } from '../store/chatStore';

export default function SettingsPanel() {
  const settingsOpen = useChatStore((state) => state.settingsOpen);
  const setSettingsOpen = useChatStore((state) => state.setSettingsOpen);
  const voiceEnabled = useChatStore((state) => state.voiceEnabled);
  const setVoiceEnabled = useChatStore((state) => state.setVoiceEnabled);
  const lang = useChatStore((state) => state.lang);
  const setLang = useChatStore((state) => state.setLang);
  const clearMessages = useChatStore((state) => state.clearMessages);
  const messageCount = useChatStore((state) => state.messages.length);

  if (!settingsOpen) return null;

  return (
    <div className="modal-backdrop" role="dialog" aria-modal="true">
      <div className="w-full max-w-md rounded-2xl border border-aura-border bg-aura-surface p-6 shadow-2xl">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">Settings</h3>
          <button
            type="button"
            onClick={() => setSettingsOpen(false)}
            className="rounded-lg px-2 py-1 text-sm text-aura-text-secondary transition-colors hover:bg-aura-surface-light hover:text-white"
            aria-label="Close settings"
          >
            Close
          </button>
        </div>

        <div className="mt-5 space-y-5">
          {/* Spoken replies */}
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium">Spoken replies</p>
              <p className="text-xs text-aura-text-secondary">
                AURA reads its answers aloud
              </p>
            </div>
            <button
              type="button"
              role="switch"
              aria-checked={voiceEnabled}
              onClick={() => setVoiceEnabled(!voiceEnabled)}
              className={`relative h-6 w-11 rounded-full transition-colors ${
                voiceEnabled ? 'bg-aura-primary' : 'bg-aura-border'
              }`}
            >
              <span
                className={`absolute top-0.5 h-5 w-5 rounded-full bg-white transition-transform ${
                  voiceEnabled ? 'translate-x-5' : 'translate-x-0.5'
                }`}
              />
            </button>
          </div>

          {/* Language */}
          <div>
            <p className="mb-1.5 text-sm font-medium">Voice language</p>
            <div className="flex gap-2">
              {[
                { value: 'en', label: 'English' },
                { value: 'hi', label: 'Hindi' },
              ].map((option) => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => setLang(option.value)}
                  className={`rounded-xl px-3 py-1.5 text-sm font-medium transition-colors ${
                    lang === option.value
                      ? 'bg-aura-primary text-white'
                      : 'border border-aura-border text-aura-text-secondary hover:text-white'
                  }`}
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>

          {/* Clear chat */}
          <div className="border-t border-aura-border pt-4">
            <button
              type="button"
              disabled={messageCount === 0}
              onClick={() => {
                clearMessages();
                setSettingsOpen(false);
              }}
              className="w-full rounded-xl border border-aura-border px-4 py-2 text-sm font-medium text-aura-text-secondary transition-colors hover:bg-aura-surface-light hover:text-white disabled:cursor-not-allowed disabled:opacity-40"
            >
              Clear chat ({messageCount} messages)
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
