# Helm chart

The generic chart installs the Lunch Money MCP server over streamable HTTP. It
is the portable path for other clusters. Kai's fleet service is owned by
`coilyco-bridge/deploy/services/lunch-money-mcp/`, and changes here do not
deploy it.

## Install and token

```sh
helm install lunch-money ./chart --set lunchMoney.token="$LUNCH_MONEY_TOKEN"
```

The MCP endpoint listens at `/mcp` on the Service port. Two mutually exclusive
token sources: `lunchMoney.token` creates a chart-managed Secret, and
`lunchMoney.existingSecret` references an existing Secret whose `token` key
holds the API token.

## Configuration

Values group by what they configure: the image (`image.*`), categorization
rules mounted at `/app/rules.yaml` (`rules.inline`), exposure
(`ingress.enabled`), scaling (`autoscaling.enabled`,
`podDisruptionBudget.enabled`), health gates (`livenessProbe`,
`readinessProbe`, `startupProbe`), egress and ingress policy
(`networkPolicy.enabled`), container execution (`command`, `args`,
`lifecycleHooks`), pod extension (`extraEnv`, `extraEnvFrom`, `extraVolumes`,
`extraVolumeMounts`), and shared metadata (`commonLabels`,
`commonAnnotations`).

The full default contract is [`chart/values.yaml`](../chart/values.yaml).
[`examples/values-homelab.yaml`](../examples/values-homelab.yaml) shows an
existing Secret, node placement, resource requests, and inline rules.

## Validate

`ward exec helm-lint` and `ward exec helm-template` cover the chart, and
`helm test lunch-money` runs the included connection test.

