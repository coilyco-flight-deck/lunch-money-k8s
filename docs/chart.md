# Helm chart

The generic chart installs the Lunch Money MCP server over streamable HTTP.
Kai's fleet uses a separate deployment bundle, while this chart remains the
portable path for other Kubernetes clusters.

## Install

```sh
helm install lunch-money ./chart \
  --set lunchMoney.token="$LUNCH_MONEY_TOKEN"
```

The MCP endpoint listens at `/mcp` on the Service port.

## Token

The chart supports two mutually exclusive token sources:

- `lunchMoney.token` creates a Secret managed by the chart.
- `lunchMoney.existingSecret` references an existing Secret whose `token` key
  contains the Lunch Money API token.

For an existing Secret:

```sh
helm install lunch-money ./chart \
  --set lunchMoney.existingSecret=lunch-money-token
```

## Configuration

- `image.repository`, `image.tag`, and `image.pullPolicy` select the image.
- `rules.inline` mounts categorization rules at `/app/rules.yaml`.
- `ingress.enabled` exposes the Service through an Ingress.
- `autoscaling.enabled` renders a HorizontalPodAutoscaler.
- `livenessProbe`, `readinessProbe`, and `startupProbe` configure health gates.
- `extraEnv`, `extraEnvFrom`, `extraVolumes`, and `extraVolumeMounts` extend the
  application pod.
- `podDisruptionBudget.enabled` renders a PodDisruptionBudget.
- `networkPolicy.enabled` allows DNS and HTTPS egress plus MCP ingress.
- `command`, `args`, and `lifecycleHooks` customize container execution.
- `commonLabels` and `commonAnnotations` apply shared metadata.

The full default contract lives in [`chart/values.yaml`](../chart/values.yaml).
[`examples/values-homelab.yaml`](../examples/values-homelab.yaml) shows an
existing Secret, node placement, resource requests, and inline rules.

## Validate

```sh
ward exec helm-lint
ward exec helm-template
```

The chart also includes a Helm connection test:

```sh
helm test lunch-money
```

## Fleet boundary

The live CoilyCo deployment stays in
`coilyco-bridge/deploy/services/lunch-money-mcp/`. That bundle owns fleet
secrets, tailnet exposure, and rollout. Changes to this generic chart do not
deploy the fleet service.
