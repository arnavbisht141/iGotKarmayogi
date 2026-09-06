"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import {
  Compass,
  PlayCircle,
  Clock,
  Award,
  Video,
  FileText,
  FlaskConical,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  ShieldCheck,
  UserCheck,
  ArrowRight,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
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
        // Expand first module by default
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

  if (loading) {
    return (
      <div className="min-h-[70vh] flex items-center justify-center">
        <div className="h-8 w-8 rounded-full border-4 border-slate-200 border-t-amber-600 animate-spin" />
      </div>
    );
  }

  if (!course) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20 text-center">
        <h2 className="text-xl font-bold text-slate-900">Course Not Found</h2>
        <p className="text-xs text-slate-500 mt-1">The requested course could not be retrieved.</p>
        <a href="/discover">
          <Button variant="outline" size="sm" className="mt-4">
            Back to Catalogue
          </Button>
        </a>
      </div>
    );
  }

  const isEnrolled = !!course.enrollment;
  const progressPct = course.enrollment?.progress_percent || 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Course Hero Banner */}
      <div className="rounded-2xl bg-white border border-slate-200 p-6 sm:p-10 shadow-xs">
        <div className="flex flex-wrap items-center gap-2 mb-3">
          <Badge variant={course.source === "external" ? "external" : "secondary"}>
            {course.source === "external" ? "ISTM Accredited External" : "MoSPI Internal Curriculum"}
          </Badge>
          <span className="text-xs font-semibold text-slate-500">• {course.category}</span>
          <span className="text-xs font-semibold text-slate-500">• {course.difficulty}</span>
        </div>

        <h1 className="text-2xl sm:text-4xl font-extrabold text-slate-900 tracking-tight leading-tight max-w-4xl">
          {course.title}
        </h1>

        <p className="mt-4 text-sm sm:text-base text-slate-600 max-w-4xl leading-relaxed">
          {course.overview}
        </p>

        {/* Instructor & Accreditation Info */}
        <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-4 py-4 border-y border-slate-100 text-xs">
          <div>
            <span className="text-slate-400 block font-medium">Faculty / Instructor</span>
            <span className="font-bold text-slate-900">{course.instructor}</span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Accredited Body</span>
            <span className="font-bold text-slate-900">{course.organization}</span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Estimated Time</span>
            <span className="font-bold text-slate-900">{course.duration_hours} Learning Hours</span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Official Rating</span>
            <span className="font-bold text-slate-900">★ {course.rating} ({course.enrolled_count} enrolled)</span>
          </div>
        </div>

        {/* Start / Resume Action CTA */}
        <div className="mt-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <Button
              size="lg"
              onClick={handleEnrollOrResume}
              disabled={enrolling}
              className={`font-semibold shadow-xs ${
                isEnrolled ? "bg-amber-600 hover:bg-amber-700 text-white" : "bg-slate-900 hover:bg-slate-800 text-white"
              }`}
            >
              <PlayCircle className="h-5 w-5 mr-1.5" />
              {isEnrolled ? "Resume Coursework" : "Enroll in Course"}
            </Button>
            {isEnrolled && (
              <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-3 py-1.5 rounded-lg border border-emerald-200">
                {progressPct}% Completed
              </span>
            )}
          </div>

          {course.assessment_id && (
            <a href={`/assess/${course.assessment_id}`}>
              <Button variant="outline" size="sm" className="text-xs">
                Take Certification Assessment <ArrowRight className="h-3.5 w-3.5 ml-1" />
              </Button>
            </a>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Column: Expandable Syllabus (Miro: Course -> Module -> Lesson) */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="border-slate-200 bg-white shadow-xs">
            <CardHeader className="border-b border-slate-100 pb-4">
              <CardTitle className="text-lg font-bold text-slate-900">
                {t("course.syllabus")}
              </CardTitle>
              <p className="text-xs text-slate-500">
                {course.modules.length} Modules • {course.counts.readings + course.counts.videos + course.counts.labs} Total Learning Units
              </p>
            </CardHeader>
            <CardContent className="p-4 space-y-3">
              {course.modules.map((mod, idx) => {
                const isExpanded = expandedModules[mod.id];
                return (
                  <div
                    key={mod.id}
                    className="border border-slate-200 rounded-xl overflow-hidden transition-all"
                  >
                    <button
                      onClick={() => toggleModule(mod.id)}
                      className="w-full px-4 py-3.5 bg-slate-50/70 hover:bg-slate-100 flex items-center justify-between text-left transition-colors cursor-pointer"
                    >
                      <div className="flex items-center gap-3">
                        <span className="h-6 w-6 rounded-full bg-slate-200 text-slate-700 font-bold text-xs flex items-center justify-center">
                          {idx + 1}
                        </span>
                        <div>
                          <h4 className="text-sm font-bold text-slate-900">{mod.title}</h4>
                          <p className="text-[11px] text-slate-500">{mod.lessons.length} lessons • {mod.description}</p>
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
                            className="py-3 flex items-center justify-between text-xs hover:bg-slate-50/50 rounded px-2"
                          >
                            <div className="flex items-center gap-2.5">
                              {lesson.content_type === "video" && <Video className="h-4 w-4 text-amber-600" />}
                              {lesson.content_type === "lab" && <FlaskConical className="h-4 w-4 text-indigo-600" />}
                              {lesson.content_type === "reading" && <FileText className="h-4 w-4 text-slate-500" />}
                              <span className="font-semibold text-slate-800">{lesson.title}</span>
                            </div>
                            <div className="flex items-center gap-3 text-slate-500">
                              {lesson.has_activity && (
                                <Badge variant="secondary" className="text-[10px]">Includes Practice</Badge>
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

        {/* Sidebar Column: Content Breakdown & Skills Gained */}
        <div className="space-y-6">
          {/* Content Breakdown Box */}
          <Card className="border-slate-200 bg-white shadow-xs">
            <CardHeader className="pb-3 border-b border-slate-100">
              <CardTitle className="text-sm font-bold text-slate-900">
                Course Materials Breakdown
              </CardTitle>
            </CardHeader>
            <CardContent className="p-4 space-y-3 text-xs">
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-slate-600">
                  <Video className="h-4 w-4 text-amber-600" /> Video Lectures
                </span>
                <span className="font-bold text-slate-900">{course.counts.videos}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-slate-600">
                  <FileText className="h-4 w-4 text-slate-500" /> Reading Modules
                </span>
                <span className="font-bold text-slate-900">{course.counts.readings}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-slate-600">
                  <FlaskConical className="h-4 w-4 text-indigo-600" /> Practical CAPI/Python Labs
                </span>
                <span className="font-bold text-slate-900">{course.counts.labs}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-slate-600">
                  <ShieldCheck className="h-4 w-4 text-emerald-600" /> MCQ Certification Test
                </span>
                <span className="font-bold text-slate-900">{course.counts.assessments}</span>
              </div>
            </CardContent>
          </Card>

          {/* Competencies Gained */}
          <Card className="border-slate-200 bg-white shadow-xs">
            <CardHeader className="pb-3 border-b border-slate-100">
              <CardTitle className="text-sm font-bold text-slate-900">
                {t("course.skillsGained")}
              </CardTitle>
            </CardHeader>
            <CardContent className="p-4">
              <div className="flex flex-wrap gap-1.5">
                {course.skills_gained.map((skill, idx) => (
                  <Badge key={idx} variant="saffron" className="text-xs py-1">
                    <CheckCircle2 className="h-3 w-3 mr-1 text-amber-700" />
                    {skill}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
