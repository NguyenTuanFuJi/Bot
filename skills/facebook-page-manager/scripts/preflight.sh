#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROFILE="${FB_PROFILE:-facebook_fujith}"
ENV_FILE="${FB_ENV_FILE:-$SKILL_DIR/credentials/$PROFILE/.env}"
TOKENS_FILE="${FB_TOKENS_FILE:-$SKILL_DIR/credentials/$PROFILE/tokens.json}"

[[ -f "$ENV_FILE" ]] || { echo "PRECHECK_FAIL: missing .env ($ENV_FILE)"; exit 1; }
[[ -f "$TOKENS_FILE" ]] || { echo "PRECHECK_FAIL: missing tokens.json ($TOKENS_FILE)"; exit 1; }

if ! command -v node >/dev/null 2>&1; then
  echo "PRECHECK_FAIL: node not found"
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "PRECHECK_FAIL: jq not found"
  exit 1
fi

jq -e '.pages and ( .pages | type == "object" )' "$TOKENS_FILE" >/dev/null || {
  echo "PRECHECK_FAIL: invalid tokens.json format"
  exit 1
}

echo "PRECHECK_OK"
