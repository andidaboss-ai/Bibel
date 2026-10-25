// Print cover (wrap: back + spine + front) as PNG at 600 dpi; tools/build.py turns it into the PDF for KDP.
// Usage: node build_wrap.mjs <out.png> <width_in> <height_in> <spine_in> <edge_x_in> <edge_y_in> <hinge_in> <dpi>
// edge = bleed (paperback) or wrap margin (hardcover); hinge = hardcover hinge next to the spine (0 for paperback).
import { createRequire } from 'module';
import { fontFaces, defs, stars, sparkle } from './cover_art.mjs';
import { front, goldCss } from './cover_front.mjs';
import { B, esc } from './book.mjs';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright')); }

const [, , out, W_in, H_in, S_in, EX_in, EY_in, F_in, dpiArg] = process.argv;
const PX = 96; // CSS pixels per inch
const W = +W_in * PX, H = +H_in * PX, S = +S_in * PX, EX = +EX_in * PX, EY = +EY_in * PX, F = +F_in * PX;
const TRIM_W = 6 * PX, TRIM_H = 9 * PX;
const panelW = EX + TRIM_W + F;                  // back or front panel incl. outer edge and hinge
const frontX = panelW + S;                       // left edge of the front panel
const scale = (+dpiArg || 600) / PX;

// Front artwork drawn for trim + edges so the art runs into the bleed/wrap
const frontW = W - frontX, frontH = H;
const K = B.back;
const backBody = `
<div style="position:absolute;left:${EX + 0.55 * PX}px;top:${EY + 0.75 * PX}px;width:${TRIM_W - 1.1 * PX}px;color:#efe6d4">
  <div style="font-family:Jost;font-weight:500;font-size:${0.105 * PX}px;letter-spacing:.38em;color:#e9cf96;text-transform:uppercase">${esc(K.kicker)}</div>
  <div class="goldtext" style="font-family:CG;font-weight:600;font-size:${0.42 * PX}px;line-height:1.02;margin-top:${0.16 * PX}px">${K.headline.map(esc).join('<br>')}</div>
  <div style="font-family:CG;font-size:${0.165 * PX}px;line-height:1.45;margin-top:${0.24 * PX}px">
    ${K.paras.map((p, i) => `<p style="margin:0 0 ${i < K.paras.length - 1 ? 0.1 * PX : 0}px">${esc(p)}</p>`).join('')}
  </div>
  <div style="font-family:Jost;font-weight:300;font-size:${0.13 * PX}px;line-height:1.7;margin-top:${0.22 * PX}px;color:#f3e7cc">
    ${K.bullets.map((b) => `✦&nbsp; ${esc(b)}`).join('<br>')}
  </div>
  ${K.quote.length ? `  <div style="font-family:CG;font-style:italic;font-size:${0.2 * PX}px;line-height:1.3;margin-top:${0.3 * PX}px;color:#f3dca6;text-align:center">${K.quote.map(esc).join('<br>')}</div>
  <div style="font-family:Jost;font-size:${0.09 * PX}px;letter-spacing:.3em;margin-top:${0.08 * PX}px;text-align:center;color:#cdbf9f;text-transform:uppercase">${esc(B.author)}` : ""}
</div>
</div>
`;

const spine = S >= 0.25 * PX ? `
<div style="position:absolute;left:${panelW}px;top:0;width:${S}px;height:${H}px;display:flex;align-items:center;justify-content:center">
  <div style="transform:rotate(90deg);white-space:nowrap;display:flex;align-items:center;gap:${0.22 * PX}px">
    <span class="goldtext" style="font-family:CG;font-weight:600;font-size:${Math.min(S * 0.5, 0.26 * PX)}px;letter-spacing:.03em">${esc(B.title)}</span>
    <span style="color:#e9cf96;font-size:${Math.min(S * 0.3, 0.12 * PX)}px">✦</span>
    <span style="font-family:Jost;font-size:${Math.min(S * 0.28, 0.1 * PX)}px;letter-spacing:.3em;color:#e9cf96;text-transform:uppercase">${esc(B.author)}</span>
  </div>
</div>` : '';

const html = `<!doctype html><html><head><meta charset="utf-8"><style>${fontFaces()}${goldCss}
html,body{margin:0;padding:0;width:${W}px;height:${H}px;overflow:hidden;background:${B.cover.sky[2]}}</style></head><body>
<svg width="${W}" height="${H}" style="position:absolute;left:0;top:0">${defs(B.cover.sky)}
  <rect width="${W}" height="${H}" fill="${B.cover.sky[2]}"/>
  <rect x="0" y="0" width="${frontX}" height="${H}" fill="url(#sky)" opacity=".75"/>
  ${stars(frontX, H, 260, 11, (x, y) => x > EX + 0.45 * PX && x < EX + TRIM_W - 0.4 * PX && y > EY + 0.6 * PX && y < EY + 7.0 * PX)}
  ${sparkle(EX + TRIM_W - 0.6 * PX, EY + 0.7 * PX, 0.08 * PX)}
</svg>
${backBody}
${spine}
<div style="position:absolute;left:${frontX}px;top:0;width:${frontW}px;height:${frontH}px;overflow:hidden">
  ${front(frontW, frontH, { x: F, y: EY, w: TRIM_W, h: TRIM_H })}
</div>
</body></html>`;

const fs = await import('fs');
const tmp = out.replace(/\.png$/, '.html');
fs.writeFileSync(tmp, html);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: Math.round(W), height: Math.round(H) }, deviceScaleFactor: scale });
await page.goto('file://' + tmp);
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: out, type: 'png' });
await browser.close();
fs.unlinkSync(tmp);
console.log(out);
