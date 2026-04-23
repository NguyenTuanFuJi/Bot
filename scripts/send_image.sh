#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   scripts/send_image.sh <image_path> [caption] [target] [channel]
# Example:
#   scripts/send_image.sh ./tmp/test.png "Ảnh test" 8602538279 telegram

IMAGE_PATH="${1:-}"
CAPTION="${2:-}"
TARGET="${3:-8602538279}"
CHANNEL="${4:-telegram}"

if [[ -z "$IMAGE_PATH" ]]; then
  echo "Thiếu đường dẫn ảnh."
  echo "Dùng: scripts/send_image.sh <image_path> [caption] [target] [channel]"
  exit 1
fi

openclaw message send \
  --channel "$CHANNEL" \
  --target "$TARGET" \
  --media "$IMAGE_PATH" \
  --message "$CAPTION"
