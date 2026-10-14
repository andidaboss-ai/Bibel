// Gemeinsames Cover-Design für E-Book und Druck:
// großer Titel „DIE BIBEL“, darunter ein leuchtendes Kreuz aus Kristall, Splitter, Funken und Kirchenfenster.
// Jeder Band hat dieselbe Komposition (gleicher Zufalls-Startwert), nur in einer anderen Farbe.
// Alles wird mit Canvas gezeichnet. So ist das Bild in jeder Größe scharf (auch 300 dpi für den Druck).

// Wird als Text in die Seite eingebaut (zeichne.toString()), darf also nichts von außen benutzen.
export function zeichne(cv, o) {
  const W = cv.width, H = cv.height, x = cv.getContext('2d');
  const R = o.rect; // Fläche des sichtbaren Covers (ohne Beschnitt/Einschlag) in Canvas-Pixeln
  let s = o.seed || 20260;
  const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  const gauss = () => { let u = 0; for (let i = 0; i < 6; i++) u += rnd(); return (u - 3) / 1.73; };
  const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  const F = o.farbe, A = o.akzent, GOLD = [255, 196, 86], HELL = [255, 246, 222];
  const u = R.w / 1000;
  const k = Math.min(R.w * 0.85, R.h * (0.775 - o.frei) / 1.12);
  const cx = R.x + R.w / 2, cy = R.y + R.h * o.frei + k * 0.47;

  x.fillStyle = '#000'; x.fillRect(0, 0, W, H);

  // ---------- Nebel ----------
  x.globalCompositeOperation = 'lighter';
  const fleck = (px, py, rr, c, a) => {
    const g = x.createRadialGradient(px, py, 0, px, py, rr);
    g.addColorStop(0, rgba(c, a)); g.addColorStop(1, rgba(c, 0));
    x.fillStyle = g; x.fillRect(px - rr, py - rr, 2 * rr, 2 * rr);
  };
  fleck(cx, cy, k * 0.95, F, 0.22);
  for (let i = 0; i < 46; i++) {
    const seite = rnd() < 0.5 ? -1 : 1;
    fleck(cx + seite * Math.abs(gauss()) * k * 0.42, cy + gauss() * k * 0.36, k * (0.06 + rnd() * 0.2),
      rnd() < 0.5 ? F : GOLD, 0.07 + rnd() * 0.1);
  }

  // ---------- Funken (Staub) ----------
  const funken = (n, streu, groesse) => {
    for (let i = 0; i < n; i++) {
      const w = rnd() * Math.PI * 2, d = Math.pow(rnd(), 0.8) * k * streu * (0.6 + 0.4 * Math.abs(gauss()));
      const px = cx + Math.cos(w) * d * 1.05, py = cy + Math.sin(w) * d * 0.95;
      if (py < R.y + R.h * o.frei) continue;
      const r = (0.6 + Math.pow(rnd(), 4) * groesse) * u;
      const c = rnd() < 0.5 ? GOLD : rnd() < 0.8 ? F : rnd() < 0.5 ? A : HELL;
      x.fillStyle = rgba(c, 0.35 + rnd() * 0.65);
      x.beginPath(); x.arc(px, py, r, 0, Math.PI * 2); x.fill();
    }
  };
  funken(14000, 1.0, 3.4);

  // ---------- Kirchenfenster ----------
  x.globalCompositeOperation = 'source-over';
  const bogen = (x0, x1, ys, yb, rf) => {
    const sp = x1 - x0, r = sp * rf, mid = (x0 + x1) / 2, ah = Math.sqrt(r * r - (r - sp / 2) ** 2);
    const p = new Path2D();
    p.moveTo(x0, yb); p.lineTo(x0, ys);
    p.arc(x0 + r, ys, r, Math.PI, Math.atan2(-ah, mid - (x0 + r)) + 2 * Math.PI);
    p.arc(x1 - r, ys, r, Math.atan2(-ah, mid - (x1 - r)) + 2 * Math.PI, 2 * Math.PI);
    p.lineTo(x1, yb); p.closePath();
    return { p, ah };
  };
  const glas = (pfad, x0, y0, x1, y1, zelle) => {
    x.save(); x.clip(pfad);
    x.fillStyle = '#05040a'; x.fillRect(x0, y0, x1 - x0, y1 - y0);
    for (let gy = y0 - zelle; gy < y1 + zelle; gy += zelle * 0.5) {
      const versatz = (Math.round((gy - y0) / (zelle * 0.5)) % 2) * zelle * 0.5;
      for (let gx = x0 - zelle + versatz; gx < x1 + zelle; gx += zelle) {
        const z = rnd();
        const c = z < 0.45 ? F : z < 0.65 ? GOLD : z < 0.8 ? A : z < 0.93 ? F.map((v) => v * 0.45) : HELL;
        const hoehe = (y1 - gy) / (y1 - y0); // oben dunkler
        x.fillStyle = rgba(c, (0.55 + rnd() * 0.45) * Math.min(1, 0.5 + (1 - hoehe) * 1.2));
        x.beginPath();
        x.moveTo(gx, gy - zelle * 0.5); x.lineTo(gx + zelle * 0.5, gy); x.lineTo(gx, gy + zelle * 0.5); x.lineTo(gx - zelle * 0.5, gy);
        x.closePath(); x.fill();
        x.strokeStyle = '#07050c'; x.lineWidth = 2.6 * u; x.stroke();
      }
    }
    // Glanz
    const g = x.createLinearGradient(x0, y0, x1, y1);
    g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(0.5, 'rgba(255,255,255,.08)'); g.addColorStop(1, 'rgba(255,255,255,0)');
    x.fillStyle = g; x.fillRect(x0, y0, x1 - x0, y1 - y0);
    x.restore();
  };
  const stein = (pfad, breite) => {
    x.save();
    x.strokeStyle = '#121018'; x.lineWidth = breite; x.stroke(pfad);
    x.strokeStyle = rgba(F, 0.35); x.lineWidth = 1.6 * u; x.stroke(pfad);
    x.restore();
  };
  // großer Bogen um das Ganze
  const span = R.w * 0.96, gx0 = R.x + R.w * 0.02, gx1 = gx0 + span;
  const gr = bogen(gx0, gx1, 0, 0, 0.62);
  const ys = R.y + R.h * (o.frei + 0.05) + gr.ah;
  const gross = bogen(gx0, gx1, ys, H + 10, 0.62);
  x.save(); x.globalAlpha = 0.9; stein(gross.p, 14 * u);
  const innen = bogen(gx0 + 26 * u, gx1 - 26 * u, ys, H + 10, 0.62);
  x.strokeStyle = rgba(GOLD, 0.16); x.lineWidth = 1.4 * u; x.stroke(innen.p); x.restore();
  // zwei Fenster unten links und rechts
  const fb = R.w * 0.27, fys = R.y + R.h * 0.8;
  for (const [a0, a1] of [[R.x + R.w * 0.035, R.x + R.w * 0.035 + fb], [R.x + R.w * 0.965 - fb, R.x + R.w * 0.965]]) {
    const f = bogen(a0, a1, fys, H + 10, 0.75);
    glas(f.p, a0, fys - f.ah, a1, H + 10, 34 * u);
    // Maßwerk: senkrechte Sprosse und ein kleiner Bogen
    x.save(); x.clip(f.p);
    x.strokeStyle = '#0d0b12'; x.lineWidth = 7 * u;
    x.beginPath(); x.moveTo((a0 + a1) / 2, fys - f.ah * 0.35); x.lineTo((a0 + a1) / 2, H + 10); x.stroke();
    x.restore();
    stein(f.p, 12 * u);
  }
  // unten abdunkeln, damit die Schrift lesbar bleibt
  const dunkel = x.createLinearGradient(0, R.y + R.h * 0.8, 0, H);
  dunkel.addColorStop(0, 'rgba(0,0,0,0)'); dunkel.addColorStop(0.55, 'rgba(0,0,0,.55)'); dunkel.addColorStop(1, 'rgba(0,0,0,.85)');
  x.fillStyle = dunkel; x.fillRect(0, R.y + R.h * 0.8, W, H);

  // ---------- Splitter ----------
  const splitter = (n, innenR, aussenR, gr0, gr1) => {
    for (let i = 0; i < n; i++) {
      const w = rnd() * Math.PI * 2, d = k * (innenR + Math.pow(rnd(), 0.75) * (aussenR - innenR));
      const px = cx + Math.cos(w) * d * 1.08, py = cy + Math.sin(w) * d * 0.92;
      const L = (gr0 + rnd() * (gr1 - gr0)) * u;
      if (py - L < R.y + R.h * o.frei || py + L > R.y + R.h * 0.83) continue;
      const b = L * (0.32 + rnd() * 0.3), rot = w + (rnd() - 0.5) * 1.2;
      const pts = [[L * 0.5, 0], [0, b * (0.4 + rnd() * 0.6)], [-L * 0.5, 0], [0, -b * (0.4 + rnd() * 0.6)]]
        .map(([a, c]) => [px + a * Math.cos(rot) - c * Math.sin(rot) + (rnd() - 0.5) * L * 0.12,
                          py + a * Math.sin(rot) + c * Math.cos(rot) + (rnd() - 0.5) * L * 0.12]);
      x.beginPath(); pts.forEach(([a, c], j) => j ? x.lineTo(a, c) : x.moveTo(a, c)); x.closePath();
      const g = x.createLinearGradient(pts[0][0], pts[0][1], pts[2][0], pts[2][1]);
      const z = rnd();
      g.addColorStop(0, rgba(F, 1));
      g.addColorStop(0.45, rgba(z < 0.3 ? A : z < 0.6 ? GOLD : HELL, 0.8));
      g.addColorStop(1, rgba(F.map((v) => v * 0.6), 0.95));
      x.save();
      x.shadowColor = rgba(F, 0.9); x.shadowBlur = 18 * u;
      x.fillStyle = g; x.fill();
      x.shadowBlur = 0;
      x.strokeStyle = rgba(HELL, 0.85); x.lineWidth = 1.4 * u; x.stroke();
      // Lichtkante
      x.beginPath(); x.moveTo(pts[0][0], pts[0][1]); x.lineTo(pts[1][0], pts[1][1]);
      x.strokeStyle = 'rgba(255,255,255,.9)'; x.lineWidth = 2.2 * u; x.stroke();
      x.restore();
    }
  };
  splitter(150, 0.22, 1.05, 18, 95);

  // ---------- Kreuz ----------
  const bw = k * 0.15, top = cy - k * 0.43, unten = cy + k * 0.62, links = cx - k * 0.36, rechts = cx + k * 0.36;
  const hy = cy - bw * 0.15;
  const ecken = [[cx - bw / 2, top], [cx + bw / 2, top], [cx + bw / 2, hy - bw / 2], [rechts, hy - bw / 2], [rechts, hy + bw / 2],
    [cx + bw / 2, hy + bw / 2], [cx + bw / 2, unten], [cx - bw / 2, unten], [cx - bw / 2, hy + bw / 2], [links, hy + bw / 2],
    [links, hy - bw / 2], [cx - bw / 2, hy - bw / 2]];
  const kreuz = new Path2D();
  ecken.forEach(([a, c], i) => {
    const [n0, n1] = ecken[(i + 1) % ecken.length];
    if (!i) kreuz.moveTo(a, c);
    const schritte = Math.max(2, Math.round(Math.hypot(n0 - a, n1 - c) / (22 * u)));
    for (let j = 1; j <= schritte; j++) {
      const t = j / schritte, z = j === schritte ? 0 : (rnd() - 0.5) * 9 * u;
      const nx = (n1 - c), ny = -(n0 - a), l = Math.hypot(nx, ny) || 1;
      kreuz.lineTo(a + (n0 - a) * t + nx / l * z, c + (n1 - c) * t + ny / l * z);
    }
  });
  kreuz.closePath();
  x.save();
  x.shadowColor = rgba(F, 1); x.shadowBlur = 60 * u;
  const kg = x.createLinearGradient(0, top, 0, unten);
  kg.addColorStop(0, rgba(F.map((v) => v * 0.55), 1)); kg.addColorStop(0.35, rgba(F, 1)); kg.addColorStop(1, rgba(F.map((v) => v * 0.35), 1));
  x.fillStyle = kg; x.fill(kreuz);
  x.restore();
  // Leiterbahnen im Kreuz
  x.save(); x.clip(kreuz);
  for (let i = 0; i < 90; i++) {
    const px = links + rnd() * (rechts - links), py = top + rnd() * (unten - top), gr = (12 + rnd() * 60) * u;
    x.beginPath(); x.moveTo(px, py); x.lineTo(px + (rnd() - 0.5) * gr * 2, py + (rnd() - 0.5) * gr * 2);
    x.lineTo(px + (rnd() - 0.5) * gr * 2, py + (rnd() - 0.5) * gr * 2); x.closePath();
    const z = rnd();
    x.fillStyle = z < 0.45 ? `rgba(0,0,0,${0.25 + rnd() * 0.35})` : z < 0.8 ? rgba(HELL, 0.12 + rnd() * 0.22) : rgba(A, 0.25 + rnd() * 0.3);
    x.fill();
  }
  for (let i = 0; i < 150; i++) {
    let px = cx + (rnd() - 0.5) * (rechts - links), py = top + rnd() * (unten - top);
    x.beginPath(); x.moveTo(px, py);
    for (let j = 0; j < 4; j++) {
      const l = (6 + rnd() * 34) * u;
      if (j % 2) px += (rnd() < 0.5 ? -l : l); else py += (rnd() < 0.5 ? -l : l);
      x.lineTo(px, py);
    }
    x.strokeStyle = rgba(GOLD, 0.5 + rnd() * 0.5); x.lineWidth = (1 + rnd() * 1.6) * u; x.stroke();
    x.fillStyle = rgba(HELL, 0.9); x.beginPath(); x.arc(px, py, 2.4 * u, 0, Math.PI * 2); x.fill();
  }
  x.restore();
  // goldener Rand
  x.save();
  x.shadowColor = rgba(GOLD, 0.9); x.shadowBlur = 16 * u;
  const rg = x.createLinearGradient(links, top, rechts, unten);
  rg.addColorStop(0, '#fff1c4'); rg.addColorStop(0.5, '#e2a93e'); rg.addColorStop(1, '#8a5a17');
  x.strokeStyle = rg; x.lineWidth = 4.5 * u; x.lineJoin = 'round'; x.stroke(kreuz);
  x.restore();
  // Tropfen (flüssiges Gold und Farbe)
  const tropfen = (tx, ty, l, b) => {
    const g = x.createLinearGradient(0, ty, 0, ty + l);
    g.addColorStop(0, '#f2c25a'); g.addColorStop(0.6, rnd() < 0.5 ? '#c98a24' : rgba(F, 1)); g.addColorStop(1, rgba(F, 0.9));
    x.fillStyle = g;
    x.beginPath(); x.moveTo(tx - b, ty); x.lineTo(tx - b * 0.55, ty + l); x.arc(tx, ty + l, b * 0.6, Math.PI, 0, true);
    x.lineTo(tx + b, ty); x.closePath(); x.fill();
    x.fillStyle = 'rgba(255,255,255,.6)'; x.beginPath(); x.arc(tx - b * 0.2, ty + l - b * 0.1, b * 0.18, 0, Math.PI * 2); x.fill();
  };
  for (let i = 0; i < 9; i++) tropfen(links + rnd() * (rechts - links), hy + bw / 2 - 2 * u, (14 + Math.pow(rnd(), 2) * 90) * u, (3 + rnd() * 5) * u);
  for (let i = 0; i < 6; i++) tropfen(cx + (rnd() - 0.5) * bw * 0.9, unten - 2 * u, (20 + Math.pow(rnd(), 1.5) * 130) * u, (3.5 + rnd() * 6) * u);

  // ---------- Lichtexplosion in der Mitte ----------
  x.globalCompositeOperation = 'lighter';
  fleck(cx, hy, k * 0.32, GOLD, 0.55);
  fleck(cx, hy, k * 0.12, HELL, 0.95);
  const strahl = (wink, l, b, a) => {
    x.save(); x.translate(cx, hy); x.rotate(wink);
    const g = x.createLinearGradient(0, 0, l, 0);
    g.addColorStop(0, `rgba(255,250,235,${a})`); g.addColorStop(0.4, rgba(GOLD, a * 0.6)); g.addColorStop(1, rgba(GOLD, 0));
    x.fillStyle = g; x.beginPath(); x.moveTo(0, -b); x.lineTo(l, 0); x.lineTo(0, b); x.closePath(); x.fill();
    x.restore();
  };
  for (let i = 0; i < 4; i++) strahl(i * Math.PI / 2, k * 0.5, 7 * u, 1);
  for (let i = 0; i < 4; i++) strahl(Math.PI / 4 + i * Math.PI / 2, k * 0.24, 4 * u, 0.9);
  for (let i = 0; i < 26; i++) strahl(rnd() * Math.PI * 2, k * (0.08 + rnd() * 0.3), (1 + rnd() * 2.5) * u, 0.7);
  // Funken obenauf
  funken(1400, 0.75, 2.4);
  x.globalCompositeOperation = 'source-over';
}

