#!/usr/bin/env python3
"""Read/write the local Expo demo state consumed by the Streamlit console."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path(".demo-state.json")

DEFAULT_STATE = {
    "stage": "READY",
    "message": "Demo ready",
    "candidate": None,
    "decision": None,
    "updated_at": None,
}


def load_state() -> dict:
    if not STATE_FILE.exists():
        return DEFAULT_STATE.copy()
    try:
        return {**DEFAULT_STATE, **json.loads(STATE_FILE.read_text())}
    except (json.JSONDecodeError, OSError):
        return DEFAULT_STATE.copy()


def save_state(stage: str, message: str, candidate: str | None = None, decision: str | None = None) -> dict:
    state = {
        "stage": stage,
        "message": message,
        "candidate": candidate,
        "decision": decision,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")
    return state


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage")
    parser.add_argument("--message", default="")
    parser.add_argument("--candidate")
    parser.add_argument("--decision")
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()

    if args.reset:
        if STATE_FILE.exists():
            STATE_FILE.unlink()
        print(json.dumps(DEFAULT_STATE, indent=2))
        return 0
    if args.show or not args.stage:
        print(json.dumps(load_state(), indent=2))
        return 0

    print(json.dumps(save_state(args.stage, args.message, args.candidate, args.decision), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
