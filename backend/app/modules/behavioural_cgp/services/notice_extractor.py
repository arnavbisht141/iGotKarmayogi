import re
from typing import Dict, Any, List
from ..schemas import GovernmentDocument

class NoticeExtractor:
    """
    Extracts administrative context, statutory citations, regulatory checkpoints,
    and decision dilemma nodes from official government notices, forms, and proceedings.
    """

    @staticmethod
    def extract_metadata(raw_text: str) -> Dict[str, Any]:
        """
        Parses raw administrative document text to extract citations, dates, and authorities.
        """
        # Extract Acts and Rules
        rule_patterns = [
            r"Rule\s+\d+(?:\([a-zA-Z0-9]+\))*",
            r"Section\s+\d+(?:\([a-zA-Z0-9]+\))*",
            r"CCS\s+\([^)]+\)\s+Rules(?:,\s+\d+)?",
            r"General Financial Rules(?:,\s+\d+)?|GFR\s+\d+",
            r"Right to Information Act(?:,\s+\d+)?|RTI\s+Act",
            r"Collection of Statistics Act(?:,\s+\d+)?"
        ]
        statutory_citations = set()
        for pat in rule_patterns:
            matches = re.findall(pat, raw_text, re.IGNORECASE)
            for m in matches:
                statutory_citations.add(m.strip())

        # Extract Department / Ministry references
        ministry_match = re.search(r"(?:MINISTRY|DEPARTMENT)\s+OF\s+([A-Z\s,&]+)", raw_text)
        issuing_authority = ministry_match.group(0).strip() if ministry_match else "Government of India Administrative Cadre"

        # Determine document type
        doc_type = "Government Notice"
        if "PROCEEDING" in raw_text.upper() or "APPEAL" in raw_text.upper():
            doc_type = "Departmental Proceeding"
        elif "FORM" in raw_text.upper() or "SCHEDULE" in raw_text.upper():
            doc_type = "Statutory Form"

        # Extract procedural milestones / timeline clauses (e.g., "15 days", "30 days")
        timelines = re.findall(r"\b\d+\s+(?:days|hours|weeks|months)\b", raw_text, re.IGNORECASE)

        return {
            "issuing_authority": issuing_authority,
            "document_type": doc_type,
            "statutory_citations": sorted(list(statutory_citations)) if statutory_citations else [
                "CCS (Conduct) Rules, 1964",
                "Principles of Natural Justice"
            ],
            "timelines_detected": list(set(timelines)),
            "summary_snippet": raw_text[:400].replace("\n", " ").strip() + "..."
        }
