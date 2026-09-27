import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260923-0900.html').read_text()
title='Hố PIT thang máy gia đình: 8 điểm cần kiểm tra để tránh sửa chữa tốn kém'
slug='ho-pit-thang-may-gia-dinh-8-diem-can-kiem-tra'
excerpt='Checklist kiểm tra hố PIT thang máy gia đình: chống thấm, kích thước, giảm chấn, chiếu sáng, lối tiếp cận và hồ sơ bảo trì để tránh phát sinh chi phí.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'hố PIT thang máy gia đình'},
 {'key':'_yoast_wpseo_metadesc','value':'Checklist kiểm tra hố PIT thang máy gia đình: chống thấm, kích thước, giảm chấn, chiếu sáng, lối tiếp cận và hồ sơ bảo trì để tránh phát sinh chi phí.'},
 {'key':'_yoast_wpseo_title','value':'Hố PIT thang máy gia đình: 8 điểm cần kiểm tra | FUJI TH'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False), flush=True)
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False), flush=True)
print(base+'/?p='+str(post_id), flush=True)
