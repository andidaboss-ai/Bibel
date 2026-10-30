"""Completeness check: Japanese vs English, per chapter. usage: check_ja.py eng.md ja.md [first last]
Ratio = Japanese chars / English words (expected ~2.4-5.0). Paragraph counts must match."""
import re, sys
def secs(p):
    s=open(p).read(); parts=re.split(r'^## (.*)$', s, flags=re.M)
    return [(parts[i].strip(), parts[i+1]) for i in range(1,len(parts),2)]
en=secs(sys.argv[1]); ja=secs(sys.argv[2])
if len(sys.argv)>3: en=en[int(sys.argv[3]):int(sys.argv[4])+1]
w=lambda t: len(re.findall(r"[A-Za-z0-9’'-]+",t))
c=lambda t: len(re.sub(r'\s','',t))
npar=lambda t: len([p for p in t.split('\n\n') if p.strip()])
bad=0
if len(en)!=len(ja): print('CHAPTER COUNT',len(en),len(ja)); bad+=1
for (te,be),(tj,bj) in zip(en,ja):
    r=c(bj)/max(1,w(be)); f=''
    if not 2.2<=r<=5.5: f+=' <-- RATIO'
    if npar(be)!=npar(bj): f+=f' <-- PARAS en {npar(be)} ja {npar(bj)}'
    if f: bad+=1
    print(f'{w(be):6d} {c(bj):6d} {r:4.2f} {te[:34]:34s}| {tj[:20]}{f}')
t=open(sys.argv[2]).read()
for pat,name in [(r'"','straight quote'),(r'[A-Za-z]{25,}','long latin'),(r'\.\.\.','dots')]:
    n=len(re.findall(pat,t))
    if n: print(name,n); bad+=1
print('problems:',bad)
