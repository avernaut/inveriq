#!/usr/bin/env python3
"""Export a compact JSON and Markdown engineering report for the Expo RC."""
from __future__ import annotations
import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

OUT = Path("reports")
OUT.mkdir(exist_ok=True)

def last_row(path):
    p = Path(path)
    if not p.exists():
        return None
    rows = list(csv.DictReader(p.open()))
    return rows[-1] if rows else None

def main():
    latest_eff = last_row(".demo-state/reports/effectiveness.csv")
    latest_real = last_row(".demo-state/reports/runs-real.csv")
    stats = {}
    p = subprocess.run([sys.executable, "scripts/aggregate_stats.py"], capture_output=True, text=True)
    if p.returncode == 0 and p.stdout.strip():
        stats = json.loads(p.stdout)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "release": "0.9.0",
        "latest_effectiveness": latest_eff,
        "latest_real_instrumentation": latest_real,
        "aggregate_statistics": stats,
        "safety_boundary": "All enforcement remains inside the isolated inveriq-gateway container.",
    }

    (OUT / "expo-rc-report.json").write_text(json.dumps(report, indent=2))

    lines = [
        "# INVERIQ v0.9.0 — Expo Release Candidate Report",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Safety boundary",
        "",
        report["safety_boundary"],
        "",
        "## Latest effectiveness run",
        "",
        "```json",
        json.dumps(latest_eff, indent=2) if latest_eff else "No data",
        "```",
        "",
        "## Latest real instrumentation run",
        "",
        "```json",
        json.dumps(latest_real, indent=2) if latest_real else "No data",
        "```",
        "",
        "## Aggregate statistics",
        "",
        "```json",
        json.dumps(stats, indent=2),
        "```",
    ]
    (OUT / "expo-rc-report.md").write_text("\n".join(lines))
    print("reports/expo-rc-report.json")
    print("reports/expo-rc-report.md")

if __name__ == "__main__":
    main()
