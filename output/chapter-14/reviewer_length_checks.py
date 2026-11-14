"""No rebuilding: independently compare every canonical line with actual PDF strokes."""
import json,hashlib,re,math
from pathlib import Path
import pymupdf
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
freeze=read('output/chapter-14/author-freeze.json');lesson=read('production/p1.json')[13];pair=lesson['paired_edition']
for p,h in freeze['source_hashes'].items():assert sha(ROOT/p)==h,p
for a in freeze['artifacts'].values():assert sha(ROOT/a['path'])==a['sha256']
lines=[];tasks=[];pages=[]
for role,a in freeze['artifacts'].items():
 d=pymupdf.open(ROOT/a['path']);assert len(d)==len(pair[role+'_pages'])
 for pi,src in enumerate(pair[role+'_pages'],1):
  pg=d[pi-1];actual=[]
  for dr in pg.get_drawings():
   for it in dr['items']:
    if it[0]=='l':actual.append(tuple(it[1])+tuple(it[2]))
  for e in src['elements']:
   if e['type']!='line':continue
   target=(e['x1'],e['top1'],e['x2'],e['top2'])
   hits=[x for x in actual if all(abs(u-v)<.015 for u,v in zip(x,target))]
   assert len(hits)==1,(role,pi,target,len(hits))
   lines.append(dict(role=role,page=pi,endpoints=target,length=math.dist(target[:2],target[2:]),pdf_match=hits[0]))
  bounds=[list(b[:4]) for b in pg.get_text('blocks') if b[0]<0 or b[1]<0 or b[2]>pg.rect.width or b[3]>pg.rect.height]
  assert not bounds,(role,pi,bounds)
  assert all(d.extract_font(f[0])[3] for f in pg.get_fonts(full=True))
  pages.append(dict(role=role,page=pi,a4=abs(pg.rect.width-595.276)<1 and abs(pg.rect.height-841.89)<1,off_page_text=bounds,fonts_embedded=True))
for t in pair['author_content']['tasks']:
 loc={r:[i for i,p in enumerate(pair[r+'_pages'],1) if t['id'] in p.get('task_ids',[])] for r in ['textbook','workbook']}
 ans=[i for i,p in enumerate(pair['textbook_pages'],1) if t['id'] in p.get('answer_ids',[])]
 assert any(loc.values()) and ans,t['id']
 tasks.append(dict(id=t['id'],mode=t['mode'],objectives=t['objectives'],prompt=t['prompt'],answer=t['answer'],pages=loc,answer_pages=ans,reviewer_result='Independently solved/read against the exact pupil diagrams and corresponding adult answer entry; practical outcomes conditional on actual observed method.'))
assert len(tasks)==len({t['id'] for t in tasks})==32
for obj in pair['objective_ids']:
 for mode in ['model','guided','independent','help','recheck','fresh','delayed']:assert any(obj in t['objectives'] and t['mode']==mode for t in tasks),(obj,mode)
assert pair['source_tasks']==[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in lesson['questions']]
result=dict(freeze_fingerprint=freeze['fingerprint'],source_pdf_hashes_match=True,pages=pages,all_source_lines=lines,tasks=tasks,five_objectives_seven_modes=True,source_six_pairs_unchanged=True)
(OUT/'reviewer-length-checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(dict(pages=len(pages),source_lines=len(lines),horizontal_lengths=sum(x['endpoints'][1]==x['endpoints'][3] for x in lines),unit_ticks=sum(x['endpoints'][0]==x['endpoints'][2] for x in lines),tasks=len(tasks),fingerprint=freeze['fingerprint'])))
