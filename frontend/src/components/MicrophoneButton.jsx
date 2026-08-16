// Large circular microphone button — pulses green while listening.
export default function MicrophoneButton({ listening, onClick, disabled }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      aria-label={listening ? 'Stop listening' : 'Start voice input'}
      title={listening ? 'Stop listening' : 'Speak to AURA'}
      className={`relative flex h-11 w-11 shrink-0 items-center justify-center rounded-full text-white transition-colors ${
        listening
          ? 'bg-green-500'
          : 'bg-aura-primary hover:bg-aura-primary-hover'
      } disabled:cursor-not-allowed disabled:opacity-40`}
    >
      {listening && (
        <span className="absolute inset-0 animate-ping rounded-full bg-green-500 opacity-50" />
      )}
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="currentColor"
        className="h-5 w-5"
        aria-hidden="true"
      >
        <path d="M12 14a3 3 0 003-3V6a3 3 0 10-6 0v5a3 3 0 003 3zm5-3a5 5 0 01-10 0H5a7 7 0 006 6.92V21h2v-3.08A7 7 0 0019 11h-2z" />
      </svg>
    </button>
  );
}
