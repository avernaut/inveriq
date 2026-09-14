#!/usr/bin/env python3
"""Generate isolated demo traffic from the attacker container."""
from __future__ import annotations
import argparse
import json
import subprocess
import time
from dataclasses import dataclass, asdict

@dataclass
class TrafficResult:
    scenario: str
    duration_s: float
    attempted: int
    succeeded: int
    failed: int
    requests_per_s: float
    success_rate_pct: float

def compose_exec(service: str, shell_cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["docker", "compose", "-f", "docker-compose.lab.yml", "exec", "-T", service, "sh", "-lc", shell_cmd],
        capture_output=True, text=True
    )

def brute_force(count: int) -> TrafficResult:
    t0 = time.perf_counter()
    succeeded = 0
    for _ in range(count):
        p = compose_exec("attacker", "curl -s -o /dev/null -w '%{http_code}' -X POST http://gateway:8080/login -d 'u=admin&p=wrong'")
        if p.returncode == 0 and (p.stdout or "").strip().startswith(("2","4")):
            succeeded += 1
    dt = max(time.perf_counter() - t0, 1e-9)
    return TrafficResult("brute-force", dt, count, succeeded, count-succeeded, count/dt, succeeded/count*100 if count else 0)

def ddos(count: int) -> TrafficResult:
    t0 = time.perf_counter()
    succeeded = 0
    for _ in range(count):
        p = compose_exec("attacker", "curl -s -o /dev/null -w '%{http_code}' http://gateway:8080/health")
        if p.returncode == 0 and (p.stdout or "").strip().startswith("2"):
            succeeded += 1
    dt = max(time.perf_counter() - t0, 1e-9)
    return TrafficResult("ddos", dt, count, succeeded, count-succeeded, count/dt, succeeded/count*100 if count else 0)

def exfiltration(count: int, payload_size: int) -> TrafficResult:
    t0 = time.perf_counter()
    succeeded = 0
    cmd = (
        "python - <<'PY'\n"
        "import urllib.request\n"
        f"data=b'x'*{payload_size}\n"
        "req=urllib.request.Request('http://gateway:8080/exfil', data=data, method='POST')\n"
        "try:\n"
        "    r=urllib.request.urlopen(req, timeout=3)\n"
        "    print(r.getcode())\n"
        "except Exception as e:\n"
        "    print('ERR')\n"
        "PY"
    )
    for _ in range(count):
        p = compose_exec("attacker", cmd)
        if p.returncode == 0 and "200" in (p.stdout or ""):
            succeeded += 1
    dt = max(time.perf_counter() - t0, 1e-9)
    return TrafficResult("exfiltration", dt, count, succeeded, count-succeeded, count/dt, succeeded/count*100 if count else 0)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", choices=["brute-force","ddos","exfiltration"], required=True)
    ap.add_argument("--count", type=int, default=40)
    ap.add_argument("--payload-size", type=int, default=8192)
    args = ap.parse_args()

    if args.scenario == "brute-force":
        res = brute_force(args.count)
    elif args.scenario == "ddos":
        res = ddos(args.count)
    else:
        res = exfiltration(args.count, args.payload_size)
    print(json.dumps(asdict(res), indent=2))

if __name__ == "__main__":
    main()
