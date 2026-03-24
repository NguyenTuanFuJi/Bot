# WP-CLI Safe Ops

## 1) Search-replace an toàn
Luôn chạy thử trước:
```bash
wp search-replace 'http://oldsite.com' 'http://newsite.com' --dry-run --path=/var/www/html
```
Sau khi xác nhận mới chạy thật:
```bash
wp search-replace 'http://oldsite.com' 'http://newsite.com' --path=/var/www/html
```

## 2) Backup trước thao tác lớn
```bash
wp db export backup-$(date +%F-%H%M).sql --path=/var/www/html
```

## 3) Update plugin có kiểm soát
```bash
wp plugin update --all --path=/var/www/html
wp plugin list --path=/var/www/html --format=table
```

## 4) Hậu kiểm nhanh
- Mở trang chủ và 3 trang quan trọng
- Kiểm tra lỗi PHP / lỗi plugin
- Kiểm tra đăng bài mới có hoạt động
