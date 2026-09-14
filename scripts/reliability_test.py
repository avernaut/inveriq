#!/usr/bin/env python3
"""Repeated reliability runner for the isolated INVERIQ demo lab."""
from __future__ import annotations
import argparse
import csv
import json
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

OUT_DIR = Path(".demo-state/reliability")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def run_once(scenario: str) -> dict:
    t0 = time.perf_counter_ns()
    p = subprocess.run(
        [sys.executable, "scripts/benchmark_effectiveness.py", "--scenario", scenario],
        capture_output=True, text=True
    )
    elapsed = (time.perf_counter_ns() - t0) / 1_000_000
    ok = p.returncode == 0
    return {
        "ok": ok,
        "elapsed_ms": round(elapsed, 3),
        "stdout": p.stdout[-1000:],
        "stderr": p.stderr[-1000:],
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", choices=["brute-force","ddos","exfiltration"], default="brute-force")
    ap.add_argument("--runs", type=int, default=100)
    args = ap.parse_args()

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + args.scenario
    rows = []
    for i in range(1, args.runs + 1):
        result = run_once(args.scenario)
        row = {
            "index": i,
            "scenario": args.scenario,
            "ok": result["ok"],
            "elapsed_ms": result["elapsed_ms"],
        }
        rows.append(row)
        print(f"[{i}/{args.runs}] {'PASS' if result['ok'] else 'FAIL'} {result['elapsed_ms']:.1f} ms")

    csv_path = OUT_DIR / f"{run_id}.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    passed = sum(1 for r in rows if r["ok"])
    summary = {
        "run_id": run_id,
        "scenario": args.scenario,
        "runs": args.runs,
        "passed": passed,
        "failed": args.runs - passed,
        "success_rate_pct": round(passed / args.runs * 100.0, 3),
        "mean_elapsed_ms": round(sum(r["elapsed_ms"] for r in rows) / len(rows), 3),
    }
    json_path = OUT_DIR / f"{run_id}.json"
    json_path.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
