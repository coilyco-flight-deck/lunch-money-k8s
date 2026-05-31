# Features

What lunch-money-k8s ships today.

## MCP server

- Full Lunch Money API surface: user profile, transactions (list/get/insert/
  update/split/unsplit/groups), categories (CRUD and groups), tags, recurring
  items, budgets, manual assets, Plaid accounts and fetch, crypto.
- v1 and v2 API support. v1 is the default; set `LUNCH_MONEY_API_VERSION=v2`
  (v2 is Lunch Money's open alpha). `LUNCH_MONEY_API_BASE` overrides the URL.
- stdio transport for local MCP clients, streamable HTTP transport for running
  as a Kubernetes service.
- API client with 429 rate-limit backoff.

## Deployment

- Dockerfile building a slim uv-based image, published to GHCR by CI.
- Helm chart: Deployment, Service, ServiceAccount, HorizontalPodAutoscaler,
  Secret, rules ConfigMap, optional Ingress, and a helm test connection probe.

## Auto-categorization

- `scripts/categorize.py` seeds a category set and assigns transactions by
  payee-prefix rules from a gitignored `rules.yaml`.

## See also

- [README.md](../README.md) - quick start.
- [AGENTS.md](../AGENTS.md) - agent instructions.
- [.coily/coily.yaml](../.coily/coily.yaml) - dev commands.

Cross-reference convention from [coilysiren/agentic-os-kai#313](https://github.com/coilyco-bridge/agentic-os-kai/issues/313).
