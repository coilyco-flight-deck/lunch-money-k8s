# lunch-money-k8s 🍱☸️

An [MCP](https://modelcontextprotocol.io/) server for the [Lunch Money](https://lunchmoney.app/) personal-finance API,
deployable to [Kubernetes](https://kubernetes.io/) as a [Helm](https://helm.sh/) chart.
Point Claude or any MCP client at it and ask about your spending in plain language.

## Who this is for

- Homelab folks running k3s who want Claude on their phone to answer "what did I spend on groceries this week" without keeping a laptop awake.
- People who want one MCP endpoint shared across desktop, mobile, and scheduled jobs, instead of stdio-per-device.
- Anyone who'd rather deploy a Helm chart than learn each MCP server's bespoke install path.

## Why you might try this one

For read/write API coverage, this is feature parity with the [other Lunch Money MCP servers](https://lunchmoney.app/developers). Reach for it when you want the deployment shape - three things stdio-on-a-laptop can't do:

- **Mobile access** - dictation-based shorthand queries from the phone. "What did I spend on groceries this week" against a [Tailscale](https://tailscale.com/)-reachable MCP works the same on the train as at the desk, no laptop awake required.
- **Scheduled dumps and analysis** - k3s is the homelab's general-purpose scheduler, and anything in k3s inherits tailnet reach. A daily routine pulls the trailing 7 days, flags the credit-card balance, enriches opaque payees, feeds uncategorized transactions back into an opinionated [`rules.yaml`](rules.example.yaml) format, and writes the digest into an [Obsidian](https://obsidian.md/) vault inbox.
- **Credential isolation** - the Lunch Money API token lives in a k8s Secret materialized from AWS SSM via ExternalSecrets. The pod gets it as an env var, the MCP exposes tool calls, and the LLM never sees the underlying key. Access control sits at the tailnet boundary.

The daily pulls compound through the vault. Each digest becomes context for the next day's question, so today's note is what next March's "what was that big charge again" finds - an [LLM-readable second brain](https://fortelabs.com/blog/introducing-the-ai-second-brain/) built up over time.

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

The chart isn't published to a registry yet ([#7](https://forgejo.coilysiren.me/coilysiren/lunch-money-k8s/issues/7)), so clone first:

```
git clone https://github.com/coilyco-flight-deck/lunch-money-k8s.git
cd lunch-money-k8s
helm install lunch-money ./chart --set lunchMoney.token=$LUNCH_MONEY_TOKEN
```

The server speaks streamable HTTP at `/mcp` on port 8080. Ingress, existing-secret
wiring, the categorization-rules ConfigMap, API-version overrides, and a real-world
homelab values file are covered in [docs/deploy.md](docs/deploy.md).

## License

AGPL-3.0. See [LICENSE](LICENSE).

## See also

- [docs/FEATURES.md](docs/FEATURES.md) - inventory of what ships today.
- [docs/deploy.md](docs/deploy.md) - Kubernetes deployment notes.
- [AGENTS.md](AGENTS.md) - agent instructions.
- [.ward/ward.yaml](.ward/ward.yaml) - allowlisted dev commands (`ward exec <verb>`).
- [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian) - the other half of the loop. This server writes digests into a vault inbox, that MCP lets an agent read and edit vault notes through Obsidian's local REST API.

Cross-reference convention from [coilysiren/agentic-os#59](https://github.com/coilyco-flight-deck/agentic-os/issues/59).
