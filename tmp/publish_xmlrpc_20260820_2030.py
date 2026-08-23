import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260820-2030.html').read_text()
title='Thang Máy Gia Đình Có Tầng Lửng: 6 Điểm Cần Tính Để Không Vướng Khi Thiết Kế'
slug='thang-may-gia-dinh-co-tang-lung-6-diem-can-tinh'
excerpt='Thang máy gia đình có tầng lửng cần chốt 6 điểm về cao độ, cửa tầng, kết cấu, tải trọng, thông gió và lối bảo trì trước khi thiết kế.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'thang máy gia đình có tầng lửng'},
 {'key':'_yoast_wpseo_metadesc','value':'Thang máy gia đình có tầng lửng cần chốt 6 điểm về cao độ, cửa tầng, kết cấu, tải trọng, thông gió và lối bảo trì.'},
 {'key':'_yoast_wpseo_title','value':'Thang máy gia đình có tầng lửng: 6 điểm cần tính'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False), flush=True)
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False), flush=True)
print(base+'/?p='+str(post_id), flush=True)
