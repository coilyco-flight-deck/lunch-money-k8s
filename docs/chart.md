# Fleet deploy handoff

This repo no longer ships a standalone Helm chart.

The active Kubernetes deploy bundle lives in
[`coilyco-bridge/deploy/services/lunch-money-mcp/`](https://github.com/coilyco-bridge/deploy/tree/main/services/lunch-money-mcp/).
That bundle owns the manifest, secret wiring, ingress, and rollout behavior.

Keep this repo focused on the MCP server source, image build, and app-level docs.
