"""Independent visible-face topology/actual-PDF checks; no chapter rebuild."""
import json,hashlib,math,itertools
from pathlib import Path
import pymupdf
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
freeze=read('output/chapter-17/author-freeze.json');hashes=freeze.get('hashes',freeze.get('source_hashes',{}))
for p,h in hashes.items():assert sha(ROOT/p)==h,p
chapter=read('production/chapter-reviews.json')['chapters'][16];lesson=read('production/p1.json')[16];pair=lesson['paired_edition']
artifacts={r:dict(path=p,sha256=hashes[p]) for r,p in chapter['artifacts'].items()}
pages=[];solids=[];shapes=[];tasks=[]
old={}
def near(a,b):return all(abs(x-y)<.025 for x,y in zip(a,b))
for role,a in artifacts.items():
 doc=pymupdf.open(ROOT/a['path']);assert len(doc)==len(pair[role+'_pages'])
 folder=OUT/'recovery-review-rasters'/role;folder.mkdir(parents=True,exist_ok=True)
 for n,src in enumerate(pair[role+'_pages'],1):
  pg=doc[n-1];drawings=pg.get_drawings();lines=[tuple(it[1])+tuple(it[2]) for d in drawings for it in d['items'] if it[0]=='l'];rects=[tuple(d['rect']) for d in drawings]
  def linehit(line):return any(near(line,z) or near(line,z[2:]+z[:2]) for z in lines)
  def recthit(rect):return any(near(rect,r) for r in rects)
  path=folder/f'{n:03}.png';pg.get_pixmap(matrix=pymupdf.Matrix(1.15,1.15),alpha=False).save(path);digest=sha(path)
  outside=[list(b[:4]) for b in pg.get_text('blocks') if b[0]<0 or b[1]<0 or b[2]>pg.rect.width or b[3]>pg.rect.height];assert not outside
  assert abs(pg.rect.width-595.276)<1 and abs(pg.rect.height-841.89)<1
  assert all(doc.extract_font(f[0])[3] for f in pg.get_fonts(full=True))
  for e in src['elements']:
   if e['type']=='line':
    target=(e['x1'],e['top1'],e['x2'],e['top2']);assert linehit(target),(role,n,target);shapes.append(dict(role=role,page=n,type='line',endpoints=target))
   elif e['type'] in ['box','ellipse']:
    target=(e['x'],e['top'],e['x']+e['width'],e['top']+e['height']);assert recthit(target),(role,n,target);shapes.append(dict(role=role,page=n,type=e['type'],rect=target))
   elif e['type']=='solid':
    kind=e['kind'];x,y,s=e['x'],e['top'],e.get('scale',1);variant=e.get('variant',0);ev=dict(role=role,page=n,kind=kind,x=x,y=y,scale=s,variant=variant)
    if kind in ['cube','non-cube cuboid']:
     dims=[70,70,70] if kind=='cube' else [110,52,65]
     if variant%2:dims[0],dims[1]=dims[1],dims[0]
     reflection=-1 if variant%3==1 else 1
     vertices={ijk:(x+reflection*math.sqrt(3)/2*(ijk[0]*dims[0]-ijk[1]*dims[1])*s,y+(ijk[0]*dims[0]/2+ijk[1]*dims[1]/2-ijk[2]*dims[2])*s) for ijk in itertools.product([0,1],repeat=3)}
     # Independently form three visible square/rectangular faces and take their edge union.
     faces=[];edgekeys=set()
     for fixed in range(3):
      axes=[i for i in range(3) if i!=fixed];cycle=[]
      for u,v in [(0,0),(1,0),(1,1),(0,1)]:
       corner=[0,0,0];corner[fixed]=1;corner[axes[0]]=u;corner[axes[1]]=v;cycle.append(tuple(corner))
      faces.append(cycle)
      for p,q in zip(cycle,cycle[1:]+cycle[:1]):edgekeys.add(tuple(sorted([p,q])))
     assert len(edgekeys)==9
     for p,q in edgekeys:assert linehit(vertices[p]+vertices[q]),(role,n,kind,p,q)
     assert (len(set(dims))==1)==(kind=='cube')
     ev.update(actual_3d_dimensions=dims,all_vertices={str(k):v for k,v in vertices.items()},visible_face_vertices=faces,visible_edges=len(edgekeys),actual_faces=6,actual_edges=12,actual_vertices=8,not_all_faces_visible=True)
    elif kind=='sphere':
     r=47*s;expected=[(x-r,y-r,x+r,y+r),(x-r,y-r/4,x+r,y+r/4)]
     assert all(recthit(z) for z in expected),(role,n,kind,expected)
     ev.update(silhouette_and_surface_curve=expected,flat_faces=0)
    elif kind=='cylinder':
     r,h,z=36*s,58*s,13*s
     if variant%2:
      sides=[(x-h,y-r,x+h,y-r),(x-h,y+r,x+h,y+r)];cap=(x-h-z,y-r,x-h+z,y+r);arc=(x+h,y-r,x+h+z,y+r)
     else:
      sides=[(x-r,y-h,x-r,y+h),(x+r,y-h,x+r,y+h)];cap=(x-r,y-h-z,x+r,y-h+z);arc=(x-r,y+h,x+r,y+h+z)
     assert all(linehit(z) for z in sides) and recthit(cap) and recthit(arc),(role,n,kind,sides,cap,arc)
     ev.update(joining_sides=sides,visible_full_circular_end=cap,far_end_visible_arc=arc,actual_circular_ends=2,curved_surface=1)
    else:raise AssertionError(kind)
    solids.append(ev)
  prior=old.get((role,n),{});pages.append(dict(role=role,page=n,pdf=a['path'],pdf_sha256=a['sha256'],image=str(path.relative_to(ROOT)).replace('\\','/'),image_sha256=digest,text=pg.get_text(),a4=True,embedded_fonts=True,outside_text=[],visual_inspected=prior.get('visual_inspected',False) and prior.get('image_sha256')==digest))
for t in pair['author_content']['tasks']:
 loc={r:[n for n,p in enumerate(pair[r+'_pages'],1) if t['id'] in p.get('task_ids',[])] for r in artifacts}
 ans={r:[n for n,p in enumerate(pair[r+'_pages'],1) if t['id'] in p.get('answer_ids',[])] for r in artifacts}
 assert any(loc.values()) and any(ans.values()),t['id'];tasks.append(dict(t,pupil_pages=loc,answer_pages=ans))
assert len(tasks)==len({t['id'] for t in tasks})
for objective in pair['objective_ids']:
 for mode in ['model','guided','independent','help','recheck','fresh','delayed']:assert any(objective in t['objectives'] and mode==t['mode'] for t in tasks),(objective,mode)
assert pair['source_tasks']==[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in lesson['questions']]
result=dict(reviewer='/root/chapter17_review_recovery',freeze=freeze,all_hashes_match=True,pages=len(pages),other_canonical_shapes=shapes,solid_geometry=solids,tasks=tasks,four_objectives_seven_modes=True,six_original_correspondences=True)
(OUT/'recovery-review-pages.json').write_text(json.dumps(pages,indent=2,ensure_ascii=False),encoding='utf-8')
(OUT/'recovery-review-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(dict(pages=len(pages),other_shapes=len(shapes),solids=len(solids),tasks=len(tasks),visual_inspected=sum(p['visual_inspected'] for p in pages))))
