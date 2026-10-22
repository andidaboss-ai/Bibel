// Baut den Buchumschlag (Rückseite, Rücken, Vorderseite) als PDF für KDP Print.
// Wird von druck_bauen.py aufgerufen:
// node umschlag.mjs <band-json> <ausgabe.pdf> <breite> <hoehe> <ruecken> <rand_x> <rand_y> <falz> <seiten>
// rand_x/rand_y: Beschnitt (Taschenbuch) bzw. Einschlag (Hardcover). falz: Gelenk neben dem Rücken (nur Hardcover).
// Alle Maße in Zoll. Das Bild wird mit 600 dpi gerendert (UMSCHLAG_DPI) und in ein PDF in exakter Größe gelegt.
import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';
import { execFileSync } from 'child_process';
import { vorderseite, bildFuer, FARBEN, EN, TXT } from '../ebook/cover_kunst.mjs';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright')); }

const hier = path.dirname(fileURLToPath(import.meta.url));
const schrift = (f) => 'file://' + path.join(hier, '..', 'ebook', 'schriften', f);
const alleBaende = JSON.parse(fs.readFileSync(path.join(hier, process.env.BIBEL_SPRACHE === 'en' ? 'baende_en.json' : 'baende.json'), 'utf8'));

const [, , bandJson, aus, b, h, r, rx, ry, fz, seiten] = process.argv;
const band = JSON.parse(bandJson);
const IN = 96; // CSS-Pixel pro Zoll
const DPI = +(process.env.UMSCHLAG_DPI || 600); // Auflösung des fertigen Umschlags
const W = +b * IN, H = +h * IN, R = +r * IN, BE = +rx * IN, BY = +ry * IN, FZ = +fz * IN;
const SB = (W - R) / 2 - BE; // Breite einer Seite des Umschlags ohne Rand, mit Falz
const cm = (px) => (px / IN * 2.54).toFixed(1).replace('.', ',');
const format = `${cm(SB - FZ)} × ${cm(H - 2 * BY)} cm`;
const name = 'band-' + band.titel.replace(/\D/g, '');
const fa = FARBEN[name] || FARBEN.gesamt;
const fc = fa.farbe.join(',');
const v = vorderseite({ ...fa, bild: bildFuer(name), band: band.titel, zeile: `${band.oben} · ${band.zeile}` },
  { W: SB + BE, H, rect: { x: FZ, y: BY, w: SB - FZ, h: H - 2 * BY }, schrift });

const liste = alleBaende.map((x) =>
  `<li class="${x.datei === band.datei ? 'aktiv' : ''}"><span>${x.titel}</span>${x.oben} · ${x.zeile}</li>`).join('');

