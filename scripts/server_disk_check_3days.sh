#!/usr/bin/env bash
set -euo pipefail

LOG_DIR="/home/tuan/.openclaw/workspace/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/server_disk_check.log"

{
  echo "=== Disk check $(date '+%F %T') ==="
  df -h
  echo
  df -i
  echo
  if command -v journalctl >/dev/null 2>&1; then
    journalctl --disk-usage || true
  fi
  echo
} >> "$LOG_FILE" 2>&1
