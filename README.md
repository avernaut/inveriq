<p align="center">
  <img src="assets/avernaut-logo.png" alt="Avernaut" width="120" />
</p>

<h1 align="center">INVERIQ</h1>
<p align="center"><strong>Verified Autonomous Defense</strong></p>
<p align="center"><em>AI decides. INVERIQ verifies.</em></p>

> **Private MVP repository — Avernaut**

INVERIQ is a verified autonomous cyber-defense platform that validates AI-generated cybersecurity actions before safely enforcing them across IoT, Edge, Cloud, and OT infrastructures.

Its design principle is simple: **no AI-generated security action should reach infrastructure blindly.**

## Core control loop

**Detect → Decide → Verify → Defend → Verify**

1. **Detect** anomalous or malicious activity.
2. **Decide** on one or more candidate mitigations.
3. **Verify** every candidate against explicit safety and operational invariants.
4. **Defend** by enforcing only a verified mitigation.
5. **Verify again** that the threat was reduced and legitimate service remains healthy.

## MVP verification gates

The INVERIQ Verification Engine evaluates six deterministic gates before an action may execute:

| Gate | Verification | Core question |
|---|---|---|
| V1 | Authorization | Is the action permitted by policy? |
| V2 | Target | Does the action match the observed evidence and intended target? |
| V3 | Reachability | Will critical flows remain reachable? |
| V4 | Availability | Will protected services remain available? |
| V5 | Blast Radius | Is collateral impact within the configured threshold? |
| V6 | Security Effectiveness | Is the action expected to reduce or stop the attack? |

Execution follows an all-gates rule:

`EXECUTE ⇔ V1 ∧ V2 ∧ V3 ∧ V4 ∧ V5 ∧ V6`

A failed gate rejects the candidate; verification is not an average score.

## IoT Tech Expo Europe demo

The MVP is designed around a short, reproducible demonstration:

- normal IoT traffic is active;
- a credential brute-force attack begins;
- INVERIQ detects and maps the threat to MITRE ATT&CK;
- multiple candidate mitigations are generated;
- a deliberately unsafe candidate is rejected;
- a safe candidate is verified and enforced through `nftables`;
- post-verification confirms threat reduction and service continuity.

Primary demo scenario: **Credential Brute Force / MITRE ATT&CK T1110**.

Secondary scenarios: DDoS/resource exhaustion and data exfiltration.

## Repository layout

```text
inveriq/
├── inveriq/
│   ├── api/
│   ├── detection/
│   ├── enforcement/
│   ├── intent/
│   ├── models/
│   ├── response/
│   ├── telemetry/
│   └── verification/
├── dashboard/
├── demo/
├── policies/
├── topology/
├── tests/
├── docs/
├── assets/
├── docker-compose.yml
└── requirements.txt
```

## Technology stack

- Python
- FastAPI
- Streamlit
- Docker / Docker Compose
- Linux `nftables`
- YAML/JSON policy definitions
- MITRE ATT&CK mapping
- ML/statistical threat detection
- Optional LLM-based response generation behind deterministic verification

## Security architecture

The LLM, when enabled, never writes directly to the firewall or infrastructure. It may only produce structured mitigation candidates from a closed action vocabulary. The deterministic Verification Engine authorizes or rejects those candidates before a trusted adapter translates them into enforcement rules.

This separation is deliberate:

`AI recommendation → structured action → deterministic verification → enforcement adapter`

## Development status

**v0.3.0 — Isolated enforcement lab**

Current repository contents establish the initial models, verification flow, policy representation, demo scenarios, dashboard skeleton, and enforcement adapter structure.

The current milestone adds an isolated Docker lab with synthetic live traffic and real `nftables` enforcement inside the lab gateway only. The host firewall is never modified by the INVERIQ demo tooling.

## Ownership and confidentiality

Copyright © 2026 Avernaut. All rights reserved.

This repository contains proprietary work in development. No license is granted to use, copy, modify, distribute, sublicense, or create derivative works unless explicitly authorized by Avernaut.

## Contact

**Avernaut**  
https://avernaut.com  
contact@avernaut.com

## v0.2.0 — Expo MVP foundation

The v0.2.0 branch adds GitHub CI/security workflows, issue and PR templates, an
end-to-end offline-safe brute-force verification scenario, enforcement preview,
and post-mitigation verification metrics. Verification decisions remain
deterministic and no generated command is executed by the application.

Run locally:

```bash
docker compose up --build
```

Then open `http://localhost:8501`.


## v0.3.0 — Isolated real-enforcement lab

The v0.3.0 milestone introduces a dedicated Docker lab on `10.77.0.0/24`:

- protected gateway/API: `10.77.0.10`;
- synthetic attacker: `10.77.0.50`;
- trusted client: `10.77.0.60`;
- real `nftables` filtering inside the gateway container;
- explicit `lab_mode` gate before a verified action becomes executable;
- no host-firewall execution path.

Start the isolated demo:

```bash
docker compose -f docker-compose.lab.yml up --build -d
python scripts/lab_status.py
python scripts/lab_enforce.py --candidate MIT-UNSAFE
python scripts/lab_enforce.py --candidate MIT-RATE
python scripts/lab_status.py
```

See [`docs/LAB.md`](docs/LAB.md) for the full workflow and safety boundary.

## Expo demo launcher (v0.4)

The complete isolated demonstration can now be run as a single scripted flow:

```bash
streamlit run dashboard/app.py
# second terminal
demo/run_demo.sh --keep-lab
```

`demo/run_demo.sh` drives the presentation stages, intentionally demonstrates rejection of `MIT-UNSAFE`, enforces only the verified `MIT-RATE` action inside `inveriq-gateway`, performs post-verification, and resets the lab. See [`docs/DEMO.md`](docs/DEMO.md).


## Expo demo

See [`demo/README.md`](demo/README.md) for the complete live-demo runbook and v0.5.0 scenario commands.