// Text und Grafik der Vorderseite als HTML-Baustein.
// a: { farbe, akzent, band, zeile } · W/H: Größe der Fläche in CSS-Pixeln · rect: sichtbares Cover darin · dpr: Pixel je CSS-Pixel
export function vorderseite(a, { W, H, rect, dpr, schrift }) {
  const r = rect, w = r.w;
  const css = `
@font-face{font-family:Anton;src:url('${schrift('Anton-Regular.ttf')}')}
.vs{position:absolute;inset:0;overflow:hidden;background:#000}
.vs canvas{position:absolute;left:0;top:0;width:${W}px;height:${H}px}
.vs .t{position:absolute;left:${r.x}px;width:${w}px;text-align:center}
.vs .titel{top:${r.y + r.h * 0.03}px;font-family:Anton;line-height:.92;color:#fff;white-space:nowrap;
  -webkit-text-stroke:${w * 0.006}px #d9a944;paint-order:stroke fill;
  filter:drop-shadow(0 0 ${w * 0.02}px rgba(${a.farbe.join(',')},.35))}
.vs .unter{font-family:Inter;font-weight:800;font-size:${w * 0.036}px;letter-spacing:.42em;padding-left:.42em;color:#e9c46e;white-space:nowrap}
.vs .unten{bottom:${H - r.y - r.h + r.h * 0.035}px}
.vs .pille{display:inline-block;font-family:Inter;font-weight:800;font-size:${w * 0.026}px;letter-spacing:.3em;
  padding:${w * 0.008}px ${w * 0.022}px ${w * 0.008}px calc(${w * 0.022}px + .3em);text-transform:uppercase;color:#120c04;
  background:linear-gradient(180deg,#f6dc98,#c9973f);border-radius:999px}
.vs .zeile{margin-top:${w * 0.012}px;font-family:Inter;font-weight:600;font-size:${w * 0.03}px;letter-spacing:.05em;color:#f1e6cf}
.vs .motto{margin-top:${w * 0.03}px;font-family:Inter;font-weight:800;font-size:${w * 0.034}px;letter-spacing:.16em;padding-left:.16em;color:#fff}`;
  const html = `<div class="vs"><canvas width="${Math.round(W * dpr)}" height="${Math.round(H * dpr)}"></canvas>
<div class="t titel"><span>DIE BIBEL</span></div>
<div class="t unter">IN LEICHTER SPRACHE</div>
<div class="t unten"><div class="pille">${a.band}</div><div class="zeile">${a.zeile}</div><div class="motto">KI-ERKLÄRT. EINFACH. KLAR.</div></div></div>`;
  const script = `<script>
${zeichne.toString()}
document.fonts.ready.then(() => {
  const t = document.querySelector('.vs .titel');
  t.style.fontSize = '100px';
  const groesse = 100 * ${w * 0.92} / t.firstChild.offsetWidth;
  t.style.fontSize = groesse + 'px';
  const unten = t.offsetTop + t.offsetHeight;
  document.querySelector('.vs .unter').style.top = (unten + ${w * 0.012}) + 'px';
  const frei = (unten + ${w * 0.07} - ${r.y}) / ${r.h};
  zeichne(document.querySelector('.vs canvas'), { farbe: ${JSON.stringify(a.farbe)}, akzent: ${JSON.stringify(a.akzent)},
    rect: { x: ${r.x * dpr}, y: ${r.y * dpr}, w: ${r.w * dpr}, h: ${r.h * dpr} }, frei, seed: 20260 });
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
