#!/usr/bin/env bash
set -euo pipefail

# Cron-safe Facebook post wrapper
# Usage:
#   bash scripts/cron-safe-post.sh --page <PAGE_ID> --message-file /abs/path/msg.txt [--photo /abs/path/img.jpg] [--link URL]
#   bash scripts/cron-safe-post.sh --page <PAGE_ID> --message "text..." [--photo ...] [--link ...]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TOKENS_FILE="$SKILL_DIR/tokens.json"
LOG_DIR="$SKILL_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/cron-post-$(date +%Y%m%d).log"

PAGE_ID=""
MESSAGE=""
MESSAGE_FILE=""
PHOTO=""
LINK=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --page) PAGE_ID="$2"; shift 2;;
    --message) MESSAGE="$2"; shift 2;;
    --message-file) MESSAGE_FILE="$2"; shift 2;;
    --photo) PHOTO="$2"; shift 2;;
    --link) LINK="$2"; shift 2;;
    *) echo "Unknown arg: $1" | tee -a "$LOG_FILE"; exit 2;;
  esac
done

if [[ -z "$PAGE_ID" ]]; then
  echo "[ERR] --page is required" | tee -a "$LOG_FILE"
  exit 2
fi

if [[ -n "$MESSAGE_FILE" ]]; then
  [[ -f "$MESSAGE_FILE" ]] || { echo "[ERR] message file not found: $MESSAGE_FILE" | tee -a "$LOG_FILE"; exit 2; }
  MESSAGE="$(cat "$MESSAGE_FILE")"
fi

if [[ -z "$MESSAGE" && -z "$LINK" && -z "$PHOTO" ]]; then
  echo "[ERR] one of --message/--link/--photo is required" | tee -a "$LOG_FILE"
  exit 2
fi

if ! command -v node >/dev/null 2>&1; then
  echo "[ERR] node not found in PATH" | tee -a "$LOG_FILE"
  exit 127
fi

[[ -f "$TOKENS_FILE" ]] || { echo "[ERR] tokens.json missing: $TOKENS_FILE" | tee -a "$LOG_FILE"; exit 1; }

cd "$SCRIPT_DIR"

CMD=(node cli.js post create --page "$PAGE_ID")
[[ -n "$MESSAGE" ]] && CMD+=(--message "$MESSAGE")
[[ -n "$PHOTO" ]] && CMD+=(--photo "$PHOTO")
[[ -n "$LINK" ]] && CMD+=(--link "$LINK")

echo "[$(date '+%F %T')] Running cron-safe post for page=$PAGE_ID" >> "$LOG_FILE"
"${CMD[@]}" >> "$LOG_FILE" 2>&1

echo "[$(date '+%F %T')] OK" >> "$LOG_FILE"
