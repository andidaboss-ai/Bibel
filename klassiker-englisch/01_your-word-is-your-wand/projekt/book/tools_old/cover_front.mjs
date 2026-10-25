// Front cover as an HTML fragment of any size (used for the e-book cover and the print wraps).
import { defs, stars, emblem, sparkle } from './cover_art.mjs';

// W x H = whole canvas (may include bleed/wrap); t = trim box inside it. Design grid 1600 x 2560;
// a shorter trim (e.g. 6 x 9 = 1600 x 2400) compresses only the vertical spacing.
export function front(W, H, t = { x: 0, y: 0, w: W, h: H }) {
  const u = t.w / 1600, v = (t.h / t.w) / 1.6;     // v < 1 for 6 x 9
  const Y = (y) => t.y + (y * v + (1 - v) * 0) * u; // vertical position in design units
  const cx = t.x + t.w / 2, cy = Y(1385), R = 400 * u * Math.min(1, v + 0.03);
  const field = stars(W, H, 520, 7, (x, y) => Math.hypot(x - cx, y - cy) < R * 0.9);
  return `
<div class="front" style="position:absolute;left:0;top:0;width:${W}px;height:${H}px;overflow:hidden;background:#0a0b1f">
<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" style="position:absolute;left:0;top:0">
  ${defs()}
  <rect width="${W}" height="${H}" fill="url(#sky)"/>
  ${field}
  <rect x="${t.x + 56 * u}" y="${t.y + 56 * u}" width="${t.w - 112 * u}" height="${t.h - 112 * u}" fill="none" stroke="url(#gold)" stroke-width="${2 * u}" opacity=".7"/>
  <rect x="${t.x + 72 * u}" y="${t.y + 72 * u}" width="${t.w - 144 * u}" height="${t.h - 144 * u}" fill="none" stroke="url(#gold)" stroke-width="${0.8 * u}" opacity=".45"/>
  ${emblem(cx, cy, R)}
  ${sparkle(cx, Y(1895), 16 * u)}
</svg>
<div style="position:absolute;left:${t.x}px;width:${t.w}px;top:${Y(150)}px;text-align:center">
  <div style="font-family:Jost;font-weight:400;font-size:${34 * u}px;letter-spacing:.42em;color:#e9cf96;text-transform:uppercase;padding-left:.42em">Florence Scovel Shinn</div>
  <div class="goldtext" style="font-family:CG;font-weight:600;font-size:${250 * u}px;line-height:.84;margin-top:${60 * u}px;letter-spacing:.02em">Your Word<br><span style="font-style:italic;font-weight:400;font-size:${130 * u}px;letter-spacing:.04em">is your</span><br>Wand</div>
</div>
<div style="position:absolute;left:${t.x}px;width:${t.w}px;top:${Y(1950)}px;text-align:center">
  <div style="font-family:Jost;font-weight:500;font-size:${38 * u}px;letter-spacing:.34em;color:#f3dca6;text-transform:uppercase;padding-left:.34em">Annotated Edition</div>
  <div style="font-family:CG;font-style:italic;font-weight:400;font-size:${50 * u}px;color:#efe6d4;margin-top:${26 * u}px;line-height:1.25">The classic book of affirmations<br>with modern commentary &amp; a 30-day practice</div>
</div>

</div>`;
}

export const goldCss = `.goldtext{background:linear-gradient(170deg,#fff4d6 0%,#f0cf86 30%,#c99a4b 55%,#f7e2a8 80%,#d6a95a 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 18px rgba(240,200,120,.25))}`;
