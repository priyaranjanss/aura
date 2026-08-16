import { useState } from 'react';

export default function Home() {
  const [input, setInput] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    // Chat wiring arrives in Phase 2 — for now the input is a visual shell.
  };

  return (
    <main className="flex min-w-0 flex-1 flex-col">
      {/* Header */}
      <header className="flex items-center justify-between border-b border-aura-border px-8 py-4">
        <h2 className="text-2xl font-bold tracking-tight">AURA</h2>
        <span className="flex items-center gap-2 rounded-full border border-aura-border bg-aura-surface px-3 py-1 text-xs font-medium text-aura-text-secondary">
          <span className="h-2 w-2 rounded-full bg-aura-border" />
          Idle
        </span>
      </header>

      {/* Empty chat area */}
      <section className="flex flex-1 flex-col items-center justify-center gap-4 px-8 text-center">
        <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-aura-surface text-3xl">
          ✨
        </div>
        <div>
          <h3 className="text-xl font-semibold">Hello, I'm AURA</h3>
          <p className="mt-1 text-sm text-aura-text-secondary">
            Ask me anything — type a message below to get started.
          </p>
        </div>
      </section>

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
            disabled={!input.trim()}
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
