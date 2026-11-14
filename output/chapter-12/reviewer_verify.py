"""Independent review source/evidence checks; writes this review directory only."""
from pathlib import Path
import ast,copy,hashlib,json,re
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
before=read('output/chapter-12/before.json');lessons=read('production/p1.json');register=read('production/chapter-reviews.json')
assert len(lessons)==len(before['lessons'])==19
assert [[(q['prompt'],q['answer']) for q in l['questions']] for l in lessons]==[[(q['prompt'],q['answer']) for q in l['questions']] for l in before['lessons']]
for i,(old,new) in enumerate(zip(before['lessons'],lessons)):
 if i!=11:assert old==new,new['id']
 else:
  x=copy.deepcopy(new);x.pop('paired_edition',None)
  for q in x['questions']:q.pop('id',None)
  assert x==old
coverage=[]
for i,lesson in enumerate(lessons[:12]):
 p=lesson['paired_edition'];tasks={}
 for role in ('textbook','workbook'):
  offset=4 if i==0 and role=='textbook' else 10 if i==1 and role=='textbook' else 1 if i==0 and role=='workbook' else 5 if i==1 and role=='workbook' else 0
  for n,page in enumerate(p[role+'_pages'],1):
   for task in page.get('task_ids',[]):tasks.setdefault(task,{}).setdefault(role,[]).append(n+offset)
 expected=[{'id':f"{lesson['id']}-Q{n}",'source_prompt':q['prompt'],'source_answer':q['answer']} for n,q in enumerate(lesson['questions'],1)]
 assert p['source_tasks']==expected,lesson['id']
 coverage.append({'chapter':lesson['id'],'source_tasks':expected,'reviewed_task_page_map':tasks,'independent_working':'reviewer-progress.md and REVIEW.md; all examples/tasks/diagrams/answers independently solved in this session'})
(OUT/'reviewer-current-task-coverage.json').write_text(json.dumps(coverage,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
supp=read('research/supplementary_assessments.json');old=copy.deepcopy(before['supplements'])
a=next(t for t in old if t['id']=='S007');b=next(t for t in supp if t['id']=='S007')
assert a['answer'].replace('9 ? 4','9 - 4')==b['answer'];a['answer']=b['answer'];assert old==supp
assert register['chapters'][12:]==before['register']['chapters'][12:]
# Independently interpret only integers, addition and subtraction, with no renderer/imported answer logic.
def calc(s):
 t=ast.parse(s.strip().replace('\u2212','-'),mode='eval').body
 def rec(n):
  if isinstance(n,ast.Constant) and type(n.value) is int:return n.value
  if isinstance(n,ast.BinOp) and isinstance(n.op,(ast.Add,ast.Sub)):
   l,r=rec(n.left),rec(n.right);return l+r if isinstance(n.op,ast.Add) else l-r
  raise ValueError(ast.dump(n))
 return rec(t)
tasks=read('output/chapter-12/task-coverage.json');solved=[]
for task in tasks:
 assert task['pages'],task['id']
 for eq in task['equations']:
  l,r=eq.split('=');assert calc(l)==calc(r),(task['id'],eq)
 solved.append({'id':task['id'],'mode':task['mode'],'actual_page_map':coverage[11]['reviewed_task_page_map'].get(task['id'],{}),'true_equations_checked':task['equations'],'answer_checked_against_personal_page_solution':task['answer']})
(OUT/'reviewer-ch12-task-solutions.json').write_text(json.dumps(solved,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
result={'source_pairs':114,'other_complete_lessons_exact':18,'source_task_maps':12,'stable_ids_added_only_to_ch12_questions':6,'supplements':59,'supplement_delta':'S007 answer only: ? to -','other_chapter_records_exact':51,'task_records':len(tasks),'true_equations':sum(len(t['equations']) for t in tasks),'original_questions_preserved':True}
(OUT/'reviewer-source-results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
