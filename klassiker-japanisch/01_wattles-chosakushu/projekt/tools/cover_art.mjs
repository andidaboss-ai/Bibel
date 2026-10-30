// Cover art for the annotated classics: night sky in the book's theme colour, gold line art, one emblem per book.
// All shapes are drawn here (SVG), nothing is taken from other editions.
import path from 'path';
import { fileURLToPath } from 'url';

const here = path.dirname(fileURLToPath(import.meta.url));
export const font = (f) => 'file://' + path.join(here, '..', 'fonts', f);

export const fontFaces = () => `
@font-face{font-family:CG;font-weight:400;src:url('${font('CG-Regular.ttf')}')}
@font-face{font-family:CG;font-weight:500;src:url('${font('CG-Medium.ttf')}')}
@font-face{font-family:CG;font-weight:600;src:url('${font('CG-SemiBold.ttf')}')}
@font-face{font-family:CG;font-style:italic;font-weight:400;src:url('${font('CG-Italic.ttf')}')}
@font-face{font-family:CG;font-style:italic;font-weight:500;src:url('${font('CG-MediumItalic.ttf')}')}
@font-face{font-family:Jost;font-weight:300;src:url('${font('Jost-Light.ttf')}')}
@font-face{font-family:Jost;font-weight:400;src:url('${font('Jost-Regular.ttf')}')}
@font-face{font-family:Jost;font-weight:500;src:url('${font('Jost-Medium.ttf')}')}` + cjkFaces();

// Japanese edition: kana/kanji from the system Noto CJK JP fonts (embedded in the PDF), Latin keeps CG/Jost.
import fs from 'fs';
const LANG = JSON.parse(fs.readFileSync(path.join(here, '..', 'book.json'), 'utf8')).lang || '';
const CJK = 'U+2015,U+2025-2026,U+3000-303F,U+3040-30FF,U+3400-4DBF,U+4E00-9FFF,U+F900-FAFF,U+FF01-FF60,U+FFE0-FFEF';
function cjkFaces() {
  if (!LANG.startsWith('ja')) return '';
  let css = '';
  const faces = [['CG', 'normal', [400, 500, 600]], ['CG', 'italic', [400, 500]], ['Jost', 'normal', [300, 400, 500]]];
  for (const [fam, st, ws] of faces)
    for (const w of ws)
      css += `@font-face{font-family:${fam};font-style:${st};font-weight:${w};src:url('${font(fam === 'Jost' ? 'NotoSansJP-Regular.ttf' : w >= 600 ? 'NotoSerifJP-Bold.ttf' : 'NotoSerifJP-Regular.ttf')}');unicode-range:${CJK}}`;
  return css;
}

// Deterministic pseudo-random numbers, so every build gives the same star field
function rng(seed) { let s = seed; return () => (s = (s * 16807) % 2147483647) / 2147483647; }

export function stars(w, h, n, seed, avoid) {
  const r = rng(seed); let out = '';
  for (let i = 0; i < n; i++) {
    const x = r() * w, y = r() * h, big = r();
    if (avoid && avoid(x, y)) continue;
    const rad = big > 0.97 ? 2.6 : big > 0.85 ? 1.6 : 0.9;
    const op = (0.35 + r() * 0.65).toFixed(2);
    out += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${rad}" fill="${big > 0.9 ? '#f3d9a4' : '#ffffff'}" opacity="${op}"/>`;
  }
  return out;
}

// Four-pointed sparkle
export const sparkle = (x, y, s, fill = 'url(#gold)', op = 1) =>
  `<path d="M${x} ${y - s} C${x + s * 0.12} ${y - s * 0.12} ${x + s * 0.12} ${y - s * 0.12} ${x + s} ${y} C${x + s * 0.12} ${y + s * 0.12} ${x + s * 0.12} ${y + s * 0.12} ${x} ${y + s} C${x - s * 0.12} ${y + s * 0.12} ${x - s * 0.12} ${y + s * 0.12} ${x - s} ${y} C${x - s * 0.12} ${y - s * 0.12} ${x - s * 0.12} ${y - s * 0.12} ${x} ${y - s}Z" fill="${fill}" opacity="${op}"/>`;

export const defs = (sky = ['#3a2a6e', '#1d1846', '#0a0b1f']) => `
<defs>
  <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#fff1c9"/><stop offset=".35" stop-color="#e2b866"/>
    <stop offset=".6" stop-color="#b8863b"/><stop offset="1" stop-color="#f6dc9c"/>
  </linearGradient>
  <linearGradient id="goldv" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff3d1"/><stop offset=".5" stop-color="#e0b462"/><stop offset="1" stop-color="#b07f35"/>
  </linearGradient>
  <radialGradient id="sky" cx=".5" cy=".46" r=".75">
    <stop offset="0" stop-color="${sky[0]}"/><stop offset=".45" stop-color="${sky[1]}"/><stop offset="1" stop-color="${sky[2]}"/>
  </radialGradient>
  <radialGradient id="glow" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#ffe9b0" stop-opacity=".95"/><stop offset=".25" stop-color="#f5c76e" stop-opacity=".45"/>
    <stop offset="1" stop-color="#f5c76e" stop-opacity="0"/>
  </radialGradient>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>`;

