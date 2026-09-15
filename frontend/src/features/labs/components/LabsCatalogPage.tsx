"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import {
  ArrowRight,
  BarChart3,
  Brain,
  Bug,
  Code2,
  Database,
  FlaskConical,
  Search,
  Server,
  ShieldCheck,
  Table2,
  type LucideIcon,
} from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import { ErrorNotice } from "@/components/shared/ErrorNotice";
import { fetchApi } from "@/lib/api";
import type { LabDetail } from "@/lib/types/labs";

const DIFFICULTIES = ["all", "beginner", "intermediate", "advanced"] as const;

function labIcon(tags: string[] = []): LucideIcon {
  const has = (...names: string[]) => tags.some((t) => names.includes(t.toLowerCase()));
  if (has("sql", "database")) return Database;
  if (has("pandas", "dataframe", "data-cleaning", "cleaning")) return Table2;
  if (has("ai-ml", "machine-learning")) return Brain;
  if (has("fastapi", "api", "backend")) return Server;
  if (has("debugging", "bug")) return Bug;
  if (has("data-visualization", "visualization", "chart")) return BarChart3;
  return Code2;
}

export default function LabsCatalogPage() {
  const [labs, setLabs] = useState<LabDetail[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [difficulty, setDifficulty] = useState<(typeof DIFFICULTIES)[number]>("all");
  const [skill, setSkill] = useState("all");

  useEffect(() => {
    fetchApi<LabDetail[]>("/technical-courses/labs")
      .then(setLabs)
      .catch((err: Error) => setError(err.message));
  }, []);

  // Skill chips come from the labs themselves, most common first.
  const skills = useMemo(() => {
    const counts = new Map<string, number>();
    for (const lab of labs ?? []) for (const tag of lab.tags ?? []) counts.set(tag, (counts.get(tag) ?? 0) + 1);
    return [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10).map(([tag]) => tag);
  }, [labs]);

  const filtered = (labs ?? []).filter((lab) => {
    const text = `${lab.title} ${lab.objective}`.toLowerCase();
    return (
      text.includes(query.trim().toLowerCase()) &&
      (difficulty === "all" || lab.difficulty === difficulty) &&
      (skill === "all" || (lab.tags ?? []).includes(skill))
    );
  });
  const totalTests = (labs ?? []).reduce((sum, lab) => sum + (lab.test_cases_count ?? lab.test_cases?.length ?? 0), 0);

  return (
    <div className="min-h-[calc(100vh-65px)] bg-slate-50">
      <div className="mx-auto max-w-7xl space-y-6 px-4 py-8 sm:px-6 lg:px-8">
        <header className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div className="space-y-2">
            <p className="text-sm font-medium text-[#0D9488]">Technical competency</p>
            <h1 className="text-3xl font-bold text-balance text-slate-900">Hands-on labs</h1>
            <p className="max-w-2xl text-pretty text-slate-600">
              Practise real statistical programming tasks in a Jupyter notebook. Run your code cell by cell in a Python
              sandbox, then submit it to be checked by automatic tests.
            </p>
          </div>
          {labs && (
            <dl className="grid grid-cols-3 gap-3 text-center sm:w-96">
              {[
                ["Labs", labs.length],
                ["Graded tests", totalTests],
                ["Language", "Python"],
              ].map(([label, value]) => (
                <div key={label} className="rounded-xl border border-slate-200 bg-white p-3">
                  <dt className="text-xs text-slate-500">{label}</dt>
                  <dd className="mt-0.5 text-lg font-semibold tabular-nums text-slate-900">{value}</dd>
                </div>
              ))}
            </dl>
          )}
        </header>

        <div className="space-y-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <div className="relative md:w-96">
              <label htmlFor="lab-search" className="sr-only">
                Search labs
              </label>
              <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-slate-400" aria-hidden="true" />
              <input
                id="lab-search"
                type="search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search labs by title or goal"
                className="w-full rounded-lg border border-slate-300 bg-white py-2 pl-9 pr-3 text-sm text-slate-900 focus:border-[#1E3A8A] focus:outline-none focus:ring-2 focus:ring-[#1E3A8A]/20"
              />
            </div>
            <div role="radiogroup" aria-label="Difficulty" className="flex rounded-lg border border-slate-200 p-0.5">
              {DIFFICULTIES.map((d) => (
                <button
                  key={d}
                  type="button"
                  role="radio"
                  aria-checked={difficulty === d}
                  onClick={() => setDifficulty(d)}
                  className={`rounded-md px-3 py-1.5 text-sm capitalize transition-colors ${
                    difficulty === d ? "bg-[#1E3A8A] font-medium text-white" : "text-slate-600 hover:bg-slate-100"
                  }`}
                >
                  {d === "all" ? "All levels" : d}
                </button>
              ))}
            </div>
          </div>
          {skills.length > 0 && (
            <div className="flex flex-wrap gap-2" role="radiogroup" aria-label="Skill">
              {["all", ...skills].map((tag) => (
                <button
                  key={tag}
                  type="button"
                  role="radio"
                  aria-checked={skill === tag}
                  onClick={() => setSkill(tag)}
                  className={`rounded-full border px-3 py-1 text-xs font-medium transition-colors ${
                    skill === tag ? "border-[#1E3A8A] bg-blue-50 text-[#1E3A8A]" : "border-slate-200 text-slate-600 hover:bg-slate-50"
                  }`}
                >
                  {tag === "all" ? "All skills" : tag}
                </button>
              ))}
            </div>
          )}
        </div>

        {error && <ErrorNotice message={error} />}

        {!labs && !error && (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3" aria-busy="true">
            {Array.from({ length: 6 }).map((_, i) => (
              <Skeleton key={i} className="h-60 w-full rounded-2xl" />
            ))}
          </div>
        )}

        {labs && filtered.length === 0 && (
          <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center">
            <FlaskConical className="mx-auto size-8 text-slate-400" aria-hidden="true" />
            <h2 className="mt-2 text-sm font-semibold text-slate-900">No labs match these filters</h2>
            <p className="mt-1 text-sm text-slate-500">Try a different search or skill.</p>
          </div>
        )}

        {filtered.length > 0 && (
          <ul className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {filtered.map((lab) => {
              const Icon = labIcon(lab.tags);
              const testCount = lab.test_cases_count ?? lab.test_cases?.length ?? 0;
              return (
                <li key={lab.id}>
                  <Link
                    href={`/labs/${lab.id}`}
                    className="group flex h-full flex-col rounded-2xl border border-slate-200 bg-white p-5 shadow-xs transition hover:border-[#1E3A8A]/40 hover:shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#1E3A8A]"
                  >
                    <div className="flex items-center justify-between">
                      <span className="flex size-10 items-center justify-center rounded-xl bg-slate-100 text-slate-700">
                        <Icon className="size-5" aria-hidden="true" />
                      </span>
                      <span className="text-xs capitalize text-slate-500">{lab.difficulty}</span>
                    </div>
                    <h2 className="mt-4 text-base font-semibold text-balance text-slate-900 group-hover:text-[#1E3A8A]">{lab.title}</h2>
                    <p className="mt-1.5 line-clamp-2 text-sm text-pretty text-slate-600">{lab.objective}</p>
                    {lab.tags && lab.tags.length > 0 && (
                      <div className="mt-3 flex flex-wrap gap-1.5">
                        {lab.tags.slice(0, 3).map((tag) => (
                          <span key={tag} className="rounded-md bg-slate-100 px-2 py-0.5 text-xs text-slate-600">
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                    <div className="mt-auto flex items-center justify-between border-t border-slate-100 pt-4 text-sm">
                      <span className="inline-flex items-center gap-1.5 text-slate-500">
                        <ShieldCheck className="size-4" aria-hidden="true" />
                        {testCount} graded {testCount === 1 ? "test" : "tests"}
                      </span>
                      <span className="inline-flex items-center gap-1 font-medium text-[#1E3A8A]">
                        Open lab
                        <ArrowRight className="size-4 transition-transform group-hover:translate-x-0.5" aria-hidden="true" />
                      </span>
                    </div>
                  </Link>
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </div>
  );
}
