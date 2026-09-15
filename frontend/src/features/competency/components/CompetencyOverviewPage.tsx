"use client";

import { useEffect, useState } from "react";
import { ArrowRight, FileQuestion, RefreshCw, Sparkles } from "lucide-react";
import { Bar, BarChart, CartesianGrid, LabelList, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Button } from "@/components/ui/button";
import { ButtonLink } from "@/components/ui/button-link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { ErrorNotice } from "@/components/shared/ErrorNotice";
import { fetchApi } from "@/lib/api";
import type { DomainGap } from "@/lib/types/competency";
import { DOMAINS, DOMAIN_ORDER, LEVEL_MAX, levelLabel } from "@/features/competency/domains";
import { CHART, ChartLegend, ChartTable, ChartTooltip, axisTick } from "@/features/analytics/chart-kit";

export default function CompetencyOverviewPage() {
  const [gaps, setGaps] = useState<DomainGap[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    fetchApi<DomainGap[]>("/competency/gaps")
      .then(setGaps)
      .catch((e: Error) => {
        if (e.message.toLowerCase().includes("no gap analysis")) setGaps([]);
        else setError(e.message);
      });
  }, []);

  async function runAnalysis() {
    setAnalyzing(true);
    setError(null);
    try {
      const res = await fetchApi<{ gaps: DomainGap[] }>("/competency/analyze", { method: "POST" });
      setGaps(res.gaps);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setAnalyzing(false);
    }
  }

  const byCode = new Map((gaps ?? []).map((g) => [g.domain_code, g]));
  const hasAnalysis = byCode.size > 0;
  const lastRun = gaps?.[0]?.generated_at;
  const chartData = DOMAIN_ORDER.map((code) => ({
    domain: DOMAINS[code].shortLabel,
    current: Number((byCode.get(code)?.current_level ?? 0).toFixed(1)),
    target: byCode.get(code)?.target_level ?? 0,
  }));

  return (
    <div className="mx-auto w-full max-w-7xl space-y-8 px-4 py-8 sm:px-6 lg:px-8">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div className="space-y-2">
          <p className="text-sm font-medium text-[#1E3A8A]">Skill intelligence</p>
          <h1 className="text-3xl font-bold text-balance text-slate-900">Competency profile</h1>
          <p className="max-w-2xl text-pretty text-slate-600">
            Your level in each competency domain of the Official Statistical System, compared with the level expected for your role and built from your assessments, labs, quizzes, and simulations.
          </p>
        </div>
        <div className="flex flex-col items-start gap-2 sm:items-end">
          <Button onClick={runAnalysis} disabled={analyzing}>
            <RefreshCw className="size-4" aria-hidden="true" />
            {analyzing ? "Analysing..." : hasAnalysis ? "Re-run analysis" : "Run gap analysis"}
          </Button>
          {lastRun && <p className="text-xs text-slate-500">Last analysed {new Date(lastRun).toLocaleString()}</p>}
        </div>
      </header>

      {error && <ErrorNotice message={error} />}

      {!gaps && !error && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4" aria-busy="true">
          {DOMAIN_ORDER.map((code) => (
            <Skeleton key={code} className="h-44 w-full" />
          ))}
        </div>
      )}

      {gaps && !hasAnalysis && (
        <Card>
          <CardContent className="flex flex-col items-start gap-3 pt-6">
            <h2 className="text-lg font-semibold text-balance text-slate-900">No gap analysis yet</h2>
            <p className="max-w-xl text-pretty text-slate-600">
              Run your first analysis to see where you stand in all four domains and get courses matched to your gaps.
            </p>
            <Button onClick={runAnalysis} disabled={analyzing}>
              {analyzing ? "Analysing..." : "Run gap analysis"}
            </Button>
          </CardContent>
        </Card>
      )}

      {hasAnalysis && (
        <>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {DOMAIN_ORDER.map((code) => {
              const meta = DOMAINS[code];
              const gap = byCode.get(code);
              const Icon = meta.icon;
              const current = gap?.current_level ?? 0;
              return (
                <Card key={code} className="flex flex-col">
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-2 text-[#1E3A8A]">
                      <Icon className="size-5" aria-hidden="true" />
                      <CardTitle className="text-base text-balance">{meta.label}</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent className="mt-auto space-y-3">
                    <p className="text-3xl font-semibold text-slate-900">
                      {current.toFixed(1)}
                      <span className="text-base font-normal text-slate-500"> / {LEVEL_MAX}</span>
                    </p>
                    <Progress value={(current / LEVEL_MAX) * 100} indicatorClassName="bg-[#1E3A8A]" aria-label={`${meta.label} level ${current.toFixed(1)} of ${LEVEL_MAX}`} />
                    <p className="text-sm text-slate-600">
                      {levelLabel(current)}
                      {gap ? (gap.gap > 0 ? ` · ${gap.gap.toFixed(1)} below target` : " · target met") : ""}
                    </p>
                    <ButtonLink href={`/competency/${code}`} variant="outline" size="sm" className="w-full" aria-label={`View ${meta.label} competency details`}>
                      View details
                      <ArrowRight className="size-4" aria-hidden="true" />
                    </ButtonLink>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          <div className="grid gap-4 lg:grid-cols-3">
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="text-balance">Current level vs role target</CardTitle>
                <CardDescription>Levels run from 0 (not yet assessed) to 5 (expert).</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <ChartLegend
                  items={[
                    { label: "Your current level", color: CHART.series[0] },
                    { label: "Target for your role", color: CHART.neutral },
                  ]}
                />
                <div className="h-72 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData} barGap={2} margin={{ top: 20, right: 8, bottom: 0, left: -16 }}>
                      <CartesianGrid vertical={false} stroke={CHART.grid} />
                      <XAxis dataKey="domain" tick={axisTick} tickLine={false} axisLine={{ stroke: CHART.axis }} />
                      <YAxis domain={[0, LEVEL_MAX]} ticks={[0, 1, 2, 3, 4, 5]} tick={axisTick} tickLine={false} axisLine={false} />
                      <Tooltip cursor={{ fill: "#f1f5f9" }} content={<ChartTooltip format={(v) => v.toFixed(1)} />} />
                      <Bar dataKey="current" name="Current level" fill={CHART.series[0]} maxBarSize={24} radius={[4, 4, 0, 0]}>
                        <LabelList dataKey="current" position="top" fill={CHART.secondaryInk} fontSize={12} />
                      </Bar>
                      <Bar dataKey="target" name="Role target" fill={CHART.neutral} maxBarSize={24} radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <ChartTable
                  caption="Current level and role target by competency domain"
                  columns={["Domain", "Current level", "Target", "Gap"]}
                  rows={DOMAIN_ORDER.map((code) => {
                    const g = byCode.get(code);
                    return [DOMAINS[code].label, (g?.current_level ?? 0).toFixed(1), (g?.target_level ?? 0).toFixed(1), (g?.gap ?? 0).toFixed(1)];
                  })}
                />
                <p className="text-xs text-pretty text-slate-500">
                  Targets use a default role-tier framework until your department configures its own.
                </p>
              </CardContent>
            </Card>

            <div className="space-y-4">
              <Card>
                <CardHeader>
                  <Sparkles className="size-5 text-[#1E3A8A]" aria-hidden="true" />
                  <CardTitle className="text-base text-balance">Close your gaps</CardTitle>
                  <CardDescription className="text-pretty">Courses from the iGOT Karmayogi catalogue ranked for your weakest domains.</CardDescription>
                </CardHeader>
                <CardContent>
                  <ButtonLink href="/recommendations" className="w-full">See recommendations</ButtonLink>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <FileQuestion className="size-5 text-[#1E3A8A]" aria-hidden="true" />
                  <CardTitle className="text-base text-balance">Test your understanding</CardTitle>
                  <CardDescription className="text-pretty">Turn any study material into a quiz with instant feedback.</CardDescription>
                </CardHeader>
                <CardContent>
                  <ButtonLink href="/quiz" variant="outline" className="w-full">Create a quiz</ButtonLink>
                </CardContent>
              </Card>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
