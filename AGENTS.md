# Agent instructions

Repo-local subset. Full operating context for Kai lives in `coilysiren/agentic-os-kai/AGENTS.md`.

## Scope

MCP server for the Lunch Money personal-finance API. Containerized, served over streamable HTTP, deployable to Kubernetes via a Helm chart.

## Project shape

- `lunch_money_mcp/` - Python package, the MCP server itself.
- `chart/` - Helm chart for deployment.
- `scripts/categorize.py` - auto-categorization driver.
- `docs/` - flat documentation (deploy, chart, FEATURES).

## Repo boundaries

This repo owns the MCP server, the Helm chart, and the auto-categorization script. The Lunch Money API and its v1/v2 shape live upstream and are not maintained here.

## Commands

Route every dev command through ward, which reads [`.ward/ward.yaml`](.ward/ward.yaml) (run verbs with `ward exec <verb>`).

## Validation

Pre-commit suite shipped from `coilysiren/agentic-os` plus local mypy and ruff hooks. Run via `pre-commit run --all-files`. CI mirrors the same gates.

## Safety

Never commit a real `rules.yaml` or LUNCH_MONEY_TOKEN. Token lives in a Kubernetes Secret or environment variable.

## Cross-repo contracts

Docker Hub image at `docker.io/coilysiren/lunch-money-k8s` is the publish target. Helm chart consumers pin against tagged releases.

## Release

Tagging `v<semver>` triggers CI to publish the Docker Hub image. Chart bumps land in the same commit as code that changes the rendered manifests.

## Agent rules

Commit to `main`, push after each commit. Every commit closes a same-repo issue with `closes #N`. Conventional Commits subject format. The commit-msg hooks enforce both.

## See also

- [README.md](README.md) - human-facing intro and quick start.
- [docs/FEATURES.md](docs/FEATURES.md) - inventory of what ships today.
- [.ward/ward.yaml](.ward/ward.yaml) - allowlisted dev commands (`ward exec <verb>`).

Cross-reference convention from [coilysiren/agentic-os-kai#313](https://github.com/coilyco-bridge/agentic-os-kai/issues/313).
