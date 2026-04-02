#!/usr/bin/env node
/**
 * X -> Facebook Page digest poster
 * - Searches X for Clawdbot + Moltbot
 * - Prioritizes use-cases/automation posts
 * - Picks 1 tweet with an image (photo)
 * - Posts to a Facebook Page as a photo post with caption + links
 *
 * Requirements:
 * - X cookies in env: AUTH_TOKEN, CT0
 * - FB profile tokens.json under credentials/<profile>/tokens.json
 */

import { execFileSync } from "child_process";
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = join(__dirname, "..");
const PROFILE = process.env.FB_PROFILE || "facebook_fujith";
const TOKENS_FILE = process.env.FB_TOKENS_FILE || join(SKILL_DIR, "credentials", PROFILE, "tokens.json");

const GRAPH_API_VERSION = "v21.0";
const FB_BASE = `https://graph.facebook.com/${GRAPH_API_VERSION}`;

function requireEnv(name) {
  const v = process.env[name];
  if (!v) throw new Error(`Missing env ${name}`);
  return v;
}

function loadFbTokens() {
  if (!existsSync(TOKENS_FILE)) {
    throw new Error(`Missing FB tokens file: ${TOKENS_FILE}. Run auth flow first.`);
  }
  return JSON.parse(readFileSync(TOKENS_FILE, "utf-8"));
}

function birdSearchJson(query, count = 12) {
  const out = execFileSync(
    "bird",
    ["search", query, "-n", String(count), "--json", "--plain"],
    {
      env: {
        ...process.env,
        AUTH_TOKEN: requireEnv("AUTH_TOKEN"),
        CT0: requireEnv("CT0"),
      },
      stdio: ["ignore", "pipe", "pipe"],
      encoding: "utf-8",
    }
  );
  return JSON.parse(out);
}

function scoreTweet(t) {
  const text = (t.text || "").toLowerCase();
  let score = 0;

  const ts = Date.parse(t.createdAt || "");
  if (!Number.isNaN(ts)) {
    const ageHrs = (Date.now() - ts) / 36e5;
    if (ageHrs < 12) score += 8;
    else if (ageHrs < 24) score += 5;
    else if (ageHrs < 72) score += 2;
  }

  const keywords = [
    "use case",
    "use-case",
    "workflow",
    "automation",
    "automate",
    "agent",
    "email",
    "calendar",
    "telegram",
    "self-host",
    "self host",
    "setup",
    "guide",
    "tutorial",
    "workers",
    "cloudflare",
    "r2",
  ];
  for (const k of keywords) if (text.includes(k)) score += 2;

  if (t.media?.some((m) => m.type === "photo" && m.url)) score += 6;

  score += Math.min(6, (t.likeCount || 0) / 50);
  score += Math.min(4, (t.retweetCount || 0) / 20);

  const u = (t.author?.username || "").toLowerCase();
  if (u.includes("steipete") || u.includes("clawdbot") || u.includes("moltbot")) score += 4;

  return score;
}

function pickTop(tweets, n = 6) {
  return [...tweets]
    .filter((t) => t?.id && t?.text)
    .sort((a, b) => scoreTweet(b) - scoreTweet(a))
    .slice(0, n);
}

function tweetUrl(t) {
  const u = t.author?.username;
  return u ? `https://x.com/${u}/status/${t.id}` : `https://x.com/i/web/status/${t.id}`;
}

async function downloadToTmp(url) {
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`Failed to download image: ${resp.status}`);
  const buf = Buffer.from(await resp.arrayBuffer());
  const dir = "/tmp/openclaw-xdigest";
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  const file = join(dir, `xdigest-${Date.now()}.jpg`);
  writeFileSync(file, buf);
  return file;
}

async function main() {
  console.log(`Using FB profile: ${PROFILE}`);
  const fb = loadFbTokens();
  console.log(`Loaded FB tokens from: ${TOKENS_FILE}`);
  console.log(`Pages available: ${Object.keys(fb.pages || {}).length}`);
}

main().catch((err) => {
  console.error(err.message || String(err));
  process.exit(1);
});
