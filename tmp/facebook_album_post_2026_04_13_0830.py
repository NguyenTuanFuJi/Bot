import json
import os
import sys
import requests

PAGE_ID = '695286863979169'
TOKEN_FILE = '/home/tuan/.openclaw/workspace/skills/facebook-page-manager/credentials/facebook_fujith/tokens.json'
MESSAGE_FILE = '/home/tuan/.openclaw/workspace/tmp/facebook_post_2026-04-13_0830.normalized.txt'
PHOTOS = [
    '/home/tuan/.openclaw/workspace/tmp/facebook_2026-04-13_0830_images/file_216---245c25ae-4be8-417a-93b1-d686ffd191a6.jpg',
    '/home/tuan/.openclaw/workspace/tmp/facebook_2026-04-13_0830_images/file_217---47078aca-60a9-49fc-9f57-a38ebd9deda0.jpg',
    '/home/tuan/.openclaw/workspace/tmp/facebook_2026-04-13_0830_images/file_218---fae45c07-7630-458b-82ec-eb65acb11bda.jpg',
    '/home/tuan/.openclaw/workspace/tmp/facebook_2026-04-13_0830_images/file_219---1d685581-bb62-42af-9e84-2614a7f386a1.jpg',
    '/home/tuan/.openclaw/workspace/tmp/facebook_2026-04-13_0830_images/file_220---dd955776-9653-413e-b18b-8128a868920b.jpg',
]
API = 'https://graph.facebook.com/v21.0'

with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
    token = json.load(f)['pages'][PAGE_ID]['token']
with open(MESSAGE_FILE, 'r', encoding='utf-8') as f:
    message = f.read().strip()

session = requests.Session()
media_ids = []
for path in PHOTOS:
    with open(path, 'rb') as img:
        resp = session.post(
            f'{API}/{PAGE_ID}/photos',
            data={'published': 'false', 'access_token': token},
            files={'source': (os.path.basename(path), img, 'image/jpeg')},
            timeout=120,
        )
    try:
        data = resp.json()
    except Exception:
        print('UPLOAD_NONJSON', resp.status_code, resp.text)
        sys.exit(1)
    if 'id' not in data:
        print('UPLOAD_FAIL', path, json.dumps(data, ensure_ascii=False))
        sys.exit(1)
    media_ids.append(data['id'])

payload = {'message': message, 'access_token': token}
for i, media_id in enumerate(media_ids):
    payload[f'attached_media[{i}]'] = json.dumps({'media_fbid': media_id}, ensure_ascii=False)

resp = session.post(f'{API}/{PAGE_ID}/feed', data=payload, timeout=120)
try:
    data = resp.json()
except Exception:
    print('POST_NONJSON', resp.status_code, resp.text)
    sys.exit(1)
if 'id' not in data:
    print('POST_FAIL', json.dumps(data, ensure_ascii=False))
    sys.exit(1)
print('POST_OK', data['id'])
