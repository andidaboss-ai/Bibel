"""Join jpn/<work>.md into text/original.md (work order of the other editions); write parts into book.json."""
import json, re
WORKS = [  # file, title, sub, label
 ('01_getting_rich', '富を得る科学', '1910年・全十七章', '章'),
 ('02_being_well', '健康になる科学', '1910年・全十七章', '章'),
 ('03_being_great', '偉大になる科学', '1910年', '章'),
 ('04_how_to_get', '望むものを手に入れる方法', '全五章', '章'),
 ('07_man_who_can', 'できる人をつくる', '1909年・全九章', '章'),
 ('08_living_healing', '生き方と癒やしの新しい科学', '全九章', '章'),
 ('10_what_is_truth', '真理とは何か', '『ノーチラス』誌・1909年・全七章', '章'),
 ('05_new_christ', '新しいキリスト', '全八章', '章'),
 ('06_jesus', 'イエス――その人と働き', '講演・1905年', ''),
 ('09_hellfire_harrison', 'ヘルファイア・ハリソン', '小説・1910年', ''),
]
UNNUM = ['序文', '編者序文(1905年)']
def secs(text):
    p = re.split(r'^## (.+)$', text, flags=re.M)
    return [(p[i].strip(), p[i + 1].strip()) for i in range(1, len(p), 2)]
orig, plist, pos = [], [], 0
for f, title, sub, label in WORKS:
    s = secs(open(f'jpn/{f}.md').read())
    assert len(s) == len(secs(open(f'eng/{f}.md').read())), f
    plist.append({"first_index": pos, "title": title, "sub": sub, "label": label})
    orig += [f'## {t}\n\n{b}\n' for t, b in s]; pos += len(s)
open('text/original.md', 'w').write('\n'.join(orig))
b = json.load(open('book.json')); b['parts'] = plist; b['unnumbered'] = UNNUM
json.dump(b, open('book.json', 'w'), ensure_ascii=False, indent=2)
print(pos, 'sections,', sum(len(re.sub(r'\s', '', x)) for x in orig), 'chars')
