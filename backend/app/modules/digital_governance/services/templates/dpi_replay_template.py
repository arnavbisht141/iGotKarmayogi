"""Digital Public Infrastructure (DPI) & API Setu Replay Defense Template (Module 8)."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import datetime
import hashlib
import json
import random

from app.modules.digital_governance.services.templates.base_template import BaseChallengeTemplate


class DpiReplayTemplate(BaseChallengeTemplate):
    """
    Template for Digital Public Infrastructure (India Stack / API Setu) Replay Attack Defense.
    Generates synthetic API gateway access telemetry with cryptographic nonce reuse,
    timestamp skew anomalies, and rate-limiting enforcement with full Marimo console.
    """

    template_id = "dpi-apisetu-replay"
    title = "DPI Security: API Setu Replay Attack & Nonce Validation"
    category = "Digital Public Infrastructure (DPI)"
    difficulty = "Advanced"
    base_points = 175
    duration_minutes = 50
    competency_id = "dpi_security"
    competency_weight = 1.0
    tags = ["dpi", "india-stack", "aadhaar", "api-setu", "replay-attack", "dpdp", "nonce", "rate-limit"]
    mitre_techniques = ["T1557", "T1071.001", "T1499"]

    ENDPOINTS = [
        "/api/v2/ekyc/verify-aadhaar-otp",
        "/api/v1/digilocker/fetch-certificate",
        "/api/v3/dbt/disbursement-validate",
    ]

    def get_slot_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "incident_codename": {"type": "str", "description": "Investigation operation codename"},
            "gateway_endpoint": {"type": "str", "description": "Target API gateway endpoint"},
            "replayed_nonce": {"type": "str", "description": "Replayed cryptographic nonce"},
            "attacker_subnet": {"type": "str", "description": "Originating botnet subnet"},
            "legit_client_id": {"type": "str", "description": "Spoofed authorized API client"},
        }

    def generate_random_slots(
        self, seed: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        rng = random.Random(seed) if seed else random.Random()
        endpoint = rng.choice(self.ENDPOINTS)
        nonce = f"nonce_{hashlib.sha256(f'{rng.random()}'.encode()).hexdigest()[:16]}"

        slots = {
            "incident_codename": f"Operation Setu-{rng.randint(301, 999)}",
            "gateway_endpoint": endpoint,
            "replayed_nonce": nonce,
            "attacker_subnet": f"{rng.randint(180, 203)}.{rng.randint(20, 150)}.{rng.randint(1, 250)}.0/24",
            "legit_client_id": f"gov.nodal.client.{rng.randint(1000, 9999)}",
            "seed_hash": hashlib.md5(f"{seed}-{rng.random()}".encode()).hexdigest(),
        }
        if overrides:
            slots.update(overrides)
        return slots

    def compute_flag(self, slots: Dict[str, Any]) -> str:
        nonce_tail = slots["replayed_nonce"][-8:]
        return f"FLAG{{apisetu_replay_blocked_{nonce_tail}_{slots['seed_hash'][:6]}}}"

    def generate_hints(self, slots: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "content": "Filter apisetu_gateway_logs.json for requests where 'x-request-nonce' appears more than once across distinct client IPs.",
                "penalty": 15,
            },
            {
                "id": 2,
                "content": f"The gateway WAF caught and logged the mitigation payload for replayed nonce '{slots['replayed_nonce']}'. Look at the 'waf_mitigation_token' field to find the flag.",
                "penalty": 25,
            },
        ]

    def generate_objectives(self, slots: Dict[str, Any]) -> List[str]:
        return [
            f"Analyze API Setu gateway telemetry to detect unauthorized duplicate nonce reuse on '{slots['gateway_endpoint']}'.",
            f"Trace the distributed botnet traffic emerging from subnet '{slots['attacker_subnet']}'.",
            "Extract the WAF cryptographic defense token and confirm mitigation.",
        ]

    def generate_scenario_description(self, slots: Dict[str, Any]) -> str:
        return f"""### API Setu Security Breach Briefing: {slots['incident_codename']}

The central API Setu gateway serving `{slots['gateway_endpoint']}` registered an alert for unauthorized duplicate authentication requests.

Adversaries intercepted signed citizen requests and attempted high-volume replay attacks against the e-KYC service without generating fresh cryptographic nonces.

