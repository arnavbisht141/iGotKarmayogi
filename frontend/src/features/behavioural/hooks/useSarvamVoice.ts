"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { fetchBlob } from "@/lib/api";

/**
 * The board member's voice: Sarvam AI text-to-speech through the backend, falling back to the
 * browser's built-in voice if Sarvam is unavailable. Playback stops on stop() and on unmount.
 */
export function useSarvamVoice() {
  const [speaking, setSpeaking] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const urlRef = useRef<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const stop = useCallback(() => {
    abortRef.current?.abort();
    abortRef.current = null;
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.removeAttribute("src");
      audioRef.current = null;
    }
    if (urlRef.current) {
      URL.revokeObjectURL(urlRef.current);
      urlRef.current = null;
    }
    if (typeof window !== "undefined") window.speechSynthesis?.cancel();
    setSpeaking(false);
  }, []);

  const speak = useCallback(
    async (text: string) => {
      stop();
      const controller = new AbortController();
      abortRef.current = controller;
      setSpeaking(true);
      try {
        const blob = await fetchBlob("/behavioural/speech/synthesize", {
          method: "POST",
          body: JSON.stringify({ text: text.slice(0, 2500) }),
          signal: controller.signal,
        });
        if (controller.signal.aborted) return;
        const url = URL.createObjectURL(blob);
        urlRef.current = url;
        const audio = new Audio(url);
        audioRef.current = audio;
        audio.onended = () => {
          setSpeaking(false);
          URL.revokeObjectURL(url);
          if (urlRef.current === url) urlRef.current = null;
        };
        await audio.play();
      } catch (err) {
        if (controller.signal.aborted) return;
        console.warn("Sarvam voice unavailable, using the browser voice:", err);
        if (!("speechSynthesis" in window)) {
          setSpeaking(false);
          return;
        }
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "en-IN";
        utterance.onend = () => setSpeaking(false);
        utterance.onerror = () => setSpeaking(false);
        window.speechSynthesis.speak(utterance);
      }
    },
    [stop],
  );

  useEffect(() => stop, [stop]);

  return { speaking, speak, stop };
}
