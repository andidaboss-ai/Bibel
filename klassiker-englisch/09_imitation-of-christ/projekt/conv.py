import re
t=open('src/g1653.txt').read()
s=t.index('INTRODUCTORY NOTE\n\n\nThe treatise'); e=t.index('*** END OF THE PROJECT')
body=t[s:e]
SUP=str.maketrans('0123456789','⁰¹²³⁴⁵⁶⁷⁸⁹')
paras=[p.strip('\n') for p in re.split(r'\n\s*\n',body) if p.strip()]
out=[]; i=0; book=0; titles={}
BOOKS={'THE FIRST BOOK':'Book One','THE SECOND BOOK':'Book Two','THE THIRD BOOK':'Book Three','THE FOURTH BOOK':'Book Four'}
pending_title=False
def clean(p):
    p=re.sub(r'\s+',' ',p).strip().replace('--','—')
    p=re.sub(r'_([^_]+)_',r'*\1*',p)
    p=re.sub(r'\((\d+)\)',lambda m:m.group(1).translate(SUP),p)
    return p
while i<len(paras):
    p=paras[i]; f=re.sub(r'\s+',' ',p).strip()
    if f=='INTRODUCTORY NOTE': out.append('## Introductory Note'); i+=1; continue
    if f=='THE IMITATION OF CHRIST': i+=1; continue
    m=re.match(r'(THE (FIRST|SECOND|THIRD|FOURTH) BOOK)',f)
    if m:
        book+=1; out.append(f'%%BOOK {book} {f[len(m.group(1)):].strip()}'); i+=1
        if book==4:
            out.append('## A Devout Exhortation to the Holy Communion'); i+=1  # next para is that title
        continue
    m=re.fullmatch(r'CHAPTER ([IVXL]+)',f)
    if m:
        ttl=re.sub(r'\s+',' ',paras[i+1]).strip()
        ttl=ttl[0].upper()+ttl[1:]
        if ttl in titles: ttl+=f' ({["","I","II","III","IV"][book]})'
        titles[ttl]=1
        out.append('## '+ttl); i+=2; continue
    if re.fullmatch(r'The Voice of (Christ|the Beloved|the Disciple)',f):
        out.append('#### '+f); i+=1; continue
    if re.match(r'^\(\d+\) ',f):
        out.append('~~ '+re.sub(r'\((\d+)\) ?',lambda m:m.group(1).translate(SUP)+' ',f).strip()); i+=1; continue
    out.append(clean(p)); i+=1
s='\n\n'.join(out)+'\n'
open('book/text/original.md','w').write(s)
print(len(titles))
