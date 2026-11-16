"""Isolated P1-17 pair; exact 3D geometry and actual PDF checks; no self-approval."""
import copy, hashlib, json, math
import fitz
from build_primary_one_opening import ROOT, EXPECTED_HASH, read, Renderer, H
from check_chapter_standard import validate
OUT=ROOT/'output/chapter-17'
FILES={r:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Solid-shapes-{r.title()}.pdf' for r in ('textbook','workbook')}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def box_geometry(el):
 cube=el['kind']=='cube'; a,b,c=(70,70,70) if cube else (110,52,65)
 v=el.get('variant',0)
 if v%2:a,b=b,a
 # Isometric projection of orthogonal three-dimensional unit vectors.
 s=el.get('scale',1); x,y=el['x'],el['top']; sign=-1 if v%3==1 else 1
 def project(i,j,k):return [x+sign*math.sqrt(3)/2*(i*a-j*b)*s,y+(.5*(i*a+j*b)-k*c)*s]
 vertices={(i,j,k):project(i,j,k) for i in (0,1) for j in (0,1) for k in (0,1)}
 # Three visible faces meeting at the near lower vertex; no hidden edges.
 edges=[]
 for key,p in vertices.items():
  for dim in range(3):
   if key[dim]:continue
   q=list(key);q[dim]=1;q=tuple(q)
   # Top, front and right outside faces; skip three back-hidden edges.
   if (key[0]==0 and q[0]==0 and key[1]==0 and q[1]==0) or (key[0]==0 and q[0]==0 and key[2]==0 and q[2]==0) or (key[1]==0 and q[1]==0 and key[2]==0 and q[2]==0):continue
   edges.append(p+vertices[q])
 assert len(edges)==9
 return dict(lengths=[a,b,c],vertices=list(vertices.values()),lines=edges)
class SolidRenderer(Renderer):
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.solids=[]
 def element(self,el):
  if el['type']!='solid':return super().element(el)
  c=self.c;x=el['x'];y=el['top'];s=el.get('scale',1);kind=el['kind'];record=dict(el,page=c.getPageNumber())
  c.saveState();c.setStrokeColorRGB(.16,.32,.51);c.setLineWidth(1.5)
  if kind in ['cube','non-cube cuboid']:
   g=box_geometry(el)
   for a,b,d,e in g['lines']:c.line(a,H-b,d,H-e)
   record.update(g)
  elif kind=='sphere':
   r=47*s;c.circle(x,H-y,r,stroke=1,fill=0)
   c.ellipse(x-r,H-y-r*.25,x+r,H-y+r*.25,stroke=1,fill=0)
   record['ellipses']=[[x-r,y-r,2*r,2*r],[x-r,y-r*.25,2*r,r*.5]]
  elif kind=='cylinder':
   # Upright/sideways rotations of the same closed circular cylinder.
   radius=36*s;half=58*s;depth=13*s
   sideways=el.get('variant',0)%2
   c.translate(x,H-y)
   if sideways:c.rotate(90)
   c.ellipse(-radius,half-depth,radius,half+depth,fill=0,stroke=1)
   c.line(-radius,half,-radius,-half);c.line(radius,half,radius,-half)
   c.arc(-radius,-half-depth,radius,-half+depth,startAng=180,extent=180)
   record.update(radius=radius,half=half,depth=depth,sideways=bool(sideways))
  else:raise ValueError(kind)
  c.restoreState();self.solids.append(record)
 def verify(self):
  result=super().verify();doc=fitz.open(self.files[self.role]);evidence=[]
  for index,d in enumerate(self.solids):
   p=doc[d['page']-1];lines=[];rects=[]
   for g in p.get_drawings():
    rects.append(list(g['rect']))
    for it in g['items']:
     if it[0]=='l':lines.append([it[1].x,it[1].y,it[2].x,it[2].y])
   if d['kind'] in ['cube','non-cube cuboid']:
    assert all(any(all(abs(a-b)<.025 for a,b in zip(edge,actual)) for actual in lines) for edge in d['lines']),(self.role,d)
    assert (len(set(d['lengths']))==1)==(d['kind']=='cube')
   elif d['kind']=='sphere':
    for x,y,w,h in d['ellipses']:assert any(all(abs(a-b)<.025 for a,b in zip([x,y,x+w,y+h],r)) for r in rects),(self.role,d)
   else:
    x,y,r,h,z=d['x'],d['top'],d['radius'],d['half'],d['depth']
    if not d['sideways']:
     expected=[[x-r,y-h,x-r,y+h],[x+r,y-h,x+r,y+h]];top=[x-r,y-h-z,x+r,y-h+z];far=[x-r,y+h,x+r,y+h+z]
    else:
     expected=[[x-h,y+r,x+h,y+r],[x-h,y-r,x+h,y-r]];top=[x-h-z,y-r,x-h+z,y+r];far=[x+h,y-r,x+h+z,y+r]
    for edge in expected:assert any(all(abs(a-b)<.025 for a,b in zip(edge,l)) or all(abs(a-b)<.025 for a,b in zip(edge,l[2:]+l[:2])) for l in lines),(d,edge,lines)
    assert any(all(abs(a-b)<.025 for a,b in zip(top,rct)) for rct in rects),(d,'circular end')
    assert any(all(abs(a-b)<.025 for a,b in zip(far,rct)) for rct in rects),(d,'far-end semicircular arc')
   evidence.append(dict(id=f'{self.role}-solid-{index+1}',**d,actual_pdf_check='exact visible box edges / circular outlines / cylinder sides and end verified from PDF vectors'))
  (self.out/'solid-geometry.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8');return result
def build():
 before=read('output/chapter-17/before.json');now=read('production/p1.json')
 assert sha(ROOT/'GombeTextbook.txt')==EXPECTED_HASH
 for i,(old,new) in enumerate(zip(before['lessons'],now)):
  if i!=16:assert old==new,new['id']
  else:
   base=copy.deepcopy(new);base.pop('paired_edition')
   for q in base['questions']:q.pop('id',None)
   assert base==old
  assert [(q['prompt'],q['answer']) for q in old['questions']]==[(q['prompt'],q['answer']) for q in new['questions']]
 for path,h in before['hashes'].items():assert sha(ROOT/path)==h,path
 assert read('research/supplementary_assessments.json')==before['supplements']
 lesson=now[16];pair=lesson['paired_edition'];assert pair['teacher_id']=='ms-binta'
 reports={r:SolidRenderer(r,pair[r+'_pages'],{'review_footer':'Solid shapes / Educational review edition'},[lesson],output_dir=OUT,files=FILES,label='Solid shapes').build() for r in FILES}
 assert pair['source_tasks']==[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in lesson['questions']]
 assert pair['supplementary_tasks']==[dict(id=s['id'],source_prompt=s['prompt'],source_answer=s['answer']) for s in before['supplements'] if s['id'] in ['S014','S015']]
 tasks=pair['author_content']['tasks'];ids={t['id'] for t in tasks};assert len(ids)==len(tasks)
 assert set().union(*(set(r['task_pages']) for r in reports.values()))==ids
 coverage=[]
 for t in tasks:
  answers={r:[n for n,p in enumerate(pair[r+'_pages'],1) if t['id'] in p.get('answer_ids',[])] for r in FILES if any(t['id'] in p.get('answer_ids',[]) for p in pair[r+'_pages'])};assert answers,t['id']
  for role,nums in answers.items():
   doc=fitz.open(FILES[role]);assert all(' '.join(t['answer'].split()) in ' '.join(doc[n-1].get_text().split()) for n in nums),t['id']
  coverage.append(dict(t,pages={r:v['task_pages'][t['id']] for r,v in reports.items() if t['id'] in v['task_pages']},answer_pages=answers))
 matrix={o:{m:[dict(id=t['id'],pages=next(x['pages'] for x in coverage if x['id']==t['id'])) for t in tasks if o in t['objectives'] and t['mode']==m] for m in ['model','guided','independent','help','recheck','fresh','delayed']} for o in pair['objective_ids']};assert all(all(v.values()) for v in matrix.values())
 ledger=sum([read(f'output/chapter-17/{r}/solid-geometry.json') for r in FILES],[])
 for name,obj in [('task-coverage',coverage),('objective-matrix',matrix),('diagram-ledger',ledger)]:(OUT/f'{name}.json').write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 validate();result=dict(pages={r:v['pages'] for r,v in reports.items()},artifacts={r:str(p.relative_to(ROOT)).replace('\\','/') for r,p in FILES.items()},tasks=len(ids),diagrams=len(ledger),protected_hashes=len(before['hashes']),status='pending_independent_review',checks=['114 original pairs,18other lessons,172protected hashes and supplements preserved','all four objectives across seven progression modes','actual PDF geometry and every answer text checked','A4 fonts bounds and all pages rendered'])
 (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':build()
