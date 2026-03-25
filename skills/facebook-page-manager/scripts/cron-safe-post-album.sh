#!/usr/bin/env bash
set -euo pipefail

# Cron-safe Facebook album post wrapper (multiple photos)
# Usage:
#   bash scripts/cron-safe-post-album.sh --page <PAGE_ID> --message-file /abs/path/msg.txt --photo /abs/1.jpg --photo /abs/2.jpg [...]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TOKENS_FILE="$SKILL_DIR/tokens.json"
LOG_DIR="$SKILL_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/cron-post-$(date +%Y%m%d).log"

PAGE_ID=""
MESSAGE=""
MESSAGE_FILE=""
PHOTOS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --page) PAGE_ID="$2"; shift 2;;
    --message) MESSAGE="$2"; shift 2;;
    --message-file) MESSAGE_FILE="$2"; shift 2;;
    --photo) PHOTOS+=("$2"); shift 2;;
    *) echo "Unknown arg: $1" | tee -a "$LOG_FILE"; exit 2;;
  esac
done

[[ -n "$PAGE_ID" ]] || { echo "[ERR] --page is required" | tee -a "$LOG_FILE"; exit 2; }
[[ -f "$TOKENS_FILE" ]] || { echo "[ERR] tokens.json missing: $TOKENS_FILE" | tee -a "$LOG_FILE"; exit 1; }

if [[ -n "$MESSAGE_FILE" ]]; then
  [[ -f "$MESSAGE_FILE" ]] || { echo "[ERR] message file not found: $MESSAGE_FILE" | tee -a "$LOG_FILE"; exit 2; }
  MESSAGE="$(cat "$MESSAGE_FILE")"
fi

[[ -n "$MESSAGE" ]] || { echo "[ERR] message is required" | tee -a "$LOG_FILE"; exit 2; }
[[ ${#PHOTOS[@]} -gt 0 ]] || { echo "[ERR] at least one --photo is required" | tee -a "$LOG_FILE"; exit 2; }

for p in "${PHOTOS[@]}"; do
  [[ -f "$p" ]] || { echo "[ERR] photo not found: $p" | tee -a "$LOG_FILE"; exit 2; }
done

if ! command -v node >/dev/null 2>&1 || ! command -v jq >/dev/null 2>&1 || ! command -v curl >/dev/null 2>&1; then
  echo "[ERR] need node + jq + curl" | tee -a "$LOG_FILE"
  exit 127
fi

TOKEN="$(node - <<'NODE'
const fs=require('fs');
const f=process.argv[1];
const page=process.argv[2];
const t=JSON.parse(fs.readFileSync(f,'utf8'));
if(!t.pages || !t.pages[page] || !t.pages[page].token){ process.exit(2); }
process.stdout.write(t.pages[page].token);
NODE
"$TOKENS_FILE" "$PAGE_ID")"

API="https://graph.facebook.com/v21.0"
ATTACHED=()

{
  echo "[$(date '+%F %T')] Uploading ${#PHOTOS[@]} photo(s) for page=$PAGE_ID"
} >> "$LOG_FILE"

for p in "${PHOTOS[@]}"; do
  PHOTO_ID="$(curl -sS -X POST "$API/$PAGE_ID/photos" \
    -F "source=@$p" \
    -F "published=false" \
    -F "access_token=$TOKEN" | jq -r '.id // empty')"

  if [[ -z "$PHOTO_ID" ]]; then
    echo "[ERR] upload failed for $p" >> "$LOG_FILE"
    exit 1
  fi
  ATTACHED+=("$PHOTO_ID")
  echo "[$(date '+%F %T')] uploaded: $p => $PHOTO_ID" >> "$LOG_FILE"
done

POST_CMD=(curl -sS -X POST "$API/$PAGE_ID/feed" --data-urlencode "message=$MESSAGE" --data-urlencode "access_token=$TOKEN")
for i in "${!ATTACHED[@]}"; do
  POST_CMD+=(--data-urlencode "attached_media[$i]={\"media_fbid\":\"${ATTACHED[$i]}\"}")
done

RESP="$(${POST_CMD[@]})"
POST_ID="$(echo "$RESP" | jq -r '.id // empty')"

if [[ -z "$POST_ID" ]]; then
  echo "[ERR] create post failed: $RESP" >> "$LOG_FILE"
  exit 1
fi

echo "[$(date '+%F %T')] OK post_id=$POST_ID" >> "$LOG_FILE"
echo "POST_OK: $POST_ID"
