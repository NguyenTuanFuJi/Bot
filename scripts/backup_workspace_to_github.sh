#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/tuan/.openclaw/workspace"
BRANCH="main"
REMOTE="origin"
SSH_CFG="/home/tuan/.ssh/config"

cd "$REPO_DIR"

# Ensure we're on the intended branch
current_branch="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$current_branch" != "$BRANCH" ]]; then
  git checkout "$BRANCH"
fi

# Refresh remote state first
GIT_SSH_COMMAND="ssh -F $SSH_CFG" git fetch "$REMOTE"

# Stage tracked changes, deletions, and new files not ignored
git add -A

# Only commit when something actually changed
if git diff --cached --quiet; then
  echo "No changes to backup."
  exit 0
fi

ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
git commit -m "Backup workspace (no secrets) ${ts}"
GIT_SSH_COMMAND="ssh -F $SSH_CFG" git push "$REMOTE" "$BRANCH"

echo "OK: workspace backup pushed at ${ts}"
