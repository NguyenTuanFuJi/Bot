import requests
from pathlib import Path

ENV = Path('/home/tuan/.openclaw/workspace/skills/wordpress-cli-app-password/.env')

env = {}
for line in ENV.read_text(encoding='utf-8').splitlines():
    line=line.strip()
    if not line or line.startswith('#') or '=' not in line:
        continue
    k,v=line.split('=',1)
    env[k]=v.strip().strip('"').strip("'")

base = env['WP_BASE_URL'].rstrip('/')
auth = (env['WP_USER'], env['WP_APP_PASSWORD'])
url_get = f"{base}/?rest_route=/wp/v2/pages/101&context=edit"
url_update = f"{base}/?rest_route=/wp/v2/pages/101"

r = requests.get(url_get, auth=auth, timeout=30)
r.raise_for_status()
page = r.json()
content = page['content']['raw']

replacements = {
    '[blog_posts style="normal" col_spacing="small" columns="1" columns__md="2" depth="1" posts="1" tags="73" show_date="false"]':
    '[blog_posts style="normal" col_spacing="small" columns="1" columns__md="2" depth="1" posts="12" cat="84" orderby="date" order="DESC" show_date="false"]',

    '[blog_posts style="normal" col_spacing="small" columns="1" columns__md="2" depth="1" ids="2511,2381" posts="2" show_date="false"]':
    '[blog_posts style="normal" col_spacing="small" columns="1" columns__md="2" depth="1" posts="12" cat="85" orderby="date" order="DESC" show_date="false"]',

    '[blog_posts style="normal" col_spacing="small" columns="1" columns__md="2" depth="1" posts="1" tags="74" show_date="false"]':
    '[blog_posts style="normal" col_spacing="small" columns="1" columns__md="2" depth="1" posts="12" cat="82" orderby="date" order="DESC" show_date="false"]',

    '[blog_posts style="normal" col_spacing="small" columns="1" columns__md="2" depth="1" posts="1" cat="83" show_date="false"]':
    '[blog_posts style="normal" col_spacing="small" columns="1" columns__md="2" depth="1" posts="12" cat="83" orderby="date" order="DESC" show_date="false"]',

    '[blog_posts style="normal" col_spacing="small" columns="3" columns__md="2" depth="1" posts="3" orderby="rand" tags="76" show_date="false"]':
    '[blog_posts style="normal" col_spacing="small" columns="3" columns__md="2" depth="1" posts="12" orderby="date" order="DESC" tags="76" show_date="false"]',

    '[blog_posts style="normal" col_spacing="xsmall" columns="3" columns__md="1" depth="1" animate="bounceInLeft" cat="72" ids="2511" posts="3" image_height="56.25%"]':
    '[blog_posts style="normal" col_spacing="xsmall" columns="3" columns__md="1" depth="1" animate="bounceInLeft" cat="72" posts="12" orderby="date" order="DESC" image_height="56.25%"]'
}

new_content = content
changed = 0
for old, new in replacements.items():
    if old in new_content:
        new_content = new_content.replace(old, new)
        changed += 1

if new_content == content:
    print('NO_CHANGE')
    raise SystemExit

u = requests.post(url_update, auth=auth, json={'content': new_content}, timeout=30)
u.raise_for_status()
out = u.json()
print({'id': out['id'], 'status': out['status'], 'changed_blocks': changed, 'link': out.get('link')})