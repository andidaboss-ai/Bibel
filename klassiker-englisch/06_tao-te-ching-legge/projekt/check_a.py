import re,sys
D='/tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/tao/book/text/'
def norm(s): return re.sub(r'\s+',' ',s).strip()
orig=open(D+'original.md',encoding='utf-8').read()
oc={}
for m in re.finditer(r'^## Chapter (\d+)\n(.*?)(?=^## Chapter |\Z)',orig,re.S|re.M):
    oc[int(m.group(1))]=norm(re.sub(r'^\| ','',m.group(2),flags=re.M))
txt=open(D+'chapters_a.md',encoding='utf-8').read()
parts=re.split(r'^## Chapter (\d+)\s*$',txt,flags=re.M)
nums=[int(x) for x in parts[1::2]]
errs=0
if nums!=list(range(1,28)): print('BAD ORDER',nums); errs+=1
wc=lambda s: len(re.findall(r"[\w'’-]+",s))
tot=0
for n,body in zip(nums,parts[2::2]):
    secs=re.split(r'^### (.+)$',body,flags=re.M)
    names=secs[1::2]
    if names!=['Reflection','Practice','Key Line']: print(n,'BAD SECTIONS',names); errs+=1; continue
    r,p,k=[s.strip() for s in secs[2::2]]
    rw,pw=wc(r),wc(p); tot+=wc(body)
    if not 70<=rw<=140: print(n,'reflection words',rw); errs+=1
    if not 25<=pw<=60: print(n,'practice words',pw); errs+=1
    q=norm(re.sub(r'^>\s?','',k,flags=re.M))
    if not k.startswith('>') or q not in oc[n]: print(n,'QUOTE MISS:',q); errs+=1
    print(f'Ch {n}: refl {rw}, prac {pw}')
print('total words',tot,'errors',errs)
