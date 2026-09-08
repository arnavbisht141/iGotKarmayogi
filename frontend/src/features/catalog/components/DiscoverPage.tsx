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
  Sparkles,
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
} from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { fetchApi } from "@/lib/api";
import { CoursePreview } from "@/lib/types";
import { useI18n } from "@/lib/i18n";

function DiscoverContent() {
  const { t, language } = useI18n();
  const searchParams = useSearchParams();

  const [query, setQuery] = useState(searchParams?.get("q") || "");
  const [category, setCategory] = useState(searchParams?.get("category") || "all");
  const [difficulty, setDifficulty] = useState("all");
  const [source, setSource] = useState(searchParams?.get("source") || "all");
  const [sort, setSort] = useState("popular");

  const [courses, setCourses] = useState<CoursePreview[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [trendingSearches, setTrendingSearches] = useState<string[]>([]);
  const [recentSearches, setRecentSearches] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchCourses = () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (query) params.append("q", query);
    if (category && category !== "all") params.append("category", category);
    if (difficulty && difficulty !== "all") params.append("difficulty", difficulty);
    if (source && source !== "all") params.append("source", source);
    if (sort) params.append("sort", sort);

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

  useEffect(() => {
    fetchCourses();
  }, [category, difficulty, source, sort]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchCourses();
  };

  const handleResetFilters = () => {
    setQuery("");
    setCategory("all");
    setDifficulty("all");
    setSource("all");
    setSort("popular");
  };

  const hasActiveFilters =
    query !== "" || category !== "all" || difficulty !== "all" || source !== "all" || sort !== "popular";

  // Helper for localized course text
  const getCourseTitle = (course: CoursePreview) => {
    const key = `course.${course.id}.title`;
    const translated = t(key);
    return translated !== key ? translated : course.title;
  };

  const getCourseOverview = (course: CoursePreview) => {
    const key = `course.${course.id}.overview`;
    const translated = t(key);
    return translated !== key ? translated : course.overview;
  };

  const getCourseOrg = (course: CoursePreview) => {
    const key = `org.${course.organization}`;
    const translated = t(key);
    return translated !== key ? translated : course.organization;
  };

  const getCategoryLabel = (cat: string) => {
    const key = `category.${cat}`;
    const translated = t(key);
    return translated !== key ? translated : cat;
  };

  const getTopicLabel = (topic: string) => {
    const key = `topic.${topic}`;
    const translated = t(key);
    return translated !== key ? translated : topic;
  };

  const getDifficultyLabel = (diff: string) => {
    switch (diff.toLowerCase()) {
      case "beginner":
        return t("discover.beginner");
      case "intermediate":
        return t("discover.intermediate");
      case "advanced":
        return t("discover.advanced");
      default:
        return diff;
    }
  };

  return (
    <div className="min-h-[calc(100vh-68px)] flex flex-col bg-[#F8FAFC] w-full text-slate-900">
      {/* 1. Official Institutional Catalogue Header */}
      <section className="bg-white border-b border-slate-200 py-10 sm:py-14">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          {/* Institutional Eyebrow - Clean typography, no AI pill box */}
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#1E3A8A] mb-2">
            <Building2 className="h-4 w-4 text-[#1E3A8A]" />
            <span>{t("discover.eyebrow")}</span>
          </div>

          {/* Main Title */}
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-slate-900 tracking-tight leading-tight">
            {t("discover.title")}
          </h1>

          {/* Subtitle */}
          <p className="mt-2 text-sm sm:text-base text-slate-600 max-w-3xl leading-relaxed">
            {t("discover.subtitle")}
          </p>

          {/* Global Search Bar */}
          <form onSubmit={handleSearchSubmit} className="mt-6 flex flex-col sm:flex-row gap-2.5 max-w-3xl">
            <div className="relative flex-1">
              <Search className="absolute left-3.5 top-3.5 h-4 w-4 text-slate-400" />
              <Input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={t("discover.searchPlaceholder")}
                className="pl-10 pr-9 h-11 text-xs sm:text-sm rounded-lg border-slate-300 focus-visible:ring-[#1E3A8A] bg-white shadow-2xs"
              />
              {query && (
                <button
                  type="button"
                  onClick={() => setQuery("")}
                  className="absolute right-3 top-3.5 text-slate-400 hover:text-slate-600 cursor-pointer"
                  title={t("discover.clearSearch")}
                >
                  <X className="h-4 w-4" />
                </button>
              )}
            </div>
            <Button
              type="submit"
              className="h-11 px-6 bg-[#1E3A8A] hover:bg-[#172554] text-white text-xs sm:text-sm font-medium rounded-lg shadow-xs transition-colors flex items-center justify-center gap-2 cursor-pointer border border-[#1E3A8A]"
            >
              <Search className="h-4 w-4" />
              <span>{t("discover.searchBtn")}</span>
            </Button>
          </form>

          {/* Trending & Recent Searches - Clean slate pills, zero emojis */}
          <div className="mt-5 flex flex-wrap items-center gap-2 text-xs">
            <span className="text-slate-500 flex items-center gap-1.5 font-medium">
              <TrendingUp className="h-3.5 w-3.5 text-amber-600" />
              {t("discover.trending")}
            </span>
            {trendingSearches.map((ts) => (
              <button
                key={ts}
                onClick={() => {
                  setQuery(ts);
                  setCategory("all");
                }}
                className="px-3 py-1 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] sm:text-xs font-medium transition-colors cursor-pointer border border-slate-200/60"
              >
                {getTopicLabel(ts)}
              </button>
            ))}

            {recentSearches.length > 0 && (
              <div className="w-full flex flex-wrap items-center gap-2 mt-3 pt-3 border-t border-slate-100 text-xs text-slate-500">
                <span className="flex items-center gap-1 font-medium">
                  <History className="h-3.5 w-3.5 text-slate-400" />
                  {t("discover.recent")}
                </span>
                {recentSearches.map((rs, idx) => (
                  <button
                    key={idx}
                    onClick={() => setQuery(rs)}
                    className="text-[#1E3A8A] hover:underline font-medium cursor-pointer"
                  >
                    {rs}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* 2. Main Catalogue Workspace */}
      <section className="py-8 sm:py-10 flex-1 w-full">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
          {/* Discipline / Category Segmented Bar - No emojis, unified Navy active state */}
          <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none text-xs">
            <button
              onClick={() => setCategory("all")}
              className={`px-4 py-2 rounded-lg font-medium transition-all cursor-pointer whitespace-nowrap border ${
                category === "all"
                  ? "bg-[#1E3A8A] text-white border-[#1E3A8A] shadow-xs"
                  : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50 hover:border-slate-300"
              }`}
            >
              {t("discover.all")}
            </button>
            <button
              onClick={() => setCategory("popular")}
              className={`px-4 py-2 rounded-lg font-medium transition-all cursor-pointer whitespace-nowrap border ${
                category === "popular"
                  ? "bg-[#1E3A8A] text-white border-[#1E3A8A] shadow-xs"
                  : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50 hover:border-slate-300"
              }`}
            >
              {t("discover.popular")}
            </button>
            <button
              onClick={() => setCategory("new")}
              className={`px-4 py-2 rounded-lg font-medium transition-all cursor-pointer whitespace-nowrap border ${
                category === "new"
                  ? "bg-[#1E3A8A] text-white border-[#1E3A8A] shadow-xs"
                  : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50 hover:border-slate-300"
              }`}
            >
              {t("discover.new")}
            </button>
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setCategory(cat)}
                className={`px-4 py-2 rounded-lg font-medium transition-all cursor-pointer whitespace-nowrap border ${
                  category === cat
                    ? "bg-[#1E3A8A] text-white border-[#1E3A8A] shadow-xs"
                    : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50 hover:border-slate-300"
                }`}
              >
                {getCategoryLabel(cat)}
              </button>
            ))}
          </div>

          {/* Filter & Sort Toolbar Ribbon */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 rounded-xl bg-white border border-slate-200 shadow-2xs text-xs">
            {/* Left: Result Count & Active Filter Reset */}
            <div className="flex items-center gap-3">
              <span className="font-semibold text-slate-900 text-sm">
                {courses.length === 1
                  ? t("discover.showingSingle")
                  : t("discover.showingMultiple").replace("{count}", courses.length.toString())}
              </span>
              {hasActiveFilters && (
                <button
                  onClick={handleResetFilters}
                  className="flex items-center gap-1 text-[11px] text-[#1E3A8A] hover:underline font-medium cursor-pointer ml-2"
                >
                  <RotateCcw className="h-3 w-3" />
                  {t("discover.resetFilters")}
                </button>
              )}
            </div>

            {/* Right: Select Controls */}
            <div className="flex flex-wrap items-center gap-3">
              {/* Provider Filter */}
              <div className="flex items-center gap-1.5">
                <Filter className="h-3.5 w-3.5 text-slate-400" />
                <select
                  value={source}
                  onChange={(e) => setSource(e.target.value)}
                  className="rounded-lg border border-slate-200 px-2.5 py-1.5 bg-white text-slate-800 text-xs font-medium focus:outline-hidden focus:border-[#1E3A8A] cursor-pointer"
                >
                  <option value="all">{t("discover.allProviders")}</option>
                  <option value="internal">{t("discover.mospiInternal")}</option>
                  <option value="external">{t("discover.externalAccredited")}</option>
                </select>
              </div>

              {/* Difficulty Filter */}
              <div className="flex items-center gap-1.5">
                <select
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                  className="rounded-lg border border-slate-200 px-2.5 py-1.5 bg-white text-slate-800 text-xs font-medium focus:outline-hidden focus:border-[#1E3A8A] cursor-pointer"
                >
                  <option value="all">{t("discover.allDifficulties")}</option>
                  <option value="beginner">{t("discover.beginner")}</option>
                  <option value="intermediate">{t("discover.intermediate")}</option>
                  <option value="advanced">{t("discover.advanced")}</option>
                </select>
              </div>

              {/* Sort Order */}
              <div className="flex items-center gap-1.5 border-l border-slate-200 pl-3">
                <ArrowUpDown className="h-3.5 w-3.5 text-slate-400" />
                <span className="text-slate-500 font-medium">{t("discover.sort")}:</span>
                <select
                  value={sort}
                  onChange={(e) => setSort(e.target.value)}
                  className="rounded-lg border border-slate-200 px-2.5 py-1.5 bg-white text-slate-800 text-xs font-medium focus:outline-hidden focus:border-[#1E3A8A] cursor-pointer"
                >
                  <option value="popular">{t("discover.sortPopular")}</option>
                  <option value="rating">{t("discover.sortRating")}</option>
                  <option value="new">{t("discover.sortNew")}</option>
                  <option value="duration">{t("discover.sortDuration")}</option>
                </select>
              </div>
            </div>
          </div>

          {/* 3. Courses Grid */}
          {loading ? (
            <div className="py-24 text-center text-xs text-slate-500">
              <div className="h-8 w-8 rounded-full border-3 border-slate-200 border-t-[#1E3A8A] animate-spin mx-auto mb-3" />
              {t("discover.updating")}
            </div>
          ) : courses.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {courses.map((course) => (
                <Card
                  key={course.id}
                  className="border-slate-200 bg-white flex flex-col justify-between hover:border-[#1E3A8A]/40 hover:shadow-md transition-all duration-200 rounded-xl overflow-hidden"
                >
                  <div className="p-6">
                    {/* Card Top: Provider Badge & Duration */}
                    <div className="flex items-center justify-between gap-2 mb-3">
                      <span
                        className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-md border ${
                          course.source === "external"
                            ? "bg-amber-50 text-amber-900 border-amber-200/70"
                            : "bg-blue-50 text-[#1E3A8A] border-blue-200/70"
                        }`}
                      >
                        {course.source === "external"
                          ? t("discover.externalBadge")
                          : t("discover.internalBadge")}
                      </span>
                      <span className="flex items-center gap-1 text-xs text-slate-500 font-medium">
                        <Clock className="h-3.5 w-3.5 text-slate-400" />
                        {course.duration_hours} {t("discover.hours")}
                      </span>
                    </div>

                    {/* Title */}
                    <h3 className="text-base font-bold text-slate-900 leading-snug mb-2 line-clamp-2 hover:text-[#1E3A8A] transition-colors">
                      {getCourseTitle(course)}
                    </h3>

                    {/* Overview Description */}
                    <p className="text-xs text-slate-600 line-clamp-3 mb-4 leading-relaxed">
                      {getCourseOverview(course)}
                    </p>

                    {/* Metadata Details */}
                    <div className="space-y-2 text-xs text-slate-500 pt-3 border-t border-slate-100">
                      <div className="flex items-center justify-between">
                        <span className="text-slate-500">{t("discover.accreditedBody")}</span>
                        <span className="font-semibold text-slate-800 text-right truncate max-w-[180px]">
                          {getCourseOrg(course)}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-slate-500">{t("discover.targetDifficulty")}</span>
                        <span className="font-medium text-slate-700">
                          {getDifficultyLabel(course.difficulty)}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-slate-500">{t("discover.modules")}</span>
                        <span className="font-medium text-slate-700">
                          {course.modules_count} {t("discover.units")}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Card Action Footer */}
                  <div className="p-4 pt-3 border-t border-slate-100 bg-slate-50/60 flex items-center justify-between">
                    <div className="flex items-center gap-1.5 text-xs text-slate-600">
                      <Star className="h-3.5 w-3.5 fill-amber-400 text-amber-500" />
                      <span className="font-bold text-slate-900">{course.rating}</span>
                      <span className="text-slate-400">•</span>
                      <span className="text-slate-500">
                        {course.enrolled_count} {t("discover.enrolled")}
                      </span>
                    </div>
                    <a href={`/courses/${course.id}`}>
                      <Button
                        size="sm"
                        className="bg-[#1E3A8A] hover:bg-[#172554] text-white text-xs font-medium rounded-lg h-8 px-3.5 shadow-2xs transition-colors flex items-center cursor-pointer border border-[#1E3A8A]"
                      >
                        {t("discover.viewCourse")}
                        <ChevronRight className="h-3.5 w-3.5 ml-1" />
                      </Button>
                    </a>
                  </div>
                </Card>
              ))}
            </div>
          ) : (
            /* Empty State */
            <div className="py-20 text-center bg-white rounded-xl border border-slate-200 max-w-xl mx-auto p-8 shadow-2xs">
              <BookOpen className="h-10 w-10 text-slate-400 mx-auto mb-3" />
              <h3 className="text-base font-bold text-slate-900">{t("discover.noCoursesFound")}</h3>
              <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto leading-relaxed">
                {t("discover.noCoursesDesc")}
              </p>
              <Button
                variant="outline"
                size="sm"
                onClick={handleResetFilters}
                className="mt-5 text-xs rounded-lg border-slate-300 text-[#1E3A8A] hover:bg-slate-50 cursor-pointer"
              >
                <RotateCcw className="h-3.5 w-3.5 mr-1.5" />
                {t("discover.resetFilters")}
              </Button>
            </div>
          )}

          {/* 4. Institutional Accreditation Ribbon */}
          <div className="pt-6 pb-2 border-t border-slate-200/80 flex flex-wrap items-center justify-center gap-x-8 gap-y-2 text-xs text-slate-500">
            <span className="flex items-center gap-1.5 font-medium text-slate-600">
              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
              {t("discover.trustTag1")}
            </span>
            <span className="flex items-center gap-1.5 font-medium text-slate-600">
              <ShieldCheck className="h-3.5 w-3.5 text-[#1E3A8A]" />
              {t("discover.trustTag2")}
            </span>
            <span className="flex items-center gap-1.5 font-medium text-slate-600">
              <Award className="h-3.5 w-3.5 text-amber-600" />
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
          <div className="h-8 w-8 rounded-full border-3 border-slate-200 border-t-[#1E3A8A] animate-spin" />
        </div>
      }
    >
      <DiscoverContent />
    </Suspense>
  );
}
