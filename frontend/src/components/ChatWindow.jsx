// Scrollable message list: empty welcome state, bubbles, thinking indicator.
import { useEffect, useRef } from 'react';
import ChatBubble from './ChatBubble';
import { useChatStore } from '../store/chatStore';

export default function ChatWindow() {
  const messages = useChatStore((state) => state.messages);
  const status = useChatStore((state) => state.status);
  const bottomRef = useRef(null);

  // Keep the newest message in view.
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, status]);

  // Empty state — welcome message until the first exchange.
  if (messages.length === 0) {
    return (
      <section className="flex flex-1 flex-col items-center justify-center gap-4 px-8 text-center">
        <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-aura-surface">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
            className="h-8 w-8 text-aura-primary"
            aria-hidden="true"
          >
            <path d="M12 2l2.4 7.6L22 12l-7.6 2.4L12 22l-2.4-7.6L2 12l7.6-2.4L12 2z" />
          </svg>
        </div>
        <div>
          <h3 className="text-xl font-semibold">Hello, I&apos;m AURA</h3>
          <p className="mt-1 text-sm text-aura-text-secondary">
            Ask me anything — type a message below to get started.
          </p>
        </div>
      </section>
    );
  }

  return (
    <section className="flex-1 space-y-4 overflow-y-auto px-8 py-6">
      {messages.map((message) => (
        <ChatBubble key={message.id} message={message} />
      ))}

      {status === 'thinking' && (
        <div className="flex justify-start">
          <div className="rounded-2xl bg-aura-surface-light px-4 py-3 text-sm text-aura-text-secondary">
            Thinking...
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </section>
  );
}
