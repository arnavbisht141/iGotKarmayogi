"""Supabase Digital Governance Knowledge Base Reader (Strictly Read-Only GET).

Queries scraped Wikipedia articles, YouTube curricula, and governance taxonomy
stored in the live Supabase instance (field: 'Digital Governance').
Enforces 100% read-only GET requests — zero write or update operations.
"""

import json
import logging
import os
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from app.core.config import settings

logger = logging.getLogger("digital_governance.supabase")

SUPABASE_URL = getattr(settings, "SUPABASE_URL", "") or os.getenv("SUPABASE_URL", "https://tdcrpjlpvkqjptvsndnp.supabase.co")
SUPABASE_KEY = getattr(settings, "SUPABASE_KEY", "") or os.getenv("SUPABASE_KEY", os.getenv("SUPABASE_ANON_KEY", ""))
DIGITAL_GOVERNANCE_FIELD_ID = "49beefed-c5d8-4032-9802-e69b2d0e559c"


class SupabaseKnowledgeService:
    """Read-only client for retrieving Digital Governance curriculum & articles from Supabase."""

    def __init__(self):
        self._cached_topics: Optional[List[Dict[str, Any]]] = None
        self._cached_articles: Dict[str, Dict[str, Any]] = {}

    def _get_headers(self) -> Dict[str, str]:
        return {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Accept": "application/json",
        }

    def _fetch_json(self, endpoint: str) -> Any:
        """Executes a strictly read-only HTTP GET request against Supabase REST API."""
        url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
        req = urllib.request.Request(url, headers=self._get_headers(), method="GET")
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            logger.warning(f"Failed to fetch read-only data from Supabase endpoint '{endpoint}': {e}")
            return None
        return None

    def get_digital_governance_topics(self) -> List[Dict[str, Any]]:
        """
        Retrieves the 5 official Digital Governance topics:
        1. Cybersecurity
        2. Data Privacy
        3. Digital Signatures
        4. Government Cloud
        5. Digital Public Infrastructure
        """
        if self._cached_topics:
            return self._cached_topics

        data = self._fetch_json(f"topics?field_id=eq.{DIGITAL_GOVERNANCE_FIELD_ID}&select=*&order=name.asc")
        if data and isinstance(data, list):
            self._cached_topics = data
            return data

        # Fallback offline taxonomy
        fallback = [
            {"id": "5ee9a783-566b-4e02-b1a6-87b2e10ae890", "name": "Cybersecurity", "slug": "cybersecurity"},
            {"id": "340a68c4-11db-4225-a52e-2d1f16b27931", "name": "Data Privacy", "slug": "data-privacy"},
            {"id": "f6488ee3-13bd-4bfc-9e64-42778297dd51", "name": "Digital Signatures", "slug": "digital-signatures"},
            {"id": "80d5c4bd-c1df-45be-bd01-99b8db920de9", "name": "Government Cloud", "slug": "government-cloud"},
            {"id": "95f58ac5-a3c9-4226-81c3-d4283216766d", "name": "Digital Public Infrastructure", "slug": "digital-public-infrastructure"},
        ]
        self._cached_topics = fallback
        return fallback

    def get_resources_by_topic(self, topic_id: str) -> List[Dict[str, Any]]:
        """Retrieves resources (scraped Wikipedia articles, YouTube curricula) for a given topic."""
        data = self._fetch_json(f"resources?topic_id=eq.{topic_id}&select=id,type,title,url,body_text,description,provider&order=created_at.asc")
        if data and isinstance(data, list):
            return data
        return []

    def get_full_knowledge_base(self) -> List[Dict[str, Any]]:
        """Compiles an aggregated view of the 5 Digital Governance pillars with articles and curricula."""
        topics = self.get_digital_governance_topics()
        kb_summary: List[Dict[str, Any]] = []

        domain_template_map = {
            "Cybersecurity": "01-soc-auth-investigation",
            "Data Privacy": "04-vulnerable-web-app",
            "Digital Signatures": "06-pki-token-dispute",
            "Government Cloud": "07-meghraj-cloud-audit",
            "Digital Public Infrastructure": "08-dpi-apisetu-replay",
        }

        for t in topics:
            res_list = self.get_resources_by_topic(t["id"])
            article = next((r for r in res_list if r.get("type") == "article"), None)
            courses = [r for r in res_list if r.get("type") == "course"]

            body_snippet = ""
            article_title = ""
            if article:
                article_title = article.get("title", "")
                raw_body = article.get("body_text") or ""
                body_snippet = raw_body[:400].strip().replace("\n", " ") + "..."

            kb_summary.append({
                "topic_id": t["id"],
                "topic_name": t["name"],
                "recommended_template_id": domain_template_map.get(t["name"], "01-soc-auth-investigation"),
                "article_title": article_title,
                "article_url": article.get("url") if article else None,
                "body_snippet": body_snippet,
                "full_text": article.get("body_text") if article else "",
                "courses_count": len(courses),
                "courses": [{"title": c.get("title"), "url": c.get("url"), "provider": c.get("provider")} for c in courses[:3]],
            })

        return kb_summary


supabase_knowledge_service = SupabaseKnowledgeService()
