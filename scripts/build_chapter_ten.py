"""Build isolated canonical P1-10 textbook/workbook pair; no approval implied."""
import copy,hashlib,json
from build_primary_one_opening import ROOT,EXPECTED_HASH,read
from build_chapter_five import BundleRenderer
from check_chapter_standard import validate
OUT=ROOT/'output/chapter-10'
FILES={r:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Add-tens-and-ones-{r.title()}.pdf' for r in ['textbook','workbook']}
def build():
 before=read('output/chapter-10/before.json');now=read('production/p1.json')
 assert hashlib.sha256((ROOT/'GombeTextbook.txt').read_bytes()).hexdigest()==EXPECTED_HASH
 assert len(now)==len(before['lessons'])==19
 for i,(old,new) in enumerate(zip(before['lessons'],now)):
  if i!=9:assert old==new,new['id']
  else:
   base=copy.deepcopy(new);base.pop('paired_edition')
   for q in base['questions']:q.pop('id',None)
   assert base==old
  assert [(q['prompt'],q['answer']) for q in old['questions']]==[(q['prompt'],q['answer']) for q in new['questions']]
 for s,sha in before['hashes'].items():assert hashlib.sha256((ROOT/s).read_bytes()).hexdigest()==sha,s
 lesson=now[9];pair=lesson['paired_edition'];assert pair['teacher_id']=='mr-aliyu'
 assert pair['source_tasks']==[dict(id=f'P1-10-Q{i}',source_prompt=q['prompt'],source_answer=q['answer']) for i,q in enumerate(lesson['questions'],1)]
 reports={r:BundleRenderer(r,pair[r+'_pages'],{'review_footer':'Chapter ten / Educational review edition'},[lesson],output_dir=OUT,files=FILES,label='Add tens and ones').build() for r in FILES}
 for role,report in reports.items():
  assert all(q['id'] in report['task_pages'] for q in pair['source_tasks'])
  ledger={x['id']:x for x in report['objects']}
  for page in pair[role+'_pages']:
   for el in page['elements']:
    if el['type']=='bundle':assert ledger[el['id']]['count']==10
  for d in read('output/chapter-10/diagram-values.json'):
   if any(k.startswith(d['id']+'-') for k in ledger):assert sum(v['count'] for k,v in ledger.items() if k.startswith(d['id']+'-'))==d['value'],d
 tasks=read('output/chapter-10/task-coverage.json');ids={x['id'] for x in tasks}
 assert len(ids)==len(tasks) and ids==set().union(*(set(r['task_pages']) for r in reports.values()))
 validate()
 (OUT/'validation.json').write_text(json.dumps(dict(pages={r:v['pages'] for r,v in reports.items()},artifacts={r:str(f.relative_to(ROOT)).replace('\\','/') for r,f in FILES.items()},checks=['114 original prompts/answers/order and18otherlessons preserved','16previousPDFs and protected source hashes preserved','each bundle ten actual vectors;each represented quantity recalculated','A4,embeddedfonts,textbounds,perpagevectorcounts;allpages rendered',f'{len(ids)}taskIDs matched to solved coverage'],status='pending_independent_review'),indent=2)+'\n',encoding='utf-8')
 print('Built chapter ten:',{r:v['pages'] for r,v in reports.items()})
if __name__=='__main__':build()
