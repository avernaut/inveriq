import csv
import json
from pathlib import Path
from demo.metrics import DemoMetrics, save_metrics, summarize

def test_metrics_summary_basic(tmp_path, monkeypatch):
    import demo.metrics as m
    monkeypatch.setattr(m, "REPORT_DIR", tmp_path)
    x = DemoMetrics(
        run_id="r1", timestamp="2026-09-14T00:00:00Z", scenario="brute-force",
        detection_latency_ms=100, decision_latency_ms=20,
        verification_latency_ms=30, enforcement_latency_ms=40,
        total_response_latency_ms=190, attack_rate_before=500,
        attack_rate_after=10, attack_reduction_pct=98,
        legitimate_rate_before=120, legitimate_rate_after=120,
        availability_pct=100, blast_radius_pct=0.4,
        unsafe_action_rejected=True, verified_action_executed=True,
    )
    jp, cp = save_metrics(x)
    assert jp.exists() and cp.exists()
    rows = list(csv.DictReader(cp.open()))
    s = summarize(rows)
    assert s["runs"] == 1
    assert s["attack_reduction_pct"]["mean"] == 98.0
