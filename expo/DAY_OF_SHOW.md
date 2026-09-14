# Day-of-Show Operating Procedure

## 60 minutes before opening

1. Connect laptop to power.
2. Connect external display.
3. Disable Wi-Fi temporarily.
4. Start Docker.
5. Run:

```bash
demo/run_expo_rc.sh brute-force
```

6. Confirm report generation.
7. Start:

```bash
streamlit run dashboard/app.py
```

8. Run one live rehearsal:

```bash
demo/run_demo.sh --scenario brute-force --no-pause --keep-lab
```

9. Reset:

```bash
python scripts/lab_reset.py
```

10. Re-enable Wi-Fi only if needed for normal event use.

## During the event

Default visitor demo:

```bash
demo/run_demo.sh --scenario brute-force --keep-lab
```

For technical visitors:

```bash
demo/run_demo.sh --scenario ddos --keep-lab
```

or:

```bash
demo/run_demo.sh --scenario exfiltration --keep-lab
```

## After 5–10 demonstrations

Check:

```bash
python scripts/lab_status.py
```

If state looks inconsistent, restart the isolated lab.

## Midday

- restart dashboard if memory use is excessive;
- export reports;
- verify backup video;
- recharge peripherals.

## End of day

Run:

```bash
python scripts/export_expo_report.py
```

Then:

```bash
docker compose -f docker-compose.lab.yml down
```

Copy `.demo-state/reports/` to backup storage.

## Visitor qualification questions

Ask one or two, not all:

- How much of your incident response is currently automated?
- Would you allow AI to apply mitigation actions directly in production?
- What would you need to verify before allowing autonomous response?
- Which infrastructure is most sensitive to unintended security changes?
- Are availability or connectivity constraints part of your response playbooks?

Record the answers after the conversation, not during the technical demo.
