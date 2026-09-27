import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260924-0900.html').read_text()
title='Thang Máy Gia Đình Cho Nhà Lệch Tầng: 6 Điểm Cần Khảo Sát Trước Khi Chọn'
slug='thang-may-gia-dinh-cho-nha-lech-tang'
excerpt='Thang máy gia đình cho nhà lệch tầng cần khảo sát cao độ, điểm dừng, bậc chuyển tiếp, giếng thang, kết cấu và lối bảo trì trước khi chốt phương án.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'thang máy gia đình cho nhà lệch tầng'},
 {'key':'_yoast_wpseo_metadesc','value':'Thang máy gia đình cho nhà lệch tầng cần khảo sát cao độ, điểm dừng, bậc chuyển tiếp, giếng thang, kết cấu và lối bảo trì trước khi chốt phương án.'},
 {'key':'_yoast_wpseo_title','value':'Thang máy gia đình cho nhà lệch tầng: 6 điểm cần khảo sát'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False), flush=True)
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False), flush=True)
print(base+'/?p='+str(post_id), flush=True)
