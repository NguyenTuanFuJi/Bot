#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
shift || true

ENV_FILE=""
MODE="wpcli"
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
    --mode) MODE="$2"; shift 2;;
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

run_rest() {
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  case "$ACTION" in
    preflight)
      : "${WP_BASE_URL:?WP_BASE_URL is required}"
      : "${WP_USER:?WP_USER is required}"
      : "${WP_APP_PASSWORD:?WP_APP_PASSWORD is required}"

      base="${WP_BASE_URL%/}"
      root_api="$base/?rest_route=/"

      code_root=$(curl -sS -o /tmp/wp_pre_root.json -w "%{http_code}" "$root_api")
      [[ "$code_root" == "200" ]] || { echo "REST preflight FAIL: REST root http=$code_root"; exit 1; }

      # check authenticated posts endpoint readable (rest_route only)
      posts_url="$base/?rest_route=/wp/v2/posts&per_page=1&_fields=id,status"

      code_posts=$(curl -sS -u "$WP_USER:$WP_APP_PASSWORD" -o /tmp/wp_pre_posts.json -w "%{http_code}" "$posts_url")
      [[ "$code_posts" == "200" ]] || { echo "REST preflight FAIL: posts endpoint http=$code_posts"; exit 1; }

      # 3) ensure response is JSON array
      jq -e 'type=="array"' /tmp/wp_pre_posts.json >/dev/null
      echo "REST preflight: OK"
      ;;

    create)
      args=(create --env "$ENV_FILE" --title "$TITLE" --status "$STATUS")
      [[ -n "$CONTENT_FILE" ]] && args+=(--content-file "$CONTENT_FILE")
      [[ -n "$CONTENT" ]] && args+=(--content "$CONTENT")
      [[ -n "$EXCERPT" ]] && args+=(--excerpt "$EXCERPT")
      [[ -n "$DATE_GMT" ]] && args+=(--date-gmt "$DATE_GMT")
      [[ -n "$SLUG" ]] && args+=(--slug "$SLUG")
      [[ -n "$FOCUSKW" ]] && args+=(--focuskw "$FOCUSKW")
      [[ -n "$SEO_TITLE" ]] && args+=(--seo-title "$SEO_TITLE")
      [[ -n "$META_DESC" ]] && args+=(--meta-desc "$META_DESC")
      bash "$script_dir/wp_posts.sh" "${args[@]}"
      ;;

    update)
      args=(update --env "$ENV_FILE" --id "$POST_ID" --status "$STATUS")
      [[ -n "$TITLE" ]] && args+=(--title "$TITLE")
      [[ -n "$CONTENT_FILE" ]] && args+=(--content-file "$CONTENT_FILE")
      [[ -n "$CONTENT" ]] && args+=(--content "$CONTENT")
      [[ -n "$EXCERPT" ]] && args+=(--excerpt "$EXCERPT")
      [[ -n "$DATE_GMT" ]] && args+=(--date-gmt "$DATE_GMT")
      [[ -n "$SLUG" ]] && args+=(--slug "$SLUG")
      [[ -n "$FOCUSKW" ]] && args+=(--focuskw "$FOCUSKW")
      [[ -n "$SEO_TITLE" ]] && args+=(--seo-title "$SEO_TITLE")
      [[ -n "$META_DESC" ]] && args+=(--meta-desc "$META_DESC")
      bash "$script_dir/wp_posts.sh" "${args[@]}"
      ;;

    publish)
      bash "$script_dir/wp_posts.sh" update --env "$ENV_FILE" --id "$POST_ID" --status publish
      ;;

    list)
      bash "$script_dir/wp_posts.sh" list --env "$ENV_FILE" --per-page "$PER_PAGE"
      ;;

    *)
      echo "Unsupported action for REST mode: $ACTION"
      exit 1
      ;;
  esac
}

run_wpcli() {
  : "${WP_PATH:?WP_PATH is required for wpcli mode}"

  wp_cmd=(wp --path="$WP_PATH")
  [[ -n "${WP_URL:-}" ]] && wp_cmd+=(--url="$WP_URL")

  case "$ACTION" in
    preflight)
      "${wp_cmd[@]}" core is-installed >/dev/null
      "${wp_cmd[@]}" core version >/dev/null
      echo "WP-CLI preflight: OK"
      ;;

    create)
      [[ -n "$TITLE" ]] || { echo "Missing --title"; exit 1; }
      [[ -n "$CONTENT" || -n "$CONTENT_FILE" ]] || { echo "Missing --content or --content-file"; exit 1; }
      if [[ -n "$CONTENT_FILE" ]]; then CONTENT="$(cat "$CONTENT_FILE")"; fi
      "${wp_cmd[@]}" post create --post_type=post --post_status="$STATUS" --post_title="$TITLE" --post_content="$CONTENT" ${EXCERPT:+--post_excerpt="$EXCERPT"} --porcelain
      ;;

    update)
      [[ -n "$POST_ID" ]] || { echo "Missing --id"; exit 1; }
      args=(post update "$POST_ID")
      [[ -n "$TITLE" ]] && args+=(--post_title="$TITLE")
      if [[ -n "$CONTENT_FILE" ]]; then CONTENT="$(cat "$CONTENT_FILE")"; fi
      [[ -n "$CONTENT" ]] && args+=(--post_content="$CONTENT")
      [[ -n "$STATUS" ]] && args+=(--post_status="$STATUS")
      [[ -n "$EXCERPT" ]] && args+=(--post_excerpt="$EXCERPT")
      "${wp_cmd[@]}" "${args[@]}"
      ;;

    publish)
      [[ -n "$POST_ID" ]] || { echo "Missing --id"; exit 1; }
      "${wp_cmd[@]}" post update "$POST_ID" --post_status=publish
      ;;

    list)
      "${wp_cmd[@]}" post list --post_type=post --posts_per_page="$PER_PAGE" --fields=ID,post_date,post_status,post_title,url --format=table
      ;;

    *)
      echo "Unsupported action for wpcli mode: $ACTION"
      exit 1
      ;;
  esac
}

case "$MODE" in
  rest) run_rest ;;
  wpcli) run_wpcli ;;
  *) echo "Invalid --mode (use: rest|wpcli)"; exit 1;;
esac
