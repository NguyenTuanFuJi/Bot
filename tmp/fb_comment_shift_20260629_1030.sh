#!/usr/bin/env bash
set -euo pipefail

PROFILE="${FB_PROFILE:-facebook_fujith}"
PAGE_ID="$1"
shift
POST_IDS=("$@")

export FB_PROFILE="$PROFILE"

tmp_dir="/home/tuan/.openclaw/workspace/tmp/fb_comment_shift_20260629_1030"
mkdir -p "$tmp_dir"

for pid in "${POST_IDS[@]}"; do
  safe_pid="${pid//\//_}"
  out="$tmp_dir/${safe_pid}.json"
  node /home/tuan/.openclaw/workspace/skills/facebook-page-manager/scripts/cli.js comments list --post "$pid" --limit 25 > "$tmp_dir/${safe_pid}.txt" || true
  # convert stdout table-ish output into json best-effort? We'll instead call API directly with node one-liner.
  node - <<NODE
import fs from 'fs';
const { readFileSync, existsSync } = fs;
const SKILL_DIR = '/home/tuan/.openclaw/workspace/skills/facebook-page-manager';
const CREDENTIALS_ROOT = SKILL_DIR + '/credentials';
const PROFILE = process.env.FB_PROFILE || 'facebook_fujith';
const ENV_FILE = CREDENTIALS_ROOT + '/' + PROFILE + '/.env';
const TOKENS_FILE = CREDENTIALS_ROOT + '/' + PROFILE + '/tokens.json';

function loadEnv(file) {
  if (!existsSync(file)) return {};
  const out = {};
  for (const line of readFileSync(file, 'utf-8').split(/\r?\n/)) {
    if (!line || line.trim().startsWith('#')) continue;
    const idx = line.indexOf('=');
    if (idx === -1) continue;
    out[line.slice(0, idx).trim()] = line.slice(idx + 1).trim();
  }
  return out;
}

const env = loadEnv(ENV_FILE);
const GRAPH_API_VERSION = env.GRAPH_API_VERSION || 'v21.0';
const tokens = JSON.parse(readFileSync(TOKENS_FILE, 'utf-8'));
const userToken = tokens.user_token;

const url = new URL('https://graph.facebook.com/' + GRAPH_API_VERSION + '/${pid}/comments');
url.searchParams.set('access_token', userToken);
url.searchParams.set('fields', 'id,message,from,created_time,like_count,is_hidden');
url.searchParams.set('limit', '25');

const resp = await fetch(url);
const data = await resp.json();
fs.writeFileSync('${out}', JSON.stringify(data, null, 2));
NODE
done
