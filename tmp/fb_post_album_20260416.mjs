import { readFileSync } from 'fs';
import { basename } from 'path';

const pageId = '695286863979169';
const tokenFile = '/home/tuan/.openclaw/workspace/skills/facebook-page-manager/credentials/facebook_fujith/tokens.json';
const captionFile = '/home/tuan/.openclaw/workspace/tmp/fb_20260416_checklist_caption.txt';
const photos = [
  '/home/tuan/.openclaw/workspace/tmp/fb_20260416_checklist_images/1.jpg',
  '/home/tuan/.openclaw/workspace/tmp/fb_20260416_checklist_images/2.jpg',
  '/home/tuan/.openclaw/workspace/tmp/fb_20260416_checklist_images/3.jpg',
  '/home/tuan/.openclaw/workspace/tmp/fb_20260416_checklist_images/4.jpg',
];
const api = 'https://graph.facebook.com/v21.0';

const tokens = JSON.parse(readFileSync(tokenFile, 'utf8'));
const token = tokens.pages?.[pageId]?.token;
if (!token) throw new Error('Missing page token');
const message = readFileSync(captionFile, 'utf8');

async function uploadPhoto(path) {
  const form = new FormData();
  form.set('published', 'false');
  form.set('source', new Blob([readFileSync(path)]), basename(path));
  const resp = await fetch(`${api}/${pageId}/photos?access_token=${encodeURIComponent(token)}`, {
    method: 'POST',
    body: form,
  });
  const data = await resp.json();
  if (!resp.ok || !data.id) {
    throw new Error(`Upload failed for ${path}: ${JSON.stringify(data)}`);
  }
  return data.id;
}

const photoIds = [];
for (const p of photos) {
  const id = await uploadPhoto(p);
  photoIds.push(id);
  console.log(`UPLOADED ${p} => ${id}`);
}

const body = new URLSearchParams();
body.set('message', message);
for (const [i, id] of photoIds.entries()) {
  body.set(`attached_media[${i}]`, JSON.stringify({ media_fbid: id }));
}

const postResp = await fetch(`${api}/${pageId}/feed?access_token=${encodeURIComponent(token)}`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body,
});
const postData = await postResp.json();
if (!postResp.ok || !postData.id) {
  throw new Error(`Create post failed: ${JSON.stringify(postData)}`);
}
console.log(`POST_ID ${postData.id}`);

const permalinkResp = await fetch(`${api}/${postData.id}?fields=permalink_url&access_token=${encodeURIComponent(token)}`);
const permalinkData = await permalinkResp.json();
if (!permalinkResp.ok) {
  throw new Error(`Permalink lookup failed: ${JSON.stringify(permalinkData)}`);
}
console.log(`POST_URL ${permalinkData.permalink_url || ''}`);
