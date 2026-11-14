"""Build isolated canonical P1-11 pair; pending independent review."""
import copy,hashlib,json
from build_primary_one_opening import ROOT,EXPECTED_HASH,read,Renderer
from check_chapter_standard import validate
OUT=ROOT/'output/chapter-11'
FILES={r:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Take-away-{r.title()}.pdf' for r in ['textbook','workbook']}
def build():
 before=read('output/chapter-11/before.json');now=read('production/p1.json')
 assert hashlib.sha256((ROOT/'GombeTextbook.txt').read_bytes()).hexdigest()==EXPECTED_HASH
 assert len(now)==len(before['lessons'])==19
 for i,(old,new) in enumerate(zip(before['lessons'],now)):
  if i!=10:assert old==new,new['id']
  else:
   base=copy.deepcopy(new);base.pop('paired_edition')
   for q in base['questions']:q.pop('id',None)
   assert base==old
  assert [(q['prompt'],q['answer']) for q in old['questions']]==[(q['prompt'],q['answer']) for q in new['questions']]
 for s,sha in before['hashes'].items():assert hashlib.sha256((ROOT/s).read_bytes()).hexdigest()==sha,s
 lesson=now[10];pair=lesson['paired_edition'];assert pair['teacher_id']=='ms-binta'
 assert pair['source_tasks']==[dict(id=f'P1-11-Q{i}',source_prompt=q['prompt'],source_answer=q['answer']) for i,q in enumerate(lesson['questions'],1)]
 reports={r:Renderer(r,pair[r+'_pages'],{'review_footer':'Chapter eleven / Educational review edition'},[lesson],output_dir=OUT,files=FILES,label='Take away').build() for r in FILES}
 diagrams={d['id']:d['count'] for d in read('output/chapter-11/diagram-values.json')}
 observed={}
 for role,report in reports.items():
  assert all(q['id'] in report['task_pages'] for q in pair['source_tasks'])
  for d in report['objects']:
   assert d['count']==diagrams[d['id']],d
   observed[d['id']]=d['count']
 assert observed==diagrams
 tasks=read('output/chapter-11/task-coverage.json');ids={x['id'] for x in tasks}
 assert len(ids)==len(tasks) and ids==set().union(*(set(r['task_pages']) for r in reports.values()))
 for task in tasks:
  for a,b,c in task['calculations']:assert 0<=b<=a<=18 and a-b==c and c+b==a,task
 validate()
 (OUT/'validation.json').write_text(json.dumps(dict(pages={r:v['pages'] for r,v in reports.items()},artifacts={r:str(f.relative_to(ROOT)).replace('\\','/') for r,f in FILES.items()},checks=['114 original prompts/answers and 18 other lessons preserved','protected baseline hashes preserved','all deterministic dot counts verified against vector PDF marks','A4,embedded fonts,text bounds;all pages rendered',f'{len(ids)} tasks matched;all subtraction/addback arithmetic recalculated'],status='pending_independent_review'),indent=2)+'\n',encoding='utf-8')
 print('Built chapter eleven:',{r:v['pages'] for r,v in reports.items()})
if __name__=='__main__':build()
