#!/usr/bin/env bash
set -euo pipefail

case "${1:-}" in
  check)
    uv run ruff check .
    uv run ruff format --check .
    ;;
  format)
    uv run ruff check --fix .
    uv run ruff format .
    ;;
  *)
    echo "usage: $0 {check|format}" >&2
    exit 2
    ;;
esac
