"""Live smoke test against the Lunch Money API - read-only, no mutations."""

from lunch_money_mcp.server import list_categories, list_transactions, spending_summary


def main() -> None:
    cats = list_categories()
    print(f"categories: {len(cats)}")

    txns = list_transactions()
    uncategorized = sum(1 for t in txns if not t.get("category_id"))
    print(f"transactions (last 30d): {len(txns)}  uncategorized: {uncategorized}")

    summary = spending_summary()
    print(f"total spend (last 30d): {summary['total']}")
    for row in summary["by_category"][:5]:
        print(f"  {row['category']}: {row['amount']}")


if __name__ == "__main__":
    main()
