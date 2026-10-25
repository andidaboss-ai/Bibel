import re,json,os,glob,csv,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import bib,bible_data,classics_data
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../..')); OUT=REPO+'/marketing/x-content'
def norm_map(s):
    rep={'’':"'",'‘':"'",'“':'"','”':'"','*':''}
    out=[];idx=[];prev_space=False
    for i,ch in enumerate(s):
        ch=rep.get(ch,ch)
        if ch=='':continue
        if ch.isspace():
            if prev_space: continue
            ch=' ';prev_space=True
        else: prev_space=False
        out.append(ch);idx.append(i)
    return ''.join(out),idx
def exact(q,src):
    ns,idx=norm_map(src); nq,_=norm_map(q); nq=nq.strip()
    k=ns.find(nq)
    if k<0: return None
    return src[idx[k]:idx[k+len(nq)-1]+1]
def xlen(t): return sum(2 if ord(c)>=0x1100 else 1 for c in t)
EN={'1-Mose':'Genesis','2-Mose':'Exodus','Josua':'Joshua','Rut':'Ruth','1-Samuel':'1 Samuel','1-Koenige':'1 Kings','Ester':'Esther','Hiob':'Job','Psalmen':'Psalm','Sprueche':'Proverbs','Prediger':'Ecclesiastes','Jesaja':'Isaiah','Jeremia':'Jeremiah','Klagelieder':'Lamentations','Daniel':'Daniel','Jona':'Jonah','Micha':'Micah','Hosea':'Hosea','Matthaeus':'Matthew','Markus':'Mark','Lukas':'Luke','Johannes':'John','Roemer':'Romans','1-Korinther':'1 Corinthians','2-Korinther':'2 Corinthians','Galater':'Galatians','Epheser':'Ephesians','Philipper':'Philippians','Kolosser':'Colossians','2-Timotheus':'2 Timothy','Hebraeer':'Hebrews','Jakobus':'James','1-Petrus':'1 Peter','1-Johannes':'1 John','Offenbarung':'Revelation','Apostelgeschichte':'Acts','1-Thessalonicher':'1 Thessalonians'}
# corpora for inline-quote check
def corpus(files): return norm_map(' '.join(open(f).read() for f in files))[0].lower()
BIB_C=corpus(glob.glob(REPO+'/texte/plain-english/*/*/*.md'))
KQ=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'kq.json'))); KQd={(o['book'][:2],o['day']):o for o in KQ}
BOOKS={}
for d in sorted(glob.glob(REPO+'/klassiker-englisch/0*')):
    BOOKS[os.path.basename(d)[:2]]=d
CL_C=corpus([BOOKS[k]+'/projekt/book/text/original.md' for k in BOOKS])
AUTH={'01':('Florence Scovel Shinn','Your Word Is Your Wand'),'02':('Christian D. Larson','Your Forces and How to Use Them'),'03':('William Walker Atkinson','Thought Vibration'),'04':('Prentice Mulford','Thoughts Are Things'),'05':('Marcus Aurelius','Meditations'),'06':('Lao Tzu','Tao Te Ching'),'07':('Brother Lawrence','The Practice of the Presence of God'),'08':('Epictetus','Enchiridion / Discourses'),'09':('Thomas à Kempis','The Imitation of Christ')}
BSTYLE="Square 1:1 image (also works 16:9). Deep midnight-blue background with subtle grain, elegant thin gold line art, warm golden glow, calm and reverent mood, minimalist, matching the @BibleSimplyExpl profile banner. No people's faces in detail, no text except the optional title in a refined gold serif. Subject: "
CSTYLE="Square 1:1 image. Dark night sky full of faint stars, deep navy-to-black gradient, a single elegant gold line icon in the center, refined gold serif typography, premium book-cover feel matching the Ancient Book Wisdom cover series. No text except the optional title. Subject: "
TB={"Proverb of the Week":"13:00 UTC (08:00 ET / 13:00 UK)","Story in 60 Seconds":"17:00 UTC (12:00 ET / 17:00 UK)","What It Really Means":"12:00 UTC (07:00 ET / 12:00 UK)","Words of Jesus":"21:00 UTC (16:00 ET / 21:00 UK)","Myth vs. Truth":"18:00 UTC (13:00 ET / 18:00 UK)","Thread":"17:00 UTC (12:00 ET / 17:00 UK)","Your Turn (Question)":"00:30 UTC (19:30 ET, evening US)","Sunday Rest (Psalm)":"14:00 UTC (09:00 ET / 14:00 UK)"}
TC={"Stoic Mindset":"12:00 UTC (07:00 ET / 12:00 UK)","Tao for Busy Minds":"13:00 UTC (08:00 ET / 13:00 UK)","Mind Power Classics":"12:00 UTC (07:00 ET / 12:00 UK)","Quiet Faith":"21:00 UTC (16:00 ET / 21:00 UK)","Then vs. Now":"17:00 UTC (12:00 ET / 17:00 UK)","Thread":"17:00 UTC (12:00 ET / 17:00 UK)","Your Turn (Question)":"00:30 UTC (19:30 ET, evening US)","Book Spotlight":"14:00 UTC (09:00 ET / 14:00 UK)"}
problems=[]
def check_inline(day,ch,parts,corp):
    for p in parts:
        for m in re.finditer(r'"([^"]{20,})"',norm_map(p)[0]):
            s=m.group(1).strip().lower().rstrip('.…')
            if s not in corp: problems.append(f'{ch} day {day}: inline quote not in source: {m.group(1)[:70]}')
