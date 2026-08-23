import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260817-0900.html').read_text()
title='Thang Máy Gia Đình Có Trẻ Nhỏ: 7 Điểm Nên Chốt Để Dùng An Toàn'
slug='thang-may-gia-dinh-co-tre-nho-7-diem-dung-an-toan'
excerpt='Thang máy gia đình có trẻ nhỏ cần chốt 7 điểm về vị trí, cửa tầng, bảng điều khiển, cứu hộ và bảo trì để dùng an toàn mỗi ngày.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'thang máy gia đình có trẻ nhỏ'},
 {'key':'_yoast_wpseo_metadesc','value':'Thang máy gia đình có trẻ nhỏ cần chốt 7 điểm về vị trí, cửa tầng, điều khiển, cứu hộ và bảo trì để dùng an toàn mỗi ngày.'},
 {'key':'_yoast_wpseo_title','value':'Thang máy gia đình có trẻ nhỏ: 7 điểm dùng an toàn'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False), flush=True)
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False), flush=True)
print(base+'/?p='+str(post_id), flush=True)