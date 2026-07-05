import { readFileSync, existsSync, writeFileSync } from "fs";
import { join } from "path";

const SKILL_DIR = "/home/tuan/.openclaw/workspace/skills/facebook-page-manager";
const CREDENTIALS_ROOT = join(SKILL_DIR, "credentials");
const PROFILE = process.env.FB_PROFILE || "facebook_fujith";
const ENV_FILE = join(CREDENTIALS_ROOT, PROFILE, ".env");
const TOKENS_FILE = join(CREDENTIALS_ROOT, PROFILE, "tokens.json");

function loadEnv(file) {
  if (!existsSync(file)) return {};
  const out = {};
  for (const line of readFileSync(file, "utf-8").split(/\r?\n/)) {
    if (!line || line.trim().startsWith("#")) continue;
    const idx = line.indexOf("=");
    if (idx === -1) continue;
    out[line.slice(0, idx).trim()] = line.slice(idx + 1).trim();
  }
  return out;
}

const env = loadEnv(ENV_FILE);
const GRAPH_API_VERSION = env.GRAPH_API_VERSION || "v21.0";
const tokens = JSON.parse(readFileSync(TOKENS_FILE, "utf-8"));
const pageId = "695286863979169";
const pageToken = tokens.pages?.[pageId]?.token;
const userToken = tokens.user_token;

async function apiGet(endpoint, token, params = {}) {
  const url = new URL(`https://graph.facebook.com/${GRAPH_API_VERSION}/${endpoint}`);
  url.searchParams.set("access_token", token);
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
  const resp = await fetch(url);
  const data = await resp.json();
  if (!resp.ok) throw new Error(`API ${resp.status}: ${JSON.stringify(data)}`);
  return data;
}

const posts = await apiGet(`${pageId}/posts`, pageToken, {
  fields: "id,message,created_time,permalink_url,comments.summary(true)",
  limit: "20",
});

const result = [];
for (const post of posts.data || []) {
  const commentCount = post.comments?.summary?.total_count || 0;
  if (!commentCount) continue;
  const comments = await apiGet(`${post.id}/comments`, userToken, {
    fields: "id,message,from,created_time,like_count,is_hidden",
    limit: "25",
  });
  result.push({
    post_id: post.id,
    post_url: post.permalink_url || null,
    comment_count: commentCount,
    comments: (comments.data || []).map((c) => ({
      id: c.id,
      message: c.message || "",
      from: c.from?.name || null,
      created_time: c.created_time,
      like_count: c.like_count || 0,
      is_hidden: !!c.is_hidden,
    })),
  });
}

const out = {
  checked_at: new Date().toISOString(),
  page_id: pageId,
  posts_with_comments: result,
};

writeFileSync("/home/tuan/.openclaw/workspace/tmp/fb_comment_scan_20260629_1030_result.json", JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
