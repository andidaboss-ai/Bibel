// Baut die E-Book-Cover (JPG, 1600 x 2560 Pixel, wie von Amazon KDP empfohlen).
// Aufruf im Hauptordner:  node werkzeuge/ebook/cover_bauen.mjs
// Danach werkzeuge/ebook/ebook_bauen.py ausführen, damit die Cover in die EPUBs kommen.
import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

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
  { datei: 'bibel-leichte-sprache-gesamt', oben: 'Altes und Neues Testament', band: 'Gesamtausgabe',
    zeile: 'Alle 66 Bücher · 1.189 Kapitel', grund: ['#07080d', '#141522'], glut: '255, 196, 92' },
  { datei: 'bibel-leichte-sprache-band-1', oben: 'Altes Testament', band: 'Band 1',
    zeile: '1. Mose bis Ester', grund: ['#0c0805', '#22160c'], glut: '255, 170, 70' },
  { datei: 'bibel-leichte-sprache-band-2', oben: 'Altes Testament', band: 'Band 2',
    zeile: 'Hiob bis Maleachi', grund: ['#05090d', '#0d1d26'], glut: '120, 200, 230' },
  { datei: 'bibel-leichte-sprache-band-3', oben: 'Neues Testament', band: 'Band 3',
    zeile: 'Matthäus bis Offenbarung', grund: ['#0d0507', '#260c12'], glut: '255, 120, 110' },
];

