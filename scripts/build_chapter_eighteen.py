"""Isolated P1-18 deterministic flat shapes; no self-approval."""
import copy, hashlib, json, math
import fitz
from build_primary_one_opening import ROOT, EXPECTED_HASH, read, Renderer, H
from check_chapter_standard import validate
OUT=ROOT/'output/chapter-18'
FILES={r:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Flat-shapes-{r.title()}.pdf' for r in ('textbook','workbook')}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class FlatRenderer(Renderer):
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.shapes=[]
 def element(self,el):
  if el['type']!='flat':return super().element(el)
  c=self.c;k=el['kind'];s=el.get('scale',1);x,y=el['x'],el['top'];a=math.radians(el.get('angle',0));r=dict(el,page=c.getPageNumber())
  c.saveState();c.setStrokeColorRGB(.16,.32,.51);c.setLineWidth(1.6)
  if k=='circle':
   radius=45*s;c.circle(x,H-y,radius,stroke=1,fill=0);r['circle']=[x,y,radius]
  else:
   w,h=(90*s,90*s) if k=='square' else (135*s,70*s)
   v=[[x+u*math.cos(a)-v*math.sin(a),y+u*math.sin(a)+v*math.cos(a)] for u,v in [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]]
   for i in range(4):u=v[i];z=v[(i+1)%4];c.line(u[0],H-u[1],z[0],H-z[1])
   r['vertices']=v
  c.restoreState();self.shapes.append(r)
 def verify(self):
  result=super().verify();doc=fitz.open(self.files[self.role]);ledger=[]
  for i,d in enumerate(self.shapes):
   pg=doc[d['page']-1];dr=pg.get_drawings();lines=[list(it[1])+list(it[2]) for g in dr for it in g['items'] if it[0]=='l']
   if 'vertices' in d:
    v=d['vertices'];edges=[v[(j+1)%4][0]-v[j][0] for j in range(4)]
    vec=[[v[(j+1)%4][z]-v[j][z] for z in [0,1]] for j in range(4)]
    lengths=[math.hypot(*e) for e in vec]
    assert all(abs(sum(vec[j][z]*vec[(j+1)%4][z] for z in [0,1]))<1e-6 for j in range(4))
    assert abs(lengths[0]-lengths[2])<1e-6 and abs(lengths[1]-lengths[3])<1e-6
    assert (abs(lengths[0]-lengths[1])<1e-6)==(d['kind']=='square')
    for j in range(4):
     expected=v[j]+v[(j+1)%4];assert any(all(abs(a-b)<.03 for a,b in zip(expected,l)) for l in lines),(d,'PDF edge missing')
    d['lengths']=lengths;d['right_angles']=4
   else:
    x,y,r=d['circle'];expected=[x-r,y-r,x+r,y+r]
    assert any(all(abs(a-b)<.03 for a,b in zip(expected,list(g['rect']))) and len([it for it in g['items'] if it[0]=='c'])==4 for g in dr),(d,'PDF circle missing')
   ledger.append(dict(id=f'{self.role}-shape-{i+1}',**d,actual_pdf_check='exact PDF endpoints/circular cubic bounds checked; polygon side lengths and adjacent dot products recomputed'))
  (self.out/'flat-geometry.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8');return result

def build():
 before=read('output/chapter-18/before.json');now=read('production/p1.json')
 assert sha(ROOT/'GombeTextbook.txt')==EXPECTED_HASH
 for i,(old,new) in enumerate(zip(before['lessons'],now)):
  if i!=17:assert old==new,new['id']
  else:
   base=copy.deepcopy(new);base.pop('paired_edition')
   for q in base['questions']:q.pop('id',None)
   assert base==old
  assert [(q['prompt'],q['answer']) for q in old['questions']]==[(q['prompt'],q['answer']) for q in new['questions']]
 for path,h in before['hashes'].items():assert sha(ROOT/path)==h,path
 assert read('research/supplementary_assessments.json')==before['supplements']
 lesson=now[17];pair=lesson['paired_edition'];assert pair['teacher_id']=='mr-aliyu'
 reports={r:FlatRenderer(r,pair[r+'_pages'],{'review_footer':'Flat shapes / Educational review edition'},[lesson],output_dir=OUT,files=FILES,label='Flat shapes').build() for r in FILES}
 assert pair['source_tasks']==[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in lesson['questions']]
 assert pair['supplementary_tasks']==[dict(id=s['id'],source_prompt=s['prompt'],source_answer=s['answer']) for s in before['supplements'] if s['id'] in ['S016','S017','S018','S019']]
 tasks=pair['author_content']['tasks'];ids={t['id'] for t in tasks};assert len(ids)==len(tasks)
 assert set().union(*(set(r['task_pages']) for r in reports.values()))==ids
 coverage=[]
 for t in tasks:
  answers={r:[n for n,p in enumerate(pair[r+'_pages'],1) if t['id'] in p.get('answer_ids',[])] for r in FILES if any(t['id'] in p.get('answer_ids',[]) for p in pair[r+'_pages'])};assert answers,t['id']
  for role,nums in answers.items():
   doc=fitz.open(FILES[role]);assert all(' '.join(t['answer'].split()) in ' '.join(doc[n-1].get_text().split()) for n in nums),t['id']
  coverage.append(dict(t,pages={r:v['task_pages'][t['id']] for r,v in reports.items() if t['id'] in v['task_pages']},answer_pages=answers))
 matrix={o:{m:[dict(id=t['id'],pages=next(x['pages'] for x in coverage if x['id']==t['id'])) for t in tasks if o in t['objectives'] and t['mode']==m] for m in ['model','guided','independent','recall','help','recheck','fresh','delayed']} for o in pair['objective_ids']};assert all(all(v.values()) for v in matrix.values())
 ledger=sum([read(f'output/chapter-18/{r}/flat-geometry.json') for r in FILES],[])
 for name,obj in [('task-coverage',coverage),('objective-matrix',matrix),('diagram-ledger',ledger)]:(OUT/f'{name}.json').write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 validate();result=dict(pages={r:v['pages'] for r,v in reports.items()},artifacts={r:str(p.relative_to(ROOT)).replace('\\','/') for r,p in FILES.items()},tasks=len(ids),diagrams=len(ledger),protected_hashes=len(before['hashes']),status='pending_independent_review',checks=['114 original pairs,18other lessons,175protected hashes and supplements preserved','all four objectives across eight progression modes','actual PDF geometry and every answer text checked','A4 fonts bounds and all pages rendered'])
 (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':build()