// The central emblem: rings of a halo, a wand rising diagonally, a star burst at its tip, a trail of sparkles.
export function wand(cx, cy, R) {
  let s = '';
  // halo rings
  s += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="url(#gold)" stroke-width="2.2" opacity=".85"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 0.93}" fill="none" stroke="url(#gold)" stroke-width="1" opacity=".55"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 1.12}" fill="none" stroke="url(#gold)" stroke-width="0.8" opacity=".35" stroke-dasharray="2 10"/>`;
  // twelve tick rays around the ring
  for (let i = 0; i < 24; i++) {
    const a = (i / 24) * Math.PI * 2, l = i % 2 ? 0.035 : 0.07;
    const x1 = cx + Math.cos(a) * R * 1.02, y1 = cy + Math.sin(a) * R * 1.02;
    const x2 = cx + Math.cos(a) * R * (1.02 + l), y2 = cy + Math.sin(a) * R * (1.02 + l);
    s += `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="url(#gold)" stroke-width="1.6" opacity=".7"/>`;
  }
  // wand: from lower left to the star point upper right
  const tx = cx + R * 0.22, ty = cy - R * 0.3;           // tip
  const bx = cx - R * 0.55, by = cy + R * 0.78;          // end of handle
  const dx = tx - bx, dy = ty - by, L = Math.hypot(dx, dy), nx = -dy / L, ny = dx / L;
  const w1 = R * 0.028, w2 = R * 0.012;
  s += `<path d="M${bx + nx * w1} ${by + ny * w1} L${tx + nx * w2} ${ty + ny * w2} L${tx - nx * w2} ${ty - ny * w2} L${bx - nx * w1} ${by - ny * w1} Z" fill="url(#goldv)"/>`;
  // grip bands
  for (const t of [0.08, 0.13, 0.18]) {
    const px = bx + dx * t, py = by + dy * t, ww = w1 * 1.6;
    s += `<line x1="${px + nx * ww}" y1="${py + ny * ww}" x2="${px - nx * ww}" y2="${py - ny * ww}" stroke="#fff1c9" stroke-width="2"/>`;
  }
  // glow + star burst at the tip
  s += `<circle cx="${tx}" cy="${ty}" r="${R * 0.55}" fill="url(#glow)"/>`;
  for (let i = 0; i < 16; i++) {
    const a = (i / 16) * Math.PI * 2 + 0.2, l = R * (i % 2 ? 0.16 : 0.32);
    s += `<line x1="${tx}" y1="${ty}" x2="${(tx + Math.cos(a) * l).toFixed(1)}" y2="${(ty + Math.sin(a) * l).toFixed(1)}" stroke="#fff4d6" stroke-width="${i % 2 ? 1.2 : 2}" opacity=".8"/>`;
  }
  s += sparkle(tx, ty, R * 0.2, '#fffaf0');
  s += sparkle(tx, ty, R * 0.11, 'url(#gold)');
  // trail of sparkles: an arc from the tip sweeping up and over, like the spoken word going out
  for (let i = 1; i <= 18; i++) {
    const t = i / 18, a = -1.25 - t * 2.2, rr = R * (0.42 + t * 0.38);
    const x = tx - R * 0.12 + Math.cos(a) * rr, y = ty + R * 0.25 + Math.sin(a) * rr * 0.8;
    s += sparkle(x, y, R * (0.055 - t * 0.032), i % 3 ? 'url(#gold)' : '#fff4d6', (1 - t * 0.55).toFixed(2));
  }
  return s;
}

// Radiance: an inner sun with long and short rays, three orbits with small "forces" travelling on them.
export function radiance(cx, cy, R) {
  let s = '';
  s += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="url(#gold)" stroke-width="2.2" opacity=".85"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 0.93}" fill="none" stroke="url(#gold)" stroke-width="1" opacity=".5"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 1.12}" fill="none" stroke="url(#gold)" stroke-width="0.8" opacity=".35" stroke-dasharray="2 10"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 0.75}" fill="url(#glow)"/>`;
  // rays
  for (let i = 0; i < 48; i++) {
    const a = (i / 48) * Math.PI * 2, long = i % 4 === 0, mid = i % 2 === 0;
    const r1 = R * 0.2, r2 = R * (long ? 0.86 : mid ? 0.6 : 0.42);
    s += `<line x1="${(cx + Math.cos(a) * r1).toFixed(1)}" y1="${(cy + Math.sin(a) * r1).toFixed(1)}" x2="${(cx + Math.cos(a) * r2).toFixed(1)}" y2="${(cy + Math.sin(a) * r2).toFixed(1)}" stroke="url(#gold)" stroke-width="${long ? 2.4 : mid ? 1.4 : 0.9}" opacity="${long ? 0.95 : 0.7}" stroke-linecap="round"/>`;
  }
  // orbits (tilted ellipses) with a small sphere on each
  const orbits = [[0.78, 0.3, -25, 0.35], [0.78, 0.3, 35, 2.2], [0.78, 0.3, 95, 4.1]];
  for (const [rx, ry, rot, t] of orbits) {
    s += `<ellipse cx="${cx}" cy="${cy}" rx="${R * rx}" ry="${R * ry}" fill="none" stroke="#f6dfa6" stroke-width="1.3" opacity=".65" transform="rotate(${rot} ${cx} ${cy})"/>`;
    const ang = rot * Math.PI / 180, ex = Math.cos(t) * R * rx, ey = Math.sin(t) * R * ry;
    const px = cx + ex * Math.cos(ang) - ey * Math.sin(ang), py = cy + ex * Math.sin(ang) + ey * Math.cos(ang);
    s += `<circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="${R * 0.035}" fill="#fff4d6"/>`;
    s += `<circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="${R * 0.08}" fill="url(#glow)"/>`;
  }
  // core
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 0.17}" fill="none" stroke="url(#gold)" stroke-width="2"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 0.11}" fill="url(#gold)"/>`;
  s += sparkle(cx, cy, R * 0.16, '#fffaf0', 0.95);
  return s;
}

