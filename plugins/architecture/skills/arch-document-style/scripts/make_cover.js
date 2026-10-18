#!/usr/bin/env node
/*
 * Genera la portada del documento como PNG a sangre completa (2550x3300 px,
 * carta a 300 ppp) a partir de un JSON.
 *
 * Uso: node make_cover.js document/source/cover.json document/source/cover.png
 *
 * cover.json: {"titulo": "...", "subtitulo": "...",
 *                "para": ["linea 1", "linea 2"], "por": ["linea 1", "linea 2"]}
 *
 * Requiere Playwright con Chromium (npm install playwright && npx playwright install chromium).
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

function load(name) {
  const tries = [
    () => require(name),
    () => require(path.join(process.cwd(), 'node_modules', name)),
    () => require(path.join(execSync('npm root -g').toString().trim(), name)),
  ];
  for (const t of tries) { try { return t(); } catch (e) { /* siguiente */ } }
  console.error(`No encuentro "${name}". Instalalo con: npm install ${name} && npx playwright install chromium`);
  process.exit(1);
}
const { chromium } = load('playwright');

const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const lines = (x) => (Array.isArray(x) ? x : [x]).filter(Boolean).map((l, i) =>
  i === 0 ? `<div class="strong">${esc(l)}</div>` : `<div>${esc(l)}</div>`).join('');

async function main() {
  const [specPath, outPath = 'cover.png'] = process.argv.slice(2);
  if (!specPath) { console.error('Uso: node make_cover.js document/source/cover.json document/source/cover.png'); process.exit(1); }
  const s = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { width: 1275px; height: 1650px; }
    body { font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif; color: #fff;
      background: linear-gradient(160deg, #0b1220 0%, #15213b 55%, #1e2f55 100%);
      display: flex; flex-direction: column; justify-content: space-between; padding: 150px 120px 120px; }
    .kicker { font-size: 26px; letter-spacing: 6px; text-transform: uppercase; color: #9fb3d9; }
    h1 { font-size: 86px; line-height: 1.08; font-weight: 700; margin-top: 36px; }
    .rule { width: 180px; height: 8px; background: #4f8cff; margin: 56px 0 44px; border-radius: 4px; }
    .sub { font-size: 38px; line-height: 1.3; color: #d5def0; max-width: 980px; }
    .foot { display: flex; gap: 120px; border-top: 2px solid rgba(255,255,255,.18); padding-top: 44px; }
    .blk { flex: 1; font-size: 24px; line-height: 1.5; color: #c4cfe4; }
    .lbl { font-size: 20px; letter-spacing: 4px; text-transform: uppercase; color: #7f93bb; margin-bottom: 12px; }
    .strong { color: #fff; font-weight: 600; font-size: 27px; }
  </style></head><body>
    <div>
      <div class="kicker">${esc(s.kicker || 'Documento de arquitectura')}</div>
      <h1>${esc(s.titulo)}</h1>
      <div class="rule"></div>
      <div class="sub">${esc(s.subtitulo)}</div>
    </div>
    <div class="foot">
      <div class="blk"><div class="lbl">Para</div>${lines(s.para)}</div>
      <div class="blk"><div class="lbl">Por</div>${lines(s.por)}</div>
    </div>
  </body></html>`;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1275, height: 1650 }, deviceScaleFactor: 2 });
  await page.setContent(html, { waitUntil: 'load' });
  await page.screenshot({ path: path.resolve(outPath), fullPage: false });
  await browser.close();
  console.log('OK ->', path.resolve(outPath));
}
main().catch((e) => { console.error(e); process.exit(1); });
