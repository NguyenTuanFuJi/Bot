import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260926-2030.html').read_text()
title='Thông Gió Cabin Thang Máy Gia Đình: 6 Điểm Cần Chốt Để Dùng Êm, An Toàn'
slug='thong-gio-cabin-thang-may-gia-dinh'
excerpt='Thông gió cabin thang máy gia đình cần tính đúng vị trí quạt, độ ồn, an toàn điện, khả năng vệ sinh và bảo trì để sử dụng thoải mái, an toàn.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'thông gió cabin thang máy'},
 {'key':'_yoast_wpseo_metadesc','value':'Thông gió cabin thang máy gia đình cần tính đúng vị trí quạt, độ ồn, an toàn điện, khả năng vệ sinh và bảo trì để sử dụng thoải mái, an toàn.'},
 {'key':'_yoast_wpseo_title','value':'Thông gió cabin thang máy gia đình: 6 điểm cần chốt'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False), flush=True)
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False), flush=True)
print(base+'/?p='+str(post_id), flush=True)
