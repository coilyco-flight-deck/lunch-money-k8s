# Features

What lunch-money-k8s ships today.

## MCP server

- Full Lunch Money API surface: user profile, transactions (list/get/insert/
  update/split/unsplit/groups), categories (CRUD and groups), tags, recurring
  items, budgets, manual assets, Plaid accounts and fetch, crypto.
- v1 and v2 API support. v1 is the default; set `LUNCH_MONEY_API_VERSION=v2`
  (v2 is Lunch Money's open alpha). `LUNCH_MONEY_API_BASE` overrides the URL.
- stdio transport for local MCP clients, streamable HTTP transport for running
  as a Kubernetes service, with env-driven HTTP host and origin allowlists for
  DNS rebinding protection.
- API client with 429 rate-limit backoff.

## Deployment

- Dockerfile building a slim uv-based image. Forgejo CI
  (`.forgejo/workflows/build-publish.yml`) runs app tests, validates the Helm
  chart, and publishes the private single-architecture fleet image as
  `forgejo.coilysiren.me/coilyco-flight-deck/lunch-money-mcp:<full-source-sha>`
  on every push to main. The trusted publisher verifies the remote manifest.
  GitHub is a PR mirror only, with no image build.
- Generic Helm chart with a Deployment, Service, ServiceAccount, optional
  Secret, rules ConfigMap, Ingress, autoscaling, disruption budget, network
  policy, probes, and a connection test.
- Fleet deploy bundle in `coilyco-bridge/deploy/services/lunch-money-mcp/`
  owns Kai's secret wiring, tailnet exposure, and rollout.

## Auto-categorization

- `scripts/categorize.py` seeds a category set and assigns transactions by
  payee-prefix rules from a gitignored `rules.yaml`.

## See also

- [README.md](../README.md) - quick start.
- [AGENTS.md](../AGENTS.md) - agent instructions.
- [.ward/ward.yaml](../.ward/ward.yaml) - dev commands (`ward exec <verb>`).

Cross-reference convention from [coilysiren/agentic-os-kai#313](https://github.com/coilyco-bridge/agentic-os-kai/issues/313).
