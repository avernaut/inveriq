#!/usr/bin/env python3
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from demo.metrics import load_all_metrics, summarize

rows = load_all_metrics()
print(json.dumps(summarize(rows), indent=2))
