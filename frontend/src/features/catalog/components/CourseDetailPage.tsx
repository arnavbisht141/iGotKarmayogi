"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import {
  PlayCircle,
  Clock,
  Video,
  FileText,
  FlaskConical,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  ShieldCheck,
  ArrowRight,
  Star,
  Building2,
  BookOpen,
  Scale,
  Sparkles,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { fetchApi } from "@/lib/api";
import { CourseDetail } from "@/lib/types";
import { useAuth } from "@/lib/auth/AuthContext";
import { useI18n } from "@/lib/i18n";

export default function CourseDetailPage() {
  const { courseId } = useParams();
  const router = useRouter();
  const { user } = useAuth();
  const { t } = useI18n();

  const [course, setCourse] = useState<CourseDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(false);
  const [expandedModules, setExpandedModules] = useState<Record<number, boolean>>({});

  useEffect(() => {
    if (!courseId) return;
    fetchApi<CourseDetail>(`/courses/${courseId}`)
      .then((data) => {
        setCourse(data);
        if (data.modules && data.modules.length > 0) {
          setExpandedModules({ [data.modules[0].id]: true });
        }
      })
      .catch((err) => console.error("Error loading course details:", err))
      .finally(() => setLoading(false));
  }, [courseId]);

  const toggleModule = (modId: number) => {
    setExpandedModules((prev) => ({
      ...prev,
      [modId]: !prev[modId],
    }));
  };

  const handleEnrollOrResume = async () => {
    if (!user) {
      router.push("/login");
      return;
    }

    if (course?.enrollment) {
      router.push(`/learn/${course.id}`);
      return;
    }

    setEnrolling(true);
    try {
      await fetchApi(`/courses/${courseId}/enroll`, {
        method: "POST",
      });
      router.push(`/learn/${courseId}`);
    } catch (err: any) {
      alert(err.message || "Failed to enroll in course");
      setEnrolling(false);
    }
  };

  // Helper for localized course text
  const getCourseTitle = () => {
    if (!course) return "";
    const key = `course.${course.id}.title`;
    const translated = t(key);
    return translated !== key ? translated : course.title;
  };

  const getCourseOverview = () => {
    if (!course) return "";
    const key = `course.${course.id}.overview`;
    const translated = t(key);
    return translated !== key ? translated : course.overview;
  };

  const getCourseOrg = () => {
    if (!course) return "";
    const key = `org.${course.organization}`;
    const translated = t(key);
    return translated !== key ? translated : course.organization;
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

  if (loading) {
    return (
      <div className="min-h-[70vh] flex items-center justify-center bg-[#F8FAFC]">
        <div className="h-8 w-8 rounded-full border-3 border-slate-200 border-t-[#1E3A8A] animate-spin" />
      </div>
    );
  }

  if (!course) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center text-center px-4 bg-[#F8FAFC]">
        <BookOpen className="h-12 w-12 text-slate-400 mb-3" />
        <h2 className="text-xl font-bold text-slate-900">{t("course.notFound")}</h2>
        <p className="text-xs text-slate-500 mt-1 max-w-sm">{t("course.notFoundDesc")}</p>
        <a href="/discover">
          <Button
            variant="outline"
            size="sm"
            className="mt-5 text-xs rounded-lg border-slate-300 text-[#1E3A8A] hover:bg-slate-50 cursor-pointer"
          >
            {t("course.backToCatalogue")}
          </Button>
        </a>
      </div>
    );
  }

  const isEnrolled = !!course.enrollment;
  const progressPct = course.enrollment?.progress_percent || 0;

  return (
    <div className="min-h-[calc(100vh-68px)] flex flex-col bg-[#F8FAFC] w-full text-slate-900">
      {/* 1. Institutional Course Header */}
      <section className="bg-white border-b border-slate-200 py-8 sm:py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          {/* Eyebrow & Badges */}
          <div className="flex flex-wrap items-center gap-2 mb-3">
            <span
              className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-md border ${
                course.source === "external"
                  ? "bg-amber-50 text-amber-900 border-amber-200/80"
                  : "bg-blue-50 text-[#1E3A8A] border-blue-200/80"
              }`}
            >
              {course.source === "external"
                ? t("discover.externalBadge")
                : t("discover.internalBadge")}
            </span>
            <span className="text-xs text-slate-400">•</span>
            <span className="text-xs font-medium text-slate-600">
              {t(`category.${course.category}`) !== `category.${course.category}`
                ? t(`category.${course.category}`)
                : course.category}
            </span>
            <span className="text-xs text-slate-400">•</span>
            <span className="text-xs font-medium text-slate-600">
              {getDifficultyLabel(course.difficulty)}
            </span>
          </div>

          {/* Title */}
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-slate-900 tracking-tight leading-tight max-w-4xl">
            {getCourseTitle()}
          </h1>

          {/* Overview */}
          <p className="mt-3 text-sm sm:text-base text-slate-600 max-w-4xl leading-relaxed">
            {getCourseOverview()}
          </p>

          {/* Instructor & Accreditation Info Strip */}
          <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-4 py-4 border-y border-slate-100 text-xs">
            <div>
              <span className="text-slate-400 block font-medium">{t("course.instructor")}</span>
              <span className="font-bold text-slate-900 mt-0.5 block">{course.instructor}</span>
            </div>
            <div>
              <span className="text-slate-400 block font-medium">{t("course.organization")}</span>
              <span className="font-bold text-slate-900 mt-0.5 block">{getCourseOrg()}</span>
            </div>
            <div>
              <span className="text-slate-400 block font-medium">{t("course.duration")}</span>
              <span className="font-bold text-slate-900 mt-0.5 block flex items-center gap-1">
                <Clock className="h-3.5 w-3.5 text-slate-400" />
                {course.duration_hours} {t("course.learningHours")}
              </span>
            </div>
            <div>
              <span className="text-slate-400 block font-medium">{t("course.officialRating")}</span>
              <span className="font-bold text-slate-900 mt-0.5 flex items-center gap-1.5">
                <Star className="h-3.5 w-3.5 fill-amber-400 text-amber-500" />
                <span>{course.rating}</span>
                <span className="text-slate-400 font-normal">
                  ({course.enrolled_count} {t("course.enrolled")})
                </span>
              </span>
            </div>
          </div>

          {/* Start / Resume Action CTA */}
          <div className="mt-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <Button
                size="lg"
                onClick={handleEnrollOrResume}
                disabled={enrolling}
                className="h-11 px-6 rounded-lg bg-[#1E3A8A] hover:bg-[#172554] text-white font-medium text-sm shadow-xs transition-colors flex items-center gap-2 cursor-pointer border border-[#1E3A8A]"
              >
                <PlayCircle className="h-4 w-4" />
                {isEnrolled ? t("course.resume") : t("course.enrollNow")}
              </Button>
              {isEnrolled && (
                <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-3 py-1.5 rounded-lg border border-emerald-200">
                  {progressPct}% {t("course.completed")}
                </span>
              )}
            </div>

            {course.assessment_id && (
              <a href={`/assess/${course.assessment_id}`}>
                <Button
                  variant="outline"
                  size="sm"
                  className="text-xs rounded-lg border-slate-300 text-slate-700 hover:bg-slate-50 hover:border-slate-400 cursor-pointer"
                >
                  {t("course.takeAssessment")} <ArrowRight className="h-3.5 w-3.5 ml-1" />
                </Button>
              </a>
            )}
          </div>
        </div>
      </section>

      {/* 2. Syllabus & Materials Section */}
      <section className="py-8 sm:py-10 flex-1 w-full">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Column: Expandable Syllabus */}
            <div className="lg:col-span-2 space-y-6">
              <Card className="border-slate-200 bg-white shadow-2xs rounded-xl overflow-hidden">
                <CardHeader className="border-b border-slate-100 pb-4">
                  <CardTitle className="text-base font-bold text-slate-900">
                    {t("course.syllabus")}
                  </CardTitle>
                  <p className="text-xs text-slate-500">
                    {course.modules.length} {t("discover.units")} •{" "}
                    {course.counts.readings + course.counts.videos + course.counts.labs}{" "}
                    {t("course.learningHours")}
                  </p>
                </CardHeader>
                <CardContent className="p-4 space-y-3">
                  {course.modules.map((mod, idx) => {
                    const isExpanded = expandedModules[mod.id];
                    return (
                      <div
                        key={mod.id}
                        className="border border-slate-200 rounded-lg overflow-hidden transition-all"
                      >
                        <button
                          onClick={() => toggleModule(mod.id)}
                          className="w-full px-4 py-3 bg-slate-50 hover:bg-slate-100/80 flex items-center justify-between text-left transition-colors cursor-pointer"
                        >
                          <div className="flex items-center gap-3">
                            <span className="h-6 w-6 rounded-full bg-slate-200 text-slate-700 font-semibold text-xs flex items-center justify-center">
                              {idx + 1}
                            </span>
                            <div>
                              <h4 className="text-xs sm:text-sm font-bold text-slate-900">
                                {mod.title}
                              </h4>
                              <p className="text-[11px] text-slate-500">
                                {mod.lessons.length} {t("course.lessons")} • {mod.description}
                              </p>
                            </div>
                          </div>
                          {isExpanded ? (
                            <ChevronDown className="h-4 w-4 text-slate-500" />
                          ) : (
                            <ChevronRight className="h-4 w-4 text-slate-500" />
                          )}
                        </button>

                        {isExpanded && (
                          <div className="divide-y divide-slate-100 bg-white px-4 py-1">
                            {mod.lessons.map((lesson) => (
                              <div
                                key={lesson.id}
                                className="py-2.5 flex items-center justify-between text-xs hover:bg-slate-50/60 rounded px-2"
                              >
                                <div className="flex items-center gap-2.5">
                                  {lesson.content_type === "video" && (
                                    <Video className="h-3.5 w-3.5 text-amber-600" />
                                  )}
                                  {lesson.content_type === "lab" && (
                                    <FlaskConical className="h-3.5 w-3.5 text-indigo-600" />
                                  )}
                                  {lesson.content_type === "reading" && (
                                    <FileText className="h-3.5 w-3.5 text-slate-400" />
                                  )}
                                  <span className="font-medium text-slate-800">{lesson.title}</span>
                                </div>
                                <div className="flex items-center gap-3 text-slate-500">
                                  {lesson.has_activity && (
                                    <span className="text-[10px] bg-slate-100 text-slate-700 font-medium px-2 py-0.5 rounded border border-slate-200">
                                      {t("course.includesPractice")}
                                    </span>
                                  )}
                                  <span>{lesson.duration_minutes}m</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </CardContent>
              </Card>
            </div>

            {/* Sidebar Column: Materials Breakdown & Skills Gained */}
            <div className="space-y-6">
              {/* Materials Breakdown */}
              <Card className="border-slate-200 bg-white shadow-2xs rounded-xl overflow-hidden">
                <CardHeader className="pb-3 border-b border-slate-100">
                  <CardTitle className="text-xs sm:text-sm font-bold text-slate-900">
                    {t("course.materials")}
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-4 space-y-3 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-2 text-slate-600">
                      <Video className="h-3.5 w-3.5 text-amber-600" /> {t("course.videoLectures")}
                    </span>
                    <span className="font-bold text-slate-900">{course.counts.videos}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-2 text-slate-600">
                      <FileText className="h-3.5 w-3.5 text-slate-400" /> {t("course.readingModules")}
                    </span>
                    <span className="font-bold text-slate-900">{course.counts.readings}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-2 text-slate-600">
                      <FlaskConical className="h-3.5 w-3.5 text-indigo-600" />{" "}
                      {t("course.practicalLabs")}
                    </span>
                    <span className="font-bold text-slate-900">{course.counts.labs}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-2 text-slate-600">
                      <ShieldCheck className="h-3.5 w-3.5 text-emerald-600" /> {t("course.mcqTest")}
                    </span>
                    <span className="font-bold text-slate-900">{course.counts.assessments}</span>
                  </div>
                </CardContent>
              </Card>

              {/* Competencies Gained */}
              <Card className="border-slate-200 bg-white shadow-2xs rounded-xl overflow-hidden">
                <CardHeader className="pb-3 border-b border-slate-100">
                  <CardTitle className="text-xs sm:text-sm font-bold text-slate-900">
                    {t("course.skillsGained")}
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-4">
                  <div className="flex flex-wrap gap-1.5">
                    {course.skills_gained.map((skill, idx) => (
                      <span
                        key={idx}
                        className="text-[11px] font-medium bg-amber-50 text-amber-900 border border-amber-200/80 px-2.5 py-1 rounded-md flex items-center gap-1.5"
                      >
                        <CheckCircle2 className="h-3 w-3 text-amber-600" />
                        {skill}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* AI Behavioral & Oral Assessment Card */}
              <Card className="border-blue-200 bg-gradient-to-br from-blue-50/60 to-slate-50 shadow-2xs rounded-xl overflow-hidden border">
                <CardHeader className="pb-2.5 border-b border-blue-100/80 bg-white/70">
                  <CardTitle className="text-xs sm:text-sm font-bold text-[#1E3A8A] flex items-center gap-1.5">
                    <Sparkles className="h-4 w-4 text-[#0D9488]" />
                    AI Behavioral & Oral Assessment
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-4 space-y-3 text-xs">
                  <p className="text-slate-600 leading-relaxed">
                    Test your civil service competencies and course comprehension through dynamic simulations and real-time AI oral examination.
                  </p>
                  <div className="space-y-2 pt-1">
                    <a
                      href={`/behavioural/interview?courseId=${course.id}`}
                      className="w-full flex items-center justify-between p-2.5 rounded-lg bg-white border border-slate-200 hover:border-[#1E3A8A] hover:shadow-xs transition-all font-semibold text-slate-800 text-xs group"
                    >
                      <span className="flex items-center gap-2">
                        <Video className="h-3.5 w-3.5 text-[#0D9488]" />
                        Launch AI Live Interview
                      </span>
                      <ArrowRight className="h-3.5 w-3.5 text-slate-400 group-hover:text-[#1E3A8A] group-hover:translate-x-0.5 transition-all" />
                    </a>
                    <a
                      href={`/behavioural/cases?courseId=${course.id}`}
                      className="w-full flex items-center justify-between p-2.5 rounded-lg bg-white border border-slate-200 hover:border-[#1E3A8A] hover:shadow-xs transition-all font-semibold text-slate-800 text-xs group"
                    >
                      <span className="flex items-center gap-2">
                        <Scale className="h-3.5 w-3.5 text-[#1E3A8A]" />
                        Solve Case Inquiries (MCQs)
                      </span>
                      <ArrowRight className="h-3.5 w-3.5 text-slate-400 group-hover:text-[#1E3A8A] group-hover:translate-x-0.5 transition-all" />
                    </a>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
