import logging
import random
import re
from typing import List, Optional, Set, Tuple

from app.agents.llm_utils import parse_llm_json

logger = logging.getLogger(__name__)

MAX_SOURCE_CHARS = 24000
CHUNK_CHARS = 6000
DIFFICULTIES = {"beginner", "intermediate", "advanced"}


def chunk_text(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text or "").strip()[:MAX_SOURCE_CHARS]
    return [text[i:i + CHUNK_CHARS] for i in range(0, len(text), CHUNK_CHARS)]


def _normalize(raw) -> Optional[dict]:
    if not isinstance(raw, dict):
        return None
    question = str(raw.get("question", "")).strip()
    options = raw.get("options")
    try:
        correct = int(raw.get("correct_index"))
    except (TypeError, ValueError):
        return None
    if not question or not isinstance(options, list) or len(options) != 4:
        return None
    options = [str(o).strip() for o in options]
    if any(not o for o in options) or len({o.lower() for o in options}) != 4 or not 0 <= correct < 4:
        return None
    # LLMs bias the correct answer toward early positions, so shuffle while tracking it.
    correct_text = options[correct]
    random.shuffle(options)
    return {
        "question": question,
        "options": options,
        "correct_index": options.index(correct_text),
        "explanation": str(raw.get("explanation", "")).strip() or f"The correct answer is: {correct_text}.",
        "concept": str(raw.get("concept", "")).strip()[:255] or None,
    }


def _llm_questions(llm, chunk: str, count: int, difficulty: str) -> List[dict]:
    prompt = f"""You are an assessment designer for capacity building in India's Official Statistical System (iGOT Karmayogi).
Create {count} {difficulty}-level multiple-choice questions strictly grounded in the SOURCE below.
Rules:
- exactly 4 options per question, exactly one unambiguously correct
- distractors must be plausible and reflect common misconceptions
- never use "all of the above" or "none of the above"
- test understanding and application, not trivia about page layout
- explanation: 1-2 sentences on why the answer is correct, grounded in the source
- concept: a 2-5 word topic label
Respond ONLY with a JSON array:
[{{"question": "...", "options": ["...", "...", "...", "..."], "correct_index": 0, "explanation": "...", "concept": "..."}}]

SOURCE:
{chunk}"""
    data = parse_llm_json(llm.invoke(prompt).content)
    if isinstance(data, dict):
        data = data.get("questions", [])
    return [q for q in (_normalize(item) for item in data) if q]


def _fallback_questions(text: str, count: int, seen: Set[str]) -> List[dict]:
    """Deterministic cloze questions used when no LLM is reachable."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if 8 <= len(s.split()) <= 40]
    vocabulary = sorted({w for w in re.findall(r"[A-Za-z][A-Za-z\-]{5,}", text)}, key=str.lower)
    questions = []
    for sentence in sentences:
        if len(questions) >= count:
            break
        candidates = [w for w in re.findall(r"[A-Za-z][A-Za-z\-]{5,}", sentence)]
        if not candidates:
            continue
        answer = max(candidates, key=len)
        distractors = [w for w in vocabulary if w.lower() != answer.lower()]
        if len(distractors) < 3:
            continue
        stem = sentence.replace(answer, "_____", 1)
        if stem.lower() in seen:
            continue
        seen.add(stem.lower())
        options = random.sample(distractors, 3) + [answer]
        random.shuffle(options)
        questions.append({
            "question": f"Fill in the blank: {stem}",
            "options": options,
            "correct_index": options.index(answer),
            "explanation": f"The source states: \"{sentence}\"",
            "concept": None,
        })
    return questions


def generate_quiz_questions(
    text: str, num_questions: int = 10, difficulty: str = "intermediate", llm_client=None
) -> Tuple[List[dict], str]:
    """Returns (questions, generator) where generator is "llm" or "fallback"."""
    chunks = chunk_text(text)
    if not chunks:
        raise ValueError("No readable text found in the uploaded material")

    if llm_client is None:
        from app.agents.recommendation.agent import get_llm_client
        llm_client = get_llm_client()

    questions: List[dict] = []
    seen: Set[str] = set()
    if llm_client is not None:
        per_chunk = max(2, -(-num_questions // len(chunks)))
        for chunk in chunks:
            if len(questions) >= num_questions:
                break
            try:
                batch = _llm_questions(llm_client, chunk, per_chunk, difficulty)
            except Exception as e:
                logger.warning("LLM quiz generation failed for a chunk: %s", e)
                continue
            for q in batch:
                key = q["question"].lower()
                if key not in seen:
                    seen.add(key)
                    questions.append(q)

    generator = "llm" if questions else "fallback"
    if len(questions) < num_questions:
        questions += _fallback_questions(" ".join(chunks), num_questions - len(questions), seen)
    return questions[:num_questions], generator
