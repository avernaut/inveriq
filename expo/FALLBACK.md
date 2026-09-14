# Demo Fallback Procedures

## Principle

Never troubleshoot publicly for more than a few seconds. If recovery is not immediate, switch to the backup path and continue the story.

## Level 0 — Normal

Run:

```bash
demo/run_demo.sh --scenario brute-force --keep-lab
```

## Level 1 — Dashboard issue

If Streamlit stops updating:

1. Keep the verbal explanation going.
2. In the dashboard terminal:

```bash
Ctrl+C
streamlit run dashboard/app.py
```

3. Refresh the browser.

If this takes too long, move directly to the backup video.

## Level 2 — Lab state is inconsistent

Run:

```bash
python scripts/lab_reset.py
python scripts/lab_status.py
```

If needed:

```bash
docker compose -f docker-compose.lab.yml down
docker compose -f docker-compose.lab.yml up --build -d
```

Then:

```bash
demo/run_demo.sh --scenario brute-force --no-pause --keep-lab
```

## Level 3 — Docker failure

Do not debug Docker at the booth.

Switch immediately to:

1. backup video;
2. static dashboard screenshots if available;
3. verbal explanation of the verification gates.

Say:

> The live lab is isolated for safety. I will show you the recorded end-to-end run while I explain exactly what is being verified.

## Level 4 — Laptop failure

Use the backup video stored on:

- secondary laptop if available;
- USB drive;
- phone/tablet as last resort.

Keep a PDF/PNG one-page on at least two devices.

## Level 5 — No Internet

No action required.

The public demo must work fully offline.

## Recovery after a failed demo

Before the next visitor:

```bash
docker compose -f docker-compose.lab.yml down
docker compose -f docker-compose.lab.yml up --build -d
python scripts/lab_reset.py
python scripts/lab_status.py
```

Run one rehearsal:

```bash
demo/run_demo.sh --scenario brute-force --no-pause --keep-lab
```

## Rule

A failed live run must never become the focus of the conversation. The product concept is the verification layer, not Docker.
