#!/usr/bin/env bash
set -euo pipefail
WORK=/home/tuan/.openclaw/workspace
WP_DIR="$WORK/skills/wordpress-cli-app-password"
FB_DIR="$WORK/skills/facebook-page-manager"
TMP_MSG="$WORK/tmp/fb-20260405-1200-share-web.txt"

LAST_LINK=$(bash "$WP_DIR/scripts/wp_posts.sh" list --env "$WP_DIR/.env" --per-page 1 | awk -F'\t' '{print $5}' | head -n1)
if [ -z "$LAST_LINK" ]; then
  LAST_LINK="https://thangmayfujith.com"
fi

cat > "$TMP_MSG" <<EOF
THANG MÁY 450KG CHO NHÀ 4-5 TẦNG: NÊN CHỌN 2CO700 HAY 2CO800?

FUJI TH vừa lên bài phân tích dễ hiểu, sát thực tế công trình nhà phố.
Anh/chị đang làm nhà để lại kích thước hố thang, đội ngũ kỹ thuật tư vấn miễn phí.

Xem bài chi tiết tại:
$LAST_LINK

Hotline: 0924286386 - 0989397282
Website: https://thangmayfujith.com
EOF

cd "$FB_DIR"
FB_PROFILE=facebook_fujith /usr/bin/env bash scripts/preflight.sh
FB_PROFILE=facebook_fujith /usr/bin/env bash scripts/cron-safe-post.sh \
  --page 695286863979169 \
  --message-file "$TMP_MSG" \
  >> /home/tuan/.openclaw/workspace/skills/facebook-page-manager/logs/cron.log 2>&1
