# Deploying the MCP server

The standalone Kubernetes deploy machinery has been retired from this repo.

The current deploy surface lives in
[`coilyco-bridge/deploy/services/lunch-money-mcp/`](https://github.com/coilyco-bridge/deploy/tree/main/services/lunch-money-mcp/).
That bundle is the source of truth for manifest layout, secret wiring, ingress,
and rollout details.

This repo keeps the Lunch Money MCP application source and the Docker image
build. For app-level configuration, see the server docs in `README.md` and the
feature inventory in `docs/FEATURES.md`.
