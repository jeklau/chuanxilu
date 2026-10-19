import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import json,glob,re,difflib,sys
raw=json.load(open(ROOT+'/data/juan1_raw.json'))
R={e['n']:e['text'] for e in raw['entries']}
try:
    R.update({e['n']:e['text'] for e in json.load(open(ROOT+'/data/juan3_raw_n.json'))['entries']})
except FileNotFoundError: pass
han=lambda s:''.join(c for c in s if '一'<=c<='鿿' or '㐀'<=c<='䶿')
def diff(a,b):
    a,b=han(a),han(b); out=[]
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal':continue
        ctx=a[max(0,i1-4):i1]
        out.append({'op':op,'from':a[i1:i2],'to':b[j1:j2],'ctx':ctx})
    return out
if __name__=='__main__':
    files=sorted(glob.glob(ROOT+'/data/b*.json'))
    tot=0;seen=set()
    only=[a for a in sys.argv[1:] if a.isdigit()]
    for f in files:
        d=json.load(open(f))
        if only and not any(f.endswith('b%02d.json'%int(o)) for o in only): continue
        for e in d['entries']:
            n=e['n'];seen.add(n)
            ds=diff(R[n],e['yw']);tot+=len(ds)
            if '-v' in sys.argv or any(len(x['from'])>6 or len(x['to'])>6 for x in ds):
                print(n,[(x['ctx'],x['from'],x['to']) for x in ds])
            for k in ['n','t','yw','bh','zs','q','a']:
                assert k in e,(n,k)
    print('entries',len(seen),'diffs',tot,'missing',len(set(R)-seen),sorted(set(R)-seen)[:8])
