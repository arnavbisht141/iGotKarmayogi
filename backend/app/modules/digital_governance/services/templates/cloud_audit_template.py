"""Government Cloud (MeghRaj / GI Cloud) & STQC Audit Template (Module 3)."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import datetime
import hashlib
import json
import random

from app.modules.digital_governance.services.templates.base_template import BaseChallengeTemplate


class CloudAuditTemplate(BaseChallengeTemplate):
    """
    Template for Government Community Cloud (MeghRaj) & STQC Audit Analysis.
    Generates synthetic cloud access logs, cross-border egress anomalies,
    and MeitY empanelment non-compliance indicators.
    """

    template_id = "cloud-meghraj-audit"
    title = "MeghRaj Cloud Audit: Cross-Border Sovereignty & Tenant Isolation"
    category = "Government Cloud / MeghRaj"
    difficulty = "Intermediate"
    base_points = 125
    duration_minutes = 45
    competency_id = "cloud_security"
    competency_weight = 1.0
    tags = ["cloud", "meghraj", "gi-cloud", "stqc", "data-localization", "sovereignty", "s3", "egress", "meity"]
    mitre_techniques = ["T1530", "T1048", "T1078.004"]

    REGIONS = ["meghraj-delhi-dc1", "meghraj-hyderabad-dc2", "unapproved-us-east-1", "unapproved-eu-central-1"]
    DEPARTMENTS = ["state-transport", "land-records", "civil-supplies", "revenue-portal"]

    def get_slot_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "incident_codename": {"type": "str", "description": "Investigation operation codename"},
            "department": {"type": "str", "description": "Affected state department"},
            "unauthorized_region": {"type": "str", "description": "Non-empaneled cloud region"},
            "egress_ip": {"type": "str", "description": "External unapproved egress endpoint"},
            "bucket_name": {"type": "str", "description": "Compromised S3 bucket"},
        }

    def generate_random_slots(
        self, seed: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        rng = random.Random(seed) if seed else random.Random()
        dept = rng.choice(self.DEPARTMENTS)
        unauth_reg = rng.choice(["unapproved-us-east-1", "unapproved-eu-west-1", "unapproved-ap-southeast-1"])

        slots = {
            "incident_codename": f"Operation Megh-{rng.randint(201, 899)}",
            "department": dept,
            "unauthorized_region": unauth_reg,
            "egress_ip": f"{rng.randint(52, 142)}.{rng.randint(10, 200)}.{rng.randint(1, 254)}.{rng.randint(2, 250)}",
            "bucket_name": f"meghraj-{dept}-vault-{rng.randint(10, 99)}",
            "seed_hash": hashlib.md5(f"{seed}-{rng.random()}".encode()).hexdigest(),
        }
        if overrides:
            slots.update(overrides)
        return slots

    def compute_flag(self, slots: Dict[str, Any]) -> str:
        tag = slots["unauthorized_region"].replace("-", "_")
        return f"FLAG{{meghraj_sovereign_{tag}_{slots['seed_hash'][:6]}}}"

    def generate_hints(self, slots: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "content": "Filter `cloud_audit_events.json` for records where 'region' does NOT start with 'meghraj-'. MeitY guidelines restrict all citizen data workloads to empaneled domestic regions.",
                "penalty": 15,
            },
            {
                "id": 2,
                "content": f"Inspect the 'response_elements' in the non-compliant region logs for S3 bucket '{slots['bucket_name']}'. The STQC remediation token provides the flag.",
                "penalty": 25,
            },
        ]

    def generate_objectives(self, slots: Dict[str, Any]) -> List[str]:
        return [
            f"Analyze cloud audit telemetry in cloud_audit_events.json to detect unauthorized foreign deployment in '{slots['unauthorized_region']}'.",
            f"Identify the non-compliant bucket '{slots['bucket_name']}' leaking citizen telemetry across borders.",
            "Verify STQC compliance parameters and recover the remediation flag.",
        ]

    def generate_scenario_description(self, slots: Dict[str, Any]) -> str:
        return f"""### Sovereign Cloud Compliance Incident: {slots['incident_codename']}

During an automated STQC audit of the State Government Community Cloud (GCC), anomalous API calls were detected originating from an overseas unempaneled cloud region (`{slots['unauthorized_region']}`).

A contractor inadvertently configured auto-scaling replicas of `{slots['bucket_name']}` across international borders, in violation of MeitY Sovereign Data Localization guidelines.

