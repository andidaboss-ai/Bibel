"""Join fra/parts/*.md into fra/<work>.md, then into frbook/text/original.md; write the parts list into frbook/book.json."""
import json, re, os
WORKS = [  # file, parts, title, sub, label
 ('01_getting_rich', ['01_a', '01_b'], 'La Science de l’enrichissement', '1910 · dix-sept chapitres', 'Chapitre'),
 ('02_being_well', ['02_a', '02_b'], 'La Science de la santé', '1910 · dix-sept chapitres', 'Chapitre'),
 ('03_being_great', ['03_a', '03_b'], 'La Science de la grandeur', '1910', 'Chapitre'),
 ('04_how_to_get', ['04'], 'Comment obtenir ce que vous voulez', 'cinq chapitres', 'Chapitre'),
 ('07_man_who_can', ['07'], 'Former l’homme qui peut', '1909 · neuf chapitres', 'Chapitre'),
 ('08_living_healing', ['08_a', '08_b'], 'La Nouvelle Science de la vie et de la guérison', 'neuf chapitres', 'Chapitre'),
 ('10_what_is_truth', ['10'], 'Qu’est-ce que la vérité ?', 'The Nautilus · 1909 · sept chapitres', 'Chapitre'),
 ('05_new_christ', ['05'], 'Un nouveau Christ', 'huit chapitres', 'Chapitre'),
 ('06_jesus', ['06'], 'Jésus : l’homme et son œuvre', 'une conférence · 1905', ''),
 ('09_hellfire_harrison', ['09_a', '09_b'], 'Harrison l’Infernal', 'un roman · 1910', ''),
]
UNNUM = ['Préface', 'Préface des éditeurs (1905)']
NB, NN = "\u00a0", "\u202f"
def frspace(s):
    """French typography: no-break spaces inside guillemets and before : ; ! ?; straight apostrophes to ’."""
    s = re.sub(r"«[ \u00a0\u202f]*", "«" + NB, s)
    s = re.sub(r"[ \u00a0\u202f]*»", NB + "»", s)
    s = re.sub(r"[ \u00a0\u202f]+([;!?])", NN + r"\1", s)
    s = re.sub(r"(?<=\w)([;!?])", NN + r"\1", s)
    s = re.sub(r"[ \u00a0\u202f]+:", NB + ":", s)
    s = re.sub(r"(?<=[\w»])'(?=\w)", "’", s)
    return s
def secs(text):
    parts = re.split(r'^## (.+)$', text, flags=re.M)
    return [(parts[i].strip(), parts[i + 1].strip()) for i in range(1, len(parts), 2)]
orig, plist, pos = [], [], 0
for f, pp, title, sub, label in WORKS:
    paths = [f'fra/parts/{p}.md' for p in pp]
    if not all(os.path.exists(p) for p in paths):
        print('MISSING', f); continue
    s = [(frspace(a), frspace(b)) for p in paths for a, b in secs(open(p).read())]
    n_en = len(secs(open(f'eng/{f}.md').read()))
    if len(s) != n_en: print('SECTION COUNT', f, len(s), n_en)
    open(f'fra/{f}.md', 'w').write('\n'.join(f'## {t}\n\n{b}\n' for t, b in s))
    plist.append({"first_index": pos, "title": title, "sub": sub, "label": label})
    orig += [f'## {t}\n\n{b}\n' for t, b in s]
    pos += len(s)
open('frbook/text/original.md', 'w').write('\n'.join(orig))
b = json.load(open('frbook/book.json'))
b['parts'] = plist; b['unnumbered'] = UNNUM
json.dump(b, open('frbook/book.json', 'w'), ensure_ascii=False, indent=2)
print(pos, 'sections,', sum(len(x.split()) for x in orig), 'words')
