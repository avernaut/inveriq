# Expo Readiness Checklist

## 7–10 days before departure

- [ ] `v0.9.0-expo-rc1` is tagged and frozen.
- [ ] 100-run brute-force reliability test completed.
- [ ] DDoS and exfiltration scenarios tested.
- [ ] `reports/expo-rc-report.md` generated and reviewed.
- [ ] Dashboard works without Internet access.
- [ ] Docker images are built locally.
- [ ] All Python dependencies are installed locally.
- [ ] No external LLM/API is required for the public demo.
- [ ] Backup video recorded.
- [ ] Backup video copied to laptop and USB drive.
- [ ] Repository clone exists locally.
- [ ] Offline ZIP backup of repository exists locally.
- [ ] Printed/QR one-page product overview prepared.
- [ ] Laptop charger packed.
- [ ] HDMI/USB-C adapters packed.
- [ ] Power bank packed if used.
- [ ] Spare mouse / presenter packed if useful.

## Day before the event

- [ ] Run `demo/run_expo_rc.sh brute-force`.
- [ ] Run dashboard full-screen.
- [ ] Confirm Docker starts after laptop reboot.
- [ ] Confirm display resolution and scaling.
- [ ] Disable automatic OS updates.
- [ ] Disable sleep while on AC power.
- [ ] Disable distracting notifications.
- [ ] Confirm browser has no unnecessary tabs.
- [ ] Confirm backup video opens locally.
- [ ] Confirm all files work with Wi-Fi disabled.
- [ ] Charge laptop and peripherals to 100%.

## Before opening the booth

- [ ] Connect power.
- [ ] Connect external monitor if available.
- [ ] Start Docker.
- [ ] Start Streamlit dashboard.
- [ ] Run a rehearsal with `--no-pause`.
- [ ] Reset lab.
- [ ] Keep Terminal 1 = dashboard.
- [ ] Keep Terminal 2 = demo runner.
- [ ] Open dashboard full-screen.
- [ ] Open backup video in a separate hidden window.
- [ ] Confirm contact QR / website is visible.

## Before each live demo

- [ ] Run `python scripts/lab_reset.py`.
- [ ] Confirm trusted service is healthy.
- [ ] Confirm dashboard is on the initial state.
- [ ] Confirm demo scenario is `brute-force`.
- [ ] Close unrelated windows.
- [ ] Start pitch only after baseline state is visible.

## End of each day

- [ ] Export latest engineering report.
- [ ] Copy lead notes.
- [ ] Backup `.demo-state/reports/`.
- [ ] Stop Docker cleanly.
- [ ] Recharge all devices.
- [ ] Review recurring questions for next day.
