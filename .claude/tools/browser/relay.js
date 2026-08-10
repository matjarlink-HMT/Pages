#!/usr/bin/env node
/**
 * relay.js — جسر جلب محلي للمتصفح
 *
 * بيئة التشغيل السحابية تمنع Chromium من فتح أنفاق HTTPS مباشرة
 * (كل محاولة ترجع ERR_CONNECTION_RESET)، بينما Node يمر عبر بروكسي
 * الوكيل بشكل طبيعي.
 *
 * هذا الملف يشغّل خادماً محلياً يجلب الرابط المطلوب عبر HTTPS ثم
 * يقدّمه للمتصفح على http://127.0.0.1. عند جلب صفحة HTML تُعاد كتابة
 * روابط الموارد (CSS، صور، خطوط) لتمر عبر نفس الخادم، فتظهر الصفحة
 * بتنسيقها الحقيقي لا كنص خام.
 *
 * التشغيل:  node relay.js [--port 8899]
 * الفحص:    curl http://127.0.0.1:8899/__relay/health
 * الجلب:    curl "http://127.0.0.1:8899/fetch?u=https%3A%2F%2Fexample.com"
 */

'use strict';

const http = require('http');
const https = require('https');
const net = require('net');
const tls = require('tls');
const zlib = require('zlib');

const PORT = Number(argValue('--port') || process.env.RELAY_PORT || 8899);
const VERBOSE = process.argv.includes('--verbose');

const USER_AGENT =
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36';

const MAX_BYTES = 40 * 1024 * 1024;
const MAX_REDIRECTS = 5;
const REQUEST_TIMEOUT_MS = 45_000;

function argValue(flag) {
  const i = process.argv.indexOf(flag);
  return i !== -1 ? process.argv[i + 1] : null;
}

function log(...args) {
  if (VERBOSE) console.error('[relay]', ...args);
}

/* ------------------------------------------------------------------ *
 * الاتصال عبر بروكسي الوكيل
 * ------------------------------------------------------------------ */

function upstreamProxy() {
  const raw = process.env.HTTPS_PROXY || process.env.https_proxy;
  if (!raw) return null;
  const u = new URL(raw);
  return { host: u.hostname, port: Number(u.port || 80) };
}

const UPSTREAM = upstreamProxy();

/** يفتح اتصال TLS للمضيف الهدف، عبر بروكسي الوكيل إن وُجد. */
function connectUpstream(host, port, callback) {
  if (!UPSTREAM) {
    const direct = tls.connect({ host, port, servername: host }, () => callback(null, direct));
    direct.once('error', callback);
    return;
  }

  const sock = net.connect(UPSTREAM.port, UPSTREAM.host);
  let settled = false;
  const fail = (err) => {
    if (settled) return;
    settled = true;
    sock.destroy();
    callback(err);
  };

  sock.once('error', fail);
  sock.setTimeout(REQUEST_TIMEOUT_MS, () => fail(new Error('upstream proxy timeout')));
  sock.once('connect', () => {
    sock.write(`CONNECT ${host}:${port} HTTP/1.1\r\nHost: ${host}:${port}\r\n\r\n`);
  });

  // رد CONNECT قد يصل مجزّأً — نجمّعه حتى نهاية الترويسات
  let buffer = Buffer.alloc(0);
  const onData = (chunk) => {
    buffer = Buffer.concat([buffer, chunk]);
    const end = buffer.indexOf('\r\n\r\n');
    if (end === -1) {
      if (buffer.length > 65536) fail(new Error('CONNECT response too large'));
      return;
    }

    sock.removeListener('data', onData);
    sock.setTimeout(0);
    const statusLine = buffer.slice(0, buffer.indexOf('\r\n')).toString();
    if (!/^HTTP\/1\.[01] 200/.test(statusLine)) {
      return fail(new Error(`upstream proxy refused CONNECT: ${statusLine}`));
    }

    const leftover = buffer.slice(end + 4);
    if (leftover.length) sock.unshift(leftover);

    const secure = tls.connect(
      { socket: sock, servername: host, ALPNProtocols: ['http/1.1'] },
      () => {
        if (settled) return;
        settled = true;
        sock.removeListener('error', fail);
        callback(null, secure);
      }
    );
    secure.once('error', fail);
  };

  sock.on('data', onData);
}

