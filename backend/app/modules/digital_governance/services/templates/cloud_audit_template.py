"""Government Cloud (MeghRaj / GI Cloud) & STQC Audit Template (Module 7)."""

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
    and MeitY empanelment non-compliance indicators with full Marimo console.
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
                "content": "Filter cloud_audit_events.json for records where 'region' does not start with 'meghraj-'. MeitY guidelines mandate strict domestic data residency.",
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
        unauth_reg = slots["unauthorized_region"]
        egress_ip = slots["egress_ip"]
        b_name = slots["bucket_name"]

        events = []
        base_t = datetime.datetime(2026, 9, 12, 6, 0, 0, tzinfo=datetime.timezone.utc)

        # 60 legitimate MeghRaj in-country API events
        for i in range(60):
            ts = base_t + datetime.timedelta(minutes=i * 2)
            events.append({
                "timestamp": ts.isoformat(),
                "event_name": random.choice(["GetObject", "PutObject", "ListBucket", "DescribeInstances"]),
                "region": random.choice(["meghraj-delhi-dc1", "meghraj-hyderabad-dc2"]),
                "source_ip": f"10.150.2.{random.randint(10, 80)}",
                "user_identity": "arn:nic:iam::998877:user/app_sync_service",
                "resource_name": f"meghraj-{slots['department']}-store",
                "status": "SUCCESS",
                "compliance_status": "COMPLIANT_IN_COUNTRY",
            })

        # 8 non-compliant foreign replication events
        for j in range(8):
            ts = base_t + datetime.timedelta(minutes=15 + j * 3)
            is_target = (j == 4)
            events.append({
                "timestamp": ts.isoformat(),
                "event_name": "ReplicateBucketMetadata" if not is_target else "ExportSovereignArchive",
                "region": unauth_reg,
                "source_ip": egress_ip,
                "user_identity": "arn:cloud:iam::unauth-contractor",
                "resource_name": b_name,
                "status": "SUCCESS",
                "compliance_status": "VIOLATION_CROSS_BORDER_TRANSFER",
                "response_elements": {"stqc_remediation_token": flag} if is_target else {"status": "replicated"},
            })

        events.sort(key=lambda x: x["timestamp"])

        audit_file = data_dir / "cloud_audit_events.json"
        audit_file.write_text(json.dumps(events, indent=2), encoding="utf-8")

        return {"cloud_audit_events.json": audit_file}

    def generate_notebook(self, slots: Dict[str, Any], output_dir: Path) -> Path:
        marimo_dir = output_dir / "marimo"
        marimo_dir.mkdir(parents=True, exist_ok=True)
        target_nb = marimo_dir / "challenge.py"

        flag = self.compute_flag(slots)
        dynamic_hash = hashlib.sha256(flag.encode()).hexdigest()

        code = _NOTEBOOK_TEMPLATE
        code = code.replace("__APP_TITLE__", f"MeghRaj Cloud Audit: {slots.get('incident_codename', 'Operation Megh')}")
        code = code.replace("__INCIDENT_CODENAME__", slots.get('incident_codename', 'INC-0707-MEGHRAJ-AUDIT'))
        code = code.replace("__DEPARTMENT__", slots.get('department', 'state-transport'))
        code = code.replace("__BUCKET_NAME__", slots.get('bucket_name', 'meghraj-vault-01'))
        code = code.replace("__UNAUTHORIZED_REGION__", slots.get('unauthorized_region', 'unapproved-us-east-1'))
        code = code.replace("__EGRESS_IP__", slots.get('egress_ip', '54.210.10.4'))
        code = code.replace("__TARGET_HASH__", dynamic_hash)

        target_nb.write_text(code, encoding="utf-8")
        return target_nb


