// Druckt eine HTML-Datei mit Chromium als PDF.
// Aufruf: node pdf_drucken.mjs <eingabe.html> <ausgabe.pdf> <breite_zoll> <hoehe_zoll>
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright')); }

const [, , ein, aus, breite, hoehe] = process.argv;
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('file://' + ein, { waitUntil: 'load', timeout: 0 });
await page.evaluate(() => document.fonts.ready);
await page.pdf({
  path: aus,
  width: `${breite}in`,
  height: `${hoehe}in`,
  printBackground: true,
  preferCSSPageSize: true,
  displayHeaderFooter: false,
  outline: false,
  tagged: true,
  timeout: 0,
});
await browser.close();
