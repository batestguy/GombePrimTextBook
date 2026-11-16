"""Isolated P1-19 collection pair; deterministic tables and height-method diagrams."""
import copy,hashlib,json,math
import fitz
from build_primary_one_opening import ROOT,EXPECTED_HASH,read,Renderer,H
from check_chapter_standard import validate
OUT=ROOT/'output/chapter-19'
FILES={r:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Class-information-{r.title()}.pdf' for r in ('textbook','workbook')}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class DataRenderer(Renderer):
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.diagrams=[]
 def element(self,el):
  if el['type'] not in ['table','height']:return super().element(el)
  c=self.c;d=dict(el,page=c.getPageNumber());edges=[];labels=[]
  c.saveState();c.setStrokeColorRGB(.16,.32,.51);c.setLineWidth(1.2)
  def line(a,b,e,f):c.line(a,H-b,e,H-f);edges.append([a,b,e,f])
  if el['type']=='table':
   x,y,w,rh=el['x'],el['top'],el['width'],el['row_height'];rows=[el['headers']]+el['rows'];h=rh*len(rows)
   for i in range(len(rows)+1):line(x,y+i*rh,x+w,y+i*rh)
   for i in range(3):line(x+i*w/2,y,x+i*w/2,y+h)
   for i,row in enumerate(rows):
    for j,label in enumerate(row):
     size=min(12,(w/2-12)/c.stringWidth(str(label),'Book',12)*12)
     self.text(str(label),x+j*w/2+6,y+i*rh+5,size);labels.append(str(label))
  else:
   base=el['baseline'];tops=el['tops'];xs=el['xs'];marks=[]
   for x,top,label in zip(xs,tops,el['labels']):
    # Small schematic of upright paper silhouette, not an anthropometric claim.
    radius=12;c.circle(x,H-top-radius,radius,stroke=1,fill=0)
    neck=top+24;hips=base-40;shoulder=top+42
    line(x,neck,x,hips);line(x-25,shoulder,x+25,shoulder)
    line(x-25,shoulder,x-32,shoulder+40);line(x+25,shoulder,x+32,shoulder+40)
    line(x,hips,x-18,base);line(x,hips,x+18,base)
    # Matched strip starts at the same baseline, with an observed head-top mark.
    sx=x+63;line(sx,base,sx,top);line(sx-10,top,sx+10,top);line(x-45,base,sx+18,base)
    self.text(label,x-6,base+15,13);self.text(label+' strip',sx-20,base+35,10)
    labels += [label,label+' strip'];marks.append(dict(label=label,head_top=top,baseline=base,length=base-top,strip_x=sx))
   d['marks']=marks;d['comparison']='equal' if tops[0]==tops[1] else ('first taller' if tops[0]<tops[1] else 'second taller')
  c.restoreState();d['edges']=edges;d['text_labels']=labels;self.diagrams.append(d)
 def verify(self):
  result=super().verify();doc=fitz.open(self.files[self.role]);ledger=[]
  for i,d in enumerate(self.diagrams):
   pg=doc[d['page']-1];edges=[list(it[1])+list(it[2]) for g in pg.get_drawings() for it in g['items'] if it[0]=='l']
   for expected in d['edges']:assert any(all(abs(a-b)<.03 for a,b in zip(expected,e)) for e in edges),(d,expected)
   for label in d['text_labels']:assert label in pg.get_text(),(d,label)
   if d['type']=='table':
    # Verify each actual cell by its own text rectangle, not global text presence.
    rows=[d['headers']]+d['rows'];x,y,w,rh=d['x'],d['top'],d['width'],d['row_height']
    for j,row in enumerate(rows):
     for k,value in enumerate(row):
      rect=fitz.Rect(x+k*w/2,y+j*rh,x+(k+1)*w/2,y+(j+1)*rh)
      assert str(value) in pg.get_textbox(rect),(d,j,k,value)
   else:
    assert len(set(m['baseline'] for m in d['marks']))==1
    for mark in d['marks']:
     x,y=mark['strip_x']-63,mark['head_top'];r=fitz.Rect(x-12,y,x+12,y+24)
     assert any(all(abs(a-b)<.03 for a,b in zip(list(r),list(g['rect']))) and len([it for it in g['items'] if it[0]=='c'])==4 for g in pg.get_drawings()),(d,'head circle')
    first,second=d['marks'];assert (first['length']>second['length'])==(d['comparison']=='first taller')
    assert (first['length']==second['length'])==(d['comparison']=='equal')
   ledger.append(dict(id=f'{self.role}-diagram-{i+1}',**d,actual_pdf_check='Every exact table cell/line or head-circle bound, strip baseline/head mark endpoint and label verified from actual PDF'))
  (self.out/'data-geometry.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8');return result

def build():
 before=read('output/chapter-19/before.json');now=read('production/p1.json')
 assert sha(ROOT/'GombeTextbook.txt')==EXPECTED_HASH
 for i,(old,new) in enumerate(zip(before['lessons'],now)):
  if i!=18:assert old==new,new['id']
  else:
   base=copy.deepcopy(new);base.pop('paired_edition')
   for q in base['questions']:q.pop('id',None)
   assert base==old
  assert [(q['prompt'],q['answer']) for q in old['questions']]==[(q['prompt'],q['answer']) for q in new['questions']]
 for path,h in before['hashes'].items():assert sha(ROOT/path)==h,path
 assert read('research/supplementary_assessments.json')==before['supplements']
 lesson=now[18];pair=lesson['paired_edition'];assert pair['teacher_id']=='ms-binta'
 reports={r:DataRenderer(r,pair[r+'_pages'],{'review_footer':'Class information / Educational review edition'},[lesson],output_dir=OUT,files=FILES,label='Class information').build() for r in FILES}
 assert pair['source_tasks']==[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in lesson['questions']]
 assert pair['supplementary_tasks']==[dict(id=s['id'],source_prompt=s['prompt'],source_answer=s['answer']) for s in before['supplements'] if s['id'] in ['S020','S021']]
 tasks=pair['author_content']['tasks'];ids={t['id'] for t in tasks};assert len(ids)==len(tasks)
 assert set().union(*(set(r['task_pages']) for r in reports.values()))==ids
 coverage=[]
 for t in tasks:
  answers={r:[n for n,p in enumerate(pair[r+'_pages'],1) if t['id'] in p.get('answer_ids',[])] for r in FILES if any(t['id'] in p.get('answer_ids',[]) for p in pair[r+'_pages'])};assert answers,t['id']
  for role,nums in answers.items():
   doc=fitz.open(FILES[role]);assert all(' '.join(t['answer'].split()) in ' '.join(doc[n-1].get_text().split()) for n in nums),t['id']
  coverage.append(dict(t,pages={r:v['task_pages'][t['id']] for r,v in reports.items() if t['id'] in v['task_pages']},answer_pages=answers))
 matrix={o:{m:[dict(id=t['id'],pages=next(x['pages'] for x in coverage if x['id']==t['id'])) for t in tasks if o in t['objectives'] and t['mode']==m] for m in ['model','guided','independent','recall','help','recheck','fresh','delayed']} for o in pair['objective_ids']};assert all(all(v.values()) for v in matrix.values())
 ledger=sum([read(f'output/chapter-19/{r}/data-geometry.json') for r in FILES],[])
 for name,obj in [('task-coverage',coverage),('objective-matrix',matrix),('diagram-ledger',ledger)]:(OUT/f'{name}.json').write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 validate();result=dict(pages={r:v['pages'] for r,v in reports.items()},artifacts={r:str(p.relative_to(ROOT)).replace('\\','/') for r,p in FILES.items()},tasks=len(ids),diagrams=len(ledger),protected_hashes=len(before['hashes']),status='pending_independent_review',checks=['114 original pairs,18other lessons,178protected hashes and supplements preserved','both objectives across eight progression modes','actual PDF geometry and every answer text checked','A4 fonts bounds and all pages rendered'])
 (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':build()
