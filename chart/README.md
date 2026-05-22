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

## Production niceties

- `livenessProbe` / `readinessProbe` / `startupProbe` - values-driven probe blocks, default to tcpSocket on the http port. Set a block to `{}` to disable that probe.
- `extraEnv` / `extraEnvFrom` - extra env vars and envFrom sources injected into the container.
- `extraVolumes` / `extraVolumeMounts` - extra volumes and mounts, merged with the rules ConfigMap volume.
- `podDisruptionBudget.enabled` - render a PodDisruptionBudget with `minAvailable` / `maxUnavailable`.
- `networkPolicy.enabled` - render a NetworkPolicy allowing DNS and HTTPS egress plus ingress to the http port.
- `command` / `args` - override the container entrypoint and arguments.
- `lifecycleHooks` - container lifecycle hooks block.
- `commonLabels` / `commonAnnotations` - labels and annotations merged onto every rendered resource.
- `revisionHistoryLimit`, `terminationGracePeriodSeconds`, `serviceAccount.automountServiceAccountToken` - Deployment and pod hardening knobs.

Full deployment notes, including the example values file, are in
[../docs/deploy.md](../docs/deploy.md).

## Test

```
helm test lunch-money
```

Runs a connection probe against the Service.
