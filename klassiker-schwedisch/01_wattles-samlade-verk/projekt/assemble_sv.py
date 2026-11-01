"""Join nld/parts/*.md into nld/<work>.md and text/original.md (work order of the other editions); write parts into book.json."""
import json, re, glob
WORKS = [  # file, prefix, title, sub, label
 ('01_getting_rich', '01', 'De wetenschap van het rijk worden', '1910 · zeventien hoofdstukken', 'Hoofdstuk'),
 ('02_being_well', '02', 'De wetenschap van het gezond zijn', '1910 · zeventien hoofdstukken', 'Hoofdstuk'),
 ('03_being_great', '03', 'De wetenschap van het groot worden', '1910', 'Hoofdstuk'),
 ('04_how_to_get', '04', 'Hoe je krijgt wat je wilt', 'vijf hoofdstukken', 'Hoofdstuk'),
 ('07_man_who_can', '07', 'De mens die het kan', '1909 · negen hoofdstukken', 'Hoofdstuk'),
 ('08_living_healing', '08', 'De nieuwe wetenschap van leven en genezen', 'negen hoofdstukken', 'Hoofdstuk'),
 ('10_what_is_truth', '10', 'Wat is waarheid?', 'The Nautilus · 1909 · zeven hoofdstukken', 'Hoofdstuk'),
 ('05_new_christ', '05', 'Een nieuwe Christus', 'acht hoofdstukken', 'Hoofdstuk'),
 ('06_jesus', '06', 'Jezus: de mens en zijn werk', 'een lezing · 1905', ''),
 ('09_hellfire_harrison', '09', 'Hellevuur-Harrison', 'een roman · 1910', ''),
]
UNNUM = ['Voorwoord', 'Voorwoord van de uitgevers (1905)']
def secs(text):
    p = re.split(r'^## (.+)$', text, flags=re.M)
    return [(p[i].strip(), p[i + 1].strip()) for i in range(1, len(p), 2)]
orig, plist, pos = [], [], 0
for f, pre, title, sub, label in WORKS:
    txt = '\n\n'.join(open(p).read().strip('\n') for p in sorted(glob.glob(f'nld/parts/{pre}_*.md')))
    s = secs(txt)
    assert len(s) == len(secs(open(f'eng/{f}.md').read())), (f, len(s))
    open(f'nld/{f}.md', 'w').write('\n'.join(f'## {t}\n\n{b}\n' for t, b in s))
    plist.append({"first_index": pos, "title": title, "sub": sub, "label": label})
    orig += [f'## {t}\n\n{b}\n' for t, b in s]; pos += len(s)
open('text/original.md', 'w').write('\n'.join(orig))
b = json.load(open('book.json')); b['parts'] = plist; b['unnumbered'] = UNNUM
json.dump(b, open('book.json', 'w'), ensure_ascii=False, indent=2)
print(pos, 'sections,', sum(len(x.split()) for x in orig), 'words')
