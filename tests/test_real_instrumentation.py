from pathlib import Path

def test_real_instrumentation_files_exist():
    assert Path("scripts/collect_instrumentation.py").exists()
    assert Path("scripts/benchmark_real.py").exists()
    assert Path("docs/V0.7.0.md").exists()

def test_demo_script_keeps_safety_boundary():
    text = Path("demo/run_demo.sh").read_text()
    assert "docker-compose.lab.yml" in text
    assert "collect_instrumentation.py" in text
