import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
u=os.environ['WP_USER']; p=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260813-0900-huong-dan-su-dung.html').read_text()
title='Hướng Dẫn Sử Dụng Thang Máy Gia Đình Đúng Cách: 5 Thói Quen An Toàn'
slug='huong-dan-su-dung-thang-may-gia-dinh-dung-cach'
excerpt='Hướng dẫn sử dụng thang máy gia đình đúng cách: cách vào cabin, bấm nút, xử lý quá tải, mất điện và nhận biết lúc cần gọi kỹ thuật viên.'
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'sử dụng thang máy gia đình'},
 {'key':'_yoast_wpseo_metadesc','value':'Hướng dẫn sử dụng thang máy gia đình đúng cách: 5 thói quen an toàn, xử lý mất điện, quá tải và dấu hiệu cần gọi kỹ thuật viên.'},
 {'key':'_yoast_wpseo_title','value':'Sử dụng thang máy gia đình đúng cách: 5 thói quen an toàn'},
]
post={'post_title':title,'post_name':slug,'post_content':content,'post_status':'draft','post_type':'post','post_excerpt':excerpt,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':seo}
post_id=server.wp.newPost(0,u,p,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False))
updated={'post_status':'publish','post_title':title,'post_name':slug,'post_content':content,'post_excerpt':excerpt,'custom_fields':seo}
ok=server.wp.editPost(0,u,p,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False))
print(base+'/?p='+str(post_id))
