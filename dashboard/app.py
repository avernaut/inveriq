import requests
import streamlit as st

st.set_page_config(page_title="INVERIQ", layout="wide")
st.title("INVERIQ")
st.caption("Verified Autonomous Defense — AI decides. INVERIQ verifies.")
st.info("Expo MVP v0.2 runs in offline-safe mode: verification is real; hostile traffic and enforcement are simulated/previewed.")

if st.button("Run Brute Force Verification Demo", type="primary"):
    data = requests.get("http://api:8000/demo/bruteforce", timeout=5).json()
    threat = data["threat"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Threat", "Brute Force")
    c2.metric("MITRE", threat["mitre"])
    c3.metric("Confidence", f"{threat['confidence'] * 100:.0f}%")
    c4.metric("Severity", threat["severity"])

    st.subheader("Verification Gate")
    rows = []
    by_id = {c["id"]: c for c in data["candidates"]}
    for result in data["verification"]:
        candidate = by_id[result["candidate"]]
        rows.append({
            "Candidate": candidate["id"],
            "Action": candidate["action"],
            "Source": candidate["source"],
            "Authorization": result["authorization"],
            "Target": result["target"],
            "Reachability": result["reachability"],
            "Availability": result["availability"],
            "Blast Radius": result["blast_radius"],
            "Effectiveness": result["effectiveness"],
            "Decision": result["decision"],
        })
    st.dataframe(rows, use_container_width=True, hide_index=True)

    selected = data.get("selected")
    if selected:
        st.success(f"VERIFIED TO EXECUTE: {selected['action']} on {selected['source']}")
        st.caption("Enforcement preview (not executed in v0.2)")
        st.code(data["enforcement"]["command"], language="bash")

        post = data["post_verification"]
        st.subheader("Post-verification")
        p1, p2, p3 = st.columns(3)
        p1.metric("Threat reduction", f"{post['threat_reduction'] * 100:.1f}%")
        p2.metric("Service availability", f"{post['availability'] * 100:.1f}%")
        p3.metric("Result", post["result"])
        st.caption(
            f"Attack requests/s: {post['attack_rate_before']:.0f} → {post['attack_rate_after']:.0f} | "
            f"Legitimate requests/s: {post['legitimate_rate_before']:.0f} → {post['legitimate_rate_after']:.0f}"
        )
