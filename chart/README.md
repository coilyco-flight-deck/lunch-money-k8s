# lunch-money-k8s chart

Helm chart for the Lunch Money MCP server, served over streamable HTTP.

## Install

```
helm install lunch-money ./chart --set lunchMoney.token=$LUNCH_MONEY_TOKEN
```

## Key values

- `image.repository` / `image.tag` - container image, defaults to the GHCR build
- `lunchMoney.token` - API token, chart creates a Secret
- `lunchMoney.existingSecret` - instead, reference a Secret with key `token`
- `rules.inline` - paste a rules.yaml body to mount auto-categorization rules
- `ingress.enabled` - expose externally, off by default
- `autoscaling.enabled` - turn on the HorizontalPodAutoscaler

Full deployment notes, including the example values file, are in
[../docs/deploy.md](../docs/deploy.md).

## Test

```
helm test lunch-money
```

Runs a connection probe against the Service.