_NOTEBOOK_TEMPLATE = r'''import marimo

__generated_with = "0.24.1"
app = marimo.App(width="full", app_title="__APP_TITLE__")


@app.cell(hide_code=True)
def __():
    import hashlib
    import json
    from pathlib import Path
    import re
    import marimo as mo
    import pandas as pd

    return Path, hashlib, json, mo, pd, re


@app.cell(hide_code=True)
def __(Path, json, pd):
    possible_paths = [
        Path("data/cloud_audit_events.json"),
        Path("../data/cloud_audit_events.json"),
        Path("/workspace/data/cloud_audit_events.json"),
    ]
    if "__file__" in globals():
        possible_paths.insert(0, Path(__file__).resolve().parent.parent / "data" / "cloud_audit_events.json")

    p = next((x for x in possible_paths if x.exists()), None)
    events = json.loads(p.read_text()) if p else []
    df = pd.DataFrame(events) if events else pd.DataFrame()

    total_events = len(df)
    domestic_events = len(df[df["compliance_status"] == "COMPLIANT_IN_COUNTRY"]) if not df.empty else 0
    violation_events = len(df[df["compliance_status"] == "VIOLATION_CROSS_BORDER_TRANSFER"]) if not df.empty else 0

    return df, domestic_events, events, p, total_events, violation_events


@app.cell(hide_code=True)
def __(mo):
    # Sidebar
    check_region = mo.ui.checkbox(label="1. Filter for unapproved overseas regions", value=False)
    check_bucket = mo.ui.checkbox(label="2. Isolate misconfigured S3 bucket", value=False)
    check_egress = mo.ui.checkbox(label="3. Trace foreign egress IP endpoint", value=False)
    check_stqc = mo.ui.checkbox(label="4. Affirm MeitY MeghRaj localization directive", value=False)
    check_flag = mo.ui.checkbox(label="5. Extract STQC remediation compliance token", value=False)

    sidebar_content = mo.vstack(
        [
            mo.md("## ☁️ MeghRaj Cloud Audit Console"),
            mo.md("**Incident ID**: `__INCIDENT_CODENAME__`"),
            mo.md("**Department**: `__DEPARTMENT__`"),
            mo.md("**Bucket Target**: `__BUCKET_NAME__`"),
            mo.md("**Non-Empaneled Region**: `__UNAUTHORIZED_REGION__`"),
            mo.md("---"),
            mo.md("### 🎯 Audit Checklist"),
            check_region,
            check_bucket,
            check_egress,
            check_stqc,
            check_flag,
            mo.md("---"),
            mo.md("### 📜 MeitY Directives"),
            mo.md(
                "- **GI Cloud (MeghRaj)**: Empaneled Community Cloud Services\n"
                "- **STQC Guidelines**: Annual Cloud Security Compliance & Audit\n"
                "- **Data Localization Mandate**: 100% Indian Jurisdiction Residency"
            ),
        ]
    )
    mo.sidebar(sidebar_content)
    return (
        check_bucket,
        check_egress,
        check_flag,
        check_region,
        check_stqc,
        sidebar_content,
    )


@app.cell(hide_code=True)
def __(domestic_events, mo, total_events, violation_events):
    # Tab 1: Scope
    tab1_view = mo.vstack(
        [
            mo.md("""
            # ☁️ MeghRaj Cloud Audit: __INCIDENT_CODENAME__
            ### GI Cloud Sovereignty & Multi-Tenant Isolation Forensics
            """),
            mo.callout(
                mo.md(
                    "**STQC Regulatory Notice**: An automated security scan flagged unexpected outbound telemetry and object replication targeting non-empaneled region `__UNAUTHORIZED_REGION__` involving bucket `__BUCKET_NAME__`. Under MeitY policy, all government citizen data must reside exclusively within the territory of India in MeghRaj empaneled data centres."
                ),
                kind="warn",
            ),
            mo.hstack(
                [
                    mo.stat(
                        value=f"{total_events}",
                        label="Total Cloud Events",
                        caption="Audited API Window",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{domestic_events}",
                        label="Empaneled Domestic Events",
                        caption="Delhi / Hyderabad GCC",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{violation_events}",
                        label="Cross-Border Violations",
                        caption="__UNAUTHORIZED_REGION__",
                        direction="increase",
                        bordered=True,
                    ),
                    mo.stat(
                        value="NON-COMPLIANT",
                        label="STQC Status",
                        caption="Immediate Containment Required",
                        bordered=True,
                    ),
                ],
                justify="start",
                gap=1,
            ),
        ]
    )
    return (tab1_view,)


@app.cell(hide_code=True)
def __(df, mo):
    # Tab 2: Telemetry Explorer
    region_filter = mo.ui.dropdown(
        options=["ALL", "meghraj-delhi-dc1", "meghraj-hyderabad-dc2", "__UNAUTHORIZED_REGION__"],
        value="ALL",
        label="Filter Cloud Region:",
    )
    return (region_filter,)


@app.cell(hide_code=True)
def __(df, mo, region_filter):
    filtered = df.copy() if not df.empty else df
    if not filtered.empty and region_filter.value != "ALL":
        filtered = filtered[filtered["region"] == region_filter.value]

    table = mo.ui.table(
        filtered[["timestamp", "event_name", "region", "source_ip", "resource_name", "compliance_status"]]
        if not filtered.empty and "region" in filtered.columns else filtered,
        selection=None,
        pagination=True,
        page_size=8,
    )

    tab2_view = mo.vstack(
        [
            mo.md("## 🔍 CloudTrail Audit Event Stream (`cloud_audit_events.json`)"),
            region_filter,
            table,
        ]
    )
    return filtered, table, tab2_view


@app.cell(hide_code=True)
def __(df, mo):
    # Tab 3: Violation Analysis
    violations = df[df["compliance_status"] == "VIOLATION_CROSS_BORDER_TRANSFER"] if not df.empty and "compliance_status" in df.columns else df
    v_table = mo.ui.table(violations, selection=None, pagination=True, page_size=6) if not violations.empty else mo.md("No violations.")

    tab3_view = mo.vstack(
        [
            mo.md("## 🚨 Cross-Border Sovereign Data Violations"),
            mo.callout(
                mo.md(
                    "**Unempaneled Replicas Detected**:\n\n"
                    "- **Target Region**: `__UNAUTHORIZED_REGION__`\n"
                    "- **Egress Destination IP**: `__EGRESS_IP__`\n"
                    "- **Misconfigured Resource**: `__BUCKET_NAME__`\n"
                    "- **Remediation Action**: Revoke foreign replication role and enforce SCP (Service Control Policy) geo-fencing."
                ),
                kind="danger",
            ),
            v_table,
        ]
    )
    return tab3_view, v_table, violations


@app.cell(hide_code=True)
def __(mo):
    # Tab 4: Flag input
    candidate_flag = mo.ui.text(
        placeholder="FLAG{...}",
        label="Enter STQC Remediation Token to Certify Sovereign Clearance:",
    )
    return (candidate_flag,)


@app.cell(hide_code=True)
def __(candidate_flag, hashlib, mo, re):
    val = candidate_flag.value.strip()
    target_hash = "__TARGET_HASH__"

    if not val:
        flag_feedback = mo.md("Enter the stqc_remediation_token found in the violation event response elements.")
        clearance_view = mo.md("🔒 *STQC Sovereign Cloud Clearance locked until valid token is verified.*")
    elif hashlib.sha256(val.encode()).hexdigest() == target_hash:
        flag_feedback = mo.callout(
            mo.md("🎉 **STQC AUDIT TOKEN CONFIRMED!**\n\nSubmit this flag in the left portal pane to claim 125 points and Cloud Security competency!"),
            kind="success",
        )
        clearance_view = mo.vstack(
            [
                mo.md("### 📋 STQC Sovereign Cloud Clearance Report:"),
                mo.md("""
                | Audit Requirement | Finding & Remediation Status |
                | :--- | :--- |
                | **Data Residency** | Overseas replication terminated — 100% domestic MeghRaj enforced |
                | **Empanelment Verification** | Non-compliant cloud region blocked via organization SCP |
                | **Sovereign Clearance** | **APPROVED** — MeitY GI Cloud Guidelines Section 4.2 |
                """),
            ]
        )
    elif re.match(r"^FLAG\{.*\}$", val):
        flag_feedback = mo.callout(mo.md("❌ Incorrect token. Inspect the `response_elements` in the non-compliant region logs."), kind="danger")
        clearance_view = mo.md("🔒 *Locked.*")
    else:
        flag_feedback = mo.callout(mo.md("⚠️ Format must begin with `FLAG{` and end with `}`."), kind="warn")
        clearance_view = mo.md("🔒 *Locked.*")

    tab4_view = mo.vstack(
        [
            mo.md("## 🏁 Sovereign Cloud Remediation & STQC Clearance"),
            candidate_flag,
            flag_feedback,
            mo.md("---"),
            clearance_view,
        ]
    )
    return clearance_view, flag_feedback, tab4_view, target_hash, val


@app.cell
def console_root(mo, tab1_view, tab2_view, tab3_view, tab4_view):
    styles = mo.Html("""
    <style>
    [data-testid="chrome-sidebar"], #app-chrome-sidebar, #app-chrome-panel, .resize-handle { display: none !important; }
    [data-testid="drag-button"], [data-testid="cell-actions-button"], [data-testid="create-cell-button"], [data-testid="run-button"], [data-testid="hide-code-button"], [data-testid="fullscreen-output-button"], [data-testid="expand-output-button"], .hover-actions-parent > .hover-action, .shoulder-right, .cell-actions, .cell-actions-button, .cell-bottom-menu, .add-cell-button { display: none !important; }
    [data-testid="filename-input"], [data-testid="chrome-controls-top-right"], [data-testid="chrome-controls-bottom-right"], [data-testid="chrome-footer"], [data-testid="footer-panel"] { display: none !important; }
    .marimo-cell:not(:has(.console-topbar)) { display: none !important; }
    .marimo-cell .cm-editor, .marimo-cell .cm-scroller, .marimo-cell .cell-editor, [data-testid="cell-editor"] { display: none !important; height: 0 !important; overflow: hidden !important; }
    .marimo-cell:has(.console-topbar) { width: 100% !important; max-width: 100% !important; margin: 0 !important; padding: 0 4px !important; }
    #App, main, #app-chrome-body, [data-testid="column-container"] { max-width: 100% !important; padding: 0 !important; margin: 0 !important; }
    .console-topbar { display: flex; align-items: center; justify-content: space-between; background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 10px 16px; margin-bottom: 10px; }
    .console-topbar .title { font-size: 13px; font-weight: 700; color: #e2e8f0; display: flex; align-items: center; gap: 10px; }
    </style>
    """)
    header = mo.Html('<div class="console-topbar" style="display:none !important; height:0; margin:0; padding:0; border:none;"></div>')
    console = mo.ui.tabs(
        {
            "📋 Audit Scope": tab1_view,
            "🔍 CloudTrail Stream": tab2_view,
            "🚨 Cross-Border Violations": tab3_view,
            "🏁 Verify & STQC Clearance": tab4_view,
        }
    )
    workspace = mo.vstack([styles, header, console])
    workspace
    return console, header, styles, workspace


if __name__ == "__main__":
    app.run()
'''