const html = `<!doctype html><html lang="${EN ? 'en' : 'de'}"><head><meta charset="utf-8"><style>
@font-face{font-family:Cinzel;font-weight:700;src:url('${schrift('Cinzel-Bold.ttf')}')}
@font-face{font-family:Cinzel;font-weight:400;src:url('${schrift('Cinzel-Regular.ttf')}')}
@font-face{font-family:Inter;font-weight:600;src:url('${schrift('Inter-SemiBold.ttf')}')}
@font-face{font-family:Inter;font-weight:800;src:url('${schrift('Inter-ExtraBold.ttf')}')}
@font-face{font-family:Literata;font-weight:400;src:url('${schrift('Literata-Regular.ttf')}')}
@font-face{font-family:Literata;font-style:italic;src:url('${schrift('Literata-Italic.ttf')}')}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:${W}px;height:${H}px;overflow:hidden}
body{position:relative;color:#f4ecdc;font-family:Inter,sans-serif;
  background:#000}
.staub{position:absolute;z-index:0;left:0;top:0;width:${W}px;height:${H}px}
.rueck{background:radial-gradient(ellipse at 30% 35%,rgba(${fc},.22),transparent 60%)}
.flaeche{position:absolute;z-index:1;top:0;height:${H}px;overflow:hidden}
.rueck{left:0;width:${BE + SB}px}
.ruecken{left:${BE + SB}px;width:${R}px;background:linear-gradient(90deg,rgba(0,0,0,.6),rgba(${fc},.22) 50%,rgba(0,0,0,.6))}
.vorn{left:${BE + SB + R}px;width:${SB + BE}px}
${v.css}
/* Rücken */
.r-text{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(-90deg) translateY(${0.019 * Math.min(0.8 * IN, R * 0.62)}px);white-space:nowrap;display:flex;align-items:center;gap:${0.7 * IN}px}
.r-titel{font-family:Anton;font-size:${Math.min(0.8 * IN, R * 0.62)}px;line-height:1;letter-spacing:.04em;color:#fff;-webkit-text-stroke:1.5px #d9a944;paint-order:stroke fill}
/* Rückseite */
.h-in{position:absolute;left:${BE + 0.75 * IN}px;right:${FZ + 0.75 * IN}px;top:${BY + 0.9 * IN}px}
.h-kicker{font-weight:600;font-size:${0.14 * IN}px;letter-spacing:.32em;text-transform:uppercase;color:#d9b86c}
.h-titel{font-family:Anton;font-size:${0.62 * IN}px;line-height:1.05;margin-top:${0.12 * IN}px;color:#fff;-webkit-text-stroke:1.2px #d9a944;paint-order:stroke fill;letter-spacing:.01em}
.h-linie{width:${1.2 * IN}px;height:2px;margin:${0.26 * IN}px 0;background:linear-gradient(90deg,#d9b86c,transparent)}
.h-text p{font-family:Literata;font-size:${0.2 * IN}px;line-height:1.5;margin-bottom:${0.1 * IN}px;color:#efe6d4}
.h-text p.stark{font-family:Inter;font-weight:800;font-size:${0.19 * IN}px;color:#f6e7c2;margin-top:${0.18 * IN}px}
.h-kasten{margin-top:${0.3 * IN}px;border-left:4px solid rgb(${fc});padding:${0.06 * IN}px 0 ${0.06 * IN}px ${0.2 * IN}px}
.h-kasten .k{font-weight:800;font-size:${0.12 * IN}px;letter-spacing:.2em;text-transform:uppercase;color:#d9b86c;margin-bottom:${0.06 * IN}px}
.h-kasten p{font-family:Literata;font-style:italic;font-size:${0.18 * IN}px;line-height:1.45;color:#efe6d4}
ul{list-style:none;margin-top:${0.36 * IN}px}
li{font-weight:600;font-size:${0.15 * IN}px;color:rgba(239,230,212,.62);margin-bottom:${0.07 * IN}px}
li span{display:inline-block;width:${(process.env.BIBEL_SPRACHE === 'en' ? 1.2 : 0.85) * IN}px;white-space:nowrap;font-weight:800;letter-spacing:.14em;text-transform:uppercase}
li.aktiv{color:#f6e7c2}
li.aktiv span{color:#d9b86c}
</style></head><body>
<div class="flaeche rueck">
  <div class="h-in">
    <p class="h-kicker">${band.oben} · ${band.titel}</p>
    <p class="h-titel">${EN ? 'THE BIBLE.<br>IN PLAIN LANGUAGE.' : 'DIE BIBEL.<br>IN LEICHTER SPRACHE.'}</p>
    <div class="h-linie"></div>
    <div class="h-text">
${EN ? `      <p>Short sentences. Clear words.</p>
      <p>One thought on every line.</p>
      <p>No verse is missing, no name and no number.</p>
      <p class="stark">For everyone who really wants to understand the Bible.</p>` : `      <p>Kurze Sätze. Klare Worte.</p>
      <p>Jede Zeile ein Gedanke.</p>
      <p>Kein Vers fehlt, kein Name und keine Zahl.</p>
      <p class="stark">Für alle, die die Bibel wirklich verstehen wollen.</p>`}
    </div>
    <div class="h-kasten"><p class="k">${EN ? 'What does this mean?' : 'Was bedeutet das?'}</p>
      <p>${EN ? 'After every section, a box explains what you have read and what it can mean for us today.' : 'Nach jedem Abschnitt erklärt ein Kasten, was du gelesen hast und was es für heute bedeuten kann.'}</p></div>
    <ul>${liste}</ul>
  </div>
</div>
<div class="flaeche ruecken"><div class="r-text">
  <span class="r-titel">${TXT.titel}</span><span class="r-titel">${band.titel.toUpperCase()}</span>
</div></div>
<div class="flaeche vorn">${v.html}</div>
<canvas class="staub" width="${Math.round(W * DPI / IN)}" height="${Math.round(H * DPI / IN)}"></canvas>
${v.script}
<script>
(() => { const c = document.querySelector('.staub'), x = c.getContext('2d'); let s = 99;
  const r = () => (s = (s * 16807) % 2147483647) / 2147483647, f = c.width * ${(BE + SB) / W};
  for (let i = 0; i < 2600; i++) { const px = r() * f, py = r() * c.height;
    x.fillStyle = r() < 0.5 ? 'rgba(255,196,86,' + (0.15 + r() * 0.5) + ')' : 'rgba(${fc},' + (0.2 + r() * 0.6) + ')';
    x.beginPath(); x.arc(px, py, (0.6 + Math.pow(r(), 5) * 3) * ${DPI / IN}, 0, 7); x.fill(); } })();
</script>
</body></html>`;

const tmp = aus + '.html';
const png = aus + '.png';
fs.writeFileSync(tmp, html);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: Math.ceil(W), height: Math.ceil(H) }, deviceScaleFactor: DPI / IN });
await page.goto('file://' + tmp, { waitUntil: 'load' });
await page.waitForFunction(() => window.fertig === true, null, { timeout: 600000 });
await page.screenshot({ path: png, type: 'png', timeout: 0 });
await browser.close();
// Das Bild als einzige Seite in ein PDF in exakter Umschlaggröße legen
execFileSync('python3', [path.join(hier, 'bild_zu_pdf.py'), png, aus, b, h, String(DPI), aus.replace(/\.pdf$/, '-vorschau.png')], { stdio: 'inherit' });
fs.unlinkSync(png);
fs.unlinkSync(tmp);
