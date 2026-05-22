"""Load categorization rules from rules.yaml (gitignored, per-user)."""

import os
from pathlib import Path

import yaml

DEFAULT_RULES_FILE = Path(__file__).resolve().parent.parent / "rules.yaml"


def rules_path() -> Path:
    """rules.yaml location - LUNCH_MONEY_RULES env var overrides the repo default."""
    env = os.environ.get("LUNCH_MONEY_RULES")
    return Path(env) if env else DEFAULT_RULES_FILE


def load_rules(path: Path | None = None) -> dict:
    """Parsed rules config: {'categories': [...], 'rules': [[prefix, category], ...]}."""
    p = path or rules_path()
    if not p.exists():
        raise FileNotFoundError(
            f"{p} not found - copy rules.example.yaml to rules.yaml and edit it."
        )
    return yaml.safe_load(p.read_text())


def match_category(payee: str, rules: list) -> str | None:
    """First rule whose prefix case-insensitively starts the payee. None if no match."""
    low = (payee or "").lower()
    return next((cat for prefix, cat in rules if low.startswith(prefix.lower())), None)
