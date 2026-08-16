import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260812-2030-ban-giao.html').read_text()
title='Checklist Bàn Giao Thang Máy Gia Đình: 7 Hạng Mục Cần Kiểm Tra'
slug='checklist-ban-giao-thang-may-gia-dinh'
excerpt='Checklist 7 hạng mục cần kiểm tra khi bàn giao thang máy gia đình: dừng tầng, cửa, nút bấm, cứu hộ, hồ sơ và lịch bảo trì.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'checklist bàn giao thang máy'},
 {'key':'_yoast_wpseo_metadesc','value':'Checklist bàn giao thang máy gia đình gồm 7 hạng mục: dừng tầng, cửa, nút bấm, cứu hộ, hồ sơ và lịch bảo trì cần kiểm tra.'},
 {'key':'_yoast_wpseo_title','value':'Checklist bàn giao thang máy gia đình: 7 hạng mục cần kiểm tra'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False))
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False))
print(base+'/?p='+str(post_id))
