"use client";

import React, { useState, useEffect, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import {
  Play,
  RotateCcw,
  Plus,
  Trash2,
  ChevronUp,
  ChevronDown,
  Download,
  FileCode,
  Layers,
  Terminal,
  CheckCircle2,
  XCircle,
  AlertCircle,
  Sparkles,
  BookOpen,
  Cpu,
  ArrowRight,
  ShieldCheck,
  Eye,
  EyeOff,
  Sliders,
  Copy,
  Check,
  SplitSquareVertical,
  FlaskConical,
  HelpCircle,
  Maximize2,
  Minimize2,
  Share2,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { fetchApi } from "@/lib/api";
import {
  LabDetail,
  NotebookCell,
  LabExecutionResult,
  CellExecutionResult,
} from "@/lib/types";
import { useI18n } from "@/lib/i18n";
import confetti from "canvas-confetti";

type ViewMode = "jupyter" | "marimo" | "ide";
type BottomTab = "terminal" | "tests" | "variables" | "marimo-graph" | "hints";

export default function LabWorkspacePage() {
  const { labId } = useParams();
  const router = useRouter();
  const { t } = useI18n();

  const [lab, setLab] = useState<LabDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<ViewMode>("jupyter");
  const [activeBottomTab, setActiveBottomTab] = useState<BottomTab>("terminal");
  const [activeCellIndex, setActiveCellIndex] = useState<number>(0);
  const [isExecutingAll, setIsExecutingAll] = useState(false);
  const [isExecutingStudent, setIsExecutingStudent] = useState(false);
  const [kernelStatus, setKernelStatus] = useState<"idle" | "busy" | "ready">("ready");
  const [executionCounter, setExecutionCounter] = useState(1);
  const [showSolution, setShowSolution] = useState(false);
  const [copiedScript, setCopiedScript] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);

  // Marimo interactive simulation state
  const [marimoSliderValue, setMarimoSliderValue] = useState(50);
  const [marimoCategoryFilter, setMarimoCategoryFilter] = useState("all");

  // Terminal logs
  const [terminalLogs, setTerminalLogs] = useState<
    Array<{ type: "info" | "stdout" | "stderr" | "success" | "error"; text: string; timestamp: string }>
  >([]);

  // Test execution result
  const [testResult, setTestResult] = useState<LabExecutionResult | null>(null);

  // Notebook cells
  const [cells, setCells] = useState<NotebookCell[]>([]);

  // Split IDE code
  const [ideCode, setIdeCode] = useState<string>("");

  useEffect(() => {
    if (!labId) return;

    setLoading(true);
    fetchApi<LabDetail>(`/technical-courses/labs/${labId}`)
      .then((data) => {
        setLab(data);
        setIdeCode(data.starter_code || "");

        // Initialize default notebook cells from starter code and instructions
        const initialCells: NotebookCell[] = [
          {
            id: "cell-intro",
            type: "markdown",
            content: `### 🧪 ${data.title}\n\n**Objective:** ${data.objective}\n\n${data.instructions || ""}`,
          },
          {
            id: "cell-code-1",
            type: "code",
            content: data.starter_code || "# Write your Python code here\n",
            execution_count: null,
            status: "idle",
            output: null,
          },
          {
            id: "cell-code-test",
            type: "code",
            content: `# Verification test harness\n# Run this cell to check your logic\n${
              data.test_cases && data.test_cases.length > 0
                ? data.test_cases[0].test_code
                : "# Define test verification here"
            }`,
            execution_count: null,
            status: "idle",
            output: null,
          },
        ];
        setCells(initialCells);

        addLog("info", `Jupyter Kernel & Docker Sandbox initialized for lab #${data.id}: "${data.title}"`);
      })
      .catch((err) => {
        console.error("Error loading lab:", err);
        addLog("error", `Failed to load lab: ${err.message}`);
      })
      .finally(() => setLoading(false));
  }, [labId]);

  const addLog = (
    type: "info" | "stdout" | "stderr" | "success" | "error",
    text: string
  ) => {
    const time = new Date().toLocaleTimeString();
    setTerminalLogs((prev) => [...prev, { type, text, timestamp: time }]);
  };

  // Run a single notebook cell
  const handleRunCell = async (index: number) => {
    const cell = cells[index];
    if (cell.type === "markdown") return;

    setKernelStatus("busy");
    setCells((prev) =>
      prev.map((c, i) => (i === index ? { ...c, status: "running" } : c))
    );

    const contextCode = cells
      .slice(0, index)
      .filter((c) => c.type === "code")
      .map((c) => c.content)
      .join("\n\n");

    const currentExecCount = executionCounter;
    setExecutionCounter((prev) => prev + 1);

    addLog("info", `Executing Cell [${currentExecCount}] in isolated Python Sandbox...`);

    try {
      const res = await fetchApi<CellExecutionResult>(
        "/technical-courses/sandbox/execute-code",
        {
          method: "POST",
          body: JSON.stringify({
            code: cell.content,
            context_code: contextCode,
          }),
        }
      );

      setCells((prev) =>
        prev.map((c, i) =>
          i === index
            ? {
                ...c,
                status: res.success ? "success" : "error",
                execution_count: currentExecCount,
                output: res.output,
                stdout: res.stdout,
                stderr: res.stderr,
                duration_ms: res.execution_time_ms,
              }
            : c
        )
      );

      if (res.stdout) addLog("stdout", res.stdout);
      if (res.stderr) addLog("stderr", res.stderr);
      addLog(
        res.success ? "success" : "error",
        `Cell [${currentExecCount}] completed in ${res.execution_time_ms}ms (Exit Code: ${res.exit_code})`
      );
    } catch (err: any) {
      setCells((prev) =>
        prev.map((c, i) =>
          i === index
            ? {
                ...c,
                status: "error",
                execution_count: currentExecCount,
                output: `Execution error: ${err.message}`,
              }
            : c
        )
      );
      addLog("error", `Cell execution failed: ${err.message}`);
    } finally {
      setKernelStatus("idle");
    }
  };

  // Run all cells sequentially
  const handleRunAllCells = async () => {
    setIsExecutingAll(true);
    setKernelStatus("busy");
    addLog("info", "Starting sequential execution of all notebook cells...");

    for (let i = 0; i < cells.length; i++) {
      if (cells[i].type === "code") {
        await handleRunCell(i);
      }
    }

    setIsExecutingAll(false);
    setKernelStatus("idle");
    addLog("success", "All notebook cells executed successfully.");
  };

  // Submit and validate full lab code in sandbox
  const handleSubmitLab = async () => {
    if (!lab) return;
    setIsExecutingStudent(true);
    setKernelStatus("busy");
    setActiveBottomTab("tests");

    // Gather solution code from IDE mode or from the primary code cell in notebook mode
    const codeToValidate =
      viewMode === "ide"
        ? ideCode
        : cells
            .filter((c) => c.type === "code")
            .map((c) => c.content)
            .join("\n\n");

    addLog("info", "Submitting solution to Docker Sandbox test harness...");

    try {
      const res = await fetchApi<LabExecutionResult>(
        `/technical-courses/labs/${lab.id}/execute`,
        {
          method: "POST",
          body: JSON.stringify({ code: codeToValidate }),
        }
      );

      setTestResult(res);

      if (res.all_passed) {
        addLog(
          "success",
          `🎉 ALL ${res.passed_tests_count}/${res.total_tests_count} TEST CASES PASSED in ${res.execution_time_ms}ms!`
        );
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 },
        });
      } else {
        addLog(
          "error",
          `⚠️ ${res.passed_tests_count} of ${res.total_tests_count} tests passed. Review failing test cases below.`
        );
      }
    } catch (err: any) {
      addLog("error", `Test execution failed: ${err.message}`);
    } finally {
      setIsExecutingStudent(false);
      setKernelStatus("idle");
    }
  };

  // Cell management
  const addCell = (index: number, type: "code" | "markdown") => {
    const newCell: NotebookCell = {
      id: `cell-${Date.now()}`,
      type,
      content: type === "code" ? "# New Python Code Cell\n" : "### Markdown Note\n",
      execution_count: null,
      status: "idle",
      output: null,
    };
    const nextCells = [...cells];
    nextCells.splice(index + 1, 0, newCell);
    setCells(nextCells);
    setActiveCellIndex(index + 1);
  };

  const removeCell = (index: number) => {
    if (cells.length <= 1) return;
    setCells(cells.filter((_, i) => i !== index));
    setActiveCellIndex(Math.max(0, index - 1));
  };

  const moveCell = (index: number, direction: "up" | "down") => {
    const targetIdx = direction === "up" ? index - 1 : index + 1;
    if (targetIdx < 0 || targetIdx >= cells.length) return;
    const nextCells = [...cells];
    const [moved] = nextCells.splice(index, 1);
    nextCells.splice(targetIdx, 0, moved);
    setCells(nextCells);
    setActiveCellIndex(targetIdx);
  };

  const updateCellContent = (index: number, newContent: string) => {
    setCells((prev) =>
      prev.map((c, i) => (i === index ? { ...c, content: newContent } : c))
    );
  };

  // Export to .ipynb or Marimo .py
  const handleExport = async (format: "ipynb" | "marimo") => {
    if (!lab) return;

    try {
      const payloadCells =
        viewMode === "ide"
          ? [
              { type: "markdown", content: `### ${lab.title}\n\n${lab.instructions}` },
              { type: "code", content: ideCode, execution_count: 1 },
            ]
          : cells.map((c) => ({
              type: c.type,
              content: c.content,
              execution_count: c.execution_count || 1,
            }));

      const res = await fetchApi<{
        filename: string;
        content: string;
        mime_type: string;
      }>("/technical-courses/notebook/export", {
        method: "POST",
        body: JSON.stringify({
          title: lab.title,
          format,
          cells: payloadCells,
        }),
      });

      // Trigger browser download
      const blob = new Blob([res.content], { type: res.mime_type });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = res.filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      addLog("success", `Downloaded notebook as ${res.filename}`);
    } catch (err: any) {
      alert(`Export failed: ${err.message}`);
    }
  };

  if (loading) {
    return (
      <div className="min-h-[85vh] flex flex-col items-center justify-center space-y-4 bg-slate-950 text-white">
        <div className="h-10 w-10 rounded-full border-4 border-slate-700 border-t-amber-500 animate-spin" />
        <p className="text-sm text-slate-400 font-mono">Initializing Jupyter Sandbox & Marimo Extension...</p>
      </div>
    );
  }

  if (!lab) {
    return (
      <div className="min-h-[80vh] flex flex-col items-center justify-center p-6 text-center">
        <AlertCircle className="h-10 w-10 text-rose-500 mb-3" />
        <h2 className="text-lg font-bold text-slate-900">Lab Not Found</h2>
        <p className="text-xs text-slate-500 mt-1 max-w-sm">
          The requested hands-on technical lab could not be loaded.
        </p>
        <Link href="/labs" className="mt-4">
          <Button size="sm">Back to Labs Catalog</Button>
        </Link>
      </div>
    );
  }

  return (
    <div
      className={`flex flex-col bg-slate-950 text-slate-100 font-sans ${
        isFullscreen ? "fixed inset-0 z-50 overflow-hidden" : "min-h-[calc(100vh-65px)]"
      }`}
    >
      {/* 1. TOP APP BAR & CONTROLS */}
      <header className="h-14 border-b border-slate-800 bg-slate-900/90 backdrop-blur px-4 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <Link
            href="/labs"
            className="text-xs font-semibold text-slate-400 hover:text-white flex items-center gap-1 transition-colors"
          >
            ← Labs
          </Link>
          <span className="text-slate-700">|</span>
          <div className="flex items-center gap-2">
            <FlaskConical className="h-4 w-4 text-amber-500" />
            <h1 className="text-sm font-bold text-white truncate max-w-xs md:max-w-md">
              {lab.title}
            </h1>
            <Badge
              variant="outline"
              className="text-[10px] uppercase font-bold border-amber-500/30 text-amber-400 bg-amber-500/10 hidden sm:inline-flex"
            >
              {lab.difficulty}
            </Badge>
          </div>
        </div>

        {/* Center: Mode Switcher (Jupyter vs Marimo vs IDE) */}
        <div className="flex items-center bg-slate-800 p-0.5 rounded-lg border border-slate-700">
          <button
            onClick={() => setViewMode("jupyter")}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-semibold transition-all cursor-pointer ${
              viewMode === "jupyter"
                ? "bg-[#1E3A8A] text-white shadow-xs"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <BookOpen className="h-3.5 w-3.5 text-amber-400" />
            <span>Jupyter Notebook</span>
          </button>
          <button
            onClick={() => setViewMode("marimo")}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-semibold transition-all cursor-pointer ${
              viewMode === "marimo"
                ? "bg-emerald-800 text-white shadow-xs"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <Sparkles className="h-3.5 w-3.5 text-emerald-400" />
            <span>Marimo Extension</span>
          </button>
          <button
            onClick={() => setViewMode("ide")}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-semibold transition-all cursor-pointer ${
              viewMode === "ide"
                ? "bg-purple-800 text-white shadow-xs"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <SplitSquareVertical className="h-3.5 w-3.5 text-purple-400" />
            <span>Split IDE</span>
          </button>
        </div>

        {/* Right: Kernel Status & Action Buttons */}
        <div className="flex items-center gap-2">
          {/* Kernel Status Badge */}
          <div className="hidden lg:flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-md bg-slate-800/80 border border-slate-700">
            <span
              className={`h-2 w-2 rounded-full ${
                kernelStatus === "busy"
                  ? "bg-amber-400 animate-ping"
                  : kernelStatus === "ready"
                  ? "bg-emerald-400"
                  : "bg-slate-400"
              }`}
            />
            <span className="text-slate-300 text-[11px] font-mono">
              Python 3.11 ({kernelStatus})
            </span>
          </div>

          {/* Export dropdown / buttons */}
          <button
            onClick={() => handleExport("marimo")}
            title="Download Marimo Reactive App (.py)"
            className="flex items-center gap-1 px-2.5 py-1 text-xs rounded-md bg-slate-800 border border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700 transition-colors cursor-pointer"
          >
            <Download className="h-3.5 w-3.5 text-emerald-400" />
            <span className="hidden sm:inline">Marimo .py</span>
          </button>

          <button
            onClick={() => handleExport("ipynb")}
            title="Download Jupyter Notebook (.ipynb)"
            className="flex items-center gap-1 px-2.5 py-1 text-xs rounded-md bg-slate-800 border border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700 transition-colors cursor-pointer"
          >
            <Download className="h-3.5 w-3.5 text-amber-400" />
            <span className="hidden sm:inline">Jupyter .ipynb</span>
          </button>

          {/* Submit / Run Test Harness Button */}
          <Button
            size="sm"
            onClick={handleSubmitLab}
            disabled={isExecutingStudent}
            className="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold px-4 cursor-pointer shadow-xs"
          >
            <ShieldCheck className="h-3.5 w-3.5 mr-1" />
            {isExecutingStudent ? "Testing..." : "Submit Lab"}
          </Button>

          {/* Fullscreen Toggle */}
          <button
            onClick={() => setIsFullscreen(!isFullscreen)}
            className="p-1.5 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition-colors cursor-pointer"
            title={isFullscreen ? "Exit Fullscreen" : "Fullscreen Workspace"}
          >
            {isFullscreen ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
          </button>
        </div>
      </header>

      {/* 2. MAIN WORKSPACE CONTENT */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Side: Instructions & Lab Specs */}
        <aside className="w-80 border-r border-slate-800 bg-slate-900/60 flex flex-col shrink-0 overflow-y-auto p-4 space-y-4 text-xs">
          <div>
            <span className="text-[10px] font-bold text-amber-400 uppercase tracking-wider">
              Official Technical Lab Spec
            </span>
            <h2 className="text-base font-bold text-white mt-1">{lab.title}</h2>
            <p className="text-slate-400 text-xs mt-1 leading-relaxed">{lab.objective}</p>
          </div>

          <div className="p-3 bg-slate-800/80 rounded-xl border border-slate-700/60 space-y-1.5">
            <span className="text-[10px] font-bold text-slate-400 uppercase">Environment</span>
            <div className="flex items-center justify-between text-slate-300">
              <span>Runtime Engine:</span>
              <span className="font-mono text-emerald-400">Docker Sandbox</span>
            </div>
            <div className="flex items-center justify-between text-slate-300">
              <span>Language:</span>
              <span className="font-mono text-amber-400">Python 3.11</span>
            </div>
            <div className="flex items-center justify-between text-slate-300">
              <span>Test Cases:</span>
              <span className="font-mono text-white">
                {lab.test_cases?.length || lab.test_cases_count || 3} unit assertions
              </span>
            </div>
          </div>

          {/* Instructions */}
          <div className="space-y-2">
            <h3 className="font-bold text-slate-200 uppercase tracking-wide text-[11px]">
              Instructions &amp; Requirements
            </h3>
            <div className="text-slate-300 prose prose-invert prose-xs leading-relaxed whitespace-pre-wrap bg-slate-950/60 p-3 rounded-lg border border-slate-800">
              {lab.instructions}
            </div>
          </div>

          {/* Constraints */}
          {lab.constraints && lab.constraints.length > 0 && (
            <div className="space-y-1.5">
              <h3 className="font-bold text-slate-200 uppercase tracking-wide text-[11px]">
                Constraints
              </h3>
              <ul className="list-disc pl-4 space-y-1 text-slate-400">
                {lab.constraints.map((c, i) => (
                  <li key={i}>{c}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Solution & Hints Accordion */}
          {lab.solution && (
            <div className="pt-2 border-t border-slate-800">
              <button
                onClick={() => setShowSolution(!showSolution)}
                className="w-full flex items-center justify-between p-2 rounded-lg bg-slate-800/60 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-semibold cursor-pointer transition-colors"
              >
                <span className="flex items-center gap-1.5">
                  {showSolution ? <EyeOff className="h-3.5 w-3.5" /> : <Eye className="h-3.5 w-3.5" />}
                  {showSolution ? "Hide Reference Solution" : "Show Reference Solution"}
                </span>
                <ChevronDown
                  className={`h-3.5 w-3.5 transform transition-transform ${
                    showSolution ? "rotate-180" : ""
                  }`}
                />
              </button>

              {showSolution && (
                <div className="mt-2 p-3 bg-slate-950 rounded-lg border border-amber-500/30 text-slate-300 space-y-2">
                  <p className="text-[11px] text-amber-400 font-semibold">Reference Implementation:</p>
                  <pre className="p-2 bg-slate-900 rounded text-[11px] font-mono text-emerald-300 overflow-x-auto">
                    {lab.solution.reference_code}
                  </pre>
                  {lab.solution.explanation && (
                    <p className="text-[11px] text-slate-400 italic">
                      {lab.solution.explanation}
                    </p>
                  )}
                </div>
              )}
            </div>
          )}
        </aside>

        {/* Center: Interactive Workspace (Notebook / Marimo / Split IDE) */}
        <main className="flex-1 flex flex-col overflow-hidden bg-slate-950">
          {/* A. JUPYTER NOTEBOOK VIEW */}
          {viewMode === "jupyter" && (
            <div className="flex-1 flex flex-col overflow-hidden">
              {/* Notebook Toolbar */}
              <div className="h-10 border-b border-slate-800 bg-slate-900/60 px-4 flex items-center justify-between shrink-0">
                <div className="flex items-center gap-1.5">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleRunCell(activeCellIndex)}
                    className="h-7 text-xs border-slate-700 text-slate-200 hover:bg-slate-800 hover:text-white cursor-pointer"
                  >
                    <Play className="h-3 w-3 text-emerald-400 mr-1" /> Run Cell
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={handleRunAllCells}
                    disabled={isExecutingAll}
                    className="h-7 text-xs border-slate-700 text-slate-200 hover:bg-slate-800 hover:text-white cursor-pointer"
                  >
                    <RotateCcw className="h-3 w-3 text-amber-400 mr-1" /> Run All
                  </Button>
                  <span className="text-slate-700 mx-1">|</span>
                  <button
                    onClick={() => addCell(activeCellIndex, "code")}
                    className="flex items-center gap-1 px-2.5 py-1 text-xs text-slate-300 hover:text-white hover:bg-slate-800 rounded transition-colors cursor-pointer"
                  >
                    <Plus className="h-3 w-3" /> + Code
                  </button>
                  <button
                    onClick={() => addCell(activeCellIndex, "markdown")}
                    className="flex items-center gap-1 px-2.5 py-1 text-xs text-slate-300 hover:text-white hover:bg-slate-800 rounded transition-colors cursor-pointer"
                  >
                    <Plus className="h-3 w-3" /> + Markdown
                  </button>
                </div>

                <div className="text-[11px] text-slate-500 font-mono">
                  {cells.length} cells • Active Cell: #{activeCellIndex + 1}
                </div>
              </div>

              {/* Notebook Cells Container */}
              <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4">
                {cells.map((cell, idx) => {
                  const isActive = idx === activeCellIndex;
                  return (
                    <div
                      key={cell.id}
                      onClick={() => setActiveCellIndex(idx)}
                      className={`rounded-xl border transition-all ${
                        isActive
                          ? "border-[#1E3A8A] ring-1 ring-blue-500/50 bg-slate-900/90 shadow-md"
                          : "border-slate-800/80 bg-slate-900/40 hover:border-slate-700"
                      }`}
                    >
                      {/* Cell Header / Action bar */}
                      <div className="px-3 py-1.5 border-b border-slate-800/70 bg-slate-900/60 flex items-center justify-between text-xs text-slate-400">
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-[11px] text-amber-400/80">
                            {cell.type === "code"
                              ? `[${cell.execution_count ?? (cell.status === "running" ? "*" : " ")}]`
                              : "Markdown"}
                          </span>
                          <span className="text-[10px] uppercase font-bold text-slate-500">
                            {cell.type}
                          </span>
                          {cell.duration_ms !== undefined && (
                            <span className="text-[10px] text-slate-500 font-mono">
                              ({cell.duration_ms}ms)
                            </span>
                          )}
                        </div>

                        <div className="flex items-center gap-1">
                          {cell.type === "code" && (
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                handleRunCell(idx);
                              }}
                              className="p-1 rounded hover:bg-emerald-950/60 text-emerald-400 hover:text-emerald-300 transition-colors cursor-pointer"
                              title="Run this cell (Shift+Enter)"
                            >
                              <Play className="h-3.5 w-3.5" />
                            </button>
                          )}
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              moveCell(idx, "up");
                            }}
                            disabled={idx === 0}
                            className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-white disabled:opacity-30 cursor-pointer"
                            title="Move Up"
                          >
                            <ChevronUp className="h-3.5 w-3.5" />
                          </button>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              moveCell(idx, "down");
                            }}
                            disabled={idx === cells.length - 1}
                            className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-white disabled:opacity-30 cursor-pointer"
                            title="Move Down"
                          >
                            <ChevronDown className="h-3.5 w-3.5" />
                          </button>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              removeCell(idx);
                            }}
                            className="p-1 rounded hover:bg-rose-950/60 text-slate-400 hover:text-rose-400 transition-colors cursor-pointer"
                            title="Delete Cell"
                          >
                            <Trash2 className="h-3.5 w-3.5" />
                          </button>
                        </div>
                      </div>

                      {/* Cell Input Area */}
                      <div className="p-3">
                        {cell.type === "markdown" ? (
                          <textarea
                            value={cell.content}
                            onChange={(e) => updateCellContent(idx, e.target.value)}
                            rows={Math.max(3, cell.content.split("\n").length)}
                            className="w-full bg-transparent font-sans text-sm text-slate-200 outline-none resize-y placeholder-slate-600 focus:ring-0 leading-relaxed"
                            placeholder="Write markdown documentation here..."
                          />
                        ) : (
                          <div className="flex font-mono text-xs">
                            <div className="pr-3 text-slate-600 select-none text-right">
                              {cell.content.split("\n").map((_, lineIdx) => (
                                <div key={lineIdx}>{lineIdx + 1}</div>
                              ))}
                            </div>
                            <textarea
                              value={cell.content}
                              onChange={(e) => updateCellContent(idx, e.target.value)}
                              onKeyDown={(e) => {
                                if (e.key === "Enter" && (e.shiftKey || e.ctrlKey)) {
                                  e.preventDefault();
                                  handleRunCell(idx);
                                }
                              }}
                              rows={Math.max(4, cell.content.split("\n").length)}
                              className="w-full bg-transparent font-mono text-xs text-emerald-300 outline-none resize-none placeholder-slate-600 focus:ring-0 leading-relaxed"
                              placeholder="# Enter Python code here..."
                              spellCheck={false}
                            />
                          </div>
                        )}
                      </div>

                      {/* Cell Output Display */}
                      {cell.output && (
                        <div className="border-t border-slate-800 bg-slate-950/90 p-3 rounded-b-xl text-xs font-mono">
                          <div className="flex items-center gap-1.5 text-[10px] text-slate-500 uppercase font-bold mb-1">
                            <span>Output:</span>
                            {cell.status === "error" ? (
                              <span className="text-rose-400 flex items-center gap-1">
                                <XCircle className="h-3 w-3" /> Error
                              </span>
                            ) : (
                              <span className="text-emerald-400 flex items-center gap-1">
                                <CheckCircle2 className="h-3 w-3" /> Finished
                              </span>
                            )}
                          </div>
                          <pre
                            className={`whitespace-pre-wrap overflow-x-auto leading-relaxed ${
                              cell.status === "error" ? "text-rose-300" : "text-slate-200"
                            }`}
                          >
                            {cell.output}
                          </pre>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* B. MARIMO REACTIVE EXTENSION VIEW */}
          {viewMode === "marimo" && (
            <div className="flex-1 flex flex-col overflow-y-auto p-6 space-y-6">
              {/* Marimo Reactive Banner */}
              <div className="p-4 rounded-xl bg-gradient-to-r from-emerald-950/80 to-slate-900 border border-emerald-500/30 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                  <div className="flex items-center gap-2">
                    <Sparkles className="h-4 w-4 text-emerald-400" />
                    <h3 className="text-sm font-bold text-white">Marimo Reactive Notebook Engine</h3>
                    <Badge className="bg-emerald-500/20 text-emerald-400 border-emerald-500/40 text-[10px]">
                      Reactive DAG Active
                    </Badge>
                  </div>
                  <p className="text-xs text-slate-400 mt-1 max-w-xl">
                    Marimo treats code cells as pure reactive nodes. Changing a variable or UI slider
                    automatically triggers downstream updates without out-of-order execution bugs.
                  </p>
                </div>

                <button
                  onClick={() => handleExport("marimo")}
                  className="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition-colors flex items-center gap-1.5 self-start sm:self-auto cursor-pointer"
                >
                  <Download className="h-3.5 w-3.5" /> Export Marimo App (.py)
                </button>
              </div>

              {/* Reactive UI Widgets Section (Marimo mo.ui Simulation) */}
              <Card className="border-slate-800 bg-slate-900/70 shadow-xs">
                <CardHeader className="pb-3 border-b border-slate-800">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Sliders className="h-4 w-4 text-emerald-400" />
                      <CardTitle className="text-sm font-bold text-white">
                        Interactive Marimo UI Controls (`mo.ui`)
                      </CardTitle>
                    </div>
                    <span className="text-[11px] font-mono text-slate-400">
                      Auto-reacts on change
                    </span>
                  </div>
                </CardHeader>
                <CardContent className="p-5 space-y-5">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {/* Reactive Slider */}
                    <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                      <div className="flex justify-between text-xs">
                        <span className="text-slate-300 font-medium">
                          `mo.ui.slider(start=1, stop=100, label="Sample Threshold")`:
                        </span>
                        <span className="font-mono text-emerald-400 font-bold">
                          {marimoSliderValue}%
                        </span>
                      </div>
                      <input
                        type="range"
                        min="1"
                        max="100"
                        value={marimoSliderValue}
                        onChange={(e) => setMarimoSliderValue(Number(e.target.value))}
                        className="w-full accent-emerald-500 cursor-pointer"
                      />
                    </div>

                    {/* Reactive Dropdown */}
                    <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                      <span className="text-xs text-slate-300 font-medium">
                        `mo.ui.dropdown(options=["all", "rural", "urban"], label="Strata")`:
                      </span>
                      <select
                        value={marimoCategoryFilter}
                        onChange={(e) => setMarimoCategoryFilter(e.target.value)}
                        className="w-full bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg p-2 outline-none"
                      >
                        <option value="all">All Strata (MoSPI Combined)</option>
                        <option value="rural">Rural Consumer Basket (CPI-R)</option>
                        <option value="urban">Urban Consumer Basket (CPI-U)</option>
                      </select>
                    </div>
                  </div>

                  {/* Reactive Output KPI Cards */}
                  <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 grid grid-cols-3 gap-3 text-center">
                    <div>
                      <p className="text-slate-500 text-[10px] uppercase font-bold">Computed Records</p>
                      <p className="text-base font-bold font-mono text-emerald-400">
                        {Math.round((marimoSliderValue / 100) * 12500)} items
                      </p>
                    </div>
                    <div>
                      <p className="text-slate-500 text-[10px] uppercase font-bold">Strata Mode</p>
                      <p className="text-base font-bold font-mono text-white capitalize">
                        {marimoCategoryFilter}
                      </p>
                    </div>
                    <div>
                      <p className="text-slate-500 text-[10px] uppercase font-bold">Confidence Interval</p>
                      <p className="text-base font-bold font-mono text-amber-400">
                        {(95 + (marimoSliderValue * 0.04)).toFixed(2)}%
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Reactive Cell Code Graph Viewer */}
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                    Reactive Cell Flow (@app.cell structure)
                  </h4>
                  <span className="text-[11px] text-slate-500 font-mono">
                    Serialized for `marimo run` &amp; `marimo edit`
                  </span>
                </div>

                {cells.map((c, i) => (
                  <div
                    key={c.id}
                    className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 font-mono text-xs space-y-2"
                  >
                    <div className="flex items-center justify-between text-slate-500 text-[11px]">
                      <span className="text-emerald-400 font-bold">@app.cell</span>
                      <span>Node #{i + 1}</span>
                    </div>
                    <pre className="text-slate-300 whitespace-pre-wrap overflow-x-auto bg-slate-950 p-3 rounded-lg border border-slate-800/80">
                      {c.type === "markdown"
                        ? `_md = mo.md(${JSON.stringify(c.content)})\nreturn (_md,)`
                        : c.content}
                    </pre>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* C. SPLIT IDE VIEW */}
          {viewMode === "ide" && (
            <div className="flex-1 flex flex-col overflow-hidden">
              <div className="h-10 border-b border-slate-800 bg-slate-900/60 px-4 flex items-center justify-between shrink-0">
                <div className="flex items-center gap-2 text-xs text-slate-300 font-mono">
                  <FileCode className="h-3.5 w-3.5 text-purple-400" />
                  <span>main.py</span>
                </div>
                <button
                  onClick={() => setIdeCode(lab.starter_code || "")}
                  className="text-[11px] text-slate-400 hover:text-white flex items-center gap-1 cursor-pointer"
                >
                  <RotateCcw className="h-3 w-3" /> Reset Code
                </button>
              </div>

              <div className="flex-1 flex overflow-hidden">
                {/* Line Numbers + Textarea */}
                <div className="flex-1 flex font-mono text-xs bg-slate-950 p-4 overflow-y-auto">
                  <div className="pr-3 text-slate-600 select-none text-right">
                    {ideCode.split("\n").map((_, i) => (
                      <div key={i}>{i + 1}</div>
                    ))}
                  </div>
                  <textarea
                    value={ideCode}
                    onChange={(e) => setIdeCode(e.target.value)}
                    className="w-full h-full bg-transparent font-mono text-xs text-emerald-300 outline-none resize-none placeholder-slate-600 focus:ring-0 leading-relaxed"
                    placeholder="# Write your technical solution here..."
                    spellCheck={false}
                  />
                </div>
              </div>
            </div>
          )}

          {/* 3. BOTTOM JUPYTER SANDBOX PANEL (Terminal / Test Runner / Variables) */}
          <div className="h-56 border-t border-slate-800 bg-slate-900/95 flex flex-col shrink-0">
            {/* Panel Tabs */}
            <div className="h-9 border-b border-slate-800 px-4 flex items-center justify-between shrink-0 bg-slate-900">
              <div className="flex items-center gap-1">
                <button
                  onClick={() => setActiveBottomTab("terminal")}
                  className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-t transition-colors cursor-pointer ${
                    activeBottomTab === "terminal"
                      ? "text-white border-b-2 border-amber-500 bg-slate-800/80"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  <Terminal className="h-3.5 w-3.5 text-amber-400" />
                  <span>Sandbox Terminal</span>
                </button>

                <button
                  onClick={() => setActiveBottomTab("tests")}
                  className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-t transition-colors cursor-pointer ${
                    activeBottomTab === "tests"
                      ? "text-white border-b-2 border-emerald-500 bg-slate-800/80"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  <ShieldCheck className="h-3.5 w-3.5 text-emerald-400" />
                  <span>Test Cases &amp; Verification</span>
                  {testResult && (
                    <span
                      className={`ml-1 text-[10px] px-1.5 py-0.2 rounded font-mono ${
                        testResult.all_passed
                          ? "bg-emerald-500/20 text-emerald-400"
                          : "bg-rose-500/20 text-rose-400"
                      }`}
                    >
                      {testResult.passed_tests_count}/{testResult.total_tests_count}
                    </span>
                  )}
                </button>

                <button
                  onClick={() => setActiveBottomTab("variables")}
                  className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-t transition-colors cursor-pointer ${
                    activeBottomTab === "variables"
                      ? "text-white border-b-2 border-blue-500 bg-slate-800/80"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  <Layers className="h-3.5 w-3.5 text-blue-400" />
                  <span>Variable State Inspector</span>
                </button>
              </div>

              <div className="flex items-center gap-2 text-[11px] text-slate-500 font-mono">
                <span>Memory Cap: 128MB</span>
                <span>•</span>
                <span>Timeout: 5s</span>
              </div>
            </div>

            {/* Panel Tab Content */}
            <div className="flex-1 overflow-y-auto p-3 text-xs font-mono bg-slate-950">
              {/* Tab 1: Terminal */}
              {activeBottomTab === "terminal" && (
                <div className="space-y-1">
                  {terminalLogs.length === 0 ? (
                    <p className="text-slate-600">Sandbox terminal ready. Run a cell or submit lab.</p>
                  ) : (
                    terminalLogs.map((log, idx) => (
                      <div key={idx} className="flex items-start gap-2 leading-relaxed">
                        <span className="text-slate-600 select-none">[{log.timestamp}]</span>
                        <span
                          className={
                            log.type === "info"
                              ? "text-cyan-400"
                              : log.type === "success"
                              ? "text-emerald-400 font-semibold"
                              : log.type === "stderr" || log.type === "error"
                              ? "text-rose-400"
                              : "text-slate-300"
                          }
                        >
                          {log.text}
                        </span>
                      </div>
                    ))
                  )}
                </div>
              )}

              {/* Tab 2: Test Cases */}
              {activeBottomTab === "tests" && (
                <div className="space-y-3">
                  {!testResult ? (
                    <div className="p-4 text-center text-slate-500 space-y-2">
                      <p>No test results yet. Click &quot;Submit Lab&quot; to evaluate your code.</p>
                      <Button
                        size="sm"
                        onClick={handleSubmitLab}
                        disabled={isExecutingStudent}
                        className="bg-emerald-700 hover:bg-emerald-600 text-white text-xs cursor-pointer"
                      >
                        Run Test Suite
                      </Button>
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <div className="flex items-center justify-between p-2 bg-slate-900 rounded border border-slate-800">
                        <span className="font-bold text-white">
                          Status: {testResult.all_passed ? "PASS (All tests met)" : "FAIL (Assertions unresolved)"}
                        </span>
                        <span className="text-slate-400">
                          {testResult.passed_tests_count} of {testResult.total_tests_count} Passed ({testResult.execution_time_ms}ms)
                        </span>
                      </div>

                      <div className="space-y-1.5">
                        {testResult.test_results.map((tr, i) => (
                          <div
                            key={i}
                            className={`p-2.5 rounded-lg border flex items-start justify-between ${
                              tr.passed
                                ? "bg-emerald-950/30 border-emerald-900/50 text-emerald-300"
                                : "bg-rose-950/30 border-rose-900/50 text-rose-300"
                            }`}
                          >
                            <div className="flex items-center gap-2">
                              {tr.passed ? (
                                <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" />
                              ) : (
                                <XCircle className="h-4 w-4 text-rose-400 shrink-0" />
                              )}
                              <div>
                                <p className="font-bold text-slate-200">{tr.name}</p>
                                {tr.error && (
                                  <p className="text-rose-400 text-[11px] mt-0.5">{tr.error}</p>
                                )}
                              </div>
                            </div>
                            <span className="text-[10px] text-slate-500 font-mono">
                              {tr.duration_ms}ms
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Tab 3: Variables Inspector */}
              {activeBottomTab === "variables" && (
                <div className="space-y-2">
                  <div className="grid grid-cols-3 gap-2 pb-1 border-b border-slate-800 text-[10px] text-slate-500 uppercase font-bold">
                    <span>Variable</span>
                    <span>Type</span>
                    <span>Value / Scope</span>
                  </div>
                  <div className="space-y-1 text-slate-300">
                    <div className="grid grid-cols-3 gap-2 py-1 border-b border-slate-900">
                      <span className="text-emerald-400">marimo_app</span>
                      <span className="text-slate-500">marimo.App</span>
                      <span className="text-slate-400">&lt;App width=&quot;medium&quot;&gt;</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2 py-1 border-b border-slate-900">
                      <span className="text-emerald-400">sample_threshold</span>
                      <span className="text-slate-500">int</span>
                      <span className="text-slate-400">{marimoSliderValue}</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2 py-1 border-b border-slate-900">
                      <span className="text-emerald-400">strata_mode</span>
                      <span className="text-slate-500">str</span>
                      <span className="text-slate-400">&quot;{marimoCategoryFilter}&quot;</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
