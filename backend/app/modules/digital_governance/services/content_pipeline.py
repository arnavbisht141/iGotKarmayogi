"""Content Generation Pipeline: Video/Lecture Transcripts -> Procedural Cyber Sandbox Packages.

Orchestrates:
1. Transcript Ingestion -> Multi-LLM Round-Robin Extraction of Objectives & Tags
2. Tag-based Template Matching against Template Registry
3. Multi-LLM Slot Filling & Seed-based Anti-Cheat Randomization
4. Artifact Synthesis (JSON telemetry, MIME EML, PCAPs) & Dynamic Marimo Notebook Generation
5. CTFd & LMS Synchronization
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

from app.modules.digital_governance.services.llm_provider import llm_provider
from app.modules.digital_governance.services.templates import (
    TEMPLATE_REGISTRY,
    get_template,
    match_template_by_metadata,
    BaseChallengeTemplate,
)

logger = logging.getLogger("digital_governance.pipeline")


EXTRACTION_SYSTEM_PROMPT = """You are an expert cybersecurity curriculum architect for the Government of India (NeGD & CERT-In).
Analyze the lecture or walkthrough transcript and extract structured learning objectives mapped to Indian cyber defense regulations (IT Act 2000 Section 70B, DPDP Act 2023, MeitY MeghRaj, and API Setu).

