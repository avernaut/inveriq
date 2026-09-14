# IoT Tech Expo demo flow — v0.4

## One-command demo

Run the dashboard in one terminal:

```bash
streamlit run dashboard/app.py
```

Run the complete lab scenario in a second terminal:

```bash
demo/run_demo.sh --keep-lab
```

For rehearsal without presentation pauses:

```bash
demo/run_demo.sh --no-pause --keep-lab
```

Stop the lab when finished:

```bash
docker compose -f docker-compose.lab.yml down
```

## Scripted stages

1. **SETUP** — reset and start the isolated Docker lab.
2. **BASELINE** — demonstrate trusted health traffic reaching the protected authentication API.
3. **DETECT** — show credential brute force mapped to MITRE ATT&CK T1110.
4. **VERIFY** — evaluate three candidate mitigations through V1–V6.
5. **REJECT** — attempt `MIT-UNSAFE`; INVERIQ refuses enforcement.
6. **ENFORCE** — execute `MIT-RATE` inside `inveriq-gateway` only.
7. **POSTVERIFY** — show post-mitigation telemetry and operational availability.
8. **COMPLETE** — reset the INVERIQ nftables table and leave the demo in a safe state.

The Streamlit console reads `.demo-state.json` written by `demo/run_demo.sh` and refreshes live while displaying gateway metrics from port `18080`.

## Safety boundary

No demo path installs nftables rules on the host. Enforcement is limited to the Docker container named `inveriq-gateway`, which alone receives `NET_ADMIN` in the lab compose file.

Target speaking time: 90 seconds. Target full interactive demonstration: under 3 minutes.
