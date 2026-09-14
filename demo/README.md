# INVERIQ Expo Demo

This guide contains the complete procedure for running the INVERIQ live demonstration.

## Demo objective

The demo shows the complete INVERIQ control loop:

**Detect → Decide → Verify → Defend → Verify**

A synthetic attack is detected, mapped to MITRE ATT&CK, evaluated against the six INVERIQ verification gates, and mitigated inside an isolated Docker laboratory. Unsafe actions are rejected before enforcement.

> Safety boundary: firewall enforcement is limited to the `inveriq-gateway` container. The demo does not install nftables rules on the host.

## Prerequisites

- Docker with Docker Compose
- Python 3.11+
- Project dependencies installed
- Streamlit
- A terminal capable of running Bash scripts

From the repository root, install the Python dependencies if required:

```bash
python -m pip install -r requirements.txt
```

## 1. Start the Expo dashboard

Open the first terminal in the repository root and run:

```bash
streamlit run dashboard/app.py
```

Keep this terminal running.

The dashboard displays:

- current demo stage;
- active threat;
- MITRE ATT&CK mapping;
- detection confidence;
- V1–V6 verification matrix;
- rejected and verified mitigation candidates;
- blast radius;
- Attacker → Gateway ← Trusted Client topology;
- total requests;
- login attempts;
- health checks;
- mitigation and post-verification status.

## 2. Run the guided demo

Open a second terminal in the repository root:

```bash
demo/run_demo.sh --keep-lab
```

The script performs the complete demonstration in sequence:

1. starts the isolated Docker lab;
2. resets the lab to a known state;
3. checks trusted/legitimate traffic;
4. starts the selected synthetic attack;
5. detects the threat;
6. maps the threat to MITRE ATT&CK;
7. creates mitigation candidates;
8. evaluates V1 Authorization;
9. evaluates V2 Target;
10. evaluates V3 Reachability;
11. evaluates V4 Availability;
12. evaluates V5 Blast Radius;
13. evaluates V6 Security Effectiveness;
14. rejects the deliberately unsafe mitigation;
15. selects a verified mitigation;
16. applies the verified nftables action inside `inveriq-gateway`;
17. performs post-mitigation verification;
18. updates the dashboard throughout the flow.

For the default scenario, the attack is Credential Brute Force mapped to MITRE ATT&CK T1110.

## 3. Quick rehearsal mode

To run the demo without pauses:

```bash
demo/run_demo.sh --no-pause --keep-lab
```

This is useful for repeated testing before the Expo.

## 4. Select an attack scenario

INVERIQ v0.5.0 supports three scenarios:

```bash
demo/run_demo.sh --scenario brute-force --keep-lab
demo/run_demo.sh --scenario ddos --keep-lab
demo/run_demo.sh --scenario exfiltration --keep-lab
```

The recommended public Expo demo is `brute-force`. DDoS and data exfiltration are secondary scenarios for technical discussions.

## 5. Demonstrate unsafe-action rejection

The demo deliberately includes an unsafe candidate. It can also be tested directly:

```bash
python scripts/lab_enforce.py --candidate MIT-UNSAFE
```

INVERIQ must reject it. It must never reach enforcement.

## 6. Demonstrate a verified action

For the brute-force scenario:

```bash
python scripts/lab_enforce.py --candidate MIT-RATE
```

The action is permitted only after the verification gates pass.

## 7. Inspect lab status

At any time:

```bash
python scripts/lab_status.py
```

This reports the state of the isolated lab and gateway.

## 8. Reset the environment

After a demonstration:

```bash
python scripts/lab_reset.py
```

Use this before a new presentation run.

## 9. Stop the Docker lab

When finished:

```bash
docker compose -f docker-compose.lab.yml down
```

## Recommended Expo workflow

Use two terminal windows plus the browser:

**Terminal 1**

```bash
streamlit run dashboard/app.py
```

**Terminal 2**

```bash
demo/run_demo.sh --scenario brute-force --keep-lab
```

**Browser**

Keep the INVERIQ dashboard full-screen.

## 90-second presentation flow

1. Show normal operation and trusted traffic.
2. Start the attack.
3. Show threat detection and MITRE mapping.
4. Show multiple mitigation candidates.
5. Highlight that the unsafe candidate could stop the attack but violates operational invariants.
6. Show INVERIQ rejecting it.
7. Show the verified candidate passing V1–V6.
8. Execute the verified mitigation.
9. Show attack reduction while legitimate connectivity remains available.
10. End with: **AI decides. INVERIQ verifies.**

## Verification gates

| Gate | Verification | Question |
|---|---|---|
| V1 | Authorization | Is the proposed action permitted? |
| V2 | Target | Does the action affect the correct entity? |
| V3 | Reachability | Do critical flows remain reachable? |
| V4 | Availability | Does the protected service remain available? |
| V5 | Blast Radius | Is legitimate impact within policy limits? |
| V6 | Security Effectiveness | Does the action actually mitigate the threat? |

Execution is allowed only when every required gate passes.

## Troubleshooting

If the lab is in an unexpected state:

```bash
python scripts/lab_reset.py
docker compose -f docker-compose.lab.yml down
docker compose -f docker-compose.lab.yml up --build -d
python scripts/lab_status.py
```

For a fast full rehearsal:

```bash
demo/run_demo.sh --scenario brute-force --no-pause --keep-lab
```

## Expo reliability rule

Do not add new functionality to the demo immediately before the event. The public demonstration should use a tested release candidate and should remain fully usable without external AI APIs or Internet connectivity.

---

**INVERIQ by Avernaut**  
Verified Autonomous Defense  
**AI decides. INVERIQ verifies.**
