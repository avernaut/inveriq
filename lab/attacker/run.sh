#!/bin/sh
set -eu
RATE="${ATTACK_DELAY:-0.05}"
while true; do
  curl -sS --connect-timeout 1 -m 2 -o /dev/null -X POST \
    -H 'content-type: application/json' \
    -d '{"username":"admin","password":"demo"}' \
    http://10.77.0.10:8080/login || true
  sleep "$RATE"
done
