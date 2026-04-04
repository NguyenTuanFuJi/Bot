#!/usr/bin/env bash
set -euo pipefail
cd /home/tuan/.openclaw/workspace/skills/facebook-page-manager
FB_PROFILE=facebook_fujith /usr/bin/env bash scripts/preflight.sh
FB_PROFILE=facebook_fujith /usr/bin/env bash scripts/cron-safe-post.sh \
  --page 695286863979169 \
  --message-file /home/tuan/.openclaw/workspace/tmp/fb-20260405-2030-3loi.txt \
  >> /home/tuan/.openclaw/workspace/skills/facebook-page-manager/logs/cron.log 2>&1
