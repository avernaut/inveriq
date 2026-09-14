#!/usr/bin/env python3
"""Aggregate INVERIQ benchmark statistics with 95% confidence intervals."""
from __future__ import annotations
import csv
import json
import math
import statistics
from pathlib import Path

FILES = [
    Path(".demo-state/reports/effectiveness.csv"),
    Path(".demo-state/reports/runs-real.csv"),
]

def ci95(values):
    values = [float(v) for v in values]
    n = len(values)
    if n == 0:
        return None
    mean = statistics.mean(values)
    if n == 1:
        return {"n": 1, "mean": mean, "ci95_low": mean, "ci95_high": mean}
    stdev = statistics.stdev(values)
    half = 1.96 * stdev / math.sqrt(n)
    return {"n": n, "mean": mean, "ci95_low": mean-half, "ci95_high": mean+half}

def main():
    out = {}
    eff = FILES[0]
    if eff.exists():
        rows = list(csv.DictReader(eff.open()))
        for key in ["attack_rate_reduction_pct","attack_success_before_pct",
                    "attack_success_after_pct","enforcement_latency_ms",
                    "availability_pct"]:
            vals = [r[key] for r in rows if r.get(key) not in ("", None)]
            if vals:
                out[key] = ci95(vals)

    real = FILES[1]
    if real.exists():
        rows = list(csv.DictReader(real.open()))
        for key in ["detection_latency_ms","verification_latency_ms",
                    "enforcement_latency_ms","total_response_latency_ms",
                    "availability_pct"]:
            vals = [r[key] for r in rows if r.get(key) not in ("", None)]
            if vals:
                out[f"real_{key}"] = ci95(vals)

    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
