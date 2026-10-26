"""Combine deu/*.md into book/text/original.md and write the parts list into book/book.json."""
import json, re, os
WORKS = [  # file, title, sub, label
 ('01_getting_rich', 'Die Wissenschaft des Reichwerdens', '1910 · siebzehn Kapitel', 'Kapitel'),
 ('02_being_well', 'Die Wissenschaft des Gesundseins', '1910 · siebzehn Kapitel', 'Kapitel'),
 ('03_being_great', 'Die Wissenschaft des Großseins', '1910', 'Kapitel'),
 ('04_how_to_get', 'Wie man bekommt, was man will', 'fünf Kapitel', 'Kapitel'),
 ('07_man_who_can', 'Den Mann formen, der es kann', '1909 · neun Kapitel', 'Kapitel'),
 ('08_living_healing', 'Die neue Wissenschaft des Lebens und Heilens', 'neun Kapitel', 'Kapitel'),
 ('10_what_is_truth', 'Was ist Wahrheit?', 'The Nautilus · 1909 · sieben Kapitel', 'Kapitel'),
 ('05_new_christ', 'Ein neuer Christus', 'acht Kapitel', 'Kapitel'),
 ('06_jesus', 'Jesus: Der Mensch und sein Werk', 'ein Vortrag · 1905', ''),
 ('09_hellfire_harrison', 'Höllenfeuer-Harrison', 'ein Roman · 1910', ''),
]
UNNUM = ['Vorwort', 'Vorwort der Herausgeber (1905)']
def secs(text):
    parts = re.split(r'^## (.+)$', text, flags=re.M)
    return [(parts[i].strip(), parts[i + 1].strip()) for i in range(1, len(parts), 2)]
orig, plist, pos = [], [], 0
for f, title, sub, label in WORKS:
    p = f'deu/{f}.md'
    if not os.path.exists(p):
        print('MISSING', p); continue
    s = secs(open(p).read())
    plist.append({"first_index": pos, "title": title, "sub": sub, "label": label})
    for t, b in s:
        orig.append(f'## {t}\n\n{b}\n')
    pos += len(s)
open('book/text/original.md', 'w').write('\n'.join(orig))
b = json.load(open('book/book.json'))
b['parts'] = plist; b['unnumbered'] = UNNUM
json.dump(b, open('book/book.json', 'w'), ensure_ascii=False, indent=2)
print(pos, 'sections,', sum(len(x.split()) for x in orig), 'words')
