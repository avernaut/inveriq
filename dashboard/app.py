import requests
import streamlit as st

st.set_page_config(page_title="INVERIQ", layout="wide")
st.title("INVERIQ")
st.caption("Verified Autonomous Defense — AI decides. INVERIQ verifies.")

if st.button("Run Brute Force Demo", type="primary"):
    data = requests.get("http://localhost:8000/demo/bruteforce", timeout=5).json()
    threat = data["threat"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Threat", threat["attack"])
    c2.metric("MITRE", threat["mitre"])
    c3.metric("Confidence", f"{threat['confidence'] * 100:.0f}%")

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
        st.code(data["enforcement_preview"], language="bash")
