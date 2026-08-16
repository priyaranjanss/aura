// Confirmation modal for dangerous actions (lock/shutdown/restart).
import { useChatStore } from '../store/chatStore';

export default function ConfirmationDialog() {
  const pendingConfirm = useChatStore((state) => state.pendingConfirm);
  const confirmPending = useChatStore((state) => state.confirmPending);

  if (!pendingConfirm) return null;

  return (
    <div className="modal-backdrop" role="dialog" aria-modal="true">
      <div className="w-full max-w-md rounded-2xl border border-aura-border bg-aura-surface p-6 shadow-2xl">
        <h3 className="text-lg font-semibold">Confirm action</h3>
        <p className="mt-2 text-sm leading-relaxed text-aura-text-secondary">
          {pendingConfirm.prompt}
        </p>
        <div className="mt-6 flex justify-end gap-3">
          <button
            type="button"
            onClick={() => confirmPending(false)}
            className="rounded-xl border border-aura-border px-4 py-2 text-sm font-medium text-aura-text-secondary transition-colors hover:bg-aura-surface-light hover:text-white"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={() => confirmPending(true)}
            className="rounded-xl bg-red-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-red-600"
          >
            Yes, do it
          </button>
        </div>
      </div>
    </div>
  );
}
