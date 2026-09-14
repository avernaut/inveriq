# INVERIQ

**Verified Autonomous Defense**

> AI decides. INVERIQ verifies.

INVERIQ is an MVP for verifying AI-generated cybersecurity mitigation actions before they are enforced on IoT/Edge infrastructure.

## Core pipeline

Detect -> Decide -> Verify -> Defend -> Verify

The Verification Engine checks six invariants before execution:

1. Authorization
2. Target consistency
3. Reachability
4. Availability
5. Blast radius
6. Security effectiveness

An action executes only if every mandatory verification returns `PASS`.

## MVP scope

- Python 3.12
- FastAPI backend
- Streamlit dashboard
- Docker Compose testbed
- Linux/nftables enforcement adapter
- YAML security intent/policy
- Demo scenarios: brute force, DDoS, exfiltration
- Offline-safe deterministic response mode

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn inveriq.api.main:app --reload
```

In another terminal:

```bash
streamlit run dashboard/app.py
```

Run tests:

```bash
pytest -q
```

## Demo concept

The demo intentionally generates multiple mitigation candidates. At least one candidate is unsafe but effective against the attack. INVERIQ rejects it because it violates operational invariants, then selects a verified alternative.

## Status

`v0.1-prealpha` — IoT Tech Expo Europe 2026 MVP.
