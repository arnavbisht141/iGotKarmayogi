import { PlayCircle } from "lucide-react";
import { getYouTubeEmbedUrl } from "@/lib/video";

export function LessonVideo({ title, videoUrl }: { title: string; videoUrl?: string | null }) {
  const embedUrl = getYouTubeEmbedUrl(videoUrl);

  if (embedUrl) {
    return (
      <div className="aspect-video w-full overflow-hidden rounded-2xl bg-slate-950 shadow-md">
        <iframe
          src={embedUrl}
          title={title}
          className="size-full"
          allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowFullScreen
          referrerPolicy="strict-origin-when-cross-origin"
          loading="lazy"
        />
      </div>
    );
  }

  if (videoUrl) {
    return (
      <div className="aspect-video w-full overflow-hidden rounded-2xl bg-slate-950 shadow-md">
        <video src={videoUrl} controls className="size-full" aria-label={title} />
      </div>
    );
  }

  return (
    <div className="flex aspect-video w-full flex-col items-center justify-center gap-3 rounded-2xl bg-slate-900 p-6 text-center text-white shadow-md">
      <PlayCircle className="size-12 text-slate-400" aria-hidden="true" />
      <h4 className="text-base font-semibold text-balance">{title}</h4>
      <p className="text-sm text-pretty text-slate-400">
        Video for this lesson is not available yet. Continue with the reading material below.
      </p>
    </div>
  );
}
