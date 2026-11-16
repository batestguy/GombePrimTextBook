"""Fresh final-page rendering and independent actual-PDF balance geometry checks."""
import json,hashlib,math,html,re
from pathlib import Path
import pymupdf
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
plain=lambda s:' '.join(html.unescape(re.sub('<[^>]+>',' ',s)).split())
freeze=read('output/chapter-16/author-freeze.json');hashes=freeze.get('hashes',freeze.get('source_hashes',{}))
for p,h in hashes.items():assert sha(ROOT/p)==h,p
chapter=read('production/chapter-reviews.json')['chapters'][15];lesson=read('production/p1.json')[15];pair=lesson['paired_edition']
artifacts={r:dict(path=p,sha256=hashes[p]) for r,p in chapter['artifacts'].items()}
pages=[];shapes=[];balances={};tasks=[]
old={(p['role'],p['page']):p for p in read('output/chapter-16/reviewer-weight-pages.json')} if (OUT/'reviewer-weight-pages.json').exists() else {}
for role,a in artifacts.items():
 doc=pymupdf.open(ROOT/a['path']);assert len(doc)==len(pair[role+'_pages'])
 folder=OUT/'reviewer-rasters'/role;folder.mkdir(parents=True,exist_ok=True)
 for n,src in enumerate(pair[role+'_pages'],1):
  pg=doc[n-1];drawings=pg.get_drawings();actual=[tuple(it[1])+tuple(it[2]) for d in drawings for it in d['items'] if it[0]=='l']
  path=folder/f'{n:03}.png';pg.get_pixmap(matrix=pymupdf.Matrix(1.15,1.15),alpha=False).save(path);digest=sha(path)
  outside=[list(b[:4]) for b in pg.get_text('blocks') if b[0]<0 or b[1]<0 or b[2]>pg.rect.width or b[3]>pg.rect.height];assert not outside
  assert abs(pg.rect.width-595.276)<1 and abs(pg.rect.height-841.89)<1
  assert all(doc.extract_font(f[0])[3] for f in pg.get_fonts(full=True))
  source_lines=[]
  for e in src['elements']:
   if e['type']=='line':
    target=(e['x1'],e['top1'],e['x2'],e['top2']);source_lines.append(list(target))
    hits=[line for line in actual if all(abs(u-v)<.02 for u,v in zip(line,target))]
    assert hits,(role,n,target);shapes.append(dict(role=role,page=n,type='line',endpoints=target))
   elif e['type'] in ['box','ellipse']:
    target=(e['x'],e['top'],e['x']+e['width'],e['top']+e['height'])
    assert any(all(abs(u-v)<.02 for u,v in zip(d['rect'],target)) for d in drawings),(role,n,target)
    shapes.append(dict(role=role,page=n,type=e['type'],rect=target))
  for spec in pair['author_content']['diagrams']:
   if not all(line in source_lines for line in spec['lines']):continue
   labels=[]
   for i,label in enumerate(spec['labels']):
    choices=[e for e in src['elements'] if e['type']=='text' and plain(e['text'])==label and e.get('x')==(75 if i==0 else 355)]
    if len(choices)!=1:break
    e=choices[0];rect=pymupdf.Rect(e['x'],e['top'],e['x']+e.get('width',160),e['top']+50)
    actual_label=plain(pg.get_textbox(rect));assert actual_label==label,(role,n,label,actual_label);labels.append(actual_label)
   if len(labels)!=2:continue
   lines=spec['lines'];beam=lines[0];pivot=lines[1][:2];leftpan=lines[5];rightpan=lines[8]
   assert leftpan[1]==leftpan[3] and rightpan[1]==rightpan[3]
   assert abs(math.dist(beam[:2],pivot)-math.dist(beam[2:],pivot))<.001
   assert leftpan[1]-beam[1]==rightpan[1]-beam[3]==75
   lower='left' if leftpan[1]>rightpan[1] else 'right' if leftpan[1]<rightpan[1] else 'neither'
   assert lower==spec['lower']
   assert ('left' if beam[1]>beam[3] else 'right' if beam[1]<beam[3] else 'neither')==lower
   key=(role,n,tuple(beam),tuple(labels))
   balances[key]=dict(role=role,page=n,beam=beam,pivot=pivot,left_pan=leftpan,right_pan=rightpan,actual_labels=labels,lower_pan=lower,heavier_label=labels[0] if lower=='left' else labels[1] if lower=='right' else 'equal loads',equal_beam_arms=True,equal_suspension_drop=75)
  prior=old.get((role,n),{});pages.append(dict(role=role,page=n,pdf=a['path'],pdf_sha256=a['sha256'],image=str(path.relative_to(ROOT)).replace('\\','/'),image_sha256=digest,text=pg.get_text(),a4=True,embedded_fonts=True,outside_text=[],visual_inspected=prior.get('visual_inspected',False) and prior.get('image_sha256')==digest))
for t in pair['author_content']['tasks']:
 loc={r:[n for n,p in enumerate(pair[r+'_pages'],1) if t['id'] in p.get('task_ids',[])] for r in artifacts}
 ans={r:[n for n,p in enumerate(pair[r+'_pages'],1) if t['id'] in p.get('answer_ids',[])] for r in artifacts}
 assert any(loc.values()) and any(ans.values()),t['id']
 tasks.append(dict(t,pupil_pages=loc,answer_pages=ans))
assert len(tasks)==len({t['id'] for t in tasks})
for objective in pair['objective_ids']:
 for mode in ['model','guided','independent','help','recheck','fresh','delayed']:assert any(objective in t['objectives'] and mode==t['mode'] for t in tasks),(objective,mode)
assert pair['source_tasks']==[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in lesson['questions']]
result=dict(reviewer='/root/chapter14_review',freeze=freeze,all_hashes_match=True,pages=len(pages),shapes=shapes,unique_balance_instances=list(balances.values()),tasks=tasks,seven_modes=True,six_original_correspondences=True)
(OUT/'reviewer-weight-pages.json').write_text(json.dumps(pages,indent=2,ensure_ascii=False),encoding='utf-8')
(OUT/'reviewer-weight-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(dict(pages=len(pages),shapes=len(shapes),balances=len(balances),tasks=len(tasks),visual_inspected=sum(p['visual_inspected'] for p in pages))))
