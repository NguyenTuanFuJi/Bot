#!/usr/bin/env bash
set -euo pipefail
cd /home/tuan/.openclaw/workspace/skills/facebook-page-manager
FB_PROFILE=facebook_fujith /usr/bin/env bash scripts/preflight.sh
FB_PROFILE=facebook_fujith /usr/bin/env bash scripts/cron-safe-post-album.sh \
  --page 695286863979169 \
  --message-file /home/tuan/.openclaw/workspace/tmp/fb-post-20260404-0800-niem-tin.txt \
  --photo /home/tuan/.openclaw/media/inbound/file_178---cc04e226-ca74-4503-b418-1e7be9e6e817.jpg \
  --photo /home/tuan/.openclaw/media/inbound/file_179---7068b984-8898-42b2-976b-1a1b5741fd91.jpg \
  --photo /home/tuan/.openclaw/media/inbound/file_180---a112eb4b-4ff3-4c93-83e7-259010aa29ba.jpg \
  --photo /home/tuan/.openclaw/media/inbound/file_181---978927d1-04d4-494f-94cd-f0c07b69f431.jpg \
  >> /home/tuan/.openclaw/workspace/skills/facebook-page-manager/logs/cron.log 2>&1
