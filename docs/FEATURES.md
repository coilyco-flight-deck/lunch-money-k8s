# Features

What lunch-money-k8s ships today.

## MCP server

- 26 tools over the Lunch Money v1 API: user profile, transactions, categories,
  tags, recurring items, budgets, manual assets, Plaid accounts, crypto.
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

- [README.md](README.md) - quick start.
- [AGENTS.md](AGENTS.md) - agent instructions.
- [.coily/coily.yaml](.coily/coily.yaml) - dev commands.
