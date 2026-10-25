import re
L=open('src/a.txt').read().split('\n')
s=L.index('PREFACE.'); e=[i for i,l in enumerate(L) if l.startswith('NOTES:')][0]
body='\n'.join(L[s:e])
notes={'1':'Gal. i, 10; Eph. vi, 5, 6.','2':'The particulars which follow are collected from other accounts of Brother Lawrence.',
'3':'*I suppose he means* that all distinct notions he could form of GOD, were unsatisfactory, because he perceived them to be unworthy of GOD; and therefore his mind was not to be satisfied but by the views of *faith*, which apprehend GOD as infinite and incomprehensible, as He is in Himself, and not as He can be conceived by human ideas.',
'4':'He took to his bed two days after, and died within the week.'}
paras=[re.sub(r'\s+',' ',p).strip() for p in re.split(r'\n\s*\n',body) if p.strip()]
out=[];sec_notes=[]
def flush():
    global sec_notes
    if sec_notes:
        out.append('* * *')
        for n in sec_notes: out.append('NOTE'+n)
    sec_notes=[]
sup={'1':'¹','2':'²','3':'³','4':'⁴'}
for p in paras:
    if p in('CONVERSATIONS.','LETTERS.'): continue
    m=re.fullmatch(r'([A-Z]+) (CONVERSATION|LETTER)\.',p)
    if p=='PREFACE.' or m:
        flush()
        out.append('## '+('Preface' if p=='PREFACE.' else m.group(1).title()+' '+m.group(2).title()))
        continue
    p=p.replace('--','—')
    p=re.sub(r'_([^_]+)_',r'*\1*',p)
    for k in re.findall(r'\[(\d)\]',p):
        p=p.replace('['+k+']',sup[k]); sec_notes.append(k)
    out.append(p)
flush()
t='\n\n'.join(out)
t=re.sub(r'NOTE(\d)',lambda m:'<<'+sup[m.group(1)]+'>> '+notes[m.group(1)],t)
open('book/text/original.md','w').write(t+'\n')
