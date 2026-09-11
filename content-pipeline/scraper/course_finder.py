import json
import subprocess
import sys
from pathlib import Path

from common.config import BASE_DIR, load_fields


def search_courses(query: str, count: int = 3) -> list[dict]:
    result = subprocess.run(
        ["yt-dlp", "--dump-json", "--no-warnings", "--skip-download", f"ytsearch{count}:{query}"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    courses = []
    for line in result.stdout.strip().splitlines():
        if not line:
            continue
        data = json.loads(line)
        courses.append({
            "title": data.get("title", ""),
            "provider": "YouTube",
            "url": data.get("webpage_url", ""),
            "channel": data.get("channel") or data.get("uploader", ""),
            "thumbnail_url": data.get("thumbnail", ""),
            "duration": data.get("duration"),
        })
    return courses


def save_courses(field_slug: str, topic_slug: str, topic_name: str, force: bool = False) -> Path:
    out_dir = BASE_DIR / "content" / field_slug / topic_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "courses.json"

    if out_path.exists() and not force:
        return out_path

    courses = search_courses(f"{topic_name} course")
    out_path.write_text(json.dumps(courses, indent=2))
    return out_path


def main(force: bool = False, fields: list | None = None) -> None:
    for field in fields if fields is not None else load_fields():
        for topic in field.topics:
            try:
                path = save_courses(field.slug, topic.slug, topic.name, force=force)
                print(f"wrote {path}")
            except Exception as exc:
                print(f"skipped (error: {exc}): {field.slug}/{topic.slug}")


if __name__ == "__main__":
    main(force="--force" in sys.argv)
