"""Dump uncategorized transactions as TSV - id, date, amount, payee."""

from lunch_money_mcp.server import list_transactions


def main() -> None:
    txns = list_transactions(uncategorized_only=True)
    for t in sorted(txns, key=lambda x: x.get("payee") or ""):
        print(f"{t['id']}\t{t['date']}\t{t.get('amount')}\t{t.get('payee')}")


if __name__ == "__main__":
    main()
