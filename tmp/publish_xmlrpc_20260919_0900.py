import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260919-0900-phong-tho.html').read_text()
title='Thang Máy Gia Đình Gần Phòng Thờ: 6 Lưu Ý Để Bố Trí Kín Đáo, Thuận Tiện'
slug='thang-may-gia-dinh-gan-phong-tho-6-luu-y'
excerpt='Thang máy gia đình gần phòng thờ cần tính khoảng đệm, lối đi, độ ồn, tầm nhìn, cao độ sàn và an toàn để dùng thuận tiện, kín đáo.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'thang máy gia đình gần phòng thờ'},
 {'key':'_yoast_wpseo_metadesc','value':'Thang máy gia đình gần phòng thờ cần tính khoảng đệm, lối đi, độ ồn, tầm nhìn, cao độ sàn và an toàn để dùng thuận tiện, kín đáo.'},
 {'key':'_yoast_wpseo_title','value':'Thang máy gia đình gần phòng thờ: 6 lưu ý bố trí kín đáo'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False), flush=True)
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False), flush=True)
print(base+'/?p='+str(post_id), flush=True)
