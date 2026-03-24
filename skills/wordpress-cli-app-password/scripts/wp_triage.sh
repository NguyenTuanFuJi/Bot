#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

has_cmd() { command -v "$1" >/dev/null 2>&1; }

is_wp=false
if [[ -f "wp-config.php" || -d "wp-content" ]]; then
  is_wp=true
fi

wpcli_available=false
if has_cmd wp; then
  wpcli_available=true
fi

has_composer=false
[[ -f composer.json ]] && has_composer=true

has_node=false
[[ -f package.json ]] && has_node=true

has_phpstan=false
if [[ -f phpstan.neon || -f phpstan.neon.dist ]]; then
  has_phpstan=true
fi

project_type="content-site"
if [[ -d wp-content/plugins && -d wp-content/themes ]]; then
  project_type="wordpress-core-site"
elif [[ -f style.css && -f functions.php ]]; then
  project_type="theme"
elif [[ -f plugin.php || -f "$(basename "$PWD").php" ]]; then
  project_type="plugin"
fi

jq -n \
  --arg root "$PWD" \
  --arg project_type "$project_type" \
  --argjson is_wp "$is_wp" \
  --argjson wpcli_available "$wpcli_available" \
  --argjson has_composer "$has_composer" \
  --argjson has_node "$has_node" \
  --argjson has_phpstan "$has_phpstan" \
  '{
    root: $root,
    project_type: $project_type,
    is_wordpress: $is_wp,
    tools: {
      wpcli: $wpcli_available,
      composer: $has_composer,
      node: $has_node,
      phpstan: $has_phpstan
    },
    recommended_mode: (if $wpcli_available then "wpcli" else "rest" end)
  }'
