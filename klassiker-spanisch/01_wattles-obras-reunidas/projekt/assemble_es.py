"""Join spa/parts/*.md into spa/<work>.md, then into esbook/text/original.md; write the parts list into esbook/book.json."""
import json, re, os
WORKS = [  # file, parts, title, sub, label
 ('01_getting_rich', ['01_a', '01_b'], 'La ciencia de hacerse rico', '1910 · diecisiete capítulos', 'Capítulo'),
 ('02_being_well', ['02_a', '02_b'], 'La ciencia de estar bien', '1910 · diecisiete capítulos', 'Capítulo'),
 ('03_being_great', ['03_a', '03_b'], 'La ciencia de ser grande', '1910', 'Capítulo'),
 ('04_how_to_get', ['04'], 'Cómo conseguir lo que se desea', 'cinco capítulos', 'Capítulo'),
 ('07_man_who_can', ['07'], 'Formar al hombre que puede', '1909 · nueve capítulos', 'Capítulo'),
 ('08_living_healing', ['08_a', '08_b'], 'La nueva ciencia de vivir y sanar', 'nueve capítulos', 'Capítulo'),
 ('10_what_is_truth', ['10'], '¿Qué es la verdad?', 'The Nautilus · 1909 · siete capítulos', 'Capítulo'),
 ('05_new_christ', ['05'], 'Un nuevo Cristo', 'ocho capítulos', 'Capítulo'),
 ('06_jesus', ['06'], 'Jesús: el hombre y su obra', 'una conferencia · 1905', ''),
 ('09_hellfire_harrison', ['09_a', '09_b'], 'Harrison el Infernal', 'una novela · 1910', ''),
]
UNNUM = ['Prefacio', 'Prólogo de los editores (1905)']
def secs(text):
    parts = re.split(r'^## (.+)$', text, flags=re.M)
    return [(parts[i].strip(), parts[i + 1].strip()) for i in range(1, len(parts), 2)]
orig, plist, pos = [], [], 0
for f, pp, title, sub, label in WORKS:
    paths = [f'spa/parts/{p}.md' for p in pp]
    if not all(os.path.exists(p) for p in paths):
        print('MISSING', f); continue
    s = [x for p in paths for x in secs(open(p).read())]
    n_en = len(secs(open(f'eng/{f}.md').read()))
    if len(s) != n_en: print('SECTION COUNT', f, len(s), n_en)
    open(f'spa/{f}.md', 'w').write('\n'.join(f'## {t}\n\n{b}\n' for t, b in s))
    plist.append({"first_index": pos, "title": title, "sub": sub, "label": label})
    orig += [f'## {t}\n\n{b}\n' for t, b in s]
    pos += len(s)
open('esbook/text/original.md', 'w').write('\n'.join(orig))
b = json.load(open('esbook/book.json'))
b['parts'] = plist; b['unnumbered'] = UNNUM
json.dump(b, open('esbook/book.json', 'w'), ensure_ascii=False, indent=2)
print(pos, 'sections,', sum(len(x.split()) for x in orig), 'words')
