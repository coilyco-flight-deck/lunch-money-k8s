"""FastMCP server exposing Lunch Money transactions and categorization."""

import os
from collections import defaultdict
from datetime import date, timedelta

from mcp.server.fastmcp import FastMCP

from lunch_money_mcp.client import LunchMoney

mcp = FastMCP("lunch-money")

# Lazily constructed so the server imports without AWS creds present.
_client: LunchMoney | None = None


def _api() -> LunchMoney:
    global _client
    if _client is None:
        _client = LunchMoney()
    return _client


def _default_range(start_date: str | None, end_date: str | None) -> tuple[str, str]:
    """Default to the trailing 30 days when a range is omitted."""
    end = date.fromisoformat(end_date) if end_date else date.today()
    start = date.fromisoformat(start_date) if start_date else end - timedelta(days=30)
    return start.isoformat(), end.isoformat()


@mcp.tool()
def list_transactions(
    start_date: str | None = None,
    end_date: str | None = None,
    uncategorized_only: bool = False,
) -> list[dict]:
    """List transactions in a date range (YYYY-MM-DD). Defaults to the last 30 days.

    Set uncategorized_only to surface just the transactions that still need a category.
    """
    start, end = _default_range(start_date, end_date)
    txns = _api().transactions(start, end)
    if uncategorized_only:
        txns = [t for t in txns if not t.get("category_id")]
    return [
        {
            "id": t["id"],
            "date": t["date"],
            "payee": t.get("payee"),
            "amount": t.get("amount"),
            "currency": t.get("currency"),
            "category_id": t.get("category_id"),
            "category_name": t.get("category_name"),
            "notes": t.get("notes"),
        }
        for t in txns
    ]


@mcp.tool()
def list_categories() -> list[dict]:
    """List all spending categories with their ids, so a category can be assigned."""
    return [
        {"id": c["id"], "name": c["name"], "is_income": c.get("is_income", False)}
        for c in _api().categories()
    ]


@mcp.tool()
def create_category(
    name: str, is_income: bool = False, exclude_from_totals: bool = False
) -> dict:
    """Create a new spending category. Returns the new category id.

    Set exclude_from_totals for transfer-like categories (credit card payments)
    so they do not double-count against spend.
    """
    result = _api().create_category(name, is_income, exclude_from_totals)
    cid = result.get("category_id") or result.get("id")
    return {"name": name, "category_id": cid, "created": True}


@mcp.tool()
def categorize_transaction(transaction_id: int, category_id: int) -> dict:
    """Assign a category to a transaction. Use list_categories to find a category id."""
    _api().set_category(transaction_id, category_id)
    return {"transaction_id": transaction_id, "category_id": category_id, "updated": True}


@mcp.tool()
def spending_summary(start_date: str | None = None, end_date: str | None = None) -> dict:
    """Total spend per category over a date range. Defaults to the last 30 days."""
    start, end = _default_range(start_date, end_date)
    by_category: dict[str, float] = defaultdict(float)
    for t in _api().transactions(start, end):
        name = t.get("category_name") or "Uncategorized"
        by_category[name] += float(t.get("amount") or 0)
    ranked = sorted(by_category.items(), key=lambda kv: kv[1], reverse=True)
    return {
        "start_date": start,
        "end_date": end,
        "total": round(sum(by_category.values()), 2),
        "by_category": [{"category": n, "amount": round(v, 2)} for n, v in ranked],
    }


@mcp.tool()
def list_budgets(start_date: str | None = None, end_date: str | None = None) -> list[dict]:
    """Budget detail per category over a date range. Defaults to the last 30 days."""
    start, end = _default_range(start_date, end_date)
    return _api().budgets(start, end)


def main() -> None:
    """Run over stdio, or streamable HTTP when LUNCH_MONEY_MCP_TRANSPORT=http."""
    transport = os.environ.get("LUNCH_MONEY_MCP_TRANSPORT", "stdio")
    if transport in ("http", "streamable-http"):
        mcp.settings.host = os.environ.get("LUNCH_MONEY_MCP_HOST", "0.0.0.0")
        mcp.settings.port = int(os.environ.get("LUNCH_MONEY_MCP_PORT", "8080"))
        mcp.run(transport="streamable-http")
    else:
        mcp.run()


if __name__ == "__main__":
    main()