class UpstreamAgent extends https.Agent {
  createConnection(options, cb) {
    connectUpstream(options.host, Number(options.port) || 443, cb);
  }
}

const upstreamAgent = new UpstreamAgent({ keepAlive: true, maxSockets: 16 });

/* ------------------------------------------------------------------ *
 * جلب رابط
 * ------------------------------------------------------------------ */

function decompress(buffer, encoding) {
  try {
    if (encoding === 'gzip') return zlib.gunzipSync(buffer);
    if (encoding === 'deflate') return zlib.inflateSync(buffer);
    if (encoding === 'br') return zlib.brotliDecompressSync(buffer);
  } catch (err) {
    log('decompress failed', encoding, err.message);
  }
  return buffer;
}

/** يجلب رابطاً ويتبع التحويلات. يعيد { status, headers, body, url }. */
function fetchUrl(rawUrl, depth = 0) {
  return new Promise((resolve, reject) => {
    let target;
    try {
      target = new URL(rawUrl);
    } catch {
      return reject(new Error(`malformed URL: ${rawUrl}`));
    }

    if (target.protocol !== 'https:' && target.protocol !== 'http:') {
      return reject(new Error(`unsupported protocol: ${target.protocol}`));
    }

    // بروكسي الوكيل لا يقبل إلا أنفاق HTTPS
    target.protocol = 'https:';

    const req = https.request(
      {
        host: target.hostname,
        port: Number(target.port) || 443,
        path: target.pathname + target.search,
        method: 'GET',
        agent: upstreamAgent,
        servername: target.hostname,
        headers: {
          host: target.host,
          'user-agent': USER_AGENT,
          accept: '*/*',
          'accept-language': 'ar,en;q=0.8',
          'accept-encoding': 'gzip, deflate, br',
        },
      },
      (res) => {
        const status = res.statusCode || 502;
        const location = res.headers.location;

        if (status >= 300 && status < 400 && location) {
          res.resume();
          if (depth >= MAX_REDIRECTS) return reject(new Error('too many redirects'));
          return resolve(fetchUrl(new URL(location, target).href, depth + 1));
        }

        const chunks = [];
        let size = 0;
        res.on('data', (c) => {
          size += c.length;
          if (size > MAX_BYTES) {
            res.destroy();
            return reject(new Error('response exceeds size limit'));
          }
          chunks.push(c);
        });
        res.on('end', () => {
          const body = decompress(Buffer.concat(chunks), res.headers['content-encoding']);
          resolve({ status, headers: res.headers, body, url: target.href });
        });
        res.on('error', reject);
      }
    );

    req.setTimeout(REQUEST_TIMEOUT_MS, () => req.destroy(new Error('request timeout')));
    req.on('error', reject);
    req.end();
  });
}

/* ------------------------------------------------------------------ *
 * إعادة كتابة روابط الموارد داخل HTML
 * ------------------------------------------------------------------ */

function relayLink(absoluteUrl) {
  return `/fetch?u=${encodeURIComponent(absoluteUrl)}`;
}

/**
 * يحوّل روابط الموارد في الصفحة إلى روابط تمر عبر هذا الخادم،
 * حتى تُحمّل الأنماط والصور بدل أن تفشل على HTTPS المحجوب.
 */
