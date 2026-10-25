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
@font-face{font-family:Jost;font-weight:500;src:url('${font('Jost-Medium.ttf')}')}`;

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

export const emblems = { wand, radiance, vibration, crystal, laurel, way };
export const emblem = (name, cx, cy, R) => (emblems[name] || wand)(cx, cy, R);
