// Baut die E-Book-Cover (JPG, 1600 x 2560 Pixel, wie von Amazon KDP empfohlen).
// Aufruf im Hauptordner:  node werkzeuge/ebook/cover_bauen.mjs
// Danach werkzeuge/ebook/ebook_bauen.py ausführen, damit die Cover in die EPUBs kommen.
import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';
import { vorderseite, FARBEN } from './cover_kunst.mjs';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright')); }

const hier = path.dirname(fileURLToPath(import.meta.url));
const wurzel = path.resolve(hier, '..', '..');
const ziel = path.join(wurzel, 'ausgabe', 'ebook');
fs.mkdirSync(ziel, { recursive: true });
const schrift = (f) => 'file://' + path.join(hier, 'schriften', f);

const ausgaben = [
  { datei: 'bibel-leichte-sprache-gesamt', band: 'Gesamtausgabe', zeile: 'Alle 66 Bücher · 1.189 Kapitel', ...FARBEN.gesamt },
  { datei: 'bibel-leichte-sprache-band-1', band: 'Band 1', zeile: 'Altes Testament · 1. Mose bis 1. Samuel', ...FARBEN['band-1'] },
  { datei: 'bibel-leichte-sprache-band-2', band: 'Band 2', zeile: 'Altes Testament · 2. Samuel bis Psalmen', ...FARBEN['band-2'] },
  { datei: 'bibel-leichte-sprache-band-3', band: 'Band 3', zeile: 'Altes Testament · Sprüche bis Maleachi', ...FARBEN['band-3'] },
  { datei: 'bibel-leichte-sprache-band-4', band: 'Band 4', zeile: 'Neues Testament · Matthäus bis Offenbarung', ...FARBEN['band-4'] },
];

const seite = (a) => {
  const v = vorderseite(a, { W: 1600, H: 2560, rect: { x: 0, y: 0, w: 1600, h: 2560 }, dpr: 1, schrift });
  return `<!doctype html><html lang="de"><head><meta charset="utf-8"><style>
@font-face{font-family:Inter;font-weight:600;src:url('${schrift('Inter-SemiBold.ttf')}')}
@font-face{font-family:Inter;font-weight:800;src:url('${schrift('Inter-ExtraBold.ttf')}')}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1600px;height:2560px;overflow:hidden;background:#000}
${v.css}
</style></head><body>${v.html}${v.script}</body></html>`;
};

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1600, height: 2560 }, deviceScaleFactor: 1 });
const nur = process.argv.slice(2);
for (const a of ausgaben) {
  if (nur.length && !nur.some((n) => a.datei.endsWith(n))) continue;
  const tmp = path.join(ziel, `.cover-${a.datei}.html`);
  fs.writeFileSync(tmp, seite(a));
  await page.goto('file://' + tmp, { waitUntil: 'load' });
  await page.waitForFunction(() => window.fertig === true, null, { timeout: 120000 });
  const datei = path.join(ziel, `${a.datei}-cover.jpg`);
  await page.screenshot({ path: datei, type: 'jpeg', quality: 92 });
  fs.unlinkSync(tmp);
  console.log(path.relative(wurzel, datei));
}
await browser.close();
