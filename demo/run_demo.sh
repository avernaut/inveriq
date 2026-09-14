#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

COMPOSE=(docker compose -f docker-compose.lab.yml)
PAUSE="${DEMO_PAUSE:-2}"
NO_PAUSE=0
KEEP_LAB=0

usage() {
  cat <<'EOF'
Usage: demo/run_demo.sh [--no-pause] [--keep-lab]

Runs the complete INVERIQ Expo lab demonstration:
  1. Reset and start isolated Docker lab
  2. Show normal/trusted traffic
  3. Detect synthetic brute-force threat (MITRE T1110)
  4. Compare mitigation candidates with V1-V6
  5. Demonstrate unsafe mitigation rejection
  6. Enforce verified rate limit inside inveriq-gateway only
  7. Show post-mitigation status
  8. Reset nftables state

Environment:
  DEMO_PAUSE=<seconds>  Delay between presentation stages (default: 2)
EOF
}

for arg in "$@"; do
  case "$arg" in
    --no-pause) NO_PAUSE=1 ;;
    --keep-lab) KEEP_LAB=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $arg" >&2; usage; exit 2 ;;
  esac
done

pause() {
  if [[ "$NO_PAUSE" -eq 0 ]]; then sleep "$PAUSE"; fi
}

stage() {
  local id="$1" message="$2"
  printf '\n\033[1;36m==> %s: %s\033[0m\n' "$id" "$message"
  python scripts/demo_state.py --stage "$id" --message "$message" >/dev/null
  pause
}

cleanup() {
  if [[ "$KEEP_LAB" -eq 0 ]]; then
    "${COMPOSE[@]}" down --remove-orphans >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

command -v docker >/dev/null || { echo "Docker is required." >&2; exit 1; }
docker info >/dev/null 2>&1 || { echo "Docker daemon is not running." >&2; exit 1; }

printf '\nINVERIQ v0.4 Expo Demo — Avernaut\n'
printf 'Safety boundary: enforcement occurs only inside container inveriq-gateway.\n'

stage "SETUP" "Starting isolated IoT/Edge lab"
"${COMPOSE[@]}" down --remove-orphans >/dev/null 2>&1 || true
"${COMPOSE[@]}" up --build -d
python scripts/lab_reset.py >/dev/null

stage "BASELINE" "Trusted traffic is reaching the protected authentication service"
python scripts/lab_status.py

stage "DETECT" "Credential brute-force activity detected and mapped to MITRE ATT&CK T1110"
python - <<'PY'
from inveriq.detection.detector import demo_bruteforce_event
print(demo_bruteforce_event().model_dump_json(indent=2))
PY

stage "VERIFY" "Evaluating three candidate mitigations through V1-V6"
python - <<'PY'
from inveriq.detection.detector import demo_bruteforce_event
from inveriq.intent.policy import load_policy
from inveriq.response.generator import generate_candidates
from inveriq.verification.engine import verify

threat = demo_bruteforce_event()
policy = load_policy()
header = f"{'ID':<12} {'ACTION':<20} {'AUTH':<6} {'TARGET':<7} {'REACH':<7} {'AVAIL':<7} {'BLAST':<7} {'EFFECT':<7} {'DECISION'}"
print(header)
print('-' * len(header))
for c in generate_candidates(threat):
    r = verify(c, threat, policy)
    print(f"{c.id:<12} {c.action:<20} {r.authorization:<6} {r.target:<7} {r.reachability:<7} {r.availability:<7} {r.blast_radius:<7} {r.effectiveness:<7} {r.decision}")
PY

stage "REJECT" "Unsafe broad mitigation is rejected before it can touch infrastructure"
python scripts/demo_state.py --stage "REJECT" --message "Unsafe mitigation rejected" --candidate "MIT-UNSAFE" --decision "REJECTED" >/dev/null
if python scripts/lab_enforce.py --candidate MIT-UNSAFE; then
  echo "ERROR: unsafe candidate unexpectedly executed" >&2
  exit 1
else
  rc=$?
  if [[ "$rc" -ne 2 ]]; then exit "$rc"; fi
fi
pause

stage "ENFORCE" "Verified low-blast-radius mitigation is enforced in the isolated gateway"
python scripts/demo_state.py --stage "ENFORCE" --message "Verified mitigation enforced" --candidate "MIT-RATE" --decision "VERIFIED" >/dev/null
python scripts/lab_enforce.py --candidate MIT-RATE
pause

stage "POSTVERIFY" "Measuring threat reduction while preserving trusted service availability"
python scripts/lab_status.py
python - <<'PY'
from inveriq.detection.detector import demo_bruteforce_event
from inveriq.postverify.engine import simulate_post_verification
from inveriq.response.generator import generate_candidates
candidate = next(c for c in generate_candidates(demo_bruteforce_event()) if c.id == 'MIT-RATE')
print(simulate_post_verification(candidate).model_dump_json(indent=2))
PY

stage "COMPLETE" "Attack mitigated; operational invariants preserved"
printf '\n\033[1;32mDEMO COMPLETE — AI decides. INVERIQ verifies.\033[0m\n'

python scripts/lab_reset.py >/dev/null
python scripts/demo_state.py --stage "COMPLETE" --message "Demo complete; lab reset" --candidate "MIT-RATE" --decision "VERIFIED" >/dev/null

if [[ "$KEEP_LAB" -eq 1 ]]; then
  trap - EXIT
  echo "Lab left running (--keep-lab). Stop with: docker compose -f docker-compose.lab.yml down"
fi
