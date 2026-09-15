import { Markdown } from "@/components/shared/Markdown";

export function LessonMarkdown({ content, title }: { content?: string | null; title?: string }) {
  // Lesson bodies often open with "# <lesson title>", which the player header already shows.
  if (title && content) {
    const [firstLine, ...rest] = content.trimStart().split("\n");
    if (firstLine.replace(/^#+\s*/, "").trim().toLowerCase() === title.trim().toLowerCase() && firstLine.startsWith("#")) {
      content = rest.join("\n");
    }
  }

  if (!content?.trim()) {
    return <p className="text-sm text-slate-500">No reading material for this lesson.</p>;
  }

  return (
    <Markdown
      content={content}
      className="prose prose-slate max-w-none prose-headings:text-balance prose-headings:font-semibold prose-h1:text-2xl prose-h2:text-xl prose-h3:text-lg prose-p:text-pretty prose-a:text-[#1E3A8A] prose-code:rounded prose-code:bg-slate-100 prose-code:px-1 prose-code:py-0.5 prose-code:before:content-none prose-code:after:content-none prose-pre:bg-slate-900 prose-table:text-sm"
    />
  );
}
