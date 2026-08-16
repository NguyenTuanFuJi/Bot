import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260813-2030-khao-sat.html').read_text()
title='Khảo Sát Thang Máy Gia Đình Cho Nhà Ống: 6 Điểm Cần Rà Trước Khi Chốt Phương Án'
slug='khao-sat-thang-may-gia-dinh-cho-nha-ong'
excerpt='Khảo sát thang máy gia đình cho nhà ống cần rà 6 điểm: vị trí, giếng thang, hố PIT, hướng cửa, nguồn điện và tải trọng sử dụng.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'khảo sát thang máy gia đình'},
 {'key':'_yoast_wpseo_metadesc','value':'Khảo sát thang máy gia đình cho nhà ống cần rà 6 điểm: vị trí, giếng thang, hố PIT, hướng cửa, nguồn điện và tải trọng.'},
 {'key':'_yoast_wpseo_title','value':'Khảo sát thang máy gia đình cho nhà ống: 6 điểm cần rà'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False), flush=True)
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False), flush=True)
print(base+'/?p='+str(post_id), flush=True)
