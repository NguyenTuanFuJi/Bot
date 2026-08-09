#!/usr/bin/env node
/**
 * seed-question.js
 * Checks recent posts (~15 min old) and adds a customer-perspective question comment
 * if the page hasn't commented yet.
 * 
 * Usage: FB_PROFILE=facebook_fujith node seed-question.js --page PAGE_ID
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";
import { config } from "dotenv";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = join(__dirname, "..");
const CREDENTIALS_ROOT = join(SKILL_DIR, "credentials");
const PROFILE = process.env.FB_PROFILE || "facebook_fujith";
const ENV_FILE = process.env.FB_ENV_FILE || join(CREDENTIALS_ROOT, PROFILE, ".env");
const TOKENS_FILE = process.env.FB_TOKENS_FILE || join(CREDENTIALS_ROOT, PROFILE, "tokens.json");
const TRACK_FILE = join(SKILL_DIR, "data", "seeded-questions.json");

config({ path: ENV_FILE });

const GRAPH_API_VERSION = "v21.0";
const GRAPH_API_BASE = `https://graph.facebook.com/${GRAPH_API_VERSION}`;
const PAGE_ID = process.argv.includes("--page") 
  ? process.argv[process.argv.indexOf("--page") + 1] 
  : null;

if (!PAGE_ID) {
  console.error("Usage: node seed-question.js --page PAGE_ID");
  process.exit(1);
}

// --- API helpers ---
function loadTokens() {
  return JSON.parse(readFileSync(TOKENS_FILE, "utf-8"));
}

function getPageToken(tokens) {
  return tokens.pages?.[PAGE_ID]?.token;
}

async function apiGet(endpoint, token, params = {}) {
  const url = new URL(`${GRAPH_API_BASE}/${endpoint}`);
  url.searchParams.set("access_token", token);
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
  const resp = await fetch(url);
  return resp.json();
}

async function apiPost(endpoint, token, body = {}) {
  const url = new URL(`${GRAPH_API_BASE}/${endpoint}`);
  url.searchParams.set("access_token", token);
  const formData = new URLSearchParams();
  for (const [k, v] of Object.entries(body)) formData.set(k, v);
  const resp = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData,
  });
  return resp.json();
}

// --- Tracking ---
function loadTracked() {
  if (!existsSync(TRACK_FILE)) return {};
  return JSON.parse(readFileSync(TRACK_FILE, "utf-8"));
}

function saveTracked(data) {
  const dir = dirname(TRACK_FILE);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(TRACK_FILE, JSON.stringify(data, null, 2));
}

// --- Question bank (varied, natural customer questions) ---
const QUESTION_TEMPLATES = [
  "Cho em hỏi bên mình có nhận lắp ở {area} không ạ?",
  "Bên mình bảo hành thang máy bao lâu vậy ạ?",
  "Nhà em 4 tầng thì lắp loại nào phù hợp ạ?",
  "Chi phí lắp thang máy gia đình tầm bao nhiêu vậy ạ?",
  "Bên mình có khảo sát tại nhà miễn phí không ạ?",
  "Thang máy này chạy êm không ạ? Nhà em có trẻ nhỏ nên muốn yên tĩnh.",
  "Thời gian lắp đặt thang máy mất bao lâu vậy ạ?",
  "Bên mình có hỗ trợ trả góp không ạ?",
  "Nhà em đang xây dựng, nên lắp thang máy lúc nào là hợp lý nhất ạ?",
  "Thang máy gia đình bên mình có tiết kiệm điện không ạ?",
  "Cho em hỏi bên mình có mẫu cabin nào đẹp không ạ?",
  "Nhà em có giếng trời nhỏ thì lắp được không ạ?",
  "Bên mình có hỗ trợ bảo trì định kỳ không ạ?",
  "Em ở tỉnh lẻ thì bên mình có lắp không ạ?",
  "Thang máy bên mình có an toàn cho người già không ạ?",
];

const AREAS = [
  "Hà Nội", "Hải Phòng", "Nam Định", "Thái Bình", "Hưng Yên",
  "Bắc Ninh", "Hải Dương", "Thanh Hóa", "Nghệ An", "Quảng Ninh",
];

function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function generateQuestion() {
  let q = pickRandom(QUESTION_TEMPLATES);
  if (q.includes("{area}")) {
    q = q.replace("{area}", pickRandom(AREAS));
  }
  return q;
}

// --- Main ---
async function main() {
  const tokens = loadTokens();
  const pageToken = getPageToken(tokens);
  if (!pageToken) {
    console.error(`No page token for ${PAGE_ID}`);
    process.exit(1);
  }

  // Get all recent posts (last 50)
  const posts = await apiGet(`${PAGE_ID}/posts`, pageToken, {
    fields: "id,message,created_time,comments.summary(true)",
    limit: "50",
  });

  if (!posts.data?.length) {
    console.log("No posts found");
    return;
  }

  const tracked = loadTracked();
  const now = Date.now();
  const ONE_DAY = 24 * 60 * 60 * 1000;
  let seededCount = 0;

  for (const post of posts.data) {
    const postId = post.id;
    const createdTime = new Date(post.created_time).getTime();
    const age = now - createdTime;

    // Skip posts older than 30 days
    if (age > 30 * ONE_DAY) continue;

    // Skip if already seeded or skipped
    if (tracked[postId]) continue;

    // Skip if post already has comments (organic engagement exists)
    const commentCount = post.comments?.summary?.total_count || 0;
    if (commentCount > 0) {
      tracked[postId] = { skipped: true, reason: "has_comments", date: new Date().toISOString() };
      saveTracked(tracked);
      continue;
    }

    // Generate and post question with @all tag
    const question = generateQuestion();
    const questionWithTag = question + " @all";
    console.log(`Post: ${postId}`);
    console.log(`Question: ${questionWithTag}`);

    const result = await apiPost(`${postId}/comments`, pageToken, { message: questionWithTag });

    if (result.id) {
      tracked[postId] = {
        commentId: result.id,
        question: questionWithTag,
        date: new Date().toISOString(),
        replied: false,
      };
      saveTracked(tracked);
      seededCount++;
      console.log(`✅ Seeded! Comment ID: ${result.id}`);

      // Only seed 1 post per run to space out naturally
      if (seededCount >= 1) break;
    } else {
      console.error("❌ Failed to post comment:", JSON.stringify(result));
    }
  }

  console.log(`Done. Seeded ${seededCount} post(s).`);
}

main().catch(console.error);
