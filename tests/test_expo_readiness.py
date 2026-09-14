from pathlib import Path

def test_expo_readiness_pack_complete():
    required = [
        "expo/README.md",
        "expo/CHECKLIST.md",
        "expo/PITCH_90S.md",
        "expo/FALLBACK.md",
        "expo/SETUP.md",
        "expo/BACKUP_VIDEO.md",
        "expo/ONE_PAGER.md",
        "expo/DAY_OF_SHOW.md",
    ]
    for item in required:
        assert Path(item).exists(), item
