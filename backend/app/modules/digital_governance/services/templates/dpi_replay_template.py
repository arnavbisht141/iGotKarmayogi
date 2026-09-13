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
                "content": "Filter apisetu_gateway_logs.json for requests where 'x_request_nonce' appears more than once across distinct client IPs.",
                "penalty": 15,
            },
            {
                "id": 2,
                "content": f"The gateway WAF caught and logged the mitigation payload for replayed nonce '{slots['replayed_nonce']}'. Look at the 'waf_mitigation_token' field to find the flag.",
                "content": f"The gateway WAF caught and logged the mitigation payload for replayed nonce '{slots['replayed_nonce']}'. Look at the 'waf_mitigation_token' field in the rejected records to find the flag.",
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
2. Group by `x_request_nonce` and isolate duplicated timestamps.
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
        legit_client = slots.get("legit_client_id", "gov.nodal.client.1042")

        logs = []
        base_t = datetime.datetime(2026, 9, 12, 8, 0, 0, tzinfo=datetime.timezone.utc)

        # 1. 80 normal transactions with unique nonces
        for i in range(80):
            ts = base_t + datetime.timedelta(seconds=i * 12)
            n = f"nonce_{hashlib.sha256(f'legit_{i}'.encode()).hexdigest()[:16]}"
            sig = hashlib.sha256(f"sig_{n}_{ts.isoformat()}".encode()).hexdigest()
            logs.append({
                "request_id": f"req-setu-{1000 + i}",
                "timestamp": ts.isoformat(),
                "endpoint": endpoint,
                "method": "POST",
                "client_id": legit_client,
                "client_ip": f"10.20.{random.randint(1, 10)}.{random.randint(10, 200)}",
                "x_request_nonce": n,
                "signature_hmac": sig[:32],
                "response_code": 200,
                "status": "VALIDATED",
                "response_time_ms": random.randint(35, 120),
            })

        # 2. Replay attack: 1 initial legitimate request + 10 replayed duplicates
        # 2. Replay attack: 1 initial legitimate request + 12 replayed duplicates
        init_ts = base_t + datetime.timedelta(minutes=18)
        replayed_sig = hashlib.sha256(f"sig_{replayed_nonce}_{init_ts.isoformat()}".encode()).hexdigest()[:32]
        logs.append({
            "request_id": "req-setu-target-orig",
            "timestamp": init_ts.isoformat(),
            "endpoint": endpoint,
            "method": "POST",
            "client_id": legit_client,
            "client_ip": "10.20.1.55",
            "x_request_nonce": replayed_nonce,
            "signature_hmac": replayed_sig,
            "response_code": 200,
            "status": "VALIDATED",
            "response_time_ms": 64,
        })

        for j in range(12):
            replay_ts = init_ts + datetime.timedelta(seconds=2 + j * 4)
            is_target = (j == 3)
            entry = {
                "request_id": f"req-setu-replay-{j+1:02d}",
                "timestamp": replay_ts.isoformat(),
                "endpoint": endpoint,
                "method": "POST",
                "client_id": legit_client,
                "client_ip": f"{subnet_prefix}.{random.randint(10, 240)}.{random.randint(2, 250)}",
                "x_request_nonce": replayed_nonce,
                "signature_hmac": replayed_sig,
                "response_code": 403,
                "status": "REJECTED_NONCE_REPLAY",
                "response_time_ms": 4,
            }
            if is_target:
                entry["waf_mitigation_token"] = flag
            logs.append(entry)

        logs.sort(key=lambda x: x["timestamp"])

        log_file = data_dir / "apisetu_gateway_logs.json"
        log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")

        return {"apisetu_gateway_logs.json": log_file}
        # Create API Setu security spec artifact
        spec = {
            "api_version": "2.4.0",
            "standard": "India Stack / API Setu Security Framework 3.4",
            "mandates": {
                "nonce_uniqueness": "RFC 6749 Section 10.12 - One-time cryptographically random nonce",
                "nonce_cache_ttl_seconds": 300,
                "timestamp_tolerance_seconds": 60,
                "signature_algorithm": "HMAC-SHA256 with asymmetric fallback (RSA-PSS)",
                "statutory_compliance": ["DPDP Act 2023 Section 8", "IT Act 2000 Section 43A", "CERT-In Directions 2022"],
            },
            "target_endpoint": endpoint,
            "monitored_client_id": legit_client,
        }
        spec_file = data_dir / "apisetu_security_spec.json"
        spec_file.write_text(json.dumps(spec, indent=2), encoding="utf-8")

        return {
            "apisetu_gateway_logs.json": log_file,
            "apisetu_security_spec.json": spec_file,
        }

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
        code = code.replace("__LEGIT_CLIENT_ID__", slots.get('legit_client_id', 'gov.nodal.client.1042'))
        code = code.replace("__TARGET_HASH__", dynamic_hash)

        target_nb.write_text(code, encoding="utf-8")
        return target_nb


_NOTEBOOK_TEMPLATE = r'''import marimo

__generated_with = "0.24.1"
app = marimo.App(width="full", app_title="__APP_TITLE__")


@app.cell(hide_code=True)
def __():
    import hashlib
    import hmac
    import json
    from pathlib import Path
    import re
    import marimo as mo
    import pandas as pd

    return Path, hashlib, json, mo, pd, re
    return Path, hashlib, hmac, json, mo, pd, re


@app.cell(hide_code=True)
def __(Path, json, pd):
    possible_paths = [
        Path("data/apisetu_gateway_logs.json"),
        Path("../data/apisetu_gateway_logs.json"),
        Path("/workspace/data/apisetu_gateway_logs.json"),
        Path("challenges/08-dpi-apisetu-replay/data/apisetu_gateway_logs.json"),
    ]
    if "__file__" in globals():
        possible_paths.insert(0, Path(__file__).resolve().parent.parent / "data" / "apisetu_gateway_logs.json")

    p = next((x for x in possible_paths if x.exists()), None)
    logs = json.loads(p.read_text()) if p else []
    raw_text = p.read_text(encoding="utf-8") if p else "[]"
    logs = json.loads(raw_text) if p else []
    df = pd.DataFrame(logs) if logs else pd.DataFrame()
    raw_json_bytes = raw_text.encode("utf-8")

    total_reqs = len(df)
    valid_reqs = len(df[df["status"] == "VALIDATED"]) if not df.empty and "status" in df.columns else 0
    replay_reqs = len(df[df["status"] == "REJECTED_NONCE_REPLAY"]) if not df.empty and "status" in df.columns else 0
    unique_nonces = df["x_request_nonce"].nunique() if not df.empty and "x_request_nonce" in df.columns else 0

    return df, logs, p, replay_reqs, total_reqs, valid_reqs
    return (
        df,
        logs,
        p,
        possible_paths,
        raw_json_bytes,
        raw_text,
        replay_reqs,
        total_reqs,
        unique_nonces,
        valid_reqs,
    )


@app.cell(hide_code=True)
def __(mo):
    # Sidebar
    check_nonce = mo.ui.checkbox(label="1. Group requests by x-request-nonce", value=False)
    # Analyst Sidebar: DPI Scope, India Stack Specs & Investigation Checklist
    check_nonce = mo.ui.checkbox(label="1. Group requests by x_request_nonce", value=False)
    check_collision = mo.ui.checkbox(label="2. Detect cryptographic nonce collision", value=False)
    check_subnet = mo.ui.checkbox(label="3. Trace botnet source IP cluster", value=False)
    check_spec = mo.ui.checkbox(label="4. Affirm India Stack mTLS & HMAC requirements", value=False)
    check_flag = mo.ui.checkbox(label="5. Extract WAF defense mitigation token", value=False)

    hints = mo.accordion(
        {
            "💡 Hint 1: Nonce Grouping & Duplication": mo.md(
                "In **Gateway Log Explorer** or using the **Analyst Python Scratchpad**, group requests by `x_request_nonce`. Count occurrences to locate nonces that appear more than once."
            ),
            "💡 Hint 2: Botnet Subnet & Status": mo.md(
                "Filter for requests where `status` is `REJECTED_NONCE_REPLAY`. Observe the `client_ip` subnet pattern and notice how all replays reuse `__REPLAYED_NONCE__`."
            ),
            "💡 Hint 3: WAF Mitigation Token": mo.md(
                "One of the blocked replay records contains the `waf_mitigation_token` emitted when the edge WAF dropped the packet. Extract this token to complete the defense audit."
            ),
        }
    )

    sidebar_content = mo.vstack(
        [
            mo.md("## 🇮🇳 API Setu DPI Defense Console"),
            mo.md("**Incident ID**: `__INCIDENT_CODENAME__`"),
            mo.md("**Endpoint**: `__GATEWAY_ENDPOINT__`"),
            mo.md("**Target Nonce**: `__REPLAYED_NONCE__`"),
            mo.md("**Target Endpoint**: `__GATEWAY_ENDPOINT__`"),
            mo.md("**Replayed Nonce**: `__REPLAYED_NONCE__`"),
            mo.md("**Botnet Subnet**: `__ATTACKER_SUBNET__`"),
            mo.md("**Target Client ID**: `__LEGIT_CLIENT_ID__`"),
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
                "- **HMAC-SHA256 / RSA**: Digital signature on request envelope\n"
                "- **DPDP Act 2023 §8**: Mandatory safeguards for identity telemetry\n"
                "- **CERT-In 6-Hour SLA**: Critical infrastructure incident reporting"
            ),
            mo.md("---"),
            hints,
        ]
    )
    mo.sidebar(sidebar_content)
    return (
        check_collision,
        check_flag,
        check_nonce,
        check_spec,
        check_subnet,
        hints,
        sidebar_content,
    )


@app.cell
def __(mo, sidebar_content):
    return (mo.sidebar(sidebar_content),)


@app.cell(hide_code=True)
def __(mo, replay_reqs, total_reqs, valid_reqs):
    # Tab 1: Scope
    tab1_view = mo.vstack(
def __(mo, replay_reqs, total_reqs, unique_nonces, valid_reqs):
    # Tab 1: Scope & DPI Topology
    triage_view = mo.vstack(
        [
            mo.md("""
            # 🇮🇳 API Setu Security: __INCIDENT_CODENAME__
            ### Digital Public Infrastructure (DPI) Replay Attack Defense & Nonce Audit
            """),
            mo.callout(
                mo.md(
                    "**DPI WAF Alert**: The national API gateway serving `__GATEWAY_ENDPOINT__` detected high-frequency requests duplicating an identical cryptographic nonce (`__REPLAYED_NONCE__`) originating from foreign botnet subnet `__ATTACKER_SUBNET__`. Inspect gateway access logs, identify the replay mechanism, and recover the WAF cryptographic defense token."
                    "**CRITICAL DPI GATEWAY ALERT**: The national API gateway serving `__GATEWAY_ENDPOINT__` detected high-frequency requests duplicating an identical cryptographic nonce (`__REPLAYED_NONCE__`) originating from foreign botnet subnet `__ATTACKER_SUBNET__`. Adversaries intercepted a signed citizen e-KYC authentication envelope and attempted automated transaction replay. Inspect gateway access logs, identify the collision mechanics, and recover the WAF cryptographic defense token."
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
                        value=f"{unique_nonces}",
                        label="Unique Nonces",
                        caption="Enforced in Memory Cache",
                        bordered=True,
                    ),
                ],
                justify="start",
                gap=1,
            ),
            mo.md("---"),
            mo.md("""
            ### 🏛️ Digital Public Infrastructure (DPI) Ecosystem Architecture
            ```text
            +--------------------+       +------------------------------------+       +-----------------------+
            | Citizen Smartphone | ----> | Authorized Consumer Application    | ----> | Central API Setu WAF  |
            | (Signed OTP / eKYC)|       | Client ID: __LEGIT_CLIENT_ID__     |       | Endpoint Gateway      |
            +--------------------+       +------------------------------------+       +-----------------------+
                                                          |                                       |
                                                          | [Adversary Wiretap]                   v
                                                          v                           +-----------------------+
                                                 [Stolen Signed Nonce]                | Redis Nonce Validator |
                                                          |                           | TTL Sliding Window    |
                                                          v                           +-----------------------+
                                              +-----------------------+                           |
                                              | Botnet Subnet         |                           | Validated (1st)
                                              | __ATTACKER_SUBNET__   |                           v
                                              | High-Frequency Replay |                +-----------------------+
                                              +-----------------------+ ------------>  | Aadhaar / DigiLocker  |
                                                                        [Blocked 403]  | Core Identity ASP     |
                                                                                       +-----------------------+
            ```
            """),
        ]
    )
    return (tab1_view,)
    return (triage_view,)


@app.cell(hide_code=True)
def __(df, mo):
    # Tab 2: Gateway Log Explorer
def __(df, mo, raw_json_bytes):
    # Tab 2: Telemetry Explorer Controls & Data Downloads
    status_choices = ["ALL"] + sorted(list(df["status"].unique())) if not df.empty and "status" in df.columns else ["ALL"]
    status_select = mo.ui.dropdown(
        options=["ALL", "VALIDATED", "REJECTED_NONCE_REPLAY"],
        options=status_choices,
        value="ALL",
        label="Filter Status:",
        label="Filter by Gateway Status:",
    )
    return (status_select,)
    search_log = mo.ui.text(
        placeholder="Filter by Nonce, IP, Request ID, or Endpoint...",
        label="Search Access Logs:",
    )
    download_json = mo.download(
        data=raw_json_bytes,
        filename="apisetu_gateway_logs.json",
        label="📥 Export apisetu_gateway_logs.json",
    )
    return download_json, search_log, status_choices, status_select


@app.cell(hide_code=True)
def __(df, mo, status_select):
def __(df, download_json, mo, search_log, status_select):
    # Tab 2: Filtered Gateway Access Telemetry Display
    filtered = df.copy() if not df.empty else df
    if not filtered.empty and status_select.value != "ALL":
        filtered = filtered[filtered["status"] == status_select.value]
    if not filtered.empty and search_log.value.strip():
        q = search_log.value.strip().lower()
        filtered = filtered[
            filtered["x_request_nonce"].str.lower().str.contains(q, na=False)
            | filtered["client_ip"].str.lower().str.contains(q, na=False)
            | filtered["endpoint"].str.lower().str.contains(q, na=False)
            | filtered.get("request_id", pd.Series([""] * len(filtered))).str.lower().str.contains(q, na=False)
        ]

    cols = [c for c in ["request_id", "timestamp", "endpoint", "client_ip", "x_request_nonce", "response_code", "status", "response_time_ms"] if c in filtered.columns]
    table = mo.ui.table(
        filtered[["timestamp", "endpoint", "client_ip", "x_request_nonce", "response_code", "status"]]
        if not filtered.empty and "endpoint" in filtered.columns else filtered,
        filtered[cols] if not filtered.empty else filtered,
        selection=None,
        pagination=True,
        page_size=8,
        show_column_summaries=False,
    )

    tab2_view = mo.vstack(
    telemetry_view = mo.vstack(
        [
            mo.md("## 🔍 API Setu Access Gateway Log Explorer (`apisetu_gateway_logs.json`)"),
            status_select,
            mo.md(
                "Examine all ingress transactions recorded by the API Setu reverse proxy. Export the raw JSON dataset or filter by request status and IP address:"
            ),
            mo.hstack([download_json], justify="start"),
            mo.md("---"),
            mo.hstack([status_select, search_log], justify="start", gap=2),
            table,
        ]
    )
    return filtered, table, tab2_view
    return cols, filtered, table, telemetry_view


@app.cell(hide_code=True)
def __(df, mo):
    # Tab 3: Nonce Collision
    # Tab 3: Cryptographic Replay & Nonce Collision Analysis
    replays = df[df["status"] == "REJECTED_NONCE_REPLAY"] if not df.empty and "status" in df.columns else df
    r_table = mo.ui.table(replays, selection=None, pagination=True, page_size=6) if not replays.empty else mo.md("No replays found.")

    tab3_view = mo.vstack(
    orig_req = df[df["x_request_nonce"] == "__REPLAYED_NONCE__"] if not df.empty and "x_request_nonce" in df.columns else pd.DataFrame()

    analyzer_view = mo.vstack(
        [
            mo.md("## ⚡ Cryptographic Nonce Collision Analysis"),
            mo.callout(
                mo.md(
                    "**Replay Attack Signature**:\n\n"
                    "- **Replayed Nonce**: `__REPLAYED_NONCE__`\n"
                    "- **Target Endpoint**: `__GATEWAY_ENDPOINT__`\n"
                    "**Adversary Attack Profile**:\n\n"
                    "- **Replayed Cryptographic Nonce**: `__REPLAYED_NONCE__`\n"
                    "- **Target Gateway Service**: `__GATEWAY_ENDPOINT__`\n"
                    "- **Botnet Subnet Cluster**: `__ATTACKER_SUBNET__`\n"
                    "- **Defense Mechanism**: Centralized in-memory nonce cache with sliding TTL window (300 seconds) prevents multiple execution of signed payloads."
                    "- **Spoofed Client Identity**: `__LEGIT_CLIENT_ID__`\n"
                    "- **WAF Response Behavior**: Legitimate client executed successfully (200 OK); 12 subsequent replays with identical nonce dropped (403 Forbidden)."
                ),
                kind="danger",
            ),
            mo.md("### 📊 Nonce Reuse Comparison: Original vs Replayed Requests"),
            mo.ui.table(orig_req, selection=None, pagination=False) if not orig_req.empty else mo.md("No matching records."),
            mo.md("---"),
            mo.md("### 🚫 Blocked Replay Telemetry Trace"),
            r_table,
        ]
    )
    return r_table, replays, tab3_view
    return analyzer_view, orig_req, r_table, replays


@app.cell(hide_code=True)
def __(mo):
    # Tab 4: Flag Input Control
    # Tab 4: Analyst Python Scratchpad Console Input
    scratchpad = mo.ui.code_editor(
        value="# Python DPI Gateway Analytics Scratchpad\n# Available: df (gateway logs dataframe), pd, re, json, hashlib, hmac\n\n# 1. Detect duplicate nonces:\nnonce_counts = df['x_request_nonce'].value_counts()\nduplicates = nonce_counts[nonce_counts > 1]\nprint('Duplicate Nonces Found:\\n', duplicates)\n\n# 2. Inspect WAF mitigation tokens in rejected replay records:\nreplays = df[df['status'] == 'REJECTED_NONCE_REPLAY']\ntokens = replays[replays['waf_mitigation_token'].notna()][['timestamp', 'client_ip', 'waf_mitigation_token']]\nprint('\\nRecovered Tokens:\\n', tokens)\n",
        language="python",
        label="Python DPI Analytics Console:",
    )
    return (scratchpad,)


@app.cell(hide_code=True)
def __(df, hashlib, hmac, json, mo, pd, re, scratchpad):
    # Tab 4: Reactive Python Execution Engine
    code_text = scratchpad.value.strip()
    eval_result = None

    if code_text:
        locs = {
            "df": df,
            "json": json,
            "pd": pd,
            "re": re,
            "hashlib": hashlib,
            "hmac": hmac,
        }
        try:
            lines = [
                l
                for l in code_text.splitlines()
                if l.strip() and not l.strip().startswith("#")
            ]
            if lines:
                exec_chunk = "\n".join(lines[:-1])
                last_line = lines[-1]
                if exec_chunk:
                    exec(exec_chunk, {"__builtins__": __builtins__}, locs)
                try:
                    res = eval(last_line, {"__builtins__": __builtins__}, locs)
                except SyntaxError:
                    exec(last_line, {"__builtins__": __builtins__}, locs)
                    res = locs.get("output", locs.get("result", "Script executed successfully."))

                if isinstance(res, pd.DataFrame):
                    eval_result = mo.ui.table(res, selection=None, pagination=True, page_size=6)
                elif isinstance(res, pd.Series):
                    eval_result = mo.ui.table(res.to_frame(), selection=None, pagination=True)
                elif res is not None:
                    eval_result = mo.md(f"```python\n{repr(res)}\n```")
                else:
                    eval_result = mo.md("✅ *Execution completed without output.*")
            else:
                eval_result = mo.md("ℹ️ *Enter Python code above to run interactive queries.*")
        except Exception as e:
            eval_result = mo.callout(
                mo.md(f"**Execution Error**: `{type(e).__name__}: {str(e)}`"),
                kind="danger",
            )
    else:
        eval_result = mo.md("ℹ️ *Analyst scratchpad idle. Write or execute expressions to query the gateway log dataset.*")

    scratchpad_view = mo.vstack(
        [
            mo.md("## 💻 Gateway Defense Scratchpad (Python)"),
            mo.md(
                "Run arbitrary pandas data filtering, calculate nonce occurrence statistics, inspect HMAC signatures, or query WAF tokens directly in Python:"
            ),
            scratchpad,
            mo.md("---"),
            mo.md("### 📤 Execution Output:"),
            eval_result,
        ]
    )
    return code_text, eval_result, scratchpad_view


@app.cell(hide_code=True)
def __(mo):
    # Tab 5: Remediation & India Stack Gateway Hardening
    diff_view = mo.ui.code_editor(
        value="""# /etc/apisetu/envoy-filter-nonce-validator.lua
-- Hardened India Stack DPI Replay Defense Policy (API Setu 3.4)

function envoy_on_request(request_handle)
    local headers = request_handle:headers()
    local nonce = headers:get("x-request-nonce")
    local req_ts = tonumber(headers:get("x-setu-timestamp") or "0")
    local now = os.time()

    -- 1. Enforce Timestamp Window Tolerance (60 seconds)
    if math.abs(now - req_ts) > 60 then
        request_handle:respond(
            {[":status"] = "401", ["content-type"] = "application/json"},
            '{"error": "TIMESTAMP_SKEW_EXCEEDED", "detail": "Request outside allowable 60s tolerance window"}'
        )
        return
    end

    -- 2. Distributed Redis Nonce Uniqueness Check with Sliding Window (300s TTL)
    local redis_key = "setu:nonce:" .. nonce
    local is_new = redis:set(redis_key, "1", "EX", 300, "NX")

    if not is_new then
        -- Cryptographic Nonce Reuse Detected: Drop Replay Attack
        request_handle:logWarn("REPLAY_ATTACK_DETECTED: nonce=" .. nonce .. " client_ip=" .. headers:get("x-forwarded-for"))
        request_handle:respond(
            {[":status"] = "403", ["content-type"] = "application/json"},
            '{"error": "REJECTED_NONCE_REPLAY", "mitigation": "NONCE_CACHE_HIT", "code": "403"}'
        )
        return
    end

    -- 3. Proceed to upstream e-KYC / DigiLocker service
end
""",
        language="lua",
        label="Hardened Gateway Envoy/Lua Defense Filter:",
    )

    hardening_view = mo.vstack(
        [
            mo.md("## 🛡️ India Stack Gateway Hardening & Lua Filter"),
            mo.callout(
                mo.md(
                    "**Statutory Gateway Requirements (MeitY / API Setu 3.4)**:\n"
                    "1. **Strict Nonce Uniqueness**: All incoming API requests must include a cryptographically random, non-repeating `X-Request-Nonce`.\n"
                    "2. **Distributed Sliding Window**: The gateway cluster must store seen nonces in an in-memory distributed cache (Redis) with a 300-second TTL using atomic `SETNX`.\n"
                    "3. **Timestamp Skew Tolerance**: Requests with timestamp skew exceeding 60 seconds are rejected with 401 Unauthorized before hitting identity engines.\n"
                    "4. **DPDP Act 2023 Section 8**: Data Fiduciaries must implement technical safeguards preventing fraudulent authentication replays against citizen accounts."
                ),
                kind="info",
            ),
            diff_view,
        ]
    )
    return diff_view, hardening_view


@app.cell(hide_code=True)
def __(mo):
    # Tab 6: Flag Input Control
    candidate_flag = mo.ui.text(
        placeholder="FLAG{...}",
        placeholder="FLAG{apisetu_replay_blocked_...}",
        label="Enter WAF Mitigation Defense Token to Verify:",
    )
    return (candidate_flag,)


@app.cell(hide_code=True)
def __(candidate_flag, hashlib, mo, re):
    val = candidate_flag.value.strip()
    target_hash = "__TARGET_HASH__"

    if not val:
        flag_feedback = mo.md("Enter the waf_mitigation_token logged in the rejected replay records.")
        flag_feedback = mo.md("Enter the `waf_mitigation_token` logged in the rejected replay records.")
        cert_view = mo.md("🔒 *National DPI Security Clearance Certificate locked until valid flag verified.*")
    elif hashlib.sha256(val.encode()).hexdigest() == target_hash:
        flag_feedback = mo.callout(
            mo.md("🎉 **WAF DEFENSE TOKEN VERIFIED!**\n\nSubmit this flag in the left CyberLab portal pane to claim 175 points and DPI Security competency!"),
            mo.md("🎉 **WAF DEFENSE TOKEN VERIFIED!**\n\nSubmit this flag in the CyberLab portal pane to claim 175 points and DPI Security competency!"),
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
                | Defense Parameter | Hardening Status | Statutory Reference |
                | :--- | :--- | :--- |
                | **Nonce Validation Engine** | **ACTIVE** — Strict one-time-use validation verified | RFC 6749 §10.12 |
                | **Replay Defense Filter** | **ENFORCED** — 100% of malicious duplicate requests dropped | API Setu Guideline 3.4 |
                | **Distributed Cache TTL** | **CONSTRAINED** — 300-second sliding expiration window | India Stack Core Spec |
                | **DPDP Act 2023 Compliance** | **VERIFIED** — Technical safeguards for citizen credentials | DPDP Act 2023 §8 |
                """),
            ]
        )
    elif re.match(r"^FLAG\{.*\}$", val):
        flag_feedback = mo.callout(mo.md("❌ Incorrect token. Inspect the `waf_mitigation_token` in the Nonce Collision tab."), kind="danger")
        flag_feedback = mo.callout(mo.md("❌ Incorrect token. Inspect the `waf_mitigation_token` field in the Nonce Collision tab or Python Scratchpad."), kind="danger")
        cert_view = mo.md("🔒 *Locked.*")
    else:
        flag_feedback = mo.callout(mo.md("⚠️ Format must begin with `FLAG{` and end with `}`."), kind="warn")
        cert_view = mo.md("🔒 *Locked.*")

    tab4_view = mo.vstack(
    verification_view = mo.vstack(
        [
            mo.md("## 🏁 DPI Hardening & Incident Closure"),
            candidate_flag,
            flag_feedback,
            mo.md("---"),
            cert_view,
        ]
    )
    return cert_view, flag_feedback, tab4_view, target_hash, val
    return cert_view, flag_feedback, target_hash, val, verification_view


@app.cell
def console_root(mo, tab1_view, tab2_view, tab3_view, tab4_view):
def console_root(
    analyzer_view,
    hardening_view,
    mo,
    scratchpad_view,
    sidebar_content,
    telemetry_view,
    triage_view,
    verification_view,
):
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
    /* Ensure Marimo chrome sidebar & inspection panels are visible */
    [data-testid="chrome-sidebar"], #app-chrome-sidebar, #app-chrome-panel, .resize-handle {
        display: block !important;
    }

    /* Un-hide all Marimo cells while keeping action toolbar hidden */
    .marimo-cell:not(:has(.cyberlab-topbar)) {
        display: block !important;
    }

    [data-testid="drag-button"],
    [data-testid="cell-actions-button"],
    [data-testid="create-cell-button"],
    [data-testid="run-button"],
    [data-testid="hide-code-button"],
    [data-testid="fullscreen-output-button"],
    [data-testid="expand-output-button"],
    .hover-actions-parent > .hover-action,
    .shoulder-right,
    .cell-actions,
    .cell-actions-button,
    .cell-bottom-menu,
    .add-cell-button {
        display: none !important;
    }

    [data-testid="filename-input"],
    [data-testid="chrome-controls-top-right"],
    [data-testid="chrome-controls-bottom-right"],
    [data-testid="chrome-footer"],
    [data-testid="footer-panel"] {
        display: none !important;
    }

    .marimo-cell:has(.cyberlab-topbar) {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 4px !important;
    }

    #App, main, #app-chrome-body, [data-testid="column-container"] {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .cyberlab-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 10px;
    }
    .cyberlab-topbar .title {
        font-size: 13px;
        font-weight: 700;
        color: #e2e8f0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .cyberlab-topbar .live-badge {
        background: #0284c7;
        color: white;
        font-size: 10px;
        font-weight: 800;
        padding: 2px 7px;
        border-radius: 4px;
        letter-spacing: 0.5px;
    }
    </style>
    """)
    header = mo.Html('<div class="cyberlab-topbar" style="display:none !important; height:0; margin:0; padding:0; border:none;"></div>')

    # Invisible anchor div keeps the .cyberlab-topbar CSS selector working
    header = mo.Html(
        '<div class="cyberlab-topbar" style="display:none !important; height:0; margin:0; padding:0; border:none;"></div>'
    )

    # Top-Level API Setu Operations Console
    console = mo.ui.tabs(
        {
            "📋 DPI Scope": tab1_view,
            "🔍 Gateway Logs": tab2_view,
            "⚡ Nonce Collision": tab3_view,
            "🏁 Verify & Certify": tab4_view,
            "📋 DPI Scope": triage_view,
            "🔍 Gateway Telemetry": telemetry_view,
            "⚡ Nonce Collision": analyzer_view,
            "💻 Python Scratchpad": scratchpad_view,
            "🛡️ Gateway Hardening": hardening_view,
            "📌 Audit Checklist": sidebar_content,
            "🏁 Verify & Clearance": verification_view,
        }
    )
    workspace = mo.vstack([styles, header, console])
    workspace
    return console, header, styles, workspace


if __name__ == "__main__":
    app.run()
'''
