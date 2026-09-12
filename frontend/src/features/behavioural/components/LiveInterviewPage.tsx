"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import {
  Video,
  VideoOff,
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Clock,
  Award,
  CheckCircle2,
  AlertCircle,
  Play,
  Square,
  Send,
  Sparkles,
  ShieldCheck,
  RotateCcw,
  Printer,
  ChevronRight,
  TrendingUp,
  UserCheck,
  Brain,
  MessageSquare
} from "lucide-react";
import { fetchApi } from "@/lib/api";

interface CompetencyScore {
  competency_name: string;
  score_percent: number;
  rating_band: string;
  key_evidence: string;
  growth_opportunity: string;
}

interface TranscriptEntry {
  speaker: string;
  content: string;
  timestamp_seconds: number;
  behavioral_tags: string[];
}

interface InterviewAnalysisResponse {
  session_id: string;
  course_id: number;
  course_title: string;
  officer_name: string;
  total_duration_formatted: string;
  total_turns: number;
  overall_score_percent: number;
  overall_rating_band: string;
  executive_summary: string;
  competency_scores: Record<string, CompetencyScore>;
  core_strengths: string[];
  priority_development_areas: string[];
  recommended_apar_actions: string[];
  transcript: TranscriptEntry[];
}

const COMPETENCY_ORDER = [
  "Course Knowledge",
  "Leadership",
  "Communication",
  "Project Management",
  "Ethics",
  "Decision Making",
  "Change Management"
];

function CompetencyRadar({ scores }: { scores: Record<string, CompetencyScore> }) {
  const size = 280;
  const cx = size / 2;
  const cy = size / 2;
  const radius = 96;
  const axes = COMPETENCY_ORDER.filter((name) => scores[name]);
  const points = axes.map((name, i) => {
    const angle = (Math.PI * 2 * i) / axes.length - Math.PI / 2;
    const mag = Math.max(0, Math.min(100, scores[name].score_percent)) / 100;
    return {
      name,
      x: cx + Math.cos(angle) * radius * mag,
      y: cy + Math.sin(angle) * radius * mag,
      lx: cx + Math.cos(angle) * (radius + 22),
      ly: cy + Math.sin(angle) * (radius + 22)
    };
  });
  const polygon = points.map((p) => `${p.x},${p.y}`).join(" ");
  const rings = [0.4, 0.7, 1];

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="mx-auto h-64 w-64" role="img" aria-label="Competency radar chart">
      {rings.map((r) => (
        <polygon
          key={r}
          fill="none"
          stroke="#1e293b"
          strokeWidth="1"
          points={axes
            .map((_, i) => {
              const angle = (Math.PI * 2 * i) / axes.length - Math.PI / 2;
              return `${cx + Math.cos(angle) * radius * r},${cy + Math.sin(angle) * radius * r}`;
            })
            .join(" ")}
        />
      ))}
      {points.map((p, i) => {
        const angle = (Math.PI * 2 * i) / axes.length - Math.PI / 2;
        return (
          <line
            key={p.name}
            x1={cx}
            y1={cy}
            x2={cx + Math.cos(angle) * radius}
            y2={cy + Math.sin(angle) * radius}
            stroke="#334155"
          />
        );
      })}
      <polygon points={polygon} fill="rgba(13,148,136,0.35)" stroke="#14b8a6" strokeWidth="2" />
      {points.map((p) => (
        <text
          key={p.name}
          x={p.lx}
          y={p.ly}
          textAnchor="middle"
          className="fill-slate-400"
          fontSize="8"
        >
          {p.name.replace(" Management", " Mgmt")}
        </text>
      ))}
    </svg>
  );
}

const COURSES = [
  { id: 1, title: "Fundamentals of National Sample Surveys (NSS)", org: "NSSO" },
  { id: 2, title: "Compilation of Consumer Price Index (CPI) & Inflation Metrics", org: "CSO" },
  { id: 3, title: "Data Quality Frameworks & Official Statistics in India", org: "NSSTA" },
  { id: 4, title: "Digital Governance & Public Financial Management System (PFMS)", org: "ISTM" },
  { id: 5, title: "Python and Statistical Computing for Public Policy", org: "MoSPI Data Lab" }
];

