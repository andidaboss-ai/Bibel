// Baut den Buchumschlag (Rückseite, Rücken, Vorderseite) als PDF für KDP Print.
// Wird von druck_bauen.py aufgerufen:
// node umschlag.mjs <band-json> <ausgabe.pdf> <breite> <hoehe> <ruecken> <seite_b> <seite_h> <beschnitt> <seiten>
// Alle Maße in Zoll. Das Bild wird mit 300 dpi gerendert und in ein PDF in exakter Größe gelegt.
import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright')); }

const hier = path.dirname(fileURLToPath(import.meta.url));
const schrift = (f) => 'file://' + path.join(hier, '..', 'ebook', 'schriften', f);
const alleBaende = JSON.parse(fs.readFileSync(path.join(hier, 'baende.json'), 'utf8'));

const [, , bandJson, aus, b, h, r, sb, sh, be, seiten] = process.argv;
const band = JSON.parse(bandJson);
const IN = 96; // CSS-Pixel pro Zoll
const W = +b * IN, H = +h * IN, R = +r * IN, SB = +sb * IN, BE = +be * IN;
const g = band.glut;

const liste = alleBaende.map((x) =>
  `<li class="${x.datei === band.datei ? 'aktiv' : ''}"><span>${x.titel}</span>${x.oben} · ${x.zeile}</li>`).join('');

