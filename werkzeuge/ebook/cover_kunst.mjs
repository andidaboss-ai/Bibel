// Gemeinsames Cover-Design für E-Book und Druck:
// großer Titel „DIE BIBEL“, darunter das Titelbild (Kreuz, Splitter, Kirchenfenster) aus cover_vorlage/.
// Jeder Band hat dasselbe Bild in einer anderen Farbe. Die Bilder erzeugt werkzeuge/ebook/cover_bild.py.
import path from 'path';
import { fileURLToPath } from 'url';
import { execFileSync } from 'child_process';

const hier = path.dirname(fileURLToPath(import.meta.url));

// Erzeugt (falls nötig) die gefärbten Titelbilder und gibt den Pfad für eine Ausgabe zurück.
let vorbereitet = false;
export function bildFuer(name) {
  if (!vorbereitet) {
    execFileSync('python3', [path.join(hier, 'cover_bild.py')], { stdio: 'inherit' });
    vorbereitet = true;
  }
  return path.join(hier, 'cover_vorlage', '.farbig', `kunst-${name}.jpg`);
}

// Text und Grafik der Vorderseite als HTML-Baustein.
// a: { farbe, akzent, band, zeile } · W/H: Größe der Fläche in CSS-Pixeln · rect: sichtbares Cover darin · dpr: Pixel je CSS-Pixel
export function vorderseite(a, { W, H, rect, schrift }) {
  const r = rect, w = r.w;
  const css = `
@font-face{font-family:Anton;src:url('${schrift('Anton-Regular.ttf')}')}
.vs{position:absolute;inset:0;overflow:hidden;background:#000}
.vs .kunst{position:absolute;left:0;width:${W}px;bottom:0;object-fit:cover;object-position:center top;
  -webkit-mask-image:linear-gradient(180deg,transparent 0,#000 ${w * 0.05}px)}
.vs .schatten{position:absolute;left:0;width:${W}px;bottom:0;height:${H - r.y - r.h * 0.8}px;
  background:linear-gradient(180deg,transparent,rgba(0,0,0,.55) 45%,rgba(0,0,0,.8))}
.vs .t{position:absolute;left:${r.x}px;width:${w}px;text-align:center}
.vs .titel{top:${r.y + r.h * 0.035}px;font-family:Anton;line-height:.92;color:#fff;white-space:nowrap;
  -webkit-text-stroke:${w * 0.006}px #d9a944;paint-order:stroke fill}
.vs .unter{font-family:Inter;font-weight:800;font-size:${w * 0.036}px;letter-spacing:.42em;padding-left:.42em;color:#e9c46e;white-space:nowrap}
.vs .unten{bottom:${H - r.y - r.h + r.h * 0.035}px}
.vs .pille{font-family:Anton;font-size:${w * 0.085}px;line-height:1;letter-spacing:.04em;padding-left:.04em;text-transform:uppercase;color:#fff;
  -webkit-text-stroke:${w * 0.0035}px #d9a944;paint-order:stroke fill;filter:drop-shadow(0 0 ${w * 0.012}px #000)}
.vs .zeile{margin-top:${w * 0.012}px;font-family:Inter;font-weight:600;font-size:${w * 0.03}px;letter-spacing:.05em;color:#f1e6cf;
  text-shadow:0 0 ${w * 0.01}px #000,0 0 ${w * 0.02}px #000}
.vs .motto{margin-top:${w * 0.03}px;font-family:Inter;font-weight:800;font-size:${w * 0.034}px;letter-spacing:.16em;padding-left:.16em;color:#fff;
  text-shadow:0 0 ${w * 0.01}px #000,0 0 ${w * 0.02}px #000}`;
  const html = `<div class="vs"><img class="kunst" src="file://${a.bild}">
<div class="schatten"></div>
<div class="t titel"><span>DIE BIBEL</span></div>
<div class="t unter">IN LEICHTER SPRACHE</div>
<div class="t unten"><div class="pille">${a.band}</div><div class="zeile">${a.zeile}</div><div class="motto">KI-ERKLÄRT. EINFACH. KLAR.</div></div></div>`;
  const script = `<script>
Promise.all([document.fonts.ready, document.querySelector('.vs .kunst').decode()]).then(() => {
  const t = document.querySelector('.vs .titel');
  t.style.fontSize = '100px';
  t.style.fontSize = (100 * ${w * 0.92} / t.firstChild.offsetWidth) + 'px';
  const u = document.querySelector('.vs .unter');
  u.style.top = (t.offsetTop + t.offsetHeight + ${w * 0.012}) + 'px';
  document.querySelector('.vs .kunst').style.top = (u.offsetTop + u.offsetHeight + ${w * 0.004}) + 'px';
  window.fertig = true;
});
</script>`;
  return { css, html, script };
}

// Farben der Ausgaben: Hauptfarbe und Akzent (für Splitter und Glas)
export const FARBEN = {
  gesamt: { farbe: [255, 150, 40], akzent: [255, 236, 170] },
  'band-1': { farbe: [138, 43, 226], akzent: [64, 210, 255] },
  'band-2': { farbe: [16, 185, 110], akzent: [190, 255, 120] },
  'band-3': { farbe: [30, 110, 255], akzent: [120, 240, 255] },
  'band-4': { farbe: [220, 20, 60], akzent: [255, 150, 90] },
};
