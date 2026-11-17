"""Independent frozen-source/PDF audit; only reviewer evidence outputs."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import re
from pathlib import Path
import fitz
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
BASE=OUT/'baseline'
def read(p): return json.loads(p.read_text('utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(b): return hashlib.sha256(b).hexdigest()
old=read(BASE/'production/p1.json'); new=read(ROOT/'production/p1.json')
ledger=read(OUT/'string-changes.json')
changes=[]
def diff(a,b,path=''):
    assert type(a)==type(b),(path,type(a),type(b))
    if isinstance(a,dict):
        assert a.keys()==b.keys(),path
        for k in a: diff(a[k],b[k],path+'/'+str(k))
    elif isinstance(a,list):
        assert len(a)==len(b),path
        for i,(x,y) in enumerate(zip(a,b)): diff(x,y,path+'/'+str(i))
    elif a!=b:
        assert isinstance(a,str),path
        assert re.findall(r'\d+',a)==re.findall(r'\d+',b),path
        changes.append(dict(path=path,before=a,after=b))
diff(old,new)
assert len(changes)==len(ledger)==167
assert {(c['path'],c['before'],c['after']) for c in changes}=={(c['path'],c['before'],c['after']) for c in ledger}
for a,b in zip(old,new):
    assert {k:v for k,v in a.items() if k!='paired_edition'}=={k:v for k,v in b.items() if k!='paired_edition'}
    assert a['paired_edition']['source_tasks']==b['paired_edition']['source_tasks']
    for role in ('textbook','workbook'):
        for p,q in zip(a['paired_edition'][role+'_pages'],b['paired_edition'][role+'_pages']):
            # Every assessed shape/count/coordinate and every font/geometry unchanged.
            def remove_prose(x):
                if isinstance(x,dict): return {k:remove_prose(v) for k,v in x.items() if k not in ('text','title','subtitle','kicker')}
                if isinstance(x,list): return [remove_prose(v) for v in x]
                return x
            assert remove_prose(p)==remove_prose(q),(b['id'],role,p['slug'])
reg=read(ROOT/'production/chapter-reviews.json')
records=[c for c in reg['chapters'] if c['id'].startswith('P1-')]+reg['annual_editions']
pdfs=sorted({p for c in records for p in c['artifacts'].values()})
authors=read(OUT/'changed-page-manifest.json')
author_lookup={(r['pdf'],r['page']):r for r in authors}
assert len(author_lookup)==1107
source_lookup={}
for lesson in new:
    c=next(c for c in records if c['id']==lesson['id'])
    for role,path in c['artifacts'].items():
        offset=(4 if role=='textbook' else 1) if lesson['id']=='P1-01' else ((10 if role=='textbook' else 5) if lesson['id']=='P1-02' else 0)
        for n,page in enumerate(lesson['paired_edition'][role+'_pages'],1):
            source_lookup[(path,n+offset)]=dict(chapter=lesson['id'],role=role,slug=page['slug'],task_ids=page.get('task_ids',[]),answer_ids=page.get('answer_ids',[]))
pages=[];changed=[]; frozen={}
for path in pdfs:
    frozen[path]=sha(ROOT/path)
    with fitz.open(ROOT/path) as current,fitz.open(BASE/path) as prior:
        assert len(current)==len(prior),path
        for n,(p,q) in enumerate(zip(current,prior),1):
            a=p.get_pixmap(matrix=fitz.Matrix(.7,.7),alpha=False).samples
            b=q.get_pixmap(matrix=fitz.Matrix(.7,.7),alpha=False).samples
            same=a==b; sametext=p.get_text()==q.get_text()
            row=dict(pdf=path,page=n,pixels_unchanged=same,text_unchanged=sametext,current_raster=digest(a),baseline_raster=digest(b))
            claim=author_lookup[(path,n)]
            assert claim['pixels_unchanged']==same and claim['text_unchanged']==sametext,(path,n)
            if not same:
                assert not sametext,(path,n,'unexplained graphical change')
                assert p.get_text()==claim['after_text'] and q.get_text()==claim['before_text']
                row['mapping']=source_lookup.get((path,n),claim.get('mapping'))
                if (path,n) in source_lookup:
                    dest=OUT/'reviewer-rasters'/Path(path).stem/f'{n:03}.png'
                    dest.parent.mkdir(exist_ok=True,parents=True)
                    p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(dest)
                    row.update(image=dest.relative_to(ROOT).as_posix(),image_sha256=sha(dest),text=p.get_text())
                    changed.append(row)
            pages.append(row)
assert len(changed)==85
maps=read(ROOT/'output/annual-edition/source-page-map.json')
prior_maps=read(OUT/'reviewer-prior-annual.json')['maps']
assert maps==prior_maps['source-page-map.json']
assert read(ROOT/'output/annual-edition/new-page-map.json')==prior_maps['new-page-map.json']
annual_paths=records[-1]['artifacts']
annual_docs={r:fitz.open(ROOT/p) for r,p in annual_paths.items()}
source_docs={p:fitz.open(ROOT/p) for p in pdfs if p not in annual_paths.values()}
annual_continuity=[]
for row in maps:
    if not row.get('annual_page'): continue
    p=source_docs[row['source_pdf']][row['source_page']-1]
    q=annual_docs[row['artifact']][row['annual_page']-1]
    clip=fitz.Rect(0,18,p.rect.width,p.rect.height)
    a=p.get_pixmap(matrix=fitz.Matrix(.85,.85),clip=clip,alpha=False).samples
    b=q.get_pixmap(matrix=fitz.Matrix(.85,.85),clip=clip,alpha=False).samples
    assert a==b,(row['artifact'],row['annual_page'],'source body mismatch')
    baseline=fitz.open(BASE/annual_paths[row['artifact']])
    header=fitz.Rect(0,0,q.rect.width,18)
    assert q.get_pixmap(matrix=fitz.Matrix(1,1),clip=header).samples==baseline[row['annual_page']-1].get_pixmap(matrix=fitz.Matrix(1,1),clip=header).samples
    baseline.close()
    annual_continuity.append(dict(row,body_verified=True,header_baseline_identical=True))
assert len(annual_continuity)==508

# Four full pages per contact sheet; exact extracted text is reviewed separately.
for batch in range(0,len(changed),4):
    sheet=Image.new('RGB',(1222,1740),'#e5e7eb'); draw=ImageDraw.Draw(sheet)
    for j,row in enumerate(changed[batch:batch+4]):
        x=10+(j%2)*606;y=10+(j//2)*865
        draw.text((x,y),f"{batch+j:02} {row['mapping']['chapter']} {row['mapping']['role']} {row['page']}",fill='black')
        sheet.paste(Image.open(ROOT/row['image']),(x,y+18))
    sheet.save(OUT/f'reviewer-contact-{batch//4+1:02}.png')
(OUT/'reviewer-pages.json').write_text(json.dumps(pages,indent=2)+'\n',encoding='utf-8')
(OUT/'reviewer-changed-pages.json').write_text(json.dumps(changed,indent=2)+'\n',encoding='utf-8')
(OUT/'reviewer-annual-continuity.json').write_text(json.dumps(annual_continuity,indent=2)+'\n',encoding='utf-8')
(OUT/'reviewer-freeze.json').write_text(json.dumps(dict(pdf_hashes=frozen,source_hashes={p:sha(ROOT/p) for p in ('production/p1.json','production/lessons.json','production/p1-opening.json','production/p1-annual.json','scripts/build_primary_one_localised.py')},canonical_leaf_changes=changes),indent=2)+'\n',encoding='utf-8')
print('PASS:167 exact prose-only differences,unchanged mathematical geometry;1107 independent full-page comparisons,85 revised source pages;508 annual bodies+headers exact;annual maps unchanged.')
