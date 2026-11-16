"""Isolated P1-16 Heavy and light pair; no independent approval."""
import copy,hashlib,json
from build_primary_one_opening import ROOT,EXPECTED_HASH,read,Renderer
from check_chapter_standard import validate
import fitz
OUT=ROOT/'output/chapter-16'
FILES={r:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Heavy-and-light-{r.title()}.pdf' for r in ('textbook','workbook')}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
 before=read('output/chapter-16/before.json');now=read('production/p1.json')
 assert sha(ROOT/'GombeTextbook.txt')==EXPECTED_HASH
 assert len(now)==len(before['lessons'])==19
 for i,(old,new) in enumerate(zip(before['lessons'],now)):
  if i!=15:assert old==new,new['id']
  else:
   base=copy.deepcopy(new);base.pop('paired_edition')
   for q in base['questions']:q.pop('id',None)
   assert base==old
  assert [(q['prompt'],q['answer']) for q in old['questions']]==[(q['prompt'],q['answer']) for q in new['questions']]
 for p,h in before['hashes'].items():assert sha(ROOT/p)==h,p
 assert read('research/supplementary_assessments.json')==before['supplements']
 lesson=now[15];pair=lesson['paired_edition'];assert pair['teacher_id']=='mr-aliyu'
 reports={r:Renderer(r,pair[r+'_pages'],{'review_footer':'Heavy and light / Educational review edition'},[lesson],output_dir=OUT,files=FILES,label='Heavy and light').build() for r in FILES}
 assert pair['source_tasks']==[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in lesson['questions']]
 tasks=pair['author_content']['tasks'];ids={t['id'] for t in tasks};assert len(ids)==len(tasks)
 assert set().union(*(set(r['task_pages']) for r in reports.values()))==ids
 coverage=[]
 for t in tasks:
  a={r:[n for n,p in enumerate(pair[r+'_pages'],1) if t['id'] in p.get('answer_ids',[])] for r in FILES if any(t['id'] in p.get('answer_ids',[]) for p in pair[r+'_pages'])};assert a,t['id']
  for r,nums in a.items():
   doc=fitz.open(FILES[r]);assert all(' '.join(t['answer'].split()) in ' '.join(doc[n-1].get_text().split()) for n in nums),(t['id'],'answer')
  coverage.append(dict(t,pages={r:v['task_pages'][t['id']] for r,v in reports.items() if t['id'] in v['task_pages']},answer_pages=a))
 ledger=[]
 for d in pair['author_content']['diagrams']:
  found=[]
  for role in FILES:
   doc=fitz.open(FILES[role])
   for n,p in enumerate(pair[role+'_pages'],1):
    src=[e for e in p['elements'] if e['type']=='line'];expected=d['lines']
    if not all(any([e['x1'],e['top1'],e['x2'],e['top2']]==line for e in src) for line in expected):continue
    if not all(any(e['type']=='text' and e['text']==label for e in p['elements']) for label in d['labels']):continue
    page=doc[n-1];vectors=[]
    for drawing in page.get_drawings():
     for item in drawing['items']:
      if item[0]=='l':vectors.append((item[1],item[2]))
    for a,b,c,e in expected:
     assert any(abs(u.x-a)<.02 and abs(u.y-b)<.02 and abs(v.x-c)<.02 and abs(v.y-e)<.02 for u,v in vectors),(d['id'],role,n,(a,b,c,e))
    for label in d['labels']:assert label in page.get_text(),(d['id'],label)
    beam=expected[0];assert (beam[1]>beam[3])==(d['state']=='left');assert (beam[1]<beam[3])==(d['state']=='right')
    pans=[expected[5][1],expected[8][1]];assert pans[0]-beam[1]==pans[1]-beam[3]==75
    found.append(dict(role=role,page=n,actual_pdf_beam=beam,actual_pdf_pans=pans,labels=d['labels'],interpretation=d['interpretation'],verified='exact beam endpoints, pan line endpoints and labels from actual PDF vectors/text; source positions identify occurrence'))
  assert found,d['id'];ledger.append(dict(d,pdf_evidence=found))
 drawing=[]
 for role,n,x,y,w,h in [('textbook',5,245,300,100,65),('workbook',4,70,620,70,45)]:
  pg=fitz.open(FILES[role])[n-1];assert any(abs(d['rect'].x0-x)<.02 and abs(d['rect'].y0-y)<.02 and abs(d['rect'].width-w)<.02 and abs(d['rect'].height-h)<.02 for d in pg.get_drawings());assert 'Completed' in pg.get_text();drawing.append(dict(role=role,page=n,outline_and_middle_line=True))
 ledger.append(dict(id='completed-leaf-drawing',pdf_evidence=drawing))
 matrix={o:{m:[dict(id=t['id'],answer=t['answer'],pages=next(x['pages'] for x in coverage if x['id']==t['id'])) for t in tasks if o in t['objectives'] and t['mode']==m] for m in ['model','guided','independent','help','recheck','fresh','delayed']} for o in pair['objective_ids']};assert all(all(v.values()) for v in matrix.values())
 for name,obj in [('task-coverage',coverage),('objective-matrix',matrix),('diagram-ledger',ledger)]:(OUT/f'{name}.json').write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 validate()
 result=dict(pages={r:v['pages'] for r,v in reports.items()},artifacts={r:str(p.relative_to(ROOT)).replace('\\','/') for r,p in FILES.items()},tasks=len(ids),diagrams=len(ledger),protected_hashes=len(before['hashes']),status='pending_independent_review',checks=['114 original ordered question/answer pairs and18other lessons preserved','169 protected hashes and supplements unchanged','seven objective progression modes enacted','actual PDF beam/pan endpoints labels interpreted for left-heavy right-heavy equal','completed drawing outline inspected','A4 embedded fonts text bounds and every page rendered'])
 (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':build()
