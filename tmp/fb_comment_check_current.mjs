import { readFileSync, writeFileSync, existsSync } from "fs";
import { join } from "path";

const workspace = "/home/tuan/.openclaw/workspace";
const skillDir = join(workspace, "skills/facebook-page-manager");
const credentialsRoot = join(skillDir, "credentials");
const profile = process.env.FB_PROFILE || "facebook_fujith";
const envFile = join(credentialsRoot, profile, ".env");
const tokensFile = join(credentialsRoot, profile, "tokens.json");
const wpEnvFile = join(workspace, "skills/wordpress-cli-app-password/.env");

const statePath = join(workspace, "state/fujith_comment_check_state.json");
const latestReportPath = join(workspace, "logs/comment_shift_report_latest.json");
const reportPath = join(workspace, "logs/comment_check_20260808_120000.json");

function loadEnv(file) {
  if (!existsSync(file)) return {};
  const out = {};
  for (const line of readFileSync(file, "utf-8").split(/\r?\n/)) {
    if (!line || line.trim().startsWith("#")) continue;
    const idx = line.indexOf("=");
    if (idx === -1) continue;
    const key = line.slice(0, idx).trim();
    let value = line.slice(idx + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    out[key] = value;
  }
  return out;
}

const env = loadEnv(envFile);
const wpEnv = loadEnv(wpEnvFile);
const GRAPH_API_VERSION = env.GRAPH_API_VERSION || "v21.0";
const tokens = JSON.parse(readFileSync(tokensFile, "utf-8"));
const pageId = "695286863979169";
const pageToken = tokens.pages?.[pageId]?.token;
const userToken = tokens.user_token;
const pageOwnerNames = new Set(["Thang Máy FUJI TH", "Thang Máy Gia Đình FUJI TH", "FUJI TH"]);

const prevState = existsSync(statePath) ? JSON.parse(readFileSync(statePath, "utf-8")) : null;
const seenCommentIds = new Set(prevState?.facebook?.seen_comment_ids || []);
const seenPostIds = new Set(prevState?.facebook?.posts_checked || []);

async function apiGet(endpoint, token, params = {}) {
  const url = new URL(`https://graph.facebook.com/${GRAPH_API_VERSION}/${endpoint}`);
  url.searchParams.set("access_token", token);
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
  const resp = await fetch(url);
  const data = await resp.json();
  if (!resp.ok) throw new Error(`FB API ${resp.status}: ${JSON.stringify(data)}`);
  return data;
}

async function apiPost(endpoint, token, body = {}) {
  const url = new URL(`https://graph.facebook.com/${GRAPH_API_VERSION}/${endpoint}`);
  url.searchParams.set("access_token", token);
  const formData = new URLSearchParams();
  for (const [k, v] of Object.entries(body)) formData.set(k, v);
  const resp = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData,
  });
  const data = await resp.json();
  if (!resp.ok) throw new Error(`FB API ${resp.status}: ${JSON.stringify(data)}`);
  return data;
}

function classifyComment(message, authorName) {
  if (authorName && pageOwnerNames.has(authorName)) return "self";
  const text = (message || "").trim();
  if (!text) return "empty";
  const lower = text.toLowerCase();
  if (/https?:\/\/|zalo\.me/.test(lower)) return "spam";
  if (/inbox\b|ib\b|nhắn tin|liên hệ|lh\b|gọi/.test(lower)) return "xin tư vấn";
  if (/giá|bao nhiêu|báo giá|quote|chi phí|tổng tiền/.test(lower)) return "hỏi giá";
  if (/bảo trì|bảo dưỡng|lỗi|sửa|sự cố|rung|ồn|kẹt|cứu hộ|bảo hành|kỹ thuật|điện/.test(lower)) return "hỏi kỹ thuật";
  if (/tư vấn|phù hợp|nhà phố|biệt thự|kích thước|hố thang|mẫu|so sánh|nên chọn|thang máy/.test(lower)) return "xin tư vấn";
  return "xin tư vấn";
}

function buildReply(message) {
  const lower = (message || "").toLowerCase();
  if (/giá|bao nhiêu|báo giá|quote|chi phí/.test(lower)) {
    return "Dạ FUJI TH cảm ơn anh/chị đã quan tâm. Để báo giá chính xác theo nhà mình, anh/chị để lại số điện thoại hoặc inbox kèm số tầng và diện tích hố thang, em gửi phương án và chi phí ngay ạ.";
  }
  if (/bảo trì|bảo dưỡng|lỗi|sửa|sự cố|rung|ồn|kẹt|cứu hộ|bảo hành|kỹ thuật|điện/.test(lower)) {
    return "Dạ em đã ghi nhận yêu cầu hỗ trợ kỹ thuật. Anh/chị để lại số điện thoại và mô tả tình trạng cụ thể, em sẽ liên hệ trong thời gian sớm nhất để xử lý ạ.";
  }
  return "Dạ FUJI TH đã ghi nhận phản hồi của anh/chị. Anh/chị để lại số điện thoại hoặc inbox trực tiếp để em hỗ trợ nhanh hơn ạ.";
}

