"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { ArrowLeft, ArrowRight, Clock, FileQuestion, Sparkles } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { ButtonLink } from "@/components/ui/button-link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { ErrorNotice } from "@/components/shared/ErrorNotice";
import { fetchApi } from "@/lib/api";
import type { DomainDetail } from "@/lib/types/competency";
import { DOMAINS, LEVEL_MAX, isDomainCode, levelLabel } from "@/features/competency/domains";

const EVIDENCE_LABELS: Record<string, string> = {
  self_declared: "Self-declared",
  assessment: "From assessments",
  inferred: "Inferred",
};

export default function CompetencyDomainPage() {
  const params = useParams<{ domain: string }>();
  const code = params.domain;
  const [detail, setDetail] = useState<DomainDetail | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isDomainCode(code)) return;
    fetchApi<DomainDetail>(`/competency/domains/${code}`)
      .then(setDetail)
      .catch((e: Error) => setError(e.message));
  }, [code]);

  if (!isDomainCode(code)) {
    return (
      <div className="mx-auto w-full max-w-3xl px-4 py-16 text-center sm:px-6">
        <h1 className="text-2xl font-bold text-balance text-slate-900">Competency domain not found</h1>
        <p className="mt-2 text-pretty text-slate-600">The four domains are Statistical, Technical, Digital Governance, and Behavioural.</p>
        <ButtonLink href="/competency" className="mt-6">
          Back to competency profile
        </ButtonLink>
      </div>
    );
  }

  const meta = DOMAINS[code];
  const Icon = meta.icon;
  const analysed = detail?.current_level !== null && detail?.current_level !== undefined;

  return (
    <div className="mx-auto w-full max-w-7xl space-y-8 px-4 py-8 sm:px-6 lg:px-8">
      <ButtonLink href="/competency" variant="ghost" size="sm" className="-ml-3">
        <ArrowLeft className="size-4" aria-hidden="true" />
        Competency profile
      </ButtonLink>

      <header className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
        <div className="flex gap-4">
          <span className="flex size-12 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-[#1E3A8A]">
            <Icon className="size-6" aria-hidden="true" />
          </span>
          <div className="space-y-2">
            <h1 className="text-3xl font-bold text-balance text-slate-900">{meta.label} competencies</h1>
            <p className="max-w-2xl text-pretty text-slate-600">{meta.description}</p>
          </div>
        </div>

        <Card className="w-full shrink-0 lg:w-80">
          <CardContent className="space-y-3 pt-6">
            {!detail && !error && <Skeleton className="h-20 w-full" />}
            {detail && analysed && (
              <>
                <div className="flex items-baseline justify-between">
                  <span className="text-sm text-slate-600">Current level</span>
                  <span className="text-2xl font-semibold text-slate-900 tabular-nums">
                    {detail.current_level!.toFixed(1)}
                    <span className="text-base text-slate-500"> / {LEVEL_MAX}</span>
                  </span>
                </div>
                <Progress value={(detail.current_level! / LEVEL_MAX) * 100} indicatorClassName="bg-[#1E3A8A]" aria-label={`Current level ${detail.current_level!.toFixed(1)} of ${LEVEL_MAX}`} />
                <p className="text-sm text-slate-600 tabular-nums">
                  Target {detail.target_level!.toFixed(1)} for your role,{" "}
                  {detail.gap! > 0 ? `gap of ${detail.gap!.toFixed(1)} levels` : "target met"}
                </p>
              </>
            )}
            {detail && !analysed && (
              <>
                <p className="text-sm text-pretty text-slate-600">Run a gap analysis to compare your level against your role target.</p>
                <ButtonLink href="/competency" size="sm">Run gap analysis</ButtonLink>
              </>
            )}
          </CardContent>
        </Card>
      </header>

      {error && <ErrorNotice message={error} />}

      <div className="grid gap-8 lg:grid-cols-3">
        <section aria-labelledby="competencies-heading" className="space-y-4 lg:col-span-2">
          <h2 id="competencies-heading" className="text-xl font-semibold text-balance text-slate-900">Competencies</h2>
          <Card>
            <ul className="divide-y divide-slate-100">
              {!detail && !error &&
                Array.from({ length: 5 }).map((_, i) => (
                  <li key={i} className="p-4">
                    <Skeleton className="h-10 w-full" />
                  </li>
                ))}
              {detail?.competencies.map((c) => (
                <li key={c.code} className="flex flex-col gap-2 p-4 sm:flex-row sm:items-center sm:gap-6">
                  <div className="min-w-0 flex-1">
                    <p className="font-medium text-slate-900">{c.name}</p>
                    <p className="text-sm text-slate-500">
                      {levelLabel(c.level)}
                      {c.evidence_source ? ` · ${EVIDENCE_LABELS[c.evidence_source] ?? c.evidence_source}` : ""}
                    </p>
                  </div>
                  <div className="flex w-full items-center gap-3 sm:w-56">
                    <Progress value={(c.level / LEVEL_MAX) * 100} indicatorClassName="bg-[#1E3A8A]" aria-label={`${c.name} level ${c.level.toFixed(1)} of ${LEVEL_MAX}`} />
                    <span className="w-12 text-right text-sm text-slate-700 tabular-nums">{c.level.toFixed(1)}</span>
                  </div>
                </li>
              ))}
            </ul>
          </Card>
        </section>

        <aside className="space-y-4">
          <h2 className="text-xl font-semibold text-balance text-slate-900">Practice this domain</h2>
          <Card>
            <CardContent className="space-y-2 pt-6">
              {meta.practice.map((p) => (
                <ButtonLink key={p.href} href={p.href} variant="outline" className="w-full justify-between">
                  {p.label}
                  <ArrowRight className="size-4" aria-hidden="true" />
                </ButtonLink>
              ))}
              <ButtonLink href="/quiz" variant="outline" className="w-full justify-between">
                Quiz yourself on your own material
                <FileQuestion className="size-4" aria-hidden="true" />
              </ButtonLink>
            </CardContent>
          </Card>
        </aside>
      </div>

      <section aria-labelledby="courses-heading" className="space-y-4">
        <div className="flex items-end justify-between gap-4">
          <h2 id="courses-heading" className="text-xl font-semibold text-balance text-slate-900">Courses in this domain</h2>
          <ButtonLink href="/recommendations" variant="ghost" size="sm">
            All recommendations
            <ArrowRight className="size-4" aria-hidden="true" />
          </ButtonLink>
        </div>
        {detail && detail.courses.length === 0 && (
          <Card>
            <CardContent className="pt-6 text-sm text-slate-600">
              No courses are mapped to this domain yet.{" "}
              <ButtonLink href="/courses" variant="ghost" size="sm">Browse the full catalogue</ButtonLink>
            </CardContent>
          </Card>
        )}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {detail?.courses.map((course) => (
            <Card key={course.id} className="flex flex-col">
              <CardHeader>
                <div className="flex flex-wrap items-center gap-2">
                  {course.recommended && (
                    <Badge variant="default">
                      <Sparkles className="mr-1 size-3" aria-hidden="true" />
                      Recommended for you
                    </Badge>
                  )}
                  <Badge variant="outline" className="capitalize">{course.difficulty}</Badge>
                </div>
                <CardTitle className="text-base text-balance">{course.title}</CardTitle>
                <CardDescription className="line-clamp-3 text-pretty">{course.reason ?? course.overview}</CardDescription>
              </CardHeader>
              <CardContent className="mt-auto flex items-center justify-between">
                <span className="flex items-center gap-1 text-sm text-slate-500 tabular-nums">
                  <Clock className="size-4" aria-hidden="true" />
                  {course.duration_hours} h
                </span>
                <ButtonLink href={`/courses/${course.id}`} size="sm">View course</ButtonLink>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
}
