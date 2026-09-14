#!/usr/bin/env python3
"""Safe failure injection inside the isolated Docker lab."""
from __future__ import annotations
import argparse
import subprocess

def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    print(p.stdout or p.stderr)
    return p.returncode

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["gateway-restart","trusted-client-restart","attacker-restart"], required=True)
    args = ap.parse_args()

    service = {
        "gateway-restart": "gateway",
        "trusted-client-restart": "trusted-client",
        "attacker-restart": "attacker",
    }[args.mode]

    print(f"Injecting isolated failure: restart {service}")
    raise SystemExit(run(["docker","compose","-f","docker-compose.lab.yml","restart",service]))

if __name__ == "__main__":
    main()
