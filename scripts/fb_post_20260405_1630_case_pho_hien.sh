#!/usr/bin/env bash
set -euo pipefail
cd /home/tuan/.openclaw/workspace/skills/facebook-page-manager
FB_PROFILE=facebook_fujith /usr/bin/env bash scripts/preflight.sh
FB_PROFILE=facebook_fujith /usr/bin/env bash scripts/cron-safe-post.sh \
  --page 695286863979169 \
  --message-file /home/tuan/.openclaw/workspace/tmp/fb-20260405-1630-case-pho-hien.txt \
  --photo /home/tuan/.openclaw/media/inbound/file_178---cc04e226-ca74-4503-b418-1e7be9e6e817.jpg \
  >> /home/tuan/.openclaw/workspace/skills/facebook-page-manager/logs/cron.log 2>&1
