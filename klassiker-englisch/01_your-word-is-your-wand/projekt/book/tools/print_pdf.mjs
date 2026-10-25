// Prints an HTML file to PDF with Chromium.
// Usage: node print_pdf.mjs <in.html> <out.pdf> <width_in> <height_in>
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright')); }

const [, , src, out, w, h] = process.argv;
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('file://' + src, { waitUntil: 'load', timeout: 0 });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: out, width: `${w}in`, height: `${h}in`, printBackground: true, preferCSSPageSize: true, tagged: true, timeout: 0 });
await browser.close();
