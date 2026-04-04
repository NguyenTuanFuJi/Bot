#!/usr/bin/env bash
set -euo pipefail
cd /home/tuan/.openclaw/workspace/skills/facebook-page-manager
FB_PROFILE=facebook_fujith /usr/bin/env bash scripts/preflight.sh
FB_PROFILE=facebook_fujith /usr/bin/env bash scripts/cron-safe-post-album.sh \
  --page 695286863979169 \
  --message-file /home/tuan/.openclaw/workspace/tmp/fb-20260405-0800-niem-tin.txt \
  --photo /home/tuan/.openclaw/media/inbound/file_183---bb90ac15-1fa8-45fa-83de-68f7e2a29cfa.jpg \
  --photo /home/tuan/.openclaw/media/inbound/file_184---07ef996c-eb38-4214-a425-3c5f7213061f.jpg \
  --photo /home/tuan/.openclaw/media/inbound/file_185---f6484f18-c5f8-4f62-b1cf-6441ef76c7c2.jpg \
  --photo /home/tuan/.openclaw/media/inbound/file_186---1e6d7cdf-81f5-41be-9f7e-9616706b29f0.jpg \
    --photo /home/tuan/.openclaw/media/inbound/file_187---9855f8ef-2a01-49c7-9ab9-c35e75738af2.jpg \
  >> /home/tuan/.openclaw/workspace/skills/facebook-page-manager/logs/cron.log 2>&1