Your mandate:
1. Load `apisetu_gateway_logs.json` in the Marimo notebook.
2. Group by `x-request-nonce` and isolate duplicated timestamps.
3. Extract the WAF mitigation flag from the rate-limit log entry.
"""

    def synthesize_artifacts(
        self, slots: Dict[str, Any], output_dir: Path
    ) -> Dict[str, Path]:
        data_dir = output_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        flag = self.compute_flag(slots)
        endpoint = slots["gateway_endpoint"]
        replayed_nonce = slots["replayed_nonce"]
        subnet_prefix = slots["attacker_subnet"].rsplit(".", 2)[0]

        logs = []
        base_t = datetime.datetime(2026, 9, 12, 8, 0, 0, tzinfo=datetime.timezone.utc)

        # 1. 80 normal transactions with unique nonces
        for i in range(80):
            ts = base_t + datetime.timedelta(seconds=i * 12)
            n = f"nonce_{hashlib.sha256(f'legit_{i}'.encode()).hexdigest()[:16]}"
            logs.append({
                "timestamp": ts.isoformat(),
                "endpoint": endpoint,
                "method": "POST",
                "client_ip": f"10.20.{random.randint(1, 10)}.{random.randint(10, 200)}",
                "x_request_nonce": n,
                "response_code": 200,
                "status": "VALIDATED",
            })

        # 2. Replay attack: 1 initial legitimate request + 10 replayed duplicates
        init_ts = base_t + datetime.timedelta(minutes=18)
        logs.append({
            "timestamp": init_ts.isoformat(),
            "endpoint": endpoint,
            "method": "POST",
            "client_ip": "10.20.1.55",
            "x_request_nonce": replayed_nonce,
            "response_code": 200,
            "status": "VALIDATED",
        })

        for j in range(10):
            replay_ts = init_ts + datetime.timedelta(seconds=2 + j * 4)
            is_target = (j == 3)
            entry = {
                "timestamp": replay_ts.isoformat(),
                "endpoint": endpoint,
                "method": "POST",
                "client_ip": f"{subnet_prefix}.{random.randint(10, 240)}.{random.randint(2, 250)}",
                "x_request_nonce": replayed_nonce,
                "response_code": 403,
                "status": "REJECTED_NONCE_REPLAY",
            }
            if is_target:
                entry["waf_mitigation_token"] = flag
            logs.append(entry)

        logs.sort(key=lambda x: x["timestamp"])

        log_file = data_dir / "apisetu_gateway_logs.json"
        log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")

        return {"apisetu_gateway_logs.json": log_file}

    def generate_notebook(self, slots: Dict[str, Any], output_dir: Path) -> Path:
        marimo_dir = output_dir / "marimo"
        marimo_dir.mkdir(parents=True, exist_ok=True)
        target_nb = marimo_dir / "challenge.py"

        flag = self.compute_flag(slots)
        dynamic_hash = hashlib.sha256(flag.encode()).hexdigest()

        code = _NOTEBOOK_TEMPLATE
        code = code.replace("__APP_TITLE__", f"API Setu Replay Defense: {slots.get('incident_codename', 'Operation Setu')}")
        code = code.replace("__INCIDENT_CODENAME__", slots.get('incident_codename', 'INC-0808-APISETU-REPLAY'))
        code = code.replace("__GATEWAY_ENDPOINT__", slots.get('gateway_endpoint', '/api/v2/ekyc/verify-aadhaar-otp'))
        code = code.replace("__REPLAYED_NONCE__", slots.get('replayed_nonce', 'nonce_abcd1234ef567890'))
        code = code.replace("__ATTACKER_SUBNET__", slots.get('attacker_subnet', '185.120.44.0/24'))
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
        Path("data/apisetu_gateway_logs.json"),
        Path("../data/apisetu_gateway_logs.json"),
        Path("/workspace/data/apisetu_gateway_logs.json"),
    ]
    if "__file__" in globals():
        possible_paths.insert(0, Path(__file__).resolve().parent.parent / "data" / "apisetu_gateway_logs.json")

    p = next((x for x in possible_paths if x.exists()), None)
    logs = json.loads(p.read_text()) if p else []
    df = pd.DataFrame(logs) if logs else pd.DataFrame()

    total_reqs = len(df)
    valid_reqs = len(df[df["status"] == "VALIDATED"]) if not df.empty and "status" in df.columns else 0
    replay_reqs = len(df[df["status"] == "REJECTED_NONCE_REPLAY"]) if not df.empty and "status" in df.columns else 0

    return df, logs, p, replay_reqs, total_reqs, valid_reqs


@app.cell(hide_code=True)
def __(mo):
    # Sidebar
    check_nonce = mo.ui.checkbox(label="1. Group requests by x-request-nonce", value=False)
    check_collision = mo.ui.checkbox(label="2. Detect cryptographic nonce collision", value=False)
    check_subnet = mo.ui.checkbox(label="3. Trace botnet source IP cluster", value=False)
    check_spec = mo.ui.checkbox(label="4. Affirm India Stack mTLS & HMAC requirements", value=False)
    check_flag = mo.ui.checkbox(label="5. Extract WAF defense mitigation token", value=False)

    sidebar_content = mo.vstack(
        [
            mo.md("## 🇮🇳 API Setu DPI Defense Console"),
            mo.md("**Incident ID**: `__INCIDENT_CODENAME__`"),
            mo.md("**Endpoint**: `__GATEWAY_ENDPOINT__`"),
            mo.md("**Target Nonce**: `__REPLAYED_NONCE__`"),
            mo.md("**Botnet Subnet**: `__ATTACKER_SUBNET__`"),
            mo.md("---"),
            mo.md("### 🎯 Investigation Checklist"),
            check_nonce,
            check_collision,
            check_subnet,
            check_spec,
            check_flag,
            mo.md("---"),
            mo.md("### 📜 India Stack Specifications"),
            mo.md(
                "- **API Setu Guideline 3.4**: Nonce uniqueness TTL = 300s\n"
                "- **mTLS & HMAC-SHA256**: Payload integrity assurance\n"
                "- **DPDP Act 2023**: Protection of citizen identity tokens"
            ),
        ]
    )
    mo.sidebar(sidebar_content)
    return (
        check_collision,
        check_flag,
        check_nonce,
        check_spec,
        check_subnet,
        sidebar_content,
    )


@app.cell(hide_code=True)
def __(mo, replay_reqs, total_reqs, valid_reqs):
    # Tab 1: Scope
    tab1_view = mo.vstack(
        [
            mo.md("""
            # 🇮🇳 API Setu Security: __INCIDENT_CODENAME__
            ### Digital Public Infrastructure (DPI) Replay Attack Defense & Nonce Audit
            """),
            mo.callout(
                mo.md(
                    "**DPI WAF Alert**: The national API gateway serving `__GATEWAY_ENDPOINT__` detected high-frequency requests duplicating an identical cryptographic nonce (`__REPLAYED_NONCE__`) originating from foreign botnet subnet `__ATTACKER_SUBNET__`. Inspect gateway access logs, identify the replay mechanism, and recover the WAF cryptographic defense token."
                ),
                kind="warn",
            ),
            mo.hstack(
                [
                    mo.stat(
                        value=f"{total_reqs}",
                        label="Gateway API Requests",
                        caption="Ingested Gateway Window",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{valid_reqs}",
                        label="Valid Transactions",
                        caption="Unique Nonces Authenticated",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{replay_reqs}",
                        label="Blocked Replays",
                        caption="Rejected with 403 Forbidden",
                        direction="increase",
                        bordered=True,
                    ),
                    mo.stat(
                        value="CONTAINED",
                        label="WAF Defense Status",
                        caption="Nonce Cache Enforced",
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
    # Tab 2: Gateway Log Explorer
    status_select = mo.ui.dropdown(
        options=["ALL", "VALIDATED", "REJECTED_NONCE_REPLAY"],
        value="ALL",
        label="Filter Status:",
    )
    return (status_select,)


@app.cell(hide_code=True)
def __(df, mo, status_select):
    filtered = df.copy() if not df.empty else df
    if not filtered.empty and status_select.value != "ALL":
        filtered = filtered[filtered["status"] == status_select.value]

    table = mo.ui.table(
        filtered[["timestamp", "endpoint", "client_ip", "x_request_nonce", "response_code", "status"]]
        if not filtered.empty and "endpoint" in filtered.columns else filtered,
        selection=None,
        pagination=True,
        page_size=8,
    )

    tab2_view = mo.vstack(
        [
            mo.md("## 🔍 API Setu Access Gateway Log Explorer (`apisetu_gateway_logs.json`)"),
            status_select,
            table,
        ]
    )
    return filtered, table, tab2_view


@app.cell(hide_code=True)
def __(df, mo):
    # Tab 3: Nonce Collision
    replays = df[df["status"] == "REJECTED_NONCE_REPLAY"] if not df.empty and "status" in df.columns else df
    r_table = mo.ui.table(replays, selection=None, pagination=True, page_size=6) if not replays.empty else mo.md("No replays found.")

    tab3_view = mo.vstack(
        [
            mo.md("## ⚡ Cryptographic Nonce Collision Analysis"),
            mo.callout(
                mo.md(
                    "**Replay Attack Signature**:\n\n"
                    "- **Replayed Nonce**: `__REPLAYED_NONCE__`\n"
                    "- **Target Endpoint**: `__GATEWAY_ENDPOINT__`\n"
                    "- **Botnet Subnet Cluster**: `__ATTACKER_SUBNET__`\n"
                    "- **Defense Mechanism**: Centralized in-memory nonce cache with sliding TTL window (300 seconds) prevents multiple execution of signed payloads."
                ),
                kind="danger",
            ),
            r_table,
        ]
    )
    return r_table, replays, tab3_view


@app.cell(hide_code=True)
def __(mo):
    # Tab 4: Flag Input Control
    candidate_flag = mo.ui.text(
        placeholder="FLAG{...}",
        label="Enter WAF Mitigation Defense Token to Verify:",
    )
    return (candidate_flag,)


@app.cell(hide_code=True)
def __(candidate_flag, hashlib, mo, re):
    val = candidate_flag.value.strip()
    target_hash = "__TARGET_HASH__"

    if not val:
        flag_feedback = mo.md("Enter the waf_mitigation_token logged in the rejected replay records.")
        cert_view = mo.md("🔒 *National DPI Security Clearance Certificate locked until valid flag verified.*")
    elif hashlib.sha256(val.encode()).hexdigest() == target_hash:
        flag_feedback = mo.callout(
            mo.md("🎉 **WAF DEFENSE TOKEN VERIFIED!**\n\nSubmit this flag in the left CyberLab portal pane to claim 175 points and DPI Security competency!"),
            kind="success",
        )
        cert_view = mo.vstack(
            [
                mo.md("### 🏛️ National Critical DPI Hardening Certification:"),
                mo.md("""
                | Defense Parameter | Hardening Status |
                | :--- | :--- |
                | **Nonce Validation Engine** | Active — Strict one-time-use validation verified |
                | **Replay Defense** | 100% of malicious duplicate requests dropped |
                | **India Stack Compliance** | **CERTIFIED** — Full conformance with UIDAI & API Setu specifications |
                """),
            ]
        )
    elif re.match(r"^FLAG\{.*\}$", val):
        flag_feedback = mo.callout(mo.md("❌ Incorrect token. Inspect the `waf_mitigation_token` in the Nonce Collision tab."), kind="danger")
        cert_view = mo.md("🔒 *Locked.*")
    else:
        flag_feedback = mo.callout(mo.md("⚠️ Format must begin with `FLAG{` and end with `}`."), kind="warn")
        cert_view = mo.md("🔒 *Locked.*")

    tab4_view = mo.vstack(
        [
            mo.md("## 🏁 DPI Hardening & Incident Closure"),
            candidate_flag,
            flag_feedback,
            mo.md("---"),
            cert_view,
        ]
    )
    return cert_view, flag_feedback, tab4_view, target_hash, val


@app.cell
def console_root(mo, tab1_view, tab2_view, tab3_view, tab4_view):
    styles = mo.Html("""
    <style>
    [data-testid="chrome-sidebar"], #app-chrome-sidebar, #app-chrome-panel, .resize-handle { display: none !important; }
    [data-testid="drag-button"], [data-testid="cell-actions-button"], [data-testid="create-cell-button"], [data-testid="run-button"], [data-testid="hide-code-button"], [data-testid="fullscreen-output-button"], [data-testid="expand-output-button"], .hover-actions-parent > .hover-action, .shoulder-right, .cell-actions, .cell-actions-button, .cell-bottom-menu, .add-cell-button { display: none !important; }
    [data-testid="filename-input"], [data-testid="chrome-controls-top-right"], [data-testid="chrome-controls-bottom-right"], [data-testid="chrome-footer"], [data-testid="footer-panel"] { display: none !important; }
    .marimo-cell:not(:has(.cyberlab-topbar)) { display: none !important; }
    .marimo-cell .cm-editor, .marimo-cell .cm-scroller, .marimo-cell .cell-editor, [data-testid="cell-editor"] { display: none !important; height: 0 !important; overflow: hidden !important; }
    .marimo-cell:has(.cyberlab-topbar) { width: 100% !important; max-width: 100% !important; margin: 0 !important; padding: 0 4px !important; }
    #App, main, #app-chrome-body, [data-testid="column-container"] { max-width: 100% !important; padding: 0 !important; margin: 0 !important; }
    .cyberlab-topbar { display: flex; align-items: center; justify-content: space-between; background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 10px 16px; margin-bottom: 10px; }
    .cyberlab-topbar .title { font-size: 13px; font-weight: 700; color: #e2e8f0; display: flex; align-items: center; gap: 10px; }
    </style>
    """)
    header = mo.Html('<div class="cyberlab-topbar" style="display:none !important; height:0; margin:0; padding:0; border:none;"></div>')
    console = mo.ui.tabs(
        {
            "📋 DPI Scope": tab1_view,
            "🔍 Gateway Logs": tab2_view,
            "⚡ Nonce Collision": tab3_view,
            "🏁 Verify & Certify": tab4_view,
        }
    )
    workspace = mo.vstack([styles, header, console])
    workspace
    return console, header, styles, workspace


if __name__ == "__main__":
    app.run()
'''
