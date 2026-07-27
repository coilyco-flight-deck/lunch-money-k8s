# lunch-money-k8s 🍱☸️

An [MCP](https://modelcontextprotocol.io/) server for the [Lunch Money](https://lunchmoney.app/) personal-finance API,
packaged as a container image and generic Helm chart, then served over streamable HTTP.
Point Claude or any MCP client at it and ask about your spending in plain language.

## Who this is for

- Homelab folks running k3s who want Claude on their phone to answer "what did I spend on groceries this week" without keeping a laptop awake.
- People who want one MCP endpoint shared across desktop, mobile, and scheduled jobs, instead of stdio-per-device.
- Anyone who'd rather install a Helm chart than learn each server's bespoke deployment shape.

## Why you might try this one

For read/write API coverage, this is feature parity with the [other Lunch Money MCP servers](https://lunchmoney.app/developers). Reach for it when you want the deployment shape - three things stdio-on-a-laptop can't do:

- **Mobile access** - dictation-based shorthand queries from the phone. "What did I spend on groceries this week" against a [Tailscale](https://tailscale.com/)-reachable MCP works the same on the train as at the desk, no laptop awake required.
- **Scheduled dumps and analysis** - k3s is the homelab's general-purpose scheduler, and anything in k3s inherits tailnet reach. A daily routine pulls the trailing 7 days, flags the credit-card balance, enriches opaque payees, feeds uncategorized transactions back into an opinionated [`rules.yaml`](rules.example.yaml) format, and writes the digest into an [Obsidian](https://obsidian.md/) vault inbox.
- **Credential isolation** - the Lunch Money API token lives in a k8s Secret materialized from AWS SSM via ExternalSecrets. The pod gets it as an env var, the MCP exposes tool calls, and the LLM never sees the underlying key. Access control sits at the tailnet boundary.

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

The chart supports a managed token or existing Secret:

```sh
helm install lunch-money ./chart \
  --set lunchMoney.token="$LUNCH_MONEY_TOKEN"
```

Ingress, existing-secret wiring, categorization rules, probes, autoscaling, and
production overrides are covered in [docs/chart.md](docs/chart.md) and
[docs/deploy.md](docs/deploy.md).

## Fleet deploy

Kai's live deployment remains in `coilyco-bridge/deploy/services/lunch-money-mcp/`.
That bundle owns fleet-specific secret wiring, tailnet exposure, and rollout.
The chart in this repo remains the portable install surface for other clusters.

Every push to canonical `main` publishes the private single-architecture fleet
image as
`forgejo.coilysiren.me/coilyco-flight-deck/lunch-money-mcp:<full-source-sha>`.
The trusted deploy runner verifies the remote manifest. The fleet bundle
consumes that exact immutable reference with a separate read-only credential.

The server speaks streamable HTTP at `/mcp` on port 8080. Deployment notes are in
[docs/deploy.md](docs/deploy.md).

## License

AGPL-3.0. See [LICENSE](LICENSE).

## See also

- [docs/FEATURES.md](docs/FEATURES.md) - inventory of what ships today.
- [docs/chart.md](docs/chart.md) - Helm values and chart behavior.
- [docs/deploy.md](docs/deploy.md) - standalone and fleet deployment paths.
- [AGENTS.md](AGENTS.md) - agent instructions.
- [.ward/ward.yaml](.ward/ward.yaml) - allowlisted dev commands (`ward exec <verb>`).
- [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian) - the other half of the loop. This server writes digests into a vault inbox, that MCP lets an agent read and edit vault notes through Obsidian's local REST API.

Cross-reference convention from [coilysiren/agentic-os#59](https://github.com/coilyco-flight-deck/agentic-os/issues/59).
