#!/usr/bin/env bash
set -euo pipefail
cd /home/tuan/.openclaw/workspace/skills/facebook-page-manager
FB_PROFILE=facebook_fujith /usr/bin/env bash scripts/preflight.sh
FB_PROFILE=facebook_fujith /usr/bin/env bash scripts/cron-safe-post.sh \
  --page 695286863979169 \
  --message-file /home/tuan/.openclaw/workspace/tmp/fb-20260405-0800-niem-tin.txt \
  --photo /home/tuan/.openclaw/media/inbound/file_183---bb90ac15-1fa8-45fa-83de-68f7e2a29cfa.jpg \
  >> /home/tuan/.openclaw/workspace/skills/facebook-page-manager/logs/cron.log 2>&1
