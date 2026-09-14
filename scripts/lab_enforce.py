#!/usr/bin/env python3
"""Apply one verified mitigation inside the isolated Docker gateway only."""
from __future__ import annotations
import argparse
import subprocess

from inveriq.detection.detector import demo_bruteforce_event
from inveriq.enforcement.nftables import build_plan
from inveriq.intent.policy import load_policy
from inveriq.response.generator import generate_candidates
from inveriq.verification.engine import verify


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", default="MIT-RATE", choices=["MIT-BLOCK", "MIT-RATE", "MIT-UNSAFE"])
    args = parser.parse_args()

    threat = demo_bruteforce_event()
    policy = load_policy()
    candidate = next(c for c in generate_candidates(threat) if c.id == args.candidate)
    result = verify(candidate, threat, policy)
    plan = build_plan(candidate, verified=result.decision == "VERIFIED", lab_mode=True)

    print(f"candidate={candidate.id} decision={result.decision}")
    print(f"command={plan.command}")
    if not plan.executable:
        print("enforcement=SKIPPED")
        return 2 if result.decision == "REJECTED" else 0

    run(["docker", "exec", "inveriq-gateway", "sh", "-lc", plan.command])
    print("enforcement=APPLIED inside inveriq-gateway")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
