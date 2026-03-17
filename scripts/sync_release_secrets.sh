#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="${1:-$ROOT_DIR/.env.release.local}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing env file: $ENV_FILE" >&2
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

if [[ -z "${PYPI_API_TOKEN:-}" ]]; then
  echo "PYPI_API_TOKEN is required in $ENV_FILE" >&2
  exit 1
fi

REPO="${GITHUB_REPO:-Lumiwealth/quantstats_lumi}"
ENV_NAME="${GITHUB_ENVIRONMENT:-pypi}"

printf '%s' "$PYPI_API_TOKEN" | gh secret set PYPI_API_TOKEN -R "$REPO" --env "$ENV_NAME"

echo "Set secret PYPI_API_TOKEN in repo=$REPO environment=$ENV_NAME"