function rewriteHtml(html, baseUrl) {
  const resolve = (value) => {
    const v = value.trim();
    if (!v || v.startsWith('data:') || v.startsWith('#') ||
        v.startsWith('javascript:') || v.startsWith('mailto:') || v.startsWith('blob:')) {
      return null;
    }
    try {
      return new URL(v, baseUrl).href;
    } catch {
      return null;
    }
  };

  // نزيل <base> الأصلي حتى لا يبطل إعادة الكتابة
  let out = html.replace(/<base\b[^>]*>/gi, '');

  // src / href / poster
  out = out.replace(
    /\b(src|href|poster)\s*=\s*("([^"]*)"|'([^']*)')/gi,
    (match, attr, _quoted, dq, sq) => {
      const abs = resolve(dq !== undefined ? dq : sq);
      return abs ? `${attr}="${relayLink(abs)}"` : match;
    }
  );

  // srcset: قائمة روابط مفصولة بفواصل
  out = out.replace(/\bsrcset\s*=\s*"([^"]*)"/gi, (match, list) => {
    const rewritten = list.split(',').map((entry) => {
      const parts = entry.trim().split(/\s+/);
      const abs = resolve(parts[0] || '');
      if (!abs) return entry.trim();
      return [relayLink(abs), ...parts.slice(1)].join(' ');
    }).join(', ');
    return `srcset="${rewritten}"`;
  });

  // url(...) داخل الأنماط المضمّنة
  out = out.replace(/url\((\s*['"]?)([^'")]+)(['"]?\s*)\)/gi, (match, open, value) => {
    const abs = resolve(value);
    return abs ? `url("${relayLink(abs)}")` : match;
  });

  return out;
}

/** إعادة كتابة url(...) داخل ملفات CSS المستقلة */
function rewriteCss(css, baseUrl) {
  return css.replace(/url\((\s*['"]?)([^'")]+)(['"]?\s*)\)/gi, (match, open, value) => {
    const v = value.trim();
    if (!v || v.startsWith('data:')) return match;
    try {
      return `url("${relayLink(new URL(v, baseUrl).href)}")`;
    } catch {
      return match;
    }
  });
}

/* ------------------------------------------------------------------ *
 * الخادم
 * ------------------------------------------------------------------ */

const server = http.createServer(async (req, res) => {
  const requested = new URL(req.url, `http://127.0.0.1:${PORT}`);

  if (requested.pathname === '/__relay/health') {
    res.writeHead(200, { 'content-type': 'application/json' });
    return res.end(JSON.stringify({ ok: true, port: PORT, upstream: UPSTREAM }));
  }

  if (requested.pathname !== '/fetch') {
    res.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
    return res.end('relay: use /fetch?u=<encoded-url> or /__relay/health');
  }

  const target = requested.searchParams.get('u');
  if (!target) {
    res.writeHead(400, { 'content-type': 'text/plain; charset=utf-8' });
    return res.end('relay: missing "u" parameter');
  }

  try {
    log('fetch', target);
    const result = await fetchUrl(target);
    const contentType = String(result.headers['content-type'] || 'application/octet-stream');

    let body = result.body;
    if (/text\/html/i.test(contentType)) {
      body = Buffer.from(rewriteHtml(body.toString('utf8'), result.url), 'utf8');
    } else if (/text\/css/i.test(contentType)) {
      body = Buffer.from(rewriteCss(body.toString('utf8'), result.url), 'utf8');
    }

    res.writeHead(result.status, {
      'content-type': contentType,
      'content-length': body.length,
      'cache-control': 'no-store',
      'x-relay-url': encodeURI(result.url),
    });
    res.end(body);
  } catch (err) {
    log('error', target, err.message);
    res.writeHead(502, { 'content-type': 'text/plain; charset=utf-8' });
    res.end(`relay fetch failed: ${err.message}`);
  }
});

server.listen(PORT, '127.0.0.1', () => {
  console.error(`[relay] listening on http://127.0.0.1:${PORT}`);
  console.error(`[relay] upstream: ${UPSTREAM ? `${UPSTREAM.host}:${UPSTREAM.port}` : 'direct'}`);
});

for (const signal of ['SIGINT', 'SIGTERM']) {
  process.on(signal, () => {
    server.close();
    process.exit(0);
  });
}
