from fastapi import FastAPI

from inveriq.detection.detector import demo_bruteforce_event
from inveriq.enforcement.nftables import build_plan
from inveriq.intent.policy import load_policy
from inveriq.postverify.engine import simulate_post_verification
from inveriq.response.generator import generate_candidates
from inveriq.verification.engine import verify

app = FastAPI(title="INVERIQ API", version="0.4.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "product": "INVERIQ", "version": "0.4.0"}


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
    # Prefer the least disruptive candidate in the deterministic demo.
    selected = min(
        (candidate for candidate, _ in verified),
        key=lambda candidate: candidate.estimated_blast_radius,
        default=None,
    )

    plan = build_plan(selected, verified=True) if selected else None
    post = simulate_post_verification(selected) if selected else None

    return {
        "threat": threat.model_dump(mode="json"),
        "candidates": [c.model_dump() for c in candidates],
        "verification": [r.model_dump() for r in results],
        "selected": selected.model_dump() if selected else None,
        "enforcement": plan.__dict__ if plan else None,
        "post_verification": post.model_dump() if post else None,
        "demo_mode": "offline-safe",
    }
