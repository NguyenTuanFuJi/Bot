import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260816-2030.html').read_text()
title='Lối Bảo Trì Thang Máy Gia Đình: 5 Khu Vực Cần Chừa Từ Khi Thiết Kế'
slug='loi-bao-tri-thang-may-gia-dinh-5-khu-vuc-can-chua'
excerpt='Lối bảo trì thang máy gia đình cần được tính từ sớm để kỹ thuật viên kiểm tra an toàn, không phải đục phá nội thất khi sửa chữa.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'lối bảo trì thang máy gia đình'},
 {'key':'_yoast_wpseo_metadesc','value':'Lối bảo trì thang máy gia đình cần chừa những khu vực nào? Checklist 5 vị trí giúp kiểm tra, sửa chữa an toàn và hạn chế đục phá nội thất.'},
 {'key':'_yoast_wpseo_title','value':'Lối bảo trì thang máy gia đình: 5 khu vực cần chừa'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False), flush=True)
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False), flush=True)
print(base+'/?p='+str(post_id), flush=True)
