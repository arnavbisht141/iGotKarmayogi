"use client";

import React, { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import {
  Search,
  Filter,
  ArrowUpDown,
  BookOpen,
  Building2,
  Clock,
  ChevronRight,
  History,
  TrendingUp,
  X,
  RotateCcw,
  Star,
  UserCheck,
  Award,
  ShieldCheck,
  CheckCircle2,
  Zap,
} from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { fetchApi } from "@/lib/api";
import { CoursePreview } from "@/lib/types";
import { useI18n } from "@/lib/i18n";

/** Accent color for category based course stripe */
const getCategoryAccent = (category: string): string => {
  const map: Record<string, string> = {
    statistics: "bg-[#1E3A8A]",
    economics:  "bg-[#0D9488]",
    survey:     "bg-amber-500",
    finance:    "bg-[#B45309]",
    technology: "bg-[#059669]",
    management: "bg-slate-600",
    policy:     "bg-purple-600",
  };
  return map[category?.toLowerCase()] ?? "bg-[#1E3A8A]";
};

const getDifficultyDot = (diff: string) => {
  switch ((diff || "").toLowerCase()) {
    case "beginner":     return "bg-[#059669]";
    case "intermediate": return "bg-amber-500";
    case "advanced":     return "bg-red-500";
    default:             return "bg-slate-400";
  }
};

function DiscoverContent() {
  const { t, language } = useI18n();
  const searchParams = useSearchParams();

  const [query, setQuery]         = useState(searchParams?.get("q") || "");
  const [category, setCategory]   = useState(searchParams?.get("category") || "all");
  const [difficulty, setDifficulty] = useState("all");
  const [source, setSource]       = useState(searchParams?.get("source") || "all");
  const [sort, setSort]           = useState("popular");

  const [courses, setCourses]               = useState<CoursePreview[]>([]);
  const [categories, setCategories]         = useState<string[]>([]);
  const [trendingSearches, setTrendingSearches] = useState<string[]>([]);
  const [recentSearches, setRecentSearches] = useState<string[]>([]);
  const [loading, setLoading]               = useState(true);

  const fetchCourses = () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (query)                      params.append("q", query);
    if (category && category !== "all")     params.append("category", category);
    if (difficulty && difficulty !== "all") params.append("difficulty", difficulty);
    if (source && source !== "all")         params.append("source", source);
    if (sort)                       params.append("sort", sort);

    fetchApi<{
      courses: CoursePreview[];
      categories: string[];
      trending_searches: string[];
      user_recent_searches: string[];
    }>(`/discover/courses?${params.toString()}`)
      .then((res) => {
        setCourses(res.courses);
        setCategories(res.categories);
        setTrendingSearches(res.trending_searches);
        setRecentSearches(res.user_recent_searches);
      })
      .catch((err) => console.error("Error fetching discover courses:", err))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchCourses(); }, [category, difficulty, source, sort]);

  const handleSearchSubmit = (e: React.FormEvent) => { e.preventDefault(); fetchCourses(); };
  const handleResetFilters = () => {
    setQuery(""); setCategory("all"); setDifficulty("all"); setSource("all"); setSort("popular");
  };

  const hasActiveFilters = query !== "" || category !== "all" || difficulty !== "all" || source !== "all" || sort !== "popular";

  const getCourseTitle = (course: CoursePreview) => {
    const key = `course.${course.id}.title`;
    const t2 = t(key);
    return t2 !== key ? t2 : course.title;
  };
  const getCourseOverview = (course: CoursePreview) => {
    const key = `course.${course.id}.overview`;
    const t2 = t(key);
    return t2 !== key ? t2 : course.overview;
  };
  const getCourseOrg = (course: CoursePreview) => {
    const key = `org.${course.organization}`;
    const t2 = t(key);
    return t2 !== key ? t2 : course.organization;
  };
  const getCategoryLabel = (cat: string) => {
    const key = `category.${cat}`;
    const t2 = t(key);
    return t2 !== key ? t2 : cat;
  };
  const getTopicLabel = (topic: string) => {
    const key = `topic.${topic}`;
    const t2 = t(key);
    return t2 !== key ? t2 : topic;
  };
  const getDifficultyLabel = (diff: string) => {
    switch (diff.toLowerCase()) {
      case "beginner":     return t("discover.beginner");
      case "intermediate": return t("discover.intermediate");
      case "advanced":     return t("discover.advanced");
      default:             return diff;
    }
  };

  return (
    <div className="min-h-[calc(100vh-68px)] flex flex-col bg-[#F8FAFC] w-full text-slate-900">

      {/* ═══════════════════════════════════════════
          Header: Sovereign Navy Search Console
          ═══════════════════════════════════════════ */}
      <section className="bg-[#0B132B] text-white py-10 sm:py-12 border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          {/* Eyebrow */}
          <div className="text-xs font-semibold text-amber-400 tracking-wider uppercase mb-1.5">
            {t("discover.eyebrow")}
          </div>

          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-white tracking-tight leading-tight">
            {t("discover.title")}
          </h1>
          <p className="mt-2 text-xs sm:text-sm text-slate-300 max-w-3xl leading-relaxed">
            {t("discover.subtitle")}
          </p>

          {/* Search Bar: High-contrast solid input */}
          <form onSubmit={handleSearchSubmit} className="mt-6 flex flex-col sm:flex-row gap-2 max-w-3xl">
            <div className="relative flex-1">
              <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={t("discover.searchPlaceholder")}
                className="w-full pl-10 pr-9 h-11 text-xs rounded-lg bg-white text-slate-900 placeholder-slate-400 border border-slate-300 focus:outline-none focus:ring-2 focus:ring-[#1E3A8A] transition-colors"
              />
              {query && (
                <button type="button" onClick={() => setQuery("")}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 cursor-pointer">
                  <X className="h-4 w-4" />
                </button>
              )}
            </div>
            <Button type="submit"
              className="h-11 px-6 bg-[#1E3A8A] hover:bg-[#162E70] text-white text-xs font-semibold rounded-lg border border-[#162E70] flex items-center justify-center gap-2 cursor-pointer active:translate-y-[1px]">
              <Search className="h-4 w-4" />
              {t("discover.searchBtn")}
            </Button>
          </form>

          {/* Trending searches */}
          <div className="mt-5 flex flex-wrap items-center gap-2 text-xs">
            <span className="text-slate-400 flex items-center gap-1.5 font-semibold">
              <TrendingUp className="h-3.5 w-3.5 text-amber-400" />
              {t("discover.trending")}
            </span>
            {trendingSearches.map((ts) => (
              <button key={ts}
                onClick={() => { setQuery(ts); setCategory("all"); }}
                className="px-2.5 py-1 rounded-md bg-slate-900 border border-slate-700 text-slate-300 hover:text-white hover:border-slate-500 text-[11px] font-medium cursor-pointer transition-colors active:translate-y-[1px]">
                {getTopicLabel(ts)}
              </button>
            ))}
            {recentSearches.length > 0 && (
              <div className="w-full flex flex-wrap items-center gap-2 mt-2 text-xs text-slate-400">
                <span className="flex items-center gap-1 font-semibold">
                  <History className="h-3.5 w-3.5 text-slate-500" />
                  {t("discover.recent")}
                </span>
                {recentSearches.map((rs, idx) => (
                  <button key={idx} onClick={() => setQuery(rs)}
                    className="text-amber-400 hover:underline font-semibold cursor-pointer">{rs}</button>
                ))}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════
          Catalogue Workspace
          ═══════════════════════════════════════════ */}
      <section className="py-8 sm:py-10 flex-1 w-full">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">

          {/* Category tabs */}
          <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none text-xs">
            {[
              { key: "all",     label: t("discover.all") },
              { key: "popular", label: t("discover.popular") },
              { key: "new",     label: t("discover.new") },
              ...categories.map(c => ({ key: c, label: getCategoryLabel(c) })),
            ].map((tab) => (
              <button key={tab.key}
                onClick={() => setCategory(tab.key)}
                className={`relative px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer whitespace-nowrap border ${
                  category === tab.key
                    ? "bg-[#1E3A8A] text-white border-[#162E70] shadow-xs"
                    : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50 hover:border-slate-300"
                }`}>
                {tab.label}
              </button>
            ))}
          </div>

          {/* Filter ribbon */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 rounded-2xl bg-white border border-slate-200 shadow-sm text-xs">
            <div className="flex items-center gap-3">
              <span className="font-bold text-slate-900 text-sm">
                {courses.length === 1
                  ? t("discover.showingSingle")
                  : t("discover.showingMultiple").replace("{count}", courses.length.toString())}
              </span>
              {hasActiveFilters && (
                <button onClick={handleResetFilters}
                  className="flex items-center gap-1 text-[11px] text-[#1E3A8A] hover:underline font-bold cursor-pointer">
                  <RotateCcw className="h-3 w-3" />
                  {t("discover.resetFilters")}
                </button>
              )}
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <div className="flex items-center gap-1.5">
                <Filter className="h-3.5 w-3.5 text-slate-400" />
                <select value={source} onChange={(e) => setSource(e.target.value)}
                  className="rounded-lg border border-slate-200 px-2.5 py-1.5 bg-white text-slate-700 text-xs font-semibold focus:outline-none focus:border-[#1E3A8A] cursor-pointer">
                  <option value="all">{t("discover.allProviders")}</option>
                  <option value="internal">{t("discover.mospiInternal")}</option>
                  <option value="external">{t("discover.externalAccredited")}</option>
                </select>
              </div>
              <div className="flex items-center gap-1.5">
                <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}
                  className="rounded-lg border border-slate-200 px-2.5 py-1.5 bg-white text-slate-700 text-xs font-semibold focus:outline-none focus:border-[#1E3A8A] cursor-pointer">
                  <option value="all">{t("discover.allDifficulties")}</option>
                  <option value="beginner">{t("discover.beginner")}</option>
                  <option value="intermediate">{t("discover.intermediate")}</option>
                  <option value="advanced">{t("discover.advanced")}</option>
                </select>
              </div>
              <div className="flex items-center gap-1.5 border-l border-slate-200 pl-3">
                <ArrowUpDown className="h-3.5 w-3.5 text-slate-400" />
                <span className="text-slate-400 font-semibold">{t("discover.sort")}:</span>
                <select value={sort} onChange={(e) => setSort(e.target.value)}
                  className="rounded-lg border border-slate-200 px-2.5 py-1.5 bg-white text-slate-700 text-xs font-semibold focus:outline-none focus:border-[#1E3A8A] cursor-pointer">
                  <option value="popular">{t("discover.sortPopular")}</option>
                  <option value="rating">{t("discover.sortRating")}</option>
                  <option value="new">{t("discover.sortNew")}</option>
                  <option value="duration">{t("discover.sortDuration")}</option>
                </select>
              </div>
            </div>
          </div>

          {/* Courses Grid */}
          {loading ? (
            <div className="py-24 text-center">
              <div className="h-9 w-9 rounded-full border-[3px] border-slate-200 border-t-[#1E3A8A] animate-spin mx-auto mb-3" />
              <p className="text-xs text-slate-400 font-medium">{t("discover.updating")}</p>
            </div>
          ) : courses.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {courses.map((course) => (
                <div key={course.id}
                  className="bg-white rounded-xl border border-slate-200 overflow-hidden flex flex-col shadow-xs hover:border-slate-300 transition-colors group">
                  <div className="p-5 flex flex-col flex-1">
                    {/* Top metadata */}
                    <div className="flex items-center justify-between gap-2 mb-3">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                        course.source === "external"
                          ? "bg-amber-50 text-amber-900 border-amber-300"
                          : "bg-blue-50 text-[#1E3A8A] border-blue-200"
                      }`}>
                        {course.source === "external" ? t("discover.externalBadge") : t("discover.internalBadge")}
                      </span>
                      <span className="flex items-center gap-1 text-xs text-slate-500 font-medium">
                        <Clock className="h-3.5 w-3.5 text-slate-400" />
                        {course.duration_hours} {t("discover.hours")}
                      </span>
                    </div>

                    {/* Title */}
                    <h3 className="text-base font-bold text-slate-900 leading-snug mb-2 line-clamp-2 group-hover:text-[#1E3A8A] transition-colors">
                      {getCourseTitle(course)}
                    </h3>

                    {/* Overview */}
                    <p className="text-xs text-slate-600 line-clamp-3 mb-4 leading-relaxed flex-1">
                      {getCourseOverview(course)}
                    </p>

                    {/* Metadata */}
                    <div className="space-y-1.5 text-xs text-slate-500 pt-3 border-t border-slate-100">
                      <div className="flex items-center justify-between">
                        <span>{t("discover.accreditedBody")}</span>
                        <span className="font-semibold text-slate-800 text-right truncate max-w-[160px]">
                          {getCourseOrg(course)}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span>{t("discover.targetDifficulty")}</span>
                        <span className="flex items-center gap-1.5 font-semibold text-slate-800">
                          <span className={`h-2 w-2 rounded-full ${getDifficultyDot(course.difficulty)}`} />
                          {getDifficultyLabel(course.difficulty)}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span>{t("discover.modules")}</span>
                        <span className="font-semibold text-slate-800">{course.modules_count} {t("discover.units")}</span>
                      </div>
                    </div>
                  </div>

                  {/* Card Footer */}
                  <div className="px-5 py-3.5 border-t border-slate-100 bg-slate-50 flex items-center justify-between">
                    <div className="flex items-center gap-1.5 text-xs text-slate-600">
                      <Star className="h-3.5 w-3.5 fill-amber-500 text-amber-500" />
                      <span className="font-bold text-slate-900 font-tabular">{course.rating}</span>
                      <span className="text-slate-300">•</span>
                      <span className="font-tabular">{course.enrolled_count} {t("discover.enrolled")}</span>
                    </div>
                    <a href={`/courses/${course.id}`}>
                      <Button size="sm"
                        className="bg-[#1E3A8A] hover:bg-[#162E70] text-white text-xs font-semibold rounded-lg h-8 px-3.5 border border-[#162E70] cursor-pointer flex items-center gap-1 active:translate-y-[1px]">
                        {t("discover.viewCourse")}
                        <ChevronRight className="h-3.5 w-3.5" />
                      </Button>
                    </a>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="py-20 text-center bg-white rounded-2xl border border-slate-200 max-w-xl mx-auto p-8 shadow-sm">
              <BookOpen className="h-12 w-12 text-slate-300 mx-auto mb-4" />
              <h3 className="text-base font-bold text-slate-900">{t("discover.noCoursesFound")}</h3>
              <p className="text-xs text-slate-400 mt-2 max-w-md mx-auto leading-relaxed">
                {t("discover.noCoursesDesc")}
              </p>
              <Button variant="outline" size="sm" onClick={handleResetFilters}
                className="mt-5 text-xs rounded-xl border-slate-300 text-[#1E3A8A] hover:bg-slate-50 cursor-pointer">
                <RotateCcw className="h-3.5 w-3.5 mr-1.5" />
                {t("discover.resetFilters")}
              </Button>
            </div>
          )}

          {/* Trust Ribbon */}
          <div className="pt-5 pb-2 border-t border-slate-200/80 flex flex-wrap items-center justify-center gap-x-8 gap-y-2 text-xs text-slate-400">
            <span className="flex items-center gap-1.5 font-medium">
              <CheckCircle2 className="h-3.5 w-3.5 text-[#059669]" />
              {t("discover.trustTag1")}
            </span>
            <span className="flex items-center gap-1.5 font-medium">
              <ShieldCheck className="h-3.5 w-3.5 text-[#1E3A8A]" />
              {t("discover.trustTag2")}
            </span>
            <span className="flex items-center gap-1.5 font-medium">
              <Award className="h-3.5 w-3.5 text-amber-500" />
              {t("discover.trustTag3")}
            </span>
          </div>
        </div>
      </section>
    </div>
  );
}

export default function DiscoverPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-[70vh] flex items-center justify-center bg-[#F8FAFC]">
          <div className="h-9 w-9 rounded-full border-[3px] border-slate-200 border-t-[#1E3A8A] animate-spin" />
        </div>
      }
    >
      <DiscoverContent />
    </Suspense>
  );
}
