"use client";

import React, { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import {
  Brain,
  Award,
  Clock,
  ArrowRight,
  CheckCircle2,
  XCircle,
  AlertCircle,
  RotateCcw,
  Sparkles,
  ChevronRight,
  Activity,
  BarChart3,
  HelpCircle,
  BookOpen
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { fetchApi } from "@/lib/api";
import { useAuth } from "@/lib/auth/AuthContext";
import { useI18n } from "@/lib/i18n";
import confetti from "canvas-confetti";

interface QuestionOption {
  id: string;
  text: string;
}

interface QuestionInstance {
  question_id: string;
  skill_id: string;
  competency_id: string;
  type: string;
  difficulty: string;
  prompt: string;
  data: Record<string, any>;
  options: QuestionOption[];
  chart?: any;
  metadata?: Record<string, any>;
}

interface MasteryUpdate {
  skill_id: string;
  previous_mastery: number;
  new_mastery: number;
}

interface AnswerSubmissionResponse {
  is_correct: boolean;
  score: number;
  feedback: string;
  explanation: string;
  next_recommended_skill?: string;
  distractor_analysis?: string;
  mastery_update?: MasteryUpdate;
}

export default function StatisticalExamPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const courseId = searchParams.get("courseId") || "2";
  const { user } = useAuth();
  const { t } = useI18n();

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [question, setQuestion] = useState<QuestionInstance | null>(null);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [result, setResult] = useState<AnswerSubmissionResponse | null>(null);
  const [timeTaken, setTimeTaken] = useState(0);
  const [streak, setStreak] = useState(0);
  const [questionsAnswered, setQuestionsAnswered] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);
  const [preferredSkillId, setPreferredSkillId] = useState<string | null>(null);
  const [skillMasteryMap, setSkillMasteryMap] = useState<Record<string, number>>({
    "price.cpi.weighted_price_relatives": 0.45,
    "price.cpi.jevons_elementary_aggregate": 0.30,
    "price.cpi.seasonal_imputation": 0.20
  });

  const userId = user?.email || "officer-iss-8842";

  // Timer effect
  useEffect(() => {
    if (result) return;
    const interval = setInterval(() => {
      setTimeTaken((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, [result]);

  const fetchNextQuestion = async (targetSkillId?: string) => {
    setLoading(true);
    setResult(null);
    setSelectedOption(null);
    setTimeTaken(0);

    try {
      const data = await fetchApi<QuestionInstance>("/questions/next", {
        method: "POST",
        body: JSON.stringify({
          user_id: userId,
          competency_id: "price_statistics",
          preferred_skill_id: targetSkillId || preferredSkillId || undefined
        })
      });
      setQuestion(data);
    } catch (err: any) {
      console.error("Failed to load question from statistical engine:", err);
      // Fallback question if API is in offline mode
      setQuestion({
        question_id: "price.cpi.weighted.mcq.001-fallback",
        skill_id: "price.cpi.weighted_price_relatives",
        competency_id: "price_statistics",
        type: "mcq",
        difficulty: "intermediate",
        prompt: "A district consumer basket consists of three essential commodity groups with the following price relatives and expenditure weights:\n• Food: Relative = 120.0, Weight = 45\n• Housing: Relative = 110.0, Weight = 30\n• Fuel & Light: Relative = 135.0, Weight = 25\n\nCompute the overall Consumer Price Index (CPI) using the Modified Laspeyres formulation.",
        data: {
          rel_food: 120.0,
          rel_housing: 110.0,
          rel_fuel: 135.0,
          w_food: 45,
          w_housing: 30,
          w_fuel: 25
        },
        options: [
          { id: "A", text: "120.75" },
          { id: "B", text: "121.67" },
          { id: "C", text: "115.00" },
          { id: "D", text: "128.50" }
        ],
        metadata: {
          template_id: "price.cpi.weighted.mcq.001",
          unit: "index_points"
        }
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNextQuestion();
  }, []);

  const handleSubmit = async () => {
    if (!selectedOption || !question || submitting) return;
    setSubmitting(true);

    try {
      const res = await fetchApi<AnswerSubmissionResponse>("/questions/submit", {
        method: "POST",
        body: JSON.stringify({
          user_id: userId,
          question_id: question.question_id,
          submitted_answer: selectedOption,
          time_taken_seconds: timeTaken
        })
      });
      setResult(res);
      setQuestionsAnswered((c) => c + 1);

      if (res.is_correct) {
        setStreak((s) => s + 1);
        setCorrectCount((c) => c + 1);
        confetti({
          particleCount: 50,
          spread: 60,
          origin: { y: 0.7 }
        });
      } else {
        setStreak(0);
      }

      if (res.mastery_update) {
        setSkillMasteryMap((prev) => ({
          ...prev,
          [res.mastery_update!.skill_id]: res.mastery_update!.new_mastery
        }));
      }

      if (res.next_recommended_skill) {
        setPreferredSkillId(res.next_recommended_skill);
      }
    } catch (err) {
      console.error("Failed to submit answer:", err);
      const isCorrect = selectedOption === "A";
      setResult({
        is_correct: isCorrect,
        score: isCorrect ? 1.0 : 0.0,
        feedback: isCorrect
          ? "Excellent calculation! You correctly applied the modified Laspeyres expenditure weights."
          : "Incorrect option. Review the weighted arithmetic mean formula: (120*45 + 110*30 + 135*25) / 100 = 120.75.",
        explanation: "Modified Laspeyres aggregates price relatives weighted by expenditure shares: CPI = sum(W_i * R_i) / sum(W_i). Here (5400 + 3300 + 3375) / 100 = 12075 / 100 = 120.75 index points.",
        distractor_analysis: selectedOption === "B" ? "Common Error: Unweighted simple arithmetic mean (120+110+135)/3 = 121.67." : undefined,
        mastery_update: {
          skill_id: question.skill_id,
          previous_mastery: 0.45,
          new_mastery: isCorrect ? 0.60 : 0.40
        }
      });
      setQuestionsAnswered((c) => c + 1);
      if (isCorrect) {
        setStreak((s) => s + 1);
        setCorrectCount((c) => c + 1);
      } else {
        setStreak(0);
      }
    } finally {
      setSubmitting(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
  };

  const getDifficultyColor = (diff: string) => {
    switch (diff?.toLowerCase()) {
      case "beginner":
        return "bg-emerald-50 text-emerald-700 border-emerald-200";
      case "intermediate":
        return "bg-blue-50 text-blue-700 border-blue-200";
      case "advanced":
        return "bg-purple-50 text-purple-700 border-purple-200";
      default:
        return "bg-slate-50 text-slate-700 border-slate-200";
    }
  };

  return (
    <div className="min-h-[calc(100vh-68px)] bg-[#F8FAFC] py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-6">
        {/* Navigation Breadcrumb & Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200 shadow-2xs">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <a href={`/courses/${courseId}`} className="hover:text-[#1E3A8A] flex items-center gap-1 font-medium">
                <BookOpen className="h-3.5 w-3.5" />
                Course Details
              </a>
              <span>/</span>
              <span className="text-slate-800 font-semibold">Statistical Competency Engine</span>
            </div>
            <h1 className="text-xl sm:text-2xl font-black text-slate-900 flex items-center gap-2">
              <Brain className="h-6 w-6 text-[#4338CA]" />
              Adaptive Examination Environment
            </h1>
            <p className="text-xs text-slate-500">
              Real-time parameter generation, server-side mathematical validation, and pedagogical branching.
            </p>
          </div>

          {/* Quick Metrics Strip */}
          <div className="flex items-center gap-3 self-start sm:self-center">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-50 border border-slate-200 text-xs">
              <Clock className="h-4 w-4 text-slate-500" />
              <span className="font-mono font-bold text-slate-800">{formatTime(timeTaken)}</span>
            </div>
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-indigo-50 border border-indigo-200 text-xs text-[#4338CA]">
              <Sparkles className="h-4 w-4" />
              <span className="font-bold">Streak: {streak}</span>
            </div>
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800">
              <Award className="h-4 w-4" />
              <span className="font-bold">Score: {correctCount}/{questionsAnswered}</span>
            </div>
          </div>
        </div>

        {/* Live Mastery Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Object.entries(skillMasteryMap).map(([skillId, score]) => {
            const label = skillId.includes("weighted")
              ? "Weighted Relatives"
              : skillId.includes("jevons")
              ? "Jevons Geometric Mean"
              : "Seasonal Imputation";
            const pct = Math.round(score * 100);
            return (
              <div
                key={skillId}
                className={`p-3.5 rounded-xl border bg-white shadow-2xs transition-all ${
                  question?.skill_id === skillId ? "border-indigo-400 ring-2 ring-indigo-100" : "border-slate-200"
                }`}
              >
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="font-bold text-slate-800">{label}</span>
                  <span className="font-mono font-bold text-indigo-600">{pct}%</span>
                </div>
                <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-indigo-600 h-full rounded-full transition-all duration-500"
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>

        {/* Main Question Workspace */}
        {loading ? (
          <Card className="border-slate-200 bg-white p-12 text-center rounded-2xl">
            <div className="h-10 w-10 border-4 border-slate-200 border-t-indigo-600 rounded-full animate-spin mx-auto mb-4" />
            <p className="text-sm font-semibold text-slate-700">Synthesizing Next Adaptive Question...</p>
            <p className="text-xs text-slate-400 mt-1">Calibrating parameters to your current skill mastery level</p>
          </Card>
        ) : question ? (
          <Card className="border-slate-200 bg-white shadow-sm rounded-2xl overflow-hidden">
            <CardHeader className="border-b border-slate-100 pb-4 bg-gradient-to-r from-slate-50 to-white">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="flex items-center gap-2">
                  <Badge variant="outline" className={`text-[11px] font-bold uppercase tracking-wider px-2.5 py-0.5 ${getDifficultyColor(question.difficulty)}`}>
                    {question.difficulty}
                  </Badge>
                  <span className="text-xs font-semibold px-2 py-0.5 rounded-md bg-slate-100 text-slate-700">
                    {question.skill_id}
                  </span>
                </div>
                <span className="text-[11px] font-mono text-slate-400">
                  ID: {question.question_id}
                </span>
              </div>
            </CardHeader>

            <CardContent className="p-6 space-y-6">
              {/* Question Prompt */}
              <div className="text-base text-slate-900 font-medium whitespace-pre-line leading-relaxed">
                {question.prompt}
              </div>

              {/* Parameter Data Table (if data exists) */}
              {question.data && Object.keys(question.data).length > 0 && (
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                  <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                    <BarChart3 className="h-3.5 w-3.5 text-indigo-600" />
                    Problem Parameters & Empirical Microdata
                  </h4>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
                    {Object.entries(question.data).map(([key, val]) => (
                      <div key={key} className="p-2 bg-white rounded-lg border border-slate-100 flex justify-between items-center">
                        <span className="font-mono text-slate-500 text-[11px]">{key}</span>
                        <span className="font-bold text-slate-900">{String(val)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Multiple Choice Options */}
              <div className="space-y-3 pt-2">
                <label className="text-xs font-bold text-slate-700 block">Select the correct mathematical result:</label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {question.options.map((opt) => {
                    const isSelected = selectedOption === opt.id;
                    return (
                      <button
                        key={opt.id}
                        disabled={!!result || submitting}
                        onClick={() => setSelectedOption(opt.id)}
                        className={`flex items-center gap-3.5 p-4 rounded-xl border text-left transition-all cursor-pointer ${
                          isSelected
                            ? "border-indigo-600 bg-indigo-50/70 shadow-sm ring-2 ring-indigo-200"
                            : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/60"
                        } ${result ? "cursor-default" : ""}`}
                      >
                        <span
                          className={`h-7 w-7 rounded-lg font-bold text-xs flex items-center justify-center shrink-0 ${
                            isSelected
                              ? "bg-indigo-600 text-white"
                              : "bg-slate-100 text-slate-600 group-hover:bg-slate-200"
                          }`}
                        >
                          {opt.id}
                        </span>
                        <span className="font-mono font-semibold text-slate-900 text-sm">
                          {opt.text}
                        </span>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Result & Pedagogical Feedback Panel */}
              {result && (
                <div
                  className={`p-5 rounded-xl border space-y-3 transition-all ${
                    result.is_correct
                      ? "bg-emerald-50/70 border-emerald-200"
                      : "bg-rose-50/70 border-rose-200"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    {result.is_correct ? (
                      <>
                        <CheckCircle2 className="h-5 w-5 text-emerald-600 shrink-0" />
                        <span className="font-bold text-emerald-900 text-sm">
                          Evaluation Passed (+{result.score} Point)
                        </span>
                      </>
                    ) : (
                      <>
                        <XCircle className="h-5 w-5 text-rose-600 shrink-0" />
                        <span className="font-bold text-rose-900 text-sm">
                          Evaluation Incorrect
                        </span>
                      </>
                    )}
                  </div>

                  <p className="text-xs text-slate-700 leading-relaxed font-medium">
                    {result.feedback}
                  </p>

                  <div className="p-3 bg-white/80 rounded-lg border border-slate-200/60 text-xs space-y-1">
                    <span className="font-bold text-slate-900 block">Step-by-step Statutory Rationale:</span>
                    <p className="text-slate-600 leading-relaxed">{result.explanation}</p>
                  </div>

                  {result.distractor_analysis && (
                    <div className="p-3 bg-amber-50/80 rounded-lg border border-amber-200 text-xs space-y-1 text-amber-900">
                      <span className="font-bold block">Distractor Misconception Analysis:</span>
                      <p className="text-amber-800 leading-relaxed">{result.distractor_analysis}</p>
                    </div>
                  )}

                  {result.mastery_update && (
                    <div className="text-[11px] font-semibold text-indigo-900 flex items-center gap-2 pt-1">
                      <Activity className="h-3.5 w-3.5 text-indigo-600" />
                      <span>
                        Mastery updated: {Math.round(result.mastery_update.previous_mastery * 100)}% →{" "}
                        {Math.round(result.mastery_update.new_mastery * 100)}%
                      </span>
                    </div>
                  )}
                </div>
              )}
            </CardContent>

            <CardFooter className="p-6 border-t border-slate-100 bg-slate-50/50 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <Button
                variant="outline"
                size="sm"
                onClick={() => router.push(`/courses/${courseId}`)}
                className="text-xs rounded-xl border-slate-300 text-slate-700 hover:bg-slate-100 cursor-pointer"
              >
                Return to Course
              </Button>

              <div className="flex items-center gap-3 w-full sm:w-auto">
                {!result ? (
                  <Button
                    onClick={handleSubmit}
                    disabled={!selectedOption || submitting}
                    className="w-full sm:w-auto text-xs font-bold rounded-xl px-6 h-10 bg-indigo-600 text-white hover:bg-indigo-700 cursor-pointer transition-all shadow-sm"
                  >
                    {submitting ? "Evaluating Result..." : "Submit Answer"}
                  </Button>
                ) : (
                  <Button
                    onClick={() => fetchNextQuestion(result.next_recommended_skill)}
                    className="w-full sm:w-auto text-xs font-bold rounded-xl px-6 h-10 bg-[#1E3A8A] text-white hover:bg-blue-900 cursor-pointer transition-all shadow-sm flex items-center gap-1.5"
                  >
                    <span>Next Adaptive Question</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Button>
                )}
              </div>
            </CardFooter>
          </Card>
        ) : null}
      </div>
    </div>
  );
}
