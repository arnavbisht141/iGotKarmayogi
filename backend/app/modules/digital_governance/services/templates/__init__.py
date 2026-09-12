"""Registry and lookup utilities for procedural cybersecurity challenge templates."""

from typing import Dict, List, Optional
from app.modules.digital_governance.services.templates.base_template import BaseChallengeTemplate
from app.modules.digital_governance.services.templates.soc_auth_template import SocAuthTemplate
from app.modules.digital_governance.services.templates.phishing_dfir_template import PhishingDfirTemplate
from app.modules.digital_governance.services.templates.linux_forensics_template import LinuxForensicsTemplate
from app.modules.digital_governance.services.templates.web_sqli_template import WebSqliTemplate
from app.modules.digital_governance.services.templates.threat_hunting_lotl_template import ThreatHuntingLotlTemplate
from app.modules.digital_governance.services.templates.pki_defense_template import PkiDefenseTemplate
from app.modules.digital_governance.services.templates.cloud_audit_template import CloudAuditTemplate
from app.modules.digital_governance.services.templates.dpi_replay_template import DpiReplayTemplate

_TEMPLATES: List[BaseChallengeTemplate] = [
    SocAuthTemplate(),
    PhishingDfirTemplate(),
    LinuxForensicsTemplate(),
    WebSqliTemplate(),
    ThreatHuntingLotlTemplate(),
    PkiDefenseTemplate(),
    CloudAuditTemplate(),
    DpiReplayTemplate(),
]

TEMPLATE_REGISTRY: Dict[str, BaseChallengeTemplate] = {
    tmpl.template_id: tmpl for tmpl in _TEMPLATES
}
# Canonical numeric and semantic aliases
if "soc-auth-investigation" in TEMPLATE_REGISTRY:
    TEMPLATE_REGISTRY["01-soc-auth-investigation"] = TEMPLATE_REGISTRY["soc-auth-investigation"]
if "phishing-dfir" in TEMPLATE_REGISTRY:
    TEMPLATE_REGISTRY["02-phishing-dfir"] = TEMPLATE_REGISTRY["phishing-dfir"]
if "cloud-meghraj-audit" in TEMPLATE_REGISTRY:
    TEMPLATE_REGISTRY["07-meghraj-cloud-audit"] = TEMPLATE_REGISTRY["cloud-meghraj-audit"]
if "dpi-apisetu-replay" in TEMPLATE_REGISTRY:
    TEMPLATE_REGISTRY["08-dpi-apisetu-replay"] = TEMPLATE_REGISTRY["dpi-apisetu-replay"]



def get_template(template_id: str) -> BaseChallengeTemplate:
    """Retrieve template by unique template_id. Defaults to Flagship SOC Auth if not found."""
    if template_id in TEMPLATE_REGISTRY:
        return TEMPLATE_REGISTRY[template_id]
    for k, v in TEMPLATE_REGISTRY.items():
        if k in template_id or template_id in k:
            return v
    return TEMPLATE_REGISTRY["01-soc-auth-investigation"]


def list_templates() -> List[BaseChallengeTemplate]:
    """List all registered challenge templates."""
    return list(_TEMPLATES)


def match_template_by_metadata(
    domain: str = "",
    tags: Optional[List[str]] = None,
    keywords: Optional[List[str]] = None,
) -> BaseChallengeTemplate:
    """
    Intelligently select the best matching template based on extracted tags,
    domain, and keywords matching the 5 Supabase Digital Governance domains.
    """
    domain_lower = domain.lower()
    all_tokens = set()
    if tags:
        all_tokens.update(t.lower() for t in tags)
    if keywords:
        all_tokens.update(k.lower() for k in keywords)

    # 1. Phishing / DFIR indicators
    if any(k in all_tokens for k in ["phish", "phishing", "email", "eml", "dmarc", "spf", "invoice"]) or "dfir" in domain_lower:
        return TEMPLATE_REGISTRY["02-phishing-dfir"]

    # 2. Linux Server & Persistence indicators
    if any(k in all_tokens for k in ["linux", "cron", "crontab", "sudo", "sudoers", "ssh", "bash_history"]):
        return TEMPLATE_REGISTRY["03-compromised-linux-server"]

    # 3. Web SQLi & Data Privacy indicators
    if any(k in all_tokens for k in ["web", "sqli", "sql", "union", "dpdp", "data-privacy", "citizen"]) or "privacy" in domain_lower:
        return TEMPLATE_REGISTRY["04-vulnerable-web-app"]

    # 4. Threat Hunting & Living off the Land
    if any(k in all_tokens for k in ["lotl", "threat-hunting", "sysmon", "entropy", "dns-tunneling"]):
        return TEMPLATE_REGISTRY["05-threat-hunting-lotl"]

    # 5. Digital Signatures & PKI
    if any(k in all_tokens for k in ["pki", "digital-signature", "dsc", "ocsp", "crl", "gem", "cca"]) or "signature" in domain_lower:
        return TEMPLATE_REGISTRY["06-pki-token-dispute"]

    # 6. Government Cloud / MeghRaj
    if any(k in all_tokens for k in ["cloud", "meghraj", "gi-cloud", "stqc", "sovereignty", "localization"]) or "cloud" in domain_lower:
        return TEMPLATE_REGISTRY["cloud-meghraj-audit"]

    # 7. Digital Public Infrastructure / API Setu
    if any(k in all_tokens for k in ["dpi", "apisetu", "api-setu", "aadhaar", "replay", "nonce", "india-stack"]) or "dpi" in domain_lower:
        return TEMPLATE_REGISTRY["dpi-apisetu-replay"]

    # 8. Default: Flagship Module 1 SOC Authentication
    return TEMPLATE_REGISTRY["01-soc-auth-investigation"]
