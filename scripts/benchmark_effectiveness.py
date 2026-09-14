#!/usr/bin/env python3
"""Measure mitigation effectiveness using real generated traffic."""
from __future__ import annotations
import argparse
import csv
import json
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

REPORT_DIR = Path(".demo-state/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def run_json(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stdout or p.stderr)
    return json.loads(p.stdout)

def timed(cmd):
    t0 = time.perf_counter_ns()
    p = subprocess.run(cmd, capture_output=True, text=True)
    return (time.perf_counter_ns()-t0)/1_000_000, p

def append_csv(row):
    path = REPORT_DIR / "effectiveness.csv"
    exists = path.exists()
    with path.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row))
        if not exists:
            w.writeheader()
        w.writerow(row)
    return path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", choices=["brute-force","ddos","exfiltration"], default="brute-force")
    ap.add_argument("--count", type=int, default=40)
    args = ap.parse_args()

    # baseline
    subprocess.run([sys.executable, "scripts/lab_reset.py"], check=False)
    before = run_json([sys.executable, "scripts/traffic_generator.py",
                       "--scenario", args.scenario, "--count", str(args.count)])

    candidate = "MIT-BLOCK" if args.scenario == "exfiltration" else "MIT-RATE"
    enforce_ms, p = timed([sys.executable, "scripts/lab_enforce.py", "--candidate", candidate])
    if p.returncode != 0:
        raise RuntimeError(p.stdout or p.stderr)

    after = run_json([sys.executable, "scripts/traffic_generator.py",
                      "--scenario", args.scenario, "--count", str(args.count)])

    # trusted service check
    trusted = subprocess.run(
        ["docker","compose","-f","docker-compose.lab.yml","exec","-T","trusted-client",
         "sh","-lc","curl -s -o /dev/null -w '%{http_code}' http://gateway:8080/health"],
        capture_output=True, text=True
    )
    trusted_ok = trusted.returncode == 0 and (trusted.stdout or "").strip().startswith("2")

    before_rate = float(before["requests_per_s"])
    after_rate = float(after["requests_per_s"])
    reduction = 0.0
    if before_rate > 0:
        reduction = max(0.0, min(100.0, (before_rate-after_rate)/before_rate*100.0))

    before_success = float(before["success_rate_pct"])
    after_success = float(after["success_rate_pct"])
    success_reduction = max(0.0, before_success-after_success)

    row = {
        "run_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+args.scenario,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scenario": args.scenario,
        "candidate": candidate,
        "attempts": args.count,
        "attack_rps_before": round(before_rate, 3),
        "attack_rps_after": round(after_rate, 3),
        "attack_rate_reduction_pct": round(reduction, 3),
        "attack_success_before_pct": round(before_success, 3),
        "attack_success_after_pct": round(after_success, 3),
        "attack_success_reduction_points": round(success_reduction, 3),
        "enforcement_latency_ms": round(enforce_ms, 3),
        "trusted_service_available": trusted_ok,
        "availability_pct": 100.0 if trusted_ok else 0.0,
    }

    jp = REPORT_DIR / f"{row['run_id']}-effectiveness.json"
    jp.write_text(json.dumps({"summary": row, "before": before, "after": after}, indent=2))
    cp = append_csv(row)
    print(json.dumps(row, indent=2))
    print(f"\nSaved JSON: {jp}")
    print(f"Updated CSV: {cp}")

if __name__ == "__main__":
    main()
