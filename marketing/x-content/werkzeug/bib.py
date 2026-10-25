import re,glob,os
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../../texte/plain-english'))
def chap(book,c):
    d=[x for x in glob.glob(R+'/*/*') if x.endswith('_'+book)][0]
    return open(f'{d}/kapitel_{c:03d}.md').read()
def verses(book,c):
    t=chap(book,c); v={}; cur=None
    for line in t.split('\n'):
        if line.startswith('>') or line.startswith('#') or line.strip()=='---': cur=None; continue
        for part in re.split(r'(?=\[\d+\])',line):
            m=re.match(r'\[(\d+)\]\s*(.*)',part)
            if m: cur=int(m[1]); v[cur]=m[2].strip()
            elif cur and part.strip(): v[cur]+=' '+part.strip()
    return v
def get(book,c,a,b=None):
    v=verses(book,c); return ' '.join(v[i] for i in range(a,(b or a)+1))
if __name__=='__main__':
    import sys
    for r in sys.argv[1:]:
        bk,c,ab=r.split(':'); a,*b=ab.split('-'); print(r,'|',get(bk,int(c),int(a),int(b[0]) if b else None))
