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
  ExternalLink,
  ChevronRight,
  History,
  TrendingUp,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { fetchApi } from "@/lib/api";
import { CoursePreview } from "@/lib/types";
import { useI18n } from "@/lib/i18n";

function DiscoverContent() {
  const { t } = useI18n();
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

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header Banner */}
      <div className="rounded-2xl bg-white border border-slate-200 p-6 sm:p-8 shadow-xs">
        <Badge variant="saffron" className="mb-2">National Course Catalogue</Badge>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          {t("discover.title")}
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1 max-w-3xl">
          {t("discover.subtitle")}
        </p>

        {/* Global Search Bar */}
        <form onSubmit={handleSearchSubmit} className="mt-6 flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-3 h-4 w-4 text-slate-400" />
            <Input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={t("discover.searchPlaceholder")}
              className="pl-10 h-11 text-xs sm:text-sm rounded-xl"
            />
          </div>
          <Button type="submit" className="h-11 px-6 bg-slate-900 text-xs font-semibold rounded-xl">
            Search
          </Button>
        </form>

        {/* Trending & Recent Searches */}
        <div className="mt-4 flex flex-wrap items-center gap-2 text-xs">
          <span className="text-slate-400 flex items-center gap-1 font-medium">
            <TrendingUp className="h-3 w-3 text-amber-600" /> Trending:
          </span>
          {trendingSearches.map((ts) => (
            <button
              key={ts}
              onClick={() => {
                setQuery(ts);
                setCategory("all");
              }}
              className="px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 hover:bg-slate-200 text-[11px] font-medium transition-colors cursor-pointer"
            >
              {ts}
            </button>
          ))}

          {recentSearches.length > 0 && (
            <div className="w-full flex items-center gap-2 mt-2 pt-2 border-t border-slate-100 text-[11px] text-slate-400">
              <History className="h-3 w-3" />
              <span>Recent:</span>
              {recentSearches.map((rs, idx) => (
                <button
                  key={idx}
                  onClick={() => setQuery(rs)}
                  className="text-slate-600 hover:underline"
                >
                  {rs}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Category Pills */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
        <button
          onClick={() => setCategory("all")}
          className={`px-4 py-2 rounded-xl font-semibold transition-all cursor-pointer whitespace-nowrap ${
            category === "all"
              ? "bg-slate-900 text-white shadow-xs"
              : "bg-white text-slate-700 border border-slate-200 hover:bg-slate-50"
          }`}
        >
          {t("discover.all")}
        </button>
        <button
          onClick={() => setCategory("popular")}
          className={`px-4 py-2 rounded-xl font-semibold transition-all cursor-pointer whitespace-nowrap ${
            category === "popular"
              ? "bg-slate-900 text-white shadow-xs"
              : "bg-white text-slate-700 border border-slate-200 hover:bg-slate-50"
          }`}
        >
          🔥 {t("discover.popular")}
        </button>
        <button
          onClick={() => setCategory("new")}
          className={`px-4 py-2 rounded-xl font-semibold transition-all cursor-pointer whitespace-nowrap ${
            category === "new"
              ? "bg-slate-900 text-white shadow-xs"
              : "bg-white text-slate-700 border border-slate-200 hover:bg-slate-50"
          }`}
        >
          ✨ {t("discover.new")}
        </button>
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setCategory(cat)}
            className={`px-4 py-2 rounded-xl font-semibold transition-all cursor-pointer whitespace-nowrap ${
              category === cat
                ? "bg-slate-900 text-white shadow-xs"
                : "bg-white text-slate-700 border border-slate-200 hover:bg-slate-50"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Filters Bar & Results Counts */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-xl bg-white border border-slate-200 text-xs">
        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-slate-500" />
          <span className="font-semibold text-slate-700">Filters:</span>

          <select
            value={source}
            onChange={(e) => setSource(e.target.value)}
            className="rounded-lg border border-slate-300 px-2 py-1 bg-white text-slate-800"
          >
            <option value="all">All Providers</option>
            <option value="internal">MoSPI Internal Only</option>
            <option value="external">External Accredited (ISTM/DoPT)</option>
          </select>

          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            className="rounded-lg border border-slate-300 px-2 py-1 bg-white text-slate-800"
          >
            <option value="all">All Difficulties</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>

        <div className="flex items-center gap-2">
          <ArrowUpDown className="h-4 w-4 text-slate-500" />
          <span className="text-slate-500 font-medium">Sort:</span>
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value)}
            className="rounded-lg border border-slate-300 px-2 py-1 bg-white text-slate-800"
          >
            <option value="popular">Most Enrolled</option>
            <option value="rating">Highest Rated</option>
            <option value="new">Newly Published</option>
            <option value="duration">Shortest Duration</option>
          </select>
        </div>
      </div>

      {/* Courses Grid */}
      {loading ? (
        <div className="py-20 text-center text-xs text-slate-500">
          <div className="h-8 w-8 rounded-full border-4 border-slate-200 border-t-slate-800 animate-spin mx-auto mb-2" />
          Updating courses...
        </div>
      ) : courses.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <Card
              key={course.id}
              className="border-slate-200 bg-white flex flex-col justify-between hover:border-slate-400 hover:shadow-sm transition-all"
            >
              <div className="p-6">
                <div className="flex items-center justify-between gap-2 mb-3">
                  <Badge variant={course.source === "external" ? "external" : "secondary"}>
                    {course.source === "external" ? "ISTM External" : "MoSPI Internal"}
                  </Badge>
                  <span className="text-xs text-slate-500 font-medium">{course.duration_hours} Hours</span>
                </div>

                <h3 className="text-base font-bold text-slate-900 leading-snug mb-2 line-clamp-2">
                  {course.title}
                </h3>

                <p className="text-xs text-slate-600 line-clamp-3 mb-4 leading-relaxed">
                  {course.overview}
                </p>

                <div className="space-y-1.5 text-xs text-slate-500 pt-3 border-t border-slate-100">
                  <div className="flex items-center justify-between">
                    <span>Accredited Body:</span>
                    <span className="font-semibold text-slate-800">{course.organization}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Target Difficulty:</span>
                    <span className="capitalize text-slate-700">{course.difficulty}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Modules:</span>
                    <span className="text-slate-700">{course.modules_count} Units</span>
                  </div>
                </div>
              </div>

              <div className="p-4 pt-0 border-t border-slate-100 bg-slate-50/50 flex items-center justify-between">
                <div className="text-xs">
                  <span className="font-bold text-slate-900">{course.enrolled_count}</span>
                  <span className="text-slate-500"> enrolled</span>
                </div>
                <a href={`/courses/${course.id}`}>
                  <Button size="sm" className="bg-slate-900 hover:bg-slate-800 text-xs font-semibold">
                    View Course <ChevronRight className="h-3.5 w-3.5 ml-1" />
                  </Button>
                </a>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <div className="py-20 text-center bg-white rounded-xl border border-slate-200">
          <BookOpen className="h-10 w-10 text-slate-400 mx-auto mb-2" />
          <h3 className="text-sm font-bold text-slate-900">No matching courses found</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
            Try adjusting your search keyword or clearing selected difficulty and provider filters.
          </p>
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setQuery("");
              setCategory("all");
              setDifficulty("all");
              setSource("all");
            }}
            className="mt-4 text-xs"
          >
            Reset Filters
          </Button>
        </div>
      )}
    </div>
  );
}

export default function DiscoverPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-[70vh] flex items-center justify-center">
          <div className="h-8 w-8 rounded-full border-4 border-slate-200 border-t-amber-600 animate-spin" />
        </div>
      }
    >
      <DiscoverContent />
    </Suspense>
  );
}
