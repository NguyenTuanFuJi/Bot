import re
from urllib.parse import urlparse
from pathlib import Path
import requests

ENV_PATH = Path('/home/tuan/.openclaw/workspace/skills/wordpress-cli-app-password/.env')

env = {}
for line in ENV_PATH.read_text(encoding='utf-8').splitlines():
    line = line.strip()
    if not line or line.startswith('#') or '=' not in line:
        continue
    k, v = line.split('=', 1)
    env[k] = v.strip().strip('"').strip("'")

base = env['WP_BASE_URL'].rstrip('/')
auth = (env['WP_USER'], env['WP_APP_PASSWORD'])
posts_api = f"{base}/?rest_route=/wp/v2/posts"
media_api = f"{base}/?rest_route=/wp/v2/media"

sess = requests.Session()

img_re = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.I)

def normalize_url(u: str):
    p = urlparse(u)
    return f"{p.scheme}://{p.netloc}{p.path}" if p.scheme and p.netloc else u.split('?')[0]

def fetch_posts():
    posts = []
    page = 1
    while True:
        r = sess.get(posts_api, params={
            'status': 'publish',
            'per_page': 100,
            'page': page,
            'context': 'edit',
            '_fields': 'id,title,content,featured_media,status,link'
        }, auth=auth, timeout=30)
        if r.status_code == 400 and 'rest_post_invalid_page_number' in r.text:
            break
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        posts.extend(batch)
        total_pages = int(r.headers.get('X-WP-TotalPages', '1'))
        if page >= total_pages:
            break
        page += 1
    return posts

def find_media_id_by_src(src: str):
    src_n = normalize_url(src)
    filename = src_n.rsplit('/', 1)[-1]
    if not filename:
        return None

    r = sess.get(media_api, params={
        'search': filename,
        'per_page': 50,
        '_fields': 'id,source_url'
    }, auth=auth, timeout=30)
    if r.status_code >= 400:
        return None
    items = r.json() if r.text.strip() else []
    if not isinstance(items, list):
        return None

    # exact normalized URL match first
    for m in items:
        su = normalize_url(m.get('source_url', ''))
        if su == src_n:
            return m.get('id')

    # fallback: same filename tail
    for m in items:
        su = normalize_url(m.get('source_url', ''))
        if su.endswith('/' + filename):
            return m.get('id')

    return None

posts = fetch_posts()
updated = []
skipped_no_img = []
skipped_no_media = []

for p in posts:
    if int(p.get('featured_media') or 0) != 0:
        continue

    raw = (p.get('content') or {}).get('raw') or (p.get('content') or {}).get('rendered') or ''
    m = img_re.search(raw)
    if not m:
        skipped_no_img.append(p['id'])
        continue

    src = m.group(1)
    media_id = find_media_id_by_src(src)
    if not media_id:
        skipped_no_media.append({'id': p['id'], 'src': src})
        continue

    u = sess.post(f"{posts_api}/{p['id']}", json={'featured_media': int(media_id)}, auth=auth, timeout=30)
    if u.status_code >= 400:
        skipped_no_media.append({'id': p['id'], 'src': src, 'error': u.text[:300]})
        continue

    updated.append({'id': p['id'], 'media_id': media_id, 'src': src, 'link': p.get('link', '')})

print({
    'publish_posts_total': len(posts),
    'updated_featured': len(updated),
    'skipped_no_img_in_content': len(skipped_no_img),
    'skipped_no_media_match': len(skipped_no_media),
    'updated_ids': [x['id'] for x in updated][:50],
})

# quick verification
r2 = sess.get(posts_api, params={
    'status': 'publish',
    'per_page': 100,
    'page': 1,
    'context': 'edit',
    '_fields': 'id,featured_media'
}, auth=auth, timeout=30)
r2.raise_for_status()
no_featured_first_page = sum(1 for x in r2.json() if int(x.get('featured_media') or 0) == 0)
print({'no_featured_first_page_after': no_featured_first_page})