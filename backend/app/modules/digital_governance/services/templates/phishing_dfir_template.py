"""Human-crafted Phishing DFIR Template (Flagship Module 2)."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import base64
import datetime
import hashlib
import json
import random

from app.modules.digital_governance.services.templates.base_template import BaseChallengeTemplate


class PhishingDfirTemplate(BaseChallengeTemplate):
    """
    Template for Spearphishing & Invoice Fraud Analysis.
    Generates synthetic email (.eml) with DKIM/SPF spoofing and DNS telemetry
    containing C2 callbacks with dynamic flags.
    """

    template_id = "phishing-dfir"
    title = "DFIR Incident: Spearphishing & Invoice Fraud Analysis"
    category = "DFIR / Phishing"
    difficulty = "Intermediate"
    base_points = 150
    duration_minutes = 50
    competency_id = "phishing_analysis"
    competency_weight = 1.0
    tags = ["phishing", "dfir", "email", "dmarc", "spf", "eml", "dns", "macro", "c2", "cybersecurity"]
    mitre_techniques = ["T1566.001", "T1204.002", "T1071.001"]

    SENDER_DOMAINS = [
        "pfms-disbursement-update.nic-in.org",
        "gem-procurement-gateway.in.net",
        "state-treasury-portal.gov-service.co",
        "epfo-pension-direct.org.in",
    ]

    C2_DOMAINS = [
        "beacon-telemetry-gateway.org",
        "sync-cloud-validator.net",
        "edge-cdn-dispatch.info",
        "telemetry-collector-service.biz",
    ]

    def get_slot_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "incident_codename": {"type": "str", "description": "Investigation operation codename"},
            "sender_domain": {"type": "str", "description": "Spoofed/typosquatted sender domain"},
            "sender_email": {"type": "str", "description": "Sender email address"},
            "recipient_email": {"type": "str", "description": "Target employee email"},
            "c2_domain": {"type": "str", "description": "Correlated C2 callback domain"},
            "malicious_ip": {"type": "str", "description": "Attacker C2 IP address"},
        }

    def generate_random_slots(
        self, seed: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        rng = random.Random(seed) if seed else random.Random()
        sender_dom = rng.choice(self.SENDER_DOMAINS)
        c2_dom = rng.choice(self.C2_DOMAINS)

        slots = {
            "incident_codename": f"Operation Raksha-{rng.randint(101, 999)}",
            "sender_domain": sender_dom,
            "sender_email": f"accounts-billing@{sender_dom}",
            "recipient_email": f"finance.nodal@{rng.choice(['meity.gov.in', 'finance.nic.in', 'cag.gov.in'])}",
            "c2_domain": c2_dom,
            "malicious_ip": f"{rng.randint(45, 185)}.{rng.randint(10, 200)}.{rng.randint(1, 250)}.{rng.randint(2, 250)}",
            "seed_hash": hashlib.md5(f"{seed}-{rng.random()}".encode()).hexdigest(),
        }
        if overrides:
            slots.update(overrides)
        return slots

    def compute_flag(self, slots: Dict[str, Any]) -> str:
        domain_tag = slots["c2_domain"].split(".")[0]
        seed_part = slots["seed_hash"][:6]
        return f"FLAG{{dmarc_fail_{domain_tag}_{seed_part}}}"

    def generate_hints(self, slots: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "content": "Inspect the 'Authentication-Results' and 'Received-SPF' headers in the raw .eml to confirm domain impersonation and DMARC failure.",
                "penalty": 15,
            },
            {
                "id": 2,
                "content": f"Check `dns_telemetry.json` for outbound lookups matching the extracted C2 domain '{slots['c2_domain']}'. The TXT/CNAME query metadata holds the flag.",
                "penalty": 25,
            },
        ]

    def generate_objectives(self, slots: Dict[str, Any]) -> List[str]:
        return [
            f"Analyze raw MIME headers in urgent_invoice.eml and detect DMARC/SPF forgery claiming to be '{slots['sender_email']}'.",
            "Extract attachment details and calculate SHA-256 fingerprint.",
            f"Correlate DNS telemetry in dns_telemetry.json to uncover C2 resolution to '{slots['c2_domain']}' and verify the flag.",
        ]

    def generate_scenario_description(self, slots: Dict[str, Any]) -> str:
        return f"""### Emergency Incident Briefing: {slots['incident_codename']}

**Spearphishing & Financial Impersonation Triage**
A high-priority alert was triggered after an employee in accounts received an urgent disbursement notice ostensibly from `{slots['sender_email']}`.

The attachment claims to contain an expedited PFMS bank transfer schedule, but mail gateway logs marked the transaction with SPF and DKIM mismatches.

Your mandate:
1. Examine `urgent_invoice.eml` using the Marimo DFIR analyst console.
2. Uncover the spoofed sender IP, SPF alignment failures, and malicious macro indicators.
3. Cross-reference internal resolver requests in `dns_telemetry.json` with external C2 servers to uncover the flag.
"""

    def synthesize_artifacts(
        self, slots: Dict[str, Any], output_dir: Path
    ) -> Dict[str, Path]:
        data_dir = output_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        flag = self.compute_flag(slots)

        # 1. Synthesize raw .eml
        eml_content = f"""From: "Disbursement Gateway" <{slots['sender_email']}>
