"""Seed the category set from rules.yaml, then auto-categorize transactions.

Rerunnable: categories that already exist are skipped, so this doubles as a
monthly cleanup pass. Matching is case-insensitive payee-prefix, first rule wins.
"""

from lunch_money_mcp.client import LunchMoney
from lunch_money_mcp.rules import load_rules, match_category
from lunch_money_mcp.server import list_transactions


def main() -> None:
    config = load_rules()
    api = LunchMoney()
    name_to_id = {c["name"]: c["id"] for c in api.categories()}

    for spec in config["categories"]:
        name = spec["name"]
        if name in name_to_id:
            print(f"exists  {name}")
            continue
        result = api.create_category(
            name, spec.get("is_income", False), spec.get("exclude_from_totals", False)
        )
        name_to_id[name] = result.get("category_id") or result.get("id")
        print(f"created {name} -> {name_to_id[name]}")

    rules = config["rules"]
    txns = list_transactions(uncategorized_only=True)
    assigned, unmatched = 0, []
    for t in txns:
        payee = t.get("payee") or ""
        cat = match_category(payee, rules)
        if cat is None:
            unmatched.append(f"{t['id']} {payee}")
            continue
        api.set_category(t["id"], name_to_id[cat])
        assigned += 1
        print(f"  {t['id']}  {payee}  ->  {cat}")

    print(f"\nassigned {assigned} / {len(txns)} transactions")
    if unmatched:
        print(f"UNMATCHED ({len(unmatched)}):")
        for u in unmatched:
            print(f"  {u}")


if __name__ == "__main__":
    main()
