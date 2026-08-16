import { useState } from 'react';
import ChatWindow from '../components/ChatWindow';
import { useChatStore } from '../store/chatStore';

const STATUS_STYLES = {
  idle: { label: 'Idle', dot: 'bg-aura-border' },
  thinking: { label: 'Thinking...', dot: 'bg-amber-500' },
};

export default function Home() {
  const [input, setInput] = useState('');
  const status = useChatStore((state) => state.status);
  const sendMessage = useChatStore((state) => state.sendMessage);

  const handleSubmit = (event) => {
    event.preventDefault();
    const text = input.trim();
    if (!text || status === 'thinking') return;
    sendMessage(text);
    setInput('');
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

      {/* Input box */}
      <footer className="px-8 pb-6 pt-2">
        <form
          onSubmit={handleSubmit}
          className="flex items-center gap-3 rounded-2xl border border-aura-border bg-aura-surface px-4 py-3 transition-colors focus-within:border-aura-primary"
        >
          <input
            type="text"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Type a message…"
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
    </main>
  );
}
