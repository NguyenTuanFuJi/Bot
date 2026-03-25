#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/tuan/.openclaw/workspace"
FB_DIR="$ROOT/skills/facebook-page-manager"
WP_DIR="$ROOT/skills/wordpress-cli-app-password"

ok=true

echo "=== Agent Skill Doctor (FUJI TH) ==="
echo

echo "[Facebook skill]"
if [[ -f "$FB_DIR/.env" ]]; then
  echo "- OK .env: $FB_DIR/.env"
else
  echo "- THIẾU .env: $FB_DIR/.env"
  ok=false
fi

if [[ -f "$FB_DIR/tokens.json" ]]; then
  echo "- OK tokens.json: $FB_DIR/tokens.json"
else
  echo "- THIẾU tokens.json: $FB_DIR/tokens.json"
  ok=false
fi

echo

echo "[WordPress skill]"
if [[ -f "$WP_DIR/.env" ]]; then
  echo "- OK .env: $WP_DIR/.env"
else
  echo "- THIẾU .env: $WP_DIR/.env"
  echo "  -> copy mẫu: $WP_DIR/references/env-template.md"
fi

echo

echo "[Lệnh dùng nhanh]"
echo "Facebook:"
echo "  cd $FB_DIR/scripts"
echo "  node cli.js pages"
echo "  node cli.js post list --page 695286863979169 --limit 5"
echo

echo "WordPress:"
echo "  cd $WP_DIR"
echo "  bash scripts/wp_ops.sh preflight --env .env --mode rest"
echo "  bash scripts/wp_ops.sh list --env .env --mode rest --per-page 5"
echo

if [[ "$ok" == true ]]; then
  echo "KẾT LUẬN: Facebook credential đã sẵn sàng."
else
  echo "KẾT LUẬN: Thiếu credential, cần bổ sung theo đường dẫn trên."
fi
