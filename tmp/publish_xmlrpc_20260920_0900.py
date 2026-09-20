import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260920-0900-cai-tao.html').read_text()
title='Lắp Thang Máy Cho Nhà Đang Cải Tạo: 7 Điểm Cần Chốt Trước Khi Thi Công'
slug='lap-thang-may-cho-nha-dang-cai-tao'
excerpt='Lắp thang máy cho nhà đang cải tạo cần rà kết cấu, vị trí giếng thang, kích thước cabin, đường kỹ thuật, tiến độ và lối bảo trì từ đầu.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'lắp thang máy cho nhà đang cải tạo'},
 {'key':'_yoast_wpseo_metadesc','value':'Lắp thang máy cho nhà đang cải tạo cần rà kết cấu, vị trí giếng thang, kích thước cabin, đường kỹ thuật, tiến độ và lối bảo trì từ đầu.'},
 {'key':'_yoast_wpseo_title','value':'Lắp thang máy cho nhà đang cải tạo: 7 điểm cần chốt'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False), flush=True)
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False), flush=True)
print(base+'/?p='+str(post_id), flush=True)