// Renders one chat message: user on the right (indigo), assistant on the left.
export default function ChatBubble({ message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[75%] whitespace-pre-wrap rounded-2xl px-4 py-3 text-[15px] leading-relaxed ${
          isUser
            ? 'bg-aura-primary text-white'
            : message.isError
              ? 'border border-aura-border bg-aura-surface text-aura-text-secondary'
              : 'bg-aura-surface-light text-white'
        }`}
      >
        {message.content}
      </div>
    </div>
  );
}
