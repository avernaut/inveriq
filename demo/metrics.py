"""Measurement and evidence utilities for the INVERIQ Expo demo."""
from __future__ import annotations
import csv
import json
import statistics
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

REPORT_DIR = Path(".demo-state/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

@dataclass
class DemoMetrics:
    run_id: str
    timestamp: str
    scenario: str
    detection_latency_ms: float
    decision_latency_ms: float
    verification_latency_ms: float
    enforcement_latency_ms: float
    total_response_latency_ms: float
    attack_rate_before: float
    attack_rate_after: float
    attack_reduction_pct: float
    legitimate_rate_before: float
    legitimate_rate_after: float
    availability_pct: float
    blast_radius_pct: float
    unsafe_action_rejected: bool
    verified_action_executed: bool

    def to_dict(self):
        return asdict(self)

def new_run_id(scenario: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}-{scenario}"

def save_metrics(metrics: DemoMetrics) -> tuple[Path, Path]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORT_DIR / f"{metrics.run_id}.json"
    csv_path = REPORT_DIR / "runs.csv"

    json_path.write_text(json.dumps(metrics.to_dict(), indent=2))

    exists = csv_path.exists()
    with csv_path.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(metrics.to_dict().keys()))
        if not exists:
            writer.writeheader()
        writer.writerow(metrics.to_dict())
    return json_path, csv_path

def load_all_metrics() -> list[dict]:
    csv_path = REPORT_DIR / "runs.csv"
    if not csv_path.exists():
        return []
    with csv_path.open(newline="") as f:
        return list(csv.DictReader(f))

def summarize(rows: Iterable[dict]) -> dict:
    rows = list(rows)
    if not rows:
        return {}
    numeric = [
        "detection_latency_ms",
        "decision_latency_ms",
        "verification_latency_ms",
        "enforcement_latency_ms",
        "total_response_latency_ms",
        "attack_reduction_pct",
        "availability_pct",
        "blast_radius_pct",
    ]
    summary = {"runs": len(rows)}
    for key in numeric:
        vals = [float(r[key]) for r in rows if r.get(key) not in (None, "")]
        if vals:
            summary[key] = {
                "mean": round(statistics.mean(vals), 3),
                "min": round(min(vals), 3),
                "max": round(max(vals), 3),
            }
    return summary
