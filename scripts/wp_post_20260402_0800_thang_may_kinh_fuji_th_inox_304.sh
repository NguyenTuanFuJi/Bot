#!/usr/bin/env bash
set -euo pipefail
bash /home/tuan/.openclaw/workspace/skills/wordpress-cli-app-password/scripts/wp_ops.sh create \
  --env /home/tuan/.openclaw/workspace/skills/wordpress-cli-app-password/.env \
  --mode rest \
  --title "Thang máy kính FUJI TH dùng inox 304, động cơ TORIN, tủ Nice3000 cho nhà ở hiện đại" \
  --content-file /home/tuan/.openclaw/workspace/tmp/post-web-20260402-thang-may-kinh-fuji-th-inox-304.html \
  --status publish \
  --slug "thang-may-kinh-fuji-th-inox-304-torin-nice3000-nha-o-hien-dai" \
  --focuskw "thang máy kính FUJI TH" \
  --seo-title "Thang máy kính FUJI TH dùng inox 304, động cơ TORIN, tủ Nice3000" \
  --meta-desc "Mẫu thang máy kính FUJI TH dùng inox 304 dày 1.2mm, khung nhôm sơn tĩnh điện màu xám đá, động cơ TORIN không hộp số, tủ Nice3000, kính an toàn 2 lớp màu ghi đậm sang trọng."
