#!/usr/bin/env python3
"""Collect real lab telemetry from the isolated Docker testbed."""
from __future__ import annotations
import argparse
import json
import subprocess
import time
from pathlib import Path
from typing import Any

STATE = Path(".demo-state")
STATE.mkdir(exist_ok=True)
OUT = STATE / "instrumentation.json"

def run(cmd: list[str], timeout: int = 10) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout or p.stderr).strip()
    except Exception as exc:
        return 1, str(exc)

def compose_exec(service: str, args: list[str]) -> tuple[int, str]:
    return run(["docker", "compose", "-f", "docker-compose.lab.yml", "exec", "-T", service] + args)

def curl_latency(service: str, url: str) -> dict[str, Any]:
    code, out = compose_exec(service, [
        "sh", "-lc",
        f"""curl -sS -o /dev/null -w '%{{http_code}} %{{time_total}}' {url}"""
    ])
    if code != 0:
        return {"ok": False, "http_code": 0, "latency_ms": None, "raw": out}
    parts = out.split()
    try:
        return {
            "ok": parts[0].startswith("2"),
            "http_code": int(parts[0]),
            "latency_ms": round(float(parts[1]) * 1000, 3),
            "raw": out,
        }
    except Exception:
        return {"ok": False, "http_code": 0, "latency_ms": None, "raw": out}

def nft_counters() -> dict[str, Any]:
    code, out = compose_exec("gateway", ["sh", "-lc", "nft -j list ruleset"])
    if code != 0:
        return {"ok": False, "raw": out, "packets": None, "bytes": None}
    try:
        data = json.loads(out)
        packets = 0
        byte_count = 0
        for item in data.get("nftables", []):
            rule = item.get("rule")
            if not rule:
                continue
            for expr in rule.get("expr", []):
                counter = expr.get("counter") if isinstance(expr, dict) else None
                if counter:
                    packets += int(counter.get("packets", 0))
                    byte_count += int(counter.get("bytes", 0))
        return {"ok": True, "packets": packets, "bytes": byte_count}
    except Exception as exc:
        return {"ok": False, "raw": str(exc), "packets": None, "bytes": None}

def container_stats(service: str) -> dict[str, Any]:
    code, cid = run(["docker", "compose", "-f", "docker-compose.lab.yml", "ps", "-q", service])
    if code != 0 or not cid:
        return {"ok": False}
    code, out = run(["docker", "stats", "--no-stream", "--format",
                     '{"cpu":"{{.CPUPerc}}","mem":"{{.MemUsage}}","net":"{{.NetIO}}"}', cid])
    if code != 0:
        return {"ok": False, "raw": out}
    try:
        d = json.loads(out)
        d["ok"] = True
        return d
    except Exception:
        return {"ok": False, "raw": out}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--label", default="snapshot")
    args = p.parse_args()

    started = time.perf_counter_ns()
    trusted = curl_latency("trusted-client", "http://gateway:8080/health")
    attacker_view = curl_latency("attacker", "http://gateway:8080/health")
    counters = nft_counters()
    gw_stats = container_stats("gateway")
    elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000

    result = {
        "label": args.label,
        "timestamp_ns": time.time_ns(),
        "collection_latency_ms": round(elapsed_ms, 3),
        "trusted_health": trusted,
        "attacker_health": attacker_view,
        "nftables": counters,
        "gateway_stats": gw_stats,
    }
    OUT.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
