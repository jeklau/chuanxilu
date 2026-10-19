import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import json,glob,sys
sys.path.insert(0,ROOT+'/tools')
from check import diff
raw1=json.load(open(ROOT+'/data/juan1_raw.json'))
raw3=json.load(open(ROOT+'/data/juan3_raw_n.json'))
R={e['n']:e for e in raw1['entries']}
R.update({e['n']:e for e in raw3['entries']})
ents=[];front=None;back=None
for f in sorted(glob.glob(ROOT+'/data/b*.json')):
    d=json.load(open(f))
    if 'front' in d: front=d['front']
    if 'back' in d: back=d['back']
    ents+=d['entries']
ents.sort(key=lambda e:e['n'])
want=list(range(1,130))+list(range(201,344))
assert [e['n'] for e in ents]==want,'entry set mismatch'
ns=set(want)
def kj(a,b):
    return [[x['op'][0],x['from'],x['to'],x['ctx']] for x in diff(a,b)]
tot=0
for e in ents:
    e.pop('s',None)
    e['rec']=R[e['n']]['rec']
    e['kj']=kj(R[e['n']]['text'],e['yw']); tot+=len(e['kj'])
    e['gl']=[g for g in dict.fromkeys(e.get('gl',[])) if g in ns and g!=e['n']]
front['intro']['kj']=[k for k in kj(raw1['intro'],front['intro']['yw']) if k[1]!='以下门人徐爱录']
front['ba']['kj']=kj(raw1['ba'],front['ba']['yw'])
back['kj']=kj(raw3['qian_ba'],back['yw'])
fk=len(front['intro']['kj'])+len(front['ba']['kj'])+len(back['kj'])
out={'front':front,'back':back,'entries':ents,'kjTotal':tot+fk,
     'kjByJuan':{'上':sum(len(e['kj']) for e in ents if e['n']<200)+len(front['intro']['kj'])+len(front['ba']['kj']),
                 '下':sum(len(e['kj']) for e in ents if e['n']>200)+len(back['kj'])}}
json.dump(out,open(ROOT+'/data/all.json','w'),ensure_ascii=False,separators=(',',':'))
print('entries',len(ents),'kj',out['kjByJuan'],'con',sum(1 for e in ents if e.get('con')),'size',os.path.getsize(ROOT+'/data/all.json'))
