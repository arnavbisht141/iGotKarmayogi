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
  Building2,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { fetchApi } from "@/lib/api";
import { LabDetail } from "@/lib/types/labs";
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
    <div className="min-h-[calc(100vh-65px)] bg-slate-50 flex flex-col w-full">
      {/* Hero Header - Full Edge-to-Edge with Digital Governance scale and looks */}
      <section className="hero-gradient relative overflow-hidden py-12 sm:py-16 w-full text-white shadow-md border-b border-blue-900/40">
        <div className="absolute inset-0 hero-mesh opacity-40 pointer-events-none" />
        <div className="absolute -top-20 -right-20 w-96 h-96 rounded-full bg-teal-500/15 blur-[100px] pointer-events-none" />

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full glass-light border border-white/20 text-xs font-bold text-teal-300 uppercase tracking-wider mb-4">
            <Building2 className="h-3.5 w-3.5" />
            Ministry of Statistics &amp; Programme Implementation (MoSPI)
          </div>

          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-tight text-white">
            Technical Competency &amp; Virtual Labs
          </h1>
          <p className="mt-4 text-sm sm:text-base lg:text-lg text-white/70 max-w-3xl leading-relaxed">
            Validate technical civil service workflows in isolated Docker sandboxes.
            Switch seamlessly between standard <strong>Jupyter Notebooks</strong> and modern reactive{" "}
            <strong>Marimo extensions</strong> with instant unit test verification.
          </p>

          {/* Core Interactive Action Buttons */}
          <div className="mt-8 flex flex-wrap items-center gap-4">
            <Link href="/labs/lab-data-cleaning-cpi">
              <Button
                size="lg"
                className="h-12 px-6 rounded-xl bg-white hover:bg-slate-100 text-[#1E3A8A] font-bold text-sm shadow-lg border-0 flex items-center gap-2.5 transition-transform hover:scale-105 cursor-pointer"
              >
                <FlaskConical className="h-5 w-5 text-[#1E3A8A]" />
                Launch Flagship Lab (Data Cleaning)
              </Button>
            </Link>

            <a href="#lab-catalog">
              <Button
                size="lg"
                variant="outline"
                className="h-12 px-6 rounded-xl border-white/30 hover:bg-white/15 text-white font-semibold text-sm flex items-center gap-2.5 cursor-pointer"
              >
                <Code2 className="h-5 w-5 text-teal-300" />
                Browse 6 Practical Labs
              </Button>
            </a>

            <Link href="/courses/3">
              <Button
                size="lg"
                variant="ghost"
                className="h-12 px-5 rounded-xl text-white/80 hover:text-white hover:bg-white/10 text-sm font-medium flex items-center gap-2 cursor-pointer"
              >
                <BookOpen className="h-4 w-4" />
                Browse Technical Courses
              </Button>
            </Link>
          </div>

          {/* Feature Badges */}
          <div className="mt-6 flex flex-wrap gap-3 pt-2">
            <div className="flex items-center gap-2 text-xs text-white/90 glass-light px-3 py-1.5 rounded-xl border border-white/15">
              <BookOpen className="h-4 w-4 text-amber-300" />
              <span>Jupyter Notebooks (.ipynb)</span>
            </div>
            <div className="flex items-center gap-2 text-xs text-white/90 glass-light px-3 py-1.5 rounded-xl border border-white/15">
              <Sparkles className="h-4 w-4 text-teal-300" />
              <span>Marimo Reactive DAG (.py)</span>
            </div>
            <div className="flex items-center gap-2 text-xs text-white/90 glass-light px-3 py-1.5 rounded-xl border border-white/15">
              <ShieldCheck className="h-4 w-4 text-blue-300" />
              <span>Docker Container Sandbox</span>
            </div>
          </div>
        </div>
      </section>

      {/* Main Body Content - Search, Filters, Grid */}
      <div id="lab-catalog" className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full space-y-8">

        {/* Search & Filter Controls */}
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search practical labs, skills, or objectives..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 py-2 text-xs rounded-xl border border-slate-200 focus:outline-hidden focus:border-[#1E3A8A] bg-slate-50/50"
            />
          </div>

          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-slate-400" />
            <span className="text-xs font-semibold text-slate-600">Difficulty:</span>
            <div className="flex gap-1">
              {["all", "beginner", "intermediate", "advanced"].map((d) => (
                <button
                  key={d}
                  onClick={() => setDifficultyFilter(d)}
                  className={`text-xs px-2.5 py-1 rounded-lg capitalize font-medium transition-all cursor-pointer ${
                    difficultyFilter === d
                      ? "bg-[#1E3A8A] text-white shadow-xs"
                      : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                  }`}
                >
                  {d}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Tags Bar */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
          {tags.map((t) => (
            <button
              key={t}
              onClick={() => setSelectedTag(t)}
              className={`text-xs px-3 py-1 rounded-full font-medium transition-all cursor-pointer shrink-0 ${
                selectedTag === t
                  ? "navy-teal-gradient text-white shadow-xs"
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
                      className="navy-teal-gradient text-white text-xs font-bold px-4 rounded-xl shadow-xs hover:opacity-95 transition-all cursor-pointer"
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