// Vibration: thought-waves going out from one centre and meeting a second, smaller centre ("like attracts like").
export function vibration(cx, cy, R) {
  let s = '';
  s += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="url(#gold)" stroke-width="2.2" opacity=".85"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 0.93}" fill="none" stroke="url(#gold)" stroke-width="1" opacity=".5"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 1.12}" fill="none" stroke="url(#gold)" stroke-width="0.8" opacity=".35" stroke-dasharray="2 10"/>`;
  s += `<clipPath id="inner"><circle cx="${cx}" cy="${cy}" r="${R * 0.9}"/></clipPath><g clip-path="url(#inner)">`;
  const ax = cx - R * 0.34, ay = cy + R * 0.16, bx = cx + R * 0.42, by = cy - R * 0.22;
  for (let i = 1; i <= 9; i++) {
    s += `<circle cx="${ax}" cy="${ay}" r="${R * 0.09 * i}" fill="none" stroke="url(#gold)" stroke-width="${(1.9 - i * 0.12).toFixed(2)}" opacity="${(1 - i * 0.08).toFixed(2)}"/>`;
  }
  for (let i = 1; i <= 5; i++) {
    s += `<circle cx="${bx}" cy="${by}" r="${R * 0.07 * i}" fill="none" stroke="#f6dfa6" stroke-width="1.1" opacity="${(0.85 - i * 0.12).toFixed(2)}"/>`;
  }
  // a fine wave line joining the two centres
  let d = `M${ax} ${ay}`; const n = 60;
  for (let k = 1; k <= n; k++) {
    const t = k / n, x = ax + (bx - ax) * t, y = ay + (by - ay) * t, nx = -(by - ay), ny = bx - ax, L = Math.hypot(nx, ny);
    const amp = R * 0.05 * Math.sin(t * Math.PI) * Math.sin(t * Math.PI * 9);
    d += ` L${(x + nx / L * amp).toFixed(1)} ${(y + ny / L * amp).toFixed(1)}`;
  }
  s += `<path d="${d}" fill="none" stroke="#fff4d6" stroke-width="1.6" opacity=".9"/></g>`;
  s += `<circle cx="${ax}" cy="${ay}" r="${R * 0.3}" fill="url(#glow)"/><circle cx="${bx}" cy="${by}" r="${R * 0.2}" fill="url(#glow)"/>`;
  s += `<circle cx="${ax}" cy="${ay}" r="${R * 0.05}" fill="url(#gold)"/>` + sparkle(ax, ay, R * 0.11, '#fffaf0');
  s += `<circle cx="${bx}" cy="${by}" r="${R * 0.035}" fill="url(#gold)"/>` + sparkle(bx, by, R * 0.07, '#fffaf0');
  return s;
}

