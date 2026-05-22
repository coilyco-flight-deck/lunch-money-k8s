"""Tests for server helpers that need no live API."""

from datetime import date

from lunch_money_mcp.server import _default_range


def test_default_range_spans_30_days():
    start, end = _default_range(None, None)
    assert (date.fromisoformat(end) - date.fromisoformat(start)).days == 30


def test_default_range_passes_explicit_dates():
    assert _default_range("2026-01-01", "2026-01-31") == ("2026-01-01", "2026-01-31")


def test_default_range_fills_start_from_end():
    start, end = _default_range(None, "2026-03-31")
    assert end == "2026-03-31"
    assert start == "2026-03-01"
