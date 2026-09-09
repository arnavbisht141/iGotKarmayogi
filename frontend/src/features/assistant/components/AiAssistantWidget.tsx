"use client";

import React, { useState, useRef, useEffect } from "react";
import { MessageSquare, Send, X, Minimize2, Loader2, CheckCircle2, BookOpen } from "lucide-react";
import { fetchApi } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
  source?: string;
}

interface AiAssistantWidgetProps {
  context?: string;
}

export function AiAssistantWidget({ context }: AiAssistantWidgetProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Namaste. I am your Official Karmayogi Statistical Learning Assistant. You can ask about survey schedules, index formulas, administrative circulars, or course modules.",
    },
  ]);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMounted(true);
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    const userText = query.trim();
    setQuery("");
    setMessages((prev) => [...prev, { role: "user", content: userText }]);
    setLoading(true);

    try {
      const data = await fetchApi<{ answer: string; source?: string }>("/assistant/query", {
        method: "POST",
        body: JSON.stringify({ query: userText, context }),
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          source: data.source || "Official MoSPI & NSSTA Cadre Training Repository",
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "The training query dispatch is currently operating in offline validation mode. Please refer directly to the NSSTA Cadre Manuals or rephrase your query.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const quickPrompts = [
    { label: "CPI Formula", query: "What is the CPI formula in MoSPI?" },
    { label: "NSS FSUs", query: "Explain NSS rural First Stage Units (FSUs)" },
    { label: "PFMS Protocol", query: "What is the Treasury Single Account (TSA) protocol in PFMS?" },
  ];

  if (!mounted) return null;

  return (
    <div className="fixed bottom-6 right-6 z-40" suppressHydrationWarning>
      {!isOpen ? (
        /* Floating Trigger Button */
        <button
          onClick={() => setIsOpen(true)}
          className="relative h-12 px-4 rounded-xl bg-[#0B132B] hover:bg-[#152C4F] text-white flex items-center gap-2.5 cursor-pointer select-none shadow-lg border border-slate-700 transition-colors active:translate-y-[1px]"
          title="Karmayogi Cadre Support Desk"
          aria-label="Karmayogi Cadre Support Desk"
        >
          <div className="h-2 w-2 rounded-full bg-emerald-400" />
          <MessageSquare className="h-4 w-4 text-white" />
          <span className="text-xs font-semibold tracking-tight">Cadre Support Desk</span>
        </button>
      ) : (
        /* Chat Panel */
        <div className="w-[380px] rounded-xl overflow-hidden flex flex-col shadow-2xl border border-slate-200 bg-white"
          style={{ height: 520 }}>

          {/* Header */}
          <div className="bg-[#0B132B] px-4 py-3.5 flex items-center justify-between shrink-0 border-b border-slate-800">
            <div className="flex items-center gap-2.5">
              <div className="h-8 w-8 rounded-lg bg-[#1E3A8A] border border-[#254BAA] flex items-center justify-center shrink-0">
                <BookOpen className="h-4 w-4 text-white" />
              </div>
              <div>
                <h3 className="text-xs font-bold text-white flex items-center gap-2">
                  Karmayogi Cadre Support
                  <span className="text-[9px] font-semibold uppercase bg-emerald-950 text-emerald-300 px-1.5 py-0.2 rounded border border-emerald-800">
                    Official
                  </span>
                </h3>
                <p className="text-[10px] text-slate-400">Statistical Methods &amp; Training Inquiries</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1.5 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition-colors cursor-pointer"
              aria-label="Minimize support desk"
            >
              <Minimize2 className="h-4 w-4" />
            </button>
          </div>

          {/* Context tag */}
          {context && (
            <div className="bg-slate-100 border-b border-slate-200 px-4 py-2 text-[11px] text-slate-700 flex items-center gap-1.5 shrink-0">
              <span className="font-bold text-slate-900">Module Context:</span>
              <span className="truncate">{context}</span>
            </div>
          )}

          {/* Messages */}
          <div className="flex-1 p-4 overflow-y-auto space-y-3 text-sm bg-[#F8FAFC]">
            {messages.map((m, idx) => (
              <div key={idx} className={`flex flex-col ${m.role === "user" ? "items-end" : "items-start"}`}>
                <div className={`max-w-[85%] rounded-lg px-3.5 py-2.5 text-xs leading-relaxed ${
                  m.role === "user"
                    ? "bg-[#1E3A8A] text-white shadow-xs"
                    : "bg-white text-slate-900 border border-slate-200 shadow-xs"
                }`}>
                  <p className="leading-relaxed">{m.content}</p>
                </div>
                {m.source && m.role === "assistant" && (
                  <span className="text-[9px] text-slate-500 mt-1 flex items-center gap-1 font-mono">
                    <CheckCircle2 className="h-2.5 w-2.5 text-emerald-600" />
                    {m.source}
                  </span>
                )}
              </div>
            ))}

            {/* Typing indicator */}
            {loading && (
              <div className="flex items-start">
                <div className="bg-white border border-slate-200 rounded-lg px-3.5 py-2.5 shadow-xs text-xs text-slate-500 flex items-center gap-2">
                  <Loader2 className="h-3.5 w-3.5 animate-spin text-[#1E3A8A]" />
                  <span>Consulting official training guidelines...</span>
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
                className="whitespace-nowrap px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 text-[11px] font-medium text-slate-700 hover:bg-blue-50 hover:text-[#1E3A8A] hover:border-blue-200 cursor-pointer transition-colors shrink-0 active:translate-y-[1px]"
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
              placeholder="Ask about official methods or courses..."
              disabled={loading}
              className="flex-1 h-9 px-3 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-[#1E3A8A] focus:border-[#1E3A8A] bg-white text-slate-900 placeholder-slate-400 transition-colors disabled:opacity-60"
            />
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="h-9 px-3 rounded-lg bg-[#1E3A8A] hover:bg-[#162E70] text-white flex items-center justify-center cursor-pointer border border-[#162E70] shadow-xs transition-colors disabled:opacity-40 disabled:cursor-not-allowed shrink-0 active:translate-y-[1px]"
            >
              {loading ? (
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
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
