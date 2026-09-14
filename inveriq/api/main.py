from fastapi import FastAPI

from inveriq.detection.detector import demo_bruteforce_event
from inveriq.enforcement.nftables import render_nftables
from inveriq.intent.policy import load_policy
from inveriq.response.generator import generate_candidates
from inveriq.verification.engine import verify

app = FastAPI(title="INVERIQ API", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "product": "INVERIQ", "version": "0.1.0"}


@app.get("/demo/bruteforce")
def brute_force_demo() -> dict:
    policy = load_policy()
    threat = demo_bruteforce_event()
    candidates = generate_candidates(threat)
    results = [verify(candidate, threat, policy) for candidate in candidates]

    verified = [
        (candidate, result)
        for candidate, result in zip(candidates, results)
        if result.decision == "VERIFIED"
    ]
    selected = verified[-1][0] if verified else None

    return {
        "threat": threat.model_dump(mode="json"),
        "candidates": [c.model_dump() for c in candidates],
        "verification": [r.model_dump() for r in results],
        "selected": selected.model_dump() if selected else None,
        "enforcement_preview": render_nftables(selected) if selected else None,
    }