To: <{slots['recipient_email']}>
Subject: URGENT: Action Required - Direct Benefit Transfer Voucher Settlement
Date: Thu, 12 Sep 2026 04:30:15 +0530
Message-ID: <disburse.20260912.{slots['seed_hash'][:8]}@{slots['sender_domain']}>
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="----=_Part_2026_09"
Authentication-Results: mx.nic.in;
    spf=fail (sender IP {slots['malicious_ip']} is not permitted by domain {slots['sender_domain']});
    dkim=temperror (no key found);
    dmarc=fail (p=reject dis=none) header.from={slots['sender_domain']}
Received-SPF: Fail (mx.nic.in: domain of {slots['sender_domain']} does not designate {slots['malicious_ip']} as permitted sender)

------=_Part_2026_09
Content-Type: text/plain; charset=UTF-8

Respected Sir/Madam,

Kindly inspect the attached settlement voucher for immediate release of state welfare funds.
Failure to acknowledge within 24 hours will delay DBT batch processing.

Regards,
Financial Controller
------=_Part_2026_09
Content-Type: application/vnd.ms-excel.sheet.macroEnabled.12; name="Voucher_Settlement.xlsm"
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="Voucher_Settlement.xlsm"

UEsDBBQAAAAIAAAAIQAAAAAAAAAAAAAAA==
------=_Part_2026_09--
"""
        eml_file = data_dir / "urgent_invoice.eml"
        eml_file.write_text(eml_content, encoding="utf-8")

        # 2. Synthesize dns_telemetry.json
        dns_events = [
            {"timestamp": "2026-09-12 04:31:02", "query": "gov.in", "query_type": "A", "response_ip": "164.100.1.10", "client_ip": "10.0.4.15"},
            {"timestamp": "2026-09-12 04:31:15", "query": "pfms.nic.in", "query_type": "A", "response_ip": "164.100.58.45", "client_ip": "10.0.4.15"},
            {"timestamp": "2026-09-12 04:32:44", "query": slots["c2_domain"], "query_type": "A", "response_ip": slots["malicious_ip"], "client_ip": "10.0.4.15"},
            {"timestamp": "2026-09-12 04:32:48", "query": f"verify.{slots['c2_domain']}", "query_type": "TXT", "response_ip": flag, "client_ip": "10.0.4.15"},
        ]
        dns_file = data_dir / "dns_telemetry.json"
        dns_file.write_text(json.dumps(dns_events, indent=2), encoding="utf-8")

        return {"urgent_invoice.eml": eml_file, "dns_telemetry.json": dns_file}

    def generate_notebook(self, slots: Dict[str, Any], output_dir: Path) -> Path:
        marimo_dir = output_dir / "marimo"
        marimo_dir.mkdir(parents=True, exist_ok=True)
        target_nb = marimo_dir / "challenge.py"

        flag = self.compute_flag(slots)
        dynamic_hash = hashlib.sha256(flag.encode()).hexdigest()

        code = self._generate_fallback_notebook(slots, dynamic_hash)
        target_nb.write_text(code, encoding="utf-8")
        return target_nb

    def _generate_fallback_notebook(self, slots: Dict[str, Any], target_hash: str) -> str:
        return f'''import marimo

__generated_with = "0.17.6"
app = marimo.App(width="full", app_title="DFIR Incident: {slots.get('incident_codename', 'Spearphish')}")


@app.cell(hide_code=True)
def __():
    import json
    import hashlib
    from pathlib import Path
    import pandas as pd
    import marimo as mo
    return Path, hashlib, json, mo, pd


@app.cell(hide_code=True)
def __(Path, json, pd):
    paths = [Path("data/dns_telemetry.json"), Path("../data/dns_telemetry.json")]
    p = next((x for x in paths if x.exists()), None)
    if p:
        df = pd.DataFrame(json.loads(p.read_text()))
    else:
        df = pd.DataFrame()
    return df, p


@app.cell
def __(df, mo):
    mo.md(f"""
    # 📧 Phishing & DNS Incident Analysis: {slots.get('incident_codename', 'Operation')}
    Target Mail: **{slots.get('recipient_email', 'N/A')}** | Attacker Domain: **{slots.get('sender_domain', 'N/A')}**
    """)
    return


@app.cell
def __(df):
    # DNS queries
    df
    return df,


@app.cell
def __(hashlib, mo):
    target_hash = "{target_hash}"
    flag_input = mo.ui.text(placeholder="Enter flag e.g. FLAG{{...}}", label="Submit Verified Flag")
    return flag_input, target_hash


@app.cell
def __(flag_input, hashlib, mo, target_hash):
    user_flag = flag_input.value.strip()
    if not user_flag:
        result = mo.md("*(Enter flag above to verify solution)*")
    elif hashlib.sha256(user_flag.encode()).hexdigest() == target_hash:
        result = mo.md("### 🎯 FLAG ACCEPTED! Phishing threat neutralized.")
    else:
        result = mo.md("### ❌ INCORRECT FLAG. Check DNS TXT response records.")
    mo.vstack([flag_input, result])
    return result, user_flag


if __name__ == "__main__":
    app.run()
'''
