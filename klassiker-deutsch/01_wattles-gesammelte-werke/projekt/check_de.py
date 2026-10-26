"""Completeness check: German translation vs English source, chapter by chapter.
usage: python3 check_de.py <english.md> <german.md> [first_en_chapter_index last_index]
Chapters are matched in order (## headings). Ratio = German words / English words; expected 0.85–1.35."""
import re,sys
def secs(p):
    s=open(p).read(); parts=re.split(r'^## (.*)$',s,flags=re.M)
    return [(parts[i].strip(),parts[i+1]) for i in range(1,len(parts),2)]
en=secs(sys.argv[1]); de=secs(sys.argv[2])
if len(sys.argv)>3: en=en[int(sys.argv[3]):int(sys.argv[4])+1]
w=lambda t:len(re.findall(r"[A-Za-zÄÖÜäöüß0-9’'-]+",t))
bad=0
if len(en)!=len(de): print(f'CHAPTER COUNT: en {len(en)} de {len(de)}'); bad+=1
for (te,be),(td,bd) in zip(en,de):
    r=w(bd)/max(1,w(be)); flag='' if 0.85<=r<=1.35 else '  <-- CHECK'
    if flag: bad+=1
    print(f'{w(be):6d} {w(bd):6d} {r:5.2f}  {te[:40]:40s} | {td[:40]}{flag}')
for p in [sys.argv[2]]:
    t=open(p).read()
    for pat,name in [(r'(?<![A-Za-zäöü])(ae|oe|ue)(?=[a-zäöüß])','ae/oe/ue?'),(r'Qü|aü|eü|Fraü','bad ü'),(r'"','straight quote'),(r'\bdass\b',None)]:
        if name and re.search(pat,t): print('WARN',name,len(re.findall(pat,t)))
print('problems:',bad)
