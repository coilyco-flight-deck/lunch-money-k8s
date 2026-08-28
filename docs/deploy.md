# Deploying the MCP server

This repo ships a portable Helm chart. Kai's live service is owned by
`coilyco-bridge/deploy/services/lunch-money-mcp/`, which supplies the fleet
image, secrets, exposure, and rollout. Changes here do not deploy it.

## Generic Kubernetes install

The portable path is the Helm chart, documented in [chart.md](chart.md).

## Image

The chart defaults to `docker.io/coilysiren/lunch-money-k8s`. Override
`image.repository` and `image.tag` when using another registry.

## Continuous integration

Canonical CI runs on Forgejo. Every push to `main` runs the app tests, lints and
renders the chart, then publishes and verifies the private
single-architecture image as
`forgejo.coilysiren.me/coilyco-flight-deck/lunch-money-mcp:<full-source-sha>`.
The trusted deploy runner receives the package-write credential. The fleet
deployment uses a separate package-read credential and consumes that exact
immutable reference. GitHub remains a PR mirror and does not publish the fleet
image.

## Categorization rules

`scripts/categorize.py` reads `rules.yaml` from the working directory. Copy
[`rules.example.yaml`](../rules.example.yaml) to `rules.yaml` and edit it for
the desired payees.

The chart can mount rules from `rules.inline`:

```sh
helm install lunch-money ./chart \
  --set lunchMoney.token="$LUNCH_MONEY_TOKEN" \
  --set-file rules.inline=rules.yaml
```
