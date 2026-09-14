from __future__ import annotations

import json
from pathlib import Path

import requests
import streamlit as st

from inveriq.detection.detector import demo_bruteforce_event
from inveriq.intent.policy import load_policy
from inveriq.response.generator import generate_candidates
from inveriq.verification.engine import verify

STATE_FILE = Path(".demo-state.json")
METRICS_URL = "http://127.0.0.1:18080/metrics"

st.set_page_config(page_title="INVERIQ — Expo Console", page_icon="🛡️", layout="wide")

st.markdown(
    """
<style>
.block-container {padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1500px;}
[data-testid="stMetric"] {border: 1px solid rgba(128,128,128,.20); border-radius: 12px; padding: 12px;}
.hero {font-size: 2.35rem; font-weight: 800; margin-bottom: .15rem;}
.subhero {font-size: 1.05rem; opacity: .72; margin-bottom: 1.2rem;}
.stage {padding: .65rem 1rem; border-radius: 10px; background: rgba(70,130,180,.12); font-weight: 650;}
</style>
""",
    unsafe_allow_html=True,
)


def read_state() -> dict:
    default = {"stage": "READY", "message": "Run demo/run_demo.sh", "candidate": None, "decision": None}
    try:
        return {**default, **json.loads(STATE_FILE.read_text())}
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def live_metrics() -> dict:
    try:
        return requests.get(METRICS_URL, timeout=0.6).json()
    except requests.RequestException:
        return {"total": 0, "login": 0, "health": 0, "requests_per_second": 0.0, "status": "offline"}


def verification_rows() -> tuple[list[dict], dict | None]:
    threat = demo_bruteforce_event()
    policy = load_policy()
    rows = []
    selected = None
    for candidate in generate_candidates(threat):
        result = verify(candidate, threat, policy)
        rows.append({
            "Candidate": candidate.id,
            "Action": candidate.action,
            "V1 Auth": result.authorization,
            "V2 Target": result.target,
            "V3 Reach": result.reachability,
            "V4 Avail": result.availability,
            "V5 Blast": result.blast_radius,
            "V6 Effect": result.effectiveness,
            "Decision": result.decision,
            "Blast %": round(candidate.estimated_blast_radius * 100, 2),
        })
        if result.decision == "VERIFIED" and (selected is None or candidate.estimated_blast_radius < selected.estimated_blast_radius):
            selected = candidate
    return rows, selected


st.markdown('<div class="hero">INVERIQ</div>', unsafe_allow_html=True)
st.markdown('<div class="subhero">Verified Autonomous Defense · AI decides. INVERIQ verifies. · by AVERNAUT</div>', unsafe_allow_html=True)


@st.fragment(run_every="1s")
def console() -> None:
    state = read_state()
    metrics = live_metrics()
    threat = demo_bruteforce_event()
    rows, selected = verification_rows()

    st.markdown(f'<div class="stage">{state["stage"]} — {state["message"]}</div>', unsafe_allow_html=True)
    st.write("")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("System", "ONLINE" if metrics.get("status") != "offline" else "OFFLINE")
    c2.metric("Threat", "BRUTE FORCE" if state["stage"] not in {"READY", "SETUP", "BASELINE"} else "NONE")
    c3.metric("MITRE", threat.mitre)
    c4.metric("Confidence", f"{threat.confidence * 100:.0f}%")
    c5.metric("Lab req/s", f"{metrics.get('requests_per_second', 0):.1f}")

    left, right = st.columns([1.25, 1])
    with left:
        st.subheader("Verification Gate")
        st.dataframe(rows, use_container_width=True, hide_index=True)
    with right:
        st.subheader("Decision")
        if state.get("decision") == "REJECTED":
            st.error(f"REJECTED — {state.get('candidate', 'unsafe action')}")
            st.caption("Stops the attack, but violates one or more operational invariants.")
        elif state.get("decision") == "VERIFIED":
            st.success(f"VERIFIED — {state.get('candidate', selected.id if selected else 'safe action')}")
            st.caption("Eligible for enforcement inside the isolated lab gateway.")
        elif selected:
            st.info(f"Lowest-blast-radius verified candidate: {selected.id}")

        st.subheader("Protected topology")
        st.code(
            "Attacker 10.77.0.50\n"
            "        │\n"
            "        ▼\n"
            "INVERIQ Gateway 10.77.0.10 ── Protected Auth API\n"
            "        ▲\n"
            "        │\n"
            "Trusted Client 10.77.0.60",
            language=None,
        )

    st.subheader("Live lab telemetry")
    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Total requests", metrics.get("total", 0))
    t2.metric("Login attempts", metrics.get("login", 0))
    t3.metric("Trusted health checks", metrics.get("health", 0))
    t4.metric("Selected blast radius", f"{(selected.estimated_blast_radius * 100 if selected else 0):.2f}%")

    if state["stage"] == "COMPLETE":
        st.success("Attack mitigated. Trusted service remains reachable. Demo reset completed.")


console()


# --- v0.6.0 Measurement & Evidence ---
try:
    import csv
    from pathlib import Path
    reports_csv = Path(".demo-state/reports/runs.csv")
    st.markdown("---")
    st.subheader("Measurement & Evidence")
    if reports_csv.exists():
        with reports_csv.open(newline="") as f:
            rows = list(csv.DictReader(f))
        if rows:
            latest = rows[-1]
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Closed-loop response", f"{float(latest['total_response_latency_ms']):.0f} ms")
            c2.metric("Attack reduction", f"{float(latest['attack_reduction_pct']):.1f}%")
            c3.metric("Availability", f"{float(latest['availability_pct']):.1f}%")
            c4.metric("Blast radius", f"{float(latest['blast_radius_pct']):.2f}%")
            st.caption(f"Latest measured run: {latest['scenario']} · {latest['run_id']}")
            st.dataframe(rows[-10:], use_container_width=True)
        else:
            st.info("No measured demo runs yet.")
    else:
        st.info("Run the demo to generate evidence reports.")
except Exception as exc:
    st.warning(f"Metrics panel unavailable: {exc}")


# --- v0.7.0 Real Testbed Instrumentation ---
try:
    import csv
    from pathlib import Path
    real_csv = Path(".demo-state/reports/runs-real.csv")
    st.markdown("---")
    st.subheader("Real Testbed Instrumentation")
    if real_csv.exists():
        with real_csv.open(newline="") as f:
            real_rows = list(csv.DictReader(f))
        if real_rows:
            r = real_rows[-1]
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Detection", f"{float(r['detection_latency_ms']):.1f} ms")
            c2.metric("Verification", f"{float(r['verification_latency_ms']):.3f} ms")
            c3.metric("Enforcement", f"{float(r['enforcement_latency_ms']):.1f} ms")
            c4.metric("Availability", f"{float(r['availability_pct']):.0f}%")
            st.caption(f"Real lab run: {r['scenario']} · {r['run_id']}")
            st.dataframe(real_rows[-10:], use_container_width=True)
        else:
            st.info("No real benchmark runs recorded yet.")
    else:
        st.info("Run scripts/benchmark_real.py to collect real lab evidence.")
except Exception as exc:
    st.warning(f"Real instrumentation unavailable: {exc}")
