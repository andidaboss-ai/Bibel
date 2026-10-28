"""Join ita/parts/*.md into ita/<work>.md, then into itbook/text/original.md; write the parts list into itbook/book.json."""
import json, re, os
WORKS = [  # file, parts, title, sub, label
 ('01_getting_rich', ['01_a', '01_b'], 'La scienza del diventare ricchi', '1910 · diciassette capitoli', 'Capitolo'),
 ('02_being_well', ['02_a', '02_b'], 'La scienza dello stare bene', '1910 · diciassette capitoli', 'Capitolo'),
 ('03_being_great', ['03_a', '03_b'], 'La scienza dell’essere grandi', '1910', 'Capitolo'),
 ('04_how_to_get', ['04'], 'Come ottenere ciò che vuoi', 'cinque capitoli', 'Capitolo'),
 ('07_man_who_can', ['07'], 'Formare l’uomo che può', '1909 · nove capitoli', 'Capitolo'),
 ('08_living_healing', ['08_a', '08_b'], 'La nuova scienza del vivere e del guarire', 'nove capitoli', 'Capitolo'),
 ('10_what_is_truth', ['10'], 'Che cos’è la verità?', 'The Nautilus · 1909 · sette capitoli', 'Capitolo'),
 ('05_new_christ', ['05'], 'Un nuovo Cristo', 'otto capitoli', 'Capitolo'),
 ('06_jesus', ['06'], 'Gesù: l’uomo e la sua opera', 'una conferenza · 1905', ''),
 ('09_hellfire_harrison', ['09_a', '09_b'], 'Harrison l’Infernale', 'un romanzo · 1910', ''),
]
UNNUM = ['Prefazione', 'Prefazione degli editori (1905)']
def secs(text):
    parts = re.split(r'^## (.+)$', text, flags=re.M)
    return [(parts[i].strip(), parts[i + 1].strip()) for i in range(1, len(parts), 2)]
orig, plist, pos = [], [], 0
for f, pp, title, sub, label in WORKS:
    paths = [f'ita/parts/{p}.md' for p in pp]
    if not all(os.path.exists(p) for p in paths):
        print('MISSING', f); continue
    s = [(a, re.sub(r"(?<=\w)'(?=\w)", '’', b)) for p in paths for a, b in secs(open(p).read())]
    n_en = len(secs(open(f'eng/{f}.md').read()))
    if len(s) != n_en: print('SECTION COUNT', f, len(s), n_en)
    open(f'ita/{f}.md', 'w').write('\n'.join(f'## {t}\n\n{b}\n' for t, b in s))
    plist.append({"first_index": pos, "title": title, "sub": sub, "label": label})
    orig += [f'## {t}\n\n{b}\n' for t, b in s]
    pos += len(s)
open('itbook/text/original.md', 'w').write('\n'.join(orig))
b = json.load(open('itbook/book.json'))
b['parts'] = plist; b['unnumbered'] = UNNUM
json.dump(b, open('itbook/book.json', 'w'), ensure_ascii=False, indent=2)
print(pos, 'sections,', sum(len(x.split()) for x in orig), 'words')