Your mandate:
1. Examine `cloud_audit_events.json` in the Marimo notebook.
2. Isolate the foreign region and egress transactions.
3. Extract the STQC security audit flag from the audit log metadata.
"""

    def synthesize_artifacts(
        self, slots: Dict[str, Any], output_dir: Path
    ) -> Dict[str, Path]:
        data_dir = output_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        flag = self.compute_flag(slots)
        events = []
        base_time = datetime.datetime(2026, 9, 12, 10, 0, 0, tzinfo=datetime.timezone.utc)

        # Baseline compliant logs in domestic MeghRaj
        for i in range(80):
            ts = base_time + datetime.timedelta(minutes=i)
            events.append({
                "timestamp": ts.isoformat(),
                "event_source": "s3.meghraj.gov.in",
                "event_name": "GetObject",
                "region": "meghraj-delhi-dc1" if i % 2 == 0 else "meghraj-hyderabad-dc2",
                "source_ip": f"10.244.{i % 10}.{i % 50}",
                "user_identity": "arn:meghraj:iam::gov:role/PortalAppRole",
                "bucket": f"meghraj-{slots['department']}-prod",
                "status": "COMPLIANT_DOMESTIC",
            })

        # Non-compliant foreign deployment event
        breach_ts = base_time + datetime.timedelta(minutes=42)
        events.append({
            "timestamp": breach_ts.isoformat(),
            "event_source": "s3.amazonaws.com",
            "event_name": "PutBucketPolicy",
            "region": slots["unauthorized_region"],
            "source_ip": slots["egress_ip"],
            "user_identity": "arn:aws:iam::thirdparty:user/devops_contractor",
            "bucket": slots["bucket_name"],
            "status": "NON_COMPLIANT_CROSS_BORDER",
            "response_elements": {"stqc_audit_token": flag, "remediation": "ENFORCE_DATA_LOCALIZATION_DPDP_SEC_8"},
        })

        events.sort(key=lambda x: x["timestamp"])
        data_file = data_dir / "cloud_audit_events.json"
        data_file.write_text(json.dumps(events, indent=2), encoding="utf-8")

        return {"cloud_audit_events.json": data_file}

    def generate_notebook(self, slots: Dict[str, Any], output_dir: Path) -> Path:
        marimo_dir = output_dir / "marimo"
        marimo_dir.mkdir(parents=True, exist_ok=True)
        target_nb = marimo_dir / "challenge.py"

        flag = self.compute_flag(slots)
        dynamic_hash = hashlib.sha256(flag.encode()).hexdigest()

        code = f'''import marimo

__generated_with = "0.17.6"
app = marimo.App(width="full", app_title="MeghRaj Cloud Audit: {slots.get('incident_codename', 'Operation')}")


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
    paths = [Path("data/cloud_audit_events.json"), Path("../data/cloud_audit_events.json")]
    p = next((x for x in paths if x.exists()), None)
    if p:
        df = pd.DataFrame(json.loads(p.read_text()))
    else:
        df = pd.DataFrame()
    return df, p


@app.cell
def __(df, mo):
    mo.md(f"""
    # ☁️ MeghRaj Cloud Audit: {slots.get('incident_codename', 'Audit')}
    Department: **{slots.get('department', 'N/A')}** | Non-Compliant Region: **{slots.get('unauthorized_region', 'N/A')}**
    """)
    return


@app.cell
def __(df):
    # Filter for non-domestic regions
    non_domestic = df[~df["region"].str.startswith("meghraj-", na=False)]
    non_domestic
    return non_domestic,


@app.cell
def __(hashlib, mo):
    target_hash = "{dynamic_hash}"
    flag_input = mo.ui.text(placeholder="Enter flag e.g. FLAG{{...}}", label="Submit Verified Flag")
    return flag_input, target_hash


@app.cell
def __(flag_input, hashlib, mo, target_hash):
    user_flag = flag_input.value.strip()
    if not user_flag:
        result = mo.md("*(Enter flag above to verify solution)*")
    elif hashlib.sha256(user_flag.encode()).hexdigest() == target_hash:
        result = mo.md("### 🎯 FLAG ACCEPTED! Sovereign data boundaries restored.")
    else:
        result = mo.md("### ❌ INCORRECT FLAG. Inspect the STQC audit token in response_elements.")
    mo.vstack([flag_input, result])
    return result, user_flag


if __name__ == "__main__":
    app.run()
'''
        target_nb.write_text(code, encoding="utf-8")
        return target_nb
