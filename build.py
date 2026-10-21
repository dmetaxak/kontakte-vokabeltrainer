import json,re
from plural_en import en_plural
rows=[]
for line in open('data/vocab.md',encoding='utf-8'):
    if not line.startswith('|'): continue
    c=[x.strip() for x in line.strip().strip('|').split('|')]
    if len(c)!=6 or c[0]=='German' or set(c[0])<=set('-'): continue
    rows.append(dict(zip(['g','e','p','f','c','n'],c)))
ex=[l.rstrip('\n') for l in open('data/examples.txt',encoding='utf-8')]
assert len(ex)==len(rows)
for r,e in zip(rows,ex): r['x']=e
cur=None
for line in open('data/einfuehrung.txt',encoding='utf-8'):
    line=line.rstrip('\n')
    if not line: continue
    if line.startswith('#'): cur=line[1:]; continue
    g,e,p,f,n,de,en=line.split(';;')
    rows.append(dict(g=g,e=e,p=p,f=f.strip(),c=cur,n=n,x=de+'|'+en))
# ---- verbs ----
cz={}
for line in open('data/cloze.txt',encoding='utf-8'):
    line=line.rstrip('\n')
    if not line: continue
    i,p,de,en=line.split(';;')
    assert i not in cz and p in ('ich','du','er','wir','ihr','sie'),line
    assert de.count('___')==1,line
    cz[i]=dict(p=['ich','du','er','wir','ihr','sie'].index(p),de=de,en=en)
verbs=[]
for line in open('data/verbs.txt',encoding='utf-8'):
    line=line.rstrip('\n')
    if not line or line.startswith('#'): continue
    f=line.split(';;')
    assert len(f)==10,(len(f),line)
    lab,en,c,pre,aux,pt,du,er,full,only=f
    i=re.sub(r'\s*\(.*\)','',lab)
    if i=='möchten': pass
    v=dict(i=i,lab=lab if lab!=i else '',en=en,c=c,pre=pre,aux=aux.split('|') if aux else [],pt=pt,du=du,er=er,
           full=full.split(',') if full else None,only=[int(only)] if only else None)
    assert i in cz,'no cloze for '+i
    if v['full']: assert len(v['full'])==6,line
    if v['pt']: assert v['aux'],line
    if pre: assert i.startswith(pre),line
    v['cz']=cz.pop(i)
    verbs.append(v)
assert not cz,cz
assert len(set(v['i'] for v in verbs))==len(verbs)
vdata=json.dumps(verbs,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
# ---- accusative fill-in-the-blank ----
art_g={'der':'m','die':'f','das':'n'}
vocab_by={r['g']:r for r in rows}
acc=[]
seen=set()
for line in open('data/acc.txt',encoding='utf-8'):
    line=line.rstrip('\n')
    if not line or line.startswith('#'): continue
    b,cs,noun,de,en=line.split(';;')
    assert b in ('der','ein','kein','mein','dein','sein','ihr','unser','euer'),line
    assert cs in ('nom','acc'),line
    assert de.count('___')==1 and de not in seen or True,line
    pl=noun.startswith('pl:')
    n=noun[3:] if pl else noun
    assert n in vocab_by,'unknown noun '+n
    r=vocab_by[n]
    if pl:
        assert r['f'].startswith('die '),(n,r['f'])
        word=r['f'][4:]
        assert re.search(r'\b'+re.escape(word)+r'\b',de),(word,de)
        g='p'
        assert b!='ein',line
    else:
        g=art_g[n.split(' ')[0]]
        word=n.split(' ',1)[1]
        assert re.search(r'\b'+re.escape(word)+r'\b',de),(word,de)
    assert de.count('___')==1,line
    key=(b,cs,de)
    assert key not in seen,('duplicate',key)
    seen.add(key)
    acc.append(dict(b=b,cs=cs,g=g,n=n,w=word,de=de,en=en))
# ---- plural words: each plural is its own word with its own progress ----
have=set(r['g'] for r in rows)
plrows=[]
for r in list(rows):
    if r['p'].startswith('noun') and r['f'].startswith('die '):
        pg=r['f'].split(';')[0].strip()
        assert pg not in have,('plural already a word',pg)
        have.add(pg)
        plrows.append(dict(g=pg,e=en_plural(r['g'],r['e']),p='noun',f='',c=r['c'],n=r['n'],x='',pl=r['g']))
pex={}
for line in open('data/plural_ex.txt',encoding='utf-8'):
    line=line.rstrip('\n')
    if not line: continue
    g,de,en=line.split(';;')
    assert g not in pex,g
    bare=g[4:]
    assert re.search(r'(?<!\w)'+re.escape(bare)+r'(?!\w)',de),('plural missing',g,de)
    pex[g]=de+'|'+en
assert set(pex)==set(r['g'] for r in plrows),(set(pex)^set(r['g'] for r in plrows))
for r in plrows: r['x']=pex[r['g']]
rows.extend(plrows)
open('plurals_preview.txt','w',encoding='utf-8').write('\n'.join(r['pl']+' | '+r['e']+' -> '+r['g']+' | '+en_plural(r['pl'],[q['e'] for q in rows if q['g']==r['pl']][0]) for r in plrows))
pron=[]
PK=('1s','2s','3m','3f','3n','1p','2p','3p','fo')
for line in open('data/pron.txt',encoding='utf-8'):
    line=line.rstrip('\n')
    if not line or line.startswith('#'): continue
    cs,p,de,en=line.split(';;')
    assert cs in ('nom','acc') and p in PK,line
    assert de.count('___')==1,line
    pron.append(dict(cs=cs,p=p,de=de,en=en))
assert len(set((x['de'] for x in pron)))==len(pron),'duplicate pronoun sentence'
pdata=json.dumps(pron,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
adata=json.dumps(acc,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
data=json.dumps(rows,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
t=open('quiz-template.html',encoding='utf-8').read()
t=t.replace('/*VOCABDATA*/','window.VOCAB = '+data+';')
t=t.replace('/*VERBDATA*/','window.VERBS = '+vdata+';')
t=t.replace('/*PRONDATA*/','window.PRON = '+pdata+';')
t=t.replace('/*ACCDATA*/','window.ACC = '+adata+';')
open('kontakte-vokabeltrainer.html','w',encoding='utf-8').write(t)
# extract pure block for testing
m=re.search(r'//PURE_START(.*?)//PURE_END',t,re.S)
open('pure.js','w').write(m.group(1))
print(len(rows),len(verbs),len(acc),len(t))
