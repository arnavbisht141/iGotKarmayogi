"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  Compass,
  PlayCircle,
  Clock,
  Flame,
  Target,
  BookOpen,
  Award,
  ArrowRight,
  TrendingUp,
  History,
  Calendar,
  CheckCircle2,
  ChevronRight,
  ShieldCheck,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { fetchApi } from "@/lib/api";
import { useAuth } from "@/lib/auth/AuthContext";
import { useI18n } from "@/lib/i18n";
import { CoursePreview } from "@/lib/types";

export default function HomePage() {
  const router = useRouter();
  const { user } = useAuth();
  const { t } = useI18n();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchApi("/dashboard/summary")
      .then((res) => setData(res))
      .catch((err) => console.error("Error loading dashboard summary:", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-[70vh] flex items-center justify-center bg-[#F8FAFC]">
        <div className="flex flex-col items-center gap-3">
          <div className="h-8 w-8 rounded-full border-2 border-slate-300 border-t-[#1E3A8A] animate-spin" />
          <p className="text-xs text-slate-500 font-medium">Loading Karmayogi dashboard...</p>
        </div>
      </div>
    );
  }

  const learner = data?.learner || {
    full_name: user?.full_name || "Official",
    designation: "Senior Statistical Officer",
    department: "MoSPI",
  };

  const continueCourse = data?.continue_learning;
  const todaysGoals = data?.todays_goals || { target_minutes: 30, achieved_minutes: 20, percent: 66 };
  const streak = data?.learning_streak || { streak_days: 6 };
  const progressStats = data?.my_learning_progress || { in_progress_count: 1, completed_count: 0, overall_progress_percent: 66.7, hours_learned: 2.8 };
  const competencies = data?.competencies?.top_skills || [];
  const recommendedCourses: CoursePreview[] = data?.recommended_courses || [];
  const trendingCourses: CoursePreview[] = data?.trending_courses || [];
  const recentlyExplored = data?.recently_explored || [];
  const futurePlanned = data?.future_planned || [];

  const getCourseTitle = (id: number, fallback: string) => {
    const key = `course.${id}.title`;
    const translated = t(key);
    return translated !== key ? translated : fallback;
  };

  const getCourseOrg = (org: string) => {
    const key = `org.${org}`;
    const translated = t(key);
    return translated !== key ? translated : org;
  };

  const getDifficultyBadge = (difficulty: string) => {
    switch ((difficulty || "").toLowerCase()) {
      case "beginner":
        return "text-emerald-800 bg-emerald-50 border-emerald-300";
      case "intermediate":
        return "text-[#1E3A8A] bg-blue-50 border-blue-200";
      case "advanced":
        return "text-amber-800 bg-amber-50 border-amber-300";
      default:
        return "text-slate-700 bg-slate-100 border-slate-300";
    }
  };

  const getInitials = (name: string) =>
    name.split(" ").map((n: string) => n[0]).slice(0, 2).join("").toUpperCase();

  return (
    <div className="min-h-[calc(100vh-68px)] flex flex-col bg-[#F8FAFC] w-full text-slate-900">

      {/* ══════════════════════════════════════════════
          1. Officer Workstation Welcome Header
          ══════════════════════════════════════════════ */}
      <section className="bg-[#0B132B] text-white py-8 sm:py-10 border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="flex items-center gap-4">
              {/* Sovereign Initials Mark */}
              <div className="h-12 w-12 rounded-lg bg-[#1E3A8A] border border-[#254BAA] text-white flex items-center justify-center font-bold text-base shrink-0">
                {getInitials(learner.full_name)}
              </div>
              <div>
                <div className="text-xs font-semibold text-amber-400 tracking-wider uppercase mb-1">
                  {t("home.eyebrow")}
                </div>
                <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-white leading-tight">
                  {t("home.welcome")}, {learner.full_name}
                </h1>
                <p className="text-xs text-slate-300 mt-1 font-medium">
                  {learner.designation} • {learner.department} • {t("home.trainingRecord")}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2.5">
              <a href="/discover">
                <Button
                  size="sm"
                  className="bg-white hover:bg-slate-100 text-slate-950 text-xs font-semibold rounded-lg h-9 px-4 active:translate-y-[1px] flex items-center gap-1.5"
                >
                  <Compass className="h-4 w-4" />
                  {t("home.browseCatalogue")}
                </Button>
              </a>
              <a href="/my-learning">
                <Button
                  variant="outline"
                  size="sm"
                  className="bg-slate-900 hover:bg-slate-800 text-white border-slate-700 text-xs font-medium rounded-lg h-9 px-4 active:translate-y-[1px] flex items-center gap-1.5"
                >
                  <BookOpen className="h-4 w-4 text-slate-300" />
                  {t("home.myLearningBtn")}
                </Button>
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════
          2. Dashboard Workspace
          ══════════════════════════════════════════════ */}
      <section className="py-8 sm:py-10 flex-1 w-full">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">

          {/* Row 1: Continue Learning + Goals + Streak */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

            {/* Continue Learning */}
            <Card className="lg:col-span-2 border-slate-200 bg-white shadow-xs rounded-xl overflow-hidden">
              <CardHeader className="pb-3 border-b border-slate-100 flex flex-row items-center justify-between">
                <div>
                  <CardTitle className="text-sm font-bold text-slate-900 flex items-center gap-2">
                    <PlayCircle className="h-4 w-4 text-[#1E3A8A]" />
                    {t("home.continueLearning")}
                  </CardTitle>
                  <CardDescription className="text-xs text-slate-500 mt-0.5">
                    {t("home.activeCoursework")}
                  </CardDescription>
                </div>
                {continueCourse && (
                  <span className="text-[11px] font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                    {t("home.inProgress")}
                  </span>
                )}
              </CardHeader>
              <CardContent className="p-5">
                {continueCourse ? (
                  <div className="space-y-4">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                      <div>
                        <h3 className="text-sm font-bold text-slate-900">
                          {getCourseTitle(continueCourse.course_id, continueCourse.course_title)}
                        </h3>
                        <p className="text-xs text-slate-500 font-medium mt-0.5">
                          {continueCourse.current_module} • {continueCourse.current_lesson}
                        </p>
                      </div>
                      <a href={`/learn/${continueCourse.course_id}`}>
                        <Button
                          size="sm"
                          className="bg-[#1E3A8A] hover:bg-[#162E70] text-white text-xs font-semibold rounded-lg h-9 px-4 gap-1.5 border border-[#162E70] active:translate-y-[1px]"
                        >
                          <PlayCircle className="h-3.5 w-3.5" />
                          {t("home.resumeCourse")}
                        </Button>
                      </a>
                    </div>
                    <div className="space-y-1.5 pt-2">
                      <div className="flex justify-between text-xs font-semibold">
                        <span className="text-slate-600">{t("home.courseCompletion")}</span>
                        <span className="text-[#1E3A8A] font-tabular">{continueCourse.progress_percent}%</span>
                      </div>
                      <div className="relative h-2 bg-slate-200 rounded-full overflow-hidden">
                        <div
                          className="absolute inset-y-0 left-0 rounded-full bg-[#1E3A8A] transition-all duration-500"
                          style={{ width: `${continueCourse.progress_percent}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="py-8 text-center space-y-3">
                    <p className="text-xs text-slate-500">{t("home.noCourseInProgress")}</p>
                    <a href="/discover">
                      <Button
                        size="sm"
                        variant="outline"
                        className="text-xs rounded-lg border-slate-300 text-[#1E3A8A] hover:bg-slate-50 cursor-pointer"
                      >
                        {t("home.exploreEnroll")} <ArrowRight className="h-3.5 w-3.5 ml-1" />
                      </Button>
                    </a>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Goals + Streak column */}
            <div className="space-y-5">
              {/* Today's Goals */}
              <Card className="border-slate-200 bg-white shadow-xs rounded-xl overflow-hidden">
                <CardContent className="p-5">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <div className="h-7 w-7 rounded-md bg-blue-50 text-[#1E3A8A] flex items-center justify-center border border-blue-200">
                        <Target className="h-3.5 w-3.5" />
                      </div>
                      <h4 className="text-xs font-bold text-slate-900">{t("home.todaysGoals")}</h4>
                    </div>
                    <span className="text-xs font-bold text-slate-900 font-tabular">
                      {todaysGoals.achieved_minutes} / {todaysGoals.target_minutes}m
                    </span>
                  </div>
                  <div className="relative h-2 bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className="absolute inset-y-0 left-0 rounded-full bg-[#1E3A8A] transition-all duration-500"
                      style={{ width: `${todaysGoals.percent}%` }}
                    />
                  </div>
                  <p className="text-[11px] text-slate-500 mt-2 flex items-center gap-1.5 font-medium">
                    {todaysGoals.achieved_minutes >= todaysGoals.target_minutes ? (
                      <>
                        <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
                        <span>{t("home.dailyGoalAchieved")}</span>
                      </>
                    ) : (
                      <span>{t("home.minutesRemaining").replace("{minutes}", (todaysGoals.target_minutes - todaysGoals.achieved_minutes).toString())}</span>
                    )}
                  </p>
                </CardContent>
              </Card>

              {/* Learning Streak */}
              <Card className="border-slate-200 bg-white shadow-xs rounded-xl overflow-hidden">
                <CardContent className="p-5 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="h-9 w-9 rounded-lg bg-amber-50 border border-amber-200 flex items-center justify-center">
                      <Flame className="h-4 w-4 text-amber-700" />
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-slate-900">{t("home.learningStreak")}</h4>
                      <p className="text-xs text-slate-500 font-medium">{t("home.activeDailyEngagement")}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-2xl font-bold text-amber-700 font-tabular">{streak.streak_days}</span>
                    <p className="text-[10px] text-amber-800 uppercase font-bold tracking-wider">{t("home.days")}</p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Row 2: Recommended Courses */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-base font-bold text-slate-900 tracking-tight">
                  {t("home.recommended")}
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">{t("home.recommendedSubtitle")}</p>
              </div>
              <a href="/discover" className="text-xs font-semibold text-[#1E3A8A] hover:underline flex items-center gap-1 cursor-pointer">
                {t("home.viewAll")} <ChevronRight className="h-3.5 w-3.5" />
              </a>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
              {recommendedCourses.map((c) => (
                <Card
                  key={c.id}
                  className="border-slate-200 bg-white flex flex-col justify-between rounded-xl overflow-hidden shadow-xs hover:border-slate-300 transition-colors"
                >
                  <div className="p-4">
                    <div className="flex items-center justify-between gap-2 mb-2.5">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${getDifficultyBadge(c.difficulty)}`}>
                        {c.difficulty.toUpperCase()}
                      </span>
                      <span className="text-[11px] text-slate-500 font-medium flex items-center gap-1">
                        <Clock className="h-3 w-3" />{c.duration_hours}h
                      </span>
                    </div>
                    <h4 className="font-bold text-slate-900 text-sm line-clamp-2 mb-1.5 hover:text-[#1E3A8A] transition-colors">
                      {getCourseTitle(c.id, c.title)}
                    </h4>
                    <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed">{c.overview}</p>
                  </div>
                  <div className="p-4 pt-3 flex items-center justify-between border-t border-slate-100 bg-slate-50 text-xs">
                    <span className="text-slate-500 font-medium truncate max-w-[120px]">{getCourseOrg(c.organization)}</span>
                    <a href={`/courses/${c.id}`} className="font-semibold text-[#1E3A8A] hover:underline flex items-center gap-0.5 cursor-pointer">
                      {t("home.inspectCourse")} →
                    </a>
                  </div>
                </Card>
              ))}
            </div>
          </div>

          {/* Row 3: Trending + Future Planned */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Trending Courses */}
            <Card className="border-slate-200 bg-white shadow-xs rounded-xl overflow-hidden">
              <CardHeader className="pb-3 border-b border-slate-100 flex flex-row items-center justify-between">
                <div>
                  <CardTitle className="text-sm font-bold text-slate-900 flex items-center gap-2">
                    <TrendingUp className="h-4 w-4 text-[#1E3A8A]" />
                    {t("home.trending")}
                  </CardTitle>
                  <CardDescription className="text-xs text-slate-500 mt-0.5">{t("home.trendingSubtitle")}</CardDescription>
                </div>
              </CardHeader>
              <CardContent className="p-4 space-y-2">
                {trendingCourses.slice(0, 3).map((tc) => (
                  <a
                    key={tc.id}
                    href={`/courses/${tc.id}`}
                    className="flex items-center justify-between p-3 rounded-lg hover:bg-slate-50 border border-slate-100 hover:border-slate-200 transition-colors block cursor-pointer group"
                  >
                    <div className="space-y-0.5">
                      <h5 className="text-xs font-bold text-slate-900 group-hover:text-[#1E3A8A] transition-colors">
                        {getCourseTitle(tc.id, tc.title)}
                      </h5>
                      <p className="text-[11px] text-slate-500">
                        {getCourseOrg(tc.organization)} • {tc.enrolled_count} {t("home.civilServantsEnrolled")}
                      </p>
                    </div>
                    <ChevronRight className="h-4 w-4 text-slate-400 group-hover:text-[#1E3A8A] shrink-0 transition-colors" />
                  </a>
                ))}
              </CardContent>
            </Card>

            {/* Future Planned */}
            <Card className="border-slate-200 bg-white shadow-xs rounded-xl overflow-hidden">
              <CardHeader className="pb-3 border-b border-slate-100 flex flex-row items-center justify-between">
                <div>
                  <CardTitle className="text-sm font-bold text-slate-900 flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-[#1E3A8A]" />
                    {t("home.futurePlanned")}
                  </CardTitle>
                  <CardDescription className="text-xs text-slate-500 mt-0.5">{t("home.futurePlannedSubtitle")}</CardDescription>
                </div>
              </CardHeader>
              <CardContent className="p-4 space-y-2">
                {futurePlanned.length > 0 ? (
                  futurePlanned.map((fc: any) => (
                    <div key={fc.id} className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200/80 text-xs">
                      <div>
                        <h5 className="font-bold text-slate-900">{fc.course_title}</h5>
                        <p className="text-[11px] text-slate-500 mt-0.5">
                          {t("home.target")} {fc.planned_for} • {t("home.scheduledBy")}{" "}
                          {fc.source === "admin" ? t("home.departmentAdmin") : t("home.self")}
                        </p>
                      </div>
                      <a href={`/courses/${fc.course_id}`}>
                        <Button
                          variant="outline"
                          size="sm"
                          className="h-7 text-xs rounded-md border-slate-300 text-slate-700 hover:bg-white cursor-pointer"
                        >
                          {t("home.viewSyllabus")}
                        </Button>
                      </a>
                    </div>
                  ))
                ) : (
                  <p className="text-xs text-slate-500 py-6 text-center font-medium">{t("home.noFutureCourses")}</p>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Row 4: Learning Stats + Competencies */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* My Progress */}
            <Card className="border-slate-200 bg-white shadow-xs rounded-xl overflow-hidden">
              <CardHeader className="pb-3 border-b border-slate-100 flex flex-row items-center justify-between">
                <CardTitle className="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <BookOpen className="h-4 w-4 text-[#1E3A8A]" />
                  {t("home.myProgress")}
                </CardTitle>
                <a href="/my-learning" className="text-xs font-semibold text-[#1E3A8A] hover:underline cursor-pointer">
                  {t("home.fullRecord")} →
                </a>
              </CardHeader>
              <CardContent className="p-5">
                <div className="grid grid-cols-3 gap-3 text-center">
                  <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-200">
                    <p className="text-2xl font-bold text-slate-900 font-tabular">{progressStats.in_progress_count}</p>
                    <p className="text-[11px] text-slate-500 font-medium mt-1">{t("home.inProgress")}</p>
                  </div>
                  <div className="p-3.5 rounded-lg bg-emerald-50 border border-emerald-200">
                    <p className="text-2xl font-bold text-emerald-800 font-tabular">{progressStats.completed_count}</p>
                    <p className="text-[11px] text-emerald-900 font-medium mt-1">{t("home.completed")}</p>
                  </div>
                  <div className="p-3.5 rounded-lg bg-blue-50 border border-blue-200">
                    <p className="text-2xl font-bold text-[#1E3A8A] font-tabular">{progressStats.hours_learned}h</p>
                    <p className="text-[11px] text-[#1E3A8A] font-medium mt-1">{t("home.learningHours")}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Competencies */}
            <Card className="border-slate-200 bg-white shadow-xs rounded-xl overflow-hidden">
              <CardHeader className="pb-3 border-b border-slate-100 flex flex-row items-center justify-between">
                <CardTitle className="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <Award className="h-4 w-4 text-amber-700" />
                  {t("home.competencies")}
                </CardTitle>
                <a href="/progress" className="text-xs font-semibold text-[#1E3A8A] hover:underline cursor-pointer">
                  {t("home.competencyRadar")} →
                </a>
              </CardHeader>
              <CardContent className="p-5">
                {competencies.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {competencies.map((skill: any) => (
                      <span
                        key={skill.id}
                        className="text-xs font-medium py-1 px-2.5 rounded-md bg-amber-50 text-amber-900 border border-amber-300 flex items-center gap-1.5"
                      >
                        <CheckCircle2 className="h-3.5 w-3.5 text-amber-600" />
                        {skill.name}
                      </span>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-6 text-slate-500 text-xs font-medium">
                    {t("home.completeAssessmentsMsg")}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Row 5: Recently Explored */}
          {recentlyExplored.length > 0 && (
            <div>
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                <History className="h-4 w-4 text-slate-400" />
                {t("home.recentlyExplored")}
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {recentlyExplored.map((re: any) => (
                  <a
                    key={re.id}
                    href={`/courses/${re.id}`}
                    className="p-4 rounded-xl border border-slate-200 bg-white hover:border-slate-300 shadow-xs block cursor-pointer transition-colors"
                  >
                    <h5 className="text-xs font-bold text-slate-900 truncate hover:text-[#1E3A8A] transition-colors">
                      {getCourseTitle(re.id, re.title)}
                    </h5>
                    <p className="text-[11px] text-slate-500 mt-1">{getCourseOrg(re.organization)} • {re.difficulty}</p>
                  </a>
                ))}
              </div>
            </div>
          )}

          {/* Trust Ribbon */}
          <div className="pt-6 pb-2 border-t border-slate-200 flex flex-wrap items-center justify-center gap-x-8 gap-y-2 text-xs text-slate-500">
            <span className="flex items-center gap-1.5 font-medium">
              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
              {t("discover.trustTag1")}
            </span>
            <span className="flex items-center gap-1.5 font-medium">
              <ShieldCheck className="h-3.5 w-3.5 text-[#1E3A8A]" />
              {t("discover.trustTag2")}
            </span>
            <span className="flex items-center gap-1.5 font-medium">
              <Award className="h-3.5 w-3.5 text-amber-700" />
              {t("discover.trustTag3")}
            </span>
          </div>
        </div>
      </section>
    </div>
  );
}
