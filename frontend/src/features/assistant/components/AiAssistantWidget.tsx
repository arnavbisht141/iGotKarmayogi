"use client";

import React, { useState, useRef, useEffect } from "react";
import { Send, X, Loader2, Minimize2, CheckCircle2, MessageSquare, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { fetchApi } from "@/lib/api";
import { useI18n } from "@/lib/i18n";

interface AiAssistantWidgetProps {
  context?: string;
}

interface Message {
  role: "user" | "assistant";
  content: string;
  source?: string;
}

export function AiAssistantWidget({ context }: AiAssistantWidgetProps) {
  const { t } = useI18n();
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [mounted, setMounted] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  React.useEffect(() => { setMounted(true); }, []);

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Namaste! I am the Karmayogi Support Assistant. Ask me about statistical methods, survey protocols, price index formulas, or navigating your course curriculum.",
      source: "karmayogi-desk",
    },
  ]);

  // Auto-scroll to latest message
  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isOpen]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    const userMsg = query.trim();
    setQuery("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);

    try {
      const data = await fetchApi<{ response: string; source: string }>("/agents/chat", {
        method: "POST",
        body: JSON.stringify({
          message: userMsg,
          context: context || "General Civil Service & Statistics Learning",
        }),
      });
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.response, source: data.source },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Could not reach the support service. Please verify server connectivity.",
          source: "error",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const quickPrompts = [
    { label: "CPI formula", query: "What is the CPI formula in MoSPI?" },
    { label: "NSS FSUs", query: "Explain NSS rural FSUs" },
    { label: "PFMS TSA", query: "What is TSA in PFMS?" },
  ];

  if (!mounted) return null;

  return (
    <div className="fixed bottom-3 right-3 sm:bottom-6 sm:right-6 z-40" suppressHydrationWarning>
      {!isOpen ? (
        /* ── Floating Trigger Button ── */
        <button
          onClick={() => setIsOpen(true)}
          className="relative h-12 w-12 sm:h-14 sm:w-14 rounded-full text-white flex items-center justify-center cursor-pointer select-none group animate-pulse-glow navy-teal-gradient shadow-xl border border-white/20 hover:scale-110 transition-transform duration-200 active:scale-95"
          title="Karmayogi Learning Support Desk"
          aria-label="Karmayogi Learning Support Desk"
        >
          <Sparkles className="h-5 w-5 sm:h-6 sm:w-6 text-white transition-transform group-hover:scale-110" />
          {/* Online pulse dot */}
          <span className="absolute top-0.5 right-0.5 h-3.5 w-3.5 rounded-full bg-emerald-400 border-2 border-white">
            <span className="absolute inset-0 rounded-full bg-emerald-400 animate-ping opacity-75" />
          </span>
          {/* Tooltip */}
          <span className="absolute right-16 top-1/2 -translate-y-1/2 whitespace-nowrap text-[11px] font-bold text-white bg-[#0C1B3D] px-2.5 py-1 rounded-lg shadow-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none border border-white/10 hidden sm:block">
            Karmayogi AI Desk
          </span>
        </button>
      ) : (
        /* ── Chat Panel ── */
        <div className="w-[calc(100vw-24px)] sm:w-[380px] max-h-[82vh] h-[520px] rounded-2xl overflow-hidden flex flex-col shadow-2xl"
          style={{ boxShadow: "0 25px 60px rgba(0,0,0,0.35), 0 0 0 1px rgba(255,255,255,0.05)" }}>

          {/* Header — navy-teal gradient */}
          <div className="navy-teal-gradient relative overflow-hidden px-4 py-3.5 flex items-center justify-between shrink-0">
            <div className="absolute inset-0 hero-mesh opacity-40" />
            <div className="relative z-10 flex items-center gap-3">
              {/* Avatar */}
              <div className="h-9 w-9 rounded-full bg-white/15 border border-white/25 flex items-center justify-center shrink-0">
                <Sparkles className="h-4 w-4 text-white" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  Karmayogi Support Desk
                  <span className="text-[9px] font-bold uppercase bg-emerald-400/30 text-emerald-200 px-1.5 py-0.5 rounded border border-emerald-400/30">
                    Online
                  </span>
                </h3>
                <p className="text-[10px] text-white/60">Statistical Guidance &amp; Course Inquiries</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="relative z-10 p-1.5 rounded-lg text-white/70 hover:text-white hover:bg-white/15 transition-colors cursor-pointer"
            >
              <Minimize2 className="h-4 w-4" />
            </button>
          </div>

          {/* Context tag */}
          {context && (
            <div className="bg-slate-50 border-b border-slate-200 px-4 py-2 text-[11px] text-slate-600 flex items-center gap-1.5 shrink-0">
              <span className="font-bold text-slate-800">Module:</span>
              <span className="truncate">{context}</span>
            </div>
          )}

          {/* Messages */}
          <div className="flex-1 p-4 overflow-y-auto space-y-3 text-sm"
            style={{ background: "radial-gradient(ellipse at top, #f0f9ff 0%, #f8fafc 100%)" }}>
            {messages.map((m, idx) => (
              <div key={idx} className={`flex flex-col ${m.role === "user" ? "items-end" : "items-start"}`}>
                <div className={`max-w-[85%] rounded-2xl px-3.5 py-2.5 leading-relaxed ${
                  m.role === "user"
                    ? "navy-teal-gradient text-white rounded-br-sm shadow-sm"
                    : "bg-white text-slate-800 border border-slate-200 rounded-bl-sm shadow-sm border-l-2 border-l-[#0D9488]"
                }`}>
                  <p className="text-xs leading-relaxed">{m.content}</p>
                </div>
                {m.source && m.role === "assistant" && (
                  <span className="text-[9px] text-slate-400 mt-1 flex items-center gap-1 font-mono">
                    <CheckCircle2 className="h-2.5 w-2.5 text-[#0D9488]" />
                    Verified official content
                  </span>
                )}
              </div>
            ))}

            {/* Typing indicator */}
            {loading && (
              <div className="flex items-start">
                <div className="bg-white border border-slate-200 rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm border-l-2 border-l-[#0D9488]">
                  <div className="flex items-center gap-1.5">
                    <span className="h-2 w-2 rounded-full bg-[#0D9488] animate-float-dot" />
                    <span className="h-2 w-2 rounded-full bg-[#0D9488] animate-float-dot-2" />
                    <span className="h-2 w-2 rounded-full bg-[#0D9488] animate-float-dot-3" />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Prompts */}
          <div className="px-3 py-2 bg-white border-t border-slate-100 flex gap-1.5 overflow-x-auto scrollbar-none shrink-0">
            {quickPrompts.map((p) => (
              <button
                key={p.label}
                onClick={() => setQuery(p.query)}
                className="whitespace-nowrap px-3 py-1.5 rounded-full bg-slate-50 border border-slate-200 text-[11px] font-semibold text-slate-600 hover:bg-blue-50 hover:text-[#1E3A8A] hover:border-blue-200 cursor-pointer transition-all hover:scale-105 shrink-0"
              >
                {p.label}
              </button>
            ))}
          </div>

          {/* Input */}
          <form onSubmit={handleSend} className="p-3 bg-white border-t border-slate-200 flex gap-2 shrink-0">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask about methods or courses..."
              disabled={loading}
              className="flex-1 h-10 px-3.5 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-[#1E3A8A]/30 focus:border-[#1E3A8A] bg-slate-50 text-slate-800 placeholder-slate-400 transition-all disabled:opacity-60"
            />
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="h-10 w-10 rounded-xl navy-teal-gradient text-white flex items-center justify-center cursor-pointer border-0 shadow-sm transition-opacity hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed shrink-0"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-3.5 w-3.5" />
              )}
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