// Crystal: a thought taking form — light rays converge from above into a faceted gold crystal.
export function crystal(cx, cy, R) {
  let s = '';
  s += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="url(#gold)" stroke-width="2.2" opacity=".85"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 0.93}" fill="none" stroke="url(#gold)" stroke-width="1" opacity=".5"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 1.12}" fill="none" stroke="url(#gold)" stroke-width="0.8" opacity=".35" stroke-dasharray="2 10"/>`;
  s += `<circle cx="${cx}" cy="${cy + R * 0.05}" r="${R * 0.62}" fill="url(#glow)" opacity=".8"/>`;
  // faceted crystal: top point, girdle of 4 visible corners, bottom point (an elongated octahedron in perspective)
  const T = [cx, cy - R * 0.62], Bt = [cx, cy + R * 0.66];
  const g = [[cx - R * 0.4, cy - R * 0.02], [cx - R * 0.12, cy + R * 0.12], [cx + R * 0.18, cy + R * 0.1], [cx + R * 0.4, cy - R * 0.04], [cx + R * 0.1, cy - R * 0.14]];
  const P = (p) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`;
  const faces = [[T, g[0], g[1], 0.62], [T, g[1], g[2], 0.95], [T, g[2], g[3], 0.72], [Bt, g[0], g[1], 0.38], [Bt, g[1], g[2], 0.55], [Bt, g[2], g[3], 0.3]];
  for (const [a, b, c, op] of faces) s += `<path d="M${P(a)} L${P(b)} L${P(c)} Z" fill="url(#gold)" opacity="${op}" stroke="#fff6dc" stroke-width="1.8" stroke-linejoin="round"/>`;
  s += `<path d="M${P(T)} L${P(g[4])} L${P(g[0])} M${P(g[4])} L${P(g[3])}" fill="none" stroke="#f6dfa6" stroke-width="0.9" opacity=".55" stroke-dasharray="3 4"/>`;
  // rays from above converging on the top point
  for (let i = -5; i <= 5; i++) {
    const x0 = cx + i * R * 0.13, y0 = cy - R * 0.92;
    s += `<line x1="${x0.toFixed(1)}" y1="${y0.toFixed(1)}" x2="${T[0]}" y2="${T[1]}" stroke="#fff4d6" stroke-width="${i % 2 ? 0.8 : 1.3}" opacity="${(0.75 - Math.abs(i) * 0.1).toFixed(2)}"/>`;
  }
  s += sparkle(T[0], T[1], R * 0.12, '#fffaf0');
  // small sparkles around
  [[-0.55, -0.35, 0.05], [0.58, 0.3, 0.045], [-0.42, 0.5, 0.035], [0.5, -0.5, 0.03]].forEach(([dx, dy, r]) => { s += sparkle(cx + dx * R, cy + dy * R, R * r, 'url(#gold)', 0.9); });
  return s;
}

// Laurel: a Roman laurel wreath around a single classical column, with a small rising sun behind it.
export function laurel(cx, cy, R) {
  let s = '';
  s += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="url(#gold)" stroke-width="2.2" opacity=".85"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 0.93}" fill="none" stroke="url(#gold)" stroke-width="1" opacity=".5"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 1.12}" fill="none" stroke="url(#gold)" stroke-width="0.8" opacity=".35" stroke-dasharray="2 10"/>`;
  s += `<circle cx="${cx}" cy="${cy - R * 0.1}" r="${R * 0.55}" fill="url(#glow)" opacity=".7"/>`;
  // sun rays behind the column
  for (let i = 0; i < 13; i++) {
    const a = Math.PI + (i / 12) * Math.PI, r1 = R * 0.26, r2 = R * (i % 2 ? 0.5 : 0.62);
    s += `<line x1="${(cx + Math.cos(a) * r1).toFixed(1)}" y1="${(cy - R * 0.05 + Math.sin(a) * r1).toFixed(1)}" x2="${(cx + Math.cos(a) * r2).toFixed(1)}" y2="${(cy - R * 0.05 + Math.sin(a) * r2).toFixed(1)}" stroke="#f6dfa6" stroke-width="${i % 2 ? 1 : 1.6}" opacity=".7"/>`;
  }
  // column: capital, shaft with flutes, base
  const w = R * 0.16, top = cy - R * 0.3, bot = cy + R * 0.42;
  s += `<rect x="${cx - w * 1.55}" y="${top - R * 0.06}" width="${w * 3.1}" height="${R * 0.05}" fill="url(#gold)"/>`;
  s += `<path d="M${cx - w * 1.3} ${top - R * 0.01} Q${cx - w * 1.6} ${top + R * 0.05} ${cx - w * 1.05} ${top + R * 0.06} L${cx + w * 1.05} ${top + R * 0.06} Q${cx + w * 1.6} ${top + R * 0.05} ${cx + w * 1.3} ${top - R * 0.01} Z" fill="url(#gold)" opacity=".9"/>`;
  s += `<rect x="${cx - w}" y="${top + R * 0.06}" width="${w * 2}" height="${bot - top - R * 0.1}" fill="url(#goldv)"/>`;
  for (let k = -2; k <= 2; k++) s += `<line x1="${cx + k * w * 0.36}" y1="${top + R * 0.08}" x2="${cx + k * w * 0.36}" y2="${bot - R * 0.06}" stroke="#7a5a26" stroke-width="1" opacity=".55"/>`;
  s += `<rect x="${cx - w * 1.3}" y="${bot - R * 0.04}" width="${w * 2.6}" height="${R * 0.045}" fill="url(#gold)"/>`;
  s += `<rect x="${cx - w * 1.6}" y="${bot + R * 0.005}" width="${w * 3.2}" height="${R * 0.05}" fill="url(#gold)"/>`;
  // laurel wreath: two branches of leaves curving up both sides
  for (const side of [-1, 1]) {
    for (let i = 0; i < 15; i++) {
      const t = i / 14, a = Math.PI / 2 + side * (0.3 + t * 2.25), rr = R * 0.74;
      const x = cx + Math.cos(a) * rr, y = cy + R * 0.02 + Math.sin(a) * rr;
      const ang = (a * 180 / Math.PI) + (side > 0 ? 90 : -90) + side * 25;
      const L = R * (0.17 - t * 0.05), Wd = L * 0.42;
      s += `<ellipse cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" rx="${(L / 2).toFixed(1)}" ry="${(Wd / 2).toFixed(1)}" transform="rotate(${ang.toFixed(1)} ${x.toFixed(1)} ${y.toFixed(1)})" fill="url(#gold)" opacity="${(0.95 - t * 0.25).toFixed(2)}"/>`;
    }
    for (let i = 0; i < 12; i++) {
      const t = i / 11, a = Math.PI / 2 + side * (0.45 + t * 2.0), rr = R * 0.64;
      const x = cx + Math.cos(a) * rr, y = cy + R * 0.02 + Math.sin(a) * rr;
      const ang = (a * 180 / Math.PI) + (side > 0 ? 90 : -90) - side * 30;
      const L = R * (0.13 - t * 0.04), Wd = L * 0.42;
      s += `<ellipse cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" rx="${(L / 2).toFixed(1)}" ry="${(Wd / 2).toFixed(1)}" transform="rotate(${ang.toFixed(1)} ${x.toFixed(1)} ${y.toFixed(1)})" fill="url(#goldv)" opacity="${(0.85 - t * 0.25).toFixed(2)}"/>`;
    }
  }
  s += sparkle(cx, top - R * 0.14, R * 0.07, '#fffaf0');
  return s;
}

// Way: an open ink-brush circle (enso), mountains, flowing water and a small moon.
export function way(cx, cy, R) {
  let s = '';
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 1.12}" fill="none" stroke="url(#gold)" stroke-width="0.8" opacity=".35" stroke-dasharray="2 10"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 0.7}" fill="url(#glow)" opacity=".45"/>`;
  // enso: a thick open circle, tapering at both ends
  const a0 = -1.25, a1 = 4.55, n = 80; let outer = '', inner = '';
  for (let i = 0; i <= n; i++) {
    const t = i / n, a = a0 + (a1 - a0) * t, w = R * (0.012 + 0.05 * Math.sin(Math.PI * Math.min(1, t * 1.15)));
    outer += `${i ? 'L' : 'M'}${(cx + Math.cos(a) * (R + w)).toFixed(1)} ${(cy + Math.sin(a) * (R + w)).toFixed(1)} `;
    inner = `L${(cx + Math.cos(a) * (R - w)).toFixed(1)} ${(cy + Math.sin(a) * (R - w)).toFixed(1)} ` + inner;
  }
  s += `<path d="${outer}${inner}Z" fill="url(#gold)" opacity=".95"/>`;
  // mountains
  const base = cy + R * 0.18;
  s += `<path d="M${cx - R * 0.72} ${base} L${cx - R * 0.38} ${cy - R * 0.28} L${cx - R * 0.18} ${cy - R * 0.06} L${cx + R * 0.06} ${cy - R * 0.46} L${cx + R * 0.42} ${cy - R * 0.02} L${cx + R * 0.56} ${cy - R * 0.14} L${cx + R * 0.74} ${base}" fill="none" stroke="url(#gold)" stroke-width="2.2" stroke-linejoin="round"/>`;
  s += `<path d="M${cx - R * 0.5} ${base} L${cx - R * 0.3} ${cy - R * 0.12} L${cx - R * 0.08} ${base}" fill="none" stroke="#f6dfa6" stroke-width="1" opacity=".6"/>`;
  // water: three flowing lines
  for (let k = 0; k < 3; k++) {
    const y0 = base + R * (0.13 + k * 0.12), amp = R * 0.025, len = R * (0.62 - k * 0.12); let d = '';
    for (let i = 0; i <= 40; i++) { const x = cx - len + (2 * len) * i / 40; d += `${i ? 'L' : 'M'}${x.toFixed(1)} ${(y0 + Math.sin(i / 40 * Math.PI * 5 + k) * amp).toFixed(1)} `; }
    s += `<path d="${d}" fill="none" stroke="url(#gold)" stroke-width="${1.8 - k * 0.4}" opacity="${(0.9 - k * 0.2).toFixed(2)}"/>`;
  }
  // moon
  s += `<circle cx="${cx + R * 0.36}" cy="${cy - R * 0.52}" r="${R * 0.07}" fill="url(#gold)"/>`;
  s += `<circle cx="${cx + R * 0.36}" cy="${cy - R * 0.52}" r="${R * 0.16}" fill="url(#glow)" opacity=".8"/>`;
  return s;
}


