// Cover art for "Your Word Is Your Wand (Annotated)": deep night sky, gold line art, a wand with a star burst.
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

export const defs = () => `
<defs>
  <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#fff1c9"/><stop offset=".35" stop-color="#e2b866"/>
    <stop offset=".6" stop-color="#b8863b"/><stop offset="1" stop-color="#f6dc9c"/>
  </linearGradient>
  <linearGradient id="goldv" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff3d1"/><stop offset=".5" stop-color="#e0b462"/><stop offset="1" stop-color="#b07f35"/>
  </linearGradient>
  <radialGradient id="sky" cx=".5" cy=".46" r=".75">
    <stop offset="0" stop-color="#3a2a6e"/><stop offset=".45" stop-color="#1d1846"/><stop offset="1" stop-color="#0a0b1f"/>
  </radialGradient>
  <radialGradient id="glow" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#ffe9b0" stop-opacity=".95"/><stop offset=".25" stop-color="#f5c76e" stop-opacity=".45"/>
    <stop offset="1" stop-color="#f5c76e" stop-opacity="0"/>
  </radialGradient>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>`;

// The central emblem: rings of a halo, a wand rising diagonally, a star burst at its tip, a trail of sparkles.
export function emblem(cx, cy, R) {
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
