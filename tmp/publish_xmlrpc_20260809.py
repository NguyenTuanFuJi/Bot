import os, json, xmlrpc.client
from pathlib import Path
base=os.environ['WP_BASE_URL'].rstrip('/')
server=xmlrpc.client.ServerProxy(base+'/xmlrpc.php', allow_none=True)
user=os.environ['WP_USER']; pw=os.environ['WP_APP_PASSWORD']
content=Path('/home/tuan/.openclaw/workspace/tmp/web-20260809-0900.html').read_text()
seo=[
 {'key':'_yoast_wpseo_focuskw','value':'thang máy gia đình kêu to vào ban đêm'},
 {'key':'_yoast_wpseo_metadesc','value':'Thang máy gia đình kêu to vào ban đêm có thể do cửa, ray, cabin hoặc hệ thống truyền động. Xem 6 loại tiếng ồn và cách xử lý an toàn.'},
 {'key':'_yoast_wpseo_title','value':'Thang máy gia đình kêu to ban đêm: 6 nguyên nhân cần biết'},
]
post={
 'post_title':'Thang Máy Gia Đình Kêu To Vào Ban Đêm: 6 Dấu Hiệu Cần Kiểm Tra',
 'post_name':'thang-may-gia-dinh-keu-to-vao-ban-dem',
 'post_content':content,
 'post_status':'draft','post_type':'post',
 'post_excerpt':'Phân biệt 6 loại tiếng ồn thường gặp ở thang máy gia đình vào ban đêm, dấu hiệu nguy hiểm và checklist ghi nhận trước khi gọi kỹ thuật.',
 'terms_names': {'category':['Chia sẻ - Kinh nghiệm']}, 'custom_fields':seo,
}
post_id=server.wp.newPost(0,user,pw,post)
print(json.dumps({'draft_id':post_id},ensure_ascii=False))
updated={'post_status':'publish','post_title':post['post_title'],'post_name':post['post_name'],'post_content':content,'post_excerpt':post['post_excerpt'],'custom_fields':seo}
ok=server.wp.editPost(0,user,pw,post_id,updated)
print(json.dumps({'published':bool(ok),'id':post_id},ensure_ascii=False))
print(base+'/?p='+str(post_id))
