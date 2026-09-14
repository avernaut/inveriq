"""Scenario catalog for the INVERIQ Expo demo."""
from __future__ import annotations
import json
from pathlib import Path

SCENARIO_FILE = Path(__file__).with_name("scenarios.json")

def load_scenarios():
    return json.loads(SCENARIO_FILE.read_text())

def get_scenario(name: str):
    scenarios = load_scenarios()
    if name not in scenarios:
        raise KeyError(f"Unknown scenario: {name}")
    return scenarios[name]

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--scenario", choices=sorted(load_scenarios()), default="brute-force")
    args = p.parse_args()
    s = get_scenario(args.scenario)
    print(json.dumps(s, indent=2))
