"""Join por/parts/*.md into por/<work>.md, then into ptbook/text/original.md; write the parts list into ptbook/book.json."""
import json, re, os
WORKS = [  # file, parts, title, sub, label
 ('01_getting_rich', ['01_a', '01_b'], 'A Ciência de Ficar Rico', '1910 · dezessete capítulos', 'Capítulo'),
 ('02_being_well', ['02_a', '02_b'], 'A Ciência de Ser Saudável', '1910 · dezessete capítulos', 'Capítulo'),
 ('03_being_great', ['03_a', '03_b'], 'A Ciência de Ser Grande', '1910', 'Capítulo'),
 ('04_how_to_get', ['04'], 'Como Conseguir o que Você Quer', 'cinco capítulos', 'Capítulo'),
 ('07_man_who_can', ['07'], 'Formando o Homem que Pode', '1909 · nove capítulos', 'Capítulo'),
 ('08_living_healing', ['08_a', '08_b'], 'A Nova Ciência de Viver e Curar', 'nove capítulos', 'Capítulo'),
 ('10_what_is_truth', ['10'], 'O que É a Verdade?', 'The Nautilus · 1909 · sete capítulos', 'Capítulo'),
 ('05_new_christ', ['05'], 'Um Novo Cristo', 'oito capítulos', 'Capítulo'),
 ('06_jesus', ['06'], 'Jesus: o Homem e Sua Obra', 'uma conferência · 1905', ''),
 ('09_hellfire_harrison', ['09_a', '09_b'], 'Harrison, o Infernal', 'um romance · 1910', ''),
]
UNNUM = ['Prefácio', 'Prefácio dos editores (1905)']
def secs(text):
    parts = re.split(r'^## (.+)$', text, flags=re.M)
    return [(parts[i].strip(), parts[i + 1].strip()) for i in range(1, len(parts), 2)]
orig, plist, pos = [], [], 0
for f, pp, title, sub, label in WORKS:
    paths = [f'por/parts/{p}.md' for p in pp]
    if not all(os.path.exists(p) for p in paths):
        print('MISSING', f); continue
    s = [x for p in paths for x in secs(open(p).read())]
    n_en = len(secs(open(f'eng/{f}.md').read()))
    if len(s) != n_en: print('SECTION COUNT', f, len(s), n_en)
    open(f'por/{f}.md', 'w').write('\n'.join(f'## {t}\n\n{b}\n' for t, b in s))
    plist.append({"first_index": pos, "title": title, "sub": sub, "label": label})
    orig += [f'## {t}\n\n{b}\n' for t, b in s]
    pos += len(s)
open('ptbook/text/original.md', 'w').write('\n'.join(orig))
b = json.load(open('ptbook/book.json'))
b['parts'] = plist; b['unnumbered'] = UNNUM
json.dump(b, open('ptbook/book.json', 'w'), ensure_ascii=False, indent=2)
print(pos, 'sections,', sum(len(x.split()) for x in orig), 'words')
