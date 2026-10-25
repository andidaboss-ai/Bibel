import re
t=open('src/long.txt').read()
a=t.index('EPICTETUS.\n\n\nVery little'); b=t.index('A SELECTION FROM THE DISCOURSES OF EPICTETUS.\n',a+20)
c=t.index('THE ENCHEIRIDION, OR MANUAL.\n',b); d=t.index('*** END OF THE PROJECT')
def isverse(p):
    L=[l for l in p.split('\n') if l.strip()]
    return all(len(l)<=60 for l in L) and len(' '.join(L))>25 and not p.isupper() and not p.startswith('and what')
def P(s):
    out=[]
    for p in re.split(r'\n\s*\n',s):
        if not p.strip(): continue
        if isverse(p): out.append('\n'.join('| '+l.strip() for l in p.split('\n') if l.strip()))
        else: out.append(re.sub(r'\s+',' ',p).strip())
    return out
SMALL={'a','an','and','the','of','or','to','in','on','by','for','with','as','at','from','that','which','who','we','is','are','be','not','what','how','his','him','our','us','he','was','were','has','had','into','one','those','these','but','if','it','its','there','than','them','they','should','ought','can','may','must','do','does','did','all','any','men','man','persons','person'}
SMALL={'a','an','and','the','of','or','to','in','on','by','for','with','as','at','from'}
def tc(h):
    w=h.lower().split(' '); out=[]
    for i,x in enumerate(w):
        core=re.sub(r'^\W+','',x)
        if i and core.rstrip('.,;:)') in SMALL and not out[-1].endswith(('.',';',':')): out.append(x)
        else:
            j=len(x)-len(core); out.append(x[:j]+core[:1].upper()+core[1:])
    s=' '.join(out)
    s=re.sub(r'\((\w)',lambda m:'('+m.group(1).upper(),s)
    return s.replace('; And ','; and ').replace('(Or ','(or ')
def greek(p):
    p=re.sub(r' ?\(\[Greek:[^\]]*\]\)','',p)
    p=p.replace('([Greek: eisagogaen)]','').replace('([Greek: anarchonti)]','')
    p=re.sub(r', \[Greek:[^\]]*\]','',p)
    p=re.sub(r'\(\[Greek:[^\]]*\],? ?','(',p)
    p=re.sub(r' ?\[Greek:[^\]]*\]','',p)
    return p
out=["## George Long’s Note on Epictetus"]
for p in P(t[a:b])[1:]:
    out.append(greek(p))
for p in P(t[b:c])[1:]:
    m=re.match(r'^([^a-z]{6,}?)[.?!]?—(.*)$',p)
    if m and m.group(1).upper()==m.group(1):
        out.append('## '+tc(m.group(1).strip().rstrip('.')))
        p=m.group(2).strip()
    out.append(greek(p))
n=0
for p in P(t[c:d])[1:]:
    if re.fullmatch(r'[IVXL]+\.',p):
        n+=1; out.append(f'## Chapter {n}'); continue
    out.append(greek(p))
s='\n\n'.join(out)+'\n'
s=s.replace('--','—').replace('under his name was written\n\nPhotius','under his name was written [by his pupil Arrian].\n\nPhotius').replace('c. 55, torn, ii.','c. 55, tom. ii.')
open('book/text/original.md','w').write(s)
