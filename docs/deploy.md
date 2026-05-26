# Deploying to Kubernetes

The Helm chart in `chart/` runs the MCP server over streamable HTTP.

## Image

The chart points at `docker.io/coilysiren/lunch-money-k8s`. Build your own with:

```
docker build -t <your-registry>/lunch-money-k8s:dev .
```

Override `image.repository` and `image.tag` in values to use it.

## Token

The server needs a Lunch Money API token. Two ways:

- **Chart-managed Secret** - `--set lunchMoney.token=...`. The chart creates a
  Secret holding it.
- **Existing Secret** - `--set lunchMoney.existingSecret=my-secret`. The Secret
  must hold the token under the key `token`.

## Categorization rules

`scripts/categorize.py` reads a `rules.yaml` from the working directory. Copy
[`rules.example.yaml`](../rules.example.yaml) to `rules.yaml` (gitignored) and
edit it for your payees.

To run auto-categorization in-cluster, pass a `rules.yaml` body as
`rules.inline`. The chart mounts it as a ConfigMap at `/app/rules.yaml`:

```
helm install lunch-money ./chart \
  --set lunchMoney.token=$LUNCH_MONEY_TOKEN \
  --set-file rules.inline=rules.yaml
```

## Configuration

The server talks to the Lunch Money v1 API by default. Set
`LUNCH_MONEY_API_VERSION=v2` to use the v2 API (Lunch Money's open alpha).
`LUNCH_MONEY_API_BASE` overrides the base URL.

## Real-world example

A Helm values file pinned to the kai-server homelab node, with ExternalSecret
and node selector wired in, lives at
[`coilysiren/infrastructure/deploy/lunch-money/values.yaml`](https://github.com/coilysiren/infrastructure/blob/5701039c414f6b49b7977181a5743f93748be577/deploy/lunch-money/values.yaml).

## Ingress

Ingress is off by default. Enable it with:

```
--set ingress.enabled=true \
--set ingress.host=lunch-money.example.com \
--set ingress.className=nginx
```

Set `ingress.tls=true` for a TLS block backed by a `<release>-tls` Secret.

## Probes

Liveness and readiness use a TCP probe on the HTTP port, so they hold up
regardless of which MCP transport path is mounted.
