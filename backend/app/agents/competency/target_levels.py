"""
Default designation-tier -> target competency level framework.

This is a DRAFTED DEFAULT, not a validated competency framework. It exists so
gap analysis has something to compare against on day one. It applies the same
target level across all 4 domains for a given tier (no per-domain weighting
yet), keyed by simple keyword matching on the officer's designation/job_role
free text. Replace with a real, validated per-role-per-domain dataset when
one is available; callers only need resolve_target_level() to keep working
with the same signature.
"""
from typing import Optional

TARGET_LEVEL_BY_TIER = {
    "senior": 4.0,
    "middle": 3.0,
    "junior": 2.0,
    "default": 2.5,
}

SENIOR_KEYWORDS = ["director", "secretary", "commissioner", "chief", "head of department"]
MIDDLE_KEYWORDS = ["officer in charge", "section officer", "deputy director", "under secretary", "superintendent"]
JUNIOR_KEYWORDS = ["junior", "assistant", "trainee", "probationer"]


def resolve_target_level(designation: Optional[str], job_role: Optional[str]) -> float:
    text = " ".join(filter(None, [designation, job_role])).lower()
    if not text.strip():
        return TARGET_LEVEL_BY_TIER["default"]

    if any(k in text for k in JUNIOR_KEYWORDS):
        return TARGET_LEVEL_BY_TIER["junior"]
    if any(k in text for k in MIDDLE_KEYWORDS):
        return TARGET_LEVEL_BY_TIER["middle"]
    if any(k in text for k in SENIOR_KEYWORDS):
        return TARGET_LEVEL_BY_TIER["senior"]
    return TARGET_LEVEL_BY_TIER["default"]
