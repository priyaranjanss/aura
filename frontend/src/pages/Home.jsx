import { useEffect, useRef, useState } from 'react';
import ChatWindow from '../components/ChatWindow';
import MicrophoneButton from '../components/MicrophoneButton';
import ConfirmationDialog from '../components/ConfirmationDialog';
import SettingsPanel from '../components/SettingsPanel';
import { useSpeech } from '../hooks/useSpeech';
import { useChatStore } from '../store/chatStore';

// One-tap example commands shown above the input box.
const QUICK_COMMANDS = [
  'What time is it',
  'Open Notepad',
  'Open YouTube',
  'Take a screenshot',
  'Search the web for cats',
  'Tell me a joke',
];

const STATUS_STYLES = {
  idle: { label: 'Idle', dot: 'bg-aura-border' },
  sleeping: { label: 'Sleeping… say “Hello” to wake up', dot: 'bg-aura-border' },
  listening: { label: 'Listening...', dot: 'bg-green-500' },
  thinking: { label: 'Thinking...', dot: 'bg-amber-500' },
  speaking: { label: 'Speaking...', dot: 'bg-aura-primary' },
};

// How long AURA stays awake after the wake word before sleeping again.
const AWAKE_MS = 8000;

export default function Home() {
  const [input, setInput] = useState('');
  const [listening, setListening] = useState(false);
  const [wakeMode, setWakeMode] = useState(false);
  const [micError, setMicError] = useState(null);
  const status = useChatStore((state) => state.status);
  const setStatus = useChatStore((state) => state.setStatus);
  const sendMessage = useChatStore((state) => state.sendMessage);
  const {
    supported,
    startListening,
    stopListening,
    startWakeListening,
    stopWakeListening,
  } = useSpeech();
  const wakeTimerRef = useRef(null);

  const sleepNow = () => {
    const current = useChatStore.getState().status;
    if (current === 'thinking' || current === 'speaking') {
      // Wait for the current reply to finish before sleeping.
      wakeTimerRef.current = setTimeout(sleepNow, 2000);
      return;
    }
    setStatus('sleeping');
  };

  const resetWakeTimer = () => {
    if (wakeTimerRef.current) clearTimeout(wakeTimerRef.current);
    wakeTimerRef.current = setTimeout(sleepNow, AWAKE_MS);
  };

  const handleWakeToggle = () => {
    if (!supported) return;

    if (wakeMode) {
      stopWakeListening();
      if (wakeTimerRef.current) clearTimeout(wakeTimerRef.current);
      setWakeMode(false);
      if (!listening) setStatus('idle');
      return;
    }

    setWakeMode(true);
    setMicError(null);
    setStatus('sleeping');
    resetWakeTimer();
    startWakeListening({
      onWake: () => {
        resetWakeTimer();
        setStatus('listening');
      },
      onCommand: (command) => {
        setInput(command);
        sendMessage(command);
        setInput('');
        resetWakeTimer(); // stay awake briefly for a follow-up
      },
      onError: () => {
        setWakeMode(false);
        setMicError(
          "AURA couldn't start listening. Check that the mic is allowed in the browser, " +
            "and that you're online (Chrome's speech recognition needs internet)."
        );
        setStatus('idle');
      },
    });
  };

  // While wake mode is on, return to 'Sleeping' after a reply finishes.
  useEffect(() => {
    if (wakeMode && status === 'idle') {
      setStatus('sleeping');
    }
  }, [wakeMode, status, setStatus]);

  // Cleanup continuous listening on unmount.
  useEffect(() => {
    return () => {
      stopWakeListening();
      if (wakeTimerRef.current) clearTimeout(wakeTimerRef.current);
    };
  }, [stopWakeListening]);

  const handleSubmit = (event) => {
    event.preventDefault();
    const text = input.trim();
    if (!text || status === 'thinking') return;
    sendMessage(text);
    setInput('');
  };

  const handleMicClick = () => {
    setMicError(null);
    if (!supported || status === 'thinking') return;

    // While wake mode is on, the mic button turns wake listening off instead.
    if (wakeMode) {
      handleWakeToggle();
      return;
    }

    if (listening) {
      stopListening();
      setListening(false);
      setStatus('idle');
      return;
    }

    setListening(true);
    setStatus('listening');
    startListening(
      (transcript) => {
        setInput(transcript); // briefly show what was heard
        sendMessage(transcript);
        setInput(''); // clear the input box after sending
      },
      () => {
        // Fired when recognition ends (after a result or on error).
        setListening(false);
        const current = useChatStore.getState().status;
        setStatus(current === 'thinking' ? current : 'idle');
      }
    );
  };

  const statusStyle = STATUS_STYLES[status] ?? STATUS_STYLES.idle;

  return (
    <main className="flex min-w-0 flex-1 flex-col">
      {/* Header */}
      <header className="flex items-center justify-between border-b border-aura-border px-8 py-4">
        <h2 className="text-2xl font-bold tracking-tight">AURA</h2>
        <span className="flex items-center gap-2 rounded-full border border-aura-border bg-aura-surface px-3 py-1 text-xs font-medium text-aura-text-secondary">
          <span className={`h-2 w-2 rounded-full ${statusStyle.dot}`} />
          {statusStyle.label}
        </span>
      </header>

      {/* Chat area */}
      <ChatWindow />

      {/* Quick command chips */}
      <div className="flex gap-2 overflow-x-auto px-8 pb-3 pt-2">
        {QUICK_COMMANDS.map((command) => (
          <button
            key={command}
            type="button"
            disabled={status === 'thinking'}
            onClick={() => sendMessage(command)}
            className="shrink-0 rounded-full border border-aura-border bg-aura-surface px-3 py-1.5 text-xs font-medium text-aura-text-secondary transition-colors hover:border-aura-primary hover:text-white disabled:cursor-not-allowed disabled:opacity-40"
          >
            {command}
          </button>
        ))}
      </div>

      {/* Input box */}
      <footer className="px-8 pb-6 pt-2">
        {micError && (
          <p className="mb-2 text-xs font-medium text-red-400">{micError}</p>
        )}
        <form
          onSubmit={handleSubmit}
          className="flex items-center gap-3 rounded-2xl border border-aura-border bg-aura-surface px-4 py-3 transition-colors focus-within:border-aura-primary"
        >
          {/* Wake word toggle */}
          <button
            type="button"
            onClick={handleWakeToggle}
            disabled={!supported}
            aria-pressed={wakeMode}
            title={
              wakeMode
                ? 'Wake word is on — click to turn off'
                : 'Wake word is off — click to turn on (say “Hello” to wake)'
            }
            className={`flex h-9 shrink-0 items-center gap-1.5 rounded-xl px-3 text-xs font-medium transition-colors ${
              wakeMode
                ? 'border border-green-500/40 bg-green-500/15 text-green-400'
                : 'border border-transparent bg-aura-surface-light text-aura-text-secondary hover:text-white'
            } disabled:cursor-not-allowed disabled:opacity-40`}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="h-4 w-4"
              aria-hidden="true"
            >
              <path d="M12 3a9 9 0 100 18 7 7 0 010-14 9 9 0 000-4z" />
            </svg>
            {wakeMode ? 'Wake: On' : 'Wake'}
          </button>

          <MicrophoneButton
            listening={listening}
            onClick={handleMicClick}
            disabled={!supported || status === 'thinking'}
          />
          <input
            type="text"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder={
              !supported
                ? 'Type a message… (microphone not supported in this browser)'
                : wakeMode
                  ? 'Wake mode on — say “Hello” to wake up…'
                  : 'Type a message or click the mic…'
            }
            className="min-w-0 flex-1 bg-transparent text-[15px] text-white placeholder:text-aura-text-secondary focus:outline-none"
          />
          <button
            type="submit"
            disabled={!input.trim() || status === 'thinking'}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-aura-primary text-white transition-colors hover:bg-aura-primary-hover disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:bg-aura-primary"
            aria-label="Send message"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="h-4 w-4"
            >
              <path d="M3.4 20.4l17.45-7.48a1 1 0 000-1.84L3.4 3.6a.993.993 0 00-1.39.91L2 9.12c0 .5.37.93.87.99L17 12 2.87 13.88c-.5.07-.87.5-.87 1l.01 4.61c0 .71.73 1.2 1.39.91z" />
            </svg>
          </button>
        </form>
      </footer>

      {/* Modals */}
      <ConfirmationDialog />
      <SettingsPanel />
    </main>
  );
}
