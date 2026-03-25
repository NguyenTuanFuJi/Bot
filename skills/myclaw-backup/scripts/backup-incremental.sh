#!/usr/bin/env bash
set -euo pipefail

OUTPUT_DIR="${1:-/tmp/openclaw-backups}"
OPENCLAW_HOME="${HOME}/.openclaw"
STATE_DIR="${OPENCLAW_HOME}/backups/state"
SNAPSHOT_FILE="${STATE_DIR}/openclaw-incremental.snar"
TS="$(date +"%Y%m%d_%H%M%S")"
ARCHIVE="${OUTPUT_DIR}/openclaw-incremental_${TS}.tar.gz"

mkdir -p "$OUTPUT_DIR" "$STATE_DIR"

# chỉ backup các phần quan trọng để giữ trí nhớ + cấu hình + credential
CANDIDATES=(
  "${OPENCLAW_HOME}/workspace"
  "${OPENCLAW_HOME}/openclaw.json"
  "${OPENCLAW_HOME}/credentials"
  "${OPENCLAW_HOME}/agents"
  "${OPENCLAW_HOME}/skills"
  "${OPENCLAW_HOME}/devices"
  "${OPENCLAW_HOME}/identity"
  "${OPENCLAW_HOME}/cron"
)

INCLUDES=()
for p in "${CANDIDATES[@]}"; do
  [[ -e "$p" ]] && INCLUDES+=("$p")
done

if [[ ${#INCLUDES[@]} -eq 0 ]]; then
  echo "No backup targets found under ${OPENCLAW_HOME}" >&2
  exit 1
fi

# tar incremental: chỉ lưu delta so với snapshot trước
# lần đầu sẽ là full baseline

tar -czf "$ARCHIVE" \
  --listed-incremental="$SNAPSHOT_FILE" \
  --warning=no-file-changed \
  --exclude='*/node_modules/*' \
  --exclude='*/.git/*' \
  --exclude='*.log' \
  --exclude='*.tmp' \
  --exclude='*.cache' \
  --exclude='*/media/*' \
  "${INCLUDES[@]}"

chmod 600 "$ARCHIVE"

# giữ tối đa 20 bản incremental gần nhất
ls -1t "${OUTPUT_DIR}"/openclaw-incremental_*.tar.gz 2>/dev/null | tail -n +21 | xargs -r rm -f

echo "INCREMENTAL_BACKUP_OK: $ARCHIVE"
