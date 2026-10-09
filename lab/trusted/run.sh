#!/bin/sh
set -eu
while true; do
  curl -sS --connect-timeout 1 -m 2 -o /dev/null http://10.77.0.10:8080/health || true
  sleep 0.5
done
