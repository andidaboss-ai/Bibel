// E-book cover: JPG 3200 x 5120 (design 1600 x 2560 rendered at scale 2).
// Usage: node tools/build_cover.mjs [out.jpg]
import { createRequire } from 'module';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { fontFaces } from './cover_art.mjs';
import { front, goldCss } from './cover_front.mjs';
import { B } from './book.mjs';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright')); }

const here = path.dirname(fileURLToPath(import.meta.url));
const out = process.argv[2] || path.join(here, '..', 'output', 'ebook', `${B.slug}-cover.jpg`);
fs.mkdirSync(path.dirname(out), { recursive: true });

const html = `<!doctype html><html><head><meta charset="utf-8"><style>${fontFaces()}${goldCss}
html,body{margin:0;padding:0}</style></head><body>${front(1600, 2560)}</body></html>`;
const tmp = path.join(here, '..', 'output', '_cover.html');
fs.writeFileSync(tmp, html);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1600, height: 2560 }, deviceScaleFactor: +(process.env.COVER_SCALE || 2) });
await page.goto('file://' + tmp);
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: out, type: 'jpeg', quality: 95 });
await browser.close();
fs.unlinkSync(tmp);
console.log(out);
