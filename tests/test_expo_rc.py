from pathlib import Path

def test_v090_release_candidate_files_exist():
    required = [
        "scripts/reliability_test.py",
        "scripts/aggregate_stats.py",
        "scripts/failure_injection.py",
        "scripts/export_expo_report.py",
        "demo/run_expo_rc.sh",
        "docs/V0.9.0.md",
        "docs/EXPO_FREEZE.md",
    ]
    for item in required:
        assert Path(item).exists(), item

def test_freeze_policy_is_offline():
    text = Path("docs/EXPO_FREEZE.md").read_text()
    assert "No external LLM/API dependency" in text
    assert "Docker lab" in text
