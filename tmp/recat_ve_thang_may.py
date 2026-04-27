import json
import os
import re
from datetime import datetime
from pathlib import Path
import requests

ENV_PATH = Path('/home/tuan/.openclaw/workspace/skills/wordpress-cli-app-password/.env')
BASE_DIR = Path('/home/tuan/.openclaw/workspace/output/wp-bulk-category')
BASE_DIR.mkdir(parents=True, exist_ok=True)

# category ids
CAT_VE_THANG_MAY = 1
CAT_GIA_DINH = 84
CAT_KHACH_SAN = 82
CAT_KINH = 85

# load env
env = {}
for line in ENV_PATH.read_text(encoding='utf-8').splitlines():
    line=line.strip()
    if not line or line.startswith('#') or '=' not in line:
        continue
    k,v=line.split('=',1)
    env[k]=v.strip().strip('"').strip("'")

base = env['WP_BASE_URL'].rstrip('/')
auth = (env['WP_USER'], env['WP_APP_PASSWORD'])
api_posts = f"{base}/?rest_route=/wp/v2/posts"

sess = requests.Session()

# fetch posts in category 1 with pagination
posts = []
page = 1
while True:
    r = sess.get(api_posts, params={
        'categories': CAT_VE_THANG_MAY,
        'per_page': 100,
        'page': page,
        'status': 'publish,draft,future,pending,private',
        'context': 'edit',
        '_fields': 'id,status,title,categories,slug,date,link'
    }, auth=auth, timeout=30)
    if r.status_code == 400 and 'rest_post_invalid_page_number' in r.text:
        break
    r.raise_for_status()
    data = r.json()
    if not data:
        break
    posts.extend(data)
    total_pages = int(r.headers.get('X-WP-TotalPages', '1'))
    if page >= total_pages:
        break
    page += 1


def pick_category(title: str):
    t = (title or '').lower()
    # hotel first
    if any(k in t for k in ['khách sạn', 'khach san', 'hotel', 'resort']):
        return CAT_KHACH_SAN, 'khach-san'
    # glass elevator
    if any(k in t for k in ['thang máy kính', 'thang may kinh', 'kính', 'kinh', 'giếng trời', 'gieng troi', 'quan sát', 'quan sat']):
        return CAT_KINH, 'kinh'
    return CAT_GIA_DINH, 'gia-dinh'

before = []
after = []
errors = []
updated = 0
skipped = 0

for p in posts:
    pid = p['id']
    title = (p.get('title') or {}).get('raw') or (p.get('title') or {}).get('rendered') or ''
    cats_before = list(p.get('categories') or [])
    target_cat, rule = pick_category(title)

    # remove category 1, keep other categories, ensure target category present
    cats_new = [c for c in cats_before if c != CAT_VE_THANG_MAY]
    if target_cat not in cats_new:
        cats_new.append(target_cat)

    # no-op
    if sorted(cats_new) == sorted(cats_before):
        skipped += 1
        before.append({'id': pid, 'title': title, 'categories': cats_before, 'rule': rule, 'action': 'skip'})
        continue

    before.append({'id': pid, 'title': title, 'categories': cats_before, 'rule': rule, 'action': 'update', 'new_categories': cats_new})

    try:
        u = sess.post(f"{api_posts}/{pid}", json={'categories': cats_new}, auth=auth, timeout=30)
        u.raise_for_status()
        j = u.json()
        updated += 1
        after.append({'id': pid, 'title': title, 'categories': j.get('categories', []), 'status': j.get('status')})
    except Exception as e:
        errors.append({'id': pid, 'title': title, 'error': str(e), 'new_categories': cats_new})

stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
report = {
    'timestamp': stamp,
    'total_found': len(posts),
    'updated': updated,
    'skipped': skipped,
    'errors': len(errors),
    'before': before,
    'after': after,
    'error_items': errors,
}

out = BASE_DIR / f'recat-ve-thang-may-{stamp}.json'
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

print(json.dumps({
    'total_found': len(posts),
    'updated': updated,
    'skipped': skipped,
    'errors': len(errors),
    'report': str(out)
}, ensure_ascii=False))