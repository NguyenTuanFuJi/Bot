#!/usr/bin/env bash
set -euo pipefail

# Weekly snapshot backup for CLIProxyAPI into the workspace-taizi git repo,
# then push via deploy key.

SRC_DIR="/home/linuxlite/CLIProxyAPI"
REPO_DIR="/home/linuxlite/.openclaw/workspace-taizi"
OUT_DIR="$REPO_DIR/cliproxyapi_snapshots"
SSH_CFG="/home/linuxlite/.ssh/config"

mkdir -p "$OUT_DIR"

TS=$(date -u +"%Y-%m-%dT%H-%M-%SZ")
SNAP="$OUT_DIR/cliproxyapi_${TS}.tar.gz"

# Create tarball excluding VCS + volatile dirs
cd "$SRC_DIR"
tar --exclude='./.git' \
    --exclude='./logs' \
    --exclude='./temp' \
    --exclude='./conv' \
    --exclude='./refs' \
    -czf "$SNAP" .

cd "$REPO_DIR"

# Commit snapshot if changed/new
# (always new filename, so always staged)
git add ".gitignore" "$SNAP"

git commit -m "Weekly cliproxyapi snapshot ${TS}" || true

# Push using deploy key
GIT_SSH_COMMAND="ssh -F $SSH_CFG" git push

echo "OK: created $SNAP"
