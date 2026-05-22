"""Tests for API version resolution - no live API."""

from lunch_money_mcp.client import API_BASES, _resolve_api


def test_resolve_api_defaults_to_v1(monkeypatch):
    monkeypatch.delenv("LUNCH_MONEY_API_VERSION", raising=False)
    monkeypatch.delenv("LUNCH_MONEY_API_BASE", raising=False)
    version, base = _resolve_api()
    assert version == "v1"
    assert base == API_BASES["v1"]


def test_resolve_api_selects_v2(monkeypatch):
    monkeypatch.setenv("LUNCH_MONEY_API_VERSION", "v2")
    monkeypatch.delenv("LUNCH_MONEY_API_BASE", raising=False)
    version, base = _resolve_api()
    assert version == "v2"
    assert base == API_BASES["v2"]


def test_resolve_api_unknown_version_falls_back_to_v1(monkeypatch):
    monkeypatch.setenv("LUNCH_MONEY_API_VERSION", "v99")
    monkeypatch.delenv("LUNCH_MONEY_API_BASE", raising=False)
    version, _ = _resolve_api()
    assert version == "v1"


def test_resolve_api_base_override(monkeypatch):
    monkeypatch.setenv("LUNCH_MONEY_API_VERSION", "v2")
    monkeypatch.setenv("LUNCH_MONEY_API_BASE", "https://example.test/v2")
    _, base = _resolve_api()
    assert base == "https://example.test/v2"
