// Renders one chat message: user on the right (indigo), assistant on the left.
// Assistant replies lead with the request analysis (What/When/Who/How/...).
export default function ChatBubble({ message }) {
  const isUser = message.role === 'user';
  const analysis = message.analysis ?? [];

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3 text-[15px] leading-relaxed ${
          isUser
            ? 'bg-aura-primary text-white'
            : message.isError
              ? 'border border-aura-border bg-aura-surface text-aura-text-secondary'
              : 'bg-aura-surface-light text-white'
        }`}
      >
        {!isUser && analysis.length > 0 && (
          <div className="mb-3 rounded-xl border border-aura-border bg-aura-bg/50 px-3 py-2">
            <p className="mb-1.5 text-[11px] font-semibold uppercase tracking-wide text-aura-text-secondary">
              Request analysis
            </p>
            <div className="grid grid-cols-1 gap-x-6 gap-y-0.5 sm:grid-cols-2">
              {analysis.map((item) => (
                <p key={item.question} className="text-[12px] leading-relaxed">
                  <span className="font-medium text-aura-text-secondary">
                    {item.question}:
                  </span>{' '}
                  <span
                    className={
                      item.answer === 'Not needed'
                        ? 'text-aura-text-secondary/70'
                        : 'text-white'
                    }
                  >
                    {item.answer}
                  </span>
                </p>
              ))}
            </div>
          </div>
        )}
        <div className="whitespace-pre-wrap">{message.content}</div>
      </div>
    </div>
  );
}
