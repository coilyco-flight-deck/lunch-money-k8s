"""Tests for payee-prefix categorization rules."""

from pathlib import Path

from lunch_money_mcp.rules import load_rules, match_category

EXAMPLE = Path(__file__).resolve().parent.parent / "rules.example.yaml"


def test_match_basic():
    rules = [["Whole Foods", "Groceries"], ["Lyft", "Transportation"]]
    assert match_category("Whole Foods Market", rules) == "Groceries"
    assert match_category("Lyft *Ride Tue", rules) == "Transportation"


def test_match_case_insensitive():
    assert match_category("NETFLIX.COM", [["netflix", "Subscriptions"]]) == "Subscriptions"


def test_match_first_rule_wins():
    rules = [["Amazon Web Services", "Software"], ["Amazon", "Shopping"]]
    assert match_category("Amazon Web Services", rules) == "Software"
    assert match_category("Amazon Fresh", rules) == "Shopping"


def test_no_match_returns_none():
    assert match_category("Unknown Payee", [["Lyft", "Transportation"]]) is None
    assert match_category("", [["Lyft", "Transportation"]]) is None


def test_example_file_parses():
    config = load_rules(EXAMPLE)
    assert config["categories"]
    assert all(len(rule) == 2 for rule in config["rules"])
