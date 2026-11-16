"""Frozen Chapter18 exact artifact checks and fresh raster generation; no rebuilding."""
import json,hashlib,math
from pathlib import Path
import pymupdf as fitz
R=Path(__file__).resolve().parents[2];O=Path(__file__).parent
read=lambda p:json.loads((R/p).read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=read('output/chapter-18/author-freeze.json')
for p,h in f['hashes'].items():assert sha(R/p)==h,p
l=read('production/p1.json')[17];pair=l['paired_edition'];reg=read('production/chapter-reviews.json')['chapters'][17]
assert pair['source_tasks']==[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in l['questions']]
assert pair['supplementary_tasks']==[dict(id=s['id'],source_prompt=s['prompt'],source_answer=s['answer']) for s in read('research/supplementary_assessments.json') if s['id'] in ['S016','S017','S018','S019']]
assert read('production/lessons.json')==read('production/p1.json')+read('production/p2.json')+read('production/p3.json')
pages=[];shapes=[];basics=[];docs={r:fitz.open(R/p) for r,p in reg['artifacts'].items()}
near=lambda a,b:all(abs(x-y)<.035 for x,y in zip(a,b))
for role,doc in docs.items():
 assert len(doc)==len(pair[role+'_pages'])
 folder=O/'reviewer-final-rasters'/role;folder.mkdir(parents=True,exist_ok=True)
 for n,(src,pg) in enumerate(zip(pair[role+'_pages'],doc),1):
  assert abs(pg.rect.width-595.2756)<.1 and abs(pg.rect.height-841.8898)<.1
  assert '\ufffd' not in pg.get_text() and all(doc.extract_font(font[0])[3] for font in pg.get_fonts(full=True))
  assert all(0<=b[0]<=b[2]<=pg.rect.width and 0<=b[1]<=b[3]<=pg.rect.height for b in pg.get_text('blocks'))
  ds=pg.get_drawings();lines=[tuple(i[1])+tuple(i[2]) for d in ds for i in d['items'] if i[0]=='l'];flatbounds=[]
  for e in src['elements']:
   if e['type']=='flat':
    kind=e['kind'];x,y,s=e['x'],e['top'],e.get('scale',1)
    if kind=='circle':
     radius=45*s;target=(x-radius,y-radius,x+radius,y+radius)
     paths=[d for d in ds if near(tuple(d['rect']),target) and len([i for i in d['items'] if i[0]=='c'])==4];assert len(paths)==1,(role,n,e)
     b=list(paths[0]['rect']);assert abs(b[2]-b[0]-(b[3]-b[1]))<.035
     details=dict(radius=radius,flat_corners=0,straight_sides=0)
    else:
     w,h=(90*s,90*s) if kind=='square' else (135*s,70*s);angle=math.radians(e.get('angle',0));u=(math.cos(angle),math.sin(angle));v=(-math.sin(angle),math.cos(angle))
     vertices=[(x+sx*w/2*u[0]+sy*h/2*v[0],y+sx*w/2*u[1]+sy*h/2*v[1]) for sx,sy in [(-1,-1),(1,-1),(1,1),(-1,1)]]
     actual=[]
     for a,b in zip(vertices,vertices[1:]+vertices[:1]):
      hits=[z for z in lines if near(z,a+b) or near(z,b+a)];assert len(hits)==1,(role,n,e,a,b)
      z=hits[0];actual.append(z[:2] if near(z[:2],a) else z[2:])
     vectors=[(b[0]-a[0],b[1]-a[1]) for a,b in zip(actual,actual[1:]+actual[:1])];lengths=[math.hypot(*z) for z in vectors]
     assert all(abs(a[0]*b[0]+a[1]*b[1])<.1 for a,b in zip(vectors,vectors[1:]+vectors[:1]))
     assert abs(lengths[0]-lengths[2])<.035 and abs(lengths[1]-lengths[3])<.035
     assert (abs(lengths[0]-lengths[1])<.035)==(kind=='square')
     b=[min(z[0] for z in actual),min(z[1] for z in actual),max(z[0] for z in actual),max(z[1] for z in actual)]
     details=dict(actual_vertices=actual,actual_side_lengths=lengths,square_corners=4)
    assert 0<=b[0]<=b[2]<=pg.rect.width and 0<=b[1]<=b[3]<=pg.rect.height
    shapes.append(dict(role=role,page=n,kind=kind,bounds=b,**details));flatbounds.append(b)
   elif e['type'] in ['box','ellipse']:
    b=(e['x'],e['top'],e['x']+e['width'],e['top']+e['height']);assert any(near(tuple(d['rect']),b) for d in ds),(role,n,e)
    assert role!='textbook' or not e.get('response'),(role,n,'write-in-textbook')
    basics.append(dict(role=role,page=n,type=e['type'],bounds=b))
   elif e['type']=='line':
    z=(e['x1'],e['top1'],e['x2'],e['top2']);assert any(near(z,a) or near(z,a[2:]+a[:2]) for a in lines),(role,n,e)
    basics.append(dict(role=role,page=n,type='line',endpoints=z))
  if src['title']=='The cover has its border':
   assert len(flatbounds)==7;outer=flatbounds[0];assert all(outer[0]<=b[0] and outer[1]<=b[1] and b[2]<=outer[2] and b[3]<=outer[3] for b in flatbounds[1:]),(role,n,'story cover containment')
  path=folder/f'{n:03}.png';pg.get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False).save(path)
  pages.append(dict(role=role,page=n,pdf=reg['artifacts'][role],pdf_sha256=sha(R/reg['artifacts'][role]),image=str(path.relative_to(R)).replace('\\','/'),image_sha256=sha(path),text=pg.get_text(),a4=True,embedded_fonts=True,visual_inspected=False))
tasks=pair['author_content']['tasks'];assert len(tasks)==21 and len({t['id'] for t in tasks})==21
for t in tasks:
 places={role:[n for n,pg in enumerate(pair[role+'_pages'],1) if t['id'] in pg.get('task_ids',[])] for role in docs}
 answers={role:[n for n,pg in enumerate(pair[role+'_pages'],1) if t['id'] in pg.get('answer_ids',[])] for role in docs}
 assert any(places.values()) and any(answers.values()),t['id']
 for role,nums in answers.items():
  for n in nums:assert ' '.join(t['answer'].split()) in ' '.join(docs[role][n-1].get_text().split()),(t['id'],role,n)
 for o in pair['objective_ids']:
  for mode in ['model','guided','independent','recall','help','recheck','fresh','delayed']:assert any(o in q['objectives'] and q['mode']==mode for q in tasks),(o,mode)
assert len(pages)==38 and len(shapes)==64
(O/'reviewer-pages.json').write_text(json.dumps(pages,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(O/'reviewer-artifact-checks.json').write_text(json.dumps(dict(reviewer='/root/chapter17_review_recovery',freeze=f,all_hashes_match=True,flat_shape_occurrences=shapes,other_canonical_shapes=basics,all21task_links_and_printed_answer_texts=True,four_objectives_eight_modes=True,source_six_and_four_supplementary_pairs=True,both_story_covers_contain_all6_border_shapes=True,pages=38,visual_inspections_inherited=0),indent=2)+'\n',encoding='utf-8')
print(f'Frozen exact checks passed: {len(pages)} pages; {len(shapes)}flat shapes; {len(basics)}other shapes;21task links;4objectives/8modes. Fresh rasters ready,0visual flags inherited.')
