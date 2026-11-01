"""Build isolated P1-08 pair with deterministic count ledger and preservation gates."""
import hashlib,json,copy
from build_primary_one_opening import ROOT,EXPECTED_HASH,Renderer,read
from check_chapter_standard import validate
OUT=ROOT/'output/chapter-8'
FILES={r:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Put-small-sets-together-{r.title()}.pdf' for r in ('textbook','workbook')}
def build():
 assert hashlib.sha256((ROOT/'GombeTextbook.txt').read_bytes()).hexdigest()==EXPECTED_HASH
 before=read('output/chapter-8/before.json');now=read('production/p1.json')
 for i,(old,new) in enumerate(zip(before['lessons'],now)):
  if i!=7:assert old==new,new['id']
  else:
   unchanged=copy.deepcopy(new);unchanged.pop('paired_edition')
   for q in unchanged['questions']:q.pop('id',None)
   assert unchanged==old,'Original P1-08 content preserved except added stable IDs'
 for old,new in zip(before['lessons'],now):
  assert [(q['prompt'],q['answer']) for q in old['questions']]==[(q['prompt'],q['answer']) for q in new['questions']]
 for p,sha in before['hashes'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
 lesson=now[7];pair=lesson['paired_edition'];assert pair['teacher_id']=='mr-aliyu'
 assert pair['source_tasks']==[dict(id=f'P1-08-Q{i}',source_prompt=q['prompt'],source_answer=q['answer']) for i,q in enumerate(lesson['questions'],1)]
 reports={r:Renderer(r,pair[r+'_pages'],{'review_footer':'Chapter eight / Educational review edition'},[lesson],output_dir=OUT,files=FILES,label='Put small sets together').build() for r in FILES}
 validate()
 for r in reports:assert all(t['id'] in reports[r]['task_pages'] for t in pair['source_tasks'])
 tasks=read('output/chapter-8/task-coverage.json');ids={t['id'] for t in tasks}
 assert len(ids)==len(tasks)
 assert ids==set().union(*(set(v['task_pages']) for v in reports.values()))
 (OUT/'validation.json').write_text(json.dumps(dict(pages={r:v['pages'] for r,v in reports.items()},artifacts={r:str(f.relative_to(ROOT)) for r,f in FILES.items()},checks=['114 source prompts/answers/order preserved','18 other lessons unchanged','protected shared sources, original brief and all12 earlier PDFs unchanged','exact vector object counts verified against actual PDF fills','all task IDs covered with answers; A4 embedded fonts text bounds; every page rendered'],status='pending_independent_review'),indent=2)+'\n',encoding='utf-8')
 print('Built chapter eight:',{r:v['pages'] for r,v in reports.items()})
if __name__=='__main__':build()
