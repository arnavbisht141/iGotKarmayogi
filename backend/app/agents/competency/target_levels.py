"""
Default designation-tier -> target competency level framework.

This is a DRAFTED DEFAULT, not a validated competency framework. It exists so
gap analysis has something to compare against on day one. It applies the same
target level across all 4 domains for a given tier (no per-domain weighting
yet), keyed by keyword matching on the officer's designation/job_role free text.
Replace with a real, validated per-role-per-domain dataset when one is
available; callers only need resolve_target_level() to keep working.
"""
from typing import Optional

TARGET_LEVEL_BY_TIER = {
    "senior": 4.0,
    "middle": 3.0,
    "junior": 2.0,
    "default": 2.5,
}

# Checked in this order. Multi-word titles come first because they contain shorter
# keywords from other tiers ("deputy director general" contains "deputy director",
# "assistant director" contains "director").
TIER_KEYWORDS = [
    ("senior", ["director general", "additional secretary", "joint secretary"]),
    ("middle", ["deputy director", "assistant director", "under secretary", "section officer",
                "officer in charge", "superintendent", "senior statistical officer"]),
    ("junior", ["junior", "assistant", "trainee", "probationer", "statistical investigator"]),
    ("senior", ["director", "secretary", "commissioner", "chief", "head of department"]),
]


def resolve_tier(designation: Optional[str], job_role: Optional[str]) -> str:
    text = " ".join(filter(None, [designation, job_role])).lower()
    if not text.strip():
        return "default"
    for tier, keywords in TIER_KEYWORDS:
        if any(k in text for k in keywords):
            return tier
    return "default"


def resolve_target_level(designation: Optional[str], job_role: Optional[str]) -> float:
    return TARGET_LEVEL_BY_TIER[resolve_tier(designation, job_role)]
