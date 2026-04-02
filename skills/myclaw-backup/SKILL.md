---
name: myclaw-backup
description: Backup and restore OpenClaw configuration, workspace data, memory, credentials, and related runtime state. Use when the user wants to create a backup, schedule recurring backups, migrate to another machine, restore from an archive, or run a browser-based backup server. Treat this skill as highly sensitive because backups contain tokens, credentials, and other private system data.
---

# MyClaw Backup

Use this skill for full-instance backup and restore operations.

## Sensitivity
This skill handles highly sensitive data, including:
- bot tokens
- API keys
- credentials
- session and workspace state

Treat restore and server exposure as high-risk operations.

## Main scripts
- `scripts/backup.sh [output-dir]`
- `scripts/backup-incremental.sh [output-dir]`
- `scripts/restore.sh <archive> [--dry-run] [--overwrite-gateway-token]`
- `scripts/serve.sh start --token TOKEN [--port 7373]`
- `scripts/serve.sh stop|status`
- `scripts/schedule.sh [--interval daily|weekly|hourly]`

## Safe workflow

### Create backup
1. Choose the output directory
2. Run full or incremental backup
3. Confirm the archive exists and is stored securely

### Restore backup
1. Always run `restore.sh --dry-run` first
2. Review what will change
3. Run the real restore only after review
4. Confirm reconnect and recovery state after restore

### HTTP server mode
1. Start only with `--token`
2. Do not expose the server publicly without proper protection
3. Use it mainly for download, upload, and controlled restore workflows

## Read references when needed
- `references/what-gets-saved.md` for backup scope

## Rules
- Never skip dry-run before restore
- Never start the HTTP server without a token
- Do not casually move or share backup archives
- Preserve the destination gateway token unless the restore scenario truly requires overwrite

Use this skill when the user’s real goal is backup safety, migration, or recovery.