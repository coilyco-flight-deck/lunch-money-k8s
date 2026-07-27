#!/usr/bin/env bash
set -euo pipefail

case "${1:-}" in
  lint)
    helm lint chart
    ;;
  template)
    helm template lunch-money chart --set lunchMoney.token=dummy
    helm template lunch-money chart \
      -f examples/values-homelab.yaml \
      --set lunchMoney.existingSecret=x
    ;;
  *)
    echo "usage: $0 {lint|template}" >&2
    exit 2
    ;;
esac
