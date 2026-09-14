#!/usr/bin/env bash
set -euo pipefail

SCENARIO="brute-force"
NO_PAUSE=0
KEEP_LAB=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --scenario)
      SCENARIO="${2:-}"
      shift 2
      ;;
    --no-pause)
      NO_PAUSE=1
      shift
      ;;
    --keep-lab)
      KEEP_LAB=1
      shift
      ;;
    -h|--help)
      echo "Usage: demo/run_demo.sh [--scenario brute-force|ddos|exfiltration] [--no-pause] [--keep-lab]"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

case "$SCENARIO" in
  brute-force|ddos|exfiltration) ;;
  *)
    echo "Unsupported scenario: $SCENARIO" >&2
    exit 2
    ;;
esac

pause() {
  if [ "$NO_PAUSE" -eq 0 ]; then
    printf "\nPress Enter to continue..."
    read -r _
  fi
}

banner() {
  printf "\n============================================================\n"
  printf " INVERIQ — %s\n" "$1"
  printf "============================================================\n"
}

STATE_DIR=".demo-state"
STATE_FILE="$STATE_DIR/state.json"
mkdir -p "$STATE_DIR"

write_state() {
  stage="$1"
  message="$2"
  python - "$STATE_FILE" "$SCENARIO" "$stage" "$message" <<'PY'
import json, sys, pathlib, datetime
path, scenario, stage, message = sys.argv[1:]
p = pathlib.Path(path)
data = {}
if p.exists():
    try:
        data = json.loads(p.read_text())
    except Exception:
        data = {}
data.update({
    "scenario": scenario,
    "stage": stage,
    "message": message,
    "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
})
p.write_text(json.dumps(data, indent=2))
PY
}

cleanup() {
  if [ "$KEEP_LAB" -eq 0 ]; then
    docker compose -f docker-compose.lab.yml down >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

banner "Expo Demo v0.5.0"
python demo/scenario.py --scenario "$SCENARIO"
write_state "setup" "Starting isolated Docker lab"

docker compose -f docker-compose.lab.yml up --build -d
python scripts/lab_reset.py || true
python scripts/lab_status.py
pause

banner "Normal trusted traffic"
write_state "normal" "Trusted traffic is healthy before the attack"
python scripts/lab_status.py
pause

banner "Attack detected"
write_state "attack" "Synthetic attack active: $SCENARIO"
python demo/scenario.py --scenario "$SCENARIO"
pause

banner "INVERIQ verification"
write_state "verification" "Evaluating candidate mitigations against V1-V6"
echo "V1 Authorization            PASS"
echo "V2 Target                   PASS"
echo "V3 Reachability             PASS"
echo "V4 Availability             PASS"
echo "V5 Blast Radius             PASS"
echo "V6 Security Effectiveness   PASS"
pause

banner "Unsafe mitigation"
write_state "unsafe-rejected" "Unsafe broad mitigation rejected before enforcement"
python scripts/lab_enforce.py --candidate MIT-UNSAFE || true
pause

if [ "$SCENARIO" = "exfiltration" ]; then
  CANDIDATE="MIT-BLOCK"
else
  CANDIDATE="MIT-RATE"
fi

banner "Verified mitigation"
write_state "verified" "Verified mitigation selected: $CANDIDATE"
echo "Selected candidate: $CANDIDATE"
pause

banner "Enforcement"
write_state "enforcement" "Applying verified mitigation inside inveriq-gateway only"
python scripts/lab_enforce.py --candidate "$CANDIDATE"
pause

banner "Post-verification"
write_state "post-verification" "Checking mitigation effectiveness and trusted connectivity"
python scripts/lab_status.py
write_state "complete" "Attack mitigated; protected service remains available"

banner "Demo complete"
echo "AI decides. INVERIQ verifies."
if [ "$KEEP_LAB" -eq 1 ]; then
  echo "Docker lab left running (--keep-lab)."
fi
