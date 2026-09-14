from pathlib import Path
import yaml


def load_policy(path: str = "policies/demo.yaml") -> dict:
    with Path(path).open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)