def strip_ins(p,sub):
    for k,v in sub.items():
        if k.startswith('q'): p=p.replace(v,'')
    return p
def write(ch,day,e,parts,sources,img,style,times,cta):
    for i,p in enumerate(parts):
        n=xlen(p)
        if n>280: problems.append(f'{ch} day {day} part {i+1}: {n} chars')
    thread=len(parts)>1
    L=[f"# Day {day:03d} – {e['t']}","",f"- **Series:** {e['s']}",f"- **Format:** {e['f']}"+(f" ({len(parts)} posts)" if thread else ""),f"- **Best time:** {times.get(e['s'],'13:00 UTC')}",f"- **CTA (link in bio):** {'yes' if cta else 'no'}",f"- **Image:** {'yes' if img else 'no'}",""]
    L.append("## Post" if not thread else "## Thread")
    for i,p in enumerate(parts):
        if thread: L.append(f"\n### Part {i+1}/{len(parts)} ({xlen(p)} chars)")
        else: L.append(f"\n_{xlen(p)} chars_")
        L.append("\n```text\n"+p+"\n```")
    if img:
        L+=["","## Image prompt","",style+img+".","","## Alt text","",f"Illustration: {img}."]
    L+=["","## Source (verified verbatim)",""]+([f"- {s}" for s in sources] or ["- No direct quote (engagement post)."])
    open(f"{OUT}/{ch}/day-{day:03d}.md","w").write('\n'.join(L)+'\n')
    return sources
def run():
    rows={'bible-simply-explained':[],'ancient-book-wisdom':[]}
    for ch in rows: os.makedirs(f'{OUT}/{ch}',exist_ok=True)
    for i,e in enumerate(bible_data.D,1):
        cta='link in bio' in ' '.join(e['p']).lower()
        sub={};srcs=[]
        for j,(q,ref) in enumerate(e['q']):
            bk,c,ab=ref.split(':'); a,*b=ab.split('-'); a=int(a); b=int(b[0]) if b else a
            v=bib.verses(bk,int(c)); txt=' '.join(v[k] for k in range(a,b+1))
            ex=exact(q,txt)
            if ex is None: problems.append(f'bible day {i}: quote not found in {ref}: {q[:60]}'); ex=q
            ex=ex.strip().strip('“”"').strip() if ex.count('“')!=ex.count('”') else ex
            sub[f'q{j}']=ex
            if j==0: sub['q']=ex
            d=[x for x in glob.glob(bib.R+'/*/*') if x.endswith('_'+bk)][0]
            srcs.append(f"{EN[bk]} {c}:{a}{'' if a==b else '–'+str(b)} — `{os.path.relpath(d,REPO)}/kapitel_{int(c):03d}.md`")
        parts=[p.replace('{q}',sub.get('q','')).replace('{q0}',sub.get('q0','')).replace('{q1}',sub.get('q1','')).replace('{q2}',sub.get('q2','')).replace('{q3}',sub.get('q3','')) for p in e['p']]
        check_inline(i,'bible',[strip_ins(p,sub) for p in parts],BIB_C)
        write('bible-simply-explained',i,e,parts,srcs,e['img'],BSTYLE,TB,cta)
        rows['bible-simply-explained'].append([i,e['t'],e['f'],'yes' if e['img'] else 'no','yes' if cta else 'no','; '.join(s.split(' — ')[0] for s in srcs)])
    for i,e in enumerate(classics_data.D,1):
        cta='link in bio' in ' '.join(e['p']).lower()
        sub={};srcs=[]
        for j,(bk,dy) in enumerate(e['k']):
            o=KQd[(bk,dy)]; q=o['quote']
            orig=open(BOOKS[bk]+'/projekt/book/text/original.md').read()
            ex=exact(q,orig)
            if ex is None: problems.append(f'classics day {i}: quote not in original.md {bk}: {q[:60]}'); ex=q
            au,ti=AUTH[bk]; a=au
            for key in ([f'q{j}','q'] if j==0 else [f'q{j}']): sub[key]=ex
            for key in ([f'a{j}','a'] if j==0 else [f'a{j}']): sub[key]=a
            srcs.append(f"{ti} ({au}) — {o['src']} — `klassiker-englisch/{os.path.basename(BOOKS[bk])}/projekt/book/text/original.md`")
        parts=[]
        for p in e['p']:
            for k in sorted(sub,key=len,reverse=True): p=p.replace('{'+k+'}',sub[k])
            parts.append(p)
        check_inline(i,'classics',[strip_ins(p,sub) for p in parts],CL_C)
        write('ancient-book-wisdom',i,e,parts,srcs,e['img'],CSTYLE,TC,cta)
        rows['ancient-book-wisdom'].append([i,e['t'],e['f'],'yes' if e['img'] else 'no','yes' if cta else 'no','; '.join(s.split(' — ')[0]+(' – '+s.split(' — ')[1]) for s in srcs)])
    for ch,r in rows.items():
        with open(f'{OUT}/{ch}/index.csv','w',newline='') as f:
            w=csv.writer(f); w.writerow(['day','title','format','image','cta','source']); w.writerows(r)
    print('\n'.join(problems) or 'ALL CHECKS PASSED'); print(len(problems),'problems')
run()
