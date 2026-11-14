"""Review-owned read-only artifact checks and fresh page rendering after root freeze."""
import json,hashlib,re,html
from pathlib import Path
import pymupdf
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def plain(s):return ' '.join(html.unescape(re.sub('<[^>]*>',' ',s)).split())
freeze=read('output/chapter-15/author-freeze.json');lesson=read('production/p1.json')[14];pair=lesson['paired_edition']
sourcehashes=freeze.get('source_hashes',freeze.get('hashes',{}))
for p,h in sourcehashes.items():assert sha(ROOT/p)==h,p
registered=read('production/chapter-reviews.json')['chapters'][14]['artifacts']
artifacts={role:dict(path=p,sha256=freeze['hashes'][p]) for role,p in registered.items()};pages=[];shapes=[];cards=[];tasks=[]
old={}
if (OUT/'reviewer-time-pages.json').is_file():old={(p['role'],p['page']):p for p in read('output/chapter-15/reviewer-time-pages.json')}
for role,a in artifacts.items():
 assert sha(ROOT/a['path'])==a['sha256'];doc=pymupdf.open(ROOT/a['path']);assert len(doc)==len(pair[role+'_pages'])
 folder=OUT/'reviewer-rasters'/role;folder.mkdir(parents=True,exist_ok=True)
 for n,src in enumerate(pair[role+'_pages'],1):
  pg=doc[n-1];drawings=pg.get_drawings();path=folder/f'{n:03}.png';pg.get_pixmap(matrix=pymupdf.Matrix(1.15,1.15),alpha=False).save(path);digest=sha(path)
  text=pg.get_text();outside=[list(b[:4]) for b in pg.get_text('blocks') if b[0]<0 or b[1]<0 or b[2]>pg.rect.width or b[3]>pg.rect.height]
  assert not outside,(role,n,outside)
  assert all(doc.extract_font(f[0])[3] for f in pg.get_fonts(full=True))
  assert abs(pg.rect.width-595.276)<1 and abs(pg.rect.height-841.89)<1
  for e in src['elements']:
   if e['type']=='box':
    target=(e['x'],e['top'],e['x']+e['width'],e['top']+e['height'])
    hits=[d for d in drawings if all(abs(u-v)<.02 for u,v in zip(d['rect'],target))]
    assert hits,(role,n,'box',target)
    shapes.append(dict(role=role,page=n,type='box',rect=target))
    labels=[x for x in src['elements'] if x['type']=='text' and x.get('x')==e['x']+10 and x.get('top')==e['top']+14]
    for label in labels:
     actual=plain(pg.get_textbox(pymupdf.Rect(target)));expected=plain(label['text']);assert actual==expected,(role,n,expected,actual)
     cards.append(dict(role=role,page=n,rect=target,text=actual))
   elif e['type']=='line':
    target=(e['x1'],e['top1'],e['x2'],e['top2']);actual=[tuple(it[1])+tuple(it[2]) for d in drawings for it in d['items'] if it[0]=='l']
    assert any(all(abs(u-v)<.02 for u,v in zip(line,target)) for line in actual),(role,n,target)
    shapes.append(dict(role=role,page=n,type='line',endpoints=target))
  previous=old.get((role,n),{});pages.append(dict(role=role,page=n,pdf=a['path'],pdf_sha256=a['sha256'],image=str(path.relative_to(ROOT)).replace('\\','/'),image_sha256=digest,text=text,a4=True,off_page_text=[],fonts_embedded=True,visual_inspected=previous.get('visual_inspected',False) and previous.get('image_sha256')==digest))
for t in pair['author_content']['tasks']:
 loc={r:[n for n,p in enumerate(pair[r+'_pages'],1) if t['id'] in p.get('task_ids',[])] for r in artifacts}
 ans={r:[n for n,p in enumerate(pair[r+'_pages'],1) if t['id'] in p.get('answer_ids',[])] for r in artifacts}
 assert any(loc.values()) and any(ans.values()),t['id']
 tasks.append(dict(id=t['id'],mode=t['mode'],objectives=t['objectives'],canonical_answer=t['answer'],pupil_pages=loc,answer_pages=ans))
assert len(tasks)==len({t['id'] for t in tasks})==18
for obj in pair['objective_ids']:
 for mode in ['model','guided','independent','help','recheck','fresh','delayed']:assert any(obj in t['objectives'] and mode==t['mode'] for t in tasks),(obj,mode)
assert pair['source_tasks']==[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in lesson['questions']]
result=dict(reviewer='/root/chapter14_review',freeze=freeze,source_pdf_hashes_match=True,shapes=shapes,cards=cards,tasks=tasks,two_objectives_seven_modes=True,source_six_correspondence=True)
(OUT/'reviewer-time-pages.json').write_text(json.dumps(pages,indent=2,ensure_ascii=False),encoding='utf-8')
(OUT/'reviewer-time-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(dict(pages=len(pages),shapes=len(shapes),cards=len(cards),task_ids=len(tasks),visual_inspected=sum(p['visual_inspected'] for p in pages))))
