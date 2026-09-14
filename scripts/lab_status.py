#!/usr/bin/env python3
import json
import urllib.request

with urllib.request.urlopen("http://127.0.0.1:18080/metrics", timeout=3) as response:
    print(json.dumps(json.load(response), indent=2))
