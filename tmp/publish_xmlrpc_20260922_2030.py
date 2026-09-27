import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260922-2030.html').read_text()
title='Khoảng Dừng Thang Máy Gia Đình: 6 Điểm Cần Chốt Trước Khi Xây'
slug='khoang-dung-thang-may-gia-dinh'
excerpt='Khoảng dừng thang máy gia đình cần chốt số tầng, cao độ sàn, hướng mở cửa, khoảng chờ, hoàn thiện và lối bảo trì trước khi xây.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'khoảng dừng thang máy gia đình'},
 {'key':'_yoast_wpseo_metadesc','value':'Khoảng dừng thang máy gia đình cần chốt số tầng, cao độ sàn, hướng mở cửa, khoảng chờ, hoàn thiện và lối bảo trì trước khi xây.'},
 {'key':'_yoast_wpseo_title','value':'Khoảng dừng thang máy gia đình: 6 điểm cần chốt trước khi xây'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False), flush=True)
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False), flush=True)
print(base+'/?p='+str(post_id), flush=True)