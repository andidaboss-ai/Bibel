import sys,re
t=open('book/text/original.md',encoding='utf-8').read()
parts=re.split(r'(?m)^## ',t)[1:]
for n in sys.argv[1:]:
    print('=====',n,parts[int(n)-1][:4000])
