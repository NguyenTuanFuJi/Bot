#!/usr/bin/env node
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';
import { spawn } from 'node:child_process';

function parseArgs(argv) {
  const out = {
    sourceAuth: process.env.CLIPROXY_CODEX_AUTH || '/home/tuan/.cli-proxy-api/codex-nguyentuanhyxx86@gmail.com-plus.json',
    baseUrl: process.env.CODEX_IMAGEN_BASE_URL || 'https://chatgpt.com/backend-api/codex',
    model: process.env.CODEX_IMAGEN_MODEL || '',
    timeout: process.env.CODEX_IMAGEN_TIMEOUT || '300',
    passthrough: [],
  };

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--source-auth') {
      out.sourceAuth = argv[++i];
    } else if (arg === '--base-url') {
      out.baseUrl = argv[++i];
    } else if (arg === '--model') {
      out.model = argv[++i];
    } else if (arg === '--timeout') {
      out.timeout = argv[++i];
    } else {
      out.passthrough.push(arg);
    }
  }

  return out;
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  const source = path.resolve(opts.sourceAuth);
  const raw = await fs.readFile(source, 'utf8');
  const data = JSON.parse(raw);

  if (!data?.access_token || !data?.account_id) {
    throw new Error('Auth file cliproxyapi thiếu access_token/account_id');
  }

  const mapped = {
    'openai-codex': {
      access: data.access_token,
      refresh: data.refresh_token || '',
      accountId: data.account_id,
      email: data.email || null,
      expires: data.expired || null,
      provider: 'openai-codex',
      type: 'oauth',
    },
  };

  const tempPath = path.join(os.tmpdir(), `codex-imagen-auth-map-${process.pid}-${Date.now()}.json`);
  await fs.writeFile(tempPath, JSON.stringify(mapped), { mode: 0o600 });

  const skillScript = '/home/tuan/.openclaw/workspace/skills/codex-imagen/scripts/codex-imagen.mjs';
  const cmdArgs = [skillScript, '--auth', tempPath, '--base-url', opts.baseUrl, '--timeout', String(opts.timeout)];
  if (opts.model) {
    cmdArgs.push('--model', opts.model);
  }
  cmdArgs.push(...opts.passthrough);

  const child = spawn('node', cmdArgs, { stdio: 'inherit' });

  child.on('close', async (code) => {
    try { await fs.unlink(tempPath); } catch {}
    process.exit(code ?? 1);
  });
}

main().catch((err) => {
  console.error(err?.message || err);
  process.exit(1);
});
