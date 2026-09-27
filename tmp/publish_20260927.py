import html, json, urllib.request, urllib.error

ENDPOINT='https://thangmayfujith.com/xmlrpc.php'
USER='fuji-temp'
PASS='Kd1a iK2j KXAm cxMO HZjf KXDC'

def esc(s): return html.escape(str(s), quote=False)
def val(v):
    if isinstance(v, int): return f'<int>{v}</int>'
    return '<string>'+esc(v)+'</string>'
def struct(d):
    return '<struct>'+''.join('<member><name>'+esc(k)+'</name><value>'+val(v)+'</value></member>' for k,v in d.items())+'</struct>'
def call(method, params):
    body='<?xml version="1.0"?><methodCall><methodName>'+method+'</methodName><params>'+''.join('<param><value>'+ (val(p) if not isinstance(p,dict) else struct(p)) +'</value></param>' for p in params)+'</params></methodCall>'
    req=urllib.request.Request(ENDPOINT, data=body.encode(), headers={'Content-Type':'text/xml'})
    with urllib.request.urlopen(req, timeout=45) as r: return r.read().decode()

title='Đệm giảm chấn thang máy gia đình: 5 điểm cần kiểm tra để cabin chạy êm'
slug='dem-giam-chan-thang-may-gia-dinh'
focus='đệm giảm chấn thang máy gia đình'
meta='Đệm giảm chấn thang máy gia đình giúp hạn chế rung, bảo vệ thiết bị và tăng độ êm khi vận hành. Xem 5 điểm cần kiểm tra trước khi nghiệm thu và bảo trì.'
content='''<p>Độ êm của thang máy gia đình không chỉ phụ thuộc vào động cơ hay bộ điều khiển. Một chi tiết nhỏ nhưng có vai trò quan trọng là <strong>đệm giảm chấn</strong> – bộ phận giúp hấp thụ lực va chạm, hạn chế rung truyền vào kết cấu và hỗ trợ cabin dừng ổn định.</p>
<p>Nếu đệm bị lắp sai vị trí, xuống cấp hoặc không phù hợp với tải trọng, thang có thể phát sinh tiếng động bất thường, rung khi chạy hoặc khó đạt chất lượng nghiệm thu. Bài viết này chia sẻ 5 điểm gia chủ nên kiểm tra cùng đơn vị kỹ thuật.</p>
<figure class="wp-block-image size-large"><img src="https://thangmayfujith.com/wp-content/uploads/2026/08/quy-trinh-lap-dat-thang-may-1.jpg" alt="Kỹ thuật viên FUJI TH khảo sát hệ thống thang máy gia đình trước khi lắp đặt đệm giảm chấn" /><figcaption>Khảo sát thực tế giúp chọn đúng giải pháp giảm rung cho từng công trình.</figcaption></figure>
<h2>Đệm giảm chấn thang máy gia đình có tác dụng gì?</h2>
<p>Đệm giảm chấn thường được bố trí tại khu vực hố PIT, bên dưới cabin hoặc đối trọng tùy cấu hình thiết bị. Khi cabin đi quá hành trình thiết kế hoặc xảy ra tình huống cần bảo vệ, bộ phận này giúp giảm năng lượng va chạm trước khi lực truyền xuống kết cấu.</p>
<ul><li>Hạn chế lực truyền xuống đáy hố PIT.</li><li>Giảm nguy cơ hư hỏng cho cabin, khung đối trọng và thiết bị liên quan.</li><li>Hỗ trợ vận hành êm hơn khi hệ thống được căn chỉnh đúng.</li><li>Tạo thêm lớp bảo vệ trong hệ thống an toàn tổng thể.</li></ul>
<p>Đệm giảm chấn không thay thế phanh an toàn, công tắc giới hạn hay bộ cứu hộ. Đây là một phần trong nhiều lớp bảo vệ và phải được kiểm tra đồng bộ.</p>
<h2>5 điểm cần kiểm tra trước khi nghiệm thu</h2>
<h3>1. Đúng chủng loại và tải trọng thiết kế</h3>
<p>Không nên chọn đệm theo kích thước nhìn bằng mắt hoặc dùng sản phẩm “tương đương” chưa được xác nhận. Chủng loại phải phù hợp với tải trọng, tốc độ, khối lượng cabin và cấu hình đối trọng của thang. Hồ sơ kỹ thuật cần thể hiện rõ thông số để đối chiếu khi nghiệm thu.</p>
<h3>2. Vị trí lắp đặt và khoảng hở</h3>
<p>Đệm phải nằm đúng tâm vùng tác động, bệ đỡ chắc chắn và không bị cấn bởi kết cấu xây dựng. Kỹ thuật viên cần đo khoảng hở theo cả chiều cao lẫn phương ngang, kiểm tra khi cabin và đối trọng ở vị trí thấp nhất. Hố PIT cũng phải đủ sạch để không làm ảnh hưởng đến hành trình của bộ phận này.</p>
<figure class="wp-block-image size-large"><img src="https://thangmayfujith.com/wp-content/uploads/2026/08/quy-trinh-lap-dat-thang-may-2.jpg" alt="Đội ngũ FUJI TH kiểm tra không gian hố thang máy gia đình và vị trí thiết bị an toàn" /><figcaption>Khoảng hở và bệ đỡ cần được kiểm tra trước khi hoàn thiện hố PIT.</figcaption></figure>
<h3>3. Bề mặt, chân đế và liên kết cố định</h3>
<p>Bề mặt đệm không được nứt, biến dạng hoặc có dấu hiệu chảy dầu bất thường. Chân đế phải phẳng, liên kết đủ chắc và không bị rỉ sét nghiêm trọng. Với công trình cải tạo, cần đặc biệt chú ý tình trạng nền hố PIT sau chống thấm để tránh việc đệm bị nghiêng hoặc lún.</p>
<h3>4. Sự đồng bộ với các thiết bị an toàn</h3>
<p>Kiểm tra đệm riêng lẻ là chưa đủ. Đơn vị lắp đặt cần đối chiếu với công tắc giới hạn, bộ giảm tốc, phanh an toàn, cảm biến cửa và hệ thống cứu hộ. Các thiết bị phải phối hợp đúng trình tự, không vô hiệu hóa công tắc hoặc tự ý thay đổi thông số để “chạy thử cho qua”.</p>
<h3>5. Ghi nhận vào hồ sơ bàn giao</h3>
<p>Gia chủ nên yêu cầu ghi rõ loại đệm, vị trí, ngày kiểm tra, kết quả chạy thử và khuyến nghị bảo trì trong hồ sơ bàn giao. Hình ảnh hố PIT trước khi đóng khu vực cũng hữu ích cho lần bảo dưỡng sau, nhất là khi thang đặt trong nhà cải tạo.</p>
<h2>Dấu hiệu đệm giảm chấn cần được kiểm tra lại</h2>
<ul><li>Xuất hiện tiếng va đập, tiếng kim loại hoặc tiếng “cộc” bất thường ở khu vực hố PIT.</li><li>Cabin rung mạnh hơn trước khi dừng hoặc sau khi khởi động.</li><li>Phát hiện dầu rò, cao su nứt, lò xo biến dạng hoặc bệ đỡ bị lệch.</li><li>Hố PIT ẩm, ngập nước hoặc có vật liệu xây dựng rơi vào.</li><li>Thang vừa trải qua sửa chữa lớn, thay đổi tải trọng hoặc thay thiết bị dẫn hướng.</li></ul>
<p>Khi có một trong các dấu hiệu trên, hãy ngừng tự ý kiểm tra bên trong hố PIT. Người sử dụng chỉ nên báo cho đơn vị bảo trì và giữ khu vực này không có người không phận sự.</p>
<figure class="wp-block-image size-large"><img src="https://thangmayfujith.com/wp-content/uploads/2026/08/quy-trinh-lap-dat-thang-may-9.jpg" alt="Kỹ thuật viên FUJI TH kiểm tra thiết bị cơ khí thang máy gia đình trong quá trình lắp đặt" /><figcaption>Kiểm tra đồng bộ thiết bị cơ khí giúp thang vận hành ổn định và an toàn hơn.</figcaption></figure>
<h2>Bảo trì đệm giảm chấn như thế nào?</h2>
<p>Trong mỗi kỳ bảo trì, kỹ thuật viên nên quan sát tình trạng bề mặt, chân đế, độ chắc của liên kết, dấu hiệu ăn mòn và tình trạng vệ sinh hố PIT. Nếu phát hiện nước, dầu hoặc vật cản, cần xử lý nguyên nhân trước khi đánh giá lại thiết bị.</p>
<p>Với gia đình, không nên tự bôi trơn, kê thêm vật liệu hoặc thay đệm bằng sản phẩm không rõ nguồn gốc. Những thay đổi nhỏ tại hố PIT có thể làm sai khoảng hở và ảnh hưởng đến chuỗi an toàn. Gia chủ có thể tham khảo thêm <a href="https://thangmayfujith.com/checklist-ho-pit-thang-may-gia-dinh/">checklist kiểm tra hố PIT thang máy gia đình</a> và <a href="https://thangmayfujith.com/ray-dan-huong-thang-may/">các điểm cần kiểm tra ở ray dẫn hướng</a> để có cái nhìn đầy đủ hơn.</p>
<h2>Kết luận</h2>
<p>Đệm giảm chấn thang máy gia đình là chi tiết nhỏ nhưng liên quan trực tiếp đến khả năng bảo vệ thiết bị và độ êm khi vận hành. Kiểm tra đúng chủng loại, vị trí, liên kết, sự đồng bộ và hồ sơ bàn giao sẽ giúp gia chủ hạn chế phát sinh sau lắp đặt.</p>
<p>Nếu sếp đang chuẩn bị lắp thang hoặc cần kiểm tra lại hố PIT, FUJI TH có thể khảo sát hiện trạng và tư vấn phương án phù hợp với tải trọng, số tầng và kết cấu từng nhà. Liên hệ <strong>0989397282</strong> hoặc <strong>0924286386</strong> để được tư vấn.</p>'''
fields={'post_name':slug,'post_content':content,'post_status':'draft','post_excerpt':'Đệm giảm chấn là chi tiết quan trọng giúp thang máy gia đình giảm rung và bảo vệ thiết bị.','post_author':1,'terms_names':{'category':['Chia sẻ - Kinh nghiệm']},'custom_fields':[{'key':'_yoast_wpseo_focuskw','value':focus},{'key':'_yoast_wpseo_metadesc','value':meta},{'key':'_yoast_wpseo_title','value':'Đệm giảm chấn thang máy gia đình: 5 điểm cần kiểm tra'}]}
r=call('wp.newPost',[1,USER,PASS,fields])
print(r)
import re
m=re.search(r'<name>post_id</name>\s*<value><string>(\d+)</string>',r) or re.search(r'<name>post_id</name>\s*<value><int>(\d+)</int>',r)
if not m:
    raise SystemExit('NO_POST_ID')
post_id=int(m.group(1))
# Publish and repeat SEO fields to ensure Yoast values persist.
update={'post_status':'publish','post_name':slug,'custom_fields':fields['custom_fields']}
r2=call('wp.editPost',[1,USER,PASS,post_id,update])
print(r2)
print('POST_ID',post_id)