const html = `<!doctype html><html lang="de"><head><meta charset="utf-8"><style>
@font-face{font-family:Cinzel;font-weight:700;src:url('${schrift('Cinzel-Bold.ttf')}')}
@font-face{font-family:Cinzel;font-weight:400;src:url('${schrift('Cinzel-Regular.ttf')}')}
@font-face{font-family:Inter;font-weight:600;src:url('${schrift('Inter-SemiBold.ttf')}')}
@font-face{font-family:Inter;font-weight:800;src:url('${schrift('Inter-ExtraBold.ttf')}')}
@font-face{font-family:Literata;font-weight:400;src:url('${schrift('Literata-Regular.ttf')}')}
@font-face{font-family:Literata;font-style:italic;src:url('${schrift('Literata-Italic.ttf')}')}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:${W}px;height:${H}px;overflow:hidden}
body{position:relative;color:#f4ecdc;font-family:Inter,sans-serif;
  background:linear-gradient(180deg,${band.grund[1]} 0%,${band.grund[0]} 60%,#020203 100%)}
.flaeche{position:absolute;top:0;height:${H}px;overflow:hidden}
.rueck{left:0;width:${BE + SB}px}
.ruecken{left:${BE + SB}px;width:${R}px;background:linear-gradient(90deg,rgba(0,0,0,.35),rgba(255,255,255,.04) 50%,rgba(0,0,0,.35))}
.vorn{left:${BE + SB + R}px;width:${SB + BE}px}
/* Vorderseite: Inhalt im sicheren Bereich (Beschnitt + 0,375 Zoll) */
.v-in{position:absolute;left:0;top:${BE}px;width:${SB}px;height:${H - 2 * BE}px}
.glut{position:absolute;left:50%;top:${2.9 * IN}px;width:${9 * IN}px;height:${9 * IN}px;margin:${-4.5 * IN}px 0 0 ${-4.5 * IN}px;border-radius:50%;
  background:radial-gradient(circle,rgba(${g},.55) 0%,rgba(${g},.22) 12%,rgba(${g},.07) 30%,transparent 55%)}
.strahlen{position:absolute;left:50%;top:${2.9 * IN}px;width:${14 * IN}px;height:${14 * IN}px;margin:${-7 * IN}px 0 0 ${-7 * IN}px;
  background:repeating-conic-gradient(from 0deg,rgba(${g},.075) 0deg 2.2deg,transparent 2.2deg 9deg);
  -webkit-mask-image:radial-gradient(circle,#000 0%,rgba(0,0,0,.55) 22%,transparent 52%)}
.ring{position:absolute;left:50%;top:${2.9 * IN}px;border-radius:50%;border:1.5px solid rgba(232,196,120,.28);transform:translate(-50%,-50%)}
.bv{position:absolute;left:50%;top:${0.7 * IN}px;width:4px;height:${4.2 * IN}px;margin-left:-2px;border-radius:2px;
  background:linear-gradient(180deg,transparent,rgba(255,236,190,.95) 38%,#fff6dc 50%,rgba(255,236,190,.95) 62%,transparent);
  box-shadow:0 0 26px 6px rgba(${g},.55),0 0 110px 26px rgba(${g},.22)}
.bh{position:absolute;left:50%;top:${2.35 * IN}px;width:${2.8 * IN}px;height:4px;margin-left:${-1.4 * IN}px;border-radius:2px;
  background:linear-gradient(90deg,transparent,rgba(255,236,190,.95) 30%,#fff6dc 50%,rgba(255,236,190,.95) 70%,transparent);
  box-shadow:0 0 26px 6px rgba(${g},.5),0 0 90px 20px rgba(${g},.2)}
.rahmen{position:absolute;left:${0.3 * IN}px;right:${0.3 * IN}px;top:${0.3 * IN}px;bottom:${0.3 * IN}px;border:1.5px solid rgba(214,178,104,.35)}
.oben{position:absolute;top:${0.62 * IN}px;width:100%;text-align:center;font-weight:600;font-size:${0.15 * IN}px;letter-spacing:.42em;padding-left:.42em;text-transform:uppercase;color:#d9b86c}
.titel{position:absolute;top:${5.0 * IN}px;width:100%;text-align:center}
.die{font-family:Cinzel;font-weight:400;font-size:${0.46 * IN}px;letter-spacing:.5em;padding-left:.5em;color:#efe2c4}
.bibel{font-family:Cinzel;font-weight:700;font-size:${1.32 * IN}px;line-height:1;letter-spacing:.06em;padding-left:.06em;margin-top:4px;
  background:linear-gradient(180deg,#fff7df 0%,#f1d48d 34%,#c9973f 62%,#8a5f1f 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.linie{width:${1.7 * IN}px;height:2px;margin:${0.2 * IN}px auto ${0.18 * IN}px;background:linear-gradient(90deg,transparent,#d9b86c,transparent)}
.leicht{font-family:Cinzel;font-weight:700;font-size:${0.34 * IN}px;line-height:1.2;letter-spacing:.14em;padding-left:.14em}
.unten{position:absolute;bottom:${0.75 * IN}px;width:100%;text-align:center}
.pille{display:inline-block;font-weight:800;font-size:${0.18 * IN}px;letter-spacing:.32em;padding:${0.1 * IN}px ${0.24 * IN}px ${0.1 * IN}px calc(${0.24 * IN}px + .32em);
  text-transform:uppercase;color:#1a1206;background:linear-gradient(180deg,#f6dc98,#c9973f);border-radius:999px}
.zeile{margin-top:${0.16 * IN}px;font-weight:600;font-size:${0.19 * IN}px;letter-spacing:.06em;color:#e9dcc0}
.motto{margin-top:${0.1 * IN}px;font-family:Literata;font-style:italic;font-size:${0.17 * IN}px;color:rgba(244,236,220,.8)}
/* Rücken */
.r-text{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(-90deg);white-space:nowrap;display:flex;align-items:center;gap:${0.28 * IN}px}
.r-titel{font-family:Cinzel;font-weight:700;font-size:${Math.min(0.42 * IN, R * 0.42)}px;letter-spacing:.08em;color:#f1d48d}
.r-unter{font-family:Cinzel;font-weight:700;font-size:${Math.min(0.2 * IN, R * 0.22)}px;letter-spacing:.12em}
.r-band{font-weight:800;font-size:${Math.min(0.17 * IN, R * 0.2)}px;letter-spacing:.24em;text-transform:uppercase;color:#1a1206;background:linear-gradient(180deg,#f6dc98,#c9973f);padding:${0.04 * IN}px ${0.14 * IN}px;border-radius:999px}
.r-zeile{font-weight:600;font-size:${Math.min(0.16 * IN, R * 0.18)}px;letter-spacing:.06em;color:#e9dcc0}
/* Rückseite */
.h-in{position:absolute;left:${BE + 0.75 * IN}px;right:${0.75 * IN}px;top:${BE + 0.9 * IN}px}
.h-kicker{font-weight:600;font-size:${0.14 * IN}px;letter-spacing:.32em;text-transform:uppercase;color:#d9b86c}
.h-titel{font-family:Cinzel;font-weight:700;font-size:${0.44 * IN}px;line-height:1.15;margin-top:${0.12 * IN}px;color:#f6e7c2}
.h-linie{width:${1.2 * IN}px;height:2px;margin:${0.26 * IN}px 0;background:linear-gradient(90deg,#d9b86c,transparent)}
.h-text p{font-family:Literata;font-size:${0.2 * IN}px;line-height:1.5;margin-bottom:${0.1 * IN}px;color:#efe6d4}
.h-text p.stark{font-family:Inter;font-weight:800;font-size:${0.19 * IN}px;color:#f6e7c2;margin-top:${0.18 * IN}px}
.h-kasten{margin-top:${0.3 * IN}px;border-left:4px solid #c9973f;padding:${0.06 * IN}px 0 ${0.06 * IN}px ${0.2 * IN}px}
.h-kasten .k{font-weight:800;font-size:${0.12 * IN}px;letter-spacing:.2em;text-transform:uppercase;color:#d9b86c;margin-bottom:${0.06 * IN}px}
.h-kasten p{font-family:Literata;font-style:italic;font-size:${0.18 * IN}px;line-height:1.45;color:#efe6d4}
ul{list-style:none;margin-top:${0.36 * IN}px}
li{font-weight:600;font-size:${0.15 * IN}px;color:rgba(239,230,212,.62);margin-bottom:${0.07 * IN}px}
li span{display:inline-block;width:${0.85 * IN}px;font-weight:800;letter-spacing:.14em;text-transform:uppercase}
li.aktiv{color:#f6e7c2}
li.aktiv span{color:#d9b86c}
.h-quelle{position:absolute;left:${BE + 0.75 * IN}px;bottom:${BE + 0.55 * IN}px;width:${3.6 * IN}px;font-size:${0.11 * IN}px;line-height:1.45;color:rgba(239,230,212,.55)}
</style></head><body>
<div class="flaeche rueck">
  <div class="h-in">
    <p class="h-kicker">${band.oben} · ${band.titel}</p>
    <p class="h-titel">Die Bibel.<br>In Leichter Sprache.</p>
    <div class="h-linie"></div>
    <div class="h-text">
      <p>Kurze Sätze. Klare Worte.</p>
      <p>Jede Zeile ein Gedanke.</p>
      <p>Kein Vers fehlt, kein Name und keine Zahl.</p>
      <p class="stark">Für alle, die die Bibel wirklich verstehen wollen.</p>
    </div>
    <div class="h-kasten"><p class="k">Was bedeutet das?</p>
      <p>Nach jedem Abschnitt erklärt ein Kasten, was du gelesen hast und was es für heute bedeuten kann.</p></div>
    <ul>${liste}</ul>
  </div>
  <p class="h-quelle">Neu übertragen aus der gemeinfreien World English Bible. Großformat 21,6 × 27,9 cm. ${seiten} Seiten.</p>
</div>
<div class="flaeche ruecken"><div class="r-text">
  <span class="r-titel">DIE BIBEL</span><span class="r-unter">IN LEICHTER SPRACHE</span>
  <span class="r-band">${band.titel}</span><span class="r-zeile">${band.zeile}</span>
</div></div>
<div class="flaeche vorn"><div class="v-in">
  <div class="glut"></div><div class="strahlen"></div>
  <div class="ring" style="width:${2.3 * IN}px;height:${2.3 * IN}px"></div>
  <div class="ring" style="width:${3.7 * IN}px;height:${3.7 * IN}px;border-color:rgba(232,196,120,.16)"></div>
  <div class="ring" style="width:${5.2 * IN}px;height:${5.2 * IN}px;border-color:rgba(232,196,120,.09)"></div>
  <div class="bv"></div><div class="bh"></div>
  <div class="rahmen"></div>
  <div class="oben">${band.oben}</div>
  <div class="titel"><div class="die">Die</div><div class="bibel">BIBEL</div><div class="linie"></div><div class="leicht">IN LEICHTER<br>SPRACHE</div></div>
  <div class="unten"><div class="pille">${band.titel}</div><div class="zeile">${band.zeile}</div><div class="motto">Kurze Sätze. Klare Worte. Jeder Abschnitt erklärt.</div></div>
</div></div>
</body></html>`;

const tmp = aus + '.html';
const png = aus + '.png';
fs.writeFileSync(tmp, html);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: Math.round(W), height: Math.round(H) }, deviceScaleFactor: 300 / IN });
await page.goto('file://' + tmp, { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: png, type: 'png' });
// Das 300-dpi-Bild als einzige Seite in ein PDF in exakter Umschlaggröße legen
fs.writeFileSync(tmp, `<!doctype html><html><head><style>@page{size:${b}in ${h}in;margin:0}html,body{margin:0}img{display:block;width:${b}in;height:${h}in}</style></head><body><img src="file://${png}"></body></html>`);
const p2 = await browser.newPage();
await p2.goto('file://' + tmp, { waitUntil: 'load' });
await p2.pdf({ path: aus, width: `${b}in`, height: `${h}in`, printBackground: true, preferCSSPageSize: true });
await browser.close();
fs.renameSync(png, aus.replace(/\.pdf$/, '-vorschau.png'));
fs.unlinkSync(tmp);
