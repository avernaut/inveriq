#!/usr/bin/env bash
set -euo pipefail

SCENARIO="${1:-brute-force}"

echo "== INVERIQ v0.9.0 Expo RC =="
echo "Scenario: $SCENARIO"

docker compose -f docker-compose.lab.yml up --build -d
python scripts/lab_reset.py || true

echo
echo "== Real instrumentation =="
python scripts/benchmark_real.py --scenario "$SCENARIO"

echo
echo "== Real traffic effectiveness =="
python scripts/benchmark_effectiveness.py --scenario "$SCENARIO"

echo
echo "== Aggregate statistics =="
python scripts/aggregate_stats.py

echo
echo "== Export report =="
python scripts/export_expo_report.py

echo
echo "RC run complete."
