---
ward:
  workflow: merge-remote-main
---
# Agent instructions

Repo-local subset. Full operating context for Kai lives in `coilysiren/agentic-os-kai/AGENTS.md`.

## Scope

MCP server for the Lunch Money personal-finance API. Containerized, served over streamable HTTP, and packaged with a generic Helm chart. Fleet deployment is handled from `coilyco-bridge/deploy`.

## Project shape

- `lunch_money_mcp/` - Python package, the MCP server itself.
- `Dockerfile` - image build for the MCP server.
- `chart/` - generic Helm chart for standalone Kubernetes installs.
- `examples/` - example values for chart consumers.
- `scripts/categorize.py` - auto-categorization driver.
- `docs/` - flat documentation (chart, deploy, FEATURES).

## Repo boundaries

This repo owns the MCP server source, image build, generic Helm chart, and auto-categorization script. Fleet-specific values, secrets, exposure, and rollout stay in `coilyco-bridge/deploy`. The Lunch Money API and its v1/v2 shape live upstream and are not maintained here.

## Commands

Route every dev command through the [`justfile`](justfile) (run verbs with `just <verb>`).

## Validation

Pre-commit suite shipped from `coilysiren/agentic-os` plus local mypy and ruff hooks. Run via `pre-commit run --all-files`. CI mirrors the same gates.

## Safety

Never commit a real `rules.yaml` or LUNCH_MONEY_TOKEN. Token lives in a Kubernetes Secret or environment variable.

## Cross-repo contracts

The generic chart defaults to `docker.io/coilysiren/lunch-money-k8s`. Forgejo
CI publishes the private single-architecture fleet image as
`forgejo.coilysiren.me/coilyco-flight-deck/lunch-money-mcp:<full-source-sha>`.
The trusted deploy runner owns the write credential and verifies the remote
manifest. `coilyco-bridge/deploy/services/lunch-money-mcp/` consumes that exact
reference through a separate read-only credential and owns its rollout.

## Release

Every push to `main` runs tests, validates the Helm chart, and publishes one
source-SHA fleet image to Forgejo OCI. Chart behavior changes bump
`chart/Chart.yaml` in the same commit. Fleet deploy changes land in the deploy
repo, not here.

## Agent rules

Commit to `main`, push after each commit. Every commit closes a same-repo issue with `closes #N`. Conventional Commits subject format. The commit-msg hooks enforce both.

## Checkout residency

This repo is not in Agent Compose's `repository-plan.yaml`, so it has no
resident checkout under `~/projects/<owner>/`. That is intentional. Work it
from a task-scoped temporary clone, and remove that clone once the work lands.

A temporary root can be purged at any time, so commit and push before pausing,
switching tasks, or ending a session. The remote is the only durable artifact.

## See also

- [README.md](README.md) - human-facing intro and quick start.
- [docs/FEATURES.md](docs/FEATURES.md) - inventory of what ships today.
- [justfile](justfile) - dev verbs (`just <verb>`).
- [.ward/ward.yaml](.ward/ward.yaml) - catalog metadata only.

Cross-reference convention from [coilysiren/agentic-os-kai#313](https://github.com/coilyco-bridge/agentic-os-kai/issues/313).
