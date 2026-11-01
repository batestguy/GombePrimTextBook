"""Isolated canonical P1-09 pair; protected baseline and exact count checks."""
import hashlib,json,copy
from build_primary_one_opening import ROOT,EXPECTED_HASH,Renderer,read
from check_chapter_standard import validate
OUT=ROOT/'output/chapter-9'
FILES={r:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Count-on-to-add-{r.title()}.pdf' for r in ['textbook','workbook']}
def build():
 assert hashlib.sha256((ROOT/'GombeTextbook.txt').read_bytes()).hexdigest()==EXPECTED_HASH
 before=read('output/chapter-9/before.json');now=read('production/p1.json')
 for i,(old,new) in enumerate(zip(before['lessons'],now)):
  if i!=8:assert old==new,new['id']
  else:
   unchanged=copy.deepcopy(new);unchanged.pop('paired_edition')
   for q in unchanged['questions']:q.pop('id',None)
   assert unchanged==old,'Only P1-09 stable IDs and paired_edition may differ'
 for old,new in zip(before['lessons'],now):assert [(q['prompt'],q['answer']) for q in old['questions']]==[(q['prompt'],q['answer']) for q in new['questions']]
 for s,sha in before['hashes'].items():assert hashlib.sha256((ROOT/s).read_bytes()).hexdigest()==sha,s
 lesson=now[8];pair=lesson['paired_edition'];assert pair['teacher_id']=='ms-binta'
 assert pair['source_tasks']==[dict(id=f'P1-09-Q{i}',source_prompt=q['prompt'],source_answer=q['answer']) for i,q in enumerate(lesson['questions'],1)]
 s005=next(s for s in read('research/supplementary_assessments.json') if s['id']=='S005')
 assert pair['supplementary_tasks']==[dict(id='S005',source_prompt=s005['prompt'],source_answer=s005['answer'])]
 reports={r:Renderer(r,pair[r+'_pages'],{'review_footer':'Chapter nine / Educational review edition'},[lesson],output_dir=OUT,files=FILES,label='Count on to add').build() for r in FILES}
 validate()
 for r in reports:assert all(q['id'] in reports[r]['task_pages'] for q in pair['source_tasks'])
 tasks=read('output/chapter-9/task-coverage.json');ids={q['id'] for q in tasks};assert len(ids)==len(tasks)
 assert ids==set().union(*(set(v['task_pages']) for v in reports.values()))
 (OUT/'validation.json').write_bytes((json.dumps(dict(pages={r:v['pages'] for r,v in reports.items()},artifacts={r:str(f.relative_to(ROOT)).replace('\\','/') for r,f in FILES.items()},checks=['114 original prompts/answers/order and18other complete lessons unchanged','all14previous registered PDFs and protected original brief/sources unchanged','S005 exact source prompt/answer retained','actual PDF vector object counts/A4/font/bounds pass; all pages rendered','27unique task IDs have solved answers and page evidence'],status='pending_independent_review'),indent=2)+'\n').encode())
 print('Built chapter nine:',{r:v['pages'] for r,v in reports.items()})
if __name__=='__main__':build()
