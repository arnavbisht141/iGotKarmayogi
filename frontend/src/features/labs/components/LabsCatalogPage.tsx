"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  FlaskConical,
  BookOpen,
  Sparkles,
  Search,
  Filter,
  CheckCircle2,
  ArrowRight,
  ShieldCheck,
  Cpu,
  Layers,
  Code2,
  Clock,
  Award,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { fetchApi } from "@/lib/api";
import { LabDetail } from "@/lib/types";
import { useI18n } from "@/lib/i18n";

export default function LabsCatalogPage() {
  const { t } = useI18n();
  const [labs, setLabs] = useState<LabDetail[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [difficultyFilter, setDifficultyFilter] = useState<string>("all");
  const [selectedTag, setSelectedTag] = useState<string>("all");

  useEffect(() => {
    setLoading(true);
    fetchApi<LabDetail[]>("/technical-courses/labs")
      .then((data) => setLabs(data))
      .catch((err) => console.error("Error fetching labs:", err))
      .finally(() => setLoading(false));
  }, []);

  const tags = ["all", "fastapi", "pandas", "data-cleaning", "api", "sampling", "cpi"];

  const filteredLabs = labs.filter((l) => {
    const matchesSearch =
      l.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      l.objective.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesDifficulty =
      difficultyFilter === "all" || l.difficulty.toLowerCase() === difficultyFilter.toLowerCase();
    const matchesTag =
      selectedTag === "all" ||
      (l.tags && l.tags.some((tag) => tag.toLowerCase() === selectedTag.toLowerCase()));

    return matchesSearch && matchesDifficulty && matchesTag;
  });

  return (
    <div className="min-h-[calc(100vh-65px)] bg-slate-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Hero Header */}
        <div className="bg-gradient-to-r from-[#0F172A] via-[#1E3A8A] to-[#0F172A] rounded-2xl p-8 sm:p-10 text-white shadow-lg relative overflow-hidden border border-slate-800">
          <div className="relative z-10 max-w-3xl space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur border border-white/20 text-xs font-semibold text-amber-300">
              <FlaskConical className="h-4 w-4" />
              <span>National Statistical &amp; Technical Competency Labs</span>
            </div>
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight">
              Interactive Hands-on Labs &amp; Jupyter Sandbox
            </h1>
            <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
              Validate technical civil service workflows in isolated Docker sandboxes.
              Switch seamlessly between standard <strong>Jupyter Notebooks</strong> and modern reactive{" "}
              <strong>Marimo extensions</strong> with instant unit test verification.
            </p>

            <div className="flex flex-wrap gap-4 pt-2">
              <div className="flex items-center gap-2 text-xs text-slate-300 bg-white/5 px-3 py-1.5 rounded-lg border border-white/10">
                <BookOpen className="h-4 w-4 text-amber-400" />
                <span>Jupyter Notebooks (.ipynb)</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-slate-300 bg-white/5 px-3 py-1.5 rounded-lg border border-white/10">
                <Sparkles className="h-4 w-4 text-emerald-400" />
                <span>Marimo Reactive DAG (.py)</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-slate-300 bg-white/5 px-3 py-1.5 rounded-lg border border-white/10">
                <ShieldCheck className="h-4 w-4 text-blue-400" />
                <span>Docker Container Sandbox</span>
              </div>
            </div>
          </div>
        </div>

        {/* Search & Filter Controls */}
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search practical labs, skills, or objectives..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 text-xs bg-slate-50 border border-slate-200 rounded-lg outline-none focus:bg-white focus:border-[#1E3A8A] transition-all"
            />
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {/* Difficulty Filter */}
            <div className="flex items-center gap-1.5 text-xs text-slate-600">
              <span className="font-semibold">Difficulty:</span>
              {["all", "beginner", "intermediate", "advanced"].map((d) => (
                <button
                  key={d}
                  onClick={() => setDifficultyFilter(d)}
                  className={`px-2.5 py-1 rounded-md text-xs font-semibold capitalize transition-all cursor-pointer ${
                    difficultyFilter === d
                      ? "bg-[#1E3A8A] text-white"
                      : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                  }`}
                >
                  {d}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Tag Pills */}
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider mr-1">
            Filter by Skill:
          </span>
          {tags.map((t) => (
            <button
              key={t}
              onClick={() => setSelectedTag(t)}
              className={`px-3 py-1 rounded-full text-xs font-medium capitalize transition-all cursor-pointer ${
                selectedTag === t
                  ? "bg-slate-900 text-white font-bold shadow-xs"
                  : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-100"
              }`}
            >
              {t === "all" ? "All Skills" : `#${t}`}
            </button>
          ))}
        </div>

        {/* Labs Grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-64 rounded-2xl bg-slate-200 animate-pulse" />
            ))}
          </div>
        ) : filteredLabs.length === 0 ? (
          <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 space-y-3">
            <FlaskConical className="h-10 w-10 text-slate-400 mx-auto" />
            <h3 className="text-sm font-bold text-slate-800">No matching technical labs found</h3>
            <p className="text-xs text-slate-500">Try adjusting your search query or skill filter.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredLabs.map((labItem) => (
              <Card
                key={labItem.id}
                className="border-slate-200 bg-white hover:border-[#1E3A8A] hover:shadow-md transition-all flex flex-col justify-between group"
              >
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <Badge
                      variant="outline"
                      className={`text-[10px] uppercase font-bold ${
                        labItem.difficulty === "beginner"
                          ? "border-emerald-300 text-emerald-800 bg-emerald-50"
                          : labItem.difficulty === "intermediate"
                          ? "border-blue-300 text-blue-800 bg-blue-50"
                          : "border-amber-300 text-amber-800 bg-amber-50"
                      }`}
                    >
                      {labItem.difficulty}
                    </Badge>

                    <span className="text-[10px] font-mono text-slate-400 flex items-center gap-1">
                      <Cpu className="h-3 w-3 text-emerald-600" /> Python 3.11
                    </span>
                  </div>

                  <CardTitle className="text-base font-bold text-slate-900 group-hover:text-[#1E3A8A] transition-colors line-clamp-2">
                    {labItem.title}
                  </CardTitle>
                  <CardDescription className="text-xs text-slate-500 line-clamp-2 mt-1">
                    {labItem.objective}
                  </CardDescription>
                </CardHeader>

                <CardContent className="space-y-3">
                  <div className="p-3 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-between text-xs text-slate-600">
                    <span className="flex items-center gap-1.5">
                      <ShieldCheck className="h-3.5 w-3.5 text-emerald-600" />
                      {labItem.test_cases_count ?? 3} Test Assertions
                    </span>
                    <span className="font-mono text-[11px] text-slate-500">Docker Sandbox</span>
                  </div>

                  {labItem.tags && labItem.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1.5">
                      {labItem.tags.slice(0, 3).map((tag, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-0.5 rounded bg-slate-100 text-slate-600 text-[10px] font-medium"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  )}
                </CardContent>

                <CardFooter className="pt-3 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-[11px] font-semibold text-slate-400">
                    ~20 mins
                  </span>

                  <Link href={`/labs/${labItem.id}`}>
                    <Button
                      size="sm"
                      className="bg-[#1E3A8A] hover:bg-[#172554] text-white text-xs font-semibold px-4 cursor-pointer"
                    >
                      Open Workspace <ArrowRight className="h-3.5 w-3.5 ml-1" />
                    </Button>
                  </Link>
                </CardFooter>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
