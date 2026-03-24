# WP-CLI Quick Ops

## Kiểm tra cơ bản
```bash
wp --info
wp core is-installed --path=/var/www/html
wp core version --path=/var/www/html
```

## Quản trị bài viết
```bash
wp post create --path=/var/www/html --post_type=post --post_status=draft --post_title="Tiêu đề" --post_content="Nội dung" --porcelain
wp post update 123 --path=/var/www/html --post_status=publish
wp post list --path=/var/www/html --post_type=post --fields=ID,post_date,post_status,post_title,url --format=table
```

## Plugin/Theme nhanh
```bash
wp plugin list --path=/var/www/html
wp plugin update --all --path=/var/www/html
wp theme list --path=/var/www/html
```

## Media
```bash
wp media regenerate --yes --path=/var/www/html
```
