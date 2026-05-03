import json, os, subprocess
from pathlib import Path

base = os.environ['WP_BASE_URL'].rstrip('/')
auth = f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}"
raw_path = Path('/tmp/post2701_raw.html')
raw = raw_path.read_text()

files = [
    ('/home/tuan/.openclaw/media/inbound/file_340---624921d3-dc38-41ed-811a-32161cfce0a0.jpg', 'thang-may-nhap-khau-nha-4-6-tang-01.jpg', 'Thang máy nhập khẩu cho nhà 4-6 tầng tại công trình FUJI TH', 'Hình ảnh thang máy nhập khẩu cho nhà 4-6 tầng', 'Thang máy nhập khẩu nhà 4-6 tầng 01'),
    ('/home/tuan/.openclaw/media/inbound/file_341---570cf4f4-da1a-48e6-af28-aca846028448.jpg', 'thang-may-nhap-khau-nha-4-6-tang-02.jpg', 'Chi tiết thang máy nhập khẩu cho nhà phố 4-6 tầng', 'Hình ảnh chi tiết thang máy nhập khẩu cho nhà phố', 'Thang máy nhập khẩu nhà 4-6 tầng 02'),
    ('/home/tuan/.openclaw/media/inbound/file_342---5a7f2563-06d7-468b-90d6-2201e4b617cc.jpg', 'thang-may-nhap-khau-nha-4-6-tang-03.jpg', 'Mẫu thang máy gia đình nhập khẩu lắp cho nhà 4-6 tầng', 'Mẫu thang máy gia đình nhập khẩu', 'Thang máy nhập khẩu nhà 4-6 tầng 03'),
]

uploaded = []
for src, filename, alt, caption, title in files:
    r = subprocess.run([
        'curl','-sS','-u',auth,'-X','POST',
        '-H',f'Content-Disposition: attachment; filename={filename}',
        '-H','Content-Type: image/jpeg',
        '--data-binary', f'@{src}',
        f'{base}/?rest_route=/wp/v2/media'
    ], capture_output=True, text=True, check=True)
    data = json.loads(r.stdout)
    if not data.get('id'):
        raise SystemExit(r.stdout)
    media_id = data['id']
    src_url = data['source_url']
    payload = json.dumps({'alt_text': alt, 'caption': caption, 'title': title}, ensure_ascii=False)
    subprocess.run([
        'curl','-sS','-u',auth,'-X','POST','-H','Content-Type: application/json',
        f'{base}/?rest_route=/wp/v2/media/{media_id}','-d',payload
    ], capture_output=True, text=True, check=True)
    uploaded.append((media_id, src_url, alt))

img1 = f'''\n<figure class="wp-block-image size-large"><img src="{uploaded[0][1]}" alt="{uploaded[0][2]}"/></figure>\n'''
img2 = f'''\n<figure class="wp-block-image size-large"><img src="{uploaded[1][1]}" alt="{uploaded[1][2]}"/></figure>\n'''
img3 = f'''\n<figure class="wp-block-image size-large"><img src="{uploaded[2][1]}" alt="{uploaded[2][2]}"/></figure>\n'''

raw = raw.replace('</ul>\n<p>Chọn đúng tải trọng ngay từ đầu giúp tránh tình trạng cabin chật, cửa mở bất tiện hoặc phải điều chỉnh kết cấu về sau.</p>', '</ul>' + img1 + '<p>Chọn đúng tải trọng ngay từ đầu giúp tránh tình trạng cabin chật, cửa mở bất tiện hoặc phải điều chỉnh kết cấu về sau.</p>', 1)
raw = raw.replace('</ul>\n\n<h2>4) Kiểm tra nguồn điện và phương án đi dây từ sớm</h2>', '</ul>' + img2 + '\n\n<h2>4) Kiểm tra nguồn điện và phương án đi dây từ sớm</h2>', 1)
raw = raw.replace('<h2>Kết luận</h2>', img3 + '\n<h2>Kết luận</h2>', 1)

Path('/tmp/post2701_updated.html').write_text(raw)
payload = json.dumps({'content': raw}, ensure_ascii=False)
r = subprocess.run([
    'curl','-sS','-u',auth,'-X','POST','-H','Content-Type: application/json',
    f'{base}/?rest_route=/wp/v2/posts/2701','-d',payload
], capture_output=True, text=True, check=True)
print(r.stdout)
print('---UPLOADED---')
for item in uploaded:
    print('\t'.join(map(str, item)))
