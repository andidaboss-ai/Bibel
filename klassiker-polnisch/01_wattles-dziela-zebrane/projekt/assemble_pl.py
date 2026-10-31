"""Join pol/parts/*.md into pol/<work>.md and text/original.md (work order of the other editions); write parts into book.json."""
import json, re, glob
WORKS = [  # file, prefix, title, sub, label
 ('01_getting_rich', '01', 'Nauka bogacenia się', '1910 · siedemnaście rozdziałów', 'Rozdział'),
 ('02_being_well', '02', 'Nauka bycia zdrowym', '1910 · siedemnaście rozdziałów', 'Rozdział'),
 ('03_being_great', '03', 'Nauka bycia wielkim', '1910', 'Rozdział'),
 ('04_how_to_get', '04', 'Jak zdobyć to, czego chcesz', 'pięć rozdziałów', 'Rozdział'),
 ('07_man_who_can', '07', 'Człowiek, który potrafi', '1909 · dziewięć rozdziałów', 'Rozdział'),
 ('08_living_healing', '08', 'Nowa nauka życia i uzdrawiania', 'dziewięć rozdziałów', 'Rozdział'),
 ('10_what_is_truth', '10', 'Czym jest prawda?', 'The Nautilus · 1909 · siedem rozdziałów', 'Rozdział'),
 ('05_new_christ', '05', 'Nowy Chrystus', 'osiem rozdziałów', 'Rozdział'),
 ('06_jesus', '06', 'Jezus: człowiek i jego dzieło', 'wykład · 1905', ''),
 ('09_hellfire_harrison', '09', 'Piekielny Harrison', 'powieść · 1910', ''),
]
UNNUM = ['Przedmowa', 'Przedmowa wydawców (1905)']
def secs(text):
    p = re.split(r'^## (.+)$', text, flags=re.M)
    return [(p[i].strip(), p[i + 1].strip()) for i in range(1, len(p), 2)]
orig, plist, pos = [], [], 0
for f, pre, title, sub, label in WORKS:
    txt = '\n\n'.join(open(p).read().strip('\n') for p in sorted(glob.glob(f'pol/parts/{pre}_*.md')))
    s = secs(txt)
    assert len(s) == len(secs(open(f'eng/{f}.md').read())), (f, len(s))
    open(f'pol/{f}.md', 'w').write('\n'.join(f'## {t}\n\n{b}\n' for t, b in s))
    plist.append({"first_index": pos, "title": title, "sub": sub, "label": label})
    orig += [f'## {t}\n\n{b}\n' for t, b in s]; pos += len(s)
open('text/original.md', 'w').write('\n'.join(orig))
b = json.load(open('book.json')); b['parts'] = plist; b['unnumbered'] = UNNUM
json.dump(b, open('book.json', 'w'), ensure_ascii=False, indent=2)
print(pos, 'sections,', sum(len(x.split()) for x in orig), 'words')
