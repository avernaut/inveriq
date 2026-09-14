import json
from pathlib import Path

def test_demo_scenarios_present():
    p = Path("demo/scenarios.json")
    data = json.loads(p.read_text())
    assert set(data) == {"brute-force", "ddos", "exfiltration"}
    assert data["brute-force"]["mitre"] == "T1110"
    assert data["ddos"]["mitre"] == "T1498"
    assert data["exfiltration"]["mitre"] == "T1048"
