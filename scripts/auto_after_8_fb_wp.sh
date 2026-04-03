#!/usr/bin/env bash
set -euo pipefail

export TZ="Asia/Ho_Chi_Minh"
WORKDIR="/home/tuan/.openclaw/workspace"
FB_DIR="$WORKDIR/skills/facebook-page-manager"
WP_DIR="$WORKDIR/skills/wordpress-cli-app-password"
LOG="$WORKDIR/skills/facebook-page-manager/logs/auto-after-8.log"
mkdir -p "$(dirname "$LOG")" "$WORKDIR/tmp"

PAGE_ID="695286863979169"
FB_PROFILE="facebook_fujith"
FB_ENV="$FB_DIR/credentials/$FB_PROFILE/.env"
FB_TOKENS="$FB_DIR/credentials/$FB_PROFILE/tokens.json"
WP_ENV="$WP_DIR/.env"

NOW_LOCAL="$(date '+%F %T')"
TODAY="$(date +%F)"
HOUR="$(date +%H)"

log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

if [ "$HOUR" -lt 8 ]; then
  log "SKIP: before 08:00"
  exit 0
fi

log "START auto_after_8 check"

# 1) Check Facebook: already posted today?
FB_HAS_TODAY=$(python3 - <<'PY'
import json, urllib.request, datetime
from zoneinfo import ZoneInfo
from pathlib import Path

page_id="695286863979169"
tokens=json.loads(Path('/home/tuan/.openclaw/workspace/skills/facebook-page-manager/credentials/facebook_fujith/tokens.json').read_text())
page=tokens.get('pages',{}).get(page_id,{})
token=page.get('token','')
if not token:
    print('ERR_NO_TOKEN')
    raise SystemExit(0)
url=f"https://graph.facebook.com/v21.0/{page_id}/posts?fields=id,created_time,permalink_url&limit=10&access_token={token}"
try:
    data=json.loads(urllib.request.urlopen(url, timeout=20).read().decode())
except Exception:
    print('ERR_API')
    raise SystemExit(0)
items=data.get('data',[])
today=datetime.datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).date()
found=False
for it in items:
    ct=it.get('created_time')
    if not ct: continue
    # format: 2026-04-03T12:34:56+0000
    dt=datetime.datetime.strptime(ct,'%Y-%m-%dT%H:%M:%S%z').astimezone(ZoneInfo('Asia/Ho_Chi_Minh'))
    if dt.date()==today:
        found=True
        break
print('YES' if found else 'NO')
PY
)

if [ "$FB_HAS_TODAY" = "ERR_NO_TOKEN" ] || [ "$FB_HAS_TODAY" = "ERR_API" ]; then
  log "WARN: facebook check error=$FB_HAS_TODAY, continue with conservative skip"
  exit 0
fi

# 2) Check Website: already posted today?
WP_HAS_TODAY=$(bash "$WP_DIR/scripts/wp_posts.sh" list --env "$WP_ENV" --per-page 15 | awk -v d="$TODAY" 'index($2,d)==1 {print "YES"; exit} END{if(NR==0) print "NO"}')
if [ -z "$WP_HAS_TODAY" ]; then WP_HAS_TODAY="NO"; fi

log "CHECK: FB_HAS_TODAY=$FB_HAS_TODAY WP_HAS_TODAY=$WP_HAS_TODAY"

# Rule: only auto-post when both channels still have no post today
if [ "$FB_HAS_TODAY" = "YES" ] || [ "$WP_HAS_TODAY" = "YES" ]; then
  log "SKIP: already has post today on at least one channel"
  exit 0
fi

# 3) Build content
TITLE="Giải pháp thang máy an toàn và tối ưu cho công trình gia đình"
SLUG="giai-phap-thang-may-an-toan-toi-uu-$(date +%Y%m%d)"
META_DESC="Giải pháp thang máy an toàn, vận hành êm, tối ưu chi phí cho công trình gia đình từ FUJI TH. Tư vấn đúng nhu cầu, thi công chuẩn kỹ thuật, hậu mãi dài lâu."
FOCUSKW="giải pháp thang máy gia đình"
SEO_TITLE="Giải pháp thang máy gia đình an toàn và tối ưu | FUJI TH"

