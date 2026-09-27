import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260925-2030.html').read_text()
title='Tay Vịn Cabin Thang Máy Gia Đình: 6 Tiêu Chí Chọn An Toàn, Dễ Dùng'
slug='tay-vin-cabin-thang-may-gia-dinh'
excerpt='Tay vịn cabin thang máy gia đình cần vừa tầm tay, chắc chắn, dễ vệ sinh và không cản lối ra vào để sử dụng an toàn, thuận tiện mỗi ngày.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'tay vịn cabin thang máy'},
 {'key':'_yoast_wpseo_metadesc','value':'Tay vịn cabin thang máy gia đình cần vừa tầm tay, chắc chắn, dễ vệ sinh và không cản lối ra vào để sử dụng an toàn, thuận tiện mỗi ngày.'},
 {'key':'_yoast_wpseo_title','value':'Tay vịn cabin thang máy: 6 tiêu chí chọn an toàn'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False), flush=True)
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False), flush=True)
print(base+'/?p='+str(post_id), flush=True)
