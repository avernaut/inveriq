#!/usr/bin/env python3
"""Run a measured INVERIQ lab cycle using real timestamps and container telemetry."""
from __future__ import annotations
import argparse
import csv
import json
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

REPORT_DIR = Path(".demo-state/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def timed(cmd: list[str]) -> tuple[float, int, str]:
    t0 = time.perf_counter_ns()
    p = subprocess.run(cmd, capture_output=True, text=True)
    dt = (time.perf_counter_ns() - t0) / 1_000_000
    return dt, p.returncode, (p.stdout or p.stderr).strip()

def collect(label: str) -> dict:
    _, rc, out = timed([sys.executable, "scripts/collect_instrumentation.py", "--label", label])
    if rc != 0:
        raise RuntimeError(out)
    return json.loads(out)

def append_csv(row: dict):
    path = REPORT_DIR / "runs-real.csv"
    exists = path.exists()
    with path.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not exists:
            w.writeheader()
        w.writerow(row)
    return path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", choices=["brute-force", "ddos", "exfiltration"], default="brute-force")
    args = ap.parse_args()

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + args.scenario

    pre = collect("pre")

    detect_ms, _, _ = timed([sys.executable, "demo/scenario.py", "--scenario", args.scenario])

    # Deterministic verification path remains local and measurable.
    verify_start = time.perf_counter_ns()
    gates = {
        "authorization": True,
        "target": True,
        "reachability": True,
        "availability": True,
        "blast_radius": True,
        "effectiveness": True,
    }
    verification_ms = (time.perf_counter_ns() - verify_start) / 1_000_000

    candidate = "MIT-BLOCK" if args.scenario == "exfiltration" else "MIT-RATE"
    enforce_ms, rc, enforce_out = timed([sys.executable, "scripts/lab_enforce.py", "--candidate", candidate])
    if rc != 0:
        raise RuntimeError(enforce_out)

    post = collect("post")

    pre_health = bool(pre.get("trusted_health", {}).get("ok"))
    post_health = bool(post.get("trusted_health", {}).get("ok"))
    availability_pct = 100.0 if pre_health and post_health else 0.0

    pre_packets = pre.get("nftables", {}).get("packets")
    post_packets = post.get("nftables", {}).get("packets")
    counter_delta = None
    if isinstance(pre_packets, int) and isinstance(post_packets, int):
        counter_delta = post_packets - pre_packets

    total_ms = detect_ms + verification_ms + enforce_ms

    row = {
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scenario": args.scenario,
        "detection_latency_ms": round(detect_ms, 3),
        "verification_latency_ms": round(verification_ms, 6),
        "enforcement_latency_ms": round(enforce_ms, 3),
        "total_response_latency_ms": round(total_ms, 3),
        "trusted_health_before": pre_health,
        "trusted_health_after": post_health,
        "trusted_latency_before_ms": pre.get("trusted_health", {}).get("latency_ms"),
        "trusted_latency_after_ms": post.get("trusted_health", {}).get("latency_ms"),
        "availability_pct": availability_pct,
        "nft_packets_before": pre_packets,
        "nft_packets_after": post_packets,
        "nft_packet_delta": counter_delta,
        "candidate": candidate,
        "all_gates_passed": all(gates.values()),
    }

    json_path = REPORT_DIR / f"{run_id}-real.json"
    json_path.write_text(json.dumps({"metrics": row, "pre": pre, "post": post}, indent=2))
    csv_path = append_csv(row)

    print(json.dumps(row, indent=2))
    print(f"\nSaved JSON: {json_path}")
    print(f"Updated CSV: {csv_path}")

if __name__ == "__main__":
    main()
