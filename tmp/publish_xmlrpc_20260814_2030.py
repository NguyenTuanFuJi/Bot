import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260814-2030-bao-tri.html').read_text()
title='Bảo Trì Thang Máy Gia Đình: 6 Hạng Mục Nên Kiểm Tra Định Kỳ'
slug='bao-tri-thang-may-gia-dinh-6-hang-muc-kiem-tra'
excerpt='Bảo trì thang máy gia đình cần kiểm tra 6 hạng mục: cửa, độ êm, máy kéo, điện, hố PIT và hệ thống cứu hộ.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'bảo trì thang máy gia đình'},
 {'key':'_yoast_wpseo_metadesc','value':'Bảo trì thang máy gia đình cần kiểm tra 6 hạng mục: cửa, độ êm, máy kéo, điện, hố PIT và hệ thống cứu hộ.'},
 {'key':'_yoast_wpseo_title','value':'Bảo trì thang máy gia đình: 6 hạng mục nên kiểm tra'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False), flush=True)
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False), flush=True)
print(base+'/?p='+str(post_id), flush=True)
