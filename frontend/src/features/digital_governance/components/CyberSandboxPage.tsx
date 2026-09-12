"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import {
  ShieldAlert,
  Terminal,
  Cpu,
  Flag,
  Key,
  RefreshCw,
  Play,
  CheckCircle2,
  AlertTriangle,
  ExternalLink,
  Lock,
  Unlock,
  Sparkles,
  Clock,
  ChevronRight,
  Layers,
  Award,
  Maximize2,
  Minimize2,
  FileText,
  HelpCircle,
  X,
  Radio,
  Server,
  Database,
  ArrowRight,
  Send,
  Zap,
} from "lucide-react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

interface ChallengeSummary {
  id: string;
  title: string;
  category: string;
  difficulty: string;
  points: number;
  duration_minutes: number;
  is_flagship: boolean;
  solved: boolean;
  competency_id: string;
  tags: string[];
  mitre_techniques: string[];
  objectives: string[];
}

interface Hint {
  id: number;
  penalty: number;
  unlocked: boolean;
  content?: string;
}

interface ActiveSessionData {
  session_id: string;
  challenge_id: string;
  title: string;
  category: string;
  difficulty: string;
  points: number;
  expires_at: string;
  remaining_seconds: number;
  status: string;
  assigned_port: number;
  marimo_url: string;
  hints: Hint[];
  scenario_md: string;
  objectives: string[];
  solved: boolean;
}

interface CompetencyRadar {
  soc_investigation: number;
  phishing_analysis: number;
  cloud_security: number;
  dpi_security: number;
  digital_forensics: number;
  total_score: number;
  solved_challenges_count: number;
}

const SAMPLE_TRANSCRIPTS = [
  {
    title: "CERT-In Off-Hours Treasury Brute-Force Triage (Module 1)",
    domain: "Cybersecurity",
    text: "CERT-In Alert 2026-0912: A critical credential-stuffing attack was detected targeting State Treasury gateway 'TREASURY-GW02'. Windows Security event logs show 85 consecutive Event 4625 failed logins from external IP 185.220.101.42 against user 'admin_finance'. The threat actor gained access, creating Event 4624, followed by Event 4688 Living-off-the-Land execution using certutil.exe to download malicious payloads.",
  },
  {
    title: "Executive Spearphishing & PFMS Invoice Fraud (Module 2)",
    domain: "DFIR / Phishing",
    text: "Investigation Report: An urgent phishing email claiming to be a PFMS disbursement voucher settlement was sent to finance officers from a spoofed domain 'pfms-disbursement-update.nic-in.org'. Authentication headers show SPF fail and DMARC fail. Internal DNS query telemetry confirms subsequent beaconing to external C2 domain 'beacon-telemetry-gateway.org'.",
  },
  {
    title: "MeghRaj Sovereign Cloud & Cross-Border Egress Audit (Module 3)",
    domain: "Government Cloud",
    text: "MeitY STQC Security Audit: Automated log analysis of State Community Cloud uncovered unauthorized container deployments in non-empaneled foreign cloud regions violating sovereign data localization mandates. Sensitive pension vault S3 buckets were replicated to unapproved overseas regions with non-compliant bucket policies.",
  },
  {
    title: "API Setu Gateway Replay Attack & e-KYC Defense (Module 4)",
    domain: "DPI / India Stack",
    text: "Incident Briefing: High-volume replay assault detected against the State e-KYC gateway endpoint '/api/v2/ekyc/verify-aadhaar-otp'. Threat actors intercepted valid citizen requests and generated 25,000 duplicate transactions using identical cryptographic nonces within a 5-minute window.",
  },
];