WEB_CONTENT_FILE="$WORKDIR/tmp/auto-web-solution-$TODAY.html"
cat > "$WEB_CONTENT_FILE" <<'HTML'
<h2>Giải pháp thang máy an toàn và tối ưu cho công trình gia đình</h2>
<p>Khi lựa chọn thang máy cho công trình, điều quan trọng không chỉ là mẫu mã mà còn là sự phù hợp thực tế với không gian xây dựng, nhu cầu sử dụng và chi phí vận hành lâu dài.</p>
<p>Tại <strong>FUJI TH</strong>, chúng tôi triển khai giải pháp theo hướng: khảo sát kỹ - tư vấn đúng - thi công chuẩn - bảo trì định kỳ, giúp thang máy vận hành êm ái và ổn định.</p>
<h3>3 yếu tố cốt lõi trong giải pháp</h3>
<ul>
  <li><strong>Tối ưu không gian:</strong> lựa chọn cấu hình cabin, cửa tầng, thông số hố thang phù hợp thực tế.</li>
  <li><strong>An toàn vận hành:</strong> thiết bị đồng bộ, lắp đặt đúng tiêu chuẩn kỹ thuật.</li>
  <li><strong>Hiệu quả lâu dài:</strong> bảo trì định kỳ và hỗ trợ kỹ thuật nhanh khi cần.</li>
</ul>
<p>Nếu anh/chị đang cần phương án phù hợp cho công trình, FUJI TH sẵn sàng tư vấn chi tiết theo đúng hiện trạng thực tế.</p>
<p><strong>Hotline:</strong> 0924286386 - 0989397282<br/>
<strong>Website:</strong> <a href="https://thangmayfujith.com">https://thangmayfujith.com</a></p>
HTML

# 4) Publish website first
WP_JSON=$(bash "$WP_DIR/scripts/wp_posts.sh" create \
  --env "$WP_ENV" \
  --title "$TITLE" \
  --content-file "$WEB_CONTENT_FILE" \
  --status publish \
  --slug "$SLUG" \
  --focuskw "$FOCUSKW" \
  --seo-title "$SEO_TITLE" \
  --meta-desc "$META_DESC")

WP_LINK=$(echo "$WP_JSON" | jq -r '.link // empty')
WP_ID=$(echo "$WP_JSON" | jq -r '.id // empty')
log "WEB_POSTED: id=$WP_ID link=$WP_LINK"

# 5) Publish facebook post with image
FB_MSG_FILE="$WORKDIR/tmp/auto-fb-solution-$TODAY.txt"
cat > "$FB_MSG_FILE" <<EOF
GIẢI PHÁP THANG MÁY AN TOÀN & TỐI ƯU CHO CÔNG TRÌNH GIA ĐÌNH

Mỗi công trình sẽ phù hợp với một phương án thang máy khác nhau.
FUJI TH tư vấn theo hiện trạng thực tế để tối ưu không gian, vận hành êm và đảm bảo an toàn lâu dài.

✅ Khảo sát kỹ trước khi triển khai
✅ Cấu hình phù hợp nhu cầu sử dụng
✅ Lắp đặt chuẩn kỹ thuật, hậu mãi rõ ràng

Xem thêm giải pháp chi tiết tại website:
$WP_LINK

Hotline: 0924286386 - 0989397282
Website: https://thangmayfujith.com

#ThangMayFujiTH #GiaiPhapThangMay #ThangMayGiaDinh
EOF

bash "$FB_DIR/scripts/preflight.sh" >/dev/null 2>&1
FB_CREATE_OUT=$(FB_PROFILE="$FB_PROFILE" node "$FB_DIR/scripts/cli.js" post create \
  --page "$PAGE_ID" \
  --message "$(cat "$FB_MSG_FILE")" \
  --photo "/home/tuan/.openclaw/media/inbound/file_178---cc04e226-ca74-4503-b418-1e7be9e6e817.jpg")

FB_POST_ID=$(echo "$FB_CREATE_OUT" | sed -n 's/.*ID: \(.*\)$/\1/p' | tail -1)
log "FB_POSTED: post_id=$FB_POST_ID"

# 6) Auto comment on the new Facebook post (best effort)
if [ -n "$FB_POST_ID" ]; then
  PAGE_TOKEN=$(jq -r --arg p "$PAGE_ID" '.pages[$p].token // empty' "$FB_TOKENS")
  if [ -n "$PAGE_TOKEN" ]; then
    COMMENT_MSG="FUJI TH đã cập nhật thêm bài chi tiết tại website: $WP_LINK | Hotline: 0924286386"
    CMT=$(curl -sS -X POST "https://graph.facebook.com/v21.0/$FB_POST_ID/comments" \
      -d "message=$COMMENT_MSG" \
      -d "access_token=$PAGE_TOKEN" || true)
    log "FB_COMMENT_RESULT: $CMT"
  else
    log "WARN: No page token to comment"
  fi
fi

log "DONE auto_after_8 success"
