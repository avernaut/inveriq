from pathlib import Path
import json

def test_v080_files_exist():
    assert Path("scripts/traffic_generator.py").exists()
    assert Path("scripts/benchmark_effectiveness.py").exists()
    assert Path("docs/V0.8.0.md").exists()

def test_traffic_generator_has_all_scenarios():
    text = Path("scripts/traffic_generator.py").read_text()
    for name in ("brute-force", "ddos", "exfiltration"):
        assert name in text

def test_demo_runner_invokes_effectiveness_benchmark():
    text = Path("demo/run_demo.sh").read_text()
    assert "benchmark_effectiveness.py" in text