export default function LiveInterviewPage() {
  // Setup State
  const [selectedCourseId, setSelectedCourseId] = useState<number>(1);
  const [officerName, setOfficerName] = useState<string>("Rajesh Kumar");
  const [targetDuration, setTargetDuration] = useState<number>(30); // 25-35 minutes
  const [isInterviewActive, setIsInterviewActive] = useState<boolean>(false);
  const [sessionId, setSessionId] = useState<string | null>(null);

  // Live Media Feed State
  const [cameraActive, setCameraActive] = useState<boolean>(true);
  const [micActive, setMicActive] = useState<boolean>(true);
  const [voiceEnabled, setVoiceEnabled] = useState<boolean>(true);
  const [audioLevel, setAudioLevel] = useState<number>(0);
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const animFrameRef = useRef<number | null>(null);

  // Speech Recognition State
  const [isListening, setIsListening] = useState<boolean>(false);
  const [speechSupported, setSpeechSupported] = useState<boolean>(false);
  const recognitionRef = useRef<any>(null);

  // Interview Progression & Pacing
  const [elapsedSeconds, setElapsedSeconds] = useState<number>(0);
  const [currentTurn, setCurrentTurn] = useState<number>(1);
  const [currentPhase, setCurrentPhase] = useState<string>("Phase 1: Foundational Subject Matter & Conceptual Rigor");
  const [targetCompetency, setTargetCompetency] = useState<string>("Course Knowledge");
  const [currentAiQuestion, setCurrentAiQuestion] = useState<string>("");
  const [officerInputText, setOfficerInputText] = useState<string>("");
  const [isSubmittingTurn, setIsSubmittingTurn] = useState<boolean>(false);
  const [pacingAdvice, setPacingAdvice] = useState<string>("");
  const [liveTranscript, setLiveTranscript] = useState<TranscriptEntry[]>([]);

  // End of Interview State
  const [isConcluded, setIsConcluded] = useState<boolean>(false);
  const [analysisReport, setAnalysisReport] = useState<InterviewAnalysisResponse | null>(null);
  const [isLoadingAnalysis, setIsLoadingAnalysis] = useState<boolean>(false);

  // Sync course selection from URL query if navigated from a course page
  useEffect(() => {
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      const cId = params.get("courseId");
      if (cId) {
        const parsed = parseInt(cId, 10);
        if (!isNaN(parsed) && parsed >= 1 && parsed <= 5) {
          setSelectedCourseId(parsed);
        }
      }
    }
  }, []);

  // Initialize Media Stream (Camera & Mic)
  useEffect(() => {
    let stream: MediaStream | null = null;

    async function setupMedia() {
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: { width: 640, height: 480, facingMode: "user" },
          audio: true
        });
        mediaStreamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }

        // Setup Audio Analyser for realistic audio visualizer
        try {
          const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
          const audioCtx = new AudioContextClass();
          audioContextRef.current = audioCtx;
          const source = audioCtx.createMediaStreamSource(stream);
          const analyser = audioCtx.createAnalyser();
          analyser.fftSize = 64;
          source.connect(analyser);
          analyserRef.current = analyser;

          const dataArray = new Uint8Array(analyser.frequencyBinCount);
          const updateAudioMeter = () => {
            if (analyserRef.current) {
              analyserRef.current.getByteFrequencyData(dataArray);
              let sum = 0;
              for (let i = 0; i < dataArray.length; i++) {
                sum += dataArray[i];
              }
              const average = sum / dataArray.length;
              setAudioLevel(Math.min(100, Math.round((average / 128) * 100)));
            }
            animFrameRef.current = requestAnimationFrame(updateAudioMeter);
          };
          updateAudioMeter();
        } catch (audioErr) {
          console.log("AudioContext visualizer not available:", audioErr);
        }
      } catch (err) {
        console.log("Camera or microphone permission not granted, running in fallback mode:", err);
        setCameraActive(false);
      }
    }

    setupMedia();

    // Check SpeechRecognition support
    if (typeof window !== "undefined") {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRecognition) {
        setSpeechSupported(true);
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-IN";

        recognition.onresult = (event: any) => {
          let fullText = "";
          for (let i = 0; i < event.results.length; i++) {
            fullText += event.results[i][0].transcript + " ";
          }
          setOfficerInputText(fullText.trim());
        };

        recognition.onerror = (e: any) => {
          console.log("Speech recognition error:", e);
          setIsListening(false);
        };

        recognition.onend = () => {
          setIsListening(false);
        };

        recognitionRef.current = recognition;
      }
    }

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current);
      }
      if (audioContextRef.current && audioContextRef.current.state !== "closed") {
        audioContextRef.current.close();
      }
    };
  }, []);

  // Timer Tick during active interview
  useEffect(() => {
    let timer: any = null;
    if (isInterviewActive && !isConcluded) {
      timer = setInterval(() => {
        setElapsedSeconds((prev) => prev + 1);
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [isInterviewActive, isConcluded]);

  // Voice synthesis helper (reads AI question aloud)
  const speakAiQuestion = (text: string) => {
    if (!voiceEnabled || typeof window === "undefined" || !("speechSynthesis" in window)) return;
    try {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      utterance.lang = "en-IN";
      window.speechSynthesis.speak(utterance);
    } catch (e) {
      console.log("TTS playback fallback:", e);
    }
  };

  // Toggle Camera
  const toggleCamera = () => {
    if (mediaStreamRef.current) {
      const videoTrack = mediaStreamRef.current.getVideoTracks()[0];
      if (videoTrack) {
        videoTrack.enabled = !cameraActive;
        setCameraActive(!cameraActive);
      }
    }
  };

  // Toggle Mic
  const toggleMic = () => {
    if (mediaStreamRef.current) {
      const audioTrack = mediaStreamRef.current.getAudioTracks()[0];
      if (audioTrack) {
        audioTrack.enabled = !micActive;
        setMicActive(!micActive);
      }
    }
  };

  // Start Speech Recognition
  const toggleSpeechRecognition = () => {
    if (!recognitionRef.current) return;
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch (e) {
        console.log("Failed to start speech recognition:", e);
      }
    }
  };

  // Start Live Interview
  const handleStartInterview = async () => {
    try {
      setElapsedSeconds(0);
      setIsConcluded(false);
      setAnalysisReport(null);
      setOfficerInputText("");

      const res = await fetchApi<{
        session_id: string;
        course_id: number;
        course_title: string;
        officer_name: string;
        target_duration_minutes: number;
        initial_ai_question: string;
        current_phase: string;
        primary_competency: string;
      }>("/behavioural/interview/start", {
        method: "POST",
        body: JSON.stringify({
          course_id: selectedCourseId,
          officer_name: officerName,
          target_duration_minutes: targetDuration
        })
      });

      setSessionId(res.session_id);
      setCurrentAiQuestion(res.initial_ai_question);
      setCurrentPhase(res.current_phase);
      setTargetCompetency(res.primary_competency);
      setCurrentTurn(1);
      setIsInterviewActive(true);

      setLiveTranscript([
        {
          speaker: "AI Interviewer",
          content: res.initial_ai_question,
          timestamp_seconds: 0,
          behavioral_tags: ["Course Knowledge", "Communication"]
        }
      ]);

      speakAiQuestion(res.initial_ai_question);
    } catch (err: any) {
      alert("Failed to start live interview: " + err.message);
    }
  };

  // Submit Officer's Speech / Text Turn
  const handleSendResponse = async () => {
    if (!sessionId || !officerInputText.trim() || isSubmittingTurn) return;

    const answer = officerInputText.trim();
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    }

    try {
      setIsSubmittingTurn(true);

      // Add to transcript
      setLiveTranscript((prev) => [
        ...prev,
        {
          speaker: `Officer ${officerName}`,
          content: answer,
          timestamp_seconds: elapsedSeconds,
          behavioral_tags: ["Deliberation"]
        }
      ]);

      const res = await fetchApi<{
        turn_number: number;
        ai_question: string;
        phase_name: string;
        phase_target_competency: string;
        elapsed_seconds: number;
        target_duration_minutes: number;
        turns_completed: number;
        is_final_turn: boolean;
        pacing_advice?: string;
        acknowledgement_note?: string;
      }>("/behavioural/interview/turn", {
        method: "POST",
        body: JSON.stringify({
          session_id: sessionId,
          officer_response: answer,
          elapsed_seconds: elapsedSeconds
        })
      });

      setOfficerInputText("");
      setCurrentTurn(res.turn_number);
      setCurrentPhase(res.phase_name);
      setTargetCompetency(res.phase_target_competency);
      setCurrentAiQuestion(res.ai_question);
      if (res.pacing_advice) setPacingAdvice(res.pacing_advice);

      setLiveTranscript((prev) => [
        ...prev,
        {
          speaker: "AI Interviewer",
          content: res.ai_question,
          timestamp_seconds: elapsedSeconds + 3,
          behavioral_tags: [res.phase_target_competency, "Communication"]
        }
      ]);

      speakAiQuestion(res.ai_question);

      if (res.is_final_turn) {
        // Automatically request concluding analysis
        handleConcludeInterview();
      }
    } catch (err: any) {
      alert("Error processing turn: " + err.message);
    } finally {
      setIsSubmittingTurn(false);
    }
  };

  // Conclude Interview & Request Analysis Scorecard
  const handleConcludeInterview = async () => {
    if (!sessionId) return;
    try {
      setIsLoadingAnalysis(true);
      setIsInterviewActive(false);
      setIsConcluded(true);
      if (window.speechSynthesis) window.speechSynthesis.cancel();

      const report = await fetchApi<InterviewAnalysisResponse>(`/behavioural/interview/${sessionId}/end`, {
        method: "POST"
      });
      setAnalysisReport(report);
    } catch (err: any) {
      alert("Failed to generate interview analysis: " + err.message);
    } finally {
      setIsLoadingAnalysis(false);
    }
  };

  // Pacing Fast Forward for Testing
  const fastForwardTime = (seconds: number) => {
    setElapsedSeconds((prev) => prev + seconds);
  };

  // Format seconds to mm:ss
  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 pb-24">
      {/* Top Header Bar */}
      <div className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-md sticky top-0 z-30">
        <div className="mx-auto max-w-7xl px-4 py-3 sm:px-6 lg:px-8 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="flex h-3 w-3 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
                <ShieldCheck className="h-3.5 w-3.5" />
                Live AI Executive Interview Board
              </span>
              <div className="text-sm font-bold text-white">
                Oral Assessment & 6 Behavioral Competencies Evaluation
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/behavioural/cases"
              className="text-xs font-semibold text-slate-400 hover:text-white transition-colors"
            >
              ← Back to Case Inquiries
            </Link>

            {isInterviewActive && (
              <button
                onClick={handleConcludeInterview}
                className="rounded-lg bg-red-600/90 hover:bg-red-600 px-3 py-1.5 text-xs font-bold text-white shadow-xs transition-all cursor-pointer flex items-center gap-1.5"
              >
                <Square className="h-3.5 w-3.5" />
                Conclude & Analyze
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        {!isInterviewActive && !analysisReport ? (
          /* Pre-Interview Briefing & Configuration Panel */
          <div className="max-w-2xl mx-auto mt-6 rounded-2xl border border-slate-800 bg-slate-950/90 p-8 shadow-2xl">
            <div className="text-center">
              <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-blue-900/40 text-blue-400 border border-blue-700/30">
                <Brain className="h-7 w-7 text-[#0D9488]" />
              </div>
              <h2 className="mt-4 text-2xl font-bold text-white">
                Live AI Competency Interview
              </h2>
              <p className="mt-2 text-xs text-slate-400 max-w-md mx-auto">
                Real-time interactive oral board examining subject matter mastery alongside the 6 core civil service
                competencies: Leadership, Communication, Project Management, Ethics, Decision Making, and Change Management.
              </p>
            </div>

            <div className="mt-8 space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-300">Select Accredited Course Curriculum</label>
                <select
                  value={selectedCourseId}
                  onChange={(e) => setSelectedCourseId(Number(e.target.value))}
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-900 px-3.5 py-2.5 text-xs text-white focus:border-blue-500 focus:outline-hidden"
                >
                  {COURSES.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.title} ({c.org})
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-300">Candidate / Officer Name</label>
                  <input
                    type="text"
                    value={officerName}
                    onChange={(e) => setOfficerName(e.target.value)}
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-900 px-3.5 py-2.5 text-xs text-white focus:border-blue-500 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-300">
                    Interview Pacing Target: {targetDuration} Minutes
                  </label>
                  <input
                    type="range"
                    min="25"
                    max="35"
                    step="1"
                    value={targetDuration}
                    onChange={(e) => setTargetDuration(Number(e.target.value))}
                    className="mt-3.5 w-full accent-[#0D9488]"
                  />
                  <div className="flex justify-between text-[10px] text-slate-500 font-mono">
                    <span>25 min (Accelerated)</span>
                    <span>30 min (Standard)</span>
                    <span>35 min (Comprehensive)</span>
                  </div>
                </div>
              </div>

              {/* Assessment Protocol Notice */}
              <div className="rounded-xl border border-blue-900/40 bg-blue-950/30 p-4 text-xs space-y-1.5 text-slate-300">
                <span className="font-bold text-blue-400 block uppercase tracking-wider text-[10px]">
                  Official Evaluation Rubric
                </span>
                <p>
                  • Target Duration: <span className="text-white font-semibold">{targetDuration} Minutes</span> across 5 evaluation phases.
                </p>
                <p>
                  • Evaluated on: <span className="text-white font-semibold">Course Mastery, Leadership, Communication, Project Management, Ethics, Decision Making, and Change Management</span>.
                </p>
                <p>• Speak directly into your microphone or type in the response terminal.</p>
              </div>

              <button
                onClick={handleStartInterview}
                className="w-full mt-4 flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-[#1E3A8A] to-[#0D9488] py-3 text-sm font-bold text-white shadow-lg hover:opacity-95 transition-all cursor-pointer"
              >
                <Play className="h-4 w-4" />
                Initialize Live Feed & Enter Board Room
              </button>
            </div>
          </div>
        ) : isInterviewActive ? (
          /* Active Live Interview Board Room */
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Left 5 Cols: Officer Live Video Feed & Audio Visualizer */}
            <div className="lg:col-span-5 space-y-4">
              <div className="relative rounded-2xl overflow-hidden border border-slate-800 bg-slate-950 shadow-2xl aspect-4/3 flex items-center justify-center">
                {/* Live Video Feed Element */}
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  className={`w-full h-full object-cover ${cameraActive ? "block" : "hidden"}`}
                />

                {!cameraActive && (
                  <div className="flex flex-col items-center justify-center text-slate-500">
                    <UserCheck className="h-16 w-16 text-slate-700" />
                    <span className="mt-2 text-xs font-semibold">Camera Feed Paused</span>
                  </div>
                )}

                {/* Top Overlay: Live Status */}
                <div className="absolute top-3 left-3 flex items-center gap-2 rounded-full bg-black/60 backdrop-blur-md px-3 py-1 border border-white/10">
                  <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-white">
                    Officer Feed • {officerName}
                  </span>
                </div>

                {/* Bottom Overlay: Media Controls & Mic Level Bar */}
                <div className="absolute bottom-3 inset-x-3 flex items-center justify-between rounded-xl bg-black/70 backdrop-blur-md p-2 border border-white/10">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={toggleCamera}
                      className={`p-2 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                        cameraActive ? "bg-slate-800 text-white" : "bg-red-600 text-white"
                      }`}
                      title="Toggle Camera"
                    >
                      {cameraActive ? <Video className="h-4 w-4" /> : <VideoOff className="h-4 w-4" />}
                    </button>

                    <button
                      onClick={toggleMic}
                      className={`p-2 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                        micActive ? "bg-slate-800 text-white" : "bg-red-600 text-white"
                      }`}
                      title="Toggle Microphone"
                    >
                      {micActive ? <Mic className="h-4 w-4" /> : <MicOff className="h-4 w-4" />}
                    </button>

                    <button
                      onClick={() => setVoiceEnabled(!voiceEnabled)}
                      className={`p-2 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                        voiceEnabled ? "bg-[#0D9488]/30 text-[#0D9488]" : "bg-slate-800 text-slate-400"
                      }`}
                      title="AI Voice Synthesis"
                    >
                      {voiceEnabled ? <Volume2 className="h-4 w-4" /> : <VolumeX className="h-4 w-4" />}
                    </button>
                  </div>

                  {/* Mic Audio Level Visualizer */}
                  <div className="flex items-center gap-1.5 px-2">
                    <span className="text-[10px] text-slate-400 font-mono">MIC</span>
                    <div className="w-16 h-2 rounded-full bg-slate-800 overflow-hidden">
                      <div
                        className="h-full bg-emerald-500 transition-all duration-75"
                        style={{ width: `${audioLevel}%` }}
                      />
                    </div>
                  </div>
                </div>
              </div>

              {/* 25 to 35 Minute Timer & Pacing Meter Card */}
              <div className="rounded-xl border border-slate-800 bg-slate-950 p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4 text-[#0D9488]" />
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                      Elapsed Time
                    </span>
                  </div>
                  <div className="font-mono text-lg font-bold text-white tracking-wider">
                    {formatTime(elapsedSeconds)} / {targetDuration}:00
                  </div>
                </div>

                {/* Progress Bar mapped against target duration */}
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-blue-600 via-teal-500 to-emerald-400 transition-all duration-500"
                    style={{
                      width: `${Math.min(100, Math.round((elapsedSeconds / (targetDuration * 60)) * 100))}%`
                    }}
                  />
                </div>

                <div className="flex items-center justify-between text-[10px] text-slate-500 font-mono">
                  <span>Turn {currentTurn} / 6</span>
                  <span className="text-emerald-400 font-semibold">{currentPhase}</span>
                </div>

                {pacingAdvice && (
                  <p className="text-xs text-teal-400 bg-teal-950/40 p-2 rounded border border-teal-800/40">
                    💡 {pacingAdvice}
                  </p>
                )}

                {/* Quick Fast Forward Buttons for Reviewers/Testers */}
                <div className="pt-1 flex items-center justify-between border-t border-slate-800/60 text-[10px] text-slate-400">
                  <span>Pacing Simulator:</span>
                  <div className="space-x-1.5">
                    <button
                      onClick={() => fastForwardTime(300)}
                      className="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all cursor-pointer"
                    >
                      +5 Mins
                    </button>
                    <button
                      onClick={() => fastForwardTime(600)}
                      className="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all cursor-pointer"
                    >
                      +10 Mins
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Right 7 Cols: AI Interview Board Inquiry & Officer Response Console */}
            <div className="lg:col-span-7 flex flex-col justify-between space-y-4">
              {/* AI Interviewer Prompt Card */}
              <div className="rounded-2xl border border-slate-800 bg-slate-950 p-6 shadow-xl relative overflow-hidden">
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                  <div className="flex items-center gap-2">
                    <div className="h-2.5 w-2.5 rounded-full bg-[#0D9488] animate-ping" />
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
                      Civil Service Interview Board Member
                    </span>
                  </div>
                  <span className="rounded bg-blue-950/60 border border-blue-800/50 px-2 py-0.5 text-[10px] font-bold text-blue-300 uppercase">
                    Testing: {targetCompetency}
                  </span>
                </div>

                <div className="mt-4">
                  <p className="text-base sm:text-lg font-medium text-white leading-relaxed">
                    "{currentAiQuestion}"
                  </p>
                </div>

                <div className="mt-4 flex items-center justify-between text-xs text-slate-400 border-t border-slate-800/60 pt-3">
                  <span className="italic text-[11px]">
                    {voiceEnabled ? "🔊 Spoken via Web Speech Audio" : "🔇 Audio muted"}
                  </span>
                  <button
                    onClick={() => speakAiQuestion(currentAiQuestion)}
                    className="text-[11px] font-bold text-[#0D9488] hover:underline flex items-center gap-1 cursor-pointer"
                  >
                    Repeat Question
                  </button>
                </div>
              </div>

              {/* Officer Live Input Console */}
              <div className="rounded-2xl border border-slate-800 bg-slate-950 p-5 shadow-xl space-y-3">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
                    <MessageSquare className="h-4 w-4 text-[#0D9488]" />
                    Officer's Oral / Text Response
                  </label>

                  {speechSupported && (
                    <button
                      onClick={toggleSpeechRecognition}
                      className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold transition-all cursor-pointer ${
                        isListening
                          ? "bg-red-600 text-white animate-pulse"
                          : "bg-slate-800 text-slate-300 hover:bg-slate-700"
                      }`}
                    >
                      <Mic className="h-3.5 w-3.5" />
                      {isListening ? "Listening... (Click to Stop)" : "Start Speech-to-Text"}
                    </button>
                  )}
                </div>

                <textarea
                  rows={4}
                  value={officerInputText}
                  onChange={(e) => setOfficerInputText(e.target.value)}
                  placeholder="Speak into your microphone or articulate your civil-service response here..."
                  className="w-full rounded-xl border border-slate-700 bg-slate-900 p-3.5 text-xs text-white focus:border-blue-500 focus:outline-hidden leading-relaxed"
                />

                <div className="flex items-center justify-between pt-1">
                  <span className="text-[10px] text-slate-500">
                    Be concise, structured, and cite relevant statutory rules or leadership principles.
                  </span>
                  <button
                    disabled={!officerInputText.trim() || isSubmittingTurn}
                    onClick={handleSendResponse}
                    className="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-[#1E3A8A] to-[#0D9488] px-5 py-2 text-xs font-bold text-white shadow-xs hover:opacity-90 disabled:opacity-40 transition-all cursor-pointer"
                  >
                    {isSubmittingTurn ? "Evaluating Response..." : "Submit Response to Board"}
                    <Send className="h-3.5 w-3.5" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        ) : analysisReport ? (
          /* End-of-Interview Comprehensive Diagnostic Scorecard */
          <div className="max-w-4xl mx-auto space-y-6">
            <div className="rounded-2xl border border-slate-800 bg-slate-950 p-8 shadow-2xl">
              {/* Top Seal & Official Dossier Header */}
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between border-b border-slate-800 pb-6 gap-4">
                <div>
                  <span className="inline-block rounded bg-emerald-950 border border-emerald-700/50 px-2.5 py-1 text-xs font-bold text-emerald-400 uppercase tracking-wider">
                    Official Competency Assessment Dossier
                  </span>
                  <h2 className="mt-2 text-2xl font-black text-white">
                    Oral Board Competency Report
                  </h2>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Candidate: <span className="text-white font-bold">{analysisReport.officer_name}</span> • Curriculum:{" "}
                    <span className="text-white font-bold">{analysisReport.course_title}</span>
                  </p>
                </div>

                <div className="text-right sm:border-l sm:border-slate-800 sm:pl-6">
                  <div className="text-3xl font-black text-emerald-400">
                    {analysisReport.overall_score_percent}%
                  </div>
                  <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mt-0.5">
                    {analysisReport.overall_rating_band}
                  </div>
                  <div className="text-[11px] text-slate-500 font-mono mt-1">
                    Duration: {analysisReport.total_duration_formatted}
                  </div>
                </div>
              </div>

              {/* Executive Summary */}
              <div className="mt-6 p-4 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300 leading-relaxed">
                <span className="font-bold text-white uppercase tracking-wider text-[11px] block mb-1">
                  Board Executive Summary
                </span>
                {analysisReport.executive_summary}
              </div>

              <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900/50 p-4">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 text-center">
                  7-Dimension Competency Radar
                </h3>
                <CompetencyRadar scores={analysisReport.competency_scores} />
              </div>

              {/* 7 Competency Breakdown Grid */}
              <div className="mt-8 space-y-4">
                <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
                  <Award className="h-4 w-4 text-[#0D9488]" />
                  Evaluated Competencies Breakdown (6 Behavioral + Course Mastery)
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.values(analysisReport.competency_scores).map((comp) => (
                    <div
                      key={comp.competency_name}
                      className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-center justify-between">
                          <h4 className="text-xs font-bold text-white">{comp.competency_name}</h4>
                          <span
                            className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                              comp.rating_band === "Exemplary"
                                ? "bg-emerald-950 text-emerald-300 border border-emerald-700/50"
                                : "bg-blue-950 text-blue-300 border border-blue-700/50"
                            }`}
                          >
                            {comp.rating_band} ({comp.score_percent}%)
                          </span>
                        </div>

                        {/* Visual Bar */}
                        <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-blue-500 to-[#0D9488]"
                            style={{ width: `${comp.score_percent}%` }}
                          />
                        </div>

                        <p className="mt-2.5 text-[11px] text-slate-400 italic">
                          <span className="font-semibold not-italic text-slate-300">Observed: </span>
                          {comp.key_evidence}
                        </p>
                      </div>

                      <div className="mt-3 pt-2.5 border-t border-slate-800 text-[11px] text-teal-400">
                        <span className="font-semibold text-slate-300">Recommendation: </span>
                        {comp.growth_opportunity}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Strengths & APAR Recommendations */}
              <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-6 pt-6 border-t border-slate-800">
                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-2 flex items-center gap-1.5">
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    Key Observed Strengths
                  </h4>
                  <ul className="space-y-1.5 text-xs text-slate-300">
                    {analysisReport.core_strengths.map((str, i) => (
                      <li key={i} className="flex items-start gap-1.5">
                        <span className="text-emerald-400">•</span>
                        <span>{str}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-blue-400 mb-2 flex items-center gap-1.5">
                    <TrendingUp className="h-3.5 w-3.5" />
                    Recommended APAR Training Actions
                  </h4>
                  <ul className="space-y-1.5 text-xs text-slate-300">
                    {analysisReport.recommended_apar_actions.map((act, i) => (
                      <li key={i} className="flex items-start gap-1.5">
                        <span className="text-blue-400">•</span>
                        <span>{act}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="mt-8 pt-6 border-t border-slate-800 flex items-center justify-between">
                <button
                  onClick={() => {
                    setIsConcluded(false);
                    setAnalysisReport(null);
                    setIsInterviewActive(false);
                  }}
                  className="inline-flex items-center gap-2 rounded-lg bg-slate-800 hover:bg-slate-700 px-4 py-2 text-xs font-bold text-white transition-all cursor-pointer"
                >
                  <RotateCcw className="h-3.5 w-3.5" />
                  Start New Interview Session
                </button>

                <button
                  onClick={() => window.print()}
                  className="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-[#1E3A8A] to-[#0D9488] px-5 py-2 text-xs font-bold text-white shadow-xs hover:opacity-90 transition-all cursor-pointer"
                >
                  <Printer className="h-3.5 w-3.5" />
                  Print Official Dossier
                </button>
              </div>
            </div>

            {/* Transcript Audit Log with Behavioral Tags */}
            <div className="rounded-2xl border border-slate-800 bg-slate-950 p-6 shadow-xl">
              <h3 className="text-sm font-bold text-white mb-3">Complete Annotated Transcript</h3>
              <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
                {analysisReport.transcript.map((entry, idx) => (
                  <div key={idx} className="p-3 rounded-lg bg-slate-900 border border-slate-800/80 text-xs">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-[#0D9488]">{entry.speaker}</span>
                      <div className="flex gap-1">
                        {entry.behavioral_tags.map((tag, tIdx) => (
                          <span
                            key={tIdx}
                            className="rounded bg-slate-800 px-1.5 py-0.5 text-[9px] font-mono text-slate-400"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                    <p className="mt-1.5 text-slate-300 leading-relaxed">{entry.content}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