// Lamp: a pointed (gothic) cloister window, inside it a single candle whose flame gives a quiet halo.
export function lamp(cx, cy, R) {
  let s = '';
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 1.12}" fill="none" stroke="url(#gold)" stroke-width="0.8" opacity=".35" stroke-dasharray="2 10"/>`;
  const w = R * 0.62, top = cy - R * 0.98, spring = cy - R * 0.28, foot = cy + R * 0.86;
  const arch = (hw, t, sp, ft) => { const r = ((sp - t) ** 2 + hw * hw * 4) / (4 * hw); return `M${cx - hw} ${ft} L${cx - hw} ${sp} A${r} ${r} 0 0 1 ${cx} ${t} A${r} ${r} 0 0 1 ${cx + hw} ${sp} L${cx + hw} ${ft}`; };
  s += `<path d="${arch(w, top, spring, foot)} Z" fill="#000" opacity=".18"/>`;
  s += `<path d="${arch(w, top, spring, foot)}" fill="none" stroke="url(#gold)" stroke-width="2.4" stroke-linejoin="round"/>`;
  s += `<path d="${arch(w * 0.88, top + R * 0.1, spring, foot - R * 0.02)}" fill="none" stroke="#f6dfa6" stroke-width="1" opacity=".55"/>`;
  // sill
  s += `<rect x="${cx - w * 1.18}" y="${foot - 1.5}" width="${w * 2.36}" height="3.2" rx="1.6" fill="url(#gold)"/>`;
  s += `<rect x="${cx - w * 1.0}" y="${foot + R * 0.05}" width="${w * 2}" height="1.4" fill="url(#gold)" opacity=".6"/>`;
  // candle and holder
  const fy = cy + R * 0.07, ct = cy + R * 0.2, cw = R * 0.075;
  s += `<circle cx="${cx}" cy="${fy}" r="${R * 0.62}" fill="url(#glow)" opacity=".75"/>`;
  for (let i = 0; i < 24; i++) {
    const a = (i / 24) * Math.PI * 2, long = i % 2 === 0, r1 = R * 0.2, r2 = R * (long ? 0.46 : 0.32);
    s += `<line x1="${(cx + Math.cos(a) * r1).toFixed(1)}" y1="${(fy + Math.sin(a) * r1).toFixed(1)}" x2="${(cx + Math.cos(a) * r2).toFixed(1)}" y2="${(fy + Math.sin(a) * r2).toFixed(1)}" stroke="url(#gold)" stroke-width="${long ? 1.4 : 0.8}" opacity="${long ? 0.7 : 0.45}" stroke-linecap="round"/>`;
  }
  s += `<rect x="${cx - cw}" y="${ct}" width="${cw * 2}" height="${R * 0.48}" rx="${cw * 0.3}" fill="url(#goldv)"/>`;
  s += `<path d="M${cx - R * 0.26} ${ct + R * 0.5} Q${cx} ${ct + R * 0.62} ${cx + R * 0.26} ${ct + R * 0.5} Z" fill="url(#gold)"/>`;
  s += `<line x1="${cx}" y1="${ct}" x2="${cx}" y2="${ct - R * 0.04}" stroke="#2a2016" stroke-width="2"/>`;
  // flame
  const fh = R * 0.24;
  s += `<path d="M${cx} ${ct - R * 0.02 - fh} C${cx + R * 0.07} ${ct - fh * 0.5} ${cx + R * 0.06} ${ct - R * 0.03} ${cx} ${ct - R * 0.02} C${cx - R * 0.06} ${ct - R * 0.03} ${cx - R * 0.07} ${ct - fh * 0.5} ${cx} ${ct - R * 0.02 - fh}Z" fill="#fff3d1"/>`;
  s += `<path d="M${cx} ${ct - R * 0.04 - fh * 0.55} C${cx + R * 0.03} ${ct - fh * 0.3} ${cx + R * 0.025} ${ct - R * 0.04} ${cx} ${ct - R * 0.035} C${cx - R * 0.025} ${ct - R * 0.04} ${cx - R * 0.03} ${ct - fh * 0.3} ${cx} ${ct - R * 0.04 - fh * 0.55}Z" fill="#e2b866"/>`;
  s += sparkle(cx, top - R * 0.16, R * 0.07, '#fff4d6', 0.9);
  return s;
}


