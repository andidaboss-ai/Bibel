import sys,re
secs=[];cur=None
for l in open('book/text/original.md',encoding='utf-8'):
    l=l.rstrip('\n')
    if l.startswith('## '): cur=[l[3:],[]];secs.append(cur);continue
    if cur: cur[1].append(l[2:] if l.startswith('| ') else l)
for p in sys.argv[1:]:
    print('===',p)
    for t,b in secs:
        txt=re.sub(r'\s+',' ',' '.join(b))
        for m in re.finditer(re.escape(p),txt,re.I):
            print('  [%s] ...%s...'%(t,txt[max(0,m.start()-250):m.end()+250]))
