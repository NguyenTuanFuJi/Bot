#!/usr/bin/env bash
set -euo pipefail
cd /home/tuan/.openclaw/workspace/skills/facebook-page-manager
FB_PROFILE=facebook_fujith /usr/bin/env bash scripts/preflight.sh
FB_PROFILE=facebook_fujith /usr/bin/env bash scripts/cron-safe-post-album.sh \
  --page 695286863979169 \
  --message-file /home/tuan/.openclaw/workspace/tmp/fb-post-20260402-0800-thang-may-kinh-450kg.txt \
  --photo /home/tuan/.openclaw/media/inbound/file_154---8975aef4-9f6e-4e7c-b07c-acdd219c856a.jpg \
  --photo /home/tuan/.openclaw/media/inbound/file_155---19a37e2d-237f-4288-9d38-588b84d1ebdf.jpg \
  --photo /home/tuan/.openclaw/media/inbound/file_156---66341d39-9ac2-484a-9f63-20ab2b3c1fa7.jpg \
  --photo /home/tuan/.openclaw/media/inbound/file_157---53165c30-4597-4e8b-a850-eb73b22e9ba6.jpg \
  --photo /home/tuan/.openclaw/media/inbound/file_158---ad166260-8b2c-4bda-8c11-dbb0b15fec79.jpg \
  --photo /home/tuan/.openclaw/media/inbound/file_159---47cc5fd4-a74a-4fc6-8d5c-8cf996ab2811.jpg \
  >> /home/tuan/.openclaw/workspace/skills/facebook-page-manager/logs/cron.log 2>&1
