#!/usr/bin/env node
/**
 * browse.js — فتح رابط في متصفح Chromium حقيقي واستخراج محتواه
 *
 * يشغّل relay.js تلقائياً إن لم يكن يعمل، ثم يفتح الصفحة في Chromium
 * ويطبع نصها ويحفظ لقطة شاشة.
 *
 * أمثلة:
 *   node browse.js https://example.com
 *   node browse.js https://example.com --shot out.png --limit 4000
 *   node browse.js https://example.com --wait "table.prices" --json
 *
 * الخيارات:
 *   --shot <path>     مسار لقطة الشاشة (افتراضي: .cache/last-shot.png)
 *   --full            لقطة للصفحة كاملة لا للجزء الظاهر فقط
 *   --wait <selector> انتظار ظهور عنصر قبل القراءة
 *   --timeout <ms>    مهلة التحميل (افتراضي 60000)
 *   --limit <n>       حد أحرف النص المطبوع (افتراضي 4000، 0 = بلا حد)
 *   --json            إخراج JSON بدل نص مقروء
 *   --no-shot         تعطيل لقطة الشاشة
 *   --port <n>        منفذ الوسيط (افتراضي 8899)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const net = require('net');
const http = require('http');
const { spawn, execSync } = require('child_process');

const CACHE_DIR = path.join(__dirname, '.cache');
const RELAY_SCRIPT = path.join(__dirname, 'relay.js');

/* ------------------------------------------------------------------ *
 * معالجة الوسائط
 * ------------------------------------------------------------------ */

function parseArgs(argv) {
  const opts = {
    url: null,
    shot: path.join(CACHE_DIR, 'last-shot.png'),
    full: false,
    wait: null,
    timeout: 60_000,
    limit: 4000,
    json: false,
    noShot: false,
    port: Number(process.env.RELAY_PORT || 8899),
  };

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    switch (arg) {
      case '--shot': opts.shot = argv[++i]; break;
      case '--full': opts.full = true; break;
      case '--wait': opts.wait = argv[++i]; break;
      case '--timeout': opts.timeout = Number(argv[++i]); break;
      case '--limit': opts.limit = Number(argv[++i]); break;
      case '--json': opts.json = true; break;
      case '--no-shot': opts.noShot = true; break;
      case '--port': opts.port = Number(argv[++i]); break;
      default:
        if (arg.startsWith('--')) throw new Error(`unknown option: ${arg}`);
        if (!opts.url) opts.url = arg;
    }
  }

  if (!opts.url) throw new Error('missing URL — usage: node browse.js <url> [options]');
  if (!/^https?:\/\//i.test(opts.url)) opts.url = `https://${opts.url}`;
  return opts;
}

/* ------------------------------------------------------------------ *
 * تحديد مكان playwright
 * ------------------------------------------------------------------ */

function loadPlaywright() {
  const candidates = [];
  try {
    candidates.push(execSync('npm root -g', { encoding: 'utf8' }).trim());
  } catch { /* npm غير متاح */ }
  candidates.push('/opt/node22/lib/node_modules', '/usr/lib/node_modules');

  try {
    return require('playwright');
  } catch { /* غير مثبت محلياً */ }

  for (const root of candidates) {
    if (!root) continue;
    try {
      return require(path.join(root, 'playwright'));
    } catch { /* التالي */ }
  }

  throw new Error(
    'playwright not found — install it globally with: npm install -g playwright\n' +
    '(Chromium نفسه مثبت مسبقاً في PLAYWRIGHT_BROWSERS_PATH)'
  );
}

/* ------------------------------------------------------------------ *
 * إدارة الوسيط
 * ------------------------------------------------------------------ */

function portInUse(port) {
  return new Promise((resolve) => {
    const sock = net.connect(port, '127.0.0.1');
    sock.once('connect', () => { sock.destroy(); resolve(true); });
    sock.once('error', () => resolve(false));
    sock.setTimeout(1500, () => { sock.destroy(); resolve(false); });
  });
}

function relayHealthy(port) {
  return new Promise((resolve) => {
    const req = http.get(`http://127.0.0.1:${port}/__relay/health`, (res) => {
      res.resume();
      resolve(res.statusCode === 200);
    });
    req.on('error', () => resolve(false));
    req.setTimeout(2000, () => { req.destroy(); resolve(false); });
  });
}

async function ensureRelay(port) {
  if (await relayHealthy(port)) return null;

  if (await portInUse(port)) {
    throw new Error(`port ${port} is busy but does not answer as relay — use --port to pick another`);
  }

  fs.mkdirSync(CACHE_DIR, { recursive: true });
  const logFile = fs.openSync(path.join(CACHE_DIR, 'relay.log'), 'a');
  const child = spawn(process.execPath, [RELAY_SCRIPT, '--port', String(port)], {
    detached: true,
    stdio: ['ignore', logFile, logFile],
  });
  child.unref();

  for (let attempt = 0; attempt < 40; attempt++) {
    await new Promise((r) => setTimeout(r, 250));
    if (await relayHealthy(port)) return child.pid;
  }

  throw new Error(`relay failed to start on port ${port} — see ${path.join(CACHE_DIR, 'relay.log')}`);
}

/* ------------------------------------------------------------------ *
 * التنفيذ
 * ------------------------------------------------------------------ */

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  const { chromium } = loadPlaywright();

  const startedPid = await ensureRelay(opts.port);
  const entry = `http://127.0.0.1:${opts.port}/fetch?u=${encodeURIComponent(opts.url)}`;

  // بلا بروكسي: كل الحركة تذهب إلى 127.0.0.1 والوسيط يتكفّل بالخارج
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    locale: 'ar-SA',
  });
  const page = await context.newPage();

  const result = { url: opts.url, relayStarted: Boolean(startedPid) };

  try {
    const response = await page.goto(entry, { waitUntil: 'domcontentloaded', timeout: opts.timeout });
    result.status = response ? response.status() : null;

    if (opts.wait) {
      await page.waitForSelector(opts.wait, { timeout: opts.timeout });
    }

    result.title = await page.title();
    const text = await page.locator('body').innerText();
    result.text = text.replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();

    if (!opts.noShot) {
      fs.mkdirSync(path.dirname(path.resolve(opts.shot)), { recursive: true });
      await page.screenshot({ path: opts.shot, fullPage: opts.full });
      result.screenshot = path.resolve(opts.shot);
    }
  } finally {
    await browser.close();
  }

  if (opts.json) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  console.log(`URL:     ${result.url}`);
  console.log(`STATUS:  ${result.status}`);
  console.log(`TITLE:   ${result.title}`);
  if (result.screenshot) console.log(`SHOT:    ${result.screenshot}`);
  console.log('--- TEXT ---');
  const body = opts.limit > 0 ? result.text.slice(0, opts.limit) : result.text;
  console.log(body);
  if (opts.limit > 0 && result.text.length > opts.limit) {
    console.log(`\n… (${result.text.length - opts.limit} حرفاً إضافياً — استخدم --limit 0 لعرض الكل)`);
  }
}

main().catch((err) => {
  console.error(`browse: ${err.message}`);
  process.exit(1);
});
