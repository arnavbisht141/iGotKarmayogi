"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { ApiError, uploadApi } from "@/lib/api";

// Sarvam's synchronous speech-to-text handles clips up to about 30 seconds, so answers are recorded in segments.
const SEGMENT_MS = 20000;
const MIN_CLIP_BYTES = 1500;

function pickMimeType(): string | null {
  if (typeof window === "undefined" || typeof MediaRecorder === "undefined") return null;
  return (
    ["audio/webm;codecs=opus", "audio/webm", "audio/mp4", "audio/ogg;codecs=opus"].find((type) =>
      MediaRecorder.isTypeSupported(type),
    ) ?? ""
  );
}

function wordCount(text: string) {
  return text.trim().split(/\s+/).filter(Boolean).length;
}

function join(a: string, b: string) {
  return [a.trim(), b.trim()].filter(Boolean).join(" ");
}

/**
 * Dictation with Sarvam AI speech-to-text: records the microphone in short segments, transcribes each
 * one through the backend as the officer keeps speaking, and appends the text to the answer.
 */
export function useSarvamDictation(onText: (text: string) => void, getStream: () => MediaStream | null) {
  const [supported, setSupported] = useState(false);
  const [listening, setListening] = useState(false);
  const [pending, setPending] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [unavailable, setUnavailable] = useState(false);

  const onTextRef = useRef(onText);
  const getStreamRef = useRef(getStream);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const ownStreamRef = useRef<MediaStream | null>(null);
  const timerRef = useRef<number | null>(null);
  const wantRef = useRef(false);
  const baseTextRef = useRef("");
  const segmentsRef = useRef<string[]>([]);
  const queueRef = useRef<Promise<void>>(Promise.resolve());
  const dictatedWordsRef = useRef(0);
  // Bumped when an answer is taken or the component unmounts, so late transcripts are dropped.
  const generationRef = useRef(0);

  useEffect(() => {
    onTextRef.current = onText;
    getStreamRef.current = getStream;
  });

  useEffect(() => {
    setSupported(pickMimeType() !== null && Boolean(navigator.mediaDevices?.getUserMedia));
  }, []);

  const transcribeClip = useCallback((blob: Blob, generation: number) => {
    setPending((n) => n + 1);
    queueRef.current = queueRef.current.then(async () => {
      try {
        const extension = blob.type.includes("mp4") ? "m4a" : blob.type.includes("ogg") ? "ogg" : "webm";
        const form = new FormData();
        form.append("file", blob, `answer.${extension}`);
        form.append("language_code", "en-IN");
        const res = await uploadApi<{ transcript: string }>("/behavioural/speech/transcribe", form);
        if (generation !== generationRef.current || !res.transcript) return;
        segmentsRef.current.push(res.transcript);
        dictatedWordsRef.current += wordCount(res.transcript);
        onTextRef.current(join(baseTextRef.current, segmentsRef.current.join(" ")));
      } catch (err) {
        if (generation !== generationRef.current) return;
        if (err instanceof ApiError && err.status === 503) setUnavailable(true);
        setError(err instanceof Error ? err.message : "Part of your answer could not be transcribed.");
      } finally {
        setPending((n) => Math.max(0, n - 1));
      }
    });
  }, []);

  const recordSegment = useCallback(
    (stream: MediaStream, generation: number) => {
      const mimeType = pickMimeType();
      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      const chunks: Blob[] = [];
      recorder.ondataavailable = (event) => {
        if (event.data.size) chunks.push(event.data);
      };
      recorder.onstop = () => {
        if (timerRef.current !== null) {
          window.clearTimeout(timerRef.current);
          timerRef.current = null;
        }
        const blob = new Blob(chunks, { type: recorder.mimeType || "audio/webm" });
        if (blob.size >= MIN_CLIP_BYTES) transcribeClip(blob, generation);
        if (wantRef.current && generation === generationRef.current) recordSegment(stream, generation);
      };
      recorderRef.current = recorder;
      recorder.start();
      timerRef.current = window.setTimeout(() => {
        if (recorder.state === "recording") recorder.stop();
      }, SEGMENT_MS);
    },
    [transcribeClip],
  );

  const stopRecording = useCallback(() => {
    wantRef.current = false;
    const recorder = recorderRef.current;
    recorderRef.current = null;
    if (recorder && recorder.state !== "inactive") recorder.stop();
    ownStreamRef.current?.getTracks().forEach((track) => track.stop());
    ownStreamRef.current = null;
    setListening(false);
  }, []);

  const start = useCallback(
    async (currentText: string) => {
      if (wantRef.current) return;
      setError(null);
      baseTextRef.current = currentText.trim();
      segmentsRef.current = [];
      let stream = getStreamRef.current();
      if (!stream || !stream.getAudioTracks().some((track) => track.readyState === "live" && track.enabled)) {
        try {
          stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true } });
          ownStreamRef.current = stream;
        } catch {
          setError("Microphone access was blocked, so dictation is unavailable. You can type your answer.");
          return;
        }
      }
      wantRef.current = true;
      setListening(true);
      recordSegment(new MediaStream(stream.getAudioTracks()), generationRef.current);
    },
    [recordSegment],
  );

  /** Stops recording and resolves with the full answer text once the last clip is transcribed. */
  const finish = useCallback(async () => {
    const generation = generationRef.current;
    const recorder = recorderRef.current;
    const stopped = new Promise<void>((resolve) => {
      if (recorder && recorder.state !== "inactive") recorder.addEventListener("stop", () => resolve(), { once: true });
      else resolve();
    });
    stopRecording();
    await stopped;
    await queueRef.current;
    return generation === generationRef.current ? join(baseTextRef.current, segmentsRef.current.join(" ")) : "";
  }, [stopRecording]);

  const takeDictatedWords = useCallback(() => {
    const words = dictatedWordsRef.current;
    dictatedWordsRef.current = 0;
    segmentsRef.current = [];
    baseTextRef.current = "";
    generationRef.current += 1;
    return words;
  }, []);

  useEffect(
    () => () => {
      generationRef.current += 1;
      stopRecording();
    },
    [stopRecording],
  );

  return {
    supported,
    listening,
    busy: pending > 0,
    error,
    unavailable,
    start,
    stop: stopRecording,
    finish,
    takeDictatedWords,
  };
}
