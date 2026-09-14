from pathlib import Path


def test_demo_script_exists_and_is_executable():
    path = Path("demo/run_demo.sh")
    assert path.exists()
    assert path.stat().st_mode & 0o111
    text = path.read_text()
    assert "MIT-UNSAFE" in text
    assert "MIT-RATE" in text
    assert "docker compose -f docker-compose.lab.yml" in text


def test_dashboard_tracks_demo_state_and_live_metrics():
    text = Path("dashboard/app.py").read_text()
    assert ".demo-state.json" in text
    assert "18080/metrics" in text
    assert "Verification Gate" in text
    assert "V1 Auth" in text and "V6 Effect" in text


def test_demo_state_defaults_safe():
    text = Path("scripts/demo_state.py").read_text()
    assert '"stage": "READY"' in text
    assert '"candidate": None' in text
