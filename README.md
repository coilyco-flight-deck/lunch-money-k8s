# lunch-money-k8s 🍱☸️

An [MCP](https://modelcontextprotocol.io/) server for the [Lunch Money](https://lunchmoney.app/) personal-finance API,
deployable to [Kubernetes](https://kubernetes.io/) as a [Helm](https://helm.sh/) chart.
Point Claude or any MCP client at it and ask about your spending in plain language.

## Why this runs as a service

Three things the stdio-on-a-laptop pattern can't do:

- **Mobile access** - dictation-based shorthand queries from the phone. "What did I spend on groceries this week" against a [Tailscale](https://tailscale.com/)-reachable MCP works the same on the train as at the desk, no laptop awake required.
- **Scheduled dumps and analysis** - k3s is the homelab's general-purpose scheduler, and anything in k3s inherits tailnet reach. A daily routine pulls the trailing 7 days, flags the credit-card balance, enriches opaque payees, feeds uncategorized transactions back into an opinionated [`rules.yaml`](rules.example.yaml) format (other Lunch Money MCPs don't ship one), and writes the digest into an [Obsidian](https://obsidian.md/) vault inbox.
- **Credential isolation** - the Lunch Money API token lives in a k8s Secret materialized from AWS SSM via ExternalSecrets. The pod gets it as an env var, the MCP exposes tool calls, and the LLM never sees the underlying key. Access control sits at the tailnet boundary.

Writing into the vault is what makes the daily pulls compound. Each digest becomes context for the next day's question, so over months you build up an [LLM-readable second brain](https://fortelabs.com/blog/introducing-the-ai-second-brain/) of your spending history. Today's digest is what next March's "what was that big charge again" finds.

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
wiring, the categorization-rules ConfigMap, and API-version overrides are covered in
[docs/deploy.md](docs/deploy.md). A real-world Helm values file pinned to a homelab
node lives at
[`coilysiren/infrastructure/deploy/lunch-money/values.yaml`](https://github.com/coilysiren/infrastructure/blob/5701039c414f6b49b7977181a5743f93748be577/deploy/lunch-money/values.yaml).

## License

AGPL-3.0. See [LICENSE](LICENSE).

## See also

- [docs/FEATURES.md](docs/FEATURES.md) - inventory of what ships today.
- [docs/deploy.md](docs/deploy.md) - Kubernetes deployment notes.
- [AGENTS.md](AGENTS.md) - agent instructions.
- [.coily/coily.yaml](.coily/coily.yaml) - allowlisted dev commands.
- [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian) - the other half of the loop. This server writes digests into a vault inbox, that MCP lets an agent read and edit vault notes through Obsidian's local REST API.

Cross-reference convention from [coilysiren/agentic-os#59](https://github.com/coilysiren/agentic-os/issues/59).