Return strictly valid JSON with this schema:
{
  "domain": "Cybersecurity | Data Privacy | Digital Signatures | Government Cloud / MeghRaj | Digital Public Infrastructure (DPI)",
  "objectives": ["Objective 1 starting with action verb", "Objective 2", "Objective 3"],
  "mitre_techniques": ["T1110.001", "T1078.002"],
  "tags": ["soc", "brute-force", "event-4625", "cert-in"],
  "difficulty": "Beginner | Intermediate | Advanced",
  "summary": "Brief 1-sentence synopsis of the incident scenario"
}
"""


class ContentGenerationPipeline:
    """End-to-end pipeline generating reproducible, randomized CTF challenge sandboxes."""

    @classmethod
    async def extract_objectives_and_tags(cls, transcript_text: str) -> Dict[str, Any]:
        """Extract domain, learning objectives, tags, and MITRE techniques using multi-LLM rotation."""
        user_prompt = f"Transcript Content:\n{transcript_text[:4500]}\n\nExtract the JSON analysis:"
        llm_res = await llm_provider.generate(
            prompt=user_prompt,
            system_prompt=EXTRACTION_SYSTEM_PROMPT,
            json_mode=True,
        )

        if not llm_res.get("is_fallback") and llm_res.get("text"):
            parsed = llm_provider.parse_json_safely(llm_res["text"])
            if parsed and "domain" in parsed and "objectives" in parsed:
                parsed["provider_used"] = llm_res["provider"]
                parsed["model_used"] = llm_res["model"]
                return parsed

        # Robust Heuristic Fallback Engine for offline / zero-token resilience
        return cls._heuristic_extraction(transcript_text)

    @classmethod
    def _heuristic_extraction(cls, text: str) -> Dict[str, Any]:
        t_low = text.lower()

        # 1. Phishing / DFIR
        if any(w in t_low for w in ["phish", "phishing", "email", "eml", "dmarc", "spf", "invoice", "macro"]):
            return {
                "domain": "Cybersecurity",
                "objectives": [
                    "Evaluate RFC 822 email headers and detect DMARC/SPF spoofing indicators",
                    "Carve and compute SHA-256 fingerprint of malicious financial invoice payload",
                    "Correlate DNS telemetry and resolve external C2 beacon callbacks",
                ],
                "mitre_techniques": ["T1566.001", "T1204.002", "T1071.001"],
                "tags": ["phishing", "dfir", "email", "dmarc", "spf", "dns", "cert-in"],
                "difficulty": "Intermediate",
                "summary": "Spearphishing campaign delivering spoofed financial disbursement vouchers with C2 callbacks.",
                "provider_used": "heuristic_engine",
                "model_used": "rule-based-civil-defense",
            }

        # 2. Sovereign Cloud / MeghRaj
        if any(w in t_low for w in ["cloud", "meghraj", "gi-cloud", "stqc", "sovereignty", "localization", "s3"]):
            return {
                "domain": "Government Cloud / MeghRaj",
                "objectives": [
                    "Inspect state cloud audit telemetry in cloud_audit_events.json for cross-border egress",
                    "Identify unauthorized non-empaneled foreign cloud deployments violating MeitY mandates",
                    "Validate STQC compliance parameters and enforce domestic data localization",
                ],
                "mitre_techniques": ["T1530", "T1048", "T1078.004"],
                "tags": ["cloud", "meghraj", "gi-cloud", "stqc", "data-localization", "sovereignty"],
                "difficulty": "Intermediate",
                "summary": "Unapproved cross-border cloud migration violating MeitY sovereign data localization rules.",
                "provider_used": "heuristic_engine",
                "model_used": "rule-based-civil-defense",
            }

        # 3. DPI / API Setu
        if any(w in t_low for w in ["dpi", "apisetu", "api setu", "aadhaar", "replay", "nonce", "india stack"]):
            return {
                "domain": "Digital Public Infrastructure (DPI)",
                "objectives": [
                    "Detect high-frequency duplicate nonce replay attacks on public API Setu e-KYC endpoints",
                    "Trace distributed botnet subnet traffic and rate-limit violations",
                    "Recover WAF cryptographic mitigation tokens and verify service integrity",
                ],
                "mitre_techniques": ["T1557", "T1071.001", "T1499"],
                "tags": ["dpi", "india-stack", "aadhaar", "api-setu", "replay-attack", "nonce"],
                "difficulty": "Advanced",
                "summary": "High-volume replay attack against citizen e-KYC gateway violating cryptographic nonce integrity.",
                "provider_used": "heuristic_engine",
                "model_used": "rule-based-civil-defense",
            }

        # 4. Default: SOC Authentication & Brute Force Triage
        return {
            "domain": "Cybersecurity",
            "objectives": [
                "Isolate external brute-force credential stuffing spikes in Windows Security Event 4625 logs",
                "Identify privileged accounts compromised during off-hours on critical state infrastructure",
                "Analyze subsequent Living-off-the-Land (LOLBin) process creation commands (Event 4688)",
            ],
            "mitre_techniques": ["T1110.001", "T1078.002", "T1105"],
            "tags": ["soc", "authentication", "brute-force", "event-4625", "lolbin", "certutil", "cert-in"],
            "difficulty": "Beginner",
            "summary": "Coordinated off-hours brute force assault on state treasury gateway and subsequent LOLBin staging.",
            "provider_used": "heuristic_engine",
            "model_used": "rule-based-civil-defense",
        }

    @classmethod
    def match_template(cls, extracted_meta: Dict[str, Any]) -> BaseChallengeTemplate:
        """Selects the challenge template best suited for the extracted objectives and tags."""
        domain = extracted_meta.get("domain", "")
        tags = extracted_meta.get("tags", [])
        return match_template_by_metadata(domain=domain, tags=tags)

    @classmethod
    async def fill_template_slots(
        cls,
        template: BaseChallengeTemplate,
        extracted_meta: Dict[str, Any],
        student_seed: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Fills template parameter slots combining procedural randomization and LLM styling."""
        # 1. Base procedural slots with student seed
        slots = template.generate_random_slots(seed=student_seed)

        # 2. Attempt LLM enhancement for civil-service realism
        prompt = f"""Given the following incident summary:
"{extracted_meta.get('summary', '')}"
Suggest an authentic Indian government incident codename (e.g. 'Operation Vajra-7', 'Operation Raksha-3')
and a state departmental server name (e.g. 'TREASURY-PAY-01', 'REVENUE-DB-02').
Return JSON: {{"incident_codename": "string", "target_host": "string"}}"""

        llm_res = await llm_provider.generate(prompt=prompt, json_mode=True)
        if not llm_res.get("is_fallback") and llm_res.get("text"):
            parsed = llm_provider.parse_json_safely(llm_res["text"])
            if parsed:
                if "incident_codename" in parsed and parsed["incident_codename"]:
                    slots["incident_codename"] = parsed["incident_codename"]
                if "target_host" in parsed and parsed["target_host"] and "target_host" in slots:
                    slots["target_host"] = parsed["target_host"]

        return slots

    @classmethod
    async def generate_challenge_package(
        cls,
        transcript_text: str,
        output_dir: Path,
        student_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Executes full generation pipeline:
        Transcript -> Extracted Tags -> Matched Template -> Filled Slots -> Artifact Synthesis -> Package
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        # 1. Extraction
        extracted_meta = await cls.extract_objectives_and_tags(transcript_text)

        # 2. Matching
        template = cls.match_template(extracted_meta)

        # 3. Slot Filling
        slots = await cls.fill_template_slots(template, extracted_meta, student_seed=student_id)

        # 4. Package Building
        pkg = template.build_challenge_package(slots, output_dir)
        manifest = pkg["manifest"]

        return {
            "challenge_id": pkg["id"],
            "title": manifest["title"],
            "category": manifest["category"],
            "difficulty": manifest["difficulty"],
            "points": manifest["points"],
            "flag": manifest["flag"],
            "hints": manifest["hints"],
            "objectives": manifest["objectives"],
            "scenario_md": manifest["scenario_md"],
            "package_path": str(pkg["directory"]),
            "extracted_meta": extracted_meta,
            "slots": slots,
        }


content_pipeline = ContentGenerationPipeline()
