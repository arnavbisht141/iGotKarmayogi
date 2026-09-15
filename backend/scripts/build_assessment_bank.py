"""Build the final-assessment question bank from course content.

Final assessments used to reuse the in-lesson practice questions word for word, so learners
had seen every exam answer before sitting it. This script asks the LLM for a separate set of
questions per course, grounded in that course's lessons, and writes them to
app/core/assessment_bank.json. The demo seed loads that file (apply_assessment_bank).

Usage (from backend/):
    python scripts/build_assessment_bank.py                 # courses missing from the bank
    python scripts/build_assessment_bank.py --refresh       # regenerate every course
    python scripts/build_assessment_bank.py --course "R for Survey Data Analysis"
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import selectinload  # noqa: E402

from app.agents.quiz.generator import _llm_questions  # noqa: E402
from app.agents.recommendation.agent import get_llm_client  # noqa: E402
from app.core.database import SessionLocal  # noqa: E402
from app.core.seed_demo import ASSESSMENT_BANK_PATH, assessment_question_target  # noqa: E402
from app.models.models import Course, Module  # noqa: E402

MAX_ROUNDS = 4


def _key(text: str) -> str:
    return " ".join(text.lower().split())


def learner_facing(text: str) -> str:
    """The generator is told to cite "the source"; learners should read plain explanations."""
    text = re.sub(
        r"\s*,?\s*\b(?:as (?:described|stated|noted|explained|mentioned|defined) in|according to|as per|per) the source\b",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"\bThe source (?:states|explains|notes|says|indicates|instructs|specifies|mentions) that\s+(\w)",
        lambda m: m.group(1).upper(),
        text,
    )
    return re.sub(r"\b([Tt]he) source\b", r"\1 course material", text)


def course_source(course: Course) -> str:
    parts = [f"COURSE: {course.title}", course.overview or ""]
    for module in course.modules:
        parts.append(f"\n## {module.title}\n{module.description or ''}")
        for lesson in module.lessons:
            parts.append(f"\n### {lesson.title}\n{lesson.content or ''}")
    return "\n".join(parts)


def build_for_course(llm, course: Course) -> list:
    lessons = [l for m in course.modules for l in m.lessons]
    target = assessment_question_target(len(lessons))
    # Practice questions stay practice: the exam must not repeat them.
    seen = {_key(l.activity_question) for l in lessons if l.activity_question}
    source = course_source(course)
    questions = []
    for _ in range(MAX_ROUNDS):
        need = target - len(questions)
        if need <= 0:
            break
        try:
            batch = _llm_questions(llm, source, need + 3, "intermediate")
        except Exception as exc:  # network or parse failure: try another round
            print(f"  round failed: {exc}")
            continue
        for q in batch:
            if _key(q["question"]) in seen:
                continue
            seen.add(_key(q["question"]))
            questions.append({k: q[k] for k in ("question", "options", "correct_index", "explanation")})
    return questions[:target]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--refresh", action="store_true", help="regenerate courses already in the bank")
    parser.add_argument("--course", help="only build this course title")
    args = parser.parse_args()

    llm = get_llm_client()
    if llm is None:
        sys.exit("No LLM key configured (GROQ_API_KEY, OPENAI_API_KEY or GOOGLE_API_KEY).")

    bank = json.loads(ASSESSMENT_BANK_PATH.read_text()) if ASSESSMENT_BANK_PATH.exists() else {}
    db = SessionLocal()
    try:
        courses = (
            db.query(Course)
            .options(selectinload(Course.modules).selectinload(Module.lessons))
            .order_by(Course.id)
            .all()
        )
        for course in courses:
            if args.course and course.title != args.course:
                continue
            if course.title in bank and not args.refresh and not args.course:
                continue
            if not any(m.lessons for m in course.modules):
                continue
            lessons = [l for m in course.modules for l in m.lessons]
            practice = {_key(l.activity_question) for l in lessons if l.activity_question}
            existing = course.assessment.questions if course.assessment else []
            if (
                not args.course
                and len(existing) >= assessment_question_target(len(lessons))
                and not any(_key(q.text) in practice for q in existing)
            ):
                print(f"{course.title}: keeps its {len(existing)} authored questions")
                continue
            questions = build_for_course(llm, course)
            print(f"{course.title}: {len(questions)} questions")
            if questions:
                bank[course.title] = questions
                ASSESSMENT_BANK_PATH.write_text(json.dumps(bank, indent=2, ensure_ascii=False) + "\n")
    finally:
        db.close()

    for questions in bank.values():
        for q in questions:
            q["question"] = learner_facing(q["question"])
            q["explanation"] = learner_facing(q["explanation"])
    ASSESSMENT_BANK_PATH.write_text(json.dumps(bank, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
