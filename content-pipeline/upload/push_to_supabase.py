import json
import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client

from common.config import BASE_DIR, load_fields

load_dotenv(BASE_DIR / ".env")


def get_client() -> Client:
    return create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SECRET_KEY"])


def parse_article(path: Path) -> dict:
    lines = path.read_text().splitlines()
    title = lines[0].removeprefix("Title: ").strip()
    source_url = lines[1].removeprefix("Source: ").strip()
    body = "\n".join(lines[3:]).strip()
    return {"title": title, "url": source_url, "body_text": body}


def upsert_field(client, slug: str, name: str) -> str:
    res = client.table("fields").upsert({"slug": slug, "name": name}, on_conflict="slug").execute()
    return res.data[0]["id"]


def upsert_topic(client, field_id: str, slug: str, name: str) -> str:
    res = client.table("topics").upsert(
        {"field_id": field_id, "slug": slug, "name": name}, on_conflict="field_id,slug"
    ).execute()
    return res.data[0]["id"]


def upsert_resource(client, topic_id: str, resource: dict) -> None:
    client.table("resources").upsert(
        {"topic_id": topic_id, **resource}, on_conflict="topic_id,url"
    ).execute()


def push_topic_content(client, topic_id: str, field_slug: str, topic_slug: str) -> None:
    topic_dir = BASE_DIR / "content" / field_slug / topic_slug

    articles_dir = topic_dir / "articles"
    if articles_dir.exists():
        for article_path in articles_dir.glob("*.md"):
            article = parse_article(article_path)
            upsert_resource(client, topic_id, {
                "type": "article",
                "title": article["title"],
                "url": article["url"],
                "body_text": article["body_text"],
                "provider": None,
                "thumbnail_url": None,
                "description": None,
            })

    courses_path = topic_dir / "courses.json"
    if courses_path.exists():
        for course in json.loads(courses_path.read_text()):
            if not course.get("url"):
                continue
            upsert_resource(client, topic_id, {
                "type": "course",
                "title": course["title"],
                "url": course["url"],
                "provider": course.get("provider"),
                "thumbnail_url": course.get("thumbnail_url"),
                "body_text": None,
                "description": course.get("channel"),
            })


def main() -> None:
    client = get_client()
    for field in load_fields():
        field_id = upsert_field(client, field.slug, field.name)
        for topic in field.topics:
            topic_id = upsert_topic(client, field_id, topic.slug, topic.name)
            try:
                push_topic_content(client, topic_id, field.slug, topic.slug)
                print(f"pushed {field.slug}/{topic.slug}")
            except Exception as exc:
                print(f"skipped (error: {exc}): {field.slug}/{topic.slug}")


if __name__ == "__main__":
    main()
