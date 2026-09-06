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
  Sparkles,
  ChevronRight,
  ShieldCheck,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
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
      .then((res) => {
        setData(res);
      })
      .catch((err) => console.error("Error loading dashboard summary:", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-[70vh] flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="h-8 w-8 rounded-full border-4 border-slate-200 border-t-amber-600 animate-spin" />
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

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Officer Welcome Banner */}
      <div className="rounded-2xl bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white p-6 sm:p-8 shadow-sm border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="h-2 w-2 rounded-full bg-emerald-400" />
            <span className="text-xs text-slate-400 font-medium tracking-wide uppercase">
              {learner.department}
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
            {t("home.welcome")}, {learner.full_name}
          </h1>
          <p className="text-xs sm:text-sm text-slate-300 mt-1 font-medium">
            {learner.designation} • Official Statistical Cadre Training Record
          </p>
        </div>

        <div className="flex items-center gap-4">
          <a href="/discover">
            <Button variant="saffron" size="sm" className="shadow-xs">
              <Compass className="h-4 w-4 mr-1.5" /> Browse Catalogue
            </Button>
          </a>
          <a href="/my-learning">
            <Button variant="outline" size="sm" className="text-white border-slate-700 hover:bg-slate-800">
              <BookOpen className="h-4 w-4 mr-1.5" /> My Learning
            </Button>
          </a>
        </div>
      </div>

      {/* Row 1: Continue Learning (Miro child) + Daily Goals & Streak (Written requirements) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Continue Learning & Current Course Progress */}
        <Card className="lg:col-span-2 border-slate-200 bg-white shadow-xs">
          <CardHeader className="pb-3 border-b border-slate-100 flex flex-row items-center justify-between">
            <div>
              <CardTitle className="text-base font-bold text-slate-900 flex items-center gap-2">
                <PlayCircle className="h-5 w-5 text-amber-600" />
                {t("home.continueLearning")}
              </CardTitle>
              <CardDescription className="text-xs">
                Resume your active coursework right where you paused
              </CardDescription>
            </div>
            {continueCourse && (
              <Badge variant="success" className="text-[10px]">In Progress</Badge>
            )}
          </CardHeader>
          <CardContent className="pt-4">
            {continueCourse ? (
              <div className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div>
                    <h3 className="text-base font-bold text-slate-900">
                      {continueCourse.course_title}
                    </h3>
                    <p className="text-xs text-slate-500 font-medium">
                      {continueCourse.current_module} • {continueCourse.current_lesson}
                    </p>
                  </div>
                  <a href={`/learn/${continueCourse.course_id}`}>
                    <Button size="sm" className="bg-slate-900 hover:bg-slate-800 text-white text-xs gap-1.5">
                      <PlayCircle className="h-4 w-4 text-amber-400" /> {t("home.resumeCourse")}
                    </Button>
                  </a>
                </div>

                <div className="space-y-1.5 pt-2">
                  <div className="flex justify-between text-xs font-semibold">
                    <span className="text-slate-600">Course Completion</span>
                    <span className="text-slate-900">{continueCourse.progress_percent}%</span>
                  </div>
                  <Progress value={continueCourse.progress_percent} indicatorClassName="bg-amber-600" />
                </div>
              </div>
            ) : (
              <div className="py-8 text-center space-y-3">
                <p className="text-xs text-slate-500">You do not currently have any course in progress.</p>
                <a href="/discover">
                  <Button size="sm" variant="outline" className="text-xs">
                    Explore & Enroll in Courses <ArrowRight className="h-3.5 w-3.5 ml-1" />
                  </Button>
                </a>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Today's Goals & Learning Streak (Written requirements confirmed in Phase 0) */}
        <div className="space-y-6">
          {/* Today's Goals */}
          <Card className="border-slate-200 bg-white shadow-xs">
            <CardContent className="p-5">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <div className="h-8 w-8 rounded-lg bg-indigo-50 text-indigo-700 flex items-center justify-center">
                    <Target className="h-4 w-4" />
                  </div>
                  <h4 className="text-xs font-bold text-slate-900">{t("home.todaysGoals")}</h4>
                </div>
                <span className="text-xs font-bold text-slate-900">
                  {todaysGoals.achieved_minutes} / {todaysGoals.target_minutes}m
                </span>
              </div>
              <Progress value={todaysGoals.percent} indicatorClassName="bg-indigo-600" />
              <p className="text-[11px] text-slate-500 mt-2">
                {todaysGoals.achieved_minutes >= todaysGoals.target_minutes
                  ? "🎉 Daily public service study goal achieved!"
                  : `${todaysGoals.target_minutes - todaysGoals.achieved_minutes} minutes remaining today`}
              </p>
            </CardContent>
          </Card>

          {/* Learning Streak */}
          <Card className="border-slate-200 bg-white shadow-xs">
            <CardContent className="p-5 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center border border-amber-200">
                  <Flame className="h-6 w-6" />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-slate-900">{t("home.learningStreak")}</h4>
                  <p className="text-xs text-slate-500">Active Daily Engagement</p>
                </div>
              </div>
              <div className="text-right">
                <span className="text-2xl font-black text-amber-600">{streak.streak_days}</span>
                <p className="text-[10px] text-slate-400 uppercase font-semibold">Days</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Row 2: Recommended / Suggested Courses (Miro child) */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-amber-600" />
              {t("home.recommended")}
            </h2>
            <p className="text-xs text-slate-500">
              Curated for your statistical cadre based on your ministry onboarding profile
            </p>
          </div>
          <a href="/discover" className="text-xs font-semibold text-slate-700 hover:text-slate-900 flex items-center gap-1">
            View All <ChevronRight className="h-3.5 w-3.5" />
          </a>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {recommendedCourses.map((c) => (
            <Card key={c.id} className="border-slate-200 bg-white flex flex-col justify-between hover:border-slate-400 transition-all">
              <div className="p-4">
                <div className="flex items-center justify-between gap-2 mb-2">
                  <Badge variant={c.source === "external" ? "external" : "secondary"}>
                    {c.source === "external" ? "ISTM External" : "MoSPI Internal"}
                  </Badge>
                  <span className="text-[11px] text-slate-500">{c.duration_hours} hrs</span>
                </div>
                <h4 className="font-bold text-slate-900 text-sm line-clamp-2 mb-1.5">
                  {c.title}
                </h4>
                <p className="text-xs text-slate-500 line-clamp-2 leading-relaxed">
                  {c.overview}
                </p>
              </div>
              <div className="p-4 pt-0 flex items-center justify-between border-t border-slate-100 mt-2 text-xs">
                <span className="text-slate-500 font-medium truncate max-w-[120px]">
                  {c.organization}
                </span>
                <a href={`/courses/${c.id}`} className="font-semibold text-amber-700 hover:text-amber-800">
                  Inspect Course →
                </a>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Row 3: Trending Courses & Future Planned Courses */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Trending Courses */}
        <Card className="border-slate-200 bg-white shadow-xs">
          <CardHeader className="pb-3 border-b border-slate-100 flex flex-row items-center justify-between">
            <div>
              <CardTitle className="text-base font-bold text-slate-900 flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-emerald-600" />
                {t("home.trending")}
              </CardTitle>
              <CardDescription className="text-xs">
                Popular training modules across central and state ministries
              </CardDescription>
            </div>
          </CardHeader>
          <CardContent className="p-4 space-y-3">
            {trendingCourses.slice(0, 3).map((tc) => (
              <a
                key={tc.id}
                href={`/courses/${tc.id}`}
                className="flex items-center justify-between p-3 rounded-lg hover:bg-slate-50 border border-slate-100 transition-colors block"
              >
                <div className="space-y-0.5">
                  <h5 className="text-xs font-bold text-slate-900">{tc.title}</h5>
                  <p className="text-[11px] text-slate-500">{tc.organization} • {tc.enrolled_count} civil servants enrolled</p>
                </div>
                <ChevronRight className="h-4 w-4 text-slate-400 shrink-0" />
              </a>
            ))}
          </CardContent>
        </Card>

        {/* Future Planned Courses */}
        <Card className="border-slate-200 bg-white shadow-xs">
          <CardHeader className="pb-3 border-b border-slate-100 flex flex-row items-center justify-between">
            <div>
              <CardTitle className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Calendar className="h-4 w-4 text-indigo-600" />
                {t("home.futurePlanned")}
              </CardTitle>
              <CardDescription className="text-xs">
                Queued capacity building modules for upcoming quarters
              </CardDescription>
            </div>
          </CardHeader>
          <CardContent className="p-4 space-y-3">
            {futurePlanned.length > 0 ? (
              futurePlanned.map((fc: any) => (
                <div
                  key={fc.id}
                  className="flex items-center justify-between p-3 rounded-lg bg-slate-50/70 border border-slate-200"
                >
                  <div>
                    <h5 className="text-xs font-bold text-slate-900">{fc.course_title}</h5>
                    <p className="text-[11px] text-slate-500">
                      Target: {fc.planned_for} • Scheduled by {fc.source === "admin" ? "Department Admin" : "Self"}
                    </p>
                  </div>
                  <a href={`/courses/${fc.course_id}`}>
                    <Button variant="outline" size="sm" className="h-7 text-xs">
                      View Syllabus
                    </Button>
                  </a>
                </div>
              ))
            ) : (
              <p className="text-xs text-slate-500 py-4 text-center">No future courses scheduled yet.</p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Row 4: My Learning Snapshot & Competencies Snapshot (Miro children) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* My Learning / Progress */}
        <Card className="border-slate-200 bg-white shadow-xs">
          <CardHeader className="pb-3 border-b border-slate-100 flex flex-row items-center justify-between">
            <CardTitle className="text-base font-bold text-slate-900 flex items-center gap-2">
              <BookOpen className="h-4 w-4 text-amber-600" />
              {t("home.myProgress")}
            </CardTitle>
            <a href="/my-learning" className="text-xs font-semibold text-slate-700 hover:text-slate-900">
              Full Record →
            </a>
          </CardHeader>
          <CardContent className="p-6">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                <p className="text-2xl font-extrabold text-slate-900">{progressStats.in_progress_count}</p>
                <p className="text-[11px] text-slate-500 font-medium">In Progress</p>
              </div>
              <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-100">
                <p className="text-2xl font-extrabold text-emerald-800">{progressStats.completed_count}</p>
                <p className="text-[11px] text-emerald-700 font-medium">Completed</p>
              </div>
              <div className="p-3 rounded-xl bg-indigo-50 border border-indigo-100">
                <p className="text-2xl font-extrabold text-indigo-800">{progressStats.hours_learned}h</p>
                <p className="text-[11px] text-indigo-700 font-medium">Learning Hours</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Competencies / Analytics */}
        <Card className="border-slate-200 bg-white shadow-xs">
          <CardHeader className="pb-3 border-b border-slate-100 flex flex-row items-center justify-between">
            <CardTitle className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Award className="h-4 w-4 text-amber-600" />
              {t("home.competencies")}
            </CardTitle>
            <a href="/progress" className="text-xs font-semibold text-slate-700 hover:text-slate-900">
              Competency Radar →
            </a>
          </CardHeader>
          <CardContent className="p-6">
            {competencies.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {competencies.map((skill: any) => (
                  <Badge key={skill.id} variant="saffron" className="text-xs py-1 px-3">
                    <CheckCircle2 className="h-3.5 w-3.5 mr-1.5 text-amber-700" />
                    {skill.name}
                  </Badge>
                ))}
              </div>
            ) : (
              <div className="text-center py-4 text-slate-500 text-xs">
                Complete assessments to earn verified statistical competencies.
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Row 5: Recently Explored Courses (Written requirement) */}
      {recentlyExplored.length > 0 && (
        <div>
          <h3 className="text-sm font-bold text-slate-700 uppercase tracking-wider mb-3 flex items-center gap-2">
            <History className="h-4 w-4 text-slate-400" />
            {t("home.recentlyExplored")}
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {recentlyExplored.map((re: any) => (
              <a
                key={re.id}
                href={`/courses/${re.id}`}
                className="p-3.5 rounded-xl border border-slate-200 bg-white hover:border-slate-400 transition-all block"
              >
                <h5 className="text-xs font-bold text-slate-900 truncate">{re.title}</h5>
                <p className="text-[11px] text-slate-500 mt-1">{re.organization} • {re.difficulty}</p>
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
