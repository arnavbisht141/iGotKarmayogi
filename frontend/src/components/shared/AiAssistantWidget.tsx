"use client";

import React, { useState } from "react";
import { Bot, Send, X, Sparkles, Loader2, Minimize2, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
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
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Namaste! I am the Karmayogi AI Learning Assistant. Ask me about statistical methods, survey protocols, price index formulas, or your current learning curriculum.",
      source: "langgraph-karmayogi-engine",
    },
  ]);

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
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "I could not reach the AI agent service. Please ensure the backend is active.",
          source: "error",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-40">
      {!isOpen ? (
        <button
          onClick={() => setIsOpen(true)}
          className="group flex items-center gap-2.5 px-4 py-3 bg-slate-900 hover:bg-slate-800 text-white rounded-full shadow-lg border border-slate-700 transition-all hover:scale-105 cursor-pointer"
          title="Open Karmayogi AI Assistant"
        >
          <div className="relative">
            <Bot className="h-5 w-5 text-amber-400" />
            <span className="absolute -top-1 -right-1 h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          </div>
          <span className="text-sm font-semibold tracking-wide">
            {t("nav.askAi")}
          </span>
          <span className="text-[10px] bg-amber-500/20 text-amber-300 px-1.5 py-0.5 rounded border border-amber-400/30">
            LangGraph
          </span>
        </button>
      ) : (
        <div className="w-96 rounded-2xl bg-white border border-slate-200 shadow-2xl overflow-hidden flex flex-col h-[500px] transition-all">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 bg-slate-900 text-white">
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-full bg-amber-500/20 border border-amber-400/40 flex items-center justify-center">
                <Bot className="h-4 w-4 text-amber-400" />
              </div>
              <div>
                <h3 className="text-sm font-bold flex items-center gap-1.5">
                  Karmayogi Copilot
                  <span className="text-[9px] font-normal uppercase bg-slate-800 text-amber-300 px-1.5 py-0.2 rounded border border-slate-700">
                    Phase 0 Stub
                  </span>
                </h3>
                <p className="text-[10px] text-slate-400">Powered by LangGraph & LangChain</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-slate-800"
            >
              <Minimize2 className="h-4 w-4" />
            </button>
          </div>

          {/* Context Tag if provided */}
          {context && (
            <div className="bg-slate-50 border-b border-slate-200 px-3 py-1.5 text-[11px] text-slate-600 flex items-center gap-1.5">
              <Sparkles className="h-3.5 w-3.5 text-amber-600" />
              <span className="font-semibold text-slate-700">Topic:</span>
              <span className="truncate">{context}</span>
            </div>
          )}

          {/* Chat Messages */}
          <div className="flex-1 p-4 overflow-y-auto space-y-3 text-sm bg-slate-50/50">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={`flex flex-col ${
                  m.role === "user" ? "items-end" : "items-start"
                }`}
              >
                <div
                  className={`max-w-[85%] rounded-2xl px-3.5 py-2.5 shadow-2xs leading-relaxed ${
                    m.role === "user"
                      ? "bg-slate-900 text-white rounded-br-xs"
                      : "bg-white text-slate-800 border border-slate-200 rounded-bl-xs"
                  }`}
                >
                  <p className="text-xs">{m.content}</p>
                </div>
                {m.source && m.role === "assistant" && (
                  <span className="text-[9px] text-slate-400 mt-1 flex items-center gap-1 font-mono">
                    <CheckCircle2 className="h-2.5 w-2.5 text-emerald-500" />
                    {m.source}
                  </span>
                )}
              </div>
            ))}
            {loading && (
              <div className="flex items-center gap-2 text-slate-400 text-xs">
                <Loader2 className="h-4 w-4 animate-spin text-amber-600" />
                <span>LangGraph agent processing query...</span>
              </div>
            )}
          </div>

          {/* Quick Prompts */}
          <div className="px-3 py-1.5 bg-slate-100/70 border-t border-slate-200 flex gap-1.5 overflow-x-auto text-[11px] text-slate-600">
            <button
              onClick={() => setQuery("What is CPI formula in MoSPI?")}
              className="whitespace-nowrap px-2 py-0.5 rounded bg-white border border-slate-300 hover:bg-slate-50 cursor-pointer"
            >
              CPI formula
            </button>
            <button
              onClick={() => setQuery("Explain NSS rural FSUs")}
              className="whitespace-nowrap px-2 py-0.5 rounded bg-white border border-slate-300 hover:bg-slate-50 cursor-pointer"
            >
              NSS FSUs
            </button>
            <button
              onClick={() => setQuery("What is TSA in PFMS?")}
              className="whitespace-nowrap px-2 py-0.5 rounded bg-white border border-slate-300 hover:bg-slate-50 cursor-pointer"
            >
              PFMS TSA
            </button>
          </div>

          {/* Input Box */}
          <form onSubmit={handleSend} className="p-3 bg-white border-t border-slate-200 flex gap-2">
            <Input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a technical or training question..."
              className="h-9 text-xs"
              disabled={loading}
            />
            <Button
              type="submit"
              size="sm"
              className="h-9 px-3 bg-slate-900 hover:bg-slate-800"
              disabled={loading || !query.trim()}
            >
              <Send className="h-3.5 w-3.5" />
            </Button>
          </form>
        </div>
      )}
    </div>
  );
}
