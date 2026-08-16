// Web Speech API wrapper — speech-to-text (Chrome/Edge).
// Provides one-shot listening (click mic) and continuous wake-word listening
// ("Hey AURA" → then the next utterance is the command, then back to sleep).
import { useCallback, useRef, useState } from 'react';

export const WAKE_PHRASES = [
  'hello aura',
  'hey aura',
  'hi aura',
  'okay aura',
  'ok aura',
  'hello',
  'hey',
  'hi',
];

export function useSpeech() {
  const [supported] = useState(() => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    return Boolean(SR);
  });

  const recognitionRef = useRef(null);
  const wakeRef = useRef(null);
  const wakeActiveRef = useRef(false);
  const wakeStateRef = useRef('sleeping'); // 'sleeping' | 'awake'

  const getRecognition = () => window.SpeechRecognition || window.webkitSpeechRecognition;

  // --- One-shot listening (click the mic) -------------------------------
  const startListening = useCallback((onResult, onEnd) => {
    const SR = getRecognition();
    if (!SR) return;
    const recognition = new SR();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript.trim();
      if (transcript) onResult?.(transcript);
    };
    recognition.onend = () => onEnd?.();
    recognition.onerror = () => onEnd?.();

    recognitionRef.current = recognition;
    recognition.start();
  }, []);

  const stopListening = useCallback(() => {
    recognitionRef.current?.stop();
  }, []);

  // --- Continuous wake-word listening ------------------------------------
  const startWakeListening = useCallback(({ onWake, onCommand, onError }) => {
    const SR = getRecognition();
    if (!SR) return;

    const recognition = new SR();
    recognition.lang = 'en-US';
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    // Stop wake listening and surface the failure to the UI (never silent).
    const fail = () => {
      wakeActiveRef.current = false;
      onError?.();
    };

    recognition.onresult = (event) => {
      let text = '';
      let isFinal = false;
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const r = event.results[i];
        text += ` ${r[0].transcript.trim()}`;
        if (r.isFinal) isFinal = true;
      }
      const transcript = text.trim().toLowerCase();
      if (!transcript) return;

      if (wakeStateRef.current === 'sleeping') {
        if (WAKE_PHRASES.some((phrase) => transcript.includes(phrase))) {
          wakeStateRef.current = 'awake';
          onWake?.();
        }
        return;
      }

      // Awake: strip the wake phrase (if present) and capture the command.
      let cleaned = transcript;
      for (const phrase of WAKE_PHRASES) {
        const idx = cleaned.indexOf(phrase);
        if (idx !== -1) cleaned = cleaned.slice(idx + phrase.length);
      }
      cleaned = cleaned.trim();
      // Only act on final results so partial transcripts aren't sent.
      if (cleaned && isFinal) {
        onCommand?.(cleaned);
        wakeStateRef.current = 'sleeping'; // one command per wake
      }
    };

    // The browser can drop the mic after silence — restart to keep listening.
    recognition.onend = () => {
      if (wakeActiveRef.current) {
        setTimeout(() => {
          if (wakeActiveRef.current) {
            try {
              recognition.start();
            } catch {
              /* already starting */
            }
          }
        }, 300);
      }
    };
    recognition.onerror = (event) => {
      const err = event && event.error;
      // Real failures: permission denied or the network request failed
      // (Chrome streams speech to its servers, so it needs internet).
      if (
        err === 'not-allowed' ||
        err === 'service-not-allowed' ||
        err === 'network' ||
        err === 'audio-capture'
      ) {
        fail();
      }
      // 'no-speech' and 'aborted' are normal in continuous mode — keep listening.
    };

    wakeActiveRef.current = true;
    wakeStateRef.current = 'sleeping';
    wakeRef.current = recognition;
    try {
      recognition.start();
    } catch {
      // Chrome throws synchronously when the mic was previously denied.
      fail();
    }
  }, []);

  const stopWakeListening = useCallback(() => {
    wakeActiveRef.current = false;
    wakeStateRef.current = 'sleeping';
    try {
      wakeRef.current?.stop();
    } catch {
      /* ignored */
    }
    wakeRef.current = null;
  }, []);

  return {
    supported,
    startListening,
    stopListening,
    startWakeListening,
    stopWakeListening,
  };
}
