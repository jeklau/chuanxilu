import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import json,glob,sys
sys.path.insert(0,ROOT+'/tools')
from check import diff
raw=json.load(open(ROOT+'/data/juan1_raw.json'))
R={e['n']:e for e in raw['entries']}
ents=[];front=None
for f in sorted(glob.glob(ROOT+'/data/b*.json')):
    d=json.load(open(f))
    if 'front' in d: front=d['front']
    ents+=d['entries']
ents.sort(key=lambda e:e['n'])
assert [e['n'] for e in ents]==list(range(1,130))
ns=set(range(1,130))
def kj(a,b):
    out=[]
    for x in diff(a,b):
        out.append([x['op'][0],x['from'],x['to'],x['ctx']])
    return out
tot=0
for e in ents:
    e['rec']=R[e['n']]['rec']
    e['kj']=kj(R[e['n']]['text'],e['yw']); tot+=len(e['kj'])
    e['gl']=[g for g in e.get('gl',[]) if g in ns and g!=e['n']]
front['intro']['kj']=[k for k in kj(raw['intro'],front['intro']['yw']) if k[1]!='以下门人徐爱录']
front['ba']['kj']=kj(raw['ba'],front['ba']['yw'])
out={'juan':'卷上','front':front,'entries':ents,'kjTotal':tot+len(front['intro']['kj'])+len(front['ba']['kj'])}
json.dump(out,open(ROOT+'/data/juan1.json','w'),ensure_ascii=False,separators=(',',':'))
print('entries',len(ents),'kj',out['kjTotal'],'con',sum(1 for e in ents if e.get('con')),'yong',sum(1 for e in ents if e.get('yong')))
import os;print(os.path.getsize(ROOT+'/data/juan1.json'))
