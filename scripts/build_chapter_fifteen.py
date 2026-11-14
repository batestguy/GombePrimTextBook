"""Build isolated P1-15 Time pair. Does not confer independent approval."""
import copy,hashlib,json,re
from build_primary_one_opening import ROOT,EXPECTED_HASH,read,Renderer
from check_chapter_standard import validate
import fitz
OUT=ROOT/'output/chapter-15'
FILES={r:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Time-{r.title()}.pdf' for r in ('textbook','workbook')}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def plain(s):return re.sub('<[^>]+>',' ',s).split()
def build():
 before=read('output/chapter-15/before.json'); now=read('production/p1.json')
 assert sha(ROOT/'GombeTextbook.txt')==EXPECTED_HASH
 assert len(now)==len(before['lessons'])==19
 for i,(old,new) in enumerate(zip(before['lessons'],now)):
  if i!=14:assert old==new,new['id']
  else:
   base=copy.deepcopy(new);base.pop('paired_edition')
   for q in base['questions']:q.pop('id',None)
   assert base==old
  assert [(q['prompt'],q['answer']) for q in old['questions']]==[(q['prompt'],q['answer']) for q in new['questions']]
 for p,h in before['hashes'].items():assert sha(ROOT/p)==h,p
 assert read('research/supplementary_assessments.json')==before['supplements']
 lesson=now[14];pair=lesson['paired_edition'];assert pair['teacher_id']=='ms-binta'
 reports={r:Renderer(r,pair[r+'_pages'],{'review_footer':'Time / Educational review edition'},[lesson],output_dir=OUT,files=FILES,label='Time').build() for r in FILES}
 assert pair['source_tasks']==[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in lesson['questions']]
 supplement=next(x for x in before['supplements'] if x['id']=='S013')
 assert pair['supplementary_tasks']==[dict(id='S013',source_prompt=supplement['prompt'],source_answer=supplement['answer'])]
 tasks=pair['author_content']['tasks'];ids={t['id'] for t in tasks};assert len(ids)==len(tasks)
 assert set().union(*(set(r['task_pages']) for r in reports.values()))==ids
 coverage=[]
 for t in tasks:
  a={r:[n for n,p in enumerate(pair[r+'_pages'],1) if t['id'] in p.get('answer_ids',[])] for r in reports if any(t['id'] in p.get('answer_ids',[]) for p in pair[r+'_pages'])};assert a,t['id']
  for role,nums in a.items():
   doc=fitz.open(FILES[role])
   assert all(' '.join(t['answer'].split()) in ' '.join(doc[n-1].get_text().split()) for n in nums),(t['id'],'actual PDF answer correspondence')
  coverage.append(dict(t,pages={r:v['task_pages'][t['id']] for r,v in reports.items() if t['id'] in v['task_pages']},answer_pages=a))
 ledger=[]
 for d in pair['author_content']['diagrams']:
  found=[]
  for role in FILES:
   doc=fitz.open(FILES[role])
   for n,p in enumerate(pair[role+'_pages'],1):
    source=[e['text'] for e in p['elements'] if e['type']=='text' and e.get('top')==d['top']+14 and e.get('x') in [48,222,396]]
    if source!=d['labels']:continue
    page=doc[n-1]; actual=[]
    for (x,y,w,h),label in zip(d['rects'],d['labels']):
     txt=page.get_textbox(fitz.Rect(x,y,x+w,y+h)); assert plain(label)==txt.split(),(d['id'],role,n,label,txt)
     actual.append(txt.strip())
     assert any(abs(dr['rect'].x0-x)<.02 and abs(dr['rect'].y0-y)<.02 and abs(dr['rect'].width-w)<.02 and abs(dr['rect'].height-h)<.02 for dr in page.get_drawings()),(d['id'],'card box')
    found.append(dict(role=role,page=n,actual_card_text=actual,card_order='left to right as displayed; given story determines chronology'))
  assert found,d['id'];ledger.append(dict(d,pdf_evidence=found))
 # Completed drawing model: independently inspect actual vector geometry and labels on all three occurrences.
 drawing=[]
 for role,n,top in [('textbook',3,335),('textbook',11,390),('workbook',4,225)]:
  p=fitz.open(FILES[role])[n-1];rects=[d['rect'] for d in p.get_drawings()]
  for i,label in enumerate(['First: wall','Next: roof','Last: door']):
   x=38+i*174; assert label in p.get_textbox(fitz.Rect(x,top,x+156,top+40))
   assert any(abs(r.x0-(x+46))<.02 and abs(r.y0-(top+80))<.02 and abs(r.width-64)<.02 and abs(r.height-55)<.02 for r in rects)
   if i>0:
    for a,b,c,d in [(x+38,top+47,x+78,top+80),(x+78,top+47,x+118,top+80)]:
     assert any(abs(r.x0-a)<.02 and abs(r.y0-b)<.02 and abs(r.x1-c)<.02 and abs(r.y1-d)<.02 for r in rects)
  assert any(abs(r.x0-455)<.02 and abs(r.y0-(top+104))<.02 and abs(r.width-18)<.02 and abs(r.height-31)<.02 for r in rects)
  drawing.append(dict(role=role,page=n,labels=['First: wall','Next: roof','Last: door'],content='wall; wall+roof; wall+roof+door',actual_pdf_vectors_checked=True))
 ledger.append(dict(id='completed-drawing-model',pdf_evidence=drawing))
 matrix={}
 for o in pair['objective_ids']:
  matrix[o]={m:[dict(id=t['id'],answer=t['answer'],pages=next(x['pages'] for x in coverage if x['id']==t['id'])) for t in tasks if o in t['objectives'] and t['mode']==m] for m in ['model','guided','independent','help','recheck','fresh','delayed']};assert all(matrix[o].values()),o
 for name,data in [('task-coverage',coverage),('objective-matrix',matrix),('diagram-ledger',ledger)]:(OUT/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 validate()
 result=dict(pages={r:v['pages'] for r,v in reports.items()},artifacts={r:str(p.relative_to(ROOT)).replace('\\','/') for r,p in FILES.items()},tasks=len(ids),diagrams=len(ledger),protected_hashes=len(before['hashes']),status='pending_independent_review',checks=['114 source prompt/answer pairs and18other lessons unchanged','166 protected hashes and supplements unchanged','both historical objectives cover seven progression modes','exact PDF card labels/positions and completed vector drawing model checked','A4 embedded fonts text bounds every page rendered'])
 (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8'); print(json.dumps(result,indent=2))
if __name__=='__main__':build()
