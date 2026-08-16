export default function Sidebar() {
  return (
    <aside className="flex w-64 shrink-0 flex-col border-r border-aura-border bg-aura-surface">
      {/* Brand */}
      <div className="flex items-center gap-3 px-6 py-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-aura-primary text-lg font-bold text-white shadow-lg shadow-aura-primary/30">
          A
        </div>
        <div>
          <h1 className="text-lg font-bold leading-tight tracking-tight">AURA</h1>
          <p className="text-xs text-aura-text-secondary">Voice Assistant</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3">
        <button
          type="button"
          className="flex w-full items-center gap-3 rounded-lg bg-aura-surface-light px-3 py-2.5 text-sm font-medium text-white"
        >
          <span className="h-2 w-2 rounded-full bg-aura-primary" />
          Chat
        </button>
        <button
          type="button"
          className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-aura-text-secondary transition-colors hover:bg-aura-surface-light hover:text-white"
          title="Coming soon"
        >
          <span className="h-2 w-2 rounded-full bg-aura-border" />
          Settings
          <span className="ml-auto rounded-full bg-aura-border px-2 py-0.5 text-[10px] font-medium text-aura-text-secondary">
            soon
          </span>
        </button>
      </nav>

      {/* Footer */}
      <div className="border-t border-aura-border px-6 py-4">
        <p className="text-xs text-aura-text-secondary">v0.1.0 · Phase 1</p>
      </div>
    </aside>
  );
}
