"""Tests for server helpers that need no live API."""

from datetime import date

from lunch_money_mcp.server import (
    DEFAULT_ALLOWED_HOSTS,
    DEFAULT_ALLOWED_ORIGINS,
    _build_mcp,
    _default_range,
    _parse_csv_env,
    _transport_security,
)


def test_default_range_spans_30_days():
    start, end = _default_range(None, None)
    assert (date.fromisoformat(end) - date.fromisoformat(start)).days == 30


def test_default_range_passes_explicit_dates():
    assert _default_range("2026-01-01", "2026-01-31") == ("2026-01-01", "2026-01-31")


def test_default_range_fills_start_from_end():
    start, end = _default_range(None, "2026-03-31")
    assert end == "2026-03-31"
    assert start == "2026-03-01"


def test_full_tool_surface_registered():
    from lunch_money_mcp.server import mcp

    names = {t.name for t in mcp._tool_manager.list_tools()}
    expected = {
        "get_user_profile",
        "api_version",
        "upsert_budget",
        "list_crypto",
        "update_crypto",
        "list_tags",
        "split_transaction",
        "unsplit_transactions",
        "add_to_category_group",
        "trigger_plaid_fetch",
    }
    assert expected <= names
    assert len(names) >= 30


def test_parse_csv_env_trims_and_skips_empty(monkeypatch):
    monkeypatch.setenv(
        "LUNCH_MONEY_MCP_ALLOWED_HOSTS", " lunch-money.coilysiren.me, ,kai-server:30080 "
    )
    assert _parse_csv_env("LUNCH_MONEY_MCP_ALLOWED_HOSTS") == [
        "lunch-money.coilysiren.me",
        "kai-server:30080",
    ]


def test_transport_security_merges_local_defaults_and_env(monkeypatch):
    monkeypatch.setenv(
        "LUNCH_MONEY_MCP_ALLOWED_HOSTS", "lunch-money.coilysiren.me,kai-server:30080"
    )
    monkeypatch.setenv(
        "LUNCH_MONEY_MCP_ALLOWED_ORIGINS",
        "https://lunch-money.coilysiren.me,http://kai-server:30080",
    )

    security = _transport_security()

    assert security.enable_dns_rebinding_protection is True
    assert set(DEFAULT_ALLOWED_HOSTS) <= set(security.allowed_hosts)
    assert {
        "lunch-money.coilysiren.me",
        "kai-server:30080",
    } <= set(security.allowed_hosts)
    assert set(DEFAULT_ALLOWED_ORIGINS) <= set(security.allowed_origins)
    assert {
        "https://lunch-money.coilysiren.me",
        "http://kai-server:30080",
    } <= set(security.allowed_origins)


def test_build_mcp_applies_http_env(monkeypatch):
    monkeypatch.setenv("LUNCH_MONEY_MCP_HOST", "0.0.0.0")
    monkeypatch.setenv("LUNCH_MONEY_MCP_PORT", "30080")
    monkeypatch.setenv(
        "LUNCH_MONEY_MCP_ALLOWED_HOSTS",
        "lunch-money.coilysiren.me,lunch-money.coilysiren.me:443",
    )
    monkeypatch.setenv("LUNCH_MONEY_MCP_ALLOWED_ORIGINS", "https://lunch-money.coilysiren.me")

    mcp = _build_mcp()

    assert mcp.settings.host == "0.0.0.0"
    assert mcp.settings.port == 30080
    assert "lunch-money.coilysiren.me" in mcp.settings.transport_security.allowed_hosts
    assert "lunch-money.coilysiren.me:443" in mcp.settings.transport_security.allowed_hosts
    assert "https://lunch-money.coilysiren.me" in mcp.settings.transport_security.allowed_origins
