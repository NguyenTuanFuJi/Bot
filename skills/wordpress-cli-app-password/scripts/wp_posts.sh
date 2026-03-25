#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
shift || true

ENV_FILE=""
TITLE=""
CONTENT_FILE=""
CONTENT=""
STATUS=""
POST_ID=""
PER_PAGE="10"
DATE_GMT=""
EXCERPT=""
SLUG=""
FOCUSKW=""
SEO_TITLE=""
META_DESC=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env) ENV_FILE="$2"; shift 2;;
    --title) TITLE="$2"; shift 2;;
    --content-file) CONTENT_FILE="$2"; shift 2;;
    --content) CONTENT="$2"; shift 2;;
    --status) STATUS="$2"; shift 2;;
    --id) POST_ID="$2"; shift 2;;
    --per-page) PER_PAGE="$2"; shift 2;;
    --date-gmt) DATE_GMT="$2"; shift 2;;
    --excerpt) EXCERPT="$2"; shift 2;;
    --slug) SLUG="$2"; shift 2;;
    --focuskw) FOCUSKW="$2"; shift 2;;
    --seo-title) SEO_TITLE="$2"; shift 2;;
    --meta-desc) META_DESC="$2"; shift 2;;
    *) echo "Unknown arg: $1"; exit 1;;
  esac
done

if [[ -z "$ENV_FILE" ]]; then
  echo "Missing --env <file>"
  exit 1
fi

# shellcheck disable=SC1090
source "$ENV_FILE"

: "${WP_BASE_URL:?WP_BASE_URL is required}"
: "${WP_USER:?WP_USER is required}"
: "${WP_APP_PASSWORD:?WP_APP_PASSWORD is required}"

BASE="${WP_BASE_URL%/}"
# Chuẩn hóa cố định REST route để tương thích site không dùng /wp-json/*
API="${BASE}/?rest_route=/wp/v2/posts"
API_QSEP="&"

AUTH="$WP_USER:$WP_APP_PASSWORD"

json_escape() {
  jq -Rs . <<<"$1"
}

build_payload_create() {
  local title_json content_json excerpt_json

  if [[ -n "$CONTENT_FILE" ]]; then
    CONTENT="$(cat "$CONTENT_FILE")"
  fi

  title_json=$(json_escape "$TITLE")
  content_json=$(json_escape "$CONTENT")
  excerpt_json=$(json_escape "$EXCERPT")

  local create_status
  create_status="${STATUS:-draft}"

  jq -n \
    --argjson title "$title_json" \
    --argjson content "$content_json" \
    --arg status "$create_status" \
    --argjson excerpt "$excerpt_json" \
    --arg date_gmt "$DATE_GMT" \
    --arg slug "$SLUG" \
    --arg focuskw "$FOCUSKW" \
    --arg seo_title "$SEO_TITLE" \
    --arg meta_desc "$META_DESC" \
    '{
      title: $title,
      content: $content,
      status: $status
    }
    + (if $excerpt != "" then {excerpt: $excerpt} else {} end)
    + (if $date_gmt != "" then {date_gmt: $date_gmt} else {} end)
    + (if $slug != "" then {slug: $slug} else {} end)
    + (if ($focuskw != "" or $seo_title != "" or $meta_desc != "") then {
        meta: ({ }
          + (if $focuskw != "" then {"_yoast_wpseo_focuskw": $focuskw} else {} end)
          + (if $seo_title != "" then {"_yoast_wpseo_title": $seo_title} else {} end)
          + (if $meta_desc != "" then {"_yoast_wpseo_metadesc": $meta_desc} else {} end)
        )
      } else {} end)
  '
}

build_payload_update() {
  local title_json content_json excerpt_json

  if [[ -n "$CONTENT_FILE" ]]; then
    CONTENT="$(cat "$CONTENT_FILE")"
  fi

  title_json=$(json_escape "$TITLE")
  content_json=$(json_escape "$CONTENT")
  excerpt_json=$(json_escape "$EXCERPT")

  jq -n \
    --argjson title "$title_json" \
    --argjson content "$content_json" \
    --arg status "$STATUS" \
    --argjson excerpt "$excerpt_json" \
    --arg date_gmt "$DATE_GMT" \
    --arg slug "$SLUG" \
    --arg focuskw "$FOCUSKW" \
    --arg seo_title "$SEO_TITLE" \
    --arg meta_desc "$META_DESC" \
    '{ }
    + (if $title != "" then {title: $title} else {} end)
    + (if $content != "" then {content: $content} else {} end)
    + (if $status != "" then {status: $status} else {} end)
    + (if $excerpt != "" then {excerpt: $excerpt} else {} end)
    + (if $date_gmt != "" then {date_gmt: $date_gmt} else {} end)
    + (if $slug != "" then {slug: $slug} else {} end)
    + (if ($focuskw != "" or $seo_title != "" or $meta_desc != "") then {
        meta: ({ }
          + (if $focuskw != "" then {"_yoast_wpseo_focuskw": $focuskw} else {} end)
          + (if $seo_title != "" then {"_yoast_wpseo_title": $seo_title} else {} end)
          + (if $meta_desc != "" then {"_yoast_wpseo_metadesc": $meta_desc} else {} end)
        )
      } else {} end)
    + (if (.title|type=="string" and (.title|length)==0) then del(.title) else . end)
    + (if (.content|type=="string" and (.content|length)==0) then del(.content) else . end)
    + (if (.excerpt|type=="string" and (.excerpt|length)==0) then del(.excerpt) else . end)
  '
}

case "$ACTION" in
  create)
    [[ -n "$TITLE" ]] || { echo "Missing --title"; exit 1; }
    [[ -n "$CONTENT" || -n "$CONTENT_FILE" ]] || { echo "Missing --content or --content-file"; exit 1; }
    payload="$(build_payload_create)"
    curl -sS -u "$AUTH" -H 'Content-Type: application/json' -X POST "$API" -d "$payload" | jq
    ;;

  update)
    [[ -n "$POST_ID" ]] || { echo "Missing --id"; exit 1; }
    payload="$(build_payload_update)"
    curl -sS -u "$AUTH" -H 'Content-Type: application/json' -X POST "$API/$POST_ID" -d "$payload" | jq
    ;;

  list)
    code=$(curl -sS -u "$AUTH" -o /tmp/wp_list.json -w "%{http_code}" "${API}${API_QSEP}per_page=$PER_PAGE&_fields=id,date,status,title,link")
    [[ "$code" == "200" ]] || { echo "WP list FAIL http=$code"; head -c 300 /tmp/wp_list.json; echo; exit 1; }
    jq -e 'type=="array"' /tmp/wp_list.json >/dev/null
    jq -r '.[] | "\(.id)\t\(.date)\t\(.status)\t\(.title.rendered)\t\(.link)"' /tmp/wp_list.json
    ;;

  *)
    cat <<EOF
Usage:
  bash scripts/wp_posts.sh create --env .env --title "..." --content-file post.md --status draft [--slug ...] [--focuskw ...] [--seo-title ...] [--meta-desc ...]
  bash scripts/wp_posts.sh update --env .env --id 123 --title "..." --status publish [--slug ...] [--focuskw ...] [--seo-title ...] [--meta-desc ...]
  bash scripts/wp_posts.sh list --env .env --per-page 10
EOF
    exit 1
    ;;
esac
