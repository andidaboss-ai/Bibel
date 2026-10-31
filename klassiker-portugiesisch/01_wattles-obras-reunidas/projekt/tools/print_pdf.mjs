// Prints an HTML file to PDF with Chromium.
// Usage: node print_pdf.mjs <in.html> <out.pdf> <width_in> <height_in>
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { try { ({ chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright')); }
  catch { ({ chromium } = createRequire(process.env.PW_NODE || '/workspace/pwnode/')('playwright-core')); } }
const LAUNCH = process.env.CHROME_PATH || (await import('fs')).existsSync('/usr/bin/google-chrome') ? { executablePath: process.env.CHROME_PATH || '/usr/bin/google-chrome' } : {};

const [, , src, out, w, h] = process.argv;
const browser = await chromium.launch(LAUNCH);
const page = await browser.newPage();
await page.goto('file://' + src, { waitUntil: 'load', timeout: 0 });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: out, width: `${w}in`, height: `${h}in`, printBackground: true, preferCSSPageSize: true, tagged: true, timeout: 0 });
await browser.close();
