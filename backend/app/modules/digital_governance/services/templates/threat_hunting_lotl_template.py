"""Upgraded Threat Hunting & Living-off-the-Land (LotL) Template (Module 5)."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import datetime
import hashlib
import json
import math
import random

from app.modules.digital_governance.services.templates.base_template import BaseChallengeTemplate


class ThreatHuntingLotlTemplate(BaseChallengeTemplate):
    """
    Template for Advanced Threat Hunting, Process Masquerading, and DNS Tunneling.
    Synthesizes Sysmon process creation events and network DNS telemetry with entropy markers.
    """

    template_id = "05-threat-hunting-lotl"
    title = "CII Threat Hunting: Process Masquerading & DNS Tunneling Exfiltration"
    category = "Threat Hunting / Cyber Defense"
    difficulty = "Advanced"
    base_points = 200
    duration_minutes = 60
    competency_id = "threat_hunting"
    competency_weight = 1.5
    tags = ["threat-hunting", "lotl", "sysmon", "dns-tunneling", "entropy", "cert-in", "cii"]
    mitre_techniques = ["T1036.005", "T1071.004", "T1048.003"]

    TUNNEL_DOMAINS = [
        "ns-tunnel.c2-dispatch.org",
        "dns-sync.exfil-stream.net",
        "telemetry-gate.data-egress.info",
    ]

    def get_slot_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "incident_codename": {"type": "str", "description": "Investigation operation codename"},
            "tunnel_domain": {"type": "str", "description": "Attacker DNS tunneling domain"},
            "masqueraded_binary": {"type": "str", "description": "Spoofed system process name"},
            "unusual_path": {"type": "str", "description": "Illegitimate process path"},
        }

    def generate_random_slots(
        self, seed: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        rng = random.Random(seed) if seed else random.Random()
        tunnel_dom = rng.choice(self.TUNNEL_DOMAINS)

        slots = {
            "incident_codename": f"Operation Garuda-{rng.randint(501, 999)}",
            "tunnel_domain": tunnel_dom,
            "masqueraded_binary": "svchost.exe",
            "unusual_path": "C:\\Users\\Public\\svchost.exe",
            "seed_hash": hashlib.md5(f"{seed}-{rng.random()}".encode()).hexdigest(),
        }
        if overrides:
            slots.update(overrides)
        return slots

    def compute_flag(self, slots: Dict[str, Any]) -> str:
        return f"FLAG{{dns_tunneling_entropy_exfil_{slots['seed_hash'][:8]}}}"

    def generate_hints(self, slots: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "content": "Inspect `sysmon_events.json` for processes named 'svchost.exe' where the image path is NOT `C:\\Windows\\System32\\svchost.exe`.",
                "penalty": 25,
            },
            {
                "id": 2,
                "content": f"Compute the Shannon entropy of query names in `dns_events.json`. Subdomains with entropy > 4.2 targeting `*.{slots['tunnel_domain']}` are tunneling payloads.",
                "penalty": 40,
            },
        ]

    def generate_objectives(self, slots: Dict[str, Any]) -> List[str]:
        return [
            f"Hunt for process masquerading by filtering Sysmon Image paths running outside System32.",
            f"Calculate Shannon entropy across DNS query labels resolving to '{slots['tunnel_domain']}'.",
            "Reconstruct the exfiltrated tunneling stream and extract the incident flag.",
        ]

    def generate_scenario_description(self, slots: Dict[str, Any]) -> str:
        return f"""### Critical Information Infrastructure Threat Hunting: {slots['incident_codename']}

CERT-In national threat intelligence flagged anomalous DNS queries originating from an air-gapped critical infrastructure subnet.

The threat actor deployed a masqueraded Living-off-the-Land process (`{slots['unusual_path']}`) designed to exfiltrate encrypted state secrets using high-entropy DNS tunneling queries via `{slots['tunnel_domain']}`.

