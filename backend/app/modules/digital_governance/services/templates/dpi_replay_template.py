"""Digital Public Infrastructure (DPI) & API Setu Replay Defense Template (Module 4)."""

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
    timestamp skew anomalies, and rate-limiting enforcement.
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
                "content": "Filter `apisetu_gateway_logs.json` for requests where the 'x-request-nonce' header appears more than once across distinct client IPs.",
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
        events = []
        base_time = datetime.datetime(2026, 9, 12, 14, 0, 0, tzinfo=datetime.timezone.utc)

        # Baseline legitimate traffic
        for i in range(100):
            ts = base_time + datetime.timedelta(seconds=i * 5)
            unique_nonce = f"nonce_{hashlib.md5(f'legit-{i}'.encode()).hexdigest()[:16]}"
            events.append({
                "timestamp": ts.isoformat(),
                "endpoint": slots["gateway_endpoint"],
                "client_id": slots["legit_client_id"],
                "client_ip": f"10.150.{i % 10}.{i % 40}",
                "x-request-nonce": unique_nonce,
                "status_code": 200,
                "response_time_ms": 42 + (i % 10),
            })

        # Replay attack cluster using same replayed_nonce
        replayed_nonce = slots["replayed_nonce"]
        burst_time = base_time + datetime.timedelta(seconds=350)
        prefix = slots["attacker_subnet"].split(".")[0]

        for j in range(25):
            ts = burst_time + datetime.timedelta(milliseconds=j * 150)
            events.append({
                "timestamp": ts.isoformat(),
                "endpoint": slots["gateway_endpoint"],
                "client_id": slots["legit_client_id"],
                "client_ip": f"{prefix}.100.{j % 5}.{j + 10}",
                "x-request-nonce": replayed_nonce,
                "status_code": 200 if j == 0 else 409,
                "response_time_ms": 15,
                "waf_mitigation_token": flag if j == 24 else None,
                "error_detail": None if j == 0 else "NONCE_REUSE_DETECTED",
            })

        events.sort(key=lambda x: x["timestamp"])
        data_file = data_dir / "apisetu_gateway_logs.json"
        data_file.write_text(json.dumps(events, indent=2), encoding="utf-8")

        return {"apisetu_gateway_logs.json": data_file}

    def generate_notebook(self, slots: Dict[str, Any], output_dir: Path) -> Path:
        marimo_dir = output_dir / "marimo"
        marimo_dir.mkdir(parents=True, exist_ok=True)
        target_nb = marimo_dir / "challenge.py"

        flag = self.compute_flag(slots)
        dynamic_hash = hashlib.sha256(flag.encode()).hexdigest()

        code = f'''import marimo

__generated_with = "0.17.6"
app = marimo.App(width="full", app_title="API Setu Security: {slots.get('incident_codename', 'Operation')}")


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
    paths = [Path("data/apisetu_gateway_logs.json"), Path("../data/apisetu_gateway_logs.json")]
    p = next((x for x in paths if x.exists()), None)
    if p:
        df = pd.DataFrame(json.loads(p.read_text()))
    else:
        df = pd.DataFrame()
    return df, p


@app.cell
def __(df, mo):
    mo.md(f"""
    # ⚡ API Setu Gateway Telemetry: {slots.get('incident_codename', 'Analysis')}
    Endpoint: **{slots.get('gateway_endpoint', 'N/A')}** | Client: **{slots.get('legit_client_id', 'N/A')}**
    """)
    return


@app.cell
def __(df):
    # Analyze duplicate nonces
    dup_nonces = df.groupby("x-request-nonce").size().reset_index(name="count")
    dup_nonces.sort_values(by="count", ascending=False).head(5)
    return dup_nonces,


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
        result = mo.md("### 🎯 FLAG ACCEPTED! Replay vulnerability resolved with cryptographic nonce validation.")
    else:
        result = mo.md("### ❌ INCORRECT FLAG. Locate the waf_mitigation_token in the replay cluster.")
    mo.vstack([flag_input, result])
    return result, user_flag


if __name__ == "__main__":
    app.run()
'''
        target_nb.write_text(code, encoding="utf-8")
        return target_nb
