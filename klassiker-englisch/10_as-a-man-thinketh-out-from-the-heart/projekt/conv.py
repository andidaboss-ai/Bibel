import re
SMALL={'a','an','and','the','of','on','in','to','from','their'}
def tc(h):
    w=h.lower().split(); return ' '.join(x if i and x in SMALL else '-'.join(p.capitalize() for p in x.split('-')) for i,x in enumerate(w))
def paras(txt):
    out=[]
    for p in re.split(r'\n\s*\n',txt):
        if not p.strip(): continue
        L=p.split('\n')
        if all(l.startswith('  ') for l in L if l.strip()):
            out.append(('v',[l.strip() for l in L if l.strip()]))
        else: out.append(('p',re.sub(r'\s+',' ',p).strip()))
    return out
def fmt(k,v):
    fix=lambda s:re.sub(r'_([^_]+)_',r'*\1*',s.replace('--','—'))
    if k=='v': return '\n'.join('| '+fix(l) for l in v)
    return fix(v)
mottos={}
out=[]
# As a Man Thinketh
t=open('src/g4507.txt').read()
m=t[t.index('_Mind is the Master'):t.index('Authorized Edition')]
mottos['A']=[re.sub(r'_','',l.strip()).replace('--','—') for l in m.split('\n') if l.strip()]
s=t.index('FOREWORD\n'); e=t.index('*** END OF THE PROJECT')
heads=['THOUGHT AND CHARACTER','EFFECT OF THOUGHT ON CIRCUMSTANCES','EFFECT OF THOUGHT ON HEALTH AND THE BODY','THOUGHT AND PURPOSE','THE THOUGHT-FACTOR IN ACHIEVEMENT','VISIONS AND IDEALS','SERENITY']
for k,v in paras(t[s:e]):
    if k=='p' and v=='FOREWORD': out.append('## Foreword'); continue
    if k=='p' and v=='AS A MAN THINKETH': continue
    if k=='p' and v in heads: out.append('## '+tc(v)); continue
    if k=='p' and v in ('BROAD PARK AVENUE,','ILFRACOMBE,','ENGLAND'):
        out[-1]=out[-1]+'\n'+v if out[-1].startswith('=>') else '=> '+v; continue
    if k=='p' and v=='JAMES ALLEN.': out.append('=> JAMES ALLEN.'); continue
    out.append(fmt(k,v))
# Out from the Heart
t=open('src/g74178.txt').read()
m=t[t.index('_Make pure thy heart'):t.index('R. F. FENNO')]
mottos['B']=[re.sub(r'_','',l.strip()).replace('strong, and fret,','strong, and free,') for l in m.split('\n') if l.strip()]
s=t.index('THE HEART AND THE LIFE\n\nAs the heart'); e=t.index('*** END OF THE PROJECT')
heads2=['THE HEART AND THE LIFE','THE NATURE AND POWER OF MIND','FORMATION OF HABIT','DOING AND KNOWING','FIRST STEPS IN THE HIGHER LIFE','MENTAL CONDITIONS AND THEIR EFFECTS','EXHORTATION']
for k,v in paras(t[s:e]):
    if k=='p' and v in heads2: out.append('## '+tc(v)); continue
    out.append(fmt(k,v))
s='\n\n'.join(out)+'\n'
open('book/text/original.md','w').write(s)
import json; json.dump(mottos,open('mottos.json','w'),ensure_ascii=False,indent=1)
# --- structured tables in "First Steps" and "Mental Conditions", cut publisher ads
s=open('book/text/original.md').read()
s=s[:s.index('| *BOOKS BY*')].rstrip()+'\n'
a=s.index('| VICES TO BE OVERCOME AND ERADICATED.'); b=s.index('| 3. Unlimited forgiveness.'); b=s.index('\n',b)
s=s[:a]+'''#### Vices to Be Overcome and Eradicated

**Vices of the Body** — *First Lesson: Discipline of the Body*

1. Indolence.
2. Self-indulgence.

**Vices of the Tongue** — *Second Lesson: Discipline of Speech*

1. Slander.
2. Gossip and idle conversation.
3. Abusive and unkind speech.
4. Levity, or irreverent speech.
5. Captiousness, or fault-finding speech.

#### Virtues to Be Practiced and Acquired

*Third Lesson: Discipline of Inclination*

1. Unselfish performance of duty.
2. Unswerving rectitude.
3. Unlimited forgiveness.'''+s[b:]
def table(s,start,endword,head):
    a=s.index(start); b=s.index(endword,a); b=s.index('\n\n',b) if '\n\n' in s[b:] else len(s)
    blk=s[a:b]; lines=[l[2:] for l in blk.split('\n') if l.startswith('| ')]
    items=[]; cur=None
    for l in lines[2:]:
        m=re.match(r'^(\S.*?[.,])\s{2,}(.*)$',l)
        if m: cur=[m.group(1),m.group(2)]; items.append(cur)
        elif cur: 
            l=l.strip()
            cur[1]+=' '+l
    md=f'#### {head}\n\n'+'\n'.join(f'- **{x}** {y}' for x,y in items)
    return s[:a]+md+s[b:]
s=table(s,'| WRONG MENTAL','| Desire, or','Wrong Mental Conditions and Their Effects')
s=table(s,'| RIGHT MENTAL','| Self-conquest.','Right Mental Conditions and Their Effects')
open('book/text/original.md','w').write(s)
s=s.replace('- **Desire, or** Grief, folly, sorrow, uncertainty, and Self-slavery. loneliness.','- **Desire, or Self-slavery.** Grief, folly, sorrow, uncertainty, and loneliness.')
s=s.replace('Gentle conditions, bliss, and blessedness\n','Gentle conditions, bliss, and blessedness.\n')
open('book/text/original.md','w').write(s)

import re as _r
s=open('book/text/original.md').read()
s=_r.sub(r'- \*\*Anger\.\*\* Loss of power and influence\. Desire, or\s+Grief, folly, sorrow, uncertainty, and\n- \*\*Self-slavery\.\*\* loneliness\.','- **Anger.** Loss of power and influence.\n- **Desire, or Self-slavery.** Grief, folly, sorrow, uncertainty, and loneliness.',s)
open('book/text/original.md','w').write(s)

s=open('book/text/original.md').read()
s=s.replace('=> JAMES ALLEN.\nBROAD PARK AVENUE,\nILFRACOMBE,\nENGLAND','=> JAMES ALLEN.\n\n=> Broad Park Avenue, Ilfracombe, England')
open('book/text/original.md','w').write(s)
s=open('book/text/original.md').read()
s=s.replace('his own mental in harmony.','his own mental inharmony.').replace('which are imminent in man','which are immanent in man')
open('book/text/original.md','w').write(s)
