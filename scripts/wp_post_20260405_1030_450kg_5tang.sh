#!/usr/bin/env bash
set -euo pipefail
cd /home/tuan/.openclaw/workspace/skills/wordpress-cli-app-password
bash scripts/wp_posts.sh create \
  --env /home/tuan/.openclaw/workspace/skills/wordpress-cli-app-password/.env \
  --title "Thang máy 450kg cho nhà 4-5 tầng: nên chọn 2CO700 hay 2CO800?" \
  --content-file /home/tuan/.openclaw/workspace/tmp/web-20260405-1030-450kg-5tang.html \
  --status publish \
  --slug "thang-may-450kg-4-5-tang-2co700-hay-2co800" \
  --focuskw "thang máy 450kg 5 tầng" \
  --seo-title "Thang máy 450kg 5 tầng: chọn 2CO700 hay 2CO800 | FUJI TH" \
  --meta-desc "Tư vấn chọn thang máy 450kg cho nhà 4-5 tầng: so sánh 2CO700 và 2CO800, kích thước hố thang phổ biến, giải pháp tối ưu từ FUJI TH." \
  >> /home/tuan/.openclaw/workspace/tmp/wp-post-20260405-1030.log 2>&1
