from dataclasses import dataclass
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass
class Topic:
    slug: str
    name: str


@dataclass
class Field:
    slug: str
    name: str
    topics: list[Topic]


def load_fields(path: str | None = None) -> list[Field]:
    config_path = Path(path) if path else BASE_DIR / "config" / "topics.yaml"
    data = yaml.safe_load(config_path.read_text())
    return [
        Field(
            slug=f["slug"],
            name=f["name"],
            topics=[Topic(slug=t["slug"], name=t["name"]) for t in f["topics"]],
        )
        for f in data["fields"]
    ]
