#!/usr/bin/env node
/**
 * reply-question.js
 * Finds seeded questions from yesterday and replies to them as the page.
 * 
 * Usage: FB_PROFILE=facebook_fujith node reply-question.js
 */

import { readFileSync, writeFileSync, existsSync } from "fs";
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

// --- API helpers ---
function loadTokens() {
  return JSON.parse(readFileSync(TOKENS_FILE, "utf-8"));
}

function getPageToken(tokens, pageId) {
  return tokens.pages?.[pageId]?.token;
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
  writeFileSync(TRACK_FILE, JSON.stringify(data, null, 2));
}

// --- Reply bank (natural, helpful answers) ---
function getReply(question) {
  const q = question.toLowerCase();

  if (q.includes("khảo sát") || q.includes("miễn phí")) {
    return pickRandom([
      "Dạ có ạ! Bên em khảo sát tại nhà hoàn toàn miễn phí luôn anh/chị ạ. Anh/chị để lại SĐT hoặc inbox em để sắp xếp lịch khảo sát nhé! 🏠",
      "Dạ anh/chị, bên em hỗ trợ khảo sát và tư vấn tại nhà miễn phí ạ. Anh/chị cho em địa chỉ và thời gian thuận tiện, em sẽ cho kỹ thuật qua ngay nhé! 😊",
    ]);
  }
  if (q.includes("bảo hành") || q.includes("bảo trì")) {
    return pickRandom([
      "Dạ anh/chị, bên em bảo hành thang máy lên đến 24 tháng và hỗ trợ bảo trì định kỳ trọn đời ạ! Anh/chị yên tâm sử dụng nhé 💪",
      "Dạ bên em bảo hành chính hãng 24 tháng, bảo trì định kỳ 6 tháng/lần miễn phí trong năm đầu tiên ạ. Anh/chị inbox em tư vấn thêm nhé! 🔧",
    ]);
  }
  if (q.includes("chi phí") || q.includes("giá") || q.includes("bao nhiêu") || q.includes("trả góp")) {
    return pickRandom([
      "Dạ anh/chị, chi phí phụ thuộc vào loại thang và số tầng ạ. Bên em có nhiều phân khúc từ tầm trung đến cao cấp. Anh/chị inbox em để em tư vấn và báo giá cụ thể theo nhu cầu nhé! 💰",
      "Dạ anh/chị, giá thang máy gia đình bên em dao động từ 250-500 triệu tùy loại ạ. Anh/chị inbox em để em tư vấn loại phù hợp nhất với nhà mình nhé! Bên em cũng hỗ trợ trả góp ạ 😊",
    ]);
  }
  if (q.includes("tỉnh") || q.includes("lẻ") || q.includes("ngoài hà nội")) {
    return pickRandom([
      "Dạ anh/chị, bên em lắp đặt thang máy trên toàn quốc luôn ạ! Dù ở tỉnh nào thì bên em cũng có đội ngũ kỹ thuật hỗ trợ tận nơi nhé 🗺️",
      "Dạ có ạ! Bên em triển khai công trình khắp cả nước từ Hà Nội, Hải Phòng đến TP.HCM luôn ạ. Anh/chị cho em biết khu vực để em tư vấn cụ thể hơn nhé! 😊",
    ]);
  }
  if (q.includes("4 tầng") || q.includes("3 tầng") || q.includes("5 tầng") || q.includes("bao nhiêu tầng")) {
    return pickRandom([
      "Dạ anh/chị, nhà 4 tầng lắp thang máy rất phù hợp ạ! Bên em có loại thang thủy lực và kéo cáp đều được. Anh/chị inbox em để em tư vấn loại nào tiết kiệm diện tích nhất cho nhà mình nhé! 🏠",
      "Dạ nhà 4 tầng là lý tưởng để lắp thang máy ạ! Bên em sẽ khảo sát và tư vấn loại phù hợp với kết cấu nhà mình. Anh/chị để lại SĐT em liên hệ tư vấn miễn phí nhé! 😊",
    ]);
  }
  if (q.includes("êm") || q.includes("ồn") || q.includes("yên tĩnh") || q.includes("trẻ nhỏ")) {
    return pickRandom([
      "Dạ anh/chị yên tâm, thang máy bên em chạy rất êm ạ! Độ ồn dưới 45dB, không ảnh hưởng đến giấc ngủ của bé. Anh/chị qua showroom bên em trải nghiệm thực tế nhé! 🤫",
      "Dạ thang máy bên em sử dụng động cơ nhập khẩu, chạy cực kỳ êm ái và an toàn cho cả người già lẫn trẻ nhỏ ạ. Anh/chị inbox em để安排tham quan showroom nhé! 😊",
    ]);
  }
  if (q.includes("thời gian") || q.includes("lâu") || q.includes("mất bao")) {
    return pickRandom([
      "Dạ anh/chị, thời gian lắp đặt thang máy gia đình thường từ 5-7 ngày làm việc ạ. Bên em sẽ khảo sát, thiết kế và thi công trọn gói luôn nhé! ⏰",
      "Dạ trung bình từ 5-7 ngày thi công ạ, tùy vào điều kiện mặt bằng. Anh/chị inbox em để em lên lịch khảo sát và tư vấn cụ thể hơn nhé! 📅",
    ]);
  }
  if (q.includes("giếng trời") || q.includes("diện tích nhỏ") || q.includes("hẹp")) {
    return pickRandom([
      "Dạ anh/chị, bên em có loại thang máy không cần hố pit, chỉ cần 1m2 là lắp được ạ! Giếng trời nhỏ vẫn ok nhé. Anh/chị cho em kích thước cụ thể để em tư vấn loại phù hợp nhất! 📐",
      "Dạ được ạ! Bên em có thang máy mini chỉ cần diện tích 850x850mm là lắp được. Giếng trời nhỏ vẫn phù hợp anh/chị nhé! Inbox em tư vấn thêm ạ 😊",
    ]);
  }
  if (q.includes("cabin") || q.includes("mẫu") || q.includes("thiết kế")) {
    return pickRandom([
      "Dạ anh/chị, bên em có nhiều mẫu cabin từ inox, kính đến gỗ sang trọng ạ! Anh/chị inbox em để em gửi catalogue mẫu cho mình tham khảo nhé! 🎨",
      "Dạ bên em có hơn 20 mẫu cabin từ hiện đại đến cổ điển ạ. Anh/chị qua showroom bên em xem trực tiếp hoặc inbox em gửi hình ảnh catalogue nhé! ✨",
    ]);
  }
  if (q.includes("an toàn") || q.includes("người già")) {
    return pickRandom([
      "Dạ anh/chị, thang máy bên em đạt tiêu chuẩn an toàn châu Âu, có cảm biến cửa, nút bấm khẩn cấp và hệ thống cứu hộ tự động khi mất điện ạ. Rất an toàn cho người già và trẻ nhỏ! 👵👶",
      "Dạ anh/chị yên tâm, thang máy bên em có đầy đủ tính năng an toàn: chống kẹt cửa, chuông báo động, cứu hộ tự động khi mất điện. Đặc biệt phù hợp cho gia đình có người lớn tuổi ạ! 💪",
    ]);
  }
  if (q.includes("xây dựng") || q.includes("nên lắp lúc nào")) {
    return pickRandom([
      "Dạ anh/chị, thời điểm lý tưởng nhất là khi đang xây dựng phần thô ạ! Bên em sẽ tư vấn vị trí và kích thước hố thang ngay từ đầu để tối ưu không gian. Anh/chị inbox em để em hỗ trợ nhé! 🏗️",
      "Dạ anh/chị, nên lắp khi đang xây dựng để dễ dàng bố trí hố thang và đường điện ạ. Nhưng nếu nhà đã xây xong thì bên em vẫn có giải pháp retrofit phù hợp nhé! Inbox em tư vấn ạ 😊",
    ]);
  }
  if (q.includes("tiết kiệm điện") || q.includes("điện")) {
    return pickRandom([
      "Dạ anh/chị, thang máy bên em sử dụng động cơ tiết kiệm điện, chỉ tốn khoảng 50-80k/tháng tiền điện ạ! Tủ lạnh còn tốn hơn 😄 Anh/chị inbox em tư vấn thêm nhé!",
      "Dạ thang máy gia đình bên em chỉ tốn khoảng 50-80k tiền điện/tháng ạ, rất tiết kiệm! Bên em sử dụng công nghệ biến tần tiên tiến nhất. Anh/chị yên tâm nhé! ⚡",
    ]);
  }
  if (q.includes("hưng yên") || q.includes("nam định") || q.includes("thái bình") || q.includes("hải dương")) {
    return pickRandom([
      "Dạ anh/chị, bên em đang triển khai nhiều công trình ở khu vực này ạ! Anh/chị cho em địa chỉ cụ thể để em安排khảo sát miễn phí nhé! 📍",
      "Dạ có ạ! Bên em lắp đặt rất nhiều công trình ở khu vực này rồi. Anh/chị inbox em để em tư vấn và khảo sát tại nhà miễn phí nhé! 😊",
    ]);
  }

  // Default reply
  return pickRandom([
    "Dạ anh/chị, cảm ơn anh/chị đã quan tâm ạ! Anh/chị inbox em hoặc gọi hotline 0989397282 để được tư vấn miễn phí và chi tiết hơn nhé! 😊",
    "Dạ anh/chị, em cảm ơn câu hỏi ạ! Anh/chị để lại SĐT hoặc inbox em, em tư vấn cụ thể theo nhu cầu của nhà mình nhé! 📞",
    "Dạ anh/chị, bên em hỗ trợ tư vấn miễn phí ạ! Anh/chị inbox em hoặc gọi 0989397282 - 0924286386 để được hỗ trợ nhanh nhất nhé! 🏗️",
  ]);
}

