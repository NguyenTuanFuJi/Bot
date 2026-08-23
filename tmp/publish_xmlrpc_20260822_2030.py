import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260822-2030.html').read_text()
title='Thang Máy Gia Đình Cho Người Dùng Xe Đẩy: 6 Điểm Cần Tính Từ Đầu'
slug='thang-may-gia-dinh-cho-nguoi-dung-xe-day'
excerpt='Thang máy gia đình cho người dùng xe đẩy cần chốt 6 điểm về lối đi, cửa tầng, cabin, bảng điều khiển, sàn và bảo trì ngay từ đầu.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'thang máy gia đình cho người dùng xe đẩy'},
 {'key':'_yoast_wpseo_metadesc','value':'Thang máy gia đình cho người dùng xe đẩy: 6 điểm cần chốt về lối đi, cửa tầng, cabin, bảng điều khiển, sàn và bảo trì.'},
 {'key':'_yoast_wpseo_title','value':'Thang máy gia đình cho người dùng xe đẩy: 6 điểm cần tính'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False), flush=True)
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False), flush=True)
print(base+'/?p='+str(post_id), flush=True)
