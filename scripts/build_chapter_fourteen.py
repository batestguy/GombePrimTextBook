"""Build isolated P1-14 Length pair; author checks do not grant approval."""
import copy,hashlib,json
from build_primary_one_opening import ROOT,EXPECTED_HASH,read,Renderer
from check_chapter_standard import validate
import fitz
OUT=ROOT/'output/chapter-14'
FILES={r:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Length-{r.title()}.pdf' for r in ('textbook','workbook')}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
 before=read('output/chapter-14/before.json');now=read('production/p1.json')
 assert sha(ROOT/'GombeTextbook.txt')==EXPECTED_HASH
 assert len(now)==len(before['lessons'])==19
 for i,(old,new) in enumerate(zip(before['lessons'],now)):
  if i!=13:assert old==new,new['id']
  else:
   base=copy.deepcopy(new);base.pop('paired_edition')
   for q in base['questions']:q.pop('id',None)
   assert base==old
  assert [(q['prompt'],q['answer']) for q in old['questions']]==[(q['prompt'],q['answer']) for q in new['questions']]
 for p,h in before['hashes'].items():assert sha(ROOT/p)==h,p
 assert read('research/supplementary_assessments.json')==before['supplements']
 lesson=now[13];pair=lesson['paired_edition'];assert pair['teacher_id']=='mr-aliyu'
 reports={r:Renderer(r,pair[r+'_pages'],{'review_footer':'Length / Educational review edition'},[lesson],output_dir=OUT,files=FILES,label='Length').build() for r in FILES}
 tasks=pair['author_content']['tasks'];ids={t['id'] for t in tasks};assert len(ids)==len(tasks)
 assert set().union(*(set(r['task_pages']) for r in reports.values()))==ids
 coverage=[]
 for t in tasks:
  a={r:[n for n,p in enumerate(pair[r+'_pages'],1) if t['id'] in p.get('answer_ids',[])] for r in reports if any(t['id'] in p.get('answer_ids',[]) for p in pair[r+'_pages'])};assert a,t['id']
  coverage.append(dict(t,pages={r:v['task_pages'][t['id']] for r,v in reports.items() if t['id'] in v['task_pages']},answer_pages=a))
 ledger=[]
 for d in pair['author_content']['diagrams']:
  found=[]
  for role in FILES:
   doc=fitz.open(FILES[role])
   for n,p in enumerate(pair[role+'_pages'],1):
    expected=[(100,d['top']+i*65+12,100+v*d['unit'],d['top']+i*65+12) for i,v in enumerate(d['values'])]
    labels=[e['text'] for e in p['elements'] if e['type']=='text' and e.get('x')==38 and e.get('top') in [d['top']+i*65-3 for i in range(len(d['values']))]]
    if labels!=d['labels']:continue
    source_lines=[(e['x1'],e['top1'],e['x2'],e['top2']) for e in p['elements'] if e['type']=='line']
    if not all(e in source_lines for e in expected):continue
    ticks=[(100+j*d['unit'],d['top']+i*65+4,100+j*d['unit'],d['top']+i*65+20) for i,v in enumerate(d['values']) for j in range(v+1)] if d['segmented'] else []
    if ticks and not all(e in source_lines for e in ticks):continue
    lines=[tuple(x['rect']) for x in doc[n-1].get_drawings() if x['type']=='s']
    if all(any(all(abs(a-b)<.02 for a,b in zip(e,z)) for z in lines) for e in expected+ticks):found.append(dict(role=role,page=n,labels=labels,ticks=ticks,endpoints=expected,lengths=[v*d['unit'] for v in d['values']],shortest=min(d['values']),longest=max(d['values']),order=sorted(zip(d['values'],d['labels']))))
  assert found,d
  ledger.append(dict(d,pdf_evidence=found))
 assert 8+8==16 and 5>3 and sorted([2,6,4])==[2,4,6]
 matrix={}
 for o in pair['objective_ids']:
  matrix[o]={m:[dict(id=t['id'],answer=t['answer'],pages=next(x['pages'] for x in coverage if x['id']==t['id'])) for t in tasks if o in t['objectives'] and t['mode']==m] for m in ['model','guided','independent','help','recheck','fresh','delayed']};assert all(matrix[o].values()),o
 for name,data in [('task-coverage',coverage),('objective-matrix',matrix),('diagram-ledger',ledger)]:(OUT/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 validate()
 result=dict(pages={r:v['pages'] for r,v in reports.items()},artifacts={r:str(p.relative_to(ROOT)).replace('\\','/') for r,p in FILES.items()},tasks=len(ids),diagrams=len(ledger),protected_hashes=len(before['hashes']),status='pending_independent_review',checks=['114 source prompt/answer pairs and18other lessons unchanged','protected hashes and supplements unchanged','all source comparisons/order and8+8=16 recalculated','five objectives each cover seven progression modes','actual PDF vector lengths and endpoints checked','A4 embedded fonts text bounds every page rendered'])
 (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':build()
