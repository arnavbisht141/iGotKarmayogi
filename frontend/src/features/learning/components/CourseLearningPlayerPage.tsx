"use client";

import React, { useEffect, useState, Suspense } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import {
  CheckCircle2,
  Circle,
  PlayCircle,
  ChevronLeft,
  ChevronRight,
  Video,
  FileText,
  FlaskConical,
  Award,
  AlertCircle,
  Sparkles,
  HelpCircle,
  BookOpen,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { fetchApi } from "@/lib/api";
import { CurrentLesson, ModuleSummary } from "@/lib/types";
import { useI18n } from "@/lib/i18n";
import confetti from "canvas-confetti";

function LearningPlayerContent() {
  const { courseId } = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();
  const { t } = useI18n();

  const lessonQueryId = searchParams?.get("lessonId");

  const [courseMeta, setCourseMeta] = useState<any>(null);
  const [modulesTree, setModulesTree] = useState<ModuleSummary[]>([]);
  const [currentLesson, setCurrentLesson] = useState<CurrentLesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [mobileSyllabusOpen, setMobileSyllabusOpen] = useState(false);

  // In-lesson Activity Practice state
  const [selectedActivityOption, setSelectedActivityOption] = useState<number | null>(null);
  const [activityFeedback, setActivityFeedback] = useState<{
    is_correct: boolean;
    explanation: string;
  } | null>(null);
  const [activityChecking, setActivityChecking] = useState(false);

  const loadPlayerData = (targetLessonId?: number | string | null) => {
    setLoading(true);
    const url = targetLessonId
      ? `/learning/course/${courseId}/player?lesson_id=${targetLessonId}`
      : `/learning/course/${courseId}/player`;

    fetchApi(url)
      .then((data) => {
        setCourseMeta(data.course);
        setModulesTree(data.modules_tree);
        setCurrentLesson(data.current_lesson);
        // Reset activity state for new lesson
        setSelectedActivityOption(null);
        setActivityFeedback(null);
      })
      .catch((err) => console.error("Error loading learning player:", err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    if (courseId) {
      loadPlayerData(lessonQueryId);
    }
  }, [courseId, lessonQueryId]);

  const handleSelectLesson = (lessonId: number) => {
    setMobileSyllabusOpen(false);
    loadPlayerData(lessonId);
  };

  const handleValidateActivity = async () => {
    if (!currentLesson || selectedActivityOption === null) return;
    setActivityChecking(true);
    try {
      const res = await fetchApi(`/learning/lesson/${currentLesson.id}/activity`, {
        method: "POST",
        body: JSON.stringify({ selected_option: selectedActivityOption }),
      });

      setActivityFeedback(res);
      if (res.is_correct) {
        confetti({
          particleCount: 50,
          spread: 60,
          origin: { y: 0.8 },
        });
      }
    } catch (err: any) {
      alert("Failed to validate practice answer");
    } finally {
      setActivityChecking(false);
    }
  };

  const handleCompleteAndNext = async () => {
    if (!currentLesson) return;
    try {
      const res = await fetchApi(`/learning/lesson/${currentLesson.id}/complete`, {
        method: "POST",
      });

      // If course is finished or this is the last lesson, transition to Assess
      if (currentLesson.is_last_lesson || res.is_course_finished) {
        if (courseMeta?.assessment_id) {
          router.push(`/assess/${courseMeta.assessment_id}`);
        } else {
          router.push(`/progress`);
        }
      } else if (currentLesson.next_lesson_id) {
        loadPlayerData(currentLesson.next_lesson_id);
      }
    } catch (err: any) {
      alert("Failed to update lesson progress");
    }
  };

  if (loading && !currentLesson) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center">
        <div className="h-8 w-8 rounded-full border-4 border-slate-200 border-t-amber-600 animate-spin" />
      </div>
    );
  }

  if (!currentLesson) {
    return (
      <div className="p-12 text-center">
        <p className="text-sm text-slate-500">Lesson content unavailable.</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col lg:flex-row min-h-[calc(100vh-65px)] bg-slate-50">
      {/* Mobile Syllabus Toggle Bar */}
      <div className="lg:hidden bg-white border-b border-slate-200 px-4 py-3 flex items-center justify-between shadow-2xs">
        <div className="flex items-center gap-2 min-w-0">
          <BookOpen className="h-4 w-4 text-[#1E3A8A] shrink-0" />
          <span className="text-xs font-bold text-slate-900 truncate">
            {currentLesson.module_title}: {currentLesson.title}
          </span>
        </div>
        <button
          onClick={() => setMobileSyllabusOpen(!mobileSyllabusOpen)}
          className="text-xs font-bold text-[#1E3A8A] hover:text-[#172554] flex items-center gap-1 shrink-0 ml-2 px-2.5 py-1 rounded-lg bg-blue-50/80 border border-blue-200/80 cursor-pointer transition-colors"
        >
          {mobileSyllabusOpen ? "Hide Syllabus" : "View Syllabus"}
          <ChevronRight className={`h-3.5 w-3.5 transition-transform duration-200 ${mobileSyllabusOpen ? "rotate-90" : ""}`} />
        </button>
      </div>

      {/* Collapsible Left Course Syllabus Sidebar */}
      <aside className={`${mobileSyllabusOpen ? "flex" : "hidden"} lg:flex w-full lg:w-80 border-r border-slate-200 bg-white flex-col shrink-0 transition-all duration-300`}>
        <div className="p-4 border-b border-slate-200 bg-slate-50/50">
          <a
            href={`/courses/${courseId}`}
            className="text-[11px] font-semibold text-slate-500 hover:text-slate-900 flex items-center gap-1 mb-2"
          >
            <ChevronLeft className="h-3.5 w-3.5" /> Back to Course Overview
          </a>
          <h2 className="text-sm font-bold text-slate-900 line-clamp-2">
            {courseMeta?.title}
          </h2>
          <div className="mt-3 space-y-1">
            <div className="flex justify-between text-[11px] font-semibold text-slate-600">
              <span>Overall Progress</span>
              <span>{courseMeta?.progress_percent}%</span>
            </div>
            <Progress value={courseMeta?.progress_percent} indicatorClassName="bg-amber-600" />
          </div>
        </div>

        {/* Modules & Lessons Tree */}
        <div className="flex-1 overflow-y-auto p-3 space-y-4">
          {modulesTree.map((mod, modIdx) => (
            <div key={mod.id} className="space-y-1.5">
              <div className="flex items-center justify-between px-2 text-xs font-bold text-slate-700">
                <span className="truncate">
                  {modIdx + 1}. {mod.title}
                </span>
                <span className="text-[10px] text-slate-400 font-normal">
                  {mod.completed_lessons}/{mod.total_lessons}
                </span>
              </div>

              <div className="space-y-1">
                {mod.lessons.map((l) => {
                  const isCurrent = l.id === currentLesson.id;
                  return (
                    <button
                      key={l.id}
                      onClick={() => handleSelectLesson(l.id)}
                      className={`w-full flex items-center justify-between p-2 rounded-lg text-left text-xs transition-colors cursor-pointer ${
                        isCurrent
                          ? "bg-[#1E3A8A] text-white font-semibold shadow-xs"
                          : l.completed
                          ? "text-slate-700 hover:bg-slate-100 bg-slate-50/80"
                          : "text-slate-600 hover:bg-slate-100"
                      }`}
                    >
                      <div className="flex items-center gap-2 truncate">
                        {l.completed ? (
                          <CheckCircle2
                            className={`h-4 w-4 shrink-0 ${
                              isCurrent ? "text-amber-400" : "text-emerald-600"
                            }`}
                          />
                        ) : (
                          <Circle
                            className={`h-4 w-4 shrink-0 ${
                              isCurrent ? "text-slate-400" : "text-slate-300"
                            }`}
                          />
                        )}
                        <span className="truncate">{l.title}</span>
                      </div>
                      <span
                        className={`text-[10px] ml-2 ${
                          isCurrent ? "text-slate-300" : "text-slate-400"
                        }`}
                      >
                        {l.duration_minutes}m
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>
          ))}

          {/* Final Assessment Shortcut Link */}
          {courseMeta?.assessment_id && (
            <div className="pt-4 border-t border-slate-100">
              <a
                href={`/assess/${courseMeta.assessment_id}`}
                className="w-full flex items-center justify-between p-3 rounded-xl bg-amber-50/80 border border-amber-200 text-amber-900 hover:bg-amber-100 text-xs font-bold transition-colors"
              >
                <span className="flex items-center gap-2">
                  <Award className="h-4 w-4 text-amber-700" />
                  Official Assessment
                </span>
                <ChevronRight className="h-4 w-4 text-amber-700" />
              </a>
            </div>
          )}
        </div>
      </aside>

      {/* Main Content Stage */}
      <main className="flex-1 flex flex-col overflow-y-auto">
        {/* Lesson Header */}
        <div className="px-4 sm:px-6 py-3.5 sm:py-4 bg-white border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <span className="text-xs font-semibold text-amber-700 uppercase tracking-wider">
              {currentLesson.module_title}
            </span>
            <h1 className="text-lg sm:text-xl font-bold text-slate-900 mt-0.5">
              {currentLesson.title}
            </h1>
          </div>

          <div className="flex items-center gap-2">
            <Badge variant="secondary" className="text-xs capitalize">
              {currentLesson.content_type} • {currentLesson.duration_minutes} Minutes
            </Badge>
            {currentLesson.completed && (
              <Badge variant="success" className="text-xs inline-flex items-center gap-1">
                <CheckCircle2 className="h-3 w-3" /> Completed
              </Badge>
            )}
          </div>
        </div>

        {/* Lesson Body Content */}
        <div className="flex-1 max-w-4xl w-full mx-auto p-4 sm:p-8 space-y-6 sm:space-y-8">
          {/* Simulated Video Player if Content Type is Video */}
          {currentLesson.content_type === "video" && (
            <div className="rounded-2xl overflow-hidden bg-slate-950 shadow-md aspect-video relative flex items-center justify-center text-white">
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/30" />
              <div className="relative text-center p-6 space-y-3 z-10">
                <div className="h-16 w-16 rounded-full bg-amber-600/90 text-white flex items-center justify-center mx-auto shadow-lg hover:scale-105 transition-transform cursor-pointer">
                  <PlayCircle className="h-10 w-10" />
                </div>
                <h4 className="text-base font-bold">{currentLesson.title}</h4>
                <p className="text-xs text-slate-300">
                  Interactive Video Lecture • National Statistical Systems Training Academy (NSSTA)
                </p>
              </div>
            </div>
          )}

          {/* Reading / Lab Content Area */}
          <div className="prose prose-slate max-w-none bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-xs leading-relaxed text-slate-800 text-sm whitespace-pre-wrap">
            {currentLesson.content}
          </div>

          {/* IN-LESSON PRACTICE ACTIVITY */}
          {currentLesson.activity && currentLesson.activity.has_activity && (
            <Card className="border-amber-200 bg-amber-50/40 shadow-xs">
              <CardHeader className="pb-3 border-b border-amber-100">
                <div className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-amber-700" />
                  <CardTitle className="text-sm font-bold text-slate-900">
                    {t("learn.practice")}
                  </CardTitle>
                </div>
                <p className="text-xs text-slate-600">
                  Check your conceptual understanding before continuing to the next unit.
                </p>
              </CardHeader>
              <CardContent className="p-5 space-y-4">
                <p className="text-sm font-semibold text-slate-900">
                  {currentLesson.activity.question}
                </p>

                <div className="space-y-2">
                  {currentLesson.activity.options.map((opt, idx) => {
                    const isSelected = selectedActivityOption === idx;
                    return (
                      <button
                        key={idx}
                        type="button"
                        onClick={() => {
                          setSelectedActivityOption(idx);
                          setActivityFeedback(null);
                        }}
                        className={`w-full p-3 rounded-xl border text-left text-xs font-medium transition-all cursor-pointer flex items-center gap-3 ${
                          isSelected
                            ? "bg-[#1E3A8A] text-white border-[#1E3A8A] shadow-xs"
                            : "bg-white text-slate-800 border-slate-200 hover:bg-slate-50"
                        }`}
                      >
                        <span
                          className={`h-5 w-5 rounded-full text-[10px] font-bold flex items-center justify-center ${
                            isSelected
                              ? "bg-amber-500 text-slate-950"
                              : "bg-slate-100 text-slate-600"
                          }`}
                        >
                          {String.fromCharCode(65 + idx)}
                        </span>
                        <span>{opt}</span>
                      </button>
                    );
                  })}
                </div>

                {/* Validation Feedback */}
                {activityFeedback && (
                  <div
                    className={`p-3 rounded-xl text-xs flex items-start gap-2.5 ${
                      activityFeedback.is_correct
                        ? "bg-emerald-100/70 border border-emerald-300 text-emerald-950"
                        : "bg-rose-100/70 border border-rose-300 text-rose-950"
                    }`}
                  >
                    {activityFeedback.is_correct ? (
                      <CheckCircle2 className="h-4 w-4 text-emerald-700 shrink-0 mt-0.5" />
                    ) : (
                      <AlertCircle className="h-4 w-4 text-rose-700 shrink-0 mt-0.5" />
                    )}
                    <div>
                      <p className="font-bold">
                        {activityFeedback.is_correct ? "Correct Concept Application!" : "Review Required"}
                      </p>
                      <p className="mt-0.5 text-[11px] leading-relaxed">
                        {activityFeedback.explanation}
                      </p>
                    </div>
                  </div>
                )}

                <div className="flex justify-end pt-2">
                  <Button
                    size="sm"
                    onClick={handleValidateActivity}
                    disabled={selectedActivityOption === null || activityChecking}
                    className="bg-amber-600 hover:bg-amber-700 text-white text-xs font-semibold"
                  >
                    {activityChecking ? "Checking..." : t("learn.checkAnswer")}
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Navigation Controls Bar */}
          <div className="pt-6 border-t border-slate-200 flex items-center justify-between">
            <Button
              variant="outline"
              size="sm"
              disabled={!currentLesson.prev_lesson_id}
              onClick={() => {
                if (currentLesson.prev_lesson_id) {
                  loadPlayerData(currentLesson.prev_lesson_id);
                }
              }}
              className="text-xs"
            >
              <ChevronLeft className="h-4 w-4 mr-1" /> {t("learn.previous")}
            </Button>

            <Button
              size="sm"
              onClick={handleCompleteAndNext}
              className="bg-[#1E3A8A] hover:bg-[#172554] text-white text-xs font-semibold px-5 cursor-pointer"
            >
              {currentLesson.is_last_lesson
                ? t("learn.takeAssessment")
                : t("learn.markCompleted")}
              <ChevronRight className="h-4 w-4 ml-1" />
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default function CourseLearningPlayerPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-[80vh] flex items-center justify-center">
          <div className="h-8 w-8 rounded-full border-4 border-slate-200 border-t-amber-600 animate-spin" />
        </div>
      }
    >
      <LearningPlayerContent />
    </Suspense>
  );
}
