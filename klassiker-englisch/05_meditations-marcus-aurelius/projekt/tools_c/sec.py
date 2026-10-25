import re,sys
t=open('book/text/original.md').read()
parts=re.split(r'^## (.+)$',t,flags=re.M)
books={}
for i in range(1,len(parts),2):
    secs={};cur=1;buf=[]
    for line in parts[i+1].split('\n'):
        m=re.match(r'^(\d+)\. ',line)
        if m: secs[cur]='\n'.join(buf).strip(); cur=int(m.group(1)); buf=[line[m.end():]]
        else: buf.append(line)
    secs[cur]='\n'.join(buf).strip()
    books[len(books)+1]=(parts[i],secs)
if __name__=='__main__':
    b=int(sys.argv[1])
    for s in sys.argv[2:]:
        print(f'--- {b},{s}:',books[b][1][int(s)][:1500])
