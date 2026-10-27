// Loads book.json (title, cover texts, back-cover texts, theme) for the cover scripts.
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const here = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.join(here, '..');
export const B = JSON.parse(fs.readFileSync(path.join(ROOT, 'book.json'), 'utf8'));
export const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
