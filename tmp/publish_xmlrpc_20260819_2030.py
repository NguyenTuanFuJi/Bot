import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260819-2030.html').read_text()
title='Cabin Inox Xước Cho Thang Máy Gia Đình: 6 Tiêu Chí Chọn Để Dùng Bền'
slug='cabin-inox-xuoc-cho-thang-may-gia-dinh-6-tieu-chi'
excerpt='Cabin inox xước cho thang máy gia đình cần được chọn theo 6 tiêu chí về bề mặt, độ đồng đều, diện tích, vệ sinh, chi tiết hoàn thiện và nghiệm thu.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'cabin inox xước thang máy gia đình'},
 {'key':'_yoast_wpseo_metadesc','value':'Cabin inox xước thang máy gia đình nên chọn theo 6 tiêu chí về bề mặt, độ bền, vệ sinh, chi tiết hoàn thiện và nghiệm thu.'},
 {'key':'_yoast_wpseo_title','value':'Cabin inox xước thang máy gia đình: 6 tiêu chí chọn để dùng bền'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False), flush=True)
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False), flush=True)
print(base+'/?p='+str(post_id), flush=True)