const seite = (a) => `<!doctype html><html lang="de"><head><meta charset="utf-8"><style>
@font-face{font-family:Cinzel;font-weight:700;src:url('${schrift('Cinzel-Bold.ttf')}')}
@font-face{font-family:Cinzel;font-weight:400;src:url('${schrift('Cinzel-Regular.ttf')}')}
@font-face{font-family:Inter;font-weight:600;src:url('${schrift('Inter-SemiBold.ttf')}')}
@font-face{font-family:Inter;font-weight:800;src:url('${schrift('Inter-ExtraBold.ttf')}')}
@font-face{font-family:Literata;font-style:italic;src:url('${schrift('Literata-Italic.ttf')}')}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1600px;height:2560px;overflow:hidden}
body{background:linear-gradient(180deg,${a.grund[1]} 0%,${a.grund[0]} 62%,#020203 100%);color:#f4ecdc;position:relative;font-family:Inter,sans-serif}
.strahlen{position:absolute;left:50%;top:880px;width:3600px;height:3600px;margin:-1800px 0 0 -1800px;
  background:repeating-conic-gradient(from 0deg,rgba(${a.glut},.075) 0deg 2.2deg,transparent 2.2deg 9deg);
  -webkit-mask-image:radial-gradient(circle,#000 0%,rgba(0,0,0,.55) 22%,transparent 52%);mask-image:radial-gradient(circle,#000 0%,rgba(0,0,0,.55) 22%,transparent 52%)}
.glut{position:absolute;left:50%;top:880px;width:2200px;height:2200px;margin:-1100px 0 0 -1100px;border-radius:50%;
  background:radial-gradient(circle,rgba(${a.glut},.55) 0%,rgba(${a.glut},.22) 12%,rgba(${a.glut},.07) 30%,transparent 55%)}
.ring{position:absolute;left:50%;top:880px;border-radius:50%;border:2px solid rgba(232,196,120,.28);transform:translate(-50%,-50%)}
.balken-v{position:absolute;left:50%;top:180px;width:6px;height:1080px;margin-left:-3px;
  background:linear-gradient(180deg,transparent 0%,rgba(255,236,190,.95) 38%,#fff6dc 50%,rgba(255,236,190,.95) 62%,transparent 100%);
  box-shadow:0 0 40px 8px rgba(${a.glut},.55),0 0 160px 40px rgba(${a.glut},.25);border-radius:3px}
.balken-h{position:absolute;left:50%;top:740px;width:700px;height:6px;margin-left:-350px;
  background:linear-gradient(90deg,transparent 0%,rgba(255,236,190,.95) 30%,#fff6dc 50%,rgba(255,236,190,.95) 70%,transparent 100%);
  box-shadow:0 0 40px 8px rgba(${a.glut},.5),0 0 140px 30px rgba(${a.glut},.2);border-radius:3px}
.korn{position:absolute;inset:0;opacity:.13;mix-blend-mode:overlay}
.rahmen{position:absolute;inset:56px;border:2px solid rgba(214,178,104,.35)}
.rahmen::after{content:'';position:absolute;inset:18px;border:1px solid rgba(214,178,104,.18)}
.oben{position:absolute;top:150px;width:100%;text-align:center;font-weight:600;font-size:38px;letter-spacing:.42em;
  text-transform:uppercase;color:#d9b86c;padding-left:.42em}
.titel{position:absolute;top:1190px;width:100%;text-align:center}
.die{font-family:Cinzel;font-weight:400;font-size:120px;letter-spacing:.5em;padding-left:.5em;color:#efe2c4}
.bibel{font-family:Cinzel;font-weight:700;font-size:330px;line-height:1;letter-spacing:.06em;padding-left:.06em;margin-top:10px;
  background:linear-gradient(180deg,#fff7df 0%,#f1d48d 34%,#c9973f 62%,#8a5f1f 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 10px 40px rgba(0,0,0,.6)) drop-shadow(0 0 60px rgba(${a.glut},.25))}
.linie{width:420px;height:3px;margin:48px auto 44px;background:linear-gradient(90deg,transparent,#d9b86c,transparent)}
.leicht{font-family:Cinzel;font-weight:700;font-size:84px;line-height:1.18;letter-spacing:.14em;padding-left:.14em;color:#f4ecdc}
.unten{position:absolute;bottom:170px;width:100%;text-align:center}
.band{display:inline-block;font-weight:800;font-size:44px;letter-spacing:.32em;padding:26px 54px 26px calc(54px + .32em);
  text-transform:uppercase;color:#1a1206;background:linear-gradient(180deg,#f6dc98,#c9973f);border-radius:999px;
  box-shadow:0 10px 40px rgba(0,0,0,.5)}
.zeile{margin-top:44px;font-weight:600;font-size:46px;letter-spacing:.08em;color:#e9dcc0}
.motto{margin-top:30px;font-family:Literata;font-style:italic;font-size:44px;color:rgba(244,236,220,.78)}
</style></head><body>
<div class="glut"></div><div class="strahlen"></div>
<div class="ring" style="width:620px;height:620px"></div>
<div class="ring" style="width:980px;height:980px;border-color:rgba(232,196,120,.16)"></div>
<div class="ring" style="width:1380px;height:1380px;border-color:rgba(232,196,120,.09)"></div>
<div class="balken-v"></div><div class="balken-h"></div>
<svg class="korn" width="1600" height="2560"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>
<div class="rahmen"></div>
<div class="oben">${a.oben}</div>
<div class="titel"><div class="die">Die</div><div class="bibel">BIBEL</div><div class="linie"></div><div class="leicht">IN LEICHTER<br>SPRACHE</div></div>
<div class="unten"><div class="band">${a.band}</div><div class="zeile">${a.zeile}</div><div class="motto">Kurze Sätze. Klare Worte. Jeder Abschnitt erklärt.</div></div>
</body></html>`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1600, height: 2560 }, deviceScaleFactor: 1 });
const nur = process.argv.slice(2);
for (const a of ausgaben) {
  if (nur.length && !nur.some((n) => a.datei.endsWith(n))) continue;
  const tmp = path.join(ziel, `.cover-${a.datei}.html`);
  fs.writeFileSync(tmp, seite(a));
  await page.goto('file://' + tmp, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const datei = path.join(ziel, `${a.datei}-cover.jpg`);
  await page.screenshot({ path: datei, type: 'jpeg', quality: 92 });
  fs.unlinkSync(tmp);
  console.log(path.relative(wurzel, datei));
}
await browser.close();