// Portico: the Stoa — a Greek porch (pediment, architrave, four columns, steps) inside a meander (Greek key) ring.
export function portico(cx, cy, R) {
  let s = '';
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 1.12}" fill="none" stroke="url(#gold)" stroke-width="0.8" opacity=".35" stroke-dasharray="2 10"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="url(#gold)" stroke-width="2.2"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 0.84}" fill="none" stroke="url(#gold)" stroke-width="1.6"/>`;
  // meander band between r=0.86R and 0.98R
  const n = 36, r0 = R * 0.865, r1 = R * 0.975, rm = (r0 + r1) / 2;
  const P = (a, r) => `${(cx + Math.cos(a) * r).toFixed(1)} ${(cy + Math.sin(a) * r).toFixed(1)}`;
  let d = '';
  for (let i = 0; i < n; i++) {
    const a0 = (i / n) * Math.PI * 2 - Math.PI / 2, w = (Math.PI * 2) / n;
    d += `M${P(a0, r0)} L${P(a0, r1)} L${P(a0 + w * 0.75, r1)} L${P(a0 + w * 0.75, rm)} L${P(a0 + w * 0.35, rm)} `;
  }
  s += `<path d="${d}" fill="none" stroke="url(#gold)" stroke-width="1.4" stroke-linejoin="miter" opacity=".9"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 0.62}" fill="url(#glow)" opacity=".35"/>`;
  // temple
  const W = R * 0.56, base = cy + R * 0.42, colTop = cy - R * 0.12, archH = R * 0.07, pedH = R * 0.2;
  const rect = (x, y, w, h, f = 'url(#gold)', o = 1) => `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${w.toFixed(1)}" height="${h.toFixed(1)}" fill="${f}" opacity="${o}"/>`;
  // steps
  s += rect(cx - W * 1.12, base, W * 2.24, R * 0.035);
  s += rect(cx - W * 1.2, base + R * 0.05, W * 2.4, R * 0.035, 'url(#gold)', 0.8);
  s += rect(cx - W * 1.28, base + R * 0.1, W * 2.56, R * 0.035, 'url(#gold)', 0.6);
  // columns with capitals
  const cols = 4, cw = R * 0.07;
  for (let k = 0; k < cols; k++) {
    const x = cx - W * 0.86 + (k * (W * 1.72)) / (cols - 1);
    s += rect(x - cw / 2, colTop + R * 0.03, cw, base - colTop - R * 0.03, 'url(#goldv)');
    for (let f = 1; f < 3; f++) s += `<rect x="${(x - cw / 2 + f * cw / 3 - 0.6).toFixed(1)}" y="${(colTop + R * 0.04).toFixed(1)}" width="1.2" height="${(base - colTop - R * 0.06).toFixed(1)}" fill="#3a2a16" opacity=".35"/>`;
    s += rect(x - cw * 0.85, colTop, cw * 1.7, R * 0.03);
  }
  // architrave and pediment
  s += rect(cx - W * 1.04, colTop - archH, W * 2.08, archH * 0.8);
  s += `<path d="M${cx - W * 1.12} ${colTop - archH - R * 0.012} L${cx} ${colTop - archH - pedH} L${cx + W * 1.12} ${colTop - archH - R * 0.012} Z" fill="none" stroke="url(#gold)" stroke-width="2.4" stroke-linejoin="miter"/>`;
  s += `<circle cx="${cx}" cy="${colTop - archH - pedH * 0.42}" r="${R * 0.035}" fill="url(#gold)"/>`;
  s += sparkle(cx, colTop - archH - pedH - R * 0.13, R * 0.06, '#fff4d6', 0.9);
  return s;
}


// Cross: a slender Latin cross with flared ends in a ring of light, standing on an open book.
export function cross(cx, cy, R) {
  let s = '';
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 1.12}" fill="none" stroke="url(#gold)" stroke-width="0.8" opacity=".35" stroke-dasharray="2 10"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="url(#gold)" stroke-width="2.2" opacity=".9"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 0.94}" fill="none" stroke="url(#gold)" stroke-width="0.9" opacity=".5"/>`;
  const hy = cy - R * 0.2;
  s += `<circle cx="${cx}" cy="${hy}" r="${R * 0.6}" fill="url(#glow)" opacity=".7"/>`;
  for (let i = 0; i < 64; i++) {
    const a = (i / 64) * Math.PI * 2, long = i % 4 === 0, r1 = R * 0.3, r2 = R * (long ? 0.86 : i % 2 ? 0.55 : 0.68);
    const x2 = cx + Math.cos(a) * r2, y2 = hy + Math.sin(a) * r2;
    if (Math.hypot(x2 - cx, y2 - cy) > R * 0.9) continue;
    s += `<line x1="${(cx + Math.cos(a) * r1).toFixed(1)}" y1="${(hy + Math.sin(a) * r1).toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="url(#gold)" stroke-width="${long ? 1.6 : 0.8}" opacity="${long ? 0.75 : 0.45}" stroke-linecap="round"/>`;
  }
  // cross with flared (pattée-like) ends
  const w = R * 0.045, top = cy - R * 0.72, bot = cy + R * 0.42, arm = R * 0.36, ay = cy - R * 0.3, f = R * 0.035;
  const d = `M${cx - w} ${top + f} L${cx - w - f} ${top} L${cx + w + f} ${top} L${cx + w} ${top + f}
    L${cx + w} ${ay - w} L${cx + arm - f} ${ay - w} L${cx + arm} ${ay - w - f} L${cx + arm} ${ay + w + f} L${cx + arm - f} ${ay + w}
    L${cx + w} ${ay + w} L${cx + w} ${bot - f} L${cx + w + f} ${bot} L${cx - w - f} ${bot} L${cx - w} ${bot - f}
    L${cx - w} ${ay + w} L${cx - arm + f} ${ay + w} L${cx - arm} ${ay + w + f} L${cx - arm} ${ay - w - f} L${cx - arm + f} ${ay - w} L${cx - w} ${ay - w} Z`;
  s += `<path d="${d}" fill="url(#goldv)"/>`;
  s += `<path d="${d}" fill="none" stroke="#fff3d1" stroke-width="0.8" opacity=".5"/>`;
  // open book
  const by = cy + R * 0.5, bw = R * 0.46, bh = R * 0.16;
  s += `<path d="M${cx} ${by} Q${cx - bw * 0.45} ${by - bh * 0.55} ${cx - bw} ${by - bh * 0.25} L${cx - bw} ${by + bh * 0.55} Q${cx - bw * 0.45} ${by + bh * 0.25} ${cx} ${by + bh * 0.8} Z" fill="url(#gold)" opacity=".95"/>`;
  s += `<path d="M${cx} ${by} Q${cx + bw * 0.45} ${by - bh * 0.55} ${cx + bw} ${by - bh * 0.25} L${cx + bw} ${by + bh * 0.55} Q${cx + bw * 0.45} ${by + bh * 0.25} ${cx} ${by + bh * 0.8} Z" fill="url(#gold)" opacity=".95"/>`;
  for (let k = 1; k <= 3; k++) {
    const yy = by + bh * (0.05 + k * 0.14);
    s += `<path d="M${cx - bw * 0.12} ${yy} Q${cx - bw * 0.5} ${yy - bh * 0.42} ${cx - bw * 0.88} ${yy - bh * 0.18}" fill="none" stroke="#3a2412" stroke-width="1" opacity=".45"/>`;
    s += `<path d="M${cx + bw * 0.12} ${yy} Q${cx + bw * 0.5} ${yy - bh * 0.42} ${cx + bw * 0.88} ${yy - bh * 0.18}" fill="none" stroke="#3a2412" stroke-width="1" opacity=".45"/>`;
  }
  return s;
}


