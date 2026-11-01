"""Join swe/parts/*.md into swe/<work>.md and text/original.md (work order of the other editions); write parts into book.json."""
import json, re, glob
WORKS = [  # file, prefix, title, sub, label
 ('01_getting_rich', '01', 'Vetenskapen om att bli rik', '1910 · sjutton kapitel', 'Kapitel'),
 ('02_being_well', '02', 'Vetenskapen om att vara frisk', '1910 · sjutton kapitel', 'Kapitel'),
 ('03_being_great', '03', 'Vetenskapen om att bli stor', '1910', 'Kapitel'),
 ('04_how_to_get', '04', 'Hur du får det du vill ha', 'fem kapitel', 'Kapitel'),
 ('07_man_who_can', '07', 'Människan som kan', '1909 · nio kapitel', 'Kapitel'),
 ('08_living_healing', '08', 'Den nya vetenskapen om liv och läkning', 'nio kapitel', 'Kapitel'),
 ('10_what_is_truth', '10', 'Vad är sanning?', 'The Nautilus · 1909 · sju kapitel', 'Kapitel'),
 ('05_new_christ', '05', 'En ny Kristus', 'åtta kapitel', 'Kapitel'),
 ('06_jesus', '06', 'Jesus: människan och hans verk', 'en föreläsning · 1905', ''),
 ('09_hellfire_harrison', '09', 'Helveteseld-Harrison', 'en roman · 1910', ''),
]
UNNUM = ['Förord', 'Utgivarnas förord (1905)']
def secs(text):
    p = re.split(r'^## (.+)$', text, flags=re.M)
    return [(p[i].strip(), p[i + 1].strip()) for i in range(1, len(p), 2)]
orig, plist, pos = [], [], 0
for f, pre, title, sub, label in WORKS:
    txt = '\n\n'.join(open(p).read().strip('\n') for p in sorted(glob.glob(f'swe/parts/{pre}_*.md')))
    s = secs(txt)
    assert len(s) == len(secs(open(f'eng/{f}.md').read())), (f, len(s))
    open(f'swe/{f}.md', 'w').write('\n'.join(f'## {t}\n\n{b}\n' for t, b in s))
    plist.append({"first_index": pos, "title": title, "sub": sub, "label": label})
    orig += [f'## {t}\n\n{b}\n' for t, b in s]; pos += len(s)
open('text/original.md', 'w').write('\n'.join(orig))
b = json.load(open('book.json')); b['parts'] = plist; b['unnumbered'] = UNNUM; b['rh_part_for'] = UNNUM
json.dump(b, open('book.json', 'w'), ensure_ascii=False, indent=2)
print(pos, 'sections,', sum(len(x.split()) for x in orig), 'words')
