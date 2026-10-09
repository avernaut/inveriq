from pathlib import Path

import pytest
from pydantic import ValidationError

from inveriq import __release_tag__, __version__
from inveriq.api.main import app, health
from inveriq.models.mitigation import MitigationCandidate


def test_release_metadata_is_rc2_and_consistent():
    assert __version__ == "0.9.0rc2"
    assert __release_tag__ == "v0.9.0-expo-rc2"
    assert app.version == __version__
    payload = health()
    assert payload["version"] == __version__
    assert payload["release"] == __release_tag__
    assert 'version = "0.9.0rc2"' in Path("pyproject.toml").read_text()


def test_demo_launchers_are_executable():
    assert Path("demo/run_demo.sh").stat().st_mode & 0o111
    assert Path("demo/run_expo_rc.sh").stat().st_mode & 0o111


def test_mitigation_source_rejects_non_ip_input():
    with pytest.raises(ValidationError):
        MitigationCandidate(
            id="MIT-INJECTION",
            threat_id="THR-001",
            action="BLOCK_SOURCE",
            source='10.77.0.50; echo unsafe',
            target="authentication-api",
            duration=60,
            reason="invalid source must not reach enforcement",
        )
