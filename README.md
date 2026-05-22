# lunch-money-k8s 🍱☸️

An MCP server for the [Lunch Money](https://lunchmoney.app/) personal-finance API,
served over HTTP and deployable to Kubernetes with a Helm chart. Point Claude or any
MCP client at it and ask about your spending in plain language.

Most Lunch Money MCP servers run stdio-only on a laptop. This one runs as a service:
containerized, Helm-installable, happy on a homelab cluster.

## Tools

- `list_transactions` - transactions in a date range, optional uncategorized filter
- `list_categories` / `create_category` - read and create categories
- `categorize_transaction` - assign a category to a transaction
- `spending_summary` - total spend per category
- `list_budgets` - budget detail per category

## Quick start (local, stdio)

Grab an API token from the [Lunch Money developers page](https://my.lunchmoney.app/developers):

```
export LUNCH_MONEY_TOKEN=...
uv sync
uv run lunch-money-mcp
```

Then register `uv run lunch-money-mcp` with your MCP client.

## Run on Kubernetes

```
helm install lunch-money ./chart --set lunchMoney.token=$LUNCH_MONEY_TOKEN
```

The server speaks streamable HTTP at `/mcp` on port 8080. Ingress, existing-secret
wiring, and the categorization-rules ConfigMap are covered in
[docs/deploy.md](docs/deploy.md).

## Auto-categorization

`scripts/categorize.py` seeds a category set and assigns transactions by
payee-prefix rules. Copy `rules.example.yaml` to `rules.yaml` (gitignored, so your
real payees never get committed) and edit it for your own spending.

## License

AGPL-3.0. See [LICENSE](LICENSE).