// Seed: "the mind is like a garden" — a seed in the soil, roots below, a young plant with paired leaves rising to a small sun.
export function seed(cx, cy, R) {
  let s = '';
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 1.12}" fill="none" stroke="url(#gold)" stroke-width="0.8" opacity=".35" stroke-dasharray="2 10"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="url(#gold)" stroke-width="2.2" opacity=".9"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 0.94}" fill="none" stroke="url(#gold)" stroke-width="0.9" opacity=".5"/>`;
  const gy = cy + R * 0.3;
  // sun and glow
  s += `<circle cx="${cx}" cy="${cy - R * 0.52}" r="${R * 0.5}" fill="url(#glow)" opacity=".55"/>`;
  s += `<circle cx="${cx}" cy="${cy - R * 0.62}" r="${R * 0.07}" fill="url(#gold)"/>`;
  for (let i = 0; i < 16; i++) {
    const a = (i / 16) * Math.PI * 2, r1 = R * 0.11, r2 = R * (i % 2 ? 0.17 : 0.22);
    s += `<line x1="${(cx + Math.cos(a) * r1).toFixed(1)}" y1="${(cy - R * 0.62 + Math.sin(a) * r1).toFixed(1)}" x2="${(cx + Math.cos(a) * r2).toFixed(1)}" y2="${(cy - R * 0.62 + Math.sin(a) * r2).toFixed(1)}" stroke="url(#gold)" stroke-width="1.3" stroke-linecap="round" opacity=".8"/>`;
  }
  // ground (chord across the circle) and soil lines
  const hw = Math.sqrt(R * R * 0.88 - (gy - cy) ** 2);
  s += `<rect x="${cx - hw}" y="${gy - 1.4}" width="${hw * 2}" height="2.8" fill="url(#gold)"/>`;
  for (let k = 1; k <= 3; k++) {
    const y = gy + R * 0.09 * k, w = Math.sqrt(Math.max(0, R * R * 0.8 - (y - cy) ** 2)) * (1 - k * 0.12);
    s += `<rect x="${cx - w}" y="${y}" width="${w * 2}" height="1" fill="url(#gold)" opacity="${0.45 - k * 0.1}"/>`;
  }
  // seed and roots
  s += `<ellipse cx="${cx}" cy="${gy + R * 0.1}" rx="${R * 0.07}" ry="${R * 0.045}" fill="url(#gold)" transform="rotate(-18 ${cx} ${gy + R * 0.1})"/>`;
  const roots = [[-0.32, 0.42], [-0.16, 0.5], [0.02, 0.55], [0.18, 0.48], [0.34, 0.4]];
  for (const [dx, dy] of roots) s += `<path d="M${cx} ${gy + R * 0.12} Q${cx + R * dx * 0.4} ${gy + R * dy * 0.6} ${cx + R * dx} ${gy + R * dy}" fill="none" stroke="url(#gold)" stroke-width="1.2" opacity=".6" stroke-linecap="round"/>`;
  // stem
  const top = cy - R * 0.32;
  s += `<path d="M${cx} ${gy + R * 0.06} C${cx - R * 0.05} ${gy - R * 0.2} ${cx + R * 0.05} ${top + R * 0.25} ${cx} ${top}" fill="none" stroke="url(#goldv)" stroke-width="3.2" stroke-linecap="round"/>`;
  // leaves (pairs), growing larger towards the middle
  const leaf = (x, y, L, ang) => { const a = ang * Math.PI / 180, ex = x + Math.cos(a) * L, ey = y + Math.sin(a) * L, nx = -Math.sin(a) * L * 0.32, ny = Math.cos(a) * L * 0.32, mx = (x + ex) / 2, my = (y + ey) / 2;
    return `<path d="M${x} ${y} Q${mx + nx} ${my + ny} ${ex} ${ey} Q${mx - nx} ${my - ny} ${x} ${y} Z" fill="url(#gold)" opacity=".95"/><path d="M${x} ${y} L${(x + ex * 0.9) / 1.9} ${(y + ey * 0.9) / 1.9}" stroke="#2a2014" stroke-width="0.8" opacity=".4"/>`; };
  const pairs = [[0.12, 0.2], [0.32, 0.28], [0.52, 0.22]];
  pairs.forEach(([t, L], i) => { const y = gy - (gy - top) * (t + 0.05);
    s += leaf(cx, y, R * L, 200 + i * 8) + leaf(cx, y, R * L, -20 - i * 8); });
  s += leaf(cx, top + 2, R * 0.13, -90);
  return s;
}