const posts = await apiGet(`${pageId}/posts`, pageToken, {
  fields: "id,message,created_time,permalink_url,comments.summary(true)",
  limit: "20",
});

const handled = [];
let postsScanned = 0;

for (const post of posts.data || []) {
  postsScanned++;
  const commentCount = post.comments?.summary?.total_count || 0;
  if (!commentCount) continue;
  const comments = await apiGet(`${post.id}/comments`, userToken, {
    fields: "id,message,from,created_time,like_count,is_hidden",
    limit: "25",
  });
  const permalink = post.permalink_url || `https://www.facebook.com/${post.id.replace("_", "/posts/")}`;
  for (const comment of comments.data || []) {
    if (seenCommentIds.has(comment.id)) continue;
    const authorName = comment.from?.name || null;
    const classification = classifyComment(comment.message, authorName);
    if (classification === "self" || classification === "empty") {
      seenCommentIds.add(comment.id);
      continue;
    }
    const action = classification === "spam" ? "skipped" : "replied";
    let replyId = null;
    let replyExcerpt = null;
    if (action === "replied") {
      const message = buildReply(comment.message);
      const res = await apiPost(`${comment.id}/comments`, userToken, { message });
      replyId = res.id || null;
      replyExcerpt = message;
    }
    handled.push({
      channel: "facebook",
      post_id: post.id,
      post_url: permalink,
      comment_id: comment.id,
      author_name: authorName,
      message: comment.message || "",
      created_at: comment.created_time,
      classification,
      action,
      reply_id: replyId,
      reply_excerpt: replyExcerpt,
    });
    seenCommentIds.add(comment.id);
  }
}

let websiteEndpoint = null;
let websiteNewCount = 0;
let websiteItems = [];
try {
  const base = (wpEnv.WP_BASE_URL || "").replace(/\/$/, "");
  const user = wpEnv.WP_USER;
  const pass = wpEnv.WP_APP_PASSWORD;
  if (base && user && pass) {
    websiteEndpoint = `${base}/?rest_route=/wp/v2/comments&per_page=20&orderby=date_gmt&order=desc&_fields=id,post,author_name,status,date_gmt,link,content`;
    const auth = Buffer.from(`${user}:${pass}`).toString("base64");
    const resp = await fetch(websiteEndpoint, { headers: { Authorization: `Basic ${auth}` } });
    if (resp.ok) {
      const data = await resp.json();
      if (Array.isArray(data)) {
        websiteNewCount = data.length;
        websiteItems = data.map((c) => ({
          channel: "website",
          comment_id: c.id,
          post_id: c.post,
          author_name: c.author_name || null,
          status: c.status,
          created_at: c.date_gmt,
          link: c.link,
          message: (c.content?.rendered || "").replace(/<[^>]+>/g, "").trim(),
        }));
      }
    }
  }
} catch (e) {
  websiteNewCount = -1;
}

const postsChecked = Array.from(new Set([...seenPostIds, ...((posts.data || []).map((p) => p.id))])).slice(0, 50);
const report = {
  checked_at: new Date().toISOString(),
  processed: handled.length,
  total_new: handled.length,
  items: handled,
  channels: {
    facebook: {
      page_id: pageId,
      posts_scanned: postsScanned,
      new_comments: handled.length,
    },
    website: {
      endpoint: websiteEndpoint,
      new_comments: websiteNewCount,
      items: websiteItems,
    },
  },
  note: handled.length
    ? `Đã xử lý ${handled.length} bình luận Facebook mới; website ${websiteNewCount === 0 ? "không có bình luận mới" : websiteNewCount === -1 ? "không kiểm tra được" : `có ${websiteNewCount} bình luận`}.`
    : `Không có bình luận Facebook mới; website ${websiteNewCount === 0 ? "không có bình luận mới" : websiteNewCount === -1 ? "không kiểm tra được" : `có ${websiteNewCount} bình luận`}.`,
};

writeFileSync(reportPath, JSON.stringify(report, null, 2));
writeFileSync(latestReportPath, JSON.stringify(report, null, 2));

const state = {
  last_checked_at: report.checked_at,
  facebook: {
    page_id: pageId,
    posts_checked: postsChecked,
    seen_comment_ids: Array.from(seenCommentIds).slice(-200),
  },
  website: {
    base_url: wpEnv.WP_BASE_URL || null,
    comments_found: websiteNewCount,
    rest_route: websiteEndpoint,
    seen_comment_ids: prevState?.website?.seen_comment_ids || [],
  },
  summary: {
    new_comments: handled.length,
    handled: handled.filter((i) => i.action === "replied").length,
  },
};
writeFileSync(statePath, JSON.stringify(state, null, 2));

console.log(JSON.stringify(report, null, 2));
