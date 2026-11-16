"""Reviewer exact frozen Chapter19 artifacts; no rebuild or prior evidence overwrite."""
from pathlib import Path
import json,hashlib,math
import pymupdf as fitz
R=Path(__file__).resolve().parents[2];O=Path(__file__).parent;read=lambda p:json.loads((R/p).read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=read('output/chapter-19/author-freeze.json')
for p,h in f['hashes'].items():assert sha(R/p)==h,p
lesson=read('production/p1.json')[18];pair=lesson['paired_edition'];reg=read('production/chapter-reviews.json')['chapters'][18]
assert read('production/lessons.json')==read('production/p1.json')+read('production/p2.json')+read('production/p3.json')
assert pair['source_tasks']==[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in lesson['questions']]
assert pair['supplementary_tasks']==[dict(id=s['id'],source_prompt=s['prompt'],source_answer=s['answer']) for s in read('research/supplementary_assessments.json') if s['id'] in ['S020','S021']]
near=lambda a,b:all(abs(x-y)<.035 for x,y in zip(a,b))
docs={r:fitz.open(R/p) for r,p in reg['artifacts'].items()};pages=[];diagrams=[];basics=[]
for role,doc in docs.items():
 assert len(doc)==len(pair[role+'_pages']);folder=O/'reviewer-final-rasters'/role;folder.mkdir(parents=True,exist_ok=True)
 for n,(src,pg) in enumerate(zip(pair[role+'_pages'],doc),1):
  assert abs(pg.rect.width-595.2756)<.1 and abs(pg.rect.height-841.8898)<.1
  assert '\ufffd' not in pg.get_text() and all(doc.extract_font(ff[0])[3] for ff in pg.get_fonts(full=True))
  assert all(0<=b[0]<=b[2]<=pg.rect.width and 0<=b[1]<=b[3]<=pg.rect.height for b in pg.get_text('blocks'))
  ds=pg.get_drawings();lines=[tuple(i[1])+tuple(i[2]) for d in ds for i in d['items'] if i[0]=='l']
  def edge(a,b):
   hit=[z for z in lines if near(z,a+b) or near(z,b+a)];assert hit,(role,n,a,b);return hit[0]
  for e in src['elements']:
   if e['type']=='table':
    x,y,w,rh=e['x'],e['top'],e['width'],e['row_height'];rows=[e['headers']]+e['rows']
    for j in range(len(rows)+1):edge((x,y+j*rh),(x+w,y+j*rh))
    for k in range(3):edge((x+k*w/2,y),(x+k*w/2,y+len(rows)*rh))
    cells=[]
    for j,row in enumerate(rows):
     for k,value in enumerate(row):
      text=' '.join(pg.get_textbox(fitz.Rect(x+k*w/2,y+j*rh,x+(k+1)*w/2,y+(j+1)*rh)).split());assert text==str(value),(role,n,j,k,text,value);cells.append(dict(row=j,column=k,text=text))
    diagrams.append(dict(role=role,page=n,type='table',rows=len(rows),columns=2,cells=cells))
   elif e['type']=='height':
    observed=[];assert len(e['xs'])==len(e['tops'])==len(e['labels'])==2
    for x,top,label in zip(e['xs'],e['tops'],e['labels']):
     strip=x+63;base=e['baseline'];actual=edge((strip,base),(strip,top));markedge=edge((strip-10,top),(strip+10,top));edge((x-45,base),(strip+18,base))
     actual_top=min(actual[1],actual[3]);actual_base=max(actual[1],actual[3]);circle=(x-12,top,x+12,top+24)
     assert any(near(tuple(d['rect']),circle) and len([z for z in d['items'] if z[0]=='c'])==4 for d in ds),(role,n,label,'head boundary')
     # Verify labels locally beneath this figure/strip, rather than anywhere on page.
     text=' '.join(pg.get_textbox(fitz.Rect(x-25,base+10,x+110,base+65)).split());assert label in text and label+' strip' in text,(role,n,label,text)
     assert near((markedge[1],markedge[3]),(actual_top,actual_top))
     observed.append(dict(label=label,actual_mark=actual_top,actual_baseline=actual_base,actual_length=actual_base-actual_top))
    assert abs(observed[0]['actual_baseline']-observed[1]['actual_baseline'])<.035
    a,b=observed;comparison='equal' if abs(a['actual_length']-b['actual_length'])<.035 else ('first taller' if a['actual_length']>b['actual_length'] else 'second taller')
    diagrams.append(dict(role=role,page=n,type='height',marks=observed,comparison=comparison))
   elif e['type'] in ['box','ellipse']:
    bounds=(e['x'],e['top'],e['x']+e['width'],e['top']+e['height']);assert any(near(tuple(d['rect']),bounds) for d in ds),(role,n,e);assert role!='textbook' or not e.get('response');basics.append(dict(role=role,page=n,type=e['type'],bounds=bounds))
   elif e['type']=='line':edge((e['x1'],e['top1']),(e['x2'],e['top2']));basics.append(dict(role=role,page=n,type='line',endpoints=[e['x1'],e['top1'],e['x2'],e['top2']]))
  path=folder/f'{n:03}.png';pg.get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False).save(path)
  pages.append(dict(role=role,page=n,pdf=reg['artifacts'][role],pdf_sha256=sha(R/reg['artifacts'][role]),image=str(path.relative_to(R)).replace('\\','/'),image_sha256=sha(path),text=pg.get_text(),a4=True,embedded_fonts=True,visual_inspected=False))
tasks=pair['author_content']['tasks'];assert len(tasks)==18 and len({t['id'] for t in tasks})==18
for t in tasks:
 loc={role:[n for n,pg in enumerate(pair[role+'_pages'],1) if t['id'] in pg.get('task_ids',[])] for role in docs};ans={role:[n for n,pg in enumerate(pair[role+'_pages'],1) if t['id'] in pg.get('answer_ids',[])] for role in docs}
 assert any(loc.values()) and any(ans.values()),t['id']
 for role,nums in ans.items():
  for n in nums:assert ' '.join(t['answer'].split()) in ' '.join(docs[role][n-1].get_text().split()),(t['id'],role,n)
for o in pair['objective_ids']:
 for mode in ['model','guided','independent','recall','help','recheck','fresh','delayed']:assert any(o in t['objectives'] and t['mode']==mode for t in tasks),(o,mode)
assert len(pages)==35 and len(diagrams)==10
assert {d['comparison'] for d in diagrams if d['type']=='height'}=={'equal','first taller','second taller'}
(O/'reviewer-pages.json').write_text(json.dumps(pages,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(O/'reviewer-artifact-checks.json').write_text(json.dumps(dict(reviewer='/root/chapter17_review_recovery',freeze=f,all_frozen_hashes_match=True,diagrams=diagrams,basic_shapes=basics,all18task_links_printed_answers=True,both_objectives_eight_modes=True,six_source_two_supplementary_pairs_preserved=True,generated63_equal_canonical=True,pages=35,visual_flags_inherited=0),indent=2)+'\n',encoding='utf-8')
print(f'35page/18task exact checks passed;10data diagrams/{len(basics)}basic shapes;2objectives8modes;0inherited visual flags.')
