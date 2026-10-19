import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import json,glob,sys
sys.path.insert(0,ROOT+'/tools')
from check import diff
raw1=json.load(open(ROOT+'/data/juan1_raw.json'))
raw3=json.load(open(ROOT+'/data/juan3_raw_n.json'))
raw2=json.load(open(ROOT+'/data/juan2_raw.json'))
R={e['n']:e for e in raw1['entries']}
R.update({e['n']:e for e in raw3['entries']})
R.update({e['n']:e for e in raw2['entries']})
ents=[];front=None;back=None;front2=None;note=None
for f in sorted(glob.glob(ROOT+'/data/b*.json')):
    d=json.load(open(f))
    if 'front' in d: front=d['front']
    if 'back' in d: back=d['back']
    if 'front2' in d: front2=d['front2']
    if 'note' in d: note=d['note']
    ents+=d['entries']
ents.sort(key=lambda e:e['n'])
want=list(range(1,344))
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
front2['kj']=kj(raw2['qian_xu'],front2['yw'])
note['kj']=kj(raw2['yuanjing_ba'].replace('钱德洪跋：','',1),note['yw'])
fk=len(front['intro']['kj'])+len(front['ba']['kj'])+len(back['kj'])+len(front2['kj'])+len(note['kj'])
out={'front':front,'back':back,'front2':front2,'note':note,'entries':ents,'kjTotal':tot+fk,
     'kjByJuan':{'上':sum(len(e['kj']) for e in ents if e['n']<130)+len(front['intro']['kj'])+len(front['ba']['kj']),
                 '中':sum(len(e['kj']) for e in ents if 129<e['n']<201)+len(front2['kj'])+len(note['kj']),
                 '下':sum(len(e['kj']) for e in ents if e['n']>200)+len(back['kj'])}}
json.dump(out,open(ROOT+'/data/all.json','w'),ensure_ascii=False,separators=(',',':'))
print('entries',len(ents),'kj',out['kjByJuan'],'con',sum(1 for e in ents if e.get('con')),'size',os.path.getsize(ROOT+'/data/all.json'))
