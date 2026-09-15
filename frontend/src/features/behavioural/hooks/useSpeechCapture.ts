"use client";

import { useCallback, useEffect, useRef, useState } from "react";

const FILLER_PATTERN = /\b(um+|uh+|erm+|hmm+|you know|i mean|sort of|kind of|basically)\b/gi;

export function countFillers(text: string) {
  return text.match(FILLER_PATTERN)?.length ?? 0;
}

function wordCount(text: string) {
  return text.trim().split(/\s+/).filter(Boolean).length;
}

function join(a: string, b: string) {
  return [a.trim(), b.trim()].filter(Boolean).join(" ");
}

interface RecognitionResult {
  isFinal: boolean;
  0: { transcript: string };
}

interface Recognition {
  lang: string;
  continuous: boolean;
  interimResults: boolean;
  start(): void;
  stop(): void;
  abort(): void;
  onresult: ((event: { results: ArrayLike<RecognitionResult> }) => void) | null;
  onerror: ((event: { error: string }) => void) | null;
  onend: (() => void) | null;
}

function recognitionClass(): (new () => Recognition) | null {
  if (typeof window === "undefined") return null;
  const w = window as unknown as {
    SpeechRecognition?: new () => Recognition;
    webkitSpeechRecognition?: new () => Recognition;
  };
  return w.SpeechRecognition ?? w.webkitSpeechRecognition ?? null;
}

/**
 * Browser dictation for interview answers. Keeps listening across Chrome's automatic stops after
 * silence, appends to what the officer already typed, and counts dictated words for pace.
 */
export function useSpeechCapture(onText: (text: string) => void) {
  const [supported, setSupported] = useState(false);
  const [listening, setListening] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const recognitionRef = useRef<Recognition | null>(null);
  const wantListeningRef = useRef(false);
  const baseTextRef = useRef("");
  const sessionTextRef = useRef("");
  const dictatedWordsRef = useRef(0);
  const sessionWordsRef = useRef(0);
  const onTextRef = useRef(onText);

  useEffect(() => {
    onTextRef.current = onText;
  });

  useEffect(() => {
    setSupported(recognitionClass() !== null);
  }, []);

  const begin = useCallback(() => {
    const Recognizer = recognitionClass();
    if (!Recognizer) return;
    const recognition = new Recognizer();
    recognition.lang = "en-IN";
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = (event) => {
      let finalText = "";
      let interim = "";
      for (let i = 0; i < event.results.length; i++) {
        const result = event.results[i];
        if (result.isFinal) finalText += `${result[0].transcript} `;
        else interim += `${result[0].transcript} `;
      }
      sessionWordsRef.current = wordCount(finalText);
      sessionTextRef.current = `${finalText}${interim}`.trim();
      onTextRef.current(join(baseTextRef.current, sessionTextRef.current));
    };

    recognition.onerror = (event) => {
      if (event.error === "no-speech" || event.error === "aborted") return;
      wantListeningRef.current = false;
      setError(
        event.error === "not-allowed" || event.error === "service-not-allowed"
          ? "Dictation was blocked by the browser. You can type your answer instead."
          : `Dictation stopped (${event.error}). Select Dictate answer to try again, or type.`,
      );
    };

    recognition.onend = () => {
      dictatedWordsRef.current += sessionWordsRef.current;
      sessionWordsRef.current = 0;
      baseTextRef.current = join(baseTextRef.current, sessionTextRef.current);
      sessionTextRef.current = "";
      recognitionRef.current = null;
      // Chrome ends recognition after a stretch of silence; keep going while the officer is still answering.
      if (wantListeningRef.current) begin();
      else setListening(false);
    };

    recognitionRef.current = recognition;
    try {
      recognition.start();
      setListening(true);
    } catch {
      recognitionRef.current = null;
      wantListeningRef.current = false;
      setListening(false);
    }
  }, []);

  const start = useCallback(
    (currentText: string) => {
      if (recognitionRef.current) return;
      setError(null);
      baseTextRef.current = currentText.trim();
      sessionTextRef.current = "";
      wantListeningRef.current = true;
      begin();
    },
    [begin],
  );

  const stop = useCallback(() => {
    wantListeningRef.current = false;
    recognitionRef.current?.stop();
    setListening(false);
  }, []);

  const takeDictatedWords = useCallback(() => {
    const words = dictatedWordsRef.current + sessionWordsRef.current;
    dictatedWordsRef.current = 0;
    sessionWordsRef.current = 0;
    return words;
  }, []);

  useEffect(
    () => () => {
      wantListeningRef.current = false;
      recognitionRef.current?.abort();
    },
    [],
  );

  return { supported, listening, error, start, stop, takeDictatedWords };
}