Your mandate:
1. Examine `sysmon_events.json` to isolate the rogue masqueraded process.
2. Analyze `dns_events.json` using Shannon entropy algorithms in the Marimo notebook.
3. Unmask the covert DNS channel and recover the flag.
"""

    def synthesize_artifacts(
        self, slots: Dict[str, Any], output_dir: Path
    ) -> Dict[str, Path]:
        data_dir = output_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        flag = self.compute_flag(slots)
        base_time = datetime.datetime(2026, 9, 12, 18, 0, 0, tzinfo=datetime.timezone.utc)

        # 1. sysmon_events.json
        sysmon_events = []
        # Legitimate svchost processes
        for i in range(25):
            sysmon_events.append({
                "timestamp": (base_time + datetime.timedelta(seconds=i * 10)).isoformat(),
                "event_id": 1,
                "process_name": "svchost.exe",
                "image_path": "C:\\Windows\\System32\\svchost.exe",
                "parent_image": "C:\\Windows\\System32\\services.exe",
                "command_line": "C:\\Windows\\system32\\svchost.exe -k netsvcs -p",
                "user": "NT AUTHORITY\\SYSTEM",
            })

        # Masqueraded malicious svchost
        sysmon_events.append({
            "timestamp": (base_time + datetime.timedelta(minutes=15)).isoformat(),
            "event_id": 1,
            "process_name": "svchost.exe",
            "image_path": slots["unusual_path"],
            "parent_image": "C:\\Windows\\explorer.exe",
            "command_line": f"{slots['unusual_path']} --egress dns --domain {slots['tunnel_domain']}",
            "user": "OFFICER-PC\\Operator",
        })

        sysmon_file = data_dir / "sysmon_events.json"
        sysmon_file.write_text(json.dumps(sysmon_events, indent=2), encoding="utf-8")

        # 2. dns_events.json
        dns_events = []
        # Baseline normal lookups
        normal_domains = ["gov.in", "nic.in", "pfms.gov.in", "cert-in.org.in", "digilocker.gov.in"]
        for j in range(60):
            dns_events.append({
                "timestamp": (base_time + datetime.timedelta(seconds=j * 5)).isoformat(),
                "query": random.choice(normal_domains),
                "query_type": "A",
                "response_code": "NOERROR",
                "entropy": round(random.uniform(2.1, 3.2), 2),
            })

        # DNS tunneling burst with high entropy
        tunnel_dom = slots["tunnel_domain"]
        dns_events.append({
            "timestamp": (base_time + datetime.timedelta(minutes=15, seconds=20)).isoformat(),
            "query": f"init.sync.{tunnel_dom}",
            "query_type": "TXT",
            "response_code": "NOERROR",
            "entropy": 3.45,
        })
        dns_events.append({
            "timestamp": (base_time + datetime.timedelta(minutes=15, seconds=25)).isoformat(),
            "query": f"aGVsZW1ldHJ5X3Rva2Vu_{slots['seed_hash'][:8]}.{tunnel_dom}",
            "query_type": "TXT",
            "response_code": "NOERROR",
            "entropy": 4.82,
            "payload_data": flag,
        })

        dns_file = data_dir / "dns_events.json"
        dns_file.write_text(json.dumps(dns_events, indent=2), encoding="utf-8")

        return {"sysmon_events.json": sysmon_file, "dns_events.json": dns_file}

    def generate_notebook(self, slots: Dict[str, Any], output_dir: Path) -> Path:
        marimo_dir = output_dir / "marimo"
        marimo_dir.mkdir(parents=True, exist_ok=True)
        target_nb = marimo_dir / "challenge.py"

        flag = self.compute_flag(slots)
        dynamic_hash = hashlib.sha256(flag.encode()).hexdigest()

        code = f'''import marimo

__generated_with = "0.17.6"
app = marimo.App(width="full", app_title="Threat Hunting: {slots.get('incident_codename', 'Garuda')}")


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
    p_sys = next((p for p in [Path("data/sysmon_events.json"), Path("../data/sysmon_events.json")] if p.exists()), None)
    p_dns = next((p for p in [Path("data/dns_events.json"), Path("../data/dns_events.json")] if p.exists()), None)

    df_sys = pd.DataFrame(json.loads(p_sys.read_text())) if p_sys else pd.DataFrame()
    df_dns = pd.DataFrame(json.loads(p_dns.read_text())) if p_dns else pd.DataFrame()
    return df_dns, df_sys, p_dns, p_sys


@app.cell
def __(df_dns, df_sys, mo):
    mo.md(f"""
    # 🦅 Threat Hunting: {slots.get('incident_codename', 'Operation')}
    Sysmon Records: **{{len(df_sys)}}** | DNS Query Logs: **{{len(df_dns)}}**
    """)
    return


@app.cell
def __(df_sys, mo):
    # Hunt for masqueraded processes (svchost outside System32)
    rogue = df_sys[~df_sys["image_path"].str.lower().str.startswith("c:\\\\windows\\\\system32", na=False)]
    mo.md("### 🕵️ Sysmon Process Hunting (Anomalous Binary Paths):")
    return rogue,


@app.cell
def __(df_dns, mo):
    # High entropy DNS queries (> 4.0)
    high_entropy = df_dns[df_dns["entropy"] > 4.0]
    mo.md("### 📡 High-Entropy DNS Tunneling Detections (Entropy > 4.0):")
    return high_entropy,


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
        result = mo.md("### 🎯 FLAG ACCEPTED! Covert DNS exfiltration severed and LotL eradicated.")
    else:
        result = mo.md("### ❌ INCORRECT FLAG. Check the payload_data in the high-entropy DNS tunnel burst.")
    mo.vstack([flag_input, result])
    return result, user_flag


if __name__ == "__main__":
    app.run()
'''
        target_nb.write_text(code, encoding="utf-8")
        return target_nb

