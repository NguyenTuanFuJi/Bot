#!/usr/bin/env bash
set -euo pipefail
cd /home/tuan/.openclaw/workspace
source skills/wordpress-cli-app-password/.env
python3 - <<'PY'
import json
from pathlib import Path
html = Path('tmp/post-web-20260418-nha-cai-tao-lap-thang-may.html').read_text(encoding='utf-8')
p = json.loads(Path('tmp/wp_create_post_20260418.json').read_text(encoding='utf-8'))
p['content'] = html
Path('tmp/wp_create_post_20260418.final.json').write_text(json.dumps(p, ensure_ascii=False), encoding='utf-8')
PY
curl -sS -u "$WP_USER:$WP_APP_PASSWORD" -H 'Content-Type: application/json' -X POST "$WP_BASE_URL/?rest_route=/wp/v2/posts" --data-binary @tmp/wp_create_post_20260418.final.json | jq '{id,link,slug,status,title:.title.rendered,categories,meta}'
