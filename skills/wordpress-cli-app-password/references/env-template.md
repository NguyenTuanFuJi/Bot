# Mẫu biến môi trường (.env)

```bash
# REST mode (Application Password)
WP_BASE_URL="https://example.com"
WP_USER="your-username"
WP_APP_PASSWORD="xxxx xxxx xxxx xxxx xxxx xxxx"

# WP-CLI mode
WP_PATH="/var/www/html"
# Optional nếu site multisite hoặc cần chỉ định domain
WP_URL="https://example.com"
```

Lưu ý:
- Không commit file `.env` chứa secret.
- Nên tách môi trường staging/production bằng 2 file env khác nhau.
