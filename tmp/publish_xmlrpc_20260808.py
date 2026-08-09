import os, json, xmlrpc.client, re
from pathlib import Path
from html import unescape

base=os.environ['WP_BASE_URL'].rstrip('/')
url=base+'/xmlrpc.php'
server=xmlrpc.client.ServerProxy(url, allow_none=True)
user=os.environ['WP_USER']; pw=os.environ['WP_APP_PASSWORD']
content=Path('tmp/web-20260808-2030.html').read_text()
# XML-RPC WordPress expects struct keys; custom_fields is a list of structs.
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'thang máy gia đình cho nhà có trẻ nhỏ'},
 {'key':'_yoast_wpseo_metadesc','value':'7 lưu ý chọn thang máy gia đình cho nhà có trẻ nhỏ: cửa chống kẹt, ánh sáng, sàn, cứu hộ và checklist nghiệm thu an toàn.'},
 {'key':'_yoast_wpseo_title','value':'Thang máy gia đình cho nhà có trẻ nhỏ: 7 lưu ý an toàn'},
]
post={
 'post_title':'Thang Máy Gia Đình Cho Nhà Có Trẻ Nhỏ: 7 Lưu Ý An Toàn Cần Chốt',
 'post_name':'thang-may-gia-dinh-cho-nha-co-tre-nho',
 'post_content':content,
 'post_status':'draft',
 'post_excerpt':'7 lưu ý thiết kế và nghiệm thu thang máy gia đình cho nhà có trẻ nhỏ, từ cửa chống kẹt, ánh sáng đến cách xử lý khi thang dừng bất thường.',
 'post_type':'post',
 'terms_names': {'category':['Chia sẻ - Kinh nghiệm']},
 'custom_fields':seo,
}
post_id=server.wp.newPost(0,user,pw,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False))
# Publish and retain SEO fields in the same edit call.
updated={
 'post_status':'publish',
 'post_title':post['post_title'],
 'post_name':post['post_name'],
 'post_content':content,
 'post_excerpt':post['post_excerpt'],
 'custom_fields':seo,
}
ok=server.wp.editPost(0,user,pw,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False))
print(base+'/?p='+str(post_id))
