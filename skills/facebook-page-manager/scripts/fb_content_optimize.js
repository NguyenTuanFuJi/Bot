#!/usr/bin/env node
/**
 * Facebook Content Optimizer (rule-based, lightweight)
 * - Build SEO-friendly Facebook caption from structured input
 * - Generate hashtags
 * - Run quality score gate
 *
 * Usage:
 *   node fb_content_optimize.js --input payload.json
 */

import { readFileSync } from "fs";

function parseArgs() {
  const args = process.argv.slice(2);
  const out = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--input") out.input = args[++i];
  }
  return out;
}

function clean(s = "") {
  return String(s).trim();
}

function uniq(arr) {
  return [...new Set(arr.filter(Boolean))];
}

function buildCaption(p) {
  const goal = clean(p.goal || "engagement");
  const keywordMain = clean(p.keyword_main || "");
  const keywordSubs = uniq((p.keyword_subs || []).map(clean));
  const hook = clean(p.hook || (keywordMain ? `${keywordMain}: Giải pháp thực tế cho bạn` : "Giải pháp thực tế cho bạn"));
  const pain = clean(p.pain || "Bạn đang gặp khó khi chọn hướng làm phù hợp?");
  const bullets = uniq((p.solutions || []).map(clean)).slice(0, 5);
  const proof = clean(p.proof || "Đã áp dụng thực tế và cho kết quả tích cực.");
  const cta = clean(p.cta || "Nhắn tin để nhận tư vấn chi tiết.");

  const body = [];
  body.push(hook);
  body.push("");
  body.push(pain);
  body.push("");

  if (bullets.length) {
    body.push("Giải pháp gợi ý:");
    for (const b of bullets) body.push(`- ${b}`);
    body.push("");
  }

  body.push(`Kết quả/ghi nhận: ${proof}`);
  body.push("");

  if (keywordSubs.length) {
    body.push(`Từ khóa liên quan: ${keywordSubs.slice(0, 5).join(", ")}`);
    body.push("");
  }

  body.push(`👉 ${cta}`);

  const tags = uniq([
    p.hashtag_brand,
    keywordMain && keywordMain.replace(/\s+/g, ""),
    ...keywordSubs.slice(0, 3).map((k) => k.replace(/\s+/g, "")),
  ])
    .filter(Boolean)
    .slice(0, 5)
    .map((x) => (x.startsWith("#") ? x : `#${x}`));

  return {
    goal,
    caption: body.join("\n"),
    hashtags: tags,
  };
}

function scoreContent(captionObj, payload) {
  let score = 100;
  const issues = [];
  const c = captionObj.caption;

  if (!payload.keyword_main || !c.toLowerCase().includes(String(payload.keyword_main).toLowerCase())) {
    score -= 20;
    issues.push("Thiếu từ khóa chính trong caption");
  }

  const lines = c.split("\n");
  if ((lines[0] || "").length < 15) {
    score -= 10;
    issues.push("Hook quá ngắn");
  }

  if (!String(payload.cta || "").trim()) {
    score -= 20;
    issues.push("Thiếu CTA rõ ràng");
  }

  const hashtagCount = captionObj.hashtags.length;
  if (hashtagCount < 2 || hashtagCount > 6) {
    score -= 10;
    issues.push("Hashtag chưa tối ưu (nên 2-6)");
  }

  if (c.length < 180) {
    score -= 10;
    issues.push("Nội dung quá ngắn, thiếu thông tin");
  }

  if (c.length > 2200) {
    score -= 10;
    issues.push("Nội dung quá dài, dễ giảm đọc hết");
  }

  return { score: Math.max(0, score), issues };
}

function main() {
  const args = parseArgs();
  if (!args.input) {
    console.error("Usage: node fb_content_optimize.js --input payload.json");
    process.exit(1);
  }

  const payload = JSON.parse(readFileSync(args.input, "utf-8"));
  const built = buildCaption(payload);
  const qa = scoreContent(built, payload);

  const out = {
    ok_to_post: qa.score >= 75,
    score: qa.score,
    issues: qa.issues,
    goal: built.goal,
    caption: `${built.caption}\n\n${built.hashtags.join(" ")}`,
    hashtags: built.hashtags,
  };

  console.log(JSON.stringify(out, null, 2));
}

main();
