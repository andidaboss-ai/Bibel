"""Combine eng/*.md (texts) and notes/*.md (intros + chapter notes) into enbook/text/original.md + chapters.md
and write the parts list into enbook/book.json."""
import json, re, sys
sys.path.insert(0, 'enbook/tools')
from md import slug
WORKS = [  # file, title, sub, label
 ('01_getting_rich', 'The Science of Getting Rich', '1910 · seventeen chapters', 'Chapter'),
 ('02_being_well', 'The Science of Being Well', '1910 · seventeen chapters', 'Chapter'),
 ('03_being_great', 'The Science of Being Great', '1910', 'Chapter'),
 ('04_how_to_get', 'How to Get What You Want', 'five chapters', 'Chapter'),
 ('07_man_who_can', 'Making the Man Who Can', '1909 · nine chapters', 'Chapter'),
 ('08_living_healing', 'The New Science of Living and Healing', 'nine chapters', 'Chapter'),
 ('10_what_is_truth', 'What Is Truth?', 'The Nautilus · 1909 · seven chapters', 'Chapter'),
 ('05_new_christ', 'A New Christ', 'eight chapters', 'Chapter'),
 ('06_jesus', 'Jesus: The Man and His Work', 'a lecture · 1905', ''),
 ('09_hellfire_harrison', 'Hell-Fire Harrison', 'a novel · 1910', ''),
]
INTRO = 'About This Work'
def secs(text):
    parts = re.split(r'^## (.+)$', text, flags=re.M)
    return [(parts[i].strip(), parts[i + 1].strip()) for i in range(1, len(parts), 2)]
orig, notes_out, parts, unnum = [], [], [], {INTRO, 'Preface', 'Foreword'}
titles = []
for f, title, sub, label in WORKS:
    text = secs(open(f'eng/{f}.md').read())
    import os
    nt = open(f'notes/{f}.md').read() if os.path.exists(f'notes/{f}.md') else '# INTRO x\n(intro pending)\n'
    m = re.search(r'^# INTRO .*?\n(.*?)(?=^## |\Z)', nt, flags=re.M | re.S)
    intro = m.group(1).strip()
    nsec = dict(secs(nt))
    seq = [(INTRO, intro, None)] + [(t, b, nsec.get(t)) for t, b in text]
    parts.append({"first": INTRO if not parts else None, "title": title, "sub": sub, "label": label})
    for i, (t, b, n) in enumerate(seq):
        titles.append(t)
        orig.append(f'## {t}\n\n{b}\n')
        if t not in (INTRO,) and n is None and t not in unnum:
            print('NO NOTES:', f, t)
        if n: notes_out.append((len(titles) - 1, n))
# unique keys exactly as build.chapter_keys
seen, keys = {}, []
for t in titles:
    k = slug(t); seen[k] = seen.get(k, 0) + 1
    keys.append(k if seen[k] == 1 else f'{k}-{seen[k]}')
# parts: "first" must be the (unique) title of the first section of each work -> the intro titles repeat,
# so the part plan is matched by position: we store the index instead
pos = 0; plist = []
for (f, title, sub, label) in WORKS:
    plist.append({"first_index": pos, "title": title, "sub": sub, "label": label})
    pos += 1 + len(secs(open(f'eng/{f}.md').read()))
open('enbook/text/original.md', 'w').write('\n'.join(orig))
open('enbook/text/chapters.md', 'w').write('\n'.join(f'## {keys[i]}\n\n{n}\n' for i, n in notes_out))
b = json.load(open('enbook/book.json'))
b['parts'] = plist; b['unnumbered'] = sorted(unnum)
json.dump(b, open('enbook/book.json', 'w'), ensure_ascii=False, indent=2)
print(len(titles), 'sections,', len(notes_out), 'with notes,', sum(len(x.split()) for x in orig), 'words')