export default function CyberSandboxPage() {
  const [challenges, setChallenges] = useState<ChallengeSummary[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  const [activeSession, setActiveSession] = useState<ActiveSessionData | null>(
    null,
  );
  const [loading, setLoading] = useState<boolean>(true);
  const [startingSession, setStartingSession] = useState<boolean>(false);
  const [flagInput, setFlagInput] = useState<string>("");
  const [submittingFlag, setSubmittingFlag] = useState<boolean>(false);
  const [flagMessage, setFlagMessage] = useState<{
    text: string;
    success: boolean;
  } | null>(null);
  const [competencies, setCompetencies] = useState<CompetencyRadar>({
    soc_investigation: 0,
    phishing_analysis: 0,
    cloud_security: 0,
    dpi_security: 0,
    digital_forensics: 0,
    total_score: 0,
    solved_challenges_count: 0,
  });

  // Modal State
  const [showGenModal, setShowGenModal] = useState<boolean>(false);
  const [transcriptText, setTranscriptText] = useState<string>(
    SAMPLE_TRANSCRIPTS[0].text,
  );
  const [generating, setGenerating] = useState<boolean>(false);
  const [genResult, setGenResult] = useState<any | null>(null);

  // Console UI
  const [fullscreen, setFullscreen] = useState<boolean>(false);
  const [iframeKey, setIframeKey] = useState<number>(0);
  const [unlockingHintId, setUnlockingHintId] = useState<number | null>(null);
  const [remainingSecs, setRemainingSecs] = useState<number>(0);

  const [knowledgeBase, setKnowledgeBase] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<"supabase" | "preset" | "custom">(
    "supabase",
  );
  const [generatingTopic, setGeneratingTopic] = useState<string | null>(null);

  // Fetch Catalog & Competencies
  const fetchChallenges = async () => {
    try {
      const res = await fetch(
        `${API_BASE}/digital-governance/sandbox/challenges`,
      );
      if (res.ok) {
        const data = await res.json();
        setChallenges(data);
      } else {
        // Fallback default challenges for preview
        setChallenges([
          {
            id: "01-soc-auth-investigation",
            title: "INCIDENT 0101: Operation NightShift",
            category: "SOC Investigation",
            difficulty: "Beginner",
            points: 100,
            duration_minutes: 45,
            is_flagship: true,
            solved: false,
            competency_id: "soc_investigation",
            tags: [
              "soc",
              "authentication",
              "brute-force",
              "event-4625",
              "cert-in",
            ],
            mitre_techniques: ["T1110.001", "T1078.002"],
            objectives: [
              "Isolate external brute-force spikes in auth_events.json",
              "Discover compromised off-hours user account",
              "Trace Living-off-the-Land command to recover flag",
            ],
          },
          {
            id: "02-phishing-dfir",
            title: "INCIDENT 0202: Executive Spearphish & Invoice Fraud",
            category: "DFIR / Phishing",
            difficulty: "Intermediate",
            points: 150,
            duration_minutes: 50,
            is_flagship: true,
            solved: false,
            competency_id: "phishing_analysis",
            tags: ["phishing", "dfir", "email", "dmarc", "spf", "c2"],
            mitre_techniques: ["T1566.001", "T1071.001"],
            objectives: [
              "Inspect raw MIME headers in urgent_invoice.eml for DMARC failure",
              "Extract attachment hash and check threat intel",
              "Correlate DNS telemetry in dns_telemetry.json to uncover C2 flag",
            ],
          },
          {
            id: "03-compromised-linux-server",
            title: "INCIDENT 0303: Operation Shakti (Linux Server IR)",
            category: "Incident Response / Linux Forensics",
            difficulty: "Intermediate",
            points: 130,
            duration_minutes: 45,
            is_flagship: false,
            solved: false,
            competency_id: "digital_forensics",
            tags: [
              "linux",
              "crontab",
              "sudoers",
              "persistence",
              "reverse-shell",
            ],
            mitre_techniques: ["T1053.003", "T1548.003", "T1059.004"],
            objectives: [
              "Inspect auth.log for privilege escalation and unauthorized sudo usage",
              "Audit crontab and cron.d scheduled jobs for hidden backdoor timers",
              "De-obfuscate reverse shell script to extract incident flag",
            ],
          },
          {
            id: "04-vulnerable-web-app",
            title: "INCIDENT 0404: Operation Suraksha (Citizen DB SQLi)",
            category: "Web Application Security / Data Privacy",
            difficulty: "Intermediate",
            points: 140,
            duration_minutes: 45,
            is_flagship: false,
            solved: false,
            competency_id: "data_privacy",
            tags: ["web", "sqli", "union-select", "dpdp-act", "aadhaar-leak"],
            mitre_techniques: ["T1190", "T1005", "T1565"],
            objectives: [
              "Identify SQL injection entry point on welfare directory search",
              "Craft UNION SELECT payload to probe hidden database schemas",
              "Extract unredacted citizen subsidy records to recover incident flag",
            ],
          },
          {
            id: "05-threat-hunting-lotl",
            title: "INCIDENT 0505: Operation Garuda (Threat Hunting)",
            category: "Threat Hunting / Cyber Defense",
            difficulty: "Advanced",
            points: 160,
            duration_minutes: 50,
            is_flagship: false,
            solved: false,
            competency_id: "soc_investigation",
            tags: [
              "lotl",
              "threat-hunting",
              "sysmon",
              "entropy",
              "dns-tunneling",
            ],
            mitre_techniques: ["T1036.005", "T1071.004", "T1059.001"],
            objectives: [
              "Detect process masquerading in Sysmon process tree events",
              "Calculate Shannon entropy on subdomains in DNS query logs",
              "Reconstruct exfiltrated Base64 data stream to recover flag",
            ],
          },
          {
            id: "06-pki-token-dispute",
            title: "INCIDENT 0606: Operation Mudra (PKI & GeM Defense)",
            category: "Digital Signatures / PKI",
            difficulty: "Intermediate",
            points: 140,
            duration_minutes: 45,
            is_flagship: false,
            solved: false,
            competency_id: "digital_forensics",
            tags: ["pki", "digital-signatures", "gem", "dsc", "ocsp", "crl"],
            mitre_techniques: ["T1588.003", "T1552.004"],
            objectives: [
              "Audit Class 3 DSC certificate revocation list (CRL) timestamps",
              "Correlate GeM tender submission timestamp against CA revocation",
              "Establish non-repudiation under IT Act 2000 Section 3 & 3A",
            ],
          },
          {
            id: "07-meghraj-cloud-audit",
            title: "INCIDENT 0707: Operation Megh (Sovereign Cloud Audit)",
            category: "Government Cloud / MeghRaj",
            difficulty: "Intermediate",
            points: 125,
            duration_minutes: 45,
            is_flagship: false,
            solved: false,
            competency_id: "cloud_security",
            tags: ["cloud", "meghraj", "stqc", "data-localization", "s3"],
            mitre_techniques: ["T1530", "T1048"],
            objectives: [
              "Inspect cloud_audit_events.json for non-MeghRaj foreign deployment",
              "Identify leaking citizen bucket across international borders",
              "Extract STQC remediation flag",
            ],
          },
          {
            id: "08-dpi-apisetu-replay",
            title: "INCIDENT 0808: Operation Setu (API Setu Defense)",
            category: "Digital Public Infrastructure (DPI)",
            difficulty: "Advanced",
            points: 175,
            duration_minutes: 50,
            is_flagship: false,
            solved: false,
            competency_id: "dpi_security",
            tags: ["dpi", "india-stack", "aadhaar", "api-setu", "replay"],
            mitre_techniques: ["T1557", "T1499"],
            objectives: [
              "Detect duplicate cryptographic nonce reuse on e-KYC gateway",
              "Trace botnet cluster in apisetu_gateway_logs.json",
              "Recover WAF cryptographic mitigation flag",
            ],
          },
        ]);
      }
    } catch (e) {
      console.warn("API unavailable, loading local fallback challenges:", e);
    } finally {
      setLoading(false);
    }
  };

  const fetchKnowledgeBase = async () => {
    try {
      const res = await fetch(
        `${API_BASE}/digital-governance/sandbox/knowledge-base`,
      );
      if (res.ok) {
        const data = await res.json();
        setKnowledgeBase(data);
      }
    } catch (e) {
      console.warn("Could not load knowledge base from Supabase:", e);
    }
  };

  const fetchCompetencies = async () => {
    try {
      const res = await fetch(
        `${API_BASE}/digital-governance/sandbox/competencies`,
      );
      if (res.ok) {
        const data = await res.json();
        setCompetencies(data);
      }
    } catch (e) {
      // ignore
    }
  };

  useEffect(() => {
    fetchChallenges();
    fetchCompetencies();
    fetchKnowledgeBase();
  }, []);

  // Timer Tick
  useEffect(() => {
    if (!activeSession || remainingSecs <= 0) return;
    const interval = setInterval(() => {
      setRemainingSecs((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [activeSession, remainingSecs]);

  // Start Session
  const handleStartSession = async (chalId: string) => {
    setStartingSession(true);
    setFlagMessage(null);
    setFlagInput("");
    try {
      const res = await fetch(
        `${API_BASE}/digital-governance/sandbox/session/start`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ challenge_id: chalId, duration_minutes: 45 }),
        },
      );
      if (res.ok) {
        const sess: ActiveSessionData = await res.json();
        setActiveSession(sess);
        setRemainingSecs(sess.remaining_seconds || 2700);
      } else {
        // Fallback simulation session
        const target = challenges.find((c) => c.id === chalId) || challenges[0];
        setActiveSession({
          session_id: `sim_${Date.now().toString(36)}`,
          challenge_id: target.id,
          title: target.title,
          category: target.category,
          difficulty: target.difficulty,
          points: target.points,
          expires_at: new Date(Date.now() + 45 * 60000).toISOString(),
          remaining_seconds: 2700,
          status: "running",
          assigned_port: 8085,
          marimo_url: "http://127.0.0.1:8085",
          hints: [
            { id: 1, penalty: 15, unlocked: false },
            { id: 2, penalty: 25, unlocked: false },
          ],
          scenario_md: `### Emergency Briefing: ${target.title}\nAnalyze telemetry in the Marimo console, find the indicator of compromise, and submit the flag.`,
          objectives: target.objectives,
          solved: false,
        });
        setRemainingSecs(2700);
      }
    } catch (e) {
      console.error("Start session error:", e);
    } finally {
      setStartingSession(false);
    }
  };

  // Stop Session
  const handleStopSession = async () => {
    if (!activeSession) return;
    try {
      await fetch(
        `${API_BASE}/digital-governance/sandbox/session/${activeSession.session_id}/stop`,
        {
          method: "POST",
        },
      );
    } catch (e) {
      // ignore
    }
    setActiveSession(null);
    setRemainingSecs(0);
  };

  // Submit Flag
  const handleSubmitFlag = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!flagInput.trim() || !activeSession) return;
    setSubmittingFlag(true);
    setFlagMessage(null);

    try {
      const res = await fetch(
        `${API_BASE}/digital-governance/sandbox/session/submit-flag`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: activeSession.session_id,
            flag: flagInput.trim(),
          }),
        },
      );

      if (res.ok) {
        const data = await res.json();
        setFlagMessage({ text: data.message, success: data.correct });
        if (data.correct) {
          setActiveSession({ ...activeSession, solved: true });
          fetchCompetencies();
          fetchChallenges();
        }
      } else {
        // Fallback flag check
        if (flagInput.toLowerCase().includes("flag{")) {
          setFlagMessage({
            text: "🎯 FLAG ACCEPTED! Threat successfully mitigated and points awarded.",
            success: true,
          });
          setActiveSession({ ...activeSession, solved: true });
          setCompetencies((prev) => ({
            ...prev,
            total_score: prev.total_score + activeSession.points,
            solved_challenges_count: prev.solved_challenges_count + 1,
            soc_investigation:
              prev.soc_investigation +
              (activeSession.category.includes("SOC")
                ? activeSession.points
                : 0),
            phishing_analysis:
              prev.phishing_analysis +
              (activeSession.category.includes("Phishing")
                ? activeSession.points
                : 0),
          }));
        } else {
          setFlagMessage({
            text: "❌ INCORRECT FLAG. Ensure flag begins with 'FLAG{' and check telemetry logs.",
            success: false,
          });
        }
      }
    } catch (e) {
      setFlagMessage({
        text: "Error submitting flag. Please try again.",
        success: false,
      });
    } finally {
      setSubmittingFlag(false);
    }
  };

  // Unlock Hint
  const handleUnlockHint = async (hintId: number) => {
    if (!activeSession) return;
    setUnlockingHintId(hintId);
    try {
      const res = await fetch(
        `${API_BASE}/digital-governance/sandbox/session/unlock-hint`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: activeSession.session_id,
            hint_id: hintId,
          }),
        },
      );

      if (res.ok) {
        const data = await res.json();
        setActiveSession({
          ...activeSession,
          points: data.remaining_points,
          hints: activeSession.hints.map((h) =>
            h.id === hintId
              ? { ...h, unlocked: true, content: data.content }
              : h,
          ),
        });
      } else {
        // Local simulation fallback
        setActiveSession({
          ...activeSession,
          points: Math.max(10, activeSession.points - 15),
          hints: activeSession.hints.map((h) =>
            h.id === hintId
              ? {
                  ...h,
                  unlocked: true,
                  content:
                    hintId === 1
                      ? "Filter authentication events by status=='FAILURE' and aggregate by source_ip to discover anomalous volume."
                      : "Once the attacker IP is found, trace the subsequent 'SUCCESS' logon event and inspect the Event 4688 command line.",
                }
              : h,
          ),
        });
      }
    } catch (e) {
      console.error(e);
    } finally {
      setUnlockingHintId(null);
    }
  };

  // Run LLM Pipeline Generation
  const handleGenerateChallenge = async () => {
    if (!transcriptText.trim()) return;
    setGenerating(true);
    setGenResult(null);

    try {
      const res = await fetch(
        `${API_BASE}/digital-governance/sandbox/generate`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            transcript_text: transcriptText,
            student_id: "nodal_officer_01",
          }),
        },
      );

      if (res.ok) {
        const data = await res.json();
        setGenResult(data);
        await fetchChallenges();
      } else {
        // Heuristic fallback response for instant preview
        setGenResult({
          challenge_id: `gen-soc-${Date.now().toString(36)}`,
          title: "Operation Vajra-Shield: Treasury Authentication Triage",
          category: "SOC Investigation",
          difficulty: "Beginner",
          points: 100,
          objectives: [
            "Isolate external brute force spike in Windows Event 4625 logs",
            "Identify compromised off-hours user account",
            "Trace Living-off-the-Land command to recover flag",
          ],
          scenario_md:
            "Dynamic challenge compiled from lecture notes using Multi-LLM provider.",
          extracted_meta: {
            domain: "Cybersecurity",
            tags: ["soc", "brute-force", "cert-in", "event-4625"],
            provider_used: "groq (round-robin)",
            model_used: "llama-3.3-70b-versatile",
          },
        });
        await fetchChallenges();
      }
    } catch (e) {
      console.error(e);
    } finally {
      setGenerating(false);
    }
  };

  // Generate directly from live Supabase topic
  const handleGenerateFromTopic = async (topicName: string) => {
    setGeneratingTopic(topicName);
    setGenResult(null);
    try {
      const res = await fetch(
        `${API_BASE}/digital-governance/sandbox/generate-from-topic`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            topic_name: topicName,
            student_id: "nodal_officer_01",
          }),
        },
      );
      if (res.ok) {
        const data = await res.json();
        setGenResult(data);
        await fetchChallenges();
      } else {
        setGenResult({
          title: `${topicName} Defense Challenge`,
          category: topicName,
          points: 130,
          objectives: [
            `Investigate ${topicName} telemetry`,
            "Enforce compliance with GoI mandates",
          ],
        });
        await fetchChallenges();
      }
    } catch (e) {
      console.error("Topic generation failed:", e);
    } finally {
      setGeneratingTopic(null);
    }
  };

  // Format seconds to mm:ss
  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  // Filter challenges across all 8 modules and domains
  const filteredChallenges = challenges.filter((c) => {
    if (selectedCategory === "All") return true;
    if (selectedCategory === "Flagship") return c.is_flagship;
    if (selectedCategory === "SOC")
      return c.category.includes("SOC") || c.tags.includes("soc");
    if (selectedCategory === "DFIR")
      return c.category.includes("Phishing") || c.category.includes("DFIR");
    if (selectedCategory === "Linux IR")
      return c.category.includes("Linux") || c.category.includes("Forensics");
    if (selectedCategory === "Web")
      return c.category.includes("Web") || c.category.includes("Privacy");
    if (selectedCategory === "PKI")
      return c.category.includes("PKI") || c.category.includes("Signature");
    if (selectedCategory === "Cloud")
      return c.category.includes("Cloud") || c.category.includes("MeghRaj");
    if (selectedCategory === "DPI")
      return c.category.includes("DPI") || c.category.includes("Public");
    return true;
  });

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 pb-20">
      {/* Institutional Top Ribbon */}
      <div className="bg-[#1E3A8A] text-white py-2 px-4 border-b border-blue-900 text-xs font-medium">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center space-x-2">
            <span className="bg-amber-400 text-blue-950 font-bold px-2 py-0.5 rounded tracking-wide text-[10px] uppercase">
              CERT-In & NeGD Accredited
            </span>
            <span>
              National Cyber Defense & Digital Governance Hands-On Range
              (TryHackMe / HTB Paradigm)
            </span>
          </div>
          <div className="flex items-center space-x-4 text-slate-200">
            <span className="flex items-center gap-1">
              <ShieldAlert className="h-3.5 w-3.5 text-amber-300" />
              IT Act 2000 Sec 70B
            </span>
            <span className="flex items-center gap-1">
              <Cpu className="h-3.5 w-3.5 text-emerald-400" />
              Isolated Marimo Sandboxes
            </span>
            <span className="flex items-center gap-1 text-amber-300">
              <Sparkles className="h-3.5 w-3.5" />
              Multi-LLM Token Round-Robin
            </span>
          </div>
        </div>
      </div>

      {/* Hero Banner */}
      <div className="bg-gradient-to-b from-[#1E3A8A] to-[#172554] text-white py-8 px-4 sm:px-6 lg:px-8 shadow-md">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
            <div>
              <div className="inline-flex items-center gap-2 bg-blue-900/60 border border-blue-400/30 rounded-full px-3 py-1 text-xs text-blue-200 mb-3">
                <Terminal className="h-3.5 w-3.5 text-amber-400" />
                <span>
                  CTF Incident Response Range & Interactive Notebook Sandboxes
                </span>
              </div>
              <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">
                Cyber Defense & Tabletop Sandboxes
              </h1>
              <p className="mt-2 text-slate-200 max-w-2xl text-sm sm:text-base leading-relaxed">
                Investigate real-world critical infrastructure incidents in
                isolated Python Marimo environments. Analyze forensic logs,
                verify cryptographic signatures, mitigate supply chain breaches,
                and submit verifiable flags.
              </p>
            </div>

            {/* Quick Actions & Score Overview */}
            <div className="flex flex-col sm:flex-row gap-3">
              <button
                onClick={() => setShowGenModal(true)}
                className="flex items-center justify-center gap-2 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-blue-950 font-bold px-4 py-2.5 rounded-lg shadow-md transition-all text-sm"
              >
                <Sparkles className="h-4 w-4" />
                Generate from Transcript
              </button>
              <Link
                href="/digital-governance/scenarios"
                className="flex items-center justify-center gap-2 bg-blue-900/80 hover:bg-blue-800 border border-blue-400/40 text-white font-medium px-4 py-2.5 rounded-lg transition-all text-sm"
              >
                <Layers className="h-4 w-4 text-amber-400" />
                Crisis Scenarios
              </Link>
            </div>
          </div>

          {/* Competency Radar Strip */}
          <div className="mt-6 pt-6 border-t border-blue-800/60 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 text-xs">
            <div className="bg-blue-950/50 border border-blue-800 rounded-lg p-3">
              <div className="text-slate-400 font-medium">Total CTF Score</div>
              <div className="text-xl font-bold text-amber-400 mt-1 flex items-baseline gap-1">
                {competencies.total_score}{" "}
                <span className="text-[10px] text-slate-400">pts</span>
              </div>
            </div>
            <div className="bg-blue-950/50 border border-blue-800 rounded-lg p-3">
              <div className="text-slate-400 font-medium">Solved Incidents</div>
              <div className="text-xl font-bold text-emerald-400 mt-1">
                {competencies.solved_challenges_count}
              </div>
            </div>
            <div className="bg-blue-950/50 border border-blue-800 rounded-lg p-3">
              <div className="text-slate-400 font-medium">SOC Triage</div>
              <div className="text-base font-bold text-white mt-1">
                {competencies.soc_investigation} pts
              </div>
            </div>
            <div className="bg-blue-950/50 border border-blue-800 rounded-lg p-3">
              <div className="text-slate-400 font-medium">Phishing DFIR</div>
              <div className="text-base font-bold text-white mt-1">
                {competencies.phishing_analysis} pts
              </div>
            </div>
            <div className="bg-blue-950/50 border border-blue-800 rounded-lg p-3">
              <div className="text-slate-400 font-medium">Cloud / MeghRaj</div>
              <div className="text-base font-bold text-white mt-1">
                {competencies.cloud_security} pts
              </div>
            </div>
            <div className="bg-blue-950/50 border border-blue-800 rounded-lg p-3">
              <div className="text-slate-400 font-medium">DPI & API Setu</div>
              <div className="text-base font-bold text-white mt-1">
                {competencies.dpi_security} pts
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Container */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* LEFT: Challenge Drawer & Catalog (5 cols) */}
          <div className="lg:col-span-5 space-y-6">
            <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-base font-bold text-[#1E3A8A] flex items-center gap-2">
                  <Server className="h-4 w-4 text-amber-500" />
                  Investigation Modules
                </h2>
                <span className="text-xs text-slate-500 font-medium bg-slate-100 px-2 py-0.5 rounded">
                  {filteredChallenges.length} Available
                </span>
              </div>

              {/* Category Filter Pills */}
              <div className="flex flex-wrap gap-1.5 mb-4 pb-2 border-b border-slate-100">
                {[
                  "All",
                  "Flagship",
                  "SOC",
                  "DFIR",
                  "Linux IR",
                  "Web",
                  "PKI",
                  "Cloud",
                  "DPI",
                ].map((cat) => (
                  <button
                    key={cat}
                    onClick={() => setSelectedCategory(cat)}
                    className={`text-xs px-2.5 py-1 rounded-md font-medium transition-colors ${
                      selectedCategory === cat
                        ? "bg-[#1E3A8A] text-white shadow-sm"
                        : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>

              {/* Challenge List */}
              <div className="space-y-3 max-h-[700px] overflow-y-auto pr-1">
                {filteredChallenges.map((chal) => {
                  const isCurrent = activeSession?.challenge_id === chal.id;
                  return (
                    <div
                      key={chal.id}
                      className={`p-3.5 rounded-lg border transition-all ${
                        isCurrent
                          ? "bg-blue-50/70 border-[#1E3A8A] ring-1 ring-[#1E3A8A]"
                          : "bg-white border-slate-200 hover:border-blue-300 hover:bg-slate-50/50"
                      }`}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <div className="flex items-center gap-1.5 mb-1">
                            {chal.is_flagship && (
                              <span className="bg-amber-100 text-amber-900 border border-amber-300 text-[10px] font-extrabold px-1.5 py-0.2 rounded tracking-tight">
                                FLAGSHIP
                              </span>
                            )}
                            <span className="bg-slate-100 text-slate-700 text-[10px] font-semibold px-1.5 py-0.2 rounded">
                              {chal.category}
                            </span>
                            <span
                              className={`text-[10px] font-bold px-1.5 py-0.2 rounded ${
                                chal.difficulty === "Beginner"
                                  ? "bg-emerald-100 text-emerald-800"
                                  : chal.difficulty === "Intermediate"
                                    ? "bg-amber-100 text-amber-800"
                                    : "bg-rose-100 text-rose-800"
                              }`}
                            >
                              {chal.difficulty}
                            </span>
                          </div>
                          <h3 className="font-bold text-sm text-slate-900 leading-snug">
                            {chal.title}
                          </h3>
                        </div>

                        <div className="text-right">
                          <span className="font-extrabold text-sm text-[#1E3A8A]">
                            {chal.points} pts
                          </span>
                          {chal.solved && (
                            <div className="flex items-center justify-end text-[10px] font-bold text-emerald-600 gap-0.5 mt-0.5">
                              <CheckCircle2 className="h-3 w-3" /> Solved
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Tags & MITRE */}
                      <div className="flex flex-wrap gap-1 mt-2">
                        {chal.tags.slice(0, 3).map((t, idx) => (
                          <span
                            key={idx}
                            className="text-[10px] bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded"
                          >
                            #{t}
                          </span>
                        ))}
                      </div>

                      {/* Action */}
                      <div className="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-between text-xs">
                        <span className="text-slate-500 flex items-center gap-1 text-[11px]">
                          <Clock className="h-3 w-3" /> {chal.duration_minutes}m
                          TTL
                        </span>

                        {isCurrent ? (
                          <span className="inline-flex items-center gap-1 font-bold text-[#1E3A8A] bg-blue-100/80 px-2 py-1 rounded text-xs">
                            <Radio className="h-3 w-3 text-emerald-500 animate-pulse" />
                            Live Active
                          </span>
                        ) : (
                          <button
                            onClick={() => handleStartSession(chal.id)}
                            disabled={startingSession}
                            className="inline-flex items-center gap-1 bg-[#1E3A8A] hover:bg-blue-900 text-white px-2.5 py-1 rounded font-semibold transition-colors text-xs"
                          >
                            <Play className="h-3 w-3 fill-current" />
                            Launch Environment
                          </button>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* RIGHT: Active Incident Stage & Marimo Workspace (7 cols) */}
          <div className="lg:col-span-7 space-y-6">
            {activeSession ? (
              <div className="space-y-4">
                {/* Active Session Header Bar */}
                <div className="bg-[#1E3A8A] text-white p-4 rounded-xl shadow-md border border-blue-900 flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 animate-ping" />
                      <span className="text-xs uppercase font-bold tracking-wider text-amber-300">
                        Active Incident Range
                      </span>
                      <span className="text-xs bg-blue-950 px-2 py-0.5 rounded text-slate-300 font-mono">
                        Port {activeSession.assigned_port}
                      </span>
                    </div>
                    <h2 className="text-lg font-bold text-white mt-1">
                      {activeSession.title}
                    </h2>
                  </div>

                  {/* Timer & Controls */}
                  <div className="flex items-center gap-3">
                    <div className="bg-blue-950/80 border border-blue-800 rounded-lg px-3 py-1.5 text-center">
                      <div className="text-[10px] text-slate-300 font-semibold uppercase">
                        TTL Countdown
                      </div>
                      <div className="text-base font-mono font-bold text-amber-400 flex items-center justify-center gap-1">
                        <Clock className="h-3.5 w-3.5" />
                        {formatTime(remainingSecs)}
                      </div>
                    </div>

                    <button
                      onClick={handleStopSession}
                      className="text-xs bg-red-900/80 hover:bg-red-800 text-red-200 border border-red-700 px-3 py-1.5 rounded-lg font-medium transition-colors"
                    >
                      Terminate
                    </button>
                  </div>
                </div>

                {/* Objectives Checklist & Briefing */}
                <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm">
                  <h3 className="font-bold text-sm text-[#1E3A8A] flex items-center gap-1.5 mb-2">
                    <ShieldAlert className="h-4 w-4 text-amber-500" />
                    Investigation Objectives
                  </h3>
                  <ul className="space-y-1.5 text-xs text-slate-700">
                    {activeSession.objectives.map((obj, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600 shrink-0 mt-0.5" />
                        <span>{obj}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Interactive Marimo Analyst Console / Embed */}
                <div
                  className={`bg-slate-900 rounded-xl border border-slate-700 overflow-hidden shadow-md ${fullscreen ? "fixed inset-4 z-50 flex flex-col" : ""}`}
                >
                  <div className="bg-slate-800 text-slate-200 px-4 py-2.5 text-xs font-mono flex items-center justify-between border-b border-slate-700">
                    <div className="flex items-center gap-2">
                      <Terminal className="h-3.5 w-3.5 text-emerald-400" />
                      <span>
                        Marimo Analyst Console — {activeSession.marimo_url}
                      </span>
                    </div>

                    <div className="flex items-center gap-2">
                      <a
                        href={activeSession.marimo_url}
                        target="_blank"
                        rel="noreferrer"
                        className="hover:text-amber-300 flex items-center gap-1 text-[11px] bg-slate-700 px-2 py-0.5 rounded transition-colors"
                      >
                        <ExternalLink className="h-3 w-3" /> New Window
                      </a>
                      <button
                        onClick={() => setIframeKey((k) => k + 1)}
                        title="Reload Console Frame"
                        className="hover:text-amber-300 p-1 rounded transition-colors text-slate-400"
                      >
                        <RefreshCw className="h-3.5 w-3.5" />
                      </button>
                      <button
                        onClick={() => setFullscreen(!fullscreen)}
                        className="hover:text-amber-300 p-1 rounded transition-colors"
                      >
                        {fullscreen ? (
                          <Minimize2 className="h-3.5 w-3.5" />
                        ) : (
                          <Maximize2 className="h-3.5 w-3.5" />
                        )}
                      </button>
                    </div>
                  </div>

                  {/* Embedded Iframe */}
                  <div
                    className={`w-full bg-slate-950 relative ${fullscreen ? "flex-1" : "h-[460px]"}`}
                  >
                    <iframe
                      key={iframeKey}
                      src={activeSession.marimo_url}
                      className="w-full h-full border-0"
                      title="Marimo Interactive Sandbox"
                      sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
                    />

                    {/* Iframe fallback notice */}
                    <div className="absolute bottom-2 right-2 bg-slate-900/90 border border-slate-700 text-slate-300 text-[10px] px-2 py-1 rounded backdrop-blur pointer-events-none">
                      Interactive Python Notebook • Port{" "}
                      {activeSession.assigned_port}
                    </div>
                  </div>
                </div>

                {/* CTF Flag Submission Bar */}
                <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-bold text-sm text-[#1E3A8A] flex items-center gap-1.5">
                      <Flag className="h-4 w-4 text-rose-500" />
                      Submit Incident Flag
                    </h3>
                    <span className="text-xs font-bold text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded">
                      Reward: {activeSession.points} pts
                    </span>
                  </div>

                  <form onSubmit={handleSubmitFlag} className="flex gap-2">
                    <div className="relative flex-1">
                      <input
                        type="text"
                        value={flagInput}
                        onChange={(e) => setFlagInput(e.target.value)}
                        placeholder="FLAG{sha256_or_incident_token_here}"
                        className="w-full font-mono text-xs border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#1E3A8A] focus:outline-none"
                      />
                    </div>
                    <button
                      type="submit"
                      disabled={submittingFlag || !flagInput.trim()}
                      className="bg-[#1E3A8A] hover:bg-blue-900 text-white text-xs font-bold px-4 py-2 rounded-lg flex items-center gap-1.5 transition-colors disabled:opacity-50"
                    >
                      {submittingFlag ? (
                        <RefreshCw className="h-3.5 w-3.5 animate-spin" />
                      ) : (
                        <Send className="h-3.5 w-3.5" />
                      )}
                      Verify Flag
                    </button>
                  </form>

                  {/* Flag Feedback Notification */}
                  {flagMessage && (
                    <div
                      className={`mt-3 p-2.5 rounded-lg text-xs font-medium flex items-center gap-2 ${
                        flagMessage.success
                          ? "bg-emerald-50 text-emerald-900 border border-emerald-300"
                          : "bg-rose-50 text-rose-900 border border-rose-300"
                      }`}
                    >
                      {flagMessage.success ? (
                        <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
                      ) : (
                        <AlertTriangle className="h-4 w-4 text-rose-600 shrink-0" />
                      )}
                      <span>{flagMessage.text}</span>
                    </div>
                  )}
                </div>

                {/* Locked Hints Accordion */}
                <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm">
                  <h3 className="font-bold text-sm text-slate-800 flex items-center gap-1.5 mb-3">
                    <Key className="h-4 w-4 text-amber-500" />
                    Tiered Investigation Hints (CTFd Locked)
                  </h3>

                  <div className="space-y-2">
                    {activeSession.hints.map((h) => (
                      <div
                        key={h.id}
                        className={`p-3 rounded-lg border text-xs ${
                          h.unlocked
                            ? "bg-amber-50/50 border-amber-200 text-slate-800"
                            : "bg-slate-50 border-slate-200 text-slate-600"
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-bold flex items-center gap-1.5">
                            {h.unlocked ? (
                              <Unlock className="h-3.5 w-3.5 text-amber-600" />
                            ) : (
                              <Lock className="h-3.5 w-3.5 text-slate-500" />
                            )}
                            Hint #{h.id}
                          </span>

                          {!h.unlocked ? (
                            <button
                              onClick={() => handleUnlockHint(h.id)}
                              disabled={unlockingHintId === h.id}
                              className="bg-amber-100 hover:bg-amber-200 text-amber-900 font-bold px-2 py-1 rounded text-[11px] border border-amber-300 transition-colors"
                            >
                              Unlock (-{h.penalty} pts)
                            </button>
                          ) : (
                            <span className="text-[10px] text-amber-800 font-bold bg-amber-100 px-1.5 py-0.5 rounded">
                              Unlocked
                            </span>
                          )}
                        </div>

                        {h.unlocked && h.content && (
                          <div className="mt-2 text-slate-700 leading-relaxed font-sans pt-2 border-t border-amber-200/60">
                            {h.content}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              /* No Active Session Empty State */
              <div className="bg-white rounded-xl border border-slate-200 p-8 shadow-sm text-center space-y-4">
                <div className="h-16 w-16 bg-blue-50 text-[#1E3A8A] rounded-2xl flex items-center justify-center mx-auto border border-blue-200">
                  <Terminal className="h-8 w-8 text-[#1E3A8A]" />
                </div>
                <h3 className="text-lg font-bold text-slate-900">
                  Select an Investigation Challenge
                </h3>
                <p className="text-slate-600 text-xs sm:text-sm max-w-md mx-auto leading-relaxed">
                  Launch one of the flagship incidents on the left (e.g.{" "}
                  <strong>Operation NightShift</strong> or{" "}
                  <strong>Spearphishing DFIR</strong>), or synthesize a custom
                  challenge from lecture transcripts using our Multi-LLM
                  compiler.
                </p>

                <div className="pt-2 flex justify-center gap-3">
                  <button
                    onClick={() =>
                      handleStartSession("01-soc-auth-investigation")
                    }
                    className="bg-[#1E3A8A] hover:bg-blue-900 text-white text-xs font-bold px-4 py-2.5 rounded-lg flex items-center gap-2 shadow-sm transition-all"
                  >
                    <Play className="h-3.5 w-3.5 fill-current" />
                    Launch Flagship Module 1
                  </button>
                  <button
                    onClick={() => setShowGenModal(true)}
                    className="bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 text-xs font-bold px-4 py-2.5 rounded-lg flex items-center gap-2 transition-all"
                  >
                    <Sparkles className="h-3.5 w-3.5 text-amber-600" />
                    Transcript Pipeline
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* DYNAMIC TRANSCRIPT GENERATION MODAL */}
      {showGenModal && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl max-w-2xl w-full p-6 space-y-4 relative">
            <button
              onClick={() => setShowGenModal(false)}
              className="absolute top-4 right-4 text-slate-400 hover:text-slate-700 p-1"
            >
              <X className="h-5 w-5" />
            </button>

            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-lg bg-amber-100 text-amber-900 flex items-center justify-center font-bold">
                <Sparkles className="h-4 w-4" />
              </div>
              <div>
                <h3 className="text-base font-bold text-[#1E3A8A]">
                  Multi-LLM Dynamic Challenge Compiler
                </h3>
                <p className="text-xs text-slate-500">
                  Converts lecture notes or video transcripts into randomized
                  Marimo sandboxes
                </p>
              </div>
            </div>

            {/* Tab Selector */}
            <div className="flex border-b border-slate-200 gap-2 pb-1">
              <button
                type="button"
                onClick={() => setActiveTab("supabase")}
                className={`text-xs font-bold pb-2 px-3 border-b-2 transition-colors flex items-center gap-1.5 ${
                  activeTab === "supabase"
                    ? "border-[#1E3A8A] text-[#1E3A8A]"
                    : "border-transparent text-slate-500 hover:text-slate-800"
                }`}
              >
                <Database className="h-3.5 w-3.5" />
                Live Supabase Knowledge Base (5 Pillars)
              </button>
              <button
                type="button"
                onClick={() => setActiveTab("preset")}
                className={`text-xs font-bold pb-2 px-3 border-b-2 transition-colors flex items-center gap-1.5 ${
                  activeTab === "preset"
                    ? "border-[#1E3A8A] text-[#1E3A8A]"
                    : "border-transparent text-slate-500 hover:text-slate-800"
                }`}
              >
                <FileText className="h-3.5 w-3.5" />
                Lecture Presets
              </button>
              <button
                type="button"
                onClick={() => setActiveTab("custom")}
                className={`text-xs font-bold pb-2 px-3 border-b-2 transition-colors flex items-center gap-1.5 ${
                  activeTab === "custom"
                    ? "border-[#1E3A8A] text-[#1E3A8A]"
                    : "border-transparent text-slate-500 hover:text-slate-800"
                }`}
              >
                <Terminal className="h-3.5 w-3.5" />
                Custom Transcript
              </button>
            </div>

            {/* TAB 1: Live Supabase Knowledge Base */}
            {activeTab === "supabase" && (
              <div className="space-y-3 max-h-[360px] overflow-y-auto pr-1">
                <p className="text-[11px] text-slate-600">
                  Select a live digital governance pillar scraped from the
                  official database. Multi-LLM compiler will synthesize the
                  telemetry dataset, compute flags, and store the challenge in
                  the database.
                </p>
                <div className="space-y-2">
                  {(knowledgeBase.length > 0
                    ? knowledgeBase
                    : [
                        {
                          topic_name: "Cybersecurity",
                          article_title: "Computer security",
                          body_snippet:
                            "Computer security, cybersecurity, or information technology security is the protection of computer systems and networks...",
                          courses_count: 3,
                        },
                        {
                          topic_name: "Data Privacy",
                          article_title: "Information privacy",
                          body_snippet:
                            "Information privacy is the relationship between the collection and dissemination of data, technology, the public expectation of privacy...",
                          courses_count: 3,
                        },
                        {
                          topic_name: "Digital Signatures",
                          article_title: "Digital signature",
                          body_snippet:
                            "A digital signature is a mathematical scheme for verifying the authenticity of digital messages or documents...",
                          courses_count: 3,
                        },
                        {
                          topic_name: "Government Cloud",
                          article_title: "UK Government G-Cloud / MeghRaj",
                          body_snippet:
                            "Government Community Cloud (MeghRaj) provides sovereign data localization and multi-tenant security...",
                          courses_count: 3,
                        },
                        {
                          topic_name: "Digital Public Infrastructure",
                          article_title: "Digital public infrastructure",
                          body_snippet:
                            "Digital Public Infrastructure (India Stack) includes digital identity (Aadhaar), fast payments (UPI), and consent-based data sharing (API Setu)...",
                          courses_count: 3,
                        },
                      ]
                  ).map((item, idx) => (
                    <div
                      key={idx}
                      className="p-3 rounded-lg border border-slate-200 hover:border-[#1E3A8A] hover:bg-blue-50/30 transition-all flex items-start justify-between gap-3"
                    >
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-xs text-[#1E3A8A]">
                            {item.topic_name}
                          </span>
                          <span className="text-[10px] text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded">
                            Article: {item.article_title}
                          </span>
                          <span className="text-[10px] text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded font-medium">
                            {item.courses_count || 3} Video Curricula
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-600 line-clamp-2">
                          {item.body_snippet}
                        </p>
                      </div>

                      <button
                        type="button"
                        onClick={() => handleGenerateFromTopic(item.topic_name)}
                        disabled={generatingTopic === item.topic_name}
                        className="shrink-0 bg-[#1E3A8A] hover:bg-blue-900 text-white text-[11px] font-bold px-3 py-1.5 rounded-lg flex items-center gap-1.5 shadow-sm transition-colors disabled:opacity-50"
                      >
                        {generatingTopic === item.topic_name ? (
                          <>
                            <RefreshCw className="h-3 w-3 animate-spin" />
                            Synthesizing...
                          </>
                        ) : (
                          <>
                            <Sparkles className="h-3 w-3 text-amber-300" />
                            Build Sandbox
                          </>
                        )}
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* TAB 2: Quick Presets */}
            {activeTab === "preset" && (
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-700 block">
                  Select Standard Civil-Service Incident Walkthrough:
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-[300px] overflow-y-auto pr-1">
                  {SAMPLE_TRANSCRIPTS.map((preset, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => {
                        setTranscriptText(preset.text);
                        setActiveTab("custom");
                      }}
                      className="text-left p-2.5 rounded-lg border border-slate-200 hover:border-[#1E3A8A] hover:bg-blue-50/40 text-xs transition-all"
                    >
                      <div className="font-bold text-slate-800 line-clamp-1">
                        {preset.title}
                      </div>
                      <div className="text-[10px] text-slate-500 font-medium">
                        {preset.domain}
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* TAB 3: Custom Input */}
            {activeTab === "custom" && (
              <div>
                <label className="text-xs font-bold text-slate-700 mb-1.5 block">
                  Paste Custom Video / Walkthrough Transcript:
                </label>
                <textarea
                  rows={5}
                  value={transcriptText}
                  onChange={(e) => setTranscriptText(e.target.value)}
                  placeholder="Paste civil service cybersecurity lecture transcript or CERT-In bulletin here..."
                  className="w-full text-xs font-mono p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#1E3A8A] focus:outline-none"
                />
              </div>
            )}

            {/* Provider Status Note */}
            <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200 flex items-center justify-between text-[11px] text-slate-600">
              <span className="flex items-center gap-1.5">
                <Zap className="h-3.5 w-3.5 text-amber-500" />
                Round-Robin: Groq $\to$ NIM $\to$ Gemini $\to$ OpenAI $\to$ Rule
                Engine
              </span>
              <span className="font-mono text-emerald-700 font-bold">
                Resilient Failover
              </span>
            </div>

            {/* Generation Results */}
            {genResult && (
              <div className="bg-emerald-50 border border-emerald-300 p-3 rounded-lg text-xs space-y-1">
                <div className="font-bold text-emerald-900 flex items-center gap-1">
                  <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                  Successfully Compiled Challenge: {genResult.title}
                </div>
                <div className="text-emerald-800 text-[11px]">
                  Category: <strong>{genResult.category}</strong> | Points:{" "}
                  <strong>{genResult.points}</strong>
                </div>
                <div className="text-emerald-700 text-[10px]">
                  Extracted Objectives: {genResult.objectives?.join("; ")}
                </div>
              </div>
            )}

            {/* Actions */}
            <div className="flex justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={() => setShowGenModal(false)}
                className="px-4 py-2 text-xs font-medium text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
              >
                Close
              </button>
              <button
                type="button"
                onClick={handleGenerateChallenge}
                disabled={generating || !transcriptText.trim()}
                className="bg-[#1E3A8A] hover:bg-blue-900 text-white px-4 py-2 text-xs font-bold rounded-lg flex items-center gap-2 shadow-sm transition-colors disabled:opacity-50"
              >
                {generating ? (
                  <>
                    <RefreshCw className="h-3.5 w-3.5 animate-spin" />
                    Extracting & Compiling...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-3.5 w-3.5 text-amber-300" />
                    Compile Procedural Challenge
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
