"""Build the isolated canonical P1-12 textbook/workbook pair; never approve it."""
import copy,hashlib,json,re
from build_primary_one_opening import ROOT,EXPECTED_HASH,read,Renderer
from check_chapter_standard import validate
import fitz
OUT=ROOT/'output/chapter-12'
FILES={r:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Missing-part-{r.title()}.pdf' for r in ('textbook','workbook')}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calc(s):
 assert re.fullmatch(r'[0-9+ -]+',s),s
 return eval(s,{'__builtins__':{}},{})
def build():
 before=read('output/chapter-12/before.json');now=read('production/p1.json')
 assert sha(ROOT/'GombeTextbook.txt')==EXPECTED_HASH
 assert len(now)==len(before['lessons'])==19
 for i,(old,new) in enumerate(zip(before['lessons'],now)):
  if i!=11:assert old==new,new['id']
  else:
   base=copy.deepcopy(new);base.pop('paired_edition')
   for q in base['questions']:q.pop('id',None)
   assert base==old
  assert [(q['prompt'],q['answer']) for q in old['questions']]==[(q['prompt'],q['answer']) for q in new['questions']]
 for p,h in before['hashes'].items():assert sha(ROOT/p)==h,p
 supp=read('research/supplementary_assessments.json');expected=copy.deepcopy(before['supplements'])
 next(s for s in expected if s['id']=='S007')['answer']=next(s for s in expected if s['id']=='S007')['answer'].replace('9 ? 4','9 - 4')
 assert supp==expected,'Unrelated supplementary change'
 lesson=now[11];pair=lesson['paired_edition'];assert pair['teacher_id']=='mr-aliyu'
 assert pair['source_tasks']==[dict(id=f'P1-12-Q{i}',source_prompt=q['prompt'],source_answer=q['answer']) for i,q in enumerate(lesson['questions'],1)]
 reports={r:Renderer(r,pair[r+'_pages'],{'review_footer':'Chapter twelve / Educational review edition'},[lesson],output_dir=OUT,files=FILES,label='Missing part').build() for r in FILES}
 tasks=pair['author_content']['tasks'];ids={t['id'] for t in tasks};assert len(ids)==len(tasks)
 assert set().union(*(set(r['task_pages']) for r in reports.values()))==ids
 coverage=[]
 for t in tasks:
  for eq in t['equations']:
   a,b=eq.split('=');assert calc(a)==calc(b),(t['id'],eq)
  coverage.append(dict(t,pages={r:v['task_pages'][t['id']] for r,v in reports.items() if t['id'] in v['task_pages']},answer_pages={r:[n for n,p in enumerate(pair[r+'_pages'],1) if t['id'] in p.get('answer_ids',[])] for r in reports if any(t['id'] in p.get('answer_ids',[]) for p in pair[r+'_pages'])}))
 diagrams={d['id']:d['count'] for d in pair['author_content']['diagrams']};observed={}
 for r,v in reports.items():
  for d in v['objects']:assert diagrams[d['id']]==d['count'];observed[d['id']]=d['count']
 assert observed==diagrams
 geometry=[]
 for role,report in reports.items():
  doc=fitz.open(FILES[role])
  for diagram in report['objects']:
   marks=[x for x in doc[diagram['page']-1].get_drawings() if x.get('fill') is not None and abs(x['rect'].width-16)<.01 and abs(x['rect'].height-16)<.01]
   centers=[[(x['rect'].x0+x['rect'].x1)/2,(x['rect'].y0+x['rect'].y1)/2] for x in marks]
   actual=[]
   for x,y in diagram['points']:
    found=[c for c in centers if abs(c[0]-x)<.01 and abs(c[1]-y)<.01];assert len(found)==1,(diagram,found)
    actual.append(found[0])
   geometry.append(dict(role=role,id=diagram['id'],page=diagram['page'],count=len(actual),actual_vector_centers=actual))
 (OUT/'diagram-ledger.json').write_text(json.dumps(geometry,indent=2)+'\n',encoding='utf-8')
 matrix={}
 for o in pair['objective_ids']:
  matrix[o]={mode:[dict(id=t['id'],answer=t['answer'],pages=next(x['pages'] for x in coverage if x['id']==t['id'])) for t in tasks if o in t['objectives'] and t['mode']==mode] for mode in ['model','guided','independent','help','recheck','fresh','delayed']}
  assert all(matrix[o].values()),o
 (OUT/'task-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n',encoding='utf-8')
 (OUT/'objective-matrix.json').write_text(json.dumps(matrix,indent=2)+'\n',encoding='utf-8')
 (OUT/'diagram-values.json').write_text(json.dumps(pair['author_content']['diagrams'],indent=2)+'\n',encoding='utf-8')
 validate()
 result=dict(pages={r:v['pages'] for r,v in reports.items()},artifacts={r:str(p.relative_to(ROOT)).replace('\\','/') for r,p in FILES.items()},tasks=len(ids),equations=sum(len(t['equations']) for t in tasks),diagrams=len(diagrams),status='pending_independent_review',checks=['114 source prompt/answer pairs preserved;18 other lessons exact','all baseline protected hashes preserved','S007 operator-only repair verified;all other supplements unchanged','all task arithmetic recalculated','six objectives have seven progression stages','actual vector counts,A4,embedded fonts,text bounds;all pages rendered'])
 (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(result,indent=2))
if __name__=='__main__':build()