function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

// --- Main ---
async function main() {
  const tokens = loadTokens();
  const tracked = loadTracked();

  // Find all seeded questions that haven't been replied to
  const toReply = Object.entries(tracked).filter(
    ([_, v]) => v.commentId && !v.replied && !v.skipped
  );

  if (!toReply.length) {
    console.log("No pending questions to reply to.");
    return;
  }

  // Get page ID from the first entry's key (format: pageId_postId)
  const PAGE_ID = toReply[0][0].split("_")[0];
  const pageToken = getPageToken(tokens, PAGE_ID);
  if (!pageToken) {
    console.error(`No page token for ${PAGE_ID}`);
    process.exit(1);
  }

  for (const [postId, entry] of toReply) {
    const reply = getReply(entry.question);
    console.log(`Post: ${postId}`);
    console.log(`Question: ${entry.question}`);
    console.log(`Reply: ${reply}`);

    const result = await apiPost(`${entry.commentId}/comments`, pageToken, { message: reply });

    if (result.id) {
      tracked[postId].replied = true;
      tracked[postId].replyId = result.id;
      tracked[postId].replyDate = new Date().toISOString();
      saveTracked(tracked);
      console.log(`✅ Replied! Comment ID: ${result.id}`);
    } else {
      console.error("❌ Failed to reply:", JSON.stringify(result));
    }
  }

  console.log("Done.");
}

main().catch(console.error);
