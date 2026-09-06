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
  const [mounted, setMounted] = useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Namaste! I am the Karmayogi AI Learning Assistant. Ask me about statistical methods, survey protocols, price index formulas, or your current learning curriculum.",
      source: "karmayogi-engine",
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

  if (!mounted) return null;

  return (
    <div className="fixed bottom-6 right-6 z-40" suppressHydrationWarning>
      {!isOpen ? (
        <button
          onClick={() => setIsOpen(true)}
          className="relative h-14 w-14 rounded-full bg-[#965C66] hover:bg-[#824E57] text-white shadow-lg border border-white/20 flex items-center justify-center transition-all duration-300 hover:scale-105 active:scale-95 cursor-pointer select-none group"
          title="Open Karmayogi AI Assistant"
          aria-label="Open Karmayogi AI Assistant"
        >
          <Bot className="h-6 w-6 text-white transition-transform group-hover:scale-110" />
          <span className="absolute top-1 right-1 h-3 w-3 rounded-full bg-emerald-400 border-2 border-white" />
        </button>
      ) : (
        <div className="w-96 rounded-2xl bg-white border border-[#C8A8A9]/50 shadow-2xl overflow-hidden flex flex-col h-[500px] transition-all">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 bg-[#965C66] text-white">
            <div className="flex items-center gap-2.5">
              <div className="h-8 w-8 rounded-full bg-white/20 border border-white/30 flex items-center justify-center">
                <Bot className="h-4 w-4 text-white" />
              </div>
              <div>
                <h3 className="text-sm font-bold flex items-center gap-1.5">
                  Karmayogi AI
                  <span className="text-[9px] font-medium uppercase bg-white/20 text-white px-1.5 py-0.2 rounded border border-white/30">
                    Active
                  </span>
                </h3>
                <p className="text-[10px] text-white/80">Civil Service Intelligence Assistant</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1.5 rounded-md text-white/80 hover:text-white hover:bg-white/20 transition-colors cursor-pointer"
            >
              <Minimize2 className="h-4 w-4" />
            </button>
          </div>

          {/* Context Tag if provided */}
          {context && (
            <div className="bg-[#EEE8E9] border-b border-[#C8A8A9]/40 px-3 py-1.5 text-[11px] text-[#44383A] flex items-center gap-1.5">
              <Sparkles className="h-3.5 w-3.5 text-[#965C66]" />
              <span className="font-semibold text-[#241E20]">Topic:</span>
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
                      ? "bg-[#965C66] text-white rounded-br-xs"
                      : "bg-white text-[#241E20] border border-[#C8A8A9]/40 rounded-bl-xs"
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
              <div className="flex items-center gap-2 text-[#5A5052] text-xs">
                <Loader2 className="h-4 w-4 animate-spin text-[#965C66]" />
                <span>AI assistant processing query...</span>
              </div>
            )}
          </div>

          {/* Quick Prompts */}
          <div className="px-3 py-1.5 bg-[#FAF8F8] border-t border-[#C8A8A9]/30 flex gap-1.5 overflow-x-auto text-[11px] text-[#5A5052]">
            <button
              onClick={() => setQuery("What is CPI formula in MoSPI?")}
              className="whitespace-nowrap px-2 py-0.5 rounded bg-white border border-[#C8A8A9]/50 hover:bg-[#965C66]/10 hover:text-[#965C66] cursor-pointer transition-colors"
            >
              CPI formula
            </button>
            <button
              onClick={() => setQuery("Explain NSS rural FSUs")}
              className="whitespace-nowrap px-2 py-0.5 rounded bg-white border border-[#C8A8A9]/50 hover:bg-[#965C66]/10 hover:text-[#965C66] cursor-pointer transition-colors"
            >
              NSS FSUs
            </button>
            <button
              onClick={() => setQuery("What is TSA in PFMS?")}
              className="whitespace-nowrap px-2 py-0.5 rounded bg-white border border-[#C8A8A9]/50 hover:bg-[#965C66]/10 hover:text-[#965C66] cursor-pointer transition-colors"
            >
              PFMS TSA
            </button>
          </div>

          {/* Input Box */}
          <form onSubmit={handleSend} className="p-3 bg-white border-t border-[#C8A8A9]/40 flex gap-2">
            <Input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a technical or training question..."
              className="h-9 text-xs border-[#C8A8A9]/60 focus-visible:ring-[#965C66] focus-visible:border-[#965C66]"
              disabled={loading}
            />
            <Button
              type="submit"
              size="sm"
              className="h-9 px-3 bg-[#965C66] hover:bg-[#824E57] text-white transition-colors"
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