// Ascent (epic): a rising sun whose long rays reach far beyond the ring, layered mountains, and a path of light
// winding up to the summit — "the advancing life": getting rich, being well, being great.
export function ascent(cx, cy, R) {
  let s = '';
  const sy = cy - R * 0.08;
  // long rays far beyond the emblem
  for (let i = 0; i < 72; i++) {
    const a = Math.PI + (i / 71) * Math.PI, long = i % 3 === 0, r1 = R * 0.34, r2 = R * (long ? 2.6 : 1.55);
    s += `<line x1="${(cx + Math.cos(a) * r1).toFixed(1)}" y1="${(sy + Math.sin(a) * r1).toFixed(1)}" x2="${(cx + Math.cos(a) * r2).toFixed(1)}" y2="${(sy + Math.sin(a) * r2).toFixed(1)}" stroke="url(#gold)" stroke-width="${long ? 1.6 : 0.7}" opacity="${long ? 0.42 : 0.22}" stroke-linecap="round"/>`;
  }
  s += `<circle cx="${cx}" cy="${sy}" r="${R * 1.5}" fill="url(#glow)" opacity=".38"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 1.12}" fill="none" stroke="url(#gold)" stroke-width="0.8" opacity=".35" stroke-dasharray="2 10"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="url(#gold)" stroke-width="2.6"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 0.95}" fill="none" stroke="url(#gold)" stroke-width="1" opacity=".55"/>`;
  s += `<clipPath id="disc"><circle cx="${cx}" cy="${cy}" r="${R * 0.93}"/></clipPath><g clip-path="url(#disc)">`;
  // sun
  s += `<circle cx="${cx}" cy="${sy}" r="${R * 0.62}" fill="url(#glow)" opacity=".95"/>`;
  s += `<circle cx="${cx}" cy="${sy}" r="${R * 0.24}" fill="url(#gold)"/>`;
  s += `<circle cx="${cx}" cy="${sy}" r="${R * 0.3}" fill="none" stroke="url(#gold)" stroke-width="1.4" opacity=".7"/>`;
  for (let i = 0; i < 36; i++) { const a = (i / 36) * Math.PI * 2, r1 = R * 0.33, r2 = R * (i % 2 ? 0.46 : 0.6);
    s += `<line x1="${(cx + Math.cos(a) * r1).toFixed(1)}" y1="${(sy + Math.sin(a) * r1).toFixed(1)}" x2="${(cx + Math.cos(a) * r2).toFixed(1)}" y2="${(sy + Math.sin(a) * r2).toFixed(1)}" stroke="url(#gold)" stroke-width="${i % 2 ? 1 : 2}" opacity=".85" stroke-linecap="round"/>`; }
  // mountain ranges (back to front)
  const ridge = (pts, fill, op, stroke) => { let d = `M${cx - R} ${cy + R}`; for (const [x, y] of pts) d += ` L${cx + R * x} ${cy + R * y}`; d += ` L${cx + R} ${cy + R} Z`;
    return `<path d="${d}" fill="${fill}" opacity="${op}"/>` + (stroke ? `<path d="M${pts.map(([x, y]) => `${cx + R * x} ${cy + R * y}`).join(' L')}" fill="none" stroke="url(#gold)" stroke-width="${stroke}" stroke-linejoin="round"/>` : ''); };
  s += ridge([[-1, 0.28], [-0.7, 0.12], [-0.48, 0.2], [-0.22, -0.02], [0, 0.14], [0.26, 0.0], [0.5, 0.16], [0.75, 0.06], [1, 0.22]], '#000', 0.35, 1.2);
  s += ridge([[-1, 0.42], [-0.62, 0.3], [-0.34, 0.38], [-0.1, 0.18], [0.08, 0.3], [0.38, 0.16], [0.66, 0.34], [1, 0.3]], '#000', 0.55, 1.8);
  s += ridge([[-1, 0.62], [-0.55, 0.5], [-0.2, 0.6], [0.18, 0.46], [0.55, 0.58], [1, 0.5]], '#000', 0.8, 2.2);
  // path of light winding up to the summit of the middle range
  let d = ''; const pts = [[0.02, 0.98], [-0.18, 0.84], [0.12, 0.72], [-0.06, 0.6], [0.06, 0.48], [-0.02, 0.36], [0.0, 0.2]];
  pts.forEach(([x, y], i) => { d += (i ? ' T' : 'M') + `${cx + R * x} ${cy + R * y}`; });
  s += `<path d="${d}" fill="none" stroke="url(#gold)" stroke-width="3" stroke-linecap="round" opacity=".95"/>`;
  s += `<path d="${d}" fill="none" stroke="#fff3d1" stroke-width="1" stroke-linecap="round" opacity=".7"/>`;
  s += `</g>`;
  s += sparkle(cx, cy - R * 1.2, R * 0.08, '#fff4d6', 0.95);
  return s;
}

export const emblems = { ascent, wand, radiance, vibration, crystal, laurel, way, lamp, portico, cross, seed };
export const emblem = (name, cx, cy, R) => (emblems[name] || wand)(cx, cy, R);
