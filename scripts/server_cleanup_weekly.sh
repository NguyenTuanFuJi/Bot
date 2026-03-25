#!/usr/bin/env bash
set -euo pipefail

LOG_DIR="/home/tuan/.openclaw/workspace/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/server_cleanup_weekly.log"

log(){
  echo "[$(date '+%F %T')] $*" | tee -a "$LOG_FILE"
}

run_cmd(){
  local desc="$1"; shift
  if "$@" >>"$LOG_FILE" 2>&1; then
    log "OK: $desc"
  else
    log "SKIP/FAIL: $desc"
  fi
}

run_sudo_cmd(){
  local desc="$1"; shift
  if command -v sudo >/dev/null 2>&1 && sudo -n true >/dev/null 2>&1; then
    if sudo "$@" >>"$LOG_FILE" 2>&1; then
      log "OK: $desc"
    else
      log "FAIL: $desc"
    fi
  else
    log "SKIP: $desc (không có sudo không mật khẩu)"
  fi
}

log "=== Weekly cleanup start ==="
run_cmd "apt cache clean" apt clean
run_cmd "remove user crash dumps" bash -lc 'rm -rf /home/tuan/.cache/*/crash/* 2>/dev/null || true'
run_sudo_cmd "journal vacuum 14d" journalctl --vacuum-time=14d
run_sudo_cmd "remove /var/crash files" bash -lc 'rm -rf /var/crash/* 2>/dev/null || true'
run_sudo_cmd "tmp cleanup" bash -lc 'find /tmp -type f -mtime +7 -delete 2>/dev/null || true'
log "=== Weekly cleanup done ==="
